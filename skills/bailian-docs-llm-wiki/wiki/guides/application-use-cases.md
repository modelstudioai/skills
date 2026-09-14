# application [use cases](use-cases.md)

`application use cases` 描述了百炼平台支持的典型端到端应用场景，覆盖 Web、企业通讯工具（如企业微信、钉钉、微信公众号）及本地知识增强型应用（RAG）。这些用例均基于平台提供的模型服务、API 接口和低代码集成能力实现，无需从零训练模型。开发者可直接复用文档中给出的标准接入路径与配置模式。

## 支持的模型/功能

- 所有场景默认调用百炼平台托管的通用大模型（如 Qwen-Max、Qwen-Plus），部分 RAG 场景支持指定 `retrieval` 模块启用向量检索；
- 企业微信、钉钉、微信公众号等集成场景依赖平台预置的 Bot SDK 和消息协议适配器，详见 [实践教程](../../raw/application-user-guide/application-use-cases.md)；
- RAG 应用需配合知识库管理模块使用，支持上传 PDF/Word/TXT 等格式文档并自动切片向量化，该能力在 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中有完整操作指引。

## 关键参数

- `model`: 必填，指定模型 ID（如 `qwen-max`）；
- `enable_retrieval`: 仅 RAG 场景需设为 `true`，并确保已绑定有效知识库 ID；
- `bot_id` / `app_key`: 各通讯平台集成时必需，由对应平台控制台生成，[实践教程](../../raw/application-user-guide/application-use-cases.md) 提供各平台获取路径；
- `stream`: 建议设为 `true` 以支持流式响应，提升终端用户体验。

## 使用方式

1. 登录百炼控制台 → 进入「应用」页签 → 点击「新建应用」；
2. 选择目标场景模板（如“企业微信机器人”或“RAG 应用”），系统自动配置基础参数与回调地址；
3. 根据向导完成平台侧认证（如企业微信扫码授权）、知识库绑定或 API 密钥配置；
4. 调用 `/v1/chat/completions` 接口（或使用 SDK 封装方法）发起请求，请求体需包含上述关键参数。

## 限制和注意事项

- 单个应用最多绑定 1 个知识库；若需多源检索，请先合并知识库或使用多路召回策略；
- 微信公众号智能客服要求公众号已通过微信认证且开通“微信开放平台”第三方平台权限；
- > **注意**：原始文档中“10分钟实现微信公众号智能客服”链接指向的帮助中心页面已更新，当前实际需配置微信服务器 URL 并验证 token，旧版免配置流程已下线，请以最新 [实践教程](../../raw/application-user-guide/application-use-cases.md) 中的步骤为准。

## 来源文档

- [实践教程](../../raw/application-user-guide/application-use-cases.md)


