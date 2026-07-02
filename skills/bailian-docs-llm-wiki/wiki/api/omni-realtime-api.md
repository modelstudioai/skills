# omni realtime api

Qwen-Omni-Realtime API 是百炼平台提供的实时[多模态](../concepts/multimodal.md)交互接口，基于 WebSocket 长连接实现低延迟的语音（以及视频/图像）对话。它通过客户端事件与服务端事件的双向消息流驱动会话，支持 VAD 自动检测与 Manual 手动控制两种交互模式，并提供声音复刻、工具调用（Function Calling）、联网搜索等能力。本文汇总客户端事件、服务端事件、Python/Java SDK、交互流程与声音复刻 API 的关键参考信息。

## 支持的模型

实时[多模态](../concepts/multimodal.md)交互涉及以下 Qwen-Omni-Realtime 系列模型，默认音色与部分参数默认值因模型而异：

| 模型系列 | 默认音色 | 备注 |
| --- | --- | --- |
| `qwen3.5-omni-realtime`（含 `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime`） | `Tina` | 支持 `semantic_vad`、`enable_search`、`idle_timeout_ms` 等新特性 |
| `qwen3-omni-flash-realtime` | `Cherry` | 支持 `smooth_output` 回复风格控制 |
| `qwen-omni-turbo-realtime` | `Chelsie` | `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed` 均**不支持修改** |

声音复刻场景下，驱动音色的全模态模型必须是 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`、`qwen3.5-omni-plus` 或 `qwen3.5-omni-flash` 之一，且复刻时声明的 `target_model` 必须与后续调用 Omni 接口时指定的模型一致，否则合成失败。详见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

## 调用地址

通过 WebSocket 接入，地域不同地址不同：

- 北京地域：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- 新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`（`{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，建议从 `wss://dashscope-intl.aliyuncs.com` 迁移至该专属域名以获得更好性能与稳定性）

