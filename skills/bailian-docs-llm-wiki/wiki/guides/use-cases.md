# use cases

本主题汇总阿里云百炼平台上围绕模型使用的典型场景与最佳实践，覆盖 Prompt 设计、文生图/文生视频、RAG 应用构建、自定义模型调优、文档转视频，以及第三方模型接入、限流应对和显式缓存等工程化能力。开发者可据此快速定位所需场景并完成接入。

## 支持的场景与能力

百炼在模型使用层面提供以下几类场景：

- **Prompt 工程**：文生文、文生图、文生视频/图生视频的提示词设计与优化。
- **RAG 应用构建**：基于 LlamaIndex 等框架接入百炼检索增强服务。
- **自定义模型调优**：基于通用大模型进行微调训练、部署与评测，贴近业务领域。
- **多模态内容生成**：借助大模型将文档自动转换为含图文、语音、字幕的视频。
- **第三方模型接入**：调用 DeepSeek、Kimi、GLM、MiniMax、MiMo、Step 等第三方模型推理服务。
- **生产化工程能力**：限流应对、显式缓存等保障稳定性与成本的最佳实践。

## Prompt 工程

### 文生文 Prompt

提示（Prompt）是输入给大模型的文本信息，越清晰、具体、没有歧义，模型表现越符合预期。构建高质量 Prompt 的要点：

- 明确目的、思考方向和执行策略，避免一句话模糊描述。
- 借助 Prompt 框架（如角色设定 + 任务要求 + 边界条件 + 输出格式）结构化描述需求。
- 百炼控制台提供 Prompt 一键优化工具，可对输入提示自动扩写和细节添加，推荐先优化再结合其他技巧。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt

文生图模型（万相-文生图 V1/V2）有两个与提示词相关的参数：`prompt`（正向提示词，支持中英文）和 `negative_prompt`（反向提示词，描述不希望出现的内容）。提示词撰写可遵循"主体 + 场景描述 + 风格/媒介"的结构，并配合官方提示词词典选择关键词。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频/图生视频 Prompt

万相视频生成可采用结构化提示词公式提升质量：**主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介**。要点包括：

- 避免主体过多或分散的句式，调整语序使主体集中。
- 表述准确，避免模糊术语；使用流畅的口语化措辞，避免过度文学化叙述。
- 适用于文生视频、首帧生视频、首尾帧生视频、参考生视频等 API。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

Vidu 视频生成采用相同的提示词公式思路，并提供关键词词典与进阶案例。详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## RAG 应用构建

基于 LlamaIndex 可直接使用百炼提供的检索增强服务。前置条件包括：获取并配置 [API Key](../concepts/api-key.md) 到环境变量、在百炼控制台开通[知识库](../concepts/knowledge-base.md)服务、如需指定[业务空间](../concepts/workspace.md)则获取[业务空间](../concepts/workspace.md) ID。开通后即可在 LlamaIndex 中集成百炼的 embedding 与 rerank 能力构建[检索增强生成](../concepts/rag.md)应用。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优

当通用大模型在特定领域表现不足时，可通过自定义模型提升准确性与适用性。自定义模型是基于通用大模型、通过领域数据微调训练得到的模型。创建流程一般包括：

1. **前提条件**：准备 [API Key](../concepts/api-key.md)、了解前置知识、确认计费信息。
2. **训练数据准备**：数据收集与上传，按要求格式化。
3. **训练任务**：选择基座模型与训练方法、配置超参并启动训练。
4. **部署与评测**：选择最佳训练产物部署为可调用模型，并评测效果。

详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 文档转视频

利用大模型与多模态应用技术可将文档自动转换为视频，所生成视频包含完整图文、语音、字幕，避免传统录制的高时间投入与专业剪辑门槛。官方提供完整代码包以便快速上手。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型接入

百炼支持接入多家第三方模型推理服务，按供应方式分为两类：

- **百炼部署**：由阿里云百炼统一部署，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用，支持多地域 Base URL。包括 DeepSeek（阿里云供应商）、Kimi、GLM、MiniMax 等。
- **原厂直供**：由模型原厂（月之暗面、智谱、稀宇科技、小米、阶跃星辰、快手万擎、硅基流动等）直接供应，通常仅在华北2（北京）地域可用，需使用该地域 [API Key](../concepts/api-key.md) 并在控制台单独开通授权。

