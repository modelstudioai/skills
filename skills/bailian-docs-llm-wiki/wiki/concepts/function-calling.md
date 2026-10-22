# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具协同机制，允许大模型在生成响应过程中主动识别用户意图、选择并调用预定义的外部函数（如企业微信消息发送、数据库查询、联网搜索等），将非文本能力无缝集成到对话流中。该能力不依赖模型自身执行代码，而是由平台在推理后解析 `tool_calls` 字段，并按约定协议触发对应服务。

## 在百炼平台的不同场景中，这个概念如何使用

函数调用在百炼平台中并非统一接口能力，而是按模型类型、API 协议和业务场景差异化支持：

- **通用对话模型（Qwen-Max/Plus/Flash 等）**：通过 OpenAI 兼容 Chat API 或 DashScope 原生 API 启用，需在请求中传入 `tools` 数组（含函数名称、描述、参数 Schema）及可选的 `tool_choice`（如 `"auto"`、`"required"` 或指定函数名）。模型返回 `message.tool_calls`，开发者需自行解析并执行对应函数，再将结果以 `tool_message` 形式拼入下一轮 `messages` 继续调用。

- **实时多模态模型（Qwen-Omni-Realtime）**：支持 `type=function` 的工具定义，但与 `enable_search` 互斥；需在 `session.update` 中声明 `tools`，并在语音/文本输入流中由模型动态触发；适用于客服坐席辅助、实时会议工具联动等低延迟场景。

- **专用模型**：
  - `tongyi-intent-detect-v3`（意图理解模型）专为函数调用优化，毫秒级输出标准化意图标签或 `tool_calls` 结构，常用于对话路由与 Bot 编排；
  - `qwen-deep-research` 不支持函数调用，其工具能力（如联网搜索）已内建于两阶段流程中；
  - `gui-plus` 系列暂未开放自定义函数调用，动作指令由模型直接生成（如 `"click(x=120, y=85)"`）。

- **应用集成场景**：在企业微信、钉钉、微信公众号等 Bot 开发中，函数调用是实现“AI 驱动业务操作”的核心路径。例如，当用户说“把这份合同发给张三”，模型可调用 `work_wechat.send_file` 工具，自动完成文件上传与消息推送。

> ⚠️ 注意：函数调用能力**取决于具体模型与所选 API 协议**。Qwen-Audio 不支持 OpenAI 兼容协议，故无法使用标准 `tool_calls`；`QwQ` 模型忽略 `system` 消息，可能影响工具描述的可见性；所有函数调用均需提前在控制台或 SDK 中完成权限配置（如企业微信 `agent_id` 白名单）。

## 关键参数和配置

| 参数 | 作用 | 必填 | 说明 |
|------|------|------|------|
| `tools` | 定义可用函数列表 | 是（启用时） | JSON 数组，每个元素含 `type="function"`、`function.name`、`function.description` 和 `function.parameters`（OpenAPI 3.0 Schema 格式）。DashScope SDK 支持 `tools` 直接传入，[OpenAI 兼容接口](openai-compatible-interface.md)要求严格遵循字段命名。 |
| `tool_choice` | 控制调用策略 | 否 | 可选值：`"none"`（禁用）、`"auto"`（默认，模型自主决定）、`"required"`（强制调用至少一个函数）、或 `{ "type": "function", "function": { "name": "xxx" } }`（指定函数）。生产环境推荐显式设置，避免行为漂移。 |
| `parallel_tool_calls` | 是否允许多函数并行调用 | 否 | 仅 Responses API 和 Anthropic Messages API 支持；设为 `true` 时模型可一次返回多个 `tool_call`，提升效率。 |
| `system` 消息内容 | 提供工具使用上下文 | 推荐 | 在 `messages[0]` 中加入清晰指令，如 `"You are a customer service bot. Always use functions to fulfill user requests."`；部分模型（如 intent-detect-v3）要求 `system` 中包含 `Response in INTENT_MODE.` 才启用函数输出模式。 |

- **安全与调试提示**：  
  - 所有 `tool_calls` 输出均为纯文本结构，**不执行任何代码**，需开发者在服务端校验参数、鉴权并调用真实后端；  
  - 建议对 `function.name` 做白名单校验，防止模型虚构函数名；  
  - 流式响应中 `tool_calls` 仅在完整响应结束时返回（非逐 token 流出），需等待 `finish_reason="tool_calls"` 后统一处理。

## 面向开发者，简洁实用

- ✅ **快速起步**：从 `tongyi-intent-detect-v3` 或 `qwen3.8-max` 开始测试，用 cURL 或 Python SDK 发送含 `tools` 的请求，观察 `response.choices[0].message.tool_calls` 字段；  
- ✅ **生产建议**：  
  - 总是设置 `tool_choice="required"`（若业务强依赖工具）或 `"auto"`（若需混合文本+工具响应）；  
  - 将 `tools` 定义提取为常量，避免硬编码；  
  - 实现幂等函数执行器——同一 `tool_call.id` 可能因重试重复到达，需去重处理；  
- ❌ **避坑提醒**：  
  - 不要将敏感凭证（如 API Key）写入 `function.parameters`，应在服务端通过配置中心注入；  
  - `qwen-deep-research`、`QwQ`、`Qwen-Audio` 等模型明确不支持标准函数调用，切勿强行传入 `tools`；  
  - 函数调用不等价于 RAG：`retrieval` 工具需单独配置 `retrieval_config`，且与 `tools` 并存时需注意优先级逻辑。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [more models](../api/more-models.md)
- [application use cases](../guides/application-use-cases.md)


