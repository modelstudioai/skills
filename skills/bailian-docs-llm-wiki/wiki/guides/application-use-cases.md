# application [use cases](use-cases.md)

本页面汇总百炼平台在实际业务场景中的典型应用模式，涵盖嵌入式AI助手、企业IM集成、智能客服及RAG类应用等方向。所有用例均基于平台提供的标准API与SDK能力实现，适用于Web、移动端及企业办公生态。具体实现细节请参考各子场景文档。

## 支持的模型/功能

- 支持调用 `qwen-max`、`qwen-plus`、`qwen-turbo` 等全系列大模型，以及 `qwen-audio`（语音）、`qwen-vl`（多模态）等专用模型  
- 提供开箱即用的对话管理、流式响应、历史上下文维护、[函数调用](../concepts/function-calling.md)（Function Calling）能力  
- RAG场景下支持向量检索（`retrieval` 模块）与知识库热更新，详见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)  

## 关键参数

- `model`: 必填，指定模型ID（如 `qwen-plus`），不同模型对 `max_tokens` 和 `temperature` 的默认值存在差异  
- `stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)时需设为 `true`，客户端须按 SSE 协议解析；部分旧版 SDK 默认关闭，需显式设置  
- `enable_search`: 仅 `qwen-max` 和 `qwen-plus` 支持，开启后自动调用百炼内置搜索服务（注意：该参数在 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中被明确要求启用）  
- `retrieval_config`: RAG场景必填，含 `top_k`、`knowledge_id` 等字段，格式与 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 严格一致  

## 使用方式

- Web端：通过 `@alibaba/bailian-js-sdk` 初始化 client，调用 `client.chat.completions.create()` 发起请求  
- 企业IM（企微/钉钉/微信公众号）：使用平台提供的 Bot SDK 或 Webhook 接入，消息体需按对应渠道协议封装（如企微需校验 `msg_signature`）  
- 后端服务：推荐使用 REST API + 短期 access token（有效期2小时），避免长期凭证硬编码；token 获取方式见 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)  

## 限制和注意事项

- 单次请求最大上下文长度受模型限制（`qwen-turbo`: 8K tokens；`qwen-plus`: 32K tokens；`qwen-max`: 32K tokens），超长输入将被截断且**不报错**  
- 流式响应中 `delta.content` 可能为空字符串（尤其在[函数调用](../concepts/function-calling.md)或工具触发阶段），客户端需容错处理  
- > **注意**：[在钉钉创建AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 文档中描述的 `dingtalk-bot-sdk v1.2.0` 已废弃，当前应使用 `@alibaba/bailian-dingtalk-sdk v2.0.0+`，旧版无法兼容新版鉴权机制  
- 所有IM渠道均要求 HTTPS 回调地址，且需在百炼控制台白名单中配置域名（非IP）  
- RAG知识库更新后，新请求默认立即生效，但已有会话的缓存检索结果**不会自动刷新**，需主动调用 `clear_session` 或新建 session

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


