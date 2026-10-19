# 使用 AOQ 接入 qwen3.8-livetranslate-flash-realtime 实现实时语音翻译

本文以 Android 平台为例，介绍如何接入 AOQ Client SDK，使用 qwen3.8-livetranslate-flash-realtime 实现语音的实时翻译。其他平台的接入流程和模型事件处理方式类似，使用对应平台的 SDK 接口即可；下文客户端代码统一使用 Java。

**说明**模型能力详情请参考[实时语音/音视频翻译模型说明](raw/model-user-guide/model-experience/speech-to-speech/qwen3-5-livetranslate-flash-realtime.md)，媒体与模型事件的分工请参考 [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)。

## SDK 获取

AOQ Client SDK 及音频 Opus 插件请参见 [SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)。本文的音频传输示例使用 Opus，需要同时导入对应平台的插件。模型支持的地域、语种、计费和限流以[实时语音/音视频翻译模型说明](raw/model-user-guide/model-experience/speech-to-speech/qwen3-5-livetranslate-flash-realtime.md)为准。

## SDK 导入

#### Android

将 `AoqClientSdk-release.aar` 放入工程 `app/libs/`，将 `libPluginOpus.so` 按 ABI 放入 `app/libs/armeabi-v7a/` 和 `app/libs/arm64-v8a/`。

在 `app/build.gradle` 中声明依赖：

```
android {
    defaultConfig {
        minSdk 21
        ndk { abiFilters 'armeabi-v7a', 'arm64-v8a' }
    }
    sourceSets { main { jniLibs.srcDirs = ['libs'] } }
}

dependencies {
    implementation fileTree(dir: 'libs', include: ['*.aar'])
}
```

如果宿主工程已包含同名原生库，应先确认版本与依赖关系，避免重复打包不同版本的库。

在 `AndroidManifest.xml` 中声明权限：

```
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
```

`RECORD_AUDIO` 还需要在运行时申请并取得用户授权。纯语音翻译不需要摄像头权限；启用视觉增强时，再声明和申请 `CAMERA`。

本文 Java 示例使用以下导入：

```
import com.alibaba.aoq.clientsdk.AoqClientEngine;
import com.alibaba.aoq.clientsdk.AoqClientEngine.*;
import com.alibaba.aoq.clientsdk.AoqClientListener;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import org.json.JSONException;
import org.json.JSONObject;
```

#### iOS

将 `AoqClientSdk.framework` 和 `PluginOpus.framework` 拖入 Xcode 工程，在 **Target > General > Frameworks, Libraries, and Embedded Content** 中选择 **Embed & Sign**。

在 `Info.plist` 中声明麦克风用途：

**Key**

**Value 示例**

`NSMicrophoneUsageDescription`

用于采集需要实时翻译的语音

启动采集前需要取得麦克风授权。仅在启用视觉增强时添加 `NSCameraUsageDescription` 并申请摄像头权限。

业务代码通过 `AoqClientSdk` 模块访问 SDK；Swift 使用 `import AoqClientSdk`，Objective-C 使用 `#import <AoqClientSdk/AoqClientSdk.h>`。后续会话配置与事件处理流程和 Android 示例相同，SDK 调用使用对应的 iOS 接口。

#### HarmonyOS

将 `AoqClientSdk.har` 放入工程根目录的 `libs/`，在 `entry/oh-package.json5` 的 `dependencies` 中添加：

```
{
  "dependencies": {
    "@aoq/client-sdk": "file:../libs/AoqClientSdk.har"
  }
}
```

将 `libPluginOpus.so` 按 ABI 放入 `entry/libs/armeabi-v7a/` 和 `entry/libs/arm64-v8a/`。

在 `entry/src/main/module.json5` 的 `module` 对象中添加以下权限配置，并在应用字符串资源中定义 `perm_mic_reason`，例如“用于采集需要实时翻译的语音”：

```
{
  "requestPermissions": [
    { "name": "ohos.permission.INTERNET" },
    {
      "name": "ohos.permission.MICROPHONE",
      "reason": "$string:perm_mic_reason",
      "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" }
    }
  ]
}
```

