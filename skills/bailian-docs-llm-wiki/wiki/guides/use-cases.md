# use cases

本页汇总阿里云百炼平台的常见使用场景与最佳实践，覆盖 Prompt 工程、多模态生成、RAG 应用、自定义模型调优、限流与缓存优化，以及 DeepSeek、Kimi、GLM、MiniMax、MiMo、Stepfun 等第三方模型的接入。文档按"调优与生成—架构与性能—模型接入"三个层次组织，帮助开发者快速定位所需能力。

## Prompt 工程

### 文生文 Prompt

设计 Prompt 是发挥 LLM 能力的最重要一步。描述越清晰、具体、无歧义，模型表现越贴近预期。推荐使用 Prompt 框架规范化结构，详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

框架包含六个要素：

- **背景**：任务相关的背景信息，保证生成内容与话题高度相关。
- **目的**：期望 LLM 完成的具体任务，设定清晰精确的目标指令。
- **风格**：指定写作风格，如某类专家或具体名人的风格。
- **语气**：正式、诙谐、温馨、关怀等，适配不同场景。
- **受众**：面向的读者群体（专业人士、入门学习者等），调整语言与内容深度。
- **输出**：规定输出形式，如列表、JSON、专业分析报告等。

百炼控制台提供 **Prompt 自动优化工具**，可对输入提示进行自动扩写和细节添加，建议先经优化工具改进后再应用其他技巧。该功能按模型推理费用计费。

### 文生图 Prompt

文生图模型（万相-文生图 V1/V2）有两个与提示词相关的参数：

- `prompt`：正向提示词，描述所需生成的图片，支持中英文。
- `negative_prompt`：反向提示词，描述不希望出现的内容。

文生图 V2 还支持 `prompt_extend`（默认 `true`），开启大模型智能改写 [prompt](prompt.md)。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

两种提示词公式：

- **基础公式**（面向新用户）：`提示词 = 主体 + 场景 + 风格`。
- **进阶公式**（面向有经验用户）：`提示词 = 主体（主体描述）+ 场景（场景描述）+ 风格（定义风格）+ 镜头语言 + 氛围词 + 细节修饰`。

提示词词典覆盖五大要素：景别（特写/近景/中景/远景）、视角（平视/俯视/仰视）、镜头拍摄类型、风格（写实/水彩/漫画等）、光线。

### 文生视频 / 图生视频 Prompt

万相视频生成提供多种提示词公式，适用范围包括文生视频、图生视频-首帧生视频、图生视频-首尾帧生视频、参考生视频 API。

- **基础公式**：`提示词 = 主体 + 场景 + 运动`。
- **进阶公式**：`提示词 = 主体（主体描述）+ 场景（场景描述）+ 运动（运动描述）+ 美学控制 + 风格化`。
- **图生视频公式**：图像已确定主体、场景与风格，提示词主要描述 `运动 + 运镜`。

万相 2.7/2.6/2.5 基于原生音频能力新增 **声音公式**，可描述人声（角色说话内容 + 情绪 + 语调 + 语速 + 音色 + 口音）、音效（音源材质 + 行为 + 环境音）、背景音乐（配乐 + 风格）。万相 2.7/2.6 支持 **多镜头公式**（总体描述 + 镜头序号 + 时间戳 + 分镜内容）和 **参考生视频公式**（参考指代 + 动作 + 场景 + 台词 + 背景音乐）。

### Vidu 视频生成 Prompt

Vidu 提示词遵循 `主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介` 结构。调优原则：避免主体过多/复杂、避免模糊术语、使用口语化措辞、保持描述丰富准确完整。详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

提示词词典覆盖：主体动态（大/中/小动态）、运镜控制（左移/右移/升/降/推/拉/固定、延时/微距/第一人称/航拍）、景别、视角、构图、画面风格（2D 动漫/3D 渲染/写实/水墨/线稿/像素/油画）、导演风格、特效（爆炸/旋涡/粉碎/扭曲/融化/石化）、氛围（快乐/悲伤/宁静/紧张/温馨浪漫）。

