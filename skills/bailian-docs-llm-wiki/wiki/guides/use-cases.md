# use cases

本页汇总阿里云百炼平台的典型使用场景与最佳实践，涵盖三大类内容：Prompt 工程指南（文生文/文生图/文生视频）、工程化最佳实践（[限流](../concepts/rate-limit.md)应对、显式缓存、RAG 构建、模型调优）、以及第三方模型接入教程（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等）。这些实践面向开发者，帮助从模型调用到完整 AI 应用落地的全流程提效。

## Prompt 工程指南

### 文生文

[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 的核心原则是构建清晰、具体、无歧义的任务描述，并推荐使用 Prompt 框架系统化组织提示词：

- **框架六要素**：背景、目的、风格、语气、受众、输出格式。
- 平台提供 **Prompt 一键优化工具**（控制台 Prompt 页面的"自动优化"），可自动扩写和添加细节。注意该功能通过调用大模型实现，按模型推理费用计费。

### 文生图

[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 适用于万相-文生图 V1/V2，关键参数：

- `prompt`：正向提示词，支持中英文。
- `negative_prompt`：反向提示词，描述不希望出现的内容。
- `prompt_extend`（仅 V2）：是否开启大模型智能改写，默认 `true`，推荐保持默认。

提示词公式：基础版为"主体 + 场景 + 风格"；进阶版追加主体/场景描述、镜头语言、氛围词与细节修饰。文档还提供景别、视角、风格、光线等维度的提示词词典。

### 文生视频 / 图生视频

[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 针对万相视频模型，按能力分层：

- **基础公式**：主体 + 场景 + 运动；**进阶公式**追加美学控制与风格化。
- **图生视频**：图像已确定主体与风格，提示词只需描述"运动 + 运镜"。
- **声音公式**（wan2.7/wan2.6/wan2.5）：支持人声（内容+情绪+语调+语速+音色+口音）、音效、背景音乐三类描述。
- **多镜头公式**（wan2.7/wan2.6）：总体描述 + 镜头序号 + 时间戳 + 分镜内容，可生成多镜头连贯叙事视频。
- **参考生视频**（wan2.7/wan2.6）：用"图n"/"视频n"指代参考素材，可参考主体外观、动态特征、音色和背景。

> **注意**：wan2.7 不再支持 `shot_type` 参数指定单镜头/多镜头，改由模型结合提示词决定；需要一镜到底时在提示词中写"生成单镜头"。

第三方 Vidu 模型有独立的提示词体系（见 Vidu视频生成Prompt指南），支持"大动态/中动态/小动态"等触发关键词、运镜控制与导演风格。

## 工程化最佳实践

### [限流](../concepts/rate-limit.md)应对

百炼 API 按主账号 + 模型维度[限流](../concepts/rate-limit.md)，分为 RPM/TPM（分钟级配额）、RPS/TPS（瞬时频率）、Traffic Burst（增速限制）三类规则。[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 按改动成本从低到高给出三层方案：

1. **平台配置**：服务端排队等待（请求头 `X-DashScope-Wait-Timeout`，建议 3~120 秒，仅对 Throttling.BurstRate 生效）、提升限流额度、PTU、Batch API。使用排队等待时需相应上调客户端超时时间（非流式：原超时 + Wait-Timeout 值）。
2. **客户端流控**：从基础重试、令牌桶/并发信号量、双重令牌桶/平滑限速器到自适应拥塞控制，按工程复杂度递进。
3. **架构兜底**：模型降级（Fallback）与基于消息队列的削峰填谷。

错误码对照：`Throttling.RateQuota`（RPM/RPS 超限）、`Throttling.AllocationQuota`（TPM/TPS 超限）、`Throttling.BurstRate`（增速超限）。

### 显式缓存

显式缓存通过在请求中添加缓存标记实现 **100% 确定性命中**：首次写入产生标准价格 25% 的额外开销，后续命中节省 90% 成本。适用于高频复用相同 Prompt、Agent 长上下文管理等场景。Claude Code、OpenCode、OpenClaw 等工具通过 Anthropic 兼容端点（`/apps/anthropic`）接入百炼后自动携带 `cache_control` 标记，无需额外配置。

### RAG 与模型定制

- **基于 LlamaIndex 构建 RAG**：使用 `DashScopeParse` 解析文档（支持 .doc/.docx/.pdf，单文件 ≤100MB 且 ≤1000 页），通过 `DashScopeCloudIndex` 创建/读取知识库，`as_retriever()` / `as_query_engine()` 构建检索与问答链路。Python 版本要求 >=3.8 且 <=3.12。
- **自定义模型调优、部署与评测**：流程为模型调优 → 模型部署 → 模型评测；调优完成的模型**必须部署后才能调用和评测**。训练数据需整理为 Prompt-Completion 格式，建议至少 500 条。
- **文档转视频**：借助大模型完成文档切片、演示文稿生成、语音字幕合成与视频剪辑，依赖 FFmpeg 与 Marp 工具。

## 第三方模型接入

百炼模型广场提供多家第三方模型，统一通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，通用模式为：

- Base URL 采用[业务空间](../concepts/workspace.md)专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（各地域不同）。
- 直供模型（硅基流动、快手万擎、月之暗面、智谱、MiniMax 稀宇、小米、阶跃星辰）通常**仅限华北2（北京）地域**，且需先在控制台模型广场开通并授权。
- 思考模式普遍通过 `enable_thinking` 控制（非 OpenAI 标准参数，Python SDK 经 `extra_body` 传入），推理过程经 `reasoning_content` 字段返回；部分模型（Kimi、GLM-智谱、Stepfun）另支持 `reasoning_effort` 控制推理深度。

各模型要点：

| 供应商 | 代表模型 | 特点 |
| --- | --- | --- |
| DeepSeek-阿里云 | deepseek-v4-pro | 多地域可用；限流更宽松，支持联网搜索与上下文缓存 |
| DeepSeek-硅基流动 | siliconflow/deepseek-v3.2 | 支持更长上下文；仅北京地域 |
| DeepSeek-快手万擎 | vanchin/deepseek-v4-pro | 仅北京地域 |
| Kimi | kimi/kimi-k3、kimi-k2.7-code | 多地域；k3 与 k2.7-code 系列为仅思考模型 |
| GLM-智谱 | ZHIPU/GLM-5.2 | 支持 1M 上下文；仅北京地域 |
| MiniMax | MiniMax/MiniMax-M2.7 | 仅北京地域 |
| MiMo-小米 | xiaomi/mimo-v2.5-pro | 默认开启思考模式；仅北京地域 |
| Stepfun-阶跃星辰 | stepfun/step-3.7-flash | [多模态](../concepts/multimodal.md)推理，**默认关闭**思考模式；仅北京地域 |

> **注意**：多款第三方模型已公布下架计划——deepseek-v3/v3.1/v3.2/r1 系列将于 2026年10月10日 下架；Moonshot-Kimi-K2-Instruct、kimi-k2-thinking、glm-4.6/4.7、MiniMax-M2.1 将于 2026年7月9日 下架。官方推荐迁移至 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash，新项目应避免依赖这些即将下架的模型。

## 解决方案模板

平台提供多个可一键部署的场景化方案（多基于函数计算 + 百炼模型，按量付费）：

- **HappyHorse 影视创作平台**：基于 Wan2.7 图像生成与视频生成能力的节点式无限画布创作平台。
- **AI 智能体与工作流应用**：以 AI 电商客服为例，覆盖智能问答、RAG、Agent、对话流四种应用形态。
- **深度研究（Qwen-Deep-Research）**：自动规划研究路径、多源交叉验证并生成结构化决策报告。
- **AI 解题 + 批改**：基于 qwen3-vl-plus 视觉模型的拍照解题与作业自动批改，支持 33 种语言。

## 限制与注意事项

- 直供第三方模型多数仅在华北2（北京）地域可用，需使用该地域的 API Key，并将 Base URL 中的 `{WorkspaceId}` 替换为真实[业务空间](../concepts/workspace.md) ID。
- `enable_thinking`、`reasoning_effort` 等均为非 OpenAI 标准参数，各 SDK 传入方式不同（Python 用 `extra_body`，Node.js 作为顶层参数）。
- Prompt 优化工具、模型调优/部署/评测均产生费用，使用前确认计费规则与账号余额。
- 服务端排队等待仅缓解突发限流，对 RPM/TPM 绝对配额超限无效，需配合客户端流控或提额。

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


