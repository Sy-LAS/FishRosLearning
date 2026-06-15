# 基于 拓展坞模块更新包 + `sdk` 的模块复用/缺失清单

> **现有**：
> - 运行时部署包：`~\slam\unitree\go2\unitree`（二进制为主；见 [`slam_go2_tutorial.md`](./slam_go2_tutorial.md)）
> - SDK 源码与头文件：`~\sdk\unitree_sdk2`（已裁剪至 Go2/Go2W 范围；见 [`possibleUse_sdk_tutorial.md`](./possibleUse_sdk_tutorial.md)）
>
> **假定目标**：
> > 使用**廉价 RGB-D 相机**绘制房间地图，但主动补偿相机缺陷；由**机载"边缘 AI"+ 远程"云 AI"** 驱动，实时评估自己的地图；检测到盲点会**自动移动**获取更好的数据；同时携带**高精度 LiDAR** 作"裁判"给出参考地图；通过**对比廉价主动改进地图 vs LiDAR 完美地图**，证明"智能软件 + 主动运动能让便宜传感器做出贵传感器的效果"。
>
> **本文档目的**：在"已有部署包 + 已有 SDK"两份资产的前提下，逐模块标出**哪些直接可用**、**哪些已有但还没接进去**、**哪些必须新写**，尝试给出最少工作量路径。
>
> **判定口径**：
> - ✅ **已具备并在用**：资产里有现成产物/代码，且部署包已在使用
> - 🟢 **已具备但未接入**：SDK/部署包已提供，但当前 `bin/unitree_slam` 没用到；目标项目可直接拿来
> - ❌ **缺失**：两份资产都没有，必须自行实现或引入开源组件
> - ➖ **不适用**：与目标项目无关（例如回桩充电）

##### 未配置资源

| 资源                                 | 启用方式                                                                   |
| ---------------------------------- | ---------------------------------------------------------------------- |
| Go2 前置摄像头 RGB 流                    | `VideoClient::GetImageSample()`（参考 `example/go2/go2_video_client.cpp`） |
| Go2 VUI（LED + 提示音）                 | `VuiClient`（参考 `example/go2/go2_vui_client.cpp`）                       |
| Go2 视觉跟踪                           | `UtrackClient`                                                         |
| 直接自写 `SportClient` 绕开部署包 PID（更灵活）  | `example/go2/go2_sport_client.cpp` 模板                                  |
| 手柄开始/急停                            | `example/wireless_controller/main.cpp` 模板                              |
| 状态机组织建图流程                          | `example/state_machine/*` 模板                                           |
| SDK 的 `Jsonize` 代替 `nlohmann/json` | `include/unitree/common/json/jsonize.hpp`                              |

##### 缺口

| # | 缺口 | 建议实现 | 预估工作量 |
| --- | --- | --- | --- |
| 1 | **RGB-D 相机驱动与时间同步** | Realsense / Orbbec + `ros2_to_dds` 桥 | 小 |
| 2 | **RGB-D SLAM 前端** | 引入 RTAB-Map（ROS2），位姿先验订阅 `rt/unitree/slam_mapping/odom` | 中 |
| 3 | **RGB-D 专用 IDL**（Image/DepthImage/CameraInfo） | 自写 `.idl` 或走 ROS2 桥 | 小 |
| 4 | **`robot/go2/slam/` 客户端三件套**（封装 7 个 API ID） | 仿 `robot/go2/sport/` 结构写 `slam_api.hpp / slam_client.hpp / slam_error.hpp` | 小 |
| 5 | **地图评估（边缘 AI）节点** | 继承 SDK `ServerBase`，订阅双地图，输出不确定度 | 中 |
| 6 | **边缘推理 runtime 集成** | ONNX Runtime（CPU/GPU）或 TensorRT | 中 |
| 7 | **NBV 主动探索节点** | frontier / information-gain；目标位姿 → `POSE_NAV_PL(1102)` | 中 |
| 8 | **云端桥接节点** | Cyclone DDS ↔ MQTT / Zenoh / gRPC | 中 |
| 9 | **双地图定量对比工具** | Python + Open3D，Chamfer / F-score / IoU | 小 |
| 10 | **新配置文件 5 份** | `config/{rgbd,active_explore,edge_ai,cloud_bridge,map_compare}/*.yaml` | 小 |
| 11 | **Go2-W `dds_wrapper`（若换轮足平台）** | 仿 `robots/go2/` 结构 | 小，可延后 |
| 12 | **改动闭源 SLAM 内部逻辑** | ❌ **不可行**：`bin/unitree_slam` / `libslam_server.so` 闭源；若需深度改只能整体换开源 FAST-LIO2 | — |

