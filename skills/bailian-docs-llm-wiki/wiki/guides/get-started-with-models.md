# get started with models

百炼平台提供统一的模型调用入口，支持通过 REST API 或 SDK 快速接入通义千问等大模型。本文档指导开发者完成模型服务的初始化配置、参数设置与首次调用，并明确关键约束条件。所有操作均需先完成 [API Key 配置](../../raw/model-user-guide/get-started-with-models.md) 和身份认证。

## 支持的模型与功能

当前平台支持通义千问系列（Qwen1.5、Qwen2、Qwen2.5、Qwen3）、Qwen-VL 多模态模型及部分开源微调模型，具体以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 为准。基础能力包括文本生成、对话补全、[函数调用](../concepts/function-calling.md)（tool calling）和流式响应；多模态模型支持图像理解与图文生成。注意：部分旧版文档中提及的 `qwen-max` 已于 2024 年 Q3 下线，实际可用模型请严格以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中的 `status: active` 条目为准。

## 关键参数

- `model`: 必填，字符串，取值必须来自 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 的 `model_id` 字段（如 `qwen-plus`、`qwen2.5-72b-instruct`），不支持别名或模糊匹配  
- `input.messages`: 必填，消息数组，每条消息含 `role`（`system`/`user`/`assistant`）和 `content`（字符串或结构化内容）  
- `parameters.temperature`: 可选，浮点数（0.0–2.0），默认 1.0；低于 0.1 时可能触发强制 deterministic 模式  
- `stream`: 布尔值，启用流式响应时设为 `true`，需按 SSE 协议解析事件流  

## 使用方式

1. **获取凭证**：在控制台「API 密钥」页生成有效 API Key（需绑定项目）  
2. **构造请求**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` 发送 POST 请求（[首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供完整 cURL 示例）  
3. **处理响应**：同步调用返回 JSON，含 `output.text` 或 `output.choices[0].message.content`；流式响应需监听 `event: message` 事件并拼接 `data` 字段  

> **注意**：原始文档中 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 提到可通过 `model_type` 参数动态路由，该机制已于 v2.3.0 版本废弃，现仅支持显式指定 `model` 字段，否则返回 `InvalidParameter.Model` 错误。

## 限制和注意事项

- 单次请求最大 `input.messages` 长度为 32768 token（按模型 tokenizer 计算），超限将返回 `400 Bad Request`（见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)）  
- 免费试用额度为 1000 次/日，超出后按 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 规则拒绝请求（HTTP 429）  
- 系统角色（`system`）消息仅在部分模型（如 `qwen2.5-*`）生效，`qwen-plus` 等模型会忽略该字段，建议优先使用用户消息引导行为  
- 所有模型均不支持自定义 stop words，`stop` 参数传入将被静默丢弃（参见 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 的“能力边界”章节）

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


