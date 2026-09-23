# AOQ Client SDK OHOS (HarmonyOS) API 参考

AOQ Client SDK HarmonyOS (OHOS) 端 API 参考，平台语言为 ArkTS (.ets)，通过 NAPI 桥接 C++ 引擎。

HarmonyOS SDK

## 目录

### 引擎生命周期

接口

简介

createEngine

创建引擎实例（静态工厂单例）

destroy

销毁引擎实例（静态方法）

getVersion

获取 SDK 版本号（静态方法）

connect

连接 Relay 服务器

disconnect

断开服务器连接

### 音频设备管理

接口

简介

startAudioCapture

打开音频采集设备（麦克风）

stopAudioCapture

关闭音频采集设备

muteAudioCapture

静音或取消静音音频采集

startAudioPlayer

开始音频渲染（播放远端音频）

stopAudioPlayer

停止音频渲染

pauseAudioPlayer

暂停音频渲染，支持淡出

resumeAudioPlayer

恢复音频渲染，支持淡入

interruptAudioPlayer

打断本轮音频通话

enableSpeakerphone

切换音频输出到扬声器或听筒

isSpeakerphoneEnabled

查询当前是否使用扬声器输出

### 音频编码配置

接口

简介

setAudioEncoderConfig

设置音频编码参数

setAudioDecoderConfig

设置音频解码参数

### 音频文件播放

接口

简介

startAudioFile

开始推流播放本地音频文件

stopAudioFile

停止音频文件播放

pauseAudioFile

暂停音频文件播放

resumeAudioFile

恢复音频文件播放

getAudioFileDuration

获取音频文件总时长

getAudioFileCurrentPosition

获取音频文件当前播放位置

setAudioFilePositionMillis

设置音频文件播放位置（seek）

setAudioFileVolume

设置音频文件音量

getAudioFileVolume

获取音频文件当前音量

### 外部音频流

接口

简介

addAudioExternalStream

新增一条外部音频流

pushAudioExternalStreamData

输入外部音频 PCM 数据

setAudioExternalStreamVolume

设置外部音频流音量

getAudioExternalStreamVolume

获取外部音频流音量

clearAudioExternalStreamBuffer

清空外部音频流缓存

removeAudioExternalStream

移除外部音频流

### 音频帧回调

接口

简介

setAudioFrameObserver

设置音频帧数据回调 observer

enableAudioFrameObserver

开启或关闭指定位置的音频帧回调

### 本地音量提示

接口

简介

enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示

### 视频设备管理

接口

简介

startVideoCapture

打开视频采集设备（摄像头）

stopVideoCapture

关闭视频采集设备

switchCamera

切换前后置摄像头

setLocalView

设置或移除本地视频渲染窗口

setRemoteView

设置或移除远端视频渲染窗口

### 视频编码与外部输入

接口

简介

setVideoEncoderConfig

设置视频编码参数

setVideoDecoderConfig

设置视频解码参数

pushExternalVideoCapturedFrame

推送外部采集视频帧

pushExternalVideoEncodedFrame

推送外部已编码视频帧

### 屏幕采集

接口

简介

startScreenCapture

启动屏幕采集

stopScreenCapture

停止屏幕采集

### 媒体流发送控制

接口

简介

enableSendMediaStream

控制本地媒体流的发送开关

### 视频帧回调

接口

简介

setVideoFrameObserver

设置视频帧数据回调 observer

enableVideoFrameObserver

开启或关闭指定位置的视频帧回调

### 实时消息

接口

简介

sendDataMsg

发送实时数据消息

### AoqEngineEventListener 回调

接口

简介

onError

引擎错误回调

onWarning

引擎警告回调

onConnectionStatusChange

连接状态变化回调

onStats

引擎统计信息回调

onAudioDeviceStateChanged

音频设备操作状态变化回调

onAudioDeviceRouteChanged

音频输出路由变化回调

onAudioDeviceInterrupted

音频设备中断回调

onVideoDeviceStateChanged

视频设备操作状态变化回调

onScreenCaptureStateChanged

屏幕采集状态变化回调

onAudioFileState

音频文件播放状态回调

onLocalAudioVolumeIndication

本地采集音量提示回调

onDataMsg

收到实时数据消息回调

### IAudioFrameObserver 回调

接口

简介

onCapturedAudioFrame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

onProcessCapturedAudioFrame

3A 处理后的音频帧回调。数据经过回声消除、噪声抑制、自动增益等 3A 处理。

onPublishAudioFrame

推流前的音频帧回调。数据即将通过编码后发送到 Relay 服务器。

onPlaybackAudioFrame

播放前的远端音频帧回调。数据为远端解码后、混音前即将播放的音频。

### IVideoFrameObserver 回调

接口

简介

onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。数据为摄像头或屏幕采集后的原始帧，未经前处理。

onPreEncodeVideoFrame

编码前的视频帧回调（前处理后）。数据经过前处理后、编码前。

onRemoteVideoFrame

远端解码后、渲染前的视频帧回调。数据为远端接收并解码后的视频帧。

## 接口详情

`pushExternalVideoCapturedFrame` 支持 Video / Screen，需先开启对应轨道的外部采集；未开启时返回 `AoqECVideoExternalCaptureNotEnabled`（211）。`pushExternalVideoEncodedFrame` 需先配置对应轨道的外部编码，未开启时返回 `AoqECVideoExternalEncoderNotEnabled`（212）。

### 引擎生命周期

#### createEngine

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。native 创建失败时返回 null。

```
static createEngine(config: AoqCreateConfig, listener: AoqEngineEventListener | null, context: common.Context): AoqClientEngine | null
```

**参数**

**类型**

**说明**

config

AoqCreateConfig

引擎创建配置

listener

AoqEngineEventListener | null

引擎事件回调监听（interface，所有回调均为可选）；可为 null

context

common.Context

UIAbility/Page 的 Context，用于 aki+ACPM 初始化

**返回值**：AoqClientEngine | null（native 创建失败时返回 null）

**说明**OHOS 端创建失败会返回 null，调用方需判空处理。context 必须是有效的 UIAbility 或 Page Context。

#### destroy

销毁引擎单例，释放所有资源。调用后需重新 createEngine 才能继续使用。

```
static destroy(): number
```

**返回值**：0 表示成功；非 0 表示失败

#### getVersion

获取 SDK 当前版本号。

```
static getVersion(): string
```

**返回值**：版本号字符串，如 "1.0.0"

#### connect

连接 Relay 服务器。连接参数由业务方 AppServer 通过 /api/v1/allocate 分配后下发给客户端。

```
connect(config: AoqConnectConfig): number
```

**参数**

**类型**

**说明**

config

AoqConnectConfig

连接配置，包含 Token、SID、Relay 接入点列表等

**返回值**：0 表示调用已下发（异步执行）；非 0 表示参数校验失败

**说明**连接状态变化通过 onConnectionStatusChange 异步通知。建议在 connect 前调用 enableSendMediaStream(false)。

#### disconnect

断开与服务器的连接，释放连接相关资源。调用后立即返回，实际断开结果通过 onConnectionStatusChange 回调通知。

```
disconnect(): number
```

参数：无。

返回值：0 表示调用已下发（异步执行）；非 0 表示失败（对应 AoqErrorCode）。

音视频采集/播放设备不会自动停止。

