# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与技术实践路径，覆盖从基础 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建到多模态实时交互等关键方向。所有用例均基于平台已上线能力，开发者可直接参考对应教程快速集成。部分高级功能（如实时语音对话）依赖特定模型与接入协议，需严格遵循参数与调用约束。

## 支持的模型/功能

- **文本生成类**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通用大模型，适用于文生文、AI 解题、深度研究等场景；[文生文Prompt指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) 提供结构化提示词设计方法。  
- **多模态生成类**：`qwen3.5-omni-plus-realtime` 和 `qwen-audio-3.0-realtime-plus` 支持实时音视频流处理，用于构建数字人、语音对话等应用；相关实践见 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-omni-realtime) 和 [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](https://help.aliyun.com/zh/model-studio/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus)。  
- **语音与音频类**：`fun-asr-realtime`（实时语音识别）、`qwen-audio-3.0-tts-flash`（低延迟语音合成）需通过 AOQ 协议接入；[使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-using-aoq-access-fun-asr-realtime) 明确了 SDK 与事件回调要求。  
- **RAG 与知识增强**：推荐使用 `qwen-plus` 或 `qwen-turbo` 搭配 LlamaIndex 构建检索增强应用；[基于LlamaIndex构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-applications-based-on-llamaindex) 给出了完整链路示例。

## 关键参数

- 实时语音类场景（如 `qwen3.5-omni-plus-realtime`）必须设置 `stream=True` 且启用 `enable_audio=True`，否则音频流无法触发；该约束在 [通过AOQ使用qwen3.5-omni-plus-realtime实现按键语音对话](https://help.aliyun.com/zh/model-studio/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue) 中有明确说明。  
- RAG 应用中，`top_k`（检索结果数）建议设为 3–5，过高易引入噪声；`retrieval_threshold` 需根据 embedding 模型精度动态调整，详见 [基于LlamaIndex构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-applications-based-on-llamaindex)。  
- 所有三方模型调用（如非百炼托管模型）必须显式声明 `model_type="third_party"` 并传入 `provider` 字段；[三方模型调用教程](https://help.aliyun.com/zh/model-studio/third-party-model-integration-tutorial) 定义了认证与路由规则。

## 使用方式

1. **直接调用**：通过 `/v1/chat/completions` 接口传入 `model` 名称与 `messages`，适用于文生文、文生图等同步任务；[文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt) 强调 `size` 和 `quality` 参数对输出分辨率的影响。  
2. **流式+多模态**：对 `qwen3.5-omni-plus-realtime` 等模型，需使用 `/v1/realtime/chat/completions` 接口，并按 [通过WebRTC使用多模态交互套件实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-multimodal-dialog) 配置信令与媒体通道。  
3. **AOQ 接入**：语音识别、TTS、实时对话等必须通过 AOQ SDK 初始化 client，调用 `start_session()` 后发送二进制音频帧；[使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](https://help.aliyun.com/zh/model-studio/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash) 给出了帧格式与采样率要求（16kHz, PCM16）。  

## 限制和注意事项

- `qwen3.5-omni-plus-realtime` 当前仅支持 WebRTC 和 AOQ 两种接入方式，**不支持 HTTP 同步调用**；若尝试以普通 `/v1/chat/completions` 方式调用，将返回 `400 Bad Request` —— 此限制在 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-omni-realtime) 和 [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-aoq-omni-realtime) 中一致确认。  
- > **注意**：[借助大模型将文档转换为视频](https://help.aliyun.com/zh/model-studio/use-llm-to-convert-document-to-video) 文档中提及的 `qwen-vl-video` 模型尚未在公开 API 列表中开放，当前实际可用方案为 `qwen3.5-omni-plus-realtime` + 外部视频合成服务，开发者应以 [实践教程](../../raw/model-user-guide/use-cases.md) 中链接的最新官方文档为准。  
- 显式缓存（`cache_level=2`）仅对 `qwen-plus` 及以上模型生效，且需配合 `cache_key` 使用；[显式缓存最佳实践](https://help.aliyun.com/zh/model-studio/explicit-cache-guide) 指出未设置 `cache_key` 将导致缓存失效。  
- 限流策略按 `project_id` 维度统计，突发流量需结合 [限流应对最佳实践](https://help.aliyun.com/zh/model-studio/rate-limiting-best-practices) 中的令牌桶预热与重试退避机制处理。  

> **注意**：原始文档 [实践教程](../../raw/model-user-guide/use-cases.md) 中列出的多个外部链接（如 Hermes Agent、声音克隆等）属于解决方案层宣传页，其技术细节可能滞后于 API 文档；开发者应优先查阅对应功能的 [原文标题](../../raw/model-user-guide/use-cases.md) 所指向的官方帮助中心子页面，而非仅依赖链接标题判断能力边界。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


