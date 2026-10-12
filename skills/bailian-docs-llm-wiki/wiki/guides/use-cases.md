# use cases

百炼平台的 use cases 覆盖从基础文本生成到[多模态](../concepts/multi-modal.md)实时交互的完整技术谱系，核心围绕“如何用 Prompt 精准驱动模型”和“如何通过 API/SDK 集成模型能力”两大主线。开发者可根据任务类型（文生文、文生图、文生视频、RAG、实时音视频等）选择对应的最佳实践路径，并需重点关注模型支持范围、关键参数配置及限流与缓存等生产级约束。

## 支持的模型/功能

百炼平台提供三类核心能力：  
- **文本生成类**：支持 Qwen 系列（如 `qwen3.7-max`）、三方直供模型（如 `DeepSeek-v4-pro`、`kimi/kimi-k3`、`ZHIPU/GLM-5.3`、`MiniMax-M2.7`、`xiaomi/mimo-v2.5-pro`、`stepfun/step-3.7-flash`、`unisound/unisound-u2`）等，均支持思考模式（`enable_thinking` 或 `reasoning_effort` 参数）与流式响应；  
- **[多模态](../concepts/multi-modal.md)生成类**：覆盖 `万相-文生图V2`、`万相3.0 视频生成`、`Vidu` 等专用模型，支持正向/反向提示词（`prompt`/`negative_prompt`）、智能改写（`prompt_extend`）及多维度控制（镜头、风格、动态、运镜等）；  
- **实时交互类**：基于 `qwen3.8-omni-flash-realtime`、`qwen-audio-3.1-realtime-plus`、`fun-asr-realtime` 等模型，通过 WebRTC 或 AOQ 协议实现低延迟音视频通话、语音合成与实时语音识别；  
- **增强与工程化类**：提供 RAG（基于 LlamaIndex 的 `DashScopeCloudIndex`）、自定义模型调优（微调+部署+评测）、显式缓存（`cache_control` 标记）、限流应对（服务端排队、客户端拥塞控制）等生产就绪能力。

> **注意**：文档中对 `DeepSeek` 模型的服务来源存在不一致描述。[DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md) 与 [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md) 均被列为独立接入方式，但后者明确指出其“支持更长上下文”，而前者强调“支持联网搜索与上下文缓存”。开发者需根据实际需求（上下文长度 vs. 外部工具调用）选择供应商，不可混用配置。

## 关键参数

不同任务类型的关键参数差异显著，需严格按模型规范设置：  
- **文生文**：通用参数包括 `model`、`messages`、`stream`；思考模式启用需通过非标准字段（如 `extra_body={"enable_thinking": true}` 或 `{"reasoning_effort": "max"}`），详见各三方模型文档；  
- **文生图**：核心为 `prompt`（正向描述）与 `negative_prompt`（负向排除），`万相V2` 额外支持 `prompt_extend: true` 启用大模型智能扩写；  
- **文生视频**：`万相3.0` 使用结构化公式，含 `[分镜 N（起-止秒）：主体 + 场景 + 运动 + 美学控制]`、`[台词]`、`[音效/BGM]`、`[负向清单]` 等模块；`Vidu` 则依赖关键词词典（如“左移”、“微距”、“宫崎骏风格”）触发特定运镜或风格；  
- **实时交互（AOQ/WebRTC）**：必须配置 `turn_detection`（`null` 表示 Manual 模式，`server_vad` 表示服务端 VAD 模式），且音频编码强制为 Opus；  
- **显式缓存**：需在请求消息中显式添加 `cache_control: {"type": "ephemeral"}`（Anthropic 协议兼容方式），系统据此确定性命中缓存；  
- **RAG**：`DashScopeCloudIndex` 初始化时需指定 `DASHSCOPE_WORKSPACE_ID` 环境变量以绑定业务空间，确保文档解析与知识库存储位置一致。

## 使用方式

集成路径分为声明式（Prompt 工程）与编程式（API/SDK）两类：  
- **Prompt 工程**：推荐使用标准化框架提升效果。文生文采用「背景+目的+风格+语气+受众+输出」六要素框架；文生图/视频遵循「主体+场景+风格」基础公式，并按需叠加「镜头语言+氛围词+细节修饰」进阶要素；[文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md) 提供了一键优化工具入口，可自动扩写模糊 Prompt；  
- **API/SDK 调用**：统一使用 `base_url = "https://{WorkspaceId}.{region}.maas.aliyuncs.com"`（推荐新域名）或 `dashscope.aliyuncs.com`（兼容旧域名），并通过 `DASHSCOPE_API_KEY` 认证；三方模型（如 DeepSeek、Kimi）需确认地域限制（多数仅华北2可用）并替换 `{WorkspaceId}`；  
- **实时音视频**：WebRTC 方案需浏览器端创建 `RTCPeerConnection` 并处理 `ontrack` 回调播放远端流；AOQ 方案需客户端集成 SDK 并实现 `run-task`/`finish-task` 事件驱动流程，所有凭证必须由业务 AppServer 代理签发，严禁 API Key 泄露至前端；  
- **RAG 应用**：使用 `DashScopeParse` 解析本地文件（支持 PDF/DOCX，单文件 ≤100MB），再通过 `DashScopeCloudIndex.from_documents()` 创建云端知识库，最后用 `index.as_retriever()` 获取检索器；  
- **自定义模型**：全流程在控制台完成：准备 ChatML 格式训练数据（≥500 条）→ 启动「模型调优」→ 部署至独占实例 → 「[模型评测](../concepts/model-evaluation.md)」验证效果，未部署模型不可调用。