### 音频设备管理

#### startAudioCapture

打开音频采集设备（麦克风）。

```
startAudioCapture(config: AoqAudioCaptureConfig): number
```

**参数**

**类型**

**说明**

config

AoqAudioCaptureConfig

采集配置

**返回值**：0 表示成功；非 0 表示失败

#### stopAudioCapture

关闭音频采集设备。

```
stopAudioCapture(): number
```

#### muteAudioCapture

静音或取消静音音频采集。

```
muteAudioCapture(mute: boolean): number
```

**参数**

**类型**

**说明**

mute

boolean

true 为静音；false 为取消静音

#### startAudioPlayer

开始音频渲染（扬声器/听筒播放远端音频）。

```
startAudioPlayer(config: AoqAudioPlaybackConfig): number
```

**参数**

**类型**

**说明**

config

AoqAudioPlaybackConfig

播放配置

#### stopAudioPlayer

停止音频渲染，关闭播放设备。

```
stopAudioPlayer(): number
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pauseAudioPlayer

暂停音频渲染，可指定淡出时长实现平滑过渡。

```
pauseAudioPlayer(fadeMs: number): number
```

**参数**

**类型**

**说明**

fadeMs

number

淡出时长（毫秒）；0 表示立即停止

#### resumeAudioPlayer

恢复音频渲染，可指定淡入时长实现平滑过渡。

```
resumeAudioPlayer(fadeMs: number): number
```

**参数**

**类型**

**说明**

fadeMs

number

淡入时长（毫秒）；0 表示立即恢复

#### interruptAudioPlayer

打断本轮音频通话。

```
interruptAudioPlayer(trackType: AoqTrackType, fadeMs: number): number
```

**参数**

**类型**

**说明**

trackType

AoqTrackType

目标轨道类型，通常传 AoqTrackTypeAudio

fadeMs

number

淡出时长（毫秒）

#### enableSpeakerphone

切换音频输出路由到扬声器或听筒。

```
enableSpeakerphone(enable: boolean): number
```

**参数**

**类型**

**说明**

enable

boolean

true 使用扬声器；false 使用听筒

#### isSpeakerphoneEnabled

查询当前是否使用扬声器输出。

```
isSpeakerphoneEnabled(): boolean
```

**返回值**：true 表示当前为扬声器模式；false 表示听筒模式

### 音频编码配置

#### setAudioEncoderConfig

设置音频编码参数，用于上行推流的音频编码。配置变更会立即生效。

```
setAudioEncoderConfig(config: AoqAudioCodecConfig): number
```

参数

类型

说明

config

AoqAudioCodecConfig

音频编码配置；trackType 应设为 AoqTrackType.AoqTrackTypeAudio

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECParamInvalid 表示参数非法）。

**说明**codecType 决定编码格式（默认 Opus），sampleRate 与 channel 需与采集端匹配；bitrate 仅在 Opus 等有损编码下生效。

#### setAudioDecoderConfig

设置音频解码参数，用于下行拉流的音频解码。需与远端编码参数匹配。

```
setAudioDecoderConfig(config: AoqAudioCodecConfig): number
```

参数

类型

说明

config

AoqAudioCodecConfig

音频解码配置；trackType 应设为 AoqTrackType.AoqTrackTypeAudio

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**sampleRate 需与远端编码器输出采样率一致，否则可能触发解码错误或音质异常。

### 音频文件播放

#### startAudioFile

开始推流播放本地音频文件。可同时推流到远端和本地播放，音量分别由 publishVolume 和 playoutVolume 控制。

```
startAudioFile(fileId: string, config: AoqAudioFileMixConfig): number
```

参数

类型

说明

fileId

string

文件标识符，业务方自定义，用于后续控制

config

AoqAudioFileMixConfig

音频文件播放配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**播放状态变化通过 onAudioFileState 回调通知；同一 fileId 重复调用会覆盖之前的播放。

#### stopAudioFile

停止音频文件播放。

```
stopAudioFile(fileId: string): number
```

参数

类型

说明

fileId

string

文件标识符，与 startAudioFile 传入的一致

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pauseAudioFile

暂停音频文件播放。

```
pauseAudioFile(fileId: string): number
```

参数

类型

说明

fileId

string

文件标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### resumeAudioFile

恢复音频文件播放。需在 pauseAudioFile 之后调用。

```
resumeAudioFile(fileId: string): number
```

参数

类型

说明

fileId

string

文件标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioFileDuration

获取音频文件总时长。

```
getAudioFileDuration(fileId: string): number
```

参数

类型

说明

fileId

string

文件标识符

返回值：文件总时长（毫秒）；文件未加载或不存在时返回 0。

#### getAudioFileCurrentPosition

获取音频文件当前播放位置。

```
getAudioFileCurrentPosition(fileId: string): number
```

参数

类型

说明

fileId

string

文件标识符

返回值：当前播放位置（毫秒）；文件未加载或不存在时返回 0。

#### setAudioFilePositionMillis

设置音频文件播放位置（seek）。

```
setAudioFilePositionMillis(fileId: string, positionMillis: number): number
```

参数

类型

说明

fileId

string

文件标识符

positionMillis

number

目标播放位置（毫秒）

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### setAudioFileVolume

设置音频文件音量，可分别控制推流音量和本地播放音量。

```
setAudioFileVolume(fileId: string, type: AoqAudioStreamDirection, volume: number): number
```

参数

类型

说明

fileId

string

文件标识符

type

AoqAudioStreamDirection

音量方向；AoqAudioStreamPublish 推流，AoqAudioStreamPlayout 播放

volume

number

音量值，取值范围 \[0-100\]

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioFileVolume

获取音频文件当前音量。

```
getAudioFileVolume(fileId: string, type: AoqAudioStreamDirection): number
```

参数

类型

说明

fileId

string

文件标识符

type

AoqAudioStreamDirection

音量方向

返回值：当前音量值 \[0-100\]；文件不存在时返回 0。

### 外部音频流

#### addAudioExternalStream

新增一条外部音频流。可创建多条独立的外部流，通过 streamId 区分。

```
addAudioExternalStream(streamId: string, config: AoqAudioExternalStreamConfig): number
```

参数

类型

说明

streamId

string

外部流标识符，业务方自定义

config

AoqAudioExternalStreamConfig

外部音频流配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pushAudioExternalStreamData

输入外部音频 PCM 数据到指定流。

```
pushAudioExternalStreamData(streamId: string, data: AoqAudioFrameData): number
```

参数

类型

说明

streamId

string

外部流标识符

data

AoqAudioFrameData

PCM 音频帧数据

返回值：0 表示调用成功；非 0 表示失败。缓冲区满时返回 AoqECAudioExternalBufferFull(110)。

**说明**data.dataPtr 指向的内存仅在调用期间有效，SDK 内部会拷贝；采样率/声道数需与 addAudioExternalStream 时的配置一致。

#### setAudioExternalStreamVolume

设置外部音频流音量，可分别控制推流音量和本地播放音量。

```
setAudioExternalStreamVolume(streamId: string, type: AoqAudioStreamDirection, vol: number): number
```

参数

类型

说明

streamId

string

外部流标识符

type

AoqAudioStreamDirection

音量方向

vol

number

音量值，取值范围 \[0-100\]

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioExternalStreamVolume

获取外部音频流当前音量。

```
getAudioExternalStreamVolume(streamId: string, type: AoqAudioStreamDirection): number
```

参数

类型

说明

streamId

string

外部流标识符

type

AoqAudioStreamDirection

音量方向

返回值：当前音量值 \[0-100\]；流不存在时返回 0。

#### clearAudioExternalStreamBuffer

清空外部音频流缓存，支持淡出效果。常用于打断当前播放内容。

```
clearAudioExternalStreamBuffer(streamId: string, fadeoutMs: number): void
```

参数

类型

说明

streamId

string

外部流标识符

fadeoutMs

number

淡出时长（毫秒）；-1 表示使用默认值，0 表示立即清空，>0 表示保留指定毫秒数淡出

返回值：无（void）。

#### removeAudioExternalStream

移除外部音频流，释放相关资源。

```
removeAudioExternalStream(streamId: string): number
```

参数

类型

说明

streamId

string

外部流标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

### 音频帧回调

#### setAudioFrameObserver

设置音频帧数据回调 observer。传入 observer=null 表示移除监听。

```
setAudioFrameObserver(observer: IAudioFrameObserver | null): number
```

参数

类型

说明

observer

IAudioFrameObserver | null

音频帧监听接口；传 null 表示移除

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需先调用本接口设置 observer，再通过 enableAudioFrameObserver 开启具体位置的回调。

#### enableAudioFrameObserver

开启或关闭指定位置的音频帧回调。

```
enableAudioFrameObserver(enabled: boolean, audioSource: AoqAudioSource, config: AoqAudioObserverConfig): number
```

参数

类型

说明

enabled

boolean

true 表示开启；false 表示关闭

audioSource

AoqAudioSource

音频源位置；可选采集/3A处理后/推流/播放

config

AoqAudioObserverConfig

回调配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**frame.dataPtr 是 native 内存的 Uint8Array 拷贝，当前为只读（ReadWrite 模式暂等效 ReadOnly，真回写为后续规划）；回调在 JS 线程异步通知，业务回调里可直接操作 ets 状态。

### 本地音量提示

#### enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示。开启后 SDK 按 config.interval 周期触发 onLocalAudioVolumeIndication 回调，上报本地采集音量及是否人声。

```
enableLocalAudioVolumeIndication(config: AoqAudioVolumeIndicationConfig): number
```

参数

类型

说明

config

AoqAudioVolumeIndicationConfig

音量提示配置；interval<=0 表示关闭回调

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需在 startAudioCapture 之后调用才有音量数据；interval>0 且 <10 时按 10 处理。

### 视频设备管理

#### startVideoCapture

打开视频采集设备（摄像头），采集内容通过 AoqTrackType.AoqTrackTypeVideo 通道发送。若使用外部视频输入（pushExternalVideoCapturedFrame），需将 isExternal 设为 true，此时不会真正打开摄像头。

```
startVideoCapture(config: AoqVideoCaptureConfig): number
```

参数

类型

说明

config

AoqVideoCaptureConfig

视频采集配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECVideoDeviceCameraAuthFailed 表示摄像头权限未获取）。

**说明**需在 module.json5 声明 ohos.permission.CAMERA 并动态申请权限；设备状态变化通过 onVideoDeviceStateChanged 回调通知。

#### stopVideoCapture

关闭视频采集设备，停止本地视频采集。

```
stopVideoCapture(): number
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### switchCamera

