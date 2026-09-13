# release notes

本页面汇总百炼平台模型与功能的最新发布动态，包括新增模型、功能迭代、参数调整及已知限制。所有变更均面向 API 调用与 SDK 集成场景，开发者应结合具体模型文档验证兼容性。历史版本变更可追溯至 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)。

## 支持的模型/功能

- 新增 Qwen3（1024K 上下文）、Qwen2.5-VL [多模态](../concepts/multi-modal.md)推理支持；  
- 开放 `stream` 模式下 `tool_choice="auto"` 的动态工具调用能力；  
- 支持通过 `system` 消息字段注入全局指令（仅限 chat 接口），详见 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)。  
> **注意**：文档中提及的“Qwen2-VL 已全面替换为 Qwen2.5-VL”与 [模型上下架与更新](../../raw/model-user-guide/release-notes.md) 中“Qwen2-VL 仍维持维护期至 2024-12-31”存在时间线冲突，请以后者为准。

## 关键参数

- `top_p`：取值范围 `[0.0, 1.0]`，默认 `0.8`；设为 `0.0` 时等效于 greedy search；  
- `stop`：支持最多 4 个字符串，长度总和 ≤ 64 字符；  
- `response_format`：当前仅 `{"type": "text"}` 和 `{"type": "json_object"}` 受支持，`json_object` 模式需配合 `response_schema` 使用（参见 [模型平台功能更新](../../raw/model-user-guide/release-notes.md)）。

## 使用方式

- 通过 `/v1/chat/completions` 接口调用，需在 `Authorization` header 中携带 Bearer [Token](../concepts/token.md)；  
- 流式响应需设置 `stream=true`，并按 SSE 格式解析 `data:` 行；  
- [多模态](../concepts/multi-modal.md)输入须将图像 base64 编码后置于 `content` 数组的 `image_url` 字段，格式要求详见原始文档说明。

## 限制和注意事项

- 单次请求最大 token 数受模型本身限制（如 Qwen3 为 1,048,576），超出将返回 `400 Bad Request`；  
- `tool_choice="required"` 与 `response_format="json_object"` 不可同时使用，否则触发 `422 Unprocessable Entity`；  
- 模型下线前 30 天仅保留推理能力，不再接受新训练任务——具体机制请参考 [模型下线机制说明](../../raw/model-user-guide/release-notes.md)。

## 来源文档

- [产品动态](../../raw/model-user-guide/release-notes.md)


