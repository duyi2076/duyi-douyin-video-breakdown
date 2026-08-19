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
3. 重新运行 `opencli doctor`，直到浏览器连接正常。

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
