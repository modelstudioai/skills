# Qwen-Audio-Live

选择 Qwen-Audio-Live 传输方式，按操作查找客户端和服务端事件。

首次接入可先跑通[快速开始](raw/model-user-guide/model-experience/speech-and-audio/speech-to-speech/qwen-audio-live.md)。

## 选择接入方式

先建立 WebSocket，再选择用哪条连接收发音频。

-   **[仅用 WebSocket](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md)**。收发事件中的 Base64 编码 PCM。省略 `session.transport`，或将其 `type` 设为 `websocket`。
-   **WebSocket + WebRTC 或 AOQ**。保持控制 WebSocket 连接，用于配置会话、协商媒体连接和发送任务请求。媒体连接就绪后，通过它收发音频，并选择控制 WebSocket 或媒体连接来接收服务端事件。
    -   **[WebRTC](raw/_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)**。通过 WebRTC 媒体轨道收发。将 `session.transport.type` 设为 `rtc`，通过控制 WebSocket 提交 Offer 并接收 Answer。
    -   **[AOQ](raw/_short/qwen-audio-live-aoq-access-7fc752b6a8e53044.md)**。用 AOQ Client SDK 连接 Relay 后收发音频。设置 `ws_audio=true` 后，还可通过控制 WebSocket 接收一份下行音频。将 `session.transport.type` 设为 `aoq`，通过 WebSocket 获取本次会话的临时凭证。

各协议共用 [WebSocket 连接地址和鉴权](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md)。发送 `session.update` 后等待 `session.updated`。WebRTC 和 AOQ 还需等待各自的媒体连接就绪。

## 按操作查找事件

### 配置和结束会话

操作

客户端发送

服务端返回

建立 WebSocket 连接

发起连接

[`session.created`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-created)

设置会话参数

[`session.update`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update)

[`session.updated`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-updated)

查看会话用量

读取服务主动上报的事件

[`session.usage.updated`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-usage-updated)

结束会话

[`session.close`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-close)

[`session.closed`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-closed)

处理请求错误

按事件返回的错误信息排查

[`error`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-error)

### 收发语音、字幕和文字

操作

客户端发送

服务端返回

纯 WebSocket 接入时收发语音

[`session.input_audio.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-input-audio-append)

[`session.output_audio.delta`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-output-audio-delta)

静音或恢复上行音频

[`session.input_audio.mute`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-input-audio-mute)、[`session.input_audio.unmute`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-input-audio-unmute)

[`session.input_audio.muted`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-input-audio-muted)、[`session.input_audio.unmuted`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-input-audio-unmuted)

显示用户转写和模型字幕

接收并累积文本片段

[`session.input_transcript.delta`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-input-transcript-delta)、[`session.output_transcript.delta`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-output-transcript-delta)

发送文字消息

[`session.item.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-item-create)，`item.type` 填 `message`

按会话配置收取音频和字幕

### 处理委派任务和函数调用

`session.delegation.type` 填 `client` 时，应用接收并处理任务。填 `responses` 时，百炼调用配置的后台模型。两种模式的操作步骤见[任务委派与工具](https://help.aliyun.com/zh/model-studio/qwen-audio-live-delegation)。

操作

请求或事件

关联字段或回执

收到自动派发的任务

服务发送 [`session.delegation.created`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-delegation-created)

`delegation_id`

更新任务进度

应用发送 [`session.thinking.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-thinking-append)

[`session.thinking.appended`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-thinking-appended)

请用户补充信息

应用发送 [`session.instruction.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-instruction-append)，填写当前任务的 `delegation_id`

收到 [`session.instructions.appended`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-instructions-appended) 回执。从后续 [`session.delegation.created`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-delegation-created) 的 `supplements`（如有）读取补充信息。

回传 Client 任务结果

应用发送 [`session.commentary.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-commentary-append)，填写 `delegation_id`

[`session.commentary.appended`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-commentary-appended)

显式启动后台生成

应用发送 [`response.item.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-response-item-create) 提供输入，再发送 [`response.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-response-create)

[`response.event`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-response-event)。内层 `response.completed` 表示后台生成结束

处理前台函数调用

服务发送 [`session.event`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-event)，应用发送 [`session.item.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-item-create) 回传结果

`call_id`

完整字段和 JSON 示例见[客户端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-client-events.md)与[服务端事件](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-server-events.md)。
