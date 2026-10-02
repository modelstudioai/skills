# sandbox

Sandbox 是阿里云百炼提供的云端安全沙箱服务，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议。每个实例拥有独立的计算资源、文件系统与网络隔离，支持按需创建、暂停、恢复与释放。其核心能力通过模版（Template）统一配置，开发者可基于不同基础镜像快速构建面向数据分析、网页自动化或混合任务的生产级 Agent 运行时 [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。

## 支持的模型/功能

Sandbox 本身不提供大语言模型，而是作为**运行时环境**支撑各类 AI 智能体执行下游任务。其功能由三种预置基础镜像定义：

- **代码解释器（`code-interpreter-v1`）**：轻量 Python/Node.js 执行环境，适用于数据分析、脚本运行与结构化结果生成。推荐用于智能问答、运营分析等场景 [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)。
- **浏览器（`browser`）**：基于 Chromium 的浏览器服务（监听 3000 端口），支持 CDP 协议接入 Puppeteer/Playwright/BrowserUse，适用于网页采集、UI 自动化、截图与巡检 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **全能型（`all-in-one`）**：集成浏览器（3000 端口）与 Code Interpreter（5000 端口）的复合环境，适用于“访问网页 → 下载产物 → 本地清洗 → 导出报告”类连续任务 [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)。

> **注意**：文档中多次强调 `e2b` SDK 必须固定为 `2.31.0` 版本（如 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md) 和 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md) 所述），更高版本调用 `Sandbox.create()` 会返回 HTTP 405 错误。该限制源于当前服务端协议兼容性，非 SDK 本身缺陷。

## 关键参数

| 参数 | 说明 | 来源与约束 |
|------|------|------------|
| `template` / `templateCode` | 模版唯一标识符，控制台创建后获得，用于实例启动 | 必填；值来自 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md) |
| `api_url` | 百炼沙箱接入地址，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox` | 必填；需替换 `{workspace_id}` 为实际工作区 ID |
| `headers.Authorization` | 鉴权凭证，格式为 `Bearer <阿里云百炼 API Key>` | **真实鉴权字段**；API Key 从控制台 [API-KEY](https://bailian.console.aliyun.com/?tab=model#/api-key) 获取 |
| `api_key` | E2B SDK 必填字段，仅用于满足 SDK 格式校验 | 值必须以 `e2b_` 开头且后续为十六进制字符（如 `e2b_123456789`）；阿里云 UID 天然满足，**不参与业务鉴权** [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md) |
| `timeoutMs` | 实例创建/连接超时（毫秒） | 浏览器类任务建议 ≥300,000；AIO 类建议 ≥900,000（含冷启动与页面加载） |

## 使用方式

1. **前置准备**：开通百炼服务并完成 [服务授权](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)，授予 `AliyunServiceRoleForSFMSandbox` 角色权限。
2. **创建模版**：在控制台 [Sandbox > 我的模版](https://bailian.console.aliyun.com/cn-beijing/sandbox/my-template) 选择镜像、资源配置（1C2G 或 4C8G）、高级配置（网络白名单、环境变量、生命周期等）。
3. **获取密钥**：在控制台左下角 [API-KEY](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建或复制 `sk-...` 格式密钥。
4. **SDK 调用**（以 Python 为例）：
   ```python
   from e2b import Sandbox  # 注意：必须使用 e2b==2.31.0

   sbx = Sandbox.create(
       api_url="https://xxx.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox",
       api_key=f"e2b_{ALIYUN_UID}",  # 占位符，满足格式即可
       headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
       template="your-template-code",
       timeoutMs=600_000,
   )
   # 执行命令、读写文件、暂停/释放等操作见 SDK 文档
   ```

## 限制和注意事项

- **生命周期限制**：实例最大存活时间为 7 天（从创建或恢复起计），空闲超时最长也为 7 天；超时后自动释放，**不支持续期** [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)。
- **SDK 版本锁定**：Python/Node.js 的 `e2b` SDK 必须使用 `2.31.0`，`e2b-code-interpreter` 必须使用 `2.8.1`（Python）或 `@e2b/code-interpreter@2.6.1`（Node.js）。高版本因协议变更导致 405 错误 [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)。
- **URL 安全风险**：沙箱公网 host（如 `xxx.sandbox.aliyuncs.com`）是完整控制凭证。**未启用应用层鉴权时，任何人持有该 URL 即可完全控制浏览器会话（含 Cookie、登录态）**。严禁公开分享、写入日志或前端代码 [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)。
- **资源与文件限制**：模版配置中可设置网络白/黑名单、文件挂载（最多 5 个）、环境变量；生产环境需主动限制单次任务的下载文件大小、类型及总输出体积，避免资源耗尽。
- **模版删除约束**：若模版关联有运行中或已暂停的实例，则无法删除，需先调用 `sbx.kill()` 或 `sbx.pause()` 清理实例 [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)。

## 来源文档

- [概述](../../raw/application-user-guide/sandbox/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/sandbox/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)
- [更新日志](../../raw/application-user-guide/sandbox/sandbox-changelog.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/sandbox/sandbox-best-practice-aio.md)


