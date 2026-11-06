# CosyVoice AOQ 接入

介绍通过 AOQ 接入 CosyVoice 的鉴权、媒体配置、建连和任务事件处理流程。

通过 AOQ 接入 CosyVoice 时，客户端通过 Data 轨提交文本和任务事件，通过 Audio 轨接收合成语音。

## 准备工作

-   选择支持 AOQ 的型号。具体支持范围参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。
-   在业务 AppServer 配置与调用地域和业务空间匹配的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   从[SDK 下载](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-sdk-download.md)导入对应平台的 AOQ SDK。下文以 Android Java 和 Opus 传输为例，请同时导入 Opus 插件。纯文本合成无需申请麦克风或摄像头权限。

## 1\. 获取连接凭证

在 AppServer 设置环境变量 `DASHSCOPE_API_KEY`，用[所选地域及业务空间的接入域名](raw/model-user-guide/get-started-with-models/regions.md)替换 `{endpoint}`。CosyVoice 使用 Inference 建连路径，以下以 `cosyvoice-v3-plus` 为例。

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/inference?model=cosyvoice-v3-plus" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-rtc-transport: moq" \
  -d '{}'
```

若使用 Token Plan，接入域名中的 `WorkspaceId` 固定为 `token-plan`。请求体中的 `clientIp` 可选，填写客户端真实公网 IP，供网关选择 Relay 接入点。未填写时，网关使用请求来源 IP。

API Key 仅保存在 AppServer。AppServer 将下表中的连接参数返回客户端，响应中的 `sidExpiresInSecs` 表示会话有效期，单位为秒。

网关响应字段

`AoqConnectConfig` 字段

`aoqTokenForClient`

`token`

`sid`

`sid`

`clientRelayCertFingerprint`

`certFingerprint`

`clientRelayEndpoints`

`relayEndpoints`，逐项转换 `endpoint`、`port` 和 `route_index`

`extraInfo.workspaceIdHash`

`workspaceIdHash`

## 2\. 初始化 SDK 并建连

用 `AoqCreateConfig` 设置 SDK 工作目录，调用 `AoqClientEngine.createEngine` 创建引擎并注册回调。在 `onConnectionStatusChange` 中处理连接状态，在 `onDataMsg` 中解析模型事件，在 `onError` 中处理 SDK 错误。[Android SDK](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/aoq-android-sdk-reference.md)提供引擎初始化和连接字段的完整接口说明。

将 AppServer 返回的凭证填入 `connectConfig` 后，发布 Data 轨，订阅 Audio 和 Data 轨。下例设置 24 kHz 单声道 Opus 解码并启动播放器。模型的输出格式由任务事件指定，SDK 解码配置用于媒体轨传输。

```
AoqClientEngine.AoqAudioCodecConfig codec = new AoqClientEngine.AoqAudioCodecConfig();
codec.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
codec.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioOpus;
codec.sampleRate = 24000;
codec.channel = 1;
engine.setAudioDecoderConfig(codec);

AoqClientEngine.AoqTrackParam audio = new AoqClientEngine.AoqTrackParam();
audio.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
connectConfig.subscribeTracks.add(audio);
AoqClientEngine.AoqTrackParam publishData = new AoqClientEngine.AoqTrackParam();
publishData.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.publishTracks.add(publishData);
AoqClientEngine.AoqTrackParam subscribeData = new AoqClientEngine.AoqTrackParam();
subscribeData.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.subscribeTracks.add(subscribeData);

AoqClientEngine.AoqAudioPlaybackConfig playback = new AoqClientEngine.AoqAudioPlaybackConfig();
playback.channel = 1;
playback.isDefaultSpeaker = true;
engine.startAudioPlayer(playback);
engine.connect(connectConfig);
```

等待 `onConnectionStatusChange` 返回 `AoqConnectionStatusConnected` 后再启动任务。连接异常时清理本地任务状态，重新建连需要获取新的连接凭证。

## 3\. 启动合成任务并处理事件

将以下 JSON 序列化为 UTF-8，写入 `AoqDataMsg.data`，再用 `sendDataMsg` 通过 Data 轨发送。每个任务生成新的 `task_id`，本轮的所有事件使用同一个值。使用与所选型号匹配的[音色](raw/model-user-guide/model-experience/speech-and-audio/speech-synthesis/tts-voice-list/cosyvoice-voice-list.md)。

```
{
  "header": {
    "action": "run-task",
    "task_id": "0706c14c-dc16-4e45-8cb6-9d00686e8e19",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "tts",
    "function": "SpeechSynthesizer",
    "model": "cosyvoice-v3-plus",
    "parameters": {
      "text_type": "PlainText",
      "voice": "longanyang",
      "format": "pcm",
      "sample_rate": 24000
    },
    "input": {}
  }
}
```

在 `onDataMsg` 中读取 `header.event`。收到 `task-started` 后，发送一个或多个 `continue-task` 提交文本。

```
{
  "header": {
    "action": "continue-task",
    "task_id": "0706c14c-dc16-4e45-8cb6-9d00686e8e19",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "text": "欢迎使用阿里云百炼。"
    }
  }
}
```

SDK 从 Audio 轨接收并播放语音。`result-generated` 是 Data 轨上的任务事件，音频由 Audio 轨传输。收到 `task-failed` 时，读取 `header.error_code` 和 `header.error_message`，并结束本轮任务。

任务参数与事件字段参见[客户端事件](raw/_short/cosyvoice-client-events-480a8821d2d60e18.md)和[服务端事件](raw/_short/cosyvoice-server-events-81793da4414e2646.md)。

## 4\. 结束任务并释放资源

提交全部文本后发送 `finish-task`。保持连接，等待服务端合成剩余文本并返回 `task-finished`。

```
{
  "header": {
    "action": "finish-task",
    "task_id": "0706c14c-dc16-4e45-8cb6-9d00686e8e19",
    "streaming": "duplex"
  },
  "payload": {
    "input": {}
  }
}
```

不再使用连接时，等待已接收的音频播放结束，依次调用 `stopAudioPlayer`、`disconnect` 和 `AoqClientEngine.destroy` 释放资源。

## 相关文档

-   [AOQ SDK](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) · [功能参考](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
-   [自定义音频播放](raw/_short/aoq-custom-audio-playback-d7aa8527189532a2.md)
