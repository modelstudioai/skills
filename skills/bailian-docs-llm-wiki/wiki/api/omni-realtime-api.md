# omni realtime api

Qwen-Omni-Realtime API 是百炼平台提供的实时多模态交互接口，基于 WebSocket 协议实现低延迟的语音、文本和图像双向流式通信。该 API 支持 Qwen3.5-Omni-Realtime、Qwen3-Omni-Flash-Realtime 和 Qwen-Omni-Turbo-Realtime 三个系列模型，适用于实时语音对话、音视频交互和声音复刻等场景。

## 支持的模型

| 模型系列 | 代表模型 | 特性 |
| --- | --- | --- |
| Qwen3.5-Omni-Realtime | qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime | 支持语义 VAD、联网搜索、工具调用、静默超时主动引导、声音复刻 |
| Qwen3-Omni-Flash-Realtime | qwen3-omni-flash-realtime | 支持 `smooth_output` 口语化/书面化风格控制 |
| Qwen-Omni-Turbo-Realtime | qwen-omni-turbo-realtime | 基础实时对话，多数生成参数不支持修改 |

各模型在默认参数上存在差异，详见下方参数说明。关于完整模型列表可参考 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的参数默认值说明。

## 交互模式

Qwen-Omni-Realtime API 提供两种交互模式，详细流程参见 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### VAD 模式（默认）

将 `session.turn_detection` 设为 `"server_vad"` 或 `"semantic_vad"` 启用。服务端自动检测语音起止并触发模型响应，适用于持续音频流输入场景。

- **server_vad**：基于声学特征检测语音结束，所有模型均支持。
- **semantic_vad**：基于语义有效性检测，可过滤回应语和背景音，仅 `qwen3.5-omni-realtime` 系列支持。

VAD 关键参数：

| 参数 | 说明 | 默认值 | 范围 |
| --- | --- | --- | --- |
| threshold | VAD 灵敏度，值越低越灵敏 | 0.5 | [-1.0, 1.0] |
| silence_duration_ms | 静音多久后触发响应 | 800 | [200, 6000] |
| idle_timeout_ms | 静默超时后模型主动引导对话（仅 qwen3.5-omni-plus/flash-realtime + server_vad） | - | [5000, 30000] |

### Manual 模式

将 `session.turn_detection` 设为 `null` 启用。客户端通过 `input_audio_buffer.commit` 提交音频，再发送 `response.create` 手动触发模型响应。适用于按下即说等需要精确控制发送节奏的场景。

## 客户端事件

客户端通过 WebSocket 向服务端发送以下事件，完整参数定义参见 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

| 事件 | 用途 |
| --- | --- |
| `session.update` | 更新会话配置（模态、音色、VAD、工具、生成参数等） |
| `input_audio_buffer.append` | 追加 Base64 编码的 PCM 音频数据（16 kHz） |
| `input_audio_buffer.commit` | 提交音频缓冲区（Manual 模式必需） |
| `input_audio_buffer.clear` | 清空音频缓冲区 |
| `input_image_buffer.append` | 追加 Base64 编码的图像数据（JPG/JPEG，建议 480p-720p，单张不超过 256KB） |
| `response.create` | 触发模型生成响应（Manual 模式或工具调用后使用） |
| `response.cancel` | 取消正在进行的响应 |
| `conversation.item.create` | 回传工具函数执行结果 |

## 服务端事件

服务端通过 WebSocket 下发的主要事件，完整定义参见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

| 事件 | 说明 |
| --- | --- |
| `session.created` / `session.updated` | 连接建立/配置更新确认 |
| `input_audio_buffer.speech_started` / `speech_stopped` | VAD 检测到语音起止 |
| `input_audio_buffer.committed` / `cleared` | 缓冲区提交/清空确认 |
| `conversation.item.created` | 对话项创建（用户消息或工具调用） |
| `conversation.item.input_audio_transcription.delta` / `completed` | 实时/最终语音转录结果 |
| `response.created` / `response.done` | 响应开始/完成 |
| `response.audio.delta` / `response.audio_transcript.delta` | 增量音频/文本[流式输出](../concepts/streaming.md) |
| `response.function_call_arguments.delta` / `done` | 工具调用参数[流式输出](../concepts/streaming.md) |
| `error` | 错误信息 |

## 关键参数

### 音频格式