### 接入地址与 SDK

百炼部署的模型通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，Base URL 因地域而异：

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

原厂直供模型（如 GLM-智谱、Kimi-月之暗面、MiniMax、MiMo-小米、Stepfun-阶跃星辰、快手万擎 DeepSeek）通常仅支持华北2（北京）地域，需使用对应地域 API Key。

### 支持的模型族

| 模型族 | 供应方 | 说明 |
| --- | --- | --- |
| DeepSeek | 阿里云 / 硅基流动 / 快手万擎 | 多供应商，阿里云供应商限流更宽松、支持联网搜索与上下文缓存；硅基流动支持更长上下文。详见 [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) |
| Kimi | 百炼部署 / 月之暗面 | 原厂直供仅在华北2（北京）可用。详见 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) |
| GLM | 百炼部署 / 智谱 | 每个模型各有 100 万免费 [Token](../concepts/token.md)；glm-5.2 支持 1M 上下文。详见 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) |
| MiniMax | 百炼部署 / 稀宇科技 | 详见 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md) |
| MiMo | 小米直供 | mimo-v2.5-pro 为混合推理模型，默认开启思考模式（`enable_thinking` 默认 `true`）。详见 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md) |
| Step | 阶跃星辰直供 | step-3.7-flash 为多模态推理模型，默认关闭思考模式，可通过 `enable_thinking:true` 开启，并用 `reasoning_effort`（low/medium/high）控制推理深度。详见 [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md) |

### 思考模式

部分第三方模型（如 MiMo、Step）支持混合推理模式，通过 `enable_thinking` 参数控制是否开启思考；开启后推理过程经 `reasoning_content` 字段返回，可用 `reasoning_effort` 控制深度。若需直接输出结果，可显式传入 `enable_thinking: false`。

## 生产化最佳实践

### 限流应对

百炼 API 按请求数和 [Token](../concepts/token.md) 用量限流。大模型请求延迟高、同时受两个维度约束，单纯"遇错重试"效果有限。应对方案按改动成本从低到高分三类：

- **平台配置方案（低成本）**：服务端排队等待（推荐首选，避免客户端自行重试）、提升限流额度、预置吞吐单元（PTU）、异步批处理（Batch API）。
- **客户端流控策略**：从基础重试到自适应拥塞控制，按工程复杂度递进的四种策略。
- **架构兜底**：在更高层面做容量与降级设计。

详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

### 显式缓存

显式缓存通过在请求中添加缓存标记，确保相同输入内容确定性命中缓存，可做到 100% 命中，不受后端资源调度影响。适用场景：

- 对缓存命中稳定性有明确要求的业务。
- 高频复用相同 Prompt 的场景：首次写入缓存仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本；只要发生至少一次命中，总体成本即低于不使用缓存。
- 工业级 Agent 的长上下文管理（压缩、recap、system reminder 等导致上下文持续变化的场景）。

详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

## 限制和注意事项

- **模型下架**：DeepSeek（deepseek-v3/v3.1/v3.2/v3.2-exp/r1/r1-0528 及 distill 系列）、Kimi（Moonshot-Kimi-K2-Instruct、kimi-k2-thinking）、GLM（glm-4.6/glm-4.7）、MiniMax（MiniMax-M2.1）等多款模型将于 **2026 年 7 月 9 日**下架，推荐转用 qwen3.7-plus / qwen3.7-max / qwen3.6-flash。
- **地域限制**：原厂直供模型（月之暗面、智谱、稀宇科技、小米、阶跃星辰、快手万擎、硅基流动）通常仅在华北2（北京）地域可用，须使用该地域 API Key；百炼部署的模型支持多地域，但各地域可调用模型与限流不同。
- **免费额度**：GLM 系列每个模型各有 100 万免费 [Token](../concepts/token.md)，具体以控制台为准。
- **限流维度**：请求数与 Token 用量双维度限流，跨地域配额独立，扩容需在对应地域申请。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践 ](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)
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


