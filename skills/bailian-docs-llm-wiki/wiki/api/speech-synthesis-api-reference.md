# speech synthesis api reference

百炼平台提供多种语音合成（TTS）模型和 API，支持将文本转换为自然语音。当前主要包含三大引擎：Qwen-TTS（千问语音合成，含非实时和实时两种模式）、CosyVoice（大模型语音合成）和 Sambert（传统语音合成），以及声音复刻能力。各引擎在接口协议、支持的功能和适用场景上有所不同，开发者可按需选择。

## 语音合成引擎概览

| 引擎 | 接口协议 | 流式输入 | 适用场景 |
|------|---------|---------|---------|
| Qwen-TTS（非实时） | HTTP REST | 支持[流式输出](../concepts/streaming.md) | 短文本离线合成 |
| Qwen-TTS-Realtime | WebSocket（Realtime API） | 支持（duplex） | 实时交互、低延迟场景 |
| CosyVoice | WebSocket | 支持（continue-task） | 实时流式合成 |
| Sambert | WebSocket | 不支持（run-task 一次性发送） | 传统 TTS、多发音人 |

## Qwen-TTS 非实时语音合成

Qwen-TTS 非实时 API 通过 HTTP REST 接口调用，使用 `MultiModalConversation` 统一接口（旧 `SpeechSynthesizer` 接口已统一合并），支持流式和非流式两种输出模式。详见 [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)。

### 关键参数

- **model**：`qwen3-tts-flash`（标准）或 `qwen3-tts-instruct-flash`（支持指令控制）
- **text**：待合成文本
- **voice**：音色名称，如 `Cherry`
- **language_type**：语种，如 `Chinese`、`English`
- **instructions**（仅 instruct 模型）：语音风格指令
- **optimize_instructions**：是否优化指令以提升自然度

### 调用方式

支持 Python SDK、Java SDK 和 curl 调用。以 Python 为例：

```python
import dashscope

response = dashscope.MultiModalConversation.call(
    model="qwen3-tts-flash",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    text="待合成文本",
    voice="Cherry"
)
```

## Qwen-TTS-Realtime 实时语音合成

Qwen-TTS-Realtime 基于 WebSocket 的 Realtime API 协议，支持流式文本输入和实时音频输出。与 CosyVoice/Sambert 的传统 WebSocket 协议不同，采用 session 管理和事件驱动模型。详见 [Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)。

### 服务端点

- 北京：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime`

### 两种交互模式

- **ServerCommit 模式**（默认）：服务端智能判断文本分段与合成时机，开发者无需关心内部状态切分
- **Commit 模式**：客户端控制每段文本的提交时间，需显式调用 `input_text_buffer.commit` 触发合成

### 核心客户端事件

| 事件 | 说明 |
|------|------|
| `session.update` | 配置音色、格式、模式等会话参数 |
| `input_text_buffer.append` | 追加待合成文本到缓冲区 |
| `input_text_buffer.commit` | 提交缓冲区触发合成 |
| `input_text_buffer.clear` | 清空文本缓冲区 |
| `session.finish` | 通知服务端结束会话 |

详细客户端和服务端事件说明见 [客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-client-events.md) 和 [服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-server-events.md)。

### 关键会话参数

- **voice**：音色，支持系统音色和声音复刻/声音设计的专属音色
- **mode**：`server_commit`（默认）或 `commit`
- **response_format**：`pcm`（默认）、`wav`、`mp3`、`opus`
- **sample_rate**：8000、16000、24000（默认）、48000
- **speech_rate**：语速，范围 [0.5, 2.0]，默认 1.0
- **language_type**：语种，默认 `Auto`，支持中英日韩等 10 种语言

SDK 支持 Python（≥1.25.11）和 Java（≥2.22.7），详见 [Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-java-sdk.md)。

## CosyVoice 语音合成

CosyVoice 使用传统 WebSocket 协议，支持流式文本输入（通过多次发送 `continue-task` 事件按顺序提交文本片段）。服务端接收到完整语句后自动合成，不完整语句缓存至完整后再合成。详见 [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)。

### 服务端点

- 北京：`wss://dashscope.aliyuncs.com/api-ws/v1/inference`
- 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`

### 交互流程

1. 建立 WebSocket 连接
2. 发送 `run-task` 事件开启任务
3. 收到 `task-started` 确认
4. 通过 `continue-task` 发送待合成文本（支持多次发送）
5. 通过 binary 通道接收音频流
6. 发送 `finish-task` 结束任务
7. 收到 `task-finished` 后关闭连接

> **注意**：同一次合成任务中，`run-task`、所有 `continue-task`、`finish-task` 必须使用相同的 `task_id`。建议复用 WebSocket 连接处理多个任务。

CosyVoice 的服务端事件包括 `task-started`、`result-generated`（含 `sentence-begin`/`sentence-synthesis`/`sentence-end` 子类型）、`task-finished` 和 `task-failed`，详见 [CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)。

## Sambert 语音合成

Sambert 仅支持北京地域，使用 WebSocket 协议但不支持流式输入——所有待合成文本必须在 `run-task` 事件中一次性发送（`streaming` 固定为 `out`）。详见 [Sambert WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-websocket-api.md)。

### 关键参数

- **model**：如 `sambert-zhichu-v1`
- **format**：`pcm`、`wav`（默认）、`mp3`
- **sample_rate**：8000、16000（默认）、22050、24000
- **volume**：音量，范围 [0, 100]，默认 50
- **rate**：语速，范围 [0.5, 2.0]，默认 1.0
- **pitch**：音调，范围 [0.5, 2.0]，默认 1.0
- **word_timestamp_enabled**：是否开启字级别时间戳
- **phoneme_timestamp_enabled**：是否开启音素级别时间戳（需先开启 word_timestamp）

### SDK 支持

Sambert 提供多平台 SDK：

- **Python SDK**：通过 `SpeechSynthesizer` 类调用，支持非流式和单向流式两种模式。详见 [语音合成Sambert Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-python-sdk.md)
- **Java SDK**：同样提供 `SpeechSynthesizer` 类，支持非流式（`call`）和流式（`ResultCallback`）调用。详见 [语音合成Sambert Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-java-sdk.md)
- **Android SDK**：原生 SDK，通过 `NativeNui` 类调用。详见 [语音合成Sambert Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-android-sdk.md)
- **iOS SDK**：原生 SDK，通过 `NeoNuiTts` 类调用。详见 [语音合成Sambert iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-ios-sdk.md)

> **注意**：Android 和 iOS SDK 的参数类型均为 `String`（而非数值类型），需注意类型转换。

## 声音复刻

声音复刻支持通过上传音频样本创建自定义音色，创建后可在语音合成时使用。支持 CosyVoice 和 Qwen-TTS 两种复刻方案。详见 [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)。

### CosyVoice 声音复刻

- **model**：`voice-enrollment`
- **target_model**：如 `cosyvoice-v3.5-plus`
- 通过 `url` 参数提供公网可访问的音频文件
- 支持 `language_hints` 指定样本语种
- 支持 `max_prompt_audio_length`（参考音频最大时长，3.0~30.0 秒）和 `enable_preprocess`（音频预处理）

### Qwen 声音复刻

- **model**：`qwen-voice-enrollment`
- **target_model**：如 `qwen3-tts-vc-realtime-2026-01-15`
- 通过 `audio` 参数提供 Base64 编码音频或音频 URL
- 支持 `text` 参数提供音频对应文本以提升复刻效果

### Python SDK

CosyVoice 复刻通过 `VoiceEnrollmentService` 类管理音色生命周期（创建、查询、更新、删除）。详见 [声音复刻Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-python-sdk.md)。

```python
from dashscope.audio.tts_v2 import VoiceEnrollmentService

