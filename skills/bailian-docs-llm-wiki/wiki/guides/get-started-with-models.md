# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）系列大模型或其它托管模型的场景。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可完成调用。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列大语言模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`），以及部分多模态和推理优化模型。模型能力覆盖文本生成、代码补全、结构化输出（JSON Schema）、流式响应等。完整模型列表及能力说明见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流与配额管理能力已在生产环境全面启用，详情请参考 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。

> **注意**：原始文档中同时存在 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 和 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 两篇独立文档，但后者为最新机制（v2.3+），前者内容已过时；实际接入应以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，首条消息 `role` 应为 `"user"`；
- `parameters.temperature`：控制生成随机性（0.0–2.0），默认值为 1.0；
- `parameters.top_p`：核采样阈值（0.0–1.0），默认 0.8；
- `parameters.max_tokens`：最大输出 token 数，硬性上限受模型本身限制（如 `qwen-turbo` 默认上限为 8192）。

## 使用方式

1. **获取 API Key**：在百炼控制台「API 密钥」页面创建并复制密钥；
2. **确定 Base URL**：根据部署地域选择接入域名，详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
3. **构造请求**：使用 `POST /v1/chat/completions`，携带 `Authorization: Bearer <api_key>` 头；
4. **首次验证**：推荐按 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 curl 示例执行最小可行调用；
5. **地域适配**：若需低延迟或满足合规要求，务必确认所选地域与业务服务器同区域，参见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system [prompt](prompt.md)）不得超过模型 context window 的 95%（例如 `qwen-max` 为 32768 tokens，则建议 ≤31130）；
- 流式响应（`stream=true`）下，`max_tokens` 必须显式指定，否则返回 400 错误；
- 所有模型均不支持跨地域 [Token](../concepts/token.md) 复用（如华东 region 的 key 无法用于华北 endpoint）；
- 非标准参数（如自定义 stop words）可能被静默忽略，以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中标注的 `supported_parameters` 字段为准。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


