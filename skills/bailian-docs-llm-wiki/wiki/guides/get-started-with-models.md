# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API，无需安装额外 SDK 即可开始。

## 支持的模型与功能

百炼平台提供多种开源与自研大模型，包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、通义万相、通义听悟等多模态模型。模型能力覆盖文本生成、代码补全、多轮对话、图像理解与生成等场景。具体模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和系统提示词（system prompt），但并非全部模型均支持——例如 qwen-turbo 当前不支持 `tools` 参数，该限制在 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 的示例中未明确说明，实际调用将返回 `400 Bad Request`。

> **注意**：[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中描述的每分钟请求数（RPM）阈值，与 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 中按 [Token](../concepts/token.md) 量级动态调整的机制存在口径差异。后者为当前生效策略，前者已过时，请以控制台配额页或 `/v1/models/{model}/quota` 接口返回为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型 ID（如 `qwen-max`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：消息数组，至少包含一个 `user` 角色消息；
- `parameters.temperature`：控制输出随机性（0.0–2.0），默认为 1.0；
- `parameters.top_p`：核采样阈值（0.0–1.0），默认为 0.8；
- `parameters.max_tokens`：最大生成 token 数，不同模型有硬上限（如 qwen-turbo 最高支持 8192）。

## 使用方式

1. **获取认证凭证**：在百炼控制台创建 API Key（AccessKey ID / Secret），用于 `Authorization: Bearer <api_key>` 请求头；
2. **确定接入地址**：根据部署地域选择 Base URL，中国大陆用户默认使用 `https://dashscope.aliyuncs.com/api/v1`；国际用户需参考 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 配置对应 endpoint；
3. **发起 POST 请求**：向 `/v1/services/aigc/text-generation/generation`（文本模型）或 `/v1/services/aigc/image-generation/generation`（图像模型）提交 JSON payload；
4. **处理响应**：成功响应含 `output.text` 或 `output.task_id`（异步任务），错误码见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 附录。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system + user + assistant）不得超过模型 context window（如 qwen-max 为 32768 tokens），超长将被截断且不报错；
- 流式响应（`stream=true`）仅支持文本生成类模型，图像/语音类模型暂不支持；
- 所有模型调用均受账户级配额约束，超出后返回 `429 Too Many Requests`，建议主动监控 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 提供的配额接口；
- 模型 ID 区分大小写，`Qwen-Max` 将导致 `404 Not Found`，务必使用小写形式（如 `qwen-max`）。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


