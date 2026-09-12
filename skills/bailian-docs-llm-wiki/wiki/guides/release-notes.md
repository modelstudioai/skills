# release notes

本页面汇总百炼平台模型与功能的最新发布动态，包括新增模型、功能迭代、参数调整及已知限制。所有变更均面向 API 调用与 SDK 集成场景，开发者应结合具体模型文档验证兼容性。历史版本变更可追溯至 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)。

## 支持的模型/功能

- 新增 Qwen3（1024K 上下文）、Qwen2.5-VL [多模态](../concepts/multi-modal.md)推理支持；  
- 开放 `stream` 模式下 `tool_choice="auto"` 的动态工具调用能力；  
- 支持通过 `system` 消息字段注入全局指令（仅限 chat 接口），详见 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)。  
> **注意**：文档中提及的“Qwen2-VL 已全面替换为 Qwen2.5-VL”与 [模型上下架与更新](../../raw/model-user-guide/release-notes.md) 中“Qwen2-VL 仍维持维护期至 2024-12-31”存在时间线冲突，请以后者为准。

## 关键参数

- `top_p`：取值范围 `[0.0, 1.0]`，默认 `0.8`；设为 `0.0` 时等效于 greedy search；  
- `stop`：最多支持 4 个字符串，长度总和 ≤ 64 字符；  
- `max_tokens`：实际生成 token 数可能略超该值（因 tokenizer 边界对齐），详情参见 [模型下线机制说明](../../raw/model-user-guide/release-notes.md)。

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `Authorization` header 中携带 Bearer [Token](../concepts/token.md)；  
- 流式响应需设置 `stream=true`，并按 SSE 格式解析 `data:` 行；  
- 工具调用需在 `messages` 中显式传入 `tools` 数组，并确保 `tool_choice` 与服务端策略匹配（参考 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)）。

## 限制和注意事项

- 单次请求最大 `input_tokens + max_tokens ≤ 1024K`（Qwen3）或 `32K`（其余模型）；  
- `system` 消息不支持在非 chat 接口（如 `/v1/completions`）中使用；  
- 模型下线前 30 天将通过控制台公告及站内信通知，下线后 API 返回 `410 Gone`，具体策略见 [模型下线机制说明](../../raw/model-user-guide/release-notes.md)。

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)



