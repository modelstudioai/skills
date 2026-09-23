# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，前者定义运行时配置，后者是实际执行单元。

## 支持的模型/功能

Sandbox 本身不提供语言模型，而是作为**执行环境**与各类 Agent 配合使用。根据基础镜像类型，支持三类能力组合：

- **代码解释器镜像（`code-interpreter-v1`）**：轻量 Python/Node.js 运行时，适用于数据分析、脚本执行、文件处理等任务。推荐搭配 `e2b-code-interpreter` SDK 使用 `run_code` 或固定脚本入口方式执行 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器镜像（`browser`）**：预装 Chromium 的浏览器环境，通过 CDP（`wss://<host>/ws/automation`）接入 Puppeteer/Playwright/BrowserUse，支持网页访问、交互、截图、PDF 生成与下载 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型镜像（`all-in-one`）**：同时集成浏览器（3000 端口）与 Code Interpreter（5000 端口），支持“网页采集 → 文件落地 → 代码清洗 → 结构化输出”端到端流水线 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：所有镜像均不支持 GPU 加速，且浏览器与 AIO 镜像中的 Chromium 默认以无头模式运行，需通过 noVNC（`/static/vnc.html?path=/ws/livestream`）进行可视化调试。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建后获得，必填 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必须与工作区匹配，详见 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) |
| `Authorization` | 真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>` | `sk-...` 格式，从控制台 [API-KEY 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 |
| `api_key` | E2B SDK 必填字段，仅用于格式校验，**不参与业务鉴权**；必须满足 `e2b_` + 十六进制字符格式（如 `e2b_${ALIYUN_UID}`） | `ALIYUN_UID` 为纯数字，天然合规；详见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `timeoutMs` | 实例创建/连接超时（毫秒），AIO 场景建议 ≥900000（15 分钟） | 浏览器冷启动、页面加载与代码执行叠加耗时高 |

## 使用方式

1. **前置准备**：完成服务授权（创建 `AliyunServiceRoleForSFMSandbox` 角色），并获取阿里云百炼 API Key [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)。
2. **创建模版**：在控制台选择镜像、资源配置（1C2G 或 4C8G）、高级配置（文件挂载/网络白名单/环境变量/生命周期），生成 `templateCode`。
3. **调用 SDK**：
   - 安装固定版本：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；更高版本创建实例时返回 405 错误。
   - 对于 Code Interpreter 能力，额外安装 `e2b-code-interpreter==2.8.1`（Python）或 `@e2b/code-interpreter@2.6.1`（Node.js）。
   - 使用 `Sandbox.create()` 创建实例，`sbx.commands.run()` 执行命令，`sbx.files.write()`/`.read()` 操作文件，`sbx.run_code()` 运行代码（需对应 SDK）。
4. **生命周期管理**：调用 `sbx.pause()` 暂停（保留状态），`Sandbox.connect()` 恢复，`sbx.kill()` 彻底释放。

## 限制和注意事项

- **SDK 版本强约束**：`e2b` 必须为 `2.31.0`，`e2b-code-interpreter` 必须为 `2.8.1`（Python）或 `2.6.1`（Node.js）。更高版本因协议变更导致创建实例返回 405 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。
- **生命周期上限**：实例最长存活 7 天（由模版中「空闲超时」或「最大存活时间」控制），超时后自动释放，不可恢复。
- **公网 URL 即凭证**：浏览器/AIO 沙箱暴露的 `wss://<host>/ws/automation` 和 noVNC 地址（`/static/vnc.html?path=/ws/livestream`）等同于控制权，**严禁公开分享、写入日志或前端代码** [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **文件路径安全**：所有文件操作路径必须为绝对路径（如 `/tmp/data-analysis/`），相对路径行为未定义；输入文件需校验类型与大小，避免 DoS。
- **鉴权分离**：`api_key` 仅满足 E2B SDK 格式要求，真实鉴权依赖 `Authorization` header 中的百炼 API Key，二者不可混淆。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


