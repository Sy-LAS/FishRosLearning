# unitree_sdk2 

本教程面向初次接触 `unitree_sdk2` 的开发者，帮助快速了解 SDK 的整体结构、各目录的职责以及每一个文件的用途。`unitree_sdk2` 是宇树科技（Unitree Robotics）发布的第二代机器人 SDK，基于 DDS（Data Distribution Service，底层使用 Eclipse Cyclone DDS）通信，覆盖 Go2 / Go2W / B2 / B2W / A2 / G1 / H1 / H2 / R1 等多款机器人，提供高层运动控制客户端（`*_client`）、底层 IDL 数据类型（`idl`）以及完整的 DDS 运行时依赖（`thirdparty`）。

## 1. 目录树

下面的目录树通过 Windows `tree /F /A` 命令生成：

```text
G:\XJTLU\SURF\SDK\UNITREE_SDK2
|   .gitignore
|   CMakeLists.txt
|   LICENSE
|   README.md
|
+---.devcontainer
|       devcontainer.json
|       docker-compose.yml
|       Dockerfile.devcontainer
|
+---.github
|   \---workflows
|           c-cpp.yml
|
+---cmake
|       unitree_sdk2Config.cmake.in
|       unitree_sdk2Targets.cmake
|
+---example
|   |   CMakeLists.txt
|   |
|   +---a2
|   |   |   CMakeLists.txt
|   |   |
|   |   +---audio
|   |   |       a2_audio_client_example.cpp
|   |   |       test.wav
|   |   |       wav.hpp
|   |   |
|   |   \---sport
|   |           a2_sport_client.cpp
|   |           a2_sport_state.cpp
|   |
|   +---b2
|   |       b2_sport_client.cpp
|   |       b2_stand_example.cpp
|   |       CMakeLists.txt
|   |
|   +---b2w
|   |       b2w_sport_client.cpp
|   |       b2w_stand_example.cpp
|   |       CMakeLists.txt
|   |
|   +---g1
|   |   |   CMakeLists.txt
|   |   |
|   |   +---audio
|   |   |       g1_audio_client_example.cpp
|   |   |       test.wav
|   |   |       wav.hpp
|   |   |
|   |   +---dex3
|   |   |       g1_dex3_example.cpp
|   |   |
|   |   +---g1d
|   |   |       g1d_arm_example.cpp
|   |   |       g1_agv_client_example.cpp
|   |   |       gamepad.hpp
|   |   |
|   |   +---high_level
|   |   |       g1_arm5_sdk_dds_example.cpp
|   |   |       g1_arm7_sdk_dds_example.cpp
|   |   |       g1_arm_action_example.cpp
|   |   |       g1_loco_client_example.cpp
|   |   |       g1_userctrl_dds_example.cpp
|   |   |
|   |   \---low_level
|   |       |   g1_ankle_swing_example.cpp
|   |       |   g1_dual_arm_example.cpp
|   |       |   gamepad.hpp
|   |       |   terminations.cpp
|   |       |
|   |       \---behavior_lib
|   |               motion.seq
|   |
|   +---go2
|   |       CMakeLists.txt
|   |       go2_low_level.cpp
|   |       go2_robot_state_client.cpp
|   |       go2_sport_client.cpp
|   |       go2_stand_example.cpp
|   |       go2_trajectory_follow.cpp
|   |       go2_video_client.cpp
|   |       go2_vui_client.cpp
|   |
|   +---go2w
|   |       CMakeLists.txt
|   |       go2w_sport_client.cpp
|   |       go2w_stand_example.cpp
|   |
|   +---h1
|   |   |   CMakeLists.txt
|   |   |   README.md
|   |   |   README_zh.md
|   |   |
|   |   +---doc
|   |   |   \---images
|   |   |           ankle.png
|   |   |           tracking.png
|   |   |           tracking_circle.png
|   |   |
|   |   +---high_level
|   |   |       h1_2_arm_sdk_dds_example.cpp
|   |   |       h1_arm_sdk_dds_example.cpp
|   |   |       h1_loco_client_example.cpp
|   |   |
|   |   \---low_level
|   |           base_state.h
|   |           data_buffer.hpp
|   |           h1_27dof_example.cpp
|   |           h1_2_ankle_track.cpp
|   |           humanoid.cpp
|   |           humanoid.hpp
|   |           motors.hpp
|   |
|   +---h2
|   |   |   CMakeLists.txt
|   |   |
|   |   +---high_level
|   |   |       h2_loco_client_example.cpp
|   |   |
|   |   \---low_level
|   |           gamepad.hpp
|   |           h2_ankle_swing_example.cpp
|   |
|   +---helloworld
|   |       CMakeLists.txt
|   |       HelloWorldData.cpp
|   |       HelloWorldData.hpp
|   |       publisher.cpp
|   |       subscriber.cpp
|   |
|   +---jsonize
|   |       CMakeLists.txt
|   |       test_jsonize.cpp
|   |
|   +---r1
|   |   |   CMakeLists.txt
|   |   |
|   |   +---high_level
|   |   |       r1_loco_client_example.cpp
|   |   |
|   |   \---low_level
|   |           gamepad.hpp
|   |           r1_ankle_swing_example.cpp
|   |
|   +---state_machine
|   |   |   cfg.hpp
|   |   |   CMakeLists.txt
|   |   |   comm.h
|   |   |   conversion.hpp
|   |   |   gamepad.hpp
|   |   |   main.cpp
|   |   |   robot_controller.hpp
|   |   |   robot_interface.hpp
|   |   |   state_machine.hpp
|   |   |   user_controller.hpp
|   |   |
|   |   \---params
|   |           params.json
|   |
|   \---wireless_controller
|           advanced_gamepad.hpp
|           CMakeLists.txt
|           main.cpp
|
+---include
|   \---unitree
|       +---common
|       |   |   any.hpp
|       |   |   assert.hpp
|       |   |   block_queue.hpp
|       |   |   decl.hpp
|       |   |   error.hpp
|       |   |   exception.hpp
|       |   |   os.hpp
|       |   |   string_tool.hpp
|       |   |
|       |   +---dds
|       |   |       dds_callback.hpp
|       |   |       dds_easy_model.hpp
|       |   |       dds_entity.hpp
|       |   |       dds_error.hpp
|       |   |       dds_exception.hpp
|       |   |       dds_factory_model.hpp
|       |   |       dds_native.hpp
|       |   |       dds_parameter.hpp
|       |   |       dds_qos.hpp
|       |   |       dds_qos_parameter.hpp
|       |   |       dds_qos_policy.hpp
|       |   |       dds_qos_policy_parameter.hpp
|       |   |       dds_qos_realize.hpp
|       |   |       dds_topic_channel.hpp
|       |   |       dds_traits.hpp
|       |   |
|       |   +---filesystem
|       |   |       directory.hpp
|       |   |       file.hpp
|       |   |       filesystem.hpp
|       |   |
|       |   +---json
|       |   |       json.hpp
|       |   |       jsonize.hpp
|       |   |       json_config.hpp
|       |   |
|       |   +---lock
|       |   |       lock.hpp
|       |   |
|       |   +---log
|       |   |       log.hpp
|       |   |       log_buffer.hpp
|       |   |       log_decl.hpp
|       |   |       log_initor.hpp
|       |   |       log_keeper.hpp
|       |   |       log_logger.hpp
|       |   |       log_policy.hpp
|       |   |       log_store.hpp
|       |   |       log_writer.hpp
|       |   |
|       |   +---service
|       |   |   |   dds_service.hpp
|       |   |   |
|       |   |   \---base
|       |   |           service_application.hpp
|       |   |           service_base.hpp
|       |   |           service_config.hpp
|       |   |           service_decl.hpp
|       |   |
|       |   +---thread
|       |   |       future.hpp
|       |   |       recurrent_thread.hpp
|       |   |       thread.hpp
|       |   |       thread_decl.hpp
|       |   |       thread_pool.hpp
|       |   |       thread_task.hpp
|       |   |
|       |   \---time
|       |           sleep.hpp
|       |           time_tool.hpp
|       |
|       +---dds_wrapper
|       |   +---common
|       |   |       crc.h
|       |   |       Publisher.h
|       |   |       Subscription.h
|       |   |       unitree_joystick.hpp
|       |   |
|       |   \---robots
|       |       +---g1
|       |       |       defines.h
|       |       |       g1.h
|       |       |       g1_pub.h
|       |       |       g1_sub.h
|       |       |
|       |       \---go2
|       |               defines.h
|       |               go2.h
|       |               go2_pub.h
|       |               go2_sub.h
|       |
|       +---idl
|       |   +---go2
|       |   |       AudioData_.hpp
|       |   |       BmsCmd_.hpp
|       |   |       BmsState_.hpp
|       |   |       ConfigChangeStatus_.hpp
|       |   |       Error_.hpp
|       |   |       Go2FrontVideoData_.hpp
|       |   |       HeightMap_.hpp
|       |   |       IMUState_.hpp
|       |   |       InterfaceConfig_.hpp
|       |   |       LidarState_.hpp
|       |   |       LowCmd_.hpp
|       |   |       LowState_.hpp
|       |   |       MotorCmds_.hpp
|       |   |       MotorCmd_.hpp
|       |   |       MotorStates_.hpp
|       |   |       MotorState_.hpp
|       |   |       PathPoint_.hpp
|       |   |       Req_.hpp
|       |   |       Res_.hpp
|       |   |       SportModeCmd_.hpp
|       |   |       SportModeState_.hpp
|       |   |       TimeSpec_.hpp
|       |   |       UwbState_.hpp
|       |   |       UwbSwitch_.hpp
|       |   |       VoxelMapCompressed_.hpp
|       |   |       WirelessController_.hpp
|       |   |
|       |   +---hg
|       |   |       AgvBmsState_.hpp
|       |   |       BmsCmd_.hpp
|       |   |       BmsState_.hpp
|       |   |       HandCmd_.hpp
|       |   |       HandState_.hpp
|       |   |       IMUState_.hpp
|       |   |       LowCmd_.hpp
|       |   |       LowState_.hpp
|       |   |       MainBoardState_.hpp
|       |   |       MotorCmd_.hpp
|       |   |       MotorState_.hpp
|       |   |       PressSensorState_.hpp
|       |   |       SportModeState_.hpp
|       |   |
|       |   +---hg_doubleimu
|       |   |       doubleIMUState_.hpp
|       |   |
|       |   \---ros2
|       |           Header_.hpp
|       |           Imu_.hpp
|       |           MapMetaData_.hpp
|       |           OccupancyGrid_.hpp
|       |           Odometry_.hpp
|       |           Point32_.hpp
|       |           PointCloud2_.hpp
|       |           PointField_.hpp
|       |           PointStamped_.hpp
|       |           Point_.hpp
|       |           Pose2D_.hpp
|       |           PoseStamped_.hpp
|       |           PoseWithCovarianceStamped_.hpp
|       |           PoseWithCovariance_.hpp
|       |           Pose_.hpp
|       |           QuaternionStamped_.hpp
|       |           Quaternion_.hpp
|       |           String_.hpp
|       |           Time_.hpp
|       |           TwistStamped_.hpp
|       |           TwistWithCovarianceStamped_.hpp
|       |           TwistWithCovariance_.hpp
|       |           Twist_.hpp
|       |           Vector3_.hpp
|       |
|       \---robot
|           +---a2
|           |   +---audio
|           |   |       audio_api.hpp
|           |   |       audio_client.hpp
|           |   |       audio_error.hpp
|           |   |
|           |   \---sport
|           |           sport_api.hpp
|           |           sport_client.hpp
|           |           sport_error.hpp
|           |
|           +---b2
|           |   +---back_video
|           |   |       back_video_api.hpp
|           |   |       back_video_client.hpp
|           |   |       back_video_error.hpp
|           |   |
|           |   +---config
|           |   |       config_api.hpp
|           |   |       config_client.hpp
|           |   |       config_error.hpp
|           |   |
|           |   +---front_video
|           |   |       front_video_api.hpp
|           |   |       front_video_client.hpp
|           |   |       front_video_error.hpp
|           |   |
|           |   +---motion_switcher
|           |   |       motion_switcher_api.hpp
|           |   |       motion_switcher_client.hpp
|           |   |       motion_switcher_error.hpp
|           |   |
|           |   +---robot_state
|           |   |       robot_state_api.hpp
|           |   |       robot_state_client.hpp
|           |   |       robot_state_error.hpp
|           |   |
|           |   \---sport
|           |           sport_api.hpp
|           |           sport_client.hpp
|           |           sport_error.hpp
|           |
|           +---channel
|           |       channel_factory.hpp
|           |       channel_labor.hpp
|           |       channel_namer.hpp
|           |       channel_publisher.hpp
|           |       channel_subscriber.hpp
|           |
|           +---client
|           |       client.hpp
|           |       client_base.hpp
|           |       client_stub.hpp
|           |       lease_client.hpp
|           |
|           +---future
|           |       request_future.hpp
|           |
|           +---g1
|           |   +---agv
|           |   |       g1_agv_api.hpp
|           |   |       g1_agv_client.hpp
|           |   |       g1_agv_error.hpp
|           |   |
|           |   +---arm
|           |   |       g1_arm_action_api.hpp
|           |   |       g1_arm_action_client.hpp
|           |   |       g1_arm_action_error.hpp
|           |   |
|           |   +---audio
|           |   |       g1_audio_api.hpp
|           |   |       g1_audio_client.hpp
|           |   |       g1_audio_error.hpp
|           |   |
|           |   +---common
|           |   |       terminations.hpp
|           |   |
|           |   \---loco
|           |           g1_loco_api.hpp
|           |           g1_loco_client.hpp
|           |           g1_loco_error.hpp
|           |
|           +---go2
|           |   +---config
|           |   |       config_api.hpp
|           |   |       config_client.hpp
|           |   |       config_error.hpp
|           |   |
|           |   +---obstacles_avoid
|           |   |       obstacles_avoid_api.hpp
|           |   |       obstacles_avoid_client.hpp
|           |   |
|           |   +---public
|           |   |       jsonize_type.hpp
|           |   |
|           |   +---robot_state
|           |   |       robot_state_api.hpp
|           |   |       robot_state_client.hpp
|           |   |       robot_state_error.hpp
|           |   |
|           |   +---sport
|           |   |       sport_api.hpp
|           |   |       sport_client.hpp
|           |   |       sport_error.hpp
|           |   |
|           |   +---utrack
|           |   |       utrack_api.hpp
|           |   |       utrack_client.hpp
|           |   |
|           |   +---video
|           |   |       video_api.hpp
|           |   |       video_client.hpp
|           |   |       video_error.hpp
|           |   |
|           |   \---vui
|           |           vui_api.hpp
|           |           vui_client.hpp
|           |           vui_error.hpp
|           |
|           +---h1
|           |   \---loco
|           |           h1_loco_api.hpp
|           |           h1_loco_client.hpp
|           |           h1_loco_error.hpp
|           |
|           +---h2
|           |   \---loco
|           |           h2_loco_api.hpp
|           |           h2_loco_client.hpp
|           |           h2_loco_error.hpp
|           |
|           +---internal
|           |   |   internal.hpp
|           |   |   internal_api.hpp
|           |   |   internal_error.hpp
|           |   |   internal_request_response.hpp
|           |   |
|           |   \---internal_idl_decl
|           |           RequestHeader_.hpp
|           |           RequestIdentity_.hpp
|           |           RequestLease_.hpp
|           |           RequestPolicy_.hpp
|           |           Request_.hpp
|           |           ResponseHeader_.hpp
|           |           ResponseStatus_.hpp
|           |           Response_.hpp
|           |
|           +---r1
|           |   \---loco
|           |           r1_loco_api.hpp
|           |           r1_loco_client.hpp
|           |           r1_loco_error.hpp
|           |
|           +---serialize
|           |       serialize.hpp
|           |
|           \---server
|                   lease_server.hpp
|                   server.hpp
|                   server_base.hpp
|                   server_stub.hpp
|
+---lib
|   +---aarch64
|   |       libunitree_sdk2.a
|   |
|   \---x86_64
|           libunitree_sdk2.a
|
+---licenses
|   +---eclipse-cyclonedds
|   |   +---cyclonedds
|   |   |       LICENSE
|   |   |
|   |   \---cyclonedds-cxx
|   |           LICENSE
|   |
|   +---eclipse-iceoryx
|   |   \---iceoryx
|   |           LICENSE
|   |
|   \---Tencent
|       \---rapidjson
|               LICENSE
|
\---thirdparty
    |   CMakeLists.txt
    |
    +---include
    |   +---dds
    |   |   |   config.h
    |   |   |   dds.h
    |   |   |   export.h
    |   |   |   features.h
    |   |   |   version.h
    |   |   |
    |   |   +---ddsc
    |   |   |       (dds_basic_types.h / dds_data_allocator.h / dds_internal_api.h /
    |   |   |        dds_loan_api.h / dds_opcodes.h / dds_public_alloc.h /
    |   |   |        dds_public_error.h / dds_public_impl.h / dds_public_listener.h /
    |   |   |        dds_public_qos.h / dds_public_qosdefs.h / dds_public_status.h /
    |   |   |        dds_rhc.h / dds_statistics.h)
    |   |   |
    |   |   +---ddsi
    |   |   |       (ddsi_*.h / q_*.h / sysdeps.h 等，共约 80 个 Cyclone DDS 内部头文件)
    |   |   |
    |   |   \---ddsrt
    |   |       |   (align.h / arch.h / atomics.h / attributes.h / avl.h / bswap.h /
    |   |       |    cdtors.h / circlist.h / countargs.h / dynlib.h / endian.h /
    |   |       |    environ.h / expand_vars.h / fibheap.h / filesystem.h / heap.h /
    |   |       |    hopscotch.h / ifaddrs.h / io.h / iovec.h / log.h / md5.h / mh3.h /
    |   |       |    misc.h / netstat.h / process.h / random.h / retcode.h / rusage.h /
    |   |       |    sched.h / sockets.h / static_assert.h / string.h / strtod.h /
    |   |       |    strtol.h / sync.h / threads.h / time.h / types.h / xmlparser.h)
    |   |       |
    |   |       +---atomics\    (arm.h gcc.h msvc.h sun.h)
    |   |       +---filesystem\ (posix.h windows.h)
    |   |       +---sockets\    (posix.h windows.h)
    |   |       +---sync\       (freertos.h posix.h windows.h)
    |   |       +---threads\    (freertos.h posix.h windows.h)
    |   |       +---time\       (freertos.h)
    |   |       \---types\      (posix.h vxworks.h windows.h)
    |   |
    |   +---ddsc
    |   |       dds.h
    |   |
    |   \---ddscxx
    |       +---dds
    |       |   |   dds.hpp / features.hpp / LICENSE
    |       |   |
    |       |   +---core     (array/BuiltinTopicTypes/conformance/ddscore/Duration/Entity/
    |       |   |            Exception/External/InstanceHandle/LengthUnlimited/macros/
    |       |   |            Optional/QosProvider/Reference/refmacros/ref_traits/
    |       |   |            SafeEnumeration/TBuiltinTopicTypes/TEntity/TEntityQos/Time/
    |       |   |            TInstanceHandle/TQosProvider/types/Value/WeakReference.hpp
    |       |   |            及其 cond/detail/policy/status/xtypes 子目录)
    |       |   +---domain   (ddsdomain/discovery/DomainParticipant/DomainParticipantListener/
    |       |   |            find/TDomainParticipant.hpp 以及 detail、qos 子目录)
    |       |   +---pub      (AnyDataWriter/CoherentSet/DataWriter/DataWriterListener/
    |       |   |            ddspub/discovery/find/Publisher/PublisherListener/
    |       |   |            SuspendedPublication 等及 detail、qos 子目录)
    |       |   +---sub      (AnyDataReader/CoherentAccess/DataReader/DataReaderListener/
    |       |   |            ddssub/discovery/find/GenerationCount/LoanedSamples/Query/
    |       |   |            Rank/Sample/SampleInfo/SampleRef/SharedSamples/Subscriber 等
    |       |   |            及 cond/detail/qos/status 子目录)
    |       |   \---topic    (AnyTopic/BuiltinTopic/ContentFilteredTopic/ddstopic/
    |       |                discovery/Filter/find/MultiTopic/Topic/TopicDescription/
    |       |                TopicInstance/TopicListener/TopicTraits 等及 detail、qos 子目录)
    |       |
    |       \---org\eclipse\cyclonedds
    |               (ForwardDeclarations.hpp 及 core/domain/pub/sub/topic 等 Delegate 层)
    |
    \---lib
        +---aarch64
        |       libddsc.so / libddsc.so.0 / libddscxx.so / libddscxx.so.0
        |
        \---x86_64
                libddsc.so / libddsc.so.0 / libddscxx.so / libddscxx.so.0
```

