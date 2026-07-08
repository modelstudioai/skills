# use cases

阿里云百炼平台为开发者提供了丰富的模型使用场景，涵盖 Prompt 工程、[多模态](../concepts/multimodal.md)内容生成、RAG 应用构建、模型微调、第三方模型集成以及 API 调用优化等方面。本文汇总了百炼平台的主要使用场景与最佳实践，帮助开发者快速找到适合自身业务的方案。

## Prompt 工程

### 文生文 Prompt 设计

设计高质量 Prompt 是充分发挥大模型能力的关键。百炼推荐使用 **Prompt 框架**来系统化组织提示词，框架包含背景、目的、风格、语气、受众、输出六个要素。此外，平台提供了 Prompt 一键优化工具，可对输入的提示词进行自动扩写和细节补充。

常用技巧包括：

- **构建清晰明确的 Prompt**：任务描述越具体，模型输出越符合预期
- **使用分隔符**：用特殊符号（如 `---`、`###`）分隔 Prompt 的不同部分
- **Few-shot 示例**：提供输入输出示例引导模型行为
- **链式思考（CoT）**：引导模型分步推理，提升复杂任务准确率

详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt 设计

文生图模型支持 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）两个参数。提示词公式分为两级：

- **基础公式**：主体 + 场景 + 风格
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

文生图 V2 还支持 `prompt_extend` 参数开启大模型智能改写（默认开启），可自动丰富提示词细节。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频 / 图生视频 Prompt 设计

视频生成的提示词公式与图片类似但增加了运动维度：

- **基础公式**：主体 + 场景 + 运动
- **进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频**：运动 + 运镜（图像已确定主体和场景）
- **声音公式**（wan2.7/wan2.6/wan2.5）：增加人声/音效/背景音乐描述
- **多镜头公式**（wan2.7/wan2.6）：总体描述 + 镜头序号 + 时间戳 + 分镜内容

wan2.7 支持通过"图n"/"视频n"指代参考素材，实现参考生视频。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

Vidu 视频生成模型也有专用的提示词体系，基本结构为"主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介"，支持通过特定关键词控制动态幅度、运镜、景别、视角和特效等。详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## RAG 应用构建

百炼支持通过 LlamaIndex 框架构建 RAG（[检索增强生成](../concepts/rag.md)）应用。核心流程：

1. **文件解析**：使用 `DashScopeParse` 解析 `.doc`、`.docx`、`.pdf` 文件（单文件 100M 以内，1000 页以内）
2. **创建知识库**：通过 `DashScopeCloudIndex.from_documents()` 创建索引
3. **获取 Retriever**：从 index 对象获取检索器
4. **构建 Query Engine**：结合 `DashScope` LLM 和知识库创建问答引擎

```python
from llama_index.indices.managed.dashscope import DashScopeCloudIndex
index = DashScopeCloudIndex("my_first_index")
retriever = index.as_retriever()
query_engine = index.as_query_engine(llm=dashscope_llm)
```

Python 版本要求 >=3.8 且 <=3.12。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优

百炼提供完整的模型定制化流程：**模型调优 -> 模型部署 -> 模型评测**。

- **训练数据**：建议至少准备 500 条"Prompt-Completion"格式的数据，需做脱敏处理
- **模型调优**：配置学习率、迭代次数等超参数，平台自动训练
- **模型部署**：调优后的模型必须部署到独占实例才能调用和评测
- **模型评测**：支持多种评测维度，结果不满意可调整策略重新训练

详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 文档转视频

借助大模型可将文档自动转换为包含图文、语音、字幕的视频。方案流程：

1. 文档切片：大模型总结标题并划分段落
2. 生成演示文稿：整合标题、正文和图片生成幻灯片
3. 生成讲解语音与字幕：[多模态](../concepts/multimodal.md)模型将文字转换为音频
4. 合成视频：将演示文稿、音频和字幕合并

