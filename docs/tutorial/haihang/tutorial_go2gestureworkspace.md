# Go2 手势控制系统教程

## 项目概述

本项目为 **Unitree Go2 机器狗的 MediaPipe 手势控制系统**。使用 **Intel RealSense D435i** 深度相机和 **Google MediaPipe** 手部追踪技术，实时识别手势并转换为机器人指令（行走、站立、跳舞、打招呼等）。系统通过 **localhost UDP 协议** 通信，**不需要 ROS2**。

**安全设计**: 默认启动为 **dry-run 模式**（仅打印到控制台，不实际控制机器人），必须显式传入 `--enable-robot` 标志才能激活真实控制。

---

## 文件结构

```
go2gestureworkspace/
├── CMakeLists.txt              # C++ 构建配置（CMake 3.16+, C++17）
├── README.md                   # 项目文档
├── include/
│   └── gesture_protocol.hpp    # C++ 头文件：手势枚举、消息结构、解析声明
├── src/
│   ├── main.cpp                # C++ 主程序：UDP 监听、状态机、安全控制器
│   └── gesture_protocol.cpp    # C++ 实现：UDP 消息解析器
├── perception/
│   └── hand_gesture_node.py    # Python：MediaPipe 手部追踪、手势分类、UDP 发送
├── scripts/
│   ├── setup_python.sh         # 创建 .venv，安装 MediaPipe ARM64 wheel
│   └── send_test_gesture.py    # 测试脚本：发送模拟手势 UDP 消息
├── build/                      # 预编译产物（aarch64, Release, GCC 9）
│   └── go2_gesture_controller  # 编译后的二进制（~3.7 MB）
└── .venv/                      # Python 3.8 虚拟环境
```

---

## 系统架构

```
+--------------------------+       UDP 127.0.0.1:44555       +---------------------------+
|  Python 感知节点          |  ==========================>    |  C++ 安全控制器            |
|                          |  "GESTURE OPEN_PALM 0.95 ts"    |                            |
|  RealSense D435i         |                                 |  状态机:                   |
|  (/dev/video4)           |                                 |  - 稳定性滤波              |
|       |                  |                                 |  - 心跳超时                |
|       v                  |                                 |  - 离散冷却                |
|  MediaPipe Hands         |                                 |  - 运动刷新                |
|       |                  |                                 |       |                    |
|       v                  |                                 |       v                    |
|  手势分类                 |                                 |  SportExecutor             |
|  (基于角度的手指          |                                 |  - Dry-run 或              |
|   伸展分析)               |                                 |  - Unitree SDK2            |
|       |                  |                                 |    SportClient             |
|       v                  |                                 |       |                    |
|  时序滤波                 |                                 |       v                    |
|  (多数投票, 5帧)          |                                 |  Go2 机器人动作            |
|       |                  |                                 |  (移动、站立、跳舞、       |
|       v                  |                                 |   抓取、打招呼等)          |
|  UDP 发送器               |                                 |                            |
+--------------------------+                                 +---------------------------+
```

**数据流**:
1. Python 从 RealSense D435i 读取摄像头帧
2. MediaPipe 检测手部关键点（21 个点）
3. 自定义角度分类器确定手势类型
4. 5 帧多数投票滤波平滑预测
5. 分类后的手势作为 UDP 文本消息发送到 localhost
6. C++ 控制器接收 UDP 消息，应用稳定性时间规则
7. 确认延迟后，命令分发到 Unitree SDK2 SportClient

---

## 支持的手势

| 手势 | 触发条件 | 动作 | 确认时间 |
|------|----------|------|----------|
| **NoHand** | 无手检测 | 立即停止机器人 | 即时 |
| **OpenPalm** | 5 指张开 | 抓取（Scrape） | 1.5 秒 |
| **ClosedFist** | 握拳 | 站立/坐下 | 1.5 秒 |
| **PointingUp** | 食指伸出 | 前进（0.18 m/s） | 350 ms（持续刷新） |
| **ThumbUp** | 拇指向上 | 打招呼（Hello） | 350 ms |
| **ThumbDown** | 拇指向下 | 跳舞（Dance1） | 350 ms |
| **Victory** | 食指+中指（V字） | 伸展（Stretch） | 350 ms |

**安全机制**:
- 动作手势（OpenPalm、ClosedFist）需要持续 1.5 秒保持，防止误触发
- 离散动作间有 2.5 秒冷却时间
- 500ms 心跳超时：无 UDP 消息时自动停止机器人
- NoHand 立即停止

---

## 部署与构建

### 硬件要求

- **平台**: ARM64 Linux (aarch64, Unitree Go2 机载计算机，Ubuntu, GCC 9, CMake 3.16)
- **摄像头**: Intel RealSense D435i，连接在 `/dev/video4`
- **Unitree SDK2**: 必须位于兄弟目录 `../unitree_sdk2`

### Python 环境设置

```bash
# 获取 ARM64 MediaPipe wheel（来自 PINTO0309/mediapipe-bin）
# SHA-256: d98b0cfcb060ba1870c8d33bc91eaf15f2b4913b3dc8a3dd15620a5ed8ec3b12
bash scripts/setup_python.sh /path/to/mediapipe-aarch64.whl
```

