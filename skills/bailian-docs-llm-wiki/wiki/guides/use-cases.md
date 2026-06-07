# use cases

本主题汇总阿里云百炼"模型使用指南"中的**典型用例**：Prompt 撰写指南、平台级最佳实践（限流、显式缓存、自定义微调）、端到端应用方案（RAG、文档转视频），以及通过百炼网关接入第三方模型（DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu 等）。文档面向需要在生产环境调用百炼能力的开发者，给出可直接复制的接入参数与工程约束。

## Prompt 撰写指南

百炼为三类生成任务分别沉淀了**结构化提示词公式**，所有公式都遵循"主体 + 场景 + 修饰"的脉络，但模态扩展点不同。

- **文生图**：使用 `prompt` / `negative_prompt`；文生图 V2 还支持 `prompt_extend`（默认开启）由大模型对原始 [prompt](prompt.md) 做智能改写。基础公式为「主体 + 场景 + 风格」，进阶公式追加「镜头语言 + 氛围词 + 细节修饰」。完整词典与示例见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。
- **文生文**：核心是"清晰具体的 Prompt"+"Prompt 框架"（背景 / 目的 / 风格 / 语气 / 受众 / 输出）。控制台提供 **Prompt 自动优化**入口可对原始描述扩写，调用按推理 Token 计费。详细技巧、Few-shot 示例与思维链模板见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。
- **文生视频 / 图生视频**：在主体 + 场景的基础上引入 **运动描述**、**美学控制**（光线 / 镜头 / 运镜）与 **风格化**。`wan2.5/2.6/2.7` 模型还支持「声音公式」（人声 / 音效 / BGM），`wan2.6/2.7` 支持「多镜头公式」用于连贯叙事。完整模板见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)；接入 Vidu 系列模型时另有专属规范，见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

> **注意**：图生视频提示词只需描述「运动 + 运镜」，**不要重复描述主体与场景**——这两项已由输入图像锁定，重复描述反而会与图像产生冲突。

## 平台级最佳实践

### 限流应对

百炼按**主账号 × 模型**维度独立限流，触发后通常 1 分钟内恢复，规则分三类：

| 限流类型 | 触发维度 | 典型错误码 |
| --- | --- | --- |
| 分钟级配额（RPM / TPM） | 请求数或 Token 量超过每分钟配额 | `Throttling.RateQuota` / `Throttling.AllocationQuota` |
| 瞬时频率（RPS / TPS） | 单秒内请求或 Token 过密 | 同上，启动瞬间集中报错 |
| 增速限制（Traffic Burst） | 短时间内请求量激增 | `Throttling.BurstRate` / `limit_burst_rate` |

应对方案按改动成本从低到高分三层：

1. **平台配置**（无需改代码）——服务端排队等待（仅加一个请求头）、申请提升配额、PTU 独占算力、Batch API 离线推理。
2. **客户端流控**——从基础重试 → 令牌桶 / 并发信号量 → 双重令牌桶 / 平滑限速器 → 自适应拥塞控制，按工程复杂度递进。
3. **架构兜底**——多模型 Fallback 降级、基于 MQ 的削峰填谷。

诊断表与各策略实现细节见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。如果当前正报 `429` 且属于突发流量，建议先试服务端排队（只需加请求头）。

### 显式缓存

显式缓存通过在请求中携带 `cache_control` 标记，**确定性命中**指定的上下文片段，不受后端调度影响。

- **写入开销**：首次写入额外消耗 25%；命中后节省 90% Token 费用——只要至少命中一次，总成本即低于不缓存方案。
- **典型场景**：高频复用相同 Prompt、Agent 长上下文管理（压缩 / recap / system reminder 不破坏关键片段命中）。
- **原生支持的工具**：Claude Code（v2.x 起默认携带 `cache_control`，三处标记 system/env/最近 user message）、OpenCode（`@ai-sdk/anthropic` 默认对 system 与最近非 system 消息注入）等。接入百炼 Anthropic 兼容端点后无需额外配置。

跨会话命中率优化、关闭缓存的环境变量（`DISABLE_PROMPT_CACHING_HAIKU/SONNET/OPUS`）等细节见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

### 自定义模型调优、部署与评测

百炼支持基于预置模型做微调，得到面向特定业务场景的"自定义大模型"。完整闭环分三主阶段 + 三辅助阶段：

1. **数据准备**：收集业务数据并整理成 `Prompt-Completion` 对，建议 ≥ 500 条；做文本切分、脱敏与质量控制。
2. **模型调优**：在控制台「训练新模型」向导配置学习率、迭代次数等超参；阿里云自动完成训练。
3. **模型部署**：调优后的模型**必须先部署到独占实例**才能调用或评测。
4. **模型评测**：通过「创建评测任务」向导按维度评分；不满意则调整训练策略（更换基础模型 / 扩充样本 / 改超参）后回到调优阶段。

数据上传、计费项与超参调优经验详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 应用方案

### RAG 检索增强

百炼提供托管的知识库 + 索引能力，可在 LlamaIndex 中无缝消费：

