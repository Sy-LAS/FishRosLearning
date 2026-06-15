# Unitree Go2 SLAM 部署包
[拓展坞资源](https://support.unitree.com/home/zh/developer/module_update#heading-7)
[官方slam接口介绍](https://support.unitree.com/home/zh/developer/SLAM%20and%20Navigation_service)

> 目标文件夹：`~slam\unitree\go2\unitree`
>
> 这是宇树官方提供的 **Go2 四足机器人 SLAM 运行时部署包**（非源码，非 SDK 头文件），对应机型代号 `Go2`。包内含已编译好的可执行文件（`bin/`）、动态库（`lib/`）、运行时配置（`config/`）、RViz2 可视化预设（`rviz2/`）、入门示例（`example/`）以及 systemd 服务安装脚本（`services/`）。把该目录拷贝到机器人端 `/unitree/module/` 下即可配合 `unitree_sdk2` 运行建图、重定位与巡航任务。
>
> 注意：`.so` 与无扩展名的可执行文件为 **预编译二进制产物**，无法在 Windows 上直接查看内容；本文件仅客观描述其在运行时承担的职责。

---

## 1. 目录树

以下目录树由 Windows `tree /F /A` 命令生成：

```
G:\XJTLU\SURF\SLAM\UNITREE\GO2\UNITREE
+---lib
+---module
|   \---unitree_slam
|       +---bin
|       |       keyDemo
|       |       mid360_driver
|       |       unitree_slam
|       |       xt16_driver
|       |
|       +---config
|       |   |   .gitkeep
|       |   |   clean_log.sh
|       |   |   cyclonedds.xml
|       |   |   dds_config.json
|       |   |
|       |   +---gridmap_config
|       |   |       config.yaml
|       |   |       demo.json
|       |   |       ele.rviz
|       |   |
|       |   +---mid360
|       |   |       mid360_config.json
|       |   |       user_config.yaml
|       |   |
|       |   +---planner_config
|       |   |       param.yaml
|       |   |       pose_ctrl_param.yaml
|       |   |
|       |   +---pl_mapping
|       |   |       mid360.yaml
|       |   |       xt16.yaml
|       |   |
|       |   +---pl_relocation
|       |   |       mid360.yaml
|       |   |       xt16.yaml
|       |   |
|       |   +---recharge_config
|       |   |       aruco_config.yaml
|       |   |       cylinder_config.yaml
|       |   |
|       |   +---slam_interfaces_server_config
|       |   |       cyclonedds.xml
|       |   |       dds_parameter.json
|       |   |       param.yaml
|       |   |
|       |   \---xt16
|       |           PandarXT-16.csv
|       |           user_config.yaml
|       |
|       +---example
|       |   |   CMakeLists.txt
|       |   |   README.md
|       |   |
|       |   +---include
|       |   |       json.hpp
|       |   |
|       |   \---src
|       |           keyDemo.cpp
|       |
|       +---lib
|       |       libbasic_data.so
|       |       libcommand_function.so
|       |       libgraph_function.so
|       |       libgrid_map_core.so
|       |       liblivox_lidar_sdk_shared.so
|       |       libodom_imu_data.so
|       |       libPandarGeneralSDK.so
|       |       libslam_server.so
|       |       libsport_control.so
|       |
|       \---rviz2
|               mapping.rviz
|               relocation.rviz
|
\---services
        install.sh
```

说明：

- 顶层 `lib/` 为空目录，仅作为目录占位；实际库文件位于 `module/unitree_slam/lib/`。
- `services/` 目录仅含一个安装脚本，对应 systemd 服务由机器人端其他位置统一管理。

---

## 2. 文件作用说明

### module/unitree_slam/bin/
- **keyDemo**：ELF 可执行文件，由同目录下 `example/src/keyDemo.cpp` 编译而来；运行 `./keyDemo eth0` 即可通过键盘（q/w/a/s/d/f/z/x）触发 **开始建图 / 结束建图 / 重定位 / 添加目标点 / 执行巡航 / 清空任务 / 暂停 / 恢复** 等 SLAM 操作，是快速验证部署效果的入口。
- **mid360_driver**：Livox MID-360 激光雷达的用户态驱动，负责按 `config/mid360/*` 中的网络与扩展参数拉起雷达、发布点云与 IMU 到 DDS 话题 `rt/unitree/slam_lidar/points`、`rt/unitree/slam_lidar/imu`。
- **unitree_slam**：核心 SLAM 服务进程（10 MB 级），加载 `lib/` 下的功能库，订阅雷达与机器人里程计、IMU，承担**前端匹配、建图、重定位、路径规划与 PID 位姿控制**，并通过 DDS 服务接口 `slam_operate` 暴露建图/重定位/导航 API。
- **xt16_driver**：Hesai PandarXT-16 机械旋转激光雷达的用户态驱动，按 `config/xt16/*` 中的 IP、网卡与标定信息拉起雷达并发布点云；Go2 平台默认使用 MID-360，该驱动用于 XT-16 兼容模式。

### module/unitree_slam/config/
- **.gitkeep**：空占位文件，用于把空目录纳入版本管理，无运行时作用。
- **clean_log.sh**：运行日志清理脚本，接受目录路径作参数，使用 `find ... -mtime +7 -exec rm -f` 删除超过 7 天的文件；典型使用场景是通过 cron 或 systemd timer 清理 `logs/gridmap/` 等输出。
- **cyclonedds.xml**：顶层 Cyclone DDS 配置，`Domain` 下声明网络接口（示例为 `wlp0s20f3`），供主 SLAM 进程参与 DDS 通信使用；实际部署时需按机器人板载网卡名修改。
- **dds_config.json**：与 `unitree_sdk2` 的 `DdsEasyModel` 对应的参数文件，指定 `DomainId=0` 与 Cyclone 配置文件路径，并设置 `Reliability=RELIABLE_RELIABILITY_QOS` 以保证 SLAM 话题的可靠传输。

### module/unitree_slam/config/gridmap_config/
- **config.yaml**：实时 2D 栅格地图（碰撞检测 / 预警）参数，按机型分区（B2、B2_W、G1、Go2、Go2_W）定义分辨率、宽度、雷达安装外参 `T_Dog2lidar`、雷达高度、订阅的点云/里程计话题、碰撞盒与预警盒尺寸、预测碰撞的步数与时间，以及日志路径 `logs/gridmap/`。
- **demo.json**：一条示例碰撞事件的序列化结果（`type: collision`、`errorCode: 421`），展示 SLAM 发布到话题的事件 JSON 格式，供开发者做解析样例参考。
- **ele.rviz**：针对高程栅格（elevation / gridmap）的 RViz2 视图预设，保存了显示项、相机视角与话题订阅，双击可直接打开可视化。

### module/unitree_slam/config/mid360/
- **mid360_config.json**：Livox SDK 的标准雷达参数文件，定义 `lidar_type=8` (MID-360)、命令/推送/点云/IMU 的 UDP 端口映射、宿主机与雷达的 IP（默认 `192.168.123.18` 与 `192.168.123.20`），以及扩展外参 `extrinsic_parameter`。
- **user_config.yaml**：驱动层用户参数，指定网卡 `eth0`、雷达频率 20 Hz、TF 坐标系 `livox_frame`、点云话题 `rt/unitree/slam_lidar/points`、IMU 话题 `rt/unitree/slam_lidar/imu`。

### module/unitree_slam/config/planner_config/
- **param.yaml**：路径规划节点基础参数（发布频率 40 Hz、前视距离 `forwardDis`、到点容忍度、旋转/调整/保持阶段的精度阈值），供 `unitree_slam` 中的巡迹模块 PID 追踪使用。
- **pose_ctrl_param.yaml**：按机型分区（B2、B2_W、G1、Go2、Go2_W、H1）的位姿级 PID 控制参数（x/y/yaw 的 Limmax/Vmax/KP/KI/KD 与阈值）及规划细粒度阈值；Go2 段是本部署包的默认生效组。

### module/unitree_slam/config/pl_mapping/
- **mid360.yaml**：MID-360 激光雷达下的 **FAST-LIO 风格点云-IMU 紧耦合建图** 参数，分机型给出 IMU/Lidar 话题、协方差、地图分辨率、雷达到 IMU 的外参 `pose_imu_lidar`、保存 pcd 开关（`save_pcd`）等；Go2 段默认使用 `rt/unitree/slam_lidar/points` 与 `rt/unitree/slam_lidar/imu`。
- **xt16.yaml**：XT-16 激光雷达下的建图参数，相较 MID-360 版使用较低的 IMU 倍率（`imu_acc_multi=1.0`）、更大的 `filter_num` 与对应外参四元数 `[0.707, 0, 0, 0.707, 0.171, 0, 0.0908]`。

### module/unitree_slam/config/pl_relocation/
- **mid360.yaml**：MID-360 下的 **点云重定位**（global-to-local ICP）参数，包含发布话题（`rt/unitree/slam_relocation/odom`、`.../global_map`、`.../local_map`）、ICP 分数阈值、近邻网格尺寸、重定位容差、速度上限 `speed_max` 等。
- **xt16.yaml**：XT-16 下的重定位参数，差异主要在外参、扫描分辨率与 ICP 阈值，其他结构与 `mid360.yaml` 相同。

### module/unitree_slam/config/recharge_config/
- **aruco_config.yaml**：回桩充电视觉标定文件，含相机内参矩阵 `intrinsic_matrix`、畸变系数 `distCoeffs`、ArUco 码实际边长 `aruco_size`、ArUco 到充电桩中心的距离、相机到狗身的距离，供回充流程做码检测与距离估计。
- **cylinder_config.yaml**：基于圆柱反光柱（高反强度点）的回桩参数，定义雷达话题、高强度点话题 `rt/high_intensity`、充电桩宽长、强度阈值 150，与充电点到中心的 0.38 m 偏移。

### module/unitree_slam/config/slam_interfaces_server_config/
- **cyclonedds.xml**：SLAM 接口服务独立的 Cyclone DDS 配置（示例网卡 `enp2s0`，`AllowMulticast=spdp`），用于把 SLAM 对外 API 与主数据通道解耦，避免多播风暴。
- **dds_parameter.json**：对应的 `Participant` 参数，固定 `DomainId=0` 并给出两个候选 Cyclone 配置路径（`/unitree/etc/cyclonedds.xml` 与相对路径），启动时加载其一。
- **param.yaml**：按机型（B2、B2_W、Go2、Go2_W、G1、H1）给出 SLAM 服务的运行时选项：网卡、激光雷达类型（`mid360` / `xt16`）、雷达序列号与 IP、订阅的狗身 odom 与 IMU 话题 `rt/dog_odom` / `rt/dog_imu_raw`、连接超时秒数。Go2 段是本包默认加载项。

### module/unitree_slam/config/xt16/
- **PandarXT-16.csv**：Hesai XT-16 的出厂 16 线竖直仰角表（从 +15° 到 -15°，步长 2°），驱动按此表把每线原始数据还原为三维点。
- **user_config.yaml**：XT-16 驱动用户参数，指定网卡 `eth0`、雷达 IP `192.168.123.20`、TF 坐标系 `rslidar`、点云话题 `rt/unitree/slam_lidar/points`。

### module/unitree_slam/example/
- **CMakeLists.txt**：示例工程构建脚本，设置 C++17、引入 `unitree_sdk2` 包、把 `src/keyDemo.cpp` 编译为 `keyDemo` 可执行文件并链接 `unitree_sdk2`；开发者修改 `keyDemo.cpp` 后在本目录 `mkdir build && cmake ..` 即可重新生成 `bin/keyDemo`。
- **README.md**：示例构建与运行说明，给出 `unitree_sdk2` 依赖链接、`cmake ..`、`make`、`./keyDemo eth0` 的最小启动步骤。

### module/unitree_slam/example/include/
- **json.hpp**：nlohmann/json 的单头文件版本（约 748 KB），`keyDemo` 用它把目标位姿序列化为 `{"data":{"targetPose":{...},"mode":...,"speed":...}}` 字符串传给 SLAM 服务，并解析 SLAM 回传的 `rt/slam_info` / `rt/slam_key_info`。

### module/unitree_slam/example/src/
- **keyDemo.cpp**：SLAM 示例客户端源码。定义了 `poseDate` 结构封装目标位姿、`TestClient` 继承 `unitree::robot::Client` 并注册七个 API：`ROBOT_API_ID_START_MAPPING_PL(1801)`、`END_MAPPING_PL(1802)`、`START_RELOCATION_PL(1804)`、`POSE_NAV_PL(1102)`、`PAUSE_NAV(1201)`、`RESUME_NAV(1202)`、`STOP_NODE(1901)`；通过 DDS 订阅 `rt/slam_info`（当前位姿）与 `rt/slam_key_info`（到点事件），以命令行方式实现多点循环巡航。关键方法：`Call(apiId, json_param, json_data)` 发起同步调用、`keyDetection/keyExecute` 做终端按键驱动、`taskLoopFun` 反转 poseList 实现往返。

### module/unitree_slam/lib/
- **libbasic_data.so**：SLAM 基础数据结构与工具库（预编译），上层其他 `lib*.so` 与 `unitree_slam` 均依赖；提供日志、几何类型、时间戳等基础设施。
- **libcommand_function.so**：命令与任务调度库，承载 DDS 服务端对外 API 的分发逻辑（把收到的 `apiId + json` 转成内部函数调用），与 `keyDemo.cpp` 中注册的 1801/1802/1804/1102/1201/1202/1901 一一对应。
- **libgraph_function.so**：拓扑/位姿图相关功能库，负责 SLAM 后端的节点/边管理（如关键帧与回环图操作）。
- **libgrid_map_core.so**：来自 ANYbotics `grid_map` 家族的核心库，提供多层栅格地图的底层存储、插值与序列化，服务于本包的 `gridmap_config` 功能。
- **liblivox_lidar_sdk_shared.so**：Livox 官方 Lidar SDK2 的共享版本，被 `mid360_driver` 与 `unitree_slam` 调用，实现 MID-360 的网络通信、时间同步与点云解析。
- **libodom_imu_data.so**：里程计与 IMU 数据聚合库，负责把机器人身上的 `rt/dog_odom`、`rt/dog_imu_raw`、激光 IMU 做时间对齐与坐标转换，对外输出统一的状态流给 SLAM 前端。
- **libPandarGeneralSDK.so**：Hesai Pandar 通用 SDK，被 `xt16_driver` 调用以解析 XT-16 UDP 数据包并发布点云。
- **libslam_server.so**：SLAM 服务封装，把建图、重定位、导航流程包装为 Unitree 风格的 DDS 服务端点，供 `keyDemo` 等客户端通过 `Client::Call` 调用。
- **libsport_control.so**：运动控制桥接库，负责把规划器输出的目标速度/位姿转成 `unitree_sdk2` 下 Sport/Loco 客户端可接收的指令，驱动 Go2 真正移动。

### module/unitree_slam/rviz2/
- **mapping.rviz**：建图过程的 RViz2 视图预设，订阅 `rt/unitree/slam_mapping/points` 与 `rt/unitree/slam_mapping/odom`，在上位机双击即可查看建图实时状态。
- **relocation.rviz**：重定位过程的 RViz2 视图预设，订阅 `rt/unitree/slam_relocation/points`、`.../global_map`、`.../local_map`、`.../odom`，便于核对点云对齐效果。

### services/
- **install.sh**：systemd 服务批量部署脚本，循环 `cp *.service /etc/systemd/system/`、`systemctl daemon-reload` 与 `systemctl restart`，最后打印绿色 "Finish Update"；需与 `.service` 单元文件一起使用，本目录未随包提供单元文件，需由机器人端原有系统补齐。

---

## 附：运行时数据流（要点）

- **输入话题**：`rt/unitree/slam_lidar/points`、`rt/unitree/slam_lidar/imu`（或 XT-16 的 `rt/rslidar_points` + `rt/dog_imu_raw`）、`rt/dog_odom`。
- **输出话题**：`rt/unitree/slam_mapping/{points,odom}`、`rt/unitree/slam_relocation/{points,odom,global_map,local_map}`、`rt/gridmap`、`rt/slam_info`、`rt/slam_key_info`。
- **服务名**：`slam_operate`（DDS 服务端），通过 `apiId` 区分建图/重定位/导航等操作。
  
- **对外客户端**：示例见 keyDemo.cpp，依赖 `unitree_sdk2` 编译