# go2/go2w现状分析与差距评估

> 目标：围绕 `~\slam\unitree\go2\unitree` 与 `~\slam\unitree\go2w\unitree` 两个部署包，客观回答 4 个问题：
> 1. 是否只有编译好的二进制？（几乎都是）
> 2. 能否从二进制 / 配置 / 依赖库逆推出前端与后端算法？（能，但意义不大）
> 3. 这两个包能否在「非宇树」设备上运行？（几乎不可）
> 4. 相对目标项目（**廉价 RGB-D 主动建图 + 高精度 LiDAR 裁判 + 边缘/云端 AI**），能复用哪些部分、还缺哪些功能？（RGB-D 建图、主动探索 NBV、地图不确定度评估、边缘 AI 推理、云端通信、双地图定量对比)

---

## 1. 源码情况：只有二进制，唯一源码是 keyDemo

两个部署包的代码文件清单如下（两包字节完全一致）：

| 类型 | 路径 | 是否源码 | 说明 |
| --- | --- | --- | --- |
| 可执行文件 | `module/unitree_slam/bin/{keyDemo, mid360_driver, unitree_slam, xt16_driver}` | ❌ 预编译 ELF | 无法直接阅读 |
| 动态库 | `module/unitree_slam/lib/lib*.so` ×9 | ❌ 预编译 ELF | 无法直接阅读 |
| 源码 | `module/unitree_slam/example/src/keyDemo.cpp` | ✅ **唯一源码** | 388 行，只是 DDS 客户端示例，**不包含任何 SLAM 算法** |
| 第三方头 | `module/unitree_slam/example/include/json.hpp` | ✅ | nlohmann/json 单头文件（748 KB），仅做 JSON 序列化 |
| 构建 | `example/CMakeLists.txt` | ✅ | 只编译 keyDemo，不编译 SLAM 主体 |
| 配置 | `config/**/*.{yaml,json,xml,csv}` | ✅ 文本 | 参数文件，本身也是重要的逆推线索 |

**结论**：**核心 SLAM 算法以闭源二进制形式分发**，用户拿到的只有运行时镜像 + 配置 + 一个调用示例。要改算法细节只能通过改 YAML 或替换 `.so`。

---

## 2. 从依赖库 + 配置字段逆推算法栈

虽然没有源码，但 **YAML 中的参数命名约定、`.so` 的命名** 都带有强特征，足以高置信度反推以下结论：

### 2.1 前端（scan-to-map 里程计 + IMU 紧耦合）：**FAST-LIO2 家族**

证据（见 `config/pl_mapping/mid360.yaml`、`xt16.yaml`）：

| 参数 | 含义 | 来源特征 |
| --- | --- | --- |
| `acc_cov` / `gyro_cov` / `b_acc_cov` / `b_gyro_cov` | IMU 过程噪声与零偏协方差 | **IESKF**（迭代误差状态卡尔曼）标准命名 |
| `lidar_meas_cov_inv` / `imu_meas_acc_cov_inv` / `imu_meas_gyro_cov_inv` | 观测协方差的**倒数** | **FAST-LIO/FAST-LIO2 专用**写法 |
| `cube_len: 300.0` / `det_range: 60.0` | 地图立方体长度 / 有效探测范围 | **FAST-LIO2 的 ikd-Tree 地图管理**专属字段 |
| `near_search_num: 5.0` | 平面拟合的最近邻数 | FAST-LIO2 `NUM_MATCH_POINTS` 对应 |
| `filter_num` | 跳采点数 | FAST-LIO2 `point_filter_num` |
| `pose_imu_lidar: [qw, qx, qy, qz, tx, ty, tz]` | IMU→LiDAR 外参 | FAST-LIO2 `extrinsic_T/R` 对应 |
| `plane_threshold: 0.1` / `ground_ang: 75.0` | 平面判定阈值 | 典型平面-LIO 策略 |

