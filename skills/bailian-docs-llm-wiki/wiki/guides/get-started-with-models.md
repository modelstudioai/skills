# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）等大模型的开发场景，无需部署模型即可通过标准 HTTP 接口调用。所有操作均基于百炼统一 API 网关，需提前完成身份认证与配额配置。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、通义万相、通义听悟等多模态模型，具体列表详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。各模型支持文本生成、[函数调用](../concepts/function-calling.md)（tool calling）、流式响应、系统提示词（system [prompt](prompt.md)）和多轮对话上下文管理。部分模型还提供图像理解（如 `qwen-vl-plus`）或语音转写能力，功能细节请参考对应模型的 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：`qwen-turbo` 在 v2024.06 后已默认启用更严格的 token 截断策略（max_tokens 默认为 8192），而旧版文档 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中示例仍使用 4096，实际调用时建议显式指定 `max_tokens` 参数以避免意外截断。

## 关键参数

调用模型 API 时，以下参数必须或强烈建议设置：

- `model`: 必填，模型标识符（如 `"qwen-max"`），须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`: 必填，消息数组，每条消息含 `role`（`user`/`assistant`/`system`）和 `content` 字段；
- `parameters.temperature`: 可选，控制输出随机性（0.0–2.0），默认值因模型而异，生产环境建议设为 `0.7` 或更低；
- `parameters.top_p`: 可选，核采样阈值，默认 `0.8`；
- `stream`: 布尔值，启用流式响应时设为 `true`，需配合 SSE 解析。

其他参数（如 `stop`、`repetition_penalty`）见各模型文档，不通用。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID + Secret），并确保所属项目已开通对应模型权限；  
2. **确定接入点**：根据部署地域选择 Base URL，例如华东1（杭州）为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
3. **发起请求**：使用 `POST` 方法，`Content-Type: application/json`，携带 `Authorization: Bearer <api_key>` 头；  
4. **处理响应**：成功返回 `200`，结构为 `{ "output": { "text": "...", "choices": [...] }, "usage": { ... } }`；流式响应按 SSE 格式逐块接收。

首次调用可参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 cURL 和 Python 示例，但请注意其 Base URL 和参数格式已随平台升级更新。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system [prompt](prompt.md)）不得超过模型 context length 上限（如 `qwen-max` 为 32768 tokens），超长将被静默截断；
- 免费试用额度仅限新用户首月，后续需通过 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 或 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 配置配额；
- 所有请求必须指定 `region`（如 `cn-hangzhou`），否则可能路由失败；地域与接入域名强绑定，详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
- 不支持跨地域共享配额，且 `qwen-vl-plus` 等多模态模型暂不支持私有化部署调用。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


