# omni realtime api

Qwen-Omni-Realtime API 是阿里云百炼平台提供的实时[多模态](../concepts/multimodal.md)交互接口，基于 WebSocket 协议实现低延迟的音视频对话。该 API 支持语音输入/输出、图像输入、语音活动检测（VAD）、工具调用（Function Calling）、联网搜索及声音复刻等功能，适用于智能客服、语音助手等实时对话场景。

## 支持的模型

| 模型系列 | 模型名称 | 特性 |
| --- | --- | --- |
| Qwen3.5-Omni-Realtime | qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime | 支持 semantic_vad、联网搜索、工具调用、idle_timeout_ms |
| Qwen3-Omni-Flash-Realtime | qwen3-omni-flash-realtime | 支持 smooth_output 参数 |
| Qwen-Omni-Turbo-Realtime | qwen-omni-turbo-realtime | 大部分生成参数不支持修改 |

各模型的默认音色不同：Qwen3.5-Omni-Realtime 系列为 `Tina`，Qwen3-Omni-Flash-Realtime 为 `Cherry`，Qwen-Omni-Turbo-Realtime 为 `Chelsie`。

## 交互模式

根据[实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)，API 支持两种交互模式：

### VAD 模式（默认）

将 `session.turn_detection` 设为 `server_vad` 或 `semantic_vad`。服务端自动检测语音起止并触发模型响应，适用于持续音频流场景。支持语音打断。

### Manual 模式

将 `session.turn_detection` 设为 `null`。客户端通过 `input_audio_buffer.commit` + `response.create` 手动控制对话节奏，适用于按下即说场景。

## 连接地址

```
wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime   # 北京地域
wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime  # 新加坡地域
```

将 `{WorkspaceId}` 替换为[业务空间](../concepts/workspace.md) ID。建议使用[业务空间](../concepts/workspace.md)专属域名以获得更好的性能和稳定性。

## 客户端事件

