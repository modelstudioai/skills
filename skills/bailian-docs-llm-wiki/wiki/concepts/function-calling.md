# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、生成结构化[工具调用](tool-calling.md)请求，并交由外部系统执行的关键能力。它使模型从“纯文本生成器”升级为可操作真实世界的智能代理，支撑搜索、计算、多模态生成、系统集成等扩展行为。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非单一接口特性，而是贯穿模型能力、插件机制与应用范式的横切能力，具体体现为以下三类实践方式：

- **模型原生[工具调用](tool-calling.md)**：`qwen-max` 和 `qwen-plus` 等支持模型可在一次推理中直接输出符合 OpenAI 或 Anthropic 规范的 `tool_calls` 结构（如 `{"name": "quark_search", "arguments": "{\"query\":\"杭州天气\"}"}`）。DashScope 原生接口则通过 `enable_web_search`、`enable_code_interpreter` 等布尔开关或 `tools` 参数显式启用，模型据此自主规划是否调用及调用哪个工具。

- **插件驱动的函数调用**：在智能体（Agent 2.0）或工作流中，插件（如 `calculator`、`text_to_image`、自定义 MCP 服务）被注册为可调用函数。模型根据系统提示词中声明的工具签名（名称、描述、参数 schema），结合用户输入生成调用请求；平台负责参数校验、鉴权转发、结果注入与错误重试。

- **专用模型的结构化输出**：部分垂直模型将函数调用作为标准输出格式。例如，`tongyi-intent-detect-v3` 在 `INTENT_MODE` 下不返回自然语言，而是直接输出 JSON 格式的函数调用对象（含 `function_name` 和 `parameters`），供下游路由至对应业务服务；`gui-plus` 模型则在系统消息中声明 `computer_use` 工具后，输出带 `action`/`target`/`value` 字段的操作指令。

> ⚠️ 注意：`qwen-turbo`、`qwen-mt-plus`、`qwen-deep-research` 等模型**不支持自动函数调用**；其中 `qwen-deep-research` 虽具备联网检索能力，但该能力内置于模型内部，不可拆解为用户可控的独立函数调用。

## 关键参数和配置

函数调用的启用与行为控制依赖以下核心参数（按作用层级组织）：

| 参数 | 作用范围 | 必填 | 说明 |
|------|----------|------|------|
| `tools` | OpenAI 兼容 / DashScope / Assistant API | 否（启用调用时必填） | JSON Schema 数组，定义可用函数的 `name`、`description`、`parameters`（OpenAPI 3.0 兼容）。模型据此理解工具能力边界。 |
| `tool_choice` | OpenAI 兼容 / Anthropic 兼容 / DashScope | 否（推荐显式指定） | 控制调用策略：<br>• `"auto"`（默认）：模型自主决定是否调用及调用哪个；<br>• `"none"`：禁用调用；<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定函数。 |
| `enable_web_search` / `enable_code_interpreter` | DashScope 原生接口 | 否 | 布尔开关，快速启用内置工具。比 `tools` 更轻量，但灵活性低（无参数定制）。 |
| `biz_params` / `user_defined_params` | 插件调用（API/SDK） | 否（透传场景必填） | 用于向插件传递业务上下文参数（如用户 ID、会话 ID），不参与模型推理，但影响工具执行逻辑。 |
| `system`（Anthropic） / `messages[0].content`（OpenAI） | 所有兼容接口 | 推荐 | 在系统消息中清晰描述可用工具及其用途，是提升调用准确率的关键提示工程实践。 |

- **参数验证要求**：所有 `tools` 中定义的 `parameters` schema 必须为有效 JSON Schema；Object 类型参数的每个子属性必须设置 `description`（否则自定义插件发布失败）。
- **安全约束**：函数调用仅在模型明确输出 `tool_calls` 字段时触发；平台**不会**执行未经声明的工具或未授权的 URL 请求。

## 面向开发者，简洁实用

- ✅ **快速启动**：若只需基础搜索/计算，优先使用 DashScope 的 `enable_web_search=true` 或 `enable_code_interpreter=true`，无需写 schema。
- ✅ **精准控制**：需调用自有服务时，用 `tools` + `tool_choice` 显式声明；在系统提示词中用自然语言+JSON 示例说明工具用法（如 `"调用 weather_api 时，务必传入 city 字段，例如：{ 'city': '北京' }"`）。
- ✅ **调试技巧**：开启 `enable_thinking=true`（工作流）或 `thinking_mode`（API），查看模型的思考链（reasoning trace），定位调用失败是因参数提取不准，还是工具描述模糊。
- ❌ **避免踩坑**：
  - 不要混用 `enable_web_search` 和 `tools` —— 二者互斥，后者优先级更高；
  - `qwen-turbo` 等轻量模型不支持任何函数调用，勿在 `tools` 中声明；
  - 流式响应中，`tool_calls` 仅在完整响应结束时一次性返回，不支持增量解析。

函数调用是构建可靠 AI 应用的基石。始终以「最小可行工具集 + 清晰系统提示 + 显式 tool_choice」为起点，再逐步扩展复杂度。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [more models](../api/more-models.md)
- [plug in](../guides/plug-in.md)
- [llm application](../guides/llm-application.md)


