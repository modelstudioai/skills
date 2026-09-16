# application [use cases](use-cases.md)

本页面汇总百炼平台在实际业务场景中的典型应用模式，涵盖轻量级嵌入式助手、企业IM集成、智能客服及RAG类知识应用等方向。所有用例均基于平台提供的标准化API与SDK实现，无需从零训练模型。开发者可按需组合模型能力与接入方式，快速落地AI功能。

## 支持的模型/功能

- 基础大模型调用：支持 Qwen 系列（如 qwen-max、qwen-plus）、以及部分开源模型（如 llama3-70b）的同步/流式推理；
- [多模态能力](../concepts/multi-modal.md)：图像理解（qwen-vl-plus）、语音转文本（whisper-large-v3）等需显式指定 model 参数；
- RAG增强：通过 `retrieval` 插件或 `knowledge_id` 参数接入已配置的知识库，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)；
- 工具调用（Function Calling）：支持 JSON Schema 定义工具函数，由模型自主决策调用时机，当前仅 qwen-max 和 qwen-plus 全面支持。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-max"`；不支持别名（如 `"max"`），必须使用完整名称 |
| `input.messages` | array | 是 | 对话消息列表，格式为 `[{ "role": "user", "content": "..." }]`；系统提示词应置于 `messages[0]` 的 `role: "system"` 中 |
| `parameters.temperature` | number | 否 | 默认 0.85；生成确定性高时建议设为 0.1–0.3；> **注意**：[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 示例中误写为 `temp`，实际应为 `temperature` |
| `parameters.top_p` | number | 否 | 默认 0.8；与 `temperature` 协同控制采样多样性 |
| `retrieval.knowledge_id` | string | 否 | 指定知识库ID以启用RAG；该参数优先级高于 `input.retrieval` 字段，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **嵌入式Web助手**：前端通过 SDK 初始化 `BailianClient`，调用 `chat.completions.create()` 发起请求；推荐使用 `stream: true` 实现逐字流式响应，降低用户等待感知；
2. **企业IM集成（企微/钉钉/公众号）**：后端接收IM平台回调事件 → 提取用户消息 → 构造 `input.messages` → 调用百炼API → 将 `output.text` 回传至IM；注意企微需处理 `markdown` 格式兼容性，参考 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)；
3. **RAG应用**：先在控制台创建并发布知识库，获取 `knowledge_id`；请求中传入该ID，平台自动完成检索+生成两阶段流程；不支持运行时动态上传文档。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（qwen-max）或 16384（qwen-plus），超限将返回 `400 Bad Request`；
- 流式响应（`stream: true`）下，`output.text` 字段不可用，需监听 `delta.content` 事件拼接结果；
- 所有IM集成场景均需自行实现会话状态管理（如 `session_id` 绑定），百炼API本身无会话上下文记忆；
- > **注意**：[10分钟实现微信公众号智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 文档中提及“自动维护对话历史”，该描述已过时；自 v2.3.0 起，API 默认不保留历史，必须显式传入完整消息列表（含历史轮次）才能维持上下文。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


