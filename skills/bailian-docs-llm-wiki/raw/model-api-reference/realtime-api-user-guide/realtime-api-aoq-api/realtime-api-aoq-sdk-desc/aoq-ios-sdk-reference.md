# AOQ Client SDK iOS API 参考

AOQ Client SDK iOS API 参考，涵盖引擎生命周期、音视频设备管理、编码配置、媒体流控制、音频文件播放、外部音频流、实时消息、帧回调、委托协议以及数据类型与枚举。

## 目录

### 引擎生命周期

**接口**

**简介**

createEngine:delegate:

创建引擎实例（单例模式）

destroy

销毁引擎实例

getVersion

获取 SDK 版本号

connect:

连接 Relay 服务器

disconnect

断开服务器连接

### 音频设备管理

**接口**

**简介**

startAudioCapture:

打开音频采集设备（麦克风）

stopAudioCapture

关闭音频采集设备

muteAudioCapture:

静音或取消静音音频采集

startAudioPlayer:

开始音频渲染（播放远端音频）

stopAudioPlayer

停止音频渲染

pauseAudioPlayer:

暂停音频渲染，支持淡出

resumeAudioPlayer:

恢复音频渲染，支持淡入

interruptAudioPlayer:fadeMs:

打断本轮音频通话

enableSpeakerphone:

切换音频输出到扬声器或听筒

isSpeakerphoneEnabled

查询当前是否使用扬声器输出

setAudioSessionRestriction:

设置 AVAudioSession 控制权限

enableLocalAudioVolumeIndication:

配置本地采集音量提示

### 音频编码配置

**接口**

**简介**

setAudioEncoderConfig:

设置音频编码参数

setAudioDecoderConfig:

设置音频解码参数

### 视频设备管理

**接口**

**简介**

startVideoCapture:

打开视频采集设备（摄像头）

stopVideoCapture

关闭视频采集设备

switchCamera:

切换前后置摄像头

setLocalView:canvas:

设置或移除本地视频渲染窗口

setRemoteView:canvas:

设置或移除远端视频渲染窗口

startScreenCapture:

开始屏幕采集

stopScreenCapture

停止屏幕采集

### 视频编码与外部输入

**接口**

**简介**

setVideoEncoderConfig:

设置视频编码参数

pushExternalVideoCapturedFrame:frame:

推送外部采集视频帧

pushExternalVideoEncodedFrame:frame:

推送外部已编码视频帧

setVideoDecoderConfig:

设置视频解码参数

### 媒体流发送控制

**接口**

**简介**

enableSendMediaStream:enable:

控制本地媒体流的发送开关

### 音频文件播放

**接口**

**简介**

startAudioFile:config:

开始推流播放本地音频文件

stopAudioFile:

停止音频文件播放

pauseAudioFile:

暂停音频文件播放

resumeAudioFile:

恢复音频文件播放

getAudioFileDuration:

获取音频文件总时长

getAudioFileCurrentPosition:

获取音频文件当前播放位置

setAudioFilePositionMillis:positionMillis:

设置音频文件播放位置（seek）

setAudioFileVolume:type:volume:

设置音频文件音量

getAudioFileVolume:type:

获取音频文件当前音量

### 外部音频流

**接口**

**简介**

addAudioExternalStream:config:

新增一条外部音频流

removeAudioExternalStream:

移除外部音频流

pushAudioExternalStreamData:data:

输入外部音频 PCM 数据

setAudioExternalStreamVolume:type:volume:

设置外部音频流音量

getAudioExternalStreamVolume:type:

获取外部音频流音量

clearAudioExternalStreamBuffer:fadeoutMs:

清空外部音频流缓存

### 实时消息

**接口**

**简介**

sendDataMsg:

发送实时数据消息

### 音频帧回调

**接口**

**简介**

setAudioFrameObserver:

设置音频帧数据回调 delegate

enableAudioFrameObserver:audioSource:config:

