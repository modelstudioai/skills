# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）系列大模型或其它托管模型的场景。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可完成调用。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列大语言模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`），以及部分多模态和推理优化模型。模型能力覆盖文本生成、代码补全、结构化输出（JSON Schema）、流式响应等。完整模型列表及能力说明见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流与配额管理功能已集成至控制台，支持按 Token 或请求次数维度配置策略，详情参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。

> **注意**：原始文档中 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 与 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 内容存在重叠，且后者更新更及时；建议以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 为准，前者已逐步归档。

## 关键参数

调用模型 API 时，以下参数为必需或强推荐：

- `model`: 模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`: 消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters.temperature`: 控制生成随机性（0.0–2.0，默认 1.0）；
- `parameters.top_p`: 核采样阈值（0.0–1.0），与 `temperature` 互斥使用；
- `stream`: 布尔值，启用流式响应需设为 `true`。

## 使用方式

1. **获取 API Key**：在百炼控制台「API 密钥」页面创建并复制密钥；
2. **确定 Base URL**：根据部署地域选择接入域名，例如中国大陆区为 `https://dashscope.aliyuncs.com/api/v1`，详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
3. **构造请求**：使用 `POST /api/v1/services/aigc/text-generation/generation`（通用文本生成路径）发送 JSON 请求；
4. **首次验证**：推荐从 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的最小示例入手，确认鉴权与网络连通性。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system [prompt](prompt.md)）不得超过模型上下文窗口限制（如 `qwen-turbo` 为 8K tokens）；
- 免费额度仅限新用户首月，后续调用受账户级配额与 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 规则双重约束；
- 地域选择影响延迟与合规性：[选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 明确了各 Region 的可用模型与 SLA 承诺，跨地域调用可能导致 404 或权限拒绝；
- 不支持自定义模型权重上传或 fine-tuning API（该能力归属 Model Studio，参见 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


