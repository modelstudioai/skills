# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与技术实践路径，覆盖从基础 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建、AI 智能体开发，到多模态实时交互等完整链路。所有用例均基于已上线模型能力与 SDK/API 接口设计，适用于开发者快速验证和集成。实际部署前请务必参考对应文档中的参数约束与调用规范。

## 支持的模型/功能

当前用例覆盖以下核心能力方向：
- **文本生成类**：文生文、文生图、文生视频、图生视频（详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)、[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)、[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)）；
- **智能体与工作流**：Hermes Agent 自进化框架、AI 应用构建（含 LlamaIndex RAG）、作业批改等（参见 [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md) 和 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）；
- **多模态实时交互**：通过 WebRTC 或 AOQ 接入 `qwen3.5-omni-plus-realtime`、`qwen-audio-3.0-realtime-plus`、`fun-asr-realtime` 等实时模型，支持语音对话、TTS、ASR（如 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/best-practice-webrtc-omni-realtime.md)）；
- **音视频生成**：声音克隆、数字人生成、文档转视频（见 [声音克隆：定制你的专属声线](../../raw/model-user-guide/use-cases/voice-cloning.md) —— 注意该链接为外部页面，实际接入需以 [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md) 为准）。

> **注意**：原始文档中 `[声音克隆：定制你的专属声线](https://www.aliyun.com/solution/tech-solution/voice-cloning)` 和 `[告别昂贵摄制，一图生成高清数字人](https://www.aliyun.com/solution/tech-solution/avatar)` 均为外部营销页链接，**不包含 API 调用细节或参数说明**；开发者应优先采用 `raw/` 下对应 AOQ 或 WebRTC 集成文档，例如 [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)。

## 关键参数

各用例涉及的关键参数因模型类型而异，通用注意事项包括：
- 所有实时语音类用例（ASR/TTS/对话）必须显式指定 `model`（如 `qwen-audio-3.0-tts-flash`）、`sample_rate`、`audio_format` 及 `stream` 开关；
- 文生图/视频类需设置 `size`、`duration`、`frame_rate` 等输出控制参数，具体取值范围见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)；
- RAG 类用例依赖 `retrieval.top_k`、`rerank.model` 等检索参数，推荐结合 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 降低延迟；
- 所有调用均需遵守 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 中定义的 QPS 与并发限制。

## 使用方式

1. **本地验证**：使用 `dashscope` CLI 或 Python SDK 初始化 client，按用例文档构造 `messages` / `input` / `parameters` 字段；
2. **生产集成**：  
   - 实时类场景（如语音对话）建议通过 AOQ 或 WebRTC SDK 直连，避免 HTTP 长轮询开销；  
   - 批处理类（如文档转视频、深度研究）可结合 [自定义模型最佳实践](../../raw/model-user-guide/use-cases/model-training-best-practices.md) 进行 pipeline 编排；  
3. **调试辅助**：启用 `enable_debug` 参数（若支持）获取中间 token 流与推理 trace，参考 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 中的 debug 日志格式。

## 限制和注意事项

- **模型可用性**：`qwen3.5-omni-plus-realtime` 仅在 AOQ/WebRTC 通道开放，**不支持标准 `/v1/chat/completions` 接口**；其输入格式（如 `audio_chunk` 分片结构）与通用 chat 模型完全不同；
- **缓存策略**：显式缓存（`cache_key`）仅对 `text-generation` 类模型生效，多模态模型（如 `qwen-audio-*`）暂不支持，详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)；
- **跨域与合规**：所有音视频类用例需确保用户授权录音/播放权限，并符合《生成式人工智能服务管理暂行办法》关于声纹数据存储的要求；
- **外部链接失效风险**：原始文档中多个 `https://www.aliyun.com/...` 链接无版本控制且不提供 API 规范，**不可作为开发依据**，务必以 `../../raw/...` 路径下的技术文档为准。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