切换前后置摄像头。

```
switchCamera(direction: AoqCameraDirection): number
```

**参数**

**类型**

**说明**

direction

AoqCameraDirection

AoqCameraDirectionFront 或 AoqCameraDirectionBack

#### setLocalView

设置或移除本地视频渲染窗口。

```
setLocalView(trackType: AoqTrackType, canvas: AoqVideoCanvas | null): number
```

**参数**

**类型**

**说明**

trackType

AoqTrackType

AoqTrackTypeVideo

canvas

AoqVideoCanvas | null

渲染画布配置；传 null 或 canvas.view 为 null 表示移除渲染窗口

**说明**OHOS 上必须在 XComponent.onLoad 回调之后调用，canvas.view 应传入 AoqXComponentController 实例。

#### setRemoteView

设置或移除远端视频渲染窗口。

```
setRemoteView(trackType: AoqTrackType, canvas: AoqVideoCanvas | null): number
```

**参数**

**类型**

**说明**

trackType

AoqTrackType

AoqTrackTypeVideo

canvas

AoqVideoCanvas | null

渲染画布配置；传 null 或 canvas.view 为 null 表示移除渲染窗口

### 视频编码与外部输入

#### setVideoEncoderConfig

设置视频编码参数，用于上行推流的视频编码，按 config.trackType 路由。若 isExternal=true，SDK 不做二次编码，由 pushExternalVideoEncodedFrame 直推已编码帧。

```
setVideoEncoderConfig(config: AoqVideoCodecConfig): number
```

参数

类型

说明

config

AoqVideoCodecConfig

视频编码配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**使用 pushExternalVideoEncodedFrame 时，必须先调用本接口且 isExternal=true，该模式不经过采集管线，无需 startVideoCapture/startScreenCapture；使用 pushExternalVideoCapturedFrame 时，isExternal 保持 false，由 SDK 内部编码。

#### setVideoDecoderConfig

```
setVideoDecoderConfig(config: AoqVideoCodecConfig): number
```

`config` 为视频解码配置。仅以下字段生效：`trackType`, `codecType`, `width`, `height`, `fps`, `bitrate`. 其余字段仅用于编码。

Screen 不支持下行解码。`config.trackType` 为 Screen 时返回 `AoqECUnSupport`，配置不下发。

返回值：0 表示成功；非 0 表示失败。

#### pushExternalVideoCapturedFrame

推送外部采集视频帧。

```
pushExternalVideoCapturedFrame(trackType: AoqTrackType, frame: AoqVideoFrame): number
```

**参数**

**类型**

**说明**

trackType

AoqTrackType

AoqTrackTypeVideo

；也支持 AoqTrackTypeScreen

frame

AoqVideoFrame

视频帧数据

**路由规则**：Video 轨道需先调用 startVideoCapture(isExternal=true)，Screen 轨道需先调用 startScreenCapture(isExternal=true)。支持格式：NV12 / NV21 / BGRA / RGBA / I420。

若缓冲区满，会返回错误码 AoqECVideoExternalBufferFull(210)，调用方需 sleep 后重试，禁止 busy loop。

#### pushExternalVideoEncodedFrame

推送外部已编码视频帧。SDK 不做二次编码，直接打包发送。

```
pushExternalVideoEncodedFrame(trackType: AoqTrackType, frame: AoqVideoEncodedFrame): number
```

**参数**

**类型**

**说明**

trackType

AoqTrackType

AoqTrackTypeVideo

；也支持 AoqTrackTypeScreen

frame

AoqVideoEncodedFrame

已编码帧数据

**路由规则**：仅在 setVideoEncoderConfig(isExternal=true) 配置后才消费。

### 屏幕采集

