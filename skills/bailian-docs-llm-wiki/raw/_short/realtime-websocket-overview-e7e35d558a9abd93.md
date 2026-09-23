# WebSocket 接入概览

了解 WebSocket 的接入地址、鉴权、Realtime 与 Inference 交互流程及各模型的事件差异。

## 前提条件

-   已开通目标模型或应用，并确认其支持的地域。
-   已获取与调用地域、业务空间匹配的 API Key，参见[Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。
-   使用业务空间专属域名时，已获取 [Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

连接协议的选型和支持范围参见 [Realtime API 概述](raw/model-api-reference/realtime-api-user-guide/realtime-api-overview.md)。

## 请求头

在 WebSocket 握手请求中设置 `Authorization`。其余请求头按对应模型的参数说明使用。

请求头

是否必需

说明

`Authorization`

是

使用 `Bearer <API_KEY>` 格式传递 API Key。

`user-agent`

否

标识调用客户端。

`X-DashScope-WorkSpace`

按模型要求

指定业务空间 ID，具体使用方式见对应模型的请求头说明。

`X-DashScope-DataInspection`

按模型要求

数据合规检查配置，支持范围与取值见对应模型的请求头说明。

## 接入地址

使用 `wss://` 协议，根据目标模型选择 API 路径和模型名的传递位置。下表列出各模型的接入方式，支持的模型及地域见对应模型文档。

模型系列

API 路径

模型名传递位置

Qwen-Omni-Realtime

`/api-ws/v1/realtime`

URL 查询参数 `model`

Qwen-Audio-TTS/CosyVoice

`/api-ws/v1/inference`

`run-task` 的 `payload.model`

Qwen-TTS-Realtime

`/api-ws/v1/realtime`

URL 查询参数 `model`

Qwen-Audio-ASR/Fun-ASR/Paraformer

`/api-ws/v1/inference`

`run-task` 的 `payload.model`

Qwen-ASR-Realtime

`/api-ws/v1/realtime`

URL 查询参数 `model`

Qwen-Audio-Realtime

`/api-ws/v1/realtime`

URL 查询参数 `model`

Qwen-LiveTranslate-Realtime

`/api-ws/v1/realtime`

URL 查询参数 `model`

业务空间专属域名：

地域

业务空间专属域名

华北 2（北京）

`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`

新加坡

`{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

将 `{WorkspaceId}` 替换为实际业务空间 ID。例如：

```
wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen3.8-omni-flash-realtime
wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference
```

Qwen-TTS-Realtime 也可使用公共域名：北京为 `dashscope.aliyuncs.com`，新加坡为 `dashscope-intl.aliyuncs.com`，API 路径仍为 `/api-ws/v1/realtime`。API Key 必须与调用地域匹配。

## 公共交互流程

`/api-ws/v1/realtime` 使用会话制协议，`/api-ws/v1/inference` 使用任务制协议。

### Realtime 协议

客户端建立连接后，通过 `session.update` 配置会话，收到 `session.updated` 后发送输入。提交输入、触发响应和结束会话的方式由目标模型决定。

![Realtime 协议的会话配置、输入输出和结束流程](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f92d7.png)

1.  **建立连接**：在 URL 的 `model` 参数中指定模型，在请求头中携带 API Key。握手成功后，服务端发送 `session.created`。
2.  **配置会话**：发送 `session.update`，设置模型支持的音频格式、输出模态、音色或语音检测参数，等待 `session.updated`。各模型支持的会话参数见对应的客户端事件文档。
3.  **发送输入**：音频通过 `input_audio_buffer.append` 发送 Base64 数据；Qwen-TTS 通过 `input_text_buffer.append` 发送文本。支持图像输入的模型使用 `input_image_buffer.append`，并遵循对应模型对图片和音频时序的要求。
4.  **提交并获取结果**：自动模式下由服务端触发处理；手动模式下按输入类型发送 `input_audio_buffer.commit` 或 `input_text_buffer.commit`。是否还需 `response.create`，以及应监听哪些结果事件，参见下方差异对照。
5.  **结束会话**：支持结束事件的模型使用 `session.finish`，等待 `session.finished` 和剩余结果；其他模型在结果接收完成后关闭 WebSocket 连接。`response.done` 表示一次响应结束，不表示整个连接关闭；纯语音识别以转录完成事件标识识别结束。

### Inference 协议

客户端发送 `run-task` 并等待 `task-started` 后，才开始传输输入。语音识别发送二进制音频帧，语音合成通过 `continue-task` 发送文本；输入结束后发送 `finish-task`，等待 `task-finished`。

![Inference 协议的语音识别与语音合成任务流程](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f92eb.png)

1.  **建立连接**：使用 `/api-ws/v1/inference`，在请求头中携带 API Key。
2.  **启动任务**：发送 `run-task`，在 `payload.model` 中指定模型，并设置输入格式等参数。为任务生成唯一的 `header.task_id`，等待 `task-started`。
3.  **传输输入并接收结果**：
    -   语音识别：发送二进制音频帧，通过 `result-generated` 获取识别结果。
    -   语音合成：通过 `continue-task` 的 `payload.input.text` 发送待合成文本，接收二进制音频帧；模型还可能通过 `result-generated` 返回时间戳等信息。
4.  **结束任务**：发送 `finish-task` 后继续接收剩余结果，直到收到 `task-finished`。同一任务的 `run-task`、`continue-task` 和 `finish-task` 必须使用相同的 `header.task_id`。之后关闭连接，或按对应模型的要求复用连接。

## 各模型差异

### Realtime 模型

下表列出输入触发和会话结束方式。VAD 类型、音频格式及其他参数的完整取值见对应模型的事件文档。

模型

输入与触发方式

结束方式

Qwen3.8-Omni / Qwen3.5-Omni

VAD 模式自动触发响应；Manual 模式先发送 `input_audio_buffer.commit`，再发送 `response.create`。

接收完结果后关闭连接。

Qwen-TTS-Realtime

`server_commit` 模式自动提交文本；`commit` 模式发送 `input_text_buffer.commit`，无需 `response.create`。

`session.finish → session.finished`

Qwen-ASR-Realtime

VAD 模式自动处理；Manual 模式发送 `input_audio_buffer.commit`，无需 `response.create`。

`session.finish → session.finished`

Qwen-Audio-Realtime

自动模式由服务端判断轮次；Manual 模式先发送 `input_audio_buffer.commit`，再发送 `response.create`。

接收完结果后关闭连接。

Qwen3.8-LiveTranslate

使用 `output_modalities` 配置输出模态，通过 `audio.input.turn_detection` 配置轮次检测。持续发送音频，输入结束后发送 `session.finish`。

`session.finish → session.finished`

Qwen3.5-LiveTranslate

使用 `modalities` 和 `turn_detection` 配置会话。Manual 模式发送 `input_audio_buffer.commit` 后自动生成响应，无需 `response.create`。

`session.finish → session.finished`

主要输出事件如下，具体返回的事件取决于配置的输出模态。

模型

主要输出事件

Qwen-Omni-Realtime

`response.text.delta` / `response.audio_transcript.delta` / `response.audio.delta` / `response.done`

Qwen-TTS-Realtime

`response.audio.delta` / `response.done`

Qwen-ASR-Realtime

`conversation.item.input_audio_transcription.text` / `conversation.item.input_audio_transcription.completed`

Qwen-Audio-Realtime

`response.audio_transcript.delta` / `response.audio.delta` / `response.done`

Qwen3.8-LiveTranslate

`response.text.delta` / `response.audio_transcript.delta` / `response.audio.delta` / `response.done`

Qwen3.5-LiveTranslate

`response.text.text` / `response.audio_transcript.text` / `response.audio.delta` / `response.done`

**说明**翻译模型的事件名与版本有关：Qwen3.8-LiveTranslate 使用 `.delta`，Qwen3.5-LiveTranslate 使用 `.text`。例如，音频对应的译文分别通过 `response.audio_transcript.delta` 和 `response.audio_transcript.text` 返回。

### Inference 模型

Qwen-Audio-TTS/CosyVoice 使用 `run-task → task-started → continue-task → finish-task → task-finished` 的任务流程；Qwen-Audio-ASR/Fun-ASR/Paraformer 语音识别在 `task-started` 后发送二进制音频帧。两类模型均通过 `task-failed` 报告任务错误。

## 各模型详细接入

### 实时全模态

-   [实时全模态](https://help.aliyun.com/zh/model-studio/realtime#bdaa43cdd7hsd)

### 实时语音合成

#### Qwen-Audio-TTS/CosyVoice

-   [WebSocket 接入指南](raw/_short/cosyvoice-websocket-api-615049d40629caf7.md)
-   [Java SDK](raw/_short/cosyvoice-java-sdk-4cad5c0351587943.md)
-   [Python SDK](raw/_short/cosyvoice-python-sdk-c20dfd31499fc83c.md)
-   [Android SDK](raw/_short/cosyvoice-android-sdk-3c17b87965adaf1e.md)
-   [iOS SDK](raw/_short/cosyvoice-ios-sdk-1995754e712f9554.md)
-   [HarmonyOS SDK](raw/_short/cosyvoice-harmonyos-sdk-59292bbe883fea24.md)

#### Qwen-TTS-Realtime

-   [WebSocket 接入指南](raw/_short/interactive-process-of-qwen-tts-realtime-synthes-3c96d28349bb779a.md)
-   [Python SDK](raw/_short/qwen-tts-realtime-python-sdk-4ee3dd3b202dcafe.md)
-   [Java SDK](raw/_short/qwen-tts-realtime-java-sdk-4a207246effe9e8c.md)

#### Sambert

-   [WebSocket 接入指南](raw/_short/sambert-websocket-api-3376aa99e8639bf5.md)
-   [Java SDK](raw/_short/sambert-java-sdk-2155fade7e0c42a0.md)
-   [Python SDK](raw/_short/sambert-python-sdk-c0d8d9c5cb8b634c.md)
-   [Android SDK](raw/_short/sambert-android-sdk-ecece410825d0555.md)
-   [iOS SDK](raw/_short/sambert-ios-sdk-3d168ae374b085dc.md)
-   [HarmonyOS SDK](raw/_short/sambert-harmonyos-sdk-3391d1ce74a26081.md)

### 实时语音识别

#### Qwen-Audio-3.x-ASR-Flash-Streaming/Qwen-Audio-3.1-ASR-Flash-Message/Fun-ASR-Realtime

-   [WebSocket 接入指南](raw/_short/fun-asr-realtime-websocket-api-d80484c92992191d.md)
-   [Python SDK](raw/_short/fun-asr-realtime-python-sdk-c8b5a715c3e66b70.md)
-   [Java SDK](raw/_short/fun-asr-realtime-java-sdk-1f6304ff694438f5.md)
-   [Android SDK](raw/_short/android-sdk-for-fun-asr-real-time-service-c55cca39825ba463.md)
-   [iOS SDK](raw/_short/ios-sdk-for-fun-asr-real-time-service-edf00c4a48ca2236.md)
-   [HarmonyOS SDK](raw/_short/harmonyos-sdk-for-fun-asr-real-time-service-a4bee2f4f80aa68b.md)

#### Qwen-ASR-Realtime

-   [WebSocket 接入指南](raw/_short/qwen-asr-realtime-interaction-process-c2a1fb44670529dd.md)
-   [Python SDK](raw/_short/qwen-asr-realtime-python-sdk-d52cbeee17e3272c.md)
-   [Java SDK](raw/_short/qwen-asr-realtime-java-sdk-70b383598ecfae85.md)

#### Paraformer

-   [WebSocket 接入指南](raw/_short/websocket-for-paraformer-real-time-service-b96dcec7afe963a4.md)
-   [Python SDK](raw/_short/paraformer-real-time-speech-recognition-python-s-145dc2b30661b050.md)
-   [Java SDK](raw/_short/paraformer-real-time-speech-recognition-java-sdk-cd32acdc922cc6bd.md)
-   [Android SDK](raw/_short/android-sdk-for-paraformer-real-time-service-3a045b654001e9de.md)
-   [iOS SDK](raw/_short/ios-sdk-for-paraformer-real-time-service-de0b0f08ebf5e89f.md)
-   [HarmonyOS SDK](raw/_short/harmonyos-sdk-for-paraformer-real-time-service-244b1e2952af17db.md)

### 实时语音对话

#### Qwen-Audio-Realtime

-   [WebSocket 接入指南](raw/_short/fun-audiochat-realtime-websocket-api-66b5ba4f8a668f28.md)
-   [Android SDK](raw/_short/android-sdk-for-qwen-audio-realtime-service-ca199805bd8bb70c.md)
-   [iOS SDK](raw/_short/ios-sdk-for-qwen-audio-realtime-service-8355a9429e58321f.md)
-   [HarmonyOS SDK](raw/_short/harmonyos-sdk-for-qwen-audio-realtime-service-b0a55b87b24035d2.md)

### 实时音视频翻译

#### Qwen-Livetranslate-Realtime

-   [Python SDK](raw/_short/qwen-livetranslate-python-sdk-0419928c3312cc76.md)
    
-   [Java SDK](raw/_short/qwen-livetranslate-java-sdk-be8175c4887f8470.md)
    
-   [实时语音翻译](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime)
    

### 多模态交互套件

-   [多模态开发套件](raw/_short/multimodal-interaction-protocol-8062cfbb96fec75a.md)

## 错误处理

-   **握手失败**：根据 HTTP 状态码和错误信息检查连接地址、API Key、业务空间及模型权限。遇到 401/403 时，优先核对鉴权配置。
-   **模型不存在或未开通**：核对模型名、服务开通状态及调用地域。
-   **Realtime 错误**：处理 `error` 事件，读取错误类型和消息。根据错误信息调整请求中的事件类型或参数。
-   **Inference 错误**：收到 `task-failed` 表示任务失败，可通过 `header.error_code` 和 `header.error_message` 获取失败原因。

修正配置或处理网络中断后，重新建立连接，并按对应协议重新配置会话或创建任务。错误码说明参见[错误码](raw/model-api-reference/preparations/error-code.md)。
