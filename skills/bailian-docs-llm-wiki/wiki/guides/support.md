# support

百炼平台的 `support` 接口用于查询当前服务支持的模型能力、服务范围及售后政策，是开发者集成前必查的元信息入口。它不提供实时推理能力，而是返回静态的、平台级的服务声明数据。所有响应内容均以 JSON 格式返回，结构稳定，适用于自动化校验与配置初始化。

## 支持的模型/功能

平台当前支持的模型列表由模型工坊（Model Studio）统一维护，涵盖通义千问系列（Qwen）、语音合成（TTS）、多模态理解（如 Qwen-VL）等类别。具体模型名称、版本号、输入输出格式及是否支持流式响应，详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)。注意：部分旧版文档中列出的实验性模型（如 `qwen-vl-preview-202312`）已在最新 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中移除，实际调用将返回 `404`。

## 关键参数

调用 `support` 接口时需传入以下参数（均为可选）：

- `model`: 指定模型 ID，用于查询该模型的详细支持能力（如 `qwen-max`）；
- `format`: 响应格式，仅支持 `json`（默认）；
- `include_deprecated`: 布尔值，设为 `true` 时返回已废弃但暂未下线的模型（默认 `false`）。

> **注意**：`include_deprecated` 参数在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中未被提及，其行为以 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 的“API 元数据查询”章节为准。

## 使用方式

通过 HTTP GET 请求访问 `/v1/support` 端点（需携带有效的 `Authorization: Bearer <api_key>` 头）。示例请求：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?model=qwen-plus" \
  -H "Authorization: Bearer sk-xxx"
```

响应包含 `models`（支持模型数组）、`service_scope`（服务地域与合规说明）和 `version`（元数据版本戳）。完整字段定义请参考 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中的附录 A。

## 限制和注意事项

- 单 IP 每分钟最多 60 次请求，超出将返回 `429 Too Many Requests`；
- `model` 参数仅接受平台注册的合法模型 ID，大小写敏感，非法值返回 `400 Bad Request`；
- 该接口不校验用户配额或模型开通状态，仅反映平台全局服务能力；  
- 所有返回的模型信息以 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 为准，其他文档（如过时的 FAQ 快照）若存在版本差异，一律以该文档为权威来源。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


