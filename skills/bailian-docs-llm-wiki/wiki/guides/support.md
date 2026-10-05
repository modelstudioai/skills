# support

百炼平台的 `support` 接口用于查询当前服务支持的模型列表、功能范围及售后政策等基础信息，主要面向开发者进行集成前的兼容性确认与服务边界评估。该接口不提供实时推理能力，仅返回静态元数据和策略说明。所有内容均以平台最新发布的模型服务协议与模型 Studio 文档为准。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方授权模型。
- 功能覆盖模型调用、微调、部署、RAG 增强、Agent 编排等核心能力，具体以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中定义的服务等级协议（SLA）为准。
- 售后支持范围（如故障响应时效、问题分类标准）请参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 关键参数

- `service_type`：必填，取值为 `model`, `fine-tuning`, `deployment`, `rag`, `agent` 之一，用于限定查询维度；
- `region_id`：可选，指定地域 ID（如 `cn-beijing`），影响返回的可用模型与服务节点；
- `version`：可选，指定 API 版本（默认 `v1`），历史版本行为可能与 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中描述存在差异。

## 使用方式

通过 HTTP GET 请求调用 `/v1/support` 端点，需携带有效的 `Authorization` Bearer Token。示例请求：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support?service_type=model&region_id=cn-hangzhou" \
  -H "Authorization: Bearer $API_KEY"
```

响应为 JSON 格式，包含 `models`, `features`, `policies` 三个顶层字段，结构与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 的 schema 保持一致。

## 限制和注意事项

- 单日调用频次上限为 100 次/项目（Project），超出后返回 `429 Too Many Requests`；
- `region_id` 参数仅对部署类服务生效，对模型元数据查询无实际过滤作用，此行为与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中“地域一致性保障”条款存在表述偏差；
> **注意**：[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中称 `support` 接口支持 `format=markdown` 输出，但实测仅接受 `application/json`，该功能已下线且未在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中同步更新，建议忽略该参数。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


