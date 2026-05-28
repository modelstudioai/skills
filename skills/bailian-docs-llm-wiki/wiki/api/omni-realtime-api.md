# omni realtime api

Qwen-Omni-Realtime API 提供基于 WebSocket 的低延迟实时多模态交互能力，支持文本、音频及视频流的实时双向通信。开发者可通过官方 Python/Java SDK 或原生 WebSocket 协议快速接入，实现类真人的语音对话、实时语音打断与智能体应用构建。

## 支持的模型与核心功能
- **核心模型系列**：支持 `qwen3.5-omni-realtime`、`qwen3-omni-flash-realtime`、`qwen-omni-turbo-realtime` 等实时系列模型。完整支持列表请参考 [[模型列表]]。
- **多模态输入输出**：支持 16kHz PCM 音频输入与 24kHz PCM 音频输出，支持实时视频流/图片输入（JPG/JPEG），并支持同时输出文本与音频模态。
- **语音活动检测 (VAD)**：内置 `server_vad`（基于声学特征）与 `semantic_vad`（基于语义有效性，过滤背景音/回应语，仅 3.5 系列支持）两种检测模式，支持自然对话轮转。
- **扩展能力**：支持 [[功能调用]]（Function Calling）与联网搜索（仅 3.5 系列），内置输入音频实时转写（固定使用 `qwen3-asr-flash-realtime` 模型）与情感识别，支持与 [[声音复刻]] 结合使用定制音色。

## 关键参数配置
建立 WebSocket 连接后，服务端会下发 `session.created` 事件返回默认配置。客户端可通过 `session.update` 事件或 SDK 配置方法修改会话参数。核心参数如下：
- **模态与音色**：`modalities` 可选 `["text"]` 或 `["text", "audio"]`（默认）。`voice` 指定音色，不同模型默认音色不同（如 3.5 系列默认 `Tina`，Flash 默认 `Cherry`，Turbo 默认 `Chelsie`）。
- **音频格式**：输入/输出音频格式均固定为 `pcm`，输入采样率 16kHz，输出采样率 24kHz，暂不支持自定义。
- **生成控制**：支持 `temperature`（默认 0.7~1.0）、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed`。建议仅配置 `temperature` 或 `top_p` 其中之一以控制生成多样性。
- **VAD 配置**：`turn_detection.type` 设为 `null` 可关闭自动检测。开启时，`threshold` 控制灵敏度（[-1.0, 1.0]，默认 0.5），`silence_duration_ms` 控制静音触发延迟（[200, 6000]，默认 800ms）。

> **注意**：`qwen-omni-turbo` 系列模型**不支持修改**生成控制参数（如 temperature、top_p、max_tokens、seed 等），传入修改值将被忽略。部分历史文档对 `smooth_output`（仅 Flash 系列生效）默认值的描述存在不一致（原文档标记为 `true`，SDK 文档标记为 `null`/`None`），建议在调用时显式声明所需风格以避免歧义。
> **注意**：工具调用 (`tools`) 与联网搜索 (`enable_search`) **互斥**，同一会话中不可同时启用。

## 交互模式与使用方式
实时交互依赖客户端与服务端的 JSON 事件流双向通信。详细事件结构定义可查阅 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 与 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

1. **[[VAD模式]]（默认推荐）**：适用于全双工语音通话场景。客户端持续通过 `input_audio_buffer.append` 流式上传音频，服务端自动检测语音起止、提交缓冲区并生成响应。模型生成期间若检测到新语音，会自动打断当前回复。完整时序参见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。
2. **[[手动模式]]**：将 `turn_detection` 设为 `null`。适用于“按住说话”场景。客户端需显式发送 `input_audio_buffer.commit` 提交音频，随后发送 `response.create` 手动触发模型响应。
3. **SDK 接入**：
   - Python：需 `dashscope >= 1.25.17`。实例化 `OmniRealtimeConversation` 并传入 `OmniRealtimeCallback` 回调对象处理事件。
   - Java：需 SDK `>= v2.22.15`。通过 `OmniRealtimeParam` 链式配置参数，实现 `OmniRealtimeCallback` 接口。具体实现可参考官方 [[Python SDK]] 与 [[Java SDK]] 示例工程。

## 限制与注意事项
- **缓冲区与分包**：关闭 VAD 时，音频缓冲区单次最多支持 15 MiB。为降低首字延迟，建议客户端按 100ms 小包流式上传音频。
- **图像输入规范**：单张图片 Base64 编码后不得超过 256KB，推荐分辨率 480p/720p。发送 `input_image_buffer.append` 前必须至少发送过一次 `input_audio_buffer.append`。图像不会单独提交，必须通过 `input_audio_buffer.commit` 随音频流一并提交。
- **工具调用回传**：服务端下发 `response.function_call_arguments.done` 后，客户端需在本地执行逻辑，并通过 `conversation.item.create`（`type: "function_call_output"`）将结果传回，最后再次发送 `response.create` 触发最终回复。
- **连接状态管理**：长时间无事件交互或网络异常可能导致 WebSocket 断开。建议基于 SDK 提供的 `on_close` 回调实现状态码监听与指数退避重连机制，并在重连后重新同步会话状态。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)