保留工程原有的依赖和模块配置，将上述字段合入对应对象，不要用片段覆盖整个配置文件。若应用使用其他 Ability 名称，将 `EntryAbility` 替换为实际名称。

启动采集前，通过 `abilityAccessCtrl.createAtManager().requestPermissionsFromUser` 请求麦克风运行时授权；仅在启用视觉增强时增加摄像头权限。

## AppServer 获取 Token

客户端不直接保存百炼 API Key。由业务 AppServer 使用对应地域、业务空间的 API Key，为每次翻译连接申请临时凭证，再通过 HTTPS 返回给已经完成业务鉴权的客户端。

按照 [Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)的 AOQ 章节搭建 AppServer。实时翻译属于 Realtime 协议，申请凭证时指定：

```
model=qwen3.8-livetranslate-flash-realtime
```

以下命令仅在 AppServer 侧执行。`BAILIAN_ENDPOINT` 设置为实际业务空间对应的 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 或 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`；`DASHSCOPE_API_KEY` 从服务端环境变量或密钥管理服务读取。

```
curl --fail-with-body --request POST \
  "https://${BAILIAN_ENDPOINT}/api/v1/webrtc/realtime?model=qwen3.8-livetranslate-flash-realtime" \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --header "x-dashscope-rtc-transport: moq" \
  --data '{}'
```

如果 AppServer 能从可信代理链中取得客户端真实公网 IP，可在请求体中加入 `clientIp`，用于接入点调度。

客户端将返回值映射到 `AoqConnectConfig`：

**网关返回字段**

**SDK 字段**

**说明**

`aoqTokenForClient`

`token`

本次连接的临时令牌

`sid`

`sid`

本次会话标识

`clientRelayCertFingerprint`

`certFingerprint`

原样使用服务端返回的证书指纹

`clientRelayEndpoints`

`relayEndpoints`

按结构转换完整接入点列表

`extraInfo.workspaceIdHash`

`workspaceIdHash`

使用返回值；未返回时按 SDK 要求处理

## 实现实时语音翻译

### 整体交互流程

![AOQ 实时语音翻译交互时序](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/images/6a4b3c2d1e0f9246.png)

### 创建引擎并设置回调

调用 `createEngine` 创建引擎，注册连接、Data 消息及错误回调。业务对象需在会话期间持有引擎和监听对象。

```
// 配置引擎工作目录。
AoqCreateConfig createConfig = new AoqCreateConfig();
createConfig.workDir = appCtx.getFilesDir().getAbsolutePath();
// 创建引擎并注册事件监听对象。
engine = AoqClientEngine.createEngine(appCtx, createConfig, listener);
```

`AoqClientListener`可以获取连接、模型消息和媒体设备等事件，请实现并在创建引擎的时候传入。

```
AoqClientListener listener = new AoqClientListener() {
    // 接收音频采集与播放设备状态。
    @Override
    public void onAudioDeviceStateChanged(AoqAudioDeviceState state) {

    }

    // 接收耳机、蓝牙及扬声器等音频路由变化。
    @Override
    public void onAudioDeviceRouteChanged(int routeType) {
        android.util.Log.i("LiveTranslate", "音频路由: " + AoqAudioDeviceRouteType.fromValue(routeType));
    }

    // 接收音频设备中断及中断结束通知。
    @Override
    public void onAudioDeviceInterrupted(boolean interrupt) {
        android.util.Log.i("LiveTranslate", "音频设备中断: " + interrupt);
    }

    // 接收 Android 音频焦点变化。
    @Override
    public void onAudioDeviceFocusChanged(int audioFocus) {
        android.util.Log.i("LiveTranslate", "音频焦点: " + audioFocus);
    }

    // 接收 SDK 异步错误。
    @Override
    public void onError(int code, String message) {
        android.util.Log.e("LiveTranslate", "SDK 错误: " + code + ", " + message);
    }
};
```

### 启动音频采集与播放

在已经取得麦克风权限的前提下，准备采集和播放。**先关闭音频发送，再启动采集**，避免引擎建连后默认推流。

采集已启动不代表模型已能接收音频。页面应在收到 `session.updated` 并成功开启发送后，再提示用户开始说话；本文不实现连接前音频缓存。

```
// 关闭音频上行，等待模型配置确认。
engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeAudio, false);

