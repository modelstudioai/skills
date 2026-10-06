# 沙箱执行环境

沙箱执行环境是百炼平台提供的轻量级、隔离式、按需启停的容器化运行时，用于安全执行用户代码、浏览器脚本或 AI Agent 指令。它通过资源硬隔离（CPU/内存/网络/文件系统）和自动生命周期管理，保障多租户环境下的安全性与稳定性。

## 在百炼平台的不同场景中，这个概念如何使用

沙箱执行环境不是单一功能模块，而是贯穿多个核心能力的**统一执行底座**，在不同场景中以不同形态被调用：

- **代码解释器场景**：作为 `code_interpreter` 运行时，执行 Python 数据分析脚本（如 Pandas、Matplotlib），适用于 RAG 后处理、图表生成等任务；常通过插件（`code_interpreter` 插件）或 Managed Agents 的 `bash`/`read`/`write` 工具间接调用。
- **浏览器自动化场景**：作为 `browser_use` 运行时，启动无头 Chromium 实例，支持网页抓取、表单提交、截图等操作；典型用于智能体联网检索后的页面解析，或工作流中“获取实时网页内容”节点。
- **AI Agent 托管场景**：作为 Managed Agents 的默认执行环境（即 `cloud` 类型 Environment），承载 Agent 的多步工具调用、文件读写、依赖安装及状态持久化（通过显式 `save_state`）；此时沙箱与会话（Session）强绑定，生命周期由平台统一托管。
- **模版化应用开发场景**：通过 Sandbox API 构建自定义模版（Template），预装特定依赖（如 PySpark、Playwright）、配置网络策略或挂载私有文件，再基于该模版批量创建实例，支撑企业级定制化 AI 应用。
- **插件增强场景**：`code_interpreter` 和 `browser_use` 均以沙箱为底层实现，插件调用本质是向沙箱实例提交指令并获取结果；开发者无需感知容器细节，但需理解其隔离性与状态限制（如默认不保留文件系统）。

> ✅ 关键认知：沙箱 ≠ 模型推理服务，而是**模型能力的延伸执行层**——当大模型需要“做事情”（运行代码、打开网页、保存文件）时，沙箱就是它调用的“手”。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 典型值 |
|------|------|------|------|--------|
| `runtime` | string | 是 | 沙箱类型，决定基础镜像与预装能力 | `"code_interpreter"`, `"browser_use"`, `"aio"` |
| `timeout` | integer | 否 | 实例总生命周期（秒），超时后自动销毁或暂停 | `300`（5分钟，默认）~ `604800`（7天） |
| `max_memory_mb` | integer | 否 | 内存上限（MB），影响可运行任务规模 | `2048`（默认）~ `8192` |
| `allow_internet_access` | boolean | 否 | 是否允许公网访问（`browser_use` 和 `aio` 场景必需） | `true` / `false` |
| `template_id` | string | 否 | 复用预置或自定义模版，覆盖默认资源配置 | `"tmpl-abc123"` |
| `lifecycle.on_timeout` | string | 否 | 超时行为：`"kill"`（立即释放）或 `"pause"`（保留状态待恢复） | `"kill"`（默认） |

⚠️ 注意：
- `code_interpreter` 默认禁用公网访问，如需调用外部 API，必须显式设置 `allow_internet_access=true`；
- `browser_use` 不支持 WebSocket/WebRTC，且所有实例执行后自动销毁（AIO Sandbox 除外）；
- 使用 SDK 时，参数名统一为 snake_case（如 `max_memory_mb`）；使用 Sandbox API 时，部分字段在请求体（`allow_internet_access`）与响应体（`allowInternetAccess`）中命名不一致。

## 面向开发者，简洁实用

- **快速开始**：优先使用 `qwen-sandbox-sdk`（v0.8.0+），3 行代码即可运行 Python：
  ```python
  from qwen_sandbox import SandboxClient
  client = SandboxClient(api_key="sk-xxx")
  result = client.run(runtime="code_interpreter", code="print('Hello from sandbox!')")
  ```

- **查可用库**：不要依赖文档列表，直接运行命令确认：
  ```bash
  sandbox-sdk list-languages --runtime python311  # 查看实际预装库
  ```

- **调试技巧**：
  - 输出日志超 10 MB 会被截断 → 用 `print()` 分段输出，或重定向到临时文件后 `read`；
  - `browser_use` 报错时，优先检查 `allow_internet_access` 是否开启；
  - AIO Sandbox 中需显式调用 `save_state()` 才能跨步骤保留文件。

- **成本提示**：
  - 免费额度仅覆盖 `code_interpreter`；
  - `browser_use` 和 `aio` 需开通付费配额，建议在控制台设置用量告警。

- **进阶建议**：
  - 高频调用？构建自定义模版（Template），预装依赖 + 固定资源配置，提升启动速度；
  - 需要长时状态？用 Managed Agents 的 `cloud` Environment + Memory Store，而非裸沙箱；
  - 需要深度定制？直接调用 Sandbox API（兼容 E2B 协议），接管实例全生命周期。

## 关联主题页

- [sandbox](../guides/sandbox.md)
- [sandbox api](../api/sandbox-api.md)
- [managed agents](../guides/managed-agents.md)
- [application component api reference](../api/application-component-api-reference.md)
- [plug in](../guides/plug-in.md)


