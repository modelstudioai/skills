# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟、多模态实时交互接口，支持语音输入/输出、文本、图像及工具调用等能力。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时反馈处理结果。该 API 专为语音助手、智能客服、实时音视频交互等场景设计。

## 支持的模型/功能

当前支持以下实时系列模型：
- `qwen3.5-omni-plus-realtime`
- `qwen3.5-omni-flash-realtime`
- `qwen3-omni-flash-realtime`
- `qwen-omni-turbo-realtime`

各模型能力存在差异：  
- **VAD 类型**：`semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持；`server_vad` 为通用默认选项 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。  
- **联网搜索（`enable_search`）**：仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 不兼容 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。  
- **声音复刻音色**：需在复刻时指定 `target_model`，且后续调用 Omni Realtime API 时必须使用**完全一致的模型名**，否则合成失败 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)。  
> **注意**：文档 2（服务端事件）中称 `output_audio_format` “当前仅支持设为 `pcm`” 且“不支持自定义输出采样率”，但文档 1 明确列出 `wav` 和 `24000` Hz 为合法值，并在示例中使用；SDK 文档（3、4）也支持 `wav` 和可配置采样率。以文档 1 和 SDK 行为为准，服务端文档此处已过时。

核心功能包括：
- 实时语音识别（ASR）与流式转录（`conversation.item.input_audio_transcription.delta`）
- 多模态响应生成（文本 + 音频同步输出）
- 语音活动检测（VAD）自动启停（`server_vad` / `semantic_vad`）
- 工具调用（Function Calling）与结果回传
- 图像理解（`input_image_buffer.append`）
- 自定义音色（Tina/Cherry/Chelsie 或声音复刻音色）

## 关键参数

所有参数均通过 `session.update` 事件或 SDK 的 `update_session` 方法配置。关键参数按功能分组如下：

| 参数 | 类型 | 说明 | 模型限制 |
|------|------|------|----------|
| `modalities` | `["text"]` 或 `["text","audio"]` | 输出模态，默认 `["text","audio"]` | 全系列支持 |
| `voice` | `string` | 音色名称。默认值：`qwen3.5-omni-*`: `Tina`；`qwen3-omni-flash-*`: `Cherry`；`qwen-omni-turbo-*`: `Chelsie` | 全系列支持 |
| `audio.input.format` / `audio.output.format` | `{type: "pcm"\|"wav", sample_rate: 8000\|16000\|24000\|48000}` | 输入/输出音频格式与采样率。推荐输入 `pcm`/`16000`，输出 `wav`/`24000` | `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime` |
| `turn_detection.type` | `"server_vad"`（默认）或 `"semantic_vad"` | VAD 类型 | `semantic_vad` 仅 `qwen3.5-omni-realtime` 系列支持 |
| `turn_detection.threshold` | `float [-1.0, 1.0]` | VAD 灵敏度，默认 `0.5` | 全系列支持 |
| `turn_detection.silence_duration_ms` | `int [200, 6000]` | 静音触发响应阈值，默认 `800` ms | 全系列支持 |
| `idle_timeout_ms` | `int [5000, 30000]` | 静默超时主动引导时间（仅 `server_vad` + `qwen3.5-omni-plus-realtime`/`flash-realtime`） | 限定模型 |
| `enable_search` | `boolean` | 启用联网搜索 | 仅 `qwen3.5-omni-realtime` 系列支持，且与 `tools` 互斥 |
| `tools` | `array` of `function` objects | 工具定义列表 | 仅 `qwen3.5-omni-realtime` 系列支持，且与 `enable_search` 互斥 |
| `temperature` / `top_p` / `top_k` | `float` / `float` / `int` | 采样控制参数。建议只设置 `temperature` 或 `top_p` 之一 | `qwen-omni-turbo` 系列不支持修改 |
| `max_tokens` | `int` | 响应最大 [Token](../concepts/token.md) 数，超长将被截断 | `qwen-omni-turbo` 系列不支持修改 |
| `repetition_penalty` / `presence_penalty` | `float` | 重复惩罚参数 | `qwen-omni-turbo` 系列不支持修改 |
| `seed` | `int` | 生成确定性种子 | `qwen-omni-turbo` 系列不支持修改 |

## 使用方式

### 连接与初始化
1. 使用 WebSocket URL 建立连接（推荐业务空间专属域名）：  
   - 北京：`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`  
   - 新加坡：`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime`  
   （`{WorkspaceId}` 从百炼控制台获取）[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)。

2. 连接后，服务端立即返回 `session.created` 事件，包含默认配置。

### 两种交互模式
- **VAD 模式（默认）**：`session.turn_detection.type = "server_vad"`。客户端持续 `append_audio`，服务端自动检测语音起止（`speech_started`/`speech_stopped`），并提交缓冲区（`input_audio_buffer.committed`）。无需手动发 `response.create`，服务端自动触发响应 [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。  
- **Manual 模式**：`session.turn_detection = null`。客户端控制节奏：`append_audio` → `commit`（创建用户消息）→ `response.create`（触发响应） [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)。

### 工具调用流程
1. 模型在 `response.function_call_arguments.done` 中返回 `call_id`；  
2. 客户端执行本地工具，得到结果；  
3. 发送 `conversation.item.create` 事件回传 `output`；  
4. VAD 模式下服务端自动响应；Manual 模式下需再发 `response.create`。

### 图像输入
通过 `input_image_buffer.append` 发送 Base64 编码的 JPG/JPEG 图像（≤256KB，建议 480p/720p）。**必须先发送至少一次 `input_audio_buffer.append`**，且图像与音频缓冲区由同一 `commit` 提交 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。

## 限制和注意事项

- **音频格式**：输入推荐 `pcm`/`16000Hz`；输出推荐 `wav`/`24000Hz`。`qwen-omni-turbo` 系列不支持修改音频参数。
- **图像限制**：单图 Base64 ≤ 256KB，格式仅 JPG/JPEG，分辨率建议 ≤1080p，发送频率 ≤1 张/秒 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)。
- **并发与超时**：`idle_timeout_ms` 仅在 `server_vad` + `qwen3.5-omni-plus-realtime`/`flash-realtime` 下生效，范围 `[5000, 30000]` ms。
- **互斥配置**：`enable_search` 与 `tools` 不可同时启用，否则参数校验失败。
- **SDK 兼容性**：Python SDK 要求 ≥1.26.5，Java SDK 要求 ≥2.22.15 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)、[Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)。
- **错误处理**：服务端返回 `error` 事件（含 `code` 和 `message`），例如 `invalid_value` 表示参数非法 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)。

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