开启或关闭指定位置的音频帧回调

### 视频帧回调

**接口**

**简介**

setVideoFrameObserver:

设置视频帧数据回调 delegate

enableVideoFrameObserver:videoSource:config:

开启或关闭指定位置的视频帧回调

### AoqEngineDelegate 回调

**回调**

**简介**

onError:message:

引擎错误回调

onWarning:message:

引擎警告回调

onConnectionStatusChange:

连接状态变化回调

onStats:

统计数据回调

onAudioDeviceStateChanged:

音频设备操作状态变化回调

onAudioDeviceRouteChanged:

音频输出路由变化回调

onAudioDeviceInterrupted:

音频设备中断回调

onVideoDeviceStateChanged:

视频设备操作状态变化回调

onAudioFileState:

音频文件播放状态回调

onDataMsg:

收到实时数据消息回调

AoqAudioFrameDelegate

音频帧数据监听协议

AoqVideoFrameDelegate

视频帧数据监听协议

onLocalAudioVolumeIndication

本地采集音量回调

onScreenCaptureStateChanged

屏幕采集状态回调

## 接口详情

### 屏幕采集

```
- (int)startScreenCapture:(AoqScreenCaptureConfig * _Nonnull)config;
- (int)stopScreenCapture;
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

启动返回 0 表示请求已受理，最终状态通过 `onScreenCaptureStateChanged` 通知；非 0 表示同步拒绝，不重复报告失败事件。停止返回 0 表示成功，非 0 表示失败，停止结果由该回调通知。

`isExternal=NO` 时使用 Broadcast Upload Extension。应用需集成并配置 `AoqScreenShare.framework`，展示系统广播选择器；等待超时通过 `onScreenCaptureStateChanged:` 回调报告失败，错误码为 `AoqECScreenStartFailed`。无需等待 Started 才启用发送。

外部原始帧：设置 `isExternal=YES` 后，不启用 Extension 接收通道，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`；不需要调用 `startScreenCapture`。

#### onScreenCaptureStateChanged

```
@optional
- (void)onScreenCaptureStateChanged:(AoqScreenCaptureState * _Nonnull)state;
```

`state` 为屏幕采集状态。Started 表示采集或外部输入已就绪，不代表媒体已发送。屏幕采集失败不重复通过 `onError` 上报。

### setVideoDecoderConfig:

```
- (int)setVideoDecoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

`config` 为视频解码配置。仅以下字段生效：`trackType`, `codecType`, `width`, `height`, `fps`, `bitrate`. 其余字段仅用于编码。

Screen 不支持下行解码。`config.trackType` 为 Screen 时返回 `AoqECUnSupport`，配置不下发。

返回值：0 表示成功；非 0 表示失败。

### enableLocalAudioVolumeIndication:

```
- (int)enableLocalAudioVolumeIndication:(AoqAudioVolumeIndicationConfig * _Nonnull)config;
```

`config` 为音量提示配置。开启后按 `config.interval` 周期回调；需在 `startAudioCapture` 之后调用此接口。

返回值：0 表示成功；非 0 表示失败。

```
- (void)onLocalAudioVolumeIndication:(AoqAudioVolume * _Nonnull)volume;
```

回调参数 `volume` 为本地采集音量。

### 引擎生命周期

#### createEngine:delegate:

创建引擎实例。SDK 内部以全局单例方式持有引擎。

```
+ (instancetype _Nonnull)createEngine:(AoqCreateConfig * _Nonnull)config
                             delegate:(id<AoqEngineDelegate> _Nonnull)delegate;
