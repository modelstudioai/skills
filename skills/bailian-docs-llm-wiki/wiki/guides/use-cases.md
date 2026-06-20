# use cases

阿里云百炼平台提供了丰富的使用场景和最佳实践，覆盖 [Prompt 工程](../concepts/prompt-engineering.md)、多模态内容生成、RAG 应用构建、自定义模型训练、API 调用优化以及第三方模型集成等方面。本文汇总了各类典型用例，帮助开发者快速找到适合自身业务的实践路径。

## [Prompt 工程](../concepts/prompt-engineering.md)指南

### 文生文 Prompt 设计

设计高质量的 Prompt 是充分发挥大模型能力的关键一步。核心原则包括：

- **清晰具体**：任务描述越清晰、无歧义，模型表现越能符合预期。
- **使用 Prompt 框架**：按照"背景 + 目的 + 风格 + 语气 + 受众 + 输出"六要素组织 Prompt，可显著提升模型输出的有效性。
- **Few-shot 示例**：提供少量示例让模型理解期望的输出格式和风格。
- **链式思考（CoT）**：引导模型逐步推理，在复杂逻辑任务中表现更优。

百炼还提供了 [Prompt 一键优化工具](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)，可对输入的 Prompt 进行自动扩写和细节添加。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt 设计

文生图模型通过 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）控制生成内容。适用于万相-文生图 V1/V2 模型。

- **基础公式**：`主体 + 场景 + 风格`，适合初次使用的新用户。
- **进阶公式**：`主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰`，可有效提升画面质感。
- **提示词词典**：涵盖景别（特写/近景/中景/远景）、视角（平视/俯视/仰视）、风格和光线等维度。

文生图 V2 还支持通过 `prompt_extend` 参数开启大模型智能改写，默认开启。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频与图生视频 Prompt 设计

适用于万相系列视频生成模型，包括文生视频、图生视频和参考生视频等模式。

- **基础公式**：`主体 + 场景 + 运动`。
- **进阶公式**：`主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化`。
- **图生视频公式**：`运动 + 运镜`，因为图像已经确定了主体和风格。
- **声音公式（wan2.7/wan2.6/wan2.5）**：支持人声、音效和背景音乐描述，实现声画同步。
- **多镜头公式（wan2.7/wan2.6）**：支持 `总体描述 + 镜头序号 + 时间戳 + 分镜内容` 生成连贯叙事视频。

详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 和 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## RAG 应用构建

基于 LlamaIndex 框架，开发者可以快速接入百炼的检索增强服务来构建 RAG 应用。核心流程包括：

1. **文件解析**：使用 `DashScopeParse` 解析 .doc、.docx、.pdf 文件（单文件 100M/1000 页以内）。
2. **创建知识库**：通过 `DashScopeCloudIndex.from_documents()` 创建知识库。
3. **检索与查询**：通过 `index.as_retriever()` 获取检索器，通过 `index.as_query_engine()` 获取查询引擎。
4. **文档管理**：支持向知识库新增或删除文档。