```
startScreenCapture(config: AoqScreenCaptureConfig): number
stopScreenCapture(): number
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

启动返回 0 表示请求已受理，最终状态通过 `onScreenCaptureStateChanged` 通知；非 0 表示同步拒绝，不重复报告失败事件。停止返回 0 表示成功，非 0 表示失败，停止结果由该回调通知。

`isExternal=false` 时由 SDK 内部采集，系统展示授权交互。无需等待 Started 才开启发送或生产外部帧。

外部原始帧：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`；不需要调用 `startScreenCapture`。

### 媒体流发送控制

#### enableSendMediaStream

控制本地媒体流的发送，按 trackType 路由到对应轨道。

```
enableSendMediaStream(trackType: AoqTrackType, enable: boolean): number
```

**参数**

**类型**

**说明**

trackType

AoqTrackType

AoqTrackTypeAudio / AoqTrackTypeVideo

；支持 AoqTrackTypeScreen

enable

boolean

true 启用发送；false 停用发送

**使用建议**：初始化后先调用 enableSendMediaStream(trackType, false)，待 connect 成功且会话握手完成（收到 onConnectionStatusChange(AoqConnectionStatusConnected)）后再开启发送。

### 视频帧回调

#### setVideoFrameObserver

设置视频帧数据回调 observer。传入 observer=null 表示移除监听。

```
setVideoFrameObserver(observer: IVideoFrameObserver | null): number
```

参数

类型

说明

observer

IVideoFrameObserver | null

视频帧监听接口；传 null 表示移除

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需先调用本接口设置 observer，再通过 enableVideoFrameObserver 开启具体位置的回调。

#### enableVideoFrameObserver

开启或关闭指定位置的视频帧回调。

```
enableVideoFrameObserver(enabled: boolean, videoSource: AoqVideoSource, config: AoqVideoObserverConfig): number
```

参数

类型

说明

enabled

boolean

true 表示开启；false 表示关闭

videoSource

AoqVideoSource

视频源位置；可选采集后/编码前/远端解码后

config

AoqVideoObserverConfig

回调配置；通过 config.trackType 指定观察 Video 或 Screen 轨道

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**frame 各 buffer 是 native 内存的 Uint8Array 拷贝，当前为只读（返回值被忽略，ReadWrite 模式暂等效 ReadOnly，真回写为后续规划）。

### 实时消息

#### sendDataMsg

发送实时数据消息到远端。需在 connect 成功且 enableSendMediaStream(Data, true) 之后调用。

```
sendDataMsg(msg: AoqDataMsg): number
```

参数

类型

说明

msg

AoqDataMsg

数据消息

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**远端通过 onDataMsg 回调接收；消息大小受 SDK 内部限制，超大消息建议分片发送。

### AoqEngineEventListener 回调

所有回调均为可选属性（?）。

```
export interface AoqEngineEventListener {
  onError?: (code: number, message: string) => void;
  onWarning?: (code: number, message: string) => void;
  onConnectionStatusChange?: (status: AoqConnectionStatus) => void;
  onStats?: (stats: AoqStats) => void;
  onAudioDeviceStateChanged?: (state: AoqAudioDeviceState) => void;
  onAudioDeviceRouteChanged?: (routeType: number) => void;
  onAudioDeviceInterrupted?: (interrupt: boolean) => void;
  onVideoDeviceStateChanged?: (state: AoqVideoDeviceState) => void;
  onAudioFileState?: (state: AoqAudioFileState) => void;
  onDataMsg?: (msg: AoqDataMsg) => void;
  onScreenCaptureStateChanged?: (state: AoqScreenCaptureState) => void;
  onLocalAudioVolumeIndication?: (volume: AoqAudioVolume) => void;
}
```

#### onError

引擎错误回调。发生不可恢复错误时触发。

```
onError?: (code: number, message: string) => void
```

参数

类型

说明

code

number

错误码，对应 AoqErrorCode 枚举值

message

string

错误描述信息

返回值：无（void）。

#### onWarning

引擎警告回调。发生可恢复异常时触发，不影响 SDK 继续运行。

```
onWarning?: (code: number, message: string) => void
```

参数

类型

说明

code

number

警告码，对应 AoqWarningCode 枚举值

message

string

警告描述信息

返回值：无（void）。

#### onConnectionStatusChange

连接状态变化回调。状态流转：Disconnected -> Connecting -> Connected/Failed -> Disconnected。

```
onConnectionStatusChange?: (status: AoqConnectionStatus) => void
```

参数

类型

说明

status

AoqConnectionStatus

当前连接状态

返回值：无（void）。

**说明**收到 Connected 后再调用 enableSendMediaStream(trackType, true) 开启媒体流发送。

#### onStats

引擎统计信息回调。SDK 周期性上报音视频推拉流及网络统计数据，可用于实时监控通话质量、网络状态、诊断音视频问题。

```
onStats?: (stats: AoqStats) => void
```

参数

类型

说明

stats

AoqStats

统计信息，包含音频/视频/数据消息的推拉流统计及网络统计

返回值：无（void）。

#### onAudioDeviceStateChanged

音频设备采集/播放操作状态变化回调。

```
onAudioDeviceStateChanged?: (state: AoqAudioDeviceState) => void
```

参数

类型

说明

state

AoqAudioDeviceState

音频设备状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

#### onAudioDeviceRouteChanged

音频输出路由变化回调。

```
onAudioDeviceRouteChanged?: (routeType: number) => void
```

参数

类型

说明

routeType

number

当前音频输出路由，对应 AoqAudioDeviceRouteType 枚举值

返回值：无（void）。

#### onAudioDeviceInterrupted

音频设备中断回调。系统级中断（如来电、其他应用抢占音频焦点）时触发。

```
onAudioDeviceInterrupted?: (interrupt: boolean) => void
```

参数

类型

说明

interrupt

boolean

true 表示被中断；false 表示中断恢复

返回值：无（void）。

#### onVideoDeviceStateChanged

视频设备采集操作状态变化回调。

```
onVideoDeviceStateChanged?: (state: AoqVideoDeviceState) => void
```

参数

类型

说明

state

AoqVideoDeviceState

视频设备状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

#### onScreenCaptureStateChanged

屏幕采集状态变化回调。使用 AoqScreenCaptureStateCode 与统一的 AoqErrorCode，在 JS 线程异步通知。屏幕失败不重复通过 onError 上报。

```
onScreenCaptureStateChanged?: (state: AoqScreenCaptureState) => void
```

参数

类型

说明

state

AoqScreenCaptureState

屏幕采集状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

**说明**Started 表示采集/外部输入已就绪，不表示媒体已发送；Fail 和 Stopped 均为清理完成后的终态。

#### onAudioFileState

音频文件播放状态回调。

```
onAudioFileState?: (state: AoqAudioFileState) => void
```

参数

类型

说明

state

AoqAudioFileState

音频文件播放状态；包含 fileId、stateCode、errorCode

返回值：无（void）。

#### onLocalAudioVolumeIndication

本地采集音量提示回调。需调用 enableLocalAudioVolumeIndication 开启后才会触发。

```
onLocalAudioVolumeIndication?: (volume: AoqAudioVolume) => void
```

参数

类型

说明

volume

AoqAudioVolume

本地音量信息；包含 isSpeech（是否人声）和 volume（平滑后瞬时音量 \[0-255\]）

返回值：无（void）。

#### onDataMsg

收到实时数据消息回调。

```
onDataMsg?: (msg: AoqDataMsg) => void
```

参数

类型

说明

msg

AoqDataMsg