> 说明：`thirdparty/include/dds/ddsi`、`thirdparty/include/ddscxx/**/detail` 等目录包含数量非常庞大的 Cyclone DDS 头文件（约 300+ 个），为保持可读性上面做了分组概括，完整文件名列表可直接用 `tree /F /A` 在本地查看；下文的文件说明章节会按分组描述这些文件的共同职责。

## 2. 文件作用说明

下列说明按目录分组组织。对数量庞大且遵循统一命名模式的文件（例如每个机器人模块都有的 `*_api.hpp / *_client.hpp / *_error.hpp` 三件套、Cyclone DDS 头文件等）采用**分组描述**而不是逐一重复。

### 根目录（unitree_sdk2/）

- **.gitignore**：Git 忽略规则，排除构建产物、IDE 临时文件等。
- **CMakeLists.txt**：SDK 顶层 CMake 构建脚本，定义项目名 `unitree_sdk2`、目标平台（x86_64 / aarch64）、头文件搜索路径、预编译静态库（`lib/<arch>/libunitree_sdk2.a`）以及 `thirdparty`（Cyclone DDS）依赖，并负责 `install` 规则与 `unitree_sdk2Config.cmake` 导出。
- **LICENSE**：SDK 的开源许可文件。
- **README.md**：英文版使用说明，介绍编译环境（Ubuntu 20.04 / GCC 9.4 / CMake 3.10+）、构建步骤（`cmake && make`）和安装方式。

