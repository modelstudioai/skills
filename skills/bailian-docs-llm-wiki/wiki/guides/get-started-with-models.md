# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、调用方式、关键参数配置及常见约束。所有模型均通过统一 API 接口调用，支持同步推理与流式响应。建议首次使用前阅读 [开始使用 (raw/model-user-guide/get-started-with-models.md)](../../raw/model-user-guide/get-started-with-models.md) 中的导航结构。

## 支持的模型与核心功能

- 当前支持的模型包括 `qwen2.5-7b`、`qwen2.5-72b`、`qwen3-8b`、`qwen3-32b`、`qwen4-max` 等（详见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)）；其中 `qwen4-max` 为最新旗舰模型，具备更强的多步推理与工具调用能力，其详细规格见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)。
- 功能覆盖文本生成、[函数调用](../concepts/function-calling.md)（Function Calling）、JSON Schema 输出、多模态输入（部分模型）、以及系统提示词（system prompt）控制。
- 所有模型均部署在百炼 Model Studio 统一管控下，支持按需启用/停用、版本灰度与自定义 endpoint 配置。

## 关键参数

调用时必需指定以下参数：
- `model`: 模型标识符（如 `"qwen3-32b"`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中的名称严格一致；
- `input.messages`: 非空消息数组，至少包含一个 `user` 角色消息；
- `parameters.temperature`: 浮点数（0.0–2.0），默认 `0.8`；设为 `0` 可启用确定性输出（推荐用于[函数调用](../concepts/function-calling.md)场景）；
- `parameters.top_p`: 浮点数（0.0–1.0），默认 `0.95`；与 `temperature` 互斥生效，二者同时设置时以 `temperature` 为准。

> **注意**：[开始使用 (raw/model-user-guide/get-started-with-models.md)](../../raw/model-user-guide/get-started-with-models.md) 中提及的 `max_tokens` 参数在 v2.1+ API 中已更名为 `parameters.max_output_tokens`，旧字段名将被忽略，请务必使用新命名。

## 使用方式

1. **认证**：使用 `X-DashScope-Access-Token` 请求头传入 API Key（需在 [DashScope 控制台](https://dashscope.console.aliyun.com/) 获取）；
2. **Endpoint**：统一调用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
3. **示例请求体**：
   ```json
   {
     "model": "qwen3-32b",
     "input": {
       "messages": [{"role": "user", "content": "你好"}]
     },
     "parameters": {
       "temperature": 0.5,
       "max_output_tokens": 512
     }
   }
   ```
4. 响应解析参考 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 文档，重点关注 `status_code` 和 `code` 字段。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（具体依模型而异，`qwen4-max` 支持 65536）；
- 默认 QPS 限流为 5，可通过 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档申请提升；
- 模型服务地域隔离，调用前需确认所选模型已在目标 Region（如 `cn-beijing`、`ap-southeast-1`）部署，参见 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)；
- 不支持跨模型 session 状态保持，每次请求均为无状态独立调用。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


