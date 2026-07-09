# use cases

阿里云百炼平台提供丰富的模型调用和应用场景，涵盖文本生成、图像生成、视频生成、RAG 应用构建、自定义模型训练以及第三方模型集成等。本文汇总平台核心使用场景及最佳实践，帮助开发者快速找到适合自身业务的落地方案。

## Prompt 工程

### 文生文 Prompt 设计

百炼平台提供系统的 Prompt 设计方法论，帮助开发者高效利用大语言模型。核心原则是构建清晰、具体、无歧义的 Prompt，使模型输出更符合预期。

推荐使用 **Prompt 框架**进行结构化设计，包含六要素：背景、目的、风格、语气、受众、输出格式。该框架充分考虑影响 LLM 输出有效性的各方面，可显著提升模型表现。详见 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)。

平台还提供 Prompt 一键优化工具，可在控制台的 Prompt 页面点击"自动优化"使用，该工具通过调用大模型对输入 Prompt 进行自动扩写和细节添加。

### 文生图 Prompt 设计

文生图模型（万相系列）的 Prompt 设计有两种公式：

- **基础公式**：主体 + 场景 + 风格（适合新用户快速上手）
- **进阶公式**：主体描述 + 场景描述 + 定义风格 + 镜头语言 + 氛围词 + 细节修饰

关键参数包括 `prompt`（正向提示词）和 `negative_prompt`（反向提示词），文生图V2 还支持 `prompt_extend` 智能改写功能。提示词词典涵盖景别、视角、拍摄类型、风格和光线五大维度。详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)。

### 文生视频/图生视频 Prompt 设计

万相系列视频模型支持结构化提示词公式：

- **基础公式**：主体 + 场景 + 运动
- **进阶公式**：主体描述 + 场景描述 + 运动描述 + 美学控制 + 风格化
- **图生视频公式**：运动 + 运镜
- **声音公式**（wan2.7/2.6/2.5）：主体 + 场景 + 运动 + 声音描述
- **多镜头公式**（wan2.7/2.6）：总体描述 + 镜头序号 + 时间戳 + 分镜内容
- **参考生视频公式**（wan2.7/2.6）：参考指代 + 动作 + 场景 + 台词 + 背景音乐

