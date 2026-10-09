# support

百炼平台的 `support` 模块提供模型服务可用性、功能边界及售后保障的统一说明，覆盖模型支持范围、关键调用参数、接入方式和使用约束。开发者应结合具体模型能力文档与售后条款进行集成设计。所有服务均以 [服务支持](../../raw/model-user-guide/support.md) 为总览入口。

## 支持的模型/功能

当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖通义千问系列（Qwen1.5/Qwen2/Qwen2.5/Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。功能支持包括文本生成、多模态推理、流式响应、[函数调用](../concepts/function-calling.md)（Tool Calling）等，具体以各模型在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注的 capability 字段为准。> **注意**：部分旧版文档中提及的“Qwen1”已归档，实际可用模型请以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 的 latest 标签为准，避免参考过时的模型别名。

## 关键参数

调用 `support` 相关接口（如 `/v1/models` 或控制台模型元数据查询）时，核心参数包括：  
- `model`（必填，字符串，需与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 model_id 完全一致）  
- `response_format`（可选，支持 `json_object` 或 `text`，影响输出结构）  
- `max_tokens`（受模型最大上下文限制，具体值见对应模型文档）  
参数合法性校验由服务端执行，非法值将返回 `400 Bad Request` 并附错误码。

## 使用方式

1. 控制台：进入「模型服务」→「模型列表」，点击目标模型查看实时支持状态与功能开关；  
2. API：通过 `GET /v1/models` 获取全部支持模型元数据，或 `GET /v1/models/{model}` 查询单个模型详情；  
3. SDK：使用 `dashscope` Python SDK 时，调用 `dashscope.get_model_list()` 或实例化 `Generation` 时传入合法 `model` 参数即可触发支持校验。所有行为均遵循 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中定义的服务等级协议（SLA）。

## 限制和注意事项

- 免费试用额度仅适用于首次开通的账号，且不覆盖商用场景，详细范围见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)；  
- 某些模型（如 Qwen-VL-Pro）需单独申请权限，未授权调用将返回 `403 Forbidden`；  
- 流式响应（`stream=true`）不支持所有模型，是否可用请严格参照 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `streaming_supported` 字段；  
- 跨区域调用（如华东1调用华北2部署的模型）可能触发额外延迟或失败，建议就近部署应用。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


