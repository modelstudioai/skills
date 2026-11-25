# AOQ Client SDK macOS API 参考

本文介绍 AOQ Client SDK macOS 版的 Objective-C 接口、回调和数据类型，帮助您在 macOS 应用中接入实时音视频和数据消息能力。

> **说明**
>
> AOQ SDK 提供通用视频接口。[Qwen-Audio-Realtime](../../realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md) 不支持视频输入或输出；其他模型可使用的媒体能力以对应接入文档为准。

SDK 以全局单例方式持有引擎实例，通过 `AoqClientEngine` 类对外提供接口，通过 `AoqEngineDelegate` 协议统一回调异步事件。

<a id="接口目录"></a>

<a id="5ac644b5aaf5"></a>

<a id="ad48e96aa70d"></a>

## 接口目录

<a id="引擎生命周期"></a>

<a id="9a119fdcdc26"></a>

<a id="3853d5fc7e0a"></a>

### 引擎生命周期

| 接口 | 简介 |
| --- | --- |
| createEngine | 创建引擎实例（单例模式） |
| destroy | 销毁引擎实例 |
| getVersion | 获取 SDK 版本号 |
| connect | 连接 Relay 服务器 |
| disconnect | 断开服务器连接 |

<a id="音频设备管理"></a>

<a id="38be8ebf1442"></a>

<a id="b4fb44f6eb28"></a>

### 音频设备管理

| 接口 | 简介 |
| --- | --- |
| startAudioCapture | 打开音频采集设备（麦克风） |
| stopAudioCapture | 关闭音频采集设备 |
| muteAudioCapture | 静音或取消静音音频采集 |
| startAudioPlayer | 开始音频渲染（播放远端音频） |
| stopAudioPlayer | 停止音频渲染 |
| pauseAudioPlayer | 暂停音频渲染，支持淡出 |
| resumeAudioPlayer | 恢复音频渲染，支持淡入 |
| interruptAudioPlayer | 打断本轮音频通话 |

<a id="音频编码配置"></a>

<a id="7fef0298f77a"></a>

<a id="ef974c1ad8ee"></a>

### 音频编码配置

| 接口 | 简介 |
| --- | --- |
| setAudioEncoderConfig | 设置音频编码参数 |
| setAudioDecoderConfig | 设置音频解码参数 |

<a id="音频文件播放"></a>

<a id="c5500080027e"></a>

<a id="28f63a96752c"></a>

### 音频文件播放

| 接口 | 简介 |
| --- | --- |
| startAudioFile | 开始推流播放本地音频文件 |
| stopAudioFile | 停止音频文件播放 |
| pauseAudioFile | 暂停音频文件播放 |
| resumeAudioFile | 恢复音频文件播放 |
| getAudioFileDuration | 获取音频文件总时长 |
| getAudioFileCurrentPosition | 获取音频文件当前播放位置 |
| setAudioFilePositionMillis | 设置音频文件播放位置（seek） |
| setAudioFileVolume | 设置音频文件音量 |
| getAudioFileVolume | 获取音频文件当前音量 |

<a id="外部音频流"></a>

<a id="ee0b8c2b9f0c"></a>

<a id="d6b4c13dff30"></a>

### 外部音频流

| 接口 | 简介 |
| --- | --- |
| addAudioExternalStream | 新增一条外部音频流 |
| pushAudioExternalStreamData | 输入外部音频 PCM 数据 |
| setAudioExternalStreamVolume | 设置外部音频流音量 |
| getAudioExternalStreamVolume | 获取外部音频流音量 |
| clearAudioExternalStreamBuffer | 清空外部音频流缓存 |
| removeAudioExternalStream | 移除外部音频流 |

<a id="音频帧回调"></a>

<a id="c23ead0436b1"></a>

<a id="b2a326f23d00"></a>

### 音频帧回调

| 接口 | 简介 |
| --- | --- |
| setAudioFrameObserver | 设置音频帧数据回调 delegate |
| enableAudioFrameObserver | 开启或关闭指定位置的音频帧回调 |

<a id="本地音量提示"></a>

### 本地音量提示

| 接口 | 简介 |
| --- | --- |
| enableLocalAudioVolumeIndication | 开启或关闭本地采集音量提示 |

<a id="视频设备管理"></a>

<a id="b39fd9f2b875"></a>

<a id="49303f7eebef"></a>

### 视频设备管理

| 接口 | 简介 |
| --- | --- |
| startVideoCapture | 打开视频采集设备（摄像头） |
| stopVideoCapture | 关闭视频采集设备 |
| setLocalView | 设置或移除本地视频渲染窗口 |
| setRemoteView | 设置或移除远端视频渲染窗口 |

<a id="视频编码与外部输入"></a>

<a id="86b67a2c4ddb"></a>

<a id="5e7b6d28c285"></a>

### 视频编码与外部输入

| 接口 | 简介 |
| --- | --- |
| setVideoEncoderConfig | 设置视频编码参数 |
| setVideoDecoderConfig | 设置视频解码参数 |
| pushExternalVideoCapturedFrame | 推送外部采集视频帧 |
| pushExternalVideoEncodedFrame | 推送外部已编码视频帧 |

<a id="屏幕采集"></a>

### 屏幕采集

| 接口 | 简介 |
| --- | --- |
| getScreenSourceList | 获取屏幕采集源列表（Mac 桌面端独有） |
| startScreenCapture | 启动屏幕采集 |
| stopScreenCapture | 停止屏幕采集 |

<a id="媒体流发送控制"></a>

<a id="8c6bddbf0e54"></a>

<a id="74db1f031e94"></a>

### 媒体流发送控制

| 接口 | 简介 |
| --- | --- |
| enableSendMediaStream | 控制本地媒体流的发送开关 |

<a id="视频帧回调"></a>

<a id="e8b6832b62f8"></a>

<a id="7d6304a9d294"></a>

### 视频帧回调

| 接口 | 简介 |
| --- | --- |
| setVideoFrameObserver | 设置视频帧数据回调 delegate |
| enableVideoFrameObserver | 开启或关闭指定位置的视频帧回调 |

<a id="实时消息"></a>

<a id="d328fbb2f654"></a>

<a id="a66495101cc7"></a>

### 实时消息

| 接口 | 简介 |
| --- | --- |
| sendDataMsg | 发送实时数据消息 |

<a id="aoqenginedelegate"></a>

<a id="bf1da4b2ac81"></a>

<a id="df084ecf9c1a"></a>

### AoqEngineDelegate

| 接口 | 简介 |
| --- | --- |
| onError | 引擎错误回调 |
| onWarning | 引擎警告回调 |
| onConnectionStatusChange | 连接状态变化回调 |
| onStats | 引擎统计信息回调 |
| onAudioDeviceStateChanged | 音频设备操作状态变化回调 |
| onAudioDeviceRouteChanged | 音频输出路由变化回调 |
| onAudioFileState | 音频文件播放状态回调 |
| onLocalAudioVolumeIndication | 本地采集音量提示回调 |
| onVideoDeviceStateChanged | 视频设备操作状态变化回调 |
| onDataMsg | 收到实时数据消息回调 |

<a id="aoqaudioframedelegate"></a>

### AoqAudioFrameDelegate

| 接口 | 简介 |
| --- | --- |
| onCapturedAudioFrame | 采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。 |
| onProcessCapturedAudioFrame | 3A 处理后的音频帧触发。数据已经过回声消除、降噪等处理。 |
| onPublishAudioFrame | 推流前的音频帧触发。数据为最终编码发送前的音频。 |
| onPlaybackAudioFrame | 播放前的远端音频帧触发。数据为解码后、混音后待播放的音频。 |

<a id="aoqvideoframedelegate"></a>

### AoqVideoFrameDelegate

| 接口 | 简介 |
| --- | --- |
| onCapturedVideoFrame | 采集到原始视频帧时触发（前处理前）。trackType 用于区分 Video / Screen 轨道。 |
| onPreEncodeVideoFrame | 编码前的视频帧触发（前处理后）。 |
| onRemoteVideoFrame | 远端解码后、渲染前的视频帧触发。 |

<a id="接口详情"></a>

<a id="6a1ce06b2380"></a>

<a id="dd0f0f808cdb"></a>

## 接口详情

<a id="引擎生命周期-2"></a>

<a id="8ed6f5cbc380"></a>

<a id="3853d5fc7e0a-details"></a>

<a id="aoq-api-category-1"></a>

### 引擎生命周期

<a id="createengine-delegate"></a>

<a id="31cbe748ff47"></a>

<a id="7962585baa3e"></a>

#### createEngine:delegate:

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

<a id="code-block"></a>

```text
+ (instancetype _Nonnull)createEngine:(AoqCreateConfig * _Nonnull)config
                             delegate:(id<AoqEngineDelegate> _Nonnull)delegate;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqCreateConfig *` | 引擎创建配置，详见 `AoqCreateConfig` |
| `delegate` | `id<AoqEngineDelegate>` | 引擎事件回调委托，详见 `AoqEngineDelegate` |

返回值：引擎实例，不会返回 nil。

<a id="destroy"></a>

<a id="47310970f999"></a>

<a id="3c32463acd34"></a>

#### destroy

销毁引擎实例。销毁后需重新调用 `createEngine:delegate:` 方可继续使用。

<a id="code-block-2"></a>

```text
+ (int)destroy;
```

返回值：0 表示成功；非 0 表示失败。

<a id="getversion"></a>

<a id="ce5dd2ebd860"></a>

<a id="9ee46ccd02a5"></a>

#### getVersion

获取 SDK 的版本号。

<a id="code-block-3"></a>

```text
+ (NSString * _Nonnull)getVersion;
```

返回值：版本号字符串。

<a id="connect"></a>

<a id="51e911a4770d"></a>

<a id="689f775b8fa6"></a>

#### connect:

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

<a id="code-block-4"></a>

```text
- (int)connect:(AoqConnectConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqConnectConfig *` | 连接鉴权配置，详见 `AoqConnectConfig` |

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

