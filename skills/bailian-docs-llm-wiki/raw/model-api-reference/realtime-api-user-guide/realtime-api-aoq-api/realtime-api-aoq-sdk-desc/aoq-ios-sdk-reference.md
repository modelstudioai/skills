# AOQ Client SDK iOS API 参考

AOQ Client SDK iOS API 参考，涵盖引擎生命周期、音视频设备管理、编码配置、媒体流控制、音频文件播放、外部音频流、实时消息、帧回调、委托协议以及数据类型与枚举。

## 目录

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

setAudioSessionRestriction

设置 AVAudioSession 控制权限（iOS 独有）

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

设置音频帧数据回调 delegate

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

启动屏幕采集（Broadcast Upload Extension）

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

设置视频帧数据回调 delegate

enableVideoFrameObserver

开启或关闭指定位置的视频帧回调

### 实时消息

接口

简介

sendDataMsg

发送实时数据消息

### AoqEngineDelegate 回调

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

onAudioFileState

音频文件播放状态回调

onLocalAudioVolumeIndication

本地采集音量提示回调

onVideoDeviceStateChanged

视频设备操作状态变化回调

onDataMsg

收到实时数据消息回调

onScreenCaptureStateChanged

屏幕采集状态变化回调（@optional）

### AoqAudioFrameDelegate 回调

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

### AoqVideoFrameDelegate 回调

接口

简介

onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。

onPreEncodeVideoFrame

编码前的视频帧触发（前处理后）。

onRemoteVideoFrame

远端解码后、渲染前的视频帧触发。

## 接口详情

### 引擎生命周期

#### createEngine:delegate:

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

```
+ (instancetype _Nonnull)createEngine:(AoqCreateConfig * _Nonnull)config
                             delegate:(id<AoqEngineDelegate> _Nonnull)delegate;
```

参数

类型

说明

config

AoqCreateConfig \*

引擎创建配置

delegate

id<AoqEngineDelegate>

引擎事件回调代理

返回值：AoqClientEngine 引擎实例，不会返回 nil。

#### destroy

销毁引擎实例，释放所有资源。销毁后需要重新调用 createEngine: 才能继续使用。

```
+ (int)destroy;
```

参数：无。

返回值：0 表示成功；非 0 表示失败（对应 AoqErrorCode）。

#### getVersion

获取 SDK 当前版本号。可在 createEngine: 之前调用。

```
+ (NSString * _Nonnull)getVersion;
```

参数：无。

返回值：版本号字符串，如 "1.3.0"。

#### connect:

连接 Relay 服务器。连接参数由业务方 AppServer 通过 /api/v1/allocate 分配后下发给客户端。调用后立即返回，实际连接结果通过 onConnectionStatusChange: 回调通知。