service = VoiceEnrollmentService()
voice_id = service.create_voice(
    target_model='cosyvoice-v3-plus',
    prefix='myvoice',
    url='https://your-audio-file-url'
)
```

## 鉴权与地域

所有语音合成 API 均需要通过 API Key 进行鉴权：
- HTTP 接口：请求头 `Authorization: Bearer <your_api_key>`
- WebSocket 接口：握手阶段请求头携带 `Authorization: Bearer <your_api_key>`

支持地域：
- **华北2（北京）**：默认地域，所有引擎均支持
- **新加坡**：CosyVoice 和 Qwen-TTS 支持，Sambert 不支持

> **注意**：新加坡地域的旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，请及时迁移到新版域名 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。北京和新加坡地域的 API Key 不同，请使用对应地域的 Key。

## 限制与注意事项

- Sambert 仅支持北京地域，不支持流式输入
- Qwen-TTS-Realtime 的旧版 `千问-TTS-Realtime` 模型仅支持 `pcm` 格式和 24000 采样率，且不支持语速、音量、音调调节
- CosyVoice 和 Sambert 的 WebSocket 协议与 Qwen-TTS-Realtime 的 Realtime API 协议不同，不可混用
- 声音复刻的 `target_model` 必须与后续语音合成调用时使用的模型一致，否则合成会失败
- DashScope Python SDK 的 `SpeechSynthesizer` 接口已统一为 `MultiModalConversation`，旧接口仍兼容

## 来源文档

- [非实时语音合成（Qwen-TTS）API参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-api.md)
- [CosyVoice WebSocket API参考](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-websocket-api.md)
- [CosyVoice服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)
- [Sambert客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-client-events.md)
- [Sambert WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-websocket-api.md)
- [Sambert服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-server-events.md)
- [语音合成Sambert Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-java-sdk.md)
- [语音合成Sambert Android SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-android-sdk.md)
- [语音合成Sambert Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-python-sdk.md)
- [Qwen-TTS-Realtime WebSocket API 参考](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/interactive-process-of-qwen-tts-realtime-synthesis.md)
- [语音合成Sambert iOS SDK](../../raw/model-api-reference/speech-synthesis-api-reference/sambert-speech-synthesis/sambert-ios-sdk.md)
- [客户端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-client-events.md)
- [服务端事件](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-server-events.md)
- [Python SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/speech-synthesis-api-reference/qwen-tts-realtime-api-reference/qwen-tts-realtime-java-sdk.md)
- [声音复刻HTTP API参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-http-api.md)
- [声音复刻Python SDK参考](../../raw/model-api-reference/speech-synthesis-api-reference/sound-reengraving/voice-clone-design-python-sdk.md)







