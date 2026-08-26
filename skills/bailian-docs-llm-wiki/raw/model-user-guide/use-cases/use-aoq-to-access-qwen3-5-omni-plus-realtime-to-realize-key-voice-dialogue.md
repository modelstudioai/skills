# 使用 AOQ 接入 qwen3.5-omni-plus-realtime 实现按键语音对话

通过 AOQ 接入 qwen3.5-omni-plus-realtime，由客户端控制语音起止，实现按键通话和可选的拍照提问。客户端代码以 iOS Swift 为例。

## 方案概述

Qwen-Omni-Realtime 支持由服务端 VAD 自动划分轮次，也支持由客户端控制轮次的 Manual 模式。本教程将 session.turn\_detection 设为 null：用户按下按钮时发送音频，松开按钮时提交音频并显式触发模型回复。

Manual 模式适用于硬件按键对讲、屏幕按住说话、噪声环境下由业务自行判停，以及在一轮语音中按需附带图片等场景。音频通过 AOQ Audio 轨传输，不需要发送 input\_audio\_buffer.append。

**对比项**

**VAD 模式**

**Manual 模式**

语音起止

服务端通过 server\_vad 或 semantic\_vad 检测

客户端根据按键或业务状态控制

会话配置

turn\_detection 为 VAD 参数

turn\_detection 为 null

提交音频

服务端自动提交

客户端发送 input\_audio\_buffer.commit

触发回复

服务端自动触发

客户端发送 response.create

图片输入

视频轨持续推流或 Data 轨按需发图

视频轨持续推流或 Data 轨按需发图

## 准备工作

