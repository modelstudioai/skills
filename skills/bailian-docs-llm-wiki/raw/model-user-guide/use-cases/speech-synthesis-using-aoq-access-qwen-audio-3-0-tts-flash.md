# 使用 AOQ 接入 qwen-audio-3.0-tts-flash 实现语音合成

通过 AOQ 接入 qwen-audio-3.0-tts-flash，分段发送文本并实时播放合成语音。客户端代码以 Android Java 为例。

## 方案概述

qwen-audio-3.0-tts-flash 支持 AOQ Inference 事件协议。本教程选择该模型演示通过 AOQ 进行流式语音合成：客户端通过 Data 轨发送 run-task、continue-task 和 finish-task，服务端通过 Audio 轨流式返回音频，并通过 Data 轨返回任务事件。

同一任务可以多次发送 continue-task。完整语句会尽快合成，不完整语句会暂存在服务端，直到后续文本补全或客户端发送 finish-task。该方式适合移动端播报、长文本分段输入和低延迟语音输出。

## 准备工作

1.  开通阿里云百炼，并按[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。API Key 只保存在业务 AppServer，不要写入客户端代码或提交到代码仓库。
2.  根据业务部署地域确认 AOQ Endpoint。地域和接入地址的选择方法请参见[选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。
3.  从[SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)获取最新版 AOQ Client SDK。
4.  搭建业务 AppServer，并按[Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)实现服务端代理鉴权。每次建立新连接前，客户端都应从 AppServer 获取新的连接凭证。

### 导入 SDK

根据开发平台导入对应 SDK。后续客户端代码以 Android Java 为例，其他平台使用相同的接口设计和事件流程。本文以 PCM 音频流为例；如果业务选择 Opus，请按 SDK 下载文档导入对应插件。

#### Android

1.  将 AoqClientSdk-release.aar 放入 app/libs，并在 app/build.gradle 中配置依赖和 SDK 支持的 ABI：

```
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

2.  在 AndroidManifest.xml 中声明以下权限：

```
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

3.  本场景不需要申请麦克风或摄像头权限。

#### iOS

1.  将 AoqClientSdk.framework 拖入 Xcode 工程，在 Target > General > Frameworks, Libraries, and Embedded Content 中选择 Embed & Sign。SDK 支持 iOS 13.0 及以上 arm64 设备。
2.  本场景不使用麦克风或摄像头，无需声明对应权限。
3.  Swift 工程使用 import AoqClientSdk；Objective-C 工程使用 #import <AoqClientSdk/AoqClientSdk.h>。

#### HarmonyOS

1.  将 AoqClientSdk.har 放入 entry/libs，并在 entry/oh-package.json5 中声明依赖。该 SDK 兼容 API 12，支持 arm64-v8a：

```
{
  "dependencies": {
    "@aoq/client-sdk": "file:./libs/AoqClientSdk.har"
  }
}
```

2.  在 entry/src/main/module.json5 中声明以下权限：

```
"requestPermissions": [
  { "name": "ohos.permission.INTERNET" }
]
```

3.  本场景不需要申请麦克风或摄像头权限。

#### Linux (Python)

1.  解压 SDK，并保持 aoq\_client\_sdk.py、libAoqClientSdk.so 和 libonnxruntime.so.1.16.3 位于同一目录。
2.  将 SDK 目录加入 Python 和动态库搜索路径：

```
export PYTHONPATH="$PWD/AoqClientSdk:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/AoqClientSdk:$LD_LIBRARY_PATH"
```

3.  在 Python 代码中使用 import aoq\_client\_sdk。也可通过 AOQ\_CLIENT\_SDK\_LIB 指定 libAoqClientSdk.so 的绝对路径。

## 体验 Demo

阿里云百炼提供适用于 Android 平台的 Demo，可用于快速验证 AOQ 接入效果。下载 APK 并配置 API Key 和 `workspaceId` 后，即可体验部分模型。

扫描以下二维码下载 Demo：

![Demo 下载二维码](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7714207871/p1095700.png)

## 实现流程

1.  AppServer 通过 Inference Token 地址获取 qwen-audio-3.0-tts-flash 的 AOQ 连接参数。
2.  客户端发布 Data 轨，订阅 Audio 和 Data 轨，并按 run-task 中选择的输出音频格式配置 SDK 解码参数。
3.  客户端启动本地播放器并建立 AOQ 连接；连接成功后使用新的 task\_id 发送 run-task。
4.  收到 task-started 后，按业务节奏发送一个或多个 continue-task 文本片段。
5.  所有文本发送完成后发送 finish-task。服务端继续返回剩余音频，最终返回 task-finished。
6.  收到 task-finished 后，可在同一 AOQ 连接上使用新的 task\_id 开始下一轮合成，或断开连接并销毁引擎。

![AOQ 流式语音合成时序图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2418966871/p1094860.png)

## AppServer 获取 Token

在 AppServer 设置 DASHSCOPE\_API\_KEY，并使用所选地域的 Endpoint 发送请求。clientIp 为客户端的真实公网 IP；该字段可选，但建议传入，以便服务分配合适的 Relay 接入点。

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/inference?model=qwen-audio-3.0-tts-flash" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -H "x-dashscope-rtc-transport: moq" \
  -d "{\"clientIp\": \"${CLIENT_REAL_IP}\"}"
```

**说明**如果 AppServer 无法获取客户端真实公网 IP，请删除 clientIp 字段，不要传空字符串。

AppServer 将响应中的以下字段返回客户端。生产环境中不要把 API Key 返回客户端。完整请求和响应字段请参见[Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)。

**响应字段**

**SDK 字段**

aoqTokenForClient

AoqConnectConfig.token

sid

AoqConnectConfig.sid

clientRelayCertFingerprint

AoqConnectConfig.certFingerprint

clientRelayEndpoints

AoqConnectConfig.relayEndpoints

extraInfo.workspaceIdHash

AoqConnectConfig.workspaceIdHash

## 实现 Android 客户端

客户端从 AppServer 获取 AoqConnectConfig 后，按以下步骤实现 Android 端流式语音合成。

### 1\. 创建引擎并设置回调

创建 AOQ 单例引擎并注册连接与 Data 轨事件回调。客户需要在连接状态回调中维护可用状态，并把任务事件交给业务状态机。

```
AoqClientListener listener = new AoqClientListener() {
    @Override
    public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
        connected = status == AoqClientEngine.AoqConnectionStatus
                .AoqConnectionStatusConnected;
    }

    @Override
    public void onDataMsg(AoqClientEngine.AoqDataMsg msg) {
        handleServerEvent(msg);
    }
};

AoqClientEngine.AoqCreateConfig createConfig = new AoqClientEngine.AoqCreateConfig();
createConfig.workDir = context.getFilesDir().getAbsolutePath();
engine = AoqClientEngine.createEngine(context, createConfig, listener);
```

### 2\. 启动音频播放

TTS 场景不采集麦克风，只需初始化本地播放器。客户可以选择默认使用扬声器或听筒；服务端 Audio 轨音频由 SDK 自动播放。

```
AoqClientEngine.AoqAudioPlaybackConfig playbackConfig =
        new AoqClientEngine.AoqAudioPlaybackConfig();
playbackConfig.channel = 1;
playbackConfig.isDefaultSpeaker = true;
engine.startAudioPlayer(playbackConfig);
```

### 3\. 配置解码器、轨道并建立连接

按 run-task 中选择的输出音频格式配置 SDK 解码参数，然后发布 Data 轨、订阅 Audio 和 Data 轨。以下数值仅为本教程的 PCM 示例配置。AoqConnectConfig 的连接字段由客户根据 AppServer Token 响应填写。

```
AoqClientEngine.AoqAudioCodecConfig audioDecoderConfig =
        new AoqClientEngine.AoqAudioCodecConfig();
audioDecoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
audioDecoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
audioDecoderConfig.sampleRate = 24000; // 示例值，应与 run-task.sample_rate 一致。
audioDecoderConfig.channel = 1;
engine.setAudioDecoderConfig(audioDecoderConfig);

AoqClientEngine.AoqTrackParam publishDataTrack = new AoqClientEngine.AoqTrackParam();
publishDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.publishTracks.add(publishDataTrack);

AoqClientEngine.AoqTrackParam subscribeAudioTrack = new AoqClientEngine.AoqTrackParam();
subscribeAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
connectConfig.subscribeTracks.add(subscribeAudioTrack);

AoqClientEngine.AoqTrackParam subscribeDataTrack = new AoqClientEngine.AoqTrackParam();
subscribeDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
connectConfig.subscribeTracks.add(subscribeDataTrack);
engine.connect(connectConfig);
```

### 4\. 调用 sendDataMsg 发送 run-task 事件

连接成功后为本轮生成新的 UUID task\_id，并配置模型、音色、文本类型、音频格式和采样率。其他可选参数请参见[客户端事件](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)。

```
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
        .put("model", "qwen-audio-3.0-tts-flash")
        .put("input", new JSONObject())
        .put("parameters", parameters);
JSONObject runTask = new JSONObject().put("header", header).put("payload", payload);
AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
dataMessage.data = runTask.toString().getBytes(StandardCharsets.UTF_8);
engine.sendDataMsg(dataMessage);
```

### 5\. 调用 sendDataMsg 发送 continue-task 事件

只能在收到 task-started 后发送 continue-task。同一任务可连续发送多个片段；单次最多 20,000 个字符，累计最多 200,000 个字符。客户应及时发送后续片段或结束任务，不要依赖固定的连接超时秒数。

```
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

### 6\. 处理服务端事件

在 onDataMsg 中读取 header.event，维护任务状态并处理失败。result-generated 只表示句子已合成，音频仍通过 Audio 轨返回。完整字段请参见[服务端事件](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)。

```
JSONObject header = event.optJSONObject("header");
if (header == null) return;
String name = header.optString("event");
if ("task-started".equals(name)) {
    // 可以发送一个或多个 continue-task 事件。
} else if ("result-generated".equals(name)) {
    // 一个语句已合成，音频通过 Audio 轨返回。
} else if ("task-finished".equals(name)) {
    taskActive = false;
} else if ("task-failed".equals(name)) {
    taskActive = false;
    String message = header.optString("error_message");
    // 展示或记录错误。
}
```

### 7\. 调用 sendDataMsg 发送 finish-task 事件

发送完全部文本后立即发送 finish-task，以合成服务端缓存的不完整语句，并等待 task-finished。详细规则请参见[客户端事件](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)。

```
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

### 8\. 断开连接并销毁引擎

不要在发送 finish-task 后立即断开。收到 task-finished 或 task-failed 后，如不再发起下一轮任务，再断开连接并销毁引擎。SDK 会自动关闭音频播放器。

```
engine.disconnect();
AoqClientEngine.destroy();
```

## 主要服务端事件

**事件**

**说明**

task-started

任务已启动，可以发送 continue-task

result-generated

一个完整语句已合成，对应音频通过 Audio 轨返回

task-finished

所有缓存文本已处理，任务结束

task-failed

任务失败，应读取错误码和错误消息

## 完整示例

以下类接收由 AppServer Token 响应转换完成的 AoqConnectConfig。连接成功后调用 synthesize(text, voice)；生产代码还需补充权限、UI 状态和重连逻辑。

```
import android.content.Context;

import com.alibaba.aoq.clientsdk.AoqClientEngine;
import com.alibaba.aoq.clientsdk.AoqClientListener;

import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.StandardCharsets;
import java.util.UUID;

public final class TtsClient {
    private AoqClientEngine engine;
    private String taskId;
    private String pendingText;
    private String pendingVoice;
    private boolean connected;
    private boolean taskActive;

    public TtsClient(Context context, AoqClientEngine.AoqConnectConfig connectConfig) {
        AoqClientListener listener = new AoqClientListener() {
            @Override
            public void onConnectionStatusChange(AoqClientEngine.AoqConnectionStatus status) {
                if (status == AoqClientEngine.AoqConnectionStatus.AoqConnectionStatusConnected) {
                    connected = true;
                } else if (status == AoqClientEngine.AoqConnectionStatus
                        .AoqConnectionStatusDisconnected) {
                    connected = false;
                }
            }

            @Override
            public void onDataMsg(AoqClientEngine.AoqDataMsg msg) {
                try {
                    JSONObject event = new JSONObject(
                            new String(msg.data, StandardCharsets.UTF_8));
                    String eventName = event.optJSONObject("header") == null
                            ? "" : event.optJSONObject("header").optString("event");
                    if ("task-started".equals(eventName)) {
                        sendContinueTask();
                        sendFinishTask();
                    } else if ("task-finished".equals(eventName)
                            || "task-failed".equals(eventName)) {
                        taskActive = false;
                    }
                } catch (JSONException e) {
                    throw new IllegalArgumentException("Invalid server event", e);
                }
            }
        };

        AoqClientEngine.AoqCreateConfig createConfig = new AoqClientEngine.AoqCreateConfig();
        createConfig.workDir = context.getFilesDir().getAbsolutePath();
        engine = AoqClientEngine.createEngine(context, createConfig, listener);

        // 示例参数，应与 run-task 中的输出音频格式一致。
        AoqClientEngine.AoqAudioCodecConfig audioDecoderConfig =
                new AoqClientEngine.AoqAudioCodecConfig();
        audioDecoderConfig.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        audioDecoderConfig.codecType = AoqClientEngine.AoqEncoderType.AoqEncoderTypeAudioPCM;
        audioDecoderConfig.sampleRate = 24000;
        audioDecoderConfig.channel = 1;
        engine.setAudioDecoderConfig(audioDecoderConfig);

        AoqClientEngine.AoqAudioPlaybackConfig playbackConfig =
                new AoqClientEngine.AoqAudioPlaybackConfig();
        playbackConfig.channel = 1;
        playbackConfig.isDefaultSpeaker = true;
        engine.startAudioPlayer(playbackConfig);

        AoqClientEngine.AoqTrackParam publishDataTrack =
                new AoqClientEngine.AoqTrackParam();
        publishDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
        connectConfig.publishTracks.add(publishDataTrack);

        AoqClientEngine.AoqTrackParam subscribeAudioTrack =
                new AoqClientEngine.AoqTrackParam();
        subscribeAudioTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeAudio;
        connectConfig.subscribeTracks.add(subscribeAudioTrack);

        AoqClientEngine.AoqTrackParam subscribeDataTrack =
                new AoqClientEngine.AoqTrackParam();
        subscribeDataTrack.trackType = AoqClientEngine.AoqTrackType.AoqTrackTypeData;
        connectConfig.subscribeTracks.add(subscribeDataTrack);

        engine.connect(connectConfig);
    }

    public void synthesize(String text, String voice) {
        if (!connected || taskActive) {
            throw new IllegalStateException("The connection is not ready or a task is active.");
        }
        taskId = UUID.randomUUID().toString();
        pendingText = text;
        pendingVoice = voice;
        taskActive = true;
        sendRunTask();
    }

    private void sendRunTask() {
        try {
            JSONObject header = new JSONObject()
                    .put("action", "run-task")
                    .put("task_id", taskId)
                    .put("streaming", "duplex");
            JSONObject parameters = new JSONObject()
                    .put("text_type", "PlainText")
                    .put("voice", pendingVoice)
                    .put("format", "pcm")
                    .put("sample_rate", 24000);
            JSONObject payload = new JSONObject()
                    .put("task_group", "audio")
                    .put("task", "tts")
                    .put("function", "SpeechSynthesizer")
                    .put("model", "qwen-audio-3.0-tts-flash")
                    .put("input", new JSONObject())
                    .put("parameters", parameters);
            JSONObject runTask = new JSONObject().put("header", header).put("payload", payload);
            AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
            dataMessage.data = runTask.toString().getBytes(StandardCharsets.UTF_8);
            engine.sendDataMsg(dataMessage);
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create run-task", e);
        }
    }

    private void sendContinueTask() {
        try {
            JSONObject header = new JSONObject()
                    .put("action", "continue-task")
                    .put("task_id", taskId)
                    .put("streaming", "duplex");
            JSONObject payload = new JSONObject()
                    .put("input", new JSONObject().put("text", pendingText));
            JSONObject continueTask = new JSONObject()
                    .put("header", header)
                    .put("payload", payload);
            AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
            dataMessage.data = continueTask.toString().getBytes(StandardCharsets.UTF_8);
            engine.sendDataMsg(dataMessage);
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create continue-task", e);
        }
    }

    private void sendFinishTask() {
        try {
            JSONObject header = new JSONObject()
                    .put("action", "finish-task")
                    .put("task_id", taskId)
                    .put("streaming", "duplex");
            JSONObject finishTask = new JSONObject()
                    .put("header", header)
                    .put("payload", new JSONObject().put("input", new JSONObject()));
            AoqClientEngine.AoqDataMsg dataMessage = new AoqClientEngine.AoqDataMsg();
            dataMessage.data = finishTask.toString().getBytes(StandardCharsets.UTF_8);
            engine.sendDataMsg(dataMessage);
        } catch (JSONException e) {
            throw new IllegalStateException("Failed to create finish-task", e);
        }
    }

    public void close() {
        engine.disconnect();
        AoqClientEngine.destroy();
    }
}
```

## 运行并验证

1.  收到 task-started 后才提交文本。
2.  完整语句的音频通过 Audio 轨连续播放；不完整语句在 finish-task 后补充合成。
3.  所有音频完成后收到 task-finished；随后可以使用新的 task\_id 开始下一轮。

## 典型场景

### 同一连接多次合成

收到 task-finished 后，可在同一 AOQ 连接上使用新的 task\_id 再次发送 run-task，无需重新申请 Token；如果连接已断开，则必须获取新的连接凭证。

### 切换音色

每个 run-task 都可以通过 parameters.voice 选择系统音色或有效的 voice\_id，因此可在同一连接的不同任务间切换音色。

### 扬声器或听筒

通过 AoqAudioPlaybackConfig.isDefaultSpeaker 设置默认输出设备；运行中可调用 enableSpeakerphone 切换。

## 常见问题

**问题**

**处理方法**

连接成功但任务不启动

确认通过 Inference Token 地址获取凭证，并检查 run-task 的模型名、task\_id 和 Data 轨发布配置。

continue-task 被拒绝

等待 task-started 后再发送，并确保 run-task、continue-task、finish-task 使用同一个 task\_id。

任务成功但没有声音

确认已订阅 Audio 轨并启动播放器，同时检查 SDK 解码配置是否与 run-task 中选择的输出音频格式一致。

末尾文本没有音频

所有文本发送完毕后必须发送 finish-task，并等待剩余音频和 task-finished 后再断开。

## 相关文档

如需查看完整参数、事件字段或其他平台接口，请参见：

-   [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   [选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)
-   [AOQ Client SDK 简介](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
-   [SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
-   [Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
-   [Qwen-Audio-TTS 用户指南](raw/model-user-guide/model-experience/tts-model.md)
-   [客户端事件](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-client-events.md)
-   [服务端事件](raw/model-api-reference/audio-api-references/speech-synthesis-api-reference/cosyvoice-large-model-for-speech-synthesis/cosyvoice-server-events.md)
