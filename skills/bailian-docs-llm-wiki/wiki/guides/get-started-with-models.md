# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）系列大模型或其它托管模型的场景。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可完成调用。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列大语言模型（如 qwen-max、qwen-plus、qwen-turbo）、多模态模型（如 qwen-vl）及部分开源微调模型。模型能力覆盖文本生成、代码补全、多轮对话、图像理解等。完整模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流与静态配额管理能力已统一整合至配额中心，具体策略请参考 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 文档。

> **注意**：原始文档中同时存在 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 两篇独立说明，但后者内容已过时，其描述的固定速率限制机制已被配额中心的弹性策略替代；实际接入应以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 为准。

## 关键参数

调用模型 API 必须指定以下参数：
- `model`：模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input`：请求数据体，结构为 `{ "messages": [...] }`，`messages` 遵循标准 ChatML 格式；
- `parameters`（可选）：控制生成行为，如 `temperature`（0.0–2.0）、`top_p`、`max_tokens` 等，详细取值范围见各模型文档。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥」页面创建并复制密钥；
2. 构造请求：使用 `POST /v1/chat/completions` 端点，Header 中携带 `Authorization: Bearer <api_key>`；
3. 设置 Base URL：根据部署地域选择对应接入域名，例如华东1（杭州）为 `https://dashscope.aliyuncs.com/api/v1`，完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
4. 地域与服务范围需提前确认，不同 Region 的模型可用性与延迟差异显著，配置方法详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

- 单次请求 `messages` 数量上限为 50 条，总 token 数（输入+输出）受模型自身限制及账户配额双重约束；
- 免费试用额度仅限新用户首次开通后 30 天内有效，超出后需绑定付费账号；
- 图像类请求（如 qwen-vl）需将 base64 编码图片置于 `messages.content` 的 `image_url` 字段，不支持本地文件路径；
- 所有调用均需显式声明 `region`（通过 Base URL 或 `x-dashscope-region` Header），未声明可能导致 404 或路由失败 —— 此要求在 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中明确强调。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


