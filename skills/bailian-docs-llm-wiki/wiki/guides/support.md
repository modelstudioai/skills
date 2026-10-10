# support

`support` 是百炼平台为模型调用和服务使用提供的基础支持能力，涵盖模型兼容性、服务范围、售后保障及合规协议等内容。开发者可通过该模块确认所选模型是否受支持、了解服务边界与限制，并获取故障排查和问题反馈路径。所有支持策略均以 [服务支持](../../raw/model-user-guide/support.md) 为准。

## 支持的模型/功能

- 当前支持的模型列表详见 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md)，包括通义千问系列（Qwen1、Qwen2、Qwen3）、Qwen-VL、Qwen-Audio 等开源与闭源模型，以及部分第三方微调模型。
- 功能支持覆盖同步推理（`/v1/chat/completions`）、异步任务（`/v1/async-tasks`）、批量处理（`/v1/batch`）及模型微调结果部署后的在线服务调用。
- 模型能力边界（如上下文长度、输入格式、多模态支持）需以各模型专属文档及 [服务支持](../../raw/model-user-guide/support.md) 中的说明为准。

## 关键参数

- `model`：必需，值必须在 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 公布的有效模型 ID 范围内，大小写敏感，非法值将返回 `400 Bad Request`。
- `enable_search` / `enable_retrieval`：仅对明确标注“支持检索增强”的模型生效（见 [服务支持](../../raw/model-user-guide/support.md) 的附录说明），默认关闭。
- `stream`：流式响应仅在模型原生支持且服务端已启用时可用；若模型不支持但强制设为 `true`，将静默降级为非流式并返回警告头 `X-Warning: stream-not-supported`。

## 使用方式

- 所有支持模型均可通过标准 OpenAI 兼容 API（`POST /v1/chat/completions`）调用，无需额外开通权限，但需确保账号已开通百炼服务并完成实名认证。
- 售后问题须通过控制台「工单系统」提交，选择对应模型与问题类型，并附上请求 ID（`X-Request-ID`）及完整错误响应体；参考 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 明确可受理范围。
- 协议约束（如数据隐私、商用许可、输出内容责任）请严格遵循 [相关协议](../../raw/model-user-guide/support/related-agreements.md)，尤其注意免费试用模型与按量付费模型的条款差异。

## 限制和注意事项

- 单次请求最大输入 token 数受模型本身限制（如 Qwen3-32B 最高支持 32768），超出将被截断并返回 `400` 错误；具体数值请查阅 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 中对应模型的“Max Context Length”字段。
- 异步任务最长保留结果 7 天，超期自动清理；此策略与 [售后说明](../../raw/model-user-guide/support/after-sales-service-scope.md) 中“历史记录查询时效”一致，但不适用于调试日志留存。
> **注意**：原始文档中 [服务支持](../../raw/model-user-guide/support.md) 提到“所有模型默认支持 JSON Schema 输出”，但最新 [模型列表](../../raw/model-user-guide/support/model-studio-model-list.md) 显示仅 Qwen3-72B-Instruct 及以上版本明确标注支持 `response_format: { "type": "json_object" }`，其余模型实际调用将忽略该参数。请以模型列表为准。

## 来源文档

- [服务支持](../../raw/model-user-guide/support.md)


