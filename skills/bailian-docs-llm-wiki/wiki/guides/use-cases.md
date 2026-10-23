# use cases

百炼平台的 use cases 文档汇总了面向开发者的核心实践场景与工程化指南，覆盖从基础 Prompt 工程、多模态生成（文生图/文生视频/数字人）、RAG 构建到高并发、限流、缓存等生产级最佳实践。所有用例均基于真实 API 调用和 SDK 集成验证，适用于快速落地与规模化部署。具体实现细节请严格参照各子文档中的参数说明与代码示例。

## 支持的模型/功能

- **文本生成类**：支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL、Qwen-Audio 等原生模型，以及通过 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md) 接入的 Llama 3、Phi-3 等开源模型；
- **多模态生成类**：万相（WanX）系列支持文生图、文生视频（含 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)）、图像驱动数字人；语音方向支持 [声音克隆：定制你的专属声线](../../raw/model-user-guide/use-cases.md) 所述的个性化 TTS 声线训练与合成；
- **检索增强类**：提供 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 的端到端集成路径，兼容自定义向量库与重排序策略。

## 关键参数

- `model`：必填，需与实际部署的模型 ID 严格一致（如 `qwen-max`, `wanx-v1`），不支持别名或模糊匹配；
- `stream`：仅部分模型（如 `qwen-plus`, `qwen-turbo`）支持流式响应，万相系列暂不支持流式图像/视频输出；
- `seed`：对图像/视频生成任务建议显式设置以保障可复现性，详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)；
- `cache_level`：控制显式缓存行为，取值 `0`（禁用）、`1`（启用）、`2`（强一致性缓存），参见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 使用方式

- 所有 use case 均通过标准 REST API 或百炼 SDK（Python/Java）调用，无需额外服务部署；
- Prompt 工程类任务（如文生文、文生图）推荐优先使用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 和 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 中定义的结构化输入格式（如 `system`, `user`, `assistant` 角色分段，或 `prompt`, `negative_prompt`, `size` 等字段）；
- RAG、TTS 高并发、实时音视频等复杂场景，须按对应指南完成前置配置（如向量库初始化、音频 WebSocket 连接管理），不可直接复用通用 `/v1/chat/completions` 接口。

## 限制和注意事项

- 万相视频生成当前仅支持 `text-to-video` 接口，`/v1/videos/generations` 路径下不兼容旧版 `wanx-v1` 模型参数，[视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 中的部分字段（如 `frame_rate`）在万相3.0中已移除，应以 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 为准；
- > **注意**：[技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md) 中列举的“一图生成高清数字人”方案依赖私有化 Avatar SDK，其 API 签名与公有云 `/v1/avatars/generate` 接口不兼容，开发者需确认部署环境类型；
- 单次请求最大 token 数受模型限制（如 `qwen-max` 上限 8192，`wanx-v1` 图像生成上限 2048），超长文档转换需按 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md) 所述进行分块处理；
- 限流策略默认按 UID + model 维度统计，若需跨模型统一配额，必须参考 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 配置自定义 rate limit rule。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


