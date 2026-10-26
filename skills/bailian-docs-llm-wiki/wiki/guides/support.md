# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后能力边界，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态配置与策略说明。所有支持状态均以 [服务支持](../../raw/model-user-guide/support.md) 文档为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能覆盖模型调用、[异步任务](../concepts/asynchronous-task.md)提交、流式响应、批量推理等核心能力；但**不支持**模型训练、微调触发或权重导出。
- 模型可用性受地域和实例类型约束，例如 `qwen-max` 仅在华东1（杭州）和华北2（北京）的 Pro 实例中开放，具体以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `region_availability` 字段为准。

## 关键参数

调用 `support` 接口时需指定以下参数（均为可选）：
- `model`：模型 ID（如 `qwen-max`），用于过滤该模型的详细支持项；
- `feature`：功能标识符（如 `streaming`、`function_calling`），返回该功能在各模型下的兼容状态；
- `format`：响应格式，支持 `json`（默认）和 `markdown`。

> **注意**：原始文档 [服务支持](../../raw/model-user-guide/support.md) 中未定义任何请求参数，实际 API 行为以 OpenAPI 规范为准；参数定义应以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 的 schema 描述为权威依据。

## 使用方式

- HTTP 方法：`GET`
- Endpoint：`/v1/support`
- 示例请求：
  ```bash
  curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model=qwen-plus&feature=streaming" \
    -H "Authorization: Bearer $API_KEY"
  ```
- 响应为 JSON 对象，含 `supported: boolean`、`reason: string` 和 `constraints: object` 字段。完整字段语义见 [服务支持](../../raw/model-user-guide/support.md)。

## 限制和注意事项

- 单账户每分钟限流 60 次，超出后返回 `429 Too Many Requests`；
- `model` 参数值必须严格匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中公布的 ID，大小写敏感，不支持别名或版本通配（如 `qwen2-*`）；
- 返回结果不含实时状态（如模型临时下线），仅反映配置态支持；运行时异常请结合 `status` 接口或日志诊断；
- 所有售后范围、SLA 承诺及免责条款以 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 为准，该文档明确排除因用户误用参数导致的失败归责。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


