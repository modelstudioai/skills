# AOQ Client SDK Android API 参考

AOQ Client SDK Android 版提供完整的实时音视频通信能力，包括引擎生命周期管理、音频/视频采集与播放、编解码配置、外部音频流注入、音频文件混音、实时消息收发、音视频帧数据回调等功能。本文档为 Android 平台 Java API 的完整参考。

## 接口目录

### 引擎生命周期

接口

简介

createEngine

创建引擎实例（单例模式）

destroy

销毁引擎实例

getVersion

获取 SDK 版本号

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

设置音频帧数据回调监听

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

设置视频帧数据回调监听

enableVideoFrameObserver

开启或关闭指定位置的视频帧回调

### 实时消息

接口

简介

sendDataMsg

发送实时数据消息

### AoqClientListener 回调

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

onScreenCaptureStateChanged

屏幕采集状态变化回调

onVideoDeviceStateChanged

视频设备操作状态变化回调

onAudioDeviceFocusChanged

音频焦点变化回调

onAudioFileState

音频文件播放状态回调

onLocalAudioVolumeIndication

本地采集音量提示回调

onDataMsg

收到实时数据消息回调

### AoqAudioFrameListener 回调

接口

简介

onCapturedAudioFrame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

onProcessCapturedAudioFrame

3A 处理后的音频帧触发。数据已经过回声消除、降噪等处理。

onPublishAudioFrame

推流前的音频帧触发。数据为最终编码发送前的音频。

onPlaybackAudioFrame

播放前的远端音频帧触发。数据为解码后、混音后待播放的音频。

### AoqVideoFrameListener 回调

接口

简介

onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。

onPreEncodeVideoFrame

编码前的视频帧触发（前处理后）。

onRemoteVideoFrame

远端解码后、渲染前的视频帧触发。

## 接口详情

`pushExternalVideoCapturedFrame` 支持 Video / Screen，需先开启对应轨道的外部采集；未开启时返回 `AoqECVideoExternalCaptureNotEnabled`（211）。

### 引擎生命周期

**createEngine**

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

```
@NonNull
public static AoqClientEngine createEngine(
    @NonNull Context context,
    @NonNull AoqCreateConfig config,
    @NonNull AoqClientListener listener)
```

**参数**

**类型**

**说明**

context

Context

Android 应用上下文

config

AoqCreateConfig

引擎创建配置

listener

AoqClientListener

引擎事件回调监听

返回值：AoqClientEngine 引擎实例，不会返回 null。

**destroy**

销毁引擎实例，释放所有资源。销毁后需要重新调用 createEngine 才能继续使用。

```
public static int destroy()
```

参数：无。

返回值：0 表示成功；非 0 表示失败（对应 AoqErrorCode）。

**getVersion**

获取 SDK 当前版本号。可在 createEngine 之前调用。

```
@NonNull
public static String getVersion()
```

参数：无。

返回值：版本号字符串，如 "1.3.0"。

**connect**

连接 Relay 服务器。连接参数由业务方 AppServer 通过 /api/v1/allocate 分配后下发给客户端。调用后立即返回，实际连接结果通过 onConnectionStatusChange 回调通知。

```
public abstract int connect(@NonNull AoqConnectConfig config)
```

参数

类型

说明

config

AoqConnectConfig

连接配置，包含 Token、SID、Relay 接入点列表、发布/订阅轨道等

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败（对应 AoqErrorCode）。

**说明**Screen track 当前仅支持上行，下行订阅尚未实现，因此 config.subscribeTracks 中不能传入 AoqTrackTypeScreen，否则返回 AoqECUnSupport 且连接不会发起；连接成功前不建议调用 enableSendMediaStream(true)，应在 onConnectionStatusChange 收到 Connected 后再开启媒体流发送。

**disconnect**

断开与服务器的连接，释放连接相关资源。调用后立即返回，实际断开结果通过 onConnectionStatusChange 回调通知。

```
public abstract int disconnect()
```

参数：无。

返回值：0 表示调用已下发（异步执行）；非 0 表示失败（对应 AoqErrorCode）。

### 音频设备管理

#### startAudioCapture

打开音频采集设备（麦克风），开始采集本地音频。若使用外部音频输入（pushAudioExternalStreamData），需将 isExternal 设为 true，此时不会真正打开麦克风。

```
public abstract int startAudioCapture(@NonNull AoqAudioCaptureConfig config)
```

参数

类型

说明

config

AoqAudioCaptureConfig

音频采集配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECAudioDeviceRecordingAuthFailed 表示录音权限未获取）。

**说明**Android 需在调用前申请 RECORD\_AUDIO 权限；设备状态变化通过 onAudioDeviceStateChanged 回调通知。

#### stopAudioCapture

关闭音频采集设备，停止本地音频采集。

```
public abstract int stopAudioCapture()
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### muteAudioCapture

静音或取消静音音频采集。静音后 SDK 仍持续采集但发送静音帧，与 stopAudioCapture 不同。

```
public abstract int muteAudioCapture(boolean mute)
```

参数

类型

说明

mute

boolean

true 表示静音；false 表示取消静音

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需在 startAudioCapture 之后调用才生效。

#### startAudioPlayer

开始音频渲染，播放远端音频到扬声器/听筒。若使用外部渲染（自行播放 PCM），需将 isExternal 设为 true。

```
public abstract int startAudioPlayer(@NonNull AoqAudioPlaybackConfig config)
```

参数

类型

说明

config

AoqAudioPlaybackConfig

音频播放配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECAudioDevicePlayoutOccupied 表示播放设备被占用）。

**说明**设备状态变化通过 onAudioDeviceStateChanged 回调通知；输出路由变化通过 onAudioDeviceRouteChanged 回调通知。

#### stopAudioPlayer

停止音频渲染，关闭播放设备。

```
public abstract int stopAudioPlayer()
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pauseAudioPlayer

暂停音频渲染，支持淡出效果。暂停期间远端音频数据仍会到达但不播放。

