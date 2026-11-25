# AOQ Client SDK Linux C++ API 参考

本文介绍 AOQ Client SDK Linux 版的 C++ 接口、回调和数据类型。

> **说明**
>
> AOQ SDK 提供通用视频接口。[Qwen-Audio-Realtime](../../realtime-api-directory/audio-realtime-api-directory/audio-realtime-aoq-access.md) 不支持视频输入或输出；其他模型可使用的媒体能力以对应接入文档为准。

<a id="接口目录"></a>

<a id="a9011dad0dbe"></a>

<a id="a2da4d212484"></a>

## 接口目录

<a id="引擎生命周期"></a>

<a id="32098d69cd10"></a>

<a id="3853d5fc7e0a"></a>

### 引擎生命周期

| 接口 | 简介 |
| --- | --- |
| createEngine | 创建引擎实例（静态方法，单例） |
| destroy | 销毁引擎实例（静态方法） |
| getVersion | 获取 SDK 版本号（静态方法） |
| connect | 连接 Relay 服务器 |
| disconnect | 断开服务器连接 |

<a id="音频设备管理"></a>

<a id="2bd2f8233bdc"></a>

<a id="b4fb44f6eb28"></a>

### 音频设备管理

| 接口 | 简介 |
| --- | --- |
| startAudioCapture | 打开音频采集设备（Linux 空实现） |
| stopAudioCapture | 关闭音频采集设备（Linux 无效果） |
| muteAudioCapture | 静音或取消静音音频采集 |
| startAudioPlayer | 开始音频渲染（Linux 空实现） |
| stopAudioPlayer | 停止音频渲染（Linux 无效果） |
| pauseAudioPlayer | 暂停音频渲染，支持淡出 |
| resumeAudioPlayer | 恢复音频渲染，支持淡入 |
| interruptAudioPlayer | 打断本轮音频播放 |

<a id="音频编解码配置"></a>

<a id="bd9e5ddce015"></a>

<a id="6a6ad5cbb0e5"></a>

### 音频编解码配置

| 接口 | 简介 |
| --- | --- |
| setAudioEncoderConfig | 设置音频编码参数 |
| setAudioDecoderConfig | 设置音频解码参数 |

<a id="视频设备管理"></a>

<a id="265cc12c4caf"></a>

<a id="49303f7eebef"></a>

### 视频设备管理

| 接口 | 简介 |
| --- | --- |
| startVideoCapture | 打开视频采集设备（Linux 仅支持外部采集模式） |
| stopVideoCapture | 关闭视频采集设备 |
| setLocalView | 设置或移除本地视频渲染窗口（Linux 无渲染实现） |
| setRemoteView | 设置或移除远端视频渲染窗口（Linux 无渲染实现） |

<a id="视频编解码与外部输入"></a>

<a id="0d1a46dde7ca"></a>

<a id="189dfcd2badb"></a>

### 视频编解码与外部输入

| 接口 | 简介 |
| --- | --- |
| setVideoEncoderConfig | 设置视频编码参数 |
| setVideoDecoderConfig | 设置视频解码参数（订阅侧 codec 提议） |
| pushExternalVideoCapturedFrame | 推送外部采集视频帧 |
| pushExternalVideoEncodedFrame | 推送外部已编码视频帧 |

<a id="屏幕采集"></a>

### 屏幕采集

| 接口 | 简介 |
| --- | --- |
| startScreenCapture | 启动屏幕采集 |
| stopScreenCapture | 停止屏幕采集 |

<a id="媒体流发送控制"></a>

<a id="2bf94d78886e"></a>

<a id="74db1f031e94"></a>

### 媒体流发送控制

| 接口 | 简介 |
| --- | --- |
| enableSendMediaStream | 控制本地媒体流的发送开关 |

<a id="音频文件播放"></a>

<a id="e867863c5e98"></a>

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

<a id="205dda3a40f3"></a>

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

<a id="实时消息"></a>

<a id="491e6061d9a6"></a>

<a id="a66495101cc7"></a>

### 实时消息

| 接口 | 简介 |
| --- | --- |
| sendDataMsg | 发送实时数据消息 |

<a id="音频帧回调"></a>

<a id="674980f382e5"></a>

<a id="b2a326f23d00"></a>

### 音频帧回调

| 接口 | 简介 |
| --- | --- |
| setAudioFrameObserver | 注册音频帧数据监听器（纯虚） |
| enableAudioFrameObserver | 开启或关闭指定位置的音频帧回调（纯虚） |

<a id="本地音量提示"></a>

<a id="650d3de2e775"></a>

<a id="08ef2d23bcdc"></a>

### 本地音量提示

| 接口 | 简介 |
| --- | --- |
| enableLocalAudioVolumeIndication | 开启或关闭本地采集音量提示回调 |

<a id="视频帧回调"></a>

<a id="3ef08630a590"></a>

<a id="a06fb694f247"></a>

### 视频帧回调

| 接口 | 简介 |
| --- | --- |
| setVideoFrameObserver | 注册视频帧数据监听器（纯虚） |
| enableVideoFrameObserver | 开启或关闭指定位置的视频帧回调（纯虚） |

<a id="aoqengineeventlistener-回调"></a>

<a id="89c8659d56b7"></a>

<a id="42d3bc5083d8"></a>

### AoqEngineEventListener 回调

| 接口 | 简介 |
| --- | --- |
| onError | 引擎错误回调 |
| onWarning | 引擎警告回调 |
| onConnectionStatusChange | 连接状态变化回调 |
| onStats | 引擎统计信息回调 |
| onAudioDeviceStateChanged | 音频设备操作状态变化回调 |
| onAudioDeviceRouteChanged | 音频输出路由变化回调（Linux 不触发） |
| onAudioFileState | 音频文件播放状态回调 |
| onLocalAudioVolumeIndication | 本地采集音量提示回调 |
| onVideoDeviceStateChanged | 视频设备操作状态变化回调 |
| onDataMsg | 收到实时数据消息回调 |

<a id="iaudioframeobserver-回调"></a>

<a id="87896880035d"></a>

<a id="9a808e64aa14"></a>

### IAudioFrameObserver 回调

| 接口 | 简介 |
| --- | --- |
| onCapturedAudioFrame | 采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。 |
| onProcessCapturedAudioFrame | 3A 处理后的音频帧回调。数据经过 3A（AEC/AGC/ANS）处理。 |
| onPublishAudioFrame | 推流前的音频帧回调。数据为即将编码发送的音频帧。 |
| onPlaybackAudioFrame | 播放前的远端音频帧回调。数据为远端解码后、即将播放的音频帧。 |

<a id="ivideoframeobserver-回调"></a>

### IVideoFrameObserver 回调

| 接口 | 简介 |
| --- | --- |
| onCapturedVideoFrame | 采集到原始视频帧时触发（前处理前）。数据为采集后的裸帧，尚未经过前处理。 |
| onPreEncodeVideoFrame | 编码前的视频帧回调（前处理后）。数据为前处理完成、即将编码的裸帧。 |
| onRemoteVideoFrame | 远端解码后、渲染前的视频帧回调。数据为远端解码完成、即将渲染的裸帧。 |

<a id="接口详情"></a>

<a id="5070c24c68a7"></a>

<a id="fa9d753dc761"></a>

## 接口详情

<a id="引擎生命周期-2"></a>

<a id="9324d0dd8aec"></a>

<a id="3853d5fc7e0a-details"></a>

<a id="aoq-api-category-1"></a>

### 引擎生命周期

<a id="createengine"></a>

<a id="1dea2f08eee9"></a>

<a id="217b83ce21b4"></a>

#### createEngine

创建引擎实例。SDK 内部以全局单例方式持有引擎，重复调用会返回已创建的实例。

<a id="code-block"></a>

```cpp
static AoqClientEngine* createEngine(const AoqCreateConfig& config,
                                    AoqEngineEventListener* listener);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqCreateConfig | 引擎创建配置 |
| listener | AoqEngineEventListener\\\* | 引擎事件回调监听器，由调用方继承实现 |

返回值：引擎实例指针；失败返回 `nullptr`。listener 生命周期需长于引擎。

<a id="destroy"></a>

<a id="0801d068af1f"></a>

<a id="3c32463acd34"></a>

#### destroy

销毁引擎实例，释放所有资源。

<a id="code-block-2"></a>

```cpp
static int destroy();
```

返回值：`0` 表示成功；非 `0` 表示失败。

<a id="getversion"></a>

<a id="92dcfeb16ff2"></a>

<a id="9ee46ccd02a5"></a>

#### getVersion

获取 SDK 当前版本号。

<a id="code-block-3"></a>

```cpp
static const char* getVersion();
```

返回值：版本号字符串，字符串由 SDK 持有。

<a id="connect"></a>

<a id="f22e050baf1c"></a>

<a id="0e054fb286f7"></a>

#### connect

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

<a id="code-block-4"></a>

```cpp
virtual int connect(const AoqConnectConfig& config);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqConnectConfig | 连接配置，包含 Token、SID、Relay 接入点数组、推拉流 track 数组等 |