wan2.7 模型支持使用"图n"或"视频n"在提示词中指代参考文件，实现主体一致性控制。详见 [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。

### Vidu 视频生成 Prompt 设计

Vidu 模型遵循"主体/场景 + 场景描述 + 环境描述 + 艺术风格/媒介"公式。提示词词典支持动态控制（大/中/小动态）、运镜控制（基础运镜、特殊拍摄手法、景别、视角、构图）、视频风格（2D动漫、3D渲染、写实等）、特效和氛围等维度。Vidu 还支持参考生视频保持主体一致性，以及 AI 漫剧创作。详见 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

## RAG 应用构建

百炼与 LlamaIndex 框架深度集成，开发者可通过 `DashScopeCloudIndex` 快速构建 RAG（[检索增强生成](../concepts/rag.md)）应用。核心流程包括：

1. **文件解析**：使用 `DashScopeParse` 解析 .doc/.docx/.pdf 文件（单文件 100M 以内，1000 页以内）
2. **创建知识库**：通过 `DashScopeCloudIndex.from_documents()` 构建
3. **检索与问答**：通过 `index.as_retriever()` 或 `index.as_query_engine()` 实现

前提条件包括获取 API Key、开通知识库服务，并安装 `llama-index-indices-managed-dashscope` 等依赖包。详见 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

## 自定义模型调优

百炼支持基于通用大语言模型进行微调训练，创建适应特定领域的自定义模型。完整流程为：

1. **训练数据准备**：收集业务数据并编排为"Prompt-Completion"格式，建议至少 500 条
2. **模型调优**：配置训练超参数（学习率、迭代次数等），平台自动训练
3. **模型部署**：将自定义模型部署到独占实例
4. **模型评测**：评测部署后的模型效果

> **注意**：完成调优的模型必须部署后才能调用和评测。如果评测结果不满意，可调整训练策略后重复流程。

平台提供数据清洗和增强工具，支持多版本数据管理。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

## 文档转视频

百炼支持借助大模型将文档自动转换为包含图文、语音、字幕的视频。方案流程为：

1. 文档切片：大模型总结标题并划分段落
2. 生成演示文稿：整合标题、正文、图片生成演示文稿图片
3. 生成讲解语音与字幕：多模态模型将文字转为音频并生成字幕
4. 生成视频：将所有素材剪辑合成

需要安装 FFmpeg 和 Marp 工具，并依赖 Python 环境。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型集成

百炼平台聚合了多家供应商的模型服务，统一通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 [DashScope SDK](../concepts/dashscope-sdk.md) 调用，使用同一个 API Key 即可访问所有模型。

### 支持的模型供应商

| 供应商 | 代表模型 | 特点 |
|--------|----------|------|
| DeepSeek（阿里云） | deepseek-v4-pro | 限流宽松，支持联网搜索与上下文缓存 |
| DeepSeek（硅基流动） | siliconflow/deepseek-v3.2 | 支持更长上下文 |
| DeepSeek（快手万擎） | vanchin/deepseek-v4-pro | 华北2（北京）地域可用 |
| Kimi（阿里云部署） | kimi-k2-thinking | 多地域可用（北京/新加坡/东京/弗吉尼亚/法兰克福） |
| Kimi（月之暗面直供） | kimi/kimi-k2.7-code | 支持多模态，速度提升 5-6 倍 |
| GLM（阿里云部署） | glm-5.2 | 支持 1M 上下文，多地域可用 |
| GLM（智谱直供） | ZHIPU/GLM-5.2 | [业务空间](../concepts/workspace.md)专属域名，更高稳定性 |
| MiniMax（阿里云部署） | MiniMax-M2.5 | 中国内地地域可用 |
| MiniMax（直供） | MiniMax/MiniMax-M2.7 | 华北2（北京）地域可用 |
| MiMo（小米直供） | xiaomi/mimo-v2.5-pro | 混合推理模型，默认开启思考 |
| Stepfun（阶跃星辰） | stepfun/step-3.7-flash | 多模态推理模型，支持 reasoning_effort 控制 |

### 调用方式

所有第三方模型均支持通过 OpenAI Python/Node.js SDK 调用，基本模式为：

```python
from openai import OpenAI
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="<模型名称>",
    messages=[{"role": "user", "content": "你好"}],
)
```

大部分模型支持通过 `enable_thinking` 参数开启思考模式（通过 `extra_body` 传入），思考过程通过 `reasoning_content` 字段返回。

> **注意**：部分第三方模型即将下架（DeepSeek 系列、Kimi K2 系列、GLM-4.x、MiniMax-M2.1 将于 2026年7月9日下架），推荐转用 qwen3.7-plus、qwen3.7-max、qwen3.6-flash 等模型。

详见各模型的集成教程：[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)。

## 限流应对与性能优化

### 限流机制

百炼 API 按主账号维度、模型独立计算限流，包含三种规则：分钟级配额限制（RPM/TPM）、瞬时频率限制（RPS/TPS）、增速限制（Traffic Burst）。

### 应对方案

按改动成本从低到高：

1. **平台配置方案**（低改动）：
   - 服务端排队等待：添加 `X-DashScope-Wait-Timeout` 请求头，服务端自动排队重试
   - 提升限流额度：在控制台直接提升临时额度，立即生效
   - PTU 预置吞吐单元：独立预留专享算力
   - Batch API：离线批量处理

2. **客户端流控策略**（改代码）：基础重试、令牌桶、平滑限速器、自适应拥塞控制

3. **架构兜底方案**（改架构）：模型降级 Fallback、基于消息队列削峰填谷

详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

### 显式缓存

百炼支持显式缓存（Explicit Cache），通过在请求中添加 `cache_control` 标记实现确定性缓存命中。首次写入仅产生标准价格 25% 的额外开销，后续命中可节省 90% 成本。

常用 Agent 工具（Claude Code、Open Code、OpenClaw、Hermes）接入百炼 Anthropic 兼容端点后均原生支持显式缓存，无需额外配置。Claude Code 可通过 `--exclude-dynamic-system-prompt-sections` 参数提升跨会话命中率。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

## 多地域服务

百炼支持多地域部署，不同地域的服务接入地址不同：

- **华北2（北京）**：`https://dashscope.aliyuncs.com/compatible-mode/v1`（推荐使用[业务空间](../concepts/workspace.md)专属域名）
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`
- **日本（东京）**：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1`

华北2（北京）地域推出了[业务空间](../concepts/workspace.md)专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，能够提供更高性能和稳定性。

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


