# get started with models

百炼平台提供统一的模型调用入口，支持多种大语言模型（如Qwen系列）及多模态模型的快速接入与使用。开发者可通过标准 REST API 或 SDK 调用模型服务，无需自行部署或管理基础设施。本文档梳理核心使用路径、关键配置项及常见约束，帮助开发者高效启动模型集成。

## 支持的模型与功能

当前平台支持 Qwen 系列语言模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、多模态模型（如 `qwen-vl`）及部分第三方模型（需开通权限）。模型能力覆盖文本生成、代码补全、多轮对话、图像理解等场景。完整模型列表及能力说明见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)；各模型的适用场景与性能对比可参考 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 关键参数

调用模型时必需指定以下参数：
- `model`: 模型标识符（如 `"qwen-turbo"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`: 对话历史数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters.temperature` / `top_p` / `max_tokens`：控制生成多样性与长度，具体取值范围详见各模型文档。

> **注意**：`temperature` 默认值在不同模型间不一致（例如 `qwen-turbo` 默认为 `0.8`，而 `qwen-max` 默认为 `0.1`），请勿依赖全局默认值，务必显式设置或查阅对应模型的 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 示例确认。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID + Secret）；
2. **构造请求**：使用 `POST /v1/services/aigc/text-generation/generation` 等标准路径，Header 中携带 `Authorization: Bearer <api_key>`；
3. **选择接入点**：根据部署地域选择 Base URL（如 `https://dashscope.aliyuncs.com/api/v1`），详细域名映射见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；
4. **调试验证**：建议从 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的最小可行示例开始测试。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（具体依模型而异，以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 标注为准）；
- 免费额度用户受动态限流策略约束，超出后返回 `429 Too Many Requests`，限流规则详见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 非中国内地地域调用需确保所选 Region 已开通服务，且 API Key 具备对应地域访问权限（参见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)）；
- 所有模型调用均需通过 HTTPS，HTTP 请求将被拒绝。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


