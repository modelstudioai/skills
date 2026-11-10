# get started with models

百炼平台提供统一的模型调用入口，支持多种大语言模型、多模态模型及定制化模型的快速接入与推理。开发者可通过 REST API 或 SDK 调用模型，无需管理底层基础设施。本文档梳理核心使用路径、参数规范及关键约束，帮助开发者高效启动模型集成。

## 支持的模型与功能

平台当前支持通义千问（Qwen）系列、Qwen-VL、Qwen-Audio 等开源及闭源模型，涵盖文本生成、对话理解、图像描述、语音转写等能力。模型列表持续更新，完整清单见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)。所有模型均通过统一的 Model Studio 接入，其架构与服务边界详见 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：部分文档中提及的“Qwen2-72B-Instruct”在 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中标注为“仅限企业版”，但 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 当前未体现该限制，建议以控制台实际可选模型为准。

## 关键参数

调用模型时需指定以下必需参数：
- `model`: 模型标识符（如 `qwen-max`、`qwen-plus`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中名称严格一致；
- `input.messages`: 对话历史数组，每项含 `role`（`user`/`assistant`/`system`）和 `content`；
- `parameters.temperature`、`top_p` 等采样参数影响输出随机性，取值范围参考各模型文档。

## 使用方式

1. 获取 API Key（通过百炼控制台「API 密钥管理」创建）；  
2. 构造 POST 请求至 `/v1/services/aigc/text-generation/generation`（文本类）或对应多模态端点；  
3. 设置 `Authorization: Bearer <API_KEY>` 与 `Content-Type: application/json`；  
4. 发送 JSON payload，解析响应中的 `output.text` 或 `output.choices[0].message.content`。

SDK 调用方式详见各语言示例（Python/Java/Go），错误处理逻辑应覆盖 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 中定义的 HTTP 状态码与 code 字段。

## 限制和注意事项

- 默认调用频率受 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 约束（如 `qwen-max` 免费版为 5 QPS）；  
- 输入长度上限因模型而异（例如 `qwen-turbo` 最大 context 长度为 8K tokens），超出将返回 400 错误；  
- 服务可用性依赖地域部署，[地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 明确了各 Region 的模型支持状态与 SLA；  
- 所有请求需在 60 秒内完成，超时将中断连接并返回 `RequestTimeout` 错误。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