进阶能力包括参考生视频（保持角色与物体多视角一致性，支持多主体交互与特征融合）和 AI 漫剧提示词案例（风格/景别/机位/构图/运镜 + 画面描述 + 图片强调三段式结构）。

## 多模态与 RAG

### 基于 LlamaIndex 构建 RAG 应用

通过 DashScopeCloudIndex 在 LlamaIndex 中使用百炼检索增强服务。前提条件：获取并配置 API Key、开通知识库服务、（可选）获取[业务空间](../concepts/workspace.md) ID；Python 版本要求 ≥3.8 且 ≤3.12。

安装依赖：

```
pip install llama-index-core
pip install llama-index-llms-dashscope
pip install llama-index-indices-managed-dashscope
```

核心流程：

1. **文件解析**：使用 `DashScopeParse`（支持在线解析 .doc/.docx/.pdf，单文件 ≤100M、页数 ≤1000）解析一个或多个文件，或配合 `SimpleDirectoryReader` 解析文件夹。
2. **创建知识库**：`DashScopeCloudIndex.from_documents(documents, "my_first_index")`。
3. **读取知识库**：`DashScopeCloudIndex("my_first_index")` 初始化已创建的知识库。
4. **获得 retriever**：`index.as_retriever()` 或 `DashScopeCloudRetriever("my_first_index")`。
5. **获得 query engine**：配合 `DashScope` LLM（如 `DashScopeGenerationModels.QWEN_MAX`）调用 `index.as_query_engine(llm=dashscope_llm)`。
6. **增删文档**：`index._insert(documents)` 新增、`index.delete_ref_doc([doc_id])` 删除。

### 借助大模型将文档转换为视频

依托 LLM 与多模态技术将文档自动转换为视频（包含图文、语音、字幕）。方案流程为：文档切片（总结标题并分段）→ 生成演示文稿（整合标题/正文/图片）→ 生成讲解语音与字幕（文字转音频并按时长生成字幕）→ 生成视频（剪辑图片并嵌入音频与字幕）。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

准备工作依赖 FFmpeg、Marp（演示文稿制作）和浏览器引擎渲染。提供完整代码包可快速体验。

## 自定义模型调优

自定义大模型基于通用 LLM，通过微调和训练适应特定领域或任务。价值在于：提高特定领域准确性、增强模型适用性、节约开发时间和成本、增强品牌与用户体验。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

### 创建流程

涉及三个主要步骤与三个辅助步骤：

1. **模型调优阶段**：模型学习训练数据的语言特征。前置训练数据准备（数据收集、清洗、数据集划分）。按"训练新模型"向导配置超参数（学习率、迭代次数等），平台自动训练。
2. **模型部署阶段**：将自定义模型部署到独占实例后才能调用或评测。按"部署新模型"向导配置规格与资源，确认预估价格后自动部署。
3. **模型评测阶段**：按"创建评测任务"向导配置评测方式、数据和维度，平台自动完成评测。

> **注意**：完成调优的模型**必须部署后才能调用和评测**，需先完成部署再评测。若评测结果不满意，可调整训练策略（换基础模型、扩充数据样本、调超参数）重复整个流程。

### 训练数据准备

- **数据收集**：来源多样化、质量控制、平衡性考量。编排成 `Prompt-Completion` 格式，建议至少 500 条训练数据。注意文本分割（聚焦单一主题）与脱敏处理。
- **数据上传**：在"数据管理"页面新增数据集（训练集由 Prompt+Completion 组成，评测集仅含 Prompt；支持多版本管理）。单次最多导入 10 个文件。

## 架构与性能

### 限流应对最佳实践

百炼 API 按主账号维度、模型独立计算限流，触发后通常 1 分钟内恢复。三种限流规则：分钟级配额（RPM/TPM）、瞬时频率（RPS/TPS）、增速限制（Traffic Burst）。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

错误码与推荐策略：