1.  开通阿里云百炼，并按[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)。API Key 只保存在业务 AppServer，不要写入客户端代码或提交到代码仓库。
2.  根据业务部署地域确认 AOQ Endpoint。地域和接入地址的选择方法请参见[选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。
3.  从[SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)获取最新版 AOQ Client SDK。
4.  搭建业务 AppServer，并按[Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)实现服务端代理鉴权。每次建立新连接前，客户端都应从 AppServer 获取新的连接凭证。

### 导入 SDK

根据开发平台导入对应 SDK。后续客户端代码以 iOS Swift 为例，其他平台使用相同的接口设计和事件流程。本文以 PCM 音频流为例。Opus 编码由插件提供；如果需要使用 Opus 编码上行，请导入 Opus 插件。

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
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.CAMERA" />
```

3.  在使用相应设备前动态申请 RECORD\_AUDIO、CAMERA 权限。

#### iOS

1.  将 AoqClientSdk.framework 拖入 Xcode 工程，在 Target > General > Frameworks, Libraries, and Embedded Content 中选择 Embed & Sign。SDK 支持 iOS 13.0 及以上 arm64 设备。
2.  在 Info.plist 中添加 NSMicrophoneUsageDescription、NSCameraUsageDescription，并在使用相应设备前请求用户授权。
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
  { "name": "ohos.permission.INTERNET" },
  { "name": "ohos.permission.MICROPHONE",
    "reason": "$string:perm_mic_reason",
    "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } },
  { "name": "ohos.permission.CAMERA",
    "reason": "$string:perm_camera_reason",
    "usedScene": { "abilities": ["EntryAbility"], "when": "inuse" } }
]
```

3.  在使用相应设备前调用 abilityAccessCtrl.createAtManager().requestPermissionsFromUser 申请 ohos.permission.MICROPHONE、ohos.permission.CAMERA。

#### Linux (Python)

1.  解压 SDK，并保持 aoq\_client\_sdk.py、libAoqClientSdk.so 和 libonnxruntime.so.1.16.3 位于同一目录。
2.  将 SDK 目录加入 Python 和动态库搜索路径：

```
export PYTHONPATH="$PWD/AoqClientSdk:$PYTHONPATH"
export LD_LIBRARY_PATH="$PWD/AoqClientSdk:$LD_LIBRARY_PATH"
```

3.  在 Python 代码中使用 import aoq\_client\_sdk。也可通过 AOQ\_CLIENT\_SDK\_LIB 指定 libAoqClientSdk.so 的绝对路径。

## 实现流程

1.  AppServer 通过 Realtime Token 地址获取 qwen3.5-omni-plus-realtime 的 AOQ 连接参数。
2.  客户端创建引擎，配置音频编解码与轨道；如需持续视觉理解，再配置 Video 轨。
3.  客户端启动本地采集和播放，默认关闭 Audio 轨发送，然后建立 AOQ 连接并发送 session.update。
4.  收到 session.updated 后，持续视频方案开启 Video 轨；Audio 轨仍保持关闭，直到用户按下说话按钮。
5.  用户按下按钮时开启 Audio 轨；松开时先关闭 Audio 轨，再按需发送图片，然后依次发送 input\_audio\_buffer.commit 和 response.create。
6.  收到 response.done 后可开始下一轮；结束使用时停止设备、断开连接并销毁引擎。

#### 视频轨持续推流

发布 Video 轨并在 session.updated 后开启视频发送。模型持续看到最新画面；每轮语音只需提交音频并触发回复。

![AOQ Manual 模式视频轨持续推流时序图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6518966871/p1094863.png)

#### Data 轨按需发图

不发布 Video 轨。需要配图时，在松开按钮后先发送 input\_image\_buffer.append，再提交本轮音频并触发回复。

![AOQ Manual 模式 Data 轨按需发图时序图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6518966871/p1094864.png)

## AppServer 获取 Token

在 AppServer 设置 DASHSCOPE\_API\_KEY，并使用所选地域的 Endpoint 发送请求。clientIp 为客户端的真实公网 IP；该字段可选，但建议传入，以便服务分配合适的 Relay 接入点。

```
curl -X POST \
  "https://{endpoint}/api/v1/webrtc/realtime?model=qwen3.5-omni-plus-realtime" \
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

## 实现 iOS 客户端

客户端从 AppServer 获取 AoqConnectConfig 后，按以下步骤实现 iOS 端按键语音对话。

### 1\. 创建引擎并设置回调

创建 AOQ 单例引擎，并把业务对象注册为回调接收方。客户需要在回调中处理连接状态、服务端事件、错误和告警。

```
let createConfig = AoqCreateConfig()
createConfig.workDir = workDir
engine = AoqClientEngine.createEngine(createConfig, delegate: self)
```

### 2\. 启动音视频设备

初始化音频采集与播放。只有持续视频轨方案需要启动摄像头；客户需要在调用前获得麦克风和摄像头权限。

```
let captureConfig = AoqAudioCaptureConfig()
captureConfig.channel = 1
captureConfig.isExternal = false
engine.startAudioCapture(captureConfig)

let playbackConfig = AoqAudioPlaybackConfig()
playbackConfig.channel = 1
playbackConfig.isExternal = false
playbackConfig.isDefaultSpeaker = true
engine.startAudioPlayer(playbackConfig)
```

### 3\. 配置编解码和轨道

根据接入模型和业务音频格式配置音频编解码参数，并根据图片输入方式选择轨道。以下音频与视频数值仅为示例，请按模型要求和业务场景调整。连接前必须关闭 Audio 轨发送。

#### 视频轨持续推流

客户需要配置 Audio、Video 和 Data 发布轨，并根据实际画质与带宽调整视频编码参数。

```
let audioEncoderConfig = AoqAudioCodecConfig()
audioEncoderConfig.trackType = .audio
audioEncoderConfig.codecType = .audioPCM
audioEncoderConfig.sampleRate = 16_000
audioEncoderConfig.channel = 1
engine.setAudioEncoderConfig(audioEncoderConfig)

let audioDecoderConfig = AoqAudioCodecConfig()
audioDecoderConfig.trackType = .audio
audioDecoderConfig.codecType = .audioPCM
audioDecoderConfig.sampleRate = 24_000
audioDecoderConfig.channel = 1
engine.setAudioDecoderConfig(audioDecoderConfig)

let videoEncoderConfig = AoqVideoCodecConfig()
videoEncoderConfig.trackType = .video
videoEncoderConfig.codecType = .videoJpeg
videoEncoderConfig.width = 960
videoEncoderConfig.height = 540
videoEncoderConfig.fps = 2
videoEncoderConfig.bitrate = 500_000
engine.setVideoEncoderConfig(videoEncoderConfig)

let publishAudioTrack = AoqTrackParam()
publishAudioTrack.trackType = .audio
let publishVideoTrack = AoqTrackParam()
publishVideoTrack.trackType = .video
let publishDataTrack = AoqTrackParam()
publishDataTrack.trackType = .data
let subscribeAudioTrack = AoqTrackParam()
subscribeAudioTrack.trackType = .audio
let subscribeDataTrack = AoqTrackParam()
subscribeDataTrack.trackType = .data
connectConfig.publishTracks = [publishAudioTrack, publishVideoTrack, publishDataTrack]
connectConfig.subscribeTracks = [subscribeAudioTrack, subscribeDataTrack]
```

#### Data 轨按需发图

客户仅配置 Audio 和 Data 轨，不配置视频编码器，从而避免持续采集、编码和传输视频。音频数值仅为示例。

```
let audioEncoderConfig = AoqAudioCodecConfig()
audioEncoderConfig.trackType = .audio
audioEncoderConfig.codecType = .audioPCM
audioEncoderConfig.sampleRate = 16_000
audioEncoderConfig.channel = 1
engine.setAudioEncoderConfig(audioEncoderConfig)

let audioDecoderConfig = AoqAudioCodecConfig()
audioDecoderConfig.trackType = .audio
audioDecoderConfig.codecType = .audioPCM
audioDecoderConfig.sampleRate = 24_000
audioDecoderConfig.channel = 1
engine.setAudioDecoderConfig(audioDecoderConfig)

let publishAudioTrack = AoqTrackParam()
publishAudioTrack.trackType = .audio
let publishDataTrack = AoqTrackParam()
publishDataTrack.trackType = .data
let subscribeAudioTrack = AoqTrackParam()
subscribeAudioTrack.trackType = .audio
let subscribeDataTrack = AoqTrackParam()
subscribeDataTrack.trackType = .data
connectConfig.publishTracks = [publishAudioTrack, publishDataTrack]
connectConfig.subscribeTracks = [subscribeAudioTrack, subscribeDataTrack]
```

### 4\. 配置 Manual 会话

连接成功后，调用 sendDataMsg 发送 session.update 事件。客户需要把 turn\_detection 设为 null，并按业务选择音色、系统指令和输出模态。示例中的音频参数需要与 SDK 编解码配置保持一致。完整字段请参见[客户端事件](raw/model-api-reference/omni-realtime-api/client-events.md)。

```
private func sendSessionUpdate() {
    let event: [String: Any] = [
        "type": "session.update",
        "session": [
            "modalities": ["text", "audio"],
            "voice": "Ethan",
            "audio": [
                "input": ["format": ["type": "pcm", "sample_rate": 16_000]],
                "output": ["format": ["type": "pcm", "sample_rate": 24_000]]
            ],
            "turn_detection": NSNull()
        ]
    ]
    guard let data = try? JSONSerialization.data(withJSONObject: event) else { return }
    let dataMessage = AoqDataMsg()
    dataMessage.data = data
    engine.sendDataMsg(dataMessage)
}
```

### 5\. 等待会话配置生效

在 onDataMsg 回调中处理 session.updated 事件，收到该事件后才能发送媒体。持续视频轨方案此时调用 enableSendMediaStream 开启 Video 轨；Audio 轨仍保持关闭，避免用户按键前的音频进入缓冲区。

```
func onDataMsg(_ msg: AoqDataMsg) {
    guard let event = try? JSONSerialization.jsonObject(with: msg.data) as? [String: Any],
          let type = event["type"] as? String else { return }
    if type == "session.updated", imageMode == .continuousVideo {
        engine.enableSendMediaStream(.video, enable: true)
    }
    // 按下通话按钮前保持 Audio 轨关闭。
}
```

### 6\. 实现按键语音交互

按下按钮时调用 enableSendMediaStream 开启 Audio 轨。松开按钮时先调用 enableSendMediaStream 关闭 Audio 轨，确认本轮确有音频，再按需发送图片，并调用 sendDataMsg 依次发送 input\_audio\_buffer.commit 和 response.create 事件。

```
func onPushToTalkPressed() {
    hasAudioInCurrentTurn = true
    engine.enableSendMediaStream(.audio, enable: true)
}

func onPushToTalkReleased(base64Jpeg: String? = nil) {
    engine.enableSendMediaStream(.audio, enable: false)
    guard hasAudioInCurrentTurn else { return }
    if imageMode == .singleImage, let base64Jpeg {
        let imageEvent: [String: Any] = [
            "type": "input_image_buffer.append",
            "image": base64Jpeg
        ]
        if let data = try? JSONSerialization.data(withJSONObject: imageEvent) {
            let dataMessage = AoqDataMsg()
            dataMessage.data = data
            engine.sendDataMsg(dataMessage)
        }
    }
    for event in [
        ["type": "input_audio_buffer.commit"],
        ["type": "response.create"]
    ] {
        guard let data = try? JSONSerialization.data(withJSONObject: event) else { continue }
        let dataMessage = AoqDataMsg()
        dataMessage.data = data
        engine.sendDataMsg(dataMessage)
    }
    hasAudioInCurrentTurn = false
}
```

### 7\. 选择图片输入方式

持续视觉理解和偶发拍照提问使用不同的轨道配置与发送方式；客户需要根据带宽、功耗和交互方式选择。

#### 视频轨持续推流

适合视频通话、画面变化较快或模型需要持续理解视觉上下文的场景。发布 Video 轨后，不要再发送 input\_image\_buffer.append。

#### Data 轨按需发送单张图片

适合拍照提问或偶发配图。客户需要把图片处理为 JPG/JPEG 并进行 Base64 编码，在松开按键后、提交音频前发送：

```
{
  "type": "input_image_buffer.append",
  "image": "<Base64-encoded JPEG data>"
}
```

-   建议分辨率为 480p 或 720p，最高不超过 1080p。
-   Base64 编码后不得超过 256 KB，建议编码前不超过 190 KB，并为 JSON 包装字段预留空间。
-   发送图片前，Audio 轨必须已经在本轮至少上行过一帧音频；随后的 input\_audio\_buffer.commit 会同时提交音频和图片。

### 8\. 断开连接并销毁引擎

结束会话时断开连接并销毁引擎。disconnect 或 destroy 会自动关闭媒体设备，无需额外调用停止接口。AoqClientEngine 为全局单例，只有 destroy 后才能重新创建。

```
engine.disconnect()
AoqClientEngine.destroy()
```

## 完整示例

以下类接收已由 AppServer Token 响应转换完成的 AoqConnectConfig。请在生产代码中补充 UI 状态、权限、错误恢复和图片压缩逻辑。

```
import Foundation
import AoqClientSdk

final class ManualPushToTalkClient: NSObject, AoqEngineDelegate {
    enum ImageMode: Equatable {
        case none
        case continuousVideo
        case singleImage
    }

    private var engine: AoqClientEngine!
    private let imageMode: ImageMode
    private var hasAudioInCurrentTurn = false

    init(workDir: String, connectConfig: AoqConnectConfig, imageMode: ImageMode) {
        self.imageMode = imageMode
        super.init()
        let createConfig = AoqCreateConfig()
        createConfig.workDir = workDir
        self.engine = AoqClientEngine.createEngine(createConfig, delegate: self)

        // 示例参数，请按接入模型和业务音频格式调整。
        let audioEncoderConfig = AoqAudioCodecConfig()
        audioEncoderConfig.trackType = .audio
        audioEncoderConfig.codecType = .audioPCM
        audioEncoderConfig.sampleRate = 16_000
        audioEncoderConfig.channel = 1
        engine.setAudioEncoderConfig(audioEncoderConfig)

        let audioDecoderConfig = AoqAudioCodecConfig()
        audioDecoderConfig.trackType = .audio
        audioDecoderConfig.codecType = .audioPCM
        audioDecoderConfig.sampleRate = 24_000
        audioDecoderConfig.channel = 1
        engine.setAudioDecoderConfig(audioDecoderConfig)

        let publishAudioTrack = AoqTrackParam()
        publishAudioTrack.trackType = .audio
        let publishDataTrack = AoqTrackParam()
        publishDataTrack.trackType = .data
        let subscribeAudioTrack = AoqTrackParam()
        subscribeAudioTrack.trackType = .audio
        let subscribeDataTrack = AoqTrackParam()
        subscribeDataTrack.trackType = .data

        connectConfig.publishTracks = [publishAudioTrack, publishDataTrack]
        connectConfig.subscribeTracks = [subscribeAudioTrack, subscribeDataTrack]

        if imageMode == .continuousVideo {
            let videoEncoderConfig = AoqVideoCodecConfig()
            videoEncoderConfig.trackType = .video
            videoEncoderConfig.codecType = .videoJpeg
            videoEncoderConfig.width = 960
            videoEncoderConfig.height = 540
            videoEncoderConfig.fps = 2
            videoEncoderConfig.bitrate = 500_000
            engine.setVideoEncoderConfig(videoEncoderConfig)

            let publishVideoTrack = AoqTrackParam()
            publishVideoTrack.trackType = .video
            connectConfig.publishTracks = [publishAudioTrack, publishVideoTrack, publishDataTrack]
        }

        let captureConfig = AoqAudioCaptureConfig()
        captureConfig.channel = 1
        captureConfig.isExternal = false
        engine.startAudioCapture(captureConfig)

        let playbackConfig = AoqAudioPlaybackConfig()
        playbackConfig.channel = 1
        playbackConfig.isExternal = false
        playbackConfig.isDefaultSpeaker = true
        engine.startAudioPlayer(playbackConfig)

        if imageMode == .continuousVideo {
            let videoCaptureConfig = AoqVideoCaptureConfig()
            videoCaptureConfig.width = 1280
            videoCaptureConfig.height = 720
            videoCaptureConfig.fps = 15
            engine.startVideoCapture(videoCaptureConfig)
        }

        engine.enableSendMediaStream(.audio, enable: false)
        if imageMode == .continuousVideo {
            engine.enableSendMediaStream(.video, enable: false)
        }
        engine.connect(connectConfig)
    }

    func onPushToTalkPressed() {
        hasAudioInCurrentTurn = true
        engine.enableSendMediaStream(.audio, enable: true)
    }

    func onPushToTalkReleased(base64Jpeg: String? = nil) {
        engine.enableSendMediaStream(.audio, enable: false)
        guard hasAudioInCurrentTurn else { return }
        if imageMode == .singleImage, let base64Jpeg {
            let imageEvent: [String: Any] = [
                "type": "input_image_buffer.append",
                "image": base64Jpeg
            ]
            if let data = try? JSONSerialization.data(withJSONObject: imageEvent) {
                let dataMessage = AoqDataMsg()
                dataMessage.data = data
                engine.sendDataMsg(dataMessage)
            }
        }
        for event in [
            ["type": "input_audio_buffer.commit"],
            ["type": "response.create"]
        ] {
            guard let data = try? JSONSerialization.data(withJSONObject: event) else { continue }
            let dataMessage = AoqDataMsg()
            dataMessage.data = data
            engine.sendDataMsg(dataMessage)
        }
        hasAudioInCurrentTurn = false
    }

    private func sendSessionUpdate() {
        let event: [String: Any] = [
            "type": "session.update",
            "session": [
                "modalities": ["text", "audio"],
                "voice": "Ethan",
                "audio": [
                    "input": ["format": ["type": "pcm", "sample_rate": 16_000]],
                    "output": ["format": ["type": "pcm", "sample_rate": 24_000]]
                ],
                "turn_detection": NSNull()
            ]
        ]
        guard let data = try? JSONSerialization.data(withJSONObject: event) else { return }
        let dataMessage = AoqDataMsg()
        dataMessage.data = data
        engine.sendDataMsg(dataMessage)
    }

    func close() {
        engine.disconnect()
        AoqClientEngine.destroy()
    }

    func onConnectionStatusChange(_ status: AoqConnectionStatus) {
        if status == .connected { sendSessionUpdate() }
    }

    func onDataMsg(_ msg: AoqDataMsg) {
        guard let event = try? JSONSerialization.jsonObject(with: msg.data) as? [String: Any],
              let type = event["type"] as? String else { return }
        if type == "session.updated", imageMode == .continuousVideo {
            engine.enableSendMediaStream(.video, enable: true)
        }
    }

    func onError(_ code: Int, message: String) {}
    func onWarning(_ code: Int, message: String) {}
    func onStats(_ stats: AoqStats) {}
    func onAudioDeviceStateChanged(_ state: AoqAudioDeviceState) {}
    func onAudioDeviceRouteChanged(_ routeType: Int) {}
    func onAudioDeviceInterrupted(_ interrupt: Bool) {}
    func onAudioFileState(_ state: AoqAudioFileState) {}
    func onVideoDeviceStateChanged(_ state: AoqVideoDeviceState) {}
}
```

## 运行并验证

分别完成一次纯语音按键对话和一次带图片的按键对话，预期结果如下：

1.  按下按钮前不发送 Audio 轨；按住按钮时持续上行音频。
2.  松开按钮后依次收到 input\_audio\_buffer.committed、response.created 和 response.done，模型语音通过订阅的 Audio 轨播放。
3.  选择单张图片方案时，模型结合本轮图片与语音作答；选择持续视频方案时，模型使用最新视频画面。

服务端事件字段和完整响应结构请参见[服务端事件](raw/model-api-reference/omni-realtime-api/server-events.md)。

## 注意事项

1.  AOQ 的 Audio 轨负责传输音频，不要另外发送 input\_audio\_buffer.append。
2.  input\_audio\_buffer.commit 只提交本轮输入，不会触发模型回复；必须随后发送 response.create。
3.  空音频缓冲区不要提交，否则服务端会返回错误。
4.  不要在收到 session.updated 前开启媒体发送；Manual 模式下也不要在用户按下按钮前开启 Audio 轨。

## 相关文档

如需查看完整参数、事件字段或其他平台接口，请参见：

-   [获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)
-   [选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)
-   [AOQ Client SDK 简介](raw/model-api-reference/realtime-api-user-guide/realtime-api-aoq-api/realtime-api-aoq-sdk-desc.md)
-   [SDK 下载](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-sdk-download.md)
-   [Token 鉴权](raw/model-api-reference/realtime-api-user-guide/realtime-api-quick-start-guide/realtime-token-authentication.md)
-   [Qwen-Omni-Realtime 用户指南](https://help.aliyun.com/zh/model-studio/realtime)
-   [通过 AOQ 实现 VAD 模式实时通话](raw/model-user-guide/use-cases/best-practice-aoq-omni-realtime.md)
-   [客户端事件](raw/model-api-reference/omni-realtime-api/client-events.md)
-   [服务端事件](raw/model-api-reference/omni-realtime-api/server-events.md)
