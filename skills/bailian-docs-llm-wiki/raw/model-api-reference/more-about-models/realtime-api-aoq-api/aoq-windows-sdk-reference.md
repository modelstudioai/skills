# AOQ Client SDK Windows API 参考

本文介绍 AOQ Client SDK Windows 版的 C++ 接口、回调和数据类型，帮助您在 Windows 应用中接入实时音视频和数据消息能力。

> **说明**
>
> AOQ SDK 提供通用视频接口。[Qwen-Audio-Realtime](../../realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md) 不支持视频输入或输出；其他模型可使用的媒体能力以对应接入文档为准。

SDK 以全局单例方式持有引擎实例，通过 `AoqClientEngine` 类对外提供接口，通过 `AoqEngineEventListener` 抽象类统一回调异步事件。所有类型定义位于 `AoqClientSdk` 命名空间，头文件为 `AoqClientEngine.h`。

> **说明**
>
> 所有 `const char*` 字符串由调用方负责生命周期，至少需保持到相应调用返回后，引擎内部将按需拷贝。

<a id="接口目录"></a>

<a id="78781eb18b11"></a>

<a id="4138388acd2a"></a>

## 接口目录

<a id="引擎生命周期"></a>

<a id="2df02a188bfc"></a>

<a id="3853d5fc7e0a"></a>

### 引擎生命周期

| 接口 | 简介 |
| --- | --- |
| `createEngine` | 创建引擎实例（单例模式） |
| `destroy` | 销毁引擎实例 |
| `getVersion` | 获取 SDK 版本号 |
| `connect` | 连接 Relay 服务器 |
| `disconnect` | 断开服务器连接 |

<a id="音频设备管理"></a>

<a id="8856b05de229"></a>

<a id="b4fb44f6eb28"></a>

### 音频设备管理

| 接口 | 简介 |
| --- | --- |
| `startAudioCapture` | 打开音频采集设备（麦克风） |
| `stopAudioCapture` | 关闭音频采集设备 |
| `muteAudioCapture` | 静音或取消静音音频采集 |
| `startAudioPlayer` | 开始音频渲染（播放远端音频） |
| `stopAudioPlayer` | 停止音频渲染 |
| `pauseAudioPlayer` | 暂停音频渲染（支持淡出） |
| `resumeAudioPlayer` | 恢复音频渲染（支持淡入） |
| `interruptAudioPlayer` | 打断本轮音频通话 |
| `enableLocalAudioVolumeIndication` | 开启或关闭本地采集音量提示 |

<a id="音频编码配置"></a>

<a id="49ccee1e595a"></a>

<a id="ef974c1ad8ee"></a>

### 音频编码配置

| 接口 | 简介 |
| --- | --- |
| `setAudioEncoderConfig` | 设置音频编码参数 |
| `setAudioDecoderConfig` | 设置音频解码参数 |

<a id="视频设备管理"></a>

<a id="895e7d4b0734"></a>

<a id="49303f7eebef"></a>

### 视频设备管理

| 接口 | 简介 |
| --- | --- |
| `startVideoCapture` | 打开视频采集设备（摄像头） |
| `stopVideoCapture` | 关闭视频采集设备 |
| `setLocalView` | 设置或移除本地视频渲染窗口 |
| `setRemoteView` | 设置或移除远端视频渲染窗口 |

<a id="视频编码与外部输入"></a>

<a id="028a6d30aa32"></a>

<a id="5e7b6d28c285"></a>

### 视频编码与外部输入

| 接口 | 简介 |
| --- | --- |
| `setVideoEncoderConfig` | 设置视频编码参数 |
| `setVideoDecoderConfig` | 设置视频解码参数 |
| `pushExternalVideoCapturedFrame` | 推送外部采集视频帧 |
| `pushExternalVideoEncodedFrame` | 推送外部已编码视频帧 |

<a id="屏幕采集"></a>

### 屏幕采集

| 接口 | 简介 |
| --- | --- |
| `getScreenSourceList` | 获取屏幕采集源列表（桌面端独有） |
| `startScreenCapture` | 启动屏幕采集 |
| `stopScreenCapture` | 停止屏幕采集 |

<a id="媒体流发送控制"></a>

<a id="973aebc4bc3c"></a>

<a id="74db1f031e94"></a>

### 媒体流发送控制

| 接口 | 简介 |
| --- | --- |
| `enableSendMediaStream` | 控制本地媒体流的发送开关 |

<a id="音频文件播放"></a>

<a id="86db58654184"></a>

<a id="28f63a96752c"></a>

### 音频文件播放

| 接口 | 简介 |
| --- | --- |
| `startAudioFile` | 开始推流播放本地音频文件 |
| `stopAudioFile` | 停止音频文件播放 |
| `pauseAudioFile` | 暂停音频文件播放 |
| `resumeAudioFile` | 恢复音频文件播放 |
| `getAudioFileDuration` | 获取音频文件总时长 |
| `getAudioFileCurrentPosition` | 获取音频文件当前播放位置 |
| `setAudioFilePositionMillis` | 设置音频文件播放位置（seek） |
| `setAudioFileVolume` | 设置音频文件音量 |
| `getAudioFileVolume` | 获取音频文件当前音量 |

<a id="外部音频流"></a>

<a id="54debe099706"></a>

<a id="d6b4c13dff30"></a>

### 外部音频流

| 接口 | 简介 |
| --- | --- |
| `addAudioExternalStream` | 新增一条外部音频流 |
| `pushAudioExternalStreamData` | 输入外部音频 PCM 数据 |
| `setAudioExternalStreamVolume` | 设置外部音频流音量 |
| `getAudioExternalStreamVolume` | 获取外部音频流音量 |
| `clearAudioExternalStreamBuffer` | 清空外部音频流缓存 |
| `removeAudioExternalStream` | 移除外部音频流 |

<a id="实时消息"></a>

<a id="b8d7effa1bfe"></a>

<a id="a66495101cc7"></a>

### 实时消息

| 接口 | 简介 |
| --- | --- |
| `sendDataMsg` | 发送实时数据消息 |

<a id="音频帧回调"></a>

<a id="a3edc1b40a23"></a>

<a id="b2a326f23d00"></a>

### 音频帧回调

| 接口 | 简介 |
| --- | --- |
| `setAudioFrameObserver` | 设置音频帧数据回调监听 |
| `enableAudioFrameObserver` | 开启或关闭指定位置的音频帧回调 |

<a id="视频帧回调"></a>

<a id="725d0c463579"></a>

<a id="7d6304a9d294"></a>

### 视频帧回调

| 接口 | 简介 |
| --- | --- |
| `setVideoFrameObserver` | 设置视频帧数据回调监听 |
| `enableVideoFrameObserver` | 开启或关闭指定位置的视频帧回调 |

<a id="aoqengineeventlistener"></a>

<a id="e12896e8dd94"></a>

<a id="e7a57cbf6d8b"></a>

### AoqEngineEventListener

| 接口 | 简介 |
| --- | --- |
| `onError` | 引擎错误回调 |
| `onWarning` | 引擎警告回调 |
| `onConnectionStatusChange` | 连接状态变化回调 |
| `onStats` | 引擎统计信息回调 |
| `onAudioDeviceStateChanged` | 音频设备操作状态变化回调 |
| `onAudioDeviceRouteChanged` | 音频输出路由变化回调 |
| `onAudioFileState` | 音频文件播放状态回调 |
| `onLocalAudioVolumeIndication` | 本地采集音量提示回调 |
| `onVideoDeviceStateChanged` | 视频设备操作状态变化回调 |
| `onDataMsg` | 收到实时数据消息回调 |

<a id="iaudioframeobserver"></a>

### IAudioFrameObserver

| 接口 | 简介 |
| --- | --- |
| onCapturedAudioFrame | 采集裸数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourceCaptured` 开启，支持设置采样率、声道数，支持读写模式。 |
| onProcessCapturedAudioFrame | 3A 后数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourceProcessCaptured` 开启，支持设置采样率、声道数，支持读写模式。 |
| onPublishAudioFrame | 推流数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourcePublish` 开启，支持设置采样率、声道数，仅支持只读模式。 |
| onPlaybackAudioFrame | 播放数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourcePlayback` 开启，支持设置采样率、声道数，支持读写模式。 |

<a id="ivideoframeobserver"></a>

### IVideoFrameObserver

