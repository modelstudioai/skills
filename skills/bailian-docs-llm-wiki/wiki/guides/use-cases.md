# use cases

百炼平台围绕大模型提供了一整套使用场景与最佳实践，覆盖文生文/文生图/文生视频的 Prompt 设计、RAG 应用搭建、自定义模型调优部署、第三方模型集成、限流应对与显式缓存等。本页汇总各类场景的关键能力、参数与注意事项，帮助开发者快速选型并避开常见坑。

## 文生文 Prompt 设计

提示（Prompt）是输入给大模型的文本信息，越清晰、具体、无歧义，模型表现越符合预期。构建 Prompt 时建议给出明确目的、思考方向与执行策略，而非一句话模糊需求。百炼控制台提供 [Prompt 一键优化](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 工具，可对输入提示自动扩写和细节添加，建议先优化再调试其他技巧。

常用技巧：
- 角色设定：让模型扮演特定领域专家（如"你是一位资深 PHP 编程专家"）。
- 结构化输出：要求分步骤、列要点，便于后续解析。
- 少样本（Few-shot）：在 Prompt 中给出示例输入/输出，引导格式与风格。
- 边界与错误处理：显式要求模型考虑边界条件、异常处理与安全考量。
- 迭代调试：通过对比模糊 vs. 清晰 Prompt 的输出差异逐步收敛。

> **注意**：Prompt 优化功能本身调用大模型实现，会消耗 Token；优化结果仍需人工校验事实性。

## 文生图与文生视频 Prompt

文生图、文生视频/图生视频对 Prompt 的描述粒度要求更高，通常需包含主体、风格、构图、镜头、时长等要素。详见 [文生图 Prompt 指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 与 [文生视频/图生视频 Prompt 指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)；Vidu 等视频生成模型可参考 [Vidu 视频生成 Prompt 指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。

视频类要点：
- 明确镜头运动（推、拉、摇、移）与转场。
- 控制时长与关键帧描述，避免一次性要求过多情节。
- 图生视频时，首帧图片质量直接决定成片稳定性。

## 基于 LlamaIndex 构建 RAG 应用

百炼支持基于 LlamaIndex 搭建检索增强生成（RAG）应用，将企业私有知识库与 LLM 结合，降低幻觉并支持事实溯源。典型流程包括文档加载切分、向量化（Embedding）、存入向量库、检索召回、拼接到 Prompt 后交给 LLM 生成。详见 [基于 LlamaIndex 构建 RAG 应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

关键参数：
- `chunk_size` / `chunk_overlap`：切分粒度，影响召回精度与上下文长度。
- `top_k`：召回数量，过大会引入噪声，过小易漏答。
- Embedding 模型选择：中英文场景选对应模型，注意维度与最大输入长度。

## 自定义模型调优、部署与[评测](../concepts/evaluation.md)

百炼支持在预训练基座上做自定义模型调优（SFT/持续训练），完成后部署为专属服务并[评测](../concepts/evaluation.md)效果。调优数据建议覆盖目标业务的真实分布，并做去重、脱敏与质量标注。部署后建议用业务[评测](../concepts/evaluation.md)集做回归，关注准确率、拒答率与稳定性指标。详见 [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)。

> **注意**：调优数据质量比数量更重要；脏数据会显著拉低线上表现。部署前务必做安全合规审核。

## 借助大模型将文档转换为视频

可通过 LLM 把结构化文档（产品说明、教程等）转换为视频脚本，再配合文生图/文生视频模型生成分镜画面，最终合成视频。关键在于让模型先产出分镜大纲（镜头、旁白、画面描述），再逐镜头生成素材，避免一次性生成导致内容失控。详见 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)。

## 第三方模型集成

百炼模型广场集成了多家第三方模型，可通过统一 OpenAI 兼容接口调用，无需自建代理。支持厂商包括：

| 厂商 | 模型 | 来源 |
| --- | --- | --- |
| DeepSeek | DeepSeek 系列 | [阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)、[硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)、[Vanchin](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md) |
| Moonshot | Kimi | [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)、[月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) |
| 智谱 | GLM | [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)、[智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md) |
| MiniMax | MiniMax | [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)、[MiniMax 官方](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md) |
| 小米 | MiMo | [MiMo](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md) |
| 阶跃星辰 | Stepfun | [Stepfun](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md) |

调用方式：将 `base_url` 指向百炼网关，`model` 字段填模型广场中的模型标识，使用百炼 API-Key 鉴权，请求/响应格式与 OpenAI Chat Completions 一致，可复用现有 SDK。

> **注意**：同一模型（如 DeepSeek、Kimi、GLM、MiniMax）可能由多个供应商提供，定价、可用区与限流策略不同，请按业务所在地域与成本选择对应供应商。

## 限流应对最佳实践

百炼对 API 调用按模型维度做限流（RPM/TPM）。超限时返回 429，建议采取：客户端指数退避重试、请求限速（令牌桶）、错峰调用、按租户/Key 分流、对非实时任务改异步队列。重试时务必带上 `Retry-After` 头的等待时间，避免雪崩。详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)。

## 显式缓存最佳实践

对于 Prompt 中固定不变的前缀（系统指令、Few-shot 示例、长上下文文档），可启用显式缓存（Explicit Cache），将前缀缓存命中后只计费增量 Token，显著降低成本与首 Token 延迟。使用时需保证前缀字节级稳定（包括空格、换行），并按文档要求在指定位置插入缓存标记。详见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)。

> **注意**：缓存命中要求前缀完全一致；任何微小改动都会导致缓存失效。动态内容（用户输入、时间戳）必须放在缓存边界之后。

## 限制与注意事项

- 第三方模型可用性与配额受供应商影响，跨可用区调用可能产生额外延迟或失败，建议生产环境配置失败回退。
- 调优与部署会占用专属资源配额，计费独立于按量调用，请提前评估成本。
- 文生图/视频模型对敏感内容有审核策略，Prompt 中含违规要素会被拒绝，需在业务侧做前置过滤。
- 显式缓存与限流策略可能随版本调整，上线前以控制台与官方文档为准。

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