```

#### destroy

```
+ (int)destroy;
```

#### getVersion

```
+ (NSString * _Nonnull)getVersion;
```

#### connect:

```
- (int)connect:(AoqConnectConfig * _Nonnull)config;
```

#### disconnect

```
- (int)disconnect;
```

### 音频设备管理

```
- (int)startAudioCapture:(AoqAudioCaptureConfig * _Nonnull)config;
- (int)stopAudioCapture;
- (int)muteAudioCapture:(BOOL)mute;
- (int)startAudioPlayer:(AoqAudioPlaybackConfig * _Nonnull)config;
- (int)stopAudioPlayer;
- (int)pauseAudioPlayer:(NSInteger)fadeMs;
- (int)resumeAudioPlayer:(NSInteger)fadeMs;
- (int)interruptAudioPlayer:(AoqTrackType)trackType fadeMs:(NSInteger)fadeMs;
- (int)enableSpeakerphone:(BOOL)enable;
- (BOOL)isSpeakerphoneEnabled;
- (int)setAudioSessionRestriction:(int)restriction;
```

### 音频编码配置

```
- (int)setAudioEncoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
- (int)setAudioDecoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

### 视频设备管理

```
- (int)startVideoCapture:(AoqVideoCaptureConfig * _Nonnull)config;
- (int)stopVideoCapture;
- (int)switchCamera:(AoqCameraDirection)direction;
- (int)setLocalView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
- (int)setRemoteView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

setLocalView/setRemoteView 的 trackType 参数传 AoqTrackTypeVideo。

### 视频编码与外部输入

```
- (int)setVideoEncoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
- (int)pushExternalVideoCapturedFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (int)pushExternalVideoEncodedFrame:(AoqTrackType)trackType frame:(AoqVideoEncodedFrame * _Nonnull)frame;
```

trackType 参数传 AoqTrackTypeVideo。

### 媒体流发送控制

```
- (int)enableSendMediaStream:(AoqTrackType)trackType enable:(BOOL)enable;
```

trackType 支持 AoqTrackTypeAudio / AoqTrackTypeVideo / AoqTrackTypeScreen。

### 音频文件播放

```
- (int)startAudioFile:(NSString * _Nonnull)fileId config:(AoqAudioFileMixConfig * _Nonnull)config;
- (int)stopAudioFile:(NSString * _Nonnull)fileId;
- (int)pauseAudioFile:(NSString * _Nonnull)fileId;
- (int)resumeAudioFile:(NSString * _Nonnull)fileId;
- (long long)getAudioFileDuration:(NSString * _Nonnull)fileId;
- (long long)getAudioFileCurrentPosition:(NSString * _Nonnull)fileId;
- (int)setAudioFilePositionMillis:(NSString * _Nonnull)fileId positionMillis:(long long)positionMillis;
- (int)setAudioFileVolume:(NSString * _Nonnull)fileId type:(AoqAudioStreamDirection)type volume:(NSInteger)volume;
- (int)getAudioFileVolume:(NSString * _Nonnull)fileId type:(AoqAudioStreamDirection)type;
```

### 外部音频流

```
- (int)addAudioExternalStream:(NSString * _Nonnull)streamId config:(AoqAudioExternalStreamConfig * _Nonnull)config;
- (int)pushAudioExternalStreamData:(NSString * _Nonnull)streamId data:(AoqAudioFrameData * _Nonnull)data;
- (int)setAudioExternalStreamVolume:(NSString * _Nonnull)streamId type:(AoqAudioStreamDirection)type volume:(NSInteger)volume;
- (int)getAudioExternalStreamVolume:(NSString * _Nonnull)streamId type:(AoqAudioStreamDirection)type;
- (void)clearAudioExternalStreamBuffer:(NSString * _Nonnull)streamId fadeoutMs:(NSInteger)fadeoutMs;
- (int)removeAudioExternalStream:(NSString * _Nonnull)streamId;
```

### 实时消息

```
- (int)sendDataMsg:(AoqDataMsg * _Nonnull)msg;
```

### 音频帧回调

```
- (int)setAudioFrameObserver:(id<AoqAudioFrameDelegate> _Nullable)delegate;
- (int)enableAudioFrameObserver:(BOOL)enabled audioSource:(AoqAudioSource)audioSource config:(AoqAudioObserverConfig * _Nonnull)config;
```

### 视频帧回调

```
- (int)setVideoFrameObserver:(id<AoqVideoFrameDelegate> _Nullable)delegate;
- (int)enableVideoFrameObserver:(BOOL)enabled videoSource:(AoqVideoSource)videoSource config:(AoqVideoObserverConfig * _Nonnull)config;
```

### AoqEngineDelegate 回调

`onScreenCaptureStateChanged:` 为 `@optional`，其余 `AoqEngineDelegate` 回调方法为 `@required`。

```
- (void)onError:(NSInteger)code message:(NSString * _Nonnull)message;
- (void)onWarning:(NSInteger)code message:(NSString * _Nonnull)message;
- (void)onConnectionStatusChange:(AoqConnectionStatus)status;
- (void)onStats:(AoqStats * _Nonnull)stats;
- (void)onAudioDeviceStateChanged:(AoqAudioDeviceState * _Nonnull)state;
- (void)onAudioDeviceRouteChanged:(NSInteger)routeType;
- (void)onAudioDeviceInterrupted:(BOOL)interrupt;
- (void)onAudioFileState:(AoqAudioFileState * _Nonnull)state;
- (void)onVideoDeviceStateChanged:(AoqVideoDeviceState * _Nonnull)state;
- (void)onDataMsg:(AoqDataMsg * _Nonnull)msg;
```

#### AoqAudioFrameDelegate (@optional)

```
- (void)onCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onProcessCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onPublishAudioFrame:(AoqTrackType)trackType frame:(AoqAudioFrameData * _Nonnull)frame;
- (void)onPlaybackAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