返回值：`0` 表示成功（异步执行）；非 `0` 表示失败。连接结果由 `onConnectionStatusChange` 通知。

> **说明**
>
> `relayEndpoints` / `publishTracks` / `subscribeTracks` 均为“C 风格数组指针 + 长度”，内存由调用方持有，仅需在 connect 调用期间有效。

<a id="disconnect"></a>

<a id="69f9ec0899ff"></a>

<a id="22d67fb3d286"></a>

#### disconnect

断开与服务器的连接，释放连接相关资源。

<a id="code-block-5"></a>

```cpp
virtual int disconnect();
```

返回值：`0` 表示成功；非 `0` 表示失败。

<a id="音频设备管理-2"></a>

<a id="0d6462fd3672"></a>

<a id="b4fb44f6eb28-details"></a>

<a id="aoq-api-category-2"></a>

### 音频设备管理

<a id="code-block-6"></a>

```cpp
virtual int startAudioCapture(const AoqAudioCaptureConfig& config);
virtual int stopAudioCapture();
virtual int muteAudioCapture(bool mute);
virtual int startAudioPlayer(const AoqAudioPlaybackConfig& config);
virtual int stopAudioPlayer();
virtual int pauseAudioPlayer(int fadeMs);
virtual int resumeAudioPlayer(int fadeMs);
virtual int interruptAudioPlayer(AoqTrackType trackType, int fadeMs);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqAudioCaptureConfig / AoqAudioPlaybackConfig | 采集 / 播放配置 |
| mute | bool | true 静音，false 取消静音 |
| fadeMs | int | 淡出 / 淡入时长（毫秒），0 表示立即执行 |
| trackType | AoqTrackType | 轨道类型 |

> **说明**
>
> **Linux 重要约束**：`startAudioCapture` / `startAudioPlayer` 在 Linux 构建下为空实现（直接返回 `0`，不打开任何声卡设备），`stopAudioCapture` / `stopAudioPlayer` 因内部状态未置位同样无实际效果。Linux 上音频输入请使用外部音频流（2.8），音频输出请使用音频帧回调（2.10）自行播放。

<a id="音频编解码配置-2"></a>

<a id="f4fdeb731511"></a>

<a id="6a6ad5cbb0e5-details"></a>

<a id="aoq-api-category-3"></a>

### 音频编解码配置

<a id="code-block-7"></a>

```cpp
virtual int setAudioEncoderConfig(const AoqAudioCodecConfig& config);
virtual int setAudioDecoderConfig(const AoqAudioCodecConfig& config);
```

建议在 `connect()` 之前调用。采样率与模式的非法组合会在 connect 时通过 `onError` 回调 `AoqECParamInvalid`。

<a id="视频设备管理-2"></a>

<a id="a57014eac4a7"></a>

<a id="49303f7eebef-details"></a>

<a id="aoq-api-category-4"></a>

### 视频设备管理

<a id="code-block-8"></a>

```cpp
virtual int startVideoCapture(const AoqVideoCaptureConfig& config);
virtual int stopVideoCapture();
virtual int setLocalView(AoqTrackType trackType, const AoqVideoCanvas& canvas);
virtual int setRemoteView(AoqTrackType trackType, const AoqVideoCanvas& canvas);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqVideoCaptureConfig | 视频采集配置 |
| trackType | AoqTrackType | 视频轨道类型 |
| canvas | AoqVideoCanvas | 渲染画布；`canvas.view == nullptr` 表示解绑 |

> **说明**
>
> **Linux 重要约束**：Linux 摄像头采集为占位实现，不会产出帧，请使用 `startVideoCapture({.isExternal = true})` + `pushExternalVideoCapturedFrame` 送帧；`setLocalView` / `setRemoteView` 在 Linux 无渲染后端，预览请通过视频帧回调（2.12）自行渲染。

<a id="视频编解码与外部输入-2"></a>

<a id="4922b0feb7de"></a>

<a id="189dfcd2badb-details"></a>

<a id="aoq-api-category-5"></a>

### 视频编解码与外部输入

<a id="code-block-9"></a>

```cpp
virtual int setVideoEncoderConfig(const AoqVideoCodecConfig& config);
virtual int setVideoDecoderConfig(const AoqVideoCodecConfig& config);
virtual int pushExternalVideoCapturedFrame(AoqTrackType trackType, const AoqVideoFrame& frame);
virtual int pushExternalVideoEncodedFrame(AoqTrackType trackType, const AoqVideoEncodedFrame& frame);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| config | AoqVideoCodecConfig | 编解码配置，按 `config.trackType` 路由 |
| trackType | AoqTrackType | 路由目标，取 `AoqTrackTypeVideo` |
| frame | AoqVideoFrame / AoqVideoEncodedFrame | 裸帧 / 已编码帧数据 |

> **说明**
>
> -   `setVideoDecoderConfig` 为订阅侧 codec 提议，需在 `connect` 之前调用；解码时仅 `trackType/codecType/width/height/fps/bitrate` 生效。
> -   `pushExternalVideoCapturedFrame` Video 轨道需先调用 `startVideoCapture(isExternal=true)`，Screen 轨道需先调用 `startScreenCapture(isExternal=true)`；未启动外部采集时返回 `AoqECVideoExternalCaptureNotEnabled(211)`，格式不支持时返回 `AoqECParamInvalid`，缓冲区满时返回 `AoqECVideoExternalBufferFull(210)`。
> -   `pushExternalVideoEncodedFrame` 需先 `setVideoEncoderConfig(isExternal=true)`，SDK 不做二次编码直接打包发送，当前仅支持 JPEG。
> -   `frame.timeStamp` 为 `0` 时由 SDK 使用本地时间补齐。

<a id="屏幕采集-2"></a>

<a id="aoq-api-category-6"></a>

### 屏幕采集

<a id="code-block-10"></a>

```cpp
virtual int startScreenCapture(const AoqScreenCaptureConfig& config);
virtual int stopScreenCapture();
```

`config` 为屏幕采集配置。屏幕画面通过 `AoqTrackTypeScreen` 轨道发送。

返回值：0 表示成功；非 0 表示失败。 接口同步返回，不提供 `onScreenCaptureStateChanged` 回调。

Linux 仅支持外部原始帧输入，必须设置 `isExternal=true`。不支持内部屏幕采集或屏幕源枚举，配置中不存在 `sourceId` 和 `sourceType` 字段。

外部原始帧：设置 `isExternal=true` 后，通过 `pushExternalVideoCapturedFrame` 输入 Screen 轨道的原始帧，由 SDK 编码。外部已编码帧：先通过 `setVideoEncoderConfig` 将 Screen 轨道设置为外部编码，再调用 `pushExternalVideoEncodedFrame`；不需要调用 `startScreenCapture`。

<a id="媒体流发送控制-2"></a>

<a id="be25c201139e"></a>

<a id="74db1f031e94-details"></a>

<a id="aoq-api-category-7"></a>

### 媒体流发送控制

<a id="code-block-11"></a>

```cpp
virtual int enableSendMediaStream(AoqTrackType trackType, bool enable);
```

控制本地某路媒体流是否发送，`trackType` 取 `AoqTrackTypeAudio` / `AoqTrackTypeVideo` 或 `AoqTrackTypeScreen`。返回 `0` 表示调用已下发（异步执行）。建议初始化后先关闭发送，待 `onConnectionStatusChange` 上报 `AoqConnectionStatusConnected` 后再开启。

<a id="音频文件播放-2"></a>

<a id="dfb57f25e52e"></a>

<a id="28f63a96752c-details"></a>

<a id="aoq-api-category-8"></a>

### 音频文件播放

<a id="code-block-12"></a>

```cpp
virtual int startAudioFile(const char* fileId, const AoqAudioFileMixConfig& config);
virtual int stopAudioFile(const char* fileId);
virtual int pauseAudioFile(const char* fileId);
virtual int resumeAudioFile(const char* fileId);
virtual int64_t getAudioFileDuration(const char* fileId);
virtual int64_t getAudioFileCurrentPosition(const char* fileId);
virtual int setAudioFilePositionMillis(const char* fileId, int64_t positionMillis);
virtual int setAudioFileVolume(const char* fileId, AoqAudioStreamDirection type, int volume);
virtual int getAudioFileVolume(const char* fileId, AoqAudioStreamDirection type);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| fileId | const char\\\* | 音频文件 Id，**业务层需保证全局唯一** |
| config | AoqAudioFileMixConfig | 文件混音配置 |
| positionMillis | int64\_t | 目标播放位置（毫秒） |
| type | AoqAudioStreamDirection | 推流音量或本地播放音量 |
| volume | int | 音量，取值范围 0-100 |

返回值说明：

-   `getAudioFileDuration` / `getAudioFileCurrentPosition`：`>=0` 为毫秒值；`<0` 失败，绝对值为 `-AoqErrorCode`。
-   `getAudioFileVolume`：`0-100` 为音量值；`<0` 失败，绝对值为 `-AoqErrorCode`。

播放状态变化通过 `onAudioFileState` 回调上报。文件混音走推流链路，不依赖本地声卡，因此在 Linux 上可用于将本地文件作为音频源推送。

<a id="外部音频流-2"></a>

