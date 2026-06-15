# use cases

百炼平台提供了丰富的使用场景指南，涵盖 [Prompt 工程](../concepts/prompt-engineering.md)、多模态内容生成、RAG 应用构建、模型微调、成本优化以及第三方模型集成等方面。本文汇总了平台核心使用场景的最佳实践与操作指引，帮助开发者快速上手并高效利用百炼的各项能力。

## [Prompt 工程](../concepts/prompt-engineering.md)指南

百炼为文本、图像、视频三大生成场景分别提供了专门的 Prompt 指南。

### 文生文 Prompt

设计有效的 Prompt 是发挥大模型能力的关键。核心原则包括：

- **清晰具体**：任务描述越明确、无歧义，模型表现越好
- **使用 Prompt 框架**：按"背景 → 目的 → 风格 → 语气 → 受众 → 输出"六要素结构化组织 Prompt
- **少样本示例（Few-shot）**：在 Prompt 中提供输入-输出示例，引导模型理解任务格式
- **思维链（Chain-of-Thought）**：对复杂推理任务，引导模型逐步思考再给出结论
- **限制输出格式**：明确指定 JSON、列表、表格等输出形式

百炼控制台还提供了 Prompt 一键优化工具，可在 Prompt 页面点击"自动优化"进行扩写改进。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt

文生图模型（万相系列）的关键参数：

| 参数 | 说明 |
|------|------|
| `prompt` | 正向提示词，描述期望生成的图像内容 |
| `negative_prompt` | 反向提示词，描述不希望出现的内容 |
| `prompt_extend` | V2 专有，是否开启大模型智能改写（默认 true） |

**基础公式**：主体 + 场景 + 风格

**进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

提示词中可组合景别（特写/近景/中景/远景）、视角（平视/俯视/仰视）、拍摄类型和光线效果来精细控制画面。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频/图生视频 Prompt

视频生成适用于万相系列的文生视频、图生视频（首帧/首尾帧）、参考生视频等接口。

**基础公式**：主体 + 场景 + 运动

**进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化

**图生视频公式**：运动 + 运镜（图像已确定主体和风格，重点描述动态过程）

wan2.5 及以上版本还支持声音描述，可通过 `prompt_extend_with_audio` 参数开启音频大模型对声音提示词的智能改写。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

## RAG 应用构建

百炼提供[检索增强生成](../concepts/rag.md)（RAG）服务，可通过 LlamaIndex 框架快速集成。核心流程：

1. **文档解析**：使用 `DashScopeParse` 解析 PDF/DOC/DOCX 文件（单文件 100MB 以内，1000 页以内）
2. **创建知识库索引**：通过 `DashScopeCloudIndex` 上传解析后的文档到百炼知识库
3. **检索与生成**：使用 `DashScopeCloudRetriever` 检索相关文档，结合 LLM 生成回答

前提条件包括获取 API Key、开通知识库服务、安装 `llama-index-indices-managed-dashscope` 等依赖包（Python >= 3.8 且 <= 3.12）。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优

当通用模型无法满足特定业务需求时，可通过百炼的模型微调功能创建自定义模型。整体流程为：

1. **训练数据准备**：收集业务数据，编排为"Prompt-Completion"格式，建议至少 500 条
2. **模型调优**：选择预置模型，配置学习率、迭代次数等超参数，平台自动训练
3. **[模型部署](../concepts/model-deployment.md)**：将训练完成的[模型部署](../concepts/model-deployment.md)到独占实例
4. **模型评测**：通过平台内置评测功能验证效果，不满意可调整策略重新训练

数据准备时需注意来源多样化、质量控制和类别平衡，同时做好脱敏处理。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 成本与性能优化

### 显式缓存

显式缓存通过在请求中添加 `cache_control` 标记，确保相同输入内容确定性命中缓存。适用场景：

- 高频复用相同 Prompt（首次写入开销为标准价格 25%，后续命中节省 90%）
- Agent 长上下文管理（对关键上下文片段标记复用）
- 需要 100% 确定性命中的业务场景

主流工具的支持情况：

