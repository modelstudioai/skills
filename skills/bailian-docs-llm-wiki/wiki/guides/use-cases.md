# use cases

`use cases` 页面汇总了百炼平台支持的典型应用场景与对应技术实践，覆盖从基础生成任务到复杂智能体构建的全链路方案。开发者可根据业务需求，参考对应指南快速集成模型能力或优化系统性能。所有用例均基于平台当前稳定 API 与模型服务设计，部分历史资源需注意兼容性。

## 支持的模型/功能

百炼平台支持[多模态](../concepts/multi-modal.md)生成与推理场景，包括但不限于：
- 文生文（如 Qwen 系列大语言模型）、文生图（万相系列）、文生视频（万相3.0、通义万相视频生成）；
- 智能体框架（Hermes Agent）、数字人驱动、声音克隆、文档转视频等垂直解决方案；
- RAG 构建（支持 LlamaIndex 集成）、三方模型调用（如 vLLM、Ollama 自托管模型）及实时音视频流处理。

> **注意**：`[技术解决方案](raw/model-user-guide/use-cases/technical-solutions.md)` 中列举的部分行业方案（如金融问答机器人）依赖特定微调模型，而 `[历史模型指南](raw/model-user-guide/use-cases/legacy-resources.md)` 明确指出 Qwen1.5-7B 以下旧版模型已不推荐用于新项目——请优先选用 Qwen2/Qwen2.5 系列或万相3.0 等当前主力模型。

## 关键参数

不同用例对请求参数有差异化要求：
- 生成类任务（如文生图、文生视频）需严格遵循 `[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)` 和 `[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)` 中定义的 `prompt` 结构、`style`、`aspect_ratio`、`duration` 等字段；
- RAG 或 Agent 场景需关注 `top_k`、`retrieval_threshold`、`max_iterations` 等控制逻辑深度的参数，详见 `[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)`；
- 缓存与限流相关参数（如 `cache_key`、`rate_limit_group`）必须按 `[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)` 和 `[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)` 规范设置，否则可能被拒绝或降级。

## 使用方式

1. **直接调用**：通过 `/v1/chat/completions`（文本）、`/v1/images/generations`（图像）等标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)发起请求，传入对应模型名（如 `qwen2.5-72b-chat`、`wanx-v3.0`）；
2. **SDK 集成**：使用 `dashscope` Python SDK 时，可复用 `Generation.call()` 或 `MultiModalConversation.call()`，并传入预置用例模板（见 `[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)` 中的 template 示例）；
3. **低代码配置**：在百炼控制台「应用编排」中拖拽 Hermes Agent 组件，结合知识库与工具插件快速搭建智能体，具体流程参见 `[Hermes Agent，打造自进化智能体](../../raw/model-user-guide/use-cases.md)` 主文档。

## 限制和注意事项

- 所有视频生成类用例（含 `[视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)`）当前仅支持中国大陆地域（`cn-shanghai`）调用，跨域请求将返回 `403`；
- 声音克隆与数字人生成需提前完成声纹/形象授权备案，未备案账号调用 `[声音克隆：定制你的专属声线](../../raw/model-user-guide/use-cases.md)` 或 `[告别昂贵摄制，一图生成高清数字人](../../raw/model-user-guide/use-cases.md)` 相关接口将触发鉴权失败；
- `[三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)` 中描述的 BYOM（Bring Your Own Model）模式暂不支持 GPU 资源弹性伸缩，需手动预设 `gpu_count`，且仅限 `vLLM` 0.4.2+ 版本兼容。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