| 错误码（DashScope / OpenAI） | 触发维度 | 推荐策略 |
| --- | --- | --- |
| `Throttling.RateQuota` / `limit_requests` | RPM 超限 | 令牌桶控制请求配额 |
| 同上 | RPS 超限 | 并发信号量或平滑限速器 |
| `Throttling.AllocationQuota` / `insufficient_quota` | TPM 超限 | 双重令牌桶（同时限制 RPM 和 TPM） |
| 同上 | TPS 超限 | 并发信号量或平滑限速器 |
| `Throttling.BurstRate` / `limit_burst_rate` | Traffic Burst | 服务端排队等待（首选）；或令牌桶设 `initial_tokens=0`；或平滑限速器 |

三类方案（按改动成本从低到高）：

- **平台配置方案**：
  - **服务端排队等待**（推荐首选，仅适用 BurstRate）：请求头添加 `X-DashScope-Wait-Timeout`（建议 3~120 秒；值为 0 不排队）。非流式请求超时 = 原超时 + Wait-Timeout；流式请求超时 > Wait-Timeout。
  - **提升限流额度**：控制台临时提升额度，立即生效（支持华北2北京和新加坡地域）。
  - **PTU**：预置吞吐单元提供独立预留专享算力，避免公共池竞争；未满负荷也持续计费。
  - **Batch API**：异步批处理，适用于无实时性要求的数据清洗、离线分析任务。
- **客户端流控策略**：基础重试 → 令牌桶/并发信号量 → 平滑限速器/双重令牌桶 → 自适应拥塞控制。
- **架构兜底方案**：模型降级（Fallback）、基于消息队列（MQ）的削峰填谷。

### 显式缓存最佳实践

显式缓存通过在请求中添加缓存标记，确保相同输入确定性命中缓存（100% 命中，不受后端调度影响），显著降低成本和延迟。首次写入缓存产生标准价格 25% 的额外开销，后续命中节省 90% 成本；只要发生至少一次命中，总体成本即低于不使用缓存的方案。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

适用场景：需要稳定命中缓存的业务、高频复用相同 Prompt、工业级 Agent 的长上下文管理（对关键上下文片段标记并固定复用）。

常用 Agent 和 Coding 工具可通过 Anthropic 协议接入百炼，原生支持显式缓存：

- **Claude Code**：v2.x 起默认在 system、env、最近 user message 三处携带 `cache_control`。接入端点：按量计费 `https://dashscope.aliyuncs.com/apps/anthropic`；Token Plan 团队版 `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`；Coding Plan `https://coding.dashscope.aliyuncs.com/apps/anthropic`。可用 `--exclude-dynamic-system-prompt-sections` 提升跨会话命中率，`DISABLE_PROMPT_CACHING=1` 关闭。
- **OpenCode**：通过 `@ai-sdk/anthropic` 接入，默认对 system 与最近非 system 消息注入 `cache_control`（`baseURL` 末尾需带 `/v1`）。
- **OpenClaw**：走 Anthropic 兼容端点默认对每次请求注入 `cache_control`，可用 `<!-- OPENCLAW_CACHE_BOUNDARY -->` 标记自定义缓存边界。
- **Hermes**：通过 `hermes config set` 配置 base URL。

## 第三方模型接入

