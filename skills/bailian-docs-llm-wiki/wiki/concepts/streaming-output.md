# 流式输出

流式输出（Streaming Output）是百炼平台提供的一种实时响应机制，允许模型在生成过程中将结果以增量方式分块返回，而非等待全部内容完成后再一次性返回。它显著降低端到端延迟，提升用户交互体验，并支持前端实时渲染、语音合成驱动、中断控制等高级交互能力。

## 在百炼平台的不同场景中如何使用

流式输出在百炼平台覆盖多种协议与模型类型，具体使用方式因接口形态而异：

- **[OpenAI 兼容接口](openai-compatible-api.md)**（`/v1/chat/completions`）：通过请求体中设置 `"stream": true` 启用；响应为 Server-Sent Events（SSE）格式，每块数据含 `delta.content` 字段，需按顺序拼接还原完整文本。
- **DashScope 原生接口**：同样支持 `stream=true`，但返回结构更细粒度，包含 `output.text`（增量文本）、`usage`（实时 token 统计，需配合 `stream_options.include_usage=true`）、以及 `finish_reason` 等调试字段。
- **Realtime API（WebSocket / HTTP/2）**：强制要求 `stream=true`，采用事件驱动模型（如 `content_block_delta`、`message_stop`），支持多模态流（`output.audio.delta`、`output.image`）、工具调用流式反馈及 `interrupt` 实时中断。
- **Omni Realtime API（全链路多模态）**：基于 WebSocket 双向流，天然支持语音识别（ASR）、大模型推理（LLM）、语音合成（TTS）的端到端流式协同；客户端可独立启用/禁用 ASR 或 TTS，并接收 `output.text.delta` 与 `output.audio.delta` 等混合事件。
- **Qwen3 / Qwen2.5 系列模型**：除基础流式外，支持增强模式——通过 `stream_options: {"include_usage": true}` 在流结束前的最后一帧中返回精确的 `prompt_tokens` 和 `completion_tokens`，便于精准计费与性能分析。

> ✅ 提示：所有流式接口均**不支持同步阻塞式调用**；若传入 `stream=false`（或未指定），将回退至传统单次响应模式，无法获得流式能力。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `stream` | boolean | 是（Realtime API 强制为 `true`） | 启用流式响应；设为 `false` 将导致部分接口（如 Realtime API）直接报错 `400` |
| `stream_options.include_usage` | boolean | 否 | 仅 DashScope 原生与新版 [OpenAI 兼容接口](openai-compatible-api.md)支持；设为 `true` 时，流末尾最后一帧将携带 `usage` 对象（含 `prompt_tokens`、`completion_tokens`） |
| `max_tokens` / `max_output_tokens` | integer | 否 | 控制流式生成的最大长度；超出后自动截断并触发 `finish_reason="length"`；注意不同接口命名略有差异（如 Omni 接口用 `max_output_tokens`） |
| `temperature` | float | 否 | 影响流式输出稳定性：值越低（如 `0.0`），逐 token 一致性越高，适合确定性任务；过高可能导致早期 token 波动加剧 |

⚠️ 注意事项：
- 流式响应中**错误不会混入数据流**：所有异常（如鉴权失败、模型不可用）均通过独立的 `error` 事件或 HTTP 错误码（如 `400`/`429`）返回，不应尝试从 `delta` 中解析错误信息；
- 客户端必须正确处理 SSE 分块（按 `data:` 行解析）、WebSocket 二进制帧或 HTTP/2 数据帧，建议优先使用官方 SDK（如 AOQ SDK、DashScope Python SDK）以规避底层协议细节风险；
- 流式连接有超时限制：Realtime API 单连接最长 30 分钟，Omni Realtime 单会话最长 300 秒，超时需主动重连并重建上下文。

## 面向开发者：快速上手建议

- ✅ **首选 SDK**：避免手动解析 SSE 或 WebSocket；使用 [DashScope Python SDK](https://help.aliyun.com/zh/model-studio/developer-reference/install-and-use-the-dashscope-sdk) 或 [AOQ 客户端 SDK](https://help.aliyun.com/zh/model-studio/developer-reference/use-the-aoq-client-sdk) 可自动处理重连、事件分发、`delta` 拼接与 `usage` 提取；
- ✅ **必加容错**：监听 `error` 事件 + HTTP 状态码，不要依赖流式数据完整性判断成功；
- ✅ **合理设限**：始终设置 `max_tokens` 防止无限生成；对语音类应用，建议结合 `temperature=0.3~0.6` 平衡流畅性与可控性；
- ✅ **调试技巧**：开启 `stream_options.include_usage=true` + 日志打印每帧 `delta` 内容，可快速定位卡顿、重复、截断等问题；
- ❌ **避免踩坑**：不要在流式响应未结束前关闭连接；不要假设 `delta.content` 永远非空（空字符串合法）；不要忽略 `finish_reason` 字段（`stop`/`length`/`tool_calls`/`error` 含义不同）。

## 关联主题页

- [test 1](../guides/test-1.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [release notes](../guides/release-notes.md)


