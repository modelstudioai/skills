# get started with models

百炼平台提供统一的模型调用入口，支持多种大语言模型（如Qwen系列）及多模态模型的快速接入与使用。开发者可通过标准 REST API 或 SDK 调用模型服务，无需自行部署或管理基础设施。本文档梳理核心使用路径、关键配置项及常见约束，帮助开发者高效启动模型集成。

## 支持的模型与功能

当前平台支持 Qwen 系列语言模型（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、多模态模型（如 `qwen-vl-plus`）及部分第三方模型（需开通权限）。模型能力覆盖文本生成、代码补全、多轮对话、图像理解等场景。完整模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

## 关键参数

调用模型时必须指定以下参数：
- `model`：模型 ID（如 `"qwen-turbo"`），需与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input`：请求内容，结构为 `{ "messages": [...] }`（文本）或 `{ "messages": [...], "images": [...] }`（多模态）；
- `parameters`：可选，用于控制温度（`temperature`）、最大输出长度（`max_tokens`）等行为，具体字段见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 示例。

> **注意**：`region` 参数在部分旧文档中被描述为必需，但根据最新 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 文档，若未显式指定，系统将自动路由至最优可用区；SDK v3.0+ 已默认隐藏该参数，建议优先依赖自动路由。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AK/SK），并确保对应账号已开通目标模型权限；  
2. **构造请求**：使用 `POST /v1/chat/completions` 接口，Base URL 须匹配所选地域（参见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)）；  
3. **发送调用**：推荐使用官方 Python SDK（`dashscope` >= 1.14.0）或 cURL 示例（见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)）验证连通性。

## 限制和注意事项

- 单次请求 `messages` 最多支持 32 轮历史对话，`images` 最多 4 张（多模态模型）；  
- 免费额度仅限新用户首月，后续调用受 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 和 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 双重约束；  
- 模型响应超时默认为 60 秒，不可修改；长上下文场景建议拆分请求或选用 `qwen-max` 等高规格模型。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


