# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与技术实践路径，覆盖从基础 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 构建到多模态实时交互等关键方向。所有用例均基于平台已上线能力，开发者可直接参考对应教程快速集成。部分高级功能（如实时语音对话）依赖特定模型与接入协议，需严格遵循参数与调用约束。

## 支持的模型/功能

- **文本生成类**：支持 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通用大模型，适用于文生文、AI 解题、深度研究等场景；[文生文Prompt指南](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide) 提供结构化提示词设计方法。
- **多模态生成类**：包括 `qwen3.5-omni-plus-realtime`（实时音视频理解与生成）、`qwen-audio-3.0-realtime-plus`（实时语音对话）、`qwen-audio-3.0-tts-flash`（低延迟 TTS）及 `fun-asr-realtime`（实时语音识别），详见 [通过AOQ使用qwen-audio-3.0-realtime-plus实现实时语音对话](https://help.aliyun.com/zh/model-studio/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus)。
- **RAG 与文档处理**：支持基于 LlamaIndex 的 RAG 应用构建，以及将 PDF/PPT/Word 等文档自动转换为视频的端到端流程，具体见 [基于LlamaIndex构建RAG应用](https://help.aliyun.com/zh/model-studio/build-rag-applications-based-on-llamaindex) 和 [借助大模型将文档转换为视频](https://help.aliyun.com/zh/model-studio/use-llm-to-convert-document-to-video)。
- **三方模型集成**：可通过 API 接入非百炼托管模型，但需自行管理鉴权、限流与错误重试逻辑，参考 [三方模型调用教程](https://help.aliyun.com/zh/model-studio/third-party-model-integration-tutorial)。

## 关键参数

- 实时语音类模型（如 `qwen3.5-omni-plus-realtime`）必须通过 AOQ 或 WebRTC 协议调用，不支持 HTTP 同步接口；采样率、音频格式、chunk 大小等参数需与服务端严格对齐，否则触发静音或中断。
- RAG 场景中，`retrieval_top_k` 默认为 3，建议根据知识库密度调整至 2–5；向量检索前需确保文档已通过 [自定义模型最佳实践](https://help.aliyun.com/zh/model-studio/model-training-best-practices) 中推荐的分块策略预处理。
- 所有生成类请求应显式设置 `stream: true`（流式）或 `stream: false`（非流式），未指定时行为因模型而异；流式响应需按 SSE 格式解析，详见 [显式缓存最佳实践](https://help.aliyun.com/zh/model-studio/explicit-cache-guide) 中的响应结构说明。

## 使用方式

1. **快速启动**：从 [高效搭建 AI 智能体与工作流应用](https://help.aliyun.com/zh/model-studio/build-ai-applications-based-on-alibaba-cloud-model-studio) 入手，使用百炼控制台可视化编排 Agent 流程。
2. **代码集成**：
   - 文本类：调用 `/v1/chat/completions`，传入 `model`、`messages`、`temperature` 等标准参数；
   - 实时音视频类：必须使用 AOQ SDK 或 WebRTC 客户端，参考 [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](https://help.aliyun.com/zh/model-studio/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue)；
   - RAG 类：结合 `retriever` + `llm` 双组件，初始化时加载已向量化知识库。
3. **[Prompt 工程](../concepts/prompt-engineering.md)**：文生图、文生视频需严格遵循 [文生图Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-image-prompt) 和 [文生视频/图生视频Prompt指南](https://help.aliyun.com/zh/model-studio/text-to-video-prompt) 中的语法与权重标记规范，否则生成质量显著下降。

## 限制和注意事项

- **并发与限流**：免费版账户默认 QPS=1，超出后返回 `429`；生产环境务必按 [限流应对最佳实践](https://help.aliyun.com/zh/model-studio/rate-limiting-best-practices) 配置指数退避与队列缓冲。
- > **注意**：原始文档中 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-webrtc-omni-realtime) 与 [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](https://help.aliyun.com/zh/model-studio/best-practice-aoq-omni-realtime) 描述的信令流程存在差异——前者要求客户端主动维护 ICE 连接，后者由 AOQ 代理完成。推荐优先采用 AOQ 方案，因其兼容性更广、错误恢复机制更完善。
- **缓存一致性**：启用显式缓存（`cache_level=2`）时，若输入 `messages` 中含时间敏感内容（如 `{{current_time}}`），需手动禁用缓存或添加随机 salt，否则可能返回过期结果；详情见 [显式缓存最佳实践](https://help.aliyun.com/zh/model-studio/explicit-cache-guide)。
- **模型兼容性**：`qwen-audio-3.0-tts-flash` 仅支持 `text` 输入，不接受 SSML；而 `qwen-audio-3.0-realtime-plus` 要求输入为 PCM 流，二者不可混用。所有音频模型均不支持跨区域调用（如华东1调用华北2部署的实例）。

> **注意**：原始文档 [实践教程](../../raw/model-user-guide/use-cases.md) 中列出的多个外部链接（如 Hermes Agent、声音克隆等）指向解决方案页，其底层技术栈可能随版本迭代变更。实际开发请以 [原文标题](../../raw/model-user-guide/use-cases.md) 中所附官方帮助中心链接为准，并定期核对 [三方模型调用教程](../../raw/model-user-guide/use-cases.md) 中的兼容性矩阵更新。

> **注意**：[原文标题](../../raw/model-user-guide/use-cases.md) 中“告别昂贵摄制，一图生成高清数字人”案例当前依赖 `wanx-avatar` 专属模型，该模型未开放通用 API，仅限控制台内使用；开发者如需程序化调用，请改用 `qwen-vl-plus` + 自定义渲染 pipeline，参考 [原文标题](../../raw/model-user-guide/use-cases.md) 中“一图生成高清数字人”的替代实现路径。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


