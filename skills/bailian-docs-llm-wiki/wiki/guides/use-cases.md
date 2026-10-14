# use cases

百炼平台的 use cases 覆盖从基础 Prompt 工程到复杂智能体构建、多模态生成及 RAG 应用落地的完整技术路径。所有实践均基于平台当前支持的模型能力与 API 行为，强调可复现性与工程稳定性。开发者应优先参考各子场景对应的专项指南，避免直接套用过时参数或接口模式。

## 支持的模型/功能

- **文本生成类**：Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL（多模态理解）、Qwen-Audio（语音理解）  
- **图像生成类**：万相 2.1 / 3.0（支持文生图、图生图、局部重绘）  
- **视频生成类**：万相 3.0 视频生成（text-to-video）、支持帧率、分辨率、时长等可控参数  
- **语音类**：声音克隆（需上传参考音频）、TTS（支持音色、语速、停顿精细控制）  
- **智能体与应用框架**：Hermes Agent（支持工具调用、记忆管理、自进化机制），LlamaIndex 集成（[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）  
- **第三方扩展**：支持通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)接入外部模型（详见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)）

> **注意**：文档中提及的“万相3.0视频生成Prompt指南”与“视频生成Prompt指南”存在内容重叠，且后者未标注版本号；实际开发中请以 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 为准，该文档明确要求 `model=wanx-v3` 且禁用 `stream=true`。

## 关键参数

| 场景 | 必填参数 | 推荐可选参数 | 说明 |
|------|----------|----------------|------|
| 文生文 | `model`, `input.messages` | `parameters.temperature`, `top_p`, `max_tokens` | `temperature` 建议 0.1–0.8，高确定性任务设为 ≤0.3 |
| 文生图 | `model=wanx`, `input.prompt` | `size`, `n`, `style`, `seed` | `size` 必须为 `"1024*1024"` 或 `"768*768"`（万相2.1）；万相3.0 支持 `"1920*1080"` |
| 视频生成 | `model=wanx-v3`, `input.prompt` | `duration`, `fps`, `aspect_ratio` | `duration` 仅支持 `2s` 或 `4s`；`aspect_ratio` 限 `"16:9"` 或 `"9:16"` |
| RAG 构建 | `model`, `retriever` 配置 | `cache_enabled`, `enable_citation` | 缓存需显式启用（见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)） |

## 使用方式

- 所有 use cases 均通过统一 `/v1/services/aigc/*` API 路径调用，具体 endpoint 由 `model` 参数隐式决定（如 `model=qwen-max` → `/v1/services/aigc/text`）  
- Prompt 工程需严格遵循对应指南格式：文生文推荐使用 [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)，文生图必须按 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md) 结构化描述主体、风格、构图  
- Hermes Agent 需配置 `tools` 列表与 `memory` 类型（`short_term`/`long_term`），初始化后通过 `POST /v1/agents/hermes/run` 提交用户输入  

## 限制和注意事项

- **速率限制**：免费版默认 5 QPS，超出将返回 `429`；生产环境务必实现退避重试，并参考 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)  
- **输入长度**：Qwen 系列最大上下文为 32768 tokens，但部分部署实例（如 `qwen-plus`）实际限制为 16384；建议始终校验 `input.tokens` 字段反馈  
- **多模态输入**：Qwen-VL 不支持 base64 图片嵌入，必须传 `image_url` 且域名在白名单内；音频同理，仅接受 OSS 或阿里云 CDN URL  
- **缓存行为**：API 默认不启用响应缓存；若需复用结果，必须显式设置 `cache_enabled=true` 并提供稳定 `input` 哈希（参见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)）  
- **数字人/声音克隆**：涉及隐私数据，所有训练样本与生成结果均不落盘，但需用户自行完成《个人信息处理同意书》签署（见 [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md) 附录）

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


