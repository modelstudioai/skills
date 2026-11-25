# 使用 AOQ 接入 qwen-audio-3.1-tts-flash 实现语音合成

通过 AOQ 接入 qwen-audio-3.1-tts-flash，分段发送文本，在 Android 应用中缓存并播放合成的 PCM 音频。

<a id="方案概述"></a>

<a id="tts-overview-title"></a>

## 方案概述

TTS 的音频生成和下发速度通常快于实时播放。合成长文本时，大量音频会先进入客户端缓存，随后逐步播放。如果使用 SDK 内置播放器，服务端空闲约 60 秒后断开连接时，SDK 播放链路也会结束，播放缓存中的剩余音频可能无法继续播放。

本文采用以下方案：

1.  使用 SDK 1.4.2 新增的接收音频回调 `onReceivedAudioFrame`，在接收侧将 PCM 音频交给应用，而不是按 SDK 播放进度获取音频。
2.  以外部模式启动 SDK 播放器，并配置 PCM 下行和 Audio 轨 Segment 模式。SDK 不向音频设备输出声音，应用使用独立播放器消费本地队列。
3.  应用自行管理缓存、播放进度、暂停、继续和停止。连接断开或引擎销毁时，不停止、不清空应用播放器，已经成功交付并保存的音频可继续播放。
4.  连接断开后如需继续合成，由应用获取新的连接凭证并重新连接。旧音频的保留、清空和新任务音频的追加策略均由应用决定。

<a id="准备工作"></a>

<a id="tts-prerequisites-title"></a>

## 准备工作