数据消息

返回值：无（void）。

**说明**回调在 JS 线程异步通知；data 仅在回调期间有效，异步使用需自行拷贝。

### IAudioFrameObserver 回调

音频帧数据监听接口。所有方法均为可选，按需实现。frame.dataPtr 是 native 内存的 Uint8Array 拷贝，当前为只读（ReadWrite 留作后续规划）。

```
export interface IAudioFrameObserver {
  onCapturedAudioFrame?: (frame: AoqAudioFrameData) => void;
  onProcessCapturedAudioFrame?: (frame: AoqAudioFrameData) => void;
  onPublishAudioFrame?: (trackType: AoqTrackType, frame: AoqAudioFrameData) => void;
  onPlaybackAudioFrame?: (frame: AoqAudioFrameData) => void;
}
```

方法

触发时机

参数

onCapturedAudioFrame

采集到原始音频帧时（AoqAudioSourceCaptured）

frame: AoqAudioFrameData

onProcessCapturedAudioFrame

3A 处理后的音频帧（AoqAudioSourceProcessCaptured）

frame: AoqAudioFrameData

onPublishAudioFrame

推流前的音频帧（AoqAudioSourcePublish）

trackType: 轨道类型；frame: AoqAudioFrameData

onPlaybackAudioFrame

播放前的远端音频帧（AoqAudioSourcePlayback）

frame: AoqAudioFrameData

返回值：无（void）。

**说明**用法为 setAudioFrameObserver(obs) + enableAudioFrameObserver(true, src, cfg)；回调在 JS 线程异步通知，业务回调里可直接操作 ets 状态。

#### onCapturedAudioFrame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

```
onCapturedAudioFrame?(frame: AoqAudioFrameData): void
```

参数

类型

说明

frame

AoqAudioFrameData

采集的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 为 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

#### onProcessCapturedAudioFrame

3A 处理后的音频帧回调。数据经过回声消除、噪声抑制、自动增益等 3A 处理。

```
onProcessCapturedAudioFrame?(frame: AoqAudioFrameData): void
```

参数

类型

说明

frame

AoqAudioFrameData

3A 处理后的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 为 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

#### onPublishAudioFrame

推流前的音频帧回调。数据即将通过编码后发送到 Relay 服务器。

```
onPublishAudioFrame?(trackType: AoqTrackType, frame: AoqAudioFrameData): void
```

参数

类型

说明

trackType

AoqTrackType

轨道类型

frame

AoqAudioFrameData

推流前的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 为 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

#### onPlaybackAudioFrame

播放前的远端音频帧回调。数据为远端解码后、混音前即将播放的音频。

```
onPlaybackAudioFrame?(frame: AoqAudioFrameData): void
```

参数

类型

说明

frame

AoqAudioFrameData

播放前的远端音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 为 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

### IVideoFrameObserver 回调

视频帧数据监听接口。所有方法均为可选，返回 boolean（当前返回值被忽略，只读语义，ReadWrite 留作后续规划）。三个回调均带 trackType 参数，用于区分 Video / Screen 轨道。

```
export interface IVideoFrameObserver {
  onCapturedVideoFrame?: (trackType: AoqTrackType, frame: AoqVideoFrame) => boolean;
  onPreEncodeVideoFrame?: (trackType: AoqTrackType, frame: AoqVideoFrame) => boolean;
  onRemoteVideoFrame?: (trackType: AoqTrackType, frame: AoqVideoFrame) => boolean;
}
```

方法

触发时机

参数

onCapturedVideoFrame

采集到原始视频帧时（前处理前，AoqVideoSourceCaptured）

trackType: 轨道类型；frame: AoqVideoFrame

onPreEncodeVideoFrame

编码前的视频帧（前处理后，AoqVideoSourcePreEncode）

trackType: 轨道类型；frame: AoqVideoFrame

onRemoteVideoFrame

远端解码后、渲染前的视频帧（AoqVideoSourceRemote）

trackType: 轨道类型；frame: AoqVideoFrame

返回值：boolean。语义上返回 true 表示数据已修改需写回 SDK；当前 OHOS NAPI 路径不真回写，返回值被忽略。

**说明**用法为 setVideoFrameObserver(obs) + enableVideoFrameObserver(true, src, cfg)；frame 各 buffer 是 native 内存的 Uint8Array 拷贝，仅回调期间有效。

#### onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。数据为摄像头或屏幕采集后的原始帧，未经前处理。

```
onCapturedVideoFrame?(trackType: AoqTrackType, frame: AoqVideoFrame): boolean
```

参数

类型

说明

trackType

AoqTrackType

轨道类型，区分 Video / Screen

frame

AoqVideoFrame

采集的视频帧数据

返回值：boolean。true 表示数据已修改需写回 SDK；当前 OHOS NAPI 路径不真回写，语义等同 false。false 表示只读。

**说明**frame 各 buffer 是 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

#### onPreEncodeVideoFrame

编码前的视频帧回调（前处理后）。数据经过前处理后、编码前。

```
onPreEncodeVideoFrame?(trackType: AoqTrackType, frame: AoqVideoFrame): boolean
```

参数

类型

说明

trackType

AoqTrackType

轨道类型，区分 Video / Screen

frame

AoqVideoFrame

编码前的视频帧数据

返回值：boolean。true 表示数据已修改需写回 SDK；当前 OHOS NAPI 路径不真回写，语义等同 false。false 表示只读。

**说明**frame 各 buffer 是 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

#### onRemoteVideoFrame

远端解码后、渲染前的视频帧回调。数据为远端接收并解码后的视频帧。

```
onRemoteVideoFrame?(trackType: AoqTrackType, frame: AoqVideoFrame): boolean
```

参数

类型

说明

trackType

AoqTrackType

轨道类型，区分 Video / Screen

frame

AoqVideoFrame

远端解码后的视频帧数据

返回值：boolean。true 表示数据已修改需写回 SDK；当前 OHOS NAPI 路径不真回写，语义等同 false。false 表示只读。

**说明**frame 各 buffer 是 native 内存的 Uint8Array 拷贝，仅在回调期间有效，异步使用需自行拷贝。

## 数据类型与枚举

v1.3.0 的 `Index.ets` 对外导出以下枚举和接口：

-   枚举：`AoqTrackMode`、`AoqScreenCaptureStateCode`。
-   接口：`AoqAudioVolumeIndicationConfig`、`AoqAudioVolume`、`AoqScreenCaptureConfig`、`AoqScreenCaptureState`。

### 通用类型

#### AoqCreateConfig

**字段**

**类型**

**默认值**

**说明**

workDir

string

""

SDK 工作目录

enableDumpAudio

boolean

false

是否开启音频原始数据 dump（调试用）

extras

string

""

扩展参数字符串

maxEncodedVideoFrameBytes

number

190 × 1024

编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。

enableDropOversizedVideoFrame

boolean

false

仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。

OHOS 无 isBTScoMode 字段。

#### AoqConnectConfig

`subscribeTracks` 不能包含 `AoqTrackTypeScreen`，否则 `connect` 返回 `AoqECUnSupport`，不发起连接。`setRemoteView` 不支持 Screen，传入时返回 `AoqECUnSupport`。

**字段**

**类型**

**默认值**

**说明**

token

string

""

连接鉴权 Token

sid

string

""

