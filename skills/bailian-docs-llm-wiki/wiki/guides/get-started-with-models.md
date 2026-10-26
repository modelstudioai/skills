# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境中的限制与注意事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK（但 SDK 可选）。

## 支持的模型与核心功能

百炼平台提供多种预训练大语言模型（如 Qwen 系列）、多模态模型及推理优化版本（如 Qwen-VL、Qwen2.5、Qwen3），支持文本生成、对话理解、代码补全、结构化输出（JSON Schema）、流式响应等能力。模型列表及能力矩阵详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型还支持工具调用（Function Calling）和自定义系统提示词（system prompt），具体以各模型文档为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `qwen-max`、`qwen-plus`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，至少包含一个 `user` 角色消息；
- `parameters.temperature`：控制输出随机性（0.0–2.0，默认 1.0）；
- `parameters.top_p`：核采样阈值（0.0–1.0，默认 0.8）；
- `stream`：布尔值，启用流式响应需显式设为 `true`。

> **注意**：`max_tokens` 参数在部分旧版文档中被描述为“默认不限制”，但实际受模型最大上下文窗口硬限制（如 qwen-max 为 32768 tokens），且平台默认截断策略可能影响长输出。请务必参考 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 中各 endpoint 的具体说明，避免因参数缺失导致 400 错误。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID/Secret），并确保对应账号已开通模型调用权限；
2. **构造请求**：使用 HTTPS POST 向对应地域的 Base URL 发送请求（例如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`），Header 中携带 `Authorization: Bearer <api_key>`；
3. **发送请求**：Body 为 JSON 格式，结构遵循 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 所示示例；
4. **处理响应**：成功返回 `200 OK`，含 `output.text` 或 `output.choices[0].message.content`；流式响应需按 SSE 协议解析事件流。

## 限制和注意事项

- 每个 API Key 默认享有动态配额（见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)），超出后返回 `429 Too Many Requests`；
- 单次请求输入 + 输出总 token 数不得超过模型上下文上限（如 qwen-plus 为 8192），否则返回 `400 Bad Request`；
- 不同地域（Region）的接入域名不可混用，须根据部署范围选择对应 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中的 endpoint；
- `system` 角色消息仅在部分模型（如 qwen-max、qwen3）中生效，其他模型会忽略该字段——此行为与早期文档中“所有模型均支持 system prompt”的描述存在不一致，请以 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 附录的模型能力表为准。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