1.  开通阿里云百炼，在百炼控制台[获取 API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。API Key 只保存在业务 AppServer，不要写入客户端代码或提交到代码仓库。
2.  根据业务部署地域确认 AOQ Endpoint。地域和接入地址的选择方法请参见[选择地域、服务部署范围和接入域名](../model-user-guide/get-started-with-models/regions.md)。
3.  从[SDK 下载](../model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)获取 AOQ Client SDK，核对所用版本为 **1.4.2 或以上**，并包含接收音频回调能力。1.4.1 及更早版本不满足本文的版本要求。
4.  按 [Qwen-Audio-TTS 的 AOQ 鉴权步骤](../model-api-reference/realtime-api-directory/realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md#authentication)搭建业务 AppServer。每次建立新连接前，客户端都应从 AppServer 获取新的连接凭证。

<a id="导入-sdk"></a>

<a id="tts-import-sdk-title"></a>

### 导入 SDK

根据开发平台导入对应 SDK。后续接收音频回调和客户端代码以 Android Java 为例；其他平台的接口签名和音频数据生命周期请以对应 SDK API 文档为准。本文使用 PCM 下行，**不需要导入 Opus 插件**。

<a id="android"></a>

<a id="tts-android-title"></a>

#### Android

1.  将 `AoqClientSdk-release.aar` 放入 `app/libs`，并在 `app/build.gradle` 中配置依赖和 SDK 支持的 ABI：
    
    <a id="code-block"></a>
    
    ```groovy
    android {
        defaultConfig {
            minSdk 21
            ndk { abiFilters 'armeabi-v7a', 'arm64-v8a' }
        }
    }
    
    dependencies {
        implementation fileTree(dir: 'libs', include: ['*.aar'])
    }
    ```
    
2.  在 `AndroidManifest.xml` 中声明以下权限：
    
    <a id="code-block-2"></a>
    
    ```xml
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    ```
    
3.  本场景不需要申请麦克风或摄像头权限。
    

<a id="ios"></a>

<a id="tts-ios-title"></a>

#### iOS

1.  将 `AoqClientSdk.framework` 拖入 Xcode 工程，在 **Target > General > Frameworks, Libraries, and Embedded Content** 中选择 **Embed & Sign**。SDK 支持 iOS 13.0 及以上 arm64 设备。
2.  本场景不使用麦克风或摄像头，无需声明对应权限。
3.  Swift 工程使用 `import AoqClientSdk`；Objective-C 工程使用 `#import <AoqClientSdk/AoqClientSdk.h>`。

<a id="harmonyos"></a>

<a id="tts-harmony-title"></a>

#### HarmonyOS

1.  将 `AoqClientSdk.har` 放入 `entry/libs`，并在 `entry/oh-package.json5` 中声明依赖。该 SDK 兼容 API 12，支持 arm64-v8a：
    
    <a id="code-block-3"></a>
    
    ```json
    {
      "dependencies": {
        "@aoq/client-sdk": "file:./libs/AoqClientSdk.har"
      }
    }
    ```
    
2.  在 `entry/src/main/module.json5` 中声明以下权限：
    
    <a id="code-block-4"></a>
    
    ```json
    {
      "requestPermissions": [
        { "name": "ohos.permission.INTERNET" }
      ]
    }
    ```
    
3.  本场景不需要申请麦克风或摄像头权限。
    

<a id="实现流程"></a>

<a id="tts-flow-title"></a>

## 实现流程

1.  AppServer 通过 Inference Token 地址获取 qwen-audio-3.1-tts-flash 的 AOQ 连接参数，并返回给客户端。
2.  客户端创建引擎，注册并开启接收音频回调，以外部模式启动 SDK 播放器，配置 PCM 解码和 Audio 轨 Segment 订阅，发布和订阅 Data 轨，然后建立连接。
3.  连接成功后使用新的 `task_id` 发送 `run-task`。收到 `task-started` 后，按业务节奏发送一个或多个 `continue-task` 文本片段。
4.  SDK 在接收侧通过 `onReceivedAudioFrame` 将 PCM 交给应用。应用快速入队，在独立线程中使用 `AudioTrack` 播放；接收速度不受本地播放进度限制。
5.  所有文本发送完成后发送 `finish-task`。服务端继续返回剩余音频和任务事件。收到 `task-finished` 后更新任务状态，但不停止播放器，也不立即关闭音频回调。
6.  连接断开后，应用将本地输入标记为结束，继续播放队列和 `AudioTrack` 中已有的数据。本地输入结束且这些数据均播放完毕，才通知播放结束。
7.  如需再次合成，连接仍可用时使用新的 `task_id`；连接已断开时获取新的凭证并重新连接。不再需要引擎时将其释放，应用播放器在播放完毕或用户退出页面后另行关闭。

以下时序图只展示核心链路。缓存和播放器属于客户 App 的内部功能，以 App 自调用表示；客户端事件的具体先后顺序见后续实现步骤。

![实现流程: AOQ / PCM](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f91f1.png)

<a id="appserver-获取-token"></a>

<a id="tts-token-request-title"></a>

## AppServer 获取 Token

在 AppServer 设置 `DASHSCOPE_API_KEY`，并使用所选地域的 Endpoint 发送请求。`clientIp` 为客户端的真实公网 IP；该字段可选，但建议传入，以便服务分配合适的 Relay 接入点。 将 `ENDPOINT` 设为该地域业务空间的接入域名；如传入公网 IP，将其赋给 `CLIENT_REAL_IP`。

<a id="code-block-5"></a>

```bash
curl -X POST \
  "https://${ENDPOINT:?}/api/v1/webrtc/inference?model=qwen-audio-3.1-tts-flash" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "x-dashscope-rtc-transport: moq" \
  -d "{\"clientIp\": \"${CLIENT_REAL_IP:?}\"}"
```

如果 AppServer 无法获取客户端真实公网 IP，请删除 `clientIp` 字段，不要传空字符串。AppServer 将响应中的以下字段返回客户端；API Key 仅保存在 AppServer。

| 响应字段 | SDK 字段 |
| --- | --- |
| `aoqTokenForClient` | `AoqConnectConfig.token` |
| `sid` | `AoqConnectConfig.sid` |
| `clientRelayCertFingerprint` | `AoqConnectConfig.certFingerprint` |
| `clientRelayEndpoints` | `AoqConnectConfig.relayEndpoints` |
| `extraInfo.workspaceIdHash` | `AoqConnectConfig.workspaceIdHash` |

<a id="客户端实现-以-android-为例"></a>

<a id="tts-implementation-title"></a>

## 客户端实现（以 Android 为例）

客户端从 AppServer 获取 `AoqConnectConfig` 后，按以下步骤实现。代码片段中的 `main` 为主线程 `Handler`，`player` 为应用的 `PcmPlayer` 实例。完整类的组合方式见 [完整示例](#tts-complete-title)。

<a id="创建引擎并设置回调"></a>

<a id="tts-step-1-title"></a>

### 创建引擎并设置回调

创建 AOQ 单例引擎并注册连接状态、Data 轨消息和错误回调。SDK 回调运行在 SDK 内部线程，示例将连接状态和任务事件转到主线程处理。

<a id="code-block-6"></a>

```java
AoqClientListener listener = new AoqClientListener() {
    @Override
    public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
        main.post(() -> handleConnectionStatus(status));
    }

    @Override
    public void onDataMsg(AoqClientEngine.AoqDataMsg msg) {

        byte[] data = msg.data;

        main.post(() -> handleServerEvent(data));
    }

    @Override
    public void onError(int code, String message) {
        Log.e(TAG, "onError code=" + code + " message=" + message);
    }
};

AoqClientEngine.AoqCreateConfig createConfig = new AoqClientEngine.AoqCreateConfig();
createConfig.workDir = context.getFilesDir().getAbsolutePath();
engine = AoqClientEngine.createEngine(context, createConfig, listener);
```

<a id="开启接收音频回调"></a>

<a id="tts-observer-title"></a>

### 开启接收音频回调

先调用 `setAudioFrameObserver` 注册音频帧回调对象，再调用 `enableAudioFrameObserver` 开启 `AoqAudioSourceReceived`。请在 `connect`**之前**完成配置，不要依赖连接后开启来建立接收路径。

<a id="code-block-7"></a>

```java
engine.setAudioFrameObserver(new AoqClientListener.AoqAudioFrameListener() {
    @Override
    public void onReceivedAudioFrame(AoqClientEngine.AoqTrackType trackType,
                                     AoqClientEngine.AoqAudioFrameData frame) {
        // 回调中只做入队，不做耗时操作，也不调用 SDK 接口。
        try {
            if (trackType != AoqClientEngine.AoqTrackType.AoqTrackTypeAudio) return;
            if (frame.dataPtr == null || frame.dataSize <= 0 || frame.bytesPerSample != 2) return;
            player.enqueue(frame.samplesPerSec, frame.numOfChannels, frame.dataPtr, frame.dataSize);
        } catch (RuntimeException e) {
            Log.e(TAG, "enqueue pcm failed", e);
        }
    }
});

AoqClientEngine.AoqAudioObserverConfig observerConfig = new AoqClientEngine.AoqAudioObserverConfig();
observerConfig.sampleRate = 24000;  // 建议与 run-task 的 sample_rate 一致。
observerConfig.channels = 1;
observerConfig.mode = AoqClientEngine.AoqAudioObserverMode.AoqAudioObserverModeReadOnly;
int ret = engine.enableAudioFrameObserver(true,
        AoqClientEngine.AoqAudioSource.AoqAudioSourceReceived, observerConfig);
if (ret != 0) {
    throw new IllegalStateException("enableAudioFrameObserver failed: " + ret);
}
```

`AoqAudioObserverConfig` 参数说明：

| 参数 | 说明 |
| --- | --- |
| `sampleRate` | 回调音频的采样率。建议与 `run-task` 的 `sample_rate` 一致，避免额外的采样率转换 |
| `channels` | 回调音频的声道数，本文使用 1 |
| `mode` | 接收音频回调按只读处理。应设置为 `AoqAudioObserverModeReadOnly`；配置为读写模式时也按只读处理，不会将修改后的数据写回 SDK |

`onReceivedAudioFrame` 回调参数说明：

| 参数 | 说明 |
| --- | --- |
| `trackType` | 音频所属的轨道类型。本文只处理 `AoqTrackTypeAudio` |
| `frame` | 本次回调的 PCM 音频数据，字段说明见下表 |

`AoqAudioFrameData` 主要字段说明：

| 字段 | 说明 |
| --- | --- |
| `dataPtr` | 16 bit 交错 PCM 数据。Android Java 回调使用独立的 `byte[]`，应用可持有该数组引用供回调后播放，无需为延长生命周期再次复制；不要将此规则推广到其他平台的原生指针 |
| `dataSize` | 本次回调 PCM 数据的字节数 |
| `numOfSamples` | 本次回调每声道的采样点数，音频时长按实际值计算 |
| `bytesPerSample` | 每个采样点的字节数，本文为 2 |
| `numOfChannels` | 回调音频的声道数 |
| `samplesPerSec` | 回调音频的采样率 |
| `timeStamp` | 时间戳，单位为毫秒。应用按回调顺序入队，不使用任务事件推断播放进度 |

接收音频回调的使用限制：

1.  仅支持 PCM 下行和 Audio 轨 Segment 模式；输出为 16 bit PCM。不支持使用该回调接收 Opus 或 Stream 模式下的音频。
2.  回调在接收侧执行，不依赖 SDK 播放时钟。不要同时开启不需要的播放音频回调，以免继续维持 SDK 播放侧缓存。
3.  单次回调不等于单个网络包。应按 `dataSize` 和 `numOfSamples` 消费数据，不依赖网络包长度或假定句尾不足一帧的数据一定会补发。
4.  回调运行在 SDK 内部线程，只做快速入队。不要在回调中调用 `enableAudioFrameObserver`、`setAudioFrameObserver`、`disconnect`、`destroy` 等 SDK 接口，也不要等待主线程，否则可能导致死锁。
5.  连接断开后的播放保障范围是**应用已成功保存的 PCM**。尚未到达客户端或尚未通过回调交付的音频，不属于应用本地缓存；如业务要求与模型输出逐采样一致，需另外校验音频边界和完整性。

<a id="以外部模式启动播放器"></a>

<a id="tts-step-2-title"></a>

### 以外部模式启动播放器

音频由应用播放，但仍需调用 `startAudioPlayer`，并将 `isExternal` 设为 `true`。SDK 不向音频设备输出声音；在本文接收 PCM 的路径中，业务 Data 消息也无需等待 SDK 的播放进度。

<a id="code-block-8"></a>

```java
AoqClientEngine.AoqAudioPlaybackConfig playbackConfig = new AoqClientEngine.AoqAudioPlaybackConfig();
playbackConfig.isExternal = true;
playbackConfig.channel = 1;
engine.startAudioPlayer(playbackConfig);
```

> **说明**
>
> 不要省略这一步，也不要将 `isExternal` 设为 `false`。否则可能使带时间戳的任务事件等待 SDK 播放进度，或造成 SDK 与应用重复播放。应用播放器的扬声器、听筒等输出设备由应用自行管理。

<a id="配置解码器-轨道并建立连接"></a>

<a id="tts-step-3-title"></a>

### 配置解码器、轨道并建立连接

以下三处配置必须匹配：

1.  `setAudioDecoderConfig` 的 `codecType` 设为 `AoqEncoderTypeAudioPCM`。
2.  订阅 Audio 轨时，`trackMode` 设为 `AoqTrackModeSegment`。
3.  `run-task` 中的 `format` 设为 `pcm`，`sample_rate` 与解码器采样率一致。

<a id="code-block-9"></a>

```java
AoqClientEngine.AoqAudioCodecConfig audioDecoderConfig = new AoqClientEngine.AoqAudioCodecConfig();
audioDecoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
audioDecoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
audioDecoderConfig.sampleRate = 24000;
audioDecoderConfig.channel = 1;
engine.setAudioDecoderConfig(audioDecoderConfig);

AoqClientEngine.AoqTrackParam publishDataTrack = new AoqClientEngine.AoqTrackParam();
publishDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.publishTracks.add(publishDataTrack);

AoqClientEngine.AoqTrackParam subscribeAudioTrack = new AoqClientEngine.AoqTrackParam();
subscribeAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
subscribeAudioTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeSegment;
connectConfig.subscribeTracks.add(subscribeAudioTrack);

AoqClientEngine.AoqTrackParam subscribeDataTrack = new AoqClientEngine.AoqTrackParam();
subscribeDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.subscribeTracks.add(subscribeDataTrack);

engine.connect(connectConfig);
```

> **说明**
>
> 开启回调不代表配置一定生效。未满足 PCM + Segment 条件时，接收路径可能不启用或不能交付音频，这不一定导致连接失败，也没有固定的错误码。请同时检查实际下行格式、回调是否到达和 SDK 日志。

<a id="调用-senddatamsg-发送-run-task-事件"></a>

<a id="tts-step-4-title"></a>

### 调用 sendDataMsg 发送 run-task 事件

连接成功后为本轮生成新的 UUID `task_id`，并配置模型、音色、文本类型、音频格式和采样率。`format` 必须为 `pcm`，`sample_rate` 与解码器配置一致。其他可选参数请参见[客户端事件](qwen-audio-tts-client-events-26c1ffacfaed1e62.md)。

<a id="code-block-10"></a>

```java
taskId = UUID.randomUUID().toString();
JSONObject header = new JSONObject()
        .put("action", "run-task")
        .put("task_id", taskId)
        .put("streaming", "duplex");
JSONObject parameters = new JSONObject()
        .put("text_type", "PlainText")
        .put("voice", voice)
        .put("format", "pcm")
        .put("sample_rate", 24000);
JSONObject payload = new JSONObject()
        .put("task_group", "audio")
        .put("task", "tts")
        .put("function", "SpeechSynthesizer")
        .put("model", "qwen-audio-3.1-tts-flash")
        .put("input", new JSONObject())
        .put("parameters", parameters);
JSONObject runTask = new JSONObject().put("header", header).put("payload", payload);
AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
dataMessage.data = runTask.toString().getBytes(StandardCharsets.UTF_8);
engine.sendDataMsg(dataMessage);
```

<a id="调用-senddatamsg-发送-continue-task-事件"></a>

<a id="tts-step-5-title"></a>

### 调用 sendDataMsg 发送 continue-task 事件

只能在收到 `task-started` 后发送 `continue-task`。同一任务可连续发送多个片段；单次最多 20,000 个字符，累计最多 200,000 个字符。`run-task`、`continue-task` 和 `finish-task` 使用同一个 `task_id`。应及时发送后续片段或结束任务，不要依赖固定的连接超时秒数。

<a id="code-block-11"></a>

```java
JSONObject continueHeader = new JSONObject()
        .put("action", "continue-task")
        .put("task_id", taskId)
        .put("streaming", "duplex");
JSONObject payload = new JSONObject()
        .put("input", new JSONObject().put("text", text));
JSONObject continueTask = new JSONObject()
        .put("header", continueHeader)
        .put("payload", payload);
AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
dataMessage.data = continueTask.toString().getBytes(StandardCharsets.UTF_8);
engine.sendDataMsg(dataMessage);
```

<a id="处理服务端事件"></a>

<a id="tts-step-6-title"></a>

### 处理服务端事件

在 `onDataMsg` 中读取 `header.event`，维护任务状态并处理失败。`result-generated` 返回句子元信息，音频通过 Audio 轨接收后由 `onReceivedAudioFrame` 交给应用。完整字段请参见[服务端事件](qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md)。

<a id="code-block-12"></a>

```java
JSONObject header = new JSONObject(new String(data, StandardCharsets.UTF_8)).optJSONObject("header");
if (header == null) return;
String name = header.optString("event");
if ("task-started".equals(name)) {
    // 可以发送一个或多个 continue-task 事件。
} else if ("result-generated".equals(name)) {
    // 句子元信息，不在此处推动播放器进度。
} else if ("task-finished".equals(name)) {
    taskActive = false;
    // 仅更新任务状态，不在此处停止播放器或标记音频输入结束。
} else if ("task-failed".equals(name)) {
    taskActive = false;
    String message = header.optString("error_message");
    // 展示或记录错误；是否停止合成、清空已收到的音频由业务决定。
}
```

本文完整示例采用保守的输入结束策略：连接进入终态，或显式释放连接和回调后，才调用 `player.markInputEnded()`。该策略用于封口本地音频输入，并不证明模型生成的所有音频都已到达。

如果连接一直保持可用，可继续接收和播放，不必为了播放而等待连接断开；但仅凭 `task-finished` 不进行本轮音频输入封口，也不生成逐任务的播放完成通知。

<a id="调用-senddatamsg-发送-finish-task-事件"></a>

<a id="tts-step-7-title"></a>

### 调用 sendDataMsg 发送 finish-task 事件

发送完全部文本后立即发送 `finish-task`，以合成服务端缓存的不完整语句，并等待后续音频和任务事件。详细规则请参见[客户端事件](qwen-audio-tts-client-events-26c1ffacfaed1e62.md)。

<a id="code-block-13"></a>

```java
JSONObject finishHeader = new JSONObject()
        .put("action", "finish-task")
        .put("task_id", taskId)
        .put("streaming", "duplex");
JSONObject finishTask = new JSONObject()
        .put("header", finishHeader)
        .put("payload", new JSONObject().put("input", new JSONObject()));
AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
dataMessage.data = finishTask.toString().getBytes(StandardCharsets.UTF_8);
engine.sendDataMsg(dataMessage);
```

不要在发送 `finish-task` 后立即断开连接。收到 `task-finished` 也不表示已播放完成；如需主动提前释放连接，应确认不会截断仍在传输的音频，或明确接受中止接收。

<a id="在应用中缓存并播放音频"></a>

<a id="tts-buffer-title"></a>

### 在应用中缓存并播放音频

应用播放器应满足以下要求：

1.  **快速入队**：回调中只提交 PCM，在独立播放线程中写入 `AudioTrack`，不要让设备写入阻塞 SDK 回调。
2.  **独立生命周期**：连接断开、引擎销毁时不清空本地队列，也不释放应用播放器。
3.  **区分缓存与实际播放**：队列为空不代表设备已经播放完毕，仍需检查 `AudioTrack` 已消耗所有写入的采样点。
4.  **支持业务控制**：暂停、继续和清空由应用实现。需要保留历史音频用于重播时，应另行保存数据，不能依赖已消费的播放队列。

播放器实现见 [完整示例](#tts-complete-title)中的 `PcmPlayer` 类。

24 kHz、单声道、16 bit PCM 的数据量为每秒 48,000 字节，即每分钟约 2.75 MiB。长文本会快速积累缓存，应用应按业务可接受的内存占用设置缓存预算；超出预算时可保存到本地文件并边读边播。文件写入也应放在独立线程，不在 SDK 回调中直接执行。

<a id="处理连接断开与播放完成"></a>

<a id="tts-terminal-title"></a>

### 处理连接断开与播放完成

请区分以下状态：

| 状态 | 判断条件 | 处理方法 |
| --- | --- | --- |
| 合成任务结束 | 收到 `task-finished` 或 `task-failed` | 更新任务状态；不停止播放，不单独据此判断音频回调全部完成 |
| 本地输入结束 | 连接状态为 `Disconnected` 或 `Failed`，或应用完成连接及回调的释放 | 调用 `markInputEnded()`；不清空队列 |
| 本地播放结束 | 本地输入已结束，队列为空，且 `AudioTrack` 已播放完所有成功写入的数据 | 通知播放完成，释放本轮 `AudioTrack` |

<a id="code-block-14"></a>

```java
private void handleConnectionStatus(AoqClientEngine.AoqConnectionStatus status) {
    if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusConnected) {
        if (!closing && !connected) {
            connected = true;
            callback.onConnected(this);
        }
    } else if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusDisconnected
            || status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusFailed) {
        connectionEnded = true;
        connected = false;
        taskActive = false;
        if (closing) {
            finishClose();  // 已请求释放：此时才注销回调并销毁引擎。
        } else {
            player.markInputEnded();  // 封口本地输入，已保存的音频继续播放。
        }
    }
}
```

`closing`、`connectionEnded` 和 `finishClose()` 用于管理异步释放流程，完整定义见 [完整示例](#tts-complete-title)。

注意事项：

1.  连接断开时不要停止或清空应用播放器。连接终态只表示不会继续从该连接接收音频，不等于本地播放已经完成。
2.  网络异常断开可能发生在音频未全部到达时。本方案可继续播放已保存的音频，但不能补回尚未收到的部分。
3.  用户主动停止属于丢弃音频的操作，可先暂停、清空本地播放并禁止继续保留音频，再异步结束连接。用户退出页面时，根据页面生命周期关闭应用播放器。

<a id="连接断开后继续合成"></a>

<a id="tts-scenario-1-title"></a>

#### 连接断开后继续合成

服务端空闲约 60 秒后会主动断开连接，具体时长以服务端为准。长文本场景中，服务端合成任务结束时，应用本地仍可能有较长的待播放音频；连接因此可能在播放过程中结束。

已经断开的连接不能直接继续发送任务。原连接凭证不要再次使用，如需继续合成，请按以下步骤处理：

1.  释放旧引擎，保留应用播放器和本地队列。
2.  从 AppServer 获取新的连接凭证。
3.  重新创建引擎，[按前述步骤完成引擎配置](#tts-step-1-title)并调用 `connect`。
4.  连接成功后，使用新的 `task_id` 发送 `run-task`。根据业务需要保留旧音频继续追加，或在新任务开始前清空旧音频。

<a id="code-block-15"></a>

```java
// 当前 client 对应的连接已断开；等待旧单例引擎真正释放后再创建新引擎。
private void synthesizeAfterDisconnect(String text, String voice) {
    client.close(() -> appServer.fetchConnectConfig(connectConfig -> main.post(() -> {
        client = new LongTtsClient(context, connectConfig, player, callback);
        pendingRequest = new Pair<>(text, voice);  // 在连接成功后调用 client.synthesize。
    })));
}
```

`appServer.fetchConnectConfig` 和 `pendingRequest` 表示应用的凭证获取及待提交请求管理逻辑，请按实际业务实现。不要把自动重连、旧任务恢复和缓存清空策略交由 SDK 隐式决定。

<a id="断开连接并销毁引擎"></a>

<a id="tts-step-8-title"></a>

### 断开连接并销毁引擎

不再接收音频时，先请求断开连接，等待连接状态进入 `Disconnected` 或 `Failed`，再在主线程中注销回调并销毁引擎。`disconnect()` 是异步操作，调用返回不代表已到达的数据已处理完毕；不要紧接着清空回调对象，也不要在 SDK 回调线程中等待断连完成。

<a id="code-block-16"></a>

```java
// 请求关闭时：若已经收到终态，可直接清理；否则保留 observer 等待终态回调。
closing = true;
if (connectionEnded) {
    finishClose();
} else {
    engine.disconnect();
}

// 由主线程上的连接终态处理逻辑调用，不在 SDK 回调线程中调用。
private void finishClose() {
    engine.enableAudioFrameObserver(false,
            AoqClientEngine.AoqAudioSource.AoqAudioSourceReceived,
            new AoqClientEngine.AoqAudioObserverConfig());
    engine.setAudioFrameObserver(null);
    AoqClientEngine.destroy();
    player.markInputEnded();
}

// 销毁引擎不停止本地播放。
// 本地音频播放完毕，或用户退出页面后再调用 player.close()。
```

主动断开会中止后续网络接收，不应将其用于证明音频已经完整收到。应用缓存和播放器的释放由应用另行控制。

<a id="主要服务端事件"></a>

<a id="tts-events-title"></a>

## 主要服务端事件

| 事件 | 说明 | 应用处理方法 |
| --- | --- | --- |
| `task-started` | 任务已启动，可以发送 `continue-task` | 提交文本 |
| `result-generated` | 返回句子元信息，对应音频通过 Audio 轨返回 | 记录合成结果；不据此推进或结束本地播放 |
| `task-finished` | 所有缓存文本已处理，合成任务结束 | 更新任务状态，继续接收和播放；不单独据此封口音频输入 |
| `task-failed` | 任务失败，应读取错误码和错误消息 | 展示或记录错误；继续播放还是主动停止由业务决定 |

<a id="完整示例"></a>

<a id="tts-complete-title"></a>

## 完整示例

以下示例包含两个类：

1.  `LongTtsClient`：负责引擎、连接和任务事件。构造时传入由 AppServer Token 响应转换得到的 `AoqConnectConfig`，连接成功后调用 `synthesize(text, voice)`。该类的构造和公开方法在主线程调用。
2.  `PcmPlayer`：负责本地缓存和播放，生命周期独立于连接。SDK 回调只提交 PCM，音频队列和设备状态在播放线程中访问，业务控制方法在主线程调用。播放完成通知在主线程交付，并通过输入代次过滤清空或新输入之前的旧通知。

示例等待连接终态后封口本地输入，`close()` 只发起异步关闭请求；`close(Runnable)` 的回调在旧引擎释放后执行，可用于安全创建新的单例引擎。连接保持可用时，即使队列暂时播放完毕，也可继续追加音频；`onPlaybackFinished` 不是每个 `task_id` 的播放完成事件。

部分设备需要预填充一定音频量才开始流式播放。示例在输入封口后非阻塞补静音，直到播放头越过真实音频末帧；静音不计入真实 PCM 时长。排空期间收到的新输入留在队列，旧 `AudioTrack` 释放后再写入新实例，避免静音破坏真实音频计数。

生产代码还需补充界面状态、超长音频的存储与缓存预算、播放器错误和播放头长期不前进的处理，以及业务侧的新连接管理。以下两个类可保存在一个 `LongTtsClient.java` 中；拆为两个文件时，分别保留所需的 import，并放入同一包。

<a id="code-block-17"></a>

```java
import android.content.Context;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.Looper;
import android.util.Log;


import com.alibaba.aoq.clientsdk.AoqClientEngine;
import com.alibaba.aoq.clientsdk.AoqClientListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.ArrayDeque;
import java.util.UUID;

public final class LongTtsClient {
    private static final String TAG = "LongTtsClient";
    private static final String MODEL = "qwen-audio-3.1-tts-flash";
    static final int SAMPLE_RATE = 24000;

    public interface Callback {
        void onConnected(LongTtsClient client);
        void onPlaybackFinished();
        void onTaskFailed(String message);
    }

    private final Handler main = new Handler(Looper.getMainLooper());
    private final PcmPlayer player;
    private final Callback callback;
    private AoqClientEngine engine;
    private String taskId;
    private String pendingText;
    private String pendingVoice;
    private boolean connected;
    private boolean taskActive;
    private boolean connectionEnded;
    private boolean closing;
    private boolean closed;
    private volatile boolean discardReceived;
    private Runnable afterClose;

    public LongTtsClient(Context context, AoqClientEngine.AoqConnectConfig connectConfig,
                         PcmPlayer player, Callback callback) {
        this.player = player;
        this.callback = callback;
        player.setOnFinishedListener(callback::onPlaybackFinished);

        AoqClientListener listener = new AoqClientListener() {
            @Override
            public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
                main.post(() -> {
                    if (!closed) handleConnectionStatus(status);
                });
            }

            @Override
            public void onDataMsg(AoqClientEngine.AoqDataMsg msg) {

                byte[] data = msg.data;

                main.post(() -> {
                    if (!closed && !closing) handleServerEvent(data);
                });
            }

            @Override
            public void onError(int code, String message) {
                Log.e(TAG, "onError code=" + code + " message=" + message);
            }
        };

        AoqClientEngine.AoqCreateConfig createConfig = new AoqClientEngine.AoqCreateConfig();
        createConfig.workDir = context.getFilesDir().getAbsolutePath();
        engine = AoqClientEngine.createEngine(context, createConfig, listener);

        // 在 connect 之前开启接收音频回调。
        engine.setAudioFrameObserver(new AoqClientListener.AoqAudioFrameListener() {
            @Override
            public void onReceivedAudioFrame(AoqClientEngine.AoqTrackType trackType,
                                             AoqClientEngine.AoqAudioFrameData frame) {
                try {
                    if (discardReceived) return;  // 用户主动停止后不再保留音频。
                    if (trackType != AoqClientEngine.AoqTrackType.AoqTrackTypeAudio) return;
                    if (frame.dataPtr == null || frame.dataSize <= 0 || frame.bytesPerSample != 2) return;
                    player.enqueue(frame.samplesPerSec, frame.numOfChannels, frame.dataPtr, frame.dataSize);
                } catch (RuntimeException e) {
                    Log.e(TAG, "enqueue pcm failed", e);
                }
            }
        });
        AoqClientEngine.AoqAudioObserverConfig observerConfig = new AoqClientEngine.AoqAudioObserverConfig();
        observerConfig.sampleRate = SAMPLE_RATE;
        observerConfig.channels = 1;
        observerConfig.mode = AoqClientEngine.AoqAudioObserverMode.AoqAudioObserverModeReadOnly;
        int ret = engine.enableAudioFrameObserver(true,
                AoqClientEngine.AoqAudioSource.AoqAudioSourceReceived, observerConfig);
        if (ret != 0) throw new IllegalStateException("enableAudioFrameObserver failed: " + ret);

        // 外部播放模式：SDK 不输出声音，业务 Data 不等待 SDK 播放进度。
        AoqClientEngine.AoqAudioPlaybackConfig playbackConfig = new AoqClientEngine.AoqAudioPlaybackConfig();
        playbackConfig.isExternal = true;
        playbackConfig.channel = 1;
        engine.startAudioPlayer(playbackConfig);

        AoqClientEngine.AoqAudioCodecConfig audioDecoderConfig = new AoqClientEngine.AoqAudioCodecConfig();
        audioDecoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        audioDecoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
        audioDecoderConfig.sampleRate = SAMPLE_RATE;
        audioDecoderConfig.channel = 1;
        engine.setAudioDecoderConfig(audioDecoderConfig);

        AoqClientEngine.AoqTrackParam publishDataTrack = new AoqClientEngine.AoqTrackParam();
        publishDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
        connectConfig.publishTracks.add(publishDataTrack);

        AoqClientEngine.AoqTrackParam subscribeAudioTrack = new AoqClientEngine.AoqTrackParam();
        subscribeAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        subscribeAudioTrack.trackMode = AoqClientEngine.AoqTrackMode.AoqTrackModeSegment;
        connectConfig.subscribeTracks.add(subscribeAudioTrack);

        AoqClientEngine.AoqTrackParam subscribeDataTrack = new AoqClientEngine.AoqTrackParam();
        subscribeDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
        connectConfig.subscribeTracks.add(subscribeDataTrack);

        engine.connect(connectConfig);
    }

    /** 主线程调用；连接成功且没有进行中的任务时，提交一轮合成。 */
    public void synthesize(String text, String voice) {
        if (!connected || taskActive) {
            throw new IllegalStateException("The connection is not ready or a task is active.");
        }
        taskId = UUID.randomUUID().toString();
        pendingText = text;
        pendingVoice = voice;
        taskActive = true;
        player.beginInput();
        sendRunTask();
    }

    /** 主线程调用；立即请求停止本地播放，并异步结束连接。 */
    public void stop() {
        if (closed) {
            player.clear();
            player.setPaused(false);
            return;
        }
        discardReceived = true;
        player.setPaused(true);
        player.clear();
        close();
    }

    /** 主线程调用；异步释放连接和引擎，已保存的音频继续播放。 */
    public void close() {
        close(null);
    }

    /** afterClose 在主线程执行，可用于等待旧单例引擎释放后创建新引擎。 */
    public void close(Runnable afterClose) {
        if (closed) {
            if (afterClose != null) afterClose.run();
            return;
        }
        if (afterClose != null) this.afterClose = afterClose;
        if (closing) return;
        closing = true;
        connected = false;
        taskActive = false;
        if (connectionEnded) {
            finishClose();
        } else {
            engine.disconnect();  // 异步操作，等待连接终态回调，不立即注销 observer。
        }
    }

    private void finishClose() {
        if (closed) return;
        closed = true;
        engine.enableAudioFrameObserver(false,
                AoqClientEngine.AoqAudioSource.AoqAudioSourceReceived,
                new AoqClientEngine.AoqAudioObserverConfig());
        engine.setAudioFrameObserver(null);
        AoqClientEngine.destroy();
        engine = null;
        if (discardReceived) {
            // 排空结束后再次清空，消除停止请求与已进入回调之间的竞争。
            player.clear();
            player.setPaused(false);
        } else {
            player.markInputEnded();
        }
        Runnable done = afterClose;
        afterClose = null;
        if (done != null) done.run();
    }

    private void handleConnectionStatus(AoqClientEngine.AoqConnectionStatus status) {
        if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusConnected) {
            if (!closing && !connected) {
                connected = true;
                callback.onConnected(this);
            }
        } else if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusDisconnected
                || status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusFailed) {
            connectionEnded = true;
            connected = false;
            taskActive = false;
            if (closing) {
                finishClose();
            } else {
                player.markInputEnded();
            }
        }
    }


    private void handleServerEvent(byte[] data) {

        try {
            JSONObject header = new JSONObject(new String(data, StandardCharsets.UTF_8))
                    .optJSONObject("header");
            if (header == null) return;
            String incomingTaskId = header.optString("task_id", "");
            if (!incomingTaskId.isEmpty() && !incomingTaskId.equals(taskId)) return;
            String event = header.optString("event");
            if ("task-started".equals(event)) {
                sendContinueTask();
                sendFinishTask();
            } else if ("task-finished".equals(event)) {
                taskActive = false;
                // 任务事件不是音频接收完成屏障，不在此处 markInputEnded。
            } else if ("task-failed".equals(event)) {
                taskActive = false;
                callback.onTaskFailed(header.optString("error_message"));
            }
        } catch (JSONException e) {
            Log.w(TAG, "Invalid server event", e);
        }
    }

    private void sendRunTask() {
        try {
            JSONObject parameters = new JSONObject()
                    .put("text_type", "PlainText")
                    .put("voice", pendingVoice)
                    .put("format", "pcm")
                    .put("sample_rate", SAMPLE_RATE);
            JSONObject payload = new JSONObject()
                    .put("task_group", "audio")
                    .put("task", "tts")
                    .put("function", "SpeechSynthesizer")
                    .put("model", MODEL)
                    .put("input", new JSONObject())
                    .put("parameters", parameters);
            send(header("run-task"), payload);
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create run-task", e);
        }
    }

    private void sendContinueTask() {
        try {
            send(header("continue-task"),
                    new JSONObject().put("input", new JSONObject().put("text", pendingText)));
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create continue-task", e);
        }
    }

    private void sendFinishTask() {
        try {
            send(header("finish-task"), new JSONObject().put("input", new JSONObject()));
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create finish-task", e);
        }
    }

    private JSONObject header(String action) throws JSONException {
        return new JSONObject()
                .put("action", action)
                .put("task_id", taskId)
                .put("streaming", "duplex");
    }

    private void send(JSONObject header, JSONObject payload) throws JSONException {
        AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
        dataMessage.data = new JSONObject().put("header", header).put("payload", payload)
                .toString().getBytes(StandardCharsets.UTF_8);
        engine.sendDataMsg(dataMessage);
    }
}

/** 本地 PCM 缓存与播放；内部状态只在播放线程中访问。 */
final class PcmPlayer implements AutoCloseable {
    private static final String TAG = "PcmPlayer";
    private static final int CHANNEL_MASK = AudioFormat.CHANNEL_OUT_MONO;
    private static final int ENCODING = AudioFormat.ENCODING_PCM_16BIT;

    private final int sampleRate;
    private final HandlerThread thread = new HandlerThread("tts-local-playout");
    private final Handler worker;
    private final Handler main = new Handler(Looper.getMainLooper());
    private final ArrayDeque<ByteBuffer> queue = new ArrayDeque<>();
    private final ByteBuffer finishSilence = ByteBuffer.allocate(2048);
    private final Runnable pump = this::pump;
    private volatile boolean closed;
    private Runnable onFinished;
    private long inputGeneration;  // 主线程访问，取消已投递的旧完成通知。
    private long workerGeneration; // 播放线程访问，标记当前输入。
    private boolean tailDraining;

    private AudioTrack track;
    private long writtenFrames;
    private boolean inputEnded = true;
    private boolean finishNotified = true;
    private boolean paused;
    private boolean pumpScheduled;

    PcmPlayer(int sampleRate) {
        this.sampleRate = sampleRate;
        thread.start();
        worker = new Handler(thread.getLooper());
    }

    void setOnFinishedListener(Runnable listener) {
        worker.post(() -> onFinished = listener);
    }

    /** 可在 SDK 回调线程调用，只向播放线程提交音频。 */

    void enqueue(int frameSampleRate, int channels, byte[] pcm, int byteCount) {

        if (closed || frameSampleRate != sampleRate || channels != 1 || byteCount <= 0
                || byteCount > pcm.length || (byteCount & 1) != 0) return;
        worker.post(() -> {
            if (closed) return;
            queue.addLast(ByteBuffer.wrap(pcm, 0, byteCount));
            schedulePump(0);
        });
    }

    /** 主线程调用；开始新输入，可保留上一轮尚未播放完的音频。 */
    void beginInput() {
        long generation = ++inputGeneration;
        worker.post(() -> {
            workerGeneration = generation;
            inputEnded = false;
            finishNotified = false;
        });
    }

    /** 确认不会再有该输入的音频后调用，不清空队列。 */
    void markInputEnded() {
        worker.post(() -> {
            inputEnded = true;
            schedulePump(0);
        });
    }

    void setPaused(boolean pause) {
        worker.post(() -> {
            paused = pause;
            if (pause && track != null) track.pause();
            if (!pause) schedulePump(0);
        });
    }

    /** 主线程调用；丢弃全部音频，取消旧完成通知。 */
    void clear() {
        ++inputGeneration;
        worker.post(() -> {
            worker.removeCallbacks(pump);
            pumpScheduled = false;
            queue.clear();
            inputEnded = true;
            finishNotified = true;
            releaseTrack();
        });
    }

    @Override
    public void close() {
        if (closed) return;
        ++inputGeneration;
        closed = true;
        worker.post(() -> {
            worker.removeCallbacks(pump);
            queue.clear();
            releaseTrack();
            thread.quitSafely();
        });
    }

    private void schedulePump(long delayMs) {
        if (pumpScheduled || paused || closed) return;
        pumpScheduled = true;
        worker.postDelayed(pump, delayMs);
    }

    private void pump() {
        pumpScheduled = false;
        if (closed || paused) return;
        try {
            if (!queue.isEmpty() && track == null) track = createTrack();
            if (track == null) {
                if (inputEnded) notifyFinishedOnce();
                return;
            }
            if (track.getPlayState() != AudioTrack.PLAYSTATE_PLAYING) track.play();
            if (tailDraining) {
                drainTail();
                return;
            }
            // 单次最多提交约 100 ms 的单声道 16 bit PCM。
            int budget = sampleRate / 5;
            while (budget > 0 && !queue.isEmpty()) {
                ByteBuffer head = queue.getFirst();
                int written = track.write(head, Math.min(head.remaining(), budget),
                        AudioTrack.WRITE_NON_BLOCKING);
                if (written < 0) throw new IllegalStateException("AudioTrack.write: " + written);
                if (written == 0) break;
                writtenFrames += written / 2;
                budget -= written;
                if (!head.hasRemaining()) queue.removeFirst();
            }
            if (inputEnded && queue.isEmpty()) {
                tailDraining = true;
                drainTail();
                return;
            }
            long playedFrames = track.getPlaybackHeadPosition() & 0xffffffffL;
            if (queue.isEmpty() && playedFrames >= writtenFrames) {
                track.pause();
                return;  // 输入仍开放，后续 enqueue 会继续驱动播放。
            }
        } catch (RuntimeException e) {
            Log.e(TAG, "Local playback failed", e);
            releaseTrack();
            return;
        }
        schedulePump(10);
    }

    /** 封口后补静音满足设备启动阈值，只统计真实 PCM 的 writtenFrames。 */
    private void drainTail() {
        long playedFrames = track.getPlaybackHeadPosition() & 0xffffffffL;
        if (playedFrames >= writtenFrames) {
            releaseTrack();
            if (inputEnded && queue.isEmpty()) notifyFinishedOnce();
            if (!queue.isEmpty()) schedulePump(0);
            return;
        }
        finishSilence.clear();
        int n = track.write(finishSilence, finishSilence.remaining(),
                AudioTrack.WRITE_NON_BLOCKING);
        if (n < 0) throw new IllegalStateException("AudioTrack padding write: " + n);
        // 不把静音加入 writtenFrames；新输入留在队列，旧 Track 排空后另建 Track。
        schedulePump(10);
    }

    /** 主线程交付前再校验代次，防止清空或新输入后收到旧完成通知。 */
    private void notifyFinishedOnce() {
        if (finishNotified) return;
        finishNotified = true;
        long generation = workerGeneration;
        Runnable listener = onFinished;
        main.post(() -> {
            if (!closed && generation == inputGeneration && listener != null) listener.run();
        });
    }

    private AudioTrack createTrack() {
        int minBytes = AudioTrack.getMinBufferSize(sampleRate, CHANNEL_MASK, ENCODING);
        if (minBytes <= 0) throw new IllegalStateException("Unsupported PCM output");
        AudioTrack output = new AudioTrack(
                new AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_MEDIA)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                        .build(),
                new AudioFormat.Builder()
                        .setSampleRate(sampleRate)
                        .setChannelMask(CHANNEL_MASK)
                        .setEncoding(ENCODING)
                        .build(),
                Math.max(minBytes, sampleRate / 5), AudioTrack.MODE_STREAM,
                AudioManager.AUDIO_SESSION_ID_GENERATE);
        if (output.getState() != AudioTrack.STATE_INITIALIZED) {
            output.release();
            throw new IllegalStateException("AudioTrack initialization failed");
        }
        writtenFrames = 0;
        return output;
    }

    private void releaseTrack() {
        if (track != null) {
            track.release();
            track = null;
        }
        writtenFrames = 0;
        tailDraining = false;
    }
}
```

调用方式：

<a id="code-block-18"></a>

```java
// 在主线程创建；播放器的生命周期跟随页面，而不是连接。
PcmPlayer player = new PcmPlayer(LongTtsClient.SAMPLE_RATE);
LongTtsClient.Callback callback = new LongTtsClient.Callback() {
    @Override public void onConnected(LongTtsClient session) {
        // voice 为模型支持的系统音色或有效 voice_id。
        session.synthesize(text, voice);
    }
    @Override public void onPlaybackFinished() { Log.i("TTS", "Playback complete"); }
    @Override public void onTaskFailed(String message) { Log.e("TTS", message); }
};
LongTtsClient client = new LongTtsClient(context, connectConfig, player, callback);


// 暂停或继续播放，不影响音频接收。
// player.setPaused(true);
// player.setPaused(false);

// 用户主动停止时：client.stop();
// 页面退出时：
// client.close();
// player.close();
```

<a id="相关文档"></a>

<a id="tts-related-title"></a>

## 相关文档

如需查看完整参数、事件字段或其他平台接口，请参见：

1.  [获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)
2.  [选择地域、服务部署范围和接入域名](../model-user-guide/get-started-with-models/regions.md)
3.  [AOQ Client SDK 简介](../model-api-reference/more-about-models/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
4.  [SDK 下载](../model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md)
5.  [Qwen-Audio-TTS AOQ 接入](../model-api-reference/realtime-api-directory/realtime-tts-model-apis/qwen-audio-tts-api/qwen-audio-tts-aoq-access.md)
6.  [Qwen-Audio-TTS 用户指南](../model-user-guide/model-experience/speech-and-audio/speech-synthesis/realtime-tts-user-guide.md)
7.  [客户端事件](qwen-audio-tts-client-events-26c1ffacfaed1e62.md)
8.  [服务端事件](qwen-audio-tts-server-events-e9137ffe8f4e3d2c.md)
