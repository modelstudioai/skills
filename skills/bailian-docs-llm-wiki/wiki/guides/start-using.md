# start using

本页面介绍如何快速开始使用百炼平台的核心能力，包括模型调用、应用构建和基础配置。开发者可基于平台提供的 API 或低代码界面快速集成大模型能力。所有操作均需先完成[账号开通与项目创建](../../raw/application-user-guide/account-setup.md)。

## 支持的模型/功能

百炼平台当前支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等开源模型，以及部分闭源增强模型（如 Qwen-Max、Qwen-Plus）。除基础文本生成外，还提供知识库问答、多轮对话管理、RAG 增强、[函数调用](../concepts/function-calling.md)（Function Calling）和多模态理解等能力。详细模型列表及能力矩阵见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型 ID）、`input.messages`（消息数组），推荐设置 `parameters.temperature`（0.1–1.0）、`parameters.top_p`（0.5–0.95）以平衡确定性与多样性。流式响应需显式设置 `stream: true`。注意：`max_tokens` 默认值因模型而异，Qwen3 默认为 8192，但实际受上下文长度限制；该行为与 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中最新公告一致。> **注意**：部分旧文档中提及的 `repetition_penalty` 默认值为 1.0，但自 v2024.07 起已统一调整为 1.05，以更好抑制重复输出，请以 [开始使用](../../raw/application-user-guide/start-using.md) 中的参数说明为准。

## 使用方式

- **API 方式**：通过 HTTPS POST 请求调用 `/v1/chat/completions` 接口，需携带 `Authorization: Bearer <api_key>`。完整请求示例见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。
- **低代码方式**：在控制台「应用开发」中选择「知识库问答助手」模板，上传文档后即可发布，无需编写代码。该流程依赖平台内置 RAG 引擎，其索引策略与检索逻辑详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数不得超过模型上下文长度（如 Qwen3 为 131072 tokens），超限将返回 `400 Bad Request`；
- 免费试用额度仅限新注册用户首月，且不可跨项目共享；
- 知识库问答应用不支持实时数据库连接，仅支持静态文档（PDF/Word/TXT/Markdown）导入；
- 所有 API 调用受每分钟请求数（QPM）和每秒令牌数（TPS）双重配额限制，具体阈值取决于所选模型和计费类型，详情参见 [开始使用](../../raw/application-user-guide/start-using.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


