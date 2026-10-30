# support

百炼平台的 `support` 接口提供模型调用过程中的基础服务支持能力，包括错误诊断、请求追踪、响应元信息返回等，主要用于调试与问题排查。该能力默认启用，无需额外配置，但部分高级功能需配合特定参数或模型版本使用。开发者应结合 [服务支持](../../raw/model-user-guide/support.md) 文档理解整体支持范围。

## 支持的模型/功能

- 所有在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中标注为“已上线”且状态为“可用”的模型均支持基础 `support` 行为（如 `x-request-id` 返回、错误码标准化）。
- 高级支持功能（如详细 token 级错误定位、输入内容合规性反馈）仅限 `qwen-plus`、`qwen-max` 及 `qwen-turbo` 的 v20240815 及之后版本。
- 流式响应（`stream=true`）下，`support` 会附加 `x-trace-id` 和 `x-error-detail`（若发生中间错误），该行为在 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中明确界定为 SLA 可观测性保障项。

## 关键参数

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `support_trace` | boolean | 否 | 设为 `true` 时强制返回 `x-trace-id` 与完整链路日志标识；默认 `false`（仅错误时返回） |
| `support_debug` | boolean | 否 | 设为 `true` 时在响应头中返回 `x-debug-info`（含模型内部处理阶段耗时），**仅限 dev 环境生效** |
| `support_level` | string | 否 | 可选 `basic`（默认）、`detailed`；`detailed` 激活 token 级错误标记，需模型支持（见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 标注） |

> **注意**：`support_debug=true` 在生产环境强制忽略，且不触发计费减免——这与 [常见问题](../../raw/model-user-guide/support/faq-about-alibaba-cloud-model-studio.md) 中旧版 FAQ 第 7 条描述存在冲突，以当前 API 行为为准。

## 使用方式

通过标准 HTTP 请求头或 query 参数启用：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen-max",
        "input": {"messages": [{"role": "user", "content": "你好"}]},
        "parameters": {"support_trace": true, "support_level": "detailed"}
      }'
```
响应头中将包含 `x-request-id`、`x-trace-id`（当启用 trace 时）及 `x-error-detail`（当发生可定位错误时）。

## 限制和注意事项

- 单次请求最多允许同时启用 `support_trace` 和 `support_level=detailed`，二者不可与 `stream=true` 组合使用（流式场景下 `support_level=detailed` 将被静默降级为 `basic`）。
- `support_debug=true` 仅在 `X-DashScope-Env: dev` 请求头存在时生效，否则被忽略；该限制未在 [相关协议](../../raw/model-user-guide/support/related-agreements.md) 中明示，属运行时强制策略。
- 错误详情字段（如 `x-error-detail`）内容遵循 RFC 7807 格式，但实际返回为简化 JSON 字符串（非标准 JSON object），解析前需做字符串 `JSON.parse()` 容错处理。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


