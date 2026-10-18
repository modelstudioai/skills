# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK（但官方 Python SDK 可简化开发）。

## 支持的模型与核心功能

百炼平台提供多类预训练大语言模型（LLM）、[多模态](../concepts/multi-modal.md)模型及专属微调模型，涵盖通用对话、代码生成、长文本理解、图像理解等场景。模型列表持续更新，具体可用模型请以控制台「模型广场」或 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档为准。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和系统提示词（system prompt），详见 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：文档中提及的「动态限流」机制（见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)）与当前实际生效的配额策略存在差异——新版配额体系已统一通过「项目级 QPS/TPM 配额」管理，旧版 per-model 限流配置已废弃，请以控制台实时配额面板为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `qwen-max`、`qwen-plus`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中列出的名称严格一致；
- `input.messages`：消息数组，至少包含一个 `user` 角色消息；
- `parameters.temperature`、`top_p` 等采样参数为可选，但建议显式设置以保障结果稳定性。

所有请求须携带有效的 `Authorization: Bearer <api_key>` 头，并使用正确的 Base URL —— 不同地域对应不同接入域名，详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

1. 在百炼控制台创建 API Key（路径：**API 密钥管理 → 创建密钥**）；  
2. 根据目标模型与地域，拼接请求 URL（例如：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`）；  
3. 发送 POST 请求，Body 为 JSON 格式，结构参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的完整示例；  
4. 解析响应中的 `output.text` 或流式 `output.choices[0].delta.content` 字段。

推荐使用 `curl` 或 Python `requests` 快速验证，无需依赖 SDK；若需异步批处理或重试逻辑，可选用官方 `dashscope` SDK（v1.20.0+）。

## 限制和注意事项

- 单次请求最大输入 tokens 数因模型而异（如 `qwen-max` 为 32768，`qwen-turbo` 为 8192），超出将返回 `400 Bad Request`；  
- 所有模型默认启用内容安全过滤，敏感输入可能被拦截并返回空响应或错误码 `422`；  
- 免费额度仅适用于新注册用户首月，后续需绑定支付方式并开通按量计费；  
- 流式响应需设置 `stream: true`，且客户端必须正确处理 SSE（Server-Sent Events）格式，否则可能丢帧或解析失败。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


