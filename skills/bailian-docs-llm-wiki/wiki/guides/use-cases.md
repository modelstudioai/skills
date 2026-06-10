# use cases

阿里云百炼平台提供丰富的使用场景，涵盖 Prompt 工程、第三方模型接入、RAG 应用构建、自定义模型调优、API 流控优化等方面。本页汇总各场景的核心要点与实践指引，帮助开发者快速定位所需能力并投入生产。

## Prompt 工程指南

百炼平台围绕文生文、文生图、文生视频三大模态提供了系统化的 Prompt 编写方法论。

### 文生文 Prompt

[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)推荐使用 **Prompt 框架**（背景、目的、风格、语气、受众、输出）来规范化提示词结构，显著提升大语言模型的输出质量。核心技巧包括：

- **构建清晰明确的 Prompt**：任务描述越具体，模型表现越符合预期。
- **少样本提示（Few-shot）**：在 Prompt 中提供示例，引导模型按期望格式输出。
- **分步推理（Chain-of-Thought）**：对复杂任务，引导模型逐步思考而非直接给出答案。

百炼控制台还提供 Prompt 一键优化工具，可自动扩写和改进提示词。

### 文生图 Prompt

[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)适用于万相文生图 V1/V2 模型，提供两层公式：

- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

关键参数包括 `prompt`（正向提示词）、`negative_prompt`（反向提示词）和 `prompt_extend`（V2 智能改写开关，默认开启）。提示词词典涵盖景别、视角、拍摄类型、风格和光线五大维度。

### 文生视频与图生视频 Prompt

[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)针对万相系列视频模型，提供多层级公式：

- **基础公式**：主体 + 场景 + 运动
- **进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频公式**：运动 + 运镜（图像已确定主体和风格）
- **声音公式**（wan2.7/wan2.6/wan2.5）：增加人声/音效/背景音乐描述
- **多镜头公式**（wan2.7/wan2.6）：总体描述 + 镜头序号 + 时间戳 + 分镜内容
- **参考生视频公式**（wan2.7/wan2.6）：支持通过"图n"/"视频n"指代参考素材，实现主体一致性

> **注意**：wan2.7 不再支持 `shot_type` 参数指定单镜头/多镜头，改为由模型结合提示词自行判断。如需强制单镜头，中文写"生成单镜头"，英文写"Generate single shot."

### Vidu 视频生成 Prompt

[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)提供初阶与进阶教程。提示词公式为"主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介"。Vidu 支持通过特定关键词触发运镜控制（推/拉/左移/右移/固定等）、动态幅度控制（大动态/中动态/小动态）、特效（爆炸/旋涡/融化/石化等）和画面风格（2D动漫/3D渲染/水墨/像素等）。参考生视频功能可保持多视角下的主体一致性。

## 第三方模型接入

百炼平台提供统一的 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)和 DashScope SDK，开发者可用同一个 API Key 调用多家第三方模型。所有模型均通过 `https://dashscope.aliyuncs.com/compatible-mode/v1` 接入。

### DeepSeek 系列

百炼提供三个供应商的 DeepSeek 服务：

| 供应商 | 模型示例 | 特点 |
|--------|----------|------|
| [阿里云百炼](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) | deepseek-v4-pro | 限流更宽松，支持联网搜索与上下文缓存 |
| [硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) | siliconflow/deepseek-v3.2 | 支持更长上下文 |
| [快手万擎](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md) | vanchin/deepseek-v4-pro | 快手直供 |

所有 DeepSeek 模型支持通过 `enable_thinking` 参数切换思考/非思考模式。思考过程通过 `reasoning_content` 字段返回。

> **注意**：deepseek-v3、deepseek-v3.1、deepseek-v3.2、deepseek-r1 等旧版模型将于 2026 年 7 月 9 日下架，推荐迁移至 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash。

### Kimi 系列

百炼提供两个供应商的 Kimi 服务：

- [月之暗面直供](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)：kimi-k2.6、kimi-k2.5，支持文本、图像和视频输入，支持 `enable_thinking` 和 `preserve_thinking`（多轮对话中传递思考过程）。
- [阿里云百炼部署](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)：支持华北2（北京）、美国（弗吉尼亚）、德国（法兰克福）三个地域。