```
public abstract int pauseAudioPlayer(int fadeMs)
```

参数

类型

说明

fadeMs

int

淡出时长（毫秒）；0 表示立即暂停

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### resumeAudioPlayer

恢复音频渲染，支持淡入效果。需在 pauseAudioPlayer 之后调用。

```
public abstract int resumeAudioPlayer(int fadeMs)
```

参数

类型

说明

fadeMs

int

淡入时长（毫秒）；0 表示立即恢复

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### interruptAudioPlayer

打断本轮音频通话，清空当前播放缓冲区。常用于 AI 对话场景下用户打断 AI 说话。

```
public abstract int interruptAudioPlayer(@NonNull AoqTrackType trackType, int fadeMs)
```

参数

类型

说明

trackType

AoqTrackType

需要打断的轨道类型

fadeMs

int

淡出时长（毫秒）；0 表示立即打断

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### enableSpeakerphone

切换音频输出到扬声器或听筒。仅在 startAudioPlayer 之后生效。

```
public abstract int enableSpeakerphone(boolean enable)
```

参数

类型

说明

enable

boolean

true 表示切换到扬声器；false 表示切换到听筒

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECAudioDeviceEarpieceRequiresVoipMode 表示听筒需要 VoIP 模式）。

**说明**切换到听筒需要 AoqAudioPlaybackConfig.isVoipMode=true；路由变化通过 onAudioDeviceRouteChanged 回调通知。

#### isSpeakerphoneEnabled

查询当前是否使用扬声器输出。

```
public abstract boolean isSpeakerphoneEnabled()
```

参数：无。

返回值：true 表示当前使用扬声器；false 表示当前使用听筒或其他路由。

### 音频编码配置

#### setAudioEncoderConfig

设置音频编码参数，用于上行推流的音频编码。配置变更会立即生效。

```
public abstract int setAudioEncoderConfig(@NonNull AoqAudioCodecConfig config)
```

参数

类型

说明

config

AoqAudioCodecConfig

音频编码配置；trackType 应设为 AoqTrackTypeAudio

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECParamInvalid 表示参数非法）。

**说明**codecType 决定编码格式（默认 Opus），sampleRate 与 channel 需与采集端匹配；bitrate 仅在 Opus 等有损编码下生效。

#### setAudioDecoderConfig

设置音频解码参数，用于下行拉流的音频解码。需与远端编码参数匹配。

```
public abstract int setAudioDecoderConfig(@NonNull AoqAudioCodecConfig config)
```

参数

类型

说明

config

AoqAudioCodecConfig

音频解码配置；trackType 应设为 AoqTrackTypeAudio

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**sampleRate 需与远端编码器输出采样率一致，否则可能触发解码错误或音质异常。

### 音频文件播放

#### startAudioFile

开始推流播放本地音频文件。可同时推流到远端和本地播放，音量分别由 publishVolume 和 playoutVolume 控制。

```
public abstract int startAudioFile(@NonNull String fileId, @NonNull AoqAudioFileMixConfig config)
```

参数

类型

说明

fileId

String

文件标识符，业务方自定义，用于后续控制

config

AoqAudioFileMixConfig

音频文件播放配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**播放状态变化通过 onAudioFileState 回调通知；同一 fileId 重复调用会覆盖之前的播放。

#### stopAudioFile

停止音频文件播放。

```
public abstract int stopAudioFile(@NonNull String fileId)
```

参数

类型

说明

fileId

String

文件标识符，与 startAudioFile 传入的一致

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pauseAudioFile

暂停音频文件播放。

```
public abstract int pauseAudioFile(@NonNull String fileId)
```

参数

类型

说明

fileId

String

文件标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### resumeAudioFile

恢复音频文件播放。需在 pauseAudioFile 之后调用。

```
public abstract int resumeAudioFile(@NonNull String fileId)
```

参数

类型

说明

fileId

String

文件标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioFileDuration

获取音频文件总时长。

```
public abstract long getAudioFileDuration(@NonNull String fileId)
```

参数

类型

说明

fileId

String

文件标识符

返回值：文件总时长（毫秒）；文件未加载或不存在时返回 0。

#### getAudioFileCurrentPosition

获取音频文件当前播放位置。

```
public abstract long getAudioFileCurrentPosition(@NonNull String fileId)
```

参数

类型

说明

fileId

String

文件标识符

返回值：当前播放位置（毫秒）；文件未加载或不存在时返回 0。

#### setAudioFilePositionMillis

设置音频文件播放位置（seek）。

```
public abstract int setAudioFilePositionMillis(@NonNull String fileId, long positionMillis)
```

参数

类型

说明

fileId

String

文件标识符

positionMillis

long

目标播放位置（毫秒）

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### setAudioFileVolume

设置音频文件音量，可分别控制推流音量和本地播放音量。

```
public abstract int setAudioFileVolume(@NonNull String fileId, @NonNull AoqAudioStreamDirection type, int volume)
```

参数

类型

说明

fileId

String

文件标识符

type

AoqAudioStreamDirection

音量方向；AoqAudioStreamPublish 推流，AoqAudioStreamPlayout 播放

volume

int

音量值，取值范围 \[0-100\]

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioFileVolume

获取音频文件当前音量。

```
public abstract int getAudioFileVolume(@NonNull String fileId, @NonNull AoqAudioStreamDirection type)
```

参数

类型

说明

fileId

String

文件标识符

type

AoqAudioStreamDirection

音量方向

返回值：当前音量值 \[0-100\]；文件不存在时返回 0。

### 外部音频流

#### addAudioExternalStream

新增一条外部音频流。可创建多条独立的外部流，通过 streamId 区分。

```
public abstract int addAudioExternalStream(@NonNull String streamId, @NonNull AoqAudioExternalStreamConfig config)
```

参数

类型

说明

streamId

String

外部流标识符，业务方自定义

config

AoqAudioExternalStreamConfig

