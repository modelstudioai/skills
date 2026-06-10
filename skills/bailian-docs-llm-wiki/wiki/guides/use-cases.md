# use cases

阿里云百炼平台的典型使用场景覆盖提示词工程、[检索增强生成（RAG）](../concepts/rag.md)、自定义模型调优、显式缓存、文档转视频、限流应对、第三方模型接入等多个方向。本文汇总平台核心 use cases 的入口、关键参数与注意事项，帮助开发者按业务需求快速选型。

## 提示词工程

提示词（Prompt）是与模型交互的核心输入，撰写质量直接影响生成效果。百炼针对文生文、文生图、文生视频三类模态分别给出了结构化的提示词公式和词典。

### 文生文 Prompt

面向大语言模型（LLM）的提示词设计强调**清晰、具体、无歧义**。推荐使用 Prompt 框架组织输入，包含六个要素：

- **背景**：与任务相关的环境信息
- **目的**：明确要完成的任务
- **风格**：指定写作风格（如某类专家的风格）
- **语气**：正式、诙谐、关怀等
- **受众**：面向专业人士、初学者或儿童等
- **输出**：规定返回形式（列表、JSON、报告等）

百炼控制台 **[Prompt](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)** 页面提供**自动优化**工具，可对输入提示词进行自动扩写和细节添加（按模型推理 Token 计费）。建议先用优化工具扩写，再结合框架精修。

详细方法与示例参见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt

万相（Wanx）文生图 V1/V2 的提示词由 `prompt`（正向）和 `negative_prompt`（反向）组成，V2 还支持 `prompt_extend` 开启大模型智能改写。

提示词公式分为两级：

- **基础公式**：主体 + 场景 + 风格 —— 适合快速灵感探索
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰 —— 提升画面质感与细节

配合**提示词词典**（景别、视角、镜头拍摄类型、风格、光线）可精准控制画面。

详细示例参见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频 / 图生视频 Prompt

万相视频系列提供了更丰富的结构化公式，按场景选择：

| 场景 | 公式 |
| --- | --- |
| 基础视频 | 主体 + 场景 + 运动 |
| 进阶视频 | 主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化 |
| 图生视频 | 运动 + 运镜 |
| 带声音（wan2.5/2.6/2.7） | 主体 + 场景 + 运动 + 声音描述（人声 / 音效 / BGM） |
| 多镜头（wan2.6/2.7） | 总体描述 + 镜头序号 + 时间戳 + 分镜内容 |
| 参考生视频（wan2.7） | 参考指代（"图n" / "视频n"）+ 动作 + 场景 + 台词 + BGM |

> **注意**：wan2.7 不再支持 `shot_type` 参数指定单/多镜头，而是由模型结合提示词发挥。要控制一镜到底，请在提示词中明确写"生成单镜头"（英文为 "Generate single shot."）。

Vidu 等第三方视频模型也提供独立的提示词规范，详见各模型的 Prompt 指南。

完整公式与示例参见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

## [检索增强生成（RAG）](../concepts/rag.md)

百炼提供托管式知识库服务，可结合 LlamaIndex 等框架快速构建 RAG 应用。核心流程：

1. **文件解析**：使用 `DashScopeParse` 解析 `.doc` / `.docx` / `.pdf`（单文件 ≤100MB、≤1000 页）
2. **创建知识库**：通过 `DashScopeCloudIndex.from_documents()` 一键建库
3. **检索与生成**：从 index 获得 `retriever` 或 `query_engine`，配合 `DashScope` LLM 完成问答
4. **增量维护**：`index._insert(documents)` 新增、`index.delete_ref_doc([doc_id])` 删除

前提条件：已获取 API Key 并配置到环境变量，且已在百炼控制台开通知识库服务。支持多[业务空间](../concepts/workspace.md)隔离（通过 `DASHSCOPE_WORKSPACE_ID` 指定）。

详细代码示例参见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优、部署与评测

当通用模型无法满足垂直领域需求时，可通过"调优 → 部署 → 评测"三段式流程构建自定义模型：

