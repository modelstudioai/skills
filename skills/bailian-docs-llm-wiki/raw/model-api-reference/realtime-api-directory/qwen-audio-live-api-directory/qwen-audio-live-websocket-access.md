# Qwen-Audio-Live WebSocket 接入

使用 WebSocket 建立会话、传输音频并处理任务事件。

## 请求地址

Qwen-Audio-Live 仅支持业务空间专属域名。填写华北2（北京）的业务空间 ID。

WebSocket`wss://WorkspaceId.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.1-live`

## 请求头

`Authorization`String必填

格式为 `Bearer <API Key>`。从华北2（北京）的 [API Key 管理](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取对应业务空间的 API Key。

## 查询参数

URL 中的 `model=qwen-audio-3.1-live` 用于选择 Qwen-Audio-Live 的服务入口。建立连接后，通过 `session.update` 中的 `session.model` 选择前台语音模型。可选值见 [session.update](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update)。

## 建立会话并收发音频

1.  建立连接，发送 [`session.update`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update)。如需通过这条连接收发音频，在会话配置中省略 `session.transport`。等待 [`session.updated`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-updated)。
2.  收到确认后，通过 `session.input_audio.append` 逐帧上传 Base64 编码的 16 kHz、16 位、单声道 PCM 音频。将 `session.output_audio.delta` 中的 Base64 数据解码为 24 kHz、16 位、单声道 PCM 音频。
3.  通过 `session.input_transcript.delta` 和 `session.output_transcript.delta` 分别读取输入转写和输出字幕。
4.  发送 `session.close`，收到 `session.closed` 后释放资源。

## 处理任务

模式

任务交互

Client

收到 `session.delegation.created` 后执行任务，并通过 `session.commentary.append` 回传。前台模型可继续用语音回复。

Responses

从 `response.event` 读取后台事件。内层 `response.completed` 表示后台生成已结束。通过 `session.output_audio.delta` 接收前台语音回复。

前台模型请求调用函数时，应用会收到 `session.event`。执行后发送 `session.item.create` 回传结果。事件格式见 [客户端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-client-events.md) 和 [服务端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-server-events.md)。

运行录音示例见[快速开始](raw/model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-live.md)。业务接入见[任务委派与工具](https://help.aliyun.com/zh/model-studio/qwen-audio-live-delegation)。使用独立媒体连接收发音频时，见 [WebRTC 接入](raw/_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)或 [AOQ 接入](raw/_short/qwen-audio-live-aoq-access-7fc752b6a8e53044.md)。

## 处理错误

收到 [error](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-error) 时，按错误码检查请求。收到 [session.closed](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-closed) 后停止发送事件。需要继续对话时，建立新连接并重新配置会话。