外部音频流配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pushAudioExternalStreamData

输入外部音频 PCM 数据到指定流。

```
public abstract int pushAudioExternalStreamData(@NonNull String streamId, @NonNull AoqAudioFrameData data)
```

参数

类型

说明

streamId

String

外部流标识符

data

AoqAudioFrameData

PCM 音频帧数据

返回值：0 表示调用成功；非 0 表示失败。缓冲区满时返回 AoqECAudioExternalBufferFull(110)。 data 仅在调用期间有效，SDK 内部会拷贝；采样率/声道数需与 addAudioExternalStream 时的配置一致。

#### setAudioExternalStreamVolume

设置外部音频流音量，可分别控制推流音量和本地播放音量。

```
public abstract int setAudioExternalStreamVolume(@NonNull String streamId, @NonNull AoqAudioStreamDirection type, int volume)
```

参数

类型

说明

streamId

String

外部流标识符

type

AoqAudioStreamDirection

音量方向

volume

int

音量值，取值范围 \[0-100\]

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioExternalStreamVolume

获取外部音频流当前音量。

```
public abstract int getAudioExternalStreamVolume(@NonNull String streamId, @NonNull AoqAudioStreamDirection type)
```

参数

类型

说明

streamId

String

外部流标识符

type

AoqAudioStreamDirection

音量方向

返回值：当前音量值 \[0-100\]；流不存在时返回 0。

#### clearAudioExternalStreamBuffer

清空外部音频流缓存，支持淡出效果。常用于打断当前播放内容。

```
public abstract void clearAudioExternalStreamBuffer(@NonNull String streamId, int fadeoutMs)
```

参数

类型

说明

streamId

String

外部流标识符

fadeoutMs

int

淡出时长（毫秒）；-1 表示使用默认值，0 表示立即清空，>0 表示保留指定毫秒数淡出

返回值：无（void）。

**说明**pushAudioExternalStreamData 缓冲区满时返回 AoqECAudioExternalBufferFull(110)，建议 Sleep 30ms 后重试。

#### removeAudioExternalStream

移除外部音频流，释放相关资源。

```
public abstract int removeAudioExternalStream(@NonNull String streamId)
```

参数

类型

说明

streamId

String

外部流标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

### 音频帧回调

#### setAudioFrameObserver

设置音频帧数据回调监听。传入 listener=null 表示移除监听。

```
public abstract int setAudioFrameObserver(@Nullable AoqClientListener.AoqAudioFrameListener listener)
```

参数

类型

说明

listener

AoqAudioFrameListener

音频帧监听接口；传 null 表示移除

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需先调用本接口设置 listener，再通过 enableAudioFrameObserver 开启具体位置的回调。

#### enableAudioFrameObserver

开启或关闭指定位置的音频帧回调。

```
public abstract int enableAudioFrameObserver(boolean enabled, @NonNull AoqAudioSource audioSource, @NonNull AoqAudioObserverConfig config)
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

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。 回调数据仅在回调期间有效，异步使用需自行拷贝。

### 本地音量提示

#### enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示。开启后 SDK 按 config.interval 周期触发 onLocalAudioVolumeIndication 回调，上报本地采集音量及是否人声。

```
public abstract int enableLocalAudioVolumeIndication(@NonNull AoqAudioVolumeIndicationConfig config)
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

打开视频采集设备（摄像头），采集内容通过 AoqTrackTypeVideo 通道发送。若使用外部视频输入（pushExternalVideoCapturedFrame），需将 isExternal 设为 true，此时不会真正打开摄像头。

```
public abstract int startVideoCapture(@NonNull AoqVideoCaptureConfig config)
```

参数

类型

说明

config

AoqVideoCaptureConfig

视频采集配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECVideoDeviceCameraAuthFailed 表示摄像头权限未获取）。

**说明**Android 需在调用前申请 CAMERA 权限；设备状态变化通过 onVideoDeviceStateChanged 回调通知。

#### stopVideoCapture

关闭视频采集设备，停止本地视频采集。

```
public abstract int stopVideoCapture()
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### switchCamera

切换前后置摄像头。需在 startVideoCapture(isExternal=false) 之后调用。

```
public abstract int switchCamera(@NonNull AoqCameraDirection direction)
```

参数

类型

说明

direction

AoqCameraDirection

目标摄像头方向；AoqCameraDirectionFront 前置，AoqCameraDirectionBack 后置

返回值：0 表示调用成功；< 0 表示失败（对应 AoqErrorCode）。

**说明**外部采集模式（isExternal=true）下调用无效。

#### setLocalView

设置或移除本地视频渲染窗口。传入 canvas=null 或 canvas.view=null 表示移除渲染。

```
public abstract int setLocalView(@NonNull AoqTrackType trackType, @Nullable AoqVideoCanvas canvas)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型

canvas

AoqVideoCanvas

视频渲染画布；传 null 表示移除渲染

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### setRemoteView

设置或移除远端视频渲染窗口。传入 canvas=null 或 canvas.view=null 表示解绑。

```
public abstract int setRemoteView(@NonNull AoqTrackType trackType, @Nullable AoqVideoCanvas canvas)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型

canvas

AoqVideoCanvas

视频渲染画布；传 null 表示解绑

返回值：0 表示调用成功；非 0 表示失败。trackType 为 AoqTrackTypeScreen 时返回 AoqECUnSupport，窗口不会绑定。

**说明**Screen track 当前仅支持上行，没有远端画面可渲染，因此 trackType 不能传入 AoqTrackTypeScreen。

### 视频编码与外部输入

#### setVideoEncoderConfig

设置视频编码参数，用于上行推流的视频编码。若 isExternal=true，SDK 不做二次编码，由 pushExternalVideoEncodedFrame 按 trackType 直推已编码帧。

```
public abstract int setVideoEncoderConfig(@NonNull AoqVideoCodecConfig config)
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

设置视频解码参数，用于下行拉流的视频解码，按 config.trackType 路由。

