# ArUco 自动充电对接系统教程

## 项目概述

本项目为 **Unitree Go2 机器狗的 ArUco 标记自动充电（对接）系统**。程序 `aruco_recharge` 运行在 Go2 机载计算机上，通过摄像头检测充电站附近的 ArUco 标记（类似二维码的方形标记），计算相机与标记之间的相对位姿，引导机器狗自主对接充电器。

工作流程：
1. ArUco 标记（ID 0）物理安装在充电站附近
2. 机器狗摄像头检测标记
3. 系统计算标记相对于相机的 6-DOF 位姿（位置+姿态）
4. 机器狗导航对齐并对接充电器

---

## 文件结构

```
aruco_recharge_20250624/
├── aruco_recharge          # ARM64 预编译可执行文件（5.3 MB）
├── aruco_config.yaml       # 相机标定 + 物理几何参数配置
├── aruco_id0.png           # ArUco 标记图片（ID 0, 200x200 RGBA）
├── aruco_in_carema.csv     # 原始位姿数据日志（相机坐标系）
├── output.csv              # 处理后的位姿数据日志
├── readme-CN.md            # 中文说明（简略）
└── readme-EN.md            # 英文说明（简略）
```

---

## 部署与配置

### 硬件要求

- **机器狗**: Unitree Go2（机载 ARM 计算机，如树莓派或 Jetson）
- **操作系统**: Linux (GNU/Linux 3.7.0+, aarch64)
- **摄像头**: 连接到机载计算机的 USB 或 CSI 摄像头
- **ArUco 标记**: 打印 `aruco_id0.png` 并安装在充电站附近

### 配置参数（aruco_config.yaml）

```yaml
intrinsic_matrix:   # 相机内参矩阵（3x3，行优先）
  - 797.6243        # fx
  - 1.6166          # 偏斜
  - 649.3817        # cx
  - 0
  - 797.8026        # fy
  - 362.877         # cy
  - 0
  - 0
  - 1

distCoeffs:         # 镜头畸变系数 [k1, k2, p1, p2, k3]
  - -0.3890
  -  0.1762
  - -0.0453
  -  0.0031
  - -0.0015

net_addr: eth0      # 网络接口名称（用于 DDS 通信）

aruco_size: 0.1075  # ArUco 标记物理边长（米），107.5mm

aruco2center_dis: 0.70  # ArUco 标记到充电站中心距离（米）

camera2dog_dis: 0.35    # 相机到机器狗身体中心距离（米）

aruco2camera_dis: 0.35  # ArUco 标记到相机的初始估计距离（米）
```

**关键配置说明**：

| 参数 | 重要性 | 说明 |
|------|--------|------|
| `intrinsic_matrix` | 极高 | 相机内参标定，特定于相机镜头，更换相机必须重新标定 |
| `distCoeffs` | 极高 | 镜头畸变系数，k1=-0.389 表示广角/鱼眼镜头 |
| `aruco_size` | 极高 | 标记物理尺寸，必须精确测量，直接影响位姿估计精度 |
| `aruco2center_dis` | 高 | 标记到对接点的距离，影响对接对齐 |
| `camera2dog_dis` | 高 | 相机安装位置偏移，影响坐标变换 |
| `net_addr` | 中 | 网络接口，通常为 eth0 |

---

## 运行方法

### 启动服务

程序通过 **ROS 2 话题** 控制：

- **话题**: `/aruco_cmd`
- **消息类型**: `std_msgs/msg/String`
- **启动命令**: 发送字符串 `"aruco_start"`

```bash
# 启动 aruco_recharge 节点后，发送启动命令
ros2 topic pub --once /aruco_cmd std_msgs/msg/String "{data: 'aruco_start'}"
```

### 工作流程

1. 将 `aruco_recharge` 部署到 Go2 机载计算机
2. 打印并安装 ArUco 标记（ID 0）
3. 根据实际相机和安装情况修改 `aruco_config.yaml`
4. 运行 `aruco_recharge` 程序（作为 ROS 2 节点）
5. 通过 `/aruco_cmd` 话题发送启动命令
6. 机器狗自动检测标记、计算位姿、导航对接

---

## 数据日志

### aruco_in_carema.csv（6,266 行）

原始 ArUco 位姿数据（相机坐标系）：
- 格式: `id, x, y, z, roll, pitch, yaw`
- ID = 1 表示标记检测成功
- 位置 (x, y, z) 单位：米
- 姿态 (roll, pitch, yaw) 单位：弧度

### output.csv（5,403 行）

处理后的位姿数据（经过坐标变换，可能为机器人本体坐标系或世界坐标系）：
- 格式同上
- 行数少于原始数据，说明进行了滤波或剔除了不良检测

---

## 依赖项

| 依赖 | 说明 |
|------|------|
| **硬件** | Unitree Go2 机器狗（ARM aarch64 机载计算机） |
| **OS** | Linux (GNU/Linux 3.7.0+) |
| **中间件** | ROS 2（话题通信） |
| **库** | OpenCV（ArUco 检测和相机标定）、C/C++ 运行时、Unitree SDK |
| **摄像头** | 物理摄像头（USB 或 CSI） |

---

## 注意事项

1. **仅预编译二进制**: `aruco_recharge` 为闭源预编译文件，无源码，无法修改算法
2. **相机标定至关重要**: 内参和畸变系数特定于相机镜头，更换相机必须重新标定，否则位姿估计不准确，对接失败
3. **物理尺寸必须精确**: `aruco_size`、`aruco2center_dis`、`camera2dog_dis` 必须精确测量，误差直接导致对接错位
4. **ArUco 标记打印**: 图片仅 200x200 像素，需高质量打印在刚性平整表面，不可弯曲、皱褶或放在反光玻璃后
5. **光照条件**: ArUco 检测对光照敏感，弱光、强逆光或标记反光可能导致检测失败
6. **网络接口**: 配置为 eth0，如机器人网络使用不同接口名需更新
7. **官方文档**: readme 极简略（仅 2 行），完整使用说明、安全事项、API 详情和故障排除参见 **Unitree 文档中心 > Go2 SDK 开发指南 > 软件服务接口 > Aruco 充电服务接口**
8. **版本日期**: 文件夹名 `aruco_recharge_20250624` 表示 2025 年 6 月 24 日发布版本

---

## 快速检查清单

- [ ] ArUco 标记已打印并安装
- [ ] 相机已标定，`intrinsic_matrix` 和 `distCoeffs` 已更新
- [ ] `aruco_size` 已精确测量（单位：米）
- [ ] `aruco2center_dis` 和 `camera2dog_dis` 已测量
- [ ] `net_addr` 与实际网络接口匹配
- [ ] ROS 2 环境已配置
- [ ] 已阅读 Unitree 官方文档

---

## 相关资源

- **位置**: `G:\xjtlu\SURF\source\haihang\Docs\aruco_recharge_20250624`
- **官方文档**: Unitree Document Center > Go2 SDK Development Guide > Software Service Interface > Aruco Recharge Service Interface