#### AoqVideoFrameDelegate (@optional)

```
- (BOOL)onCapturedVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (BOOL)onPreEncodeVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
- (BOOL)onRemoteVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
```

## 数据类型与枚举

### AoqScreenCaptureState

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

### AoqScreenCaptureStateCode

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

### AoqScreenCaptureConfig

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

### AoqVideoCodecConfig

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

### AoqAudioVolume

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

### AoqAudioVolumeIndicationConfig

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

### AoqTrackParam.trackMode

字段

类型

默认值

说明

trackMode

AoqTrackMode

AoqTrackModeSegment

仅对音频下行生效。

### AoqTrackMode

枚举值

值

说明

AoqTrackModeSegment

0

分段：按语义片段（如一句话）交付数据；仅对音频下行生效。

AoqTrackModeStream

1

流式：连续交付数据；仅对音频下行生效。

### AoqCreateConfig（v1.3.0 新增字段）

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

### AoqErrorCode

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

### AoqTrackType

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

### AoqConnectConfig

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

### AoqAudioPlaybackConfig

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

trackType / bitrate / bytes / encodeVolume

#### AoqVideoPublishStats

trackType / bitrate / bytes / encodeFps

#### AoqAudioSubscribeStats

trackType / bitrate / bytes / playVolume

#### AoqVideoSubscribeStats

trackType / bitrate / bytes / decodeFps / renderFps

#### AoqDataMsgPublishStats / AoqDataMsgSubscribeStats

trackType / bitrate / bytes

## 与 Android 版本的主要差异

**差异点**

**iOS**

**Android**

回调模式

@protocol delegate

abstract class listener

AVAudioSession 控制

setAudioSessionRestriction:（iOS 独有）

无对应接口

音频焦点回调

无（iOS 用 onAudioDeviceInterrupted: 代替）

onAudioDeviceFocusChanged

视频像素格式

支持 CVPixelBuffer 零拷贝

支持 TextureOES / Texture2D

视频渲染 View

UIView

SurfaceView / TextureView

蓝牙模式配置

无 isBTScoMode（系统自动管理）

AoqCreateConfig.isBTScoMode

视频帧回调写回

I420 / CVPixelBuffer

I420
