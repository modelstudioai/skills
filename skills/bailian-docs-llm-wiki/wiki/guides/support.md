# support

百炼平台的 `support` 接口用于查询当前服务支持的模型能力、服务范围及售后政策，不提供实时推理功能，仅作为元信息查询入口。开发者可通过该接口确认模型可用性、调用限制及合规要求。所有返回内容均以平台最新控制台配置和[服务支持](../../raw/model-user-guide/support.md)文档为准。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包含通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方授权模型。
- 功能覆盖文本生成、多模态理解、语音转写、代码补全等，但具体能力需以各模型在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注的“支持能力”字段为准。
- 不支持动态模型注册或自定义模型接入；新增模型需等待平台统一发布，详情参见 [服务支持](../../raw/model-user-guide/support.md)。

## 关键参数

- `model_id`（必选，string）：模型唯一标识，必须与 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中列出的 ID 完全一致（区分大小写，含版本后缀如 `qwen-max-20240806`）。
- `region_id`（可选，string）：指定地域，默认为用户主账号所在 region；跨 region 查询可能返回空结果。
- `with_quota`（布尔，默认 `false`）：设为 `true` 时返回当前账号在该模型下的剩余调用量与速率限制。

## 使用方式

通过 HTTP GET 请求调用 `/v1/support/models`（鉴权方式同其他百炼 API，需携带 `Authorization: Bearer <api_key>`）：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/support/models?model_id=qwen-plus&with_quota=true" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

响应为 JSON 格式，包含 `model_id`、`status`（`available` / `unavailable` / `deprecated`）、`capabilities` 数组及配额信息（当 `with_quota=true` 时）。完整字段说明请参考 [服务支持](../../raw/model-user-guide/support.md)。

## 限制和注意事项

- 单次请求最多查询 10 个 `model_id`（批量传入时以逗号分隔），超出将返回 400 错误。
- `deprecated` 状态模型仍可调用，但已停止维护，建议尽快迁移；其详细下线时间以 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 公告为准。
> **注意**：[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中关于“免费额度自动续期”的描述与当前控制台策略不一致——实际规则为按自然月重置，非滚动周期，以 [服务支持](../../raw/model-user-guide/support.md) 及控制台实时展示为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