### .devcontainer/
用于 VSCode Dev Container / Docker 开发环境。
- **Dockerfile.devcontainer**：构建开发容器的 Dockerfile，预装编译器与依赖。
- **devcontainer.json**：VSCode Remote-Containers 配置，指定容器镜像、挂载点与扩展。
- **docker-compose.yml**：通过 docker-compose 启动开发环境的服务定义。

### .github/workflows/
- **c-cpp.yml**：GitHub Actions CI 工作流，用于在 push / PR 时自动编译 C/C++ 代码以做基本验证。

### cmake/
CMake 安装与 `find_package()` 支持文件。
- **unitree_sdk2Config.cmake.in**：`find_package(unitree_sdk2)` 所使用的配置文件模板，`configure_file` 生成后安装到系统中，供下游 CMake 项目引用。
- **unitree_sdk2Targets.cmake**：导出 `unitree_sdk2` 库的 CMake 目标（imported target），用于对外暴露 include 目录与静态库文件路径。

---

### example/
SDK 示例程序根目录，按机器人型号和示例主题划分为多个子目录。

- **example/CMakeLists.txt**：示例模块的根 CMake，使用 `add_subdirectory()` 纳入各机器人 / 专题子工程。

#### example/a2/（A2 四足机器人示例）
- **a2/CMakeLists.txt**：A2 示例的构建脚本。
- **a2/audio/a2_audio_client_example.cpp**：A2 音频客户端示例，演示如何调用 `audio_client` 播放 / 录制音频。
- **a2/audio/test.wav**：示例使用的测试音频素材（二进制 WAV 文件）。
- **a2/audio/wav.hpp**：轻量 WAV 文件读写头文件，用于示例解析 `test.wav`。
- **a2/sport/a2_sport_client.cpp**：调用 A2 `sport_client` 发送运动指令（站立 / 行走等）的示例。
- **a2/sport/a2_sport_state.cpp**：订阅 A2 运动状态话题、打印 IMU / 姿态等信息的示例。