<a id="d925b0475fbf"></a>

<a id="d6b4c13dff30-details"></a>

<a id="aoq-api-category-9"></a>

### 外部音频流

<a id="code-block-13"></a>

```cpp
virtual int addAudioExternalStream(const char* streamId, const AoqAudioExternalStreamConfig& config);
virtual int pushAudioExternalStreamData(const char* streamId, AoqAudioFrameData& data);
virtual int setAudioExternalStreamVolume(const char* streamId, AoqAudioStreamDirection type, int vol);
virtual int getAudioExternalStreamVolume(const char* streamId, AoqAudioStreamDirection type);
virtual void clearAudioExternalStreamBuffer(const char* streamId, int fadeoutMs);
virtual int removeAudioExternalStream(const char* streamId);
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| streamId | const char\\\* | 外部音频流 Id，**业务层需保证全局唯一** |
| config | AoqAudioExternalStreamConfig | 外部音频流配置 |
| data | AoqAudioFrameData | 外部音频裸数据（PCM），非 const 引用 |
| type | AoqAudioStreamDirection | 推流音量或本地播放音量 |
| vol | int | 音量，取值范围 0-100 |
| fadeoutMs | int | 淡出时长；`-1` 用 SDK 默认淡出，`0` 全部清空无淡出，`>0` 保留指定毫秒淡出 |

> **说明**
>
> -   `pushAudioExternalStreamData` 返回 `AoqECAudioExternalBufferFull(110)` 表示 SDK 内部缓冲区已满，**建议等待 20ms 后重新送当前数据帧**。
>     
> -   最佳实践：实时采集场景一次 Push 10ms 数据、有数据就 Push；文件源场景一次 Push 40ms 数据、间隔 30ms 送一次，并处理 `AoqECAudioExternalBufferFull` 返回。
>     
> -   `getAudioExternalStreamVolume`：`0-100` 为音量值；`<0` 失败，绝对值为 `-AoqErrorCode`。
>     
> -   `clearAudioExternalStreamBuffer` 返回 `void`，无返回值。
>     
> -   `data.pushSequence` 用于 SDK 消费完成通知（PCM 输入轮次）。
>     
>     > **说明**
>     >
>     > Linux 上无真实采集设备，**本组接口是音频上行的主链路**。

<a id="实时消息-2"></a>

<a id="6fb531ac805a"></a>

<a id="a66495101cc7-details"></a>

<a id="aoq-api-category-10"></a>

### 实时消息

<a id="code-block-14"></a>

```cpp
virtual int sendDataMsg(const AoqDataMsg& msg);
```

发送实时数据消息。`msg.data` 指向调用方持有的内存，仅需在调用期间有效。对端消息通过 `onDataMsg` 回调。

<a id="音频帧回调-2"></a>

<a id="c39a0e98cf59"></a>

<a id="b2a326f23d00-details"></a>

<a id="aoq-api-category-11"></a>

### 音频帧回调

<a id="code-block-15"></a>

```cpp
virtual int setAudioFrameObserver(IAudioFrameObserver* observer) = 0;
virtual int enableAudioFrameObserver(bool enabled, AoqAudioSource audioSource,
                                     const AoqAudioObserverConfig& config) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| observer | IAudioFrameObserver\\\* | 监听器实例；传 `nullptr` 停止回调 |
| enabled | bool | 是否开启该位置的数据回调 |
| audioSource | AoqAudioSource | 音频裸数据源位置 |
| config | AoqAudioObserverConfig | 回调采样率、声道数与读写模式 |

使用步骤：先 `setAudioFrameObserver(observer)` 注册监听器，再对需要的位置调 `enableAudioFrameObserver`。observer 生命周期需覆盖整个回调期间；取消注册后再释放。

读写模式支持情况（见 IAudioFrameObserver 声明）：`onCapturedAudioFrame` / `onProcessCapturedAudioFrame` / `onPlaybackAudioFrame` 支持读写，`onPublishAudioFrame` 仅支持只读。

> **说明**
>
> Linux 上 `setAudioFrameObserver` 内部走异步投递（PostTask 到控制线程）完成注册，因此调用返回后回调可能略后生效；**释放 observer 前请留足安全间隔或保持对象存活**。

<a id="本地音量提示-2"></a>

<a id="fd58e47c9c7d"></a>

<a id="08ef2d23bcdc-details"></a>

<a id="aoq-api-category-12"></a>

### 本地音量提示

<a id="code-block-16"></a>

```cpp
virtual int enableLocalAudioVolumeIndication(const AoqAudioVolumeIndicationConfig& config);
```

开启/关闭本地采集音量提示。`config.interval <= 0` 时关闭回调；开启后按 `config.interval` 周期触发 `onLocalAudioVolumeIndication`。需在 `startAudioCapture` 之后调用才有音量数据。

> **说明**
>
> Linux 上无设备采集，该回调的音量数据来自推流/播放混音链路（mixer）。

<a id="视频帧回调-2"></a>

<a id="e9225f13866c"></a>

<a id="a06fb694f247-details"></a>

<a id="aoq-api-category-13"></a>

### 视频帧回调

<a id="code-block-17"></a>

```cpp
virtual int setVideoFrameObserver(IVideoFrameObserver* observer) = 0;
virtual int enableVideoFrameObserver(bool enabled, AoqVideoSource videoSource,
                                     const AoqVideoObserverConfig& config) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| observer | IVideoFrameObserver\\\* | 监听器实例；传 `nullptr` 停止回调 |
| enabled | bool | 是否开启该位置的数据回调 |
| videoSource | AoqVideoSource | 视频帧回调数据源（管线位置） |
| config | AoqVideoObserverConfig | 期望像素格式、对齐策略、读写模式、镜像 |

回调返回 `true` 表示数据已修改需写回 SDK（仅 I420 / CVPixelBuffer 生效，Linux 下即仅 I420）；返回 `false` 为只读。

> **说明**
>
> Linux 无内置渲染，**本组回调是获取远端视频画面的唯一途径**（`AoqVideoSourceRemote`）。

<a id="aoqengineeventlistener-回调-2"></a>

<a id="628a3235dc29"></a>

<a id="42d3bc5083d8-details"></a>

<a id="aoq-api-category-14"></a>

### AoqEngineEventListener 回调

`AoqEngineEventListener` 是 SDK 所有异步事件通知的统一出口，由调用方继承实现并在 `createEngine` 时传入。

> **说明**
>
> 该类所有回调均为**纯虚函数**（`= 0`），无默认空实现，Linux 下必须完整实现下列 10 个方法，否则派生类无法实例化。回调可能在 SDK 内部线程触发。

<a id="code-block-18"></a>

```cpp
class AOQ_API AoqEngineEventListener {
public:
    AoqEngineEventListener();
    virtual ~AoqEngineEventListener();