会话 ID

certFingerprint

string

""

服务器证书指纹

relayEndpoints

AoqRelayEndpoint\[\]

\[\]

Relay 接入点列表

workspaceIdHash

string

""

工作空间 ID Hash

publishTracks

AoqTrackParam\[\]

\[\]

本端计划发布的轨道列表

subscribeTracks

AoqTrackParam\[\]

\[\]

本端计划订阅的轨道列表

#### AoqRelayEndpoint

**字段**

**类型**

**说明**

endpoint

string

Relay 服务器域名或 IP

port

number

Relay 服务器端口

routeIndex

number

路径序号，默认值为 -1。

tcpPort

number

默认值为 0。TCP 降级端口；0 表示使用 SDK 默认端口 443。

#### AoqTrackParam

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

trackMode

AoqTrackMode

默认 AoqTrackModeSegment，仅对音频下行生效。

### 枚举类型

#### AoqErrorCode

**枚举值**

**值**

**说明**

AoqECOK

0

成功

AoqECParamInvalid

1

参数非法

AoqECStateInvalid

2

状态非法

AoqECUnSupport

3

不支持

AoqECAudio

100

音频通用错误

AoqECAudioExternalBufferFull

110

外部音频缓冲区满

AoqECAudioDevice

120

音频设备通用错误

AoqECAudioDeviceRecordingAuthFailed

121

录音权限未获取

AoqECAudioDeviceRecordingOccupied

122

录音设备被占用

AoqECAudioDeviceRecordingBackgroundStart

123

后台启动录音失败

AoqECAudioDeviceRecordingStartFail

124

录音启动失败

AoqECAudioDevicePlayoutOccupied

125

播放设备被占用

AoqECAudioDevicePlayoutBackgroundStart

126

后台启动播放失败

AoqECAudioDevicePlayoutStartFail

127

播放启动失败

AoqECAudioDeviceEarpieceRequiresVoipMode

128

听筒模式需要启用 VoIP 模式

AoqECVideo

200

视频通用错误

AoqECVideoExternalBufferFull

210

外部视频缓冲区满

AoqECVideoExternalCaptureNotEnabled

211

外部视频采集未启用

AoqECVideoExternalEncoderNotEnabled

212

外部视频编码器未启用

AoqECVideoDevice

220

视频设备通用错误

AoqECVideoDeviceCameraOpenFail

221

摄像头打开失败

AoqECVideoDeviceCameraAuthFailed

222

摄像头权限未获取

AoqECVideoDeviceCameraOccupied

223

摄像头被占用

AoqECVideoDeviceCameraRunningError

224

摄像头运行异常

AoqECVideoCodec

230

视频编解码通用错误

AoqECVideoCodecEncoderInitFail

231

视频编码器初始化失败

AoqECVideoRender

240

视频渲染通用错误

AoqECVideoRenderCreateFail

241

视频渲染创建失败

AoqECVideoRenderDrawError

242

视频渲染绘制错误

AoqECScreen

300

屏幕共享通用错误

AoqECScreenAuthFailed

310

屏幕共享授权失败

AoqECScreenStartFailed

311

屏幕共享启动失败

#### AoqWarningCode

**枚举值**

**值**

**说明**

AoqWCOK

0

无警告

AoqWCAudio

100

音频通用警告

AoqWCAudioHowling

101

音频啸叫检测

AoqWCAudioDevice

120

音频设备通用警告

AoqWCAudioDeviceMicEnumerateError

121

麦克风枚举错误

AoqWCAudioDeviceMicStartTimeout

122

麦克风启动超时

AoqWCAudioDeviceRecordingError

123

录音过程错误

AoqWCAudioDeviceSpeakerEnumerateError

124

扬声器枚举错误

AoqWCAudioDeviceSpeakerStartTimeout

125

扬声器启动超时

AoqWCAudioDevicePlayoutError

126

播放过程错误

AoqWCVideo

200

视频通用警告

AoqWCVideoCameraEnumerateError

201

摄像头枚举错误

AoqWCVideoEncoderSwitched

202

视频编码器已切换

AoqWCVideoRenderDowngrade

203

视频渲染降级

#### AoqTrackType

**枚举值**

**值**

**说明**

AoqTrackTypeAudio

0

音频轨道

AoqTrackTypeVideo

1

视频轨道

AoqTrackTypeData

2

数据消息轨道

AoqTrackTypeScreen

3

屏幕共享轨道，仅支持上行。

#### AoqEncoderType

Track 媒体编码格式。

枚举值

值

说明

AoqEncoderTypeUnknown

0

未知格式

AoqEncoderTypeAudioPCM

1

音频 PCM

AoqEncoderTypeAudioOpus

2

音频 Opus

AoqEncoderTypeVideoH264

3

视频 H.264

AoqEncoderTypeVideoJpeg

4

视频 JPEG

AoqEncoderTypeDataText

5

数据文本

#### AoqTrackMode

枚举值

值

说明

AoqTrackModeSegment

0

分段：按语义片段（如一句话）交付数据；仅对音频下行生效。

AoqTrackModeStream

1

流式：连续交付数据；仅对音频下行生效。

#### AoqConnectionStatus

**枚举值**

**值**

**说明**

AoqConnectionStatusDisconnected

0

未连接

AoqConnectionStatusConnecting

1

连接中

AoqConnectionStatusConnected

2

已连接

AoqConnectionStatusFailed

3

连接失败

#### AoqMirrorMode

镜像模式。

枚举值

值

说明

AoqMirrorModeDisabled

0

关闭镜像

AoqMirrorModeEnabled

1

开启镜像

#### AoqOrientationMode

视频方向模式。

枚举值

值

说明

AoqOrientationModeAuto

0

自动适应

AoqOrientationModePortrait

1

竖屏

AoqOrientationModeLandscape

2

横屏

### 音频类型

#### AoqAudioCaptureConfig

**字段**

**类型**

**默认值**

**说明**

isExternal

boolean

false

true 使用外部音频输入

isVoipMode

boolean

false

true 启用 VoIP 模式（硬件 AEC）

channel

number

1

声道数，支持 1/2

#### AoqAudioPlaybackConfig

**字段**

**类型**

**默认值**

**说明**

isVoipMode

boolean

false

true 启用 VoIP 模式（硬件 AEC），采集/播放参数先到为准

isDefaultSpeaker

boolean

true

true 默认扬声器；false 默认听筒

isExternal

boolean

false

true 使用外部音频输出

channel

number

1

声道数，支持 1/2

#### AoqAudioCodecConfig

**字段**

**类型**

**默认值**

**说明**

trackType

AoqTrackType

AoqTrackTypeAudio

目标轨道

codecType

AoqEncoderType

AoqEncoderTypeAudioOpus

编码格式

sampleRate

number

48000

采样率(Hz)

channel

number

1

声道数

bitrate

number

32000

码率(bps)

#### AoqAudioDeviceStateCode

音频设备采集播放操作状态码。

枚举值

值

说明

AoqAudioDeviceNone

0

无状态

AoqAudioDeviceRecordStarting

1

采集启动中

AoqAudioDeviceRecordStarted

2

采集已启动

AoqAudioDeviceRecordStopping

3

采集停止中

AoqAudioDeviceRecordStopped

4

采集已停止

AoqAudioDeviceRecordFail

5