---

## 1. 现有盘点

### 1.1 `unitree` 部署包提供的**运行时能力**（全部 ✅）

| 能力 | 承载文件 | 对外接口 |
| --- | --- | --- |
| LiDAR 驱动（MID-360 / XT-16） | `bin/{mid360_driver, xt16_driver}` + `config/{mid360,xt16}/*` | 发布 `rt/unitree/slam_lidar/{points,imu}` |
| LiDAR SLAM 前端（FAST-LIO2 风格建图） | `bin/unitree_slam` + `lib/libbasic_data.so` + `libodom_imu_data.so` + `config/pl_mapping/*` | 输出 `rt/unitree/slam_mapping/{points,odom}`，保存 pcd |
| 重定位（NDT / Voxel-GICP） | `lib/libslam_server.so` + `config/pl_relocation/*` | 输出 `rt/unitree/slam_relocation/{odom,global_map,local_map}` |
| 位姿图后端 | `lib/libgraph_function.so` | 内部维护关键帧 |
| 栅格地图与碰撞预警 | `lib/libgrid_map_core.so` + `config/gridmap_config/config.yaml` | 发布 `rt/gridmap` |
| 路径规划 + PID 巡迹 | `bin/unitree_slam` + `config/planner_config/*` | 通过 `slam_operate` 服务的 `POSE_NAV_PL(1102)` 接收目标点 |
| 下发运动指令到 Go2 本体 | `lib/libsport_control.so` | 内部调用 `SportClient` |
| DDS API 服务端 | `lib/libcommand_function.so` + `libslam_server.so` | `slam_operate` 服务，7 个 API ID（1801/1802/1804/1102/1201/1202/1901） |
| 示例客户端 | `example/src/keyDemo.cpp` | 键盘驱动上述 7 个 API |
| systemd 启动 | `services/install.sh` + `rviz2/*.rviz` | 开机自启 + 可视化 |

### 1.2 `sdk/unitree_sdk2` 提供的**可编程能力**（全部 ✅）

