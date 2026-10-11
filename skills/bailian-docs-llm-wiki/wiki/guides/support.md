# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后保障政策，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态配置与策略说明。所有支持状态均以 [服务支持](../../raw/model-user-guide/support.md) 文档为准。

## 支持的模型/功能

- 支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能覆盖模型调用、异步任务提交、流式响应、批量推理等核心能力；但**不支持**模型训练、微调或私有化部署配置查询。
- 模型可用性受地域和实例类型约束，具体以控制台实际展示为准，而非 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的全量清单。

## 关键参数

- `model_id`（必填）：模型唯一标识，需严格匹配 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中的 `model_id` 字段值，区分大小写与连字符。
- `region_id`（可选）：指定地域 ID（如 `cn-shanghai`），未指定时默认返回全局支持列表；部分模型仅在特定 region 可用。
- `with_capability`（布尔，默认 `false`）：设为 `true` 时返回各模型支持的 capabilities（如 `streaming`, `function_calling`）。

## 使用方式

通过 HTTP GET 请求调用 `/v1/support` 端点，需携带有效的 `Authorization: Bearer <api_key>` 头。示例请求：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model_id=qwen-max&region_id=cn-shanghai" \
  -H "Authorization: Bearer sk-xxx"
```

响应为 JSON 格式，含 `supported`, `capabilities`, `service_scope` 等字段。完整字段定义与示例见 [服务支持](../../raw/model-user-guide/support.md)。

## 限制和注意事项

- 单日调用频率上限为 1000 次/项目（Project），超出后返回 `429 Too Many Requests`。
- 返回的 `service_scope` 字段引用 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)，但注意：该文档中关于“7×24 小时人工响应”的描述**已过时**，实际 SLA 以控制台「服务协议」页最新版本为准。
- > **注意**：[服务支持](../../raw/model-user-guide/support.md) 中列出的 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 链接路径已失效，正确路径应为 `raw/legal/acceptance-agreement.md`，请勿直接跳转原链接。
- 不支持跨账号查询；`model_id` 若不存在或已下线，返回 `404 Not Found` 而非空列表。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


