

# FAST-LIO（ROS 2 版本）：快速鲁棒的 LiDAR-惯性里程计

> 源码位置：`source/FAST_LIO_ROS2-ros2/`
> 论文：*FAST-LIO2: Fast Direct LiDAR-inertial Odometry*
> 原版开发者：Wei Xu、Yixi Cai 等，香港大学 MARS 实验室
> ROS 2 移植维护者：[Ericsiii](https://github.com/Ericsii)
> 许可证：GPLv2

---

## 1. 项目简介

FAST-LIO（Fast LiDAR-Inertial Odometry）是一个计算高效、鲁棒的 **LiDAR-惯性里程计** 系统。它使用紧耦合迭代扩展卡尔曼滤波（iEKF）融合 LiDAR 特征点与 IMU 数据，能够在快速运动、高噪声或杂乱退化环境中实现稳健导航。

### 核心特点

- **快速迭代卡尔曼滤波**：专门为里程计优化的 iEKF，计算效率高
- **自动初始化**：在大多数静止环境下可自动完成初始化，无需手动干预
- **并行 KD-Tree 搜索**：降低计算复杂度
- **ikd-Tree 增量建图**：FAST-LIO2 引入的动态 KD-Tree，支持 100 Hz 以上 LiDAR 帧率
- **直接里程计（Scan-to-Map）**：直接在原始点云上进行匹配，可选择关闭特征提取，精度更高
- **多 LiDAR 支持**：无需特征提取即可支持旋转式（Velodyne、Ouster）和固态（Livox Avia/Horizon/MID-70/MID-360）等多种 LiDAR
- **外部 IMU 支持**：可接入机器人本体 IMU
- **ARM 平台兼容**：支持 Khadas VIM3、NVIDIA TX2、树莓派 4B 等嵌入式平台

---

## 2. 系统架构

```
LiDAR 点云 ──┐
             ├──> 紧耦合 iEKF ──> 位姿输出 ──> ikd-Tree 增量地图
IMU 数据   ──┘
```

### 管线流程

1. **前向传播**：利用 IMU 数据进行状态预测（位置、速度、姿态）
2. **后向传播 + 迭代更新**：将 LiDAR 点云与 ikd-Tree 地图做 scan-to-map 匹配，通过 iEKF 迭代修正状态
3. **增量建图**：将新帧点云插入 ikd-Tree，同时删除过远/过旧节点

---

## 3. 依赖项

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Ubuntu | ≥ 20.04 | 操作系统 |
| ROS 2 | ≥ Foxy（推荐 Humble） | 构建框架（colcon） |
| PCL | ≥ 1.8 | 点云处理（apt 默认版本即可） |
| Eigen | ≥ 3.3.4 | 线性代数（apt 默认版本即可） |
| livox_ros_driver2 | — | Livox LiDAR ROS 2 驱动 |

### livox_ros_driver2 安装

```bash
# 官方版本
git clone https://github.com/Livox-SDK/livox_ros_driver2.git

# 或移植者修改版（推荐使用标准单位）
git clone https://github.com/Ericsii/livox_ros_driver2.git -b feature/use-standard-unit
```

> **重要**：livox_ros_driver 必须在运行 FAST-LIO 前完成编译并 source，建议写入 `~/.bashrc`。

---

## 4. 构建方法

```bash
cd <ros2_ws>/src
git clone https://github.com/Ericsii/FAST_LIO_ROS2.git --recursive
cd ..
rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install
. ./install/setup.bash
```

> 如需使用自定义 PCL，设置 `export PCL_ROOT={CUSTOM_PCL_PATH}`。

---

## 5. 运行方法

### 5.1 实时 LiDAR 连接

```bash
# 启动 FAST-LIO（以 Avia 为例）
ros2 launch fast_lio mapping.launch.py config_file:=avia.yaml

# 在另一终端启动 Livox 驱动（以 MID-360 为例）
ros2 launch livox_ros_driver2 msg_MID360_launch.py
```

### 5.2 配置文件说明

`config/` 目录下提供多种 LiDAR 配置：

| 配置文件 | 对应 LiDAR |
|----------|-----------|
| `avia.yaml` | Livox Avia |
| `mid360.yaml` | Livox MID-360 |
| `horizon.yaml` | Livox Horizon |
| `velodyne.yaml` | Velodyne 系列 |
| `ouster.yaml` | Ouster 系列 |

关键配置参数：
- `lid_topic`：LiDAR 点云话题名
- `imu_topic`：IMU 话题名
- `extrinsic_T`：LiDAR 到 IMU 的平移外参
- `extrinsic_R`：LiDAR 到 IMU 的旋转外参（旋转矩阵格式）
- `extrinsic_est_en`：是否在线估计外参（已知外参时建议设为 `false`）
- `time_sync_en`：软件时间同步开关（仅在硬件同步不可用时开启）
- `pcd_save.pcd_save_en`：是否保存 PCD 地图文件

### 5.3 PCD 地图保存

1. 在配置文件中设置 `pcd_save.pcd_save_en: true` 和 `map_file_path`
2. 运行 FAST-LIO
3. 在 RQt 中调用 `Plugins → Services → Service Caller`，触发 `/map_save` 服务

---

## 6. 注意事项

- **IMU 与 LiDAR 必须时间同步**，这是系统精度的关键前提
- 警告 `"Failed to find match for field 'time'"` 表示点云缺少逐点时间戳，会影响运动补偿
- Livox LiDAR 仅支持 `livox_lidar_msg.launch` 采集的数据（`CustomMsg` 格式含逐点时间戳）
- ROS 1 bag 文件需转换为 ROS 2 格式后才能播放

---

## 7. 与当前项目的关系

FAST-LIO（ROS 2 版）是 LIO 部署的**核心候选方案**：

- **直接可用**：ROS 2 + colcon 构建，与 Go2 部署包中 `unitree_slam` 的 FAST-LIO 风格建图同源
- **MID-360 原生支持**：Go2 默认搭载的 Livox MID-360 可直接对接
- **PCD 输出**：`save_pcd` 功能可直接产出 LiDAR 参考地图，对应项目 M5（LiDAR 裁判）模块
- **与宇树部署包的区别**：部署包内的 `unitree_slam` 是闭源封装版，FAST-LIO ROS 2 是开源独立版，可独立运行验证

### 相关扩展项目

| 项目 | 说明 |
|------|------|
| [ikd-Tree](https://github.com/hku-mars/ikd-Tree) | 动态 KD-Tree，FAST-LIO2 核心数据结构 |
| [R2LIVE](https://github.com/hku-mars/r2live) | LiDAR-惯性-视觉融合，以 FAST-LIO 为前端 |
| [LI_Init](https://github.com/hku-mars/LiDAR_IMU_Init) | LiDAR-IMU 外参初始化与同步工具 |
| [FAST-LIO-LOCALIZATION](https://github.com/HViktorTsoi/FAST_LIO_LOCALIZATION) | FAST-LIO + 重定位模块 |
| [IKFoM](https://github.com/hku-mars/IKFoM) | 流形上快速高精度卡尔曼滤波工具箱 |
