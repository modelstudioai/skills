# application [use cases](use-cases.md)

`application use cases` 模块面向开发者提供开箱即用的 AI 应用集成方案，覆盖主流企业通讯平台（如企业微信、钉钉、微信公众号）及 Web 端嵌入场景，并支持基于本地知识库的 RAG 构建。所有用例均基于百炼平台统一 API 接口与模型服务抽象层实现，无需从零训练模型即可快速部署。具体能力边界和配置细节需结合 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中的子文档验证。

## 支持的模型/功能

- 所有应用用例默认调用 `qwen-max` 或 `qwen-plus`（取决于所选场景的延迟与精度权衡），部分轻量级嵌入场景（如网站侧边栏助手）可降级至 `qwen-turbo`  
- 功能层面统一支持：上下文感知对话、多轮会话保持（依赖 `conversation_id`）、流式响应（`stream=true`）、系统提示词注入（`system` 字段）  
- RAG 类用例额外启用向量检索插件，支持上传 PDF/Word/TXT 文件并自动构建本地索引，该能力由 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 详细说明  

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 必须为平台已开通的模型 ID，如 `qwen-plus`；不支持自定义模型别名 |
| `input.messages` | array | 是 | 至少包含一个 `user` 角色消息；`system` 消息仅在首条生效 |
| `parameters.temperature` | number | 否 | 默认 `0.8`，RAG 场景建议设为 `0.1` 以提升答案稳定性 |
| `enable_search` | boolean | 否 | 仅 RAG 用例有效；设为 `true` 时自动触发知识库检索（见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md)） |

> **注意**：[在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 文档中提及的 `auto_init_conversation` 参数已在 v2.3.0 版本废弃，当前必须显式传入 `conversation_id` 或留空由服务端生成；请以 [实践教程](../../raw/application-user-guide/application-use-cases.md) 的最新子文档为准。

## 使用方式

1. **初始化 SDK 或调用 REST API**：使用 `POST /v1/chat/completions`，Header 中携带 `Authorization: Bearer <api_key>`  
2. **构造请求体**：按上述关键参数组织 JSON，例如企业微信集成需在 `input.messages` 中预置欢迎语模板（参见 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md)）  
3. **处理响应**：检查 `output.choices[0].message.content`，流式场景监听 `event: message` SSE 事件  

## 限制和注意事项

- 单次请求最大 `input.messages` 长度为 16K tokens（含 system [prompt](prompt.md)），超长文本需前端截断或启用 `enable_search` 走 RAG 分片检索  
- 所有通讯平台集成（微信/钉钉/企业微信）均要求后端服务完成 OAuth2 回调认证，前端不可直接暴露 API Key  
- RAG 用例中，单个知识库文件上限 50MB，总容量上限 10GB；索引构建异步完成，需轮询 `/v1/kb/status` 接口确认就绪状态  
- 钉钉机器人场景暂不支持富文本卡片（`card`）格式返回，仅支持纯文本或 Markdown（见 [在钉钉创建AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md)）

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


