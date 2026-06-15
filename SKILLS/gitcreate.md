---
name: gitcreate
description: 从零开始将本地项目目录上传至 GitHub 的完整流程。涵盖 gh CLI 安装检查与安装、GitHub 认证（token 方式）、通过 API 创建远程仓库、git 初始化、.gitignore 配置、首次提交与推送。适用于用户要求"上传到 GitHub"、"创建 GitHub 仓库"、"初始化 git 并推送"等场景。
---

# GitHub 仓库创建与首次推送

将本地项目目录完整上传为 GitHub 公开/私有仓库，包含认证、仓库创建、git 初始化和首次推送。

## 前置信息收集

在开始前，必须向用户确认以下信息：

| 信息 | 说明 | 示例(非示例本身，用户不说的话记得问) |
|------|------|------|
| GitHub 用户名 | 注意大小写，API 返回的可能与用户自述不同 | `name`(非name本身，用户不说的话记得问) |
| GitHub 邮箱 | 用于 git config | `user@example.com`  |
| 仓库名称 | 最终 URL 的一部分 | `MyProject` |
| 仓库可见性 | public 或 private | `public` |
| 仓库描述（可选） | 一句话描述 | `Learning project` |
| 子目录是否含独立 `.git` | 若有则需先删除 | `subdir/.git` |

---

## 流程总览

```
Task 1: 检查与安装 gh CLI       → Agent 自动
Task 2: GitHub 认证              → 人机协作（人提供 token，Agent 执行认证）
Task 3: 清理子目录 git 残留      → Agent 自动
Task 4: 通过 API 创建远程仓库    → Agent 自动
Task 5: Git 初始化 + .gitignore  → Agent 自动
Task 6: 首次提交与推送           → Agent 自动
Task 7: 验证                     → Agent 自动
```

---

## Task 1: 检查与安装 gh CLI

**执行者：Agent**

### 检查是否已安装

```bash
which gh 2>/dev/null && gh --version || echo "gh NOT installed"
```

### 若未安装（Ubuntu/Debian）

需要 sudo 权限，**会要求用户输入密码**：

```bash
(type -p wget >/dev/null || (sudo apt update && sudo apt-get install wget -y)) \
  && sudo mkdir -p -m 755 /etc/apt/keyrings \
  && out=$(mktemp) && wget -nv -O "$out" https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  && cat "$out" | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
  && sudo chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && sudo apt update && sudo apt install gh -y
```

> **人工介入点**：如果系统提示输入 sudo 密码，需用户在终端中手动输入。Agent 应提前告知用户。

---

## Task 2: GitHub 认证

**执行者：人机协作**

### 方式选择

| 方式 | 优点 | 缺点 |
|------|------|------|
| **Token 认证（推荐）** | 简单直接，不依赖浏览器弹窗 | 需要用户手动生成 token |
| `gh auth login --web` | 无需手动管理 token | 依赖浏览器自动打开，沙箱环境可能卡住 |

### 推荐：Token 认证流程

#### 人工步骤

1. 打开浏览器访问：**https://github.com/settings/tokens/new**
2. 填写 **Note**（如 `project-setup`）
3. 选择 **Expiration**（建议 30 days）
4. **勾选权限**（重要！）：
   - `repo`（完整）— 用于推送代码
   - `admin:repo` — 用于创建仓库
   - `read:org` — gh CLI 要求此权限，否则 `gh auth login --with-token` 会报错
5. 点击 **Generate token**
6. 复制 token（以 `ghp_` 开头）发给 Agent

#### Agent 步骤

**方案 A：直接用 token + API（更可靠，绕过 gh CLI 的 read:org 要求）**

```bash
# 验证 token 有效性并获取真实用户名
curl -s -H "Authorization: token <TOKEN>" https://api.github.com/user | grep '"login"'
```

**方案 B：通过 gh CLI（需 token 包含 read:org 权限）**

```bash
echo "<TOKEN>" | gh auth login --with-token
gh auth status
```

> **注意**：`gh auth login --with-token` 要求 token 必须有 `read:org` 权限，否则会报 `missing required scope 'read:org'` 错误。如果用户生成的 token 没有此权限，直接用 API 方式（方案 A）即可。

### 凭证持久化

推送前配置 git credential store，避免每次推送都要输入 token：

```bash
git config credential.helper store
printf "protocol=https\nhost=github.com\nusername=<USERNAME>\npassword=<TOKEN>\n" | git credential approve
```

推送完成后，**清理远程 URL 中的 token 明文**：

```bash
git remote set-url origin https://github.com/<USERNAME>/<REPO>.git
```

---

## Task 3: 清理子目录 git 残留

**执行者：Agent**

如果子目录（如 `ros2bookcode/`）有独立的 `.git` 目录，必须先删除，否则主仓库会将其视为 submodule 或产生冲突。