```
- (int)connect:(AoqConnectConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqConnectConfig \*

连接配置，包含 Token、SID、Relay 接入点列表、发布/订阅轨道等

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败（对应 AoqErrorCode）。

**说明**Screen track 当前仅支持上行，下行订阅尚未实现，因此 config.subscribeTracks 中不能传入 AoqTrackTypeScreen，否则返回 AoqECUnSupport 且连接不会发起；连接成功前不建议调用 enableSendMediaStream:enable:YES，应在 onConnectionStatusChange: 收到 Connected 后再开启。

#### disconnect

断开与服务器的连接，释放连接相关资源。调用后立即返回，实际断开结果通过 onConnectionStatusChange: 回调通知。

```
- (int)disconnect;
```

参数：无。

返回值：0 表示调用已下发（异步执行）；非 0 表示失败（对应 AoqErrorCode）。

### 音频设备管理

#### startAudioCapture:

打开音频采集设备（麦克风），开始采集本地音频。若使用外部音频输入（pushAudioExternalStreamData:data:），需将 isExternal 设为 YES，此时不会真正打开麦克风。

```
- (int)startAudioCapture:(AoqAudioCaptureConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqAudioCaptureConfig \*

音频采集配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECAudioDeviceRecordingAuthFailed 表示录音权限未获取）。

**说明**需在 Info.plist 配置 NSMicrophoneUsageDescription 并获取录音权限；设备状态变化通过 onAudioDeviceStateChanged: 回调通知。

#### stopAudioCapture

关闭音频采集设备，停止本地音频采集。

```
- (int)stopAudioCapture;
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### muteAudioCapture:

静音或取消静音音频采集。静音后 SDK 仍持续采集但发送静音帧，与 stopAudioCapture 不同。

```
- (int)muteAudioCapture:(BOOL)mute;
```

参数

类型

说明

mute

BOOL

YES 表示静音；NO 表示取消静音

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需在 startAudioCapture: 之后调用才生效。

#### startAudioPlayer:

开始音频渲染，播放远端音频到扬声器/听筒。若使用外部渲染（自行播放 PCM），需将 isExternal 设为 YES。

```
- (int)startAudioPlayer:(AoqAudioPlaybackConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqAudioPlaybackConfig \*

音频播放配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECAudioDevicePlayoutOccupied 表示播放设备被占用）。

**说明**设备状态变化通过 onAudioDeviceStateChanged: 回调通知；输出路由变化通过 onAudioDeviceRouteChanged: 回调通知。

#### stopAudioPlayer

停止音频渲染，关闭播放设备。

```
- (int)stopAudioPlayer;
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pauseAudioPlayer:

暂停音频渲染，支持淡出效果。暂停期间远端音频数据仍会到达但不播放。

```
- (int)pauseAudioPlayer:(NSInteger)fadeMs;
```

参数

类型

说明

fadeMs

NSInteger

淡出时长（毫秒）；0 表示立即暂停

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### resumeAudioPlayer:

恢复音频渲染，支持淡入效果。需在 pauseAudioPlayer: 之后调用。

```
- (int)resumeAudioPlayer:(NSInteger)fadeMs;
```

参数

类型

说明

fadeMs

NSInteger

淡入时长（毫秒）；0 表示立即恢复

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### interruptAudioPlayer:fadeMs:

打断本轮音频通话，清空当前播放缓冲区。常用于 AI 对话场景下用户打断 AI 说话。

```
- (int)interruptAudioPlayer:(AoqTrackType)trackType fadeMs:(NSInteger)fadeMs;
```

参数

类型

说明

trackType

AoqTrackType

需要打断的轨道类型

fadeMs

NSInteger

淡出时长（毫秒）；0 表示立即打断

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### enableSpeakerphone:

切换音频输出到扬声器或听筒。仅在 startAudioPlayer: 之后生效。

```
- (int)enableSpeakerphone:(BOOL)enable;
```

参数

类型

说明

enable

BOOL

YES 表示切换到扬声器；NO 表示切换到听筒

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECAudioDeviceEarpieceRequiresVoipMode 表示听筒需要 VoIP 模式）。

**说明**切换到听筒需要 AoqAudioPlaybackConfig.isVoipMode=YES；路由变化通过 onAudioDeviceRouteChanged: 回调通知。

#### isSpeakerphoneEnabled

查询当前是否使用扬声器输出。

```
- (BOOL)isSpeakerphoneEnabled;
```

参数：无。

返回值：YES 表示当前使用扬声器；NO 表示当前使用听筒或其他路由。

#### setAudioSessionRestriction:

设置 SDK 对 AVAudioSession 的控制权限（iOS 独有）。用于业务方自行管理 AVAudioSession 时，限制 SDK 的干预范围。

```
- (int)setAudioSessionRestriction:(int)restriction;
```

参数

类型

说明

restriction

int

AVAudioSession 控制权限位掩码，对应 AoqAudioSessionRestriction；可多位按位或组合

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**默认 SDK 完全管理 AVAudioSession；若业务方需要自行控制 category/激活状态，通过本接口约束 SDK 行为。

### 音频编码配置

#### setAudioEncoderConfig:

设置音频编码参数，用于上行推流的音频编码。配置变更会立即生效。

```
- (int)setAudioEncoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqAudioCodecConfig \*

音频编码配置；trackType 应设为 AoqTrackTypeAudio

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECParamInvalid 表示参数非法）。

**说明**codecType 决定编码格式（默认 Opus），sampleRate 与 channel 需与采集端匹配；bitrate 仅在 Opus 等有损编码下生效。

#### setAudioDecoderConfig:

设置音频解码参数，用于下行拉流的音频解码。需与远端编码参数匹配。

```
- (int)setAudioDecoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqAudioCodecConfig \*

音频解码配置；trackType 应设为 AoqTrackTypeAudio

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**sampleRate 需与远端编码器输出采样率一致，否则可能触发解码错误或音质异常。

### 音频文件播放

#### startAudioFile:config:

开始推流播放本地音频文件。可同时推流到远端和本地播放，音量分别由 publishVolume 和 playoutVolume 控制。

```
- (int)startAudioFile:(NSString * _Nonnull)fileId config:(AoqAudioFileMixConfig * _Nonnull)config;
```

参数

类型

说明

fileId

NSString \*

文件标识符，业务方自定义，用于后续控制

config

AoqAudioFileMixConfig \*

音频文件播放配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**播放状态变化通过 onAudioFileState: 回调通知；同一 fileId 重复调用会覆盖之前的播放。

#### stopAudioFile:

停止音频文件播放。

```
- (int)stopAudioFile:(NSString * _Nonnull)fileId;
```

参数

类型

说明

fileId

NSString \*

文件标识符，与 startAudioFile:config: 传入的一致

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pauseAudioFile:

暂停音频文件播放。

```
- (int)pauseAudioFile:(NSString * _Nonnull)fileId;
```

参数

类型

说明

fileId

NSString \*

文件标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### resumeAudioFile:

恢复音频文件播放。需在 pauseAudioFile: 之后调用。

```
- (int)resumeAudioFile:(NSString * _Nonnull)fileId;
```

参数

类型

说明

fileId

NSString \*

文件标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioFileDuration:

获取音频文件总时长。

```
- (long long)getAudioFileDuration:(NSString * _Nonnull)fileId;
```

参数

类型

说明

fileId

NSString \*

文件标识符

返回值：文件总时长（毫秒）；文件未加载或不存在时返回 0。

#### getAudioFileCurrentPosition:

获取音频文件当前播放位置。

```
- (long long)getAudioFileCurrentPosition:(NSString * _Nonnull)fileId;
```

参数

类型

说明

fileId

NSString \*

文件标识符

返回值：当前播放位置（毫秒）；文件未加载或不存在时返回 0。

#### setAudioFilePositionMillis:positionMillis:

设置音频文件播放位置（seek）。

```
- (int)setAudioFilePositionMillis:(NSString * _Nonnull)fileId positionMillis:(long long)positionMillis;
```

参数

类型

说明

fileId

NSString \*

文件标识符

positionMillis

long long

目标播放位置（毫秒）

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### setAudioFileVolume:type:volume:

设置音频文件音量，可分别控制推流音量和本地播放音量。

```
- (int)setAudioFileVolume:(NSString * _Nonnull)fileId type:(AoqAudioStreamDirection)type volume:(NSInteger)volume;
```

参数

类型

说明

fileId

NSString \*

文件标识符

type

AoqAudioStreamDirection

音量方向；AoqAudioStreamPublish 推流，AoqAudioStreamPlayout 播放

volume

NSInteger

音量值，取值范围 \[0-100\]

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioFileVolume:type:

获取音频文件当前音量。

```
- (int)getAudioFileVolume:(NSString * _Nonnull)fileId type:(AoqAudioStreamDirection)type;
```

参数

类型

说明

fileId

NSString \*

文件标识符

type

AoqAudioStreamDirection

音量方向

返回值：当前音量值 \[0-100\]；文件不存在时返回 0。

### 外部音频流

#### addAudioExternalStream:config:

新增一条外部音频流。可创建多条独立的外部流，通过 streamId 区分。

```
- (int)addAudioExternalStream:(NSString * _Nonnull)streamId config:(AoqAudioExternalStreamConfig * _Nonnull)config;
```

参数

类型

说明

streamId

NSString \*

外部流标识符，业务方自定义

config

AoqAudioExternalStreamConfig \*

外部音频流配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### pushAudioExternalStreamData:data:

输入外部音频 PCM 数据到指定流。

```
- (int)pushAudioExternalStreamData:(NSString * _Nonnull)streamId data:(AoqAudioFrameData * _Nonnull)data;
```

参数

类型

说明

streamId

NSString \*

外部流标识符

data

AoqAudioFrameData \*

PCM 音频帧数据

返回值：0 表示调用成功；非 0 表示失败。缓冲区满时返回 AoqECAudioExternalBufferFull(110)。

**说明**data.dataPtr 指向的内存仅在调用期间有效，SDK 内部会拷贝；采样率/声道数需与 addAudioExternalStream:config: 时的配置一致。

#### setAudioExternalStreamVolume:type:volume:

设置外部音频流音量，可分别控制推流音量和本地播放音量。

```
- (int)setAudioExternalStreamVolume:(NSString * _Nonnull)streamId type:(AoqAudioStreamDirection)type volume:(NSInteger)volume;
```

参数

类型

说明

streamId

NSString \*

外部流标识符

type

AoqAudioStreamDirection

音量方向

volume

NSInteger

音量值，取值范围 \[0-100\]

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### getAudioExternalStreamVolume:type:

获取外部音频流当前音量。

```
- (int)getAudioExternalStreamVolume:(NSString * _Nonnull)streamId type:(AoqAudioStreamDirection)type;
```

参数

类型

说明

streamId

NSString \*

外部流标识符

type

AoqAudioStreamDirection

音量方向

返回值：当前音量值 \[0-100\]；流不存在时返回 0。

#### clearAudioExternalStreamBuffer:fadeoutMs:

清空外部音频流缓存，支持淡出效果。常用于打断当前播放内容。

```
- (void)clearAudioExternalStreamBuffer:(NSString * _Nonnull)streamId fadeoutMs:(NSInteger)fadeoutMs;
```

参数

类型

说明

streamId

NSString \*

外部流标识符

fadeoutMs

NSInteger

淡出时长（毫秒）；-1 表示使用默认值，0 表示立即清空，>0 表示保留指定毫秒数淡出

返回值：无（void）。

#### removeAudioExternalStream:

移除外部音频流，释放相关资源。

```
- (int)removeAudioExternalStream:(NSString * _Nonnull)streamId;
```

参数

类型

说明

streamId

NSString \*

外部流标识符

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

### 音频帧回调

#### setAudioFrameObserver:

设置音频帧数据回调 delegate。传入 delegate=nil 表示移除监听。

```
- (int)setAudioFrameObserver:(id<AoqAudioFrameDelegate> _Nullable)delegate;
```

参数

类型

说明

delegate

id<AoqAudioFrameDelegate>

音频帧监听协议；传 nil 表示移除

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需先调用本接口设置 delegate，再通过 enableAudioFrameObserver:audioSource:config: 开启具体位置的回调。

#### enableAudioFrameObserver:audioSource:config:

开启或关闭指定位置的音频帧回调。

```
- (int)enableAudioFrameObserver:(BOOL)enabled audioSource:(AoqAudioSource)audioSource config:(AoqAudioObserverConfig * _Nonnull)config;
```

参数

类型

说明

enabled

BOOL

YES 表示开启；NO 表示关闭

audioSource

AoqAudioSource

音频源位置；可选采集/3A处理后/推流/播放

config

AoqAudioObserverConfig \*

回调配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**回调线程为 SDK 内部线程，禁止在回调中执行耗时操作或阻塞调用；dataPtr 仅在回调期间有效，异步使用需自行拷贝。

### 本地音量提示

#### enableLocalAudioVolumeIndication:

开启或关闭本地采集音量提示。开启后 SDK 按 config.interval 周期触发 onLocalAudioVolumeIndication: 回调，上报本地采集音量及是否人声。

```
- (int)enableLocalAudioVolumeIndication:(AoqAudioVolumeIndicationConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqAudioVolumeIndicationConfig \*

音量提示配置；interval<=0 表示关闭回调

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需在 startAudioCapture: 之后调用才有音量数据；interval>0 且 <10 时按 10 处理。

### 视频设备管理

#### startVideoCapture:

打开视频采集设备（摄像头），采集内容通过 AoqTrackTypeVideo 通道发送。若使用外部视频输入（pushExternalVideoCapturedFrame:frame:），需将 isExternal 设为 YES，此时不会真正打开摄像头。

```
- (int)startVideoCapture:(AoqVideoCaptureConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqVideoCaptureConfig \*

视频采集配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode，如 AoqECVideoDeviceCameraAuthFailed 表示摄像头权限未获取）。

**说明**需在 Info.plist 配置 NSCameraUsageDescription 并获取摄像头权限；设备状态变化通过 onVideoDeviceStateChanged: 回调通知。

#### stopVideoCapture

关闭视频采集设备，停止本地视频采集。

```
- (int)stopVideoCapture;
```

参数：无。

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### switchCamera:

切换前后置摄像头。需在 startVideoCapture:(isExternal=NO) 之后调用。

```
- (int)switchCamera:(AoqCameraDirection)direction;
```

参数

类型

说明

direction

AoqCameraDirection

目标摄像头方向；AoqCameraDirectionFront 前置，AoqCameraDirectionBack 后置

返回值：0 表示调用成功；< 0 表示失败（对应 AoqErrorCode）。

**说明**外部采集模式（isExternal=YES）下调用无效。

#### setLocalView:canvas:

设置或移除本地视频渲染窗口。传入 canvas=nil 或 canvas.view=nil 表示解绑渲染。

```
- (int)setLocalView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型；本地预览传 AoqTrackTypeVideo

canvas

AoqVideoCanvas \*

视频渲染画布；传 nil 表示解绑

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

#### setRemoteView:canvas:

设置或移除远端视频渲染窗口。传入 canvas=nil 或 canvas.view=nil 表示解绑。

```
- (int)setRemoteView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型

canvas

AoqVideoCanvas \*

视频渲染画布；传 nil 表示解绑

返回值：0 表示调用成功；非 0 表示失败。trackType 为 AoqTrackTypeScreen 时返回 AoqECUnSupport，窗口不会绑定。

**说明**Screen track 当前仅支持上行，没有远端画面可渲染，因此 trackType 不能传入 AoqTrackTypeScreen。

### 视频编码与外部输入

#### setVideoEncoderConfig:

设置视频编码参数，用于上行推流的视频编码，按 config.trackType 路由。若 isExternal=YES，SDK 不做二次编码，由 pushExternalVideoEncodedFrame:frame: 直推已编码帧。

```
- (int)setVideoEncoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqVideoCodecConfig \*

视频编码配置

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**使用 pushExternalVideoEncodedFrame: 时，必须先调用本接口且 isExternal=YES，该模式不经过采集管线，无需 startVideoCapture:/startScreenCapture:；使用 pushExternalVideoCapturedFrame: 时，isExternal 保持 NO，由 SDK 内部编码。

#### setVideoDecoderConfig:

设置视频解码参数，用于下行拉流的视频解码，按 config.trackType 路由。解码时仅 trackType/codecType/width/height/fps/bitrate 生效，其余字段仅编码使用。

```
- (int)setVideoDecoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

参数

类型

说明

config

AoqVideoCodecConfig \*

视频解码配置

返回值：0 表示调用成功；非 0 表示失败。config.trackType 为 AoqTrackTypeScreen 时返回 AoqECUnSupport，配置不会下发。

**说明**Screen track 当前仅支持上行，没有下行订阅，因此 config.trackType 不能传入 AoqTrackTypeScreen。

#### pushExternalVideoCapturedFrame:frame:

推送外部原始视频帧，SDK 编码后发送。按 trackType 路由，对应通道需已开启外部采集。

```
- (int)pushExternalVideoCapturedFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型；AoqTrackTypeVideo 需先 startVideoCapture:(isExternal=YES)，AoqTrackTypeScreen 需先 startScreenCapture:(isExternal=YES)

frame

AoqVideoFrame \*

外部视频帧数据

返回值：0 表示调用成功；对应通道未开启外部采集返回 AoqECVideoExternalCaptureNotEnabled(211)；缓冲满返回 AoqECVideoExternalBufferFull(210)；< 0 表示其他失败。

**说明**frame.timeStamp<=0 时 SDK 会用本地时钟自动补齐；支持 CVPixelBuffer 零拷贝路径（format=AoqVideoPixelFormatCVPixelBuffer）。

#### pushExternalVideoEncodedFrame:frame:

推送外部已编码视频帧（SDK 不做二次编码，直接打包发送）。仅当对应 trackType 已 setVideoEncoderConfig:(isExternal=YES) 后才消费，不依赖 startVideoCapture:/startScreenCapture:。

```
- (int)pushExternalVideoEncodedFrame:(AoqTrackType)trackType frame:(AoqVideoEncodedFrame * _Nonnull)frame;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型；支持 AoqTrackTypeVideo / AoqTrackTypeScreen

frame

AoqVideoEncodedFrame \*

外部已编码视频帧

返回值：0 表示调用成功；对应通道未开启外部编码返回 AoqECVideoExternalEncoderNotEnabled(212)；< 0 表示失败。

**说明**frame.timeStamp 直接透传，SDK 不做补齐；调用方需自行保证时间戳单调递增。

### 屏幕采集

```
- (int)startScreenCapture:(AoqScreenCaptureConfig * _Nonnull)config;
- (int)stopScreenCapture;
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

启动返回 0 表示请求已受理，最终状态通过 `onScreenCaptureStateChanged` 通知；非 0 表示同步拒绝，不重复报告失败事件。停止返回 0 表示成功，非 0 表示失败，停止结果由该回调通知。

`isExternal=NO` 时使用 Broadcast Upload Extension。应用需集成并配置 `AoqScreenShare.framework`，展示系统广播选择器；等待超时通过 `onScreenCaptureStateChanged:` 回调报告失败，错误码为 `AoqECScreenStartFailed`。无需等待 Started 才启用发送。

外部原始帧：设置 `isExternal=YES` 后，不启用 Extension 接收通道，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`；不需要调用 `startScreenCapture`。

### 媒体流发送控制

#### enableSendMediaStream:enable:

控制本地媒体流的发送开关，按 trackType 路由。关闭时 SDK 仍采集/编码但不发送到网络。

```
- (int)enableSendMediaStream:(AoqTrackType)trackType enable:(BOOL)enable;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型；支持 AoqTrackTypeAudio/AoqTrackTypeVideo/AoqTrackTypeScreen

enable

BOOL

YES 表示开启发送；NO 表示关闭发送

返回值：0 表示调用成功；< 0 表示失败（对应 AoqErrorCode）。

**说明**建议初始化后先 enableSendMediaStream:enable:NO，待 onConnectionStatusChange: 收到 Connected 后再开启，避免连接建立前的数据丢失。

### 视频帧回调

#### setVideoFrameObserver:

设置视频帧数据回调 delegate。传入 delegate=nil 表示移除监听。

```
- (int)setVideoFrameObserver:(id<AoqVideoFrameDelegate> _Nullable)delegate;
```

参数

类型

说明

delegate

id<AoqVideoFrameDelegate>

视频帧监听协议；传 nil 表示移除

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**需先调用本接口设置 delegate，再通过 enableVideoFrameObserver:videoSource:config: 开启具体位置的回调。

#### enableVideoFrameObserver:videoSource:config:

开启或关闭指定位置的视频帧回调。

```
- (int)enableVideoFrameObserver:(BOOL)enabled videoSource:(AoqVideoSource)videoSource config:(AoqVideoObserverConfig * _Nonnull)config;
```

参数

类型

说明

enabled

BOOL

YES 表示开启；NO 表示关闭

videoSource

AoqVideoSource

视频源位置；可选采集后/编码前/远端解码后

config

AoqVideoObserverConfig \*

回调配置；通过 config.trackType 指定观察 Video 或 Screen 轨道

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**回调线程为 SDK 内部线程，禁止在回调中执行耗时操作；仅 I420/CVPixelBuffer 格式支持读写模式（mode=ReadWrite），其他格式只读。

### 实时消息

#### sendDataMsg:

发送实时数据消息到远端。需在 connect: 成功且 enableSendMediaStream:(Data, YES) 之后调用。

```
- (int)sendDataMsg:(AoqDataMsg * _Nonnull)msg;
```

参数

类型

说明

msg

AoqDataMsg \*

数据消息

返回值：0 表示调用成功；非 0 表示失败（对应 AoqErrorCode）。

**说明**远端通过 onDataMsg: 回调接收；消息大小受 SDK 内部限制，超大消息建议分片发送。

### AoqEngineDelegate 回调

#### onError:message:

引擎错误回调。发生不可恢复错误时触发。

```
- (void)onError:(NSInteger)code message:(NSString * _Nonnull)message;
```

参数

类型

说明

code

NSInteger

错误码，对应 AoqErrorCode 枚举值

message

NSString \*

错误描述信息

返回值：无（void）。

#### onWarning:message:

引擎警告回调。发生可恢复异常时触发，不影响 SDK 继续运行。

```
- (void)onWarning:(NSInteger)code message:(NSString * _Nonnull)message;
```

参数

类型

说明

code

NSInteger

警告码，对应 AoqWarningCode 枚举值

message

NSString \*

警告描述信息

返回值：无（void）。

#### onConnectionStatusChange:

连接状态变化回调。状态流转：Disconnected -> Connecting -> Connected/Failed -> Disconnected。

```
- (void)onConnectionStatusChange:(AoqConnectionStatus)status;
```

参数

类型

说明

status

AoqConnectionStatus

当前连接状态

返回值：无（void）。

**说明**收到 Connected 后再调用 enableSendMediaStream:enable:YES 开启媒体流发送。

#### onStats:

引擎统计信息回调。SDK 周期性上报音视频推拉流及网络统计数据，可用于实时监控通话质量、网络状态、诊断音视频问题。

```
- (void)onStats:(AoqStats * _Nonnull)stats;
```

参数

类型

说明

stats

AoqStats \*

统计信息，包含音频/视频/数据消息的推拉流统计及网络统计

返回值：无（void）。

#### onAudioDeviceStateChanged:

音频设备采集/播放操作状态变化回调。

```
- (void)onAudioDeviceStateChanged:(AoqAudioDeviceState * _Nonnull)state;
```

参数

类型

说明

state

AoqAudioDeviceState \*

音频设备状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

#### onAudioDeviceRouteChanged:

音频输出路由变化回调。

```
- (void)onAudioDeviceRouteChanged:(NSInteger)routeType;
```

参数

类型

说明

routeType

NSInteger

当前音频输出路由，对应 AoqAudioDeviceRouteType 枚举值

返回值：无（void）。

#### onAudioDeviceInterrupted:

音频设备中断回调。系统级中断（如来电、其他 App 抢占音频焦点）时触发。

```
- (void)onAudioDeviceInterrupted:(BOOL)interrupt;
```

参数

类型

说明

interrupt

BOOL

YES 表示被中断；NO 表示中断恢复

返回值：无（void）。

#### onAudioFileState:

音频文件播放状态回调。

```
- (void)onAudioFileState:(AoqAudioFileState * _Nonnull)state;
```

参数

类型

说明

state

AoqAudioFileState \*

音频文件播放状态；包含 fileId、stateCode、errorCode

返回值：无（void）。

#### onLocalAudioVolumeIndication:

本地采集音量提示回调。需调用 enableLocalAudioVolumeIndication: 开启后才会触发。

```
- (void)onLocalAudioVolumeIndication:(AoqAudioVolume * _Nonnull)volume;
```

参数

类型

说明

volume

AoqAudioVolume \*

本地音量信息；包含 isSpeech（是否人声）和 volume（平滑后瞬时音量 \[0-255\]）

返回值：无（void）。

`onScreenCaptureStateChanged:` 为 `@optional`，其余 `AoqEngineDelegate` 回调方法为 `@required`。

#### onVideoDeviceStateChanged:

视频设备采集操作状态变化回调。

```
- (void)onVideoDeviceStateChanged:(AoqVideoDeviceState * _Nonnull)state;
```

参数

类型

说明

state

AoqVideoDeviceState \*

视频设备状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

#### onDataMsg:

收到实时数据消息回调。

```
- (void)onDataMsg:(AoqDataMsg * _Nonnull)msg;
```

参数

类型

说明

msg

AoqDataMsg \*

数据消息

返回值：无（void）。

**说明**回调线程为 SDK 内部线程，禁止在回调中执行耗时操作；NSData 仅在回调期间有效，异步使用需自行拷贝。

#### onScreenCaptureStateChanged

屏幕采集状态变化回调（@optional）。使用 AoqScreenCaptureStateCode 与统一的 AoqErrorCode，在主线程按顺序通知。屏幕失败不重复通过 onError: 上报。

```
- (void)onScreenCaptureStateChanged:(AoqScreenCaptureState * _Nonnull)state;
```

参数

类型

说明

state

AoqScreenCaptureState \*

屏幕采集状态；包含 state（状态码）和 reason（错误原因）

返回值：无（void）。

**说明**Started 表示采集/外部输入已就绪，不表示媒体已发送；Fail 和 Stopped 均为清理完成后的终态。

### AoqAudioFrameDelegate 回调

音频帧数据监听协议。所有方法均为 @optional，按需实现。

```
@protocol AoqAudioFrameDelegate <NSObject>
@optional
- (void)onCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onProcessCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onPublishAudioFrame:(AoqTrackType)trackType frame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onPlaybackAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
@end
```

方法

触发时机

参数

onCapturedAudioFrame:

采集到原始音频帧时

frame: AoqAudioFrameData \*

onProcessCapturedAudioFrame:

3A 处理后的音频帧

frame: AoqAudioFrameData \*

onPublishAudioFrame:frame:

推流前的音频帧

trackType: 轨道类型；frame: AoqAudioFrameData \*

onPlaybackAudioFrame:

播放前的远端音频帧

frame: AoqAudioFrameData \*

返回值：无（void）。

**说明**通过 enableAudioFrameObserver:audioSource:config: 开启对应 AoqAudioSource 后才会触发；dataPtr 仅在回调期间有效。

#### onCapturedAudioFrame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

```
- (void)onCapturedAudioFrame:(AoqAudioFrameData *)frame;
```

参数

类型

说明

frame

AoqAudioFrameData \*

采集的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onProcessCapturedAudioFrame

3A 处理后的音频帧触发。数据已经过回声消除、降噪等处理。

```
- (void)onProcessCapturedAudioFrame:(AoqAudioFrameData *)frame;
```

参数

类型

说明

frame

AoqAudioFrameData \*

3A 处理后的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onPublishAudioFrame

推流前的音频帧触发。数据为最终编码发送前的音频。

```
- (void)onPublishAudioFrame:(AoqTrackType)trackType frame:(AoqAudioFrameData *)frame;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型

frame

AoqAudioFrameData \*

推流前的音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onPlaybackAudioFrame

播放前的远端音频帧触发。数据为解码后、混音后待播放的音频。

```
- (void)onPlaybackAudioFrame:(AoqAudioFrameData *)frame;
```

参数

类型

说明

frame

AoqAudioFrameData \*

播放前的远端音频帧数据

返回值：无（void）。

**说明**frame.dataPtr 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

### AoqVideoFrameDelegate 回调

视频帧数据监听协议。所有方法均为 @optional，返回 NO 表示不修改数据。三个回调均带 trackType 参数，用于区分 Video / Screen 轨道。

```
@protocol AoqVideoFrameDelegate <NSObject>
@optional
- (BOOL)onCapturedVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (BOOL)onPreEncodeVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (BOOL)onRemoteVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
@end
```

方法

触发时机

参数

onCapturedVideoFrame:frame:

采集到原始视频帧时（前处理前）

trackType: 轨道类型；frame: AoqVideoFrame \*

onPreEncodeVideoFrame:frame:

编码前的视频帧（前处理后）

trackType: 轨道类型；frame: AoqVideoFrame \*

onRemoteVideoFrame:frame:

远端解码后、渲染前的视频帧

trackType: 轨道类型；frame: AoqVideoFrame \*

返回值：BOOL。返回 YES 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 格式写回生效）；返回 NO 表示不修改。

**说明**通过 enableVideoFrameObserver:videoSource:config: 开启对应 AoqVideoSource 后才会触发；frame 中 NSData/pixelBuffer 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。

```
- (BOOL)onCapturedVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame *)frame;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型(Video/Screen)

frame

AoqVideoFrame \*

采集的视频帧数据

返回值：BOOL。YES 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 生效），NO 表示不修改。

**说明**通过 enableVideoFrameObserver:videoSource:config: 开启对应 AoqVideoSource 后才会触发；frame 中 NSData/pixelBuffer 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onPreEncodeVideoFrame

编码前的视频帧触发（前处理后）。

```
- (BOOL)onPreEncodeVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame *)frame;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型(Video/Screen)

frame

AoqVideoFrame \*

编码前的视频帧数据

返回值：BOOL。YES 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 生效），NO 表示不修改。

**说明**通过 enableVideoFrameObserver:videoSource:config: 开启对应 AoqVideoSource 后才会触发；frame 中 NSData/pixelBuffer 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

#### onRemoteVideoFrame

远端解码后、渲染前的视频帧触发。

```
- (BOOL)onRemoteVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame *)frame;
```

参数

类型

说明

trackType

AoqTrackType

轨道类型(Video/Screen)

frame

AoqVideoFrame \*

远端解码后的视频帧数据

返回值：BOOL。YES 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 生效），NO 表示不修改。

**说明**通过 enableVideoFrameObserver:videoSource:config: 开启对应 AoqVideoSource 后才会触发；frame 中 NSData/pixelBuffer 引用 SDK 内部内存，仅在回调期间有效，异步使用需自行拷贝。

## 数据类型与枚举

### 通用类型

#### AoqConnectConfig

`subscribeTracks` 不能包含 `AoqTrackTypeScreen`，否则 `connect` 返回 `AoqECUnSupport`，不发起连接。`setRemoteView` 不支持 Screen，传入时返回 `AoqECUnSupport`。

**字段**

**类型**

**说明**

token

NSString \*

连接鉴权 Token

sid

NSString \*

会话 ID

certFingerprint

NSString \*

服务器证书指纹

relayEndpoints

NSArray<AoqRelayEndpoint \*> \*

Relay 接入点列表

workspaceIdHash

NSString \*

工作空间 ID Hash

publishTracks

NSArray<AoqTrackParam \*> \*

本端计划发布的轨道列表

subscribeTracks

NSArray<AoqTrackParam \*> \*

本端计划订阅的轨道列表

#### AoqRelayEndpoint

Relay 接入点。

字段

类型

默认值

说明

routeIndex

NSInteger

\-1

路径序号

endpoint

NSString \*

""

服务端地址（域名或 IP）

port

NSInteger

0

服务端 UDP 端口

tcpPort

NSInteger

0

TCP 降级端口，0 表示使用 SDK 默认端口 443

#### AoqTrackParam.trackMode

字段

类型

默认值

说明

trackMode

AoqTrackMode

AoqTrackModeSegment

仅对音频下行生效。

#### AoqCreateConfig（v1.3.0 新增字段）

字段

类型

默认值

说明

maxEncodedVideoFrameBytes

NSInteger

190 × 1024

编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。

enableDropOversizedVideoFrame

BOOL

NO

仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。

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

不支持的操作

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

听筒输出需要 VoIP 模式

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

#### AoqWarningCode

警告码枚举。

枚举值

值

说明

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

#### AoqEncoderType

Track 媒体格式。

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

#### AoqConnectionStatus

引擎连接状态。

枚举值

值

说明

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

#### AoqAudioPlaybackConfig

**字段**

**类型**

**默认值**

**说明**

isVoipMode

BOOL

NO

YES 启用 VoIP 模式（硬件 AEC），移动端有效

isDefaultSpeaker

BOOL

YES

YES 默认扬声器；NO 听筒

isExternal

BOOL

NO

YES 外部音频输出

channel

NSInteger

1

声道数 1/2

#### AoqAudioCaptureConfig

音频采集配置。

字段

类型

默认值

说明

isExternal

BOOL

NO

是否为外部采集模式

isVoipMode

BOOL

NO

是否启用 VoIP 模式（硬件 AEC），移动端有效

channel

NSInteger

1

声道数，支持 1/2

#### AoqAudioCodecConfig

音频编解码配置。setAudioEncoderConfig: 与 setAudioDecoderConfig: 共用。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeAudio

轨道类型

codecType

AoqEncoderType

AoqEncoderTypeAudioOpus

编码格式

sampleRate

NSInteger

48000

采样率（Hz）

channel

NSInteger

1

声道数

bitrate

NSInteger

32000

比特率（bps）

#### AoqAudioSessionRestriction

AVAudioSession 控制权限位掩码（NS\_OPTIONS，可按位或组合）。setAudioSessionRestriction: 使用。

枚举值

值

说明

AoqAudioSessionNone

0

不限制（SDK 完全管理 AVAudioSession）

AoqAudioSessionSetCategory

1

限制 SDK 设置 category

AoqAudioSessionConfigureSession

2

限制 SDK 配置 session

AoqAudioSessionDeactivateSession

4

限制 SDK 反激活 session

AoqAudioSessionActivateSession

8

限制 SDK 激活 session

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

NSInteger

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

NSString \*

""

文件名（含路径），非空

cycles

NSInteger

\-1

循环次数，-1 表示无限循环

startPosMs

NSInteger

0

起始播放位置（毫秒）

publishVolume

NSInteger

100

推流音量，取值范围 \[0-100\]

playoutVolume

NSInteger

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

NSString \*

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

#### AoqAudioVolume

字段

类型

默认值

说明

isSpeech

BOOL

NO

是否为人声。

volume

NSInteger

0

平滑后的瞬时音量，范围 0～255。

#### AoqAudioVolumeIndicationConfig

字段

类型

默认值

说明

reportSpeech

BOOL

NO

是否检测人声。

interval

NSInteger

0

回调间隔（毫秒）；小于等于 0 时关闭，大于 0 且小于 10 时按 10 处理。

smooth

NSInteger

3

平滑系数，范围 0～10；越大越平滑。

#### AoqAudioStreamDirection

音频流方向。

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

外部音频流配置。

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeAudio

音频轨道类型

codecType

AoqEncoderType

AoqEncoderTypeAudioPCM

音频流格式

channels

NSInteger

1

声道数

sampleRate

NSInteger

48000

采样率（Hz）

playoutVolume

NSInteger

100

播放音量 \[0-100\]

publishVolume

NSInteger

100

推流音量 \[0-100\]

maxBufferDuration

NSInteger

1000

最大缓冲时长（毫秒）

enable3A

BOOL

NO

是否对输入 PCM 进行 3A 处理

#### AoqAudioFrameData

外部音频帧数据。

字段

类型

默认值

说明

dataPtr

void \*

NULL

音频 PCM 裸数据指针（@Nullable）

dataSize

NSInteger

0

PCM 数据字节数

numOfSamples

NSInteger

0

采样点数（单声道）

bytesPerSample

NSInteger

0

每个采样点的字节数

numOfChannels

NSInteger

0

声道数

samplesPerSec

NSInteger

0

每秒采样点数（采样率）

pushSequence

int32\_t

0

PCM 输入轮次

timeStamp

int64\_t

0

时间戳

autoGenMute

BOOL

NO

数据回调有效，YES 表示 SDK 生成的静音数据

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

NSInteger

48000

回调音频采样率（Hz）

channels

NSInteger

1

回调音频声道数

mode

AoqAudioObserverMode

AoqAudioObserverModeReadOnly

读写模式

### 视频类型

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

NSInteger

0

正常为 0；失败时为 AoqErrorCode 错误码。

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

#### AoqScreenCaptureConfig

字段

类型

默认值

说明

isExternal

BOOL

NO

是否由应用提供屏幕原始帧。

appGroup

NSString \*

nil

可选的主 App 与 Broadcast Extension 共享 AppGroup 标识。为空时通过 Socket 握手传递配置，两者均无需申请 App Groups 能力；外部采集时无效。

#### AoqVideoCodecConfig

字段

类型

默认值

说明

trackType

AoqTrackType

AoqTrackTypeVideo

轨道类型

codecType

AoqEncoderType

AoqEncoderTypeVideoH264

编解码格式

width

NSInteger

540

宽度（像素）

height

NSInteger

960

高度（像素）

fps

NSInteger

5

帧率

bitrate

NSInteger

500000

码率（bps）

minBitrate

NSInteger

128000

最小码率（bps）

keyframeInterval

NSInteger

2

关键帧间隔（秒）

mirrorMode

AoqMirrorMode

AoqMirrorModeDisabled

镜像模式

orientationMode

AoqOrientationMode

AoqOrientationModeAuto

方向模式

isExternal

BOOL

NO

是否由应用输入已编码帧。

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

拉伸平铺模式，宽高比不一致时画面会变形

AoqRenderModeFill

2

填充黑边模式，宽高比不一致时上下或左右填充黑边

AoqRenderModeCrop

3

裁剪模式，宽高比不一致时裁剪宽或高，画面内容会丢失

#### AoqVideoCanvas

视频渲染画布。

字段

类型

默认值

说明

view

UIView \*

nil

显示视图，传 nil 表示移除渲染绑定（@Nullable）

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

后置摄像头（移动端有效）

#### AoqVideoCaptureConfig

视频采集配置。

字段

类型

默认值

说明

width

NSInteger

1280

采集宽度（像素），isExternal=YES 时无效

height

NSInteger

720

采集高度（像素），isExternal=YES 时无效

fps

NSInteger

15

采集帧率，isExternal=YES 时无效（节奏由送帧决定）

isExternal

BOOL

NO

是否外部采集；YES 时不打开摄像头，由 pushExternalVideoCapturedFrame: 喂帧

cameraDirection

AoqCameraDirection

AoqCameraDirectionFront

摄像头方向，isExternal=YES 时无效

#### AoqVideoPixelFormat

视频像素格式。

枚举值

值

说明

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

AoqVideoPixelFormatCVPixelBuffer

6

Apple 平台零拷贝路径，pixelBuffer 字段填 CVPixelBufferRef

**说明**iOS 不支持 TextureOES/Texture2D，零拷贝路径使用 CVPixelBuffer。

#### AoqVideoFrame

外部视频数据，同时用于视频帧回调（AoqVideoFrameDelegate）。

字段

类型

默认值

说明

format

AoqVideoPixelFormat

AoqVideoPixelFormatUnknown

像素格式

width

NSInteger

0

宽度（像素）

height

NSInteger

0

高度（像素）

data

NSData \*

nil

打包格式数据（NV12/NV21/BGRA/RGBA）（@Nullable）

dataY

NSData \*

nil

I420 Y 平面数据（@Nullable）

dataU

NSData \*

nil

I420 U 平面数据（@Nullable）

dataV

NSData \*

nil

I420 V 平面数据（@Nullable）

strideY

NSInteger

0

Y 平面行跨度

strideU

NSInteger

0

U 平面行跨度

strideV

NSInteger

0

V 平面行跨度

pixelBuffer

CVPixelBufferRef

NULL

Apple 零拷贝；format=AoqVideoPixelFormatCVPixelBuffer 时使用（@Nullable）

timeStamp

int64\_t

0

时间戳（毫秒）；0 时 SDK 用本地时钟补齐

**说明**iOS 无 textureId/transformMatrix/eglContext 字段，零拷贝改用 pixelBuffer。

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

NSData \*

非空

编码后数据

width

NSInteger

0

宽度（像素）

height

NSInteger

0

高度（像素）

timeStamp

int64\_t

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

NSInteger

0

错误原因代码（参考 AoqErrorCode）

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

读写模式，仅 I420/CVPixelBuffer 支持读写

mirrorApplied

BOOL

NO

是否对回调数据应用镜像

### 数据消息类型

#### AoqDataMsg

实时消息数据结构。

字段

类型

默认值

说明

data

NSData \*

空 NSData

消息数据，指向调用方持有的内存

### 统计数据类型

#### AoqStats

**字段**

**类型**

**说明**

audioPublishStats

NSArray<AoqAudioPublishStats \*> \*

音频推流统计

videoPublishStats

NSArray<AoqVideoPublishStats \*> \*

视频推流统计

dataMsgPublishStats

NSArray<AoqDataMsgPublishStats \*> \*

数据消息推流统计

audioSubscribeStats

NSArray<AoqAudioSubscribeStats \*> \*

音频拉流统计

videoSubscribeStats

NSArray<AoqVideoSubscribeStats \*> \*

视频拉流统计

dataMsgSubscribeStats

NSArray<AoqDataMsgSubscribeStats \*> \*

数据消息拉流统计

networkStats

AoqNetworkStats \*

网络统计

#### AoqNetworkStats

**字段**

**类型**

**说明**

sendBitrate

NSUInteger

发送码率(bps)

sendBytes

NSUInteger

累计发送字节

recvBitrate

NSUInteger

接收码率(bps)

recvBytes

NSUInteger

累计接收字节

loss

NSUInteger

丢包率

rtt

NSUInteger

往返时延(ms)

#### AoqAudioPublishStats

音频推流统计。

字段

类型

说明

trackType

AoqTrackType

轨道类型

bitrate

NSUInteger

码率（bps）

bytes

NSUInteger

累计发送字节数

encodeVolume

NSUInteger

推流编码音量

#### AoqVideoPublishStats

视频推流统计。

字段

类型

说明

trackType

AoqTrackType

轨道类型

bitrate

NSUInteger

码率（bps）

bytes

NSUInteger

累计发送字节数

encodeFps

NSUInteger

编码帧率

#### AoqAudioSubscribeStats

音频拉流统计。

字段

类型

说明

trackType

AoqTrackType

轨道类型

bitrate

NSUInteger

码率（bps）

bytes

NSUInteger

累计接收字节数

playVolume

NSUInteger

播放音量

#### AoqVideoSubscribeStats

视频拉流统计。

字段

类型

说明

trackType

AoqTrackType

轨道类型

bitrate

NSUInteger

码率（bps）

bytes

NSUInteger

累计接收字节数

decodeFps

NSUInteger

解码帧率

renderFps

NSUInteger

渲染帧率

#### AoqDataMsgPublishStats

数据消息推流统计。

字段

类型

说明

trackType

AoqTrackType

轨道类型

bitrate

NSUInteger

码率（bps）

bytes

NSUInteger

累计发送字节数

#### AoqDataMsgSubscribeStats

数据消息拉流统计。

字段

类型

说明

trackType

AoqTrackType

轨道类型

bitrate

NSUInteger

码率（bps）

bytes

NSUInteger

累计接收字节数
