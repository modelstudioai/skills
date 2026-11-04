# support

百炼平台的 `support` 接口用于查询模型服务的可用性、能力范围及售后保障信息，是开发者集成前验证环境兼容性和服务边界的必要入口。该接口不直接执行推理，而是提供元数据级支持能力查询，适用于自动化部署检查与合规性预检。所有返回字段均以结构化 JSON 形式交付，符合 OpenAPI 3.0 规范。

## 支持的模型/功能

当前 `support` 接口覆盖百炼 Model Studio 中全部已上线模型，包括通义千问系列（Qwen1、Qwen2、Qwen2.5、Qwen3）、Qwen-VL、Qwen-Audio 等多模态模型，以及部分第三方托管模型（如 Llama-3-70b-Instruct）。具体模型清单以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 为准。接口支持按 `model_id` 查询单模型能力矩阵（如是否支持[流式输出](../concepts/streaming-output.md)、function calling、JSON Schema 输出等），也支持全量模型能力摘要聚合。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model_id` | string | 否 | 指定模型 ID；为空时返回全部模型摘要 |
| `capability` | string[] | 否 | 过滤能力标签，如 `["stream", "tools", "json_output"]`；详见 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中“能力标识定义”章节 |
| `region_id` | string | 否 | 指定地域（如 `cn-shanghai`），影响可用模型集；默认为调用方 AK 所属主地域 |

> **注意**：`capability` 参数在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中被标记为“仅用于前端展示过滤”，但实际 API 已支持后端能力校验——请以 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 的最新版行为说明为准。

## 使用方式

通过 HTTP GET 请求调用 `/v1/support` 端点，需携带有效的 `Authorization: Bearer <access_token>` 头。示例请求：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model_id=qwen-max" \
  -H "Authorization: Bearer sk-xxx"
```

响应体包含 `models` 数组（每个元素含 `id`, `status`, `capabilities`, `region_availability` 字段）及 `meta.last_updated` 时间戳。完整字段定义与错误码见 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 附录 C。

## 限制和注意事项

- 单账号 QPS 限流为 5，超出返回 `429 Too Many Requests`；
- `model_id` 必须精确匹配（区分大小写），不支持模糊匹配或通配符；
- 返回的 `region_availability` 字段仅表示模型在该地域“已部署”，不代表具备实时服务能力——实际调用仍需结合 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中的服务 SLA 条款判断可用性；
- 非企业版账号无法查询部分商用模型（如 `qwen-plus`）的完整能力矩阵，该限制在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中有明确标注。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