仅以下字段生效：`trackType`, `codecType`, `width`, `height`, `fps`, `bitrate`。其余字段仅用于编码。

```
public abstract int setVideoDecoderConfig(@NonNull AoqVideoCodecConfig config)
```

参数

类型

说明

config

AoqVideoCodecConfig

视频解码配置

返回值：0 表示调用成功；非 0 表示失败。config.trackType 为 AoqTrackTypeScreen 时返回 AoqECUnSupport，配置不会下发。

**说明**Screen track 当前仅支持上行，没有下行订阅，因此 config.trackType 不能传入 AoqTrackTypeScreen。

#### pushExternalVideoCapturedFrame

推送外部原始视频帧，SDK 编码后发送。按 trackType 路由，对应通道需已开启外部采集。

```
public abstract int pushExternalVideoCapturedFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrame frame)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型；AoqTrackTypeVideo 需先 startVideoCapture(isExternal=true)，AoqTrackTypeScreen 需先 startScreenCapture(isExternal=true)

frame

AoqVideoFrame

外部视频帧数据

返回值：0 表示调用成功；对应通道未开启外部采集返回 AoqECVideoExternalCaptureNotEnabled(211)；< 0 表示失败。 帧数据仅在调用期间有效，SDK 内部会拷贝。

#### pushExternalVideoEncodedFrame

推送外部已编码视频帧（SDK 不做二次编码，直接打包发送）。仅当对应 trackType 已 setVideoEncoderConfig(isExternal=true) 后才消费，不依赖 startVideoCapture/startScreenCapture。

```
public abstract int pushExternalVideoEncodedFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoEncodedFrame frame)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型

frame

AoqVideoEncodedFrame

外部已编码视频帧

返回值：0 表示调用成功；对应通道未开启外部编码返回 AoqECVideoExternalEncoderNotEnabled(212)；< 0 表示失败。

**说明**frame.timeStamp 直接透传，SDK 不做补齐；调用方需自行保证时间戳单调递增。

**说明**pushExternalVideoCapturedFrame Video 轨道需先调用 startVideoCapture(isExternal=true)，Screen 轨道需先调用 startScreenCapture(isExternal=true)。若缓冲区满返回 AoqECVideoExternalBufferFull(210)。

### 屏幕采集

```
public abstract int startScreenCapture(@NonNull AoqScreenCaptureConfig config)
public abstract int stopScreenCapture()
```

`trackType` 支持 `AoqTrackTypeAudio`、`AoqTrackTypeVideo` 和 `AoqTrackTypeScreen`。

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

启动返回 0 表示请求已受理，最终状态通过 `onScreenCaptureStateChanged` 通知；非 0 表示同步拒绝。停止返回 0 表示成功，非 0 表示失败，停止结果由该回调通知。

`isExternal=false` 时通过 MediaProjection 采集；重复启动返回 `AoqECStateInvalid`，停止可重复调用。

外部原始帧：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`；不需要调用 `startScreenCapture`。

### 媒体流发送控制

#### enableSendMediaStream

控制本地媒体流的发送开关，按 trackType 路由。关闭时 SDK 仍采集/编码但不发送到网络。

```
public abstract int enableSendMediaStream(@NonNull AoqTrackType trackType, boolean enable)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型；支持 AoqTrackTypeAudio/AoqTrackTypeVideo/AoqTrackTypeScreen

enable

boolean

true 表示开启发送；false 表示关闭发送

返回值：0 表示调用成功；< 0 表示失败（对应 AoqErrorCode）。

**说明**建议初始化后先 enableSendMediaStream(false)，待 onConnectionStatusChange 收到 Connected 后再开启，避免连接建立前的数据丢失。

### 视频帧回调

#### setVideoFrameObserver

设置视频帧数据回调监听。传入 listener=null 表示移除监听。

```
public abstract int setVideoFrameObserver(@Nullable AoqClientListener.AoqVideoFrameListener listener)
```

参数

类型

说明

listener

AoqVideoFrameListener

视频帧监听接口；传 null 表示移除

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需先调用本接口设置 listener，再通过 enableVideoFrameObserver 开启具体位置的回调。

#### enableVideoFrameObserver

开启或关闭指定位置的视频帧回调。