#### example/b2/（B2 四足机器人示例）
- **b2/CMakeLists.txt**：B2 示例构建脚本。
- **b2/b2_sport_client.cpp**：调用 B2 `sport_client` 的示例，演示 Damp / StandUp / Move 等典型指令。
- **b2/b2_stand_example.cpp**：最小化的 B2 起身示例。

#### example/b2w/（B2W 轮足机器人示例）
- **b2w/CMakeLists.txt**：B2W 示例构建脚本。
- **b2w/b2w_sport_client.cpp**：B2W 运动控制客户端示例，相较 B2 多了轮式运动相关调用。
- **b2w/b2w_stand_example.cpp**：B2W 起身示例。

#### example/g1/（G1 人形机器人示例，顶层 `CMakeLists.txt`）
- **g1/CMakeLists.txt**：统一管理 G1 下所有子示例的构建。
- **g1/audio/g1_audio_client_example.cpp**：G1 音频客户端示例（播放 WAV、TTS 等）。
- **g1/audio/test.wav**：G1 音频示例用的测试音频。
- **g1/audio/wav.hpp**：供 G1 音频示例使用的 WAV 读写工具头文件。
- **g1/dex3/g1_dex3_example.cpp**：G1 Dex3 灵巧手（三指 / 多指）控制示例。
- **g1/g1d/g1d_arm_example.cpp**：G1-D 构型手臂运动示例。
- **g1/g1d/g1_agv_client_example.cpp**：G1 AGV 底盘客户端示例（移动底盘运动指令）。
- **g1/g1d/gamepad.hpp**：示例内部使用的手柄按键解析工具头文件。
- **g1/high_level/g1_arm5_sdk_dds_example.cpp**：G1 五自由度手臂高层 DDS 控制示例。
- **g1/high_level/g1_arm7_sdk_dds_example.cpp**：G1 七自由度手臂高层 DDS 控制示例。
- **g1/high_level/g1_arm_action_example.cpp**：调用预置手臂动作（如挥手、握手）的示例。
- **g1/high_level/g1_loco_client_example.cpp**：G1 高层运动（loco，即 locomotion）客户端示例，演示步态切换、移动速度指令等。
- **g1/high_level/g1_userctrl_dds_example.cpp**：G1 用户自定义控制 DDS 通道示例。
- **g1/low_level/g1_ankle_swing_example.cpp**：G1 底层控制示例，通过 `LowCmd_` 直接控制脚踝电机周期摆动。
- **g1/low_level/g1_dual_arm_example.cpp**：G1 双臂底层联动示例。
- **g1/low_level/gamepad.hpp**：底层示例使用的手柄解析工具头文件。
- **g1/low_level/terminations.cpp**：底层示例的急停 / 退出信号处理实现。
- **g1/low_level/behavior_lib/motion.seq**：预录制的动作序列文件，供底层示例回放播放。

#### example/go2/（Go2 四足机器人示例）
- **go2/CMakeLists.txt**：Go2 示例构建脚本。
- **go2/go2_low_level.cpp**：Go2 底层电机控制示例（`LowCmd_` / `LowState_`）。
- **go2/go2_robot_state_client.cpp**：演示如何通过 `robot_state_client` 查询机器人服务状态。
- **go2/go2_sport_client.cpp**：Go2 高层运动客户端示例（StandUp / Damp / Move / Euler 等）。
- **go2/go2_stand_example.cpp**：最小化的 Go2 起身示例。
- **go2/go2_trajectory_follow.cpp**：让 Go2 按预定义轨迹运动的示例。
- **go2/go2_video_client.cpp**：调用 `video_client` 拉取前置摄像头图像流的示例。
- **go2/go2_vui_client.cpp**：调用 `vui_client`（机身 LED、提示音等 Visual / User Interface）的示例。

#### example/go2w/（Go2W 轮足示例）
- **go2w/CMakeLists.txt**：Go2W 示例构建脚本。
- **go2w/go2w_sport_client.cpp**：Go2W 运动控制示例（含轮式模式）。
- **go2w/go2w_stand_example.cpp**：Go2W 起身示例。

