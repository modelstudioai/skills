# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，所有实例均基于模板启动，具备独立计算资源、文件系统与网络隔离能力。它兼容 E2B SDK/API 协议，开发者可快速集成至智能体工作流中。详细设计目标与核心架构见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 本身不提供大模型推理能力，而是作为**运行时环境**支撑智能体调用外部工具（如代码解释器、浏览器、文件系统）。其能力由所选基础镜像决定：

- **代码解释器镜像**（`code-interpreter-v1`）：轻量 Python/Node.js 运行时，适用于数据分析、脚本执行与结构化结果生成。推荐用于智能问答、报表生成等场景，详见 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器镜像**（`browser`）：预装 Chromium 的浏览器环境，通过 CDP（Chrome DevTools Protocol）暴露 `wss://<host>/ws/automation` 端点，支持 Puppeteer、Playwright 或 BrowserUse 接入，适用于网页自动化、截图、巡检等任务。
- **全能型镜像**（`all-in-one`）：同时集成浏览器（3000 端口）与 Code Interpreter（5000 端口），支持“访问网页 → 下载/截图 → 数据清洗 → 导出报告”端到端链路，适用于多步骤混合任务。

> **注意**：文档 6 和文档 7 均强调“沙箱公网 URL 应视为访问凭证”，但文档 1 未明确此安全风险；实际生产中必须按 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 和 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) 中的警告执行访问控制，禁止公开分享或日志记录 URL。

## 关键参数

- `template`（必填）：模版 code，由控制台创建模版后生成，决定镜像类型、资源配置与生命周期策略。
- `api_url`：百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。
- `headers.Authorization`：真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>`（`sk-...` 格式）。
- `api_key`：E2B SDK 必填字段，仅用于满足 SDK 格式校验（需以 `e2b_` 开头且后缀为十六进制字符），**不参与业务鉴权**；推荐设为 `e2b_${ALIYUN_UID}`。
- `timeoutMs`：SDK 创建/连接实例的超时时间（毫秒），浏览器类任务建议 ≥300,000（5 分钟），AIO 类任务建议 ≥900,000（15 分钟）。

## 使用方式

1. **前置准备**：完成服务授权（SLR 角色 `AliyunServiceRoleForSFMSandbox`），获取阿里云 UID 与百炼 API Key（[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）。
2. **创建模版**：在控制台选择镜像、配置资源（1C2G 或 4C8G）、设置高级选项（如网络白名单、生命周期），生成 `templateCode`。
3. **调用 SDK**：
   - 安装固定版本 SDK：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；更高版本创建实例时返回 405 错误。
   - 对于 Code Interpreter 能力，额外安装 `e2b-code-interpreter==2.8.1`（Python）或 `@e2b/code-interpreter@2.6.1`（Node.js）。
   - 使用 `Sandbox.create()` 启动实例，通过 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()` 等方法操作数据面。
4. **管理生命周期**：支持 `pause()`（休眠保留状态）、`connect()`（恢复连接）、`kill()`（释放资源）；空闲超时与最大存活时间由模版配置，最长 7 天。

## 限制和注意事项

- **SDK 版本强约束**：所有文档（3、4、5、6、7）一致指出，`e2b>=2.32.0` 及更高版本创建实例时返回 HTTP 405 错误，必须锁定为 `2.31.0`；`e2b-code-interpreter` 也需匹配验证版本（2.8.1 / 2.6.1）。
- **资源与时间限制**：单实例最大资源配置为 4 Core｜8 GB；实例最长存活时间为 7 天（由模版生命周期配置）；命令/代码执行默认超时为 30 秒，需显式传入 `timeoutMs` 参数延长。
- **安全边界**：
  - 公网 URL（如 `wss://<sandbox-host>/ws/automation`）等同于控制权凭证，严禁泄露；
  - 模板中**不得固化敏感信息**（如账号 Cookie、API Key），应通过运行时 `envs` 注入；
  - 浏览器任务需限制域名白名单，代码任务需校验输入文件类型与大小。
- **能力边界**：模版管理（创建/更新/删除）无稳定 SDK 封装，必须通过 [Sandbox API](../../raw/application-api-reference/sandbox-api/sandbox-api-overview.md) 的管控面接口调用；数据面操作（命令、文件、代码）才推荐使用 SDK。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


