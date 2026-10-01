# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、自主决策并调用外部工具（如插件、知识库、API 或自定义服务）执行具体任务的核心能力。它使模型从“文本生成器”升级为“可执行智能体”，支持动态规划、实时信息获取、结构化计算与多步骤任务闭环。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非独立接口，而是贯穿于多个能力层的**统一语义机制**，其底层均基于 OpenAI 兼容的 `tools` + `tool_choice` 协议实现，但在不同场景下封装层级与配置方式不同：

- **模型 API 直接调用**（`/v1/chat/completions`）：需显式启用 `enable_function_calling: true`，并在请求中传入符合 OpenAI 格式的 `tools` 数组（含 `function.name`、`description`、`parameters`）。模型返回 `tool_calls` 字段，开发者需解析并同步/异步执行对应工具，再将结果以 `tool_message` 形式回传继续对话。
  
- **智能体应用（Agent 2.0）**：函数调用被抽象为“工具调用”，知识库、MCP 服务、官方插件（如 `calculator`、`quark_search`）均统一注册为工具。无需手动构造 `tools`，只需在控制台绑定工具并开启“自动调用”，模型会根据系统提示词和用户输入自主规划调用序列，并支持完整链路回溯（规划→执行→反思）。

- **工作流应用（Workflow）**：函数调用体现为“工具节点”或“API 节点”的显式编排。开发者通过拖拽将插件/MCP/自定义 API 作为确定性节点接入流程，由人工定义触发条件与参数传递逻辑，不依赖模型自主决策，适用于强流程约束场景。

- **插件集成**：所有插件（官方、三方、自定义）本质上都是可被函数调用机制发现和调度的标准化工具。自定义插件需明确定义 `function.name`、参数 schema 和鉴权方式，发布后即可被 Agent 或模型 API 调用。

> ✅ 关键区别：模型 API 和 Agent 2.0 依赖模型**自主决策调用**（`auto` / `required` 模式），而工作流是**人工编排调用**；前者灵活但不可控，后者确定但需预设逻辑。

## 关键参数和配置

| 参数名 | 类型 | 必填 | 说明 | 使用位置 |
|--------|------|------|------|-----------|
| `enable_function_calling` | boolean | 是（模型 API） | 启用函数调用能力，必须设为 `true` 才能触发 `tool_calls` 响应 | 模型 API 请求 `parameters` |
| `tools` | array | 是（模型 API / Agent 工具绑定） | OpenAI 兼容格式的工具定义数组，每个元素含 `function.name`、`description`、`parameters`（JSON Schema） | 模型 API `input` 或 Agent 控制台工具管理 |
| `tool_choice` | string / object | 否 | 控制调用策略：`"none"`（禁用）、`"auto"`（默认，模型自主决定）、`"required"`（强制调用至少一个）、`{"type": "function", "function": {"name": "xxx"}}`（指定工具） | 模型 API `input` |
| `biz_params.user_defined_params` | object | 否（推荐） | 用于向工具透传业务参数（如 `{"city": "杭州"}`），避免依赖模型抽取，提升准确率与安全性 | 所有支持插件的 API（`application call` / 模型 API） |
| `workspace` | string | 否（子空间必需） | 调用子业务空间内插件或应用时必须传入，确保工具上下文隔离 | HTTP Header（`X-DashScope-Workspace`） |

> ⚠️ 注意事项：
> - `tools` 中 `parameters` 必须为严格有效的 JSON Schema（支持 `string`/`number`/`boolean`/`object`/`array` 及嵌套），空 `properties` 或语法错误将导致调用失败；
> - 模型对工具名称和描述的语义理解高度敏感，建议 `function.name` 简洁唯一（如 `get_weather_by_city`），`description` 明确说明用途、输入约束与输出格式；
> - 在 Agent 2.0 中，工具调用失败时模型可能重试或降级处理，可通过系统提示词添加兜底指令（如“若工具不可用，请如实告知用户”）。

## 面向开发者，简洁实用

- **快速验证**：用 `qwen-turbo` + 最小 `tools`（如单个 `calculator`）发起一次 `/v1/chat/completions` 请求，观察是否返回 `tool_calls`，而非普通文本回复。
- **生产建议**：
  - 优先使用 **Agent 2.0** 替代裸模型 API 调用函数，它内置工具路由、错误重试、结果解析与上下文融合，大幅降低工程复杂度；
  - 对确定性流程（如“查订单→转工单→发短信”），选 **工作流应用**，避免模型幻觉导致工具误调；
  - 自定义插件务必启用 **调试模式** 并测试边界参数（空值、超长字符串、非法类型），工具返回非 2xx 响应需在 `responses` 中明确 `error` 字段供模型理解；
  - 所有工具调用结果请做**可信度校验**（如搜索结果是否含有效链接、代码执行是否超时），再决定是否回传给模型，防止污染推理链路。

函数调用不是功能开关，而是构建可靠 AI 应用的**协议基石**——设计清晰的工具契约、控制好调用边界、善用平台抽象层，才能让大模型真正“动起来”。

## 关联主题页

- [start using](../guides/start-using.md)
- [get started with models](../guides/get-started-with-models.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [plug in](../guides/plug-in.md)


