# Qwen-Audio-Live

为语音助手和客服应用接入实时语音对话与工具调用。

Qwen-Audio-Live 的前台模型负责听取用户语音、提问和回复。遇到需要调用业务接口或进行推理的任务，可以把任务交给应用或后台模型，继续与用户对话。

以查订单为例，查询期间，前台模型仍可以接收用户补充的订单号，并播报查询进展和结果。Client 模式由应用处理任务并回传结果。Responses 模式由百炼调用配置的后台模型处理任务，并将结果交给前台模型。

![前台模型在订单查询期间继续对话，应用或后台模型根据所选模式处理任务并回传结果。](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f9009.png)

会话配置、音频收发和用量查询见[管理会话](#live-sessions)。接入业务系统或后台模型见[任务委派与工具](#live-delegation)。

## 快速开始

-   想先验证接入，可以[运行本页的 Python 示例](#live-first-session)，发送一段录音，检查能否收到字幕和音频。
-   想直接和模型对话，可以[运行 WebRTC 浏览器示例](https://help.aliyun.com/zh/model-studio/qwen-audio-live-webrtc-access#live-webrtc-browser-demo)，用麦克风说话，并听取模型回复。

### 建立第一个会话

本例通过 WebSocket 将一段录音发送给模型，并将语音回复保存到 `reply.wav`。

#### 准备录音和凭证

-   Qwen-Audio-Live 仅支持业务空间专属域名。本例需要华北2（北京）的业务空间 ID 和 [API Key](raw/model-api-reference/preparations/get-api-key.md)。长期 API Key 保存在应用服务端。
-   安装 Python 和 FFmpeg。录一句「请从一数到三」，保存为 `input.wav`。

将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，然后安装依赖，并将录音转换为 16 kHz、16 位、单声道的 PCM 音频。

```
python -m pip install "websockets>=15"
ffmpeg -i input.wav -ar 16000 -ac 1 -f s16le input.pcm
```

#### 发送录音并接收回复

将下面的代码保存为 `live_quickstart.py`，在连接地址中填入上一步准备的业务空间 ID。两个模型参数都可以沿用示例值。

```
import base64
import json
import os
import sys
import time
import uuid
import wave
from pathlib import Path

from websockets.sync.client import connect

WEBSOCKET_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.1-live"
SESSION_MODEL = "qwen-audio-4.0-realtime-preview"
REPLY_TIMEOUT_SECONDS = 12

def main():
    audio = Path(sys.argv[1]).read_bytes()
    if not audio or len(audio) % 2:
        raise ValueError("请提供非空的 16 位 PCM 文件")
    headers = {"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"}
    with connect(
        WEBSOCKET_URL,
        additional_headers=headers,
        close_timeout=2,
    ) as ws:
        def send(event_type, **payload):
            ws.send(json.dumps({
                "type": event_type,
                "event_id": uuid.uuid4().hex,
                **payload,
            }))

        session = {
            "model": SESSION_MODEL,
            "modalities": ["text", "audio"],
            "turn_detection": {"type": "duplex"},
            "delegation": {"type": "client"},
        }
        send("session.update", session=session)

        deadline = time.monotonic() + 20
        while True:
            event = json.loads(ws.recv(timeout=max(0, deadline - time.monotonic())))
            if event["type"] == "session.updated":
                break
            if event["type"] in ("error", "session.closed"):
                raise RuntimeError(event)

        audio += bytes(32000 * 3)
        with wave.open("reply.wav", "wb") as reply:
            reply.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            start = time.monotonic()
            offset = 0
            deadline = start + len(audio) / 32000 + REPLY_TIMEOUT_SECONDS
            while time.monotonic() < deadline:
                if offset < len(audio) and time.monotonic() >= start + offset / 32000:
                    frame = audio[offset:offset + 640]
                    send("session.input_audio.append",
                         audio=base64.b64encode(frame).decode("ascii"))
                    offset += len(frame)
                try:
                    event = json.loads(ws.recv(timeout=0.02 if offset < len(audio) else 0.25))
                except TimeoutError:
                    continue
                event_type = event["type"]
                if event_type == "session.output_audio.delta":
                    reply.writeframesraw(base64.b64decode(event["delta"]))
                elif event_type == "session.output_transcript.delta":
                    print(event["delta"], end="", flush=True)
                elif event_type == "session.closed":
                    break
                elif event_type == "error":
                    raise RuntimeError(event["error"])
            else:
                send("session.close")
                close_deadline = time.monotonic() + 2
                while time.monotonic() < close_deadline:
                    try:
                        event = json.loads(ws.recv(timeout=max(0, close_deadline - time.monotonic())))
                    except TimeoutError:
                        break
                    if event["type"] == "session.closed":
                        break
            if not reply.getnframes():
                raise RuntimeError("未收到语音回复")

main()
```

用上一步准备的录音运行脚本：

```
python live_quickstart.py input.pcm
```

运行后，终端会显示回复字幕。打开生成的 `reply.wav`，确认能听到模型数数。该文件是 24 kHz、16 位、单声道 WAV。要调整示例中的模型、音色或音频传输方式，见[配置会话](#live-session-config)。

如果没有收到回复，先检查 API Key、业务空间 ID 和连接地址是否属于同一地域，再确认脚本是在收到 [`session.updated`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-updated) 后才发送录音。其他现象可按[排查接入问题](#live-troubleshoot-session)逐项检查。

### 选择接入方式

两种接入方式都先建立 WebSocket 主连接。您可以用这条连接直接收发音频，也可以另外建立一条 WebRTC 或 AOQ 媒体连接来收发音频。

-   **[仅用 WebSocket](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md)**。适合用录音验证接入，或由服务端直接处理音频。音频、字幕和任务事件都走同一条连接。
    
    ![应用与百炼共用一条 WebSocket 连接收发音频和事件。](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f901d.png)
-   **WebSocket + WebRTC 或 AOQ**。保留 WebSocket 主连接，用它配置会话、协商媒体连接和发送任务请求。媒体连接就绪后，用它收发音频，同时可从 WebSocket 主连接或媒体连接接收服务端事件。
    
    ![控制 WebSocket 是主连接。WebRTC 或 AOQ 媒体连接收发音频，也可接收服务端事件。](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f9018.png)
    -   **[WebRTC](raw/_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)**。适合在浏览器或应用中实时采集和播放语音。通过控制 WebSocket 交换 SDP。
    -   **[AOQ](raw/_short/qwen-audio-live-aoq-access-7fc752b6a8e53044.md)**。适合已集成 AOQ Client SDK 的应用。通过控制 WebSocket 获取临时凭证，再用 SDK 连接 Relay。

[API 参考](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-api-reference.md)按操作提供请求与响应事件的入口。[模型详情](raw/model-user-guide/get-started-with-models/model-studio-model-list/model-list-speech-to-speech/qwen-audio-3-1-live.md)列出地域、限流和价格。

## 编写提示词

### 编写前台对话提示词

在 `session.instructions` 中设置前台的角色和语气，说明何时追问、何时委派，以及如何播报结果。

初次配置会话时，省略 `session.instructions` 会使用内置提示词。如果填写了自定义提示词，它会替换内置提示词，因此请把对话需要遵循的规则写完整。

要让客服先简短回答，再问客户是否需要帮助，可在 `session.update` 的 `session` 中加入以下字段，并保留已有的 `model` 和 `delegation` 等设置。

```
{
  "instructions": "担任门店客服。先用一句话回答，再询问用户是否需要其他帮助。"
}
```

### 编写任务处理规则

任务提示词说明处理步骤、输入校验和结果格式。用 Client 模式时，在应用或 Agent 中定义这些规则。用 Responses 模式时，在 `session.delegation.responses.instructions` 中写明后台模型需要遵循的规则，百炼没有内置的后台提示词。

### 用提示词分配计算任务

在 Responses 模式下，可以让前台问清计算条件，由后台计算总价。

-   **前台提示词**说明何时追问、何时交给后台。例如，缺少单价或数量时，先向用户确认。条件齐全后，把计算任务交给后台模型，并在收到结果后用一句话播报。
-   **后台提示词**说明怎么算、返回什么。例如，根据单价和数量计算总价，返回金额和币种。

完整的会话配置和验证步骤见 [Responses 模式示例](#live-use-responses)。

## 管理会话

建立连接后，先配置会话，确定由哪个前台模型和用户交谈、使用什么音色、如何传输音频，以及任务交给谁处理。

### 配置会话

设置

配置位置和用途

前台模型

连接地址中的 `model=qwen-audio-3.1-live` 指定要接入的服务。`session.model` 指定与用户交谈的前台模型。快速开始使用 `qwen-audio-4.0-realtime-preview`，并将 `session.turn_detection.type` 设为 `duplex`，开启全双工对话。模型可以边听边说，在回复时仍能接收用户语音。

对话指令和音色

通过 `instructions` 和 `voice` 设置。见[编写提示词](#live-write-prompts)和[配置音色](#live-configure-voice)。

输出类型

`modalities` 同时包含 `text` 和 `audio` 时，服务返回语音和字幕。

音频传输方式

通过 `session.transport` 选择音频走哪条连接。省略时，音频通过 WebSocket 收发。使用 WebRTC 或 AOQ 时，按各自的[接入流程](https://help.aliyun.com/zh/model-studio/qwen-audio-live-api-reference#live-select-transport)建立媒体连接。

任务处理模式

通过 `session.delegation` 设置。见[任务委派与工具](#live-delegation)。

完整配置字段见 [session.update](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update)。

发送 [`session.update`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update) 后，通过 [`session.updated`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-updated) 确认哪些配置已生效。仅用 WebSocket 时，收到该事件后就可以发送音频。使用 WebRTC 或 AOQ 时，还要等媒体连接就绪。

### 配置音色

在 `session.update` 的 `session` 对象中设置音色 ID，保留其余会话配置。

```
{
  "voice": "qingyou"
}
```

示例中的 `qingyou` 对应「青柚」，默认值为 `yunshu`（云舒）。完整列表见[客户端事件](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-voice)。

### 收发语音和字幕

发送麦克风音频和播放模型回复时，使用建连时选定的音频通道。开启全双工对话后，播放回复时也要继续采集并发送用户语音，同时读取服务端事件。

-   **WebRTC** 通过媒体轨道收发音频。浏览器收到远端音轨后，将它交给播放器。
-   **AOQ** 通过 SDK 发送用户语音和播放模型回复。上行音频必须通过 AOQ 发送。将 `session.transport.aoq.ws_audio` 设为 `true` 后，控制 WebSocket 也会收到一份模型的回复音频。详见 [AOQ 接入](raw/_short/qwen-audio-live-aoq-access-7fc752b6a8e53044.md)。
-   **WebSocket** 通过 JSON 事件收发音频。输入和输出都使用单声道 PCM，采样率见下表。

下表的音频收发流程适用于纯 WebSocket 接入。无论音频通过哪条连接传输，都可以用表中的字幕事件显示用户转写和模型回复。

数据

事件

处理方式

麦克风音频或录音

发送 `session.input_audio.append`

将 16 kHz、16 位、单声道 PCM 音频分片并编码为 Base64。快速开始以 20 毫秒为一帧。

模型回复音频

接收 `session.output_audio.delta`

解码事件的 `delta`，按到达顺序播放 24 kHz、16 位、单声道 PCM。

字幕

接收 `session.input_transcript.delta` 和 `session.output_transcript.delta`

前者是用户语音的转写，后者是模型回复的字幕。

如果用户在模型播报时补充一句话，用户字幕和模型字幕可能同时更新。把用户转写和模型字幕分别追加到各自的对话气泡。界面上的播报状态以播放器为准。

WebRTC 或 AOQ 媒体连接就绪后，控制 WebSocket 和媒体连接都可用于接收字幕。如果应用同时监听这两条连接，追加字幕前按 `event_id` 去重。

如果界面有麦克风开关，可在用户切换时发送 `session.input_audio.mute` 或 `session.input_audio.unmute`，等服务确认后再更新开关状态。静音期间，会话仍保持连接。

### 发送文字消息

除了语音，用户也可以在通话中用文字补充信息，例如输入要查的商品名。应用通过 `session.item.create` 将这段文字作为用户消息发给模型。

```
{
  "type": "session.item.create",
  "event_id": "evt_user_message",
  "item": {
    "role": "user",
    "type": "message",
    "content": [
      {"type": "input_text", "text": "我想查黑色折叠伞。"}
    ]
  }
}
```

### 结束会话和查看用量

用户挂断或点击结束时，发送 `session.close` 并停止采集麦克风音频。等收到 `session.closed` 后，再关闭连接并释放资源。

会话激活后，服务每 5 秒通过 `session.usage.updated` 上报 `usage.seconds`，表示会话累计计费时长（秒）。会话期间取最新值，结束后以 `session.closed` 中的 `usage.seconds` 为准。

单次会话没有时长上限，费用按会话时长（秒）计算。连接建立后至少计费 3 秒，超过 3 秒则按实际会话时长计费。发送文字消息、静音和空闲的时间都计入会话时长。百炼调用后台模型时，还会按该模型的实际 Token 用量另行计费。价格及后台模型计费见[计费说明](https://help.aliyun.com/zh/model-studio/model-pricing#qwen-audio-live-pricing)。

### 排查接入问题

问题现象

排查方法

上传音频后没有回复

先确认收到 `session.updated`。纯 WebSocket 接入时，检查上行音频是否为 16 kHz、16 位、单声道 PCM。使用 WebRTC 或 AOQ 时，确认媒体连接已就绪，并已通过该连接发送音频。

收到字幕，未听到语音回复

纯 WebSocket 接入时，检查是否收到 `session.output_audio.delta`，并以 24 kHz 播放。使用 WebRTC 或 AOQ 时，检查播放器是否接收到所选通道的下行音频。

字幕里有重复的字词或整句

使用 WebRTC 或 AOQ 时，控制 WebSocket 和媒体连接都可能收到同一条字幕。选择一路更新字幕即可。如果同时监听两路，在追加字幕前按 `event_id` 去重。

任务已处理，未听到语音播报

检查应用是否接收并播放前台模型的语音。Client 模式下，确认回传的 `delegation_id` 与任务一致。

收到 `error` 或 `session.closed`

收到 `error` 时，按[错误事件](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-error)检查请求。会话关闭后，如需继续通话，重新建连并配置会话。

## 任务委派与工具

本节示例沿用[快速开始](#live-quickstart)的纯 WebSocket 连接。使用 WebRTC 或 AOQ 时，会话配置和任务请求仍通过控制 WebSocket 发送，音频则通过媒体连接收发。

### 前后台工具选型

用户在对话中提出业务请求时，前台模型可以直接发起函数调用，也可以把任务委派给后台。接入时，可以根据任务的处理步骤和响应要求，选择把工具配置在哪里。

-   **前台工具**适合可直接执行、需要快速响应的操作。例如，用户说「播放音乐」时，前台模型调用通过 `session.tools` 注册的函数，由应用执行播放指令。
-   **后台工具**适合需要判断条件或依次调用多个工具的任务。例如，查询可改签班次时，如果后台模型已配置相应的查询工具，就可以先查订单和改签规则，再查符合条件的班次，由前台模型向用户播报。

### 选择处理任务模式

希望百炼调用后台模型并传回结果时，选择 [Responses 模式](#live-use-responses)。已有业务接口、工作流或 Agent，或者需要由应用先核对结果再决定播报内容时，选择 [Client 模式](#live-use-client)。

在 [`session.update`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-session-update) 中设置 `session.delegation.type`。Responses 模式填 `responses`，Client 模式填 `client`。

要决定的事

Responses 模式

Client 模式

谁处理任务

百炼调用配置的后台 Responses 模型。

应用调用业务接口、工作流、Agent 或模型。

谁准备任务输入

应用预先配置后台模型和任务指令。需要委派时，百炼根据当前对话准备输入并发起请求。

应用从委派事件读取任务摘要和上下文，结合业务数据构造请求。

谁决定回传什么

后台结果由百炼交给前台模型。

应用可以校验、汇总或筛选结果，再把适合播报的内容交给前台模型。

同样是查询可改签班次，如果让百炼调用后台模型，由模型使用已配置的工具完成查询，可以选择 Responses 模式。如果已有票务工作流负责查询，并且需要应用核对班次后再播报，可以选择 Client 模式。

两种模式都可以[配置前台函数](#live-call-frontend-functions)，用 `call_id` 将函数调用与结果对应起来。Client 模式中的任务委派则使用 `delegation_id` 关联同一任务的进度、追问和结果。接入业务系统前，先确认应用拥有接口权限，并了解接口需要哪些输入、会返回什么。

### 使用 Responses 模式调用后台模型

#### 接入准备

准备业务空间可调用的后台 Responses 模型。示例使用 `qwen4-max` 计算总价，再由前台模型播报。

#### 配置会话

将 `session.delegation.type` 设为 `responses`，在 `session.delegation.responses` 中指定后台模型（`model`）。还可以为后台模型编写任务指令（`instructions`）或配置工具（`tools`）。

以计算总价为例，前台提示词可以写成“缺少单价或数量时，先向用户确认。两项齐全后，把计算交给后台”。后台提示词则写明“根据单价和数量计算总价，返回金额和币种”。

#### 接收后台事件

自动委派开始时，服务发送 [`session.delegation.created`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-delegation-created)。后台生成期间，服务通过 [`response.event`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-response-event) 转发后台事件。按外层的 `delegation_id`（如有）关联任务，按 `event.type` 区分后台事件。

收到内层 `response.completed` 表示后台生成结束。用户听到的回复仍由前台模型播报，脚本会显示前台字幕并将语音保存为 `reply.wav`。

#### 验证委派与播报

将以下完整示例保存为 `live_responses.py`，并在连接地址中填入业务空间 ID。脚本为后台处理和语音播报预留 30 秒。

```
import base64
import json
import os
import sys
import time
import uuid
import wave
from pathlib import Path

from websockets.sync.client import connect

WEBSOCKET_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.1-live"
SESSION_MODEL = "qwen-audio-4.0-realtime-preview"
REPLY_TIMEOUT_SECONDS = 30

def main():
    audio = Path(sys.argv[1]).read_bytes()
    if not audio or len(audio) % 2:
        raise ValueError("请提供非空的 16 位 PCM 文件")
    headers = {"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"}
    with connect(
        WEBSOCKET_URL,
        additional_headers=headers,
        close_timeout=2,
    ) as ws:
        def send(event_type, **payload):
            ws.send(json.dumps({
                "type": event_type,
                "event_id": uuid.uuid4().hex,
                **payload,
            }))

        session = {
            "model": SESSION_MODEL,
            "modalities": ["text", "audio"],
            "turn_detection": {"type": "duplex"},
            "instructions": (
                "担任语音客服。"
                "计算总价时，如果缺少单价或数量，先向用户确认。"
                "条件齐全后，将计算任务交给后台模型。"
                "收到结果后，用一句话播报。"
            ),
            "delegation": {
                "type": "responses",
                "responses": {
                    "model": "qwen4-max",
                    "instructions": (
                        "根据单价和数量计算总价，返回金额和币种。"
                        "缺少必要条件时，说明缺少哪一项。"
                    ),
                },
            },
        }
        send("session.update", session=session)

        deadline = time.monotonic() + 20
        while True:
            event = json.loads(ws.recv(timeout=max(0, deadline - time.monotonic())))
            if event["type"] == "session.updated":
                break
            if event["type"] in ("error", "session.closed"):
                raise RuntimeError(event)

        audio += bytes(32000 * 3)
        with wave.open("reply.wav", "wb") as reply:
            reply.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            start = time.monotonic()
            offset = 0
            deadline = start + len(audio) / 32000 + REPLY_TIMEOUT_SECONDS
            while time.monotonic() < deadline:
                if offset < len(audio) and time.monotonic() >= start + offset / 32000:
                    frame = audio[offset:offset + 640]
                    send("session.input_audio.append",
                         audio=base64.b64encode(frame).decode("ascii"))
                    offset += len(frame)
                try:
                    event = json.loads(ws.recv(timeout=0.02 if offset < len(audio) else 0.25))
                except TimeoutError:
                    continue
                event_type = event["type"]
                if event_type == "session.output_audio.delta":
                    reply.writeframesraw(base64.b64decode(event["delta"]))
                elif event_type == "session.output_transcript.delta":
                    print(event["delta"], end="", flush=True)
                elif event_type == "session.delegation.created":
                    print(f"\n已派发任务 {event['delegation_id']}", flush=True)
                elif event_type == "response.event":
                    backend_event = event["event"]
                    if backend_event["type"] == "response.completed":
                        print("\n后台模型已完成生成", flush=True)
                    elif backend_event["type"] == "response.failed":
                        print("\n后台生成失败", backend_event.get("response", {}).get("error"), flush=True)
                elif event_type == "session.closed":
                    break
                elif event_type == "error":
                    raise RuntimeError(event["error"])
            else:
                send("session.close")
                close_deadline = time.monotonic() + 2
                while time.monotonic() < close_deadline:
                    try:
                        event = json.loads(ws.recv(timeout=max(0, close_deadline - time.monotonic())))
                    except TimeoutError:
                        break
                    if event["type"] == "session.closed":
                        break
            if not reply.getnframes():
                raise RuntimeError("未收到语音回复")

main()
```

录下「每件商品三百二十七元，买十三件一共多少钱」，保存为 `responses.wav`。转换录音并运行脚本。

```
ffmpeg -i responses.wav -ar 16000 -ac 1 -f s16le responses.pcm
python live_responses.py responses.pcm
```

先看终端是否记录了任务派发，以及 [`response.event`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-response-event) 中的 `response.completed`。再打开 `reply.wav`，确认模型播报了总价 4,251 元。应用中如需显示播报进度，以播放器的实际状态为准。

再录一段只提供单价的请求，例如「每件三百二十七元，一共多少钱」。用同样的方法转换录音并运行脚本，检查字幕或新的 `reply.wav` 是否追问购买数量。

#### 配置和观察后台工具

通过 `session.delegation.responses.tools` 声明供后台模型使用的工具。工具定义的格式见 [Responses API](raw/model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)。自动委派中，服务执行受支持的后台工具并处理结果。应用可监听 [`response.event`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-response-event) 观察执行情况。收到内层 `response.output_item.done` 且 `event.item.type` 为 `function_call` 时，可从 `event.item` 读取函数名 `name`、参数 `arguments` 和调用 ID `call_id`。

如果业务系统需要由应用执行和校验，使用 [Client 模式](#live-use-client)接收任务，或[在前台声明函数](#live-call-frontend-functions)以获取结构化参数。

#### 由应用发起后台生成

应用已有完整输入时，可通过 [`response.item.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-response-item-create) 提供文本，再通过 [`response.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-response-create) 发起独立的后台任务。结果从 `response.event` 读取。

将以下完整示例保存为 `live_responses_text.py`，并在连接地址中填入业务空间 ID。脚本直接发送文本，在终端显示后台返回的计算结果。

```
import json
import os
import time
import uuid

from websockets.sync.client import connect

WEBSOCKET_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.1-live"
SESSION_MODEL = "qwen-audio-4.0-realtime-preview"
REPLY_TIMEOUT_SECONDS = 30

def main():
    headers = {"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"}
    with connect(
        WEBSOCKET_URL,
        additional_headers=headers,
        close_timeout=2,
    ) as ws:
        def send(event_type, **payload):
            ws.send(json.dumps({
                "type": event_type,
                "event_id": uuid.uuid4().hex,
                **payload,
            }))

        session = {
            "model": SESSION_MODEL,
            "modalities": ["text", "audio"],
            "turn_detection": {"type": "duplex"},
            "instructions": (
                "担任语音客服。"
                "计算总价时，如果缺少单价或数量，先向用户确认。"
                "条件齐全后，将计算任务交给后台模型。"
                "收到结果后，用一句话播报。"
            ),
            "delegation": {
                "type": "responses",
                "responses": {
                    "model": "qwen4-max",
                    "instructions": (
                        "根据单价和数量计算总价，返回金额和币种。"
                        "缺少必要条件时，说明缺少哪一项。"
                    ),
                },
            },
        }
        send("session.update", session=session)

        deadline = time.monotonic() + 20
        while True:
            event = json.loads(ws.recv(timeout=max(0, deadline - time.monotonic())))
            if event["type"] == "session.updated":
                break
            if event["type"] in ("error", "session.closed"):
                raise RuntimeError(event)

        send("response.item.create", item={
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": "单价 327 元，数量 13，计算总价。"}],
        })
        send("response.create")

        deadline = time.monotonic() + REPLY_TIMEOUT_SECONDS
        while True:
            event = json.loads(ws.recv(timeout=max(0, deadline - time.monotonic())))
            if event["type"] in ("error", "session.closed"):
                raise RuntimeError(event)
            if event["type"] != "response.event":
                continue

            backend_event = event["event"]
            kind = backend_event["type"]
            if kind == "response.output_text.delta":
                print(backend_event["delta"], end="", flush=True)
            elif kind == "response.completed":
                print()
                break
            elif kind == "response.failed":
                raise RuntimeError(backend_event)

        send("session.close")

main()
```

运行 `python live_responses_text.py`。终端应输出后台模型返回的金额。

### 使用 Client 模式接入业务系统

在 Client 模式下，前台模型把任务交给应用。应用执行业务操作，把结果发回前台模型，由它告诉用户。

#### 接入准备

-   **运行示例**：按[快速开始](#live-first-session)准备业务空间 ID、API Key 和运行环境，并录一段询问库存的语音。应用收到查询任务后，直接回传预设的“黑色折叠伞还有七把”，供前台模型播报。运行示例无需库存接口。
-   **接入自己的业务系统**：确认应用有权调用业务接口，了解接口需要哪些参数，以及返回结果中哪些信息要告诉用户。例如，库存接口如果按商品 ID 查询，应用需要先根据用户说的商品名称找到对应的 ID，再查询库存，将商品名称和剩余数量一起回传。

#### 配置会话

将 `session.delegation.type` 设为 `client`，在前台提示词中说明哪些任务交给应用，以及收到结果后如何回复用户。库存查询示例使用的提示词是“将库存查询交给应用，收到结果后用语音回复用户”。

#### 接收任务并准备上下文

收到 [`session.delegation.created`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-delegation-created) 后，用 `event_id` 去重，并保存 `delegation_id`，用于关联后续更新。从 `summary` 和 `context`（如有）提取任务信息，再结合应用保存的业务状态准备请求。例如，查库存时，可以用任务里的商品名称和当前门店，找到库存接口所需的商品 ID。

任务缺少必要信息时，应用可以请前台模型向用户追问。例如，用户想查库存却没说商品名称，就请前台模型问清要查哪件商品。收到后续的 `session.delegation.created` 时，用 `delegation_id` 关联同一任务。如果事件带有 `supplements`，可以从中读取补充内容。等查询条件齐全后再执行。

#### 回传进度、补充问题和结果

根据要回传的是进度、追问还是结果，选择下表中的事件。发送时填入当前任务的 `delegation_id`。

要回传的内容

发送的事件

`content` 示例

更新进度，暂不播报

[`session.thinking.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-thinking-append)

正在查询该门店的库存。

需要向用户追问的条件

[`session.instruction.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-instruction-append)

请询问用户要查询哪件商品。

要让前台模型播报的结果

[`session.commentary.append`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-commentary-append)

黑色折叠伞还有七把。

业务调用较慢时，可以在应用后台执行，让主循环继续收发音频和处理事件。核对业务结果后，再把适合播报的内容交给前台模型。

#### 验证任务派发和结果播报

将以下完整示例保存为 `live_client.py`，并在连接地址中填入业务空间 ID。

```
import base64
import json
import os
import sys
import time
import uuid
import wave
from pathlib import Path

from websockets.sync.client import connect

WEBSOCKET_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime?model=qwen-audio-3.1-live"
SESSION_MODEL = "qwen-audio-4.0-realtime-preview"
REPLY_TIMEOUT_SECONDS = 30

def main():
    audio = Path(sys.argv[1]).read_bytes()
    if not audio or len(audio) % 2:
        raise ValueError("请提供非空的 16 位 PCM 文件")
    headers = {"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"}
    with connect(
        WEBSOCKET_URL,
        additional_headers=headers,
        close_timeout=2,
    ) as ws:
        def send(event_type, **payload):
            ws.send(json.dumps({
                "type": event_type,
                "event_id": uuid.uuid4().hex,
                **payload,
            }))

        session = {
            "model": SESSION_MODEL,
            "modalities": ["text", "audio"],
            "turn_detection": {"type": "duplex"},
            "delegation": {"type": "client"},
            "instructions": "将库存查询交给应用，收到结果后用语音回复用户。",
        }
        seen_delegation_events = set()
        send("session.update", session=session)

        deadline = time.monotonic() + 20
        while True:
            event = json.loads(ws.recv(timeout=max(0, deadline - time.monotonic())))
            if event["type"] == "session.updated":
                break
            if event["type"] in ("error", "session.closed"):
                raise RuntimeError(event)

        audio += bytes(32000 * 3)
        with wave.open("reply.wav", "wb") as reply:
            reply.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            start = time.monotonic()
            offset = 0
            deadline = start + len(audio) / 32000 + REPLY_TIMEOUT_SECONDS
            while time.monotonic() < deadline:
                if offset < len(audio) and time.monotonic() >= start + offset / 32000:
                    frame = audio[offset:offset + 640]
                    send("session.input_audio.append",
                         audio=base64.b64encode(frame).decode("ascii"))
                    offset += len(frame)
                try:
                    event = json.loads(ws.recv(timeout=0.02 if offset < len(audio) else 0.25))
                except TimeoutError:
                    continue
                event_type = event["type"]
                if event_type == "session.output_audio.delta":
                    reply.writeframesraw(base64.b64decode(event["delta"]))
                elif event_type == "session.output_transcript.delta":
                    print(event["delta"], end="", flush=True)
                elif event_type == "session.delegation.created":
                    if event["event_id"] in seen_delegation_events:
                        continue
                    seen_delegation_events.add(event["event_id"])
                    task_id = event["delegation_id"]
                    print(f"\n收到任务 {task_id}", flush=True)
                    send("session.commentary.append",
                         delegation_id=task_id,
                         content="黑色折叠伞还有七把。")
                elif event_type == "session.commentary.appended":
                    print("\n服务已受理任务结果", flush=True)
                elif event_type == "session.closed":
                    break
                elif event_type == "error":
                    raise RuntimeError(event["error"])
            else:
                send("session.close")
                close_deadline = time.monotonic() + 2
                while time.monotonic() < close_deadline:
                    try:
                        event = json.loads(ws.recv(timeout=max(0, close_deadline - time.monotonic())))
                    except TimeoutError:
                        break
                    if event["type"] == "session.closed":
                        break
            if not reply.getnframes():
                raise RuntimeError("未收到语音回复")

main()
```

录下「请查一下黑色折叠伞有没有货」，保存为 `client.wav`。转换录音并运行脚本。

```
ffmpeg -i client.wav -ar 16000 -ac 1 -f s16le client.pcm
python live_client.py client.pcm
```

先在终端确认应用收到了任务派发，而且服务已受理回传的结果。再打开 `reply.wav`，听模型是否说出了库存结果。接入真实库存接口后，用查询结果替换示例中的固定结果。

### 配置和处理前台函数

前面的库存示例把整个查询任务交给应用，由应用准备查询条件。如果已有一个按商品名称查库存的函数，可以让前台模型直接调用它。应用在 `session.tools` 中声明函数和参数，前台模型就能从对话中提取商品名称，交给应用执行。Client 和 Responses 模式都可以使用前台函数。

将以下字段加入 `session.update` 的 `session` 对象，其余会话配置沿用原值。

```
{
  "tools": [
    {
      "type": "function",
      "name": "lookup_stock",
      "description": "查询指定商品的库存数量",
      "parameters": {
        "type": "object",
        "properties": {
          "item": {"type": "string", "description": "商品名称"}
        },
        "required": ["item"]
      }
    }
  ]
}
```

1.  收到 [`session.event`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-server-events#live-session-event) 后，读取 `event.item` 中 `type` 为 `function_call` 的调用项。
2.  按 `name` 找到函数，将 `arguments` 从 JSON 字符串解析为参数，校验后执行。同一个 `call_id` 只执行一次。
3.  发送 [`session.item.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-item-create) 回传结果。将 `item.type` 设为 `function_call_output`，在 `item.call_id` 中填写本次函数调用的 `call_id`。

```
{
  "type": "session.item.create",
  "event_id": "evt_function_result",
  "item": {
    "type": "function_call_output",
    "call_id": "call_stock",
    "output": "{\"stock\":7}"
  }
}
```

在 Client 模式下，前台模型等待函数结果时仍可接收用户语音并回复。应用可继续收发音频和处理事件。需要查询网页或其他实时信息时，可注册搜索服务，或由 Client 模式下的应用调用搜索服务。

## 从 Qwen-Audio-Realtime 接入

如果应用已使用 Qwen-Audio-Realtime，可保留现有业务接口和工具实现。先用快速开始验证 Qwen-Audio-Live 的语音收发，再迁移事件处理和任务逻辑。

迁移项

在 Qwen-Audio-Live 中的处理方式

WebSocket 连接

使用 [Qwen-Audio-Live 请求地址](raw/model-api-reference/realtime-api-directory/qwen-audio-live-api-directory/qwen-audio-live-websocket-access.md)，并在 `session.update` 中配置前台模型和任务处理模式。

WebSocket 音频

用 `session.input_audio.append` 发送用户语音，从 `session.output_audio.delta` 读取模型回复。按本页示例开启全双工对话后，应用持续发送音频即可，无需再用手动模式的 `input_audio_buffer.commit` 和 `response.create` 触发语音回复。格式和采样率见[收发语音和字幕](#live-session-media)。

WebRTC 信令

原来通过 HTTP 交换 SDP。接入 Live 时，通过控制 WebSocket 发送 Offer，并从 `session.updated` 的 `session.transport.sdp` 读取 Answer。见 [WebRTC 接入](raw/_short/qwen-audio-live-webrtc-access-2a873a21a2d29a3b.md)。

前台函数

从 `session.event` 读取函数调用。执行后通过 `session.item.create` 按 `call_id` 回传。旧流程用 `response.create` 触发前台继续回复。Live 的 [`response.create`](https://help.aliyun.com/zh/model-studio/qwen-audio-live-client-events#live-response-create) 用于显式启动后台任务。

耗时业务任务

按[任务委派与工具](#live-delegation)选择 Client 或 Responses。用一条需要调用工具的语音请求验证任务结果和语音播报。
