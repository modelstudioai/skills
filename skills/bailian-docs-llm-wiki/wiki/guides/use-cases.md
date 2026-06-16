# use cases

阿里云百炼平台提供了丰富的使用场景和最佳实践，涵盖 [Prompt 工程](../concepts/prompt-engineering.md)、多模态内容生成、第三方模型集成、RAG 应用构建、自定义模型训练以及生产环境优化等方面。本文整理了平台核心使用场景的关键信息，帮助开发者快速定位所需方案。

## [Prompt 工程](../concepts/prompt-engineering.md)指南

百炼平台针对不同模态提供了系统的 Prompt 编写方法论。

### 文生文 Prompt

设计高质量文生文 Prompt 的核心原则是**清晰、具体、无歧义**。推荐使用 Prompt 框架来组织内容，包含背景、目的、风格、语气、受众和输出格式六个要素。此外，百炼控制台提供了 [Prompt 一键优化工具](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)，可自动扩写和细化 Prompt。详见[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt

文生图模型（万相系列）支持 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）两个参数，文生图 V2 还支持通过 `prompt_extend` 开启大模型智能改写。

Prompt 编写提供两级公式：

- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

详见[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频 / 图生视频 Prompt

万相视频模型的 Prompt 结构如下：

- **基础公式**：主体 + 场景 + 运动
- **进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频公式**：运动 + 运镜（图像已确定主体和风格）
- **声音公式（wan2.7/wan2.6/wan2.5）**：主体 + 场景 + 运动 + 声音描述（人声/音效/背景音乐）
- **多镜头公式（wan2.7/wan2.6）**：总体描述 + 镜头序号 + 时间戳 + 分镜内容
- **参考生视频公式（wan2.7/wan2.6）**：通过"图n"或"视频n"指代参考素材，实现主体一致性

详见[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

### Vidu 视频生成 Prompt

Vidu 模型使用 **主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介** 公式。支持通过特定关键词控制动态幅度（大动态/中动态/小动态）、运镜方向、景别视角和特效。Vidu 在参考生视频场景下能保持多视角的主体一致性。详见[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## 第三方模型集成

百炼平台通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)和 DashScope SDK 统一接入多家第三方模型，开发者只需更换 `model` 参数即可切换模型。所有模型的调用方式高度一致：获取 API Key、配置环境变量、通过 `https://dashscope.aliyuncs.com/compatible-mode/v1` 端点调用。

### 可用模型一览

| 模型系列 | 供应商 | 最新模型 | 思考模式 |
|---------|--------|---------|---------|
| DeepSeek | 阿里云百炼 | deepseek-v4-pro | 支持（`enable_thinking`） |
| DeepSeek | 硅基流动 | siliconflow/deepseek-v3.2 | 支持 |
| DeepSeek | 快手万擎 | vanchin/deepseek-v4-pro | 支持 |
| Kimi | 月之暗面 | kimi/kimi-k2.7-code, kimi/kimi-k2.6 | 支持 |
| GLM | 智谱 | ZHIPU/GLM-5.1 | 支持 |
| GLM | 阿里云百炼 | glm-5.1 | 支持 |
| MiniMax | 阿里云百炼 | MiniMax-M2.5 | 支持 |
| MiniMax | 稀宇科技 | MiniMax/MiniMax-M2.7 | 支持 |
| MiMo | 小米 | xiaomi/mimo-v2.5-pro | 默认开启 |
| Stepfun | 阶跃星辰 | stepfun/step-3.7-flash | 支持（`reasoning_effort`） |

> **注意**：部分模型即将下架。deepseek-v3/r1 系列、glm-4.6/4.7、Moonshot-Kimi-K2-Instruct、MiniMax-M2.1 等将于 **2026年7月9日** 下架，推荐转用 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash。

### 调用要点

- `enable_thinking` 是非 OpenAI 标准参数，Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入
- 思考模式输出的推理过程通过 `reasoning_content` 字段返回
- 部分模型（如 kimi/kimi-k2.7-code）为仅思考模型，无法关闭思考模式
- 不同供应商的同系列模型存在差异：硅基流动 DeepSeek 支持更长上下文，百炼部署版限流更宽松且支持联网搜索和上下文缓存

详见各模型文档：[DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)、[GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)。

## RAG 应用构建

通过 LlamaIndex 集成百炼知识库服务，可快速构建 RAG 应用。核心步骤：

1. **文档解析**：使用 `DashScopeParse` 解析 .doc/.docx/.pdf 文件（单文件 100M 以内、1000 页以内）
2. **创建知识库**：调用 `DashScopeCloudIndex.from_documents()` 创建索引
3. **检索与问答**：通过 `index.as_retriever()` 获取检索器，或通过 `index.as_query_engine(llm=dashscope_llm)` 获取问答引擎

需安装 `llama-index-core`、`llama-index-llms-dashscope`、`llama-index-indices-managed-dashscope`，Python 版本要求 >=3.8 且 <=3.12。详见[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型训练

百炼支持基于通用大模型进行微调训练，流程为**模型调优 -> 模型部署 -> 模型评测**三步。关键注意事项：

- 训练数据需编排为"Prompt-Completion"格式，建议至少准备 500 条训练数据
- 完成调优的模型**必须部署后才能调用和评测**
- 如评测结果不满意，可调整训练策略后重复整个流程
- 涉及模型调优、部署和评测多种计费项

详见[自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 生产环境优化

### 显式缓存

通过在请求中添加缓存标记（`cache_control`），确保相同输入内容确定性命中缓存，降低 90% 成本。适用于高频复用 Prompt 和 Agent 长上下文管理场景。Claude Code、Open Code、OpenClaw、Hermes 等工具通过 Anthropic 兼容端点接入后可原生支持显式缓存。

接入端点包括：

- 按量计费：`https://dashscope.aliyuncs.com/apps/anthropic`
- Token Plan 团队版：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- Coding Plan：`https://coding.dashscope.aliyuncs.com/apps/anthropic`

详见[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

### 限流应对

百炼 API 按 RPM/TPM（分钟配额）、RPS/TPS（瞬时频率）和 Traffic Burst（增速）三个维度限流。应对方案按改动成本递进：

1. **平台配置**（低成本）：服务端排队等待（添加 `X-DashScope-Wait-Timeout` 请求头）、提升限流额度、PTU 预置吞吐单元、Batch API 异步批处理
2. **客户端流控**（改代码）：基础重试、令牌桶、平滑限速器、自适应拥塞控制
3. **架构兜底**（改架构）：模型降级 Fallback、基于消息队列的削峰填谷

突发流量触发 429 错误时，推荐首先尝试服务端排队等待。详见[限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 文档转视频

借助大模型可将文档自动转换为包含图文、语音、字幕的视频。方案分四步：文档切片（LLM 总结标题和段落）-> 生成演示文稿 -> 生成讲解语音与字幕 -> 合成视频。依赖 FFmpeg 和 Marp 工具，支持 macOS 和 Windows。详见[借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

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