- 安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`（Python ≥ 3.8 且 ≤ 3.12）。
- 通过 `DashScopeParse` 在线解析 `.doc / .docx / .pdf`（单文件 ≤ 100 MB、≤ 1000 页）。
- 解析结果用 `DashScopeCloudIndex.from_documents()` 写入百炼托管索引，后续按业务空间检索。

需先开通百炼"知识库"服务并准备 `DASHSCOPE_WORKSPACE_ID`。完整端到端示例见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

### 文档转视频

利用 LLM + 多模态能力把长文档自动加工为带图、带语音、带字幕的视频，端到端流水线：

1. **文档切片**：LLM 总结文档并生成分段标题。
2. **生成演示文稿**：组合标题、正文、配图渲染为幻灯片（Marp）。
3. **生成语音与字幕**：多模态模型 TTS + 时长对齐生成字幕。
4. **生成视频**：FFmpeg 把幻灯片剪辑成视频并嵌入音频与字幕。

依赖工具：FFmpeg、Marp（macOS `brew`/Windows conda+npm 均可）。配套完整代码包与示例见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型接入

百炼把多家厂商的旗舰模型托管在统一网关，调用方式**统一为两套接口**：

- **OpenAI 兼容模式**：`base_url = https://dashscope.aliyuncs.com/compatible-mode/v1`，沿用 OpenAI SDK；非标参数（如 `enable_thinking`）通过 Python 的 `extra_body` 或 Node.js 的顶层字段透传，`reasoning_effort` 是 OpenAI 标准参数，可直接顶层传入。
- **DashScope 原生**：HTTP 走 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（纯文本）或 `.../multimodal-generation/generation`（多模态）；DashScope SDK 调用无需手动配 `base_url`。

只需把 `model` 字段切换为对应模型名即可复用同一份业务代码：

| 厂商 / 系列 | 代表模型 | 接入文档 |
| --- | --- | --- |
| DeepSeek（官方旗舰） | `deepseek-v4-pro`，支持 `enable_thinking` 切换思考/非思考 | [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) |
| DeepSeek（万擎部署） | 同名模型，万擎稳定渠道 | [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md) |
| DeepSeek（硅基流动） | 硅基流动托管的 DeepSeek 系列 | [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) |
| Kimi（月之暗面官方） | `kimi-k2-thinking`、`kimi-k2.5`、`kimi-k2.6` | [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) |
| Kimi（百炼托管） | 多地域：华北2 / 美国弗吉尼亚 / 德国法兰克福 | [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md) |
| GLM（百炼托管） | `glm-5.1`，支持 `enable_thinking` | [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md) |
| GLM（智谱官方渠道） | 智谱原厂部署 | [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) |
| MiniMax（百炼托管） | `MiniMax-M2.5`，仅中国内地地域 | [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md) |
| MiniMax（厂商直连） | 走 MiniMax 自家渠道 | [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md) |
| MiMo（小米） | 小米 MiMo 系列 | [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md) |
| Stepfun（阶跃星辰） | Step 系列 | [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md) |
| Vidu | 视频生成，配套专属 Prompt 公式 | [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md) |

> **注意**：同一模型可能由多条渠道提供（如 DeepSeek 有 `deepseek-api` / `deepseek-api-by-vanchin` / `siliconflow-deepseek-api` 三套接入文档；Kimi、GLM、MiniMax 也存在"百炼托管"与"厂商直连"两种入口），不同渠道的 SLA、计费与 API 兼容性可能不同——以**最新文档的模型名与 base_url 为准**，文档之间的实例名差异（如 `deepseek-v4-pro`、`glm-5.1`、`MiniMax-M2.5`）请以控制台「模型广场」实际列出的版本为最终依据。

## 地域与端点约定

| 地域 | OpenAI 兼容 `base_url` | DashScope HTTP |
| --- | --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/api/v1/...` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` | `https://dashscope-us.aliyuncs.com/api/v1/...` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` | 同 host 下的 `/api/v1/...` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`（旧版 `dashscope-intl.aliyuncs.com` 即将下线，请尽快迁移） | 同 host 下的 `/api/v1/...` |

不同模型对地域的覆盖不同：例如 MiniMax 仅限中国内地，Kimi 支持北京 / 美国 / 德国三地域。接入前请以对应模型文档为准。

## 使用约束与常见陷阱

- **API Key**：所有用例都要求先 [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量（推荐 `DASHSCOPE_API_KEY`），避免硬编码。
- **`enable_thinking` 与 SDK 差异**：DeepSeek、GLM、Kimi 等"思考型"模型的 `enable_thinking` 不是 OpenAI 标准字段——Python 必须放 `extra_body`，Node.js 才可作为顶层字段；混用会导致参数被静默丢弃。
- **流式响应**：使用 `stream=True` 时建议同步开启 `stream_options={"include_usage": True}`，否则无法在末包获得 Token 用量。
- **限流叠加缓存**：显式缓存只能降低 Token 成本，不会降低 RPM；高 QPS 场景仍需配合客户端流控策略。
- **自定义模型必须先部署**：调优产物在未部署到独占实例前既不能被推理调用，也不能进入评测任务。
- **Vidu / 万相 Prompt 不通用**：万相系列的"声音公式 / 多镜头公式"是 `wan2.5+` 专属，套用到 Vidu 模型会被忽略；接入 Vidu 时请使用其专属 Prompt 规范。

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



