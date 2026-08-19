# duyi-douyin-video-breakdown-v3

把公开抖音链接整理成可核验的证据目录、深度拆解报告和本地 HTML 页面。

这是一个公开核心包：只保留采集、转写、关键帧、报告和 HTML 呈现能力，不包含个人知识库或远端工作台同步。运行时由 AI 先检查依赖，缺少可信公开依赖时自动安装；不要求用户先手工读安装教程。

## 能做什么

- 保存公开页面可见数据、评论和截图
- 下载公开抖音视频或页面提取出的公开媒体
- 生成带时间戳的转写和关键帧
- 分析开篇、创作者层级、营销动作、留存机制、结构和 CTA
- 生成可迁移的结构槽位、填空模板和评论选题
- 把最终 Markdown 报告渲染成自包含 HTML

## 快速开始

```bash
python3 scripts/run_breakdown.py \
  --source "https://v.douyin.com/your-link/" \
  --out-root "$HOME/douyin-video-breakdowns"
```

Runner 完成后，AI 读取证据和自动初稿，生成最终的 `完整拆解报告.md`，并在同一 run directory 写入 `report-web.json`，然后运行：

```bash
python3 scripts/finalize_breakdown.py \
  --run-dir "/path/to/run" \
  --final-report "/path/to/完整拆解报告.md"
```

默认输出 `/path/to/run/拆解报告.html`。

Windows、Linux 或不支持 MLX 的 macOS 不需要安装 `mlx_whisper`，AI 会改用普通 Whisper，并在运行时开启慢速 CPU 回退。依赖预检和平台安装路由见 [`references/runtime-dependencies.md`](references/runtime-dependencies.md)。

抖音链接采集还需要 OpenCLI CLI 和 Chrome Browser Bridge。缺少 CLI 时，AI 可以自动通过可信 npm 安装；Chrome 扩展安装和抖音登录需要用户一次确认。完整设置见 [`references/opencli-setup.md`](references/opencli-setup.md)。

## 公开边界

只读取公开页面和用户明确提供的本地素材，不访问创作者后台，不绕过权限，不把可见评论或互动数当成后台真实数据或付费验证。报告中的原话必须能回到转写或用户原稿，缺证据就标记为“素材不足”或“待核验”。

结构迁移只复用功能关系，不照搬原作者的句壳、比喻、口头禅、节奏和人设承诺。

## 私有 ASR

默认不依赖凭证。如果使用私有 Agent Plan ASR，必须显式传入 `--asr-script` 和 `--env`，这两个文件不属于本公开包，也不应提交到版本库：

```bash
python3 scripts/run_breakdown.py \
  --source "https://v.douyin.com/your-link/" \
  --use-doubao \
  --asr-script "/private/path/asr_adapter.py" \
  --asr-env "/private/path/asr.env" \
  --out-root "$HOME/douyin-video-breakdowns"
```

## 验收

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m compileall -q scripts tests
node --check scripts/collect_douyin_video.mjs
```

详见 [SKILL.md](SKILL.md) 和 `references/` 下的报告标准。

## 许可证与安全边界

本仓库自有内容采用 [CC BY-NC 4.0](LICENSE)：允许署名分享和改编，但禁止商业使用。这是源码公开（source-available）协议，不是 OSI 认可的软件开源许可证。

运行边界、凭证处理和依赖说明见 [SECURITY.md](SECURITY.md) 与
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。不要把 API Key、Cookie、
Bearer Token、环境文件、浏览器配置或私有 ASR 适配器提交到仓库。
