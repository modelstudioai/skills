# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。你将了解支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK 即可集成。

## 支持的模型与功能

百炼平台提供多种预置模型，包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、文本嵌入模型（如 text-embedding-v1）及多模态模型（如 qwen-vl-plus）。模型能力覆盖文本生成、推理、摘要、代码生成、多轮对话、图像理解等场景。完整模型列表及适用场景请参阅 [选择模型](../../raw/model-user-guide/get-started-with-models.md)。部分模型支持流式响应（`stream=true`）和[函数调用](../concepts/function-calling.md)（`tools` 参数），具体能力以各模型文档为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型 ID（如 `"qwen-turbo"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models.md) 中公布的名称严格一致；
- `input.messages`：消息数组，格式为 `[{ "role": "user", "content": "..." }]`，系统角色（`system`）仅在部分模型中生效；
- `parameters`：可选对象，常用字段包括 `temperature`（0.0–2.0）、`top_p`、`max_tokens`（注意：不同模型默认值与上限差异显著，详见各模型文档）。

> **注意**：原始文档中 [动态限流](../../raw/model-user-guide/get-started-with-models.md) 与 [限流](../../raw/model-user-guide/get-started-with-models.md) 两节描述存在不一致——前者强调按 token 动态配额，后者以 QPS 固定阈值为主。实际生效策略以控制台「配额管理」实时配置为准，建议优先参考 [动态限流](../../raw/model-user-guide/get-started-with-models.md) 的实现逻辑。

## 使用方式

1. **认证**：使用阿里云 AccessKey（`Authorization: Bearer <api_key>`）或 STS 临时凭证；
2. **Endpoint**：根据地域选择 Base URL，例如华东 1（杭州）为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射见 [Base URL总览](../../raw/model-user-guide/get-started-with-models.md)；
3. **发送请求**：推荐使用 `POST` 方法，`Content-Type: application/json`，Body 包含 `model` 和 `input` 字段；
4. **调试建议**：首次调用前，请务必完成 [首次调用千问API](../../raw/model-user-guide/get-started-with-models.md) 中的密钥配置与权限校验步骤。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 role + content）不得超过模型上下文窗口限制（如 qwen-turbo 为 8K tokens），超长内容需截断或分块；
- 免费试用额度仅适用于指定模型（如 qwen-turbo），调用其他模型可能立即产生费用，详情见控制台配额页；
- 地域隔离：模型服务按地域部署，[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models.md) 明确了各 Region 对应的 endpoint，跨地域调用将失败；
- 错误码 `429 Too Many Requests` 表示触发限流，此时应检查是否超出账户级或模型级配额（参见 [动态限流](../../raw/model-user-guide/get-started-with-models.md)）。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