1. **训练数据准备**：收集业务数据，整理为 Prompt-Completion 格式（建议 ≥500 条）；通过数据管理页面上传训练集、评测集；使用平台提供的清洗与增强工具提升质量
2. **模型调优**：选择预置基座模型，配置学习率、迭代次数等超参数，平台自动训练
3. **模型部署**：部署到独占实例，按规格计费；完成部署后才能调用和评测
4. **模型评测**：选择评测方式、数据与维度，平台自动出分；不满意可调整策略再迭代

> **注意**：完成调优的模型**必须先部署**，才能被调用或评测，这与通用模型的即时可用不同。

完整流程与最佳实践参见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 显式缓存

显式缓存通过在请求中添加 `cache_control` 标记，确保相同输入确定性命中缓存。首次写入缓存仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本，只要发生至少一次命中，总体成本即低于不使用缓存。

**典型场景**：

- 高频复用相同 Prompt（如模板化调用）
- 工业级 Agent 的长上下文管理（固定 system [prompt](prompt.md)、recap 等关键片段）
- 对缓存命中率有明确 SLA 要求的业务

**原生支持显式缓存的工具**：Claude Code、OpenCode、OpenClaw、Hermes。这些工具通过 Anthropic 协议接入百炼后，会自动在 system 与最近 user message 上注入 `cache_control`。

**接入要点**：

- 按量计费端点：`https://dashscope.aliyuncs.com/apps/anthropic`
- Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- Coding Plan：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

Claude Code 跨会话命中率可通过 `claude --exclude-dynamic-system-prompt-sections` 提升；OpenClaw 可在 system [prompt](prompt.md) 中插入 `<!-- OPENCLAW_CACHE_BOUNDARY -->` 标记划分稳定前缀与动态后缀。

详细配置参见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

## 文档转视频

百炼提供完整的"文档 → 视频"流水线，结合 LLM、TTS、Marp、FFmpeg 等工具，把文字材料自动生成包含图文、语音、字幕的演示视频：

1. **文档切片**：大模型总结标题并划分段落
2. **生成演示文稿**：整合标题、正文、图片，使用 Marp 渲染幻灯片图
3. **生成语音与字幕**：多模态大模型 TTS + 按时长对齐字幕
4. **合成视频**：FFmpeg 拼接图片、嵌入音频与字幕

环境依赖：FFmpeg、Marp、Python（含 `dashscope`、`pyppeteer`、`moviepy` 等）以及浏览器引擎（用于 Marp 渲染）。

完整代码与教程参见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 限流应对

百炼 API 按**主账号 + 模型**维度限流，包含三类规则：

- **分钟级配额**：RPM（请求数/分钟）、TPM（Token/分钟）
- **瞬时频率**：RPS / TPS
- **增速限制**（Traffic Burst）：短时间激增触发，阈值动态调整

按改动成本由低到高，有三层应对方案：

### 平台配置方案（低改动）

| 方案 | 适用 | 说明 |
| --- | --- | --- |
| 服务端排队等待 | 增速/突发限流 | 请求头加 `X-DashScope-Wait-Timeout: 30`，服务端排队重试，显著提升突发成功率 |
| 提升限流额度 | RPM/TPM 不足 | 控制台提交后立即生效（北京、新加坡地域） |
| PTU 预置吞吐 | 确定性高吞吐 SLA | 独立预留算力，避免资源竞争；未满负荷也持续计费 |
| Batch API | 离线批处理 | 数据清洗、分析等无实时性要求场景 |

### 客户端流控策略（改代码）

按工程复杂度递进：基础重试 → 令牌桶/并发信号量 → 平滑限速器 → 自适应拥塞控制。

### 架构兜底（改架构）

- **模型降级（Fallback）**：主模型不可用时切到备用模型
- **消息队列削峰填谷**：用 MQ 缓冲突发流量

> **注意**：服务端排队等待需相应调大客户端超时——非流式 `超时 = 原超时 + Wait-Timeout`，流式只需保证首包超时大于排队时间。

