# Go2 运动控制命令行工具教程

## 项目概述

本项目为 **Unitree Go2 机器狗的交互式命令行控制工具**。提供菜单驱动界面，允许用户实时触发 39 种不同的运动/动作，从基础操作（站立、坐下、停止）到高级甚至危险动作（前翻、后翻、倒立、跳跃）。工具通过 **Unitree SDK2**（v2.0.0）的网络接口与机器狗通信，使用 DDS（Data Distribution Service）协议。

**双语界面**: 所有提示、菜单项和错误信息均显示中英文。

---

## 文件结构

```
go2sportworkspace/
├── main.cpp              # 完整应用源码（289 行）
├── CMakeLists.txt        # CMake 构建配置（16 行）
└── build/                # 预编译产物目录
    ├── go2_stand_control # 编译后的 ELF 二进制（ARM aarch64）
    ├── CMakeCache.txt    # CMake 缓存
    ├── Makefile          # 生成的 Makefile
    └── unitree_sdk2/     # SDK 构建产物
```

---

## 支持的 39 种动作

### 基础动作

| ID | 动作 | 说明 |
|----|------|------|
| 1 | Damp | 阻尼模式（关节柔顺） |
| 2 | BalanceStand | 平衡站立 |
| 3 | StopMove | 停止移动 |
| 4 | StandUp | 站立 |
| 5 | StandDown | 趴下 |
| 6 | RecoveryStand | 恢复站立 |
| 7 | Sit | 坐下 |
| 8 | RiseSit | 从坐姿站起 |

### 参数化控制

| ID | 动作 | 参数 |
|----|------|------|
| 9 | Euler | roll/pitch/yaw 角度 |
| 10 | Move | vx/vy/yaw 速度 |
| 11 | SpeedLevel | 速度等级 |

### 手势/表演

| ID | 动作 | 说明 |
|----|------|------|
| 12 | Hello | 打招呼 |
| 13 | Stretch | 伸展 |
| 14 | Content | 满足表情 |
| 15 | Heart | 比心 |
| 16 | Scrape | 抓取 |
| 17 | Dance1 | 跳舞 1 |
| 18 | Dance2 | 跳舞 2 |

### 模式切换

| ID | 动作 | 说明 |
|----|------|------|
| 19 | SwitchJoystick | 切换手柄控制 |
| 20 | Pose | 姿态模式 |
| 21 | FreeWalk | 自由行走 |
| 22 | FreeBound | 自由跳跃 |
| 23 | FreeAvoid | 自由避障 |
| 24 | ClassicWalk | 经典步态 |
| 25 | WalkUpright | 直立行走 |
| 26 | CrossStep | 交叉步 |
| 27 | AutoRecoverSet | 自动恢复设置 |
| 28 | AutoRecoverGet | 自动恢复查询 |

### 高级/危险动作 ⚠️

| ID | 动作 | 风险 |
|----|------|------|
| 29 | FrontFlip | 前翻 [危险] |
| 30 | FrontJump | 前跳 [危险] |
| 31 | FrontPounce | 前扑 [危险] |
| 32 | LeftFlip | 左翻 [危险] |
| 33 | BackFlip | 后翻 [危险] |
| 34 | HandStand | 倒立 [危险] |
| 35 | FreeJump | 自由跳跃 [危险] |

### 步态模式

| ID | 动作 | 说明 |
|----|------|------|
| 36 | StaticWalk | 静态行走 |
| 37 | TrotRun | 小跑 |
| 38 | EconomicGait | 经济步态 |
| 39 | SwitchAvoidMode | 切换避障模式 |

---

## 部署与构建

### 硬件要求

- **架构**: ARM aarch64（NVIDIA Jetson 或机器狗机载计算机）
- **OS**: Linux (kernel 5.10.104-tegra, Ubuntu 20.04, GCC 9.4.0)
- **预编译二进制**: ARM aarch64 ELF，**无法**在 x86/x64 桌面机运行

### 前置条件

1. **Unitree SDK2** (v2.0.0): 必须位于兄弟目录 `../unitree_sdk2`
   ```
   /home/unitree/Documents/unitree_sdk2/     # 机器狗上路径
   ```
   SDK 提供：
   - 头文件: `unitree_sdk2/include/`
   - 预编译静态库: `unitree_sdk2/lib/aarch64/libunitree_sdk2.a`
   - 第三方依赖（DDS 库）: `unitree_sdk2/thirdparty/`

2. **CMake** >= 3.5（构建使用 3.16.3）
3. **GCC** >= 9.0（C++17 支持）
4. **Make**（Unix Makefiles 生成器）
5. **pthread** 支持

### 目录布局

```
/home/unitree/Documents/
├── unitree_sdk2/              # Unitree SDK2 源码 + 预编译库
│   ├── include/
│   ├── lib/aarch64/           # libunitree_sdk2.a
│   └── thirdparty/
│       ├── include/
│       └── lib/aarch64/       # libddsc.so, libddscxx.so
└── go2sportworkspace/         # 本项目
    ├── main.cpp
    ├── CMakeLists.txt
    └── build/
```

