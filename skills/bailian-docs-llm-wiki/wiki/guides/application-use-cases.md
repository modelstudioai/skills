# application [use cases](use-cases.md)

本页面汇总百炼平台在实际业务场景中的典型应用模式，涵盖从轻量级嵌入式助手到复杂知识增强型应用的完整链路。所有用例均基于平台提供的标准 API 和 SDK 实现，无需修改底层模型逻辑。开发者可按需组合模型能力、工具调用与上下文管理机制。

## 支持的模型/功能

当前支持的应用场景主要依赖以下模型与功能模块：
- 通用大语言模型（如 Qwen-Max、Qwen-Plus）用于对话理解、内容生成与指令执行；
- [函数调用](../concepts/function-calling.md)（Function Calling）能力用于对接企业微信、钉钉、微信公众号等第三方平台事件回调；
- RAG 框架（含向量检索 + 重排序）用于本地知识库问答，支持 PDF/Word/TXT 等格式解析（详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)）；
- Web UI 组件（如 `ChatBox`、`MessageInput`）提供开箱即用的前端嵌入方案，适用于网站 AI 助手快速集成（参见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）。

> **注意**：文档 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中提及的“自建消息加解密服务”已由平台 v2.3.0 起默认内置，无需手动实现；旧版教程未同步更新该变更。

## 关键参数

各场景共性关键参数包括：
- `model`: 必填，指定调用模型 ID（如 `qwen-max`），不同场景对推理延迟与上下文长度有差异化要求；
- `tools`: 可选，用于声明启用的工具集（如 `work_wechat`, `dingtalk_bot`, `retrieval`），需与业务平台权限配置一致；
- `retrieval_config`: 仅 RAG 场景必需，包含 `top_k`（默认 3）、`rerank`（布尔值，默认 false）等字段，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)；
- `stream`: 建议设为 `true` 以支持流式响应，尤其适用于网页/小程序等交互式前端。

## 使用方式

标准接入流程为三步：
1. **初始化客户端**：使用 `BailianClient(api_key=...)` 实例化，推荐复用单例；
2. **构造请求体**：根据目标场景选择对应 `tools` 并填充必要参数（如 `work_wechat` 需传入 `agent_id` 和 `corp_id`）；
3. **发起调用**：调用 `client.chat.completions.create()`，处理 `response.choices[0].message.content` 或 `response.choices[0].message.tool_calls`。

例如，在钉钉机器人中触发[函数调用](../concepts/function-calling.md)，需确保 `tools` 中包含 `dingtalk_bot`，且 `tool_choice` 显式设为 `"required"` —— 此细节在 [在钉钉创建AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 中有明确示例。

## 限制和注意事项

- 单次请求最大 `input_tokens` 限制为 32768（Qwen-Max）或 65536（Qwen-Plus），超出将被截断，RAG 场景需预估 chunk 合并后总长度；
- 企业微信/钉钉/微信公众号等平台集成，必须完成对应平台的 OAuth2 授权与 IP 白名单配置，否则 `tools` 调用将返回 `403`；
- 所有 Web 嵌入类用例（如网站 AI 助手、微信公众号客服）默认不持久化会话历史，如需长期上下文，须自行实现 `session_id` 管理并传入 `extra_session_params`；
- 微信公众号智能客服的模板消息推送能力受限于微信官方接口配额（每日 100 条/用户），该约束在 [10分钟实现微信公众号智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 中未作强调，需开发者额外关注。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


