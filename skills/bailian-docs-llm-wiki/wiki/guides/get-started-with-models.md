# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。核心包括模型选择、API 调用方式、关键参数配置及基础限制说明。所有操作均基于标准 RESTful API 接口，无需安装额外 SDK（但推荐使用官方 SDK 简化鉴权与重试逻辑）。

## 支持的模型与功能

百炼平台当前支持 Qwen 系列（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、Qwen-VL 多模态模型，以及部分第三方模型（需单独开通权限）。模型能力覆盖文本生成、代码补全、多轮对话、结构化输出（JSON Schema）、流式响应等。完整模型列表及能力说明见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态能力（如工具调用、函数执行）需在请求中显式启用 `tools` 字段，并参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的示例。

## 关键参数

必需参数包括：  
- `model`: 模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；  
- `input.messages`: 非空消息数组，格式为 `[{ "role": "user", "content": "..." }]`；  
- `parameters.temperature`: 控制随机性（0.0–2.0，默认 1.0），值越低输出越确定；  
- `parameters.max_tokens`: 输出长度上限（注意：该值不包含输入 token 数，总 token 消耗受配额约束）。

> **注意**：`parameters.top_p` 在部分旧文档中被描述为“默认 0.8”，但最新 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 明确其默认值为 `1.0`，以兼容更广义的采样策略，请以该文档为准。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID / Secret），用于 `Authorization: Bearer <api_key>` 请求头鉴权；  
2. **确定接入点**：根据部署地域选择 Base URL，例如华东 1（杭州）对应 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 和 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；  
3. **发起 POST 请求**：Body 为 JSON，含 `model`、`input`、`parameters` 字段，Content-Type 必须为 `application/json`；  
4. **处理响应**：成功时返回 `output.text` 或 `output.choices[0].message.content`（取决于接口版本），流式响应需解析 SSE 数据块。

## 限制和注意事项

- 单次请求最大输入 token 数因模型而异（`qwen-turbo` 为 8K，`qwen-max` 为 32K），超出将返回 `400 Bad Request`；  
- 默认调用频次限制为 5 QPS（每秒查询数），可通过 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 提交提额申请；  
- 同一 API Key 下所有模型共享配额，且 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 规则优先于单模型配额生效；  
- 不支持跨地域调用（如使用华东 1 的 Key 访问华北 2 域名），否则返回 `403 Forbidden`；  
- 所有模型均不支持自定义训练权重或 LoRA 微调部署——此为百炼专属模型服务，非开源模型托管平台。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