    virtual void onError(int code, const char* message) = 0;
    virtual void onWarning(int code, const char* message) = 0;
    virtual void onConnectionStatusChange(AoqConnectionStatus status) = 0;
    virtual void onStats(const AoqStats& stats) = 0;
    virtual void onAudioDeviceStateChanged(const AoqAudioDeviceState& state) = 0;
    virtual void onAudioDeviceRouteChanged(int routeType) = 0;
    virtual void onAudioFileState(const AoqAudioFileState& state) = 0;
    virtual void onLocalAudioVolumeIndication(const AoqAudioVolume& volume) = 0;
    virtual void onVideoDeviceStateChanged(const AoqVideoDeviceState& state) = 0;
    virtual void onDataMsg(const AoqDataMsg& msg) = 0;
};
```

<a id="onerror"></a>

<a id="c833816cf831"></a>

<a id="041a008599c4"></a>

#### onError

引擎错误回调。`code` 对应 `AoqErrorCode` 枚举值（见 3.3），`message` 仅回调期间有效。

<a id="onwarning"></a>

<a id="88328cd2b742"></a>

<a id="7f5de347d086"></a>

#### onWarning

引擎警告回调。`code` 对应 `AoqWarningCode` 枚举值（见 3.3）。

<a id="onconnectionstatuschange"></a>

<a id="f59556295b44"></a>

<a id="531e564ffb39"></a>

#### onConnectionStatusChange

连接状态变化回调。状态流转：Disconnected -> Connecting -> Connected / Failed -> Disconnected。

<a id="onstats"></a>

<a id="72dd3201524c"></a>

<a id="e4911422f0d4"></a>

#### onStats

引擎统计信息回调。SDK 周期性上报音视频推拉流及网络统计数据，可用于实时监测通话质量、网络状态、诊断音视频问题。

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| stats | AoqStats | 包含音频 / 视频 / 数据消息的推拉流统计及网络统计 |

> **说明**
>
> `AoqStats` 内部为“数组指针 + 计数”结构，指针仅回调期间有效，异步使用需自行拷贝。

<a id="onaudiodevicestatechanged"></a>

<a id="45d742401ad8"></a>

<a id="86cad5c9b5a8"></a>

#### onAudioDeviceStateChanged

音频设备采集 / 播放操作状态变化回调。`state.reason` 为 `AoqErrorCode` 数值。

<a id="onaudiodeviceroutechanged"></a>

<a id="ab6d432ac26f"></a>

<a id="7af35bfcfc45"></a>

#### onAudioDeviceRouteChanged

音频输出路由变化回调。`routeType` 对应 `AoqAudioDeviceRouteType` 枚举值（见 3.4）。

> **说明**
>
> **Linux 不会触发**：Linux 构建未包含平台设备监听器，且服务端音频设备不产生路由事件；仍需实现此方法（纯虚），但可空实现。

<a id="onaudiofilestate"></a>

<a id="264e4e1f26d6"></a>

<a id="4879b3394dd2"></a>

#### onAudioFileState

音频文件播放状态回调。`state.fileId` 仅回调期间有效。

<a id="onlocalaudiovolumeindication"></a>

<a id="a8ebba9b0c6e"></a>

<a id="89b1352928e4"></a>

#### onLocalAudioVolumeIndication

本地采集音量提示回调，需调用 `enableLocalAudioVolumeIndication` 开启。

<a id="onvideodevicestatechanged"></a>

<a id="50f557fb17dd"></a>

<a id="0824f8ffb050"></a>

#### onVideoDeviceStateChanged

视频设备采集操作状态变化回调。`state.reason` 为 `AoqErrorCode` 数值。

<a id="ondatamsg"></a>

<a id="46f3e9a98aa9"></a>

<a id="825294c8fc0b"></a>

#### onDataMsg

收到实时数据消息回调。`msg.data`**仅保证回调期间有效**，如需异步使用请自行拷贝。

<a id="iaudioframeobserver-回调-2"></a>

<a id="d4594a2798c1"></a>

<a id="341e02fe4e34"></a>

<a id="aoq-api-category-15"></a>

<a id="bd5ce9437788"></a>

<a id="9a808e64aa14-details"></a>

### IAudioFrameObserver 回调

音频数据监听接口。**请不要在回调中做任何耗时操作，否则可能导致声音异常**。全部为纯虚函数，需完整实现。

<a id="code-block-19"></a>

```cpp
class AOQ_API IAudioFrameObserver {
public:
    virtual ~IAudioFrameObserver() {}
    virtual void onCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
    virtual void onProcessCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
    virtual void onPublishAudioFrame(AoqTrackType trackType, const AoqAudioFrameData& data) = 0;
    virtual void onPlaybackAudioFrame(const AoqAudioFrameData& data) = 0;
};
```

| 回调 | 开启方式（audioSource） | 读写模式 |
| --- | --- | --- |
| onCapturedAudioFrame | AoqAudioSourceCaptured | 支持读写 |
| onProcessCapturedAudioFrame | AoqAudioSourceProcessCaptured | 支持读写 |
| onPublishAudioFrame | AoqAudioSourcePublish（需 connect 成功） | 仅只读 |
| onPlaybackAudioFrame | AoqAudioSourcePlayback | 支持读写 |

以上回调均支持通过 `AoqAudioObserverConfig` 设置采样率与声道数。

> **说明**
>
> Linux 上 `onPlaybackAudioFrame` 是取远端下行 PCM 的主链路；`onProcessCapturedAudioFrame`（3A 后数据）因 Linux 未编译 3A 模块，数据与采集原始数据无实质差异。

<a id="oncapturedaudioframe"></a>

#### onCapturedAudioFrame

采集到原始音频帧时触发。数据为采集后的原始 PCM，未经任何处理。

<a id="code-block-20"></a>

```cpp
virtual void onCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | const AoqAudioFrameData& | 采集的音频帧数据 |

返回值：无（void）。

> **说明**
>
> data 中的指针仅在回调期间有效，异步使用需自行拷贝。Linux 上无真实采集设备，此回调的数据来自外部音频流或混音链路。

<a id="onprocesscapturedaudioframe"></a>

#### onProcessCapturedAudioFrame

3A 处理后的音频帧回调。数据经过 3A（AEC/AGC/ANS）处理。

<a id="code-block-21"></a>

```cpp
virtual void onProcessCapturedAudioFrame(const AoqAudioFrameData& data) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | const AoqAudioFrameData& | 3A 处理后的音频帧数据 |

返回值：无（void）。

> **说明**
>
> data 中的指针仅在回调期间有效，异步使用需自行拷贝。Linux 上未编译 3A 模块，数据与采集原始数据无实质差异。

<a id="onpublishaudioframe"></a>

#### onPublishAudioFrame

推流前的音频帧回调。数据为即将编码发送的音频帧。

<a id="code-block-22"></a>

```cpp
virtual void onPublishAudioFrame(AoqTrackType trackType, const AoqAudioFrameData& data) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| trackType | AoqTrackType | 音频轨道类型 |
| data | const AoqAudioFrameData& | 推流前的音频帧数据 |

返回值：无（void）。

> **说明**
>
> data 中的指针仅在回调期间有效，异步使用需自行拷贝。此回调仅支持只读模式。

<a id="onplaybackaudioframe"></a>

#### onPlaybackAudioFrame

播放前的远端音频帧回调。数据为远端解码后、即将播放的音频帧。

<a id="code-block-23"></a>

```cpp
virtual void onPlaybackAudioFrame(const AoqAudioFrameData& data) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| data | const AoqAudioFrameData& | 播放前的远端音频帧数据 |

返回值：无（void）。

> **说明**
>
> data 中的指针仅在回调期间有效，异步使用需自行拷贝。Linux 上此回调是取远端下行 PCM 的主链路。

<a id="ivideoframeobserver-回调-2"></a>

<a id="2545f977a98d"></a>

<a id="261977ee8a1f"></a>

<a id="aoq-api-category-16"></a>

### IVideoFrameObserver 回调

视频数据监听接口。**请不要在回调中做任何耗时操作，否则可能导致画面卡顿**。全部为纯虚函数。

<a id="code-block-24"></a>

```cpp
class AOQ_API IVideoFrameObserver {
public:
    virtual ~IVideoFrameObserver() {}
    virtual bool onCapturedVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
    virtual bool onPreEncodeVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
    virtual bool onRemoteVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
};
```

| 回调 | 开启方式（videoSource） | 说明 |
| --- | --- | --- |
| onCapturedVideoFrame | AoqVideoSourceCaptured | 本地采集后裸数据（前处理前） |
| onPreEncodeVideoFrame | AoqVideoSourcePreEncode | 本地编码前裸数据（前处理后） |
| onRemoteVideoFrame | AoqVideoSourceRemote | 远端解码后、渲染前裸数据 |

返回值：`true` 表示数据已修改、需写回 SDK（仅 I420 / CVPixelBuffer 生效）；`false` 表示只读。`frame` 中的指针仅回调期间有效，异步使用需自行拷贝。

<a id="oncapturedvideoframe"></a>

#### onCapturedVideoFrame

采集到原始视频帧时触发（前处理前）。数据为采集后的裸帧，尚未经过前处理。

<a id="code-block-25"></a>

```cpp
virtual bool onCapturedVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| trackType | AoqTrackType | 帧所属轨道（Video / Screen） |
| frame | AoqVideoFrame& | 采集的视频帧数据 |

返回值：true 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 生效），false 表示只读。

> **说明**
>
> frame 中的指针仅在回调期间有效，异步使用需自行拷贝。

<a id="onpreencodevideoframe"></a>

#### onPreEncodeVideoFrame

编码前的视频帧回调（前处理后）。数据为前处理完成、即将编码的裸帧。

<a id="code-block-26"></a>

