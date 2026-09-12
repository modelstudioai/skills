# release notes

本页面汇总百炼平台模型与功能的最新发布动态，包括新增模型、功能迭代、参数调整及已知限制。所有变更均面向 API 调用与 SDK 集成场景，开发者应结合具体模型文档验证兼容性。历史版本变更可追溯至 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)。

## 支持的模型/功能

- 新增 Qwen3（qwen3）和 Qwen2.5-VL（qwen2.5-vl）模型，支持长上下文（最高 128K tokens）与多模态输入；  
- 上线「流式响应增强模式」，通过 `stream_options.include_usage=true` 可在流式末尾返回 token 统计；  
- 模型上下架遵循统一生命周期策略，详情参见 [模型上下架与更新](../../raw/model-user-guide/release-notes.md)；  
- 已下线 Qwen1.5-0.5B 和 Qwen-VL-Chat，相关调用将返回 `404 Model Not Found`，迁移指引见 [模型下线机制说明](../../raw/model-user-guide/release-notes.md)。

## 关键参数

- `temperature`：取值范围 `[0.0, 2.0]`，默认 `0.8`；Qwen3 模型对 `temperature=0` 的确定性行为优化显著；  
- `top_p`：推荐值 `[0.5, 0.95]`，不建议设为 `1.0`（可能引发重复输出）；  
- `max_tokens`：最大输出长度受模型上下文窗口硬性约束，例如 qwen2.5-vl 最高支持 `8192` 输出 tokens；  
- `response_format`：仅 `qwen3` 和 `qwen2.5` 系列支持 `{"type": "json_object"}`，其他模型忽略该字段。

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `Authorization` header 中携带 Bearer [Token](../concepts/token.md)；  
- 启用流式响应时，设置 `stream=true`，并按 SSE 格式解析 `data:` 块；若需用量统计，务必同时传入 `stream_options: {"include_usage": true}`；  
- 多模态请求需将图像 base64 编码后置于 `messages[].content[].image_url.url` 字段（仅 `qwen2.5-vl` 及后续多模态模型支持）；  
- 所有模型列表与实时状态可通过 `GET /v1/models` 接口获取，该接口结果与 [模型平台功能更新](../../raw/model-user-guide/release-notes.md) 保持同步。

## 限制和注意事项

- 单次请求总 tokens（[prompt](prompt.md) + completion）不得超过模型上下文长度，超限将触发 `400 Bad Request`；  
- `qwen2.5-vl` 不支持 `system` 角色消息，若传入将被静默丢弃；  
- > **注意**：原始文档中 [模型上下架与更新](../../raw/model-user-guide/release-notes.md) 提到“Qwen2-VL 将于 2024-Q3 下线”，但 `/v1/models` 接口当前仍返回其状态为 `active` —— 请以接口实时响应为准，该文档信息已过时；  
- 免费试用额度不适用于新上线的 `qwen3` 模型，需开通按量付费；  
- 流式响应中 `usage` 字段仅在 `stream_options.include_usage=true` 且非空响应时返回，空响应或错误响应中不会包含。

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)


