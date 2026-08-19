# OpenCLI 与 Chrome Browser Bridge

抖音链接采集需要 OpenCLI 的浏览器入口。OpenCLI 本体是公开的第三方 npm
工具，浏览器连接还需要 Chrome/Chromium 中安装 Browser Bridge 扩展，并且用户
已经在目标网站登录。

## 自动安装范围

AI 可以在当前环境缺少 `opencli` 时，用可信的 Node.js/npm 安装：

```bash
npm install -g @jackwener/opencli
opencli --version
```

如果当前环境没有 Node.js 或 npm，只使用系统已有的可信包管理器补齐，不要下载
来路不明的安装器。Node.js 的最低版本以 OpenCLI 官方安装文档为准。

## 浏览器一次性设置

CLI 安装成功后检查：

```bash
opencli doctor
opencli profile list
```

如果提示 Browser Bridge 未连接，用户需要完成一次浏览器设置：

1. 安装 OpenCLI 官方 Chrome Web Store 扩展，或安装 OpenCLIApp。
2. 在 Chrome 中打开抖音并登录目标账号。
3. 确认扩展已启用，并按 Chrome 提示允许它访问目标网站。
4. 重新运行 `opencli doctor`，直到浏览器连接正常。

AI 应直接把下面这段操作告诉用户，而不是只报“未连接”：

```text
请保持 Chrome 开着，并在 Chrome 里打开抖音、确认已经登录。
如果还没有 OpenCLI Browser Bridge，请安装官方扩展或 OpenCLIApp，并启用它。
然后在终端运行：

opencli doctor
```

如果用户有多个 Chrome Profile：

```bash
opencli profile list
opencli profile use <已配置的别名>
opencli doctor
```

如果是本地 Daemon 未运行：

```bash
opencli daemon restart
opencli doctor
```

连续两次 `doctor` 仍然失败时，停止重装和重试，把 `doctor` 的具体输出作为阻塞信息
交给用户；不要复制 Cookie 或浏览器 Profile，也不要绕过扩展权限。

如果当前 Agent 具备浏览器截图能力，AI 还应把安装过程改成截图引导：

1. 打开 OpenCLI 官方安装页或 Browser Bridge 安装页。
2. 截图标出扩展安装入口或 OpenCLIApp 下载入口。
3. 截图标出 Chrome 中扩展已启用的位置。
4. 截图标出抖音页面已打开、等待用户登录的位置。
5. 用户完成操作后，再截图或展示 `opencli doctor` 的连接结果。

截图只能展示公开安装页面和必要的操作区域。必须遮挡账号名、Cookie、Profile
标识、私聊内容、其他标签页和本地路径。浏览器截图能力不可用时，才退回到上面的
文字步骤和官方链接；不能编造截图或把终端报错截图当成安装指引。

AI 不应静默修改 Chrome 扩展、复制浏览器 Profile 或导出 Cookie 文件。浏览器
扩展安装和登录属于用户确认边界。

官方资料：

- https://github.com/jackwener/opencli
- https://github.com/jackwener/opencli/blob/main/docs/guide/installation.md
- https://github.com/jackwener/opencli/blob/main/docs/guide/browser-bridge.md

## 运行分支

- `opencli` 与 Browser Bridge 都正常：运行完整页面证据采集。
- 只有 `opencli` CLI、Browser Bridge 未连接：停止链接采集，报告具体阻塞点。
- 用户提供本地视频：跳过 OpenCLI，继续转写、抽帧和深度拆解。

OpenCLI 不是本 Skill 的源码依赖，也不随本仓库重新分发；它按自己的许可证和
更新节奏维护。