```
public abstract int enableVideoFrameObserver(boolean enabled, @NonNull AoqVideoSource videoSource, @NonNull AoqVideoObserverConfig config)
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

**说明**回调线程为 SDK 内部线程，禁止在回调中执行耗时操作；仅 I420 格式支持读写模式（mode=ReadWrite），其他格式只读。

### 实时消息

#### sendDataMsg

发送实时数据消息到远端。需在 connect 成功且 enableSendMediaStream(Data, true) 之后调用。

```
public abstract int sendDataMsg(@NonNull AoqDataMsg msg)
```

参数

类型

说明

msg

AoqDataMsg

数据消息

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**远端通过 onDataMsg 回调接收；消息大小受 SDK 内部限制，超大消息建议分片发送。

### AoqClientListener 回调

#### onError

引擎错误回调。发生不可恢复错误时触发。

```
public void onError(int code, String message)
```

参数

类型

说明

code

int

错误码，对应 AoqErrorCode 枚举值

message

String

错误描述信息

返回值：无（void）。

#### onWarning

引擎警告回调。发生可恢复异常时触发，不影响 SDK 继续运行。

```
public void onWarning(int code, String message)
```

参数

类型

说明

code

int

警告码，对应 AoqWarningCode 枚举值

message

String

警告描述信息

返回值：无（void）。

#### onConnectionStatusChange

连接状态变化回调。状态流转：Disconnected -> Connecting -> Connected/Failed -> Disconnected。

```
public void onConnectionStatusChange(@NonNull AoqClientEngine.AoqConnectionStatus status)
```

参数

类型

说明

status

AoqConnectionStatus

当前连接状态

返回值：无（void）。

**说明**收到 Connected 后再调用 enableSendMediaStream(true) 开启媒体流发送。

#### onStats

引擎统计信息回调。SDK 周期性上报音视频推拉流及网络统计数据，可用于实时监控通话质量、网络状态、诊断音视频问题。

```
public void onStats(@NonNull AoqClientEngine.AoqStats stats)
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
public void onAudioDeviceStateChanged(@NonNull AoqClientEngine.AoqAudioDeviceState state)
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
public void onAudioDeviceRouteChanged(int routeType)
```

参数

类型

说明

routeType

int

当前音频输出路由，对应 AoqAudioDeviceRouteType 枚举值

返回值：无（void）。

#### onAudioDeviceInterrupted

音频设备中断回调。系统级中断（如来电、其他 App 抢占音频焦点）时触发。

```
public void onAudioDeviceInterrupted(boolean interrupt)
```

参数

类型

说明

interrupt

boolean

true 表示被中断；false 表示中断恢复

返回值：无（void）。

#### onScreenCaptureStateChanged

屏幕采集状态变化回调。使用 AoqScreenCaptureStateCode 与统一的 AoqErrorCode，在 Android 主线程按顺序通知。

```
public void onScreenCaptureStateChanged(@NonNull AoqClientEngine.AoqScreenCaptureState state)
```

参数

类型

说明

state

AoqScreenCaptureState

屏幕采集状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

**说明**Started 表示采集/外部输入已就绪，不表示媒体已发送；Fail 和 Stopped 均为清理完成后的终态；采集失败仅通过本回调报告。

#### onVideoDeviceStateChanged

视频设备采集操作状态变化回调。

```
public void onVideoDeviceStateChanged(@NonNull AoqClientEngine.AoqVideoDeviceState state)
```

参数

类型

说明

state

AoqVideoDeviceState

视频设备状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

#### onAudioDeviceFocusChanged

音频焦点变化回调。

```
public void onAudioDeviceFocusChanged(int audioFocus)
```

参数

类型

说明

audioFocus

int

Android AUDIOFOCUS\_\* 常量（AUDIOFOCUS\_GAIN/AUDIOFOCUS\_LOSS/AUDIOFOCUS\_LOSS\_TRANSIENT 等）

返回值：无（void）。

#### onAudioFileState

音频文件播放状态回调。

```
public void onAudioFileState(@NonNull AoqClientEngine.AoqAudioFileState state)
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
public void onLocalAudioVolumeIndication(@NonNull AoqClientEngine.AoqAudioVolume volume)
```

参数

类型

说明

volume

AoqAudioVolume

本地音量信息；包含 isSpeech（是否人声）和 volume（平滑后瞬时音量 \[0-255\]）

返回值：无（void）。

AoqClientListener 是 SDK 所有异步事件通知的统一出口。所有回调方法都带有默认空实现，无需强制重写不关心的方法。

#### onDataMsg

收到实时数据消息回调。

```
public void onDataMsg(@NonNull AoqClientEngine.AoqDataMsg msg)
```

参数

类型

说明

msg

AoqDataMsg

数据消息

返回值：无（void）。 消息数据仅在回调期间有效，异步使用需自行拷贝。

### AoqAudioFrameListener 回调

音频帧数据监听接口。所有方法均为 default 空实现，按需重写。

```
public interface AoqAudioFrameListener {
    default void onCapturedAudioFrame(@NonNull AoqAudioFrameData frame) {}
    default void onProcessCapturedAudioFrame(@NonNull AoqAudioFrameData frame) {}
    default void onPublishAudioFrame(@NonNull AoqTrackType trackType, @NonNull AoqAudioFrameData frame) {}
    default void onPlaybackAudioFrame(@NonNull AoqAudioFrameData frame) {}
}
```

方法

触发时机

参数

onCapturedAudioFrame

采集到原始音频帧时

frame: AoqAudioFrameData

onProcessCapturedAudioFrame

3A 处理后的音频帧

frame: AoqAudioFrameData

onPublishAudioFrame

推流前的音频帧

trackType: 轨道类型；frame: AoqAudioFrameData

onPlaybackAudioFrame

播放前的远端音频帧

frame: AoqAudioFrameData

返回值：无（void）。 帧数据仅在回调期间有效。

#### onCapturedAudioFrame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

```
void onCapturedAudioFrame(@NonNull AoqAudioFrameData frame)
```

参数

类型

说明

frame

AoqAudioFrameData

采集的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onProcessCapturedAudioFrame

3A 处理后的音频帧触发。数据已经过回声消除、降噪等处理。

```
void onProcessCapturedAudioFrame(@NonNull AoqAudioFrameData frame)
```

参数

类型

说明

frame

AoqAudioFrameData

3A 处理后的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onPublishAudioFrame

推流前的音频帧触发。数据为最终编码发送前的音频。

```
void onPublishAudioFrame(@NonNull AoqTrackType trackType, @NonNull AoqAudioFrameData frame)
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

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onPlaybackAudioFrame

播放前的远端音频帧触发。数据为解码后、混音后待播放的音频。

```
void onPlaybackAudioFrame(@NonNull AoqAudioFrameData frame)
```

参数

类型

说明

frame

AoqAudioFrameData

播放前的远端音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

### AoqVideoFrameListener 回调

视频帧数据监听接口。所有方法均为 default 实现，返回 false 表示不修改数据。三个回调均带 trackType 参数，用于区分 Video / Screen 轨道。

```
public interface AoqVideoFrameListener {
    default boolean onCapturedVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame) { return false; }
    default boolean onPreEncodeVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame) { return false; }
    default boolean onRemoteVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame) { return false; }
}
```

方法

触发时机

参数

onCapturedVideoFrame

采集到原始视频帧时（前处理前）

trackType: 轨道类型；frame: AoqVideoFrameData

onPreEncodeVideoFrame

编码前的视频帧（前处理后）

trackType: 轨道类型；frame: AoqVideoFrameData

onRemoteVideoFrame