声音复刻接口为 HTTP REST：`https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`（北京），新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` 同路径。

## 交互模式

会话通过 `session.turn_detection` 字段切换两种模式，流程细节参见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### VAD 模式（默认）

将 `session.turn_detection.type` 设为 `server_vad`（或 `semantic_vad`，仅 `qwen3.5-omni-realtime` 支持）启用。服务端自动检测语音起止：

1. 检测到语音开始 → 服务端发送 `input_audio_buffer.speech_started`
2. 客户端随时通过 `input_audio_buffer.append` 追加音频
3. 检测到语音结束 → 服务端发送 `input_audio_buffer.speech_stopped`，并自动提交音频缓冲区（`input_audio_buffer.committed`）
4. 服务端创建用户消息项（`conversation.item.created`）并自动生成响应

关键参数：
- `threshold`：VAD 灵敏度，范围 `[-1.0, 1.0]`，默认 0.5。值越低越灵敏
- `silence_duration_ms`：语音结束后保持静音的最短时间，范围 `[200, 6000]`，默认 800
- `idle_timeout_ms`：静默超时（仅 `qwen3.5-omni-plus-realtime` / `qwen3.5-omni-flash-realtime` 且 `server_vad` 时生效），范围 `[5000, 30000]`，超时后模型主动引导对话

### Manual 模式

将 `session.turn_detection` 设为 `null` 启用，适用于按下即说场景。客户端需显式控制：

1. `input_audio_buffer.append` 追加音频
2. `input_audio_buffer.commit` 提交缓冲区，创建用户消息项
3. `response.create` 触发模型生成响应

> Manual 模式下，关闭 `turn_detection` 时客户端每个事件最多放置 15 MiB 音频；流式发送较小数据块可让 VAD 响应更迅速（针对 SDK 的 `append_audio`）。

## 客户端事件

客户端通过 WebSocket 向服务端发送以下事件，完整字段定义参见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

| 事件 | 作用 |
| --- | --- |
| `session.update` | 建立连接后更新会话默认配置；服务端校验参数后返回 `session.updated` 或 `error` |
| `response.create` | 指示服务端生成响应（VAD 模式自动生成，Manual 模式或工具调用回传结果后需手动发送） |
| `response.cancel` | 取消正在进行的响应 |
| `input_audio_buffer.append` | 将 Base64 音频字节追加到输入音频缓冲区 |
| `input_audio_buffer.commit` | 提交音频缓冲区（Manual 模式必需；VAD 模式由服务端自动提交） |
| `input_audio_buffer.clear` | 清除音频缓冲区 |
| `input_image_buffer.append` | 将 Base64 图像数据追加到图像缓冲区（发送前必须已至少发送过一次 `input_audio_buffer.append`） |
| `conversation.item.create` | 创建对话项；当前仅支持 `function_call_output` 类型，用于回传工具执行结果 |

### 图像输入限制

- 格式：JPG / JPEG，建议 480p 或 720p，最高 1080p
- 单张 Base64 编码后 ≤ 256KB（建议编码前原始大小 ≤ 190KB）
- 建议发送频率 1 张/秒
- 图像缓冲区与音频缓冲区通过 `input_audio_buffer.commit` 一起提交

### session.update 核心参数

- `modalities`：输出模态，`["text"]` 或 `["text","audio"]`（默认）
- `voice`：音色，默认值见上文模型表
- `input_audio_format` / `output_audio_format`：仅支持 `pcm`；输入 16 kHz、输出 24 kHz PCM，不支持自定义输出采样率
- `instructions`：系统消息，设定模型角色
- `turn_detection`：VAD 配置（见上文）
- `enable_search`：仅 `qwen3.5-omni-realtime` 生效，启用联网搜索（与 `tools` 不兼容）
- `search_options.enable_source`：是否返回搜索来源列表
- `tools`：工具定义列表，仅 `qwen3.5-omni-realtime` 生效
- `smooth_output`：仅 `qwen3-omni-flash-realtime` 生效，`true` 口语化（默认）、`false` 书面化、`null` 自动选择
- 采样参数：`temperature` `[0, 2)`、`top_p` `(0, 1.0]`、`top_k` ≥ 0（>100 或 `null` 时禁用，仅 `top_p` 生效）、`max_tokens`、`repetition_penalty` > 0、`presence_penalty` `[-2.0, 2.0]`、`seed` `[0, 2^31−1]`（默认 -1）

> 各模型 `temperature`/`top_p`/`top_k`/`repetition_penalty`/`presence_penalty` 默认值不同，详见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 与 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。`qwen-omni-turbo` 系列上述采样参数均不支持修改。

## 服务端事件

服务端通过回调下发以下事件，完整字段定义参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

| 事件 | 作用 |
| --- | --- |
| `error` | 错误信息，含 `error.type` / `code` / `message` / `param` |
| `session.created` | 连接后第一个事件，返回默认会话配置 |
| `session.updated` | `session.update` 处理成功后返回更新后的完整配置 |
| `input_audio_buffer.speech_started` / `.speech_stopped` | VAD 检测到语音起止 |
| `input_audio_buffer.committed` / `.cleared` | 音频缓冲区提交/清除 |
| `conversation.item.created` | 对话项创建（`message` 或 `function_call`） |
| `conversation.item.input_audio_transcription.delta` | 输入音频转录中间结果（高频） |
| `conversation.item.input_audio_transcription.completed` | 输入音频转录完成 |
| `response.created` / `.output_item.added` / `.content_part.added` / `.audio_transcript.delta` / `.audio.delta` / `.audio_transcript.done` / `.audio.done` / `.content_part.done` / `.output_item.done` / `.done` | 响应生成全生命周期 |
| `response.function_call_arguments.delta` / `.done` | 工具调用参数增量与完成 |

### 输入音频转录

开启 `input_audio_transcription` 后，转录模型固定为 `qwen3-asr-flash-realtime`，不支持修改。`delta` 事件中实时预览句子 = `text`（已确认前缀）+ `stash`（临时草稿后缀），最终结果以 `completed` 事件的 `transcript` 为准。`delta` 还返回 `language`（语种）与 `emotion`（情感：`neutral`/`happy`/`sad`/`angry`/`surprised`/`disgusted`/`fearful`）。

> 转录文本可能与 Qwen-Omni-Realtime 模型的理解存在差异，仅供参考。

## 工具调用（Function Calling）

仅 `qwen3.5-omni-realtime` 模型支持。命中工具调用时模型不生成音频，仅返回工具调用参数。`tools` 与 `enable_search` 不兼容，不可同时开启。

工具定义结构（`tools` 数组项）：
- `type`：固定 `function`
- `function.name`：函数名（必选）
- `function.description`：功能描述（可选）
- `function.parameters`：入参描述，`type` 固定 `object`，含 `properties` 与 `required`

交互流程：
1. 服务端发送 `response.function_call_arguments.delta`（增量）→ `.done`（完成，含 `call_id`）
2. 客户端本地执行工具
3. 客户端发送 `conversation.item.create`，`item.type` 为 `function_call_output`，`call_id` 对应上一步返回值，`output` 为执行结果字符串
4. VAD 模式下服务端自动基于结果生成响应；Manual 模式下客户端需再发送 `response.create` 触发最终响应

## SDK

百炼提供 DashScope Python SDK 与 Java SDK 封装 WebSocket 交互，示例代码位于 [GitHub alibabacloud-bailian-speech-demo](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)，提供音频对话、音视频对话、本地调用三种示例。

### Python SDK

要求 dashscope ≥ 1.25.17。核心类：

- `OmniRealtimeConversation`（`from dashscope.audio.qwen_omni import OmniRealtimeConversation`）
  - `connect()`：建立连接，服务端返回 `session.created` / `session.updated`
  - `update_session(...)`：更新会话配置（`output_modalities`、`voice`、`input_audio_format`、`output_audio_format`、`enable_input_audio_transcription`、`input_audio_transcription_model`、`enable_turn_detection`、`turn_detection_type`、`turn_detection_threshold`、`turn_detection_silence_duration_ms`、`turn_detection_param`、`enable_search`、`search_options`、`tools`、采样参数等）
  - `append_audio(audio_b64)` / `append_video(video_b64)`：追加音视频
  - `clear_appended_audio()`：清空音频缓冲区
  - `commit()`：提交音视频缓冲区
  - `create_response(instructions, output_modalities)`：触发响应
  - `cancel_response()`：取消响应
  - `create_item(item)`：回传工具结果（`item` 含 `type`=`function_call_output`、`call_id`、`output`）
  - `close()` / `get_session_id()` / `get_last_response_id()`

- `OmniRealtimeCallback`（`from dashscope.audio.qwen_omni import OmniRealtimeCallback`）：实现 `on_open()` 与 `on_event(message)` 处理服务端事件

音频格式枚举：`AudioFormat.PCM_16000HZ_MONO_16BIT`（输入）、`AudioFormat.PCM_24000HZ_MONO_16BIT`（输出）；输出模态枚举 `MultiModality.TEXT` / `MultiModality.AUDIO`。

详见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

### Java SDK

要求 dashscope Java SDK ≥ v2.22.15。核心类：

- `OmniRealtimeConversation`（`import com.alibaba.dashscope.audio.omni.OmniRealtimeConversation;`）
  - `connect()` / `updateSession(OmniRealtimeConfig config)` / `appendAudio(String)` / `appendVideo(String)` / `clearAppendedAudio()` / `commit()` / `createResponse(String instructions, List<OmniRealtimeModality> modalities)` / `cancelResponse()` / `createItem(JsonObject item)` / `close()`
- `OmniRealtimeParam`：构造方法配置 `model`、`url`
- `OmniRealtimeConfig`：链式 setter 配置会话参数

> Java SDK 中 `instructions`、`smooth_output`、`enable_search`、`search_options`、`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` 等需通过 `OmniRealtimeConfig` 的 `.parameters(Map.of(...))` 方法设置，与直接 setter 的参数用法不同。详见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

## 声音复刻

声音复刻（Voice Cloning）依托 `qwen-voice-enrollment` 模型，无需训练，仅需 10~20 秒音频即可生成定制音色。流程为"先创建，后使用"：

1. 调用创建音色接口（HTTP POST），指定 `target_model`（驱动音色的全模态模型）与音频，返回 `voice` 音色 ID
2. 调用 Omni 接口（实时或非实时），传入上一步的 `voice`，且模型必须与 `target_model` 一致

### 音频要求

- 格式：WAV（16bit）、MP3、M4A
- 时长：推荐 10~20 秒，最长 ≤ 60 秒
- 文件大小：< 10 MB
- 采样率：≥ 24 kHz，单声道
- 内容：至少 3 秒连续清晰朗读（无背景音），其余部分停顿 ≤ 2 秒；避免背景音乐/噪音/其他人声；使用正常说话音频，不要上传歌曲
- 语言：支持中文、英文、德语等 29 种语言，及东北话、四川话等中文方言

创建音色请求体示例：

```json
{
  "model": "qwen-voice-enrollment",
  "input": {
    "action": "create",
    "target_model": "qwen3.5-omni-plus-realtime",
    "preferred_name": "guanyu",
    "audio": { "data": "data:audio/mpeg;base64,..." }
  }
}
```

响应 `output.voice` 即为复刻音色 ID，后续作为 `voice` 参数传入 `update_session`。完整端到端示例（Python/Java）参见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

## 限制与注意事项

- **模型能力差异**：`semantic_vad`、`enable_search`、`tools`、`idle_timeout_ms` 仅 `qwen3.5-omni-realtime` 系列支持；`smooth_output` 仅 `qwen3-omni-flash-realtime` 系列支持；`qwen-omni-turbo` 系列的采样类参数均不支持修改。
- **音频格式固定**：输入仅支持 16 kHz PCM，输出仅支持 24 kHz PCM，不支持自定义输出采样率。
- **图像输入前置条件**：发送 `input_image_buffer.append` 前必须已至少发送过一次 `input_audio_buffer.append`；图像与音频缓冲区通过 `input_audio_buffer.commit` 一起提交。
- **工具与搜索互斥**：`tools` 和 `enable_search` 不可同时开启。
- **转录仅供参考**：`qwen3-asr-flash-realtime` 转录结果可能与 Omni 模型理解存在差异。
- **声音复刻模型一致性**：复刻时 `target_model` 必须与后续 Omni 调用模型完全一致，否则合成失败。
- **回声风险**：VAD 模式下推荐使用耳机播放音频，避免回声触发误语音打断。
- **地域与域名**：新加坡地域建议使用[业务空间](../concepts/workspace.md)专属域名以获得更好性能；各地域 [API Key](../concepts/api-key.md) 与 URL 不同。
- **max_tokens 不影响生成过程**：超过 `max_tokens` 时响应被截断，适用于控制成本/缩短响应时间场景。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)






