# use cases

阿里云百炼平台提供丰富的应用场景支持，涵盖 Prompt 工程、[多模态](../concepts/multimodal.md)内容生成、RAG 应用构建、模型自定义调优、第三方模型集成、限流应对以及显式缓存优化等方向。本文汇总各类典型使用场景的核心要点和实践指引，帮助开发者快速定位适合业务需求的方案。

## Prompt 工程

### 文生文 Prompt 设计

高质量 Prompt 是发挥大模型能力的关键。核心原则：

- **清晰具体**：任务描述越明确，模型输出越符合预期
- **使用 Prompt 框架**：按「背景 + 目的 + 风格 + 语气 + 受众 + 输出」六要素结构化编写
- **借助优化工具**：百炼控制台提供 Prompt 一键优化（自动扩写），可在 [Prompt 页面](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt) 使用

详细技巧参见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt 设计

适用于万相-文生图 V1/V2 模型，关键参数包括 `prompt`（正向提示词）、`negative_prompt`（反向提示词）和 `prompt_extend`（智能改写，V2 默认开启）。

两种公式：

- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

通过景别（特写/近景/中景/远景）、视角（平视/俯视/仰视）、光线和风格等维度可精细控制画面效果。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频 / 图生视频 Prompt 设计

适用于万相系列视频生成模型（wan2.5/2.6/2.7），核心公式：

- **基础**：主体 + 场景 + 运动
- **进阶**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频**：运动 + 运镜（图像已确定主体和风格）
- **声音公式**（wan2.6/2.7）：增加人声/音效/背景音乐描述
- **多镜头公式**（wan2.6/2.7）：总体描述 + 镜头序号 + 时间戳 + 分镜内容

wan2.7/2.6 还支持参考生视频，使用"图n"或"视频n"指代参考素材。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

### Vidu 视频生成

Vidu 模型使用提示词公式：主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介。支持通过关键词控制动态幅度（大/中/小动态）、运镜（推/拉/平移/环绕等）、景别视角和视频风格（2D动漫/3D渲染/写实/水墨等）。详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## RAG 应用构建

通过 LlamaIndex 与百炼知识库服务集成，可快速构建 RAG 应用：

1. **文件解析**：使用 `DashScopeParse` 解析 .doc/.docx/.pdf 文件（单文件 100M 以内、1000 页以内）
2. **创建知识库**：`DashScopeCloudIndex.from_documents(documents, "index_name")`
3. **检索与问答**：通过 `index.as_retriever()` 获取 retriever，或 `index.as_query_engine(llm=dashscope_llm)` 直接问答

前提条件：安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优

创建自定义模型包含三个主要步骤：

1. **模型调优**：准备训练数据（Prompt-Completion 格式，建议 500+ 条）→ 配置训练超参数 → 自动训练
2. **模型部署**：将调优后的模型部署到独占实例（完成调优的模型必须部署后才能调用和评测）
3. **模型评测**：配置评测任务验证模型效果

训练数据准备要点：来源多样化、质量控制、平衡性考量。平台提供数据清洗和数据增强工具。如评测不满意，可调整训练策略后重复流程。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 文档转视频

借助大模型可将文档自动转换为带图文、语音、字幕的视频：

1. 文档切片（LLM 总结标题、划分段落）
2. 生成演示文稿（Marp 渲染）
3. 生成讲解语音与字幕（[多模态](../concepts/multimodal.md)模型 TTS）
4. 合成视频（FFmpeg 剪辑）

依赖 FFmpeg 和 Marp CLI。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型集成

百炼平台支持通过统一的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用多家第三方模型：

| 供应商 | 代表模型 | 供应方式 |
|--------|----------|----------|
| DeepSeek | deepseek-v4-pro | 阿里云部署 / 硅基流动直供 / 快手万擎直供 |
| Kimi (月之暗面) | kimi-k2.7-code, kimi-k2.6 | 阿里云部署 / 月之暗面直供 |
| GLM (智谱) | glm-5.2 | 阿里云部署 / 智谱直供 |
| MiniMax | MiniMax-M2.7, MiniMax-M2.5 | 阿里云部署 / MiniMax 直供 |
| MiMo (小米) | mimo-v2.5-pro | 小米直供 |
| Stepfun (阶跃星辰) | step-3.7-flash | 阶跃星辰直供 |

调用方式统一：配置 `base_url` 为百炼端点 + 使用 `DASHSCOPE_API_KEY`，支持思考模式（`enable_thinking` 参数）。多数第三方模型支持多地域（北京、新加坡、弗吉尼亚、法兰克福、东京）。

> **注意**：部分第三方模型（deepseek-v3 系列、glm-4.6/4.7、Kimi-K2-Instruct、MiniMax-M2.1 等）将于 2026 年 7 月 9 日下架，推荐转用 qwen3.7-plus / qwen3.7-max / qwen3.6-flash。

## 限流应对

百炼 API 按请求数（RPM/RPS）和 [Token](../concepts/token.md) 用量（TPM/TPS）限流，还有增速限制（Traffic Burst）。应对方案按改动成本从低到高：

**平台配置（低成本）**：
- 服务端排队等待：请求头添加 `X-DashScope-Wait-Timeout`，突发限流时服务端自动排队重试
- 提升限流额度：控制台直接申请，即时生效
- PTU 预置吞吐单元：独立专享算力，保障 SLA
- Batch API：离线批处理，不受在线限流约束

**客户端流控**：从基础重试 → 令牌桶/并发信号量 → 平滑限速器/双重令牌桶 → 自适应拥塞控制，按复杂度递进。

**架构兜底**：模型降级（Fallback）、基于消息队列的削峰填谷。

详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 显式缓存

显式缓存通过在请求中添加 `cache_control` 标记，确保相同输入确定性命中缓存，节省 90% 成本。适用场景：

- 高频复用相同 Prompt
- 工业级 Agent 长上下文管理
- 需要稳定命中保证

多款 Agent/Coding 工具原生支持（通过 Anthropic 协议接入百炼）：

- **Claude Code**：v2.x 起默认携带缓存标记，接入百炼端点即可
- **OpenCode**：通过 `@ai-sdk/anthropic` 接入，自动注入缓存控制
- **OpenClaw**：支持自定义缓存边界标记（`<!-- OPENCLAW_CACHE_BOUNDARY -->`）
- **Hermes**：通过配置命令设置接入参数

端点选择：按量[计费](../concepts/billing.md)用 `dashscope.aliyuncs.com/apps/anthropic`，[Token](../concepts/token.md) Plan 团队版和 Coding Plan 有各自专属端点。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)