远端解码后、渲染前的视频帧

trackType: 轨道类型；frame: AoqVideoFrameData

返回值：boolean。返回 true 表示数据已修改需写回 SDK（仅 I420 格式写回生效）；返回 false 表示不修改。

**说明**通过 enableVideoFrameObserver 开启对应 AoqVideoSource 后才会触发；frame.data 与 textureId 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。

```
boolean onCapturedVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型(Video/Screen)

frame

AoqVideoFrameData

采集的视频帧数据

返回值：boolean。true 表示数据已修改需写回 SDK（仅 I420 格式写回生效），false 表示不修改。

**说明**通过 enableVideoFrameObserver 开启对应 AoqVideoSource 后才会触发；frame.data 与 textureId 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onPreEncodeVideoFrame

编码前的视频帧触发（前处理后）。

```
boolean onPreEncodeVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型(Video/Screen)

frame

AoqVideoFrameData

编码前的视频帧数据

返回值：boolean。true 表示数据已修改需写回 SDK（仅 I420 格式写回生效），false 表示不修改。

**说明**通过 enableVideoFrameObserver 开启对应 AoqVideoSource 后才会触发；frame.data 与 textureId 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onRemoteVideoFrame

远端解码后、渲染前的视频帧触发。

```
boolean onRemoteVideoFrame(@NonNull AoqTrackType trackType, @NonNull AoqVideoFrameData frame)
```

参数

类型

说明

trackType

AoqTrackType

轨道类型(Video/Screen)

frame

AoqVideoFrameData

远端解码后的视频帧数据

返回值：boolean。true 表示数据已修改需写回 SDK（仅 I420 格式写回生效），false 表示不修改。

**说明**通过 enableVideoFrameObserver 开启对应 AoqVideoSource 后才会触发；frame.data 与 textureId 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

## 数据类型与枚举

### 通用类型

#### AoqRelayEndpoint

Relay 接入点。

字段

类型

默认值

说明

routeIndex

int

\-1

路由索引

endpoint

String

""

Relay 服务器域名或 IP

port

int

0

Relay 服务器 UDP 端口

tcpPort

int

0

Relay 服务器 TCP 端口

#### AoqTrackParam

Track 属性。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeAudio

轨道类型

trackMode

AoqTrackMode

AoqTrackModeSegment

流式与非流式模式，仅对音频下行生效

#### AoqTrackParam.trackMode

字段

类型

默认值

说明

trackMode

AoqTrackMode

AoqTrackModeSegment

仅对音频下行生效。

**AoqCreateConfig**

**字段**

**类型**

**默认值**

**说明**

workDir

String

""

SDK 工作目录

isBTScoMode

boolean

false

true 蓝牙 SCO 模式；false A2DP 模式

enableDumpAudio

boolean

false

是否开启音频 dump（调试用）

extras

String

""

扩展参数字符串

maxEncodedVideoFrameBytes

int

190 × 1024

编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。

enableDropOversizedVideoFrame

boolean

false

仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。

**AoqConnectConfig**

`subscribeTracks` 不能包含 `AoqTrackTypeScreen`，否则 `connect` 返回 `AoqECUnSupport`，不发起连接。`setRemoteView` 不支持 Screen，传入时返回 `AoqECUnSupport`。

**字段**

**类型**

**默认值**

**说明**

token

String

""

连接鉴权 Token

sid

String

""

会话 ID

certFingerprint

String

""

服务器证书指纹

relayEndpoints

List<AoqRelayEndpoint>

空

Relay 接入点列表

workspaceIdHash

String

""

工作空间 ID Hash

publishTracks

List<AoqTrackParam>

空

本端发布轨道列表

subscribeTracks

List<AoqTrackParam>

空

本端订阅轨道列表

### 统计信息类型

**AoqNetworkStats**

**字段**

**类型**

**说明**

sendBitrate

int

发送码率（bps）

sendBytes

long

累计发送字节数

recvBitrate

int

接收码率（bps）

recvBytes

long

累计接收字节数

loss

int

丢包率（0-100）

rtt

int

往返延迟（ms）

#### AoqStats

引擎统计信息汇总。SDK 通过 onStats 回调周期性上报。所有字段均可能为 null。

字段

类型

说明

audioPublishStats

AoqAudioPublishStats 数组

音频推流统计数组（@Nullable）

videoPublishStats

AoqVideoPublishStats 数组

视频推流统计数组（@Nullable）

dataMsgPublishStats

AoqDataMsgPublishStats 数组

数据消息推流统计数组（@Nullable）

audioSubscribeStats

AoqAudioSubscribeStats 数组

音频拉流统计数组（@Nullable）

videoSubscribeStats

AoqVideoSubscribeStats 数组

视频拉流统计数组（@Nullable）

dataMsgSubscribeStats

AoqDataMsgSubscribeStats 数组

数据消息拉流统计数组（@Nullable）

networkStats

AoqNetworkStats

网络统计信息（@Nullable）

#### AoqAudioPublishStats

音频推流统计。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeAudio

轨道类型

bitrate

int

0

码率（bps）

bytes

long

0

累计发送字节数

encodeVolume

int

0

推流编码音量

#### AoqVideoPublishStats

视频推流统计。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeVideo

轨道类型

bitrate

int

0

码率（bps）

bytes

long

0

累计发送字节数

encodeFps

int

0

编码帧率

#### AoqDataMsgPublishStats

数据消息推流统计。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeData

轨道类型

bitrate

int

0

码率（bps）

bytes

long

0

累计发送字节数

#### AoqAudioSubscribeStats

音频拉流统计。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeAudio

轨道类型

bitrate

int

0

码率（bps）

bytes

long

0

累计接收字节数

playVolume

int

0

播放音量

#### AoqVideoSubscribeStats

视频拉流统计。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeVideo

轨道类型

bitrate

int

0

码率（bps）

bytes

long

0

累计接收字节数

decodeFps

int

0

解码帧率

renderFps

