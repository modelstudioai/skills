# application [use cases](use-cases.md)

`application use cases` 模块面向开发者提供开箱即用的 AI 应用集成方案，覆盖主流企业通讯与内容平台（如企业微信、钉钉、微信公众号、网站嵌入）及本地知识增强场景（RAG）。所有用例均基于百炼平台统一 API 和 SDK 实现，无需从零训练模型。实际部署前请务必参考对应场景的完整实践文档。

## 支持的模型/功能

- 所有应用用例默认使用 `qwen-max` 或 `qwen-plus`（取决于性能与成本权衡），部分轻量场景支持 `qwen-turbo`；模型选择需在请求参数中显式指定。
- 功能上支持：多轮对话上下文管理、流式响应（`stream=true`）、自定义系统提示（`system_prompt`）、文件上传解析（PDF/Word/Excel/TXT）及向量检索增强（仅 RAG 场景）。
- 注意：[在钉钉创建AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 中提及的“自动同步钉钉组织架构”能力，已在 v2.3.0 后移除，当前需通过 OpenAPI 手动同步用户信息；详见 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 的权限配置说明。

## 关键参数

- `model`: 必填，取值为 `qwen-max`、`qwen-plus` 或 `qwen-turbo`（RAG 场景推荐 `qwen-plus`）。
- `stream`: 布尔值，启用[流式输出](../concepts/streaming-output.md)时设为 `true`，适用于前端实时渲染。
- `retrieval_enabled`: 仅 RAG 场景有效，设为 `true` 并配合 `knowledge_id` 使用。
- `knowledge_id`: RAG 场景必填，指向已上传并切片完成的知识库 ID；该 ID 需通过 `/v1/knowledge` 接口创建后获取。
- 其他通用参数（如 `temperature`、`top_p`）行为与 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 文档一致。

## 使用方式

1. **初始化 SDK 或调用 REST API**：使用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（通用生成）或 `https://dashscope.aliyuncs.com/api/v1/services/aigc/retrieval-augmented-generation/generation`（RAG 专用）。
2. **按场景配置参数**：例如在网站嵌入场景中，需设置 `system_prompt` 为“你是一个友好、简洁的客服助手”，并启用 `stream=true`；详情见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)。
3. **处理回调与错误**：企业微信/钉钉等平台需配置 HTTPS 回调地址，并校验 `x-hub-signature-256` 头；签名密钥在控制台「应用凭证」中获取。

## 限制和注意事项

- 单次请求最大上下文长度为 32768 token（`qwen-max`），RAG 场景中检索返回的 chunk 总长度计入该限制。
- 文件解析类用例（如微信公众号客服）仅支持 UTF-8 编码文本，非 UTF-8 的 Word/PDF 可能解析失败；建议预处理转码。
- > **注意**：[10分钟实现微信公众号智能客服](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-wechat-in-10-minutes.md) 中描述的“自动接入公众号消息接口”步骤，因微信平台策略更新，自 2024 年 7 月起必须通过「微信公众号平台 → 开发 → 基本配置 → 服务器配置」手动填写 Token 和 EncodingAESKey，不再支持一键导入。
- 所有平台集成均需在百炼控制台完成「应用授权」与「平台 OAuth 配置」，未授权的应用将返回 `403 Forbidden`。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