| 层 | SDK 位置 | 对目标项目的价值 |
| --- | --- | --- |
| 通用基础设施 | `include/unitree/common/`（dds / json / thread / log / service / filesystem / time） | 写任何新节点都要用 |
| DDS 通道 | `include/unitree/robot/channel/{factory,publisher,subscriber,...}` | 发布/订阅点云、位姿、AI 结果的唯一途径 |
| DDS 客户端基类 | `include/unitree/robot/client/{client,client_base,...}` | 调用 `slam_operate` / 自写客户端 |
| DDS 服务端基类 | `include/unitree/robot/server/{server,server_base,...}` | **自建边缘 AI / NBV 服务**的骨架 |
| Go2 高层运动客户端 | `include/unitree/robot/go2/sport/*` | 替部署包之外的节点也能直接驱动 Go2 |
| Go2 避障 | `include/unitree/robot/go2/obstacles_avoid/*` | 主动移动期间保护机体 |
| Go2 机器人状态 | `include/unitree/robot/go2/robot_state/*` | 查电量、服务状态 |
| Go2 视频客户端 | `include/unitree/robot/go2/video/*` | 🟢 **目标项目可直接调内置摄像头**（部署包未使用） |
| Go2 VUI（LED/语音） | `include/unitree/robot/go2/vui/*` | 🟢 扫描完成提示音 / 灯效 |
| Go2 视觉跟踪 | `include/unitree/robot/go2/utrack/*` | 🟢 目标跟随（可选） |
| Go2-W 运动 | `example/go2w/*` + `robot/go2/sport/*`（Go2-W 复用 go2 三件套的变体） | 🟢 若换 Go2-W 平台可用 |
| 底层 `LowCmd_/LowState_` | `include/unitree/idl/go2/*` | 查电机 / 关节状态 |
| ROS2 通用消息类型 | `include/unitree/idl/ros2/*`（Pose/Twist/Imu/PointCloud2/OccupancyGrid/Odometry/Header/Time 等 24 个） | **双地图交换的标准载体** |
| Go2 机型 DDS 封装糖 | `include/unitree/dds_wrapper/robots/go2/{defines,go2,go2_pub,go2_sub}.h` | 写 RGB-D 节点时少打一半样板 |
| 示例合集 | `example/go2/*.cpp`（sport / low_level / robot_state / trajectory_follow / **video** / vui）、`helloworld/{publisher,subscriber}.cpp`、`jsonize/test_jsonize.cpp`、`wireless_controller/main.cpp`、`state_machine/*` | **写 RGB-D、NBV、AI 节点时直接照抄** |
| 第三方运行时 | `thirdparty/include/dds{,cxx}/*` + `thirdparty/lib/{aarch64,x86_64}/libddsc(xx).so` | Cyclone DDS 完整 C/C++ 绑定 |

### 1.3 一句话合并结论

**"机器人本体 + LiDAR 裁判 + 下发运动 + 通信总线 + 编程框架"五件事已经 100% 具备**；
**真正要补的是"RGB-D 采集 → 廉价地图 → 地图不确定度 → 主动探索 → 云端对比"这条新链路。**

---

## 2. 按 SDK 模块逐项对照

### 2.1 `include/unitree/common/` — 基础库

| 子模块 | 部署包是否在用 | 目标项目要不要写新模块时用 | 判定 |
| --- | --- | --- | --- |
| 顶层 8 个头（any/assert/block_queue/error/exception/os/string_tool/decl） | ✅ `.so` 内部 | ✅ | 已具备 |
| `dds/`（15 个 QoS/Entity 头） | ✅ | ✅ 自建 AI 服务时必用 | 已具备 |
| `filesystem/` / `lock/` / `time/` | ✅ | ✅ | 已具备 |
| `json/`（`Jsonize` 基类） | 🟢 部署包用 nlohmann/json，SDK 的 `Jsonize` 未用 | ✅ 推荐新节点用 `Jsonize`，与 SDK 一致 | 已具备，推荐接入 |
| `log/`（9 个头） | ✅ `bin/unitree_slam` 用 | ✅ 新节点直接 `LOGI`/`LOGE` | 已具备 |
| `service/` + `service/base/` | ✅ `libslam_server.so` 继承 `ServiceBase` | ✅ **边缘 AI 做成 DDS 服务必用** | 已具备 |
| `thread/`（`recurrent_thread` 尤重要） | ✅ | ✅ RGB-D 发布环、NBV 打分环必用 | 已具备 |

**缺失**：无。

### 2.2 `include/unitree/dds_wrapper/` — DDS 封装糖

| 路径 | 文件 | 部署包 | 目标项目 | 判定 |
| --- | --- | --- | --- | --- |
| `dds_wrapper/common/` | `Publisher.h / Subscription.h / crc.h / unitree_joystick.hpp`（4 个） | ✅ | ✅ 任何新节点可直接 include | 已具备 |
| `dds_wrapper/robots/go2/` | `defines.h / go2.h / go2_pub.h / go2_sub.h`（4 个） | ✅ `libsport_control.so` 内部 | ✅ 新节点可直接 include | 已具备 |


