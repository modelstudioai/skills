# application [use cases](use-cases.md)

`application use cases` 模块面向开发者提供开箱即用的 AI 应用集成方案，覆盖主流企业通讯与内容平台（如企业微信、钉钉、微信公众号、网站嵌入）及本地知识增强场景（RAG）。所有用例均基于百炼平台统一 API 与 SDK 实现，无需从零训练模型。实际部署前请确认所选模型与功能在目标环境中受支持。

## 支持的模型/功能

- 所有应用用例默认调用 `qwen-max` 或 `qwen-plus`（取决于上下文长度与响应质量要求），部分轻量级嵌入场景可选用 `qwen-turbo`  
- 功能上支持：流式响应、历史会话管理（`enable_history=true`）、自定义系统提示（`system_prompt`）、文件上传解析（仅限 RAG 场景）  
- 注意：[在钉钉创建AI机器人](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-dingtalk.md) 文档中提及的“自动同步组织架构”功能，仅对开通了 DingTalk Open Platform 企业认证的账号生效；未认证账号将忽略该参数，此限制未在 [在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中明确说明，需开发者自行校验权限。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 必须为平台已发布的模型 ID，如 `qwen-plus`；不支持自定义微调模型 ID |
| `enable_history` | boolean | 否 | 默认 `false`；启用后需传入 `conversation_id`，否则返回 400 |
| `system_prompt` | string | 否 | 最长 2048 字符；若与知识库检索结果拼接使用，需预留至少 512 字符空间给检索内容 |
| `retrieval_config` | object | 否 | 仅 RAG 场景有效，结构见 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) |

## 使用方式

1. **初始化 SDK**：使用 `BailianClient(app_id="xxx", api_key="xxx")` 初始化客户端  
2. **构造请求体**：按需设置 `model`、`enable_history`、`system_prompt` 等字段  
3. **调用接口**：对嵌入类用例（如网站助手、公众号客服），推荐使用 `/v1/chat/completions`；对需事件驱动的平台（如钉钉、企微），必须配合对应平台 Webhook 回调地址注册，并在请求中携带 `callback_url`（详见 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md)）  
4. **处理响应**：流式响应需监听 `event: message`，非流式直接解析 JSON 中的 `output.text`

## 限制和注意事项

- 单次请求最大上下文长度为 32768 token（`qwen-plus`），超出将被截断且不报错；建议在前端预估输入长度  
- 所有平台集成用例（企微、钉钉、公众号）均**不支持**直接上传图片/音视频作为输入，仅支持文本与 base64 编码的 PDF/Word/TXT 文件（后者仅限 RAG 场景）  
- > **注意**：[在企业微信集成AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-work-wechat.md) 中描述的“消息加签验证方式”与当前百炼 v2.3+ 版本实际要求的 HMAC-SHA256 签名算法不一致，应以 [在网站上增加一个AI助手](../../raw/application-user-guide/application-use-cases/add-an-ai-assistant-to-your-website-in-10-minutes.md) 中的签名示例代码为准  
- RAG 场景下，知识库索引更新延迟最长 2 分钟，期间新文档不可检出；该行为在 [基于本地知识库构建RAG应用](../../raw/application-user-guide/application-use-cases/build-rag-application-based-on-local-retrieval.md) 中有明确说明

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