| 工具 | 缓存支持 |
|------|----------|
| Claude Code | v2.x 起默认携带 `cache_control`，无需额外配置 |
| Open Code | 通过 `@ai-sdk/anthropic` 接入时默认注入 |
| Cline / Roo Code | 原生支持，配置 Anthropic 端点即可 |

详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

### 限流应对

百炼 API 按请求数（RPM/RPS）和 Token 用量（TPM/TPS）限流，还有增速限制（Traffic Burst）。应对方案按改动成本递进：

- **平台配置**（低成本）：服务端排队等待（加 `X-DashScope-WaitTimeout` 请求头）、提升限流额度、PTU 预留吞吐、Batch API
- **客户端流控**（改代码）：指数退避重试 → 令牌桶/并发信号量 → 双重令牌桶/平滑限速器 → 自适应拥塞控制
- **架构兜底**（改架构）：模型降级 Fallback、消息队列削峰填谷

遇到 `429` 错误时，可根据错误码（`Throttling.RateQuota` / `Throttling.AllocationQuota` / `Throttling.BurstRate`）定位原因并选择对应策略。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 文档转视频

百炼支持借助大模型将文档自动转换为包含图文、语音、字幕的视频。方案流程：

1. **文档切片**：大模型总结标题，划分段落
2. **生成演示文稿**：整合标题、正文和图片生成幻灯片图像
3. **生成语音与字幕**：多模态模型将文字转为音频，自动生成字幕
4. **合成视频**：将演示文稿剪辑为视频并嵌入音频字幕

详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型集成

百炼平台除自有的通义千问系列外，还聚合了多家第三方模型供应商的推理服务。所有第三方模型均可通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 调用，统一使用百炼 API Key。

### 可用模型一览

| 模型系列 | 供应商 | 典型模型 | 特点 |
|----------|--------|----------|------|
| DeepSeek | 阿里云百炼部署 | deepseek-v4-pro | 编程、数学和通用任务表现出色，支持思考模式 |
| DeepSeek | 硅基流动直供 | siliconflow/deepseek-v3 | 支持更长上下文 |
| DeepSeek | 快手万擎直供 | vanchin/deepseek-v3 | 直供推理服务 |
| Kimi | 月之暗面直供 | moonshot-ai/kimi-k2 | 直供推理，支持思考模式 |
| Kimi | 阿里云百炼部署 | Moonshot-Kimi-K2-Instruct | 多地域支持 |
| GLM | 智谱直供 | zhipu/glm-4.9 | 支持更长回复长度 |
| GLM | 阿里云百炼部署 | glm-4.6 | 提供免费额度，阶梯计费 |
| MiniMax | 稀宇科技直供 | minimax/MiniMax-M2.5 | 直供推理服务 |
| MiniMax | 阿里云百炼部署 | MiniMax-M2.1 | 中国内地地域可用 |
| MiMo | 小米直供 | xiaomi/mimo-v2.5-pro | 混合推理模型，默认开启思考模式 |
| Step | 阶跃星辰直供 | stepfun/step-3.7-flash | 多模态推理，默认关闭思考模式 |
| Vidu | 第三方 | vidu 系列 | 视频生成，提供专用 Prompt 指南 |

> **注意**：部分模型计划下架，包括 deepseek-v3/r1 系列、Moonshot-Kimi-K2-Instruct、glm-4.6/4.7、MiniMax-M2.1 等，将于 2026 年 7 月 9 日下架。建议迁移至 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash。

### 通用接入方式

第三方模型的调用方式与百炼自有模型一致：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-dashscope-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="deepseek-v4-pro",  # 替换为目标模型名称
    messages=[{"role": "user", "content": "你好"}]
)
```

支持思考模式的模型（DeepSeek、Kimi、MiMo、Step 等）可通过 `enable_thinking` 参数切换，思考过程通过 `reasoning_content` 字段返回。

> **注意**：大部分第三方直供模型仅在华北2（北京）地域可用，需使用对应地域的 API Key。阿里云百炼自行部署的版本通常支持更多地域。

### Vidu 视频生成

Vidu 视频生成模型有独立的 Prompt 指南，公式为：主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介。支持通过镜头运动、光线、色彩分级等参数精细控制视频效果。详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

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