#### example/h1/（H1 人形机器人示例）
- **h1/CMakeLists.txt**：H1 示例构建脚本。
- **h1/README.md / README_zh.md**：英文 / 中文的 H1 示例说明文档，介绍各示例的运行方式与前置条件。
- **h1/doc/images/ankle.png / tracking.png / tracking_circle.png**：README 中引用的图示（踝关节坐标系、跟踪效果等）。
- **h1/high_level/h1_2_arm_sdk_dds_example.cpp**：H1-2 手臂高层 DDS 控制示例。
- **h1/high_level/h1_arm_sdk_dds_example.cpp**：H1 手臂高层 DDS 控制示例。
- **h1/high_level/h1_loco_client_example.cpp**：H1 行走高层客户端示例。
- **h1/low_level/base_state.h**：示例内使用的 IMU / Base 姿态结构体定义。
- **h1/low_level/data_buffer.hpp**：线程安全的数据缓冲模板类，用于跨线程传递最新状态样本。
- **h1/low_level/h1_27dof_example.cpp**：H1 27 自由度全身底层控制示例。
- **h1/low_level/h1_2_ankle_track.cpp**：H1-2 脚踝轨迹跟踪示例。
- **h1/low_level/humanoid.cpp / humanoid.hpp**：示例用的 `Humanoid` 辅助类，封装关节数量、初始化与状态访问等。
- **h1/low_level/motors.hpp**：H1 关节电机 ID 与类型的枚举 / 常量定义。

#### example/h2/（H2 人形机器人示例）
- **h2/CMakeLists.txt**：H2 示例构建脚本。
- **h2/high_level/h2_loco_client_example.cpp**：H2 行走高层客户端示例。
- **h2/low_level/gamepad.hpp**：H2 底层示例使用的手柄解析头文件。
- **h2/low_level/h2_ankle_swing_example.cpp**：H2 脚踝摆动底层示例。

#### example/helloworld/（DDS 基础通信示例）
- **helloworld/CMakeLists.txt**：HelloWorld 示例构建脚本。
- **helloworld/HelloWorldData.hpp / HelloWorldData.cpp**：IDL 生成或手写的 `HelloWorldData` 消息类型定义（含 CDR 序列化代码）。
- **helloworld/publisher.cpp**：向 HelloWorld 话题发布数据的最小示例。
- **helloworld/subscriber.cpp**：订阅 HelloWorld 话题并打印数据的最小示例。

#### example/jsonize/（JSON 序列化示例）
- **jsonize/CMakeLists.txt**：构建脚本。
- **jsonize/test_jsonize.cpp**：演示 `unitree::common::Jsonize` 基类把 C++ 结构序列化 / 反序列化为 JSON。

#### example/r1/（R1 机器人示例）
- **r1/CMakeLists.txt**：R1 示例构建脚本。
- **r1/high_level/r1_loco_client_example.cpp**：R1 高层行走客户端示例。
- **r1/low_level/gamepad.hpp**：R1 底层示例手柄解析工具头文件。
- **r1/low_level/r1_ankle_swing_example.cpp**：R1 脚踝摆动底层示例。

#### example/state_machine/（自定义状态机示例）
一套更接近完整应用的示例，演示如何用状态机组织用户控制逻辑。
- **state_machine/CMakeLists.txt**：构建脚本。
- **state_machine/cfg.hpp**：示例所用的全局配置结构体。
- **state_machine/comm.h**：通信相关常量与工具声明。
- **state_machine/conversion.hpp**：各类单位 / 坐标 / 数据格式的转换工具。
- **state_machine/gamepad.hpp**：手柄按键解析头文件。
- **state_machine/main.cpp**：示例入口，启动订阅 / 控制循环 / 状态机。
- **state_machine/robot_controller.hpp**：面向机器人的控制器抽象，负责把状态机输出转成下位机指令。
- **state_machine/robot_interface.hpp**：机器人抽象接口，屏蔽不同机型的 DDS 细节。
- **state_machine/state_machine.hpp**：通用状态机模板 / 基类定义。
- **state_machine/user_controller.hpp**：用户自定义控制器基类，供开发者扩展自己的控制逻辑。
- **state_machine/params/params.json**：运行期参数配置文件（控制增益、阈值等）。

#### example/wireless_controller/（无线手柄示例）
- **wireless_controller/CMakeLists.txt**：构建脚本。
- **wireless_controller/advanced_gamepad.hpp**：带长按 / 双击 / 组合键识别的高级手柄解析工具。
- **wireless_controller/main.cpp**：订阅 `WirelessController_` 话题并打印 / 响应按键事件的示例入口。

---

### include/unitree/common/
SDK 的通用基础库（跨机器人 / 跨模块）。

#### 直接位于 common/ 下的头文件
- **any.hpp**：类似 `std::any` 的通用类型擦除容器实现。
- **assert.hpp**：断言宏，封装 `UT_ASSERT` 等带信息输出的断言。
- **block_queue.hpp**：线程安全的阻塞队列模板，用于生产者-消费者模式。
- **decl.hpp**：通用宏 / 前向声明（导出符号、编译器探测等）。
- **error.hpp**：错误码基类与常用错误码常量。
- **exception.hpp**：SDK 自定义异常基类（如 `CommonException`）。
- **os.hpp**：操作系统抽象（获取进程名、PID、环境变量等）。
- **string_tool.hpp**：字符串工具函数（分割、trim、大小写转换等）。

#### common/dds/（DDS 封装层）
对 Cyclone DDS C++ API 做面向对象封装。
- **dds_callback.hpp**：DDS 回调函数包装（监听器 / 事件分发）。
- **dds_easy_model.hpp**：`EasyModel` 简化模型，便于快速创建发布者 / 订阅者。
- **dds_entity.hpp**：DDS Participant / Publisher / Subscriber / Reader / Writer 的统一实体抽象。
- **dds_error.hpp**：DDS 错误码 / 错误解析。
- **dds_exception.hpp**：DDS 专用异常类。
- **dds_factory_model.hpp**：工厂模式创建 DDS 实体的封装。
- **dds_native.hpp**：直接暴露底层 Cyclone DDS 原生接口的桥接层。
- **dds_parameter.hpp**：DDS 参数（Domain、Topic 名等）数据结构。
- **dds_qos.hpp**：QoS（服务质量）聚合配置类。
- **dds_qos_parameter.hpp / dds_qos_policy.hpp / dds_qos_policy_parameter.hpp / dds_qos_realize.hpp**：分层实现 QoS Policy 的参数描述、具体策略（Reliability / Durability 等）与落地到底层 DDS 的逻辑。
- **dds_topic_channel.hpp**：Topic 通道抽象，负责话题名拼接与 Reader/Writer 的双向绑定。
- **dds_traits.hpp**：DDS 类型萃取（Topic 名、Type 名的模板特化）。

#### common/filesystem/
- **directory.hpp**：目录操作工具（创建、遍历、删除）。
- **file.hpp**：文件读写 / 存在性判断工具。
- **filesystem.hpp**：统一入口，include 目录与文件工具并提供路径辅助函数。

#### common/json/
- **json.hpp**：对 RapidJSON 的薄封装，提供 `JSON` 类型别名与读写工具。
- **json_config.hpp**：基于 JSON 文件的配置加载 / 保存工具。
- **jsonize.hpp**：`Jsonize` 基类，子类重载 `toJson` / `fromJson` 即可自动序列化。

#### common/lock/
- **lock.hpp**：互斥锁 / 读写锁 / 作用域锁封装。