```cpp
virtual bool onPreEncodeVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| trackType | AoqTrackType | 帧所属轨道（Video / Screen） |
| frame | AoqVideoFrame& | 编码前的视频帧数据 |

返回值：true 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 生效），false 表示只读。

> **说明**
>
> frame 中的指针仅在回调期间有效，异步使用需自行拷贝。

<a id="onremotevideoframe"></a>

#### onRemoteVideoFrame

远端解码后、渲染前的视频帧回调。数据为远端解码完成、即将渲染的裸帧。

<a id="code-block-27"></a>

```cpp
virtual bool onRemoteVideoFrame(AoqTrackType trackType, AoqVideoFrame& frame) = 0;
```

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| trackType | AoqTrackType | 帧所属轨道（Video / Screen） |
| frame | AoqVideoFrame& | 远端解码后的视频帧数据 |

返回值：true 表示数据已修改需写回 SDK（仅 I420/CVPixelBuffer 生效），false 表示只读。

> **说明**
>
> frame 中的指针仅在回调期间有效，异步使用需自行拷贝。Linux 无内置渲染，此回调是获取远端视频画面的唯一途径。

<a id="数据类型与枚举"></a>

<a id="a110f2e82b37"></a>

<a id="766626a04136"></a>

## 数据类型与枚举

<a id="通用类型"></a>

<a id="8d1fce66b1fa"></a>

<a id="07322b5db657"></a>

### 通用类型

<a id="aoqcreateconfig"></a>

<a id="d5c7c0727008"></a>

<a id="eed0f444e642"></a>

#### AoqCreateConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| workDir | const char\\\* | nullptr | SDK 工作目录（日志与临时文件） |
| enableDumpAudio | bool | false | 是否开启音频数据保存（调试用） |
| extras | const char\\\* | nullptr | 扩展参数（JSON 字符串） |
| maxEncodedVideoFrameBytes | int | 190 × 1024 | 编码后单帧大小上限（字节），仅用于 SDK 内部 JPEG 编码。0 表示关闭限制。 |
| enableDropOversizedVideoFrame | bool | false | 仅用于 SDK 内部 JPEG 编码：降至最低质量后仍超限时，是否允许丢弃该帧。 |

> **说明**
>
> 字符串字段至少需保持到 `createEngine` 返回后，引擎内部按需拷贝。Linux 无 `isBTScoMode` 字段。

<a id="aoqconnectconfig"></a>

<a id="461b4e5b73ab"></a>

<a id="3e7902dce8b5"></a>

#### AoqConnectConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| token | const char\\\* | nullptr | 连接鉴权 Token |
| sid | const char\\\* | nullptr | 会话 ID |
| certFingerprint | const char\\\* | nullptr | 服务器证书指纹 |
| workspaceIdHash | const char\\\* | nullptr | 工作空间 ID Hash |
| relayEndpoints | const AoqRelayEndpoint\\\* | nullptr | Relay 接入点数组首地址 |
| relayEndpointsCount | size\_t | 0 | Relay 接入点个数 |
| publishTracks | const AoqTrackParam\\\* | nullptr | 推流 track 属性数组首地址 |
| publishTracksCount | size\_t | 0 | 推流 track 个数 |
| subscribeTracks | const AoqTrackParam\\\* | nullptr | 拉流 track 属性数组首地址 |
| subscribeTracksCount | size\_t | 0 | 拉流 track 个数 |

<a id="aoqrelayendpoint"></a>

<a id="3caf57531f94"></a>

<a id="b58a1473e07b"></a>

#### AoqRelayEndpoint

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| route\_index | int | \-1 | 路由序号 |
| endpoint | const char\\\* | nullptr | Relay 服务器域名或 IP |
| port | int | 0 | Relay 服务器端口 |
| tcp\_port | int | 0 | TCP 降级端口；0 表示使用 SDK 默认端口 443。 |

> **说明**
>
> 注意字段名为下划线风格 `route_index`，与其余字段的 camelCase 不同。

<a id="aoqtrackparam"></a>

<a id="a3367e5ed7ae"></a>

<a id="570fc294b704"></a>

#### AoqTrackParam

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeAudio | 轨道类型 |
| trackMode | AoqTrackMode | AoqTrackModeSegment | 流式 / 非流式模式，仅对音频下行生效 |

<a id="aoqdatamsg"></a>

<a id="84e79504a5c7"></a>

<a id="e0d8895ec85c"></a>

#### AoqDataMsg

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| data | const uint8\_t\\\* | nullptr | 消息内容，指向调用方持有的内存 |
| dataSize | size\_t | 0 | 字节数 |

> **说明**
>
> 回调中使用时仅保证回调期间有效，如需异步使用请自行拷贝。

<a id="统计信息类型"></a>

<a id="43fab486a8f9"></a>

<a id="cc8be743dfe5"></a>

### 统计信息类型

<a id="aoqstats"></a>

<a id="f1e16409571e"></a>

<a id="86a11bf11767"></a>

#### AoqStats

引擎统计信息汇总，通过 `onStats` 周期性上报。采用“数组指针 + 计数”结构，所有指针默认 `nullptr`、计数默认 `0`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| audioPublishStats | const AoqAudioPublishStats\\\* | 音频推流统计数组 |
| audioPublishStatsCount | unsigned int | 音频推流统计个数 |
| videoPublishStats | const AoqVideoPublishStats\\\* | 视频推流统计数组 |
| videoPublishStatsCount | unsigned int | 视频推流统计个数 |
| dataMsgPublishStats | const AoqDataMsgPublishStats\\\* | 数据消息推流统计数组 |
| dataMsgPublishStatsCount | unsigned int | 数据消息推流统计个数 |
| audioSubscribeStats | const AoqAudioSubscribeStats\\\* | 音频拉流统计数组 |
| audioSubscribeStatsCount | unsigned int | 音频拉流统计个数 |
| videoSubscribeStats | const AoqVideoSubscribeStats\\\* | 视频拉流统计数组 |
| videoSubscribeStatsCount | unsigned int | 视频拉流统计个数 |
| dataMsgSubscribeStats | const AoqDataMsgSubscribeStats\\\* | 数据消息拉流统计数组 |
| dataMsgSubscribeStatsCount | unsigned int | 数据消息拉流统计个数 |
| networkStats | const AoqNetworkStats\\\* | 网络统计信息 |

<a id="aoqaudiopublishstats"></a>

<a id="7cbcd1e78b42"></a>

<a id="49a572d6136d"></a>

#### AoqAudioPublishStats

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeAudio | 轨道类型 |
| bitrate | unsigned int | 0 | 码率（bps） |
| bytes | uint64\_t | 0 | 累计发送字节数 |
| encodeVolume | unsigned int | 0 | 推流编码音量 |

<a id="aoqaudiosubscribestats"></a>

<a id="93322791c9e9"></a>

<a id="db3288b89c28"></a>

#### AoqAudioSubscribeStats

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeAudio | 轨道类型 |
| bitrate | unsigned int | 0 | 码率（bps） |
| bytes | uint64\_t | 0 | 累计接收字节数 |
| playVolume | unsigned int | 0 | 播放音量 |

<a id="aoqvideopublishstats"></a>

<a id="3ae8f021fe08"></a>

<a id="41ad9a0276e8"></a>

#### AoqVideoPublishStats

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeVideo | 轨道类型 |
| bitrate | unsigned int | 0 | 码率（bps） |
| bytes | uint64\_t | 0 | 累计发送字节数 |
| encodeFps | unsigned int | 0 | 编码帧率 |

<a id="aoqvideosubscribestats"></a>

<a id="74efaabcc7ac"></a>

<a id="ba67dc7745e1"></a>

#### AoqVideoSubscribeStats

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeVideo | 轨道类型 |
| bitrate | unsigned int | 0 | 码率（bps） |
| bytes | uint64\_t | 0 | 累计接收字节数 |
| decodeFps | unsigned int | 0 | 解码帧率 |
| renderFps | unsigned int | 0 | 渲染帧率 |

<a id="aoqdatamsgpublishstats-aoqdatamsgsubscribestats"></a>

<a id="67c577a486da"></a>

<a id="2cc7816af4f3"></a>

#### AoqDataMsgPublishStats / AoqDataMsgSubscribeStats

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeData | 轨道类型 |
| bitrate | unsigned int | 0 | 码率（bps） |
| bytes | uint64\_t | 0 | 累计发送 / 接收字节数 |

<a id="aoqnetworkstats"></a>

<a id="39fa98fa29e7"></a>

<a id="d76371d0d4bd"></a>

#### AoqNetworkStats

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| sendBitrate | unsigned int | 0 | 发送码率（bps） |
| sendBytes | uint64\_t | 0 | 累计发送字节数 |
| recvBitrate | unsigned int | 0 | 接收码率（bps） |
| recvBytes | uint64\_t | 0 | 累计接收字节数 |
| loss | unsigned int | 0 | 丢包率（0-100） |
| rtt | unsigned int | 0 | 往返延迟（ms） |

<a id="枚举类型"></a>

<a id="e053daf72c5d"></a>

<a id="15c0fdfe25ae"></a>

### 枚举类型

<a id="aoqtracktype"></a>

<a id="5aabeaf5de44"></a>

<a id="3fdbea5749db"></a>

#### AoqTrackType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqTrackTypeAudio | 0 | 音频轨道 |
| AoqTrackTypeVideo | 1 | 视频轨道 |
| AoqTrackTypeData | 2 | 数据消息轨道 |
| AoqTrackTypeScreen | 3 | 屏幕共享轨道，仅支持上行。 |

<a id="aoqtrackmode"></a>

<a id="fe51f12512ab"></a>

<a id="8d076f2fd379"></a>

#### AoqTrackMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqTrackModeSegment | 0 | 分段：数据按语义片段（如一句话）打包送达 |
| AoqTrackModeStream | 1 | 流式：数据持续、连续地送达 |

<a id="aoqencodertype"></a>

<a id="47116c781e06"></a>

<a id="9b1a9915d442"></a>

#### AoqEncoderType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqEncoderTypeUnknown | 0 | 未知格式 |
| AoqEncoderTypeAudioPCM | 1 | 音频 PCM |
| AoqEncoderTypeAudioOpus | 2 | 音频 Opus（插件化；Linux 已静态内置，开箱可用） |
| AoqEncoderTypeVideoH264 | 3 | 视频 H.264 |
| AoqEncoderTypeVideoJpeg | 4 | 视频 JPEG |
| AoqEncoderTypeDataText | 5 | 数据文本 |

<a id="aoqconnectionstatus"></a>

<a id="5cbdcdae0cee"></a>

<a id="135d71f67043"></a>

#### AoqConnectionStatus

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqConnectionStatusDisconnected | 0 | 未连接 |
| AoqConnectionStatusConnecting | 1 | 连接中 |
| AoqConnectionStatusConnected | 2 | 已连接 |
| AoqConnectionStatusFailed | 3 | 连接失败 |

<a id="aoqerrorcode"></a>

<a id="c4d3567a2c37"></a>

<a id="9386b370e4a2"></a>

#### AoqErrorCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqECOK | 0 | 成功 |
| AoqECParamInvalid | 1 | 参数非法 |
| AoqECStateInvalid | 2 | 状态非法 |
| AoqECUnSupport | 3 | 接口被调但当前平台 / 模式未实现 |
| AoqECAudio | 100 | 音频通用错误 |
| AoqECAudioExternalBufferFull | 110 | 外部音频缓冲区满 |
| AoqECAudioDevice | 120 | 音频设备通用错误 |
| AoqECAudioDeviceRecordingAuthFailed | 121 | 录音权限未获取 |
| AoqECAudioDeviceRecordingOccupied | 122 | 录音设备被占用 |
| AoqECAudioDeviceRecordingBackgroundStart | 123 | 后台启动录音失败 |
| AoqECAudioDeviceRecordingStartFail | 124 | 录音启动失败 |
| AoqECAudioDevicePlayoutOccupied | 125 | 播放设备被占用 |
| AoqECAudioDevicePlayoutBackgroundStart | 126 | 后台启动播放失败 |
| AoqECAudioDevicePlayoutStartFail | 127 | 播放启动失败 |
| AoqECAudioDeviceEarpieceRequiresVoipMode | 128 | 听筒需要 VoIP 模式（移动端场景） |
| AoqECVideo | 200 | 视频通用错误 |
| AoqECVideoExternalBufferFull | 210 | 外部视频缓冲区满 |
| AoqECVideoExternalCaptureNotEnabled | 211 | 外部视频采集未启用 |
| AoqECVideoExternalEncoderNotEnabled | 212 | 外部视频编码未启用 |
| AoqECVideoDevice | 220 | 视频设备通用错误 |
| AoqECVideoDeviceCameraOpenFail | 221 | 摄像头打开失败 |
| AoqECVideoDeviceCameraAuthFailed | 222 | 摄像头权限未获取 |
| AoqECVideoDeviceCameraOccupied | 223 | 摄像头被占用 |
| AoqECVideoDeviceCameraRunningError | 224 | 摄像头运行异常 |
| AoqECVideoCodec | 230 | 视频编解码通用错误 |
| AoqECVideoCodecEncoderInitFail | 231 | 视频编码器初始化失败 |
| AoqECVideoRender | 240 | 视频渲染通用错误 |
| AoqECVideoRenderCreateFail | 241 | 视频渲染创建失败 |
| AoqECVideoRenderDrawError | 242 | 视频渲染绘制错误 |
| AoqECScreen | 300 | 屏幕采集通用错误 |
| AoqECScreenAuthFailed | 310 | 屏幕采集授权失败 |
| AoqECScreenStartFailed | 311 | 屏幕采集启动失败 |

<a id="aoqwarningcode"></a>

<a id="2764e9ca7a7d"></a>

<a id="d0063370a974"></a>

#### AoqWarningCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqWCOK | 0 | 无警告 |
| AoqWCAudio | 100 | 音频通用警告 |
| AoqWCAudioHowling | 101 | 音频啸叫检测 |
| AoqWCAudioDevice | 120 | 音频设备通用警告 |
| AoqWCAudioDeviceMicEnumerateError | 121 | 麦克风枚举错误 |
| AoqWCAudioDeviceMicStartTimeout | 122 | 麦克风启动超时 |
| AoqWCAudioDeviceRecordingError | 123 | 录音过程错误 |
| AoqWCAudioDeviceSpeakerEnumerateError | 124 | 扬声器枚举错误 |
| AoqWCAudioDeviceSpeakerStartTimeout | 125 | 扬声器启动超时 |
| AoqWCAudioDevicePlayoutError | 126 | 播放过程错误 |
| AoqWCVideo | 200 | 视频通用警告 |
| AoqWCVideoCameraEnumerateError | 201 | 摄像头枚举错误 |
| AoqWCVideoEncoderSwitched | 202 | 视频编码器已切换 |
| AoqWCVideoRenderDowngrade | 203 | 视频渲染降级 |

<a id="aoqmirrormode"></a>

<a id="13762327da5e"></a>

<a id="eddaf8964076"></a>

#### AoqMirrorMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqMirrorModeDisabled | 0 | 关闭镜像 |
| AoqMirrorModeEnabled | 1 | 开启镜像 |

<a id="aoqorientationmode"></a>

<a id="f043bb825333"></a>

<a id="e5316f53804b"></a>

#### AoqOrientationMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqOrientationModeAuto | 0 | 自动适应 |
| AoqOrientationModePortrait | 1 | 竖屏 |
| AoqOrientationModeLandscape | 2 | 横屏 |

<a id="aoqrendermode"></a>

<a id="27ce765c688b"></a>

<a id="c5b270577e22"></a>

#### AoqRenderMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqRenderModeAuto | 0 | 自适应模式 |
| AoqRenderModeStretch | 1 | 拉伸模式 |
| AoqRenderModeFill | 2 | 填充模式 |
| AoqRenderModeCrop | 3 | 裁剪模式 |

> **说明**
>
> 仅作为 `AoqVideoCanvas.renderMode` 使用；Linux 无渲染实现，该枚举实际不生效。

<a id="aoqaudiostreamdirection"></a>

<a id="a5e0b0667d74"></a>

<a id="fd4659864a5e"></a>

#### AoqAudioStreamDirection

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioStreamPublish | 0 | 推流音频 |
| AoqAudioStreamPlayout | 1 | 播放音频 |

<a id="aoqaudioexternalstreamtoggle"></a>

<a id="c8a20055c656"></a>

<a id="7584f62a8236"></a>

#### AoqAudioExternalStreamToggle

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioExternalStreamToggleNormal | 0 | 恢复正常 |
| AoqAudioExternalStreamTogglePause | 1 | 暂停 |

> **说明**
>
> 该枚举已在头中声明，但**当前没有任何对外接口使用它**，属预留定义。

<a id="音频类型"></a>

<a id="3f73cd4ff816"></a>

<a id="f6812fd3ecd3"></a>

### 音频类型

<a id="aoqaudiocaptureconfig"></a>

<a id="ed6bbbc1f827"></a>

<a id="55191a7475de"></a>

#### AoqAudioCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isExternal | bool | false | 是否外部采集 |
| channel | int | 1 | 音频采集通道数，支持 1 / 2 |

<a id="aoqaudioplaybackconfig"></a>

<a id="db84758fe90a"></a>

<a id="0b30f197ac02"></a>

#### AoqAudioPlaybackConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isExternal | bool | false | 是否外部播放 |
| channel | int | 1 | 音频播放通道数，支持 1 / 2 |

<a id="aoqaudiocodecconfig"></a>

<a id="f111a93cf1f6"></a>

<a id="87b9f458d857"></a>

#### AoqAudioCodecConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeAudio | 轨道类型 |
| codecType | AoqEncoderType | AoqEncoderTypeAudioOpus | 编码类型 |
| sampleRate | int | 48000 | 采样率（Hz） |
| channel | int | 1 | 声道数，支持 1 / 2 |
| bitrate | int | 32000 | 码率（bps） |

采样率约束（摘自头文件注释）：

-   编码：Opus 支持 8 / 16 / 48K，PCM 支持 8 / 16 / 32 / 48K；
-   解码：额外支持 24K，但 **24K 仅限 Segment 模式**（Stream 模式不支持 24K）；
-   非法组合在 `connect` 时通过 `onError` 回调 `AoqECParamInvalid`。

<a id="aoqaudiodeviceroutetype"></a>

<a id="b188a3d64dfb"></a>

<a id="8638ddda03f1"></a>

#### AoqAudioDeviceRouteType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioDeviceRouteDefault | 0 | 默认路由 |
| AoqAudioDeviceRouteHeadset | 1 | 耳机 |
| AoqAudioDeviceRouteEarpiece | 2 | 听筒 |
| AoqAudioDeviceRouteHeadsetNoMic | 3 | 无麦耳机 |
| AoqAudioDeviceRouteSpeakerPhone | 4 | 内置扬声器 |
| AoqAudioDeviceRouteUsb | 5 | USB 音频设备 |
| AoqAudioDeviceRouteBluetooth | 6 | 蓝牙 |
| AoqAudioDeviceRouteBluetoothA2dp | 7 | 蓝牙 A2DP |

> **说明**
>
> 仅作为 `onAudioDeviceRouteChanged` 的 `routeType` 取值参照；Linux 不会触发该回调。

<a id="aoqaudiodevicestatecode"></a>

<a id="792c8d8f46c8"></a>

<a id="95bf5350f070"></a>

#### AoqAudioDeviceStateCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioDeviceNone | 0 | 无状态 |
| AoqAudioDeviceRecordStarting | 1 | 采集启动中 |
| AoqAudioDeviceRecordStarted | 2 | 采集已启动 |
| AoqAudioDeviceRecordStopping | 3 | 采集停止中 |
| AoqAudioDeviceRecordStopped | 4 | 采集已停止 |
| AoqAudioDeviceRecordFail | 5 | 采集失败 |
| AoqAudioDevicePlayStarting | 6 | 播放启动中 |
| AoqAudioDevicePlayStarted | 7 | 播放已启动 |
| AoqAudioDevicePlayStopping | 8 | 播放停止中 |
| AoqAudioDevicePlayStopped | 9 | 播放已停止 |
| AoqAudioDevicePlayFail | 10 | 播放失败 |

<a id="aoqaudiodevicestate"></a>

<a id="638a50d13925"></a>

<a id="1caa61af22ae"></a>

#### AoqAudioDeviceState

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| state | AoqAudioDeviceStateCode | AoqAudioDeviceNone | 设备操作状态 |
| reason | int | 0 | 错误原因代码（参考 AoqErrorCode） |

<a id="aoqaudioframedata"></a>

<a id="e23d82f21302"></a>

<a id="b5e4199178e2"></a>

#### AoqAudioFrameData

音频裸数据（既用于外部送流 `pushAudioExternalStreamData`，也用于 `IAudioFrameObserver` 回调）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| dataPtr | void\\\* | 0 | 音频 PCM 数据指针 |
| numOfSamples | int | 0 | 采样点数（单个声道） |
| bytesPerSample | int | 0 | 每个采样点的字节数 |
| numOfChannels | int | 0 | 声道数 |
| samplesPerSec | int | 0 | 每秒采样点数（采样率） |
| pushSequence | int | 0 | PCM 输入轮次（用于送流消费完成通知） |
| timeStamp | int64\_t | 0 | 时间戳 |
| dataSize | int | 0 | 数据长度（字节） |
| autoGenMute | bool | false | 仅回调时有效；true 表示 SDK 生成的静音数据 |

<a id="aoqaudiosource"></a>

<a id="2a77db2210f4"></a>

<a id="9db0077b90a2"></a>

#### AoqAudioSource

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioSourceCaptured | 0 | 采集的音频数据 |
| AoqAudioSourceProcessCaptured | 1 | 3A 后的音频数据 |
| AoqAudioSourcePublish | 2 | 推流的音频数据（需 connect 成功） |
| AoqAudioSourcePlayback | 3 | 播放的音频数据 |
| AoqAudioSourceMax | 4 | 占位，不要使用 |

<a id="aoqaudioobservermode"></a>

<a id="3ff6ff1b0ed2"></a>

<a id="8abf7987fbe2"></a>

#### AoqAudioObserverMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioObserverModeReadOnly | 0 | 只读模式 |
| AoqAudioObserverModeReadWrite | 1 | 读写模式 |

<a id="aoqaudioobserverconfig"></a>

<a id="1e93804760c0"></a>

<a id="b6dd11f9b536"></a>

#### AoqAudioObserverConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| sampleRate | int | 48000 | 回调音频采样率（Hz），与源不一致时重采样 |
| channels | int | 1 | 回调音频声道数，支持 1 / 2，受限拉流 Codec 参数 |
| mode | AoqAudioObserverMode | AoqAudioObserverModeReadOnly | 回调模式 |

采样率支持：8 / 12 / 16 / 24 / 32 / 44.1 / 48 / 64 / 88.2 / 96 / 176.4 / 192K。

<a id="aoqaudiovolumeindicationconfig"></a>

<a id="6b75ab69686c"></a>

<a id="2e47053efbf5"></a>

#### AoqAudioVolumeIndicationConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| reportSpeech | bool | false | 是否检测人声 |
| interval | int | 0 | 回调间隔（毫秒）；小于等于 0 表示关闭回调，大于 0 且小于 10 时按 10 处理 |
| smooth | int | 3 | 音量平滑系数，取值越大越平滑，取值范围 0-10 |

<a id="aoqaudiovolume"></a>

<a id="173ae81f4a84"></a>

<a id="a65ef6b8887f"></a>

#### AoqAudioVolume

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isSpeech | bool | false | 是否为人声 |
| volume | int | 0 | 平滑后的瞬时音量，取值范围 0-255 |

<a id="音频文件与外部音频流类型"></a>

<a id="f685bc747b45"></a>

<a id="53bfbbb8a76e"></a>

### 音频文件与外部音频流类型

<a id="aoqaudiofilemixconfig"></a>

<a id="5f1c56613a82"></a>

<a id="6d4a7c298a96"></a>

#### AoqAudioFileMixConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| fileName | const char\\\* | nullptr | 文件名（含路径） |
| cycles | int | \-1 | 循环次数，-1 表示无限循环 |
| startPosMs | long | 0 | 起始播放位置（毫秒） |
| publishVolume | int | 100 | 推流音量，取值范围 0-100 |
| playoutVolume | int | 100 | 播放音量，取值范围 0-100 |

> **说明**
>
> `fileId` 不在配置体内，作为 `startAudioFile` 的独立入参传入。

<a id="aoqaudiofilestatecode"></a>

<a id="17275ac65877"></a>

<a id="e49a79527418"></a>

#### AoqAudioFileStateCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioFileNone | 0 | 无状态 |
| AoqAudioFileStarted | 1 | 开始播放 |
| AoqAudioFileStopped | 2 | 停止播放 |
| AoqAudioFilePaused | 3 | 暂停播放 |
| AoqAudioFileResumed | 4 | 恢复播放 |
| AoqAudioFileEnded | 5 | 播放完毕 |
| AoqAudioFileBuffering | 6 | 正在缓冲 |
| AoqAudioFileBufferingEnd | 7 | 缓冲结束 |
| AoqAudioFileFailed | 8 | 播放失败 |

<a id="aoqaudiofileerrorcode"></a>

<a id="fed01d8ef3a7"></a>

<a id="5622cda71f66"></a>

#### AoqAudioFileErrorCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqAudioFileNoError | 0 | 没有错误 |
| AoqAudioFileOpenFailed | 1 | 打开文件失败 |
| AoqAudioFileDecodeFailed | 2 | 解码文件失败 |

<a id="aoqaudiofilestate"></a>

<a id="2d9436968f41"></a>

<a id="82b495ab4ca5"></a>

#### AoqAudioFileState

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| fileId | const char\\\* | nullptr | 文件 ID，仅回调期间有效 |
| stateCode | AoqAudioFileStateCode | AoqAudioFileNone | 文件状态码 |
| errorCode | AoqAudioFileErrorCode | AoqAudioFileNoError | 文件错误码 |

<a id="aoqaudioexternalstreamconfig"></a>

<a id="24ba60b98be9"></a>

<a id="f4414bef223f"></a>

#### AoqAudioExternalStreamConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| trackType | AoqTrackType | AoqTrackTypeAudio | 音频轨道类型 |
| codecType | AoqEncoderType | AoqEncoderTypeAudioPCM | 音频流格式，支持 PCM |
| channels | int | 1 | 声道数，受限推流音频 Codec（支持 1 / 2，超过的声道忽略） |
| sampleRate | int | 48000 | 采样率（Hz） |
| playoutVolume | int | 100 | 播放音量，取值范围 0-100 |
| publishVolume | int | 100 | 推流音量，取值范围 0-100 |
| maxBufferDuration | int | 600000 | 最大缓冲时长（毫秒，即 10 分钟），取值范围 100 以上；超过时 Push 失败 |
| enable3A | bool | false | 对输入 PCM 做 3A 处理（**Linux 不生效**） |

采样率支持：8 / 12 / 16 / 24 / 32 / 44.1 / 48 / 64 / 88.2 / 96 / 176.4 / 192K。

> **说明**
>
> `streamId` 不在配置体内，作为 `addAudioExternalStream` 的独立入参传入。

<a id="视频类型"></a>

<a id="4b5d759b5924"></a>

<a id="867ec95a6454"></a>

### 视频类型

<a id="aoqvideocanvas"></a>

<a id="9a8471b3387d"></a>

<a id="cccc21903d45"></a>

#### AoqVideoCanvas

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| view | void\\\* | nullptr | 平台原生视图句柄的不透明指针；传 nullptr 表示解绑 |
| renderMode | AoqRenderMode | AoqRenderModeAuto | 渲染填充模式 |

调用方需保证 `view` 生命周期长于 `setLocalView` / `setRemoteView` 设置期间。

> **说明**
>
> **Linux 无对应平台实现**，该结构在 Linux 上无实际用途。

<a id="aoqvideocaptureconfig"></a>

<a id="b842df2eefca"></a>

<a id="104bc99f0aef"></a>

#### AoqVideoCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| width | int | 1280 | 采集宽度（像素），isExternal=true 时无效 |
| height | int | 720 | 采集高度（像素），isExternal=true 时无效 |
| fps | int | 15 | 采集帧率，isExternal=true 时无效（节奏由送帧决定） |
| isExternal | bool | false | 是否外部采集；true 时不打开摄像头，由 pushExternalVideoCapturedFrame 喂帧 |

> **说明**
>
> Linux 上建议**始终置** `isExternal = true`。

<a id="aoqvideocodecconfig"></a>

<a id="d6a457544d1e"></a>

<a id="0293277c7007"></a>

#### AoqVideoCodecConfig

编码与解码共用同一结构。用于解码时仅 `trackType` / `codecType` / `width` / `height` / `fps` / `bitrate` 生效（作为订阅提议参与协商）；`minBitrate` / `keyframeInterval` / `mirrorMode` / `orientationMode` / `isExternal` 仅编码使用。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isExternal | bool | false | 外部编码模式；true 时由客户推送已编码帧，SDK 不做采集和编码 |
| trackType | AoqTrackType | AoqTrackTypeVideo | 轨道类型 |
| codecType | AoqEncoderType | AoqEncoderTypeVideoH264 | 编码类型 |
| width | int | 540 | 分辨率宽（像素） |
| height | int | 960 | 分辨率高（像素） |
| fps | int | 5 | 帧率 |
| bitrate | int | 500000 | 起始码率（bps） |
| minBitrate | int | 128000 | 最小码率（bps） |
| keyframeInterval | int | 2 | 关键帧间隔（秒） |
| mirrorMode | AoqMirrorMode | AoqMirrorModeDisabled | 镜像模式 |
| orientationMode | AoqOrientationMode | AoqOrientationModeAuto | 方向模式 |

<a id="aoqvideopixelformat"></a>

<a id="72d868fda36e"></a>

<a id="dcdb68475533"></a>

#### AoqVideoPixelFormat

| 枚举值 | 值 | 说明 | Linux 可用 |
| --- | --- | --- | --- |
| AoqVideoPixelFormatUnknown | 0 | 未知格式 | \- |
| AoqVideoPixelFormatI420 | 1 | I420（YUV 三平面） | 可用 |
| AoqVideoPixelFormatNV12 | 2 | NV12（YUV 半平面） | 可用 |
| AoqVideoPixelFormatNV21 | 3 | NV21（YUV 半平面） | 可用 |
| AoqVideoPixelFormatBGRA | 4 | BGRA（32 位） | 可用 |
| AoqVideoPixelFormatRGBA | 5 | RGBA（32 位） | 可用 |
| AoqVideoPixelFormatCVPixelBuffer | 6 | 仅 Apple 平台有效 | 不可用 |
| AoqVideoPixelFormatTextureOES | 7 | Android 外部 OES 纹理 | 不可用 |
| AoqVideoPixelFormatTexture2D | 8 | Android 普通 2D 纹理 | 不可用 |

> **说明**
>
> 枚举值 6/7/8 在头文件中仍可见（未被条件编译屏蔽），但 Linux 上无对应平台能力，传入会被当作不支持的格式处理。

<a id="aoqvideoframe"></a>

<a id="4d3a4cf2e3b6"></a>

<a id="240e2c8d5b17"></a>

#### AoqVideoFrame

外部视频裸帧（既用于 `pushExternalVideoCapturedFrame`，也用于 `IVideoFrameObserver` 回调）。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| format | AoqVideoPixelFormat | AoqVideoPixelFormatUnknown | 像素格式 |
| width | int | 0 | 宽度（像素） |
| height | int | 0 | 高度（像素） |
| dataPtr | void\\\* | 0 | 打包格式数据（NV12 / NV21 / BGRA / RGBA） |
| dataSize | int | 0 | 打包数据字节数 |
| dataY | void\\\* | 0 | I420 Y 平面 |
| dataU | void\\\* | 0 | I420 U 平面 |
| dataV | void\\\* | 0 | I420 V 平面 |
| strideY | int | 0 | Y 平面行跨度 |
| strideU | int | 0 | U 平面行跨度 |
| strideV | int | 0 | V 平面行跨度 |
| nativePixelBuffer | void\\\* | 0 | Apple 零拷贝用（CVPixelBufferRef），Linux 不使用 |
| textureId | int | 0 | Android 纹理 ID，Linux 不使用 |
| transformMatrix | float数组（16元素） | 全 0 | 纹理变换矩阵（行优先 4x4），Linux 不使用 |
| timeStamp | int64\_t | 0 | 时间戳（毫秒）；0 时 SDK 用本地时间补齐 |

<a id="aoqvideocodectype"></a>

<a id="a06a3c2f0834"></a>

<a id="fd276d4a663a"></a>

#### AoqVideoCodecType

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqVideoCodecTypeJPEG | 0 | JPEG 编码 |

<a id="aoqvideoencodedframe"></a>

<a id="6ceb40df424f"></a>

<a id="ffa6a3b6aa5a"></a>

#### AoqVideoEncodedFrame

外部已编码视频帧。调用方自行完成编码，SDK 不做二次编码，直接打包发送。

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| codec | AoqVideoCodecType | AoqVideoCodecTypeJPEG | 编码格式 |
| data | void\\\* | nullptr | 编码后数据指针 |
| dataSize | int | 0 | 编码后数据字节数 |
| width | int | 0 | 宽度（像素） |
| height | int | 0 | 高度（像素） |
| timeStamp | int64\_t | 0 | 时间戳（毫秒）；0 时 SDK 用本地时间补齐 |

<a id="aoqvideodevicestatecode"></a>

<a id="2a6677c5dcc5"></a>

<a id="dbb0628b6432"></a>

#### AoqVideoDeviceStateCode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqVideoDeviceNone | 0 | 无状态 |
| AoqVideoDeviceCaptureStarting | 1 | 摄像头正在启动 |
| AoqVideoDeviceCaptureStarted | 2 | 摄像头已启动 |
| AoqVideoDeviceCaptureStopping | 3 | 摄像头正在停止 |
| AoqVideoDeviceCaptureStopped | 4 | 摄像头已停止 |
| AoqVideoDeviceCaptureFail | 5 | 摄像头启动失败（权限拒绝、设备不可用等） |

<a id="aoqvideodevicestate"></a>

<a id="49ff78d36033"></a>

<a id="5692337c65cf"></a>

#### AoqVideoDeviceState

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| state | AoqVideoDeviceStateCode | AoqVideoDeviceNone | 设备采集操作状态 |
| reason | int | 0 | 错误原因代码（参考 AoqErrorCode） |

<a id="aoqvideosource"></a>

<a id="fbf91acaeb69"></a>

<a id="1be6cfae7031"></a>

#### AoqVideoSource

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqVideoSourceCaptured | 0 | 采集后的视频数据（前处理前） |
| AoqVideoSourcePreEncode | 1 | 编码前的视频数据（前处理后） |
| AoqVideoSourceRemote | 2 | 远端解码后、渲染前的视频数据 |
| AoqVideoSourceMax | 3 | 占位，不要使用 |

<a id="aoqvideoobservermode"></a>

<a id="9896a263e5d5"></a>

<a id="8c1330861bd2"></a>

#### AoqVideoObserverMode

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqVideoObserverModeReadOnly | 0 | 只读模式 |
| AoqVideoObserverModeReadWrite | 1 | 读写模式（仅 I420 / CVPixelBuffer 支持） |

<a id="aoqvideoobserveralignment"></a>

<a id="01e57e6123e1"></a>

<a id="fadecb923b1b"></a>

#### AoqVideoObserverAlignment

| 枚举值 | 值 | 说明 |
| --- | --- | --- |
| AoqVideoObserverAlignmentDefault | 0 | 默认对齐 |
| AoqVideoObserverAlignmentEven | 1 | 偶数对齐 |
| AoqVideoObserverAlignment4 | 2 | 4 字节对齐 |
| AoqVideoObserverAlignment8 | 3 | 8 字节对齐 |
| AoqVideoObserverAlignment16 | 4 | 16 字节对齐 |

<a id="aoqvideoobserverconfig"></a>

<a id="91c7859714bb"></a>

<a id="52c609e9f333"></a>

#### AoqVideoObserverConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| format | AoqVideoPixelFormat | AoqVideoPixelFormatI420 | 期望回调像素格式 |
| alignment | AoqVideoObserverAlignment | AoqVideoObserverAlignmentDefault | 宽度对齐策略 |
| mode | AoqVideoObserverMode | AoqVideoObserverModeReadOnly | 回调模式，仅 I420 / CVPixelBuffer 支持 ReadWrite |
| mirrorApplied | bool | false | 是否对回调数据应用镜像 |
| trackType | AoqTrackType | AoqTrackTypeVideo | 需要观察的视频轨道；仅支持 Video / Screen。 |

<a id="屏幕采集类型"></a>

### 屏幕采集类型

<a id="aoqscreencaptureconfig"></a>

#### AoqScreenCaptureConfig

| 字段 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| isExternal | bool | false | Linux 必须设置为 true，由应用采集屏幕并输入原始帧。 |
| appGroup | const char\* | nullptr | iOS 专用，本平台不使用。 |

全部类型定义于 `AoqClientEngine.h`，命名空间 `AoqClientSdk`。结构体均为 POD 并带默认值，直接声明即可获得表中默认值。字段是否在 Linux 下存在及适用范围，以各结构体的说明为准。`AoqScreenCaptureConfig.appGroup` 保留在结构体中，但仅供 iOS 使用；`sourceId` 和 `sourceType` 则在 Linux 下被条件编译屏蔽，不存在于结构体中。

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