int

0

渲染帧率

#### AoqDataMsgSubscribeStats

数据消息拉流统计。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeData

轨道类型

bitrate

int

0

码率（bps）

bytes

long

0

累计接收字节数

### 枚举类型

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

**AoqErrorCode**

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

听筒需要 VoIP 模式

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

外部视频编码未启用

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

**AoqWarningCode**

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

**AoqTrackType**

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

**AoqEncoderType**

**枚举值**

**值**

**说明**

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

**AoqConnectionStatus**

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

视频方向。

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

**AoqAudioCaptureConfig**

**字段**

**类型**

**默认值**

**说明**

isExternal

boolean

false

是否为外部采集模式

isVoipMode

boolean

false

是否启用 VoIP 模式（影响设备路由，如听筒）

channel

int

1

声道数（默认单声道）

**AoqAudioPlaybackConfig**

**字段**

**类型**

**默认值**

**说明**

isVoipMode

boolean

false

是否启用 VoIP 模式（硬件 AEC），移动端有效

isDefaultSpeaker

boolean

true

是否默认扬声器，移动端有效

isExternal

boolean

false

是否为外部播放模式

channel

int

1

声道数（默认单声道）

**AoqAudioCodecConfig**

**字段**

**类型**

**默认值**

**说明**

trackType

AoqTrackType

Audio

轨道类型

codecType

AoqEncoderType

AudioOpus

编码格式

sampleRate

int

48000

采样率（Hz）

channel

int

1

声道数

bitrate

int

32000

比特率（bps）

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

音频设备采集播放操作状态。

字段

类型

默认值

说明

state

AoqAudioDeviceStateCode

AoqAudioDeviceNone

设备操作状态

reason

int

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

音频文件播放配置。

字段

类型

默认值

说明

fileName

String

""

文件名（含路径），非空

cycles

int

\-1

循环次数，-1 表示无限循环

startPosMs

long

0

起始播放位置（毫秒）

publishVolume

int

100

推流音量，取值范围 \[0-100\]

playoutVolume

int

100

播放音量，取值范围 \[0-100\]

#### AoqAudioFileStateCode

音频文件播放状态码。

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

音频文件播放错误码。

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

String

""

文件标识符

stateCode

AoqAudioFileStateCode

AoqAudioFileNone

文件播放状态码

errorCode

AoqAudioFileErrorCode

AoqAudioFileNoError

文件错误码

### 外部音频流与音量类型

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

#### AoqAudioFrameData

外部音频帧数据。

字段

类型

默认值

说明

dataPtr

byte 数组

null

音频 PCM 裸数据（@Nullable）

dataSize

int

0

PCM 数据字节数

numOfSamples

int

0

采样点数（单声道）

bytesPerSample

int

0

每个采样点的字节数

numOfChannels

int

0

声道数

samplesPerSec

int

0

每秒采样点数（采样率）

pushSequence

int

0

PCM 输入轮次

timeStamp

long

0

时间戳

autoGenMute

boolean

false

数据回调有效，true 表示 SDK 生成的静音数据

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

读写模式

#### AoqAudioObserverConfig

音频帧回调配置。

字段

类型

默认值

说明

sampleRate

int

48000

回调音频采样率（Hz）

channels

int

1

回调音频声道数

mode

AoqAudioObserverMode

AoqAudioObserverModeReadOnly

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

int

0

回调间隔（毫秒）；小于等于 0 时关闭，大于 0 且小于 10 时按 10 处理。

smooth

int

3

平滑系数，范围 0～10；越大越平滑。

#### AoqAudioVolume

字段

类型

默认值

说明

isSpeech

boolean

false

是否为人声。

volume

int

0

平滑后的瞬时音量，范围 0～255。

### 视频类型

#### AoqRenderMode

渲染显示模式。

枚举值

值

说明

AoqRenderModeAuto

0

自适应模式

AoqRenderModeStretch

1

拉伸模式

AoqRenderModeFill

2

填充模式

AoqRenderModeCrop

3

裁剪模式

#### AoqVideoCanvas

视频渲染画布。

字段

类型

默认值

说明

view

View

null

渲染显示的 Android View（@Nullable）

renderMode

AoqRenderMode

AoqRenderModeAuto

渲染模式

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

#### AoqScreenCaptureConfig

字段

类型

默认值

说明

isExternal

boolean

false

是否由应用提供屏幕原始帧。

mediaProjectionIntent

Intent

null

已有 MediaProjection 授权时传入；null 由 SDK 申请。外部采集时无效。

notificationFactory

AoqScreenShareNotificationFactory

null

前台服务通知工厂；null 使用默认通知。外部采集时无效。

**AoqVideoCaptureConfig**

**字段**

**类型**

**默认值**

**说明**

width

int

1280

采集宽度（像素），isExternal=true 时无效

height

int

720

采集高度（像素），isExternal=true 时无效

fps

int

15

采集帧率，isExternal=true 时无效

isExternal

boolean

false

是否外部采集，true 时不打开摄像头

cameraDirection

AoqCameraDirection

Front

摄像头方向，isExternal=true 时无效

**AoqVideoCodecConfig**

**字段**

**类型**

**默认值**

**说明**

trackType

AoqTrackType

Video

轨道类型

codecType

AoqEncoderType

VideoH264

编码格式

width

int

540

编码宽度（像素）

height

int

960

编码高度（像素）

fps

int

5

编码帧率

bitrate

int

500000

目标比特率（bps）

minBitrate

int

128000

最小比特率（bps）

keyframeInterval

int

2

关键帧间隔（秒）

mirrorMode

AoqMirrorMode

Disabled

镜像模式

orientationMode

AoqOrientationMode

Auto

视频方向模式

isExternal

boolean

false

true 时 SDK 不做二次编码，由 pushExternalVideoEncodedFrame 直推

**AoqVideoPixelFormat**

**枚举值**

**值**

**说明**

AoqVideoPixelFormatUnknown

0

