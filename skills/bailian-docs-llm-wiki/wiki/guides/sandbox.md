# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，通过模版统一配置运行时环境，再基于模版快速生成多个隔离实例。

## 支持的模型/功能

Sandbox 不直接运行大语言模型，而是作为智能体的**执行底座**，提供三种预置基础镜像，分别适配不同任务类型：

- **代码解释器（`code-interpreter-v1`）**：轻量 Python/Node.js 运行时，适用于数据分析、脚本执行与结构化结果生成。推荐用于[使用 Code Interpreter Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)类场景。
- **浏览器（`browser`）**：预装 Chromium 的浏览器环境，暴露 CDP 端点（`wss://<host>/ws/automation`），支持 Puppeteer、Playwright 或 BrowserUse 接入，适用于网页自动化、截图、巡检等任务。
- **全能型（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口）的复合镜像，支持在同一实例中完成“访问网页 → 下载/截图 → 数据清洗 → 导出报告”的端到端链路，适用于[使用 AIO Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)类复杂任务。

> **注意**：文档 6 和文档 7 均强调沙箱公网 URL 应视为高危访问凭证，未设应用层鉴权时持有者可完全控制浏览器会话（含 Cookie 与登录态）。此安全约束在所有浏览器类镜像中一致，开发者必须自行管控 URL 分发与生命周期。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，创建实例时必填。在控制台创建模版后获得，如 `tmpl-abc123`。 | 见 [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 阿里云百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。需替换 `{workspace_id}` 为实际工作区 ID。 | 见 [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `Authorization: Bearer <API Key>` | **真实鉴权凭据**。使用阿里云百炼控制台生成的 API Key（`sk-...`），通过 HTTP Header 传递。 | 见 [快速开始](raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `api_key` | E2B SDK 必填字段，**仅用于满足 SDK 格式校验**，不参与业务鉴权。必须以 `e2b_` 开头，后接十六进制字符（如 `e2b_${ALIYUN_UID}`）。 | 见 [快速开始](raw/application-user-guide/sandbox/sandbox-quick-start.md) 和 [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `timeoutMs` | 实例创建或命令执行超时时间（毫秒）。浏览器冷启动、页面加载与代码执行均需预留足够时间，AIO 场景建议 ≥900000（15 分钟）。 | 见 [使用 Browser Use Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) |

## 使用方式

1. **前置准备**：开通百炼服务并完成[服务授权](raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取阿里云 UID 与 API Key。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）、高级配置（网络白名单、环境变量、生命周期等），生成 `templateCode`。
3. **调用 SDK 创建实例**：
   - 安装固定版本 SDK：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；更高版本创建实例时返回 405 错误。
   - 使用 `Sandbox.create()` 传入 `api_url`、`api_key`（占位）、`headers`（含真实 `Authorization`）和 `template`。
4. **数据面操作**：
   - 执行命令：`sbx.commands.run("ls -l")`
   - 读写文件：`sbx.files.write("/path", content)` / `sbx.files.read("/path")`
   - 运行代码（需 `e2b-code-interpreter`）：`sbx.run_code("print(1+1)")`
   - 浏览器接入：调用 `sbx.getHost(3000)` 获取 host，构造 `wss://<host>/ws/automation` 连接 CDP。
5. **生命周期管理**：`sbx.pause()` 暂停（保留状态）、`Sandbox.connect()` 恢复、`sbx.kill()` 彻底释放。

## 限制和注意事项

- **SDK 版本强约束**：所有文档（[快速开始](raw/application-user-guide/sandbox/sandbox-quick-start.md)、[实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)、[使用 Code Interpreter Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)、[使用 Browser Use Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)、[使用 AIO Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)）均明确要求 `e2b` SDK 固定为 `2.31.0`，更高版本创建实例时返回 405 错误。Node.js 侧 `@e2b/code-interpreter` 同样需固定为 `2.6.1`。
- **实例生命周期上限**：模版中配置的「最大存活时间」最长为 7 天，超时后自动释放，不可续期。
- **计费粒度**：按秒计费，包含「会话运行费」（按配置规格小时单价折算）与「数据保留费」（暂停或 Snapshot 占用的 GiB·小时）。
- **安全红线**：
  - 浏览器镜像的公网 URL 是完整控制凭证，禁止日志打印、前端暴露或未授权分享。
  - 登录态、Cookie、API Key 等敏感凭证必须运行时注入，严禁固化到模版镜像中。
- **能力边界**：模版管理（创建/更新/删除）无稳定 SDK 封装，需通过 raw HTTP 调用管控面 API；实例生命周期与数据面操作可通过 SDK 完成。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [计费说明](../../raw/application-user-guide/sandbox/sandbox-billing.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


