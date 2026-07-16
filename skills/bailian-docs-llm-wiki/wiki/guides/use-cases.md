# use cases

本页汇总阿里云百炼平台的典型使用场景与实践指南，覆盖三大方向：Prompt 设计技巧（文生文、文生图、文生视频）、第三方/多供应商模型接入（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等），以及工程化最佳实践（RAG、限流应对、显式缓存、模型调优、端到端解决方案）。面向开发者，以下内容按主题组织，便于快速定位到对应的参数、调用方式和注意事项。

## Prompt 设计与生成类场景

针对不同模态，百炼提供了结构化的提示词方法论：

- **文生文**：推荐使用「背景 / 目的 / 风格 / 语气 / 受众 / 输出」六要素的 Prompt 框架，任务描述越清晰具体，模型表现越贴近预期。控制台还提供 Prompt「自动优化」工具，可自动扩写和补充细节（该功能调用大模型，按推理费用计费）。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图**：核心参数为正向提示词 `prompt`、反向提示词 `negative_prompt`；文生图 V2 额外支持 `prompt_extend`（默认 `true`，开启大模型智能改写）。提示词公式分基础版（主体 + 场景 + 风格）与进阶版（增加镜头语言、氛围词、细节修饰），并配有景别、视角、风格、光线等提示词词典。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频 / 图生视频**：正向提示词描述画面内容与运动过程。基础公式为「主体 + 场景 + 运动」，进阶公式增加「美学控制 + 风格化」，图生视频则以「运动 + 运镜」为主。较新的 wan2.7 / wan2.6 还支持声音公式（人声/音效/BGM）、多镜头公式（镜头序号 + 时间戳 + 分镜内容）和参考生视频公式。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)；第三方视频模型可参考 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)（含大动态、运镜、风格等触发关键词词典）。

> **注意**：wan2.7 模型不再支持通过 `shot_type` 指定单镜头/多镜头，改由模型结合提示词自行发挥；如需一镜到底，中文写「生成单镜头」、英文写「Generate single shot.」。

## 第三方与多供应商模型接入

多篇教程介绍了在百炼平台通过 **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)** 或 **DashScope SDK** 调用第三方模型，通用要点如下：

- **前置条件**：先[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量；部分模型需在控制台模型广场「立即开通」后才能调用。
- **思考模式**：多数模型通过 `enable_thinking` 参数控制是否输出推理过程（`reasoning_content`）。注意 `enable_thinking` 非 OpenAI 标准参数——OpenAI Python SDK 需通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。
- **地域差异**：不同地域的 Base URL 不同，部分供应商（硅基流动、快手万擎、月之暗面、智谱、MiniMax、小米、阶跃星辰）仅限特定地域（多为华北2（北京））。详见 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 与 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。

各供应商的默认思考模式行为并不一致，接入时需按模型区分：

- **默认开启思考**：`mimo-v2.5-pro`（[MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)）、`kimi/kimi-k2.6`/`kimi-k2.5` 默认开启，可关闭。
- **仅思考模型**：`kimi/kimi-k2.7-code` 系列 `enable_thinking` 始终为 `true`，无法关闭；`kimi-k2.7-code-highspeed` 功能与 `kimi-k2.7-code` 一致但速度提升 5~6 倍（见 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）。
- **默认关闭思考**：`stepfun/step-3.7-flash` 默认关闭，需显式开启，并可用 `reasoning_effort`（`low`/`medium`/`high`）控制深度。
- **供应商差异**：同为 DeepSeek，硅基流动供应商支持更长上下文；阿里云百炼供应商限流更宽松，并支持联网搜索与上下文缓存。GLM 智谱直供的 `glm-5.2` 支持 1M 上下文，并可用 `reasoning_effort`（`max`/`high`/`none`）。

> **注意**：多篇教程标注 deepseek-v3/v3.1/v3.2/r1 系列、`MoonshotKimi-K2` 与 `kimi-k2-thinking`、`glm-4.6`/`glm-4.7`、`MiniMax-M2.1` 等模型将于 **2026年7月9日** 下架，推荐转用 `qwen3.7-plus` / `qwen3.7-max` / `qwen3.6-flash`。同时不同教程示例中出现的模型版本号存在差异（如 deepseek-v3.2 与 deepseek-v4-pro、MiniMax-M2.5 与 MiniMax-M2.7、kimi-k2.5 与 kimi-k2.7），以模型广场实际可用列表为准。

## RAG 与知识库

[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 演示了在 LlamaIndex 中使用百炼检索增强服务的完整链路：

- 安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`（Python 版本要求 >=3.8 且 <=3.12）。
- 使用 `DashScopeParse` 在线解析 .doc/.docx/.pdf 文件（单文件 <100M、页数 <1000），再通过 `DashScopeCloudIndex.from_documents` 创建知识库，`index.as_retriever()` / `index.as_query_engine()` 获取检索器与查询引擎。

## 工程化最佳实践

- **限流应对**：百炼 API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三种规则限流，按主账号维度、模型独立计算，触发后通常 1 分钟恢复。方案按改动成本由低到高分为平台配置（服务端排队等待、提升额度、PTU、Batch API）、客户端流控（重试、令牌桶、平滑限速、自适应拥塞控制）、架构兜底（模型降级、MQ 削峰）。针对突发限流推荐首选在请求头添加 `X-DashScope-Wait-Timeout`（建议 3~120 秒），并相应调大客户端超时时间。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **显式缓存**：通过在请求中添加缓存标记实现 100% 确定性命中，适合高频复用相同 Prompt、长上下文 Agent 等场景。首次写入约产生标准价格 25% 的额外开销，后续命中可节省约 90% 成本。Claude Code、OpenCode、OpenClaw 等工具通过 Anthropic 兼容端点（`/apps/anthropic`）接入时原生支持。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。
- **自定义模型**：创建自定义模型分为模型调优、模型部署、模型评测三个主步骤，配套训练数据准备、评测模板设计、调整训练策略。数据需编排为「Prompt-Completion」格式，建议至少准备 500 条并做脱敏处理。注意**调优后的模型必须先部署才能调用和评测**。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 端到端解决方案

多篇实践方案展示了如何组合百炼模型能力构建完整应用，多数基于函数计算 FC、开箱即用并提供免费试用额度：

- **文档转视频**：结合大模型与多模态技术，将文档自动切片、生成演示文稿、语音字幕并合成视频，依赖 FFmpeg 与 Marp 工具，提供完整代码包。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。
- **AI 智能体与工作流**：以 AI 电商客服为例，覆盖智能问答、RAG、自主决策 Agent、对话流四种应用形态（[高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)）。
- **视觉创作平台**：集成 Wan2.7 图像生成与 HappyHorse 视频生成，提供节点式编排、AI 导演与在线剪辑（[HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)）。
- **深度研究报告**：Qwen-Deep-Research 自动规划检索路径、多源交叉验证并生成结构化洞察报告（[深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)）。
- **AI 解题批改**：基于 Qwen3-VL 视觉模型实现拍照解题与作业自动批改，支持 33 种语言（[AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)）。

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
- [HappyHorse 打造一站式影视创作平台](../../raw/model-user-guide/use-cases/infinite-canvas.md)
- [高效搭建 AI 智能体与工作流应用](../../raw/model-user-guide/use-cases/build-ai-applications-based-on-alibaba-cloud-model-studio.md)
- [深度研究：生成你的独家洞察报告](../../raw/model-user-guide/use-cases/deep-research.md)
- [AI 解题 + 批改：推动课程教学智变](../../raw/model-user-guide/use-cases/ai-homework-helper.md)