AoqAudioCaptureConfig audioCaptureConfig = new AoqAudioCaptureConfig();
audioCaptureConfig.channel = 1;
audioCaptureConfig.isExternal = false;
// 启动 SDK 内置麦克风采集。
engine.startAudioCapture(audioCaptureConfig);

AoqAudioPlaybackConfig audioPlaybackConfig = new AoqAudioPlaybackConfig();
audioPlaybackConfig.channel = 1;
audioPlaybackConfig.isExternal = false;
// 启动 SDK 内置播放器，播放下行译音。
engine.startAudioPlayer(audioPlaybackConfig);
```

### 设置编解码及建立连接

主场景需要：

**方向**

**轨道**

**用途**

发布

Audio

向模型输入语音

发布

Data

发送会话配置与结束事件

订阅

Audio

接收翻译语音

订阅

Data

接收原文、译文与状态事件

音频上行和下行分别配置。以下代码以 **Opus、16 kHz、单声道传输配置**为例。

```
AoqAudioCodecConfig audioEncoderConfig = new AoqAudioCodecConfig();
audioEncoderConfig.codecType = AoqEncoderType.AoqEncoderTypeAudioOpus;
audioEncoderConfig.sampleRate = 16000;
audioEncoderConfig.channel = 1;
// 设置上行音频编码参数。
engine.setAudioEncoderConfig(audioEncoderConfig);

AoqAudioCodecConfig audioDecoderConfig = new AoqAudioCodecConfig();
audioDecoderConfig.codecType = AoqEncoderType.AoqEncoderTypeAudioOpus;
audioDecoderConfig.sampleRate = 16000;
audioDecoderConfig.channel = 1;
// 设置下行音频解码参数。
engine.setAudioDecoderConfig(audioDecoderConfig);

AoqTrackParam audioTrackParam = new AoqTrackParam();
audioTrackParam.trackType = AoqTrackType.AoqTrackTypeAudio;
AoqTrackParam dataTrackParam = new AoqTrackParam();
dataTrackParam.trackType = AoqTrackType.AoqTrackTypeData;
// 发布音频和 Data 轨，发送语音及模型事件。
connectConfig.publishTracks.add(audioTrackParam);
connectConfig.publishTracks.add(dataTrackParam);
// 订阅音频和 Data 轨，接收译音及字幕事件。
connectConfig.subscribeTracks.add(audioTrackParam);
connectConfig.subscribeTracks.add(dataTrackParam);

// 发起 AOQ 连接，连接结果通过 onConnectionStatusChange 返回。
engine.connect(connectConfig);
```

`connect` 返回成功仅表示调用被接受。等待 `onConnectionStatusChange` 通知连接成功后，再发送模型配置。

### 配置翻译会话

连接成功后，通过 Data 轨发送下面的 `session.update`。该配置使用默认音色，不开启声音复刻：

```
{
  "type": "session.update",
  "session": {
    "output_modalities": ["text", "audio"],
    "audio": {
      "input": {
        "turn_detection": {
          "type": "speaker_detection",
          "threshold": 0.5
        }
      }
    },
    "translation": {
      "language": "en"
    }
  }
}
```

交互流程请参考[实时翻译模型说明](raw/model-user-guide/model-experience/speech-to-speech/qwen3-5-livetranslate-flash-realtime.md)，`session.update` 完整参数请参考[实时翻译客户端事件](raw/_short/live-translator-client-events-666da53ef8b3942d.md)。

将上述 JSON 编码为 UTF-8 字节，通过 `sendDataMsg` 发送。

```
private static final String SESSION_UPDATE_JSON =
        "{\"type\":\"session.update\",\"session\":{"
        + "\"output_modalities\":[\"text\",\"audio\"],"
        + "\"audio\":{\"input\":{\"turn_detection\":{"
        + "\"type\":\"speaker_detection\",\"threshold\":0.5}}},"
        + "\"translation\":{\"language\":\"en\"}}}";