采集失败

AoqAudioDevicePlayStarting

6

播放启动中

AoqAudioDevicePlayStarted

7

播放已启动

AoqAudioDevicePlayStopping

8

播放停止中

AoqAudioDevicePlayStopped

9

播放已停止

AoqAudioDevicePlayFail

10

播放失败

#### AoqAudioDeviceState

音频设备状态。

字段

类型

默认值

说明

state

AoqAudioDeviceStateCode

AoqAudioDeviceNone

状态码

reason

number

0

错误原因代码（参考 AoqErrorCode）

#### AoqAudioDeviceRouteType

音频设备路由类型。

枚举值

值

说明

AoqAudioDeviceRouteDefault

0

默认路由

AoqAudioDeviceRouteHeadset

1

有麦克风的头戴设备

AoqAudioDeviceRouteEarpiece

2

听筒

AoqAudioDeviceRouteHeadsetNoMic

3

无麦克风的头戴设备

AoqAudioDeviceRouteSpeakerPhone

4

扬声器

AoqAudioDeviceRouteUsb

5

USB 音频设备

AoqAudioDeviceRouteBluetooth

6

蓝牙 SCO 模式

AoqAudioDeviceRouteBluetoothA2dp

7

蓝牙 A2DP 模式

### 音频文件类型

#### AoqAudioFileMixConfig

**字段**

**类型**

**默认值**

**说明**

fileName

string

""

文件名（含路径）

cycles

number

\-1

循环次数，-1 无限循环

startPosMs

number

0

起始播放位置(ms)

publishVolume

number

100

推流音量 \[0,100\]

playoutVolume

number

100

本地播放音量 \[0,100\]

#### AoqAudioFileStateCode

音频文件状态码。

枚举值

值

说明

AoqAudioFileNone

0

无状态

AoqAudioFileStarted

1

播放已启动

AoqAudioFileStopped

2

播放已停止

AoqAudioFilePaused

3

播放已暂停

AoqAudioFileResumed

4

播放已恢复

AoqAudioFileEnded

5

播放已结束

AoqAudioFileBuffering

6

播放缓冲中

AoqAudioFileBufferingEnd

7

缓冲结束

AoqAudioFileFailed

8

播放失败

#### AoqAudioFileErrorCode

音频文件错误码。

枚举值

值

说明

AoqAudioFileNoError

0

无错误

AoqAudioFileOpenFailed

1

文件打开失败

AoqAudioFileDecodeFailed

2

文件解码失败

#### AoqAudioFileState

音频文件状态。

字段

类型

默认值

说明

fileId

string

""

文件 ID

stateCode

AoqAudioFileStateCode

AoqAudioFileNone

状态码

errorCode

AoqAudioFileErrorCode

AoqAudioFileNoError

错误码

### 外部音频流与音量类型

#### AoqAudioStreamDirection

外部音频流方向。

枚举值

值

说明

AoqAudioStreamPublish

0

发布流（推流）

AoqAudioStreamPlayout

1

播放流（拉流）

#### AoqAudioExternalStreamToggle

外部音频流切换状态。

枚举值

值

说明

AoqAudioExternalStreamToggleNormal

0

正常状态

AoqAudioExternalStreamTogglePause

1

暂停状态

#### AoqAudioExternalStreamConfig

**字段**

**类型**

**默认值**

**说明**

trackType

AoqTrackType

AoqTrackTypeAudio

轨道类型

codecType

AoqEncoderType

AoqEncoderTypeAudioPCM

音频格式

channels

number

1

声道数

sampleRate

number

48000

采样率(Hz)

playoutVolume

number

100

播放音量 \[0,100\]

publishVolume

number

100

推流音量 \[0,100\]

maxBufferDuration

number

1000

最大缓冲(ms)

enable3A

boolean

false

输入 PCM 做 3A 处理

#### AoqAudioFrameData

**字段**

**类型**

**说明**

dataPtr

ArrayBuffer | Uint8Array | null

音频 PCM 裸数据

dataSize

number

PCM 字节数

numOfSamples

number

采样点数(单声道)

bytesPerSample

number

每采样点字节数

numOfChannels

number

声道数

samplesPerSec

number

每秒采样点数

pushSequence

number

PCM 输入轮次

timeStamp

number

时间戳

autoGenMute

boolean

true 表示 SDK 生成的静音数据

#### AoqAudioSource

音频帧回调数据来源。

枚举值

值

说明

AoqAudioSourceCaptured

0

采集的音频数据

AoqAudioSourceProcessCaptured

1

3A 处理后的音频数据

AoqAudioSourcePublish

2

推流的音频数据

AoqAudioSourcePlayback

3

播放的音频数据

#### AoqAudioObserverMode

音频帧回调模式。

枚举值

值

说明

AoqAudioObserverModeReadOnly

0

只读模式

AoqAudioObserverModeReadWrite

1

读写模式（当前 OHOS NAPI 路径不真回写，语义等同 ReadOnly）

#### AoqAudioObserverConfig

**字段**

**类型**

**默认值**

**说明**

sampleRate

number

48000

回调采样率

channels

number

1

回调声道数

mode

AoqAudioObserverMode

ReadOnly

读写模式

#### AoqAudioVolumeIndicationConfig

字段

类型

默认值

说明

reportSpeech

boolean

false

是否检测人声。

interval

number

0

回调间隔（毫秒）；小于等于 0 时关闭，大于 0 且小于 10 时按 10 处理。

smooth

number

3

平滑系数，范围 0～10；越大越平滑。

#### AoqAudioVolume

字段

类型

说明

isSpeech

boolean

是否为人声。

volume

number

平滑后的瞬时音量，范围 0～255。

### 视频类型

#### AoqRenderMode

渲染显示模式。

枚举值

值

说明

AoqRenderModeAuto

0

自动模式

AoqRenderModeStretch

1

拉伸平铺，画面可能变形

AoqRenderModeFill

2

填充黑边，画面完整

AoqRenderModeCrop

3

裁剪模式，画面内容可能丢失

#### AoqVideoCanvas

**字段**

**类型**

**默认值**

**说明**

view

Object | null

null

AoqXComponentController 实例；传 null 表示移除渲染绑定

renderMode

AoqRenderMode

AoqRenderModeAuto

显示模式

#### AoqCameraDirection

摄像头方向。

枚举值

值

说明

AoqCameraDirectionFront

0

前置摄像头

AoqCameraDirectionBack

1

后置摄像头

#### AoqVideoCaptureConfig

**字段**

**类型**

**默认值**

**说明**

width

number

1280

采集宽度；isExternal=true 时无效

height

number

720

采集高度

fps

number

15

采集帧率

isExternal

boolean

false

true 不打开摄像头，由 pushExternalVideoCapturedFrame 喂帧

cameraDirection

AoqCameraDirection

Front

摄像头方向

#### AoqScreenCaptureConfig

字段

类型

默认值

说明

isExternal

boolean

false

是否由应用提供屏幕原始帧。

#### AoqVideoPixelFormat

**枚举值**

**值**

**说明**

AoqVideoPixelFormatUnknown

0

未知

AoqVideoPixelFormatI420

1

I420

AoqVideoPixelFormatNV12

2

NV12

AoqVideoPixelFormatNV21

3

NV21

AoqVideoPixelFormatBGRA

4

