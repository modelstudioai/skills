# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，通过模版统一配置运行时环境，再基于模版启动多个隔离实例。

## 支持的模型/功能

Sandbox 不直接提供语言模型，而是作为**运行时环境**支撑智能体调用各类能力。根据基础镜像不同，支持以下功能组合：

- **代码解释器镜像（`code-interpreter-v1`）**：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行与结构化结果生成。推荐用于[使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)类任务。
- **浏览器镜像（`browser`）**：预装 Chromium 的浏览器服务（监听 3000 端口），支持通过 CDP 连接 Puppeteer/Playwright/BrowserUse，完成网页访问、交互、截图与下载。
- **全能型镜像（`all-in-one`）**：同时集成浏览器（3000 端口）与 Code Interpreter（5000 端口），支持“网页采集 → 文件保存 → 代码清洗 → 结果导出”端到端链路，适用于[使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)场景。

> **注意**：文档 6 和文档 7 均强调沙箱公网 URL 应视为访问凭证，未设应用层鉴权时持有者可完全控制浏览器会话（含 Cookie 与登录态）。该安全约束在所有浏览器类镜像中一致适用，开发者必须自行管控 URL 分发与日志记录。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建后生成，必填 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 文档 2、4、5、6、7 均明确要求此格式 |
| `Authorization: Bearer <API Key>` | **真实鉴权凭据**，使用阿里云百炼 API Key（`sk-...`） | [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 明确指出此为唯一有效鉴权方式 |
| `api_key` | E2B SDK 必填字段，仅用于满足 SDK 格式校验；**不参与百炼侧业务鉴权**，推荐填 `e2b_${ALIYUN_UID}` | 文档 2 与文档 4 均强调其占位性质，且 `ALIYUN_UID` 需为纯数字以通过十六进制校验 |
| `timeoutMs` | 实例创建/连接超时（毫秒），浏览器类任务建议 ≥300000（5 分钟），AIO 类建议 ≥900000（15 分钟） | 文档 6 与文档 7 的示例均显式设置高超时值，反映冷启动开销 |

## 使用方式

1. **前置准备**：开通百炼服务并完成[服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，获取阿里云 UID 与 API Key；
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）及高级配置（如网络白名单、生命周期）；
3. **调用 SDK**：
   - 安装固定版本 SDK：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；
   - 创建实例：传入 `api_url`、`Authorization` 头、`api_key` 占位符与 `template`；
   - 数据面操作：调用 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()`（需 `e2b-code-interpreter`）等方法；
   - 生命周期管理：`sbx.pause()` 暂停、`Sandbox.connect()` 恢复、`sbx.kill()` 释放。

> **注意**：文档 4、5、6、7 均明确指出，**更高版本的 E2B SDK（>2.31.0）在创建实例时返回 HTTP 405 错误**。此为已知兼容性限制，非配置错误。

## 限制和注意事项

- **生命周期限制**：实例空闲超时与最大存活时间二选一，**最长不超过 7 天**（见[概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)与[快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）；
- **SDK 版本锁定**：必须使用 `e2b==2.31.0`（Python）或 `e2b@2.31.0`（Node.js），更高版本不兼容；
- **鉴权分离**：`api_key` 仅为 SDK 格式占位符，**真实鉴权仅依赖 `Authorization: Bearer <百炼 API Key>`**；
- **URL 安全风险**：浏览器/AIO 镜像暴露的公网 host（如 `wss://<sandbox-host>/ws/automation`）等同于控制凭证，禁止公开分享、写入日志或前端代码；
- **noVNC 路径规范**：调试用 noVNC 地址必须为 `https://<sandbox-host>/static/vnc.html?path=/ws/livestream&autoconnect=true`，`path` 参数不可省略且必须以 `/` 开头，否则连接失败（见文档 6 与文档 7）；
- **模版删除约束**：存在运行中或已暂停实例时，模版无法删除，需先释放实例（见[模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)）。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)