### C++ 构建

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j2
```

---

## 运行方法

### 自检（验证协议解析）

```bash
./build/go2_gesture_controller --self-test
```

### Dry-Run 模式（无机器人，仅控制台输出）

**终端 1** — 启动 C++ 控制器：
```bash
./build/go2_gesture_controller
```

**终端 2** — 启动 Python 感知节点：
```bash
./.venv/bin/python perception/hand_gesture_node.py
```

### 远程预览（SSH 模式）

```bash
./.venv/bin/python perception/hand_gesture_node.py --web-preview
# 然后在本地浏览器打开 http://ROBOT_IP:8080/
```

### 无摄像头测试

```bash
# 终端 1: 启动控制器
./build/go2_gesture_controller

# 终端 2: 发送模拟手势
.venv/bin/python scripts/send_test_gesture.py open_palm --seconds 3
.venv/bin/python scripts/send_test_gesture.py victory --seconds 2
```

### 机器人模式（真实控制）

```bash
# 仅在 dry-run 验证通过后，机器狗抬起或处于安全区域时
./build/go2_gesture_controller --enable-robot --interface eth0
# 将 eth0 替换为实际连接 Go2 的网络接口
```

---

## 依赖项

### C++ 依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| **Unitree SDK2** | 2.0.0 | 机器人通信（SportClient） |
| **CMake** | >= 3.16 | 构建系统 |
| **GCC** | >= 9 (C++17) | 编译 |
| **POSIX sockets** | 系统 | UDP 网络 |
| **pthreads** | 系统 | 线程 |

### Python 依赖

| 包 | 版本 | 用途 |
|---|---|---|
| **MediaPipe** | ARM64 社区 wheel (PINTO0309/mediapipe-bin) | 手部关键点检测 |
| **OpenCV** | 系统安装 | 摄像头捕获、图像处理 |
| **numpy** | 1.19.5 | 数值计算 |
| **protobuf** | 3.20.3 | MediaPipe 序列化 |
| **absl-py** | 1.4.0 | MediaPipe 依赖 |
| **attrs** | 21.4.0 | MediaPipe 依赖 |

### 硬件

- Unitree Go2 机器狗
- Intel RealSense D435i 摄像头（`/dev/video4`）
- ARM64 Linux 计算机（机载，Jetson 或树莓派级别）

---

## 注意事项

1. **无需 ROS2**: 系统使用原生 UDP 套接字，故意避免 ROS2 复杂性
2. **默认 Dry-Run**: 控制器**不会**移动机器人，除非显式提供 `--enable-robot --interface <iface>`
3. **紧急停止**: 张开手掌**不是**紧急停止（它触发抓取）。停止机器人方法：
   - 将手完全移出摄像头视野
   - 停止视觉进程（500ms 心跳超时触发）
   - 在控制器终端按 Ctrl+C
   - 使用物理遥控器（主要紧急停止方式）
4. **手势保持时间**: 张开手掌和握拳需要持续 1.5 秒，其他手势仅需 ~350ms
5. **MediaPipe Wheel**: 使用社区构建的 ARM64 wheel（非官方 x86 wheel），来自 `PINTO0309/mediapipe-bin`，SHA-256 哈希值需验证
6. **unitree_sdk2 位置**: CMakeLists.txt 期望 SDK 源码位于 `../unitree_sdk2`（工作区上一级目录），机器人上路径为 `/home/unitree/Documents/unitree_sdk2`，此工作区副本**不包含** SDK
7. **构建产物**: `build/` 包含预编译二进制（aarch64, Release, GCC 9），**无法**在 x86 Windows/Linux 运行，必须重新编译
8. **摄像头设备**: 默认为 `/dev/video4`，不同硬件配置可能需要调整（`--device`）
9. **网络接口**: 使用 `--enable-robot` 时，`--interface` 必须指定实际连接 Go2 的网络接口（如 eth0）
10. **仅单手**: MediaPipe 配置为 `max_num_hands=1`，仅追踪和分类第一只手
11. **预览限制**: `--preview` 需要本地图形显示（`$DISPLAY`），无头/SSH 会话使用 `--web-preview`（端口 8080 MJPEG 流）
12. **摄像头测试**: `--camera-test` 标志用于初始设置验证，读取 60 帧并报告 FPS，不发送命令

---

## 快速检查清单

- [ ] Unitree SDK2 已放置在 `../unitree_sdk2`
- [ ] MediaPipe ARM64 wheel 已下载并验证 SHA-256
- [ ] Python 虚拟环境已创建（`.venv`）
- [ ] C++ 程序已编译（`build/go2_gesture_controller`）
- [ ] RealSense D435i 摄像头已连接（`/dev/video4`）
- [ ] Dry-run 模式测试通过
- [ ] 网络接口已确认（`eth0` 或其他）
- [ ] 已理解紧急停止方法（非张开手掌）
- [ ] 物理遥控器已准备好作为紧急停止

---

## 相关资源

- **位置**: `G:\xjtlu\SURF\source\haihang\Docs\go2gestureworkspace`
- **MediaPipe ARM64**: https://github.com/PINTO0309/mediapipe-bin
- **Unitree SDK2**: 需从 Unitree 官方获取