### 2.3 `include/unitree/idl/` — 消息类型

| IDL 子集 | 目标项目用途 | 判定 |
| --- | --- | --- |
| `idl/go2/`（25+ 个：LowCmd/LowState/SportModeCmd/IMUState/HeightMap/VoxelMapCompressed/WirelessController/BmsState/…） | 读取 Go2 本体状态、下发运动 | ✅ |
| `idl/ros2/`（24 个：Header/Imu/PointCloud2/PointField/OccupancyGrid/Odometry/Pose*/Twist*/String/Time/…） | **LiDAR 地图、RGB-D 地图、NBV 目标姿、双地图对比结果的统一载体** | ✅ 已具备（部署包 `keyDemo` 已用 `String_`，`bin/unitree_slam` 大概率用 `PointCloud2_`/`Odometry_`） |
| `idl/hg/` + `idl/hg_doubleimu/` | 人形机器人专用 | ➖ 不适用 |

**缺失**：
- ❌ **RGB-D 专用 IDL**：SDK 的 `idl/ros2/` **没有 `Image_` / `CompressedImage_` / `CameraInfo_` / `DepthImage_`**。需要自写 `.idl`（或用 ROS2 bridge → DDS）。
- ✅ **点云与位姿可直接走 `PointCloud2_` / `Pose*_` / `Odometry_`**，不用新增。

### 2.4 `include/unitree/robot/` — 高层客户端（核心复用面）

#### A. 通用基础

| 模块 | 部署包 | 目标项目 | 判定 |
| --- | --- | --- | --- |
| `channel/`（`ChannelFactory` / `ChannelPublisher<T>` / `ChannelSubscriber<T>` / …） | ✅ `keyDemo` + `libslam_server` | ✅ 必用 | 已具备 |
| `client/`（`Client` / `ClientBase` / `LeaseClient`） | ✅ `keyDemo` | ✅ 自写 `slam_client` 封装时作基类 | 已具备 |
| `server/`（`ServerBase` / `LeaseServer` / `server_stub`） | ✅ `libslam_server` 继承 | ✅ **边缘 AI 节点用它做服务端** | 已具备 |
| `future/request_future.hpp` | ✅ 被 `Client::Call` 异步路径内部用 | 🟡 一般不直接用 | 已具备 |
| `serialize/serialize.hpp` | ✅ | ✅ | 已具备 |
| `internal/*`（`Request_` / `Response_` / `RequestHeader_` …） | ✅ RPC 封包 | 🟡 一般不直接用 | 已具备 |

#### B. Go2 专属客户端

| 客户端 | 部署包在用吗 | 目标项目应该怎么用 | 判定 |
| --- | --- | --- | --- |
| `go2/sport/*` | ✅ 由 `libsport_control.so` 封装 | ✅ **NBV 规划器把目标位姿下发**（也可直接写 `SportClient` 走 Move/Euler，绕开部署包） | 已具备 |
| `go2/robot_state/*` | 🟡 部署包少量使用 | ✅ 查机器人锁状态、电量 | 已具备 |
| `go2/config/*` | 🟡 | ✅ 热改运行时参数 | 已具备 |
| `go2/obstacles_avoid/*` | ✅ SLAM 闭环默认开启 | ✅ 主动移动时务必保持开启 | 已具备 |
| `go2/video/*` | 🟢 **部署包未用** | ✅ **目标项目直接调用取前置摄像头帧**，作为 RGB-D 之外的 RGB 补充 | 🟢 已具备但未接入 |
| `go2/vui/*` | 🟢 未用 | 🟢 扫描完成提示音、LED 反馈 | 🟢 已具备但未接入 |
| `go2/utrack/*` | 🟢 未用 | 🟢 若做人跟随可选 | 🟢 已具备但未接入 |
| `go2/public/jsonize_type.hpp` | 🟡 | ✅ 拼请求体的标准结构 | 已具备 |

