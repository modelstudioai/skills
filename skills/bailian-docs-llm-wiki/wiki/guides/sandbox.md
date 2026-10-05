# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立计算资源、文件系统与网络隔离，支持按需创建、暂停、恢复与释放。其核心抽象为「模版（Template）」与「实例（Sandbox）」，通过模版统一配置运行时环境，再基于模版快速启动多个实例。

## 支持的模型/功能

Sandbox 本身不提供大模型推理能力，而是作为**运行时环境载体**，支持三类基础镜像，分别适配不同任务形态：

- **代码解释器（`code-interpreter-v1`）**：轻量 Python/Node.js 运行环境，适用于数据分析、脚本执行与结构化结果生成。推荐用于智能问答、运营分析等场景，详见 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器（`browser`）**：预装 Chromium 的浏览器执行环境，暴露 CDP 端点（`wss://<host>/ws/automation`），支持 Puppeteer、Playwright 或 BrowserUse 接入，适用于网页自动化、截图、巡检与轻量 E2E 测试。
- **全能型（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口）的复合镜像，适用于“访问网页 → 下载/截图 → 数据清洗 → 报告生成”等连续任务链路，详见 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档中多次强调 `e2b` SDK 必须固定为 `2.31.0` 版本（如 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 和 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 所述），更高版本调用 `Sandbox.create()` 会返回 HTTP 405 错误。该限制在所有相关文档中一致，非过时信息，属当前平台强制要求。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建模版后生成，必填 | 见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 所有 SDK 示例均采用此格式，见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `Authorization: Bearer <API Key>` | **真实鉴权凭证**，使用阿里云百炼 API Key（`sk-...`） | 文档明确指出 `api_key` 字段仅用于满足 E2B SDK 格式校验，**不参与业务鉴权**（见 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) 和 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)） |
| `api_key` | E2B SDK 必填字段，格式须为 `e2b_` + 十六进制字符串；推荐填 `e2b_${ALIYUN_UID}`（UID 为纯数字，天然合规） | 同上，多处文档交叉验证 |
| `timeoutMs` | 实例创建/连接超时（毫秒），浏览器类任务建议 ≥300,000（5 分钟），AIO 类建议 ≥900,000（15 分钟） | 见 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 与 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) |

## 使用方式

1. **前置准备**：开通百炼服务并完成 [服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，授予 `AliyunServiceRoleForSFMSandbox` 角色。
2. **创建模版**：在控制台选择镜像（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）、高级配置（网络白名单、环境变量、生命周期），获取 `templateCode`。
3. **获取 API Key**：在控制台「API-KEY」页生成或复制 `sk-...` 密钥。
4. **SDK 调用**：
   - 安装指定版本：`pip install "e2b==2.31.0"`（Python）或 `npm install e2b@2.31.0`（Node.js）；
   - 创建实例：传入 `api_url`、`headers={"Authorization": "Bearer <sk-...>"}`、`template` 和 `api_key`；
   - 执行操作：调用 `sbx.commands.run()`、`sbx.files.write()`、`sbx.run_code()`（需 `e2b-code-interpreter`）或 `sbx.getHost(3000)` 获取 CDP 地址；
   - 生命周期管理：`sbx.pause()` 暂停、`Sandbox.connect()` 恢复、`sbx.kill()` 释放。

## 限制和注意事项

- **生命周期限制**：实例最大存活时间与空闲超时二选一，**最长不超过 7 天**（见 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md) 和 [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)）。
- **SDK 版本强约束**：`e2b` 必须为 `2.31.0`，`e2b-code-interpreter` 必须为 `2.8.1`（Python）或 `2.6.1`（Node.js），否则创建失败（HTTP 405）。该限制在全部 SDK 相关文档中一致，属当前平台硬性要求。
- **公网 URL 安全风险**：沙箱暴露的 `wss://<host>/ws/automation` 或 noVNC 地址（`/static/vnc.html?path=/ws/livestream`）等同于访问凭证，**未启用应用层鉴权时，持有者可完全控制浏览器会话（含 Cookie、登录态）**。严禁公开分享、写入日志或前端代码（见 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 和 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md) 的警告）。
- **资源与文件限制**：生产环境需主动限制单次任务的输入文件大小/类型、下载文件总大小、命令超时及沙箱生命周期，避免资源耗尽（见各最佳实践文档的「上线建议」章节）。
- **模版不可删除条件**：若模版下存在运行中或已暂停的实例，则无法删除，需先调用 `sbx.kill()` 或控制台释放实例（见 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)）。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)


