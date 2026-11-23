# API 兼容性升级

阿里云百炼 API 兼容性升级记录，持续更新请求参数、响应结构及接口行为调整。

为提升协议兼容性，阿里云百炼将持续升级 API 的请求参数、响应结构和接口行为。以下按公告更新日期记录升级内容。

## 2026 年 11 月 2 日

升级点

涉及 API

说明

`max_tokens` 行为调整，对齐 OpenAI 最新协议

[OpenAI Chat Completions API](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)、[DashScope API](raw/model-api-reference/qwen-api-reference/qwen-api-via-dashscope.md)

-   **升级前**：限制范围随模型及 `thinking_budget` 设置而异，可能仅包含最终回答，也可能包含思考与回答。
-   **升级后**：自 `qwen4-max-preview` / `qwen4-max` 起，Qwen 系列新模型的 `max_tokens` 等效于 `max_completion_tokens`，限制思考内容与最终回答的 Token 总量；`max_completion_tokens` 含义不变。开启思考时，思考内容占用同一输出预算。`qwen4-max-preview` 之前的存量模型行为不变。