需要安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope` 等包。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优、部署与评测

当通用模型无法满足特定业务需求时，可通过自定义模型来提升领域准确性。完整流程为：

1. **训练数据准备**：收集业务数据并编排为 Prompt-Completion 格式，建议至少 500 条训练数据。
2. **模型调优**：在百炼控制台配置训练超参数，平台自动完成训练。
3. **模型部署**：将训练好的模型部署到独占实例上。
4. **模型评测**：配置评测任务验证模型效果。如不满意可调整训练策略重复整个流程。

> **注意**：完成调优的模型必须部署后才能调用和评测。

详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 大模型文档转视频

百炼支持借助大模型将文档自动转换为包含图文、语音、字幕的视频。方案流程为：

1. **文档切片**：利用大模型总结标题并划分段落。
2. **生成演示文稿**：整合标题、正文、图片等生成演示文稿图片。
3. **生成讲解语音与字幕**：通过多模态大模型将文字转换为音频并生成字幕。
4. **生成视频**：将演示文稿剪辑为视频，嵌入音频和字幕。

依赖工具包括 FFmpeg 和 Marp CLI。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## API 调用优化

### 限流应对

百炼 API 按请求数（RPM/RPS）和 Token 用量（TPM/TPS）限流，还有增速限制（Traffic Burst）。按改动成本从低到高的应对方案：

**平台配置方案（低成本）**：
- **服务端排队等待**（推荐首选）：在请求头添加 `X-DashScope-Wait-Timeout`，服务端在指定时间内排队重试，仅适用于 Traffic Burst 限流。
- **提升限流额度**：在控制台直接提升临时限流额度，立即生效。
- **PTU（预置吞吐单元）**：提供独立预留的专享算力，保障实时高吞吐。
- **Batch API**：适用于无实时性要求的离线任务。

**客户端流控策略**：从基础重试到令牌桶、平滑限速器、自适应拥塞控制，按工程复杂度递进。

**架构兜底方案**：包括模型降级（Fallback）和基于消息队列的削峰填谷。

详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

### 显式缓存

通过在请求中添加 `cache_control` 标记，确保相同输入确定性命中缓存，首次写入缓存仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本。

适用场景包括高频复用相同 Prompt、工业级 Agent 长上下文管理等。多种 Agent 和 Coding 工具（Claude Code、Open Code、OpenClaw、Hermes）已原生支持通过 Anthropic 兼容端点接入百炼并自动使用显式缓存。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

## 第三方模型集成

百炼平台通过模型市场汇聚了多个第三方模型供应商，开发者可通过统一的 [OpenAI 兼容接口](../concepts/openai-compatible.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用这些模型。所有第三方模型的调用方式一致：获取 API Key、配置环境变量、使用统一的 `base_url`（`https://dashscope.aliyuncs.com/compatible-mode/v1`）即可。

### DeepSeek 系列

百炼提供多个供应商的 DeepSeek 模型：

| 供应商 | 模型示例 | 特点 |
|--------|----------|------|
| 阿里云百炼 | deepseek-v4-pro | 限流更宽松，支持联网搜索与上下文缓存 |
| 硅基流动 | siliconflow/deepseek-v3.2 | 支持更长上下文 |
| 快手万擎 | vanchin/deepseek-v4-pro | 第三方直供 |

所有 DeepSeek 模型均支持通过 `enable_thinking` 参数在思考与非思考模式之间切换。

> **注意**：部分旧版 DeepSeek 模型（deepseek-v3、deepseek-r1 等）将于 2026 年 7 月 9 日下架，推荐转用 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash。

详见 [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[DeepSeek（快手万擎）](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)。

### Kimi 系列

百炼提供两种 Kimi 接入方式：

- **月之暗面直供**（`kimi/kimi-k2.6` 等）：支持文本、图像、视频输入，kimi-k2.7-code 系列为仅思考模型。
- **百炼部署**（`kimi-k2-thinking` 等）：支持多地域（华北2、美国、德国）。

> **注意**：百炼部署的 Moonshot-Kimi-K2-Instruct、kimi-k2-thinking 将于 2026 年 7 月 9 日下架。

详见 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。

### GLM 系列

- **百炼部署**（`glm-5.2`）：上下文长度 1M，支持思考模式。
- **智谱直供**（`ZHIPU/GLM-5.2`）：支持 `reasoning_effort` 参数控制思考深度（max/high/none）。

> **注意**：glm-4.6、glm-4.7 将于 2026 年 7 月 9 日下架。

详见 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

### MiniMax 系列

- **百炼部署**（`MiniMax-M2.5`）：支持思考模式。
- **MiniMax 直供**（`MiniMax/MiniMax-M2.7`）：华北2 地域可用。

> **注意**：MiniMax-M2.1 将于 2026 年 7 月 9 日下架。

详见 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)。

### 其他第三方模型

| 模型 | 供应商 | 模型标识 | 说明 |
|------|--------|----------|------|
| MiMo | 小米 | xiaomi/mimo-v2.5-pro | 混合推理模型，默认开启思考模式 |
| Step | 阶跃星辰 | stepfun/step-3.7-flash | 多模态推理模型，默认关闭思考模式 |

详见 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)、[Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)。

## 统一调用方式

无论使用哪个模型，百炼平台提供了统一的调用体验：

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并配置到环境变量。
2. 使用 [OpenAI 兼容接口](../concepts/openai-compatible.md)，`base_url` 设为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。
3. 通过 `model` 参数指定模型名称即可切换不同模型。
4. 支持思考模式的模型可通过 `enable_thinking` 参数控制。

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
- [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
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



