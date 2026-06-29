# 函数调用

函数调用（Function Calling）是大模型根据用户输入和工具描述，自主判断是否调用外部工具、选择合适工具并将工具返回结果合并回上下文以生成最终回答的能力。它是智能体应用扩展模型能力边界、获取最新信息、精确计算与操作外部系统的核心机制。

## 在百炼平台中的使用方式

百炼平台的函数调用并非单一接口，而是分布在多个层面：

- **OpenAI 兼容 Chat Completions**：支持标准 function call 流程，开发者按 OpenAI 协议定义 `tools`，模型在响应中返回工具调用参数，调用方执行后回传结果。适合接入第三方 OpenAI 生态工具。
- **OpenAI 兼容 Responses 接口**：内置联网搜索、代码解释器、网页内容提取等工具，开箱即用，无需自行定义；同时通过 `previous_response_id` 自动维护上下文。
- **Anthropic 兼容 Messages 接口**：支持思考（thinking）与工具调用，按 Anthropic 协议定义工具。
- **DashScope 原生接口**：功能集最完整，参数支持最丰富，适合需要最全采样参数与业务字段的场景。
- **Omni Realtime API**：基于 WebSocket 的实时[多模态](multimodal.md)交互同样支持 Function Calling，通过 `response.create` 事件触发；Manual 模式下工具调用回传结果后需手动发送 `response.create` 触发下一轮响应。
- **智能体应用 / Assistant API**：模型依据用户输入、工具名称与描述判断是否调用工具，应用内部完成调用并将结果与用户内容合并再次输入模型，无需调用时直接生成输出。
- **工作流应用**：插件作为工作流节点按编排顺序执行，而非模型主动规划调用。

> 注意：联网搜索、代码解释器、网页内容提取为 Responses 接口专属内置能力；OpenAI Chat Completions 与 Anthropic Messages 接口不内置这些工具，需通过工具调用协议自行接入。

## 关键参数与配置

- **model**：通过请求体的 `model` 字段指定具体模型名。智能体应用推荐选用具备强工具调用能力的模型，如 `qwen-max` 系列。
- **tools**：在 OpenAI/Anthropic 兼容接口中按对应协议定义工具名称、描述与参数 schema；描述应使用自然语言，帮助模型判断是否调用。
- **工具 ID**：通过 Assistant API 调用插件工具时需正确传递工具 ID（在插件详情页"插件工具"下获取，例如 `calculator`）。
- **ReAct 最大轮次**：智能体应用取值范围 1–50，限制单次会话中工具调用的最大次数，超出后自动退出工具调用链路并由模型生成最终回复。
- **turn_detection**：Omni Realtime API 中，Manual 模式（设为 `null`）下工具调用回传结果后需手动发送 `response.create`；VAD 模式由服务端自动生成响应。
- **base_url / api_key**：迁移到百炼时替换为业务空间专属域名与百炼 API Key，即可复用现有 OpenAI 代码。

## 插件与工具集成

百炼插件是工具集合的载体，一个插件可包含多个工具（API）。插件分三类：

- **官方插件**：组件广场预置，如 Python 代码解释器（`code_interpreter`）、计算器（`calculator`）、夸克搜索（`quark_search`）等，无需配置输入输出参数。
- **三方插件**：涵盖商业服务、图像视频、学习教育等领域，开通后直接调用。
- **自定义插件**：通过配置 API 路径、请求参数与返回数据创建，或从云市场导入；只有已发布的工具才能在应用中被调用。

子业务空间调用官方插件前，需先在插件详情页为子业务空间授权；每个智能体应用最多添加 10 个工具。

## 注意事项

- 各模型对插件/工具调用的兼容性可能有差异，最新状态以控制台实际执行结果为准。
- 从 OpenAI / Anthropic 迁移时，应先确认目标 Qwen 模型在对应兼容接口下是否支持 `tools`、`stream` 等所需参数。
- 兼容接口为保证协议一致性，可能不暴露百炼原生全部参数；如需最全能力建议改用 DashScope 原生接口。
- 首次访问插件页面需授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`；RAM 子账号缺少创建服务关联角色权限会报错（错误码 140052），需先由主账号授予相应自定义策略。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more about models](../api/more-about-models.md)
- [plug in](../guides/plug-in.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [llm application](../guides/llm-application.md)