**缺失点（Go2 视角）**：
- ❌ **SDK 未提供官方 `robot/go2/slam/` 客户端三件套**。当前 `slam_operate` 的 7 个 API ID 靠 `keyDemo.cpp` 手拼 `Request_`。**这是最小且收益最高的封装工作**。
- ❌ **未提供 `robot/go2/gridmap/` 客户端**。`rt/gridmap` 只能裸用 `ChannelSubscriber<OccupancyGrid_>`。
 
### 2.5 `lib/` — 二进制静态库

| 文件 | 对应的资产 | 判定 |
| --- | --- | --- |
| `sdk/unitree_sdk2/lib/{aarch64,x86_64}/libunitree_sdk2.a` | ✅ 工作区已提供，`find_package(unitree_sdk2)` 可直接用 | 已具备 |
| 部署包 `module/unitree_slam/lib/lib*.so`（9 个） | ✅ 运行时加载 | 已具备 |
| `sdk/unitree_sdk2/thirdparty/lib/{aarch64,x86_64}/libddsc(xx).so(.0)` | ✅ | 已具备 |

**缺失**：无（之前文档把"需要先装 SDK"列为缺失是误判，已改正）。

### 2.6 `example/` — 可参考的官方示例

| 示例 | 对目标项目的价值 | 备注 |
| --- | --- | --- |
| `example/helloworld/{publisher,subscriber}.cpp` | **最小 DDS 发布/订阅模板**，写 RGB-D 发布节点直接照抄 | ✅ 已有 |
| `example/go2/go2_sport_client.cpp` | NBV 规划结果下发 Move/Euler/BalanceStand 的标准写法 | ✅ 已有 |
| `example/go2/go2_video_client.cpp` | **目标项目直接从这里起步拉前置相机** | ✅ 已有 |
| `example/go2/go2_robot_state_client.cpp` | 查状态范式 | ✅ 已有 |
| `example/go2/go2_trajectory_follow.cpp` | 按预定轨迹走，NBV 回退方案 | ✅ 已有 |
| `example/go2/go2_low_level.cpp` | 底层电机，通常用不到 | 🟡 参考 |
| `example/go2/go2_vui_client.cpp` | LED/声音反馈 | ✅ 已有 |
| `example/jsonize/test_jsonize.cpp` | 新 API 请求体序列化 | ✅ 已有 |
| `example/state_machine/*` | 把"建图 → NBV → 完成 → 对比"组织成状态机 | ✅ 已有 |
| `example/wireless_controller/main.cpp` | 手柄触发开始 / 紧急停止 | ✅ 已有 |
| 部署包 `example/src/keyDemo.cpp` | 调用 `slam_operate` 的唯一实例 | ✅ 已有 |

**缺失**：无（所有目标项目需要的编程模板都能在 SDK 示例里找到对应物）。

### 2.7 `config/` — 运行时参数

部署包已经写满，参见 [`slam_go2_tutorial.md`](./slam_go2_tutorial.md) §2；**所有 LiDAR / SLAM 侧参数都不用动**。

**缺失**（需要为目标项目新增）：
- ❌ `config/rgbd/*.yaml`：RGB-D 相机内外参、话题名、帧率
- ❌ `config/active_explore/*.yaml`：NBV 打分权重、盲点阈值、探索步长
- ❌ `config/edge_ai/*.yaml`：ONNX / TensorRT 模型路径、置信度阈值
- ❌ `config/cloud_bridge/*.yaml`：MQTT/Zenoh 端点、鉴权
- ❌ `config/map_compare/*.yaml`：Chamfer / F-score 评估阈值

---

## 3. 对照目标项目的 5 大功能 — 逐块列"现成的 vs 缺失的"

> 目标项目拆成 5 大模块：**M1 RGB-D 廉价建图 → M2 地图评估 → M3 主动运动 → M4 云端对比 → M5 LiDAR 裁判**。

