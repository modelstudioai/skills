# use cases

百炼平台提供覆盖文本、图像、视频、语音等多模态内容生成与理解的完整能力矩阵，支持从基础 [Prompt 工程](../concepts/prompt-engineering.md)、RAG 应用构建，到实时音视频交互、第三方模型集成等多样化场景。本文档结构化梳理核心使用方式、关键参数、限制条件及最佳实践，面向开发者提供可直接落地的技术参考。

## 支持的模型/功能

百炼支持三类核心模型能力：  
- **文生文（LLM）**：包括通义千问系列（qwen3.x）、Kimi、GLM、MiniMax、DeepSeek、Stepfun、MiMo、Unisound 等数十种第三方直供模型，均通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope SDK 调用；所有模型均支持 `enable_thinking`（或等效参数如 `thinking`、`reasoning_effort`）控制思考模式，部分模型（如 `kimi/kimi-k2.6`、`ZHIPU/GLM-5.3`）支持 `preserve_thinking` 在多轮对话中传递推理过程 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)。  
- **文生图/图生图**：万相系列（`wan-image-api-reference/text-to-image-v2-api-reference.md`）支持 `prompt`（正向提示词）、`negative_prompt`（反向提示词）及 `prompt_extend`（智能改写开关，默认开启）；Vidu 视频生成则提供更细粒度的运镜、动态、风格等维度控制 [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)。  
- **文生视频/图生视频**：万相视频模型（`text-to-video-api-reference.md`）采用分层提示词公式，基础为 `主体 + 场景 + 运动`，进阶支持 `美学控制` 与 `风格化`；Vidu 还额外支持 `声音描述`（人声/音效/BGM）和 `多镜头公式`（含时间戳与分镜内容）[文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)。  
- **实时音视频**：通过 WebRTC 或 AOQ 协议接入 `qwen3.8-omni-flash-realtime`、`fun-asr-realtime`、`qwen-audio-3.1-realtime-plus` 等模型，支持服务端 VAD 自动轮次划分或客户端 Manual 模式按键控制 [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)。  
- **RAG 与知识库**：基于 LlamaIndex 集成，支持 `DashScopeParse` 文档解析器（`.pdf/.doc/.docx`，单文件 ≤100MB、≤1000页），并自动上传至百炼知识库服务 [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)。

> **注意**：多个文档对同一模型的下架时间存在不一致表述。例如，`kimi-k2-instruct` 在 [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md) 中标注下架时间为“2026年7月9日”，而 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 中 `kimi/kimi-k2.5` 的下架时间为“2026年8月31日”。实际以百炼控制台最新公告为准，建议优先选用推荐替代模型（如 `qwen3.7-plus`）。

## 关键参数

| 参数名 | 适用模型 | 说明 | 示例值 |
|--------|----------|------|--------|
| `prompt` / `input.prompt` | 文生文、文生图、文生视频 | 正向提示词，描述期望输出内容的核心指令 | `"一只柯基幼犬在大泳池里游泳"` |
| `negative_prompt` | 文生图（万相V1/V2） | 明确排除不希望出现的元素 | `"人物,文字,水印"` |
| `prompt_extend` | 万相文生图V2 | 是否启用大模型智能扩写提示词，默认 `true` | `true` |
| `enable_thinking` | Kimi、GLM、DeepSeek、Stepfun、MiMo、Unisound 等 | 开启思考模式，返回 `reasoning_content` 字段 | `true` |
| `reasoning_effort` | Kimi、GLM、Stepfun、Unisound | 控制思考深度，可选 `low`/`medium`/`high`/`max`/`xhigh` | `"max"` |
| `preserve_thinking` | Kimi（kimi-k2.6+）、GLM（glm-5.2+） | 多轮对话中保留并复用上一轮推理过程 | `true` |
| `server_vad` / `semantic_vad` | qwen3.8-omni-flash-realtime、qwen-audio-3.1-realtime-plus | 服务端语音活动检测模式，用于自动划分对话轮次 | `"semantic_vad"` |
| `turn_detection: null` | qwen3.8-omni-flash-realtime（Manual 模式） | 客户端完全控制音频提交与回复触发时机 | `null` |

