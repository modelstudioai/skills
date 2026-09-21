# use cases

百炼平台的 use cases 文档汇总了面向开发者的核心应用场景与工程实践，覆盖从基础 Prompt 工程、多模态生成（文生图/文生视频/数字人）到高级架构模式（RAG、智能体、缓存与限流）等完整链路。所有用例均基于真实客户落地经验提炼，强调可复现性与生产就绪性。开发者应结合具体模型能力与业务约束选择适配方案。

## 支持的模型/功能

当前 use cases 覆盖以下能力维度：
- **文本生成类**：通用大语言模型（Qwen 系列）、代码模型（Qwen-Coder）、推理优化模型（Qwen2.5-Max）；
- **多模态生成类**：文生图（Qwen-VL、通义万相）、文生视频/图生视频（Tongyi Tingwu + Tongyi Yingxiang）、声音克隆（Tongyi Tingwu）；
- **智能体与应用框架**：Hermes Agent 框架、LlamaIndex 集成、三方模型桥接（如 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）；
- **基础设施增强**：显式缓存、实时音视频流接入、文档转视频流水线。

> **注意**：`[Hermes Agent，打造自进化智能体](../../raw/model-user-guide/use-cases.md)` 中描述的 Hermes Agent 当前仅支持 Qwen2.5-Max 及以上版本，旧版 Qwen1.5 不兼容该框架——此限制未在 [自定义模型最佳实践](../../raw/model-user-guide/use-cases/model-training-best-practices.md) 中明确说明，需以本页为准。

## 关键参数

不同用例对请求参数有差异化要求：
- **Prompt 类用例**（如 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)）：强依赖 `system_prompt`、`temperature`（建议 0.3–0.7）、`max_tokens`（需预留 20% 余量用于工具调用）；
- **多模态生成类**（如 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)）：必须指定 `size`（如 `"1024x1024"`）、`style`（`"realistic"` / `"anime"`），且 `prompt` 长度上限为 512 字符；
- **RAG 与缓存类**（如 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)）：需设置 `cache_level=2` 并传入 `cache_key`，否则不触发缓存命中。

## 使用方式

1. **直接调用**：通过 `/v1/chat/completions` 或 `/v1/images/generations` 等标准 API 接口，按对应用例的参数规范构造请求；
2. **集成 SDK**：使用 `dashscope` Python SDK 的 `Generation.call()` 或 `MultiModalConversation.call()` 方法，自动处理多模态 payload 序列化；
3. **低代码编排**：在百炼控制台「工作流」中拖拽组件，例如将 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 封装为可复用节点；
4. **端侧部署**：部分用例（如声音克隆）支持导出 ONNX 模型至边缘设备，详见 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)。

## 限制和注意事项

- 所有生成类用例默认启用内容安全过滤，敏感词拦截不可关闭；若需白名单豁免，须提交工单申请审核；
- `[借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)` 要求输入文档为 PDF/TXT/DOCX，且单次处理不超过 50 页或 10MB，超限需分片预处理；
- 三方模型调用（见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)）不享受百炼平台级限流保护，需自行实现熔断与重试；
- 显式缓存仅对完全相同的 `model` + `input` + `parameters` 组合生效，`top_p` 与 `temperature` 的微小浮点差异（如 `0.5` vs `0.5000001`）会导致缓存未命中。

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


