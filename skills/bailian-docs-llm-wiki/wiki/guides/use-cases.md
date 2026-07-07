# use cases

阿里云百炼平台提供了丰富的使用场景支持，涵盖 Prompt 工程、[多模态](../concepts/multimodal.md)内容生成、RAG 应用构建、自定义模型训练、第三方模型集成以及 API 调用优化等方面。本文汇总了平台的主要使用场景，帮助开发者快速找到适合自身业务需求的实践方案。

## Prompt 工程

### 文生文 Prompt 优化

设计高质量 Prompt 是充分发挥大模型能力的关键。百炼推荐使用 Prompt 框架来系统化地组织输入，该框架包含背景、目的、风格、语气、受众和输出六个要素，能显著提升模型输出的相关性和有效性。此外，百炼控制台提供了 [Prompt 一键优化工具](https://bailian.console.aliyun.com/?tab=app#/component-manage/prompt)，可对输入的 Prompt 进行自动扩写和细节添加。详细的 Prompt 设计技巧、分隔符使用、Few-shot 示例编排等方法参见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

### 文生图 Prompt 技巧

文生图模型通过 `prompt`（正向提示词）和 `negative_prompt`（反向提示词）两个参数控制图像生成。百炼提供两种提示词公式：

- **基础公式**：`主体 + 场景 + 风格`，适合初次尝试的用户
- **进阶公式**：`主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰`，适合有经验的用户

文生图 V2 还支持 `prompt_extend` 参数开启大模型智能改写，默认开启。提示词词典覆盖景别、视角、镜头拍摄类型、风格和光线五大维度，详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 视频生成 Prompt 技巧

万相系列模型支持文生视频和图生视频，提示词公式为 `主体 + 场景 + 运动`。进阶公式在此基础上增加美学控制和风格化描述。wan2.7/wan2.6 模型还支持多镜头连贯叙事、参考生视频、以及原生音频能力（人声/音效/背景音乐描述）。图生视频场景中，由于图像已确定主体和风格，提示词主要描述运动和运镜。

此外，Vidu 视频生成模型提供了独立的提示词体系，支持通过特定关键词触发动态控制、运镜控制、视频风格和特效等能力，详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## 应用构建

### 基于 LlamaIndex 构建 RAG 应用

百炼提供了与 LlamaIndex 的集成方案，通过 `DashScopeCloudIndex` 和 `DashScopeCloudRetriever` 组件，开发者可以在 LlamaIndex 框架中直接使用百炼的知识库检索增强服务。完整流程包括：

1. 使用 `DashScopeParse` 解析文档（支持 .doc/.docx/.pdf，单文件 100M、1000 页以内）
2. 通过 `DashScopeCloudIndex.from_documents()` 创建知识库
3. 获取 retriever 或 query engine 进行检索和问答

前提条件为获取 API Key 并安装 `llama-index-indices-managed-dashscope` 等依赖包。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

### 借助大模型将文档转换为视频

百炼支持利用大语言模型和[多模态](../concepts/multimodal.md)技术将文档自动转换为包含图文、语音、字幕的视频。方案流程为：文档切片（LLM 总结标题和段落）、生成演示文稿（Marp）、生成讲解语音与字幕（[多模态](../concepts/multimodal.md)模型）、合成视频（FFmpeg）。该方案依赖 FFmpeg 和 Marp 工具，提供了完整的 Python 代码包。

## 自定义模型调优

百炼支持基于通用大语言模型创建自定义模型，流程包含三个主要步骤和三个辅助步骤：

| 步骤 | 说明 |
|------|------|
| 训练数据准备 | 收集业务数据，编排为 Prompt-Completion 格式，建议至少 500 条 |
| 模型调优 | 配置超参数（学习率、迭代次数等），平台自动训练 |
| 模型部署 | 部署到独占实例，完成部署后方可调用和评测 |
| 模型评测 | 选择评测方式、数据和维度，平台自动完成评测 |

如果评测结果不满意，可调整训练策略（更换基础模型、扩充数据、调整超参数）后重复流程。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 第三方模型集成

百炼平台聚合了多家第三方模型供应商的推理服务，统一通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用，开发者只需使用百炼 API Key 即可访问。

### 可用模型

| 模型系列 | 供应商 | 最新型号 | 可用地域 |
|---------|--------|---------|---------|
| DeepSeek | 阿里云百炼 | deepseek-v4-pro | 北京、弗吉尼亚、新加坡、法兰克福、东京 |
| DeepSeek | 硅基流动 | siliconflow/deepseek-v3.2 | 仅北京 |
| DeepSeek | 快手万擎 | vanchin/deepseek-v4-pro | 仅北京 |
| Kimi | 阿里云百炼 | kimi-k2-thinking | 北京、新加坡、东京、弗吉尼亚、法兰克福 |
| Kimi | 月之暗面 | kimi/kimi-k2.7-code | 仅北京 |
| GLM | 阿里云百炼 | glm-5.2 | 北京、弗吉尼亚、法兰克福、新加坡 |
| GLM | 智谱 | ZHIPU/GLM-5.2 | 仅北京 |
| MiniMax | 阿里云百炼 | MiniMax-M2.5 | 仅中国内地 |
| MiniMax | 稀宇科技 | MiniMax/MiniMax-M2.7 | 仅北京 |
| MiMo | 小米 | xiaomi/mimo-v2.5-pro | 仅北京 |
| Step | 阶跃星辰 | stepfun/step-3.7-flash | 仅北京 |

> **注意**：部分模型即将下架。deepseek-v3 系列、glm-4.6/4.7、Moonshot-Kimi-K2-Instruct、kimi-k2-thinking、MiniMax-M2.1 将于 2026 年 7 月 9 日下架，推荐转用 qwen3.7-plus、qwen3.7-max 或 qwen3.6-flash。

### 调用方式

所有第三方模型均支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，大部分也支持 [DashScope SDK](../concepts/dashscope-sdk.md)。以 OpenAI Python SDK 为例：

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="deepseek-v4-pro",  # 替换为目标模型名称
    messages=[{"role": "user", "content": "你好"}],
)
```

多数模型支持通过 `enable_thinking` 参数开启思考模式，开启后模型会输出 `reasoning_content` 字段展示推理过程。该参数为非标准参数，Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。

> **注意**：同一模型在不同供应商间存在差异。例如硅基流动供应商的 DeepSeek 支持更长上下文，而阿里云百炼供应商的限流条件更宽松且支持联网搜索和上下文缓存。部分直供模型（如月之暗面 Kimi、智谱 GLM、小米 MiMo 等）需先在百炼控制台搜索并开通服务后方可调用。

## API 调用优化

### 限流应对

百炼 API 按主账号和模型维度独立限流，包括分钟级配额（RPM/TPM）、瞬时频率（RPS/TPS）和增速限制（Traffic Burst）三种规则。应对方案按改动成本从低到高分为三类：

1. **平台配置方案**：服务端排队等待（推荐首选，仅需添加 `X-DashScope-Wait-Timeout` 请求头）、提升限流额度、PTU 预置吞吐单元、Batch API 异步批处理
2. **客户端流控策略**：从基础重试到令牌桶、平滑限速器、自适应拥塞控制，按工程复杂度递进
3. **架构兜底方案**：模型降级（Fallback）、基于消息队列的削峰填谷

遇到 `429` 错误时，可根据错误码和触发维度特征快速定位原因并选择策略。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

### 显式缓存

显式缓存通过在请求中添加 `cache_control` 标记，确保相同输入内容确定性命中缓存，首次写入仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本。适用于高频复用相同 Prompt、工业级 Agent 长上下文管理等场景。

多种主流 Agent 和 Coding 工具已原生支持显式缓存：

- **Claude Code**：v2.x 起默认携带 `cache_control` 标记，接入百炼 Anthropic 兼容端点后自动生效
- **Open Code**：通过 `@ai-sdk/anthropic` 接入时默认注入缓存标记
- **OpenClaw**：走 Anthropic 兼容端点时默认启用
- **Hermes**：通过配置接入参数即可使用

详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

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


