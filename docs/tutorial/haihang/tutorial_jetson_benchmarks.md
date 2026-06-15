# Jetson 基准测试工具教程

## 项目概述

本项目为 **NVIDIA 官方 Jetson 嵌入式 AI 设备基准测试工具包**。测量流行深度学习模型在 Jetson 硬件上使用 **TensorRT** 作为推理引擎的推理性能（FPS）。基准测试针对 **GPU + 2x DLA（深度学习加速器）** 硬件组合（如可用），提供设备 AI 计算吞吐量的全面衡量。

基准测试结果发布在 [NVIDIA Jetson Benchmarks 网页](https://developer.nvidia.com/embedded/jetson-benchmarks)。

**来源**: NVIDIA 官方 GitHub 仓库 `NVIDIA-AI-IOT/jetson_benchmarks`，MIT 许可证。

---

## 文件结构

```
jetson_benchmarks/
├── benchmark.py              # 主入口：编排整个基准测试流程
├── install_requirements.sh   # 安装 Python 依赖的 shell 脚本
├── README.md                 # 完整文档
├── LICENSE.md                # MIT 许可证
├── utils/
│   ├── __init__.py
│   ├── benchmark_argparser.py    # CLI 参数定义
│   ├── download_models.py        # 从 Dropbox 下载模型文件
│   ├── load_store_engine.py      # 核心引擎管理：trtexec 命令生成、构建、运行
│   ├── read_write_data.py        # 读取 CSV 配置、解析 trtexec 日志、计算 FPS
│   ├── run_benchmark_models.py   # 胶水类：读取配置、创建引擎、运行、报告结果
│   ├── utilities.py              # 系统级工具：电源模式、时钟、风扇、GPU/DLA 频率
│   └── run_xavier_maxn.sh        # Xavier MAXN 模式设置脚本
├── models/                       # 模型文件目录（默认空，需下载）
└── benchmark_csv/                # 7 个设备配置文件
    ├── nx-benchmarks.csv             # Jetson Xavier NX
    ├── xavier-benchmarks.csv         # Jetson AGX Xavier
    ├── tx2-nano-benchmarks.csv       # Jetson TX2 / Nano
    ├── orin-benchmarks.csv           # Jetson AGX Orin
    ├── orin-nano-benchmarks.csv      # Jetson Orin Nano
    ├── orin-nx-8gb-benchmarks.csv    # Jetson Orin NX 8GB
    └── orin-nx-16gb-benchmarks.csv   # Jetson Orin NX 16GB
```

---

## 支持的模型

最多 **9 个模型**（取决于设备）：

| # | 模型名称 | CSV 名称 | 分辨率 | 框架 | 类型 |
|---|----------|----------|--------|------|------|
| 1 | `inception_v4` | `inception_v4` | 299x299 | Caffe | 图像分类 |
| 2 | `vgg19` | `vgg19_N2` | 224x224 | Caffe | 图像分类 |
| 3 | `super_resolution` | `super_resolution_bsd500` | 481x321 | ONNX | 超分辨率 |
| 4 | `unet` | `unet-segmentation` | 256x256 | TensorRT UFF | 图像分割 |
| 5 | `pose_estimation` | `pose_estimation` | 256x456 | Caffe | 姿态估计 (OpenPose) |
| 6 | `tiny-yolov3` | `yolov3-tiny-416` | 608x608 | ONNX | 目标检测 |
| 7 | `resnet` | `ResNet50_224x224` | 224x224 | Caffe | 图像分类 |
| 8 | `ssd-mobilenet-v1` | `mobilenet_v1_ssd` | - | Caffe/ONNX | 目标检测 |
| 9 | `ssd-resnet34` | `ssd_resnet34_1200x1200` | 1200x1200 | Caffe | 目标检测 |

### 各设备模型可用性

| 模型 | NX | Xavier | TX2/Nano | Orin | Orin Nano | Orin NX 8GB | Orin NX 16GB |
|------|----|--------|----------|------|-----------|-------------|--------------|
| inception_v4 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| vgg19_N2 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| super_resolution | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| unet | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| pose_estimation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| yolov3-tiny | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ResNet50 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ssd-mobilenet-v1 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ssd_resnet34 | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |

---

## 安装

### 硬件要求

支持的 NVIDIA Jetson 设备：TX2、Nano、Xavier NX、AGX Xavier、Orin、Orin Nano、Orin NX

### 软件要求

- **JetPack 4.4+**（NVIDIA Jetson SDK）
- **TensorRT 7+**（必须安装在 `/usr/src/tensorrt/bin/trtexec`）
- **Python 3**
- **Python 包**: `Cython`, `numpy`, `pandas`, `matplotlib`, `cairocffi`
- **系统工具**: `wget`, `unzip`, `sudo` 权限

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/NVIDIA-AI-IOT/jetson_benchmarks.git
cd jetson_benchmarks

# 2. 创建模型目录
mkdir models

# 3. 安装 Python 依赖
sudo sh install_requirements.sh
```

`install_requirements.sh` 安装：
- `python3-pip` (apt)
- `Cython`, `numpy`, `pandas` (pip)
- `python3-matplotlib`, `python3-cairocffi` (apt)

---

## 运行基准测试

### 步骤 1: 下载模型

```bash
python3 utils/download_models.py --all \
    --csv_file_path <路径>/benchmark_csv/<设备>-benchmarks.csv \
    --save_dir <绝对路径>/models
```

模型从 Dropbox 下载，ONNX 模型为 `.zip` 归档并自动解压。

### 步骤 2: 运行基准测试

**运行所有模型**:
```bash
sudo python3 benchmark.py --all \
    --csv_file_path <路径>/benchmark_csv/<设备>-benchmarks.csv \
    --model_dir <绝对路径>/models
```

**运行单个模型**:
```bash
sudo python3 benchmark.py --model_name <模型名称> \
    --csv_file_path <路径>/benchmark_csv/<设备>-benchmarks.csv \
    --model_dir <绝对路径>/models
```

### 可选标志

| 标志 | 默认值 | 说明 |
|------|--------|------|
| `--jetson_clocks` | 否 | 通过 `jetson_clocks` 设置所有时钟为最大（Orin Nano 使用） |
| `--precision int8\|fp16` | `int8` | 推理精度（TX2/Nano 使用 `fp16`） |
| `--jetson_devkit orin\|xavier\|tx2\|nano\|xavier-nx` | `orin` | 设备类型 |
| `--power_mode <int>` | `0` (MAXN) | 电源模式索引 |
| `--gpu_freq <int>` | `1300500000` | GPU 时钟频率 (Hz) |
| `--dla_freq <int>` | `1536000000` | DLA 时钟频率 (Hz) |
| `--plot` | 否 | 生成条形图 PNG 保存到模型目录 |

---

## 设备特定示例

### Jetson AGX Orin

```bash
sudo nvpmodel -m 0  # 先设置为 MAXN 电源模式
sudo python3 benchmark.py --all \
    --csv_file_path benchmark_csv/orin-benchmarks.csv \
    --model_dir /absolute/path/to/models
```

### Jetson Orin Nano

```bash
sudo python3 benchmark.py --all \
    --csv_file_path benchmark_csv/orin-nano-benchmarks.csv \
    --model_dir /absolute/path/to/models \
    --jetson_clocks
```

### Jetson AGX Xavier

```bash
sudo python3 benchmark.py --all \
    --csv_file_path benchmark_csv/xavier-benchmarks.csv \
    --model_dir /absolute/path/to/models \
    --jetson_devkit xavier \
    --gpu_freq 1377000000 --dla_freq 1395200000 \
    --power_mode 0 --jetson_clocks
```

### Jetson TX2

```bash
sudo python3 benchmark.py --all \
    --csv_file_path benchmark_csv/tx2-nano-benchmarks.csv \
    --model_dir /absolute/path/to/models \
    --jetson_devkit tx2 \
    --gpu_freq 1122000000 --power_mode 3 --precision fp16
```

### Jetson Nano

```bash
sudo python3 benchmark.py --all \
    --csv_file_path benchmark_csv/tx2-nano-benchmarks.csv \
    --model_dir /absolute/path/to/models \
    --jetson_devkit nano \
    --gpu_freq 921600000 --power_mode 0 --precision fp16
```

---

## 基准测试执行流程（内部）

1. 提示用户关闭所有应用并按 Enter
2. 检查 TensorRT 的 `trtexec` 二进制是否存在于 `/usr/src/tensorrt/bin/trtexec`
3. 设置 Jetson 为指定电源模式和时钟频率
4. 清除 RAM 缓存（`/proc/sys/vm/drop_caches`）
5. 可选运行 `jetson_clocks` 或通过 DVFS 手动设置 GPU/DLA 频率
6. 设置风扇为最大（255）
7. 对 CSV 中每个模型：
   - 从 CSV 行读取模型配置
   - 验证模型文件存在于模型目录
   - 为每个设备（GPU、DLA0、DLA1）生成 `trtexec` 构建命令
   - 构建并保存 TensorRT 引擎文件（`.engine`）
   - 使用 Python 线程**并发**加载和运行引擎（100 次平均运行，每个引擎 180 秒持续时间）
   - 解析 `trtexec` 输出日志提取 GPU 延迟值
   - 使用**时间窗口算法**找到所有并发线程的重叠测量期（晚开始/最早结束），仅计算该有效窗口内的平均延迟
   - 计算总 FPS 为所有活跃设备的 `batch_size * (1000 / latency_ms)` 之和
   - 打印结果并清理引擎/日志文件
8. 所有模型完成后，打印汇总表并可选保存条形图
9. 重置风扇为 0 并清除 RAM

**预计运行时间**: 所有模型至少 **2 小时**。

---

## CSV 配置列说明

| 列 | 说明 |
|----|------|
| `ModelName` | 模型名称标识符 |
| `FrameWork` | 框架: `caffe`, `onnx`, 或 `tensorrt` (UFF) |
| `Devices` | 推理设备数: `1` (仅 GPU), `2` (GPU+1 DLA), 或 `3` (GPU+2 DLA) |
| `BatchSizeGPU` | GPU 推理批大小 |
| `BatchSizeDLA` | DLA 推理批大小 |
| `WS_GPU` | GPU 工作区大小 (MB) |
| `WS_DLA` | DLA 工作区大小 (MB) |
| `input` | 模型输入张量名（或 `NA`） |
| `output` | 模型输出张量名（多输出用冒号分隔） |
| `URL` | 模型文件的 Dropbox 下载 URL |

---

## 依赖项

| 依赖 | 说明 |
|------|------|
| **硬件** | 支持的 NVIDIA Jetson 设备之一 |
| **JetPack** | 4.4+ |
| **TensorRT** | 7+（必须安装在 `/usr/src/tensorrt/bin/trtexec`） |
| **Python 3** | 所有脚本使用 `python3` |
| **Python 包** | `Cython`, `numpy`, `pandas`, `matplotlib`, `cairocffi` |
| **系统工具** | `wget`, `unzip`, `sudo` 权限 |
| **Linux 内核接口** | 读写 sysfs/debugfs 路径用于时钟/风扇控制 |

---

## 注意事项

1. **需要 root/sudo 权限**: 基准测试必须用 `sudo` 运行，因为它修改电源模式、时钟频率、风扇速度和内核缓存设置
2. **TensorRT 必须预安装**: 脚本硬编码路径 `/usr/src/tensorrt/bin/trtexec`，不在此路径会立即退出
3. **推荐无头模式**: 当任何设备报告零延迟时打印"建议在无头模式下运行基准测试"，显示消耗 GPU 资源可能导致此问题
4. **长时间运行**: 所有基准测试至少 **2 小时**，每个模型引擎运行使用 `--avgRuns=100 --duration=180`（每个设备 180 秒推理）
5. **模型托管在 Dropbox**: 下载使用 `wget --auth-no-challenge --no-check-certificate`，需要网络访问 Dropbox
6. **`models/` 目录默认为空**: 用户必须创建并通过下载脚本填充
7. **精度默认值重要**: 默认为 `int8`，适用于 Xavier NX、AGX Xavier 和 Orin 设备，**TX2 和 Nano 不支持 INT8**，必须使用 `--precision fp16`
8. **时钟频率特定于设备**: 每个 Jetson 设备有不同的可用 GPU/DLA 频率，README 提供正确值和发现命令：
   - GPU: `sudo cat /sys/devices/gpu.0/devfreq/*/available_frequencies`
   - DLA: `sudo cat /sys/kernel/debug/bpmp/debug/clk/nafll_dla/max_rate`
9. **时间窗口同步**: FPS 计算复杂：在多个设备（GPU + DLA0 + DLA1）并发运行时，脚本找到所有设备活跃推理的重叠时间窗口，仅计算该窗口内的延迟，避免先完成或后启动的设备扭曲结果
10. **TensorRT 版本兼容性**: 日志解析器处理两种 `trtexec` 输出格式：TRT 7.0-8.3（包含"end to end"延迟）和 TRT 8.4+（不包含）
11. **`ssd-resnet34` 模型**: 代码中在索引 8 存在但 README 未文档化为独立 `--model_name` 选项，仅在 Orin 系列 CSV 中可用
12. **引擎和日志文件自动清理**: 每个模型运行后自动清理，除非出错，此时日志文件保留在模型目录用于调试
13. **风扇控制路径因设备而异**: 工具检查两个可能的 sysfs 路径：`/sys/devices/pwm-fan/target_pwm` 和 `/sys/devices/platform/pwm-fan`
14. **仅适用于 Jetson 硬件**: 无法在 x86/桌面 GPU 或其他平台工作，依赖 Jetson 特定 sysfs 路径、`nvpmodel`、`jetson_clocks` 和 DLA 硬件

---

## 快速检查清单

- [ ] Jetson 设备已确认为支持型号
- [ ] JetPack 4.4+ 已安装
- [ ] TensorRT 已安装在 `/usr/src/tensorrt/bin/trtexec`
- [ ] Python 3 和依赖包已安装（`sudo sh install_requirements.sh`）
- [ ] `models/` 目录已创建
- [ ] 模型已下载（`python3 utils/download_models.py`）
- [ ] 网络可访问 Dropbox（下载模型时）
- [ ] 已确认设备类型和对应的 CSV 文件
- [ ] 已确认正确的精度（`int8` 或 `fp16`）
- [ ] 已确认正确的 GPU/DLA 时钟频率
- [ ] 有 sudo 权限
- [ ] 已预留至少 2 小时运行时间
- [ ] 建议在无头模式运行（无显示器消耗 GPU）

---

## 相关资源

- **位置**: `G:\xjtlu\SURF\source\haihang\Docs\jetson_benchmarks`
- **官方仓库**: https://github.com/NVIDIA-AI-IOT/jetson_benchmarks
- **基准测试结果**: https://developer.nvidia.com/embedded/jetson-benchmarks
- **许可证**: MIT License (Copyright 2019-2020, NVIDIA CORPORATION)
