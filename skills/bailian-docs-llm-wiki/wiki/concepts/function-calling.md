# 函数调用

函数调用（Function Calling）是百炼平台中实现大模型与外部能力协同的核心机制，指由大模型在推理过程中自主识别用户意图、生成结构化工具请求，并交由平台执行指定函数（如 MCP 服务、Skill 或自定义代码逻辑）的过程。该机制使 LLM 不再仅输出文本，而是可主动触发真实世界操作，构成 Agent 智能体“感知-决策-执行”闭环的关键一环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台并非单一 API 能力，而是贯穿多个抽象层级的统一语义行为，具体体现为：

- **Agent 场景（Managed / Flow / Sandbox）**：  
  当用户输入涉及工具需求（如“查北京今天天气”“解析附件表格”），LLM 会生成符合协议的函数调用请求（含 `name` 和 `arguments`）。平台根据 `tools` 参数配置自动路由至对应 MCP 服务或 Skill；Flow Agent 还支持在流程图中显式添加「函数节点」，手动绑定函数并传入上游节点输出作为参数——此时函数调用由编排逻辑驱动，而非纯模型决策。

- **MCP 服务集成**：  
  MCP 是函数调用的标准化载体。每个 MCP 服务注册后即成为一个可被调用的函数，其 `name`（如 `web_search`）、`description`（功能说明）和 `parameters`（JSON Schema 定义）共同构成函数签名。模型依据此签名生成合法调用，平台负责协议转换（如将 MCP 的 SSE 流转为模型可理解的 JSON 响应）。

- **Sandbox 模式**：  
  开发者可在 `main.py` 中定义任意 Python 函数（如 `def get_stock_price(symbol: str) -> dict:`），并通过 `@tool` 装饰器或 `register_tool()` 注册为可调用函数。Sandbox 运行时内置函数调度器，接收模型生成的调用请求，执行函数并返回结果——这是最灵活的函数调用形式，支持复杂状态、多步交互与异常处理。

- **Skill 调用**：  
  Skill 本质是预封装的函数包。当用户上传文件并发出匹配 `SKILL.md` 中 `description` 的指令（如“把 PDF 转成 Word”），平台自动触发对应 Skill 的执行函数，完成文件解析、转换等操作。调用过程对开发者透明，但需确保 `description` 描述精准以提升触发准确率。

> ⚠️ 注意：函数调用始终是**同步阻塞式**（当前所有 Agent 类型均不支持异步回调或后台任务）。模型必须等待函数执行完成并返回结果后，才能继续生成后续响应。

## 关键参数和配置

| 参数/配置 | 位置 | 说明 |
|-----------|------|------|
| `tools` | Agent API 请求体（`/v1/agents/{agent_id}/chat`） | 必填数组，声明本次对话中可用的函数列表。格式为 `[{ "type": "mcp", "name": "xxx" }]` 或 `[{ "type": "skill", "skill_id": "yyy" }]`。`type` 决定函数来源，`name`/`skill_id` 为唯一标识。 |
| `function_call` | （可选）Agent API 请求体 | 控制调用行为：<br>• `"auto"`（默认）：模型自主决定是否调用及调用哪个函数；<br>• `{"name": "xxx"}`：强制模型仅调用指定函数（适用于确定性工作流）；<br>• `"none"`：禁用函数调用，仅文本生成。 |
| `parameters`（JSON Schema） | MCP/Skill 元信息 | 定义函数入参结构。MCP 在服务注册时通过 OpenAPI Spec 声明；Skill 在 `SKILL.md` 中用 YAML 描述。模型严格按此 Schema 生成 `arguments` 字符串。 |
| `timeout_ms` | Agent 创建或调用参数 | 函数执行超时时间（毫秒）。Flow Agent 默认 30s，Sandbox 最高支持 120s。超时将中断执行并返回错误。 |
| `enable_sandbox` | Agent 配置项 | 若函数需在 Sandbox 中运行（如自定义 Python 函数），必须显式设置为 `true`，否则调用失败。 |

## 面向开发者，简洁实用

- ✅ **调试建议**：开启 `enable_tracing: true`，查看完整调用链路（模型生成的 `function_call` → 平台分发日志 → 函数执行耗时与返回值），快速定位是模型未识别意图、参数生成错误，还是函数本身异常。
- ✅ **参数安全**：所有函数调用参数均经平台校验。若模型生成的 `arguments` 不符合 `parameters` Schema，平台将自动重试或返回 `invalid_function_call` 错误，无需在函数内做二次校验。
- ✅ **错误处理**：函数执行失败（如网络超时、HTTP 4xx/5xx）时，平台统一返回结构化错误信息（含 `error_code` 和 `message`），模型可据此生成友好提示（如“天气服务暂时不可用，请稍后再试”）。
- ❌ **禁止行为**：不得在函数内部发起新的函数调用（禁止嵌套调用）；避免在函数中执行长耗时计算（建议拆分为[异步任务](asynchronous-task.md)+轮询）；禁止访问 `/tmp` 以外的本地路径或内网地址。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [agent development](../guides/agent-development.md)
- [agent store](../guides/agent-store.md)
- [more about models](../api/more-about-models.md)


