# start using

`start using` 是百炼平台的入门引导模块，帮助开发者快速初始化应用、接入模型服务并构建基础 AI 功能。它不提供独立 API，而是通过控制台向导、SDK 初始化或低代码组件配置触发后续流程。所有操作均需先完成项目创建与身份鉴权。

## 支持的模型/功能

当前支持以下核心能力：
- 知识库问答（基于文档切片与向量检索）  
- 多轮对话上下文管理（依赖 `conversation_id` 透传）  
- 模型路由：自动匹配 `qwen-max`、`qwen-plus`、`qwen-turbo` 及第三方模型（如 `llama3-70b`），具体可用模型列表以 [开始使用](../../raw/application-user-guide/start-using.md) 实时展示为准  
- 内置插件调用（如搜索、计算器），需在应用配置中显式启用  

> **注意**：[开始使用](../../raw/application-user-guide/start-using.md) 中列出的“0代码构建问答应用”路径已整合至新版控制台「应用模板」页，旧版独立文档 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 的界面截图和按钮文案已过时，建议以控制台实际 UI 为准。

## 关键参数

初始化阶段需关注以下参数（SDK 或 API 请求中常见）：
- `app_id`：必填，应用唯一标识，从控制台「应用设置」获取  
- `model`：可选，指定推理模型；若未指定，由平台按应用默认策略路由  
- `enable_search`：布尔值，启用后自动注入搜索插件（仅对知识库类应用生效）  
- `stream`：布尔值，控制响应[流式输出](../concepts/streaming.md)，默认 `false`；流式场景下需处理 `event: message` SSE 格式  

## 使用方式

1. **控制台快速启动**：进入「应用开发」→「新建应用」→ 选择「知识库问答」模板 → 上传文档 → 发布  
2. **SDK 初始化（Python 示例）**：  
   ```python
   from alibabacloud_bailian20231219 import models as bailian_models
   client = bailian_models.Client(
       access_key_id="YOUR_KEY",
       access_key_secret="YOUR_SECRET",
       endpoint="https://dashscope.aliyuncs.com/api/v1"
   )
   # 后续调用 chat_completions.create(...)
   ```
3. **API 直连（推荐用于调试）**：  
   POST `/api/v1/chat/completions`，Header 需含 `Authorization: Bearer <api_key>`，Body 包含 `app_id` 和 `messages` 字段  

详细参数说明与完整 SDK 示例见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 限制和注意事项

- 单次请求 `messages` 最多 50 条，总 token 数上限为模型 context length 的 90%（例如 `qwen-max` 为 28k tokens）  
- 知识库问答默认启用 RAG 重排（rerank），不可关闭；如需禁用，须联系技术支持开通白名单  
- 免费试用额度仅覆盖 `qwen-turbo` 和 `qwen-plus`，`qwen-max` 及第三方模型需单独开通配额  
- 所有请求必须携带有效 `app_id`，否则返回 `401 Unauthorized`；该约束在 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中明确强调，且自 v2.3.0 起强制执行

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


