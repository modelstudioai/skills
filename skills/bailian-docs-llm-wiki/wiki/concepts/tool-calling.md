# 工具调用

工具调用是百炼平台中模型（尤其是 Agent 专用模型）主动识别用户意图、自主规划并执行外部能力的核心机制。它使大模型突破自身能力边界，通过标准化接口调用知识库、API、插件、函数计算等外部服务，实现“规划—调用—推理—整合”的闭环决策过程。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体应用（Agent）**：在 Agent 2.0 中，工具调用由模型端到端自主驱动——模型根据系统提示词和对话历史，动态决定是否调用、调用哪个工具、传入哪些参数，并将结果融入后续推理。所有工具（知识库、MCP、插件、AppFlow 等）统一抽象为可发现、可调度的“工具”，调用过程全程可追溯于 `trace` 日志。Agent 1.0 则采用分阶段策略（先 RAG 检索，再条件触发工具），适用于流程确定性强的场景。  
- **工作流应用（Workflow）**：工具调用以显式节点形式存在（如 API 节点、MCP 节点、插件节点、函数计算节点），由开发者通过画布编排执行顺序与数据流向，不依赖模型自动规划。节点间通过 `${节点名/输出字段}` 变量语法传递参数，支持同步阻塞与异步回调两种模式。  
- **Sandbox Agent**：开发者使用 `@tool` 装饰器在 Python 代码中声明自定义工具函数，平台将其注册为可被模型调度的工具；调用时参数自动序列化，返回值需为 JSON-serializable 对象，供模型后续解析与整合。  
- **框架集成（LlamaIndex / Spring AI Alibaba）**：通过 `tools` 参数传入工具描述列表，框架适配器自动将模型生成的 `tool_calls` 解析为实际 HTTP 请求，并透传鉴权、重试、超时等配置，屏蔽底层协议细节。  
- **Assistant API 与 SDK 调用**：在请求体中声明 `tools` 数组及 `tool_choice` 策略（如 `"auto"` 或指定工具 ID），平台在模型推理阶段自动插入工具调用逻辑，响应中返回结构化的 `tool_calls` 和 `tool_outputs` 字段，支持多轮交互式调用。

## 关键参数和配置

- **工具定义必需字段**（控制台或 SDK 中配置）：
  - `tool_id`：全局唯一标识符，用于模型识别与路由；
  - `description`：自然语言描述工具功能与输入约束（含示例），直接影响模型参数提取准确率；
  - `parameters`：OpenAPI 3.0 兼容的 JSON Schema，要求 Object 类型参数的子属性**不可为空**，嵌套层级宜扁平（≤2 层）；
- **调用控制参数**（请求级）：
  - `tool_choice`：指定调用策略，可选 `"auto"`（模型自主决策）、`"none"`（禁用工具）、或 `{ "type": "function", "function": { "name": "xxx" } }`（强制指定）；
  - `tools`：工具描述数组，每个元素包含 `type`（固定为 `"function"`）、`function`（含 `name`, `description`, `parameters`）；
- **参数传递方式**（影响模型能否正确提取）：
  - `大模型识别`：模型从用户输入中抽取参数，依赖 `description` 和 `parameters` 的清晰性；
  - `业务透传`：由上游系统通过 `biz_params`（HTTP）或 `user_defined_params`（SDK）直接注入，绕过模型抽取，更可靠；
- **鉴权配置**（自定义/MCP/插件类工具必需）：
  - 支持 `basic` / `bearer` / `appcode` 三种认证类型；
  - [Token](token.md) 可置于 `Header`（推荐）或 `Query`，调试与生产环境需保持一致。

## 面向开发者，简洁实用

- ✅ **优先使用 `业务透传`**：对关键参数（如订单 ID、用户 token），避免依赖模型抽取，直接通过 `biz_params` 传入，提升鲁棒性。  
- ✅ **工具描述要“像人说话”**：`description` 中必须包含具体示例（如 `"city": "杭州"`），避免模糊表述（如“城市名称”）。  
- ✅ **输出结构尽量扁平**：工具返回 JSON 应避免深层嵌套（如 `{"data": {"result": {"value": 42}}}`），推荐 `{"value": 42, "unit": "元"}`，便于模型直接引用。  
- ⚠️ **注意模型兼容性**：仅 `qwen-max`、`qwen-plus` 及 Agent 专用模型（如 `qwen-max-agentic`）支持工具调用；通用模型（如 `qwen-turbo`）不支持。  
- ⚠️ **调试必看 `trace`**：智能体调用失败时，首查响应中的 `trace` 字段，定位是规划失败（未生成 `tool_calls`）、调用失败（HTTP 错误），还是解析失败（返回非 JSON）。  
- ⚠️ **发布前务必“调试成功”**：工具状态必须为 **已发布 + 调试通过**，否则关联应用无法生效；删除工具将导致所有引用立即中断，不可逆。

## 关联主题页

- [llm application](../guides/llm-application.md)
- [plug in](../guides/plug-in.md)
- [agent development](../guides/agent-development.md)
- [frameworks](../api/frameworks.md)
- [more about models](../api/more-about-models.md)


