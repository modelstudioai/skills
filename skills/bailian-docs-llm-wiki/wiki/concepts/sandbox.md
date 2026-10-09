# 沙箱执行环境

沙箱执行环境是阿里云百炼平台提供的**隔离、可控、按需启停的云端运行时底座**，专为 AI 智能体的安全代码执行、浏览器自动化与文件处理任务设计。它不运行大语言模型，而是作为智能体的“手脚”，在独立计算资源、文件系统和网络空间中执行工具调用指令，确保多租户间强隔离与任务级资源可控。

## 在百炼平台的不同场景中如何使用

- **Managed Agents（托管智能体）**：沙箱是其默认执行环境。当智能体调用 `bash`、`read`、`write` 或 `web_fetch` 等内置工具时，所有操作均在后台自动创建并绑定的沙箱实例中完成；会话状态、临时文件、浏览器 Cookie 均持久化于该沙箱生命周期内，支持跨轮次续接。
- **LLM 应用（智能体应用/Agent 2.0）**：启用 `bash`/`code interpreter` 工具后，平台自动为其分配 `code-interpreter-v1` 或 `all-in-one` 沙箱实例；若任务涉及网页访问+截图+数据清洗（如生成日报），推荐直接选用 `all-in-one` 模版，避免多实例编排。
- **自定义开发（SDK/API 直接调用）**：开发者可通过 E2B SDK 或百炼 Sandbox API 手动创建、连接、控制沙箱实例，适用于需要精细生命周期管理（如长时爬虫、定时批处理）、自定义网络策略或集成 Puppeteer/Playwright 的场景。
- **工作流（Workflow）中的工具节点**：当工作流中配置了「代码执行」或「浏览器自动化」节点时，底层同样调度沙箱实例执行，但由平台自动管理模版选择、实例复用与超时释放，开发者无需显式编码。
- **高代码应用（Rich Code Application）**：可通过 MCP 协议或直接调用 Sandbox API，在 Python 函数中动态拉起沙箱，实现“模型决策 → 沙箱执行 → 结果回传”的闭环，适合需深度定制执行逻辑的生产级应用。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `template` / `templateID` | 模版唯一标识符（如 `tmpl-abc123`），决定镜像类型（`code-interpreter-v1`/`browser`/`all-in-one`）、资源配置（1C2G 或 4C8G）及网络策略。**创建实例必填**。 | 模版需先在控制台构建并确认 `buildStatus=ready`；自定义镜像需符合平台基础要求。 |
| `timeout` / `timeoutMs` | 实例最大存活时间（秒）或命令执行超时（毫秒）。AIO 类复杂任务建议 ≥900 秒（15 分钟）。 | 超时后默认 `pause`（保留状态），可设 `lifecycle.on_timeout="terminate"` 彻底释放。 |
| `network.allowOut` / `denyOut` | 出口网络白名单/黑名单，支持域名（`example.com`）、CIDR（`10.0.0.0/8`）、IPv4/IPv6。`denyOut` 不支持域名。 | 浏览器类任务需放行目标网站域名；敏感任务建议显式设置 `denyOut: ["0.0.0.0/0"]` 并仅白名单必要地址。 |
| `api_url` | 百炼沙箱 API 地址：`https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox`。**必须替换 `{workspace_id}`**。 | 当前仅支持 `cn-beijing` 地域；其他地域请求将失败。 |
| `Authorization: Bearer <API Key>` | **真实业务鉴权凭据**，使用百炼控制台生成的 `sk-...` API Key，通过 HTTP Header 传递。 | 此为唯一有效鉴权方式；E2B SDK 中的 `api_key` 字段仅为协议占位（须以 `e2b_` 开头），不参与鉴权。 |
| `autoPauseTime` / `maxRunningTimeout` | 实例空闲暂停时间（秒）与模版级最大运行时间（秒）。两者共存时，`maxRunningTimeout` 优先级更高。 | 合理设置可降低闲置成本；生产任务建议设为 `0`（禁用自动暂停）并手动控制生命周期。 |

## 面向开发者：简洁实用提示

- ✅ **首选 SDK**：Python 用 `pip install "e2b==2.31.0"`，Node.js 用 `npm install e2b@2.31.0` —— 高版本会返回 405 错误。
- ✅ **浏览器安全第一**：`wss://<host>/ws/automation` 是高危凭证，切勿日志打印、前端暴露或长期缓存；用完立即 `sbx.kill()`。
- ✅ **文件路径约定**：沙箱内统一使用绝对路径，如 `/mnt/session/uploads/file.pdf`（上传文件）、`/mnt/memory/my_db.csv`（挂载记忆库）。
- ✅ **调试技巧**：创建实例后，先 `sbx.commands.run("ls -l /mnt")` 确认挂载点；浏览器任务用 `sbx.getHost(3000)` 获取 host，再拼 CDP 地址。
- ⚠️ **避坑提醒**：`api_key` 字段不是密钥，只是 SDK 格式要求的占位符；真实鉴权只认 `Authorization` Header；模版未就绪（`buildStatus!=ready`）即创建实例会返回 409。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application support](../guides/application-support.md)


