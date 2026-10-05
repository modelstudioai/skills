# 函数调用

函数调用（Function Calling）是百炼平台中大模型主动识别用户意图、结构化提取参数，并按预定义协议触发外部工具或服务的核心能力。它使模型不再局限于文本生成，而是能安全、可控地与现实世界交互，完成搜索、计算、代码执行、图像生成等确定性任务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台以统一语义、多形态落地，具体取决于所使用的接口和运行环境：

- **Omni Realtime API**：在实时语音交互会话中，通过 `session.update` 的 `tools` 字段声明函数列表（`type=function`），模型在流式响应过程中可动态触发 `function_call` 事件；此时调用由模型自主决策，支持与 `server_vad`/`semantic_vad` 协同实现“边说边调”；注意：`tools` 与 `enable_search` 不可同时启用。
  
- **Application Support（智能体应用）**：在 Assistant API 或控制台智能体配置中，通过 `tools` 数组传入 OpenAI-style 函数定义（含 `name`、`description`、`parameters`），模型返回结构化 `tool_calls` 后，平台自动透传 `Authorization` header 并发起 HTTP 请求；自定义插件必须严格遵循此协议，且仅 `Authorization` 可被透传。

- **Plug-in（插件体系）**：官方/三方/自定义插件本质是函数调用的封装载体。插件注册时需明确定义输入输出参数、鉴权方式及调用协议；调用时，模型根据 `tool_id`（如 `calculator`）匹配并填充参数，平台负责路由、鉴权、错误重试与结果注入。

- **Managed Agents API**：在托管式 Agent 中，函数调用作为技能（Skill）执行的基础机制。Agent 创建时可通过 `skills` 字段绑定插件或自定义工具，会话中模型生成 `tool_call` 后，平台自动调度对应 Skill，并将结果写入 Memory Store；事件流中可通过监听 `tool_call` 和 `tool_result` 事件实现细粒度控制。

## 关键参数和配置

函数调用本身不依赖独立参数，但其行为高度依赖以下配置项：

- **`tools`（必需）**：数组类型，每个元素为标准函数定义对象，必须包含：
  - `type`: `"function"`（百炼当前仅支持该类型，`"mcp"` 属于另一协议，不可混用）
  - `function.name`: 工具唯一标识（如 `quark_search`），需与插件市场或自定义插件注册 ID 一致
  - `function.description`: 清晰描述功能与适用场景（影响模型调用准确率）
  - `function.parameters`: JSON Schema 格式，定义必填/可选字段、类型、枚举值；Object 类型子属性**不能为空**

- **`tool_choice`（可选）**：控制调用策略：
  - `"auto"`（默认）：模型自主判断是否调用及调用哪个工具
  - `"none"`：禁止任何工具调用
  - `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某工具（适用于确定性流程）

- **透传限制（重要）**：所有场景下，仅 `Authorization` header 可被透传至目标服务端；其他自定义 header（如 `X-User-ID`）将被静默丢弃。

- **错误处理**：调用失败时，平台返回 `tool_call` 对应的 `error` 字段（如 `HTTP 500`、`timeout`），模型可据此重试或降级回复；开发者需在业务侧监听 `tool_result` 或检查响应中的 `tool_calls` 状态。

## 面向开发者，简洁实用

- ✅ 始终使用 `tools` 数组声明函数，勿混用 `enable_search`  
- ✅ 自定义插件的 `parameters` Schema 中，Object 类型必须定义非空子字段  
- ✅ 鉴权 Token 必须通过 `Authorization` header 传递，其他 header 无效  
- ✅ 在 Omni Realtime 中，`tools` 需在 `session.update` 时一次性声明，会话中不可动态增删  
- ✅ Managed Agents 中，`tool_call` 结果默认持久化到 Memory Store，可用于后续推理  
- ❌ 不要尝试在 `stream=True` 下手动解析 `tool_calls` —— 百炼已封装为结构化事件（如 `tool_call`、`tool_result`）或响应字段，直接消费即可

## 关联主题页

- [omni realtime api](../api/omni-realtime-api.md)
- [application support](../guides/application-support.md)
- [plug in](../guides/plug-in.md)
- [managed agents api](../api/managed-agents-api.md)


