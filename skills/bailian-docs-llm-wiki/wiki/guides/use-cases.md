# use cases

阿里云百炼平台提供了丰富的使用场景和最佳实践，涵盖 [Prompt 工程](../concepts/prompt-engineering.md)、第三方模型集成、自定义模型调优、RAG 应用构建、性能优化等方面。本页面按场景分类汇总各实践指南，帮助开发者快速找到适合自身业务需求的参考方案。

## [Prompt 工程](../concepts/prompt-engineering.md)

百炼平台为不同模态的内容生成提供了系统的 Prompt 编写指南。

### 文生图 Prompt

文生图模型通过 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）两个参数控制图像生成。文生图 V2 还支持通过 `prompt_extend` 参数开启大模型智能改写，默认启用。

Prompt 编写遵循两种公式：

- **基础公式**：主体 + 场景 + 风格，适合初次尝试 AI 创作的用户
- **进阶公式**：主体 + 场景 + 景别/视角/镜头拍摄类型 + 风格 + 光线，适合有明确创作目标的用户

详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生文 Prompt

文生文场景下，有效的提示词编写需要关注任务描述的完整性、上下文信息的充分性以及输出格式的明确性。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 视频生成 Prompt

视频生成 Prompt 遵循"主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介"的结构。Vidu 模型支持通过特定关键词触发动态控制（大/中/小动态）、运镜控制（推拉摇移升降固定）、特殊拍摄手法（延时、微距、航拍等）以及画面风格（2D 动漫、3D 渲染、写实等）。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md) 和 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## 第三方模型集成

百炼平台除了自有的通义千问系列模型外，还集成了多个第三方模型提供商的推理服务。所有第三方模型均通过百炼统一的 API Key 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)/DashScope SDK 调用，开发者无需为每家模型单独申请账号。

### DeepSeek 系列

百炼提供三个供应商的 DeepSeek 模型服务：

| 供应商 | 代表模型 | 特点 |
|--------|----------|------|
| 阿里云百炼 | deepseek-v4-pro | 限流更宽松，支持联网搜索与上下文缓存 |
| 硅基流动 | siliconflow/deepseek-v3.2 | 支持更长上下文 |
| 快手万擎 | vanchin/deepseek-v4-pro | 华北2（北京）地域可用 |

> **注意**：deepseek-v3、deepseek-r1 等旧版模型将于 2026 年 7 月 9 日下架，推荐转用 qwen3.7-plus、qwen3.7-max、qwen3.6-flash。

所有 DeepSeek 模型均支持通过 `enable_thinking` 参数切换思考/非思考模式。详见 [DeepSeek大语言模型](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[DeepSeek（快手万擎）](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)。

### Kimi 系列

百炼提供两个供应商的 Kimi 模型服务：

| 供应商 | 代表模型 | 特点 |
|--------|----------|------|
| 月之暗面直供 | kimi/kimi-k2.7-code、kimi/kimi-k2.6 | 支持文本、图像、视频多模态输入；支持 `preserve_thinking` 多轮传递思考过程 |
| 阿里云百炼 | kimi-k2-thinking | 支持华北2、美国、德国多地域部署 |

> **注意**：Moonshot-Kimi-K2-Instruct、kimi-k2-thinking 将于 2026 年 7 月 9 日下架，推荐转用 qwen3.7 系列。

kimi/kimi-k2.7-code 为仅思考模型（`enable_thinking` 始终为 true）。详见 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 和 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。

### GLM 系列

百炼提供两个供应商的 GLM 模型服务：

| 供应商 | 代表模型 | 特点 |
|--------|----------|------|
| 智谱直供 | ZHIPU/GLM-5.1 | 支持更长回复长度 |
| 阿里云百炼 | glm-5.1 | 提供免费额度，阶梯计费 |

> **注意**：glm-4.6、glm-4.7 将于 2026 年 7 月 9 日下架。

详见 [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) 和 [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)。

### MiniMax 系列

| 供应商 | 代表模型 |
|--------|----------|
| 阿里云百炼 | MiniMax-M2.5 |
| MiniMax 直供 | MiniMax/MiniMax-M2.7 |

> **注意**：MiniMax-M2.1 将于 2026 年 7 月 9 日下架。

详见 [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md) 和 [MiniMax（直供）](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)。

### 其他第三方模型

- **MiMo（小米）**：mimo-v2.5-pro 为混合推理模型，默认开启思考模式。仅华北2（北京）地域可用。详见 [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)。
- **Stepfun（阶跃星辰）**：stepfun/step-3.7-flash 为多模态推理模型，默认关闭思考模式，可通过 `reasoning_effort` 参数控制推理深度。仅华北2（北京）地域可用。详见 [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)。

### 第三方模型通用调用模式

所有第三方模型均通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，基础配置如下：

```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
```

支持思考模式的模型通过 `extra_body={"enable_thinking": True}` 开启（Python SDK），Node.js SDK 则作为顶层参数传入。

## 自定义模型调优与评测

百炼支持基于通用大语言模型进行微调训练，创建自定义模型。整体流程为：

1. **数据准备**：收集业务数据，编排为 Prompt-Completion 格式，建议至少 500 条训练数据
2. **数据上传**：通过百炼控制台上传训练集和评测集，支持数据清洗和增强工具
3. **模型调优**：配置超参数（学习率、迭代次数等），平台自动训练
4. **[模型部署](../concepts/model-deployment.md)**：将训练完成的[模型部署](../concepts/model-deployment.md)到独占实例
5. **模型评测**：对已部署的模型进行评测，不满意可调整策略重复流程

> **注意**：完成调优的模型必须先部署才能调用和评测。

详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## RAG 应用构建

百炼通过 LlamaIndex 的 `DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 组件支持快速构建 RAG 应用。开发者可以：

- 使用 `DashScopeCloudIndex.from_documents()` 从本地文档创建知识库
- 通过 `index.as_retriever()` 获取检索器
- 结合 `DashScope` LLM 构建完整的问答引擎

详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 性能优化与成本控制

### 显式缓存

显式缓存通过在请求中添加 `cache_control` 标记，确保相同输入内容确定性命中缓存，可节省 90% 成本。适用场景包括：

- 需要稳定命中缓存的业务场景
- 高频复用相同 Prompt 的场景
- Agent 长上下文管理场景

多个主流 Agent/Coding 工具原生支持显式缓存，通过 Anthropic 协议接入百炼即可自动启用：Claude Code、Open Code、OpenClaw、Hermes 等。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-best-practice.md)。

### 限流应对

百炼 API 按请求数（RPM/RPS）和 Token 用量（TPM/TPS）限流，还有增速限制（Traffic Burst）。应对方案按改动成本递进：

1. **平台配置**（低改动）：服务端排队等待（添加 `X-DashScope-Wait-Timeout` 请求头）、提升限流额度、PTU 独享算力、Batch API 异步处理
2. **客户端流控**（改代码）：基础重试、令牌桶、平滑限速器、自适应拥塞控制
3. **架构兜底**（改架构）：模型降级 Fallback、消息队列削峰填谷

如果遇到 `429` 错误且为突发流量触发，推荐首选服务端排队等待方案。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 多模态应用

### 文档转视频

百炼支持借助大模型将文档自动转换为包含图文、语音、字幕的完整视频。流程包括：文档切片 → 生成演示文稿 → 生成讲解语音与字幕 → 合成视频。依赖 FFmpeg 和 Marp 工具。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

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



