# Qwen-Audio-ASR-Streaming AOQ 接入

介绍通过 AOQ 接入 Qwen-Audio-ASR-Streaming 的鉴权、媒体配置、建连和任务事件处理流程。

通过 AOQ 接入 Qwen-Audio-ASR-Streaming 时，客户端通过 Audio 轨上传音频，通过 Data 轨发送任务事件并接收识别结果。

## 准备工作

-   使用 `qwen-audio-3.1-asr-flash-streaming` 或 `qwen-audio-3.0-asr-flash-streaming`。具体支持范围参见[模型与协议支持范围](https://help.aliyun.com/zh/model-studio/realtime-api-overview#rtov-s02h2)。
-   在业务 AppServer 配置与调用地域和业务空间匹配的 [API Key](raw/model-api-reference/preparations/get-api-key.md)。
-   从[SDK 下载](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-sdk-download.md)导入对应平台的 AOQ SDK。下文以 Android Java 和 Opus 传输为例，请同时导入 Opus 插件。使用麦克风采集时，请在客户端申请录音权限。

## 1\. 获取连接凭证

**说明**如需提前获取 Token，或了解完整的鉴权流程，请参见[建连鉴权详解](https://help.aliyun.com/zh/model-studio/realtime-api-overview#tkauth-auth-detail-title)。

在 AppServer 设置环境变量 `DASHSCOPE_API_KEY`，用[所选地域及业务空间的接入域名](raw/model-user-guide/get-started-with-models/regions.md)替换 `{endpoint}`。Qwen-Audio-ASR-Streaming 使用 Inference 建连路径，以下以 `qwen-audio-3.1-asr-flash-streaming` 为例。

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/inference?model=qwen-audio-3.1-asr-flash-streaming" \
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

将 AppServer 返回的凭证填入 `connectConfig` 后，发布 Audio 和 Data 轨，订阅 Data 轨。下例设置 16 kHz 单声道 Opus 编码和内置采集，建连时关闭 Audio 轨发送。模型的输入格式由任务事件指定，SDK 编码配置用于媒体轨传输。

```
AoqClientEngine.AoqAudioCodecConfig codec = new AoqClientEngine.AoqAudioCodecConfig();
codec.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
codec.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioOpus;
codec.sampleRate = 16000;
codec.channel = 1;
codec.bitrate = 24000;
engine.setAudioEncoderConfig(codec);

AoqClientEngine.AoqTrackParam audio = new AoqClientEngine.AoqTrackParam();
audio.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
connectConfig.publishTracks.add(audio);
AoqClientEngine.AoqTrackParam publishData = new AoqClientEngine.AoqTrackParam();
publishData.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.publishTracks.add(publishData);
AoqClientEngine.AoqTrackParam subscribeData = new AoqClientEngine.AoqTrackParam();
subscribeData.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.subscribeTracks.add(subscribeData);

AoqClientEngine.AoqAudioCaptureConfig capture = new AoqClientEngine.AoqAudioCaptureConfig();
capture.channel = 1;
capture.isExternal = false;
engine.startAudioCapture(capture);
engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, false);
engine.connect(connectConfig);
```

等待 `onConnectionStatusChange` 返回 `AoqConnectionStatusConnected` 后再启动任务。连接异常时清理本地任务状态，重新建连需要获取新的连接凭证。

## 3\. 启动识别任务并处理事件

将以下 JSON 序列化为 UTF-8，写入 `AoqDataMsg.data`，再用 `sendDataMsg` 通过 Data 轨发送。每个任务生成新的 `task_id`，本轮的所有事件使用同一个值。

```
{
  "header": {
    "action": "run-task",
    "task_id": "0706c14c-dc16-4e45-8cb6-9d00686e8e19",
    "streaming": "duplex"
  },
  "payload": {
    "task_group": "audio",
    "task": "asr",
    "function": "recognition",
    "model": "qwen-audio-3.1-asr-flash-streaming",
    "parameters": {
      "format": "pcm",
      "sample_rate": 16000
    },
    "input": {}
  }
}
```

在 `onDataMsg` 中读取 `header.event`。收到 `task-started` 后才允许上行音频。

```
engine.enableSendMediaStream(AoqClientEngine.AoqTrackType.AoqTrackTypeAudio, true);
```

从 `result-generated` 的 `payload.output.sentence` 中读取识别文本，并跳过 `heartbeat=true` 的心跳。`sentence_end=false` 表示中间文本，`sentence_end=true` 表示句子最终文本。按 `sentence_id` 更新同一句的文本。收到 `task-failed` 时，停止本轮上行并读取 `header.error_code` 和 `header.error_message`。

任务参数与事件字段参见[客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-3240c8efa3976e48.md)和[服务端事件](raw/_short/qwen-audio-asr-streaming-server-events-4757090610f208c7.md)。

## 4\. 结束任务并释放资源

录音结束后，停止采集新的音频，等待待发送的音频送出。调用 `enableSendMediaStream` 关闭 Audio 轨上行，再通过 Data 轨发送 `finish-task`。保持连接，接收剩余识别结果并等待 `task-finished`。

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

不再使用连接时，依次调用 `stopAudioCapture`、`disconnect` 和 `AoqClientEngine.destroy` 释放资源。

## 相关文档

-   [AOQ SDK](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api.md) · [功能参考](raw/model-api-reference/realtime-api-directory/realtime-api-aoq-api/realtime-api-aoq-sdk-function.md)
-   [媒体流发送管理](raw/_short/aoq-media-stream-control-1278a5c1aba30cc3.md) · [自定义音频采集](raw/_short/aoq-custom-audio-capture-79471541298aac63.md)
-   [使用 AOQ 接入 Qwen-Audio-ASR-Streaming](raw/model-user-guide/use-cases/realtime-audio-video-integration/voice-input-using-aoq-access-qwen-audio-asr.md)
