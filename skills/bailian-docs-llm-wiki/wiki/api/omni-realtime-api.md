# omni realtime api

Qwen-Omni-Realtime API 是阿里云百炼平台提供的实时多模态交互接口，基于 WebSocket 协议实现低延迟的音频/视频/文本双向通信。该 API 支持 Qwen3.5-Omni-Realtime、Qwen3-Omni-Flash-Realtime、Qwen-Omni-Turbo-Realtime 等多个模型系列，适用于语音对话、音视频理解、工具调用等场景。

## 支持的模型

当前 Qwen-Omni-Realtime API 涵盖以下模型系列：

| 模型系列 | 默认音色 | 特有能力 |
| --- | --- | --- |
| Qwen3.5-Omni-Realtime（含 plus/flash） | Tina | 语义 VAD（`semantic_vad`）、联网搜索、工具调用、静默超时主动响应 |
| Qwen3-Omni-Flash-Realtime | Cherry | `smooth_output` 口语化/书面化控制 |
| Qwen-Omni-Turbo-Realtime | Chelsie | 参数不可修改（temperature、top_p 等固定） |

各模型的采样参数默认值有差异，详见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)中 `session.update` 的参数说明。

## 交互模式

Qwen-Omni-Realtime API 提供两种交互模式，详细流程参见[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### VAD 模式（默认）

将 `session.turn_detection` 设为 `"server_vad"` 或 `"semantic_vad"` 启用。服务端自动检测语音起止并触发模型响应，适用于持续发送音频流的场景。

核心事件流：
1. 客户端通过 `input_audio_buffer.append` 持续发送音频
2. 服务端检测到语音开始，发送 `input_audio_buffer.speech_started`
3. 服务端检测到语音结束，发送 `input_audio_buffer.speech_stopped`
4. 服务端自动提交缓冲区并生成响应

VAD 配置参数：

- **threshold**：灵敏度，取值 `[-1.0, 1.0]`，默认 0.5。值越低越灵敏
- **silence_duration_ms**：静音触发时间，取值 `[200, 6000]`，默认 800ms
- **idle_timeout_ms**：静默超时（仅 qwen3.5-omni-plus/flash-realtime + server_vad），取值 `[5000, 30000]`，超时后模型主动引导对话

### Manual 模式

将 `session.turn_detection` 设为 `null` 启用。客户端手动调用 `input_audio_buffer.commit` 提交音频，再发送 `response.create` 触发响应。适用于"按下即说"等场景。

## 客户端事件

客户端通过 WebSocket 向服务端发送以下事件，完整参数定义参见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

| 事件 | 用途 |
| --- | --- |
| `session.update` | 更新会话配置（模态、音色、VAD、工具等） |
| `input_audio_buffer.append` | 追加 Base64 编码的 PCM 音频（16kHz） |
| `input_audio_buffer.commit` | 提交音频缓冲区（Manual 模式必需） |
| `input_audio_buffer.clear` | 清空音频缓冲区 |
| `input_image_buffer.append` | 追加 Base64 编码的图片（JPG/JPEG，最大 1080p） |
| `response.create` | 手动触发模型响应 |
| `response.cancel` | 取消进行中的响应 |
| `conversation.item.create` | 回传工具调用结果（`function_call_output`） |

## 服务端事件

服务端通过 WebSocket 向客户端推送事件，完整定义参见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

关键事件包括：

- **会话管理**：`session.created`、`session.updated`、`error`
- **音频缓冲区**：`input_audio_buffer.speech_started`、`speech_stopped`、`committed`、`cleared`
- **语音转录**：`conversation.item.input_audio_transcription.delta`（实时中间结果，含 `text` + `stash` 拼接机制）、`conversation.item.input_audio_transcription.completed`
- **响应生成**：`response.created`、`response.audio.delta`、`response.audio_transcript.delta`、`response.text.delta`、`response.done`
- **工具调用**：`response.function_call_arguments.delta`、`response.function_call_arguments.done`

> **注意**：语音转录由内置模型 `qwen3-asr-flash-realtime` 处理，不支持修改。转录结果可能与 Omni 模型的理解存在差异，仅供参考。

## 关键参数

### 会话配置（session.update）

| 参数 | 说明 |
| --- | --- |
| `modalities` | 输出模态：`["text"]` 或 `["text", "audio"]`（默认） |
| `voice` | 音色，支持预置音色和声音复刻音色 |
| `input_audio_format` | 输入格式，仅支持 `pcm`（16kHz） |
| `output_audio_format` | 输出格式，仅支持 `pcm`（24kHz） |
| `instructions` | 系统消息，设定角色/目标 |
| `smooth_output` | 口语化控制（仅 Qwen3-Omni-Flash-Realtime） |
| `enable_search` | 联网搜索（仅 Qwen3.5-Omni-Realtime） |
| `tools` | 工具定义列表（仅 Qwen3.5-Omni-Realtime） |

> **注意**：`tools` 和 `enable_search` 不兼容，不可同时开启。

### 采样参数

各模型系列的默认值不同，`qwen-omni-turbo` 系列不支持修改这些参数：

| 参数 | qwen3.5-omni-realtime | qwen3-omni-flash-realtime | qwen-omni-turbo-realtime |
| --- | --- | --- | --- |
| temperature | 0.7 | 0.9 | 1.0 |
| top_p | 0.8 | 1.0 | 0.01 |
| top_k | 20 | 50 | 20 |
| repetition_penalty | 1.0 | 1.05 | 1.05 |
| presence_penalty | 1.5 | 0.0 | 0.0 |

## 工具调用（Function Calling）

Qwen3.5-Omni-Realtime 模型支持工具调用。通过 `session.update` 的 `tools` 字段定义工具函数，模型可自主判断是否调用。调用流程：

1. 服务端识别到需要调用工具，发送 `response.function_call_arguments.done`（含 `call_id` 和参数）
2. 客户端本地执行工具函数
3. 客户端通过 `conversation.item.create` 回传结果（`type: "function_call_output"`，带上 `call_id`）
4. VAD 模式下服务端自动生成最终响应；Manual 模式下需额外发送 `response.create`

## SDK 接入

### Python SDK

需要 `dashscope >= 1.25.17`。核心类为 `OmniRealtimeConversation`，通过回调（`OmniRealtimeCallback`）接收服务端事件。关键方法参见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

```python
from dashscope.audio.qwen_omni import OmniRealtimeConversation, OmniRealtimeCallback, MultiModality

conv = OmniRealtimeConversation(model="qwen3.5-omni-flash-realtime", callback=callback)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice="Tina",
    enable_turn_detection=True
)
# 持续发送音频
conv.append_audio(audio_base64)
```

### Java SDK

需要 `dashscope-sdk-java >= 2.22.15`。核心类为 `OmniRealtimeConversation`，通过 `OmniRealtimeParam` 和 `OmniRealtimeConfig` 配置参数。关键接口参见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

```java
OmniRealtimeParam param = OmniRealtimeParam.builder()
    .model("qwen3.5-omni-flash-realtime")
    .build();
OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, callback);
conversation.connect();
conversation.updateSession(OmniRealtimeConfig.builder()
    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
    .voice("Tina")
    .enableTurnDetection(true)
    .build());
```

WebSocket 连接地址：
- 北京地域：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- 新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`（推荐使用业务空间专属域名）

## 声音复刻

Qwen-Omni-Realtime 支持声音复刻功能，仅需 10~20 秒音频即可生成定制音色。流程为"先创建音色，后在对话中使用"。声音复刻使用 `qwen-voice-enrollment` 模型，需通过 `target_model` 指定驱动音色的全模态模型，且后续对话必须使用相同模型。详细参数和接口参见[声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

音频要求：WAV/MP3/M4A 格式，10~20 秒（最长 60 秒），采样率不低于 24kHz，单声道，文件小于 10MB，需包含至少 3 秒连续清晰朗读。

支持的驱动模型：`qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-omni-plus`、`qwen3.5-omni-flash`。

## 限制与注意事项

- 音频格式固定：输入 PCM 16kHz，输出 PCM 24kHz，不支持自定义采样率
- 图片输入要求 JPG/JPEG，Base64 编码后不超过 256KB，建议 1 帧/秒，发送前需先发过至少一次音频
- `semantic_vad` 仅 `qwen3.5-omni-realtime` 支持
- `qwen-omni-turbo` 系列不支持修改采样参数
- 工具调用命中时模型不生成音频，仅返回工具调用参数
- 语音转录模型固定为 `qwen3-asr-flash-realtime`，不可更换

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


