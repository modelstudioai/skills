# 流式输出

流式输出（Streaming Output）是指模型服务在生成响应过程中，将结果以增量方式分块、实时推送至客户端，而非等待全部内容生成完毕后一次性返回。这种方式显著降低端到端延迟，提升交互自然性，是构建低延迟对话、实时语音处理、代码补全等体验的关键能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **Test 1 基础文本生成服务**：通过 `stream=true` 参数启用流式响应，返回标准 SSE（`text/event-stream`）格式；适用于轻量级调试与简单聊天应用，仅支持 `qwen-max` 和 `qwen-plus` 模型。
  
- **Realtime API（实时文本接口）**：流式为强制模式（`stream` 必须为 `true`），专为高实时性场景设计；支持 SSE 与 WebSocket 双协议，提供细粒度事件（如 `message`、`done`、`error`），并支持多轮上下文保持与中断恢复。

- **Omni Realtime API（[多模态](multi-modal.md)实时接口）**：采用事件驱动的双向流式通信（WebSocket），实现 ASR 输入流与 TTS/文本输出流的端到端协同；全程延迟控制在 300ms 内，适用于虚拟人、会议助手等强实时交互场景。

- **Qwen 系列 [OpenAI 兼容接口](openai-compatibility.md)**：兼容 `stream=true` 参数，返回符合 OpenAI 标准的 SSE 格式（含 `choices[0].delta.content` 字段）；但需注意：DashScope 原生接口与 [OpenAI 兼容接口](openai-compatibility.md)的流式响应结构不同（前者用 `output.text` 增量更新），客户端解析逻辑不可复用。

- **Audio API（音频处理接口）**：ASR（语音识别）和 Voice Chat（语音对话）支持 `stream=true` 查询参数，返回渐进式转写结果或中间响应；TTS 和音乐生成暂不支持流式输出。

## 关键参数和配置

| 参数 | 所属接口 | 类型 | 说明 |
|------|----------|------|------|
| `stream` | Test 1、Realtime API、Qwen（OpenAI/DashScope）、Audio（ASR/Chat） | boolean | **必须显式设置为 `true`** 才启用流式；Realtime API 中设为 `false` 将直接返回 400 错误 |
| `Accept: text/event-stream` | Test 1、Realtime API、Qwen（OpenAI 兼容）、Audio（ASR/Chat） | HTTP Header | 请求头中必需，告知服务端返回 SSE 格式 |
| `Connection: upgrade` + `Upgrade: websocket` | Realtime API、Omni Realtime API | HTTP Header | 启用 WebSocket 协议时必需 |
| `enable_intermediate_results` | Omni Realtime API | boolean | 控制是否推送 ASR 中间结果（如实时字幕），默认 `false` |

> ⚠️ 注意事项：
> - 流式响应中 `delta.content` 或 `output.text` 可能为空字符串（模型思考中或生成非文本内容），客户端需做空值容错；
> - 所有流式接口均需正确解析 `event:` 字段区分消息类型（如 `message`、`error`、`done`），不可仅依赖 `data:` 解析；
> - WebSocket 连接有超时限制（Realtime API：15 分钟；Omni：5 分钟），客户端须实现带指数退避的自动重连逻辑。

## 面向开发者，简洁实用

- ✅ **首选 SDK**：使用最新版 `dashscope` Python SDK（v1.20.0+），它自动适配各接口的流式协议差异，并内置 SSE 解析器与重连机制。
- ✅ **调试建议**：本地测试时可用 `curl -N` 或浏览器 DevTools 的 Network → EventStream 查看原始 SSE 流；生产环境务必监听 `done` 事件确认响应结束。
- ✅ **错误防御**：始终检查 `event` 字段，对 `error` 事件做降级处理（如 fallback 到非流式请求）；对 `done` 事件校验 `usage` 字段确保计费与 token 统计准确。
- ❌ **避免踩坑**：不要混用 DashScope 原生与 [OpenAI 兼容接口](openai-compatibility.md)的流式解析逻辑；不要忽略 `max_tokens` 硬上限（Realtime API 为 4096），否则可能被静默截断。

## 关联主题页

- [test 1](../guides/test-1.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [omni realtime api](../api/omni-realtime-api.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [audio api references](../api/audio-api-references.md)


