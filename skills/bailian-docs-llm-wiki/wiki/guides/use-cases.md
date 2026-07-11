# use cases

本页汇总阿里云百炼平台的典型使用场景，涵盖 Prompt 工程（文生文/文生图/文生视频）、第三方模型接入、RAG 与知识库、限流与缓存治理，以及一批开箱即用的行业解决方案。内容面向开发者，聚焦可落地的参数、调用方式与注意事项。

## Prompt 工程

不同生成任务的 Prompt 结构差异明显，百炼为每类任务提供了公式化模板：

- **文生文**：核心是构建清晰、无歧义的 Prompt，并推荐使用「背景 / 目的 / 风格 / 语气 / 受众 / 输出」六要素框架系统化描述需求。控制台还提供 Prompt 一键优化工具（自动扩写），该功能通过调用大模型实现，会消耗 Token 并按推理费用计费。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生图**：两个关键参数是 `prompt`（正向，支持中英文）与 `negative_prompt`（反向，描述不希望出现的内容）。文生图 V2 额外支持 `prompt_extend`（默认 `true`，开启大模型智能改写）。提示词遵循「主体 + 场景 + 风格」基础公式，进阶时叠加镜头语言、氛围词、细节修饰。参见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生视频/图生视频**：基础公式为「主体 + 场景 + 运动」；图生视频因图像已定主体，主要写「运动 + 运镜」。wan2.7/wan2.6/wan2.5 支持声音描述（人声/音效/BGM），wan2.7/wan2.6 支持多镜头连贯叙事与参考生视频。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。
- **Vidu 视频**：结构为「主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介」，并通过触发关键词（如「大动态」「镜头推进」）控制运动幅度与运镜，详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## 第三方模型接入

百炼以统一的 **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**和 **[DashScope SDK](../concepts/dashscope-sdk.md)** 托管多家第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等）。通用约定：

- 先获取 API Key 并配置到环境变量；OpenAI 兼容基础地址为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
- 思考模式通过 `enable_thinking` 参数控制。注意它**不是 OpenAI 标准参数**：OpenAI Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。思考内容通过 `reasoning_content` 字段返回。
- 不同供应商默认行为不同：Kimi 的 `kimi-k2.7-code` 系列为仅思考模型（`enable_thinking` 恒为 true）；MiMo `mimo-v2.5-pro` 默认开启思考；Stepfun `step-3.7-flash` 默认关闭思考。GLM/Stepfun 还支持 `reasoning_effort` 控制推理深度。

> **注意**：同一模型可能有多个供应商版本，能力与限制不同。例如 DeepSeek 同时有[阿里云自营](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)与[快手万擎](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)三种接入，模型名前缀（如 `siliconflow/`、`vanchin/`）和支持地域各异。硅基流动供应商上下文更长，阿里云自营限流更宽松且支持联网搜索与上下文缓存。

> **注意**：多篇接入文档标注部分模型（deepseek-v3.x/r1、Kimi-K2、glm-4.6/4.7、MiniMax-M2.1 等）将于 **2026年7月9日下架**，推荐转用 qwen3.7-plus / qwen3.7-max / qwen3.6-flash。同时文档正文出现了 deepseek-v4-pro、kimi-k2.6、glm-5.2、MiniMax-M2.5/M2.7、mimo-v2.5-pro 等更新版本命名，模型版本演进较快，接入前请以控制台模型广场的实时信息为准。

> **注意**：地域限制差异大。硅基流动 DeepSeek、月之暗面直供 Kimi、GLM-智谱、MiniMax 直供、MiMo、Stepfun 等多为**仅华北2（北京）**地域可用；华北2（北京）新推业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，性能与稳定性更优，建议从 `https://dashscope.aliyuncs.com` 迁移，旧域名仍可用。

## RAG 与知识库

[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 展示了在 LlamaIndex 中集成百炼检索增强服务的完整链路：

- 依赖安装：`llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`，Python 版本要求 `>=3.8 且 <=3.12`。
- 用 `DashScopeParse`（`ResultType.DASHSCOPE_DOCMIND`）解析文档，支持 .doc/.docx/.pdf，单文件 100M 以内、页数 1000 以内。
- 通过 `DashScopeCloudIndex.from_documents` 建库，`index.as_retriever()` 获取检索器，`index.as_query_engine(llm=...)` 构建问答引擎，并支持 `_insert` / `delete_ref_doc` 增删文档。

## 限流与缓存治理

生产调用需处理限流与成本问题：

- **限流**：百炼按主账号、按模型独立限流，规则包含分钟级（RPM/TPM）、瞬时（RPS/TPS）与增速（Traffic Burst）三类。针对突发流量，推荐首选「服务端排队等待」——在请求头加 `X-DashScope-Wait-Timeout`（建议 3~120 秒），并相应放大客户端超时时间。该功能**仅对增速/突发限流（Throttling.BurstRate）生效，不适用于 RPM/TPM 绝对值限流**。更多策略（令牌桶、平滑限速器、模型降级、MQ 削峰）见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。
- **显式缓存**：可做到 100% 确定性命中，适合高频复用相同 Prompt 与 Agent 长上下文管理。首次写入缓存产生标准价格 25% 的额外开销，后续命中可节省 90% 成本。Claude Code、OpenCode、OpenClaw 等工具通过 Anthropic 兼容端点（`/apps/anthropic`）接入时会自动注入 `cache_control`，详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 自定义模型

[自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md) 描述了「调优 → 部署 → 评测」三阶段流程。要点：

- 训练数据编排为「Prompt-Completion」格式，建议至少准备 500 条，并做文本分割与脱敏处理。
- **完成调优的模型必须先部署到独占实例，才能被调用和评测**；对评测结果不满意可调整训练策略（换基础模型、扩充数据、调超参）后重复整个流程。

## 行业解决方案

百炼提供多套函数计算（FC）驱动的开箱即用方案，可一键部署：

- **文档转视频**：结合 LLM 与[多模态](../concepts/multimodal.md)能力，经「文档切片 → 生成演示文稿 → 生成语音字幕 → 合成视频」四步产出图文/语音/字幕视频，依赖 FFmpeg 与 Marp。
- **AI 智能体与工作流**：以电商客服为例，涵盖智能问答、RAG、自主决策 Agent、对话流四类应用。
- **深度研究**：Qwen-Deep-Research 自动规划检索路径、多源交叉验证并生成结构化洞察报告。
- **AI 解题 + 批改**：基于 Qwen3-VL 视觉模型，支持拍照解题与作业自动批改，覆盖多学科、33 种语言。
- **一站式影视创作（HappyHorse）**：集成 Wan2.7 图像生成与 HappyHorse 视频生成，提供节点式编排、AI 导演与在线剪辑。

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


