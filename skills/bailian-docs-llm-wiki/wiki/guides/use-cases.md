# use cases

阿里云百炼平台提供了丰富的使用场景和最佳实践，涵盖 [Prompt 工程](../concepts/prompt-engineering.md)、多模态内容生成、RAG 应用构建、模型调优部署、API 调用优化以及第三方模型集成等方面。本页汇总了这些典型用例，帮助开发者快速找到适合自身业务的实践方案。

## [Prompt 工程](../concepts/prompt-engineering.md)

### 文生文 Prompt 设计

设计高质量的 Prompt 是发挥大语言模型能力的关键。百炼推荐使用 **Prompt 框架**来系统化构建提示词，包含六个要素：背景、目的、风格、语气、受众、输出。核心原则是让任务描述越清晰、具体、无歧义，模型表现越好。

常用优化技巧：
- **使用分隔符**：用 `---` 或 `"""` 分隔指令与待处理内容，避免混淆
- **少样本提示（Few-shot）**：在 Prompt 中提供示例，引导模型输出格式和风格
- **思维链（Chain-of-Thought）**：引导模型逐步推理，提升复杂任务的准确性
- **让模型扮演角色**：指定模型身份（如"你是一位资深 Python 工程师"），使输出更专业

百炼控制台还提供了 Prompt 一键优化工具，可自动扩写和细化提示词。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt 设计

文生图场景中，提示词通过 `prompt`（正向）和 `negative_prompt`（反向）两个参数控制。百炼提供两种提示词公式：

- **基础公式**：`主体 + 场景 + 风格`，适合新用户快速上手
- **进阶公式**：`主体 + 场景 + 风格 + 景别 + 视角 + 镜头类型 + 光线`，适合追求精确控制的用户

文生图 V2 额外支持 `prompt_extend` 参数（默认开启），可通过大模型智能改写 Prompt。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频 / 图生视频 Prompt 设计

视频生成的提示词重点在描述画面内容和运动过程：

- **基础公式**：`主体 + 场景 + 运动`
- **进阶公式**：`主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化`
- **图生视频**：由于图像已确定主体和场景，提示词主要描述动态过程和运镜

详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

## 应用构建实践

### 基于 LlamaIndex 构建 RAG 应用

百炼提供了与 LlamaIndex 框架的深度集成，支持通过 `DashScopeCloudIndex` 使用百炼的检索增强服务。主要流程：

1. 使用 `DashScopeParse` 解析文档（支持 .doc、.docx、.pdf，单文件 100M / 1000 页以内）
2. 创建 `DashScopeCloudIndex` 索引，自动上传到百炼知识库
3. 使用 `DashScopeCloudRetriever` 进行检索并结合 LLM 生成回答

前置条件包括获取 API Key、开通知识库服务、安装 `llama-index-indices-managed-dashscope` 等包。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

### 借助大模型将文档转换为视频

该方案通过大语言模型和多模态技术，自动将文档转换为包含图文、语音、字幕的视频。流程分为四步：文档切片、生成演示文稿、生成讲解语音与字幕、合成视频。依赖 FFmpeg 和 Marp 工具。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 模型调优与部署

百炼支持基于通用大语言模型进行自定义微调，创建适配特定业务场景的模型。完整流程包括三个主要步骤：

1. **模型调优**：准备训练数据（收集、清洗、划分），配置超参数（学习率、迭代次数等），平台自动训练
2. **模型部署**：将训练完成的模型部署到独占实例，才能调用和评测
3. **模型评测**：使用自定义数据和评测维度验证模型效果

如果评测结果不满意，可调整训练策略（更换基础模型、扩充数据、修改超参数）后重复流程。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## API 调用优化

### 限流应对

百炼 API 按主账号维度、模型独立计算限流，包含三种规则：分钟级配额（RPM/TPM）、瞬时频率（RPS/TPS）、增速限制（Traffic Burst）。应对方案按改动成本从低到高分为：

- **平台配置**：服务端排队等待（加请求头）、提升限流额度、PTU、Batch API
- **客户端流控**：从基础重试到自适应拥塞控制的四级策略
- **架构兜底**：模型降级 Fallback、基于消息队列的削峰填谷

遇到 `429` 错误时，推荐先尝试服务端排队等待功能。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

### 显式缓存

显式缓存通过在请求中添加缓存标记，确保相同输入内容 100% 确定性命中缓存。适用场景：

- 高频复用相同 Prompt（首次写入成本仅为标准价格的 25%，命中后节省 90%）
- 工业级 Agent 的长上下文管理（固定关键上下文片段）

Claude Code、Cursor、Cline、Windsurf 等主流 Agent 和 Coding 工具可通过 Anthropic 协议接入百炼，原生支持显式缓存。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

## 第三方模型集成

百炼平台提供了多种第三方模型的托管服务，开发者可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 统一调用。支持的模型包括：

| 模型系列 | 代表模型 | 说明 |
|---------|---------|------|
| DeepSeek | deepseek-v4-pro | 编程、数学和通用任务表现出色，支持思考模式 |
| Kimi | Moonshot-Kimi-K2-Instruct | 月之暗面出品，支持多地域部署 |
| GLM | glm-4.6、glm-4.7 | 智谱 AI 出品，每个模型各有 100 万免费 Token |
| MiniMax | MiniMax 系列 | 支持通过百炼统一接口调用 |
| MiMo | MiMo 系列 | 小米出品的推理模型 |
| Stepfun | Stepfun 系列 | 阶跃星辰出品 |
| Vidu | Vidu 视频生成 | 支持文生视频，有专用 Prompt 指南 |

> **注意**：部分第三方模型（如 DeepSeek V3/R1 系列旧版、Kimi K2、GLM 4.6/4.7）计划于 2026 年 7 月 9 日下架，建议迁移至 Qwen 系列模型（qwen3.7-plus、qwen3.7-max、qwen3.6-flash）。

所有第三方模型均可通过统一的 `base_url`（如 `https://dashscope.aliyuncs.com/compatible-mode/v1`）调用，支持华北2（北京）、美国（弗吉尼亚）等多地域。调用前需获取 API Key 并安装对应 SDK。详见各模型文档：[DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)
- [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)