#### common/log/
SDK 日志子系统。
- **log.hpp**：日志模块对外统一入口，宏 `LOGI / LOGE` 等。
- **log_buffer.hpp**：环形日志缓冲区。
- **log_decl.hpp**：日志等级、字段声明。
- **log_initor.hpp**：日志系统初始化器。
- **log_keeper.hpp**：日志单例管理与作用域日志守护。
- **log_logger.hpp**：`Logger` 实现类，负责格式化与分发。
- **log_policy.hpp**：日志滚动策略（按大小 / 按时间）。
- **log_store.hpp**：日志存储后端（文件 / 控制台）。
- **log_writer.hpp**：实际写入磁盘 / 控制台的 Writer。

#### common/service/（通用服务框架）
- **dds_service.hpp**：基于 DDS 的服务抽象封装。
- **service/base/service_application.hpp**：服务进程级应用入口基类。
- **service/base/service_base.hpp**：单个服务的基类（生命周期 init/start/stop）。
- **service/base/service_config.hpp**：服务配置对象。
- **service/base/service_decl.hpp**：服务相关通用声明 / 宏。

#### common/thread/
- **future.hpp**：`Future` / `Promise` 轻量实现。
- **recurrent_thread.hpp**：按固定周期重复执行任务的线程类。
- **thread.hpp**：统一线程封装。
- **thread_decl.hpp**：线程相关宏 / 前向声明。
- **thread_pool.hpp**：线程池。
- **thread_task.hpp**：线程任务抽象（可提交到线程池）。

#### common/time/
- **sleep.hpp**：跨平台 sleep 工具（`SleepMs`、`SleepUs` 等）。
- **time_tool.hpp**：时间戳 / 计时 / 格式化工具。

---

### include/unitree/dds_wrapper/
面向特定机器人型号的 DDS 封装层，屏蔽 Topic 名称和 IDL 类型细节。

#### dds_wrapper/common/
- **Publisher.h**：通用 DDS 发布者模板。
- **Subscription.h**：通用 DDS 订阅者模板。
- **crc.h**：CRC 校验工具（底层指令需要校验保护）。
- **unitree_joystick.hpp**：把 `WirelessController_` 消息解析为结构化手柄按键状态的工具类。

#### dds_wrapper/robots/g1/ 与 dds_wrapper/robots/go2/
两个机器人各自提供对称的 4 个文件：
- **defines.h**：该机器人特有的 Topic 名、关节数等常量。
- **g1.h / go2.h**：机器人级封装入口，聚合该机型的 Publisher / Subscriber。
- **g1_pub.h / go2_pub.h**：该机型所有可发布话题（LowCmd、SportModeCmd 等）的封装。
- **g1_sub.h / go2_sub.h**：该机型所有可订阅话题（LowState、IMU、BMS 等）的封装。

---

### include/unitree/idl/
由 IDL 编译器生成的 CDR 消息类型头文件，命名统一以 `_.hpp` 结尾。这些文件是**自动生成**的，不应手工修改。

#### idl/go2/（Go2 及其他四足的消息类型）
涵盖机器人常用数据结构：
- **AudioData_.hpp**：音频流数据包。
- **BmsCmd_.hpp / BmsState_.hpp**：电池管理系统（Battery Management System）的指令与状态。
- **ConfigChangeStatus_.hpp**：配置变更结果。
- **Error_.hpp**：通用错误消息。
- **Go2FrontVideoData_.hpp**：前置摄像头视频帧。
- **HeightMap_.hpp**：高度图数据。
- **IMUState_.hpp**：IMU 姿态 / 角速度 / 加速度。
- **InterfaceConfig_.hpp**：接口配置项。
- **LidarState_.hpp**：激光雷达状态。
- **LowCmd_.hpp / LowState_.hpp**：底层电机指令 / 反馈。
- **MotorCmd_.hpp / MotorCmds_.hpp / MotorState_.hpp / MotorStates_.hpp**：单电机及电机数组的指令与状态。
- **PathPoint_.hpp**：轨迹路径点。
- **Req_.hpp / Res_.hpp**：通用请求 / 响应消息。
- **SportModeCmd_.hpp / SportModeState_.hpp**：高层运动指令 / 状态。
- **TimeSpec_.hpp**：时间戳结构。
- **UwbState_.hpp / UwbSwitch_.hpp**：UWB 定位模块状态 / 开关。
- **VoxelMapCompressed_.hpp**：压缩体素地图。
- **WirelessController_.hpp**：遥控手柄按键消息。

#### idl/hg/（Humanoid-General，人形机器人通用）
- **AgvBmsState_.hpp**：AGV 底盘电池状态。
- **BmsCmd_.hpp / BmsState_.hpp**：人形机电池指令 / 状态。
- **HandCmd_.hpp / HandState_.hpp**：灵巧手指令 / 状态。
- **IMUState_.hpp**：人形机 IMU 状态。
- **LowCmd_.hpp / LowState_.hpp**：人形机底层指令 / 状态（关节数量、字段不同于 go2）。
- **MainBoardState_.hpp**：主控板状态。
- **MotorCmd_.hpp / MotorState_.hpp**：单电机指令 / 状态。
- **PressSensorState_.hpp**：压力 / 触觉传感器状态。
- **SportModeState_.hpp**：高层运动状态。

#### idl/hg_doubleimu/
- **doubleIMUState_.hpp**：带双 IMU 的状态结构（适用于部分人形机构型）。

#### idl/ros2/
ROS2 标准消息的 IDL 版本，方便与 ROS2 生态对齐。
- **Header_.hpp**：`std_msgs/Header`。
- **Imu_.hpp**：`sensor_msgs/Imu`。
- **MapMetaData_.hpp / OccupancyGrid_.hpp**：`nav_msgs` 中占用栅格及其元信息。
- **Odometry_.hpp**：`nav_msgs/Odometry`。
- **Point_.hpp / Point32_.hpp / PointStamped_.hpp**：点类型。
- **PointCloud2_.hpp / PointField_.hpp**：`sensor_msgs/PointCloud2` 点云及字段描述。
- **Pose_.hpp / Pose2D_.hpp / PoseStamped_.hpp / PoseWithCovariance_.hpp / PoseWithCovarianceStamped_.hpp**：位姿及其带协方差 / 带时间戳版本。
- **Quaternion_.hpp / QuaternionStamped_.hpp**：四元数。
- **String_.hpp**：`std_msgs/String`。
- **Time_.hpp**：`builtin_interfaces/Time`。
- **Twist_.hpp / TwistStamped_.hpp / TwistWithCovariance_.hpp / TwistWithCovarianceStamped_.hpp**：速度指令。
- **Vector3_.hpp**：三维向量。

---

### include/unitree/robot/
面向具体机器人的高层客户端库。**几乎每个功能模块都由 `*_api.hpp` / `*_client.hpp` / `*_error.hpp` 三件套构成**，在下文按机器人分组说明。

**三件套通用职责**（适用于 robot/ 下所有同类文件）：
- `*_api.hpp`：声明该模块对外暴露的 API 名称常量（字符串，用作 DDS 服务 ID）以及请求 / 应答的 JSON 字段约定；可视为 IDL 级别的接口契约。
- `*_client.hpp`：客户端类定义，继承自 `ClientBase`，把 API 调用封装成同步 / 异步 C++ 方法（如 `StandUp()`、`Move()`、`PlayStream()` 等）。
- `*_error.hpp`：该模块专属的错误码枚举与字符串映射。