// 接收 AOQ 连接状态变化。
@Override
public void onConnectionStatusChange(AoqConnectionStatus status) {
    if (status == AoqConnectionStatus.AoqConnectionStatusConnected) {
        AoqDataMsg message = new AoqDataMsg();
        message.data = SESSION_UPDATE_JSON.getBytes(StandardCharsets.UTF_8);
        // 通过 Data 轨发送翻译会话配置。
        engine.sendDataMsg(message);
    }
}
```

### 收到 session.updated 后开启媒体发送

在 `onDataMsg` 中解析事件类型。

下面先展示控制事件分流；原文与译文事件的处理见[服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)。收到 `session.finished` 后设置业务完成状态，再由“断开连接与销毁引擎”中的释放方法收尾。

```
// 接收 Data 轨中的模型事件。
@Override
public void onDataMsg(AoqDataMsg message) {
    if (message == null || message.data == null) { return; }
    try {
        JSONObject event = new JSONObject(new String(message.data, StandardCharsets.UTF_8));
        String type = event.optString("type");
        if ("session.updated".equals(type)) {
            // 模型配置生效后，开启音频上行。
            engine.enableSendMediaStream(AoqTrackType.AoqTrackTypeAudio, true);
        } else if ("session.finished".equals(type)) {
            android.util.Log.i("LiveTranslate", "服务端已完成本次翻译处理");
        } else if ("error".equals(type)) {
            android.util.Log.e("LiveTranslate", "翻译模型错误: " + event.optJSONObject("error"));
        }
    } catch (JSONException error) {
        android.util.Log.e("LiveTranslate", "无法解析模型事件", error);
    }
}
```

**说明****AOQ 与 WebSocket 的区别**：本文通过 Audio 轨直接发送和接收音频。不要再发送 `input_audio_buffer.append` 重复上传同一份音频，也不要照搬 WebSocket 示例，在收到 `response.audio.delta` 后另起一个播放器重复播音。译音由 SDK 音频订阅和播放器处理；Data 轨用于字幕与模型事件。媒体与 Data 轨的使用方式请参考 [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)。

### 结束输入，等待尾句翻译

点击结束时，正常结束顺序为：

1.  停止采集，不再提交新的输入。
2.  完成输入收尾后，关闭音频上行，发送一次 `session.finish`；保持 AOQ 连接、Data 订阅和音频播放。
3.  继续接收尾句原文、译文和译音，等待 `session.finished`。
4.  按本地播放收尾策略断开连接、释放资源。

`session.finish` 的发送要求请参考[实时翻译客户端事件](raw/_short/live-translator-client-events-666da53ef8b3942d.md)，`session.finished` 的字段与含义请参考[实时翻译服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)。

```
AoqDataMsg message = new AoqDataMsg();
message.data = "{\"type\":\"session.finish\"}".getBytes(StandardCharsets.UTF_8);
// 通知模型输入结束，等待 session.finished。
engine.sendDataMsg(message);
```

### 断开连接与销毁引擎

收到 `session.finished` 后，服务端已经完成本会话处理，但**这不等于本地扬声器已经播放完最后一段音频**。如果产品要求完整播完译音，应先完成本地播放收尾，再执行以下方法。

```
// 停止译音播放。
engine.stopAudioPlayer();
// 断开 AOQ 连接。
engine.disconnect();
// 销毁本会话独占的引擎。
AoqClientEngine.destroy();
```

## 相关文档

-   [实时语音/音视频翻译](raw/model-user-guide/model-experience/speech-to-speech/qwen3-5-livetranslate-flash-realtime.md)
-   [客户端事件](raw/_short/live-translator-client-events-666da53ef8b3942d.md)
-   [服务端事件](raw/_short/live-translator-server-events-e9db9578a7b303d5.md)
-   [AOQ 接入](raw/model-api-reference/realtime-api-user-guide/realtime-model-connection/realtime-aoq-access.md)
-   [Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
-   [AOQ Client SDK 简介](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
-   [SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
-   [通过 AOQ 使用 qwen3.8-omni-flash-realtime 实现实时通话](raw/model-user-guide/use-cases/realtime-audio-video-integration/best-practice-aoq-omni-realtime.md)
