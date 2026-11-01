# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）等大模型的开发场景，无需部署模型即可通过标准 HTTP 接口调用。所有操作均基于百炼统一 API 网关，需提前完成身份认证与配额配置。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列大语言模型（如 qwen-max、qwen-plus、qwen-turbo），以及部分多模态和推理优化模型。模型能力覆盖文本生成、代码补全、结构化输出（JSON Schema）、流式响应等。具体可用模型列表及特性详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流策略与模型能力绑定，不同模型享有独立的默认 QPS 和并发限制，详情参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。

## 关键参数

调用模型 API 时，以下参数为必需或强推荐：

- `model`: 模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`: 非空消息数组，首条消息 `role` 应为 `"user"`；
- `parameters.temperature`: 控制输出随机性（0.0–1.0），默认值为 0.85；
- `parameters.top_p`: 核采样阈值（0.0–1.0），默认 0.8；
- `parameters.max_tokens`: 输出长度上限，各模型有硬性上限（如 qwen-max 为 8192），超出将被截断。

> **注意**：`parameters.stop` 字段在部分旧版文档中被描述为支持字符串数组，但实际 API 仅接受字符串（非数组）；该不一致已在最新 SDK 中修正，请以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 的示例代码为准。

## 使用方式

1. **获取凭证**：在百炼控制台创建 AccessKey（AK/SK），用于签名认证；
2. **确定接入点**：根据部署地域选择对应 Base URL，例如华东 1（杭州）使用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射请参考 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
3. **构造请求**：使用 POST 方法，`Content-Type: application/json`，Body 包含 `model`、`input` 和 `parameters`；
4. **处理响应**：成功返回 `200`，结果位于 `output.text` 或 `output.choices[0].message.content`（取决于接口版本）。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数不得超过模型上下文窗口（如 qwen-turbo 为 4096），超限将返回 `400 Bad Request`；
- 默认限流策略为每秒 5 次请求（QPS）且最大并发 10，可通过控制台申请提升，但受 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 规则约束；
- 流式响应（`stream: true`）需按 SSE 协议解析，不可直接 JSON.parse 整个响应体；
- 所有模型调用均按 token 计费，输入与输出 token 分别计数，计费逻辑以控制台实时展示为准。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


