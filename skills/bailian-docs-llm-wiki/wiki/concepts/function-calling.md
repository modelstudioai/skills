# 函数调用

函数调用（Function Calling）是百炼平台支持的一种结构化工具调用机制，允许大模型在推理过程中自主识别用户意图、生成符合 OpenAI 兼容 Schema 的 `tool_calls` 请求，并交由外部系统执行具体操作（如查询数据库、调用 API、检索知识库等），再将结果注入后续对话上下文。该能力不改变模型核心生成逻辑，而是通过标准化的输入/输出协议实现 LLM 与现实世界服务的安全、可控协同。

## 在百炼平台的不同场景中，这个概念如何使用

- **应用层调用（`application support`）**：在 `/apps/{app_id}/chat/completions` 接口请求中，通过 `tools` 参数传入工具定义列表（JSON Schema 格式），模型将根据用户输入自动决定是否调用、调用哪个工具及传入何参数；调用结果需由开发者在客户端侧解析 `tool_calls` 并执行，再以 `tool_result` 形式发起下一轮请求（即多轮 tool-augmented 对话）。  
- **Agent 开发（`agent development`）**：Managed Agent 和 Flow Agent 原生集成函数调用能力，无需手动构造 `tools` 或处理 `tool_calls`——平台自动完成工具发现、参数提取、异步执行、错误重试与结果注入；Sandbox 模式则需开发者在 `main()` 函数中自行解析 `event.tools` 和 `event.tool_calls` 字段，调用对应函数并返回结构化响应。  
- **基础模型 API（`preparations` & `more about models`）**：所有公开模型（如 `qwen-max`、`qwen3-vl-plus`）均支持函数调用，但需确保 SDK 版本 ≥ v1.18.0（Python）或 Java SDK ≥ v2.5.0；多模态模型调用时，若工具涉及图像/视频处理，需配合 `X-DashScope-OssResourceResolve: enable` Header 解析 OSS URL。  

> ⚠️ 注意：函数调用本身不执行任何实际操作——它仅生成调用指令。**执行权始终在开发者侧**，平台不代为调用外部服务，也不托管工具代码。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 |
|------|------|------|------|
| `tools` | 请求体（`application support` / 基础 API） | array | 必填（启用函数调用时）；每个元素为 OpenAI 兼容的工具定义对象，含 `type="function"`、`function.name`、`function.description`、`function.parameters`（JSON Schema）；最多支持 10 个工具。 |
| `tool_choice` | 请求体（可选） | string 或 object | 控制调用策略：<br>• `"auto"`（默认）：由模型自主决策是否调用；<br>• `"none"`：禁用函数调用；<br>• `{"type": "function", "function": {"name": "xxx"}}`：强制调用指定工具。 |
| `enable_tracing` | Agent 配置（`agent development`） | boolean | 启用后，全链路追踪日志将包含完整的 `tool_calls` 输入、执行耗时、原始返回及注入后的上下文，便于调试工具逻辑。 |
| `max_iterations` | Agent 配置（`agent development`） | integer | 管控函数调用循环深度：Managed Agent 默认 10 轮，Flow Agent 默认 5 轮；超出后终止流程并返回最终响应（不报错）。 |

- **安全要求**：所有工具执行必须在可信环境内完成，禁止在前端暴露工具凭证；建议通过百炼「连接器」统一管理外部服务认证信息。  
- **错误处理**：工具执行失败时，API 默认返回空 `tool_calls` 数组（而非抛出异常），开发者需主动检查 `response.message.tool_calls` 是否为空，并根据业务逻辑降级或提示用户。  

## 面向开发者，简洁实用

- ✅ **快速启用**：只需在请求中添加 `tools` 数组，无需修改模型或部署配置。  
- ✅ **兼容 OpenAI**：工具 Schema 完全兼容 `openai>=1.0.0` 格式，已有 OpenAI 工具可直接复用。  
- ✅ **流式支持**：启用 `stream=true` 时，`tool_calls` 将作为独立 chunk 流式返回（`delta.tool_calls`），便于实时渲染调用状态。  
- ❌ **不支持嵌套调用**：单次模型响应最多触发一次 `tool_calls`；如需多步工具协作，请在客户端控制调用顺序。  
- 📏 **长度限制**：单次 `tool_calls` 中所有参数 JSON 序列化后总长 ≤ 1MB；超限将导致 `400 Bad Request`。  

> 提示：本地调试推荐使用 `bailian-cli --tool-mode` 模拟工具注册与调用闭环；生产环境务必设置 `timeout_ms`（Agent）或 `timeout`（SDK）防止工具阻塞。

## 关联主题页

- [preparations](../api/preparations.md)
- [agent development](../guides/agent-development.md)
- [more about models](../api/more-about-models.md)
- [application support](../guides/application-support.md)


