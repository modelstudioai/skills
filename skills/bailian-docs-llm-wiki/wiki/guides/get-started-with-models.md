# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境中的限制与注意事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK（但 SDK 可选）。

## 支持的模型与核心功能

百炼平台提供多种预训练大语言模型（如 Qwen 系列）、多模态模型及推理优化版本（如 Qwen-VL、Qwen2.5、Qwen3），支持文本生成、对话理解、代码补全、结构化输出（JSON Schema）、流式响应等能力。模型列表及能力矩阵详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型还支持工具调用（Function Calling）和自定义系统提示词（system [prompt](prompt.md)），具体以各模型文档为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `qwen-max`、`qwen-plus`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：消息数组，至少包含一个 `user` 角色消息；
- `parameters.temperature`：控制输出随机性（0.0–2.0，默认 1.0）；
- `parameters.top_p`：核采样阈值（0.0–1.0，默认 0.8）；
- `parameters.max_tokens`：最大生成 token 数（硬上限，超出将被截断）。

> **注意**：`parameters.stop` 字段在 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 文档中被错误描述为“影响配额计算”，实际该字段仅用于终止生成，**不参与任何配额或计费逻辑**；正确说明见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 使用方式

1. **获取 API Key**：在百炼控制台「API 密钥管理」中创建并复制密钥；
2. **构造请求**：使用 `POST /v1/chat/completions`（或 `/v1/completions`）端点，Header 中设置 `Authorization: Bearer <your_api_key>`；
3. **指定 Base URL 和地域**：根据部署区域选择对应接入域名，例如 `https://dashscope.aliyuncs.com/api/v1`（公共云杭州）或 `https://dashscope-intl.aliyuncs.com/api/v1`（国际站），完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
4. **发起调用**：参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 curl 示例完成首次验证。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system + user + assistant）不得超过模型 context 长度的 95%（预留 token 给响应）；
- 流式响应（`stream=true`）需按 SSE 格式解析，不可直接 JSON.parse 整体响应体；
- 免费额度与付费配额独立管理，超限后返回 `429 Too Many Requests`，具体策略参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；
- 模型输出可能包含不安全内容，建议在业务侧启用内容安全过滤（如阿里云内容安全服务）。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