**判定**：前端是 **FAST-LIO2 的二次工程化版本**（宇树加了地面点处理、多机型分段）。

### 2.2 重定位（已知地图下的 global-to-local 匹配）：**NDT / GICP 体素匹配**

证据（见 `config/pl_relocation/mid360.yaml`）：

| 参数 | 含义 |
| --- | --- |
| `icp_score: 0.03` | ICP 收敛评分阈值 |
| `gridResolutionX/Y/Z: 30` | **体素网格分辨率**（NDT / Voxel-GICP 标配） |
| `nearbyMethod: NEARBY26` | **26 邻域搜索**——这是 `pclomp/ndt_omp` 或 Autoware NDT 的 **NEIGHBORHOOD_METHOD** 字面量 |
| `init_local_map_res: 0.15` | 局部地图初始分辨率 |
| `re_position_tollerance / re_angle_tollerance / re_score_tollerance` | 重定位三阈值 |

**判定**：重定位采用 **NDT-OMP 或 Voxel GICP**，先把保存的 `.pcd` 全局地图体素化，再做 scan-to-submap 配准。

### 2.3 后端（位姿图）：**g2o / GTSAM 家族**（置信度中）

证据：
- `lib/libgraph_function.so` 的命名 → 位姿图（pose graph）功能库
- 配置中没有出现 `loop_closure_thresh`、`isam`、`smoother_lag` 等典型字段 → 可能是 **轻量级位姿图 + 关键帧拼接**，未必有完整回环
- `libbasic_data.so` 中大概率封装了 SE3 / KeyFrame / Factor 等基础类型

**判定**：**有位姿图结构，但回环检测链路薄弱**（YAML 里完全找不到 Scan Context、BoW、description-matching 之类的参数）。

### 2.4 建图输出与可通行性：**grid_map + 自研碰撞检测**

证据：
- `lib/libgrid_map_core.so` → 直接引用 **ANYbotics grid_map** 库
- `config/gridmap_config/config.yaml` 里的 `collision_x_range` / `warning_x_range` / `predict_num` / `predict_time` → 是宇树自研的 **2D 栅格碰撞 + 预测碰撞**

### 2.5 驱动与通信

| 依赖 | 来源 |
| --- | --- |
| `liblivox_lidar_sdk_shared.so` | **Livox Lidar SDK v2**（开源） |
| `libPandarGeneralSDK.so` | **Hesai Pandar General SDK**（开源） |
| `libodom_imu_data.so` | 宇树自研：腿部 odom + IMU 融合 |
| `libsport_control.so` | 宇树自研：封装 `unitree_sdk2` 的 Sport/Loco 指令 |
| `libslam_server.so` / `libcommand_function.so` | 宇树自研：DDS 服务端 + API 分发 |

### 2.6 一张图总结算法栈

```
 Livox MID-360 / Hesai XT-16
        │  (liblivox_lidar_sdk / libPandarGeneralSDK)
        ▼
  点云 + IMU
        │
        ▼  ┌────────────────────────────────────────┐
  前端：FAST-LIO2（IESKF，紧耦合，ikd-Tree）         │ ← libbasic_data / libodom_imu_data
        │  输出 rt/unitree/slam_mapping/{points,odom}│
        ▼                                          │
  建图：关键帧 + 位姿图（g2o/GTSAM 家族）           │ ← libgraph_function
        │  保存 pcd（save_pcd: true）               │
        ▼                                          │
  重定位：NDT-OMP / Voxel-GICP                     │ ← libslam_server
        │  输出 rt/unitree/slam_relocation/{...}    │
        ▼                                          │
  可通行性：ANYbotics grid_map + 碰撞/预警         │ ← libgrid_map_core
        │  输出 rt/gridmap                         │
        ▼                                          │
  规划/PID：自研巡迹 → libsport_control             │
        │  → unitree_sdk2 Sport/Loco               │
        ▼                                          │
  机器人本体执行                                    │
                                                   │
  服务接口：DDS slam_operate（1801/1802/1804/1102...│ ← libcommand_function
```