> **注意**：Moonshot-Kimi-K2-Instruct、kimi-k2-thinking 将于 2026 年 7 月 9 日下架。

### GLM 系列

- [智谱直供](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)：ZHIPU/GLM-5.1，支持更长回复长度。
- [阿里云百炼部署](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)：glm-5.1，提供免费额度，采取阶梯计费。每个模型各有 100 万免费 Token。

> **注意**：glm-4.6、glm-4.7 将于 2026 年 7 月 9 日下架。

### MiniMax 系列

- [阿里云百炼部署](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)：MiniMax-M2.5。
- [MiniMax 直供](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)：MiniMax/MiniMax-M2.7。

> **注意**：MiniMax-M2.1 将于 2026 年 7 月 9 日下架。

### 其他模型

- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)：xiaomi/mimo-v2.5-pro，默认开启思考模式。
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)：stepfun/step-3.7-flash，多模态推理模型，默认关闭思考模式，支持 `reasoning_effort` 参数控制推理深度（low/medium/high）。

### 通用调用模式

所有第三方模型均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，核心步骤：

1. 获取 API Key 并配置环境变量 `DASHSCOPE_API_KEY`
2. 设置 `base_url` 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`
3. 使用对应的 `model` 名称调用（部分需带供应商前缀，如 `siliconflow/deepseek-v3.2`）
4. 思考模式通过 `enable_thinking` 参数控制（Python SDK 需放在 `extra_body` 中）

## 应用实践

### 基于 LlamaIndex 构建 RAG 应用

[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)介绍了在 LlamaIndex 中使用百炼检索增强服务的完整流程：

1. **文件解析**：使用 `DashScopeParse` 解析 .doc/.docx/.pdf 文件（单文件 100M 以内，1000 页以内）
2. **创建知识库**：通过 `DashScopeCloudIndex.from_documents()` 创建
3. **检索与查询**：获取 `retriever` 或 `query_engine` 进行语义检索和问答

需要 Python >= 3.8 且 <= 3.12，安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`。

### 文档转视频

[借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)展示了一个端到端方案：文档切片 -> 生成演示文稿 -> 生成讲解语音与字幕 -> 合成视频。依赖 FFmpeg（音视频处理）和 Marp（演示文稿制作），调用百炼大语言模型和多模态模型完成内容生成。

### 自定义模型调优与评测

[自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)介绍了完整的自定义模型创建流程：

1. **训练数据准备**：收集业务数据，编排为 Prompt-Completion 格式，建议至少 500 条
2. **模型调优**：选择预置模型，配置超参数（学习率、迭代次数等），平台自动训练
3. **模型部署**：部署到独占实例后才能调用和评测
4. **模型评测**：支持自动化评测，不满意可调整训练策略后重复流程

## API 最佳实践

### 限流应对

[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)提供了三层应对方案：

- **平台配置**（低改动成本）：服务端排队等待（`X-DashScope-Wait-Timeout` 请求头，推荐首选）、提升限流额度、PTU 预留算力、Batch API 异步批处理
- **客户端流控**：基础重试、令牌桶、平滑限速器、自适应拥塞控制
- **架构兜底**：模型降级（Fallback）、基于消息队列的削峰填谷

百炼 API 有三种限流规则：分钟级配额（RPM/TPM）、瞬时频率（RPS/TPS）、增速限制（Traffic Burst）。限流按主账号维度、模型独立计算，触发后通常 1 分钟内恢复。

### 显式缓存

[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)通过在请求中添加 `cache_control` 标记实现确定性缓存命中，首次写入仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本。适用于高频复用相同 Prompt、工业级 Agent 长上下文管理等场景。

以下工具原生支持显式缓存：

| 工具 | 缓存行为 |
|------|----------|
| Claude Code | v2.x 起默认携带 `cache_control`，接入百炼 Anthropic 端点后自动生效 |
| Open Code | 通过 `@ai-sdk/anthropic` 接入时默认注入 |
| OpenClaw | 走 Anthropic 端点时默认注入，支持 `OPENCLAW_CACHE_BOUNDARY` 自定义缓存边界 |
| Hermes | 通过配置接入 |

接入端点根据套餐不同：按量计费使用 `dashscope.aliyuncs.com/apps/anthropic`，Token Plan 团队版和 Coding Plan 使用各自专用域名。

## 来源文档

- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


