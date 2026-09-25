# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，模版定义运行时配置，实例基于模版启动并承载实际任务 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 本身不提供大模型推理能力，而是作为**运行时环境**，支撑智能体调用多种能力：

- **代码执行**：通过 `code-interpreter-v1` 镜像支持 Python / Node.js 脚本运行、数据分析与结构化输出，推荐搭配 `e2b-code-interpreter` SDK 使用 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器自动化**：通过 `browser` 镜像提供 Chromium 浏览器服务（端口 3000），支持 Puppeteer、Playwright 或 BrowserUse 通过 CDP 连接，完成网页访问、交互、截图与下载 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **一体化任务（AIO）**：通过 `all-in-one` 镜像同时暴露浏览器（3000 端口）与 Code Interpreter（5000 端口），支持在单个沙箱中串联网页采集、文件下载与后续数据清洗/报告生成 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档 5、6、7 中均强调 `e2b` SDK 必须固定为 `2.31.0` 版本，更高版本创建实例时返回 HTTP 405 错误；而文档 3 的“推荐版本”节也明确验证了该约束。此为当前强制要求，非可选建议。

## 关键参数

| 参数 | 说明 | 来源/备注 |
|------|------|-----------|
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 所有 SDK 示例均使用此格式 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `Authorization` | 真实鉴权头，值为 `Bearer <阿里云百炼 API Key>`（`sk-...`） | 鉴权由百炼侧完成，`api_key` 字段仅用于 SDK 格式校验 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `api_key` | E2B SDK 必填字段，**仅格式校验用**，必须以 `e2b_` 开头且后缀为十六进制字符（如 `e2b_${ALIYUN_UID}`） | 文档 2 和 3 均明确说明百炼侧不使用该字段鉴权 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `template` | 控制台创建模版后生成的 `templateCode`，用于指定基础镜像与资源配置 | 模版管理页面直接展示该字段 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `timeoutMs` | 实例创建超时（如文档 6 推荐设为 `300_000` ms）、命令执行超时（如文档 5 示例设为 `30_000` ms）等 | 不同场景需差异化设置，AIO 场景因含浏览器冷启动，建议设为 `900_000` ms [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) |

## 使用方式

1. **前置准备**：开通百炼服务并完成 SLR 授权（角色名 `AliyunServiceRoleForSFMSandbox`）[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）、高级配置（网络白名单、生命周期等），获取 `templateCode`。
3. **获取密钥**：在控制台 API Key 页面创建或复制 `sk-...` 格式的百炼 API Key。
4. **SDK 调用**：
   - 安装固定版本：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；
   - 创建实例：传入 `api_url`、`api_key`（占位）、`headers={"Authorization": "Bearer <sk-...>"}` 和 `template`；
   - 执行操作：调用 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()`（需额外安装 `e2b-code-interpreter`）或 `sbx.getHost(3000)` 获取 CDP 地址；
   - 生命周期管理：`sbx.pause()` 暂停、`Sandbox.connect()` 恢复、`sbx.kill()` 释放。

## 限制和注意事项

- **生命周期限制**：实例最大存活时间与空闲超时二选一，**最长不超过 7 天**，超时后自动释放 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。
- **SDK 版本强约束**：`e2b` SDK 必须使用 `2.31.0`，`e2b-code-interpreter` 必须使用 `2.8.1`（Python）或 `2.6.1`（Node.js），更高版本创建实例返回 405 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。
- **公网 URL 即凭证**：沙箱暴露的浏览器 CDP 地址（`wss://<host>/ws/automation`）或 noVNC 地址（`https://<host>/static/vnc.html?path=/ws/livestream`）**等同于访问密钥**，未加应用层鉴权时，持有者可完全控制浏览器会话（含 Cookie、登录态），严禁公开分享或写入日志 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **文件路径安全**：noVNC 的 `path` 参数**必须以 `/` 开头**（如 `/ws/livestream`），相对路径会被错误解析至 `/static/ws/livestream` 导致连接失败；根路径 `/vnc.html` 返回 404 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **模版删除依赖**：模版存在运行中或已暂停的实例时，无法删除，需先调用 `sbx.kill()` 或 `sbx.pause()` 后再操作 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