未知格式

AoqVideoPixelFormatI420

1

I420（YUV 三平面格式）

AoqVideoPixelFormatNV12

2

NV12（YUV 半平面格式）

AoqVideoPixelFormatNV21

3

NV21（YUV 半平面格式）

AoqVideoPixelFormatBGRA

4

BGRA（32 位）

AoqVideoPixelFormatRGBA

5

RGBA（32 位）

AoqVideoPixelFormatTextureOES

7

外部 OES 纹理

AoqVideoPixelFormatTexture2D

8

普通 2D 纹理

#### AoqVideoFrame

外部视频数据。

字段

类型

默认值

说明

format

AoqVideoPixelFormat

AoqVideoPixelFormatUnknown

像素格式

width

int

0

视频宽度（像素）

height

int

0

视频高度（像素）

data

byte 数组

null

打包格式数据（NV12/NV21/BGRA/RGBA）（@Nullable）

dataY

byte 数组

null

I420 Y 平面数据（@Nullable）

dataU

byte 数组

null

I420 U 平面数据（@Nullable）

dataV

byte 数组

null

I420 V 平面数据（@Nullable）

strideY

int

0

Y 平面行跨度

strideU

int

0

U 平面行跨度

strideV

int

0

V 平面行跨度

textureId

int

0

纹理 ID（TEXTURE\_OES/TEXTURE\_2D 时有效）

transformMatrix

float 数组

null

4×4 行优先纹理变换矩阵（@Nullable）

eglContext

EGLContext

null

共享 EGL context（@Nullable）

timeStamp

long

0

时间戳（毫秒）；0 时 SDK 用本地时钟补齐

#### AoqVideoCodecType

外部编码帧 codec 类型。

枚举值

值

说明

AoqVideoCodecTypeJPEG

0

JPEG 编码

#### AoqVideoEncodedFrame

外部已编码视频帧。调用方自行完成编码，SDK 不做二次编码，直接打包发送。

字段

类型

默认值

说明

codec

AoqVideoCodecType

AoqVideoCodecTypeJPEG

编码格式

data

byte 数组

null

编码后数据（@Nullable）

width

int

0

宽度（像素）

height

int

0

高度（像素）

timeStamp

long

0

时间戳（毫秒）；0 时 SDK 用本地时钟补齐

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

采集启动中

AoqVideoDeviceCaptureStarted

2

采集已启动

AoqVideoDeviceCaptureStopping

3

采集停止中

AoqVideoDeviceCaptureStopped

4

采集已停止

AoqVideoDeviceCaptureFail

5

采集失败

#### AoqVideoDeviceState

视频设备采集操作状态。

字段

类型

默认值

说明

state

AoqVideoDeviceStateCode

AoqVideoDeviceNone

设备采集操作状态

reason

int

0

错误原因代码（参考 AoqErrorCode）

**AoqAudioExternalStreamConfig**

**字段**

**类型**

**默认值**

**说明**

trackType

AoqTrackType

Audio

音频轨道类型

codecType

AoqEncoderType

AudioPCM

音频流格式

channels

int

1

声道数

sampleRate

int

48000

采样率（Hz）

playoutVolume

int

100

播放音量 \[0-100\]

publishVolume

int

100

推流音量 \[0-100\]

maxBufferDuration

int

1000

最大缓冲时长（毫秒）

enable3A

boolean

false

是否对输入 PCM 进行 3A 处理

**AoqAudioStreamDirection**

**枚举值**

**值**

**说明**

AoqAudioStreamPublish

0

发布流（推流）

AoqAudioStreamPlayout

1

播放流（拉流）

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

AoqScreenCaptureNone

屏幕采集状态。

reason

int

0

正常为 0；失败时为 AoqErrorCode 错误码。

#### AoqScreenShareNotificationFactory

```
public interface AoqScreenShareNotificationFactory {
    @Nullable Notification createNotification(@NonNull Context serviceContext);
}
```

返回 null 使用 SDK 默认通知。自定义通知关联的 NotificationChannel 必须先通过 `createNotificationChannel` 创建，否则前台服务启动失败。

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

读写模式

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

视频帧回调配置。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeVideo

需要观察的视频轨道；仅支持 Video / Screen

format

AoqVideoPixelFormat

AoqVideoPixelFormatI420

期望回调像素格式

alignment

AoqVideoObserverAlignment

AoqVideoObserverAlignmentDefault

宽度对齐策略

mode

AoqVideoObserverMode

AoqVideoObserverModeReadOnly

读写模式，仅 I420 支持读写

mirrorApplied

boolean

false

是否对回调数据应用镜像

#### AoqVideoFrameData

视频帧回调数据。byte/texture 字段引用 SDK 内部内存，仅回调期间有效；异步使用请自行拷贝。

字段

类型

默认值

说明

format

AoqVideoPixelFormat

AoqVideoPixelFormatUnknown

像素格式

width

int

0

宽度（像素）

height

int

0

高度（像素）

data

ByteBuffer

null

打包格式数据（NV12/NV21/BGRA/RGBA）；direct ByteBuffer 引用 native 内存（@Nullable）

dataY

ByteBuffer

null

I420 Y 平面（@Nullable）

dataU

ByteBuffer

null

I420 U 平面（@Nullable）

dataV

ByteBuffer

null

I420 V 平面（@Nullable）

strideY

int

0

Y 平面行跨度

strideU

int

0

U 平面行跨度

strideV

int

0

V 平面行跨度

textureId

int

0

纹理 ID（TEXTURE\_OES/TEXTURE\_2D 时有效）

transformMatrix

float 数组

null

4×4 行优先纹理变换矩阵（TEXTURE\_OES/TEXTURE\_2D 时有效）（@Nullable）

timeStamp

long

0

时间戳（毫秒）

### 数据消息类型

**AoqDataMsg**

**字段**

**类型**

**默认值**

**说明**

data

byte\[\]

new byte\[0\]

消息数据（字节数组）
