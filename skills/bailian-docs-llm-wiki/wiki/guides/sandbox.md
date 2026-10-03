# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，通过模版统一配置运行时环境，再基于模版快速启动多个隔离实例。

## 支持的模型/功能

Sandbox 本身不提供语言模型，而是作为**运行时环境**，支撑各类 AI 智能体执行具体任务。根据基础镜像不同，支持三类能力组合：

- **代码解释器镜像（`code-interpreter-v1`）**：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行、结构化结果生成等场景。推荐搭配 `e2b-code-interpreter` SDK 使用 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器镜像（`browser`）**：预装 Chromium 的浏览器服务（监听 3000 端口），支持通过 CDP 连接 Puppeteer/Playwright/BrowserUse，完成网页访问、交互、截图、PDF 生成与下载 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型镜像（`all-in-one`）**：同时集成浏览器（3000 端口）与 Code Interpreter（5000 端口），适用于需在单次会话中串联网页操作与后续数据处理的任务，如“采集 HTML → 清洗 → 生成报表” [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档 4 和文档 5 均明确指出，`e2b` SDK 必须固定为 `2.31.0` 版本，更高版本创建实例时返回 HTTP 405 错误；同理，`e2b-code-interpreter` 在 Python 中需用 `2.8.1`，在 Node.js 中对应包 `@e2b/code-interpreter` 需用 `2.6.1`。该兼容性限制是当前强制要求，非可选建议。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建模版后生成，必填。决定基础镜像、资源配置、网络策略等所有运行时行为 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 文档 2、4、5、6、7 均一致引用此格式 |
| `Authorization` header | 真实鉴权凭证，值为 `Bearer <阿里云百炼 API Key>`（`sk-...`） | 所有 SDK 调用均依赖此 header，`api_key` 字段仅用于满足 E2B SDK 格式校验 |
| `api_key` | E2B SDK 必填字段，**仅格式校验用**，必须以 `e2b_` 开头且后缀为十六进制字符（如 `e2b_${ALIYUN_UID}`）。百炼侧**完全忽略其内容**，不参与业务鉴权 | [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 与 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 均强调此点 |
| `timeoutMs` | 实例创建/连接超时（毫秒），浏览器类任务建议 ≥300000（5 分钟），AIO 类建议 ≥900000（15 分钟） | 文档 6、7 明确给出推荐值 |

## 使用方式

1. **前置准备**：开通百炼服务并完成[服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取阿里云 UID 与百炼 API Key（`sk-...`）。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）、生命周期（空闲超时或最大存活时间，最长 7 天），记录生成的 `templateCode`。
3. **初始化 SDK**：
   ```bash
   pip install "e2b==2.31.0"  # 必须指定版本
   pip install "e2b-code-interpreter==2.8.1"  # 如需 run_code
   ```
4. **创建并使用实例**：
   - 创建：`Sandbox.create(template="xxx", api_url="...", headers={"Authorization": "Bearer sk-..."})`
   - 执行命令：`sbx.commands.run("ls")`
   - 读写文件：`sbx.files.write("/path", content)` / `sbx.files.read("/path")`
   - 运行代码（Code Interpreter）：`sbx.run_code("print(1+1)")`
   - 浏览器接入：调用 `sbx.getHost(3000)` 获取公网 host，构造 `wss://<host>/ws/automation` 连接 CDP
5. **生命周期管理**：`sbx.pause()` 暂停（保留状态）、`Sandbox.connect(sandbox_id=...)` 恢复、`sbx.kill()` 彻底释放。

## 限制和注意事项

- **SDK 版本强约束**：`e2b==2.31.0` 是当前唯一稳定版本，所有文档（2、4、5、6、7）均验证并强制要求此版本，升级将导致 405 错误。
- **鉴权分离**：`api_key` 仅为 SDK 格式占位符（如 `e2b_123456`），真实鉴权**仅依赖 `Authorization: Bearer <sk-...>` header**。混淆二者将导致调用失败。
- **URL 安全风险**：沙箱公网 host（如 `xxx.cn-beijing.maas.aliyuncs.com`）是完整控制凭证，含已登录态与 Cookie。**严禁公开分享、写入日志或前端代码** [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 与 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) 均加粗警告。
- **资源与时间限制**：单实例最大资源配置为 4 Core｜8 GB；实例最长存活时间为 7 天（由模版生命周期配置）；浏览器服务 `/health` 探活、CDP 连接、页面加载、代码执行等环节需综合设置足够 `timeoutMs`。
- **noVNC 路径规范**：调试时使用 `https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true`，`path` 参数**必须以 `/` 开头且不可省略**，否则解析错误导致 404。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


