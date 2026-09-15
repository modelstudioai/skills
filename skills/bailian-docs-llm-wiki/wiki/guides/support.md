# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后保障政策，是开发者集成前必查的元信息入口。该接口不提供实时推理能力，仅返回静态服务元数据，适用于初始化配置、兼容性校验与合规性审查。所有响应内容以平台最新发布版本为准，历史文档可能滞后。

## 支持的模型/功能

- 当前支持的模型详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，涵盖通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方授权模型。
- 功能覆盖文本生成、多模态理解、语音转写、代码补全等，但具体能力需结合各模型的 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 判断是否包含商用授权。
- > **注意**：[模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为“Beta”的模型，其 API 行为与正式版可能存在差异，建议在生产环境使用前查阅 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中的兼容性说明。

## 关键参数

- `format`: 可选 `json`（默认）或 `markdown`，控制返回结构化程度；
- `scope`: 可选 `all`（全部模型）、`public`（公开可用）、`private`（租户专属），默认为 `public`；
- `version`: 指定模型版本号（如 `qwen2.5-7b`），留空则返回最新稳定版元数据。

## 使用方式

调用 `GET /v1/support`（需携带有效的 `Authorization: Bearer <token>`），示例请求：
```bash
curl -H "Authorization: Bearer $API_KEY" \
     "https://dashscope.aliyuncs.com/api/v1/support?scope=public&format=json"
```
响应为标准 JSON，含 `models[]` 数组，每项包含 `id`、`name`、`status`（active/beta/deprecated）、`input_types` 和 `output_types` 字段。详细字段定义参见 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 的附录 A。

## 限制和注意事项

- 接口限流为 10 QPS / 租户，超出将返回 `429 Too Many Requests`；
- 不支持跨地域查询，请求必须发往与租户绑定的 Region Endpoint；
- `deprecated` 状态模型虽可查到，但已停止维护，其 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 明确不提供故障响应与 SLA 保障；
- > **注意**：[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中关于“免费额度是否适用于 support 接口”的描述已过时——自 2024 年 8 月起，该接口调用不计入任何免费额度，但也不产生计费。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


