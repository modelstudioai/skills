# application [use cases](use-cases.md)

`application use cases` 描述了百炼平台支持的典型端到端应用场景，覆盖轻量级嵌入式助手到基于私有知识的智能应用。这些用例均基于平台提供的标准化 API、低代码集成组件及 RAG 工具链实现，适用于 Web、IM 平台和本地知识服务等主流部署形态。开发者可直接复用文档中验证过的流程与配置模式。

## 支持的模型/功能

- 基础大模型调用：支持 Qwen 系列（如 qwen-max、qwen-plus）及第三方模型（通过 Model Studio 接入），用于生成式任务；
- 多模态能力：部分用例（如企业微信、钉钉机器人）默认启用图文理解与结构化输出；
- RAG 扩展：支持基于上传文档构建向量知识库，并通过 `retrieval` 参数启用[检索增强生成](../concepts/rag.md)，详见 [实践教程](../../raw/application-user-guide/application-use-cases.md)；
- 预置连接器：提供微信公众号、企业微信、钉钉、网站嵌入等开箱即用的 SDK 和 Webhook 模板，其能力边界与认证方式在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中明确列出。

## 关键参数

- `model`: 必填，指定模型 ID（如 `qwen-plus`），需与所选场景的推理要求匹配；
- `retrieval`: 布尔值或对象，启用 RAG 时设为 `true` 或 `{ "knowledge_id": "xxx" }`，该参数行为与 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中“基于本地知识库构建RAG应用”章节一致；
- `stream`: 建议在 Web/IM 场景中设为 `true` 以支持流式响应；
- `system_prompt`: 可选，用于定义角色与约束，但注意部分 IM 平台（如微信公众号）对 system [prompt](prompt.md) 的长度和生效时机存在限制（见下文“限制和注意事项”）。

## 使用方式

1. **低代码集成**：通过 Model Studio 控制台选择对应模板（如“微信公众号智能客服”），配置 webhook 地址与 token 后一键部署；
2. **API 调用**：使用 `/v1/chat/completions` 接口，按需传入 `model`、`messages` 及 `retrieval` 等参数；
3. **SDK 快速接入**：各平台（企业微信、钉钉）提供官方 SDK，封装了签名、加解密与消息格式转换逻辑，具体示例参见 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中对应链接。

## 限制和注意事项

- 微信公众号接口要求 `system_prompt` 不得超过 200 字符，且仅在会话首次请求时生效；企业微信则支持会话级持久化 system [prompt](prompt.md) —> **注意**：此差异未在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中明确说明，实际开发请以最新版企业微信 SDK 文档为准；
- RAG 场景下，知识库更新后需手动触发索引重建，否则新文档不参与检索；
- 网站嵌入方案依赖前端 SDK，不支持跨域 cookie 认证，建议配合后端代理转发请求以规避 CORS 限制。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


