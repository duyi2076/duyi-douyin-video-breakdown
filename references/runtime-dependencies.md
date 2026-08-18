# 运行时依赖与自动安装

本文件给执行 Skill 的 AI 读取，不要求最终用户手工照着安装。目标是：先检查，再用可信包管理器补齐，安装后验证，再继续流水线。

## 依赖分层

### 必需基础工具

- Python 3.10 或更高版本
- Node.js（链接采集入口需要）
- `ffmpeg` 和 `ffprobe`（视频、音频、关键帧处理）
- `curl`（分离媒体下载）
- `yt-dlp`（公开媒体下载兜底）
- Python 包 `markdown`（HTML 渲染）

### ASR

| 平台 | 优先工具 | AI 的处理方式 |
|---|---|---|
| Apple Silicon macOS | `mlx_whisper` | 缺少时用 `python3 -m pip install -U mlx-whisper` 安装，然后运行 `--preflight` |
| Windows | `openai-whisper` | 用 `py -m pip install -U openai-whisper` 安装，并在 Runner 加 `--allow-slow-whisper` |
| Linux | `openai-whisper` | 用 `python3 -m pip install -U openai-whisper` 安装，并在 Runner 加 `--allow-slow-whisper` |
| Intel macOS 或其他不支持 MLX 的环境 | `openai-whisper` | 同普通 Whisper 路径，不安装或强行调用 `mlx_whisper` |

当前 V3 只直接支持 `mlx_whisper` 和 `openai-whisper` 两个命令入口。不要自行把 `faster-whisper` 当成兼容替代品，除非同时修改脚本并补测试。

## 平台安装路由

先检查命令是否存在。只安装缺少的项目，不重复覆盖已有环境。

### macOS

```bash
brew install ffmpeg node
python3 -m pip install -U markdown yt-dlp
```

Apple Silicon 再安装：

```bash
python3 -m pip install -U mlx-whisper
```

不支持 MLX 的 macOS 安装：

```bash
python3 -m pip install -U openai-whisper
```

### Windows

```powershell
winget install --id Gyan.FFmpeg -e
winget install --id OpenJS.NodeJS.LTS -e
py -m pip install -U markdown yt-dlp openai-whisper
```

如果系统没有 `winget`，只在已有可信包管理器可用时改用它；不要下载来路不明的安装器。

### Linux

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg nodejs npm
python3 -m pip install -U markdown yt-dlp openai-whisper
```

如果当前用户没有管理员权限，保留明确错误，不要改系统权限或绕过发行版安全策略。

## 验证顺序

安装后至少验证：

```bash
python3 -c "import markdown; print('markdown ok')"
ffmpeg -version
ffprobe -version
yt-dlp --version
node --version
```

ASR 再按平台验证：

```bash
python3 "{SKILL_ROOT}/scripts/transcribe_with_doubao.py" --preflight
```

Windows、Linux 或普通 Whisper 路径的 `--preflight` 只检查 MLX，不应被当成唯一门禁。此时直接用一个真实本地视频运行 ASR，确认 `transcript/asr.json` 的 `ok` 为 `true` 且 `provider` 为 `openai_whisper`。

## 浏览器采集边界

抖音链接采集脚本通过 `opencli` 访问公开页面。`opencli` 可能由宿主 Agent 环境提供，不等同于 Node.js 或 npm 包。AI 应先检查 `opencli` 是否存在：

- 存在：继续链接采集。
- 缺少但当前环境有明确、可信的安装入口：安装后用 `opencli --help` 或实际公开页面采集验证。
- 缺少且没有可信安装入口：不猜包名、不装不明替代品，改用用户提供的本地视频，或把采集阶段标记为环境阻塞。

任何凭证、Cookie、环境文件和浏览器登录状态都不进入 Skill 源码、公开报告或 Git 提交。
