# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与技术实践路径，覆盖从基础 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建到[多模态](../concepts/multi-modal.md)实时交互等关键方向。所有用例均基于平台已上线能力，开发者可直接参考对应教程快速集成。部分高级功能（如实时语音对话）依赖特定模型与接入协议，需严格遵循参数与调用约束。

## 支持的模型/功能

- **文本生成类**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通用大模型，适用于文生文、AI 解题、深度研究等场景；[文生文Prompt指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) 提供结构化提示词设计方法。
- **[多模态](../concepts/multi-modal.md)生成类**：包括 `qwen3.5-omni-plus-realtime`（实时音视频理解与生成）、`qwen-audio-3.0-realtime-plus`（实时语音对话）、`qwen-audio-3.0-tts-flash`（低延迟 TTS）及 `fun-asr-realtime`（实时语音识别），详见 [通过AOQ使用qwen-audio-3.0-realtime-plus实现实时语音对话](https://help.aliyun.com/zh/model-studio/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus)。
- **RAG 与文档处理**：支持基于 LlamaIndex 的 RAG 应用构建，以及将 PDF/PPT/Word 等文档自动转换为视频的端到端流程，具体见 [基于LlamaIndex构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-applications-based-on-llamaindex) 和 [借助大模型将文档转换为视频](https://help.aliyun.com/zh/model-studio/use-llm-to-convert-document-to-video)。
- **三方模型集成**：可通过 API 接入非百炼托管模型，但需自行管理鉴权、限流与错误重试逻辑，参考 [三方模型调用教程](https://help.aliyun.com/zh/model-studio/third-party-model-integration-tutorial)。

## 关键参数

- 实时语音类模型（如 `qwen3.5-omni-plus-realtime`）必须通过 AOQ 或 WebRTC 协议调用，不支持 HTTP 同步接口；采样率、音频格式、chunk 大小等参数需与服务端严格对齐，否则触发静音或中断。
- RAG 场景中，`retrieval_top_k` 默认为 3，建议根据知识库密度调整至 1–5；向量检索前需确保文档已通过 [自定义模型最佳实践](https://help.aliyun.com/zh/model-studio/model-training-best-practices) 中推荐的分块策略预处理。
- 所有流式响应接口（含 `text/event-stream` 和 WebRTC data channel）要求客户端维持长连接，超时阈值由服务端统一设为 60 秒，不可覆盖。

## 使用方式

1. **快速启动**：从 [高效搭建 AI 智能体与工作流应用](https://help.aliyun.com/zh/model-studio/build-ai-applications-based-on-alibaba-cloud-model-studio) 入手，使用百炼控制台可视化编排智能体节点。
2. **代码集成**：
   - 文本类：调用 `/v1/chat/completions`，指定 `model` 参数（如 `qwen-plus`），启用 `stream=true` 获取 SSE 流。
   - 实时音视频：必须使用 AOQ SDK 或 WebRTC 客户端，参考 [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](https://help.aliyun.com/zh/model-studio/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue)。
   - RAG：结合 `llamaindex` Python SDK 与百炼向量库 endpoint，初始化 `VectorStoreIndex` 时传入 `api_key` 和 `base_url`。
3. **Prompt 调优**：文生图/文生视频任务需严格遵循 [文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt) 和 [文生视频/图生视频Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-video-prompt) 中的语法规范（如 negative [prompt](prompt.md) 格式、分辨率关键词），否则生成质量显著下降。

## 限制和注意事项

- **模型可用性**：`qwen3.5-omni-plus-realtime` 当前仅在华东1（杭州）地域开放，其他地域调用将返回 `404 Not Found`；该限制未在 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-omni-realtime) 中明确说明，> **注意**：请以控制台地域列表为准，避免跨域调用失败。
- **缓存行为**：显式缓存（`cache_level=2`）仅对 `qwen-turbo` 和 `qwen-plus` 生效，对 `qwen-max` 及所有 omni 系列模型无效；相关配置需在请求 header 中设置 `X-Bailian-Cache-Level: 2`，详见 [显式缓存最佳实践](https://help.aliyun.com/zh/model-studio/explicit-cache-guide)。
- **限流策略**：默认 QPS 为 5，突发流量需配合 [限流应对最佳实践](https://help.aliyun.com/zh/model-studio/rate-limiting-best-practices) 中的令牌桶+重试退避方案，避免 `429 Too Many Requests`。
- **三方模型兼容性**：调用非百炼模型时，`system` 字段可能被忽略，且不支持 `tool_choice` 等高级参数；务必在 [三方模型调用教程](https://help.aliyun.com/zh/model-studio/third-party-model-integration-tutorial) 中验证接口契约一致性。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


