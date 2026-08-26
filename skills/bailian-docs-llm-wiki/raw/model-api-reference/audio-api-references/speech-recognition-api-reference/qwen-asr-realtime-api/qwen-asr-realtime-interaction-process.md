# Qwen-ASR实时语音识别WebSocket API

实时语音识别-千问服务通过 WebSocket 协议，接收实时音频流并实时转写。支持 VAD 模式 和 Manual 模式 交互流程。

**用户指南：**关于模型介绍和选型建议请参见[语音识别](raw/model-user-guide/model-experience/asr-model.md)，示例代码请参见[实时语音识别](https://help.aliyun.com/zh/model-studio/real-time-speech-recognition-user-guide)。

## 接口地址

WebSocket URL 固定如下，通过查询参数 `model` 指定要调用的模型名称（将 `<model_name>` 替换为实际的模型）：

#### 华北2（北京）

`wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

#### 新加坡

`wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime?model=<model_name>`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)。现有域名仍可正常使用。

**重要**URL 必须使用 `wss://` 协议。Authorization 在请求头中设置（参见[请求头](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-interaction-process#b02603aacf7e9)），模型通过 URL 查询参数 `model` 指定。

## 请求头

请求头中需添加如下信息：

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为 `Bearer <your_api_key>`，将 `<your_api_key>` 替换为实际的 API Key。

user-agent

string

否

客户端标识，便于服务端追踪来源。

X-DashScope-WorkSpace

string

否

阿里云百炼[业务空间ID](https://help.aliyun.com/zh/model-studio/use-workspace)。

X-DashScope-DataInspection

string

否

是否启用数据合规检测功能。默认不传或设为`enable`。如非必要，请勿启用该参数。

**重要**Authorization 鉴权在 WebSocket 握手阶段验证。如果 API Key 无效或缺失，握手将失败并返回 HTTP 401/403 错误。

## 交互流程

客户端事件和服务端事件的详细说明，请参见[客户端事件](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-client-events.md)和[服务端事件](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/qwen-asr-realtime-api/qwen-asr-realtime-server-events.md)。

支持两种交互模式：

-   **VAD 模式（默认）**：服务端自动检测语音的起点和终点（断句），适用于实时对话、会议记录等场景。
-   **Manual 模式**：由客户端控制断句，适用于客户端能明确判断语句边界的场景，如聊天软件中的发送语音。

### VAD 模式（默认）

服务端自动检测语音的起点和终点（断句）。开发者只需持续发送音频流，服务端会在检测到一句话结束时自动返回最终识别结果。此模式适用于实时对话、会议记录等场景。

**启用方式：**配置客户端`session.update`事件的`session.turn_detection`参数。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9052835871/CAEQaxiBgICW9b6H3RkiIGM5MDgwMTNkMjBjMDRlNTNiOGZlODNjZGJhNDQ3NGJm5812623_20251022102739.334.svg)

-   客户端通过发送`input_audio_buffer.append`事件将音频追加到缓冲区。
    
-   服务端在检测到语音时返回`input_audio_buffer.speech_started`事件。
    
    **注意**：如果客户端尚未收到该事件，就直接发送`session.finish`结束会话，服务端会直接返回`session.finished`事件，随后客户端需主动断开连接。
    
-   客户端继续发送`input_audio_buffer.append`事件提交音频。
    
-   客户端在音频提交完后，发送`session.finish`事件通知服务端结束当前会话。
    
    **警告**在 VAD 模式下，推完音频后必须先发送`session.finish`事件再关闭连接。如果客户端直接关闭 WebSocket 连接而未发送该事件，服务端将丢弃当前 in\_progress item，`conversation.item.input_audio_transcription.completed` 等事件将不会到达。建议在调用 `ws.Close()` 之前，先发送 `{"type":"session.finish"}`，并等待收到`session.finished`事件后再关闭连接。
    
-   服务端在检测到语音结束时返回`input_audio_buffer.speech_stopped`事件。
    
-   服务端返回`input_audio_buffer.committed`事件。
    
-   服务端返回`conversation.item.created`事件。
    
-   服务端返回`conversation.item.input_audio_transcription.text`事件，其中包含语音识别实时结果。
    
-   服务端返回`conversation.item.input_audio_transcription.completed`事件，其中包含语音识别最终结果。
    
-   服务端返回`session.finished`事件，通知客户端识别结束，此时客户端需要主动断开连接。
    

### Manual 模式

由客户端控制断句。客户端需要发送完一整句话的音频后，再发送一个`input_audio_buffer.commit`事件来通知服务端。此模式适用于客户端能明确判断语句边界的场景，如聊天软件中的发送语音。

**启用方式：**将客户端`session.update`事件的`session.turn_detection`设为null。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9052835871/CAEQaxiBgMDUp8qH3RkiIGEyYTc0NTI1ZmQ1OTQ5NjliNWE0OTYwYTAwMDBlMjBm5812623_20251022102739.334.svg)

-   客户端通过发送`input_audio_buffer.append`事件将音频追加到缓冲区。
-   客户端通过发送`input_audio_buffer.commit`事件来提交输入音频缓冲区。 该提交会在对话中创建一个新的用户消息项。
-   客户端发送`session.finish`事件通知服务端结束当前会话。
-   服务端返回`input_audio_buffer.committed`事件进行响应。
-   服务端返回`conversation.item.input_audio_transcription.text`事件，其中包含语音识别实时结果。
-   服务端返回`conversation.item.input_audio_transcription.completed`事件，其中包含语音识别最终结果。
-   服务端返回`session.finished`事件，通知客户端识别结束，此时客户端需要主动断开连接。
