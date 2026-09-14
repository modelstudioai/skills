# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。你将了解支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 [原文标题](../../raw/model-user-guide/get-started-with-models.md) 中列出的官方指引。

## 支持的模型与核心功能

百炼平台提供多种预置模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义微调模型，覆盖文本生成、多模态理解、代码生成等场景。模型能力与部署状态可在 [选择模型](https://help.aliyun.com/zh/model-studio/models) 页面实时查看；部分模型需开通对应服务后方可调用。动态扩缩容与多地域部署能力详见 [选择地域、服务部署范围和接入域名](https://help.aliyun.com/zh/model-studio/regions) —— 该文档明确指出：**同一模型在不同地域可能具有不同版本或可用性**，务必按实际部署地域确认模型 ID。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型唯一标识（如 `qwen-max`、`qwen-plus`），必须与所选地域下实际发布的模型 ID 严格一致；
- `input.messages`：消息数组，格式为 `[{"role": "user", "content": "..." }]`；
- `parameters`（可选）：控制生成行为，如 `temperature`、`top_p`、`max_tokens` 等，具体取值范围以 [原文标题](../../raw/model-user-guide/get-started-with-models.md) 中链接的 [产品简介](https://help.aliyun.com/zh/model-studio/what-is-model-studio) 和各模型详情页为准。

> **注意**：[原文标题](../../raw/model-user-guide/get-started-with-models.md) 中同时列出 [限流](https://help.aliyun.com/zh/model-studio/rate-limit) 和 [动态限流](https://help.aliyun.com/zh/model-studio/quota-management) 两篇文档，但后者为新版配额管理机制，前者已归档；请以 [动态限流](https://help.aliyun.com/zh/model-studio/quota-management) 文档为准，其定义了按 [Token](../concepts/token.md) 或请求量计费的细粒度配额策略。

## 使用方式

1. 获取 API Key（通过阿里云 RAM 控制台创建并授权 `AliyunBaiLianFullAccess` 策略）；
2. 构造 HTTPS POST 请求，Base URL 需根据所选地域确定（参见 [Base URL总览](https://help.aliyun.com/zh/model-studio/base-url)）；
3. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
4. 发送请求体（JSON 格式），解析响应中的 `output.text` 或 `output.choices[0].message.content`。

首次调用建议参考 [首次调用千问API](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen)，该指南包含完整 cURL 示例与错误码速查。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system [prompt](prompt.md)）不得超过模型上下文窗口限制（例如 `qwen-max` 为 32768 tokens），超长输入将被截断或报错；
- 免费试用额度仅限新用户首月，后续需绑定支付方式并配置配额；配额生效依赖 [动态限流](https://help.aliyun.com/zh/model-studio/quota-management) 中设置的 Quota Group；
- 所有模型调用均受地域隔离约束：**跨地域调用将返回 404 或 403 错误**，务必确保 Base URL、模型 ID 与所选地域三者一致 —— 此要求在 [选择地域、服务部署范围和接入域名](https://help.aliyun.com/zh/model-studio/regions) 中被反复强调。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