- **输入音频**：仅支持 PCM，16 kHz 采样率。
- **输出音频**：仅支持 PCM，24 kHz 采样率，不支持自定义。

### 音色配置

通过 `session.update` 的 `voice` 字段设置，各模型默认音色不同：

- Qwen3.5-Omni-Realtime 系列：`Tina`
- Qwen3-Omni-Flash-Realtime：`Cherry`
- Qwen-Omni-Turbo-Realtime：`Chelsie`

### 生成参数

| 参数 | Qwen3.5-Omni-Realtime 默认 | Qwen3-Omni-Flash-Realtime 默认 | Qwen-Omni-Turbo-Realtime 默认 |
| --- | --- | --- | --- |
| temperature | 0.7 | 0.9 | 1.0（不可改） |
| top_p | 0.8 | 1.0 | 0.01（不可改） |
| top_k | 20 | 50 | 20（不可改） |
| repetition_penalty | 1.0 | 1.05 | 1.05（不可改） |
| presence_penalty | 1.5 | 0.0 | 0.0（不可改） |

> **注意**：`qwen-omni-turbo` 系列模型的 temperature、top_p、top_k、repetition_penalty、presence_penalty、max_tokens、seed 均不支持修改。

## 工具调用（Function Calling）

仅 Qwen3.5-Omni-Realtime 模型支持。在 `session.update` 中通过 `tools` 字段定义工具列表，模型可自主判断是否调用。工具调用流程：

1. 服务端识别到需要调用工具，通过 `response.function_call_arguments.done` 返回参数和 `call_id`。
2. 客户端执行工具函数，通过 `conversation.item.create` 回传结果（`type` 为 `function_call_output`）。
3. 发送 `response.create`（Manual 模式）或等待服务端自动生成响应（VAD 模式）。

> **注意**：`tools` 和 `enable_search` 不兼容，不可同时开启。

## 联网搜索

仅 Qwen3.5-Omni-Realtime 模型支持。设置 `enable_search: true` 启用，模型可自主判断是否需要联网搜索来回答问题。通过 `search_options.enable_source` 可获取搜索结果来源列表。

## 声音复刻

通过 `qwen-voice-enrollment` 模型，上传 10-20 秒音频即可创建专属复刻音色，无需训练。创建时必须指定 `target_model`，后续调用 Omni 接口时使用的模型必须与之一致。详细的音频要求和接口参数参见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。

支持复刻的驱动模型：qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime、qwen3.5-omni-plus、qwen3.5-omni-flash。

音频要求摘要：WAV/MP3/M4A 格式，采样率不低于 24 kHz，单声道，文件小于 10 MB，包含至少 3 秒连续清晰朗读。

## SDK 支持

百炼提供 Python SDK 和 Java SDK 调用 Qwen-Omni-Realtime API，SDK 封装了 WebSocket 连接管理和事件回调。

### Python SDK

通过 `dashscope.audio.qwen_omni` 模块引入，SDK 版本需不低于 1.25.17。核心类 `OmniRealtimeConversation` 提供 `connect()`、`update_session()`、`append_audio()`、`append_video()`、`commit()`、`create_response()`、`create_item()` 等方法。详见 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

### Java SDK

通过 `com.alibaba.dashscope.audio.omni.OmniRealtimeConversation` 引入，SDK 版本需不低于 2.22.15。使用 `OmniRealtimeParam` 构建连接参数，`OmniRealtimeConfig` 更新会话配置。详见 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。

### 调用地址

- 北京地域：`wss://dashscope.aliyuncs.com/api-ws/v1/realtime`
- 新加坡地域：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`（推荐使用[业务空间](../concepts/workspace.md)专属域名）

## 图像输入限制

- 格式：JPG 或 JPEG
- 分辨率：建议 480p 或 720p，最高 1080p
- 大小：Base64 编码后不超过 256KB（原始图片建议不超过 190KB）
- 频率：建议 1 张/秒
- 前置条件：发送图像前至少已发送过一次音频数据

## 实时语音转录

输入音频转录由内置模型 `qwen3-asr-flash-realtime` 处理，不支持修改。转录事件 `conversation.item.input_audio_transcription.delta` 提供实时中间结果（`text` + `stash` 拼接获取当前预览），`completed` 事件提供最终结果。

> **注意**：语音识别模型生成的转录文本可能与 Qwen-Omni-Realtime 模型的理解存在差异，仅供参考。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)




