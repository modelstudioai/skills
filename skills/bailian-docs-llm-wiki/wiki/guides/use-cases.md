# use cases

百炼平台提供覆盖文本、图像、视频、语音、实时交互等多模态场景的完整能力矩阵，支持从基础 Prompt 工程到复杂 RAG 应用、自定义模型调优及端侧实时音视频集成的全栈用例。开发者可根据业务需求选择合适的技术路径，所有能力均通过统一 API 接入，并受平台级限流与缓存机制统一管理。

## 支持的模型/功能

百炼支持三类核心模型能力：  
- **文生文（LLM）**：包括 Qwen 系列（如 `qwen3.7-max`）、三方直供模型（如 `deepseek-v4-pro`、`kimi/kimi-k3`、`ZHIPU/GLM-5.3`、`MiniMax/MiniMax-M2.7`、`xiaomi/mimo-v2.5-pro`、`stepfun/step-3.7-flash`、`unisound/unisound-u2`），均支持 `enable_thinking` 或 `reasoning_effort` 参数控制思考模式 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)；  
- **文生图/图生图**：万相系列（`wan-image-api-reference/text-to-image-v2-api-reference.md`）支持 `prompt` 与 `negative_prompt` 双参数及 `prompt_extend` 智能改写；  
- **文生视频/图生视频**：万相视频模型（`text-to-video-api-reference.md`）支持多镜头公式、声音公式及运镜控制；Vidu 视频生成模型（[Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)）提供细粒度动态、运镜、风格词典；  
- **实时音视频**：`qwen3.5-omni-plus-realtime`、`qwen-audio-3.0-realtime-plus`、`fun-asr-realtime` 等模型通过 WebRTC 或 AOQ 协议接入，支持服务端 VAD 与 Manual 模式双路控制 [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)；  
- **RAG 与文档处理**：基于 LlamaIndex 的 `DashScopeCloudIndex` 支持文档解析、知识库构建与检索增强 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)；  
- **文档转视频**：端到端流水线支持文档切片、PPT 生成、语音合成与视频合成。

> **注意**：多个三方模型文档存在下架时间冲突。例如，`deepseek-v3.2`（[DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)）与 `deepseek-v3`（[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)）均标注将于 2026 年 10 月 10 日下架，但推荐迁移目标不一致（前者推 `qwen3.7-plus`，后者亦推 `qwen3.7-plus`）；而 `kimi-k2-thinking`（[Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)）下架时间为 2026 年 7 月 9 日，`kimi/kimi-k2.5`（[Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)）为 2026 年 8 月 31 日。开发者应以控制台实际可用模型为准，优先选用 `qwen3.x` 系列。

## 关键参数

| 功能类型 | 参数名 | 说明 | 示例值 |
|----------|--------|------|--------|
| **文生文** | `enable_thinking` / `reasoning_effort` | 控制思考模式开关与深度 | `{"enable_thinking": true, "reasoning_effort": "max"}` |
| **文生图** | `prompt`, `negative_prompt`, `prompt_extend` | 正向提示词、反向提示词、是否启用大模型智能扩写 | `"prompt_extend": true` |
| **文生视频** | `prompt`, `motion`, `aesthetic_control`, `style` | 主体+场景+运动为基础，支持美学控制与风格化 | `"镜头推进", "赛博朋克"` |
| **Vidu 视频** | `dynamic_control`, `camera_movement`, `composition` | 动态强度、运镜指令、构图方式 | `"大动态", "镜头拉远", "三分构图"` |
| **实时音视频（Manual）** | `turn_detection: null` | 客户端显式控制轮次起止 | 配合 `input_audio_buffer.commit` 和 `response.create` |
| **实时音视频（VAD）** | `server_vad`, `semantic_vad` | 服务端自动语音活动检测 | `"server_vad"` |
| **显式缓存** | `cache_control` | 在 message 中标记可缓存片段 | `{"type": "ephemeral"}` |

## 使用方式

- **Prompt 工程**：文生文推荐使用 [Prompt框架](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)，包含背景、目的、风格、语气、受众、输出六要素；文生图/视频需按公式组织（如“主体+场景+运动”基础公式或“主体描述+场景描述+运动描述+美学控制+风格化”进阶公式）；  
- **API 调用**：所有模型统一通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或 DashScope SDK 调用，需配置地域专属 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）并传入 `model` 名称；  
- **RAG 构建**：使用 `DashScopeParse` 解析文档，`DashScopeCloudIndex.from_documents()` 创建知识库，再通过 `index.as_retriever()` 获取检索器；  
- **实时交互**：WebRTC 方案需浏览器调用 `navigator.mediaDevices.getUserMedia()` 获取媒体流，AOQ 方案需客户端集成 SDK 并由 AppServer 代理 Token 鉴权；  
- **缓存优化**：在 Anthropic 协议兼容客户端（如 Claude Code、OpenCode）中启用 `cache_control` 标记，或在请求中手动注入 `cache_control` 字段。

## 限制和注意事项

- **限流约束**：API 按 RPM/TPM（分钟级）、RPS/TPS（瞬时）、Traffic Burst（增速）三维度限流，错误码 `Throttling.RateQuota` 对应请求频率超限，`Throttling.AllocationQuota` 对应 Token 用量超限 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
- **地域绑定**：绝大多数三方直供模型（如 DeepSeek-硅基流动、Kimi-月之暗面、GLM-智谱、MiniMax-稀宇科技、MiMo-小米、Stepfun-阶跃星辰、Unisound-云知声）仅支持华北2（北京）地域，且必须使用该地域的 API Key 与业务空间 ID；  
- **缓存成本**：显式缓存首次写入产生标准价格 25% 额外开销，但后续命中可节省 90% 成本，适用于高频复用相同 Prompt 的工业级 Agent 场景；  
- **文件限制**：`DashScopeParse` 文档解析器要求单个 `.pdf/.doc/.docx` 文件 ≤100MB 且 ≤1000 页；  
- **安全规范**：API Key 必须保存于服务端（AppServer），严禁硬编码至客户端代码或提交至代码仓库；移动端需动态申请 `RECORD_AUDIO` 权限，iOS/HarmonyOS 需在 Info.plist/module.json5 中声明权限用途；  
- **协议差异**：AOQ 接入需区分 `Realtime` 协议（用于 `qwen3.5-omni-plus-realtime`）与 `Inference` 协议（用于 `fun-asr-realtime`、`qwen-audio-3.0-tts-flash`），二者事件语义与轨设计不同。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/use-aoq-to-access-qwen3-5-omni-plus-realtime-to-realize-key-voice-dialogue.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/speech-synthesis-using-aoq-access-qwen-audio-3-0-tts-flash.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-speech-recognition-using-aoq-access-fun-asr-realtime.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [使用 AOQ 接入 qwen-audio-3.0-realtime-plus 实现实时语音对话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/real-time-voice-conversation-using-aoq-access-qwen-audio-3-0-realtime-plus.md)


