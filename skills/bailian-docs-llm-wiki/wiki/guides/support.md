# support

百炼平台的 `support` 接口用于查询当前服务支持的模型能力、服务范围及售后政策，是开发者集成前必查的基础信息通道。该接口不提供实时推理能力，仅返回静态元数据与策略说明。所有内容均以 [服务支持 (raw/model-user-guide/support.md)](../../raw/model-user-guide/support.md) 为权威来源。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖 Qwen 系列（如 qwen-max、qwen-plus）、开源微调模型及部分第三方模型（需单独开通权限）。
- 功能支持包括：同步文本生成、异步任务提交、流式响应（仅限部分模型）、基础图像理解（multimodal 模型需显式启用 `enable_multimodal: true`）。
- 不支持的功能：实时语音流式输入、原生视频理解、本地模型热加载。这些限制在 [服务支持 (raw/model-user-guide/support.md)](../../raw/model-user-guide/support.md) 中明确列出。

## 关键参数

- `model`: 必填，模型 ID，必须来自 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的有效值，大小写敏感。
- `with_capability`: 可选，布尔值，默认 `false`；设为 `true` 时返回该模型支持的具体能力（如 `tool_use`、`json_output`）。
- `region`: 可选，指定服务地域（如 `cn-beijing`），影响可用模型集；未指定时使用账户默认 region。

## 使用方式

通过 HTTP GET 请求访问 `/v1/support` 端点（认证方式同其他 API，需携带 `Authorization: Bearer <api_key>`）：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model=qwen-max&with_capability=true" \
  -H "Authorization: Bearer sk-xxx"
```

响应为 JSON，包含 `model`, `status`, `capabilities`, `region_scoped` 等字段。完整字段定义请参考 [服务支持 (raw/model-user-guide/support.md)](../../raw/model-user-guide/support.md)。

## 限制和注意事项

- 单账户每分钟最多 60 次请求，超出将返回 `429 Too Many Requests`。
- `model` 参数若传入非列表中模型，返回 `400 Bad Request` 并附错误码 `ModelNotSupported`。
> **注意**：文档 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中提及“7×24 小时技术支持”，但实际工单响应 SLA 为工作日 5×8 小时（依据最新 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 第 3.2 条），请以协议文本为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


