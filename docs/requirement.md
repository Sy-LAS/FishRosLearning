# 项目需求

## 当前任务：将 fishros 项目上传至 GitHub

### 目标
将 `/home/chuil/Desktop/fishros` 目录作为 GitHub 仓库 `FishRosLearning`（public）进行版本管理。

### 具体要求
1. **清理子模块 git**：删除 `ros2bookcode/` 中已有的 `.git` 目录，使其成为主仓库的一部分而非独立仓库
2. **GitHub 账号配置**：用户名 `SyLAS`，邮箱 `Yingkai.Shao25@student.xjtlu.edu.cn`
3. **仓库创建**：仓库名 `FishRosLearning`，public，在 GitHub 上创建
4. **Git 初始化与推送**：在主目录初始化 git，配置 `.gitignore`（参考 `ros2bookcode/.gitignore`），完成首次提交并推送
5. **验证**：确认远程仓库可正常访问，代码完整

### 参考
- `ros2bookcode/.gitignore` 中已有的忽略规则：`install/`, `build/`, `log/`, `CMakeFiles/`, `CMakeCache.txt`, `*.out`
- 项目目录约定见 `CLAUDE.md` 第6节