## 使用方式

1. **[Prompt 工程](../concepts/prompt-engineering.md)**：  
   - 文生文推荐使用结构化 Prompt 框架（背景+目的+风格+语气+受众+输出），并善用 [Prompt一键优化工具](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 进行自动扩写；  
   - 文生图/视频需按公式组织提示词：基础公式（主体+场景+运动/风格）→ 进阶公式（增加镜头语言、氛围词、细节修饰）；Vidu 还需明确指定运镜（如 `镜头推进`）和动态强度（如 `大动态`）。

2. **第三方模型调用**：  
   - 统一使用华北2（北京）专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（推荐迁移自 `dashscope.aliyuncs.com`）；  
   - 思考模式参数必须通过 `extra_body`（Python SDK）或顶层参数（Node.js SDK）传入，不可置于 `messages` 中；  
   - 所有模型均需配置 `DASHSCOPE_API_KEY` 及业务空间 ID，且仅华北2（北京）地域支持大部分直供模型（如 DeepSeek-万擎、MiniMax-稀宇科技、GLM-智谱）。

3. **实时音视频接入**：  
   - WebRTC 方案适用于浏览器端低延迟场景，需处理 `RTCPeerConnection` 生命周期、媒体流获取与轨道添加；  
   - AOQ 方案适用于移动端（Android/iOS/HarmonyOS），需导入 `AoqClientSdk` 及 `PluginOpus` 插件，并严格遵循 [Token](../concepts/token.md) 鉴权流程（API Key 严禁暴露于客户端）；  
   - Manual 模式下，客户端需显式调用 `input_audio_buffer.commit` 和 `response.create` 触发模型响应。

4. **RAG 应用构建**：  
   - 使用 `DashScopeParse` 解析本地文档后，通过 `DashScopeCloudIndex.from_documents()` 创建知识库；  
   - 检索器（`DashScopeCloudRetriever`）可直接基于知识库名称初始化，无需加载全部文档。

## 限制和注意事项

- **限流机制**：百炼 API 按主账号、模型独立计算 RPM（每分钟请求数）、TPM（每分钟 [Token](../concepts/token.md) 数）、RPS（每秒请求数）、TPS（每秒 [Token](../concepts/token.md) 数）及 Traffic Burst（突发流量）五维限流。`429` 错误需结合 [错误诊断表](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md) 定位具体维度，推荐优先尝试服务端排队等待（加 `X-DashScope-Queue-Enable: true` 请求头）。
- **缓存策略**：显式缓存（`cache_control`）仅在 Anthropic 协议兼容端点（如 `qwen3.7-max`）原生支持，Claude Code、OpenCode 等工具默认启用；普通 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)不支持该特性。
- **地域与模型绑定**：除通义千问系列外，绝大多数第三方模型（Kimi、GLM、MiniMax、DeepSeek、Stepfun、MiMo、Unisound）**仅在华北2（北京）地域可用**，且必须使用业务空间专属域名，跨地域调用将失败。
- **文件与资源限制**：`DashScopeParse` 解析器单文件上限为 100MB 且 ≤1000 页；实时音视频方案中，WebRTC 受浏览器 CORS 限制，SDP 交换需后端代理；AOQ 方案要求客户端权限申请（`RECORD_AUDIO` 必须，`CAMERA` 按需）。
- **模型弃用风险**：大量第三方模型已明确标注下架时间（如 `kimi-k2-instruct`、`MiniMax-M2.1`、`glm-4.6`、`deepseek-v3` 系列等），生产环境应避免依赖即将下架模型，并及时迁移到推荐替代型号。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [文生视频/图生视频Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)