| 接口 | 简介 |
| --- | --- |
| onCapturedVideoFrame | 本地采集后裸数据回调（前处理前）。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourceCaptured` 开启。 |
| onPreEncodeVideoFrame | 本地编码前裸数据回调（前处理后）。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourcePreEncode` 开启。 |
| onRemoteVideoFrame | 远端解码后、渲染前裸数据回调。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourceRemote` 开启。 |

<a id="接口详情"></a>

<a id="137213dfda56"></a>

<a id="4b5e018041ca"></a>

## 接口详情

<a id="引擎生命周期-2"></a>

<a id="ebbe3a5d59ba"></a>

<a id="3853d5fc7e0a-details"></a>

<a id="aoq-api-category-1"></a>

### 引擎生命周期

<a id="createengine"></a>

<a id="b0593a8a2b74"></a>

<a id="217b83ce21b4"></a>

#### createEngine

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

<a id="code-block"></a>

```cpp
static AoqClientEngine* createEngine(const AoqCreateConfig& config,
                                     AoqEngineEventListener* listener);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqCreateConfig&` | 引擎创建配置，详见 `AoqCreateConfig` |
| `listener` | `AoqEngineEventListener*` | 事件回调监听器，详见 `AoqEngineEventListener` |

返回值：引擎实例指针，失败返回 `nullptr`。

<a id="destroy"></a>

<a id="d0fa17158df9"></a>

<a id="3c32463acd34"></a>

#### destroy

销毁引擎实例。销毁后需重新调用 `createEngine` 方可继续使用。

<a id="code-block-2"></a>

```cpp
static int destroy();
```

返回值：0 表示成功；非 0 表示失败。

<a id="getversion"></a>

<a id="32c06938a3fa"></a>

<a id="9ee46ccd02a5"></a>

#### getVersion

获取 SDK 的版本号。

<a id="code-block-3"></a>

```cpp
static const char* getVersion();
```

返回值：版本号字符串。

<a id="connect"></a>

<a id="9b81eca2100d"></a>

<a id="0e054fb286f7"></a>

#### connect

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

<a id="code-block-4"></a>

```cpp
virtual int connect(const AoqConnectConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqConnectConfig&` | 连接鉴权配置，详见 `AoqConnectConfig` |

返回值：0 表示调用已下发（异步执行）；非 0 表示参数校验失败。

<a id="disconnect"></a>

<a id="cd0f29877845"></a>

<a id="22d67fb3d286"></a>

#### disconnect

断开服务器连接。

<a id="code-block-5"></a>

```cpp
virtual int disconnect();
```

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

<a id="音频设备管理-2"></a>

<a id="17e1d9ab708e"></a>

<a id="b4fb44f6eb28-details"></a>

<a id="aoq-api-category-2"></a>

### 音频设备管理

<a id="startaudiocapture"></a>

<a id="ae943695acb8"></a>

<a id="9b12ccc07e71"></a>

#### startAudioCapture

打开音频采集设备（麦克风）。

<a id="code-block-6"></a>

```cpp
virtual int startAudioCapture(const AoqAudioCaptureConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqAudioCaptureConfig&` | 音频采集配置，详见 `AoqAudioCaptureConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopaudiocapture"></a>

<a id="8107c7dacfc6"></a>

<a id="5316db42022d"></a>

#### stopAudioCapture

关闭音频采集设备。

<a id="code-block-7"></a>

```cpp
virtual int stopAudioCapture();
```

返回值：0 表示成功；非 0 表示失败。

<a id="muteaudiocapture"></a>

<a id="176280af0629"></a>

<a id="a294c65932da"></a>

#### muteAudioCapture

静音或取消静音音频采集。

<a id="code-block-8"></a>

```cpp
virtual int muteAudioCapture(bool mute);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `mute` | `bool` | `true` 静音；`false` 取消静音 |

返回值：0 表示成功；非 0 表示失败。

<a id="startaudioplayer"></a>

<a id="acc48ac21aee"></a>

<a id="2b12c6427ae8"></a>

#### startAudioPlayer

开始音频渲染，播放远端音频。

<a id="code-block-9"></a>

```cpp
virtual int startAudioPlayer(const AoqAudioPlaybackConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqAudioPlaybackConfig&` | 音频播放配置，详见 `AoqAudioPlaybackConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopaudioplayer"></a>

<a id="00296dd2ac79"></a>

<a id="7411f06c2d53"></a>

#### stopAudioPlayer

停止音频渲染。

<a id="code-block-10"></a>

```cpp
virtual int stopAudioPlayer();
```

返回值：0 表示成功；非 0 表示失败。

<a id="pauseaudioplayer"></a>

<a id="73d02b06e825"></a>

<a id="3cbf7919a47d"></a>

#### pauseAudioPlayer

暂停音频渲染，支持淡出。

<a id="code-block-11"></a>

```cpp
virtual int pauseAudioPlayer(int fadeMs);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fadeMs` | `int` | 淡出时长，单位毫秒；0 表示立即暂停 |

返回值：0 表示成功；非 0 表示失败。

<a id="resumeaudioplayer"></a>

<a id="460e1581824e"></a>

<a id="a97a33838ddc"></a>

#### resumeAudioPlayer

恢复音频渲染，支持淡入。

<a id="code-block-12"></a>

```cpp
virtual int resumeAudioPlayer(int fadeMs);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fadeMs` | `int` | 淡入时长，单位毫秒；0 表示立即恢复 |

返回值：0 表示成功；非 0 表示失败。

<a id="interruptaudioplayer"></a>

<a id="5d8c464fa7bb"></a>

<a id="e924062403cf"></a>

#### interruptAudioPlayer

打断本轮音频通话，停止当前正在播放的音频内容。

<a id="code-block-13"></a>

```cpp
virtual int interruptAudioPlayer(AoqTrackType trackType, int fadeMs);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 音轨类型，详见 `AoqTrackType` |
| `fadeMs` | `int` | 淡出时长，单位毫秒；0 表示立即打断 |

返回值：0 表示成功；非 0 表示失败。

<a id="enablelocalaudiovolumeindication"></a>

<a id="187805d6d450"></a>

<a id="020bb922e703"></a>

#### enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示。开启后按 `config.interval` 周期触发 `onLocalAudioVolumeIndication` 回调；`config.interval <= 0` 时关闭回调。需在 `startAudioCapture` 之后调用才有音量数据。

<a id="code-block-14"></a>

```cpp
virtual int enableLocalAudioVolumeIndication(const AoqAudioVolumeIndicationConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqAudioVolumeIndicationConfig&` | 音量提示配置，详见 `AoqAudioVolumeIndicationConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="音频编码配置-2"></a>

<a id="540053d53b1c"></a>

<a id="ef974c1ad8ee-details"></a>

<a id="aoq-api-category-3"></a>

### 音频编码配置

<a id="setaudioencoderconfig"></a>

<a id="c7d19c71b298"></a>

<a id="a81284af9f27"></a>

#### setAudioEncoderConfig

设置音频编码参数。

<a id="code-block-15"></a>

```cpp
virtual int setAudioEncoderConfig(const AoqAudioCodecConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqAudioCodecConfig&` | 音频编解码配置，详见 `AoqAudioCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="setaudiodecoderconfig"></a>

<a id="ffa75942faba"></a>

<a id="787dc3f51ed0"></a>

#### setAudioDecoderConfig

设置音频解码参数。

<a id="code-block-16"></a>

```cpp
virtual int setAudioDecoderConfig(const AoqAudioCodecConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqAudioCodecConfig&` | 音频编解码配置，详见 `AoqAudioCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="视频设备管理-2"></a>

<a id="bc606baf0498"></a>

<a id="49303f7eebef-details"></a>

<a id="aoq-api-category-4"></a>

### 视频设备管理

<a id="startvideocapture"></a>

<a id="b7e234be86aa"></a>

<a id="0388d5c6cea4"></a>

#### startVideoCapture

打开视频采集设备（摄像头）。配置 `isExternal=true` 时不打开摄像头，由 `pushExternalVideoCapturedFrame` 喂帧。

<a id="code-block-17"></a>

```cpp
virtual int startVideoCapture(const AoqVideoCaptureConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqVideoCaptureConfig&` | 视频采集配置，详见 `AoqVideoCaptureConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopvideocapture"></a>

<a id="d91bb8af2b54"></a>

<a id="793310d05029"></a>

#### stopVideoCapture

关闭视频采集设备。

<a id="code-block-18"></a>

```cpp
virtual int stopVideoCapture();
```

返回值：0 表示成功；非 0 表示失败。

<a id="setlocalview"></a>

<a id="ce5db9367a45"></a>

<a id="00c6effda84e"></a>

#### setLocalView

设置或移除本地视频渲染窗口。`canvas.view == nullptr` 表示解绑。

<a id="code-block-19"></a>

```cpp
virtual int setLocalView(AoqTrackType trackType, const AoqVideoCanvas& canvas);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道，传 `AoqTrackTypeVideo` |
| `canvas` | `const AoqVideoCanvas&` | 渲染画布，详见 `AoqVideoCanvas`；`view` 为 `nullptr` 表示解绑 |

返回值：0 表示成功；非 0 表示失败。

<a id="setremoteview"></a>

<a id="62689220c0ea"></a>

<a id="4a387150ed2e"></a>

#### setRemoteView

设置或移除远端视频渲染窗口。`canvas.view == nullptr` 表示解绑。

<a id="code-block-20"></a>

```cpp
virtual int setRemoteView(AoqTrackType trackType, const AoqVideoCanvas& canvas);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道，传 `AoqTrackTypeVideo` |
| `canvas` | `const AoqVideoCanvas&` | 渲染画布，详见 `AoqVideoCanvas`；`view` 为 `nullptr` 表示解绑 |

返回值：0 表示成功；非 0 表示失败。

<a id="视频编码与外部输入-2"></a>

<a id="a6e991adc167"></a>

<a id="5e7b6d28c285-details"></a>

<a id="aoq-api-category-5"></a>

### 视频编码与外部输入

<a id="setvideoencoderconfig"></a>

<a id="fd52b01e0b1e"></a>

<a id="726cc854d49e"></a>

#### setVideoEncoderConfig

设置视频编码参数，按 `config.trackType` 路由。

<a id="code-block-21"></a>

```cpp
virtual int setVideoEncoderConfig(const AoqVideoCodecConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqVideoCodecConfig&` | 视频编解码配置，详见 `AoqVideoCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="setvideodecoderconfig"></a>

<a id="6c6886628486"></a>

<a id="dfcac35c8230"></a>

#### setVideoDecoderConfig

设置视频解码参数（订阅侧 codec 提议，需在 `connect` 之前调用），按 `config.trackType` 路由。

<a id="code-block-22"></a>

```cpp
virtual int setVideoDecoderConfig(const AoqVideoCodecConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `config` | `const AoqVideoCodecConfig&` | 视频编解码配置，详见 `AoqVideoCodecConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="pushexternalvideocapturedframe"></a>

<a id="c5e12571d7a5"></a>

<a id="33485b14ef1c"></a>

#### pushExternalVideoCapturedFrame

推送外部视频帧。需先调用 `startVideoCapture` 且配置 `isExternal=true`。未启动外部视频采集时返回 `AoqECVideoExternalCaptureNotEnabled`（211）；帧格式不支持时返回 `AoqECParamInvalid`。

<a id="code-block-23"></a>

```cpp
virtual int pushExternalVideoCapturedFrame(AoqTrackType trackType, const AoqVideoFrame& frame);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 路由目标，传 `AoqTrackTypeVideo`<br><br>；也支持 AoqTrackTypeScreen |
| `frame` | `const AoqVideoFrame&` | 外部视频帧数据，详见 `AoqVideoFrame` |

返回值：0 表示成功；`AoqECVideoExternalBufferFull`（210）表示缓冲区满；`AoqECVideoExternalCaptureNotEnabled`（211）表示未启用外部视频采集；`AoqECParamInvalid` 表示帧格式不支持；其他非 0 值表示其他错误。

<a id="pushexternalvideoencodedframe"></a>

<a id="63e22526b933"></a>

<a id="e850d42c0e0d"></a>

#### pushExternalVideoEncodedFrame

推送外部已编码视频帧，bypass 编码器直推。需先调用 `setVideoEncoderConfig` 且配置 `isExternal=true`，当前仅支持 JPEG。

<a id="code-block-24"></a>

```cpp
virtual int pushExternalVideoEncodedFrame(AoqTrackType trackType, const AoqVideoEncodedFrame& frame);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 路由目标，传 `AoqTrackTypeVideo`<br><br>；也支持 AoqTrackTypeScreen |
| `frame` | `const AoqVideoEncodedFrame&` | 外部已编码帧数据，详见 `AoqVideoEncodedFrame` |

返回值：0 表示成功；非 0 表示失败。

<a id="屏幕采集-2"></a>

<a id="aoq-api-category-6"></a>

### 屏幕采集

<a id="code-block-25"></a>

```cpp
virtual int startScreenCapture(const AoqScreenCaptureConfig& config);
virtual int stopScreenCapture();
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

返回值：0 表示成功；非 0 表示失败。 接口同步返回，不提供 `onScreenCaptureStateChanged` 回调。

先调用 `getScreenSourceList` 获取屏幕或窗口源，再将选定的 `sourceId` 和 `sourceType` 传入采集配置。

外部原始帧：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`。

<a id="getscreensourcelist"></a>

#### getScreenSourceList

<a id="code-block-26"></a>

```cpp
virtual AoqScreenSourceList getScreenSourceList();
```

返回屏幕源列表。使用后必须调用 `AoqScreenSourceList::screenSourceListFree(list)` 释放列表内存。

<a id="媒体流发送控制-2"></a>

<a id="4d9280b343ae"></a>

<a id="74db1f031e94-details"></a>

<a id="aoq-api-category-7"></a>

### 媒体流发送控制

<a id="enablesendmediastream"></a>

<a id="1e9ad91241c3"></a>

<a id="8cd0cfefb656"></a>

#### enableSendMediaStream

控制本地媒体流的发送开关。建议初始化后先关闭发送，待 `onConnectionStatusChange` 回调 `AoqConnectionStatusConnected` 后再开启。

<a id="code-block-27"></a>

```cpp
virtual int enableSendMediaStream(AoqTrackType trackType, bool enable);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 路由目标，支持 `AoqTrackTypeAudio` / `AoqTrackTypeVideo`<br><br>；支持 AoqTrackTypeScreen |
| `enable` | `bool` | `true` 启用发送；`false` 停用发送 |

返回值：0 表示调用已下发（异步执行）；非 0 表示失败。

<a id="音频文件播放-2"></a>

<a id="bb130eeb6412"></a>

<a id="28f63a96752c-details"></a>

<a id="aoq-api-category-8"></a>

### 音频文件播放

<a id="startaudiofile"></a>

<a id="db6dc8b06994"></a>

<a id="b8154b4e2163"></a>

#### startAudioFile

开始推流播放本地音频文件。

<a id="code-block-28"></a>

```cpp
virtual int startAudioFile(const char* fileId, const AoqAudioFileMixConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID，业务层需保证唯一性 |
| `config` | `const AoqAudioFileMixConfig&` | 音频文件混音配置，详见 `AoqAudioFileMixConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="stopaudiofile"></a>

<a id="f4b204b0e33b"></a>

<a id="cb0fc3c90ec5"></a>

#### stopAudioFile

停止音频文件播放。

<a id="code-block-29"></a>

```cpp
virtual int stopAudioFile(const char* fileId);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="pauseaudiofile"></a>

<a id="71cde3380705"></a>

<a id="22a7c021444c"></a>

#### pauseAudioFile

暂停音频文件播放。

<a id="code-block-30"></a>

```cpp
virtual int pauseAudioFile(const char* fileId);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="resumeaudiofile"></a>

<a id="1ad51ce39766"></a>

<a id="7fb6fb8652a7"></a>

#### resumeAudioFile

恢复音频文件播放。

<a id="code-block-31"></a>

```cpp
virtual int resumeAudioFile(const char* fileId);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="getaudiofileduration"></a>

<a id="1836ec67bb9e"></a>

<a id="c9f5b906758a"></a>

#### getAudioFileDuration

获取音频文件总时长。

<a id="code-block-32"></a>

```cpp
virtual int64_t getAudioFileDuration(const char* fileId);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |

返回值：>=0 表示音频文件时长，单位毫秒；<0 表示失败（`-AoqErrorCode`）。

<a id="getaudiofilecurrentposition"></a>

<a id="eb233777123b"></a>

<a id="55d157a740ab"></a>

#### getAudioFileCurrentPosition

获取音频文件当前播放位置。

<a id="code-block-33"></a>

```cpp
virtual int64_t getAudioFileCurrentPosition(const char* fileId);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |

返回值：>=0 表示当前播放位置，单位毫秒；<0 表示失败（`-AoqErrorCode`）。

<a id="setaudiofilepositionmillis"></a>

<a id="9bfe582f6e81"></a>

<a id="b3b35917cf95"></a>

#### setAudioFilePositionMillis

设置音频文件播放位置（seek）。

<a id="code-block-34"></a>

```cpp
virtual int setAudioFilePositionMillis(const char* fileId, int64_t positionMillis);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |
| `positionMillis` | `int64_t` | 播放位置，单位毫秒 |

返回值：0 表示成功；非 0 表示失败。

<a id="setaudiofilevolume"></a>

<a id="4f4429088a6d"></a>

<a id="2e131819b227"></a>

#### setAudioFileVolume

设置音频文件音量。

<a id="code-block-35"></a>

```cpp
virtual int setAudioFileVolume(const char* fileId, AoqAudioStreamDirection type, int volume);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |
| `type` | `AoqAudioStreamDirection` | 音频流方向，详见 `AoqAudioStreamDirection` |
| `volume` | `int` | 音量值，范围 \[0, 100\] |

返回值：0 表示成功；非 0 表示失败。

<a id="getaudiofilevolume"></a>

<a id="457f2ef7cb79"></a>

<a id="3daa8596c5d2"></a>

#### getAudioFileVolume

获取音频文件当前音量。

<a id="code-block-36"></a>

```cpp
virtual int getAudioFileVolume(const char* fileId, AoqAudioStreamDirection type);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 音频文件 ID |
| `type` | `AoqAudioStreamDirection` | 音频流方向，详见 `AoqAudioStreamDirection` |

返回值：\[0, 100\] 表示音量值；<0 表示失败（`-AoqErrorCode`）。

<a id="外部音频流-2"></a>

<a id="da1eee3d880c"></a>

<a id="d6b4c13dff30-details"></a>

<a id="aoq-api-category-9"></a>

### 外部音频流

<a id="addaudioexternalstream"></a>

<a id="2fffa94caffa"></a>

<a id="2d7a43b89583"></a>

#### addAudioExternalStream

新增一条外部音频流。

<a id="code-block-37"></a>

```cpp
virtual int addAudioExternalStream(const char* streamId, const AoqAudioExternalStreamConfig& config);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `const char*` | 外部音频流 ID，业务层需保证唯一性 |
| `config` | `const AoqAudioExternalStreamConfig&` | 外部音频流配置，详见 `AoqAudioExternalStreamConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="pushaudioexternalstreamdata"></a>

<a id="dcf6e57c99bc"></a>

<a id="47a918aa81a7"></a>

#### pushAudioExternalStreamData

输入外部音频 PCM 数据。返回 `AoqECAudioExternalBufferFull`（110）时表示 SDK 缓存已满，建议等待约 20ms 后重新送当前数据帧。

<a id="code-block-38"></a>

```cpp
virtual int pushAudioExternalStreamData(const char* streamId, AoqAudioFrameData& data);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `const char*` | 外部音频流 ID |
| `data` | `AoqAudioFrameData&` | 外部音频裸数据，详见 `AoqAudioFrameData` |

返回值：0 表示成功；非 0 表示失败。

> **说明**
>
> 最佳实践：实时采集场景一次 Push 10ms 数据长度，有数据即 Push；数据来源为文件时一次 Push 40ms 数据长度、间隔 30ms 给一次，并处理 `AoqECAudioExternalBufferFull` 返回。

<a id="setaudioexternalstreamvolume"></a>

<a id="ac9d2fc4b818"></a>

<a id="e5d6c04bf335"></a>

#### setAudioExternalStreamVolume

设置外部音频流音量。

<a id="code-block-39"></a>

```cpp
virtual int setAudioExternalStreamVolume(const char* streamId, AoqAudioStreamDirection type, int vol);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `const char*` | 外部音频流 ID |
| `type` | `AoqAudioStreamDirection` | 外部音频流类型，详见 `AoqAudioStreamDirection` |
| `vol` | `int` | 音量值，范围 \[0, 100\] |

返回值：0 表示成功；非 0 表示失败。

<a id="getaudioexternalstreamvolume"></a>

<a id="1affd15125d3"></a>

<a id="43c5949e586c"></a>

#### getAudioExternalStreamVolume

获取外部音频流音量。

<a id="code-block-40"></a>

```cpp
virtual int getAudioExternalStreamVolume(const char* streamId, AoqAudioStreamDirection type);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `const char*` | 外部音频流 ID |
| `type` | `AoqAudioStreamDirection` | 外部音频流类型，详见 `AoqAudioStreamDirection` |

返回值：\[0, 100\] 表示音量值；<0 表示失败（`-AoqErrorCode`）。

<a id="clearaudioexternalstreambuffer"></a>

<a id="59bec8f937fb"></a>

<a id="77feb095dc0c"></a>

#### clearAudioExternalStreamBuffer

清空外部音频流缓存。

<a id="code-block-41"></a>

```cpp
virtual void clearAudioExternalStreamBuffer(const char* streamId, int fadeoutMs);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `const char*` | 外部音频流 ID |
| `fadeoutMs` | `int` | 淡出时长；-1 使用 SDK 内部默认淡出，0 表示全部清空无淡出，>0 保留指定毫秒淡出 |

返回值：无。

<a id="removeaudioexternalstream"></a>

<a id="538eeb559a3a"></a>

<a id="715e01dbba82"></a>

#### removeAudioExternalStream

移除外部音频流。

<a id="code-block-42"></a>

```cpp
virtual int removeAudioExternalStream(const char* streamId);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `streamId` | `const char*` | 外部音频流 ID |

返回值：0 表示成功；非 0 表示失败。

<a id="实时消息-2"></a>

<a id="6ea743f1801d"></a>

<a id="a66495101cc7-details"></a>

<a id="aoq-api-category-10"></a>

### 实时消息

<a id="senddatamsg"></a>

<a id="c6e02b094bdd"></a>

<a id="87e4773415e4"></a>

#### sendDataMsg

发送实时数据消息。

<a id="code-block-43"></a>

```cpp
virtual int sendDataMsg(const AoqDataMsg& msg);
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `msg` | `const AoqDataMsg&` | 消息内容，详见 `AoqDataMsg` |

返回值：0 表示成功；非 0 表示失败。

<a id="音频帧回调-2"></a>

<a id="99209f0fe884"></a>

<a id="b2a326f23d00-details"></a>

<a id="aoq-api-category-11"></a>

### 音频帧回调

<a id="setaudioframeobserver"></a>

<a id="5ddb8a5eb8b9"></a>

<a id="b37eac68a0dc"></a>

#### setAudioFrameObserver

设置音频帧数据回调监听器，传 `nullptr` 停止回调。设置后需调用 `enableAudioFrameObserver` 开启对应数据源的回调。

<a id="code-block-44"></a>

```cpp
virtual int setAudioFrameObserver(IAudioFrameObserver* observer) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `observer` | `IAudioFrameObserver*` | 音频帧回调监听器，详见 `IAudioFrameObserver`；传 `nullptr` 停止回调 |

返回值：0 表示成功；非 0 表示失败。

<a id="enableaudioframeobserver"></a>

<a id="d563d8d545f8"></a>

<a id="16c9ff8e6616"></a>

#### enableAudioFrameObserver

开启或关闭指定位置的音频帧回调。

<a id="code-block-45"></a>

```cpp
virtual int enableAudioFrameObserver(bool enabled, AoqAudioSource audioSource,
                                     const AoqAudioObserverConfig& config) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | `bool` | 是否允许数据回调 |
| `audioSource` | `AoqAudioSource` | 音频裸数据源类型，详见 `AoqAudioSource` |
| `config` | `const AoqAudioObserverConfig&` | 回调参数设置，详见 `AoqAudioObserverConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="视频帧回调-2"></a>

<a id="0cc5cadac0ac"></a>

<a id="7d6304a9d294-details"></a>

<a id="aoq-api-category-12"></a>

### 视频帧回调

<a id="setvideoframeobserver"></a>

<a id="f788f78cabe3"></a>

<a id="df69654262e0"></a>

#### setVideoFrameObserver

设置视频帧数据回调监听器，传 `nullptr` 停止回调。设置后需调用 `enableVideoFrameObserver` 开启对应数据源的回调。

<a id="code-block-46"></a>

```cpp
virtual int setVideoFrameObserver(IVideoFrameObserver* observer) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `observer` | `IVideoFrameObserver*` | 视频帧回调监听器，详见 `IVideoFrameObserver`；传 `nullptr` 停止回调 |

返回值：0 表示成功；非 0 表示失败。

<a id="enablevideoframeobserver"></a>

<a id="35b8303dda36"></a>

<a id="9183f900caf6"></a>

#### enableVideoFrameObserver

开启或关闭指定位置的视频帧回调。

<a id="code-block-47"></a>

```cpp
virtual int enableVideoFrameObserver(bool enabled, AoqVideoSource videoSource,
                                     const AoqVideoObserverConfig& config) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `enabled` | `bool` | 是否启用某位置数据回调 |
| `videoSource` | `AoqVideoSource` | 视频帧回调数据源（管线位置），详见 `AoqVideoSource` |
| `config` | `const AoqVideoObserverConfig&` | 回调参数设置，详见 `AoqVideoObserverConfig` |

返回值：0 表示成功；非 0 表示失败。

<a id="aoqengineeventlistener-2"></a>

<a id="9db3023ec502"></a>

<a id="f572dd70014e"></a>

<a id="aoq-api-category-13"></a>

<a id="e2e55718db33"></a>

<a id="dc2ae020492f"></a>

### AoqEngineEventListener

`AoqEngineEventListener` 是 SDK 所有异步事件通知的统一出口，为抽象类，由调用方继承实现并在 `createEngine` 时传入。所有回调可能在内部线程触发，实现者需自行处理线程安全。连接状态流转：`Disconnected → Connecting → Connected/Failed → Disconnected`。

<a id="onerror"></a>

<a id="b47b050fae92"></a>

<a id="bfdfb43d4665"></a>

#### onError

引擎错误回调。

<a id="code-block-48"></a>

```cpp
virtual void onError(int code, const char* message) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `int` | 错误码，详见 `AoqErrorCode` |
| `message` | `const char*` | 错误描述 |

<a id="onwarning"></a>

<a id="f43f0c38a097"></a>

<a id="25597277142a"></a>

#### onWarning

引擎警告回调。

<a id="code-block-49"></a>

```cpp
virtual void onWarning(int code, const char* message) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `int` | 警告码，详见 `AoqWarningCode` |
| `message` | `const char*` | 警告描述 |

<a id="onconnectionstatuschange"></a>

<a id="8e43a1f61e4f"></a>

<a id="87337ade8d8c"></a>

#### onConnectionStatusChange

引擎连接状态变化回调。

<a id="code-block-50"></a>

```cpp
virtual void onConnectionStatusChange(AoqConnectionStatus status) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `status` | `AoqConnectionStatus` | 连接状态，详见 `AoqConnectionStatus` |

<a id="onstats"></a>

<a id="b2159408800f"></a>

<a id="9d87054eab12"></a>

#### onStats

引擎统计信息回调。

<a id="code-block-51"></a>

```cpp
virtual void onStats(const AoqStats& stats) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `stats` | `const AoqStats&` | 统计数据，详见 `AoqStats` |

<a id="onaudiodevicestatechanged"></a>

<a id="9b541fae6d94"></a>

<a id="3f7a0b43501a"></a>

#### onAudioDeviceStateChanged

音频设备采集 / 播放操作状态变化回调。

<a id="code-block-52"></a>

```cpp
virtual void onAudioDeviceStateChanged(const AoqAudioDeviceState& state) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `const AoqAudioDeviceState&` | 音频设备状态，详见 `AoqAudioDeviceState` |

<a id="onaudiodeviceroutechanged"></a>

<a id="061e76f8249b"></a>

<a id="0960a0ed1b9e"></a>

#### onAudioDeviceRouteChanged

音频输出路由变化回调。

<a id="code-block-53"></a>

```cpp
virtual void onAudioDeviceRouteChanged(int routeType) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `routeType` | `int` | 路由类型，取值详见 `AoqAudioDeviceRouteType` |

<a id="onaudiofilestate"></a>

<a id="836fc0cd3d73"></a>

<a id="c8a0b9aba273"></a>

#### onAudioFileState

音频文件播放状态回调。

<a id="code-block-54"></a>

```cpp
virtual void onAudioFileState(const AoqAudioFileState& state) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `const AoqAudioFileState&` | 文件播放状态，详见 `AoqAudioFileState` |

<a id="onlocalaudiovolumeindication"></a>

<a id="6044662dfa69"></a>

<a id="04a9135abb54"></a>

#### onLocalAudioVolumeIndication

本地采集音量提示回调，需调用 `enableLocalAudioVolumeIndication` 开启。

<a id="code-block-55"></a>

```cpp
virtual void onLocalAudioVolumeIndication(const AoqAudioVolume& volume) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `volume` | `const AoqAudioVolume&` | 本地音量信息，详见 `AoqAudioVolume` |

<a id="onvideodevicestatechanged"></a>

<a id="1ba58262fcb4"></a>

<a id="5057be7b856a"></a>

#### onVideoDeviceStateChanged

视频设备采集操作状态变化回调。

<a id="code-block-56"></a>

```cpp
virtual void onVideoDeviceStateChanged(const AoqVideoDeviceState& state) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `const AoqVideoDeviceState&` | 视频设备状态，详见 `AoqVideoDeviceState` |

<a id="ondatamsg"></a>

<a id="767ecb05ce51"></a>

<a id="c81880540086"></a>

#### onDataMsg

收到实时数据消息回调。

<a id="code-block-57"></a>

```cpp
virtual void onDataMsg(const AoqDataMsg& msg) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `msg` | `const AoqDataMsg&` | 数据消息，详见 `AoqDataMsg` |

<a id="iaudioframeobserver-2"></a>

<a id="46a12e565a4c"></a>

<a id="ef12cdcf3425"></a>

<a id="aoq-api-category-14"></a>

### IAudioFrameObserver

音频帧数据回调接口，由调用方继承实现。请不要在回调中做任何耗时操作，否则可能导致声音异常。

<a id="oncapturedaudioframe"></a>

<a id="de7135dfcf6b"></a>

<a id="19f85934cbdb"></a>

#### onCapturedAudioFrame

采集裸数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourceCaptured` 开启，支持设置采样率、声道数，支持读写模式。

<a id="code-block-58"></a>

```cpp
virtual void onCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `const AoqAudioFrameData&` | 采集音频裸数据，详见 `AoqAudioFrameData` |

<a id="onprocesscapturedaudioframe"></a>

<a id="f0172aaf007f"></a>

<a id="3692eaefd00b"></a>

#### onProcessCapturedAudioFrame

3A 后数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourceProcessCaptured` 开启，支持设置采样率、声道数，支持读写模式。

<a id="code-block-59"></a>

```cpp
virtual void onProcessCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `const AoqAudioFrameData&` | 3A 处理后音频裸数据，详见 `AoqAudioFrameData` |

<a id="onpublishaudioframe"></a>

<a id="b33325be88a0"></a>

<a id="33651e95c703"></a>

#### onPublishAudioFrame

推流数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourcePublish` 开启，支持设置采样率、声道数，仅支持只读模式。

<a id="code-block-60"></a>

```cpp
virtual void onPublishAudioFrame(AoqTrackType trackType, const AoqAudioFrameData& data) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 音轨类型，详见 `AoqTrackType` |
| `data` | `const AoqAudioFrameData&` | 推流音频裸数据，详见 `AoqAudioFrameData` |

<a id="onplaybackaudioframe"></a>

<a id="36be7161c78e"></a>

<a id="200bed2e2604"></a>

#### onPlaybackAudioFrame

播放数据回调。通过 `enableAudioFrameObserver` 设置 `audioSource = AoqAudioSourcePlayback` 开启，支持设置采样率、声道数，支持读写模式。

<a id="code-block-61"></a>

```cpp
virtual void onPlaybackAudioFrame(const AoqAudioFrameData& data) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `const AoqAudioFrameData&` | 播放音频裸数据，详见 `AoqAudioFrameData` |

<a id="ivideoframeobserver-2"></a>

<a id="c105b7a4fbc2"></a>

<a id="3d86238a79c6"></a>

<a id="aoq-api-category-15"></a>

### IVideoFrameObserver

视频帧数据回调接口，由调用方继承实现。请不要在回调中做任何耗时操作，否则可能导致画面卡顿。回调返回 `true` 表示数据已修改、需写回 SDK（写回仅对 I420 生效）；返回 `false` 表示只读。`frame` 中的数据仅在回调期间有效，异步使用需自行拷贝。

<a id="oncapturedvideoframe"></a>

<a id="4dd9aa6fa6aa"></a>

<a id="251d613b17fe"></a>

#### onCapturedVideoFrame

本地采集后裸数据回调（前处理前）。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourceCaptured` 开启。

<a id="code-block-62"></a>

```cpp
virtual bool onCapturedVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `frame` | `AoqVideoFrame&` | 采集视频帧数据，详见 `AoqVideoFrame` |
| trackType | AoqTrackType | 视频轨道类型，支持 Video / Screen。 |

返回值：`true` 数据已修改、需写回 SDK；`false` 只读。

<a id="onpreencodevideoframe"></a>

<a id="0da777ba7ac9"></a>

<a id="cf345b014c22"></a>

#### onPreEncodeVideoFrame

本地编码前裸数据回调（前处理后）。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourcePreEncode` 开启。

<a id="code-block-63"></a>

```cpp
virtual bool onPreEncodeVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道类型，详见 `AoqTrackType` |
| `frame` | `AoqVideoFrame&` | 编码前视频帧数据，详见 `AoqVideoFrame` |

返回值：`true` 数据已修改、需写回 SDK；`false` 只读。

<a id="onremotevideoframe"></a>

<a id="7e0a16e6d08a"></a>

<a id="9138d0ffdb33"></a>

#### onRemoteVideoFrame

远端解码后、渲染前裸数据回调。通过 `enableVideoFrameObserver` 设置 `videoSource = AoqVideoSourceRemote` 开启。

<a id="code-block-64"></a>

```cpp
virtual bool onRemoteVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

参数

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 视频轨道类型，详见 `AoqTrackType` |
| `frame` | `AoqVideoFrame&` | 远端视频帧数据，详见 `AoqVideoFrame` |

返回值：`true` 数据已修改、需写回 SDK；`false` 只读。

<a id="数据类型与枚举"></a>

<a id="f743b74c8409"></a>

<a id="fcf9cebd495e"></a>

## 数据类型与枚举

<a id="通用类型"></a>

<a id="24f93b8633aa"></a>

<a id="c30de1d03af2"></a>

### 通用类型

<a id="aoqcreateconfig"></a>

<a id="49ea2d49b2b8"></a>

<a id="eed0f444e642"></a>

#### AoqCreateConfig

引擎创建配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `workDir` | `const char*` | `nullptr` | SDK 工作目录 |
| `enableDumpAudio` | `bool` | `false` | 是否开启音频数据保存（调试用） |
| `extras` | `const char*` | `nullptr` | 扩展参数（JSON 字符串） |
| maxEncodedVideoFrameBytes | int | 190 × 1024 | 编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。0 表示关闭限制。 |
| enableDropOversizedVideoFrame | bool | false | 仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。 |

<a id="aoqconnectconfig"></a>

<a id="f2c3edc0e06b"></a>

<a id="3e7902dce8b5"></a>

#### AoqConnectConfig

连接 Relay 服务器配置。`relayEndpoints` / `publishTracks` / `subscribeTracks` 为 C 风格数组 + 长度，数组内存由调用方持有，仅需在 `connect` 调用期间保持有效。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `token` | `const char*` | 连接鉴权 Token |
| `sid` | `const char*` | 会话 ID |
| `certFingerprint` | `const char*` | 服务器证书指纹 |
| `workspaceIdHash` | `const char*` | 工作空间哈希 ID |
| `relayEndpoints` | `const AoqRelayEndpoint*` | Relay 接入点数组 |
| `relayEndpointsCount` | `size_t` | Relay 接入点数量 |
| `publishTracks` | `const AoqTrackParam*` | 本端推流 track 属性数组 |
| `publishTracksCount` | `size_t` | 推流 track 数量 |
| `subscribeTracks` | `const AoqTrackParam*` | 本端拉流 track 属性数组 |
| `subscribeTracksCount` | `size_t` | 拉流 track 数量 |

<a id="aoqrelayendpoint"></a>

<a id="bd79250d00c4"></a>

<a id="b58a1473e07b"></a>

#### AoqRelayEndpoint

Relay 接入点。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `route_index` | `int` | `-1` | 路径序号 |
| `endpoint` | `const char*` | `nullptr` | 服务端地址（域名或 IP） |
| `port` | `int` | `0` | 服务端端口 |
| tcp\_port | int | 0 | TCP 降级端口；0 表示使用 SDK 默认端口 443。 |

<a id="aoqtrackparam"></a>

<a id="8c6243e03b50"></a>

<a id="570fc294b704"></a>

#### AoqTrackParam

track 属性。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trackType` | `AoqTrackType` | `Audio` | track 类型 |
| `trackMode` | `AoqTrackMode` | `Segment` | 流式与非流式模式，仅对音频下行生效 |

<a id="aoqdatamsg"></a>

<a id="25c6cc119f2e"></a>

<a id="e0d8895ec85c"></a>

#### AoqDataMsg

消息数据结构。回调中使用时仅保证回调期间有效，如需异步使用请自行拷贝。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | `const uint8_t*` | 消息内容，指向调用方持有的内存 |
| `dataSize` | `size_t` | 字节数 |

<a id="统计信息类型"></a>

<a id="1d9fe4ca4699"></a>

<a id="6c1131f5ff28"></a>

### 统计信息类型

<a id="aoqstats"></a>

<a id="5ab56084fd18"></a>

<a id="86a11bf11767"></a>

#### AoqStats

引擎统计信息。各统计数组以指针 + 数量形式提供。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `audioPublishStats` / `audioPublishStatsCount` | `const AoqAudioPublishStats*` / `unsigned int` | 音频推流统计数组及数量 |
| `videoPublishStats` / `videoPublishStatsCount` | `const AoqVideoPublishStats*` / `unsigned int` | 视频推流统计数组及数量 |
| `dataMsgPublishStats` / `dataMsgPublishStatsCount` | `const AoqDataMsgPublishStats*` / `unsigned int` | 数据消息推流统计数组及数量 |
| `audioSubscribeStats` / `audioSubscribeStatsCount` | `const AoqAudioSubscribeStats*` / `unsigned int` | 音频拉流统计数组及数量 |
| `videoSubscribeStats` / `videoSubscribeStatsCount` | `const AoqVideoSubscribeStats*` / `unsigned int` | 视频拉流统计数组及数量 |
| `dataMsgSubscribeStats` / `dataMsgSubscribeStatsCount` | `const AoqDataMsgSubscribeStats*` / `unsigned int` | 数据消息拉流统计数组及数量 |
| `networkStats` | `const AoqNetworkStats*` | 网络统计信息 |

<a id="aoqnetworkstats"></a>

<a id="c38f1ffc6068"></a>

<a id="d91a1777cf69"></a>

#### AoqNetworkStats

网络统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sendBitrate` | `unsigned int` | 发送码率（bps） |
| `sendBytes` | `uint64_t` | 累计发送字节数 |
| `recvBitrate` | `unsigned int` | 接收码率（bps） |
| `recvBytes` | `uint64_t` | 累计接收字节数 |
| `loss` | `unsigned int` | 丢包率（0-100） |
| `rtt` | `unsigned int` | 往返延迟（ms） |

<a id="aoqaudiopublishstats"></a>

<a id="dc73db16f6e0"></a>

<a id="dd142fc5bad8"></a>

#### AoqAudioPublishStats

音频推流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `unsigned int` | 码率（bps） |
| `bytes` | `uint64_t` | 累计字节数 |
| `encodeVolume` | `unsigned int` | 推流编码音量 |

<a id="aoqvideopublishstats"></a>

<a id="72688dfc8af0"></a>

<a id="41ad9a0276e8"></a>

#### AoqVideoPublishStats

视频推流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `unsigned int` | 码率（bps） |
| `bytes` | `uint64_t` | 累计字节数 |
| `encodeFps` | `unsigned int` | 编码帧率 |

<a id="aoqdatamsgpublishstats"></a>

<a id="b51ed201e28d"></a>

<a id="2e52c6768d0f"></a>

#### AoqDataMsgPublishStats

数据消息推流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `unsigned int` | 码率（bps） |
| `bytes` | `uint64_t` | 累计字节数 |

<a id="aoqaudiosubscribestats"></a>

<a id="65495a5760c5"></a>

<a id="cf1e1224e73d"></a>

#### AoqAudioSubscribeStats

音频拉流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `unsigned int` | 码率（bps） |
| `bytes` | `uint64_t` | 累计字节数 |
| `playVolume` | `unsigned int` | 播放音量 |

<a id="aoqvideosubscribestats"></a>

<a id="5f98abe085e9"></a>

<a id="0440768ab1f7"></a>

#### AoqVideoSubscribeStats

视频拉流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `unsigned int` | 码率（bps） |
| `bytes` | `uint64_t` | 累计字节数 |
| `decodeFps` | `unsigned int` | 解码帧率 |
| `renderFps` | `unsigned int` | 渲染帧率 |

<a id="aoqdatamsgsubscribestats"></a>

<a id="68f89b6f767c"></a>

<a id="81380624effe"></a>

#### AoqDataMsgSubscribeStats

数据消息拉流统计信息。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `trackType` | `AoqTrackType` | 轨道类型 |
| `bitrate` | `unsigned int` | 码率（bps） |
| `bytes` | `uint64_t` | 累计字节数 |

<a id="枚举类型"></a>

<a id="5f34a9466e68"></a>

<a id="e6365c67dabb"></a>

### 枚举类型

<a id="aoqerrorcode"></a>

<a id="ea5356c2eff8"></a>

<a id="a22cd1d8b665"></a>

#### AoqErrorCode

错误码枚举。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqECOK` | 0 | 成功 |
| `AoqECParamInvalid` | 1 | 参数非法 |
| `AoqECStateInvalid` | 2 | 状态非法 |
| `AoqECUnSupport` | 3 | 接口被调但当前平台 / 模式未实现 |
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
| `AoqECAudioDeviceEarpieceRequiresVoipMode` | 128 | 听筒模式需启用 VoIP |
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
| AoqECScreen | 300 | 屏幕共享通用错误 |
| AoqECScreenAuthFailed | 310 | 屏幕共享授权失败 |
| AoqECScreenStartFailed | 311 | 屏幕共享启动失败 |

<a id="aoqwarningcode"></a>

<a id="465fe23041c6"></a>

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

<a id="cc3b7b02223c"></a>

<a id="47f3d99e128f"></a>

#### AoqTrackType

轨道类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqTrackTypeAudio` | 0 | 音频轨道 |
| `AoqTrackTypeVideo` | 1 | 视频轨道 |
| `AoqTrackTypeData` | 2 | 数据消息轨道 |
| AoqTrackTypeScreen | 3 | 屏幕共享轨道，仅支持上行。 |

<a id="aoqencodertype"></a>

<a id="41f5db81cf0a"></a>

<a id="8c23a1705af2"></a>

#### AoqEncoderType

编码器类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqEncoderTypeUnknown` | 0 | 未知格式 |
| `AoqEncoderTypeAudioPCM` | 1 | 音频 PCM |
| `AoqEncoderTypeAudioOpus` | 2 | 音频 Opus（插件化，需联系 SDK 提供内置或动态下载到 APP 下） |
| `AoqEncoderTypeVideoH264` | 3 | 视频 H.264 |
| `AoqEncoderTypeVideoJpeg` | 4 | 视频 JPEG |
| `AoqEncoderTypeDataText` | 5 | 数据文本 |

<a id="aoqtrackmode"></a>

<a id="a1a04dadd62e"></a>

<a id="ebbb9cd49726"></a>

#### AoqTrackMode

流式与非流式模式，仅对音频下行生效。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqTrackModeSegment` | 0 | 分段：数据按语义片段（如一句话）打包送达 |
| `AoqTrackModeStream` | 1 | 流式：数据持续、连续地送达 |

<a id="aoqconnectionstatus"></a>

<a id="1e3033a25040"></a>

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

<a id="763d6c7bab61"></a>

<a id="e78befcafa59"></a>

### 音频类型

<a id="aoqaudiocaptureconfig"></a>

<a id="291cd84d3676"></a>

<a id="55191a7475de"></a>

#### AoqAudioCaptureConfig

音频采集配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `isExternal` | `bool` | `false` | 是否外部采集 |
| `channel` | `int` | `1` | 音频采集通道数，支持 1/2 |

<a id="aoqaudioplaybackconfig"></a>

<a id="fd9013b95ce1"></a>

<a id="0b30f197ac02"></a>

#### AoqAudioPlaybackConfig

音频播放配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `isExternal` | `bool` | `false` | 是否外部播放 |
| `channel` | `int` | `1` | 音频播放通道数，支持 1/2 |

<a id="aoqaudiocodecconfig"></a>

<a id="d4076aef1f59"></a>

<a id="87b9f458d857"></a>

#### AoqAudioCodecConfig

音频编解码配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trackType` | `AoqTrackType` | `Audio` | 轨道类型 |
| `codecType` | `AoqEncoderType` | `AudioOpus` | 编码格式 |
| `sampleRate` | `int` | `48000` | 采样率（Hz）。编码支持 Opus 8/16/48K、PCM 8/16/32/48K；解码额外支持 24K，但 24K 仅限 Segment 模式（Stream 模式不支持 24K，非法组合在 connect 时通过 onError 回调 AoqECParamInvalid） |
| `channel` | `int` | `1` | 声道数，支持 1/2 |
| `bitrate` | `int` | `32000` | 比特率（bps） |

<a id="aoqaudiodevicestate"></a>

<a id="b5774fe56a35"></a>

<a id="5fa4025c496a"></a>

#### AoqAudioDeviceState

音频设备状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqAudioDeviceStateCode` | 状态码 |
| `reason` | `int` | 错误码（`AoqErrorCode`） |

<a id="aoqaudiodevicestatecode"></a>

<a id="caf0b89c42b4"></a>

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

<a id="aoqaudiodeviceroutetype"></a>

<a id="2f67c4a300e8"></a>

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

<a id="aoqaudiofilemixconfig"></a>

<a id="218c7b215531"></a>

<a id="856f8de1a37f"></a>

#### AoqAudioFileMixConfig

音频文件推流播放配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `fileName` | `const char*` | `nullptr` | 文件名（含路径），必填 |
| `cycles` | `int` | `-1` | 循环次数，-1 表示无限循环 |
| `startPosMs` | `long` | `0` | 起始播放位置（ms） |
| `publishVolume` | `int` | `100` | 推流音量，范围 \[0, 100\] |
| `playoutVolume` | `int` | `100` | 播放音量，范围 \[0, 100\] |

<a id="aoqaudiofilestate"></a>

<a id="3c59057bb51e"></a>

<a id="3e8c30a8d288"></a>

#### AoqAudioFileState

音频文件状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `fileId` | `const char*` | 文件 ID |
| `stateCode` | `AoqAudioFileStateCode` | 状态码 |
| `errorCode` | `AoqAudioFileErrorCode` | 错误码 |

<a id="aoqaudiofilestatecode"></a>

<a id="c0d1f2f2e88c"></a>

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

<a id="d44756e0ab50"></a>

<a id="b155fc9c7de7"></a>

#### AoqAudioFileErrorCode

音频文件播放错误码。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioFileNoError` | 0 | 没有错误 |
| `AoqAudioFileOpenFailed` | 1 | 打开文件失败 |
| `AoqAudioFileDecodeFailed` | 2 | 解码文件失败 |

<a id="aoqaudioexternalstreamconfig"></a>

<a id="7ebef4dca1c5"></a>

<a id="1674e432627e"></a>

#### AoqAudioExternalStreamConfig

外部音频流配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `trackType` | `AoqTrackType` | `Audio` | 音频轨道类型 |
| `codecType` | `AoqEncoderType` | `AudioPCM` | 音频流格式，支持 PCM |
| `channels` | `int` | `1` | 声道数，受限推流音频 Codec 支持 1/2，超过的声道忽略 |
| `sampleRate` | `int` | `48000` | 采样率（Hz），支持 8/12/16/24/32/44.1/48/64/88.2/96/176.4/192K |
| `playoutVolume` | `int` | `100` | 播放音量，范围 \[0, 100\] |
| `publishVolume` | `int` | `100` | 推流音量，范围 \[0, 100\] |
| `maxBufferDuration` | `int` | `600000` | 最大缓冲时长（ms），取值范围 \[100, ~\]，SDK 缓存时长超过时 Push 会失败 |
| `enable3A` | `bool` | `false` | 输入 PCM 是否做 3A 处理 |

<a id="aoqaudioframedata"></a>

<a id="ff3e4a4fcc4b"></a>

<a id="9c6f3494e07f"></a>

#### AoqAudioFrameData

音频数据。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `dataPtr` | `void*` | 音频数据指针 |
| `numOfSamples` | `int` | 采样点数（单个声道） |
| `bytesPerSample` | `int` | 每个采样点的字节数 |
| `numOfChannels` | `int` | 声道数 |
| `samplesPerSec` | `int` | 每秒采样点数 |
| `pushSequence` | `int` | PCM 输入轮次（用于 `pushAudioExternalStreamData` 消费完通知） |
| `timeStamp` | `int64_t` | 时间戳 |
| `dataSize` | `int` | 数据长度 |
| `autoGenMute` | `bool` | 数据回调有效，`true` 表示 SDK 生成的静音数据 |

<a id="aoqaudiostreamdirection"></a>

<a id="6fdeb6be252e"></a>

<a id="62f229fbb122"></a>

#### AoqAudioStreamDirection

音频流方向。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioStreamPublish` | 0 | 推流音频 |
| `AoqAudioStreamPlayout` | 1 | 播放音频 |

<a id="aoqaudioexternalstreamtoggle"></a>

<a id="e7d816ca968b"></a>

<a id="4f46a3401fc1"></a>

#### AoqAudioExternalStreamToggle

外部音频流控制。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioExternalStreamToggleNormal` | 0 | 恢复正常 |
| `AoqAudioExternalStreamTogglePause` | 1 | 暂停 |

<a id="aoqaudiosource"></a>

<a id="e79b36636a1e"></a>

<a id="cdfc294b6724"></a>

#### AoqAudioSource

音频数据源类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioSourceCaptured` | 0 | 采集的音频数据 |
| `AoqAudioSourceProcessCaptured` | 1 | 3A 后的音频数据 |
| `AoqAudioSourcePublish` | 2 | 推流的音频数据（需 Connect 成功） |
| `AoqAudioSourcePlayback` | 3 | 播放的音频数据 |

<a id="aoqaudioobservermode"></a>

<a id="3d9a94e53de2"></a>

<a id="cf87e52060da"></a>

#### AoqAudioObserverMode

音频帧回调模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqAudioObserverModeReadOnly` | 0 | 只读 |
| `AoqAudioObserverModeReadWrite` | 1 | 读写 |

<a id="aoqaudioobserverconfig"></a>

<a id="a0b31c2f50e7"></a>

<a id="e0fd24cba102"></a>

#### AoqAudioObserverConfig

音频数据回调参数设置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sampleRate` | `int` | `48000` | 回调音频采样率，受限 Source 源，不一致时重采样，支持 8/12/16/24/32/44.1/48/64/88.2/96/176.4/192K |
| `channels` | `int` | `1` | 回调音频声道数，支持 1/2，受限拉流 Codec 参数 |
| `mode` | `AoqAudioObserverMode` | `ReadOnly` | 回调模式 |

<a id="aoqaudiovolumeindicationconfig"></a>

<a id="bda9b9e075f8"></a>

<a id="2b85baf1d900"></a>

#### AoqAudioVolumeIndicationConfig

本地音量提示配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| reportSpeech | bool | false | 是否检测人声。 |
| interval | int | 0 | 回调间隔（毫秒）；小于等于 0 时关闭，大于 0 且小于 10 时按 10 处理。 |
| smooth | int | 3 | 平滑系数，范围 0～10；越大越平滑。 |

<a id="aoqaudiovolume"></a>

<a id="794b0a858de5"></a>

<a id="8aba98a38c7c"></a>

#### AoqAudioVolume

本地音量信息。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isSpeech | bool | false | 是否为人声。 |
| volume | int | 0 | 平滑后的瞬时音量，范围 0～255。 |

<a id="视频类型"></a>

<a id="ae23fe3181cb"></a>

<a id="c354bef7242d"></a>

### 视频类型

<a id="aoqvideocaptureconfig"></a>

<a id="21e083e0fab2"></a>

<a id="cde328a703a7"></a>

#### AoqVideoCaptureConfig

视频采集配置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `width` | `int` | `1280` | 采集宽度（像素）；`isExternal=true` 时无效 |
| `height` | `int` | `720` | 采集高度（像素）；`isExternal=true` 时无效 |
| `fps` | `int` | `15` | 采集帧率；`isExternal=true` 时无效（节奏由送帧决定） |
| `isExternal` | `bool` | `false` | 是否外部采集；`true` 时不打开摄像头，由 `pushExternalVideoCapturedFrame` 喂帧 |

<a id="aoqvideocanvas"></a>

<a id="9b56c7f9aee1"></a>

<a id="0ad24da46a66"></a>

#### AoqVideoCanvas

视频渲染数据结构。`view` 为平台原生视图句柄的不透明指针，Windows 平台填窗口句柄 `HWND`。调用方需保证 `view` 生命周期长于 `setLocalView` / `setRemoteView` 设置期间。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `view` | `void*` | `nullptr` | 显示视图句柄（`HWND`），传 `nullptr` 表示移除渲染绑定 |
| `renderMode` | `AoqRenderMode` | `Auto` | 渲染模式 |

<a id="aoqrendermode"></a>

<a id="590ac38b4a3e"></a>

<a id="21b813017a0e"></a>

#### AoqRenderMode

渲染显示模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqRenderModeAuto` | 0 | 自动模式 |
| `AoqRenderModeStretch` | 1 | 拉伸平铺模式，宽高比不一致时拉伸到目标比例，画面会变形 |
| `AoqRenderModeFill` | 2 | 填充黑边模式，宽高比不一致时上下或左右填充黑边 |
| `AoqRenderModeCrop` | 3 | 裁剪模式，宽高比不一致时裁剪宽或高，画面内容会丢失 |

<a id="aoqvideopixelformat"></a>

<a id="4b58fbc421a1"></a>

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

<a id="aoqvideoframe"></a>

<a id="64db084755d4"></a>

<a id="240e2c8d5b17"></a>

#### AoqVideoFrame

外部视频数据。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `format` | `AoqVideoPixelFormat` | 像素格式 |
| `width` | `int` | 宽度（像素） |
| `height` | `int` | 高度（像素） |
| `dataPtr` | `void*` | 打包格式数据指针（NV12/NV21/BGRA/RGBA） |
| `dataSize` | `int` | 打包数据字节数 |
| `dataY` / `dataU` / `dataV` | `void*` | I420 三平面数据指针 |
| `strideY` / `strideU` / `strideV` | `int` | I420 三平面步长 |
| `timeStamp` | `int64_t` | 时间戳（ms）；0 时 SDK 用本地时钟补 |
| `nativePixelBuffer` | `void*` | 跨平台保留字段，Windows 不使用。 |
| `textureId` | `int` | 跨平台保留字段，Windows 不使用。 |
| `transformMatrix` | `float[16]` | 跨平台保留字段，Windows 不使用。 |

<a id="aoqvideoencodedframe"></a>

<a id="df0f1a1f1e50"></a>

<a id="1238aa9ae51b"></a>

#### AoqVideoEncodedFrame

外部已编码视频帧。调用方自行完成编码，SDK 不做二次编码，直接打包发送。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `codec` | `AoqVideoCodecType` | 编码格式 |
| `data` | `void*` | 编码后数据指针 |
| `dataSize` | `int` | 编码后数据字节数 |
| `width` | `int` | 宽度（像素） |
| `height` | `int` | 高度（像素） |
| `timeStamp` | `int64_t` | 时间戳（ms）；0 时 SDK 用本地时钟补 |

<a id="aoqvideocodectype"></a>

<a id="658e76cfed76"></a>

<a id="38586533f3db"></a>

#### AoqVideoCodecType

外部编码帧 codec 类型。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoCodecTypeJPEG` | 0 | JPEG |

<a id="aoqvideodevicestate"></a>

<a id="8a56790b323f"></a>

<a id="53053117285e"></a>

#### AoqVideoDeviceState

视频设备状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `state` | `AoqVideoDeviceStateCode` | 状态码 |
| `reason` | `int` | 错误码（`AoqErrorCode`） |

<a id="aoqvideodevicestatecode"></a>

<a id="1ebf77f07437"></a>

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
| `AoqVideoDeviceCaptureFail` | 5 | 摄像头启动失败（权限拒绝、设备不可用等） |

<a id="aoqmirrormode"></a>

<a id="269f5c7bc380"></a>

<a id="d21d46b0f130"></a>

#### AoqMirrorMode

镜像模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqMirrorModeDisabled` | 0 | 关闭镜像 |
| `AoqMirrorModeEnabled` | 1 | 开启镜像 |

<a id="aoqorientationmode"></a>

<a id="d353145e203f"></a>

<a id="95529f330ec5"></a>

#### AoqOrientationMode

方向模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqOrientationModeAuto` | 0 | 自动 |
| `AoqOrientationModePortrait` | 1 | 竖屏 |
| `AoqOrientationModeLandscape` | 2 | 横屏 |

<a id="aoqvideocodecconfig"></a>

<a id="09e062a37084"></a>

<a id="4d1a3bbc242f"></a>

#### AoqVideoCodecConfig

视频编解码参数（编解码共用）。用于解码时仅 `trackType` / `codecType` / `width` / `height` / `fps` / `bitrate` 生效（作为订阅提议参与协商），`minBitrate` / `keyframeInterval` / `mirrorMode` / `orientationMode` / `isExternal` 仅编码使用。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `isExternal` | `bool` | `false` | 外部编码模式；`true` 时由客户推送已编码帧，SDK 不做采集和编码 |
| `trackType` | `AoqTrackType` | `Video` | 轨道类型 |
| `codecType` | `AoqEncoderType` | `VideoH264` | 编码格式 |
| `width` | `int` | `540` | 分辨率宽 |
| `height` | `int` | `960` | 分辨率高 |
| `fps` | `int` | `5` | 帧率 |
| `bitrate` | `int` | `500000` | 起始码率（bps） |
| `minBitrate` | `int` | `128000` | 最小码率（bps） |
| `keyframeInterval` | `int` | `2` | 关键帧间隔（秒） |
| `mirrorMode` | `AoqMirrorMode` | `Disabled` | 镜像模式 |
| `orientationMode` | `AoqOrientationMode` | `Auto` | 方向模式 |

<a id="aoqvideosource"></a>

<a id="9a725a031c63"></a>

<a id="418539a8369c"></a>

#### AoqVideoSource

视频帧回调数据源（管线位置）。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoSourceCaptured` | 0 | 采集后的视频数据（前处理前） |
| `AoqVideoSourcePreEncode` | 1 | 编码前的视频数据（前处理后） |
| `AoqVideoSourceRemote` | 2 | 远端解码后、渲染前的视频数据 |

<a id="aoqvideoobservermode"></a>

<a id="7d76ced175ca"></a>

<a id="3e0387c6422c"></a>

#### AoqVideoObserverMode

视频帧回调模式。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| `AoqVideoObserverModeReadOnly` | 0 | 只读 |
| `AoqVideoObserverModeReadWrite` | 1 | 读写 |

<a id="aoqvideoobserveralignment"></a>

<a id="6e50004fc75c"></a>

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

<a id="8cf94d286e7a"></a>

<a id="5872956c3dd0"></a>

#### AoqVideoObserverConfig

视频数据回调参数设置。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `format` | `AoqVideoPixelFormat` | `I420` | 期望回调像素格式 |
| `alignment` | `AoqVideoObserverAlignment` | `Default` | 宽度对齐策略 |
| `mode` | `AoqVideoObserverMode` | `ReadOnly` | 回调模式，仅 I420 支持 ReadWrite |
| `mirrorApplied` | `bool` | `false` | 是否对回调数据应用镜像 |
| trackType | AoqTrackType | AoqTrackTypeVideo | 需要观察的视频轨道；仅支持 Video / Screen。 |

<a id="屏幕采集类型"></a>

### 屏幕采集类型

<a id="aoqscreencapturestatecode"></a>

#### AoqScreenCaptureStateCode

屏幕采集状态枚举。当前 SDK 已定义该类型，但没有对应的状态回调。

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqScreenCaptureNone | 0 | 无 |
| AoqScreenCaptureStarting | 1 | 启动中 |
| AoqScreenCaptureStarted | 2 | 已启动 |
| AoqScreenCaptureStopping | 3 | 停止中 |
| AoqScreenCaptureStopped | 4 | 已停止 |
| AoqScreenCaptureFail | 5 | 失败 |

<a id="aoqscreencapturestate"></a>

#### AoqScreenCaptureState

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| state | AoqScreenCaptureStateCode | 屏幕采集状态码。 |
| reason | int | 错误码，对应 AoqErrorCode；正常为 0。 |

<a id="aoqscreensourcelist"></a>

#### AoqScreenSourceList

| 字段/方法 | 类型 | 说明 |
| --- | --- | --- |
| sourceCount | int | 源数量 |
| sourceList | const AoqScreenSourceInfo\* | 源数组；使用后调用 screenSourceListFree(list) 释放。 |
| screenSourceListFree(list) | static void | 释放列表内存。调用方必须调用，否则会发生内存泄漏。 |

<a id="aoqscreensourceinfo"></a>

#### AoqScreenSourceInfo

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| sourceType | AoqScreenShareSourceType | Desktop | 源类型 |
| sourceId | int64\_t | 0 | 源 ID |
| sourceName | const char\* | nullptr | 源名称 |
| sourceIsSelf | bool | false | 是否为自身进程窗口 |

<a id="aoqscreensharesourcetype"></a>

#### AoqScreenShareSourceType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqScreenShareSourceTypeDesktop | 0 | 整个桌面 |
| AoqScreenShareSourceTypeWindow | 1 | 指定窗口 |

<a id="aoqscreencaptureconfig"></a>

#### AoqScreenCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isExternal | bool | false | 是否由应用提供屏幕原始帧。 |
| sourceId | int64\_t | 0 | 屏幕源 ID。 |
| sourceType | AoqScreenShareSourceType | AoqScreenShareSourceTypeDesktop | 屏幕源类型。 |
| appGroup | const char\* | nullptr | iOS 专用，本平台不使用。 |
