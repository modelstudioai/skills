# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解平台支持的主流模型类型、关键请求参数含义、标准调用方式，以及生产环境需关注的限流与地域部署约束。所有操作均基于 RESTful API，无需安装额外 SDK。

## 支持的模型与核心功能

百炼平台当前提供 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、Qwen2 系列及部分开源模型的托管与推理服务，支持文本生成、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应（stream=true）和多轮对话上下文管理。模型能力与更新状态详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态推理能力（如工具调用、JSON Schema 输出约束）需配合对应模型版本使用，具体兼容性请参考 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 关键参数

调用 `/v1/chat/completions` 接口时，必填参数包括：  
- `model`：模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中列出的名称严格一致；  
- `messages`：非空消息数组，格式为 `[{ "role": "user", "content": "..." }]`；  
- `Authorization`：Bearer Token，通过控制台「API Key」页面获取。  
可选参数中，`stream`（布尔值）、`temperature`（0.0–2.0）、`max_tokens`（默认 2048，最大 32768）影响输出行为；`response_format`（如 `{"type": "json_object"}`）仅对支持 JSON 模式的模型生效。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）；  
2. **确认接入点**：根据部署地域选择 Base URL，中国大陆用户默认使用 `https://dashscope.aliyuncs.com/api/v1`，海外用户需参考 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 配置对应 endpoint；  
3. **发起请求**：使用 curl 或 HTTP 客户端发送 POST 请求，示例见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

> **注意**：文档中同时存在 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 两篇，但后者内容已过时——当前统一采用基于 Quota 的动态配额管理体系，`X-RateLimit-Limit` 等旧版限流响应头不再返回，请以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 为准。

## 限制和注意事项

- 单次请求 `messages` 总长度（含 system [prompt](prompt.md)）不得超过模型 context length（例如 qwen-max 为 32768 tokens），超长将被截断并返回 400 错误；  
- 流式响应（`stream: true`）下，`max_tokens` 仍生效，且首 token 延迟受模型加载与网络 RTT 影响；  
- 所有请求必须携带 `Content-Type: application/json`，缺失将返回 415；  
- 地域隔离严格：密钥仅在其创建地域生效，跨地域调用需单独申请对应 region 的 API Key（参见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


