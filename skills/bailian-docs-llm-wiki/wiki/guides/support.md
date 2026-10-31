# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后保障政策，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态配置与策略说明。所有支持状态均以 [服务支持](../../raw/model-user-guide/support.md) 文档为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能覆盖模型调用、[异步任务](../concepts/asynchronous-task.md)提交、流式响应、批量推理等核心能力；但**不支持**模型训练、微调或私有化部署配置查询。
- 模型可用性受地域和实例类型约束，例如 `qwen-max` 仅在华东1（杭州）和华北2（北京）Region 的 Pro 实例中开放，具体以 [服务支持](../../raw/model-user-guide/support.md) 中的 Region 支持矩阵为准。

## 关键参数

- `model`: 必填，模型标识符（如 `qwen-max`, `qwen-plus`），需严格匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `model_id` 字段。
- `region`: 可选，指定查询目标地域（如 `cn-hangzhou`），缺省为调用方默认 Region；若未在 [服务支持](../../raw/model-user-guide/support.md) 的售后说明中声明支持该 region，则返回 `404`。
- `with_details`: 布尔值，默认 `false`；设为 `true` 时返回模型的输入/输出 token 限制、最大上下文长度、是否支持 tools call 等详细能力字段。

## 使用方式

通过 HTTP GET 请求访问 `/v1/support` 端点（认证方式同其他 API，需携带 `Authorization: Bearer <api_key>`）：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model=qwen-max&with_details=true" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

响应为 JSON 格式，含 `supported: boolean`、`reason: string`（如 `"model_not_found"` 或 `"region_not_supported"`）及可选的 `capabilities` 对象。错误码与含义参考 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的“API 错误响应”章节。

## 限制和注意事项

- 单日调用频次上限为 100 次/Key，超出后返回 `429 Too Many Requests`；该限制不计入配额系统，无法申请提升。
- 模型支持状态可能滞后于控制台展示——例如控制台已上线 `qwen3`，但 [服务支持](../../raw/model-user-guide/support.md) 文档尚未更新其 `region` 支持列表，此时以文档为准，避免依赖控制台 UI。
> **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注 `status: experimental` 的模型，其 `support` 接口返回的 `supported` 字段恒为 `false`，即使实际可调用；此为设计行为，非 Bug。  
> **注意**：[售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 明确排除“因用户误传参数导致的 token 超限失败”为服务故障，此类 case 不触发 SLA 补偿。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


