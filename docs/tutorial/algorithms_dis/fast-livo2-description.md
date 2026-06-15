# FAST-LIVO2：快速直接的 LiDAR-惯性-视觉里程计

> 源码位置：`source/FAST-LIVO2-main/`
> 论文：*FAST-LIVO2: Fast, Direct LiDAR-Inertial-Visual Odometry*（T-RO 2024）
> 开发者：Chunran Zheng（郑纯然），香港大学 MARS 实验室
> 许可证：GPLv2

---

## 1. 项目简介

FAST-LIVO2 是一个高效、精确的 **LiDAR-惯性-视觉三融合定位与建图系统**。它将激光雷达点云、IMU 惯性数据和相机图像紧密耦合，在严重退化环境（如长走廊、开阔场地、特征稀少场景）中实现实时三维重建和机器人定位。

### 核心特点

- **三传感器融合**：同时利用 LiDAR、IMU 和相机数据，相比纯 LiDAR-惯性系统（如 FAST-LIO2）在退化场景下更鲁棒
- **直接法（Direct Method）**：不依赖特征提取，直接在原始点云和像素灰度上进行优化，适用于多种 LiDAR 和相机型号
- **紧耦合架构**：LiDAR-惯性-视觉在前端即紧密融合，而非松耦合后处理
- **实时性能**：面向机载嵌入式平台的实时运行设计
- **资源受限平台支持**：有专门论文讨论在资源受限平台上的部署

### 相关论文

| 论文 | 说明 |
|------|------|
| FAST-LIVO2 (T-RO 2024) | 主算法，三融合直接法 LIO |
| FAST-LIVO2 on Resource-Constrained Platforms | 嵌入式端部署方案 |
| FAST-LIVO (IROS 2022) | 前代版本，稀疏直接法 |
| FAST-Calib | LiDAR-相机外参快速标定工具 |

---

## 2. 系统架构

```
LiDAR 点云 ──┐
IMU 数据   ──┼──> 紧耦合迭代 EKF ──> 位姿估计 + 增量建图
相机图像   ──┘
```

系统采用前向传播（IMU 预测）+ 后向传播（LiDAR/视觉观测修正）的迭代卡尔曼滤波框架，结合 ikd-Tree 增量地图进行高效近邻搜索。

---

## 3. 依赖项

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Ubuntu | 18.04 ~ 20.04 | 操作系统 |
| ROS | Melodic / Noetic | 构建框架（catkin） |
| PCL | ≥ 1.8 | 点云处理 |
| Eigen | ≥ 3.3.4 | 线性代数 |
| OpenCV | ≥ 4.2 | 图像处理 |
| Sophus | non-templated/double-only | 李群/李代数运算（需 checkout `a621ff`） |
| Vikit | rpg_vikit（xuankuzcr fork） | 相机模型、数学插值工具 |

---

## 4. 构建方法

```bash
# 安装 Sophus（注意版本）
git clone https://github.com/strasdat/Sophus.git
cd Sophus && git checkout a621ff
mkdir build && cd build && cmake .. && make
sudo make install

# 安装 Vikit（放入 catkin 工作空间）
cd ~/catkin_ws/src
git clone https://github.com/xuankuzcr/rpg_vikit.git

# 编译 FAST-LIVO2
cd ~/catkin_ws/src
git clone https://github.com/hku-mars/FAST-LIVO2
cd ..
catkin_make
source ~/catkin_ws/devel/setup.bash
```

---

## 5. 运行方法

```bash
# 启动建图节点（以 Avia LiDAR 为例）
roslaunch fast_livo mapping_avia.launch

# 播放数据集
rosbag play YOUR_DOWNLOADED.bag
```

支持的 LiDAR 配置文件包括：
- `config/avia.yaml` — Livox Avia
- `config/MARS_LVIG.yaml` — MARS LVIG 平台
- `config/NTU_VIRAL.yaml` — NTU VIRAL 数据集
- `config/HILTI22.yaml` — HILTI 2022 数据集

配套数据集可从 [FAST-LIVO2-Dataset](https://github.com/xuankuzcr/Global-LVBA) 下载。

---

## 6. 与当前项目的关系

FAST-LIVO2 作为 **LiDAR-惯性-视觉三融合** 的开源方案，与 SURF 项目的"廉价 RGB-D 建图 + LiDAR 裁判"架构有以下关联：

- **参考架构**：其紧耦合三融合管线可作为 LIO 系统部署的技术参考
- **退化场景鲁棒性**：在 LiDAR 退化场景下视觉通道可补偿，与项目"主动探索"目标互补
- **注意**：FAST-LIVO2 使用 **ROS 1（catkin）**，而宇树 Go2 部署包基于 **Cyclone DDS**，直接集成需要 DDS-ROS 桥接或独立部署

---

## 7. 硬件同步方案

项目开源了手持设备方案 [LIV_handhold](https://github.com/xuankuzcr/LIV_handhold)，包含：
- CAD 模型文件
- STM32 硬件同步源码
- 接线说明
- 传感器 ROS 驱动

外参标定推荐使用 [FAST-Calib](https://github.com/hku-mars/FAST-Calib)，可在一秒内完成 LiDAR-相机外参标定，输出参数直接填入 YAML 配置文件。