## 限制和注意事项

- **限流策略**：百炼 API 按主账号、模型维度独立限制 RPM/TPM（分钟级）、RPS/TPS（瞬时）及 Traffic Burst（增速）。突发流量建议优先启用「服务端排队等待」（加 `X-DashScope-Queue-Enable: true` 请求头），而非简单重试；高并发场景需结合客户端令牌桶或架构层 MQ 削峰；详情参见 [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)；  
- **地域与域名**：绝大多数三方模型（DeepSeek、Kimi、GLM、MiniMax 等）仅支持华北2（北京）地域，且强烈推荐使用业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 以获得更高稳定性；  
- **安全合规**：API Key 必须通过环境变量或服务端 [Token](../concepts/token.md) 代理传递，禁止硬编码于客户端代码；上传训练数据前须完成脱敏（移除 PII 敏感信息）；  
- **缓存成本**：显式缓存首次写入产生 25% 额外开销，但后续命中可节省 90% 成本；若跨会话命中率低（如 Claude Code 默认注入动态 git 状态），应启用 `--exclude-dynamic-system-prompt-sections` 参数；  
- **模型下架风险**：注意 [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md) 文档明确提示 `kimi/kimi-k2.5` 将于 2026年8月31日下架，应尽快迁移至 `kimi-k2.6` 或其他替代模型。

## 来源文档

- [文生文Prompt指南](../../raw/model-user-guide/use-cases/prompt-engineering-guide.md)
- [文生图Prompt指南](../../raw/model-user-guide/use-cases/text-to-image-prompt.md)
- [万相3.0视频生成Prompt指南](../../raw/model-user-guide/use-cases/wan3-video-generation-prompt-guide.md)
- [视频生成Prompt指南](../../raw/model-user-guide/use-cases/text-to-video-prompt.md)
- [基于LlamaIndex构建RAG应用](../../raw/model-user-guide/use-cases/build-rag-applications-based-on-llamaindex.md)
- [自定义模型调优、部署与评测](../../raw/model-user-guide/use-cases/model-training-best-practices.md)
- [借助大模型将文档转换为视频](../../raw/model-user-guide/use-cases/use-llm-to-convert-document-to-video.md)
- [限流应对最佳实践](../../raw/model-user-guide/use-cases/rate-limiting-best-practices.md)
- [显式缓存最佳实践](../../raw/model-user-guide/use-cases/explicit-cache-guide.md)
- [三方模型调用教程](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial.md)
- [DeepSeek-阿里云](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)
- [DeepSeek-硅基流动](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/siliconflow-deepseek-api.md)
- [DeepSeek](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api-by-vanchin.md)
- [Kimi](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)
- [Kimi-月之暗面](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api-by-moonshot-ai.md)
- [GLM](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api.md)
- [GLM-智谱](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/glm-zhipu.md)
- [MiMo-小米](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/mimo.md)
- [Stepfun-阶跃星辰](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/stepfun.md)
- [MiniMax](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/minimax-api-by-minimax.md)
- [实时音视频接入](../../raw/model-user-guide/use-cases/realtime-audio-video-integration.md)
- [通过WebRTC使用多模态交互套件实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-multimodal-dialog.md)
- [Unisound-云知声](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/unisound-cloud-sound.md)
- [通过WebRTC使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-webrtc-omni-realtime.md)
- [使用 AOQ 接入 qwen3.8-omni-flash-realtime 实现按键语音对话](../../raw/_short/use-aoq-to-access-qwen3-5-omni-plus-realtime-to--dee7ca70112bd23e.md)
- [使用 AOQ 接入 qwen-audio-3.1-realtime-plus 实现实时语音对话](../../raw/_short/real-time-voice-conversation-using-aoq-access-qw-7e2ab540f9ffd31d.md)
- [使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成](../../raw/_short/speech-synthesis-using-aoq-access-qwen-audio-3-0-43022e91dedcb0c1.md)
- [使用 AOQ 接入 fun-asr-realtime 实现实时语音识别](../../raw/_short/real-time-speech-recognition-using-aoq-access-fu-1f528aaba4a8fd1b.md)
- [技术解决方案](../../raw/model-user-guide/use-cases/technical-solutions.md)
- [通过AOQ使用qwen3.8-omni-flash-realtime实现实时通话](../../raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
- [Vidu视频生成Prompt指南](../../raw/model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md)