```bash
# 检查子目录是否含 .git
ls -la <subdir>/.git 2>/dev/null && echo "EXISTS" || echo "CLEAN"

# 删除子目录 .git
rm -rf <subdir>/.git
```

> **安全提醒**：删除前确认用户已知晓此操作，因为子目录的独立 git 历史会丢失。

---

## Task 4: 通过 API 创建远程仓库

**执行者：Agent**

```bash
curl -s -H "Authorization: token <TOKEN>" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/user/repos \
     -d '{"name":"<REPO_NAME>","description":"<DESCRIPTION>","private":false}'
```

### 验证创建成功

```bash
curl -s -H "Authorization: token <TOKEN>" \
     https://api.github.com/repos/<USERNAME>/<REPO_NAME> | grep '"full_name"'
```

### 创建失败处理

- **401 Unauthorized**：token 无效或过期，让用户重新生成
- **422 Unprocessable**：仓库名已存在，让用户确认是否使用已有仓库或改名
- **403 Forbidden**：token 缺少 `repo` 权限

---

## Task 5: Git 初始化 + .gitignore

**执行者：Agent**

### 初始化 git

```bash
git init
git config user.name "<USERNAME>"
git config user.email "<EMAIL>"
git branch -m main
```

### 创建 .gitignore

根据项目类型编写 `.gitignore`。参考模板：

```gitignore
# 构建产物
install/
build/
log/

# CMake
CMakeFiles/
CMakeCache.txt
cmake_install.cmake
Makefile
*.out
*.exe

# 编译二进制
*.o
*.so
*.a
*.pyc
__pycache__/

# IDE / 编辑器
.vscode/
.obsidian/
.qoder/

# 系统文件
.DS_Store
Thumbs.db
```

### 验证忽略效果

```bash
git add .
git status --short | grep -E "CMakeCache|CMakeFiles|\.exe" || echo "构建产物已正确忽略"
```

---

## Task 6: 首次提交与推送

**执行者：Agent**

```bash
git add .
git commit -m "Initial commit: <project description>"
git remote add origin https://<TOKEN>@github.com/<USERNAME>/<REPO>.git
git push -u origin main
```

推送成功后立即清理 URL 中的 token：

```bash
git remote set-url origin https://github.com/<USERNAME>/<REPO>.git
```

---

## Task 7: 验证

**执行者：Agent**

### 本地验证

```bash
git log --oneline          # 确认提交存在
git remote -v              # 确认远程 URL（不含 token）
git branch -a              # 确认 main 分支跟踪 origin/main
git status                 # 确认工作区干净
```

### 远程验证

```bash
curl -s -H "Authorization: token <TOKEN>" \
     https://api.github.com/repos/<USERNAME>/<REPO>/contents/ \
     | python3 -c "import sys,json; [print(d['name']) for d in json.load(sys.stdin)]"
```

对比远程文件列表与本地顶层目录是否一致。

---

## 常见问题速查

| 问题 | 原因 | 解决 |
|------|------|------|
| `gh auth login --with-token` 报 `missing required scope 'read:org'` | token 未勾选 `read:org` | 重新生成 token 或改用 API 方式 |
| `gh auth login --web` 卡住无反应 | 沙箱/无桌面环境无法打开浏览器 | 改用 token 认证方式 |
| push 报 `Authentication failed` | token 过期或权限不足 | 重新生成 token，确保勾选 `repo` 权限 |
| `remote: Repository not found` | 仓库名拼写错误或未创建 | 检查 API 创建结果，确认用户名和仓库名 |
| 子目录 `.git` 导致 git 识别为 submodule | 嵌套 git 仓库 | 删除子目录的 `.git` |
| 推送 URL 含 token 明文 | 直接用 token 拼接 URL | `git remote set-url` 清理 |

---

## 人工 / Agent 职责对照表

| 步骤 | 人工 | Agent |
|------|------|-------|
| 提供 GitHub 用户名、邮箱、仓库名 | ✅ 提供 | — |
| 输入 sudo 密码 | ✅ 在终端输入 | — |
| 生成 GitHub token | ✅ 在浏览器操作 | — |
| 将 token 发给 Agent | ✅ 粘贴 | — |
| 检查 gh CLI 是否安装 | — | ✅ 自动检查 |
| 安装 gh CLI | — | ✅ 执行安装命令 |
| 验证 token 有效性 | — | ✅ 调用 API |
| 清理子目录 .git | — | ✅ 确认后删除 |
| 创建远程仓库 | — | ✅ 调用 API |
| Git init + .gitignore | — | ✅ 自动完成 |
| 首次提交与推送 | — | ✅ 自动完成 |
| 清理 URL 中的 token | — | ✅ 自动完成 |
| 验证推送结果 | — | ✅ 检查本地+远程 |
| 撤销/更换 token（安全） | ✅ 在 GitHub 设置中操作 | — |
