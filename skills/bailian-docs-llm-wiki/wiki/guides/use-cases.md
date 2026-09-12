# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与技术实践路径，覆盖从基础 Prompt 工程、RAG 构建到多模态实时交互等关键方向。所有用例均基于已上线能力验证，开发者可直接参考对应教程快速集成。部分高级功能（如实时语音对话）依赖特定模型与接入协议，需严格遵循参数约束与调用规范。

## 支持的模型/功能

- **文本生成类**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通用大模型，适用于文生文、AI 解题、深度研究等场景；[文生文Prompt指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) 提供结构化提示词设计方法。
- **多模态生成类**：`qwen3.5-omni-plus-realtime`、`qwen-audio-3.0-realtime-plus`、`qwen-audio-3.0-tts-flash`、`fun-asr-realtime` 等模型分别支撑实时音视频对话、TTS 与 ASR 能力；相关实践见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-omni-realtime) 和 [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash)。
- **RAG 与工具链**：支持基于 LlamaIndex 的 RAG 应用构建，也兼容自定义模型微调流程；[基于LlamaIndex构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-applications-based-on-llamaindex) 和 [自定义模型最佳实践](https://help.aliyun.com/zh/model-studio/model-training-best-practices) 提供端到端参考。

## 关键参数

- 实时语音/视频类用例必须启用 `stream=true` 并配合 `enable_search=false`（若非检索增强场景），否则可能触发非预期缓存或超时；具体参数组合请严格参照 [通过AOQ使用qwen3.5-omni-plus-realtime实现按键语音对话](https://help.aliyun.com/zh/model-studio/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue) 中的请求体示例。
- 显式缓存需显式传入 `cache_level=2` 且 `cache_key` 符合业务语义唯一性要求；[显式缓存最佳实践](https://help.aliyun.com/zh/model-studio/explicit-cache-guide) 明确禁止在实时对话流中复用同一 `cache_key`。
- 三方模型调用须配置 `provider` 字段（如 `"provider": "openai"`），并确保 endpoint 与认证方式与 [三方模型调用教程](https://help.aliyun.com/zh/model-studio/third-party-model-integration-tutorial) 一致。

## 使用方式

1. 选择匹配场景的模型（参见 [实践教程](../../raw/model-user-guide/use-cases.md) 中的链接列表）；
2. 按对应文档配置请求参数（如 `input` 结构、`parameters` 字段、`stream` 开关）；
3. 对于 WebRTC 或 AOQ 接入，需额外部署信令服务与媒体代理，不可直连模型 API；详细步骤见 [通过WebRTC使用多模态交互套件实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-multimodal-dialog)；
4. 生产环境务必集成限流应对逻辑，推荐采用令牌桶 + 重试退避策略；[限流应对最佳实践](https://help.aliyun.com/zh/model-studio/rate-limiting-best-practices) 给出 SDK 层封装建议。

## 限制和注意事项

- `qwen3.5-omni-plus-realtime` 仅支持通过 AOQ 或 WebRTC 协议接入，**不支持 HTTP 同步调用**；尝试直接 POST 到 `/v1/chat/completions` 将返回 `400 Unsupported model` 错误。> **注意**：该限制与部分旧版文档中“通用模型统一 API 入口”的描述存在冲突，请以 [通过AOQ使用qwen3.5-omni-plus-realtime实现按键语音对话](../../raw/model-user-guide/use-cases.md) 为准。
- 文生图/文生视频 Prompt 指南中推荐的 negative [prompt](prompt.md) 语法（如 `--no text, watermark`）**仅对 `wanx-v1` 及后续图像模型生效**，对 `qwen-vl` 等多模态理解模型无效；详见 [文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt)。
- 所有实时语音类用例（ASR/TTS/双工对话）要求客户端网络延迟 ≤ 200ms，且音频采样率必须为 16kHz、单声道、PCM 编码；不符合条件将导致静音或识别失败。该要求未在 [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-using-aoq-access-fun-asr-realtime) 中明确强调，但已在 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases.md) 的“环境准备”章节注明。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


