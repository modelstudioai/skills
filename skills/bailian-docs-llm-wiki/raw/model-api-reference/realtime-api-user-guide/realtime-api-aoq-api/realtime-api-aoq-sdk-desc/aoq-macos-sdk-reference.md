# AOQ Client SDK macOS API 参考

本文介绍 AOQ Client SDK macOS 版的 Objective-C 接口、回调和数据类型，帮助您在 macOS 应用中接入实时音视频和数据消息能力。

SDK 以全局单例方式持有引擎实例，通过 `AoqClientEngine` 类对外提供接口，通过 `AoqEngineDelegate` 协议统一回调异步事件。

## 接口目录

### 引擎生命周期

**接口**

**简介**

`createEngine:delegate:`

创建引擎实例（单例模式）

`destroy`

销毁引擎实例

`getVersion`

获取 SDK 版本号

`connect:`

连接 Relay 服务器

`disconnect`

断开服务器连接

### 音频设备管理

**接口**

**简介**

`startAudioCapture:`

打开音频采集设备（麦克风）

`stopAudioCapture`

关闭音频采集设备

`muteAudioCapture:`

静音或取消静音音频采集

`startAudioPlayer:`

开始音频渲染（播放远端音频）

`stopAudioPlayer`

停止音频渲染

`pauseAudioPlayer:`

暂停音频渲染（支持淡出）

`resumeAudioPlayer:`

恢复音频渲染（支持淡入）

`interruptAudioPlayer:fadeMs:`

打断本轮音频通话

`enableLocalAudioVolumeIndication:`

开启或关闭本地采集音量提示

### 音频编码配置

**接口**

**简介**

`setAudioEncoderConfig:`

设置音频编码参数

`setAudioDecoderConfig:`

设置音频解码参数

### 视频设备管理

**接口**

**简介**

`startVideoCapture:`

打开视频采集设备（摄像头）

`stopVideoCapture`

关闭视频采集设备

`setLocalView:canvas:`

设置或移除本地视频渲染窗口

`setRemoteView:canvas:`

设置或移除远端视频渲染窗口

getScreenSourceList

获取屏幕和窗口源

startScreenCapture:

开始屏幕采集

stopScreenCapture

停止屏幕采集

### 视频编码与外部输入

**接口**

**简介**

`setVideoEncoderConfig:`

设置视频编码参数

`setVideoDecoderConfig:`

设置视频解码参数

`pushExternalVideoCapturedFrame:frame:`

推送外部采集视频帧

`pushExternalVideoEncodedFrame:frame:`

推送外部已编码视频帧

### 媒体流发送控制

**接口**

**简介**

`enableSendMediaStream:enable:`

控制本地媒体流的发送开关

### 音频文件播放

**接口**

**简介**

`startAudioFile:config:`

开始推流播放本地音频文件

`stopAudioFile:`

停止音频文件播放

`pauseAudioFile:`

暂停音频文件播放

`resumeAudioFile:`

恢复音频文件播放

`getAudioFileDuration:`

获取音频文件总时长

`getAudioFileCurrentPosition:`

获取音频文件当前播放位置

`setAudioFilePositionMillis:positionMillis:`

设置音频文件播放位置（seek）

`setAudioFileVolume:type:volume:`

设置音频文件音量

`getAudioFileVolume:type:`

获取音频文件当前音量

### 外部音频流

**接口**

**简介**

`addAudioExternalStream:config:`

新增一条外部音频流

`pushAudioExternalStreamData:data:`

输入外部音频 PCM 数据

`setAudioExternalStreamVolume:type:volume:`

设置外部音频流音量

`getAudioExternalStreamVolume:type:`

获取外部音频流音量

`clearAudioExternalStreamBuffer:fadeoutMs:`

清空外部音频流缓存

`removeAudioExternalStream:`

移除外部音频流

### 实时消息

**接口**

**简介**

`sendDataMsg:`

发送实时数据消息

### 音频帧回调

**接口**

**简介**

`setAudioFrameObserver:`

设置音频帧数据回调监听

`enableAudioFrameObserver:audioSource:config:`

开启或关闭指定位置的音频帧回调

### 视频帧回调

**接口**

**简介**

`setVideoFrameObserver:`

设置视频帧数据回调监听

`enableVideoFrameObserver:videoSource:config:`

开启或关闭指定位置的视频帧回调

### AoqEngineDelegate 回调

**回调**

**简介**

`onError:message:`

引擎错误回调

`onWarning:message:`

引擎警告回调

`onConnectionStatusChange:`

连接状态变化回调

`onStats:`

引擎统计信息回调

`onAudioDeviceStateChanged:`

音频设备操作状态变化回调

`onAudioDeviceRouteChanged:`

音频输出路由变化回调

`onAudioFileState:`

音频文件播放状态回调

`onLocalAudioVolumeIndication:`

本地采集音量提示回调

`onVideoDeviceStateChanged:`

视频设备操作状态变化回调

`onDataMsg:`

收到实时数据消息回调

## 接口详情

### 屏幕采集

```
- (int)startScreenCapture:(AoqScreenCaptureConfig * _Nonnull)config;
- (int)stopScreenCapture;
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

返回值：0 表示成功；非 0 表示失败。 接口同步返回，不提供 `onScreenCaptureStateChanged` 回调。

先调用 `getScreenSourceList` 获取屏幕或窗口源，再将选定的 `sourceId` 和 `sourceType` 传入采集配置。

外部原始帧：设置 `isExternal=YES` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`。

#### getScreenSourceList

```
- (AoqScreenSourceList * _Nullable)getScreenSourceList;
```

返回屏幕源列表，失败返回 nil。

### 引擎生命周期

#### createEngine:delegate:

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

```
+ (instancetype _Nonnull)createEngine:(AoqCreateConfig * _Nonnull)config
                             delegate:(id<AoqEngineDelegate> _Nonnull)delegate;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqCreateConfig *`

引擎创建配置，详见 `AoqCreateConfig`

`delegate`

`id<AoqEngineDelegate>`

引擎事件回调委托，详见 `AoqEngineDelegate`

返回值：引擎实例，不会返回 nil。

#### destroy

销毁引擎实例。销毁后需重新调用 `createEngine:delegate:` 方可继续使用。

```
+ (int)destroy;
```

返回值：0 表示成功；非 0 表示失败。

#### getVersion

获取 SDK 的版本号。

```
+ (NSString * _Nonnull)getVersion;
```

返回值：版本号字符串。

#### connect:

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

```
- (int)connect:(AoqConnectConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqConnectConfig *`

连接鉴权配置，详见 `AoqConnectConfig`

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

#### disconnect

断开服务器连接。