---

## 3. 能否在非宇树设备上运行？——**几乎不能**

这两个包是 **紧耦合在宇树机器人上的闭源运行时**，搬到通用 Linux/PC 会遇到至少 4 层障碍。

| 障碍层 | 具体内容 | 可解决性 |
| --- | --- | --- |
| **① CPU 架构** | `.so` 与 bin 是 Linux ELF，**很可能是 aarch64**（宇树机器人控制板为 ARM）。在 x86_64 PC 上直接加载会 `ELF class mismatch` 报错 | ❌ 除非宇树也发了 x86_64 版，否则不可解 |
| **② 系统 ABI** | 依赖特定 glibc / libstdc++ / libboost 版本（宇树机器人 Ubuntu 20.04 基线） | ⚠️ 可通过 docker 模拟 |
| **③ DDS 话题上游** | `unitree_slam` 强依赖机器人端持续发布的 `rt/dog_odom`、`rt/dog_imu_raw`、`rt/utlidar/*`，**PC 上无源** | ❌ 必须自行造同名发布者（格式严格遵守 `unitree_sdk2` 的 IDL） |
| **④ 运动闭环** | `libsport_control.so` 会把规划结果发给宇树 Sport Client；**若没有宇树机器人，发出去没人执行**，导航会停在"发送成功但机器人不动" | ❌ 规划/导航模块无法闭环；但建图/重定位可以 |

### 实务性结论

- **完全脱离宇树硬件直接运行整包**：**不可行**。
- **仅复用"建图 + 重定位"**（不需要底盘动）：**理论可行**，前提是：
  1. 在 aarch64 Linux 或其模拟环境中执行；
  2. 用任意节点（bag 回放 / 自写 publisher）按 IDL 发布 `rt/unitree/slam_lidar/points` + `rt/unitree/slam_lidar/imu`；
  3. 忽略 `rt/dog_odom` / `rt/dog_imu_raw`（SLAM 会退化为纯 LIO，可用但精度略降）。
- **作为"LiDAR 数据采集 + 离线 SLAM"参考**：**建议直接换成开源 FAST-LIO2**，因为完全没有被闭源锁住的必要。

---

## 4. 现状 SLAM 性能评估

| 维度 | 评价 | 说明 |
| --- | --- | --- |
| 精度 | **中高** | FAST-LIO2 在 MID-360 下轨迹漂移典型 < 0.5 %；短期建图足够精细 |
| 实时性 | **高** | IESKF 前端单帧 10–20 ms；MID-360 20 Hz 可稳定跟上 |
| 鲁棒性 | **中** | 静态或慢速场景 OK；快速旋转、长走廊、空旷场景会退化（典型 LIO 通病） |
| 回环能力 | **弱** | 未见 Scan Context / BoW 相关配置；长距离闭环误差难以修正 |
| 重定位 | **中** | NDT/GICP 对已知地图 < 30 m 初始偏差可恢复；大偏差需要先给初值 |
| 多传感器融合 | **弱** | 只融合 LiDAR + IMU + 腿 odom；**不支持 RGB-D、视觉、UWB、GNSS** |
| 建图类型 | 点云 pcd + 2D gridmap | 不输出 occupancy grid（只有自研碰撞栅格），也**不输出 elevation map / TSDF / mesh** |
| 可扩展性 | **差** | 闭源 `.so`；改前端/后端策略几乎只能替换整条通路 |

**总体判定**：作为"把 Go2/Go2-W 机器人开箱即用地跑起来建图 + 巡航"的完整方案，**性能够用**；作为研究平台扩展到新传感器、新算法，**扩展空间非常有限**。

---

## 5. 相对目标项目（RGB-D 主动建图 + LiDAR 裁判 + Edge/Cloud AI）的复用与缺口

