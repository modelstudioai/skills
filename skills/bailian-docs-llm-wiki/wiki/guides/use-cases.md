# use cases

百炼平台的 use cases 文档汇总了面向开发者的核心实践场景与工程化指南，覆盖从基础 [Prompt 工程](../concepts/prompt-engineering.md)、多模态生成（文生图/文生视频/数字人）、RAG 构建到高并发、限流、缓存等生产级最佳实践。所有用例均基于真实 API 调用和 SDK 集成验证，适用于快速落地与规模化部署。内容持续更新，建议结合具体模型文档与 SDK 版本同步参考。

## 支持的模型/功能

当前 use cases 涵盖以下能力方向：
- **多模态生成**：万相系列（万相3.0视频生成、文生图）、语音克隆、数字人驱动；
- **大模型应用开发**：Hermes Agent 智能体构建、RAG（基于 LlamaIndex）、文档转视频；
- **工程优化**：限流应对、显式缓存、TTS 高并发、三方模型集成、实时音视频接入；
- **[Prompt 工程](../concepts/prompt-engineering.md)体系**：含文生文、文生图、文本生成视频等专用 Prompt 指南。

> **注意**：`万相3.0视频生成Prompt指南` 与 `视频生成Prompt指南` 内容存在重叠，且后者未标注适用模型版本；实际调用万相3.0时请优先参考 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)，避免因模型能力演进导致提示词失效。

## 关键参数

各用例涉及的关键参数需严格匹配对应模型要求：
- 文生图/视频类任务：`size`、`frame_rate`、`duration`、`negative_prompt` 等字段在不同模型中语义或默认值不同，须查阅具体模型文档；
- RAG 场景：`chunk_size`、`embedding_model`、`retriever_top_k` 需与 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 中的初始化配置一致；
- 缓存与限流：`cache_key` 格式、`rate_limit_quota` 单位（如 QPM/QPD）必须与 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 和 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 的定义对齐。

## 使用方式

- 所有指南均以代码片段 + 配置说明形式呈现，推荐通过 `dashscope` Python SDK 或 RESTful API 直接调用；
- Prompt 类用例（如 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）提供可复用模板，但需根据目标模型（Qwen-Max、Qwen-Plus 等）调整 system [prompt](prompt.md) 结构；
- RAG、Agent、数字人等复合场景，需组合多个 API 调用链路，建议使用百炼控制台「工作流」功能进行可视化编排与调试。

## 限制和注意事项

- 视频生成类服务（尤其是万相3.0）对输入文本长度、图像分辨率、时长有硬性上限，超出将触发 400 错误，详见 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)；
- 实时音视频接入依赖 WebRTC 协议栈，不支持纯服务端直连，需前端 SDK 配合，参考 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)；
- 三方模型调用（如 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）仅支持异步模式，且不享受百炼平台原生缓存与限流策略，务必阅读 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 中的鉴权与错误重试章节。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


