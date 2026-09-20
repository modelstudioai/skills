# AOQ Client SDK Windows API 参考

本文介绍 AOQ Client SDK Windows 版的 C++ 接口、回调和数据类型，帮助您在 Windows 应用中接入实时音视频和数据消息能力。

SDK 以全局单例方式持有引擎实例，通过 `AoqClientEngine` 类对外提供接口，通过 `AoqEngineEventListener` 抽象类统一回调异步事件。所有类型定义位于 `AoqClientSdk` 命名空间，头文件为 `AoqClientEngine.h`。

**说明**所有 `const char*` 字符串由调用方负责生命周期，至少需保持到相应调用返回后，引擎内部将按需拷贝。

## 接口目录

### 引擎生命周期

**接口**

**简介**

`createEngine`

创建引擎实例（单例模式）

`destroy`

销毁引擎实例

`getVersion`

获取 SDK 版本号

`connect`

连接 Relay 服务器

`disconnect`

断开服务器连接

### 音频设备管理

**接口**

**简介**

`startAudioCapture`

打开音频采集设备（麦克风）

`stopAudioCapture`

关闭音频采集设备

`muteAudioCapture`

静音或取消静音音频采集

`startAudioPlayer`

开始音频渲染（播放远端音频）

`stopAudioPlayer`

停止音频渲染

`pauseAudioPlayer`

暂停音频渲染（支持淡出）

`resumeAudioPlayer`

恢复音频渲染（支持淡入）

`interruptAudioPlayer`

打断本轮音频通话

`enableLocalAudioVolumeIndication`

开启或关闭本地采集音量提示

### 音频编码配置

**接口**

**简介**

`setAudioEncoderConfig`

设置音频编码参数

`setAudioDecoderConfig`

设置音频解码参数

### 视频设备管理

**接口**

**简介**

`startVideoCapture`

打开视频采集设备（摄像头）

`stopVideoCapture`

关闭视频采集设备

`setLocalView`

设置或移除本地视频渲染窗口

`setRemoteView`

设置或移除远端视频渲染窗口

getScreenSourceList

获取屏幕和窗口源

startScreenCapture

开始屏幕采集

stopScreenCapture

停止屏幕采集

### 视频编码与外部输入

**接口**

**简介**

`setVideoEncoderConfig`

设置视频编码参数

`setVideoDecoderConfig`

设置视频解码参数

`pushExternalVideoCapturedFrame`

推送外部采集视频帧

`pushExternalVideoEncodedFrame`

推送外部已编码视频帧

### 媒体流发送控制

**接口**

**简介**

`enableSendMediaStream`

控制本地媒体流的发送开关

### 音频文件播放

**接口**

**简介**

`startAudioFile`

开始推流播放本地音频文件

`stopAudioFile`

停止音频文件播放

`pauseAudioFile`

暂停音频文件播放

`resumeAudioFile`

恢复音频文件播放

`getAudioFileDuration`

获取音频文件总时长

`getAudioFileCurrentPosition`

获取音频文件当前播放位置

`setAudioFilePositionMillis`

设置音频文件播放位置（seek）

`setAudioFileVolume`

设置音频文件音量

`getAudioFileVolume`

获取音频文件当前音量

### 外部音频流

**接口**

**简介**

`addAudioExternalStream`

新增一条外部音频流

`pushAudioExternalStreamData`

输入外部音频 PCM 数据

`setAudioExternalStreamVolume`

设置外部音频流音量

`getAudioExternalStreamVolume`

获取外部音频流音量

`clearAudioExternalStreamBuffer`

清空外部音频流缓存

`removeAudioExternalStream`

移除外部音频流

### 实时消息

**接口**

**简介**

`sendDataMsg`

发送实时数据消息

### 音频帧回调

**接口**

**简介**

`setAudioFrameObserver`

设置音频帧数据回调监听

`enableAudioFrameObserver`

开启或关闭指定位置的音频帧回调

### 视频帧回调

**接口**

**简介**

`setVideoFrameObserver`

设置视频帧数据回调监听

`enableVideoFrameObserver`

开启或关闭指定位置的视频帧回调

### AoqEngineEventListener 回调

**回调**

**简介**

`onError`

引擎错误回调

`onWarning`

引擎警告回调

`onConnectionStatusChange`

连接状态变化回调

`onStats`

引擎统计信息回调

`onAudioDeviceStateChanged`

音频设备操作状态变化回调

`onAudioDeviceRouteChanged`

音频输出路由变化回调

`onAudioFileState`

音频文件播放状态回调

`onLocalAudioVolumeIndication`

本地采集音量提示回调

`onVideoDeviceStateChanged`

视频设备操作状态变化回调

`onDataMsg`

收到实时数据消息回调

## 接口详情

### 屏幕采集

```
virtual int startScreenCapture(const AoqScreenCaptureConfig& config);
virtual int stopScreenCapture();
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

返回值：0 表示成功；非 0 表示失败。 接口同步返回，不提供 `onScreenCaptureStateChanged` 回调。

先调用 `getScreenSourceList` 获取屏幕或窗口源，再将选定的 `sourceId` 和 `sourceType` 传入采集配置。

外部原始帧：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`。