### 5.1 目标项目拆解

把那段描述拆成 6 个功能块：

| 功能块 | 关键词 |
| --- | --- |
| F1 | **廉价 RGB-D** 建图（Realsense / Azure Kinect / Orbbec） |
| F2 | **主动运动** — 检测盲点后自动移动以采样 |
| F3 | **边缘 AI** — 机载实时评估地图质量 |
| F4 | **云端 AI** — 远端评估、对比、联合推理 |
| F5 | **LiDAR 参考地图** — 作为 ground-truth "裁判" |
| F6 | **双地图对比** — 廉价地图 vs LiDAR 地图的定量评估 |

### 5.2 可复用 ✅ vs 缺失 ❌ 一览

| # | 目标能力 | 部署包现状 | 复用方式 / 缺口 |
| --- | --- | --- | --- |
| F1 | RGB-D 建图 | ❌ **完全缺失** | 无 RGB-D 驱动、无视觉特征、无深度融合。**要从零引入** RTAB-Map / ORB-SLAM3 / ElasticFusion / Open3D-Slam 之一 |
| F2 | 主动运动（NBV） | ❌ 缺失 | 现有 `POSE_NAV_PL(1102)` 只能执行**预设航点**；没有 frontier exploration / next-best-view / information-gain 评估 |
| F2-子 | 底盘控制通道 | ✅ **可复用** | `SportClient` / `LocoClient` / `POSE_NAV_PL` / `PAUSE_NAV(1201)` / `RESUME_NAV(1202)`，直接把 NBV 规划结果送进去即可 |
| F3 | 边缘 AI 推理 | ❌ 缺失 | 没有 ONNX / TensorRT / LibTorch / OpenVINO 链路；需自备 runtime |
| F3-子 | 边缘数据入口 | ✅ 可复用 | DDS 通道成熟（`rt/unitree/slam_*`、`rt/gridmap`），AI 模块作为新的 DDS subscriber 即可实时消费 |
| F4 | 云端 AI 通信 | ❌ 缺失 | Cyclone DDS **仅在局域网有效**；要云端需额外接 MQTT / gRPC / WebRTC / Zenoh |
| F5 | LiDAR 参考地图 | ✅ **几乎开箱即用** | `unitree_slam` + MID-360/XT-16 + `save_pcd:true` 直接产出高精度 pcd；可作 ground-truth |
| F5-子 | 参考地图的可视化 | ✅ 可复用 | `rviz2/mapping.rviz` / `relocation.rviz` |
| F5-子 | 参考地图的重定位 | ✅ 可复用 | `START_RELOCATION_PL(1804)` 用 NDT/GICP 把两套地图对齐到同坐标系，是后续"对比"的前置 |
| F6 | 双地图定量对比 | ❌ 缺失 | 没有 chamfer distance / F-score / accuracy-completeness / gaussian splatting metric 等评估工具；**须另写评估脚本** |
| — | 可通行性地图 | ✅ 可复用 | `libgrid_map_core` + `rt/gridmap`，NBV 规划时可直接消费 |
| — | 回桩充电 | ⚠️ 与目标无关 | 可忽略 |


## 总结
- **能复用**：LiDAR 驱动 + FAST-LIO2 建图 + pcd 保存 + gridmap 碰撞检测 + 重定位 + 机器人底盘控制通道 + DDS 数据总线 —— 基本覆盖 **"裁判"** 和 **"执行机构"** 两条主线。
- **完全缺失**：RGB-D 建图、主动探索 NBV、地图不确定度评估、边缘 AI 推理、云端通信、双地图定量对比 —— 需要从零构建，占整个项目**约 60–70 %** 的工作量。
- **关键建议**：把本部署包定位为 **"数据提供方 + 执行器驱动"**，把创新集中在 RGB-D + AI + 主动运动那一侧；**不要试图改宇树闭源 SLAM 的内部逻辑**（没有源码，成本极高）。