```
- (int)disconnect;
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

### 音频设备管理

#### startAudioCapture:

打开音频采集设备（麦克风）。

```
- (int)startAudioCapture:(AoqAudioCaptureConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqAudioCaptureConfig *`

音频采集配置，详见 `AoqAudioCaptureConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopAudioCapture

关闭音频采集设备。

```
- (int)stopAudioCapture;
```

返回值：0 表示成功；非 0 表示失败。

#### muteAudioCapture:

静音或取消静音音频采集。

```
- (int)muteAudioCapture:(BOOL)mute;
```

参数

**参数**

**类型**

**说明**

`mute`

`BOOL`

`YES` 静音；`NO` 取消静音

返回值：0 表示成功；非 0 表示失败。

#### startAudioPlayer:

开始音频渲染，播放远端音频。

```
- (int)startAudioPlayer:(AoqAudioPlaybackConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqAudioPlaybackConfig *`

音频播放配置，详见 `AoqAudioPlaybackConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopAudioPlayer

停止音频渲染。

```
- (int)stopAudioPlayer;
```

返回值：0 表示成功；非 0 表示失败。

#### pauseAudioPlayer:

暂停音频渲染，支持淡出。

```
- (int)pauseAudioPlayer:(NSInteger)fadeMs;
```

参数

**参数**

**类型**

**说明**

`fadeMs`

`NSInteger`

淡出时长，单位毫秒；0 表示立即暂停

返回值：0 表示成功；非 0 表示失败。

#### resumeAudioPlayer:

恢复音频渲染，支持淡入。

```
- (int)resumeAudioPlayer:(NSInteger)fadeMs;
```

参数

**参数**

**类型**

**说明**

`fadeMs`

`NSInteger`

淡入时长，单位毫秒；0 表示立即恢复

返回值：0 表示成功；非 0 表示失败。

#### interruptAudioPlayer:fadeMs:

打断本轮音频通话，停止当前正在播放的音频内容。

```
- (int)interruptAudioPlayer:(AoqTrackType)trackType fadeMs:(NSInteger)fadeMs;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

音轨类型，详见 `AoqTrackType`

`fadeMs`

`NSInteger`

淡出时长，单位毫秒；0 表示立即打断

返回值：0 表示成功；非 0 表示失败。

#### enableLocalAudioVolumeIndication:

开启或关闭本地采集音量提示。开启后按 `config.interval` 周期触发 `onLocalAudioVolumeIndication:` 回调；`config.interval <= 0` 时关闭回调。需在 `startAudioCapture:` 之后调用才有音量数据。

```
- (int)enableLocalAudioVolumeIndication:(AoqAudioVolumeIndicationConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqAudioVolumeIndicationConfig *`

音量提示配置，详见 `AoqAudioVolumeIndicationConfig`

返回值：0 表示成功；非 0 表示失败。

### 音频编码配置

#### setAudioEncoderConfig:

设置音频编码参数。

```
- (int)setAudioEncoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqAudioCodecConfig *`

音频编解码配置，详见 `AoqAudioCodecConfig`

返回值：0 表示成功；非 0 表示失败。

#### setAudioDecoderConfig:

设置音频解码参数。

```
- (int)setAudioDecoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqAudioCodecConfig *`

音频编解码配置，详见 `AoqAudioCodecConfig`

返回值：0 表示成功；非 0 表示失败。

### 视频设备管理

#### startVideoCapture:

打开视频采集设备（摄像头）。配置 `isExternal=YES` 时不打开摄像头，由 `pushExternalVideoCapturedFrame:frame:` 喂帧。

```
- (int)startVideoCapture:(AoqVideoCaptureConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqVideoCaptureConfig *`

视频采集配置，详见 `AoqVideoCaptureConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopVideoCapture

关闭视频采集设备。

```
- (int)stopVideoCapture;
```

返回值：0 表示成功；非 0 表示失败。

#### setLocalView:canvas:

设置或移除本地视频渲染窗口。`canvas` 传 nil 或 `canvas.view` 为 nil 表示解绑。

```
- (int)setLocalView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道，传 `AoqTrackTypeVideo`

`canvas`

`AoqVideoCanvas *`

渲染画布，详见 `AoqVideoCanvas`；传 nil 表示解绑

返回值：0 表示成功；非 0 表示失败。

#### setRemoteView:canvas:

设置或移除远端视频渲染窗口。`canvas` 传 nil 或 `canvas.view` 为 nil 表示解绑。

```
- (int)setRemoteView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道，传 `AoqTrackTypeVideo`

`canvas`

`AoqVideoCanvas *`

渲染画布，详见 `AoqVideoCanvas`；传 nil 表示解绑

返回值：0 表示成功；非 0 表示失败。

### 视频编码与外部输入

#### setVideoEncoderConfig:

设置视频编码参数，按 `config.trackType` 路由。

```
- (int)setVideoEncoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqVideoCodecConfig *`

视频编解码配置，详见 `AoqVideoCodecConfig`

返回值：0 表示成功；非 0 表示失败。

#### setVideoDecoderConfig:

设置视频解码参数（订阅侧 codec 提议，需在 `connect:` 之前调用），按 `config.trackType` 路由。

```
- (int)setVideoDecoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`config`

`AoqVideoCodecConfig *`

视频编解码配置，详见 `AoqVideoCodecConfig`

返回值：0 表示成功；非 0 表示失败。

#### pushExternalVideoCapturedFrame:frame:

推送外部视频帧。需先调用 `startVideoCapture:` 且配置 `isExternal=YES`，未启动外部视频采集或格式不支持时返回 `AoqECParamInvalid`。

```
- (int)pushExternalVideoCapturedFrame:(AoqTrackType)trackType
                                frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

路由目标，传 `AoqTrackTypeVideo`

；也支持 AoqTrackTypeScreen

`frame`

`AoqVideoFrame *`

外部视频帧数据，详见 `AoqVideoFrame`

返回值：0 表示成功；`AoqECVideoExternalBufferFull`（210）表示缓冲区满；<0 表示其他错误。

#### pushExternalVideoEncodedFrame:frame:

推送外部已编码视频帧，bypass 编码器直推。需先调用 `setVideoEncoderConfig:` 且配置 `isExternal=YES`，当前仅支持 JPEG。

```
- (int)pushExternalVideoEncodedFrame:(AoqTrackType)trackType
                               frame:(AoqVideoEncodedFrame * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

路由目标，传 `AoqTrackTypeVideo`

；也支持 AoqTrackTypeScreen

`frame`

`AoqVideoEncodedFrame *`

外部已编码帧数据，详见 `AoqVideoEncodedFrame`

返回值：0 表示成功；非 0 表示失败。

### 媒体流发送控制

#### enableSendMediaStream:enable:

控制本地媒体流的发送开关。建议初始化后先关闭发送，待 `onConnectionStatusChange:` 回调 `AoqConnectionStatusConnected` 后再开启。

```
- (int)enableSendMediaStream:(AoqTrackType)trackType enable:(BOOL)enable;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

路由目标，支持 `AoqTrackTypeAudio` / `AoqTrackTypeVideo`

；支持 AoqTrackTypeScreen

`enable`

`BOOL`

`YES` 启用发送；`NO` 停用发送

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

### 音频文件播放

#### startAudioFile:config:

开始推流播放本地音频文件。

```
- (int)startAudioFile:(NSString * _Nonnull)fileId
               config:(AoqAudioFileMixConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID，业务层需保证唯一性

`config`

`AoqAudioFileMixConfig *`

音频文件混音配置，详见 `AoqAudioFileMixConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopAudioFile:

停止音频文件播放。

```
- (int)stopAudioFile:(NSString * _Nonnull)fileId;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

返回值：0 表示成功；非 0 表示失败。

#### pauseAudioFile:

暂停音频文件播放。

```
- (int)pauseAudioFile:(NSString * _Nonnull)fileId;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

返回值：0 表示成功；非 0 表示失败。

#### resumeAudioFile:

恢复音频文件播放。

```
- (int)resumeAudioFile:(NSString * _Nonnull)fileId;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

返回值：0 表示成功；非 0 表示失败。

#### getAudioFileDuration:

获取音频文件总时长。

```
- (long long)getAudioFileDuration:(NSString * _Nonnull)fileId;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

返回值：>=0 表示音频文件时长，单位毫秒；<0 表示失败。

#### getAudioFileCurrentPosition:

获取音频文件当前播放位置。

```
- (long long)getAudioFileCurrentPosition:(NSString * _Nonnull)fileId;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

返回值：>=0 表示当前播放位置，单位毫秒；<0 表示失败。

#### setAudioFilePositionMillis:positionMillis:

设置音频文件播放位置（seek）。

```
- (int)setAudioFilePositionMillis:(NSString * _Nonnull)fileId
                  positionMillis:(long long)positionMillis;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

`positionMillis`

`long long`

播放位置，单位毫秒

返回值：0 表示成功；非 0 表示失败。

#### setAudioFileVolume:type:volume:

设置音频文件音量。

```
- (int)setAudioFileVolume:(NSString * _Nonnull)fileId
                     type:(AoqAudioStreamDirection)type
                   volume:(NSInteger)volume;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

`type`

`AoqAudioStreamDirection`

音频流方向，详见 `AoqAudioStreamDirection`

`volume`

`NSInteger`

音量值，范围 \[0, 100\]

返回值：0 表示成功；非 0 表示失败。

#### getAudioFileVolume:type:

获取音频文件当前音量。

```
- (int)getAudioFileVolume:(NSString * _Nonnull)fileId
                     type:(AoqAudioStreamDirection)type;
```

参数

**参数**

**类型**

**说明**

`fileId`

`NSString *`

音频文件 ID

`type`

`AoqAudioStreamDirection`

音频流方向，详见 `AoqAudioStreamDirection`

返回值：\[0, 100\] 表示音量值；<0 表示失败。

### 外部音频流

#### addAudioExternalStream:config:

新增一条外部音频流。

```
- (int)addAudioExternalStream:(NSString * _Nonnull)streamId
                       config:(AoqAudioExternalStreamConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`streamId`

`NSString *`

外部音频流 ID，业务层需保证唯一性

`config`

`AoqAudioExternalStreamConfig *`

外部音频流配置，详见 `AoqAudioExternalStreamConfig`

返回值：0 表示成功；非 0 表示失败。

#### pushAudioExternalStreamData:data:

输入外部音频 PCM 数据。返回 `AoqECAudioExternalBufferFull`（110）时表示 SDK 缓存已满，建议等待约 20ms 后重新送当前数据帧。

```
- (int)pushAudioExternalStreamData:(NSString * _Nonnull)streamId
                              data:(AoqAudioFrameData * _Nonnull)data;
```

参数

**参数**

**类型**

**说明**

`streamId`

`NSString *`

外部音频流 ID

`data`

`AoqAudioFrameData *`

外部音频裸数据，详见 `AoqAudioFrameData`

返回值：0 表示成功；非 0 表示失败。

**说明**最佳实践：实时采集场景一次 Push 10ms 数据长度，有数据即 Push；数据来源为文件时一次 Push 40ms 数据长度、间隔 30ms 给一次，并处理 `AoqECAudioExternalBufferFull` 返回。

#### setAudioExternalStreamVolume:type:volume:

设置外部音频流音量。

```
- (int)setAudioExternalStreamVolume:(NSString * _Nonnull)streamId
                               type:(AoqAudioStreamDirection)type
                             volume:(NSInteger)volume;
```

参数

**参数**

**类型**

**说明**

`streamId`

`NSString *`

外部音频流 ID

`type`

`AoqAudioStreamDirection`

外部音频流类型，详见 `AoqAudioStreamDirection`

`volume`

`NSInteger`

音量值，范围 \[0, 100\]

返回值：0 表示成功；非 0 表示失败。

#### getAudioExternalStreamVolume:type:

获取外部音频流音量。

```
- (int)getAudioExternalStreamVolume:(NSString * _Nonnull)streamId
                               type:(AoqAudioStreamDirection)type;
```

参数

**参数**

**类型**

**说明**

`streamId`

`NSString *`

外部音频流 ID

`type`

`AoqAudioStreamDirection`

外部音频流类型，详见 `AoqAudioStreamDirection`

返回值：\[0, 100\] 表示音量值；<0 表示失败。

#### clearAudioExternalStreamBuffer:fadeoutMs:

清空外部音频流缓存。

```
- (void)clearAudioExternalStreamBuffer:(NSString * _Nonnull)streamId
                              fadeoutMs:(NSInteger)fadeoutMs;
```

参数

**参数**

**类型**

**说明**

`streamId`

`NSString *`

外部音频流 ID

`fadeoutMs`

`NSInteger`

淡出时长；-1 使用 SDK 内部默认淡出，0 表示全部清空无淡出，>0 保留指定毫秒淡出

返回值：无。

#### removeAudioExternalStream:

移除外部音频流。

```
- (int)removeAudioExternalStream:(NSString * _Nonnull)streamId;
```

参数

**参数**

**类型**

**说明**

`streamId`

`NSString *`

外部音频流 ID

返回值：0 表示成功；非 0 表示失败。

### 实时消息

#### sendDataMsg:

发送实时数据消息。

```
- (int)sendDataMsg:(AoqDataMsg * _Nonnull)msg;
```

参数

**参数**

**类型**

**说明**

`msg`

`AoqDataMsg *`

消息内容，详见 `AoqDataMsg`

返回值：0 表示成功；非 0 表示失败。

### 音频帧回调

#### setAudioFrameObserver:

设置音频帧数据回调委托，传 nil 停止回调。设置后需调用 `enableAudioFrameObserver:audioSource:config:` 开启对应数据源的回调。

```
- (int)setAudioFrameObserver:(id<AoqAudioFrameDelegate> _Nullable)delegate;
```

参数

**参数**

**类型**

**说明**

`delegate`

`id<AoqAudioFrameDelegate>`

音频帧回调委托，详见 `AoqAudioFrameDelegate`；传 nil 停止回调

返回值：0 表示成功；非 0 表示失败。

#### enableAudioFrameObserver:audioSource:config:

开启或关闭指定位置的音频帧回调。

```
- (int)enableAudioFrameObserver:(BOOL)enabled
                   audioSource:(AoqAudioSource)audioSource
                        config:(AoqAudioObserverConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`enabled`

`BOOL`

是否允许数据回调

`audioSource`

`AoqAudioSource`

音频裸数据源类型，详见 `AoqAudioSource`

`config`

`AoqAudioObserverConfig *`

回调参数设置，详见 `AoqAudioObserverConfig`

返回值：0 表示成功；非 0 表示失败。

### 视频帧回调

#### setVideoFrameObserver:

设置视频帧数据回调委托，传 nil 停止回调。设置后需调用 `enableVideoFrameObserver:videoSource:config:` 开启对应数据源的回调。

```
- (int)setVideoFrameObserver:(id<AoqVideoFrameDelegate> _Nullable)delegate;
```

参数

**参数**

**类型**

**说明**

`delegate`

`id<AoqVideoFrameDelegate>`

视频帧回调委托，详见 `AoqVideoFrameDelegate`；传 nil 停止回调

返回值：0 表示成功；非 0 表示失败。

#### enableVideoFrameObserver:videoSource:config:

开启或关闭指定位置的视频帧回调。

```
- (int)enableVideoFrameObserver:(BOOL)enabled
                    videoSource:(AoqVideoSource)videoSource
                         config:(AoqVideoObserverConfig * _Nonnull)config;
```

参数

**参数**

**类型**

**说明**

`enabled`

`BOOL`

是否启用某位置数据回调

`videoSource`

`AoqVideoSource`

视频帧回调数据源（管线位置），详见 `AoqVideoSource`

`config`

`AoqVideoObserverConfig *`

回调参数设置，详见 `AoqVideoObserverConfig`

返回值：0 表示成功；非 0 表示失败。

## 回调

### AoqEngineDelegate

`AoqEngineDelegate` 是 SDK 所有异步事件通知的统一出口，在 `createEngine:delegate:` 时传入。所有回调方法均为 `@required`。连接状态流转：`Disconnected → Connecting → Connected/Failed → Disconnected`。

#### onError:message:

引擎错误回调。

```
- (void)onError:(NSInteger)code message:(NSString * _Nonnull)message;
```

参数

**参数**

**类型**

**说明**

`code`

`NSInteger`

错误码，详见 `AoqErrorCode`

`message`

`NSString *`

错误描述

#### onWarning:message:

引擎警告回调。

```
- (void)onWarning:(NSInteger)code message:(NSString * _Nonnull)message;
```

参数

**参数**

**类型**

**说明**

`code`

`NSInteger`

警告码，详见 `AoqWarningCode`

`message`

`NSString *`

警告描述

#### onConnectionStatusChange:

引擎连接状态变化回调。

```
- (void)onConnectionStatusChange:(AoqConnectionStatus)status;
```

参数

**参数**

**类型**

**说明**

`status`

`AoqConnectionStatus`

连接状态，详见 `AoqConnectionStatus`

#### onStats:

引擎统计信息回调。

```
- (void)onStats:(AoqStats * _Nonnull)stats;
```

参数

**参数**

**类型**

**说明**

`stats`

`AoqStats *`

统计数据，详见 `AoqStats`

#### onAudioDeviceStateChanged:

音频设备采集 / 播放操作状态变化回调。

```
- (void)onAudioDeviceStateChanged:(AoqAudioDeviceState * _Nonnull)state;
```

参数

**参数**

**类型**

**说明**

`state`

`AoqAudioDeviceState *`

音频设备状态，详见 `AoqAudioDeviceState`

#### onAudioDeviceRouteChanged:

音频输出路由变化回调。

```
- (void)onAudioDeviceRouteChanged:(NSInteger)routeType;
```

参数

**参数**

**类型**

**说明**

`routeType`

`NSInteger`

路由类型，取值详见 `AoqAudioDeviceRouteType`

#### onAudioFileState:

音频文件播放状态回调。

```
- (void)onAudioFileState:(AoqAudioFileState * _Nonnull)state;
```

参数

**参数**

**类型**

**说明**

`state`

`AoqAudioFileState *`

文件播放状态，详见 `AoqAudioFileState`

#### onLocalAudioVolumeIndication:

本地采集音量提示回调，需调用 `enableLocalAudioVolumeIndication:` 开启。

```
- (void)onLocalAudioVolumeIndication:(AoqAudioVolume * _Nonnull)volume;
```

参数

**参数**

**类型**

**说明**

`volume`

`AoqAudioVolume *`

本地音量信息，详见 `AoqAudioVolume`

#### onVideoDeviceStateChanged:

视频设备采集操作状态变化回调。

```
- (void)onVideoDeviceStateChanged:(AoqVideoDeviceState * _Nonnull)state;
```

参数

**参数**

**类型**

**说明**

`state`

`AoqVideoDeviceState *`

视频设备状态，详见 `AoqVideoDeviceState`

#### onDataMsg:

收到实时数据消息回调。

```
- (void)onDataMsg:(AoqDataMsg * _Nonnull)msg;
```

参数

**参数**

**类型**

**说明**

`msg`

`AoqDataMsg *`

数据消息，详见 `AoqDataMsg`

### AoqAudioFrameDelegate

音频帧数据回调协议，所有方法均为 `@optional`。请不要在回调中做任何耗时操作，否则可能导致声音异常。

#### onCapturedAudioFrame:

采集裸数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourceCaptured` 开启，支持设置采样率、声道数，支持读写模式。

```
- (void)onCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`frame`

`AoqAudioFrameData *`

采集音频裸数据，详见 `AoqAudioFrameData`

#### onProcessCapturedAudioFrame:

3A 后数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourceProcessCaptured` 开启，支持设置采样率、声道数，支持读写模式。

```
- (void)onProcessCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`frame`

`AoqAudioFrameData *`

3A 处理后音频裸数据，详见 `AoqAudioFrameData`

#### onPublishAudioFrame:frame:

推流数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourcePublish` 开启，支持设置采样率、声道数，仅支持只读模式。

```
- (void)onPublishAudioFrame:(AoqTrackType)trackType
                      frame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

音轨类型，详见 `AoqTrackType`

`frame`

`AoqAudioFrameData *`

推流音频裸数据，详见 `AoqAudioFrameData`

#### onPlaybackAudioFrame:

播放数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourcePlayback` 开启，支持设置采样率、声道数，支持读写模式。

```
- (void)onPlaybackAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`frame`

`AoqAudioFrameData *`

播放音频裸数据，详见 `AoqAudioFrameData`

### AoqVideoFrameDelegate

视频帧数据回调协议，所有方法均为 `@optional`。请不要在回调中做任何耗时操作，否则可能导致画面卡顿。回调返回 `YES` 表示数据已修改、需写回 SDK（写回仅对 I420 / CVPixelBuffer 生效）；返回 `NO` 表示只读。`frame` 中的数据仅在回调期间有效，异步使用需自行拷贝。

#### onCapturedVideoFrame:

本地采集后裸数据回调（前处理前）。通过 `enableVideoFrameObserver:` 设置 `videoSource = AoqVideoSourceCaptured` 开启。

```
- (BOOL)onCapturedVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`frame`

`AoqVideoFrame *`

采集视频帧数据，详见 `AoqVideoFrame`

trackType

AoqTrackType

视频轨道类型，支持 Video / Screen。

返回值：`YES` 数据已修改、需写回 SDK；`NO` 只读。

#### onPreEncodeVideoFrame:frame:

本地编码前裸数据回调（前处理后）。通过 `enableVideoFrameObserver:` 设置 `videoSource = AoqVideoSourcePreEncode` 开启。

```
- (BOOL)onPreEncodeVideoFrame:(AoqTrackType)trackType
                        frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道类型，详见 `AoqTrackType`

`frame`

`AoqVideoFrame *`

编码前视频帧数据，详见 `AoqVideoFrame`

返回值：`YES` 数据已修改、需写回 SDK；`NO` 只读。

#### onRemoteVideoFrame:frame:

远端解码后、渲染前裸数据回调。通过 `enableVideoFrameObserver:` 设置 `videoSource = AoqVideoSourceRemote` 开启。

```
- (BOOL)onRemoteVideoFrame:(AoqTrackType)trackType
                     frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道类型，详见 `AoqTrackType`

`frame`

`AoqVideoFrame *`

远端视频帧数据，详见 `AoqVideoFrame`

返回值：`YES` 数据已修改、需写回 SDK；`NO` 只读。

## 数据类型与枚举

### AoqScreenSourceList

字段

类型

说明

sourceList

NSArray<AoqScreenSourceInfo \*> \*

屏幕源数组

### AoqScreenSourceInfo

字段

类型

默认值

说明

sourceType

AoqScreenShareSourceType

Desktop

源类型

sourceId

int64\_t

0

源 ID

sourceName

NSString \*

—

源名称

sourceIsSelf

BOOL

—

是否为自身进程窗口

### AoqScreenShareSourceType

枚举值

值

说明

AoqScreenShareSourceTypeDesktop

0

整个桌面

AoqScreenShareSourceTypeWindow

1

指定窗口

### AoqScreenCaptureConfig

字段

类型

默认值

说明

isExternal

BOOL

NO

是否由应用提供屏幕原始帧。

sourceId

int64\_t

0

屏幕源 ID。

sourceType

AoqScreenShareSourceType

AoqScreenShareSourceTypeWindow

屏幕源类型。

### 通用类型

#### AoqCreateConfig

引擎创建配置。

**字段**

**类型**

**默认值**

**说明**

`workDir`

`NSString *`

`""`

SDK 工作目录

`enableDumpAudio`

`BOOL`

`NO`

是否开启音频原始数据 dump（调试用）

`extras`

`NSString *`

`""`

扩展参数

maxEncodedVideoFrameBytes

NSInteger

190 × 1024

编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。0 表示关闭限制。

enableDropOversizedVideoFrame

BOOL

NO

仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。

#### AoqConnectConfig

连接 Relay 服务器配置。

**字段**

**类型**

**说明**

`token`

`NSString *`

连接鉴权 Token

`sid`

`NSString *`

会话 ID

`certFingerprint`

`NSString *`

服务器证书指纹

`relayEndpoints`

`NSArray<AoqRelayEndpoint *> *`

Relay 接入点列表

`workspaceIdHash`

`NSString *`

工作空间哈希 ID

`publishTracks`

`NSArray<AoqTrackParam *> *`

本端推流 track 属性数组

`subscribeTracks`

`NSArray<AoqTrackParam *> *`

本端拉流 track 属性数组

#### AoqRelayEndpoint

Relay 接入点。

**字段**

**类型**

**默认值**

**说明**

`routeIndex`

`NSInteger`

`-1`

路径序号

`endpoint`

`NSString *`

`""`

服务端地址（域名或 IP）

`port`

`NSInteger`

`0`

服务端端口

tcpPort

NSInteger

0

TCP 降级端口；0 表示使用 SDK 默认端口 443。

#### AoqTrackParam

track 属性。

**字段**

**类型**

**默认值**

**说明**

`trackType`

`AoqTrackType`

`Audio`

track 类型

`trackMode`

`AoqTrackMode`

`Segment`

流式与非流式模式，仅对音频下行生效

#### AoqDataMsg

实时消息数据结构。

**字段**

**类型**

**说明**

`data`

`NSData *`

消息内容，指向调用方持有的内存

### 统计信息类型

#### AoqStats

引擎统计信息。

**字段**

**类型**

**说明**

`audioPublishStats`

`NSArray<AoqAudioPublishStats *> *`

音频推流统计数组

`videoPublishStats`

`NSArray<AoqVideoPublishStats *> *`

视频推流统计数组

`dataMsgPublishStats`

`NSArray<AoqDataMsgPublishStats *> *`

数据消息推流统计数组

`audioSubscribeStats`

`NSArray<AoqAudioSubscribeStats *> *`

音频拉流统计数组

`videoSubscribeStats`

`NSArray<AoqVideoSubscribeStats *> *`

视频拉流统计数组

`dataMsgSubscribeStats`

`NSArray<AoqDataMsgSubscribeStats *> *`

数据消息拉流统计数组

`networkStats`

`AoqNetworkStats *`

网络统计信息

#### AoqNetworkStats

网络统计信息。

**字段**

**类型**

**说明**

`sendBitrate`

`NSUInteger`

发送码率（bps）

`sendBytes`

`NSUInteger`

累计发送字节数

`recvBitrate`

`NSUInteger`

接收码率（bps）

`recvBytes`

`NSUInteger`

累计接收字节数

`loss`

`NSUInteger`

丢包率（0-100）

`rtt`

`NSUInteger`

往返延迟（ms）

#### AoqAudioPublishStats

音频推流统计信息。

**字段**

**类型**

**说明**

`trackType`

`AoqTrackType`

轨道类型

`bitrate`

`NSUInteger`

码率（bps）

`bytes`

`NSUInteger`

累计字节数

`encodeVolume`

`NSUInteger`

推流编码音量

#### AoqVideoPublishStats

视频推流统计信息。

**字段**

**类型**

**说明**

`trackType`

`AoqTrackType`

轨道类型

`bitrate`

`NSUInteger`

码率（bps）

`bytes`

`NSUInteger`

累计字节数

`encodeFps`

`NSUInteger`

编码帧率

#### AoqDataMsgPublishStats

数据消息推流统计信息。

**字段**

**类型**

**说明**

`trackType`

`AoqTrackType`

轨道类型

`bitrate`

`NSUInteger`

码率（bps）

`bytes`

`NSUInteger`

累计字节数

#### AoqAudioSubscribeStats

音频拉流统计信息。

**字段**

**类型**

**说明**

`trackType`

`AoqTrackType`

轨道类型

`bitrate`

`NSUInteger`

码率（bps）

`bytes`

`NSUInteger`

累计字节数

`playVolume`

`NSUInteger`

播放音量

#### AoqVideoSubscribeStats

视频拉流统计信息。

**字段**

**类型**

**说明**

`trackType`

`AoqTrackType`

轨道类型

`bitrate`

`NSUInteger`

码率（bps）

`bytes`

`NSUInteger`

累计字节数

`decodeFps`

`NSUInteger`

解码帧率

`renderFps`

`NSUInteger`

渲染帧率

#### AoqDataMsgSubscribeStats

数据消息拉流统计信息。

**字段**

**类型**

**说明**

`trackType`

`AoqTrackType`

轨道类型

`bitrate`

`NSUInteger`

码率（bps）

`bytes`

`NSUInteger`

累计字节数

### 枚举类型

#### AoqErrorCode

错误码枚举。

**枚举值**

**值**

**说明**

`AoqECOK`

0

成功

`AoqECParamInvalid`

1

参数非法

`AoqECStateInvalid`

2

状态非法

`AoqECUnSupport`

3

接口不支持

`AoqECAudio`

100

音频通用错误

`AoqECAudioExternalBufferFull`

110

外部音频缓冲区满

`AoqECAudioDevice`

120

音频设备通用错误

`AoqECAudioDeviceRecordingAuthFailed`

121

录音权限未获取

`AoqECAudioDeviceRecordingOccupied`

122

录音设备被占用

`AoqECAudioDeviceRecordingBackgroundStart`

123

后台启动录音

`AoqECAudioDeviceRecordingStartFail`

124

录音启动失败

`AoqECAudioDevicePlayoutOccupied`

125

播放设备被占用

`AoqECAudioDevicePlayoutBackgroundStart`

126

后台启动播放

`AoqECAudioDevicePlayoutStartFail`

127

播放启动失败

`AoqECVideo`

200

视频通用错误

`AoqECVideoExternalBufferFull`

210

外部视频缓冲区满

`AoqECVideoExternalCaptureNotEnabled`

211

未启用外部视频采集

`AoqECVideoExternalEncoderNotEnabled`

212

未启用外部视频编码

`AoqECVideoDevice`

220

视频设备通用错误

`AoqECVideoDeviceCameraOpenFail`

221

摄像头打开失败

`AoqECVideoDeviceCameraAuthFailed`

222

摄像头权限未获取

`AoqECVideoDeviceCameraOccupied`

223

摄像头被占用

`AoqECVideoDeviceCameraRunningError`

224

摄像头运行错误

`AoqECVideoCodec`

230

视频编解码通用错误

`AoqECVideoCodecEncoderInitFail`

231

编码器初始化失败

`AoqECVideoRender`

240

视频渲染通用错误

`AoqECVideoRenderCreateFail`

241

渲染视图创建失败

`AoqECVideoRenderDrawError`

242

渲染绘制错误

#### AoqWarningCode

警告码枚举。

**枚举值**

**值**

**说明**

`AoqWCOK`

0

无警告

`AoqWCAudio`

100

音频通用警告

`AoqWCAudioHowling`

101

音频啸叫检测

`AoqWCAudioDevice`

120

音频设备通用警告

`AoqWCAudioDeviceMicEnumerateError`

121

麦克风枚举错误

`AoqWCAudioDeviceMicStartTimeout`

122

麦克风启动超时

`AoqWCAudioDeviceRecordingError`

123

录音错误

`AoqWCAudioDeviceSpeakerEnumerateError`

124

扬声器枚举错误

`AoqWCAudioDeviceSpeakerStartTimeout`

125

扬声器启动超时

`AoqWCAudioDevicePlayoutError`

126

播放错误

`AoqWCVideo`

200

视频通用警告

`AoqWCVideoCameraEnumerateError`

201

摄像头枚举错误

`AoqWCVideoEncoderSwitched`

202

视频编码器已切换

`AoqWCVideoRenderDowngrade`

203

视频渲染降级

#### AoqTrackType

轨道类型。

**枚举值**

**值**

**说明**

`AoqTrackTypeAudio`

0

音频轨道

`AoqTrackTypeVideo`

1

视频轨道

`AoqTrackTypeData`

2

数据消息轨道

AoqTrackTypeScreen

3

屏幕共享轨道，支持上行。

#### AoqEncoderType

编码器类型。

**枚举值**

**值**

**说明**

`AoqEncoderTypeUnknown`

0

未知格式

`AoqEncoderTypeAudioPCM`

1

音频 PCM

`AoqEncoderTypeAudioOpus`

2

音频 Opus

`AoqEncoderTypeVideoH264`

3

视频 H.264

`AoqEncoderTypeVideoJpeg`

4

视频 JPEG

`AoqEncoderTypeDataText`

5

数据文本

#### AoqTrackMode

流式与非流式模式，仅对音频下行生效。

**枚举值**

**值**

**说明**

`AoqTrackModeSegment`

0

分段：数据按语义片段（如一句话）打包送达

`AoqTrackModeStream`

1

流式：数据持续、连续地送达

#### AoqConnectionStatus

引擎连接状态。

**枚举值**

**值**

**说明**

`AoqConnectionStatusDisconnected`

0

未连接

`AoqConnectionStatusConnecting`

1

连接中

`AoqConnectionStatusConnected`

2

已连接

`AoqConnectionStatusFailed`

3

连接失败

### 音频类型

#### AoqAudioCaptureConfig

音频采集配置。

**字段**

**类型**

**默认值**

**说明**

`isExternal`

`BOOL`

`NO`

是否外部采集

`channel`

`NSInteger`

`1`

音频采集通道数，支持 1/2

#### AoqAudioPlaybackConfig

音频播放配置。

**字段**

**类型**

**默认值**

**说明**

`isExternal`

`BOOL`

`NO`

是否外部播放

`channel`

`NSInteger`

`1`

音频播放通道数，支持 1/2

#### AoqAudioCodecConfig

音频编解码配置。

**字段**

**类型**

**默认值**

**说明**

`trackType`

`AoqTrackType`

`Audio`

轨道类型

`codecType`

`AoqEncoderType`

`AudioOpus`

编码格式

`sampleRate`

`NSInteger`

`48000`

采样率（Hz）

`channel`

`NSInteger`

`1`

声道数

`bitrate`

`NSInteger`

`32000`

比特率（bps）

#### AoqAudioDeviceState

音频设备状态。

**字段**

**类型**

**说明**

`state`

`AoqAudioDeviceStateCode`

状态码

`reason`

`NSInteger`

错误码（`AoqErrorCode`）

#### AoqAudioDeviceStateCode

音频设备状态码。

**枚举值**

**值**

**说明**

`AoqAudioDeviceNone`

0

无状态

`AoqAudioDeviceRecordStarting`

1

采集正在启动

`AoqAudioDeviceRecordStarted`

2

采集已启动

`AoqAudioDeviceRecordStopping`

3

采集正在停止

`AoqAudioDeviceRecordStopped`

4

采集已停止

`AoqAudioDeviceRecordFail`

5

采集失败

`AoqAudioDevicePlayStarting`

6

播放正在启动

`AoqAudioDevicePlayStarted`

7

播放已启动

`AoqAudioDevicePlayStopping`

8

播放正在停止

`AoqAudioDevicePlayStopped`

9

播放已停止

`AoqAudioDevicePlayFail`

10

播放失败

#### AoqAudioDeviceRouteType

音频设备路由类型。

**枚举值**

**值**

**说明**

`AoqAudioDeviceRouteDefault`

0

默认

`AoqAudioDeviceRouteHeadset`

1

耳机

`AoqAudioDeviceRouteEarpiece`

2

听筒

`AoqAudioDeviceRouteHeadsetNoMic`

3

无麦耳机

`AoqAudioDeviceRouteSpeakerPhone`

4

内置扬声器

`AoqAudioDeviceRouteUsb`

5

USB

`AoqAudioDeviceRouteBluetooth`

6

蓝牙

`AoqAudioDeviceRouteBluetoothA2dp`

7

蓝牙 A2DP

#### AoqAudioFileMixConfig

音频文件推流播放配置。

**字段**

**类型**

**默认值**

**说明**

`fileName`

`NSString *`

\-

文件名（含路径），必填

`cycles`

`NSInteger`

`-1`

循环次数，-1 表示无限循环

`startPosMs`

`NSInteger`

`0`

起始播放位置（ms）

`publishVolume`

`NSInteger`

`100`

推流音量，范围 \[0, 100\]

`playoutVolume`

`NSInteger`

`100`

播放音量，范围 \[0, 100\]

#### AoqAudioFileState

音频文件状态。

**字段**

**类型**

**说明**

`fileId`

`NSString *`

文件 ID

`stateCode`

`AoqAudioFileStateCode`

状态码

`errorCode`

`AoqAudioFileErrorCode`

错误码

#### AoqAudioFileStateCode

音频文件状态码。

**枚举值**

**值**

**说明**

`AoqAudioFileNone`

0

无状态

`AoqAudioFileStarted`

1

开始播放

`AoqAudioFileStopped`

2

停止播放

`AoqAudioFilePaused`

3

暂停播放

`AoqAudioFileResumed`

4

恢复播放

`AoqAudioFileEnded`

5

播放完毕

`AoqAudioFileBuffering`

6

正在缓冲

`AoqAudioFileBufferingEnd`

7

缓冲结束

`AoqAudioFileFailed`

8

播放失败

#### AoqAudioFileErrorCode

音频文件播放错误码。

**枚举值**

**值**

**说明**

`AoqAudioFileNoError`

0

没有错误

`AoqAudioFileOpenFailed`

1

打开文件失败

`AoqAudioFileDecodeFailed`

2

解码文件失败

#### AoqAudioExternalStreamConfig

外部音频流配置。

**字段**

**类型**

**默认值**

**说明**

`trackType`

`AoqTrackType`

`Audio`

音频轨道类型

`codecType`

`AoqEncoderType`

`AudioPCM`

音频流格式，支持 PCM

`channels`

`NSInteger`

`1`

声道数

`sampleRate`

`NSInteger`

`48000`

采样率（Hz）

`playoutVolume`

`NSInteger`

`100`

播放音量，范围 \[0, 100\]

`publishVolume`

`NSInteger`

`100`

推流音量，范围 \[0, 100\]

`maxBufferDuration`

`NSInteger`

`1000`

最大缓冲时长（ms）

`enable3A`

`BOOL`

`NO`

输入 PCM 是否做 3A 处理

#### AoqAudioFrameData

外部音频数据。

**字段**

**类型**

**说明**

`dataPtr`

`void *`

音频 PCM 裸数据指针

`dataSize`

`NSInteger`

PCM 数据字节数

`numOfSamples`

`NSInteger`

采样点数（单声道）

`bytesPerSample`

`NSInteger`

每个采样点字节数

`numOfChannels`

`NSInteger`

声道数

`samplesPerSec`

`NSInteger`

每秒采样点数

`pushSequence`

`int32_t`

PCM 输入轮次

`timeStamp`

`int64_t`

时间戳

`autoGenMute`

`BOOL`

数据回调有效，`YES` 表示 SDK 生成的静音数据

#### AoqAudioStreamDirection

外部音频流方向。

**枚举值**

**值**

**说明**

`AoqAudioStreamPublish`

0

推流音频

`AoqAudioStreamPlayout`

1

播放音频

#### AoqAudioExternalStreamToggle

外部音频流切换状态。

**枚举值**

**值**

**说明**

`AoqAudioExternalStreamToggleNormal`

0

恢复正常

`AoqAudioExternalStreamTogglePause`

1

暂停

#### AoqAudioSource

音频帧回调数据来源。

**枚举值**

**值**

**说明**

`AoqAudioSourceCaptured`

0

采集的音频数据

`AoqAudioSourceProcessCaptured`

1

3A 后的音频数据

`AoqAudioSourcePublish`

2

推流的音频数据（需 Connect 成功）

`AoqAudioSourcePlayback`

3

播放的音频数据

#### AoqAudioObserverMode

音频帧回调模式。

**枚举值**

**值**

**说明**

`AoqAudioObserverModeReadOnly`

0

只读

`AoqAudioObserverModeReadWrite`

1

读写

#### AoqAudioObserverConfig

音频帧回调配置。

**字段**

**类型**

**默认值**

**说明**

`sampleRate`

`NSInteger`

`48000`

回调音频采样率

`channels`

`NSInteger`

`1`

回调音频声道数

`mode`

`AoqAudioObserverMode`

`ReadOnly`

读写模式

#### AoqAudioVolumeIndicationConfig

本地音量提示配置。

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

#### AoqAudioVolume

本地音量信息。

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

### 视频类型

#### AoqVideoCaptureConfig

视频采集配置。

**字段**

**类型**

**默认值**

**说明**

`width`

`NSInteger`

`1280`

采集宽度（像素）；`isExternal=YES` 时无效

`height`

`NSInteger`

`720`

采集高度（像素）；`isExternal=YES` 时无效

`fps`

`NSInteger`

`15`

采集帧率；`isExternal=YES` 时无效（节奏由送帧决定）

`isExternal`

`BOOL`

`NO`

是否外部采集；`YES` 时不打开摄像头，由 `pushExternalVideoCapturedFrame:` 喂帧

#### AoqVideoCanvas

视频渲染数据结构。

**字段**

**类型**

**默认值**

**说明**

`view`

`NSView *`

`nil`

显示视图，传 nil 表示移除渲染绑定

`renderMode`

`AoqRenderMode`

`Auto`

渲染模式

调用方需保证 `view` 生命周期长于 `setLocalView:` / `setRemoteView:` 设置期间。

#### AoqRenderMode

渲染显示模式。

**枚举值**

**值**

**说明**

`AoqRenderModeAuto`

0

自动模式

`AoqRenderModeStretch`

1

拉伸平铺模式，宽高比不一致时拉伸到目标比例，画面会变形

`AoqRenderModeFill`

2

填充黑边模式，宽高比不一致时上下或左右填充黑边

`AoqRenderModeCrop`

3

裁剪模式，宽高比不一致时裁剪宽或高，画面内容会丢失

#### AoqVideoPixelFormat

视频像素格式。

**枚举值**

**值**

**说明**

`AoqVideoPixelFormatUnknown`

0

未知格式

`AoqVideoPixelFormatI420`

1

I420

`AoqVideoPixelFormatNV12`

2

NV12

`AoqVideoPixelFormatNV21`

3

NV21

`AoqVideoPixelFormatBGRA`

4

BGRA

`AoqVideoPixelFormatRGBA`

5

RGBA

`AoqVideoPixelFormatCVPixelBuffer`

6

零拷贝路径，`pixelBuffer` 字段填 `CVPixelBufferRef`

#### AoqVideoFrame

外部视频数据。

**字段**

**类型**

**说明**

`format`

`AoqVideoPixelFormat`

像素格式

`width`

`NSInteger`

宽度（像素）

`height`

`NSInteger`

高度（像素）

`data`

`NSData *`

打包格式数据（NV12/NV21/BGRA/RGBA）

`dataY` / `dataU` / `dataV`

`NSData *`

I420 三平面数据

`strideY` / `strideU` / `strideV`

`NSInteger`

I420 三平面步长

`pixelBuffer`

`CVPixelBufferRef`

零拷贝，`format=AoqVideoPixelFormatCVPixelBuffer` 时使用

`timeStamp`

`int64_t`

时间戳（ms）；0 时 SDK 用本地时钟补

#### AoqVideoEncodedFrame

外部已编码视频帧。调用方自行完成编码，SDK 不做二次编码，直接打包发送。

**字段**

**类型**

**说明**

`codec`

`AoqVideoCodecType`

编码格式

`data`

`NSData *`

编码后数据

`width`

`NSInteger`

宽度（像素）

`height`

`NSInteger`

高度（像素）

`timeStamp`

`int64_t`

时间戳（ms）；0 时 SDK 用本地时钟补

#### AoqVideoCodecType

外部编码帧 codec 类型。

**枚举值**

**值**

**说明**

`AoqVideoCodecTypeJPEG`

0

JPEG

#### AoqVideoDeviceState

视频设备状态。

**字段**

**类型**

**说明**

`state`

`AoqVideoDeviceStateCode`

状态码

`reason`

`NSInteger`

错误码（`AoqErrorCode`）

#### AoqVideoDeviceStateCode

视频设备状态码。

**枚举值**

**值**

**说明**

`AoqVideoDeviceNone`

0

无状态

`AoqVideoDeviceCaptureStarting`

1

摄像头正在启动

`AoqVideoDeviceCaptureStarted`

2

摄像头已启动

`AoqVideoDeviceCaptureStopping`

3

摄像头正在停止

`AoqVideoDeviceCaptureStopped`

4

摄像头已停止

`AoqVideoDeviceCaptureFail`

5

摄像头启动失败

#### AoqMirrorMode

镜像模式。

**枚举值**

**值**

**说明**

`AoqMirrorModeDisabled`

0

关闭镜像

`AoqMirrorModeEnabled`

1

开启镜像

#### AoqOrientationMode

方向模式。

**枚举值**

**值**

**说明**

`AoqOrientationModeAuto`

0

自动

`AoqOrientationModePortrait`

1

竖屏

`AoqOrientationModeLandscape`

2

横屏

#### AoqVideoCodecConfig

视频编解码参数（编解码共用）。用于解码时仅 `trackType` / `codecType` / `width` / `height` / `fps` / `bitrate` 生效（作为订阅提议参与协商），其余字段仅编码使用。

**字段**

**类型**

**默认值**

**说明**

`isExternal`

`BOOL`

`NO`

外部编码模式；`YES` 时由客户推送已编码帧，SDK 不做采集和编码

`trackType`

`AoqTrackType`

`Video`

轨道类型

`codecType`

`AoqEncoderType`

`VideoH264`

编码格式

`width`

`NSInteger`

`540`

分辨率宽

`height`

`NSInteger`

`960`

分辨率高

`fps`

`NSInteger`

`5`

帧率

`bitrate`

`NSInteger`

`500000`

起始码率（bps）

`minBitrate`

`NSInteger`

`128000`

最小码率（bps）

`keyframeInterval`

`NSInteger`

`2`

关键帧间隔（秒）

`mirrorMode`

`AoqMirrorMode`

`Disabled`

镜像模式

`orientationMode`

`AoqOrientationMode`

`Auto`

方向模式

#### AoqVideoSource

视频帧回调数据源（管线位置）。

**枚举值**

**值**

**说明**

`AoqVideoSourceCaptured`

0

采集后的视频数据（前处理前）

`AoqVideoSourcePreEncode`

1

编码前的视频数据（前处理后）

`AoqVideoSourceRemote`

2

远端解码后、渲染前的视频数据

#### AoqVideoObserverMode

视频帧回调模式。

**枚举值**

**值**

**说明**

`AoqVideoObserverModeReadOnly`

0

只读

`AoqVideoObserverModeReadWrite`

1

读写

#### AoqVideoObserverAlignment

视频输出宽度对齐方式。

**枚举值**

**值**

**说明**

`AoqVideoObserverAlignmentDefault`

0

默认

`AoqVideoObserverAlignmentEven`

1

偶数对齐

`AoqVideoObserverAlignment4`

2

4 对齐

`AoqVideoObserverAlignment8`

3

8 对齐

`AoqVideoObserverAlignment16`

4

16 对齐

#### AoqVideoObserverConfig

视频帧回调配置。

**字段**

**类型**

**默认值**

**说明**

`format`

`AoqVideoPixelFormat`

`I420`

期望回调像素格式

`alignment`

`AoqVideoObserverAlignment`

`Default`

宽度对齐策略

`mode`

`AoqVideoObserverMode`

`ReadOnly`

读写模式，仅 I420 / CVPixelBuffer 支持 ReadWrite

`mirrorApplied`

`BOOL`

`NO`

是否对回调数据应用镜像

trackType

AoqTrackType

AoqTrackTypeVideo

需要观察的视频轨道；仅支持 Video / Screen。

#### AoqRenderView

渲染视图控件，继承自 `NSView`，可作为 `AoqVideoCanvas.view` 使用。

**属性**

**类型**

**说明**

`engineDisplayView`

`NSView *`（只读）

引擎内部显示视图

`renderWidth`

`int`（只读）

渲染宽度

`renderHeight`

`int`（只读）

渲染高度

`enableMetal`

`BOOL`（只读）

是否启用 Metal 渲染

`delegate`

`id<AoqRenderViewDelegate>`

渲染视图事件委托

#### AoqRenderViewDelegate

渲染视图事件委托协议。

```
- (void)onRenderViewSizeChanged:(AoqRenderView * _Nonnull)view;
```

**回调**

**说明**

`onRenderViewSizeChanged:`

渲染视图尺寸变化回调
