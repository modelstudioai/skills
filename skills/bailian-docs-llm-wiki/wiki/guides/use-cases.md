# use cases

百炼模型计算服务（Model Studio）不仅提供统一的模型推理 API，还围绕"如何把大模型真正用起来"提供了一整套使用范式与最佳实践。本主题页把官方使用指南中分散的场景化文档归纳为六类典型用法，帮助开发者快速定位与自己需求最接近的范式，再深入对应专题文档落地。

## 总览：六类典型用法

| 类别 | 解决的问题 | 关键文档 |
| --- | --- | --- |
| 文本生成与 Prompt 工程 | 用通义/第三方大模型做对话、抽取、改写等文本任务 | 文生文 Prompt 指南 |
| [多模态](../concepts/multimodal.md)生成 | 文生图、文生视频、图生视频、文档转视频 | 文生图/文生视频 Prompt 指南、文档转视频 |
| 检索增强生成（RAG） | 让模型基于私有知识回答，降低幻觉 | 基于 LlamaIndex 构建 RAG 应用 |
| 模型调优与评测 | 用自有数据微调、部署、评测自定义模型 | 自定义模型调优、部署与评测 |
| 第三方模型 API 接入 | 在百炼统一调用 DeepSeek、Kimi、GLM、MiniMax 等第三方模型 | DeepSeek / Kimi / GLM / MiniMax / MiMo / Vidu / Stepfun 接入指南 |
| 工程化与稳定性 | 控成本、控流量、提吞吐 | 限流应对最佳实践、显式缓存最佳实践 |

## 文本生成与 Prompt 工程

文生文是大模型最基础也最灵活的用法。百炼将通义千问系列及多家第三方大模型统一封装为 OpenAI 兼容的 Chat Completions 接口，开发者只需更换 `model` 参数即可在不同模型间切换，无需改动业务代码。

Prompt 工程是提升文本任务质量的核心手段，官方指南主要给出以下方向：

- **角色与任务定义**：用系统消息（system）明确模型身份、任务目标与输出格式，降低跑题概率。
- **少样本示例（few-shot）**：在请求中提供 1–3 条符合期望格式的输入/输出样例，让模型模仿风格与结构。
- **结构化输出**：要求模型返回 JSON、Markdown 表格等可解析结构，便于下游程序消费；可结合 `response_format` 参数强制 JSON。
- **思维链（CoT）**：对推理类任务，显式要求"先思考再回答"，并把推理过程放在可折叠或可丢弃的字段中。
- **约束与否定**：用正向约束描述"应当做什么"，比单纯罗列"不要做什么"更有效；必要时再用否定约束兜底。
- **上下文长度管理**：长上下文场景下注意将最关键指令放在末尾，并对超长文档做分块/摘要后再喂入。

> 实践建议：先在百炼控制台"模型体验"中迭代 Prompt，确认效果稳定后再固化到代码；同一 Prompt 在不同模型上效果差异较大，切换模型后应回归测试。

## [多模态](../concepts/multimodal.md)生成

### 文生图

文生图 Prompt 指南面向通义万相等图像生成模型。要点包括：

- 用"主体 + 风格 + 构图 + 光照 + 画质修饰"的结构化描述提升可控性。
- 明确画幅比例、镜头视角、艺术风格（写实/插画/油画等）。
- 负面提示词（negative [prompt](prompt.md)）用于排除不想要的元素。
- 复杂场景拆分为多轮生成或使用图像编辑接口做局部修改。

### 文生视频 / 图生视频

文生视频与图生视频 Prompt 指南（含 Vidu 等模型）强调：

- 描述要包含"镜头运动 + 主体动作 + 场景变化 + 时长"。
- 图生视频时首帧图的质量与构图直接决定成片质量。
- 避免在一条 Prompt 中塞入过多动作，必要时分段生成再拼接。
- 注意各模型对分辨率、时长、帧率的限制。

### 文档转视频

"借助大模型将文档转换为视频"展示了一条端到端链路：先用大模型把文档内容拆解为讲解脚本与分镜，再调用文生图/文生视频接口生成画面素材，最后合成带配音与字幕的视频。适合快速把技术文档、产品介绍转化为可传播的视听内容。

## 检索增强生成（RAG）

