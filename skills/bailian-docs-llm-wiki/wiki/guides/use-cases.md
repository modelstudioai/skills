# use cases

`use cases` 是百炼平台面向开发者提供的典型应用场景与工程实践集合，覆盖从基础模型调用、[Prompt 工程](../concepts/prompt.md)、RAG 构建到音视频生成等全链路能力。本页结构化梳理核心能力边界、参数规范、接入方式及关键约束，便于快速选型与落地。所有实践均基于当前稳定版 API 与控制台功能，历史方案请参考 [历史模型指南](../../raw/model-user-guide/use-cases/legacy-resources.md)。

## 支持的模型/功能

- **文本生成类**：Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL（多模态理解）、Qwen-Audio（语音理解）  
- **生成式多模态**：万相（WanX）支持文生图、图生图、文生视频（含万相3.0）、数字人驱动；[万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 明确了帧率、时长与分辨率约束  
- **语音能力**：TTS（语音合成）、ASR（语音识别）、声音克隆（需合规授权），详见 [声音克隆：定制你的专属声线](../../raw/model-user-guide/use-cases.md) 中的技术方案入口  
- **检索增强**：原生支持 RAG 流水线构建，推荐使用 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 的轻量集成路径  
- **三方扩展**：支持通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用第三方模型，具体配置见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，如 `qwen-max`、`wanx-v1`、`tts-1`；不支持别名或模糊匹配 |
| `stream` | boolean | 否 | 仅文本/语音合成支持流式响应；视频/图像生成不支持流式 |
| `seed` | integer | 否 | 文生图/文生视频中用于结果复现，取值范围 `0–4294967295`；[文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 强调 seed 对构图稳定性的影响 |
| `max_tokens` | integer | 否 | 仅文本模型生效；图像/视频模型忽略该参数，由 `size` 或 `duration` 控制输出规模 |

> **注意**：`temperature` 在 Qwen 系列模型中默认为 `0.8`，但 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 示例中统一设为 `0.3` 以提升确定性——生产环境应显式传参，不可依赖默认值。

## 使用方式

1. **API 调用**：通过 `/v1/chat/completions`（文本）、`/v1/images/generations`（图像）、`/v1/videos/generations`（视频）等标准路径发起 POST 请求  
2. **控制台调试**：在「模型服务」→「在线调试」中选择对应模型，粘贴 Prompt 或上传文件后直接运行  
3. **SDK 集成**：Python SDK 中 `Bailian` 客户端已封装多模态请求逻辑，推荐使用 `bailian.ImageGenerationClient` 或 `bailian.VideoGenerationClient` 分离调用  
4. **批量处理**：文档转视频等长耗时任务需异步轮询 `job_id`，参考 [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)

## 限制和注意事项

- **配额与限流**：默认每分钟 60 次请求（TPM），单次文生视频最大时长 8 秒；超出需申请提升，详见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)  
- **缓存策略**：显式缓存（`cache_level=2`）仅对完全相同的 `model`+`prompt`+`parameters` 组合生效，且不跨版本；[显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md) 明确禁止在 `seed` 变动场景下启用  
- **合规要求**：声音克隆、数字人生成必须完成实名认证与内容安全备案；未备案调用将返回 `403 Forbidden`  
- **文件限制**：上传文档转视频时，PDF/PPTX 单文件 ≤ 50MB，文本长度 ≤ 10,000 字符；超限需预处理分片  
- **地域约束**：实时音视频接入（WebRTC）仅支持 `cn-shanghai` 和 `cn-beijing` 区域，其他地域需代理中转，参考 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


