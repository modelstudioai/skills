# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后能力边界，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态配置与策略说明。所有支持状态均以 [服务支持](../../raw/model-user-guide/support.md) 文档为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能覆盖模型调用、[异步任务](../concepts/asynchronous-task.md)提交、流式响应、批量推理等基础能力；高级功能（如自定义工具调用、RAG 插件链）需单独确认模型兼容性，参见 [服务支持](../../raw/model-user-guide/support.md) 中的“功能矩阵”章节。
- 所有已上线模型均支持标准 REST API 与 SDK 调用，但部分模型（如 Qwen2.5-72B）暂不开放[流式输出](../concepts/streaming-output.md)，具体以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 的 `streaming_supported` 字段为准。

## 关键参数

- `model_id`（必需）：模型唯一标识符，必须与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中列出的 `model_id` 完全一致，区分大小写。
- `region`（可选）：指定服务地域，默认为 `cn-beijing`；跨区域调用可能触发额外延迟或权限限制。
- `with_capability`（可选，布尔值）：设为 `true` 时返回该模型支持的具体能力标签（如 `"function_calling"`, `"vision"`），否则仅返回基础元数据。

## 使用方式

通过 `GET /v1/support/models` 发起请求，需携带有效的 `Authorization: Bearer <api_key>` 头。示例：
```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support/models?model_id=qwen2.5-7b-instruct" \
  -H "Authorization: Bearer sk-xxx"
```
响应为 JSON 格式，包含 `model_id`, `status`, `capabilities`, `max_input_tokens` 等字段。完整字段定义请参考 [服务支持](../../raw/model-user-guide/support.md)。

## 限制和注意事项

- 单日调用频次上限为 100 次/项目（Project），超出后返回 `429 Too Many Requests`。
- `model_id` 不支持模糊匹配或别名（如 `qwen2.5` 不等价于 `qwen2.5-7b-instruct`），必须精确匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的值。
> **注意**：原始文档中 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 提到“模型不可用时提供 72 小时内补偿”，但该条款已于 2024 年 6 月起调整为“按 SLA 协议执行”，最新细则以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 附录 C 为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