#### getScreenSourceList

```
virtual AoqScreenSourceList getScreenSourceList();
```

返回屏幕源列表。使用后必须调用 `AoqScreenSourceList::screenSourceListFree(list)` 释放列表内存。

### 引擎生命周期

#### createEngine

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

```
static AoqClientEngine* createEngine(const AoqCreateConfig& config,
                                     AoqEngineEventListener* listener);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqCreateConfig&`

引擎创建配置，详见 `AoqCreateConfig`

`listener`

`AoqEngineEventListener*`

事件回调监听器，详见 `AoqEngineEventListener`

返回值：引擎实例指针，失败返回 `nullptr`。

#### destroy

销毁引擎实例。销毁后需重新调用 `createEngine` 方可继续使用。

```
static int destroy();
```

返回值：0 表示成功；非 0 表示失败。

#### getVersion

获取 SDK 的版本号。

```
static const char* getVersion();
```

返回值：版本号字符串。

#### connect

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

```
virtual int connect(const AoqConnectConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqConnectConfig&`

连接鉴权配置，详见 `AoqConnectConfig`

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

#### disconnect

断开服务器连接。

```
virtual int disconnect();
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

### 音频设备管理

#### startAudioCapture

打开音频采集设备（麦克风）。

```
virtual int startAudioCapture(const AoqAudioCaptureConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqAudioCaptureConfig&`

音频采集配置，详见 `AoqAudioCaptureConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopAudioCapture

关闭音频采集设备。

```
virtual int stopAudioCapture();
```

返回值：0 表示成功；非 0 表示失败。

#### muteAudioCapture

静音或取消静音音频采集。

```
virtual int muteAudioCapture(bool mute);
```

参数

**参数**

**类型**

**说明**

`mute`

`bool`

`true` 静音；`false` 取消静音

返回值：0 表示成功；非 0 表示失败。

#### startAudioPlayer

开始音频渲染，播放远端音频。

```
virtual int startAudioPlayer(const AoqAudioPlaybackConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqAudioPlaybackConfig&`

音频播放配置，详见 `AoqAudioPlaybackConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopAudioPlayer

停止音频渲染。

```
virtual int stopAudioPlayer();
```

返回值：0 表示成功；非 0 表示失败。

#### pauseAudioPlayer

暂停音频渲染，支持淡出。

```
virtual int pauseAudioPlayer(int fadeMs);
```

参数

**参数**

**类型**

**说明**

`fadeMs`

`int`

淡出时长，单位毫秒；0 表示立即暂停

返回值：0 表示成功；非 0 表示失败。

#### resumeAudioPlayer

恢复音频渲染，支持淡入。

```
virtual int resumeAudioPlayer(int fadeMs);
```

参数

**参数**

**类型**

**说明**

`fadeMs`

`int`

淡入时长，单位毫秒；0 表示立即恢复

返回值：0 表示成功；非 0 表示失败。

#### interruptAudioPlayer

打断本轮音频通话，停止当前正在播放的音频内容。

```
virtual int interruptAudioPlayer(AoqTrackType trackType, int fadeMs);
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

音轨类型，详见 `AoqTrackType`

`fadeMs`

`int`

淡出时长，单位毫秒；0 表示立即打断

返回值：0 表示成功；非 0 表示失败。

#### enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示。开启后按 `config.interval` 周期触发 `onLocalAudioVolumeIndication` 回调；`config.interval <= 0` 时关闭回调。需在 `startAudioCapture` 之后调用才有音量数据。

```
virtual int enableLocalAudioVolumeIndication(const AoqAudioVolumeIndicationConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqAudioVolumeIndicationConfig&`

音量提示配置，详见 `AoqAudioVolumeIndicationConfig`

返回值：0 表示成功；非 0 表示失败。

### 音频编码配置

#### setAudioEncoderConfig

设置音频编码参数。

```
virtual int setAudioEncoderConfig(const AoqAudioCodecConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqAudioCodecConfig&`

音频编解码配置，详见 `AoqAudioCodecConfig`

返回值：0 表示成功；非 0 表示失败。

#### setAudioDecoderConfig

设置音频解码参数。

```
virtual int setAudioDecoderConfig(const AoqAudioCodecConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqAudioCodecConfig&`

音频编解码配置，详见 `AoqAudioCodecConfig`

返回值：0 表示成功；非 0 表示失败。

### 视频设备管理

#### startVideoCapture

打开视频采集设备（摄像头）。配置 `isExternal=true` 时不打开摄像头，由 `pushExternalVideoCapturedFrame` 喂帧。

```
virtual int startVideoCapture(const AoqVideoCaptureConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqVideoCaptureConfig&`

视频采集配置，详见 `AoqVideoCaptureConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopVideoCapture

关闭视频采集设备。

```
virtual int stopVideoCapture();
```

返回值：0 表示成功；非 0 表示失败。

#### setLocalView

设置或移除本地视频渲染窗口。`canvas.view == nullptr` 表示解绑。

```
virtual int setLocalView(AoqTrackType trackType, const AoqVideoCanvas& canvas);
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道，传 `AoqTrackTypeVideo`

`canvas`

`const AoqVideoCanvas&`

渲染画布，详见 `AoqVideoCanvas`；`view` 为 `nullptr` 表示解绑

返回值：0 表示成功；非 0 表示失败。

#### setRemoteView

设置或移除远端视频渲染窗口。`canvas.view == nullptr` 表示解绑。

```
virtual int setRemoteView(AoqTrackType trackType, const AoqVideoCanvas& canvas);
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道，传 `AoqTrackTypeVideo`

`canvas`

`const AoqVideoCanvas&`

渲染画布，详见 `AoqVideoCanvas`；`view` 为 `nullptr` 表示解绑

返回值：0 表示成功；非 0 表示失败。

### 视频编码与外部输入

#### setVideoEncoderConfig

设置视频编码参数，按 `config.trackType` 路由。

```
virtual int setVideoEncoderConfig(const AoqVideoCodecConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqVideoCodecConfig&`

视频编解码配置，详见 `AoqVideoCodecConfig`

返回值：0 表示成功；非 0 表示失败。

#### setVideoDecoderConfig

设置视频解码参数（订阅侧 codec 提议，需在 `connect` 之前调用），按 `config.trackType` 路由。

```
virtual int setVideoDecoderConfig(const AoqVideoCodecConfig& config);
```

参数

**参数**

**类型**

**说明**

`config`

`const AoqVideoCodecConfig&`

视频编解码配置，详见 `AoqVideoCodecConfig`

返回值：0 表示成功；非 0 表示失败。

#### pushExternalVideoCapturedFrame

推送外部视频帧。需先调用 `startVideoCapture` 且配置 `isExternal=true`。未启动外部视频采集时返回 `AoqECVideoExternalCaptureNotEnabled`（211）；帧格式不支持时返回 `AoqECParamInvalid`。

```
virtual int pushExternalVideoCapturedFrame(AoqTrackType trackType, const AoqVideoFrame& frame);
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

`const AoqVideoFrame&`

外部视频帧数据，详见 `AoqVideoFrame`

返回值：0 表示成功；`AoqECVideoExternalBufferFull`（210）表示缓冲区满；`AoqECVideoExternalCaptureNotEnabled`（211）表示未启用外部视频采集；`AoqECParamInvalid` 表示帧格式不支持；其他非 0 值表示其他错误。

#### pushExternalVideoEncodedFrame

推送外部已编码视频帧，bypass 编码器直推。需先调用 `setVideoEncoderConfig` 且配置 `isExternal=true`，当前仅支持 JPEG。

```
virtual int pushExternalVideoEncodedFrame(AoqTrackType trackType, const AoqVideoEncodedFrame& frame);
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

`const AoqVideoEncodedFrame&`

外部已编码帧数据，详见 `AoqVideoEncodedFrame`

返回值：0 表示成功；非 0 表示失败。

### 媒体流发送控制

#### enableSendMediaStream

控制本地媒体流的发送开关。建议初始化后先关闭发送，待 `onConnectionStatusChange` 回调 `AoqConnectionStatusConnected` 后再开启。

```
virtual int enableSendMediaStream(AoqTrackType trackType, bool enable);
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

`bool`

`true` 启用发送；`false` 停用发送

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

### 音频文件播放

#### startAudioFile

开始推流播放本地音频文件。

```
virtual int startAudioFile(const char* fileId, const AoqAudioFileMixConfig& config);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID，业务层需保证唯一性

`config`

`const AoqAudioFileMixConfig&`

音频文件混音配置，详见 `AoqAudioFileMixConfig`

返回值：0 表示成功；非 0 表示失败。

#### stopAudioFile

停止音频文件播放。

```
virtual int stopAudioFile(const char* fileId);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

返回值：0 表示成功；非 0 表示失败。

#### pauseAudioFile

暂停音频文件播放。

```
virtual int pauseAudioFile(const char* fileId);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

返回值：0 表示成功；非 0 表示失败。

#### resumeAudioFile

恢复音频文件播放。

```
virtual int resumeAudioFile(const char* fileId);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

返回值：0 表示成功；非 0 表示失败。

#### getAudioFileDuration

获取音频文件总时长。

```
virtual int64_t getAudioFileDuration(const char* fileId);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

返回值：>=0 表示音频文件时长，单位毫秒；<0 表示失败（`-AoqErrorCode`）。

#### getAudioFileCurrentPosition

获取音频文件当前播放位置。

```
virtual int64_t getAudioFileCurrentPosition(const char* fileId);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

返回值：>=0 表示当前播放位置，单位毫秒；<0 表示失败（`-AoqErrorCode`）。

#### setAudioFilePositionMillis

设置音频文件播放位置（seek）。

```
virtual int setAudioFilePositionMillis(const char* fileId, int64_t positionMillis);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

`positionMillis`

`int64_t`

播放位置，单位毫秒

返回值：0 表示成功；非 0 表示失败。

#### setAudioFileVolume

设置音频文件音量。

```
virtual int setAudioFileVolume(const char* fileId, AoqAudioStreamDirection type, int volume);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

`type`

`AoqAudioStreamDirection`

音频流方向，详见 `AoqAudioStreamDirection`

`volume`

`int`

音量值，范围 \[0, 100\]

返回值：0 表示成功；非 0 表示失败。

#### getAudioFileVolume

获取音频文件当前音量。

```
virtual int getAudioFileVolume(const char* fileId, AoqAudioStreamDirection type);
```

参数

**参数**

**类型**

**说明**

`fileId`

`const char*`

音频文件 ID

`type`

`AoqAudioStreamDirection`

音频流方向，详见 `AoqAudioStreamDirection`

返回值：\[0, 100\] 表示音量值；<0 表示失败（`-AoqErrorCode`）。

### 外部音频流

#### addAudioExternalStream

新增一条外部音频流。

```
virtual int addAudioExternalStream(const char* streamId, const AoqAudioExternalStreamConfig& config);
```

参数

**参数**

**类型**

**说明**

`streamId`

`const char*`

外部音频流 ID，业务层需保证唯一性

`config`

`const AoqAudioExternalStreamConfig&`

外部音频流配置，详见 `AoqAudioExternalStreamConfig`

返回值：0 表示成功；非 0 表示失败。

#### pushAudioExternalStreamData

输入外部音频 PCM 数据。返回 `AoqECAudioExternalBufferFull`（110）时表示 SDK 缓存已满，建议等待约 20ms 后重新送当前数据帧。

```
virtual int pushAudioExternalStreamData(const char* streamId, AoqAudioFrameData& data);
```

参数

**参数**

**类型**

**说明**

`streamId`

`const char*`

外部音频流 ID

`data`

`AoqAudioFrameData&`

外部音频裸数据，详见 `AoqAudioFrameData`

返回值：0 表示成功；非 0 表示失败。

**说明**最佳实践：实时采集场景一次 Push 10ms 数据长度，有数据即 Push；数据来源为文件时一次 Push 40ms 数据长度、间隔 30ms 给一次，并处理 `AoqECAudioExternalBufferFull` 返回。

#### setAudioExternalStreamVolume

设置外部音频流音量。

```
virtual int setAudioExternalStreamVolume(const char* streamId, AoqAudioStreamDirection type, int vol);
```

参数

**参数**

**类型**

**说明**

`streamId`

`const char*`

外部音频流 ID

`type`

`AoqAudioStreamDirection`

外部音频流类型，详见 `AoqAudioStreamDirection`

`vol`

`int`

音量值，范围 \[0, 100\]

返回值：0 表示成功；非 0 表示失败。

#### getAudioExternalStreamVolume

获取外部音频流音量。

```
virtual int getAudioExternalStreamVolume(const char* streamId, AoqAudioStreamDirection type);
```

参数

**参数**

**类型**

**说明**

`streamId`

`const char*`

外部音频流 ID

`type`

`AoqAudioStreamDirection`

外部音频流类型，详见 `AoqAudioStreamDirection`

返回值：\[0, 100\] 表示音量值；<0 表示失败（`-AoqErrorCode`）。

#### clearAudioExternalStreamBuffer

清空外部音频流缓存。

```
virtual void clearAudioExternalStreamBuffer(const char* streamId, int fadeoutMs);
```

参数

**参数**

**类型**

**说明**

`streamId`

`const char*`

外部音频流 ID

`fadeoutMs`

`int`

淡出时长；-1 使用 SDK 内部默认淡出，0 表示全部清空无淡出，>0 保留指定毫秒淡出

返回值：无。

#### removeAudioExternalStream

移除外部音频流。

```
virtual int removeAudioExternalStream(const char* streamId);
```

参数

**参数**

**类型**

**说明**

`streamId`

`const char*`

外部音频流 ID

返回值：0 表示成功；非 0 表示失败。

### 实时消息

#### sendDataMsg

发送实时数据消息。

```
virtual int sendDataMsg(const AoqDataMsg& msg);
```

参数

**参数**

**类型**

**说明**

`msg`

`const AoqDataMsg&`

消息内容，详见 `AoqDataMsg`

返回值：0 表示成功；非 0 表示失败。

### 音频帧回调

#### setAudioFrameObserver

设置音频帧数据回调监听器，传 `nullptr` 停止回调。设置后需调用 `enableAudioFrameObserver` 开启对应数据源的回调。

```
virtual int setAudioFrameObserver(IAudioFrameObserver* observer) = 0;
```

参数

**参数**

**类型**

**说明**

`observer`

`IAudioFrameObserver*`

音频帧回调监听器，详见 `IAudioFrameObserver`；传 `nullptr` 停止回调

返回值：0 表示成功；非 0 表示失败。

#### enableAudioFrameObserver

开启或关闭指定位置的音频帧回调。

```
virtual int enableAudioFrameObserver(bool enabled, AoqAudioSource audioSource,
                                     const AoqAudioObserverConfig& config) = 0;
```

参数

**参数**

**类型**

**说明**

`enabled`

`bool`

是否允许数据回调

`audioSource`

`AoqAudioSource`

音频裸数据源类型，详见 `AoqAudioSource`

`config`

`const AoqAudioObserverConfig&`

回调参数设置，详见 `AoqAudioObserverConfig`

返回值：0 表示成功；非 0 表示失败。

### 视频帧回调

#### setVideoFrameObserver

设置视频帧数据回调监听器，传 `nullptr` 停止回调。设置后需调用 `enableVideoFrameObserver` 开启对应数据源的回调。

```
virtual int setVideoFrameObserver(IVideoFrameObserver* observer) = 0;
```

参数

**参数**

**类型**

**说明**

`observer`

`IVideoFrameObserver*`

视频帧回调监听器，详见 `IVideoFrameObserver`；传 `nullptr` 停止回调

返回值：0 表示成功；非 0 表示失败。

#### enableVideoFrameObserver

开启或关闭指定位置的视频帧回调。

```
virtual int enableVideoFrameObserver(bool enabled, AoqVideoSource videoSource,
                                     const AoqVideoObserverConfig& config) = 0;
```

参数

**参数**

**类型**

**说明**

`enabled`

`bool`

是否启用某位置数据回调

`videoSource`

`AoqVideoSource`

视频帧回调数据源（管线位置），详见 `AoqVideoSource`

`config`

`const AoqVideoObserverConfig&`

回调参数设置，详见 `AoqVideoObserverConfig`

返回值：0 表示成功；非 0 表示失败。

## 回调

### AoqEngineEventListener

`AoqEngineEventListener` 是 SDK 所有异步事件通知的统一出口，为抽象类，由调用方继承实现并在 `createEngine` 时传入。所有回调可能在内部线程触发，实现者需自行处理线程安全。连接状态流转：`Disconnected → Connecting → Connected/Failed → Disconnected`。

#### onError

引擎错误回调。

```
virtual void onError(int code, const char* message) = 0;
```

参数

**参数**

**类型**

**说明**

`code`

`int`

错误码，详见 `AoqErrorCode`

`message`

`const char*`

错误描述

#### onWarning

引擎警告回调。

```
virtual void onWarning(int code, const char* message) = 0;
```

参数

**参数**

**类型**

**说明**

`code`

`int`

警告码，详见 `AoqWarningCode`

`message`

`const char*`

警告描述

#### onConnectionStatusChange

引擎连接状态变化回调。

```
virtual void onConnectionStatusChange(AoqConnectionStatus status) = 0;
```

参数

**参数**

**类型**

**说明**

`status`

`AoqConnectionStatus`

连接状态，详见 `AoqConnectionStatus`

#### onStats

引擎统计信息回调。

```
virtual void onStats(const AoqStats& stats) = 0;
```

参数

**参数**

**类型**

**说明**

`stats`

`const AoqStats&`

统计数据，详见 `AoqStats`

#### onAudioDeviceStateChanged

音频设备采集 / 播放操作状态变化回调。

```
virtual void onAudioDeviceStateChanged(const AoqAudioDeviceState& state) = 0;
```

参数

**参数**

**类型**

**说明**

`state`

`const AoqAudioDeviceState&`

音频设备状态，详见 `AoqAudioDeviceState`

#### onAudioDeviceRouteChanged

音频输出路由变化回调。

```
virtual void onAudioDeviceRouteChanged(int routeType) = 0;
```

参数

**参数**

**类型**

**说明**

`routeType`

`int`

路由类型，取值详见 `AoqAudioDeviceRouteType`

#### onAudioFileState

音频文件播放状态回调。

```
virtual void onAudioFileState(const AoqAudioFileState& state) = 0;
```

参数

**参数**

**类型**

**说明**

`state`

`const AoqAudioFileState&`

文件播放状态，详见 `AoqAudioFileState`

#### onLocalAudioVolumeIndication

本地采集音量提示回调，需调用 `enableLocalAudioVolumeIndication` 开启。

```
virtual void onLocalAudioVolumeIndication(const AoqAudioVolume& volume) = 0;
```

参数

**参数**

**类型**

**说明**

`volume`

`const AoqAudioVolume&`

本地音量信息，详见 `AoqAudioVolume`

#### onVideoDeviceStateChanged

视频设备采集操作状态变化回调。

```
virtual void onVideoDeviceStateChanged(const AoqVideoDeviceState& state) = 0;
```

参数

**参数**

**类型**

**说明**

`state`

`const AoqVideoDeviceState&`

视频设备状态，详见 `AoqVideoDeviceState`

#### onDataMsg

收到实时数据消息回调。

```
virtual void onDataMsg(const AoqDataMsg& msg) = 0;
```

参数

**参数**

**类型**

**说明**

`msg`

`const AoqDataMsg&`

数据消息，详见 `AoqDataMsg`

### IAudioFrameObserver

音频帧数据回调接口，由调用方继承实现。请不要在回调中做任何耗时操作，否则可能导致声音异常。

#### onCapturedAudioFrame

采集裸数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourceCaptured` 开启，支持设置采样率、声道数，支持读写模式。

```
virtual void onCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
```

参数

**参数**

**类型**

**说明**

`data`

`const AoqAudioFrameData&`

采集音频裸数据，详见 `AoqAudioFrameData`

#### onProcessCapturedAudioFrame

3A 后数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourceProcessCaptured` 开启，支持设置采样率、声道数，支持读写模式。

```
virtual void onProcessCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
```

参数

**参数**

**类型**

**说明**

`data`

`const AoqAudioFrameData&`

3A 处理后音频裸数据，详见 `AoqAudioFrameData`

#### onPublishAudioFrame

推流数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourcePublish` 开启，支持设置采样率、声道数，仅支持只读模式。

```
virtual void onPublishAudioFrame(AoqTrackType trackType, const AoqAudioFrameData& data) = 0;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

音轨类型，详见 `AoqTrackType`

`data`

`const AoqAudioFrameData&`

推流音频裸数据，详见 `AoqAudioFrameData`

#### onPlaybackAudioFrame

播放数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourcePlayback` 开启，支持设置采样率、声道数，支持读写模式。

```
virtual void onPlaybackAudioFrame(const AoqAudioFrameData& data) = 0;
```

参数

**参数**

**类型**

**说明**

`data`

`const AoqAudioFrameData&`

播放音频裸数据，详见 `AoqAudioFrameData`

### IVideoFrameObserver

视频帧数据回调接口，由调用方继承实现。请不要在回调中做任何耗时操作，否则可能导致画面卡顿。回调返回 `true` 表示数据已修改、需写回 SDK（写回仅对 I420 生效）；返回 `false` 表示只读。`frame` 中的数据仅在回调期间有效，异步使用需自行拷贝。

#### onCapturedVideoFrame

本地采集后裸数据回调（前处理前）。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourceCaptured` 开启。

```
virtual bool onCapturedVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

参数

**参数**

**类型**

**说明**

`frame`

`AoqVideoFrame&`

采集视频帧数据，详见 `AoqVideoFrame`

trackType

AoqTrackType

视频轨道类型，支持 Video / Screen。

返回值：`true` 数据已修改、需写回 SDK；`false` 只读。

#### onPreEncodeVideoFrame

本地编码前裸数据回调（前处理后）。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourcePreEncode` 开启。

```
virtual bool onPreEncodeVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道类型，详见 `AoqTrackType`

`frame`

`AoqVideoFrame&`

编码前视频帧数据，详见 `AoqVideoFrame`

返回值：`true` 数据已修改、需写回 SDK；`false` 只读。

#### onRemoteVideoFrame

远端解码后、渲染前裸数据回调。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourceRemote` 开启。

```
virtual bool onRemoteVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

参数

**参数**

**类型**

**说明**

`trackType`

`AoqTrackType`

视频轨道类型，详见 `AoqTrackType`

`frame`

`AoqVideoFrame&`

远端视频帧数据，详见 `AoqVideoFrame`

返回值：`true` 数据已修改、需写回 SDK；`false` 只读。

## 数据类型与枚举

### AoqScreenCaptureStateCode

屏幕采集状态枚举。当前 SDK 已定义该类型，但没有对应的状态回调。

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

已启动

AoqScreenCaptureStopping

3

停止中

AoqScreenCaptureStopped

4

已停止

AoqScreenCaptureFail

5

失败

### AoqScreenCaptureState

字段

类型

说明

state

AoqScreenCaptureStateCode

屏幕采集状态码。

reason

int

错误码，对应 AoqErrorCode；正常为 0。

### AoqScreenSourceList

字段/方法

类型

说明

sourceCount

int

源数量

sourceList

const AoqScreenSourceInfo\*

源数组；使用后调用 screenSourceListFree(list) 释放。

screenSourceListFree(list)

static void

释放列表内存。调用方必须调用，否则会发生内存泄漏。

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

const char\*

nullptr

源名称

sourceIsSelf

bool

false

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

bool

false

是否由应用提供屏幕原始帧。

sourceId

int64\_t

0

屏幕源 ID。

sourceType

AoqScreenShareSourceType

AoqScreenShareSourceTypeDesktop

屏幕源类型。

appGroup

const char\*

nullptr

iOS 专用，本平台不使用。

### 通用类型

#### AoqCreateConfig

引擎创建配置。

**字段**

**类型**

**默认值**

**说明**

`workDir`

`const char*`

`nullptr`

SDK 工作目录

`enableDumpAudio`

`bool`

`false`

是否开启音频数据保存（调试用）

`extras`

`const char*`

`nullptr`

扩展参数（JSON 字符串）

maxEncodedVideoFrameBytes

int

190 × 1024

编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。0 表示关闭限制。

enableDropOversizedVideoFrame

bool

false

仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。

#### AoqConnectConfig

连接 Relay 服务器配置。`relayEndpoints` / `publishTracks` / `subscribeTracks` 为 C 风格数组 + 长度，数组内存由调用方持有，仅需在 `connect` 调用期间保持有效。

**字段**

**类型**

**说明**

`token`

`const char*`

连接鉴权 Token

`sid`

`const char*`

会话 ID

`certFingerprint`

`const char*`

服务器证书指纹

`workspaceIdHash`

`const char*`

工作空间哈希 ID

`relayEndpoints`

`const AoqRelayEndpoint*`

Relay 接入点数组

`relayEndpointsCount`

`size_t`

Relay 接入点数量

`publishTracks`

`const AoqTrackParam*`

本端推流 track 属性数组

`publishTracksCount`

`size_t`

推流 track 数量

`subscribeTracks`

`const AoqTrackParam*`

本端拉流 track 属性数组

`subscribeTracksCount`

`size_t`

拉流 track 数量

#### AoqRelayEndpoint

Relay 接入点。

**字段**

**类型**

**默认值**

**说明**

`route_index`

`int`

`-1`

路径序号

`endpoint`

`const char*`

`nullptr`

服务端地址（域名或 IP）

`port`

`int`

`0`

服务端端口

tcp\_port

int

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

消息数据结构。回调中使用时仅保证回调期间有效，如需异步使用请自行拷贝。

**字段**

**类型**

**说明**

`data`

`const uint8_t*`

消息内容，指向调用方持有的内存

`dataSize`

`size_t`

字节数

### 统计信息类型

#### AoqStats

引擎统计信息。各统计数组以指针 + 数量形式提供。

**字段**

**类型**

**说明**

`audioPublishStats` / `audioPublishStatsCount`

`const AoqAudioPublishStats*` / `unsigned int`

音频推流统计数组及数量

`videoPublishStats` / `videoPublishStatsCount`

`const AoqVideoPublishStats*` / `unsigned int`

视频推流统计数组及数量

`dataMsgPublishStats` / `dataMsgPublishStatsCount`

`const AoqDataMsgPublishStats*` / `unsigned int`

数据消息推流统计数组及数量

`audioSubscribeStats` / `audioSubscribeStatsCount`

`const AoqAudioSubscribeStats*` / `unsigned int`

音频拉流统计数组及数量

`videoSubscribeStats` / `videoSubscribeStatsCount`

`const AoqVideoSubscribeStats*` / `unsigned int`

视频拉流统计数组及数量

`dataMsgSubscribeStats` / `dataMsgSubscribeStatsCount`

`const AoqDataMsgSubscribeStats*` / `unsigned int`

数据消息拉流统计数组及数量

`networkStats`

`const AoqNetworkStats*`

网络统计信息

#### AoqNetworkStats

网络统计信息。

**字段**

**类型**

**说明**

`sendBitrate`

`unsigned int`

发送码率（bps）

`sendBytes`

`uint64_t`

累计发送字节数

`recvBitrate`

`unsigned int`

接收码率（bps）

`recvBytes`

`uint64_t`

累计接收字节数

`loss`

`unsigned int`

丢包率（0-100）

`rtt`

`unsigned int`

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

`unsigned int`

码率（bps）

`bytes`

`uint64_t`

累计字节数

`encodeVolume`

`unsigned int`

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

`unsigned int`

码率（bps）

`bytes`

`uint64_t`

累计字节数

`encodeFps`

`unsigned int`

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

`unsigned int`

码率（bps）

`bytes`

`uint64_t`

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

`unsigned int`

码率（bps）

`bytes`

`uint64_t`

累计字节数

`playVolume`

`unsigned int`

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

`unsigned int`

码率（bps）

`bytes`

`uint64_t`

累计字节数

`decodeFps`

`unsigned int`

解码帧率

`renderFps`

`unsigned int`

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

`unsigned int`

码率（bps）

`bytes`

`uint64_t`

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

接口被调但当前平台 / 模式未实现

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

`AoqECAudioDeviceEarpieceRequiresVoipMode`

128

听筒模式需启用 VoIP

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

屏幕共享轨道，仅支持上行。

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

音频 Opus（插件化，需联系 SDK 提供内置或动态下载到 APP 下）

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

`bool`

`false`

是否外部采集

`channel`

`int`

`1`

音频采集通道数，支持 1/2

#### AoqAudioPlaybackConfig

音频播放配置。

**字段**

**类型**

**默认值**

**说明**

`isExternal`

`bool`

`false`

是否外部播放

`channel`

`int`

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

`int`

`48000`

采样率（Hz）。编码支持 Opus 8/16/48K、PCM 8/16/32/48K；解码额外支持 24K，但 24K 仅限 Segment 模式（Stream 模式不支持 24K，非法组合在 connect 时通过 onError 回调 AoqECParamInvalid）

`channel`

`int`

`1`

声道数，支持 1/2

`bitrate`

`int`

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

`int`

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

`const char*`

`nullptr`

文件名（含路径），必填

`cycles`

`int`

`-1`

循环次数，-1 表示无限循环

`startPosMs`

`long`

`0`

起始播放位置（ms）

`publishVolume`

`int`

`100`

推流音量，范围 \[0, 100\]

`playoutVolume`

`int`

`100`

播放音量，范围 \[0, 100\]

#### AoqAudioFileState

音频文件状态。

**字段**

**类型**

**说明**

`fileId`

`const char*`

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

`int`

`1`

声道数，受限推流音频 Codec 支持 1/2，超过的声道忽略

`sampleRate`

`int`

`48000`

采样率（Hz），支持 8/12/16/24/32/44.1/48/64/88.2/96/176.4/192K

`playoutVolume`

`int`

`100`

播放音量，范围 \[0, 100\]

`publishVolume`

`int`

`100`

推流音量，范围 \[0, 100\]

`maxBufferDuration`

`int`

`600000`

最大缓冲时长（ms），取值范围 \[100, ~\]，SDK 缓存时长超过时 Push 会失败

`enable3A`

`bool`

`false`

输入 PCM 是否做 3A 处理

#### AoqAudioFrameData

音频数据。

**字段**

**类型**

**说明**

`dataPtr`

`void*`

音频数据指针

`numOfSamples`

`int`

采样点数（单个声道）

`bytesPerSample`

`int`

每个采样点的字节数

`numOfChannels`

`int`

声道数

`samplesPerSec`

`int`

每秒采样点数

`pushSequence`

`int`

PCM 输入轮次（用于 `pushAudioExternalStreamData` 消费完通知）

`timeStamp`

`int64_t`

时间戳

`dataSize`

`int`

数据长度

`autoGenMute`

`bool`

数据回调有效，`true` 表示 SDK 生成的静音数据

#### AoqAudioStreamDirection

音频流方向。

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

外部音频流控制。

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

音频数据源类型。

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

音频数据回调参数设置。

**字段**

**类型**

**默认值**

**说明**

`sampleRate`

`int`

`48000`

回调音频采样率，受限 Source 源，不一致时重采样，支持 8/12/16/24/32/44.1/48/64/88.2/96/176.4/192K

`channels`

`int`

`1`

回调音频声道数，支持 1/2，受限拉流 Codec 参数

`mode`

`AoqAudioObserverMode`

`ReadOnly`

回调模式

#### AoqAudioVolumeIndicationConfig

本地音量提示配置。

字段

类型

默认值

说明

reportSpeech

bool

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

本地音量信息。

字段

类型

默认值

说明

isSpeech

bool

false

是否为人声。

volume

int

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

`int`

`1280`

采集宽度（像素）；`isExternal=true` 时无效

`height`

`int`

`720`

采集高度（像素）；`isExternal=true` 时无效

`fps`

`int`

`15`

采集帧率；`isExternal=true` 时无效（节奏由送帧决定）

`isExternal`

`bool`

`false`

是否外部采集；`true` 时不打开摄像头，由 `pushExternalVideoCapturedFrame` 喂帧

#### AoqVideoCanvas

视频渲染数据结构。`view` 为平台原生视图句柄的不透明指针，Windows 平台填窗口句柄 `HWND`。调用方需保证 `view` 生命周期长于 `setLocalView` / `setRemoteView` 设置期间。

**字段**

**类型**

**默认值**

**说明**

`view`

`void*`

`nullptr`

显示视图句柄（`HWND`），传 `nullptr` 表示移除渲染绑定

`renderMode`

`AoqRenderMode`

`Auto`

渲染模式

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

#### AoqVideoFrame

外部视频数据。

**字段**

**类型**

**说明**

`format`

`AoqVideoPixelFormat`

像素格式

`width`

`int`

宽度（像素）

`height`

`int`

高度（像素）

`dataPtr`

`void*`

打包格式数据指针（NV12/NV21/BGRA/RGBA）

`dataSize`

`int`

打包数据字节数

`dataY` / `dataU` / `dataV`

`void*`

I420 三平面数据指针

`strideY` / `strideU` / `strideV`

`int`

I420 三平面步长

`timeStamp`

`int64_t`

时间戳（ms）；0 时 SDK 用本地时钟补

`nativePixelBuffer`

`void*`

跨平台保留字段，Windows 不使用。

`textureId`

`int`

跨平台保留字段，Windows 不使用。

`transformMatrix`

`float[16]`

跨平台保留字段，Windows 不使用。

#### AoqVideoEncodedFrame

外部已编码视频帧。调用方自行完成编码，SDK 不做二次编码，直接打包发送。

**字段**

**类型**

**说明**

`codec`

`AoqVideoCodecType`

编码格式

`data`

`void*`

编码后数据指针

`dataSize`

`int`

编码后数据字节数

`width`

`int`

宽度（像素）

`height`

`int`

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

`int`

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

摄像头启动失败（权限拒绝、设备不可用等）

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

视频编解码参数（编解码共用）。用于解码时仅 `trackType` / `codecType` / `width` / `height` / `fps` / `bitrate` 生效（作为订阅提议参与协商），`minBitrate` / `keyframeInterval` / `mirrorMode` / `orientationMode` / `isExternal` 仅编码使用。

**字段**

**类型**

**默认值**

**说明**

`isExternal`

`bool`

`false`

外部编码模式；`true` 时由客户推送已编码帧，SDK 不做采集和编码

`trackType`

`AoqTrackType`

`Video`

轨道类型

`codecType`

`AoqEncoderType`

`VideoH264`

编码格式

`width`

`int`

`540`

分辨率宽

`height`

`int`

`960`

分辨率高

`fps`

`int`

`5`

帧率

`bitrate`

`int`

`500000`

起始码率（bps）

`minBitrate`

`int`

`128000`

最小码率（bps）

`keyframeInterval`

`int`

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

视频数据回调参数设置。

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

回调模式，仅 I420 支持 ReadWrite

`mirrorApplied`

`bool`

`false`

是否对回调数据应用镜像

trackType

AoqTrackType

AoqTrackTypeVideo

需要观察的视频轨道；仅支持 Video / Screen。
