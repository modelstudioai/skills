# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息获取等，主要用于调试与可观测性场景。该接口不参与模型推理逻辑，而是作为配套服务存在，需配合具体模型调用（如 `chat` 或 `embed`）使用。详细服务范围和责任边界请参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md)。

## 支持的模型/功能

- 当前仅对百炼平台托管的 **SaaS 模型**（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）提供 `support` 接口支持；自部署模型（BYOM）暂不支持。
- 功能覆盖：请求 ID 查询、失败原因解析、[Token](../concepts/token.md) 使用量回溯、限流状态反馈。不提供模型权重下载、微调日志导出或训练过程监控。
- 完整受支持模型清单见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `request_id` | string | 是 | 调用主接口（如 `/v1/chat/completions`）返回的 `id` 字段值，用于关联查询 |
| `include_trace` | boolean | 否 | 是否返回完整调用链路（默认 `false`，仅返回摘要） |
| `timeout_ms` | integer | 否 | 查询超时毫秒数，取值范围 `100–5000`，默认 `1000` |

> **注意**：部分旧版文档中将 `include_trace` 描述为默认 `true`，但实际行为以 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中最新说明为准（v2024.06 起已统一为 `false`）。

## 使用方式

1. 在调用主模型接口（如 `chat`）时，记录响应头中的 `X-Request-ID` 或响应体中的 `id`；
2. 向 `POST /v1/support/query` 发起请求，携带上述 `request_id`；
3. 解析返回的 JSON，重点关注 `status`（`success`/`failed`/`timeout`）、`error_code`（如 `RATE_LIMIT_EXCEEDED`）、`usage`（含 `prompt_tokens`/`completion_tokens`）字段。

示例请求：
```bash
curl -X POST https://dashscope.aliyuncs.com/v1/support/query \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"request_id": "req-xxx", "include_trace": false}'
```

## 限制和注意事项

- 单个 `request_id` 最多可查询 **3 次**，超过后返回 `404 Not Found`；
- 查询窗口期为请求发起后 **30 分钟**，超时后数据自动清理；
- 不支持跨账号查询，且仅返回当前 API Key 所属项目下的请求记录；
- 若发现响应中 `error_code` 为 `UNKNOWN_REQUEST_ID`，请确认是否调用的是 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中明确列出的受支持模型及接口路径。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