依赖工具：FFmpeg（音视频处理）、Marp（演示文稿制作）、浏览器引擎。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型集成

百炼平台统一接入了多家第三方模型供应商，均可通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用。

### 支持的第三方模型

| 模型系列 | 供应商 | 代表模型 | 特点 |
|---------|--------|---------|------|
| DeepSeek | 阿里云百炼 / 硅基流动 / 快手万擎 | deepseek-v4-pro | 编程、数学、通用任务；支持思考模式 |
| Kimi | 阿里云百炼 / 月之暗面 | kimi-k2.7-code, kimi-k2.6 | [多模态](../concepts/multimodal.md)支持；kimi-k2.7-code 为仅思考模型 |
| GLM | 阿里云百炼 / 智谱 | glm-5.2 | 支持 1M 上下文 |
| MiniMax | 阿里云百炼 / 稀宇科技 | MiniMax-M2.7, MiniMax-M2.5 | 思考模式 |
| MiMo | 小米 | mimo-v2.5-pro | 混合推理模型，默认开启思考 |
| Step | 阶跃星辰 | step-3.7-flash | 多模态推理，默认关闭思考 |

> **注意**：多个第三方模型（deepseek-v3/r1 系列、kimi-k2 系列部分模型、glm-4.6/4.7、MiniMax-M2.1）将于 **2026年7月9日** 下架，推荐迁移至 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash。

### 调用方式

所有第三方模型的调用模式统一，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)：

```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="<模型名>",  # 如 "siliconflow/deepseek-v3.2"
    messages=[{"role": "user", "content": "你好"}],
    extra_body={"enable_thinking": True},  # 开启思考模式
)
```

`enable_thinking` 为非 OpenAI 标准参数，Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。部分模型还支持 `reasoning_effort` 参数控制思考深度（可选值：`low`、`medium`、`high`、`max`、`none`）。

> **注意**：不同供应商提供的同名模型在地域支持、限流条件和功能特性上存在差异。例如，硅基流动供应的 DeepSeek 支持更长上下文，而阿里云百炼供应的 DeepSeek 限流更宽松且支持联网搜索和上下文缓存。部分供应商仅限华北2（北京）地域使用。

### 多地域支持

百炼在多个地域提供服务，不同地域的 Base URL 不同：

- **华北2（北京）**：`https://dashscope.aliyuncs.com/compatible-mode/v1`（推荐使用[业务空间](../concepts/workspace.md)专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **新加坡 / 德国 / 日本**：`https://{WorkspaceId}.<region>.maas.aliyuncs.com/compatible-mode/v1`

## API 调用优化

### 限流应对

百炼 API 按请求数（RPM/RPS）和 [Token](../concepts/token.md) 用量（TPM/TPS）限流，还有增速限制（Traffic Burst）。按改动成本从低到高的应对方案：

**平台配置方案**（低改动成本）：

- **服务端排队等待**（推荐首选）：请求头添加 `X-DashScope-Wait-Timeout`，服务端在指定时间内排队重试，仅适用于 Traffic Burst 限流
- **提升限流额度**：在百炼控制台直接提升，提交后立即生效
- **PTU**：独立预留专享算力，避免公共资源池竞争
- **Batch API**：离线任务批量提交，不受在线限流约束

**客户端流控策略**（需改代码）：

- 基础重试 -> 令牌桶 -> 平滑限速器 -> 自适应拥塞控制

**架构兜底方案**：模型降级（Fallback）、基于 MQ 的削峰填谷。

详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

### 显式缓存

显式缓存通过在请求中添加 `cache_control` 标记，确保相同输入确定性命中缓存。首次写入缓存产生标准价格 25% 的额外开销，后续命中可节省 90% 成本。

适用场景：高频复用相同 Prompt、工业级 Agent 的长上下文管理。

主流 Coding Agent 工具（Claude Code、Open Code、OpenClaw、Hermes）通过 Anthropic 兼容端点接入百炼时原生支持显式缓存，无需额外配置。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

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