详细参数说明参见[客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

| 事件 | 用途 |
| --- | --- |
| `session.update` | 更新会话配置（模态、音色、VAD、工具等） |
| `input_audio_buffer.append` | 追加音频数据（Base64 编码） |
| `input_audio_buffer.commit` | 提交音频缓冲区（Manual 模式必需） |
| `input_audio_buffer.clear` | 清空音频缓冲区 |
| `input_image_buffer.append` | 追加图像数据（JPG/JPEG，Base64 编码） |
| `response.create` | 触发模型生成响应 |
| `response.cancel` | 取消正在进行的响应 |
| `conversation.item.create` | 回传工具调用结果 |

## 服务端事件

详细参数说明参见[服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

| 事件 | 含义 |
| --- | --- |
| `session.created` | 连接建立，返回默认配置 |
| `session.updated` | 会话配置更新成功 |
| `error` | 错误信息 |
| `input_audio_buffer.speech_started` | VAD 检测到语音开始 |
| `input_audio_buffer.speech_stopped` | VAD 检测到语音结束 |
| `input_audio_buffer.committed` | 音频缓冲区已提交 |
| `response.audio.delta` | 增量音频输出 |
| `response.audio_transcript.delta` | 增量文本转录 |
| `response.done` | 响应完成 |
| `response.function_call_arguments.done` | 工具调用参数完成 |
| `conversation.item.input_audio_transcription.delta` | 实时语音识别中间结果 |

## 关键会话参数

通过 `session.update` 事件配置：

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `modalities` | 输出模态：`["text"]` 或 `["text","audio"]` | `["text","audio"]` |
| `voice` | 音色名称 | 因模型而异 |
| `input_audio_format` | 输入音频格式，仅支持 `pcm`（16kHz） | `pcm` |
| `output_audio_format` | 输出音频格式，仅支持 `pcm`（24kHz） | `pcm` |
| `instructions` | 系统消息 | - |
| `turn_detection.type` | VAD 类型：`server_vad` / `semantic_vad` | `server_vad` |
| `turn_detection.threshold` | VAD 灵敏度，范围 [-1.0, 1.0] | 0.5 |
| `turn_detection.silence_duration_ms` | 静音触发时间（ms），范围 [200, 6000] | 800 |
| `turn_detection.idle_timeout_ms` | 静默超时（ms），范围 [5000, 30000]，仅 qwen3.5 系列 | - |
| `enable_search` | 联网搜索，仅 Qwen3.5-Omni-Realtime | `false` |
| `tools` | 工具定义列表，仅 Qwen3.5-Omni-Realtime | `[]` |
| `smooth_output` | 口语化风格，仅 Qwen3-Omni-Flash-Realtime | `true` |

> **注意**：`tools` 和 `enable_search` 不兼容，不可同时开启。

### 生成参数

| 参数 | Qwen3.5-Omni-Realtime | Qwen3-Omni-Flash-Realtime | Qwen-Omni-Turbo-Realtime |
| --- | --- | --- | --- |
| `temperature` | 0.7 | 0.9 | 1.0（不可改） |
| `top_p` | 0.8 | 1.0 | 0.01（不可改） |
| `top_k` | 20 | 50 | 20（不可改） |
| `repetition_penalty` | 1.0 | 1.05 | 1.05（不可改） |
| `presence_penalty` | 1.5 | 0.0 | 0.0（不可改） |

> **注意**：`qwen-omni-turbo` 系列模型的生成参数不支持修改。

## SDK 使用

### Python SDK

需要 [DashScope SDK](../concepts/dashscope-sdk.md) >= 1.25.17。核心类为 `OmniRealtimeConversation`，通过 `from dashscope.audio.qwen_omni import OmniRealtimeConversation` 引入。详见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

```python
from dashscope.audio.qwen_omni import MultiModality, OmniRealtimeCallback, OmniRealtimeConversation

conv = OmniRealtimeConversation(model="qwen3.5-omni-plus-realtime", callback=callback, url=url)
conv.connect()
conv.update_session(
    output_modalities=[MultiModality.AUDIO, MultiModality.TEXT],
    voice="Tina",
    enable_turn_detection=True
)
conv.append_audio(audio_base64)
conv.close()
```

### Java SDK

需要 DashScope Java SDK >= 2.22.15。核心类为 `OmniRealtimeConversation`，通过 `OmniRealtimeParam` 和 `OmniRealtimeConfig` 配置参数。详见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

```java
OmniRealtimeParam param = OmniRealtimeParam.builder()
    .model("qwen3.5-omni-plus-realtime")
    .url(url)
    .build();
OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, callback);
conversation.connect();
conversation.updateSession(OmniRealtimeConfig.builder()
    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
    .voice("Tina")
    .enableTurnDetection(true)
    .build());
```

> **注意**：Java SDK 中 `instructions`、`smooth_output`、`enable_search`、`search_options`、`tools` 及生成参数（temperature/top_p/top_k 等）需通过 `OmniRealtimeConfig` 的 `parameters` 方法设置。

## 工具调用（Function Calling）

仅 Qwen3.5-Omni-Realtime 模型支持。流程如下：

1. 通过 `session.update` 配置 `tools` 列表
2. 服务端识别到需要调用工具时，通过 `response.function_call_arguments.done` 返回函数名和参数
3. 客户端执行工具函数，通过 `conversation.item.create` 回传结果（`type: "function_call_output"`）
4. VAD 模式下服务端自动生成响应；Manual 模式下需额外发送 `response.create`

## 声音复刻

通过 `qwen-voice-enrollment` 模型创建自定义音色，然后在实时对话中使用。音频要求：WAV/MP3/M4A 格式，10-20 秒，采样率 >= 24kHz，单声道，文件 < 10MB。创建音色时指定的 `target_model` 必须与后续对话使用的模型一致。

支持的驱动模型：qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime。

## 输入限制

- 音频输入：16kHz 采样率 PCM，音频缓冲区最大 15MiB
- 图像输入：JPG/JPEG 格式，建议 480p-720p（最高 1080p），Base64 编码后不超过 256KB，建议 1 帧/秒
- 图像需在至少一次 `input_audio_buffer.append` 之后发送，通过 `input_audio_buffer.commit` 与音频一起提交

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)









