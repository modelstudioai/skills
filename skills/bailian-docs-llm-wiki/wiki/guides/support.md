# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后保障政策，是开发者集成前确认兼容性与服务能力的关键入口。该接口不提供实时推理能力，仅返回元数据和策略说明。所有支持信息均以 [服务支持](../../raw/model-user-guide/support.md) 为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖 Qwen 系列（如 qwen-max、qwen-plus）、开源微调模型及部分第三方授权模型。
- 功能支持包括：同步/异步调用、流式响应、自定义 system [prompt](prompt.md)、多轮对话上下文管理（最大 32K tokens），但**不支持**训练任务提交或模型权重导出。
- 模型能力边界（如是否支持 vision、code、tool calling）需交叉核对 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `capabilities` 字段，而非仅依赖通用文档描述。

## 关键参数

- `model`: 必填，字符串类型，必须为 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确列出的 model_id（区分大小写，如 `qwen-max`）。
- `with_capability`: 可选布尔值，默认 `false`；设为 `true` 时返回该模型支持的具体能力（如 `"vision": true`, `"tools": false`）。
- `format`: 可选，取值 `"json"` 或 `"markdown"`，影响响应结构化程度；默认 `"json"`。

## 使用方式

通过 HTTP GET 请求访问 `https://dashscope.aliyuncs.com/api/v1/support?model=qwen-max`（需携带有效的 `Authorization: Bearer <api_key>` 头）。  
响应示例（`with_capability=true`）：
```json
{
  "model": "qwen-max",
  "status": "active",
  "capabilities": ["chat", "vision", "function_calling"],
  "max_input_tokens": 32768,
  "max_output_tokens": 8192
}
```
> **注意**：[服务支持](../../raw/model-user-guide/support.md) 中提及的“支持批量模型查询”功能尚未上线，实际 API 仅支持单 model 查询，该描述已过时。

## 限制和注意事项

- 单次请求仅支持一个 `model` 参数，不支持逗号分隔或多值数组。
- 接口无配额限制，但受百炼平台整体 API 调用频控约束（默认 10 QPS / key）。
- 返回的 `status: "active"` 表示模型可调用，但不保证实时可用性；若模型正在维护，仍可能返回 `503 Service Unavailable`，建议捕获 HTTP 状态码而非仅依赖响应体字段。
- 售后服务范围（如 SLA、故障响应时效）以 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 为准，与模型能力无关。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


