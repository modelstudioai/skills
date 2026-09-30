# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具调用机制，允许大模型在推理过程中自主识别用户意图、生成符合预定义 Schema 的函数参数，并触发外部工具或服务执行。该能力是构建智能体（Agent）、工作流（Workflow）及高代码应用中“工具编排”与“任务自动化”的核心技术基础。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）应用**：在 Agent 2.0 中，函数调用作为默认启用的内置能力，模型可基于系统提示词和用户输入，自动选择并调用已配置的内置插件（如计算器、图片生成、夸克搜索）或自定义 MCP 工具；开发者通过 `tools` 字段声明函数 Schema（OpenAPI 3.0 兼容），无需手动解析 JSON 或编写调度逻辑。  
- **工作流（Workflow）应用**：函数调用以「MCP 节点」或「API 调用节点」形式显式编排，由工作流引擎控制调用时机与上下文传递；适用于需强顺序、错误重试、多工具协同的复杂流程（如“先查天气 → 再订机票 → 发送通知”）。  
- **API 直接调用**：在 `/v1/chat/completions`（OpenAI 兼容）或 `/apps/{app_id}/completion`（DashScope 原生）接口中，通过 `tools` + `tool_choice` 参数启用函数调用；模型返回 `{"role": "assistant", "content": null, "tool_calls": [...]}` 结构，客户端需解析 `tool_calls` 并同步/异步执行对应函数，再将结果以 `tool` 角色消息回传继续对话。  
- **高代码应用**：通过 `fastmcp.Client` 集成 MCP 协议，在 Python 代码中注册本地函数为工具，模型可直接调用并获取实时返回值，实现深度定制化逻辑（如数据库查询、内部 API 封装、业务规则校验）。

> ⚠️ 注意：函数调用能力依赖模型本身支持（当前仅 `qwen-max`、`qwen-plus` 及部分千问 VL 模型完整支持），且需在应用配置或请求体中显式声明 `tools`；未声明时模型不会触发任何工具调用。

## 关键参数和配置

| 参数名 | 类型 | 说明 | 是否必填 |
|--------|------|------|----------|
| `tools` | array of object | 工具列表，每个对象包含 `type`（固定为 `"function"`）、`function.name`、`function.description` 和 `function.parameters`（JSON Schema 格式） | 是（启用函数调用时） |
| `tool_choice` | string or object | 控制调用策略：<br>• `"auto"`（默认）：由模型自主决定是否调用及调用哪个工具<br>• `"none"`：禁止调用任何工具<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制指定调用某函数 | 否（默认 `"auto"`） |
| `enable_thinking` | boolean | 启用思维链推理，提升复杂工具选择与参数生成准确性（尤其对多步骤、多工具场景） | 否（建议开启） |
| `thinking_budget` | integer | 思维链推理所允许的最大 token 数，默认 4000，避免过度消耗上下文 | 否（仅当 `enable_thinking=true` 时生效） |

- **Schema 要求**：`function.parameters` 必须为合法 JSON Schema（支持 `string`、`number`、`boolean`、`object`、`array` 及嵌套），不支持 `null` 类型或 `$ref` 引用；推荐使用 `required` 字段明确必填参数。
- **响应处理**：函数执行后，需将结果以 `{"role": "tool", "tool_call_id": "...", "content": "..."}` 格式作为新消息加入 `messages`，再次调用模型完成最终回复。

## 面向开发者，简洁实用

- ✅ **快速起步**：在控制台创建 Agent 2.0 应用 → 绑定知识库与内置插件 → 发布后即可测试函数调用效果；无需写一行工具调用代码。  
- ✅ **调试技巧**：开启 `stream=false` + `enable_thinking=true`，观察模型返回的 `tool_calls` 内容是否符合预期；若参数缺失或格式错误，检查 `parameters` Schema 中 `required` 和 `type` 定义。  
- ✅ **生产建议**：  
  - 对关键业务函数（如支付、删库），务必在工具实现层做鉴权与幂等校验；  
  - 避免在 `function.description` 中暴露敏感逻辑，仅描述用途与输入输出语义；  
  - 流式场景下，`tool_calls` 仅在首 chunk 返回，后续 chunk 为工具执行结果或最终回复，需按 `delta.role` 区分处理。  
- ❌ **常见误区**：  
  - 误以为 `tools` 声明后模型一定会调用——实际仍取决于输入意图与模型能力；  
  - 将函数返回的原始 JSON 当作最终答案——必须回传给模型生成自然语言总结；  
  - 在非函数调用模式（如纯文本生成）下传入 `tools` 参数，将被忽略且不报错。

## 关联主题页

- [start using](../guides/start-using.md)
- [test 1](../guides/test-1.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [application support](../guides/application-support.md)


