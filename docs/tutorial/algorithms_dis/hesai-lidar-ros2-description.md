# HesaiLidar ROS 2.0：禾赛激光雷达 ROS 驱动

> 源码位置：`source/HesaiLidar_ROS_2.0-master/`
> 基于：[HesaiLidar_SDK_2.0](https://github.com/HesaiTechnology/HesaiLidar_SDK_2.0)
> 开发者：禾赛科技（Hesai Technology）

---

## 1. 项目简介

HesaiLidar_ROS_2.0 是禾赛科技官方提供的 **ROS/ROS 2 激光雷达驱动**，负责监听 UDP 数据包、解析雷达原始数据并发布点云帧到 ROS 话题。它是连接禾赛 LiDAR 硬件与上层 SLAM/感知算法的桥梁层。

### 支持的 LiDAR 型号

| 系列 | 型号 |
|------|------|
| **Pandar** | Pandar40P、Pandar40M、Pandar64、Pandar128E3X、Pandar90E3X |
| **OT** | OT128、OT128_40 |
| **QT** | PandarQT、QT128C2X |
| **XT** | PandarXT、**PandarXT-16**、XT32M2X |
| **AT** | AT128E2X、AT128P、ATX |
| **FT** | FT120、FTX |
| **JT** | JT128、JT64P、JT16 |

> **PandarXT-16** 与 Go2 部署包中的 `xt16_driver` 对应，是 Go2 兼容模式下的雷达选择。

---

## 2. 核心功能

- **实时点云发布**：解析 UDP 数据包，输出标准 `sensor_msgs/PointCloud2` 格式
- **IMU 数据发布**：部分型号内置 IMU，驱动可同步发布
- **多数据源支持**：
  - `source_type=1`：实时雷达连接（UDP）
  - `source_type=2`：PCAP 文件回放
  - `source_type=3`：ROS bag 数据包回放
  - `source_type=4`：串口数据解析
- **多雷达融合**：配置文件支持同时驱动多台雷达，各自独立话题
- **GPU 加速（可选）**：通过 CUDA 加速点云解析
- **PTC 通信**：支持 TCP/TCP-SSL 的雷达参数控制通道
- **丢包检测**：内置 UDP 丢包监控工具
- **FOV 过滤**：支持按方位角范围过滤点云

---

## 3. 依赖项

| 依赖 | 说明 |
|------|------|
| Ubuntu | 16.04 / 18.04 / 20.04 / 22.04 / 24.04 |
| ROS / ROS 2 | Kinetic / Melodic / Noetic / Dashing / Foxy / Humble / Jazzy |
| Boost | `libboost-all-dev` |
| yaml-cpp | `libyaml-cpp-dev` |
| HesaiLidar_SDK_2.0 | 作为 git submodule 自动拉取 |

### 安装依赖

```bash
sudo apt-get update
sudo apt-get install libboost-all-dev
sudo apt-get install -y libyaml-cpp-dev
```

---

## 4. 构建方法

### ROS 1（catkin）

```bash
# 创建工作空间
mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src
git clone --recurse-submodules https://github.com/HesaiTechnology/HesaiLidar_ROS_2.0.git
cd ..
catkin_make
source devel/setup.bash
roslaunch hesai_ros_driver start.launch
```

### ROS 2（colcon）

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone --recurse-submodules https://github.com/HesaiTechnology/HesaiLidar_ROS_2.0.git
cd ..
colcon build --symlink-install
. install/local_setup.bash

# Dashing 版本
ros2 launch hesai_ros_driver dashing_start.py

# 其他 ROS 2 版本
ros2 launch hesai_ros_driver start.py
```

### CMake 编译选项

| 选项 | 默认 | 说明 |
|------|------|------|
| `WITH_PTCS_USE` | ON | 启用 PTC SSL 支持 |
| `FIND_CUDA` | OFF | 启用 CUDA GPU 加速 |
| `CMAKE_CUDA_ARCHITECTURES` | 61 | CUDA 计算能力（如 50/60/61/70/75/80/86/89/90） |

```bash
# 示例：关闭 PTC SSL + 启用 CUDA
colcon build --symlink-install --cmake-args -DWITH_PTCS_USE=OFF -DFIND_CUDA=ON
```

---

## 5. 配置文件详解

核心配置文件为 `config/config.yaml`，关键参数如下：

### 驱动层参数（`driver:`）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `use_gpu` | false | 是否使用 GPU 加速 |
| `source_type` | 1 | 数据源类型（1=实时/2=PCAP/3=ROS bag/4=串口） |
| `thread_num` | 4 | 解析线程数 |
| `use_timestamp_type` | 0 | 0=点云时间戳，1=接收时间戳 |
| `frame_frequency` | 0 | 点云发布频率 |
| `echo_mode_filter` | 0 | 回波模式过滤 |
| `transform_flag` | false | 是否应用坐标变换 |
| `fov_start` / `fov_end` | -1 | FOV 方位角范围（-1 为默认全范围） |
| `enable_packet_loss_tool` | true | 启用丢包检测 |
| `distance_correction_flag` | false | 光学中心距离修正 |
| `xt_spot_correction` | false | XT 系列光斑修正 |

### UDP 连接参数（`lidar_udp_type:`）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `device_ip_address` | 192.168.1.201 | 雷达 IP 地址 |
| `udp_port` | 2368 | UDP 目标端口 |
| `ptc_port` | 9347 | PTC 控制端口 |
| `correction_file_path` | — | 角度标定文件路径（推荐配置） |
| `firetimes_path` | — | 发射时间文件路径 |
| `standby_mode` | -1 | 待机模式（-1=无效/0=运行/1=待机） |
| `speed` | -1 | 转速设置（-1=无效） |
| `ptc_mode` | 0 | PTC 模式（0=TCP/1=TCP-SSL） |

### ROS 话题参数（`ros:`）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ros_frame_id` | hesai_lidar | TF 坐标系 ID |
| `ros_send_point_cloud_topic` | /lidar_points | 点云输出话题 |
| `ros_send_imu_topic` | /lidar_imu | IMU 输出话题 |
| `ros_recv_packet_topic` | /lidar_packets | 数据包接收话题 |
| `send_point_cloud_ros` | true | 是否发布点云 |
| `send_imu_ros` | true | 是否发布 IMU |

---

## 6. 多雷达配置

在 `config.yaml` 的 `lidar:` 列表中添加多个 `driver` 条目即可实现多雷达融合，每台雷达配置独立的 IP、端口和话题名：

```yaml
lidar:
  - driver:
      lidar_udp_type:
        device_ip_address: 192.168.1.201
        udp_port: 2368
      # ... 其他参数
    ros:
      ros_send_point_cloud_topic: /lidar_points
  - driver:
      lidar_udp_type:
        device_ip_address: 192.168.1.202
        udp_port: 2369
      # ... 其他参数
    ros:
      ros_send_point_cloud_topic: /lidar_points_2
```

---

## 7. 与当前项目的关系

HesaiLidar_ROS_2.0 驱动与 SURF 项目的关系：

- **XT-16 兼容模式**：Go2 部署包内含 `xt16_driver` 和 `PandarXT-16.csv` 仰角表，该驱动是其上游完整版本，提供更丰富的配置能力
- **数据桥接**：驱动输出的标准 `PointCloud2` 可直接对接 FAST-LIO / FAST-LIVO2 等 LIO 算法
- **多雷达场景**：若项目后续扩展多雷达配置，该驱动的多实例支持可直接复用
- **PCAP 回放**：支持离线回放雷达数据，方便算法调试和复现

### 与 Go2 部署包内驱动的对比

| 特性 | 部署包 `xt16_driver` | HesaiLidar_ROS_2.0 |
|------|---------------------|---------------------|
| LiDAR 支持 | 仅 XT-16 | 全系列 40+ 型号 |
| 构建系统 | 预编译 ELF | ROS/ROS 2 编译 |
| 数据源 | 仅实时 UDP | 实时/PCAP/ROS bag/串口 |
| GPU 加速 | 无 | 可选 CUDA |
| 多雷达 | 不支持 | 原生支持 |
| 配置灵活度 | 固定 | 完整 YAML 配置 |
