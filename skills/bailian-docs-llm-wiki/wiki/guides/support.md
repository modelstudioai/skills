# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后能力边界，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态配置与策略说明。所有支持状态均以 [服务支持](../../raw/model-user-guide/support.md) 文档为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含百炼自研模型（如 Qwen 系列）及部分经认证的第三方模型。
- 功能覆盖模型调用、微调、部署、监控等全生命周期环节，但具体可用性因模型而异；例如，部分模型仅支持 API 调用，不支持私有化微调，详情请参考 [服务支持](../../raw/model-user-guide/support.md) 中的“功能矩阵”章节。
- 语音、多模态等扩展能力需单独开通权限，其支持状态同步更新至 [服务支持](../../raw/model-user-guide/support.md) 的附录表格中。

## 关键参数

- `model_id`（必填）：模型唯一标识，须与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中列出的 ID 完全一致，区分大小写。
- `region`（可选）：指定地域，默认为 `cn-shanghai`；若目标模型未在该 region 部署，将返回 `404 Not Supported`。
- `with_capability`（布尔值，默认 `false`）：设为 `true` 时返回该模型支持的具体能力标签（如 `"streaming"`, `"function_calling"`），标签定义见 [服务支持](../../raw/model-user-guide/support.md) 附录。

## 使用方式

通过 HTTP GET 请求访问 `/v1/support/models`（需携带有效 `Authorization` 头）：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support/models?model_id=qwen-max&with_capability=true" \
  -H "Authorization: Bearer $API_KEY"
```

响应体为 JSON，含 `model_id`, `status`（`active`/`deprecated`/`unavailable`），及 `capabilities` 数组（当 `with_capability=true` 时）。  
> **注意**：文档中提及的 `/v1/support/features` 路径已在 v2.3.0 版本中废弃，实际应统一使用 `/v1/support/models` —— 请以 [服务支持](../../raw/model-user-guide/support.md) 的最新版接口说明为准。

## 限制和注意事项

- 单次请求最多查询 10 个 `model_id`（逗号分隔），超出将返回 `400 Bad Request`。
- `deprecated` 状态模型仍可调用，但不再接收功能更新，建议在 3 个月内迁移到 `active` 模型。
- 所有支持信息按季度人工校验并发布，若发现 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 与控制台实时显示不一致，请以控制台为准，并同步反馈至工单系统。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


