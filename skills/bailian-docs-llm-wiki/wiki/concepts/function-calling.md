# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化工具调用请求的核心能力。它使模型能根据对话上下文，自主决定是否调用外部工具、选择具体工具，并精确构造符合 OpenAPI 规范的参数，从而突破纯文本生成的边界，实现搜索、计算、代码执行、API 集成等真实世界操作。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用不是独立服务，而是贯穿多个能力层的底层机制，其行为和控制粒度因使用场景而异：

- **Agent（智能体）场景**：模型自动触发函数调用。开发者通过 `input.tools` 提供工具 Schema（含 `function.name`、`description` 和 `parameters`），模型在推理过程中动态生成 `tool_calls` 数组（含 `name` 和 `arguments`）。调用结果需由开发者或平台注入 `observation` 后，模型继续推理，形成「规划→调用→观察→反思」闭环。深度限制为 8 层嵌套调用。

- **插件（Plug-in）场景**：函数调用即“工具调用”，插件是工具的集合封装。官方/三方插件以预置工具 ID（如 `"search"`、`"calculator"`）形式注册；自定义插件则需明确定义 `tool_path`、`in_params`（含 `passing_method` 区分“大模型识别”或“业务透传”）和 `out_params`。调用时，参数可由模型生成（智能体模式），也可由工作流节点或 API 显式传入（确定性编排模式）。

- **Application Call（应用调用）场景**：函数调用作为高级功能被集成。在调用已发布的 Agent 或 Workflow 时，可通过 `biz_params` 或 `extra_body.biz_params` 透传插件所需参数（如用户级 [Token](token.md)、业务上下文），平台自动完成工具路由与鉴权，无需在请求体中重复定义工具 Schema。

- **Toolkits & Frameworks（工具包）场景**：[OpenAI 兼容接口](openai-compatibility.md)（如 `/v1/chat/completions`）原生支持 `tools` 和 `tool_choice` 参数，行为与 Agent 场景一致。百炼兼容该协议，开发者可直接复用 LangChain 等生态的 `bind_tools`、`with_structured_output` 等模式，零改造迁移已有函数调用逻辑。

- **Sandbox Agent（沙箱智能体）场景**：函数调用完全由开发者代码控制。`main.py` 中的 `run()` 函数可自由调用任意 HTTP API、本地库或平台提供的 SDK（如 `dashscope`），无需依赖模型生成 `tool_calls`。此时“函数调用”退化为常规编程调用，但需自行处理超时、错误、结果解析与上下文传递。

## 关键参数和配置

函数调用的有效性高度依赖以下关键配置项：

- **工具定义（必填）**  
  - `function.name`：工具唯一标识符，仅限字母、数字、下划线，长度 ≤ 64 字符；  
  - `function.description`：简洁说明工具用途（≤ 512 字符），直接影响模型调用准确率；  
  - `function.parameters`：标准 JSON Schema（非 Swagger），必须为 `object` 类型，`required` 字段需显式声明；Object 子属性不可为空，否则发布失败（错误码 130022）。

- **调用控制（可选）**  
  - `tool_choice`：控制调用策略，可选 `"auto"`（默认）、`"none"`（禁用）或 `{"type": "function", "function": {"name": "xxx"}}`（强制指定）；  
  - `passing_method`（插件专用）：设为 `"大模型识别"` 时，参数由模型从用户输入中提取；设为 `"业务透传"` 时，参数由 `biz_params` 或工作流节点固定传入，不依赖模型理解；  
  - `stream` + `incremental_output`：流式响应下，`tool_calls` 仅在最终 chunk 中完整返回，中间 chunk 不含 `delta.tool_calls` 字段。

- **安全与鉴权（按需）**  
  - 插件级鉴权：通过 `plugin_url` 拼接路径，并配置 `Header`（如 `Authorization: Bearer <token>`）或 `Query`（如 `?api_key=xxx`）方式；  
  - 业务透传参数：通过 `biz_params.user_defined_params`（DashScope API）或 `extra_body.biz_params`（Responses API）传递，适用于动态 [Token](token.md)、用户 ID 等敏感信息。

## 面向开发者，简洁实用

- ✅ **起步最快**：用 `qwen-plus` 或 `qwen-max` 模型 + 符合 OpenAPI 3.0 的工具 Schema，即可启用自动函数调用；  
- ✅ **调试要点**：若模型未触发调用，优先检查 `description` 是否清晰、`parameters` 是否为合法 JSON Schema、首条 `messages` 是否为 `role: "user"` 且 `content` 非空；  
- ✅ **生产建议**：对关键业务参数，采用 `"业务透传"` 模式而非依赖模型提取，避免幻觉；对复杂 Object 输入，提供 `user_input → expected_payload` 示例对提升准确率；  
- ⚠️ **避坑提醒**：单个智能体最多关联 10 个工具；GET 请求不支持 Object 类型参数；删除插件将级联删除其所有工具并导致已关联应用立即失效；  
- 📌 **终极控制权**：当自动调用不可控时，切换至 Sandbox Agent 或工作流节点，用代码 100% 掌握调用时机、参数与重试逻辑。

## 关联主题页

- [get started with agents](../guides/get-started-with-agents.md)
- [plug in](../guides/plug-in.md)
- [agent development](../guides/agent-development.md)
- [application call](../api/application-call.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


