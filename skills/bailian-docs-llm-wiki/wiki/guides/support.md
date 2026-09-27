# support

百炼平台的 `support` 模块提供模型调用过程中的基础服务保障能力，包括模型可用性、错误响应规范、售后范围界定及合规协议支持。开发者可通过该模块了解所用模型的服务边界与技术支持路径。所有服务条款以 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 和 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 为准。

## 支持的模型/功能

- 当前支持调用的模型均来自百炼 Model Studio 官方发布列表，涵盖文本生成、代码补全、多模态理解等类别；具体模型清单请参见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)。
- 功能层面支持同步推理（`/v1/chat/completions`）、流式响应（`stream=true`）、批量请求（需启用 Batch API 权限）及基础错误码反馈（如 `429 Too Many Requests`, `400 Invalid Parameter`）。
- 不支持模型微调任务的实时在线调试、私有化部署环境下的本地日志回传，此类需求需通过工单系统单独申请。

## 关键参数

- `model`: 必填，必须为 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中明确标注“已上线”的模型 ID（如 `qwen-max`, `qwen-plus`），不接受别名或版本后缀（如 `qwen-max-202406`）。
- `timeout`: 可选，单位为秒，默认 60；超过该值将触发 `504 Gateway Timeout`，但实际超时由网关层统一控制，客户端设置仅作参考。
- `request_id`: 建议携带，用于问题定位；若未提供，平台将自动生成 UUID v4 格式 ID 并返回于响应头 `X-Request-ID`。

## 使用方式

1. 确保 API Key 已在百炼控制台开通对应模型的调用权限；
2. 发起标准 OpenAI 兼容格式 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/chat/completions`；
3. 在请求头中添加 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`；
4. 错误响应体遵循 RFC 7807 标准，含 `type`, `title`, `status`, `detail` 字段，便于结构化解析。

## 限制和注意事项

- 单账户默认 QPS 限制为 5（部分大模型为 1），超出将返回 `429`；配额可于控制台「API 调用管理」中申请提升。
- 流式响应中 `delta.content` 字段可能为空字符串（尤其在首 chunk 含 system [prompt](prompt.md) 时），客户端需容错处理，不可假设每 chunk 均含有效文本。
- > **注意**：[常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中提及的“免费额度可叠加使用”已于 2024 年 7 月起失效，当前免费额度按自然月重置且不可跨月累积，以 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 最新版本为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


