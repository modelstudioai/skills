# use cases

百炼平台的 use cases 覆盖从基础 [Prompt 工程](../concepts/prompt.md)到复杂智能体构建、多模态生成及 RAG 应用落地的完整技术路径。所有实践均基于平台当前支持的模型能力与 API 行为，强调可复现性与工程稳定性。开发者应优先参考各子场景对应的专项指南，避免直接套用过时参数或接口模式。

## 支持的模型/功能

- **文本生成类**：Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）、Qwen-VL（多模态理解）、Qwen-Audio（语音理解）  
- **图像生成类**：万相 2.1 / 3.0（支持文生图、图生图、局部重绘）  
- **视频生成类**：万相 3.0 视频生成（text-to-video）、支持帧率、分辨率、时长等可控参数  
- **语音类**：声音克隆（需上传参考音频）、TTS（支持音色、语速、停顿精细控制）  
- **智能体与应用框架**：Hermes Agent（支持工具调用、记忆管理、自进化机制），LlamaIndex 集成（[基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)）  
- **第三方扩展**：支持通过标准 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)接入外部模型（详见 [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)）

> **注意**：文档中提及的“万相3.0视频生成Prompt指南”与“视频生成Prompt指南”存在内容重叠，且后者未标注版本号；实际开发中请以 [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md) 为准，该文档已同步更新至 v3.0 API 的 `video_generation` 参数规范。

## 关键参数

- **通用参数**：`model`（必填，如 `qwen-max`, `wanx-v3`）、`temperature`（0.0–2.0）、`top_p`（0.1–1.0）、`max_tokens`（上限依模型而异）  
- **多模态专用**：`input_images`（base64 或 URL 列表，Qwen-VL）、`audio_url`（Qwen-Audio）、`voice_id`（声音克隆场景）  
- **视频生成专用**：`aspect_ratio`（`16:9`/`9:16`/`1:1`）、`duration`（秒，仅万相3.0支持）、`motion_intensity`（低/中/高）  
- **缓存控制**：`cache_level`（0=禁用，1=自动，2=显式，需配合 `cache_key` 使用；参见 [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)）

## 使用方式

1. **调用入口**：统一通过 `/v1/chat/completions`（文本）、`/v1/images/generations`（图像）、`/v1/videos/generations`（视频）等 RESTful 接口  
2. **Prompt 构建**：严格遵循各场景指南——例如文生图需使用结构化 prompt 模板（含 `subject`, `style`, `lighting` 等字段），详见 [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)  
3. **Agent 开发**：Hermes Agent 需配置 `tools` 描述与 `memory` schema，初始化后通过 `agent.run()` 启动循环；完整流程见 [Hermes Agent，打造自进化智能体](../../raw/model-user-guide/use-cases.md)  
4. **RAG 集成**：推荐使用 LlamaIndex 的 `VectorStoreIndex` + 百炼 Embedding 模型（`text-embedding-v3`），索引构建与查询逻辑需与 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md) 保持一致  

## 限制和注意事项

- 单次请求最大 `input_images` 数量为 4 张（Qwen-VL），单张图像分辨率上限 4096×4096  
- 万相视频生成最长支持 8 秒，超时请求将被截断并返回 `status=partial`；生成失败不计入配额但会触发限流熔断  
- 所有涉及用户音频/视频数据的场景（如声音克隆、实时音视频接入），必须在调用前完成隐私合规声明，并确保数据已脱敏（参见 [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md) 中的安全要求）  
- 限流策略按 `project_id` 维度统计，突发流量需结合 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 实施客户端退避与队列缓冲  
- 自定义模型微调产出不可直接用于 Hermes Agent 的 `tool` 执行层，须经 `model.export()` 导出为服务化 endpoint 后再集成

## 来源文档

- [实践教程](../../raw/model-user-guide/use-cases.md)