### 构建步骤

```bash
cd /home/unitree/Documents/go2sportworkspace
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
```

生成的 `go2_stand_control` 可执行文件位于 `build/` 目录。

---

## 运行方法

### 启动程序

```bash
./go2_stand_control <网络接口名称>
```

示例：
```bash
./go2_stand_control eth0
```

网络接口名称为连接机器狗内部网络的以太网接口。

### 交互命令

程序启动后：
1. 初始化 DDS 通信通道
2. 打印 39 个动作菜单
3. 进入交互提示，输入：
   - **数字** (1-39): 执行对应动作
   - **list**: 重新显示菜单
   - **q** 或 **quit**: 停止机器人并退出

### 参数化动作示例

**Euler（姿态角）**:
```
输入动作编号: 9
请输入 roll (度): 5
请输入 pitch (度): 0
请输入 yaw (度): 10
```

**Move（移动速度）**:
```
输入动作编号: 10
请输入 vx (m/s): 0.2
请输入 vy (m/s): 0
请输入 yaw 速度 (rad/s): 0.1
```

### 危险动作确认

危险动作（前翻、后翻、倒立等）需要输入 `yes` 确认：
```
输入动作编号: 29
[危险] 前翻
确认执行? (输入 yes 继续): yes
```

---

## 依赖项

| 依赖 | 类型 | 版本 | 用途 |
|------|------|------|------|
| **Unitree SDK2** | C++ 静态库 | 2.0.0 | 机器人通信 API（SportClient, ChannelFactory） |
| **CycloneDDS** (`libddsc`) | 共享库 | SDK 附带 | DDS 中间件 |
| **CycloneDDS-CXX** (`libddscxx`) | 共享库 | SDK 附带 | DDS C++ 绑定 |
| **pthread** | 系统库 | 系统 | 线程支持 |
| **CMake** | 构建系统 | >= 3.5 | 构建配置 |
| **GCC** | 编译器 | >= 9.0 (C++17) | 编译 |

**关键 SDK 头文件**:
```cpp
#include <unitree/robot/go2/sport/sport_client.hpp>
```

提供 `unitree::robot::go2::SportClient` 类和 `unitree::robot::ChannelFactory`。

---

## 注意事项

1. **仅 ARM 目标**: 预编译二进制和 SDK 库为 **aarch64**（ARM 64 位），无法在 x86/x64 机器构建或运行，除非有该架构的 SDK
2. **SDK 路径硬编码**: `CMakeLists.txt` 期望 `unitree_sdk2` 位于 `../unitree_sdk2`，移动项目必须保持此相对布局或更新 `add_subdirectory` 路径
3. **网络接口必需**: 程序必须传入网络接口名称作为参数，机器狗上通常为 `eth0`，无参数运行会打印用法并退出
4. **危险动作**: ID 19-21（前翻/前跳/前扑）、24-25（左翻/后翻）、26（倒立）、29（自由跳跃）标记为危险，程序要求输入 `yes` 确认，执行前务必清理机器狗周围区域
5. **退出安全**: 程序退出时总是调用 `StopMove()`，确保机器人安全停止
6. **可执行文件名误导**: 二进制名为 `go2_stand_control`，但实际提供完整运动控制（39 个动作），不仅是站立
7. **DDS 运行时库**: 二进制动态链接 SDK 第三方目录中的 `libddsc.so` 和 `libddscxx.so`，`rpath` 嵌入指向 `/home/unitree/Documents/unitree_sdk2/thirdparty/lib/aarch64`，移动 SDK 会导致找不到库，需更新 `LD_LIBRARY_PATH` 或重新链接
8. **构建类型**: 现有构建为 **Release** 模式（`-O3 -DNDEBUG`），调试需重新构建 `-DCMAKE_BUILD_TYPE=Debug`
9. **交叉编译**: 从桌面向机器狗交叉编译需要 aarch64 交叉编译工具链，设置 `CMAKE_C_COMPILER` 和 `CMAKE_CXX_COMPILER` 为交叉编译器（构建日志显示 `aarch64-linux-gnu-gcc-9` / `aarch64-linux-gnu-g++-9`）

---

## 快速检查清单

- [ ] Unitree SDK2 已放置在 `../unitree_sdk2`
- [ ] C++ 程序已编译（`build/go2_stand_control`）
- [ ] 网络接口已确认（`eth0` 或其他）
- [ ] 已理解危险动作需要输入 `yes` 确认
- [ ] 已理解退出时自动调用 `StopMove()`
- [ ] 机器狗周围区域已清理（执行危险动作前）
- [ ] DDS 运行时库路径正确（`LD_LIBRARY_PATH` 或 rpath）

---

## 相关资源

- **位置**: `G:\xjtlu\SURF\source\haihang\Docs\go2sportworkspace`
- **Unitree SDK2**: 需从 Unitree 官方获取
- **相关项目**: `go2gestureworkspace`（手势控制）