### M1. 廉价 RGB-D 建图

| 要素 | 现状 | 行动 |
| --- | --- | --- |
| RGB-D 相机驱动 | ❌ 缺失 | 新增：`realsense2_camera` ROS2 节点 or 自写 Orbbec / Azure SDK 适配 |
| RGB-D → DDS 桥 | ❌ 缺失（SDK `idl/ros2/` 无 `Image_`） | 新增：① 写 `.idl` 与自动生成；② 或用 `ros2_to_dds` 桥将 `sensor_msgs/Image` 落到 Cyclone DDS |
| RGB-D SLAM 前端 | ❌ 缺失 | 引入开源：**RTAB-Map**（推荐）/ ORB-SLAM3 / Open3D-Slam；输出 `rt/rgbd/{points,odom,mesh}` |
| 位姿先验 | ✅ 已有 `rt/unitree/slam_mapping/odom`（FAST-LIO2 输出）可直接喂给 RTAB-Map | 只需订阅 |
| 时间同步 | 🟢 SDK `common/time/time_tool.hpp` 可用 | 接入 |

### M2. 地图评估（边缘 AI）

| 要素 | 现状 | 行动 |
| --- | --- | --- |
| 边缘推理 runtime | ❌ 无 ONNX/TensorRT/LibTorch | 新增；Jetson 平台推荐 TensorRT |
| DDS 服务骨架 | ✅ SDK `robot/server/server_base.hpp` + `common/service/service_base.hpp` 直接套 | **按 `libslam_server.so` 的模板写**：订阅双地图 → 评估 → 发 `rt/ai/map_quality` |
| 双地图输入通道 | ✅ `rt/unitree/slam_mapping/points` + 新 `rt/rgbd/points` | 直接订阅 |
| 不确定度 / 盲点度量 | ❌ 缺失 | 新增：点云密度熵、voxel 空洞率、法向一致性 |
| 结果话题 IDL | ✅ 可复用 `String_`（JSON）或 `OccupancyGrid_`（盲点栅格） | 选择其一 |

### M3. 主动运动（NBV）

| 要素 | 现状 | 行动 |
| --- | --- | --- |
| 地图输入 | ✅ `rt/gridmap` + M2 输出 | 订阅 |
| NBV 算法 | ❌ 缺失（frontier exploration / information gain） | 新增，参考开源 `nbv_exploration` / `rrt_exploration` |
| 下发运动目标 | ✅ **两条路都通**：<br>① 调 `slam_operate` 的 `POSE_NAV_PL(1102)` → 走部署包自带规划 + PID<br>② 直接用 `robot/go2/sport/SportClient::Move(vx,vy,w)` 自己闭环 | **推荐 ①**（免自写规划） |
| 紧急暂停 / 恢复 | ✅ `PAUSE_NAV(1201)` / `RESUME_NAV(1202)` | 直接用 |
| 紧急避障 | ✅ `robot/go2/obstacles_avoid/` | 开启 |
| 运行状态反馈 | ✅ `rt/slam_info` / `rt/slam_key_info`（`keyDemo` 里已订阅） | 直接订阅 |

### M4. 云端 AI / 双地图对比

| 要素 | 现状 | 行动 |
| --- | --- | --- |
| 云端通信 | ❌ Cyclone DDS 局域网为主 | 新增：机器人侧 `cloud_bridge` 节点，桥接 DDS ↔ MQTT / Zenoh / gRPC |
| 双地图同坐标系对齐 | ✅ `START_RELOCATION_PL(1804)` 用 NDT 把任意 pcd 对齐到参考地图帧 | 直接用 |
| 地图对比指标 | ❌ Chamfer / F-score / accuracy-completeness / IoU | 新增；离线 Python（Open3D / trimesh） |
| 云端训练 / 长周期比对 | ❌ 业务层 | 新增 |
| 机器人→云 上行带宽 | 🟡 | 新增；建议只上传压缩 pcd + 关键帧图像 |