BGRA

AoqVideoPixelFormatRGBA

5

RGBA

OHOS 不支持 TextureOES/Texture2D。

#### AoqVideoFrame

**字段**

**类型**

**说明**

format

AoqVideoPixelFormat

像素格式

width

number

宽度(像素)

height

number

高度(像素)

dataPtr

ArrayBuffer | Uint8Array | null

打包格式数据

dataSize

number

打包数据字节数

dataY / dataU / dataV

ArrayBuffer | Uint8Array | null

I420 平面

strideY / strideU / strideV

number

平面 stride

timeStamp

number

时间戳(ms)；0 时 SDK 用本地时钟补

#### AoqVideoCodecType

外部编码帧 codec 类型。

枚举值

值

说明

AoqVideoCodecTypeJPEG

0

JPEG 编码

#### AoqVideoEncodedFrame

**字段**

**类型**

**说明**

codec

AoqVideoCodecType

编码格式 (AoqVideoCodecTypeJPEG=0)

data

ArrayBuffer | Uint8Array

编码后数据

width

number

宽度

height

number

高度

timeStamp

number

时间戳(ms)

#### AoqVideoCodecConfig

**字段**

**类型**

**默认值**

**说明**

trackType

AoqTrackType

AoqTrackTypeVideo

目标轨道

codecType

AoqEncoderType

AoqEncoderTypeVideoH264

编码格式

width

number

540

编码宽度

height

number

960

编码高度

fps

number

5

帧率

bitrate

number

500000

码率(bps)

minBitrate

number

128000

最小码率(bps)

keyframeInterval

number

2

关键帧间隔(秒)

mirrorMode

AoqMirrorMode

Disabled

镜像模式

orientationMode

AoqOrientationMode

Auto

视频方向

isExternal

boolean

false

true 时 SDK 不做二次编码

#### AoqVideoDeviceStateCode

视频设备采集操作状态码。

枚举值

值

说明

AoqVideoDeviceNone

0

无状态

AoqVideoDeviceCaptureStarting

1

摄像头正在启动

AoqVideoDeviceCaptureStarted

2

摄像头已启动

AoqVideoDeviceCaptureStopping

3

摄像头正在停止

AoqVideoDeviceCaptureStopped

4

摄像头已停止

AoqVideoDeviceCaptureFail

5

摄像头启动失败

#### AoqVideoDeviceState

视频设备状态。

字段

类型

默认值

说明

state

AoqVideoDeviceStateCode

AoqVideoDeviceNone

状态码

reason

number

0

错误原因代码（参考 AoqErrorCode）

#### AoqScreenCaptureStateCode

枚举值

值

说明

AoqScreenCaptureNone

0

无

AoqScreenCaptureStarting

1

启动中

AoqScreenCaptureStarted

2

输入已就绪，不表示媒体已发送

AoqScreenCaptureStopping

3

停止中

AoqScreenCaptureStopped

4

已停止

AoqScreenCaptureFail

5

启动或运行失败

#### AoqScreenCaptureState

字段

类型

默认值

说明

state

AoqScreenCaptureStateCode

—

屏幕采集状态。

reason

number

—

正常为 0；失败时为 AoqErrorCode 错误码。

### 视频帧回调类型

#### AoqVideoSource

视频帧回调数据源（管线位置）。

枚举值

值

说明

AoqVideoSourceCaptured

0

采集后的视频数据（前处理前）

AoqVideoSourcePreEncode

1

编码前的视频数据（前处理后）

AoqVideoSourceRemote

2

远端解码后、渲染前的视频数据

#### AoqVideoObserverMode

视频帧回调模式。

枚举值

值

说明

AoqVideoObserverModeReadOnly

0

只读模式

AoqVideoObserverModeReadWrite

1

读写模式（当前 OHOS NAPI 路径不真回写，语义等同 ReadOnly）

#### AoqVideoObserverAlignment

视频输出宽度对齐方式。

枚举值

值

说明

AoqVideoObserverAlignmentDefault

0

默认对齐

AoqVideoObserverAlignmentEven

1

偶数对齐

AoqVideoObserverAlignment4

2

4 字节对齐

AoqVideoObserverAlignment8

3

8 字节对齐

AoqVideoObserverAlignment16

4

16 字节对齐

#### AoqVideoObserverConfig

**字段**

**类型**

**默认值**

**说明**

format

AoqVideoPixelFormat

I420

回调像素格式

alignment

AoqVideoObserverAlignment

Default

宽度对齐

mode

AoqVideoObserverMode

ReadOnly

读写模式

mirrorApplied

boolean

false

是否应用镜像

trackType

AoqTrackType

AoqTrackTypeVideo

需要观察的视频轨道；仅支持 Video / Screen。

### 数据消息类型

#### AoqDataMsg

实时消息数据结构。

字段

类型

默认值

说明

data

ArrayBuffer / Uint8Array

必填

消息数据

### 统计数据类型

#### AoqStats

**字段**

**类型**

**说明**

audioPublishStats

AoqAudioPublishStats\[\]

音频推流统计

videoPublishStats

AoqVideoPublishStats\[\]

视频推流统计

dataMsgPublishStats

AoqDataMsgPublishStats\[\]

数据消息推流统计

audioSubscribeStats

AoqAudioSubscribeStats\[\]

音频拉流统计

videoSubscribeStats

AoqVideoSubscribeStats\[\]

视频拉流统计

dataMsgSubscribeStats

AoqDataMsgSubscribeStats\[\]

数据消息拉流统计

networkStats

AoqNetworkStats | null

网络统计

#### AoqAudioPublishStats

音频推流统计。

字段

类型

说明

trackType

number

轨道类型（对应 AoqTrackType）

bitrate

number

码率（bps）

bytes

number

累计发送字节数

encodeVolume

number

推流编码音量

#### AoqVideoPublishStats

视频推流统计。

字段

类型

说明

trackType

number

轨道类型（对应 AoqTrackType）

bitrate

number

码率（bps）

bytes

number

累计发送字节数

encodeFps

number

编码帧率

#### AoqDataMsgPublishStats

数据消息推流统计。

字段

类型

说明

trackType

number

轨道类型（对应 AoqTrackType）

bitrate

number

码率（bps）

bytes

number

累计发送字节数

#### AoqAudioSubscribeStats

音频拉流统计。

字段

类型

说明

trackType

number

轨道类型（对应 AoqTrackType）

bitrate

number

码率（bps）

bytes

number

累计接收字节数

playVolume

number

播放音量

#### AoqVideoSubscribeStats

视频拉流统计。

字段

类型

说明

trackType

number

轨道类型（对应 AoqTrackType）

bitrate

number

码率（bps）

bytes

number

累计接收字节数

decodeFps

number

解码帧率

renderFps

number

渲染帧率

#### AoqDataMsgSubscribeStats

数据消息拉流统计。

字段

类型

说明

trackType

number

轨道类型（对应 AoqTrackType）

bitrate

number

码率（bps）

bytes

number

累计接收字节数

#### AoqNetworkStats

网络统计。

字段

类型

说明

sendBitrate

number

发送码率（bps）

sendBytes

number

累计发送字节数

recvBitrate

number

接收码率（bps）

recvBytes

number

累计接收字节数

loss

number

丢包率（0-100）

rtt

number

往返延迟（ms）