<a id="disconnect"></a>

<a id="c1da927cc806"></a>

<a id="22d67fb3d286"></a>

#### disconnect

断开服务器连接。

<a id="code-block-5"></a>

```text
- (int)disconnect;
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

<a id="音频设备管理-2"></a>

<a id="a2055abb7fe8"></a>

<a id="b4fb44f6eb28-details"></a>

<a id="aoq-api-category-2"></a>

### 音频设备管理

<a id="startaudiocapture"></a>

<a id="af8b051fa6a9"></a>

<a id="9fbcfa5847c4"></a>

#### startAudioCapture:

打开音频采集设备（麦克风）。

<a id="code-block-6"></a>

```text
- (int)startAudioCapture:(AoqAudioCaptureConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqAudioCaptureConfig *` | 音频采集配置，详见 `AoqAudioCaptureConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopaudiocapture"></a>

<a id="0bd5b16cc7e1"></a>

<a id="5316db42022d"></a>

#### stopAudioCapture

关闭音频采集设备。

<a id="code-block-7"></a>

```text
- (int)stopAudioCapture;
```

返回值：0 表示成功；非 0 表示失败。

<a id="muteaudiocapture"></a>

<a id="fae5e64a2834"></a>

<a id="44b8061c1cb6"></a>

#### muteAudioCapture:

静音或取消静音音频采集。

<a id="code-block-8"></a>

```text
- (int)muteAudioCapture:(BOOL)mute;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `mute` | `BOOL` | `YES` 静音；`NO` 取消静音 |

返回值：0 表示成功；非 0 表示失败。

<a id="startaudioplayer"></a>

<a id="f753e9aea3df"></a>

<a id="bc5f8e1fcd21"></a>

#### startAudioPlayer:

开始音频渲染，播放远端音频。

<a id="code-block-9"></a>

```text
- (int)startAudioPlayer:(AoqAudioPlaybackConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqAudioPlaybackConfig *` | 音频播放配置，详见 `AoqAudioPlaybackConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopaudioplayer"></a>

<a id="713427caeee9"></a>

<a id="7411f06c2d53"></a>

#### stopAudioPlayer

停止音频渲染。

<a id="code-block-10"></a>

```text
- (int)stopAudioPlayer;
```

返回值：0 表示成功；非 0 表示失败。

<a id="pauseaudioplayer"></a>

<a id="f6a99b2340f1"></a>

<a id="95dd1fe21709"></a>

#### pauseAudioPlayer:

暂停音频渲染，支持淡出。

<a id="code-block-11"></a>

```text
- (int)pauseAudioPlayer:(NSInteger)fadeMs;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fadeMs` | `NSInteger` | 淡出时长，单位毫秒；0 表示立即暂停 |

返回值：0 表示成功；非 0 表示失败。

<a id="resumeaudioplayer"></a>

<a id="bd5fb5e29fb1"></a>

<a id="4ad15041700e"></a>

#### resumeAudioPlayer:

恢复音频渲染，支持淡入。

<a id="code-block-12"></a>

```text
- (int)resumeAudioPlayer:(NSInteger)fadeMs;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fadeMs` | `NSInteger` | 淡入时长，单位毫秒；0 表示立即恢复 |

返回值：0 表示成功；非 0 表示失败。

<a id="interruptaudioplayer-fadems"></a>

<a id="6611daf5c1f7"></a>

<a id="e80069262f74"></a>

#### interruptAudioPlayer:fadeMs:

打断本轮音频通话，停止当前正在播放的音频内容。

<a id="code-block-13"></a>

```text
- (int)interruptAudioPlayer:(AoqTrackType)trackType fadeMs:(NSInteger)fadeMs;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 音轨类型，详见 `AoqTrackType` |
| `fadeMs` | `NSInteger` | 淡出时长，单位毫秒；0 表示立即打断 |

返回值：0 表示成功；非 0 表示失败。

<a id="音频编码配置-2"></a>

<a id="604c8c224a40"></a>

<a id="ef974c1ad8ee-details"></a>

<a id="aoq-api-category-3"></a>

### 音频编码配置

<a id="setaudioencoderconfig"></a>

<a id="68254747da4f"></a>

<a id="4c2bc667f223"></a>

#### setAudioEncoderConfig:

设置音频编码参数。

<a id="code-block-14"></a>

```text
- (int)setAudioEncoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqAudioCodecConfig *` | 音频编解码配置，详见 `AoqAudioCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="setaudiodecoderconfig"></a>

<a id="1b55ec98775d"></a>

<a id="a135e718425d"></a>

#### setAudioDecoderConfig:

设置音频解码参数。

<a id="code-block-15"></a>

```text
- (int)setAudioDecoderConfig:(AoqAudioCodecConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqAudioCodecConfig *` | 音频编解码配置，详见 `AoqAudioCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="音频文件播放-2"></a>

<a id="1617192f4d13"></a>

<a id="28f63a96752c-details"></a>

<a id="aoq-api-category-4"></a>

### 音频文件播放

<a id="startaudiofile-config"></a>

<a id="056bd834f758"></a>

<a id="f4578ced2d56"></a>

#### startAudioFile:config:

开始推流播放本地音频文件。

<a id="code-block-16"></a>

```text
- (int)startAudioFile:(NSString * _Nonnull)fileId
               config:(AoqAudioFileMixConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID，业务层需保证唯一性 |
| `config` | `AoqAudioFileMixConfig *` | 音频文件混音配置，详见 `AoqAudioFileMixConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopaudiofile"></a>

<a id="a9004d61b331"></a>

<a id="df09e699e2c8"></a>

#### stopAudioFile:

停止音频文件播放。

<a id="code-block-17"></a>

```text
- (int)stopAudioFile:(NSString * _Nonnull)fileId;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="pauseaudiofile"></a>

<a id="9cca062d04fc"></a>

<a id="72a878832956"></a>

#### pauseAudioFile:

暂停音频文件播放。

<a id="code-block-18"></a>

```text
- (int)pauseAudioFile:(NSString * _Nonnull)fileId;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="resumeaudiofile"></a>

<a id="dcbceb303fff"></a>

<a id="9033de9f4074"></a>

#### resumeAudioFile:

恢复音频文件播放。

<a id="code-block-19"></a>

```text
- (int)resumeAudioFile:(NSString * _Nonnull)fileId;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="getaudiofileduration"></a>

<a id="e18ba9da8415"></a>

<a id="3afa6901779d"></a>

#### getAudioFileDuration:

获取音频文件总时长。

<a id="code-block-20"></a>

```text
- (long long)getAudioFileDuration:(NSString * _Nonnull)fileId;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |

返回值：>=0 表示音频文件时长，单位毫秒；<0 表示失败。

<a id="getaudiofilecurrentposition"></a>

<a id="f6d15abba317"></a>

<a id="35ae368c3b9b"></a>

#### getAudioFileCurrentPosition:

获取音频文件当前播放位置。

<a id="code-block-21"></a>

```text
- (long long)getAudioFileCurrentPosition:(NSString * _Nonnull)fileId;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |

返回值：>=0 表示当前播放位置，单位毫秒；<0 表示失败。

<a id="setaudiofilepositionmillis-positionmillis"></a>

<a id="499abf8802b8"></a>

<a id="a5d2006a6775"></a>

#### setAudioFilePositionMillis:positionMillis:

设置音频文件播放位置（seek）。

<a id="code-block-22"></a>

```text
- (int)setAudioFilePositionMillis:(NSString * _Nonnull)fileId
                  positionMillis:(long long)positionMillis;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |
| `positionMillis` | `long long` | 播放位置，单位毫秒 |

返回值：0 表示成功；非 0 表示失败。

<a id="setaudiofilevolume-type-volume"></a>

<a id="6c9198653624"></a>

<a id="5a495261b558"></a>

#### setAudioFileVolume:type:volume:

设置音频文件音量。

<a id="code-block-23"></a>

```text
- (int)setAudioFileVolume:(NSString * _Nonnull)fileId
                     type:(AoqAudioStreamDirection)type
                   volume:(NSInteger)volume;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |
| `type` | `AoqAudioStreamDirection` | 音频流方向，详见 `AoqAudioStreamDirection` |
| `volume` | `NSInteger` | 音量值，范围 \[0, 100\] |

返回值：0 表示成功；非 0 表示失败。

<a id="getaudiofilevolume-type"></a>

<a id="f607da77d753"></a>

<a id="bb9ba3c4d677"></a>

#### getAudioFileVolume:type:

获取音频文件当前音量。

<a id="code-block-24"></a>

```text
- (int)getAudioFileVolume:(NSString * _Nonnull)fileId
                     type:(AoqAudioStreamDirection)type;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 音频文件 ID |
| `type` | `AoqAudioStreamDirection` | 音频流方向，详见 `AoqAudioStreamDirection` |

返回值：\[0, 100\] 表示音量值；<0 表示失败。

<a id="外部音频流-2"></a>

<a id="20c2c6f099b4"></a>

<a id="d6b4c13dff30-details"></a>

<a id="aoq-api-category-5"></a>

### 外部音频流

<a id="addaudioexternalstream-config"></a>

<a id="d0ed57dc8612"></a>

<a id="f0bf78245dcc"></a>

#### addAudioExternalStream:config:

新增一条外部音频流。

<a id="code-block-25"></a>

```text
- (int)addAudioExternalStream:(NSString * _Nonnull)streamId
                       config:(AoqAudioExternalStreamConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `NSString *` | 外部音频流 ID，业务层需保证唯一性 |
| `config` | `AoqAudioExternalStreamConfig *` | 外部音频流配置，详见 `AoqAudioExternalStreamConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="pushaudioexternalstreamdata-data"></a>

<a id="b1f69f98d7b9"></a>

<a id="c572caa27c2e"></a>

#### pushAudioExternalStreamData:data:

输入外部音频 PCM 数据。返回 `AoqECAudioExternalBufferFull`（110）时表示 SDK 缓存已满，建议等待约 20ms 后重新送当前数据帧。

<a id="code-block-26"></a>

```text
- (int)pushAudioExternalStreamData:(NSString * _Nonnull)streamId
                              data:(AoqAudioFrameData * _Nonnull)data;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `NSString *` | 外部音频流 ID |
| `data` | `AoqAudioFrameData *` | 外部音频裸数据，详见 `AoqAudioFrameData` |

返回值：0 表示成功；非 0 表示失败。

> **说明**
>
> 最佳实践：实时采集场景一次 Push 10ms 数据长度，有数据即 Push；数据来源为文件时一次 Push 40ms 数据长度、间隔 30ms 给一次，并处理 `AoqECAudioExternalBufferFull` 返回。

<a id="setaudioexternalstreamvolume-type-volume"></a>

<a id="9ce42a7d8828"></a>

<a id="8e50ba036468"></a>

#### setAudioExternalStreamVolume:type:volume:

设置外部音频流音量。

<a id="code-block-27"></a>

```text
- (int)setAudioExternalStreamVolume:(NSString * _Nonnull)streamId
                               type:(AoqAudioStreamDirection)type
                             volume:(NSInteger)volume;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `NSString *` | 外部音频流 ID |
| `type` | `AoqAudioStreamDirection` | 外部音频流类型，详见 `AoqAudioStreamDirection` |
| `volume` | `NSInteger` | 音量值，范围 \[0, 100\] |

返回值：0 表示成功；非 0 表示失败。

<a id="getaudioexternalstreamvolume-type"></a>

<a id="307393a0385e"></a>

<a id="c2b0f086290d"></a>

#### getAudioExternalStreamVolume:type:

获取外部音频流音量。

<a id="code-block-28"></a>

```text
- (int)getAudioExternalStreamVolume:(NSString * _Nonnull)streamId
                               type:(AoqAudioStreamDirection)type;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `NSString *` | 外部音频流 ID |
| `type` | `AoqAudioStreamDirection` | 外部音频流类型，详见 `AoqAudioStreamDirection` |

返回值：\[0, 100\] 表示音量值；<0 表示失败。

<a id="clearaudioexternalstreambuffer-fadeoutms"></a>

<a id="0d0cf07e96f6"></a>

<a id="65b2b58d5b33"></a>

#### clearAudioExternalStreamBuffer:fadeoutMs:

清空外部音频流缓存。

<a id="code-block-29"></a>

```text
- (void)clearAudioExternalStreamBuffer:(NSString * _Nonnull)streamId
                              fadeoutMs:(NSInteger)fadeoutMs;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `NSString *` | 外部音频流 ID |
| `fadeoutMs` | `NSInteger` | 淡出时长；-1 使用 SDK 内部默认淡出，0 表示全部清空无淡出，>0 保留指定毫秒淡出 |

返回值：无。

<a id="removeaudioexternalstream"></a>

<a id="daaa2d8e960e"></a>

<a id="06e2a5253294"></a>

#### removeAudioExternalStream:

移除外部音频流。

<a id="code-block-30"></a>

```text
- (int)removeAudioExternalStream:(NSString * _Nonnull)streamId;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `NSString *` | 外部音频流 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="音频帧回调-2"></a>

<a id="c2f2a40d63ed"></a>

<a id="b2a326f23d00-details"></a>

<a id="aoq-api-category-6"></a>

### 音频帧回调

<a id="setaudioframeobserver"></a>

<a id="ca957baf5677"></a>

<a id="ccaf4a8408b2"></a>

#### setAudioFrameObserver:

设置音频帧数据回调委托，传 nil 停止回调。设置后需调用 `enableAudioFrameObserver:audioSource:config:` 开启对应数据源的回调。

<a id="code-block-31"></a>

```text
- (int)setAudioFrameObserver:(id<AoqAudioFrameDelegate> _Nullable)delegate;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `delegate` | `id<AoqAudioFrameDelegate>` | 音频帧回调委托，详见 `AoqAudioFrameDelegate`；传 nil 停止回调 |

返回值：0 表示成功；非 0 表示失败。

<a id="enableaudioframeobserver-audiosource-config"></a>

<a id="aeafc0201c95"></a>

<a id="fcece862c08a"></a>

#### enableAudioFrameObserver:audioSource:config:

开启或关闭指定位置的音频帧回调。

<a id="code-block-32"></a>

```text
- (int)enableAudioFrameObserver:(BOOL)enabled
                   audioSource:(AoqAudioSource)audioSource
                        config:(AoqAudioObserverConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | `BOOL` | 是否允许数据回调 |
| `audioSource` | `AoqAudioSource` | 音频裸数据源类型，详见 `AoqAudioSource` |
| `config` | `AoqAudioObserverConfig *` | 回调参数设置，详见 `AoqAudioObserverConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="本地音量提示-2"></a>

<a id="aoq-api-category-7"></a>

### 本地音量提示

<a id="enablelocalaudiovolumeindication"></a>

<a id="0480ac16c35c"></a>

<a id="092f66dc04af"></a>

#### enableLocalAudioVolumeIndication:

开启或关闭本地采集音量提示。开启后按 `config.interval` 周期触发 `onLocalAudioVolumeIndication:` 回调；`config.interval <= 0` 时关闭回调。需在 `startAudioCapture:` 之后调用才有音量数据。

<a id="code-block-33"></a>

```text
- (int)enableLocalAudioVolumeIndication:(AoqAudioVolumeIndicationConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqAudioVolumeIndicationConfig *` | 音量提示配置，详见 `AoqAudioVolumeIndicationConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="视频设备管理-2"></a>

<a id="4387da6b9680"></a>

<a id="49303f7eebef-details"></a>

<a id="aoq-api-category-8"></a>

### 视频设备管理

<a id="startvideocapture"></a>

<a id="8f8a160a06f0"></a>

<a id="6c1813b779f8"></a>

#### startVideoCapture:

打开视频采集设备（摄像头）。配置 `isExternal=YES` 时不打开摄像头，由 `pushExternalVideoCapturedFrame:frame:` 喂帧。

<a id="code-block-34"></a>

```text
- (int)startVideoCapture:(AoqVideoCaptureConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqVideoCaptureConfig *` | 视频采集配置，详见 `AoqVideoCaptureConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopvideocapture"></a>

<a id="b18819932526"></a>

<a id="793310d05029"></a>

#### stopVideoCapture

关闭视频采集设备。

<a id="code-block-35"></a>

```text
- (int)stopVideoCapture;
```

返回值：0 表示成功；非 0 表示失败。

<a id="setlocalview-canvas"></a>

<a id="0a1b00018294"></a>

<a id="e18fabf3d932"></a>

#### setLocalView:canvas:

设置或移除本地视频渲染窗口。`canvas` 传 nil 或 `canvas.view` 为 nil 表示解绑。

<a id="code-block-36"></a>

```text
- (int)setLocalView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道，传 `AoqTrackTypeVideo` |
| `canvas` | `AoqVideoCanvas *` | 渲染画布，详见 `AoqVideoCanvas`；传 nil 表示解绑 |

返回值：0 表示成功；非 0 表示失败。

<a id="setremoteview-canvas"></a>

<a id="9e761fc346d9"></a>

<a id="234644b814a6"></a>

#### setRemoteView:canvas:

设置或移除远端视频渲染窗口。`canvas` 传 nil 或 `canvas.view` 为 nil 表示解绑。

<a id="code-block-37"></a>

```text
- (int)setRemoteView:(AoqTrackType)trackType canvas:(AoqVideoCanvas * _Nullable)canvas;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道，传 `AoqTrackTypeVideo` |
| `canvas` | `AoqVideoCanvas *` | 渲染画布，详见 `AoqVideoCanvas`；传 nil 表示解绑 |

返回值：0 表示成功；非 0 表示失败。

<a id="视频编码与外部输入-2"></a>

<a id="070585f3c9af"></a>

<a id="5e7b6d28c285-details"></a>

<a id="aoq-api-category-9"></a>

### 视频编码与外部输入

<a id="setvideoencoderconfig"></a>

<a id="616879a04d12"></a>

<a id="1fb459d60a2b"></a>

#### setVideoEncoderConfig:

设置视频编码参数，按 `config.trackType` 路由。

<a id="code-block-38"></a>

```text
- (int)setVideoEncoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqVideoCodecConfig *` | 视频编解码配置，详见 `AoqVideoCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="setvideodecoderconfig"></a>

<a id="c60a0e748272"></a>

<a id="53640b74719c"></a>

#### setVideoDecoderConfig:

设置视频解码参数（订阅侧 codec 提议，需在 `connect:` 之前调用），按 `config.trackType` 路由。

<a id="code-block-39"></a>

```text
- (int)setVideoDecoderConfig:(AoqVideoCodecConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `AoqVideoCodecConfig *` | 视频编解码配置，详见 `AoqVideoCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="pushexternalvideocapturedframe-frame"></a>

<a id="6bc2e21de5c7"></a>

<a id="16dbb9f94f83"></a>

#### pushExternalVideoCapturedFrame:frame:

推送外部视频帧。需先调用 `startVideoCapture:` 且配置 `isExternal=YES`，未启动外部视频采集或格式不支持时返回 `AoqECParamInvalid`。

<a id="code-block-40"></a>

```text
- (int)pushExternalVideoCapturedFrame:(AoqTrackType)trackType
                                frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 路由目标，传 `AoqTrackTypeVideo`<br><br>；也支持 AoqTrackTypeScreen |
| `frame` | `AoqVideoFrame *` | 外部视频帧数据，详见 `AoqVideoFrame` |

返回值：0 表示成功；`AoqECVideoExternalBufferFull`（210）表示缓冲区满；<0 表示其他错误。

<a id="pushexternalvideoencodedframe-frame"></a>

<a id="be0611e226c6"></a>

<a id="3b74901ff2d4"></a>

#### pushExternalVideoEncodedFrame:frame:

推送外部已编码视频帧，bypass 编码器直推。需先调用 `setVideoEncoderConfig:` 且配置 `isExternal=YES`，当前仅支持 JPEG。

<a id="code-block-41"></a>

```text
- (int)pushExternalVideoEncodedFrame:(AoqTrackType)trackType
                               frame:(AoqVideoEncodedFrame * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 路由目标，传 `AoqTrackTypeVideo`<br><br>；也支持 AoqTrackTypeScreen |
| `frame` | `AoqVideoEncodedFrame *` | 外部已编码帧数据，详见 `AoqVideoEncodedFrame` |

返回值：0 表示成功；非 0 表示失败。

<a id="屏幕采集-2"></a>

<a id="aoq-api-category-10"></a>

### 屏幕采集

<a id="code-block-42"></a>

```objective-c
- (int)startScreenCapture:(AoqScreenCaptureConfig * _Nonnull)config;
- (int)stopScreenCapture;
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

返回值：0 表示成功；非 0 表示失败。 接口同步返回，不提供 `onScreenCaptureStateChanged` 回调。

先调用 `getScreenSourceList` 获取屏幕或窗口源，再将选定的 `sourceId` 和 `sourceType` 传入采集配置。

外部原始帧：设置 `isExternal=YES` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`。

<a id="getscreensourcelist"></a>

#### getScreenSourceList

<a id="code-block-43"></a>

```objective-c
- (AoqScreenSourceList * _Nullable)getScreenSourceList;
```

返回屏幕源列表，失败返回 nil。

<a id="媒体流发送控制-2"></a>

<a id="9f3a291082d9"></a>

<a id="74db1f031e94-details"></a>

<a id="aoq-api-category-11"></a>

### 媒体流发送控制

<a id="enablesendmediastream-enable"></a>

<a id="60c81fadda31"></a>

<a id="78ca6e27e052"></a>

#### enableSendMediaStream:enable:

控制本地媒体流的发送开关。建议初始化后先关闭发送，待 `onConnectionStatusChange:` 回调 `AoqConnectionStatusConnected` 后再开启。

<a id="code-block-44"></a>

```text
- (int)enableSendMediaStream:(AoqTrackType)trackType enable:(BOOL)enable;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 路由目标，支持 `AoqTrackTypeAudio` / `AoqTrackTypeVideo`<br><br>；支持 AoqTrackTypeScreen |
| `enable` | `BOOL` | `YES` 启用发送；`NO` 停用发送 |

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

<a id="视频帧回调-2"></a>

<a id="0ac65fc9869e"></a>

<a id="7d6304a9d294-details"></a>

<a id="aoq-api-category-12"></a>

### 视频帧回调

<a id="setvideoframeobserver"></a>

<a id="9c1620f758d0"></a>

<a id="cceff5cc147d"></a>

#### setVideoFrameObserver:

设置视频帧数据回调委托，传 nil 停止回调。设置后需调用 `enableVideoFrameObserver:videoSource:config:` 开启对应数据源的回调。

<a id="code-block-45"></a>

```text
- (int)setVideoFrameObserver:(id<AoqVideoFrameDelegate> _Nullable)delegate;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `delegate` | `id<AoqVideoFrameDelegate>` | 视频帧回调委托，详见 `AoqVideoFrameDelegate`；传 nil 停止回调 |

返回值：0 表示成功；非 0 表示失败。

<a id="enablevideoframeobserver-videosource-config"></a>

<a id="477c672d25a5"></a>

<a id="887e60560474"></a>

#### enableVideoFrameObserver:videoSource:config:

开启或关闭指定位置的视频帧回调。

<a id="code-block-46"></a>

```text
- (int)enableVideoFrameObserver:(BOOL)enabled
                    videoSource:(AoqVideoSource)videoSource
                         config:(AoqVideoObserverConfig * _Nonnull)config;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | `BOOL` | 是否启用某位置数据回调 |
| `videoSource` | `AoqVideoSource` | 视频帧回调数据源（管线位置），详见 `AoqVideoSource` |
| `config` | `AoqVideoObserverConfig *` | 回调参数设置，详见 `AoqVideoObserverConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="实时消息-2"></a>

<a id="ae2f0dbb49ff"></a>

<a id="a66495101cc7-details"></a>

<a id="aoq-api-category-13"></a>

### 实时消息

<a id="senddatamsg"></a>

<a id="73aba35f063f"></a>

<a id="cb3286d458ed"></a>

#### sendDataMsg:

发送实时数据消息。

<a id="code-block-47"></a>

```text
- (int)sendDataMsg:(AoqDataMsg * _Nonnull)msg;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `msg` | `AoqDataMsg *` | 消息内容，详见 `AoqDataMsg` |

返回值：0 表示成功；非 0 表示失败。

<a id="aoqenginedelegate-2"></a>

<a id="08ad4a83f8df"></a>

<a id="9415b72aa2ba"></a>

<a id="aoq-api-category-14"></a>

<a id="b91d0dde1233"></a>

<a id="008f847f1c29"></a>

### AoqEngineDelegate

`AoqEngineDelegate` 是 SDK 所有异步事件通知的统一出口，在 `createEngine:delegate:` 时传入。所有回调方法均为 `@required`。连接状态流转：`Disconnected → Connecting → Connected/Failed → Disconnected`。

<a id="onerror-message"></a>

<a id="7f446f067dcd"></a>

<a id="889eba812615"></a>

#### onError:message:

引擎错误回调。

<a id="code-block-48"></a>

```text
- (void)onError:(NSInteger)code message:(NSString * _Nonnull)message;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `NSInteger` | 错误码，详见 `AoqErrorCode` |
| `message` | `NSString *` | 错误描述 |

<a id="onwarning-message"></a>

<a id="c3a778b2dd2b"></a>

<a id="cfe428070d27"></a>

#### onWarning:message:

引擎警告回调。

<a id="code-block-49"></a>

```text
- (void)onWarning:(NSInteger)code message:(NSString * _Nonnull)message;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `NSInteger` | 警告码，详见 `AoqWarningCode` |
| `message` | `NSString *` | 警告描述 |

<a id="onconnectionstatuschange"></a>

<a id="26eaeda2bd70"></a>

<a id="0fb798a462cd"></a>

#### onConnectionStatusChange:

引擎连接状态变化回调。

<a id="code-block-50"></a>

```text
- (void)onConnectionStatusChange:(AoqConnectionStatus)status;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `status` | `AoqConnectionStatus` | 连接状态，详见 `AoqConnectionStatus` |

<a id="onstats"></a>

<a id="a827aee0c335"></a>

<a id="9a3032e02fd1"></a>

#### onStats:

引擎统计信息回调。

<a id="code-block-51"></a>

```text
- (void)onStats:(AoqStats * _Nonnull)stats;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `stats` | `AoqStats *` | 统计数据，详见 `AoqStats` |

<a id="onaudiodevicestatechanged"></a>

<a id="b6799c3b535f"></a>

<a id="3e7801adc26e"></a>

#### onAudioDeviceStateChanged:

音频设备采集 / 播放操作状态变化回调。

<a id="code-block-52"></a>

```text
- (void)onAudioDeviceStateChanged:(AoqAudioDeviceState * _Nonnull)state;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqAudioDeviceState *` | 音频设备状态，详见 `AoqAudioDeviceState` |

<a id="onaudiodeviceroutechanged"></a>

<a id="ff0e84cb00b5"></a>

<a id="63fe945b09e0"></a>

#### onAudioDeviceRouteChanged:

音频输出路由变化回调。

<a id="code-block-53"></a>

```text
- (void)onAudioDeviceRouteChanged:(NSInteger)routeType;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `routeType` | `NSInteger` | 路由类型，取值详见 `AoqAudioDeviceRouteType` |

<a id="onaudiofilestate"></a>

<a id="aaa3956fc514"></a>

<a id="99780972b3ff"></a>

#### onAudioFileState:

音频文件播放状态回调。

<a id="code-block-54"></a>

```text
- (void)onAudioFileState:(AoqAudioFileState * _Nonnull)state;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqAudioFileState *` | 文件播放状态，详见 `AoqAudioFileState` |

<a id="onlocalaudiovolumeindication"></a>

<a id="60b1483282e9"></a>

<a id="5fdbfecc5a5d"></a>

#### onLocalAudioVolumeIndication:

本地采集音量提示回调，需调用 `enableLocalAudioVolumeIndication:` 开启。

<a id="code-block-55"></a>

```text
- (void)onLocalAudioVolumeIndication:(AoqAudioVolume * _Nonnull)volume;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `volume` | `AoqAudioVolume *` | 本地音量信息，详见 `AoqAudioVolume` |

<a id="onvideodevicestatechanged"></a>

<a id="6bd114182a97"></a>

<a id="6c5016d5d9e9"></a>

#### onVideoDeviceStateChanged:

视频设备采集操作状态变化回调。

<a id="code-block-56"></a>

```text
- (void)onVideoDeviceStateChanged:(AoqVideoDeviceState * _Nonnull)state;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqVideoDeviceState *` | 视频设备状态，详见 `AoqVideoDeviceState` |

<a id="ondatamsg"></a>

<a id="90a7639c1fb7"></a>

<a id="b698f4693480"></a>

#### onDataMsg:

收到实时数据消息回调。

<a id="code-block-57"></a>

```text
- (void)onDataMsg:(AoqDataMsg * _Nonnull)msg;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `msg` | `AoqDataMsg *` | 数据消息，详见 `AoqDataMsg` |

<a id="aoqaudioframedelegate-2"></a>

<a id="ca57db6d4a1f"></a>

<a id="0d414192359d"></a>

<a id="aoq-api-category-15"></a>

### AoqAudioFrameDelegate

音频帧数据回调协议，所有方法均为 `@optional`。请不要在回调中做任何耗时操作，否则可能导致声音异常。

<a id="oncapturedaudioframe"></a>

<a id="fd9ef39c56a4"></a>

<a id="bd057ec44d81"></a>

#### onCapturedAudioFrame:

采集裸数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourceCaptured` 开启，支持设置采样率、声道数，支持读写模式。

<a id="code-block-58"></a>

```text
- (void)onCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `frame` | `AoqAudioFrameData *` | 采集音频裸数据，详见 `AoqAudioFrameData` |

<a id="onprocesscapturedaudioframe"></a>

<a id="42fc4fae5b3f"></a>

<a id="95f33aadd81e"></a>

#### onProcessCapturedAudioFrame:

3A 后数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourceProcessCaptured` 开启，支持设置采样率、声道数，支持读写模式。

<a id="code-block-59"></a>

```text
- (void)onProcessCapturedAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `frame` | `AoqAudioFrameData *` | 3A 处理后音频裸数据，详见 `AoqAudioFrameData` |

<a id="onpublishaudioframe-frame"></a>

<a id="437a2768f213"></a>

<a id="daf1f1a3bb21"></a>

#### onPublishAudioFrame:frame:

推流数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourcePublish` 开启，支持设置采样率、声道数，仅支持只读模式。

<a id="code-block-60"></a>

```text
- (void)onPublishAudioFrame:(AoqTrackType)trackType
                      frame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 音轨类型，详见 `AoqTrackType` |
| `frame` | `AoqAudioFrameData *` | 推流音频裸数据，详见 `AoqAudioFrameData` |

<a id="onplaybackaudioframe"></a>

<a id="b6b3ab943bba"></a>

<a id="8b583e78ae04"></a>

#### onPlaybackAudioFrame:

播放数据回调。通过 `enableAudioFrameObserver:` 设置 `audioSource = AoqAudioSourcePlayback` 开启，支持设置采样率、声道数，支持读写模式。

<a id="code-block-61"></a>

```text
- (void)onPlaybackAudioFrame:(AoqAudioFrameData * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `frame` | `AoqAudioFrameData *` | 播放音频裸数据，详见 `AoqAudioFrameData` |

<a id="aoqvideoframedelegate-2"></a>

<a id="9d9dc45694a0"></a>

<a id="d1e2f83251e6"></a>

<a id="aoq-api-category-16"></a>

### AoqVideoFrameDelegate

视频帧数据回调协议，所有方法均为 `@optional`。请不要在回调中做任何耗时操作，否则可能导致画面卡顿。回调返回 `YES` 表示数据已修改、需写回 SDK（写回仅对 I420 / CVPixelBuffer 生效）；返回 `NO` 表示只读。`frame` 中的数据仅在回调期间有效，异步使用需自行拷贝。

<a id="oncapturedvideoframe"></a>

<a id="19a03ecadee4"></a>

<a id="a3d931243db1"></a>

#### onCapturedVideoFrame:

本地采集后裸数据回调（前处理前）。通过 `enableVideoFrameObserver:` 设置 `videoSource = AoqVideoSourceCaptured` 开启。

<a id="code-block-62"></a>

```text
- (BOOL)onCapturedVideoFrame:(AoqTrackType)trackType frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `frame` | `AoqVideoFrame *` | 采集视频帧数据，详见 `AoqVideoFrame` |
| trackType | AoqTrackType | 视频轨道类型，支持 Video / Screen。 |

返回值：`YES` 数据已修改、需写回 SDK；`NO` 只读。

<a id="onpreencodevideoframe-frame"></a>

<a id="81f1745e2817"></a>

<a id="3c0f5e41120f"></a>

#### onPreEncodeVideoFrame:frame:

本地编码前裸数据回调（前处理后）。通过 `enableVideoFrameObserver:` 设置 `videoSource = AoqVideoSourcePreEncode` 开启。

<a id="code-block-63"></a>

```text
- (BOOL)onPreEncodeVideoFrame:(AoqTrackType)trackType
                        frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道类型，详见 `AoqTrackType` |
| `frame` | `AoqVideoFrame *` | 编码前视频帧数据，详见 `AoqVideoFrame` |

返回值：`YES` 数据已修改、需写回 SDK；`NO` 只读。

<a id="onremotevideoframe-frame"></a>

<a id="b9a937e3ec81"></a>

<a id="579153883a7b"></a>

#### onRemoteVideoFrame:frame:

远端解码后、渲染前裸数据回调。通过 `enableVideoFrameObserver:` 设置 `videoSource = AoqVideoSourceRemote` 开启。

<a id="code-block-64"></a>

```text
- (BOOL)onRemoteVideoFrame:(AoqTrackType)trackType
                     frame:(AoqVideoFrame * _Nonnull)frame;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道类型，详见 `AoqTrackType` |
| `frame` | `AoqVideoFrame *` | 远端视频帧数据，详见 `AoqVideoFrame` |

返回值：`YES` 数据已修改、需写回 SDK；`NO` 只读。

<a id="数据类型与枚举"></a>

<a id="f12b02111cbf"></a>

<a id="754e7c278654"></a>

## 数据类型与枚举

<a id="通用类型"></a>

<a id="7dbbd5f241c4"></a>

<a id="c30de1d03af2"></a>

### 通用类型

<a id="aoqcreateconfig"></a>

<a id="bfe1c07d72f2"></a>

<a id="eed0f444e642"></a>

#### AoqCreateConfig

引擎创建配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `workDir` | `NSString *` | `""` | SDK 工作目录 |
| `enableDumpAudio` | `BOOL` | `NO` | 是否开启音频原始数据 dump（调试用） |
| `extras` | `NSString *` | `""` | 扩展参数 |
| maxEncodedVideoFrameBytes | NSInteger | 190 × 1024 | 编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。0 表示关闭限制。 |
| enableDropOversizedVideoFrame | BOOL | NO | 仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。 |

<a id="aoqconnectconfig"></a>

<a id="fa745b60698b"></a>

<a id="3e7902dce8b5"></a>

#### AoqConnectConfig

连接 Relay 服务器配置。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `token` | `NSString *` | 连接鉴权 Token |
| `sid` | `NSString *` | 会话 ID |
| `certFingerprint` | `NSString *` | 服务器证书指纹 |
| `relayEndpoints` | `NSArray<AoqRelayEndpoint *> *` | Relay 接入点列表 |
| `workspaceIdHash` | `NSString *` | 工作空间哈希 ID |
| `publishTracks` | `NSArray<AoqTrackParam *> *` | 本端推流 track 属性数组 |
| `subscribeTracks` | `NSArray<AoqTrackParam *> *` | 本端拉流 track 属性数组 |

<a id="aoqrelayendpoint"></a>

<a id="86533ea39864"></a>

<a id="b58a1473e07b"></a>

#### AoqRelayEndpoint

Relay 接入点。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `routeIndex` | `NSInteger` | `-1` | 路径序号 |
| `endpoint` | `NSString *` | `""` | 服务端地址（域名或 IP） |
| `port` | `NSInteger` | `0` | 服务端端口 |
| tcpPort | NSInteger | 0 | TCP 降级端口；0 表示使用 SDK 默认端口 443。 |

<a id="aoqtrackparam"></a>

<a id="21f32641eb31"></a>

<a id="570fc294b704"></a>

#### AoqTrackParam

track 属性。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trackType` | `AoqTrackType` | `Audio` | track 类型 |
| `trackMode` | `AoqTrackMode` | `Segment` | 流式与非流式模式，仅对音频下行生效 |

<a id="aoqdatamsg"></a>

<a id="a5f6033fdb4d"></a>

<a id="e0d8895ec85c"></a>

#### AoqDataMsg

实时消息数据结构。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `NSData *` | 消息内容，指向调用方持有的内存 |

<a id="统计信息类型"></a>

<a id="7fb3aeef1450"></a>

<a id="6c1131f5ff28"></a>

### 统计信息类型

<a id="aoqstats"></a>

<a id="6547a2ac9c7c"></a>

<a id="86a11bf11767"></a>

#### AoqStats

引擎统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `audioPublishStats` | `NSArray<AoqAudioPublishStats *> *` | 音频推流统计数组 |
| `videoPublishStats` | `NSArray<AoqVideoPublishStats *> *` | 视频推流统计数组 |
| `dataMsgPublishStats` | `NSArray<AoqDataMsgPublishStats *> *` | 数据消息推流统计数组 |
| `audioSubscribeStats` | `NSArray<AoqAudioSubscribeStats *> *` | 音频拉流统计数组 |
| `videoSubscribeStats` | `NSArray<AoqVideoSubscribeStats *> *` | 视频拉流统计数组 |
| `dataMsgSubscribeStats` | `NSArray<AoqDataMsgSubscribeStats *> *` | 数据消息拉流统计数组 |
| `networkStats` | `AoqNetworkStats *` | 网络统计信息 |

<a id="aoqnetworkstats"></a>

<a id="0d62fd838f82"></a>

<a id="d91a1777cf69"></a>

#### AoqNetworkStats

网络统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sendBitrate` | `NSUInteger` | 发送码率（bps） |
| `sendBytes` | `NSUInteger` | 累计发送字节数 |
| `recvBitrate` | `NSUInteger` | 接收码率（bps） |
| `recvBytes` | `NSUInteger` | 累计接收字节数 |
| `loss` | `NSUInteger` | 丢包率（0-100） |
| `rtt` | `NSUInteger` | 往返延迟（ms） |

<a id="aoqaudiopublishstats"></a>

<a id="d3d933686770"></a>

<a id="dd142fc5bad8"></a>

#### AoqAudioPublishStats

音频推流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `NSUInteger` | 码率（bps） |
| `bytes` | `NSUInteger` | 累计字节数 |
| `encodeVolume` | `NSUInteger` | 推流编码音量 |

<a id="aoqvideopublishstats"></a>

<a id="d4df26baa7dd"></a>

<a id="41ad9a0276e8"></a>

#### AoqVideoPublishStats

视频推流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `NSUInteger` | 码率（bps） |
| `bytes` | `NSUInteger` | 累计字节数 |
| `encodeFps` | `NSUInteger` | 编码帧率 |

<a id="aoqdatamsgpublishstats"></a>

<a id="47c0d02cad5a"></a>

<a id="2e52c6768d0f"></a>

#### AoqDataMsgPublishStats

数据消息推流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `NSUInteger` | 码率（bps） |
| `bytes` | `NSUInteger` | 累计字节数 |

<a id="aoqaudiosubscribestats"></a>

<a id="2ba3be82c499"></a>

<a id="cf1e1224e73d"></a>

#### AoqAudioSubscribeStats

音频拉流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `NSUInteger` | 码率（bps） |
| `bytes` | `NSUInteger` | 累计字节数 |
| `playVolume` | `NSUInteger` | 播放音量 |

<a id="aoqvideosubscribestats"></a>

<a id="a9b6ed46bb41"></a>

<a id="0440768ab1f7"></a>

#### AoqVideoSubscribeStats

视频拉流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `NSUInteger` | 码率（bps） |
| `bytes` | `NSUInteger` | 累计字节数 |
| `decodeFps` | `NSUInteger` | 解码帧率 |
| `renderFps` | `NSUInteger` | 渲染帧率 |

<a id="aoqdatamsgsubscribestats"></a>

<a id="f637b5c95f73"></a>

<a id="81380624effe"></a>

#### AoqDataMsgSubscribeStats

数据消息拉流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `NSUInteger` | 码率（bps） |
| `bytes` | `NSUInteger` | 累计字节数 |

<a id="枚举类型"></a>

<a id="d108754b5a62"></a>

<a id="e6365c67dabb"></a>

### 枚举类型

<a id="aoqerrorcode"></a>

<a id="3fe5100c06e7"></a>

<a id="a22cd1d8b665"></a>

#### AoqErrorCode

错误码枚举。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqECOK` | 0 | 成功 |
| `AoqECParamInvalid` | 1 | 参数非法 |
| `AoqECStateInvalid` | 2 | 状态非法 |
| `AoqECUnSupport` | 3 | 接口不支持 |
| `AoqECAudio` | 100 | 音频通用错误 |
| `AoqECAudioExternalBufferFull` | 110 | 外部音频缓冲区满 |
| `AoqECAudioDevice` | 120 | 音频设备通用错误 |
| `AoqECAudioDeviceRecordingAuthFailed` | 121 | 录音权限未获取 |
| `AoqECAudioDeviceRecordingOccupied` | 122 | 录音设备被占用 |
| `AoqECAudioDeviceRecordingBackgroundStart` | 123 | 后台启动录音 |
| `AoqECAudioDeviceRecordingStartFail` | 124 | 录音启动失败 |
| `AoqECAudioDevicePlayoutOccupied` | 125 | 播放设备被占用 |
| `AoqECAudioDevicePlayoutBackgroundStart` | 126 | 后台启动播放 |
| `AoqECAudioDevicePlayoutStartFail` | 127 | 播放启动失败 |
| `AoqECVideo` | 200 | 视频通用错误 |
| `AoqECVideoExternalBufferFull` | 210 | 外部视频缓冲区满 |
| `AoqECVideoExternalCaptureNotEnabled` | 211 | 未启用外部视频采集 |
| `AoqECVideoExternalEncoderNotEnabled` | 212 | 未启用外部视频编码 |
| `AoqECVideoDevice` | 220 | 视频设备通用错误 |
| `AoqECVideoDeviceCameraOpenFail` | 221 | 摄像头打开失败 |
| `AoqECVideoDeviceCameraAuthFailed` | 222 | 摄像头权限未获取 |
| `AoqECVideoDeviceCameraOccupied` | 223 | 摄像头被占用 |
| `AoqECVideoDeviceCameraRunningError` | 224 | 摄像头运行错误 |
| `AoqECVideoCodec` | 230 | 视频编解码通用错误 |
| `AoqECVideoCodecEncoderInitFail` | 231 | 编码器初始化失败 |
| `AoqECVideoRender` | 240 | 视频渲染通用错误 |
| `AoqECVideoRenderCreateFail` | 241 | 渲染视图创建失败 |
| `AoqECVideoRenderDrawError` | 242 | 渲染绘制错误 |

<a id="aoqwarningcode"></a>

<a id="265ed299c540"></a>

<a id="c91c3dcf71fa"></a>

#### AoqWarningCode

警告码枚举。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqWCOK` | 0 | 无警告 |
| `AoqWCAudio` | 100 | 音频通用警告 |
| `AoqWCAudioHowling` | 101 | 音频啸叫检测 |
| `AoqWCAudioDevice` | 120 | 音频设备通用警告 |
| `AoqWCAudioDeviceMicEnumerateError` | 121 | 麦克风枚举错误 |
| `AoqWCAudioDeviceMicStartTimeout` | 122 | 麦克风启动超时 |
| `AoqWCAudioDeviceRecordingError` | 123 | 录音错误 |
| `AoqWCAudioDeviceSpeakerEnumerateError` | 124 | 扬声器枚举错误 |
| `AoqWCAudioDeviceSpeakerStartTimeout` | 125 | 扬声器启动超时 |
| `AoqWCAudioDevicePlayoutError` | 126 | 播放错误 |
| `AoqWCVideo` | 200 | 视频通用警告 |
| `AoqWCVideoCameraEnumerateError` | 201 | 摄像头枚举错误 |
| `AoqWCVideoEncoderSwitched` | 202 | 视频编码器已切换 |
| `AoqWCVideoRenderDowngrade` | 203 | 视频渲染降级 |

<a id="aoqtracktype"></a>

<a id="10a9c6a60083"></a>

<a id="47f3d99e128f"></a>

#### AoqTrackType

轨道类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqTrackTypeAudio` | 0 | 音频轨道 |
| `AoqTrackTypeVideo` | 1 | 视频轨道 |
| `AoqTrackTypeData` | 2 | 数据消息轨道 |
| AoqTrackTypeScreen | 3 | 屏幕共享轨道，支持上行。 |

<a id="aoqencodertype"></a>

<a id="eeaa821807b7"></a>

<a id="8c23a1705af2"></a>

#### AoqEncoderType

编码器类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqEncoderTypeUnknown` | 0 | 未知格式 |
| `AoqEncoderTypeAudioPCM` | 1 | 音频 PCM |
| `AoqEncoderTypeAudioOpus` | 2 | 音频 Opus |
| `AoqEncoderTypeVideoH264` | 3 | 视频 H.264 |
| `AoqEncoderTypeVideoJpeg` | 4 | 视频 JPEG |
| `AoqEncoderTypeDataText` | 5 | 数据文本 |

<a id="aoqtrackmode"></a>

<a id="0e2883a5b3a2"></a>

<a id="ebbb9cd49726"></a>

#### AoqTrackMode

流式与非流式模式，仅对音频下行生效。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqTrackModeSegment` | 0 | 分段：数据按语义片段（如一句话）打包送达 |
| `AoqTrackModeStream` | 1 | 流式：数据持续、连续地送达 |

<a id="aoqconnectionstatus"></a>

<a id="efb7d2daa52a"></a>

<a id="b745e0c2e803"></a>

#### AoqConnectionStatus

引擎连接状态。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqConnectionStatusDisconnected` | 0 | 未连接 |
| `AoqConnectionStatusConnecting` | 1 | 连接中 |
| `AoqConnectionStatusConnected` | 2 | 已连接 |
| `AoqConnectionStatusFailed` | 3 | 连接失败 |

<a id="音频类型"></a>

<a id="7772afb37b1c"></a>

<a id="e78befcafa59"></a>

### 音频类型

<a id="aoqaudiocaptureconfig"></a>

<a id="8e7dac8f383e"></a>

<a id="55191a7475de"></a>

#### AoqAudioCaptureConfig

音频采集配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `isExternal` | `BOOL` | `NO` | 是否外部采集 |
| `channel` | `NSInteger` | `1` | 音频采集通道数，支持 1/2 |

<a id="aoqaudioplaybackconfig"></a>

<a id="50871b08e8d1"></a>

<a id="0b30f197ac02"></a>

#### AoqAudioPlaybackConfig

音频播放配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `isExternal` | `BOOL` | `NO` | 是否外部播放 |
| `channel` | `NSInteger` | `1` | 音频播放通道数，支持 1/2 |

<a id="aoqaudiocodecconfig"></a>

<a id="d85574657aca"></a>

<a id="87b9f458d857"></a>

#### AoqAudioCodecConfig

音频编解码配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trackType` | `AoqTrackType` | `Audio` | 轨道类型 |
| `codecType` | `AoqEncoderType` | `AudioOpus` | 编码格式 |
| `sampleRate` | `NSInteger` | `48000` | 采样率（Hz） |
| `channel` | `NSInteger` | `1` | 声道数 |
| `bitrate` | `NSInteger` | `32000` | 比特率（bps） |

<a id="aoqaudiodevicestatecode"></a>

<a id="65aa485e00cd"></a>

<a id="95bf5350f070"></a>

#### AoqAudioDeviceStateCode

音频设备状态码。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioDeviceNone` | 0 | 无状态 |
| `AoqAudioDeviceRecordStarting` | 1 | 采集正在启动 |
| `AoqAudioDeviceRecordStarted` | 2 | 采集已启动 |
| `AoqAudioDeviceRecordStopping` | 3 | 采集正在停止 |
| `AoqAudioDeviceRecordStopped` | 4 | 采集已停止 |
| `AoqAudioDeviceRecordFail` | 5 | 采集失败 |
| `AoqAudioDevicePlayStarting` | 6 | 播放正在启动 |
| `AoqAudioDevicePlayStarted` | 7 | 播放已启动 |
| `AoqAudioDevicePlayStopping` | 8 | 播放正在停止 |
| `AoqAudioDevicePlayStopped` | 9 | 播放已停止 |
| `AoqAudioDevicePlayFail` | 10 | 播放失败 |

<a id="aoqaudiodevicestate"></a>

<a id="a769fa1666ef"></a>

<a id="5fa4025c496a"></a>

#### AoqAudioDeviceState

音频设备状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqAudioDeviceStateCode` | 状态码 |
| `reason` | `NSInteger` | 错误码（`AoqErrorCode`） |

<a id="aoqaudiodeviceroutetype"></a>

<a id="4522acb9ef0a"></a>

<a id="e914c3d7115c"></a>

#### AoqAudioDeviceRouteType

音频设备路由类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioDeviceRouteDefault` | 0 | 默认 |
| `AoqAudioDeviceRouteHeadset` | 1 | 耳机 |
| `AoqAudioDeviceRouteEarpiece` | 2 | 听筒 |
| `AoqAudioDeviceRouteHeadsetNoMic` | 3 | 无麦耳机 |
| `AoqAudioDeviceRouteSpeakerPhone` | 4 | 内置扬声器 |
| `AoqAudioDeviceRouteUsb` | 5 | USB |
| `AoqAudioDeviceRouteBluetooth` | 6 | 蓝牙 |
| `AoqAudioDeviceRouteBluetoothA2dp` | 7 | 蓝牙 A2DP |

<a id="音频文件类型"></a>

### 音频文件类型

<a id="aoqaudiofilemixconfig"></a>

<a id="4577f4932d28"></a>

<a id="856f8de1a37f"></a>

#### AoqAudioFileMixConfig

音频文件推流播放配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `fileName` | `NSString *` | \- | 文件名（含路径），必填 |
| `cycles` | `NSInteger` | `-1` | 循环次数，-1 表示无限循环 |
| `startPosMs` | `NSInteger` | `0` | 起始播放位置（ms） |
| `publishVolume` | `NSInteger` | `100` | 推流音量，范围 \[0, 100\] |
| `playoutVolume` | `NSInteger` | `100` | 播放音量，范围 \[0, 100\] |

<a id="aoqaudiofilestatecode"></a>

<a id="516e5577cb8c"></a>

<a id="4907a22eb813"></a>

#### AoqAudioFileStateCode

音频文件状态码。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioFileNone` | 0 | 无状态 |
| `AoqAudioFileStarted` | 1 | 开始播放 |
| `AoqAudioFileStopped` | 2 | 停止播放 |
| `AoqAudioFilePaused` | 3 | 暂停播放 |
| `AoqAudioFileResumed` | 4 | 恢复播放 |
| `AoqAudioFileEnded` | 5 | 播放完毕 |
| `AoqAudioFileBuffering` | 6 | 正在缓冲 |
| `AoqAudioFileBufferingEnd` | 7 | 缓冲结束 |
| `AoqAudioFileFailed` | 8 | 播放失败 |

<a id="aoqaudiofileerrorcode"></a>

<a id="5528036090e5"></a>

<a id="b155fc9c7de7"></a>

#### AoqAudioFileErrorCode

音频文件播放错误码。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioFileNoError` | 0 | 没有错误 |
| `AoqAudioFileOpenFailed` | 1 | 打开文件失败 |
| `AoqAudioFileDecodeFailed` | 2 | 解码文件失败 |

<a id="aoqaudiofilestate"></a>

<a id="2266efc0fd2a"></a>

<a id="3e8c30a8d288"></a>

#### AoqAudioFileState

音频文件状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `NSString *` | 文件 ID |
| `stateCode` | `AoqAudioFileStateCode` | 状态码 |
| `errorCode` | `AoqAudioFileErrorCode` | 错误码 |

<a id="外部音频流与音量类型"></a>

### 外部音频流与音量类型

<a id="aoqaudiostreamdirection"></a>

<a id="da9c9b6b0420"></a>

<a id="62f229fbb122"></a>

#### AoqAudioStreamDirection

外部音频流方向。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioStreamPublish` | 0 | 推流音频 |
| `AoqAudioStreamPlayout` | 1 | 播放音频 |

<a id="aoqaudioexternalstreamtoggle"></a>

<a id="9df9b344d7f9"></a>

<a id="4f46a3401fc1"></a>

#### AoqAudioExternalStreamToggle

外部音频流切换状态。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioExternalStreamToggleNormal` | 0 | 恢复正常 |
| `AoqAudioExternalStreamTogglePause` | 1 | 暂停 |

<a id="aoqaudioexternalstreamconfig"></a>

<a id="a4a9dcde5a27"></a>

<a id="1674e432627e"></a>

#### AoqAudioExternalStreamConfig

外部音频流配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trackType` | `AoqTrackType` | `Audio` | 音频轨道类型 |
| `codecType` | `AoqEncoderType` | `AudioPCM` | 音频流格式，支持 PCM |
| `channels` | `NSInteger` | `1` | 声道数 |
| `sampleRate` | `NSInteger` | `48000` | 采样率（Hz） |
| `playoutVolume` | `NSInteger` | `100` | 播放音量，范围 \[0, 100\] |
| `publishVolume` | `NSInteger` | `100` | 推流音量，范围 \[0, 100\] |
| `maxBufferDuration` | `NSInteger` | `1000` | 最大缓冲时长（ms） |
| `enable3A` | `BOOL` | `NO` | 输入 PCM 是否做 3A 处理 |

<a id="aoqaudioframedata"></a>

<a id="5bbda6187037"></a>

<a id="9c6f3494e07f"></a>

#### AoqAudioFrameData

外部音频数据。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `dataPtr` | `void *` | 音频 PCM 裸数据指针 |
| `dataSize` | `NSInteger` | PCM 数据字节数 |
| `numOfSamples` | `NSInteger` | 采样点数（单声道） |
| `bytesPerSample` | `NSInteger` | 每个采样点字节数 |
| `numOfChannels` | `NSInteger` | 声道数 |
| `samplesPerSec` | `NSInteger` | 每秒采样点数 |
| `pushSequence` | `int32_t` | PCM 输入轮次 |
| `timeStamp` | `int64_t` | 时间戳 |
| `autoGenMute` | `BOOL` | 数据回调有效，`YES` 表示 SDK 生成的静音数据 |

<a id="aoqaudiosource"></a>

<a id="43dd10a3c6a5"></a>

<a id="cdfc294b6724"></a>

#### AoqAudioSource

音频帧回调数据来源。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioSourceCaptured` | 0 | 采集的音频数据 |
| `AoqAudioSourceProcessCaptured` | 1 | 3A 后的音频数据 |
| `AoqAudioSourcePublish` | 2 | 推流的音频数据（需 Connect 成功） |
| `AoqAudioSourcePlayback` | 3 | 播放的音频数据 |

<a id="aoqaudioobservermode"></a>

<a id="0a1e84e55132"></a>

<a id="cf87e52060da"></a>

#### AoqAudioObserverMode

音频帧回调模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioObserverModeReadOnly` | 0 | 只读 |
| `AoqAudioObserverModeReadWrite` | 1 | 读写 |

<a id="aoqaudioobserverconfig"></a>

<a id="9e8e4fb05096"></a>

<a id="e0fd24cba102"></a>

#### AoqAudioObserverConfig

音频帧回调配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sampleRate` | `NSInteger` | `48000` | 回调音频采样率 |
| `channels` | `NSInteger` | `1` | 回调音频声道数 |
| `mode` | `AoqAudioObserverMode` | `ReadOnly` | 读写模式 |

<a id="aoqaudiovolumeindicationconfig"></a>

<a id="3203ee64d8c6"></a>

<a id="2b85baf1d900"></a>

#### AoqAudioVolumeIndicationConfig

本地音量提示配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| reportSpeech | BOOL | NO | 是否检测人声。 |
| interval | NSInteger | 0 | 回调间隔（毫秒）；小于等于 0 时关闭，大于 0 且小于 10 时按 10 处理。 |
| smooth | NSInteger | 3 | 平滑系数，范围 0～10；越大越平滑。 |

<a id="aoqaudiovolume"></a>

<a id="0e1b7b9651ed"></a>

<a id="8aba98a38c7c"></a>

#### AoqAudioVolume

本地音量信息。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isSpeech | BOOL | NO | 是否为人声。 |
| volume | NSInteger | 0 | 平滑后的瞬时音量，范围 0～255。 |

<a id="视频类型"></a>

<a id="2afb1912a750"></a>

<a id="c354bef7242d"></a>

### 视频类型

<a id="aoqvideocaptureconfig"></a>

<a id="566fa296fdba"></a>

<a id="cde328a703a7"></a>

#### AoqVideoCaptureConfig

视频采集配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `width` | `NSInteger` | `1280` | 采集宽度（像素）；`isExternal=YES` 时无效 |
| `height` | `NSInteger` | `720` | 采集高度（像素）；`isExternal=YES` 时无效 |
| `fps` | `NSInteger` | `15` | 采集帧率；`isExternal=YES` 时无效（节奏由送帧决定） |
| `isExternal` | `BOOL` | `NO` | 是否外部采集；`YES` 时不打开摄像头，由 `pushExternalVideoCapturedFrame:` 喂帧 |

<a id="aoqvideocanvas"></a>

<a id="ca34b2901390"></a>

<a id="0ad24da46a66"></a>

#### AoqVideoCanvas

视频渲染数据结构。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `view` | `NSView *` | `nil` | 显示视图，传 nil 表示移除渲染绑定 |
| `renderMode` | `AoqRenderMode` | `Auto` | 渲染模式 |

调用方需保证 `view` 生命周期长于 `setLocalView:` / `setRemoteView:` 设置期间。

<a id="aoqrendermode"></a>

<a id="9d09b47035c4"></a>

<a id="21b813017a0e"></a>

#### AoqRenderMode

渲染显示模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqRenderModeAuto` | 0 | 自动模式 |
| `AoqRenderModeStretch` | 1 | 拉伸平铺模式，宽高比不一致时拉伸到目标比例，画面会变形 |
| `AoqRenderModeFill` | 2 | 填充黑边模式，宽高比不一致时上下或左右填充黑边 |
| `AoqRenderModeCrop` | 3 | 裁剪模式，宽高比不一致时裁剪宽或高，画面内容会丢失 |

<a id="aoqrenderview"></a>

<a id="248b81f24a10"></a>

<a id="ed01a1b137df"></a>

#### AoqRenderView

渲染视图控件，继承自 `NSView`，可作为 `AoqVideoCanvas.view` 使用。

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `engineDisplayView` | `NSView *`（只读） | 引擎内部显示视图 |
| `renderWidth` | `int`（只读） | 渲染宽度 |
| `renderHeight` | `int`（只读） | 渲染高度 |
| `enableMetal` | `BOOL`（只读） | 是否启用 Metal 渲染 |
| `delegate` | `id<AoqRenderViewDelegate>` | 渲染视图事件委托 |

<a id="aoqrenderviewdelegate"></a>

<a id="46fa661b1353"></a>

<a id="cb2227bff1ab"></a>

#### AoqRenderViewDelegate

渲染视图事件委托协议。

<a id="code-block-65"></a>

```text
- (void)onRenderViewSizeChanged:(AoqRenderView * _Nonnull)view;
```

| 回调 | 说明 |
| --- | --- |
| `onRenderViewSizeChanged:` | 渲染视图尺寸变化回调 |

<a id="aoqvideopixelformat"></a>

<a id="9455a6e8914a"></a>

<a id="dcdb68475533"></a>

#### AoqVideoPixelFormat

视频像素格式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoPixelFormatUnknown` | 0 | 未知格式 |
| `AoqVideoPixelFormatI420` | 1 | I420 |
| `AoqVideoPixelFormatNV12` | 2 | NV12 |
| `AoqVideoPixelFormatNV21` | 3 | NV21 |
| `AoqVideoPixelFormatBGRA` | 4 | BGRA |
| `AoqVideoPixelFormatRGBA` | 5 | RGBA |
| `AoqVideoPixelFormatCVPixelBuffer` | 6 | 零拷贝路径，`pixelBuffer` 字段填 `CVPixelBufferRef` |

<a id="aoqvideoframe"></a>

<a id="456401f4c2b0"></a>

<a id="240e2c8d5b17"></a>

#### AoqVideoFrame

外部视频数据。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `format` | `AoqVideoPixelFormat` | 像素格式 |
| `width` | `NSInteger` | 宽度（像素） |
| `height` | `NSInteger` | 高度（像素） |
| `data` | `NSData *` | 打包格式数据（NV12/NV21/BGRA/RGBA） |
| `dataY` / `dataU` / `dataV` | `NSData *` | I420 三平面数据 |
| `strideY` / `strideU` / `strideV` | `NSInteger` | I420 三平面步长 |
| `pixelBuffer` | `CVPixelBufferRef` | 零拷贝，`format=AoqVideoPixelFormatCVPixelBuffer` 时使用 |
| `timeStamp` | `int64_t` | 时间戳（ms）；0 时 SDK 用本地时钟补 |

<a id="aoqvideocodectype"></a>

<a id="c66e076dc930"></a>

<a id="38586533f3db"></a>

#### AoqVideoCodecType

外部编码帧 codec 类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoCodecTypeJPEG` | 0 | JPEG |

<a id="aoqvideoencodedframe"></a>

<a id="2b5141998711"></a>

<a id="1238aa9ae51b"></a>

#### AoqVideoEncodedFrame

外部已编码视频帧。调用方自行完成编码，SDK 不做二次编码，直接打包发送。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `codec` | `AoqVideoCodecType` | 编码格式 |
| `data` | `NSData *` | 编码后数据 |
| `width` | `NSInteger` | 宽度（像素） |
| `height` | `NSInteger` | 高度（像素） |
| `timeStamp` | `int64_t` | 时间戳（ms）；0 时 SDK 用本地时钟补 |

<a id="aoqvideocodecconfig"></a>

<a id="c42fa632a13d"></a>

<a id="4d1a3bbc242f"></a>

#### AoqVideoCodecConfig

视频编解码参数（编解码共用）。用于解码时仅 `trackType` / `codecType` / `width` / `height` / `fps` / `bitrate` 生效（作为订阅提议参与协商），其余字段仅编码使用。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `isExternal` | `BOOL` | `NO` | 外部编码模式；`YES` 时由客户推送已编码帧，SDK 不做采集和编码 |
| `trackType` | `AoqTrackType` | `Video` | 轨道类型 |
| `codecType` | `AoqEncoderType` | `VideoH264` | 编码格式 |
| `width` | `NSInteger` | `540` | 分辨率宽 |
| `height` | `NSInteger` | `960` | 分辨率高 |
| `fps` | `NSInteger` | `5` | 帧率 |
| `bitrate` | `NSInteger` | `500000` | 起始码率（bps） |
| `minBitrate` | `NSInteger` | `128000` | 最小码率（bps） |
| `keyframeInterval` | `NSInteger` | `2` | 关键帧间隔（秒） |
| `mirrorMode` | `AoqMirrorMode` | `Disabled` | 镜像模式 |
| `orientationMode` | `AoqOrientationMode` | `Auto` | 方向模式 |

<a id="aoqmirrormode"></a>

<a id="a8004c442d6d"></a>

<a id="d21d46b0f130"></a>

#### AoqMirrorMode

镜像模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqMirrorModeDisabled` | 0 | 关闭镜像 |
| `AoqMirrorModeEnabled` | 1 | 开启镜像 |

<a id="aoqorientationmode"></a>

<a id="909d5e2dd845"></a>

<a id="95529f330ec5"></a>

#### AoqOrientationMode

方向模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqOrientationModeAuto` | 0 | 自动 |
| `AoqOrientationModePortrait` | 1 | 竖屏 |
| `AoqOrientationModeLandscape` | 2 | 横屏 |

<a id="aoqvideodevicestatecode"></a>

<a id="bd406efa92c7"></a>

<a id="b15d67a4508e"></a>

#### AoqVideoDeviceStateCode

视频设备状态码。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoDeviceNone` | 0 | 无状态 |
| `AoqVideoDeviceCaptureStarting` | 1 | 摄像头正在启动 |
| `AoqVideoDeviceCaptureStarted` | 2 | 摄像头已启动 |
| `AoqVideoDeviceCaptureStopping` | 3 | 摄像头正在停止 |
| `AoqVideoDeviceCaptureStopped` | 4 | 摄像头已停止 |
| `AoqVideoDeviceCaptureFail` | 5 | 摄像头启动失败 |

<a id="aoqvideodevicestate"></a>

<a id="430cc3e563bd"></a>

<a id="53053117285e"></a>

#### AoqVideoDeviceState

视频设备状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqVideoDeviceStateCode` | 状态码 |
| `reason` | `NSInteger` | 错误码（`AoqErrorCode`） |

<a id="aoqvideosource"></a>

<a id="5dab3781b77a"></a>

<a id="418539a8369c"></a>

#### AoqVideoSource

视频帧回调数据源（管线位置）。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoSourceCaptured` | 0 | 采集后的视频数据（前处理前） |
| `AoqVideoSourcePreEncode` | 1 | 编码前的视频数据（前处理后） |
| `AoqVideoSourceRemote` | 2 | 远端解码后、渲染前的视频数据 |

<a id="aoqvideoobservermode"></a>

<a id="e5e09fcc29a4"></a>

<a id="3e0387c6422c"></a>

#### AoqVideoObserverMode

视频帧回调模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoObserverModeReadOnly` | 0 | 只读 |
| `AoqVideoObserverModeReadWrite` | 1 | 读写 |

<a id="aoqvideoobserveralignment"></a>

<a id="2ef1df48442c"></a>

<a id="fbc82f013dbc"></a>

#### AoqVideoObserverAlignment

视频输出宽度对齐方式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoObserverAlignmentDefault` | 0 | 默认 |
| `AoqVideoObserverAlignmentEven` | 1 | 偶数对齐 |
| `AoqVideoObserverAlignment4` | 2 | 4 对齐 |
| `AoqVideoObserverAlignment8` | 3 | 8 对齐 |
| `AoqVideoObserverAlignment16` | 4 | 16 对齐 |

<a id="aoqvideoobserverconfig"></a>

<a id="70cd705df3b4"></a>

<a id="5872956c3dd0"></a>

#### AoqVideoObserverConfig

视频帧回调配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `format` | `AoqVideoPixelFormat` | `I420` | 期望回调像素格式 |
| `alignment` | `AoqVideoObserverAlignment` | `Default` | 宽度对齐策略 |
| `mode` | `AoqVideoObserverMode` | `ReadOnly` | 读写模式，仅 I420 / CVPixelBuffer 支持 ReadWrite |
| `mirrorApplied` | `BOOL` | `NO` | 是否对回调数据应用镜像 |
| trackType | AoqTrackType | AoqTrackTypeVideo | 需要观察的视频轨道；仅支持 Video / Screen。 |

<a id="屏幕采集类型"></a>

### 屏幕采集类型

<a id="aoqscreensharesourcetype"></a>

#### AoqScreenShareSourceType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqScreenShareSourceTypeDesktop | 0 | 整个桌面 |
| AoqScreenShareSourceTypeWindow | 1 | 指定窗口 |

<a id="aoqscreensourceinfo"></a>

#### AoqScreenSourceInfo

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| sourceType | AoqScreenShareSourceType | Desktop | 源类型 |
| sourceId | int64\_t | 0 | 源 ID |
| sourceName | NSString \* | — | 源名称 |
| sourceIsSelf | BOOL | — | 是否为自身进程窗口 |

<a id="aoqscreensourcelist"></a>

#### AoqScreenSourceList

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| sourceList | NSArray<AoqScreenSourceInfo \*> \* | 屏幕源数组 |

<a id="aoqscreencaptureconfig"></a>

#### AoqScreenCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isExternal | BOOL | NO | 是否由应用提供屏幕原始帧。 |
| sourceId | int64\_t | 0 | 屏幕源 ID。 |
| sourceType | AoqScreenShareSourceType | AoqScreenShareSourceTypeWindow | 屏幕源类型。 |