### M5. LiDAR 裁判

| 要素 | 现状 | 行动 |
| --- | --- | --- |
| 高精度 LiDAR 建图 | ✅ 部署包开箱即用（MID-360 + FAST-LIO2） | 0 行代码 |
| pcd 保存 | ✅ `config/pl_mapping/mid360.yaml` 里 `save_pcd: true` | 0 行代码 |
| 参考地图可视化 | ✅ `rviz2/mapping.rviz` | 0 行代码 |
| 重定位把廉价地图对齐 | ✅ `START_RELOCATION_PL(1804)` + `config/pl_relocation/*` | 0 行代码 |
| 裁判权威性 | ✅ FAST-LIO2 典型轨迹漂移 < 0.5%；MID-360 20 Hz 稳定 | — |

---

## 4. 总表：已经有什么 / 还要写什么

### 4.1 ✅ 已具备可直接用（不必再做）

| 类别 | 来源 |
| --- | --- |
| LiDAR 建图 / 重定位 / gridmap / PID 巡迹 / API 服务 | `unitree` 部署包 `bin/` + `lib/` + `config/` |
| 7 个 `slam_operate` API | `keyDemo.cpp` 已演示调用 |
| DDS 通道框架（Channel/Client/Server/Factory/ChannelSubscriber） | `sdk` `include/unitree/robot/{channel,client,server}/*` |
| 通用基础（log/thread/service/json/filesystem/dds） | `sdk` `include/unitree/common/*` |
| Go2 全套客户端（sport/video/vui/robot_state/config/obstacles_avoid/utrack） | `sdk` `include/unitree/robot/go2/*` |
| Go2 机型 DDS 糖 | `sdk` `include/unitree/dds_wrapper/robots/go2/*` |
| 全部 `idl/go2/` + `idl/ros2/` 消息类型 | `sdk` `include/unitree/idl/*` |
| Cyclone DDS C/C++ 运行时 | `sdk` `thirdparty/` |
| 10+ 可直接抄的官方示例 | `sdk` `example/*` |

### 4.2 🟢 已具备但部署包未启用（目标项目"捡起来就能用"）

| 资产 | 启用方式 |
| --- | --- |
| Go2 前置摄像头 RGB 流 | `VideoClient::GetImageSample()`（参考 `example/go2/go2_video_client.cpp`） |
| Go2 VUI（LED + 提示音） | `VuiClient`（参考 `example/go2/go2_vui_client.cpp`） |
| Go2 视觉跟踪 | `UtrackClient` |
| 直接自写 `SportClient` 绕开部署包 PID（更灵活） | `example/go2/go2_sport_client.cpp` 模板 |
| 手柄开始/急停 | `example/wireless_controller/main.cpp` 模板 |
| 状态机组织建图流程 | `example/state_machine/*` 模板 |
| SDK 的 `Jsonize` 代替 `nlohmann/json` | `include/unitree/common/json/jsonize.hpp` |

### 4.3 ❌ 必须自行新增（真正的缺口）