详细错误码诊断与策略推荐参见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 第三方模型接入

百炼作为聚合平台，除通义千问系列外，还通过直供或第三方供应商接入了 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun、Vidu 等主流模型。所有模型均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 调用，Base URL 统一为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。

### 模型系列与调用约定

| 模型系列 | 供应商 | 典型模型名 | 关键能力 |
| --- | --- | --- | --- |
| DeepSeek | 阿里云百炼 / 硅基流动 / 快手万擎 | `deepseek-v4-pro`、`siliconflow/deepseek-v3.2`、`vanchin/deepseek-v4-pro` | 思考模式（`enable_thinking`）、编程、数学 |
| Kimi | 月之暗面直供 / 阿里云百炼 | `kimi/kimi-k2.6`、`kimi-k2.5` | 多模态（图像/视频）、思考模式、`preserve_thinking` 跨轮传递 |
| GLM | 智谱直供 / 阿里云百炼 | `glm-4`、`glm-zhipu/*` | 通用对话、工具调用 |
| MiniMax | MiniMax 直供 / 阿里云百炼 | `minimax/*` | 长上下文、语音 |
| MiMo | 小米 | `mimo/*` | 推理、多模态 |
| Stepfun | 阶跃星辰 | `stepfun/*` | 通用对话 |
| Vidu | 生数科技 | `vidu/*` | 视频生成，独立 Prompt 规范 |

### 通用接入流程

1. **开通服务**：在百炼控制台模型广场搜索对应模型卡片，点击"立即开通"并确认授权
2. **获取 API Key**：部分模型仅限特定地域（如 DeepSeek 硅基流动版仅限北京地域），需使用对应地域的 API Key
3. **调用模型**：使用 OpenAI SDK 或 DashScope SDK，`base_url` 指向百炼兼容端点

### 思考模式（DeepSeek / Kimi 等）

思考模型会额外输出 `reasoning_content` 字段，包含推理链。开启方式：

- Python OpenAI SDK：`extra_body={"enable_thinking": True}`
- Node.js OpenAI SDK：顶层参数 `enable_thinking: true`
- HTTP：请求体中直接设置 `"enable_thinking": true`

[流式输出](../concepts/streaming-output.md)时需分别处理 `delta.reasoning_content`（思考）与 `delta.content`（回复）。

> **注意**：各供应商对同一系列模型的支持能力可能不同（例如硅基流动版 DeepSeek 支持更长上下文，百炼直供版支持联网搜索与上下文缓存）。选型时需对照各文档确认。

## 关键参数速查

| 参数 | 适用模态 | 说明 |
| --- | --- | --- |
| `prompt` / `negative_prompt` | 文生图 / 文生视频 | 正向 / 反向提示词 |
| `prompt_extend` | 文生图 V2 | 是否开启智能改写，默认 true |
| `enable_thinking` | 文本推理模型 | 开启思考模式，返回 `reasoning_content` |
| `preserve_thinking` | Kimi | 多轮对话中传递思考过程 |
| `X-DashScope-Wait-Timeout` | 所有 API | 突发限流时服务端排队等待秒数 |
| `cache_control` | Anthropic 协议 | 显式缓存标记，工具自动注入 |
| `shot_type` | 旧版万相视频 | 已废弃，wan2.7 起由提示词控制 |

## 限制与注意事项

- **提示词语言**：万相文生图、视频模型对中英文提示词均支持，但效果可能存在差异，建议优先使用中文
- **文件尺寸**：RAG 单文件 ≤100MB、≤1000 页；图片理解仅支持公网 URL，不支持 Base64
- **地域限制**：部分第三方模型仅限华北2（北京）地域，调用前确认 API Key 地域
- **计费差异**：显式缓存写入按标准价 25% 计费，命中节省 90%；PTU 为预留资源，闲置也计费；Prompt 优化工具按推理 Token 计费
- **思考模式 Token**：思考过程消耗的 Token 计入输出，需纳入成本与限流评估
- **流式超时**：使用服务端排队等待时，流式与非流式的超时调整策略不同，参见限流章节

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