#### robot/a2/
- **a2/audio/{audio_api.hpp, audio_client.hpp, audio_error.hpp}**：A2 音频子系统客户端三件套。
- **a2/sport/{sport_api.hpp, sport_client.hpp, sport_error.hpp}**：A2 高层运动客户端三件套。

#### robot/b2/
- **b2/back_video/** 三件套：B2 后置视频客户端。
- **b2/config/** 三件套：B2 配置读写客户端。
- **b2/front_video/** 三件套：B2 前置视频客户端。
- **b2/motion_switcher/** 三件套：B2 运动模式切换客户端。
- **b2/robot_state/** 三件套：B2 机器人服务状态客户端。
- **b2/sport/** 三件套：B2 高层运动客户端。

#### robot/channel/（DDS 通道上层封装）
- **channel_factory.hpp**：`ChannelFactory` 单例，负责初始化 DDS Domain、创建 Participant。
- **channel_labor.hpp**：后台工作线程（IO 派发）。
- **channel_namer.hpp**：Topic / 服务名命名规则工具。
- **channel_publisher.hpp**：基于 Topic 的泛型发布者模板。
- **channel_subscriber.hpp**：基于 Topic 的泛型订阅者模板（带回调）。

#### robot/client/（客户端通用基类）
- **client.hpp**：面向用户的 Client 汇总头文件。
- **client_base.hpp**：`ClientBase` 抽象基类，封装 request/response 调度、超时、序列号管理。
- **client_stub.hpp**：客户端桩（stub）生成所需的宏 / 模板。
- **lease_client.hpp**：租约（Lease）机制的客户端，保持与机器人服务的心跳。

#### robot/future/
- **request_future.hpp**：`RequestFuture` 模板，封装异步请求的等待 / 获取结果逻辑。

#### robot/g1/
- **g1/agv/** 三件套：G1 AGV 底盘运动控制客户端。
- **g1/arm/** 三件套：G1 预置手臂动作（`g1_arm_action_*`）客户端。
- **g1/audio/** 三件套：G1 音频客户端。
- **g1/common/terminations.hpp**：G1 通用终止码 / 异常退出常量定义。
- **g1/loco/** 三件套：G1 行走 / 运动客户端（主要入口）。

#### robot/go2/
- **go2/config/** 三件套：Go2 参数配置客户端。
- **go2/obstacles_avoid/{obstacles_avoid_api.hpp, obstacles_avoid_client.hpp}**：Go2 避障开关客户端（仅 API + Client，无独立 error 文件）。
- **go2/public/jsonize_type.hpp**：Go2 公共请求 / 应答 JSON 结构的 `Jsonize` 定义。
- **go2/robot_state/** 三件套：Go2 服务状态客户端。
- **go2/sport/** 三件套：Go2 高层运动客户端。
- **go2/utrack/{utrack_api.hpp, utrack_client.hpp}**：Go2 视觉跟踪（UTrack）客户端。
- **go2/video/** 三件套：Go2 视频客户端（图传 / 录像）。
- **go2/vui/** 三件套：Go2 VUI（语音 / LED 交互）客户端。

#### robot/h1/
- **h1/loco/** 三件套：H1 行走 / 运动客户端。

#### robot/h2/
- **h2/loco/** 三件套：H2 行走 / 运动客户端。

#### robot/internal/（SDK 内部通信协议）
- **internal.hpp**：内部协议汇总 include。
- **internal_api.hpp**：内部 API 常量 / 路由表。
- **internal_error.hpp**：内部错误码。
- **internal_request_response.hpp**：内部请求 / 应答结构定义。
- **internal_idl_decl/Request_.hpp / RequestHeader_.hpp / RequestIdentity_.hpp / RequestLease_.hpp / RequestPolicy_.hpp / Response_.hpp / ResponseHeader_.hpp / ResponseStatus_.hpp**：内部 RPC 所使用的 IDL 生成消息类型头文件（CDR 序列化代码，自动生成）。

#### robot/r1/
- **r1/loco/** 三件套：R1 行走 / 运动客户端。

#### robot/serialize/
- **serialize.hpp**：请求 / 应答载荷的序列化工具（配合 JSON / IDL）。

#### robot/server/（对称的服务端抽象，供实现自定义 Server 使用）
- **lease_server.hpp**：租约服务端实现，用于发放 / 续期 Lease。
- **server.hpp**：服务端汇总 include。
- **server_base.hpp**：`ServerBase` 抽象基类，处理请求分发。
- **server_stub.hpp**：服务端桩宏 / 模板。

---

### lib/
预编译静态库产物。
- **lib/aarch64/libunitree_sdk2.a**：aarch64（如 Jetson / 机器人本体板）平台的 SDK 静态库。
- **lib/x86_64/libunitree_sdk2.a**：x86_64 平台的 SDK 静态库。

### licenses/
第三方依赖的许可证文件，仅做合规保留，无需修改。
- **eclipse-cyclonedds/cyclonedds/LICENSE**：Cyclone DDS C 核心许可证（EPL-2.0）。
- **eclipse-cyclonedds/cyclonedds-cxx/LICENSE**：Cyclone DDS C++ 绑定许可证。
- **eclipse-iceoryx/iceoryx/LICENSE**：iceoryx 共享内存传输库许可证。
- **Tencent/rapidjson/LICENSE**：RapidJSON 库许可证（MIT）。

---

### thirdparty/
第三方依赖的头文件与预编译动态库，SDK 在构建时会把其 include 暴露给上层。

- **thirdparty/CMakeLists.txt**：把 `thirdparty/include` 与 `thirdparty/lib/<arch>` 注册成 CMake 目标，供上层 `target_link_libraries` 使用。

#### thirdparty/include/dds/
Cyclone DDS C 接口总入口。
- **config.h / dds.h / export.h / features.h / version.h**：Cyclone DDS 的公共配置、主入口、符号导出宏、可选特性开关与版本号定义。

#### thirdparty/include/dds/ddsc/（DDS C API 头文件组）
统一负责 DDS 各子系统的 C 级 API：`dds_basic_types.h`（基本数据类型）、`dds_data_allocator.h`（数据分配）、`dds_internal_api.h`（内部 API）、`dds_loan_api.h`（零拷贝 Loan）、`dds_opcodes.h`（操作码）、`dds_public_alloc.h`（公共分配器）、`dds_public_error.h`（错误码）、`dds_public_impl.h`（实现辅助）、`dds_public_listener.h`（监听器）、`dds_public_qos.h` / `dds_public_qosdefs.h`（QoS 类型与定义）、`dds_public_status.h`（状态）、`dds_rhc.h`（Reader History Cache）、`dds_statistics.h`（统计信息）。

#### thirdparty/include/dds/ddsi/（DDS-RTPS 协议内部头文件组）
这些 `ddsi_*.h`、`q_*.h`、`sysdeps.h` 等共约 80 个头文件实现 DDS-RTPS 底层协议：包括实体（`ddsi_entity*.h`、`ddsi_endpoint.h`、`ddsi_participant.h`）、发现（`q_ddsi_discovery.h`、`ddsi_typelookup.h`）、传输（`ddsi_tcp.h / udp.h / raweth.h / ssl.h / shm_transport.h`）、序列化（`ddsi_serdata*.h`、`ddsi_cdrstream.h`、`ddsi_xt_*`）、安全（`ddsi_security_*.h`）、时间与生命周期（`ddsi_time.h / ddsi_lifespan.h / ddsi_deadline.h`）、队列与传输控制（`q_xmsg.h / q_xevent.h / q_whc.h`）等。`.idl` 文件（如 `ddsi_xt_typeinfo.idl`）为这些类型的 IDL 定义源文件。上述文件均属于 Cyclone DDS 内部实现，**通常不需要用户直接包含**。

#### thirdparty/include/dds/ddsrt/（DDS Runtime 跨平台抽象层）
`ddsrt` 提供了线程、同步、时间、字节序、原子操作、文件系统、Socket 等跨平台基础设施头文件：如 `atomics.h / sync.h / threads.h / time.h / sockets.h / filesystem.h / string.h / log.h / retcode.h / process.h` 等。其子目录按平台细分：
- **atomics/**（arm.h / gcc.h / msvc.h / sun.h）：不同编译器 / CPU 的原子操作实现。
- **filesystem/**（posix.h / windows.h）：文件系统在 POSIX / Windows 上的实现。
- **sockets/**（posix.h / windows.h）：Socket API 差异化适配。
- **sync/**（freertos.h / posix.h / windows.h）：同步原语（互斥、条件变量）的平台实现。
- **threads/**（freertos.h / posix.h / windows.h）：线程原语。
- **time/**（freertos.h）：时间 API（仅 FreeRTOS 特化，其他平台走默认实现）。
- **types/**（posix.h / vxworks.h / windows.h）：平台相关基础类型别名。

#### thirdparty/include/ddsc/dds.h
Cyclone DDS C 接口再导出头文件（与 `dds/dds.h` 配合，主要为路径兼容目的）。

#### thirdparty/include/ddscxx/（Cyclone DDS C++ 绑定）
这一整棵目录是 Cyclone DDS 的 C++ 实现，按 DDS 规范拆分为以下核心模块，每个模块的文件可分为**公开类**（直接使用）、`T*.hpp`（模板声明）、`detail/` 下的实现与 `qos/` 下的服务质量配置。

- **ddscxx/dds/dds.hpp / features.hpp / LICENSE**：C++ 绑定总入口、特性开关与许可证。
- **ddscxx/dds/core/**：DDS 核心类型，例如 `Entity`（所有 DDS 实体基类）、`QosProvider`（QoS 加载器）、`Duration` / `Time`（时间）、`Exception`（异常）、`InstanceHandle`（实例句柄）、`Reference` 系列（智能引用计数）、`WaitSet` / `Condition`（等待集 / 条件）、`policy/`（QoS 策略）、`status/`（状态）、`xtypes/`（XTypes 动态类型 `DynamicType / DynamicData / StructType / UnionType` 等）。`detail/` 子目录提供上述类的内部实现。
- **ddscxx/dds/domain/**：`DomainParticipant`、`DomainParticipantListener`、`discovery.hpp`、`find.hpp` 等 Domain 层 API，配套 `qos/DomainParticipantQos.hpp` 提供 QoS。
- **ddscxx/dds/pub/**：发布者侧 API —— `Publisher` / `DataWriter` / `AnyDataWriter` / `DataWriterListener` / `CoherentSet` / `SuspendedPublication` / `discovery.hpp` / `find.hpp` / `ddspub.hpp`；`qos/DataWriterQos.hpp` 与 `qos/PublisherQos.hpp` 定义 QoS。
- **ddscxx/dds/sub/**：订阅者侧 API —— `Subscriber` / `DataReader` / `AnyDataReader` / `DataReaderListener` / `LoanedSamples` / `SharedSamples` / `Sample` / `SampleInfo` / `SampleRef` / `GenerationCount` / `Rank` / `Query` / `CoherentAccess` / `ddssub.hpp`；`cond/` 下是读条件（`ReadCondition` / `QueryCondition`）；`qos/` 下是 `DataReaderQos` / `SubscriberQos`；`status/DataState.hpp` 描述样本状态。
- **ddscxx/dds/topic/**：Topic 系列 —— `Topic` / `AnyTopic` / `BuiltinTopic` / `ContentFilteredTopic` / `MultiTopic` / `TopicDescription` / `TopicInstance` / `TopicListener` / `TopicTraits` / `Filter` / `discovery.hpp` / `find.hpp` / `ddstopic.hpp`；`qos/TopicQos.hpp` 提供 QoS。
- **ddscxx/org/eclipse/cyclonedds/**：Cyclone DDS 官方实现的 **Delegate（代理实现）层**，与 `dds::` 命名空间的公开类一一对应。包括 `core/`（`EntityDelegate` / `ObjectDelegate` / `ReportUtils` / `Mutex` / `ScopedLock` / `TimeHelper` / cdr 序列化 / cond / policy / status）、`domain/`（`DomainParticipantDelegate` / `DomainWrap` / qos）、`pub/`（`PublisherDelegate` / `AnyDataWriterDelegate` / `CoherentSetDelegate` / qos）、`sub/`（`SubscriberDelegate` / `AnyDataReaderDelegate` / `BuiltinSubscriberDelegate` / `QueryDelegate` / cond / qos）、`topic/`（`BuiltinTopicDelegate` / `AnyTopicDelegate` / `CDRBlob` / `datatopic.hpp` / `discovery.hpp` / `hash.hpp` / `TopicTraits.hpp` / qos）。`ForwardDeclarations.hpp` 统一做前向声明。**这些文件由 Cyclone DDS C++ 项目提供，不应修改。**

#### thirdparty/lib/
Cyclone DDS 动态库（C 版本 `libddsc.so` 与 C++ 版本 `libddscxx.so`，带 `.0` 的为 soname 软链接），分别提供 aarch64 与 x86_64 两个平台的二进制：
- **thirdparty/lib/aarch64/libddsc.so / libddsc.so.0 / libddscxx.so / libddscxx.so.0**
- **thirdparty/lib/x86_64/libddsc.so / libddsc.so.0 / libddscxx.so / libddscxx.so.0**

---

## 附：关于自动生成文件与空文件的说明

- `include/unitree/idl/` 下所有 `*_.hpp`、以及 `include/unitree/robot/internal/internal_idl_decl/*_.hpp`、`example/helloworld/HelloWorldData.hpp/.cpp` 均为 IDL 编译器生成的 CDR 序列化代码，**不建议手工编辑**。
- `thirdparty/include/ddscxx/org/eclipse/cyclonedds/` 下的 Delegate 层头文件、`thirdparty/include/dds/ddsi/`、`thirdparty/include/dds/ddsrt/` 下的头文件来自 Cyclone DDS 上游项目，属于**外部依赖源码**。
- `lib/` 与 `thirdparty/lib/` 下的 `.a` / `.so` 为二进制产物，不包含源码。
- 目录树中未见明显空文件；`motion.seq`、`test.wav`、`*.png` 等为示例运行所需的**数据资源**而非代码文件。