| # | 缺口 | 建议实现 | 预估工作量 |
| --- | --- | --- | --- |
| 1 | **RGB-D 相机驱动与时间同步** | Realsense / Orbbec + `ros2_to_dds` 桥 | 小 |
| 2 | **RGB-D SLAM 前端** | 引入 RTAB-Map（ROS2），位姿先验订阅 `rt/unitree/slam_mapping/odom` | 中 |
| 3 | **RGB-D 专用 IDL**（Image/DepthImage/CameraInfo） | 自写 `.idl` 或走 ROS2 桥 | 小 |
| 4 | **`robot/go2/slam/` 客户端三件套**（封装 7 个 API ID） | 仿 `robot/go2/sport/` 结构写 `slam_api.hpp / slam_client.hpp / slam_error.hpp` | 小 |
| 5 | **地图评估（边缘 AI）节点** | 继承 SDK `ServerBase`，订阅双地图，输出不确定度 | 中 |
| 6 | **边缘推理 runtime 集成** | ONNX Runtime（CPU/GPU）或 TensorRT | 中 |
| 7 | **NBV 主动探索节点** | frontier / information-gain；目标位姿 → `POSE_NAV_PL(1102)` | 中 |
| 8 | **云端桥接节点** | Cyclone DDS ↔ MQTT / Zenoh / gRPC | 中 |
| 9 | **双地图定量对比工具** | Python + Open3D，Chamfer / F-score / IoU | 小 |
| 10 | **新配置文件 5 份** | `config/{rgbd,active_explore,edge_ai,cloud_bridge,map_compare}/*.yaml` | 小 |
| 11 | **Go2-W `dds_wrapper`（若换轮足平台）** | 仿 `robots/go2/` 结构 | 小，可延后 |
| 12 | **改动闭源 SLAM 内部逻辑** | ❌ **不可行**：`bin/unitree_slam` / `libslam_server.so` 闭源；若需深度改只能整体换开源 FAST-LIO2 | — |

---

## 5. 最省力落地顺序（最大化复用）

```
Step 0   确认资产到位
         ├─ sdk/unitree_sdk2 可 find_package → ✅ 已具备
         └─ unitree 部署包 systemd 起起来 → ✅ 已具备

Step 1   封装 slam_client（缺口 #4）          ← 半天
         仿 example/go2/go2_sport_client.cpp 写 slam_api/client/error

Step 2   接 RGB-D（缺口 #1 + #2 + #3）        ← 2–3 天
         Realsense D435 → RTAB-Map → 发 rt/rgbd/{points,odom}
         位姿先验用 rt/unitree/slam_mapping/odom

Step 3   写"双地图对齐 + Chamfer"离线脚本（缺口 #9）   ← 1 天
         调 START_RELOCATION_PL(1804) 对齐坐标系，Python 算 Chamfer

Step 4   写边缘 AI 评估节点（缺口 #5 + #6）   ← 3–5 天
         SDK ServerBase 订双地图；输出 rt/ai/map_quality

Step 5   写 NBV 节点（缺口 #7）               ← 3–5 天
         订阅 rt/ai/map_quality + rt/gridmap
         目标位姿 → slam_client.PoseNavPl()

Step 6   写云端桥（缺口 #8）                   ← 2 天
         把 rt/ai/map_quality + pcd 发 MQTT

Step 7   封装状态机 + 手柄触发                ← 1 天
         复用 example/state_machine + wireless_controller 模板
```

**总工作量估计**： **80% 的代码量集中在 "RGB-D / AI / NBV / 云端对比" 四个新模块**，SDK 与部署包提供的"通信 + 底盘 + 裁判"全部免费。

---

## 6. 结论

1. **"需要装 SDK"不是真缺口**：`sdk/unitree_sdk2` 已随工作区提供，`find_package(unitree_sdk2)` 开箱可用。
2. **部署包把"LiDAR 裁判 + 底盘 + 巡迹 + 服务骨架"这四件事做到了 100%**，目标项目只需复用不需重写。
3. **SDK 提供了写"RGB-D + AI + NBV + 云端"所需的全部通信/框架基础设施**（channel / client / server / thread / service / json / log / idl），**不需要引入额外的 RPC / DDS / 序列化框架**。
4. **真正要写的代码集中在 5 处**：RGB-D 驱动/桥、RGB-D SLAM 前端（建议 RTAB-Map）、边缘 AI 评估、NBV 探索、云端桥 + 对比。
5. **最小封装作业**是给 `slam_operate` 的 7 个 API ID 做一个 `slam_client` 三件套，此后所有上层代码都能像调用 `SportClient::Move()` 一样调用 `SlamClient::StartMapping()`、`PoseNavPl()` 等，工程清晰度立刻拉高。
