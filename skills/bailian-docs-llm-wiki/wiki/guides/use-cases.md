# use cases

本页面汇总了阿里云百炼平台的核心应用场景与工程实践，涵盖多模态内容生成、检索增强系统构建、模型微调及高并发架构优化。开发者可通过标准化的 [[openai-compatible-api|OpenAI 兼容接口]]与提示词工程指南，快速将大模型能力集成至生产环境。下文按功能维度梳理关键参数配置、典型调用范式及部署限制。

## 支持的模型/功能
- **多模态生成与理解**：提供 [[文生文Prompt指南]]、文生图/图生图（参考 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-[[prompt|prompt]].md)）、文生视频/图生视频及文档转视频流水线。支持基础/进阶/多镜头提示词公式与声音合成控制。
- **企业级应用开发**：内置 [[RAG应用构建]] 方案，支持云端知识库索引、向量检索与查询引擎编排。提供显式缓存机制以降低高频重复调用的延迟与成本（详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practices.md)）。
- **模型定制与优化**：支持基于业务数据（≥500条 Prompt-Completion 对）的自定义模型微调、独占实例部署与自动化评测。集成限流应对策略，提供从排队等待到架构削峰的完整方案（参考 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)）。
- **第三方模型生态**：统一接入 DeepSeek、Kimi、GLM、MiniMax、MiMo（小米）及 Vidu 等模型。所有推理服务均通过 DashScope 网关代理，原生支持深度思考模式、长上下文与多模态输入。

## 关键参数
- **生成控制**：`[[prompt|prompt]]`（正向描述）、`negative_[[prompt|prompt]]`（反向排除）。万相 V2/视频模型支持 `prompt_extend`（默认 `true`），通过 LLM 智能改写提升画面一致性。
- **推理与思考模式**：`enable_thinking` 控制深度推理开关。开启后流式返回 `reasoning_content`（思维链）与 `content`（最终回复）。部分模型支持 `preserve_thinking` 用于多轮对话上下文传递。
- **性能与限流**：`X-DashScope-Wait-Timeout` 请求头定义服务端最大排队秒数（建议 3~120s）。客户端需同步调整 `timeout` 避免连接提前关闭。显式缓存通过在消息对象注入 `cache_control: {"type": "ephemeral"}` 标记可复用片段。

## 使用方式
- **提示词工程构建**：采用结构化公式提升可控性。例如文生视频进阶公式为 `主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化`。多镜头叙事需显式声明镜头序号与时间戳（如 `镜头1[0-3秒]`）。
- **标准化 API 调用**：统一 Base URL 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。Python 示例：
  ```python
  client.chat.completions.create(
      model="glm-5.1", messages=[...], extra_body={"enable_thinking": True}, stream=True
  )
  ```
  Node.js 需将非标准参数置于请求顶层。RAG 场景可通过 `DashScopeParse` 解析文档后调用 `DashScopeCloudIndex.from_documents()` 创建索引，并绑定 `DashScopeCloudRetriever`。
- **自定义模型迭代**：按“训练集/评测集分离”原则准备数据 → 平台自动调优 → 部署至专属实例 → 发起评测任务。评测不达标时可调整预置基座模型、扩充数据或修改超参数重试。
- **高可用架构设计**：结合流控策略实施限流管理。冷启动建议使用令牌桶控制初始速率；长文本并发采用双重令牌桶同步限制 RPM/TPM；非实时任务优先迁移至 Batch API。AI 编程工具（如 Claude Code）接入百炼 Anthropic 端点后默认自动注入缓存标记，无需额外代码修改。

> **注意**：不同 SDK 对非 OpenAI 标准参数的解析逻辑存在差异。Python SDK 必须将 `enable_thinking` 放入 `extra_body` 字典，而 Node.js SDK 需作为顶层属性传递。混用将导致参数被静默忽略或抛出 400 错误。
> **注意**：万相视频模型 `wan2.7` 已移除 `shot_type` 字段，多镜头与一镜到底的切换完全依赖提示词自然语言描述。
> **注意**：Kimi 系列模型的多模态输入仅支持公网 URL，不支持 Base64 编码数据直传。部分第三方供应商模型（如硅基流动 DeepSeek、月之暗面直供 Kimi）仅限“中国内地（北京）”地域 API Key 调用。

## 限制和注意事项
- **配额与限流维度**：平台按主账号与模型独立计算 RPM/TPM（分钟级）、RPS/TPS（瞬时）及 Traffic Burst（增速限流）。绝对配额超限无法通过 `X-DashScope-Wait-Timeout` 解决，需通过控制台提升临时额度或采购 PTU 预留算力。
- **缓存命中率优化**：开发工具默认在 System Prompt 注入时间戳与路径等动态信息，会破坏缓存边界。建议通过启动参数剥离动态字段，或使用分隔标记（如 `<!-- CACHE_BOUNDARY -->`）显式区分静态模板与动态内容。
- **计费与 Token 消耗**：启用 `prompt_extend`、流式思考模式及多模态解析均会产生额外 Token。首次写入显式缓存收取标准价格 25% 的开销，后续稳定命中可节省约 90% 成本；若需完全关闭，可通过环境变量 `DISABLE_PROMPT_CACHING=1` 或模型粒度开关配置。
- **环境依赖**：文档转视频等离线流水线依赖 FFmpeg、Marp 及 Chromium 渲染引擎。需确保运行环境网络可访问外部依赖源，并配置 Python 3.8~3.12 兼容的虚拟环境。文件解析器 `DashScopeParse` 要求单个文件 ≤100MB 且 ≤1000 页。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)
- [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)