当模型需要基于企业私有知识回答时，直接把知识塞进 Prompt 受上下文长度与成本限制，且易产生幻觉。RAG（Retrieval-Augmented Generation）的典型流程为：

1. **知识准备**：把文档、网页、数据库等知识源切分为语义块（chunk）。
2. **向量化**：调用百炼的 Embedding 模型生成向量。
3. **入库检索**：写入向量数据库，按用户 query 召回 top-K 相关块。
4. **拼装上下文**：把召回块与用户问题一起作为上下文送入大模型。
5. **生成回答**：模型基于上下文生成带来源引用的回答。

百炼提供"数据管理"模块托管上述流程，也支持通过 LlamaIndex 等开源框架自建 RAG 应用——官方《基于 LlamaIndex 构建 RAG 应用》指南演示了如何用 LlamaIndex 接入百炼的 Embedding 与 Chat 模型，快速搭建一个可问答的知识库应用。

## 模型调优、部署与评测

当通用大模型在特定领域效果不足时，可在百炼上做自定义模型调优：

- **训练数据准备**：按 SFT/DPO 等范式准备指令对或偏好对数据，注意去重、脱敏与类别均衡。
- **训练任务**：基于通义千问等基座发起微调任务，监控 loss 与评估指标。
- **部署**：训练完成后部署为独占 API 端点，获得稳定 QPS 与隔离资源。
- **评测**：用内置评测集或自定义评测集对调优前后模型打分，确认增益后再上线。

调优前应先穷尽 Prompt 工程与 RAG 方案——只有当这些手段都无法满足时再投入训练成本，性价比最高。

## 第三方模型 API 接入

百炼模型广场聚合了多家第三方大模型，统一通过百炼网关调用，免自建鉴权与配额管理。覆盖范围（按厂商）：

- **DeepSeek**：DeepSeek-V3/R1 等推理模型，支持深度思考模式；可通过百炼默认入口或 SiliconFlow、Vanchin 等渠道接入。
- **Kimi（Moonshot AI）**：超长上下文对话，适合长文档处理。
- **GLM（智谱 AI）**：通用对话与[多模态](../concepts/multimodal.md)能力。
- **MiniMax**：对话与语音/视频生成。
- **MiMo（小米）**：推理与通用任务。
- **Vidu**：视频生成。
- **Stepfun（阶跃星辰）**：多模态通用模型。

接入方式高度一致：在控制台开通对应模型后，将 `model` 参数替换为该模型标识，其余请求结构、鉴权方式与通义模型相同。切换模型前应关注各模型在上下文长度、[函数调用](../concepts/function-calling.md)、[流式输出](../concepts/streaming-output.md)、[计费](../concepts/billing.md)方式上的差异。

## 工程化与稳定性

### 限流应对

百炼对每个模型/账号施加 QPS 与 TPM 限制以保证服务稳定。当遇到 429 限流时，最佳实践为：

- **指数退避重试**：对 429 响应按指数退避 + 抖动重试，避免雪崩。
- **错峰与排队**：在客户端用令牌桶/漏桶控制发送速率，平滑突发流量。
- **分级降级**：高峰期降级到更轻量模型或关闭非核心调用。
- **批量与流式**：能合并的请求用批量接口；长输出用流式降低单次超时风险。
- **配额监控**：监控剩余配额，临近上限时主动限速。

### 显式缓存

显式缓存（Explicit Cache）通过复用前缀的计算结果，显著降低重复上下文的延迟与成本。适用场景：

- 多轮对话中系统提示词与历史消息较长且稳定。
- RAG 中同一知识库 chunk 被多次复用。
- 固定指令模板 + 变量后缀的批量请求。

使用时需按接口要求显式标记缓存边界，并注意缓存的 TTL 与命中条件；变更前缀内容会使缓存失效，应把稳定部分放在最前。

## 选型建议

- 先用 **Prompt 工程** 验证需求是否可被通用模型满足。
- 涉及私有知识时优先 **RAG**，而非把知识塞进上下文。
- 需要图像/视频产出时走 **多模态生成** 链路。
- 效果瓶颈确属模型能力不足时再投入 **模型调优**。
- 对延迟与成本敏感的长前缀场景开启 **显式缓存**。
- 高并发线上服务必须前置 **限流应对** 策略。

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