百炼支持通过 [OpenAI 兼容接口](../concepts/openai-compatible.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用多家第三方模型。各模型统一通过 `DASHSCOPE_API_KEY` 鉴权，OpenAI 兼容 Base URL 通常为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。多数模型支持 `enable_thinking` 参数切换思考/非思考模式（非 OpenAI 标准参数，Python SDK 走 `extra_body`，Node.js SDK 作为顶层参数）；思考模式下推理过程通过 `reasoning_content` 字段返回。

### 模型总览

| 模型族 | 供应商 | 模型示例 | 特性 |
| --- | --- | --- | --- |
| DeepSeek | 硅基流动 | `siliconflow/deepseek-v3.2` | 支持更长上下文；仅华北2（北京） |
| DeepSeek | 阿里云百炼 | `deepseek-v4-pro` | 限流更宽松，支持联网搜索与上下文缓存；多地域 |
| DeepSeek | 快手万擎 | `vanchin/deepseek-v4-pro` | 仅华北2（北京） |
| Kimi | 月之暗面 | `kimi/kimi-k2.7-code-highspeed`、`kimi/kimi-k2.7-code`、`kimi/kimi-k2.6`、`kimi/kimi-k2.5` | 支持文本/图像/视频；k2.7-code 为仅思考模型；k2.6/k2.5 可控思考模式；支持 `preserve_thinking` 多轮传递 |
| Kimi | 百炼部署 | `kimi-k2-thinking` 等 | 多地域；部分模型 2026/7/9 下架 |
| GLM | 智谱直供 | `ZHIPU/GLM-5.2` | 支持 1M 上下文；`reasoning_effort` 控制思考深度（max/high/none） |
| GLM | 百炼部署 | `glm-4.6`、`glm-4.7` | 多地域；2026/7/9 下架 |
| MiniMax | 稀宇科技直供 | `MiniMax/MiniMax-M2.7` | 仅华北2（北京） |
| MiniMax | 百炼部署 | `MiniMax-M2.5` | 仅中国内地地域；MiniMax-M2.1 于 2026/7/9 下架 |
| MiMo | 小米直供 | `xiaomi/mimo-v2.5-pro` | 混合推理模型，默认开启思考模式；仅华北2（北京） |
| Step | 阶跃星辰直供 | `stepfun/step-3.7-flash` | 多模态推理模型，默认关闭思考模式；`reasoning_effort`（low/medium/high） |

> **注意**：DeepSeek（deepseek-v3/v3.1/v3.2/v3.2-exp/r1/r1-0528/distill 系列）、Moonshot-Kimi-K2-Instruct、kimi-k2-thinking、glm-4.6、glm-4.7、MiniMax-M2.1 将于 **2026 年 7 月 9 日下架**。官方推荐转用 `qwen3.7-plus`、`qwen3.7-max`、`qwen3.6-flash`。

### 地域与服务接入

- **仅华北2（北京）**：硅基流动 DeepSeek、快手万擎 DeepSeek、月之暗面 Kimi、智谱直供 GLM、稀宇 MiniMax、小米 MiMo、阶跃星辰 Step。
- **多地域**（华北2北京、美国弗吉尼亚、德国法兰克福、新加坡、日本东京）：百炼部署的 DeepSeek、Kimi、GLM。新加坡/德国/日本等地域部分接入地址需替换 `{WorkspaceId}` 为真实[业务空间](../concepts/workspace.md) ID。
- **新加坡专属域名**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，性能与稳定性更优，建议从 `https://dashscope-intl.aliyuncs.com` 迁移。

### 接入示例

以 `xiaomi/mimo-v2.5-pro`（默认开启思考模式）为例：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="xiaomi/mimo-v2.5-pro",
    messages=[{"role": "user", "content": "1+1 等于多少？"}],
    stream=True,
    stream_options={"include_usage": True},
)
```

如需关闭思考模式，显式传入 `extra_body={"enable_thinking": False}`。各模型的开通步骤均为：百炼控制台模型广场搜索对应模型卡片 → 单击立即开通 → 确认授权。

## 注意事项

- 第三方直供模型（硅基流动、快手万擎、月之暗面、智谱、稀宇、小米、阶跃星辰）地域受限，需使用对应地域的 API Key。
- `enable_thinking` 为非 OpenAI 标准参数，调用方式因 SDK 而异：Python SDK 走 `extra_body`，Node.js SDK 作为顶层参数。`reasoning_effort` 是 OpenAI 标准参数，可直接作为顶层参数传入。
- DeepSeek 硅基流动供应商支持更长上下文；阿里云百炼供应商限流更宽松且支持联网搜索与上下文缓存——两者按业务需求选择。
- Kimi 多模态模型走 DashScope 协议时使用 `multimodal-generation/generation` 端点，纯文本模型走 `text-generation/generation` 端点。
- 限流问题应优先评估平台配置方案（服务端排队等待仅需加一个请求头），再考虑客户端流控或架构兜底。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


