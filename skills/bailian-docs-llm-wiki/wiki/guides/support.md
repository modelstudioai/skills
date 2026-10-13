# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后保障政策，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态配置与策略说明。所有支持状态均以 [服务支持](../../raw/model-user-guide/support.md) 文档为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能覆盖模型调用、异步任务提交、流式响应、批量推理等基础能力；高级功能（如[函数调用](../concepts/function-calling.md)、多模态结构化输出）需结合具体模型能力确认，参见 [服务支持](../../raw/model-user-guide/support.md) 中的链接索引。
- 售后服务范围（如 SLA、故障响应时效、计费异常处理）定义在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)，开发者应据此评估业务容错设计。

## 关键参数

- `model_id`（可选）：指定模型 ID，用于查询单个模型的详细支持状态（如是否启用流式、最大上下文长度等），若未提供则返回全量模型摘要。
- `format`（可选，默认 `json`）：响应格式，支持 `json` 和 `markdown`，后者便于快速阅读，但不适用于程序解析。
- `include_deprecated`（布尔，默认 `false`）：是否包含已标记为废弃（deprecated）的模型，生产环境建议保持默认值。

## 使用方式

通过 HTTP GET 请求访问 `/v1/support` 端点，需携带有效的 `Authorization: Bearer <api_key>` 头。示例请求：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model_id=qwen-max" \
  -H "Authorization: Bearer sk-xxx"
```

响应体为 JSON 对象，含 `models` 数组及 `service_policies` 字段。完整字段定义与示例请参考 [服务支持](../../raw/model-user-guide/support.md)。

## 限制和注意事项

- 单日调用频率上限为 100 次，超出后返回 `429 Too Many Requests`；高频查询建议本地缓存并定期刷新（推荐 TTL ≤ 24h）。
- 返回的模型列表**不保证实时性**：新模型上线或下线可能存在最多 2 小时延迟，关键业务应以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 的最新更新时间戳为准。
- > **注意**：[服务支持](../../raw/model-user-guide/support.md) 中提及“所有模型默认支持[函数调用](../concepts/function-calling.md)”，但 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 明确标注 `qwen-turbo` 不支持该功能——请以模型列表中的具体能力字段为准，此处为文档过时表述。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


