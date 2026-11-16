# application [use cases](use-cases.md)

本页面汇总百炼平台在实际业务场景中的典型应用模式，涵盖从轻量级嵌入式助手到复杂知识增强型应用的完整链路。所有用例均基于平台提供的标准 API 和 SDK 实现，无需修改底层模型。开发者可按需组合模型能力、工具调用与上下文管理机制快速落地。

## 支持的模型/功能

当前支持的应用场景主要依赖以下模型与功能模块：
- 通用大语言模型（如 Qwen-Max、Qwen-Plus）用于对话理解与生成；
- [函数调用](../concepts/function-calling.md)（Function Calling）能力用于对接企业微信、钉钉等平台的开放接口；
- RAG 检索增强模块（`retrieval` + `rerank`）支持本地知识库接入，适用于客服、内部问答等场景；
- Webhook 回调与事件驱动机制，用于实现异步消息处理（如公众号被动回复）。  
详细能力边界请参考 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中列出的全部子文档。

## 关键参数

不同场景下需关注的核心参数包括：
- `model`: 必填，指定推理模型（如 `qwen-max`），影响响应质量与延迟；
- `tools`: 可选，声明可用工具列表（如 `work_wechat_send_message`），仅当启用[函数调用](../concepts/function-calling.md)时生效；
- `retrieval_config`: 仅 RAG 场景需配置，含 `top_k`、`rerank_model` 等字段；  
> **注意**：部分旧文档中提及的 `enable_rag: true` 参数已废弃，应统一使用 `retrieval_config` 对象，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)。

## 使用方式

所有用例均通过 `/v1/chat/completions` 接口或对应 SDK（Python/Java/Node.js）调用，典型流程为：
1. 初始化客户端并配置鉴权（API Key 或 STS Token）；
2. 构造 `messages`（含 system/user/assistant 角色）与上述关键参数；
3. 发送请求，解析响应（含 `tool_calls` 或 `retrieval_results` 字段）；  
例如，在企业微信中部署 AI 助手需额外配置 `agent_type: "work_wechat"` 并传入 `corpid`、`agent_secret`，具体实现见 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)。

## 限制和注意事项

- 单次请求最大 `messages` 长度为 32768 token（含 system prompt），超长上下文需截断或启用流式分块；
- RAG 场景中，本地知识库仅支持 `.txt`、`.md`、`.pdf`（文本可提取）、`.docx` 格式，不支持图像内嵌文本；
- 微信公众号与钉钉机器人需完成平台侧审核与 webhook 白名单配置，否则回调失败；  
- 所有嵌入式助手（如网站 AI 助手）默认启用会话状态保持（`session_id` 必传），若未传将导致上下文丢失。  
更多部署细节与排障建议，请查阅 [实践教程](../../raw/application-user-guide/application-use-cases.md) 及其子文档。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


