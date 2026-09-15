# AOQ Client SDK Electron API 参考

本文介绍 AOQ Client SDK Electron 版的 TypeScript 接口、事件和数据类型。该 SDK 适用于 macOS x64/arm64 和 Windows x64，要求 Node.js 16 或更高版本。

**说明**适用包：`aoq-electron-sdk`（npm）。支持平台：macOS（x64 / arm64）、Windows x64；Node.js >= 16。

## 接口目录

### 引擎入口与生命周期

**接口**

**简介**

createAoqClientEngine

获取引擎包装实例（模块级懒加载单例）

createEngine

创建 native 引擎实例

destroy

销毁引擎实例

getVersion

获取 SDK 版本号

connect

连接 Relay 服务器

disconnect

断开服务器连接

### 音频设备管理

**接口**

**简介**

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

### 音频编解码配置

**接口**

**简介**

setAudioEncoderConfig

设置音频编码参数

setAudioDecoderConfig

设置音频解码参数

### 视频设备管理

**接口**

**简介**

startVideoCapture

打开视频采集设备（摄像头）

stopVideoCapture

关闭视频采集设备

### 视频编解码与外部输入

**接口**

**简介**

setVideoEncoderConfig

设置视频编码参数

setVideoDecoderConfig

设置视频解码参数

pushExternalVideoCapturedFrame

推送外部采集视频帧

pushExternalVideoEncodedFrame

推送外部已编码视频帧

### 媒体流发送控制

**接口**

**简介**

enableSendMediaStream

控制本地媒体流的发送开关

### 音频文件播放

**接口**

**简介**

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

**接口**

**简介**

addAudioExternalStream

新增一条外部音频流

removeAudioExternalStream

移除外部音频流

pushAudioExternalStreamData

输入外部音频 PCM 数据

setAudioExternalStreamVolume

设置外部音频流音量

getAudioExternalStreamVolume

获取外部音频流音量

clearAudioExternalStreamBuffer

清空外部音频流缓存

### 实时消息

**接口**

**简介**

sendDataMsg

发送实时数据消息

### 音频帧回调

**接口**

**简介**

setAudioFrameObserver

开启或关闭音频帧数据观察者

enableAudioFrameObserver

开启或关闭指定位置的音频帧回调

### 本地音量提示

**接口**

**简介**

enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示回调

### 视频帧回调

**接口**

**简介**

setVideoFrameObserver

开启或关闭视频帧数据观察者

enableVideoFrameObserver

开启或关闭指定位置的视频帧回调

### 视频渲染（YUVCanvasRenderer）

**接口**

**简介**

bind

绑定 canvas 元素

unbind

解绑并清空画面

bound

查询当前是否已绑定

drawFrame

绘制一帧 I420 视频数据

### 引擎事件（IAoqEngineEvents）

**事件**

**简介**

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

onAudioFileState

音频文件播放状态回调

onLocalAudioVolumeIndication

本地采集音量提示回调

onVideoDeviceStateChanged

视频设备操作状态变化回调

onDataMsg

收到实时数据消息回调

onCapturedAudioFrame

采集裸音频数据回调

onProcessCapturedAudioFrame

3A 处理后音频数据回调

onPublishAudioFrame

推流音频数据回调

onPlaybackAudioFrame

播放音频数据回调

onCapturedVideoFrame

本地采集后裸视频数据回调

onPreEncodeVideoFrame

本地编码前裸视频数据回调

onRemoteVideoFrame

远端解码后、渲染前视频数据回调

## 接口详情

### 引擎入口与生命周期

#### createAoqClientEngine

获取引擎包装实例。模块级懒加载单例，重复调用返回同一实例，与 native 引擎单例语义对齐；也是包的 default export。

```
import createAoqClientEngine from 'aoq-electron-sdk';
export function createAoqClientEngine(): IAoqClientEngine
```

返回值：`IAoqClientEngine` 引擎实例。注意本方法仅创建 JS 包装层与 native bridge，真正创建引擎需再调 `createEngine()`。

#### createEngine

创建 native 引擎实例。引擎为全局单例，重复调用直接返回成功。

```
createEngine(config: AoqCreateConfig): number
```

**参数**

**类型**

**说明**

config

AoqCreateConfig

引擎创建配置

返回值：`0` 成功；`-1` 表示创建失败或参数不是合法 JSON。

**说明**Windows 上 `createEngine()` 会在当前 JS 线程的 libuv 循环上挂一个 16ms 的 Win32 消息泵（摄像头采集依赖），`destroy()` 时停掉；因此不要在 `createEngine()` 之后长时间同步阻塞 JS 线程。

#### destroy

销毁引擎实例，释放所有资源。

```
destroy(): number
```

返回值：`0` 表示成功；非 `0` 表示失败。引擎未创建时返回 `0`。

#### getVersion

获取 SDK 当前版本号，无需先调 `createEngine()`。

```
getVersion(): string
```

返回值：版本号字符串，如 "1.2.0"；取不到时返回空字符串。

#### connect

连接 Relay 服务器。业务 AppServer 应根据所用协议获取临时 AOQ 连接参数并下发给客户端，具体操作请参见Token 鉴权。

```
connect(config: AoqConnectConfig): number
```

**参数**

**类型**

**说明**

config

AoqConnectConfig

连接配置，包含 Token、SID、Relay 接入点列表、推拉流 track 列表等

返回值：`0` 表示调用已下发（异步执行）；非 `0` 表示参数校验失败。连接结果由 `onConnectionStatusChange` 事件通知。

#### disconnect

断开与服务器的连接，释放连接相关资源。

```
disconnect(): number
```

返回值：`0` 表示调用已下发（异步执行）；非 `0` 表示失败。

### 音频设备管理

#### startAudioCapture

```
startAudioCapture(config: AoqAudioCaptureConfig): number
```

打开音频采集设备（麦克风）。首次采集会触发系统授权，macOS 需在应用 `Info.plist` 中声明 `NSMicrophoneUsageDescription`。

#### stopAudioCapture

```
stopAudioCapture(): number
```

关闭音频采集设备。

#### muteAudioCapture

```
muteAudioCapture(mute: boolean): number
```

静音或取消静音音频采集。`mute=true` 静音，`false` 取消静音。

#### startAudioPlayer

```
startAudioPlayer(config: AoqAudioPlaybackConfig): number
```

开始音频渲染（播放远端音频）。

#### stopAudioPlayer / pauseAudioPlayer / resumeAudioPlayer

```
stopAudioPlayer(): number
pauseAudioPlayer(fadeMs: number): number
resumeAudioPlayer(fadeMs: number): number
```

`fadeMs`：淡出/淡入时长（毫秒）；`0` 表示立即执行。

#### interruptAudioPlayer

```
interruptAudioPlayer(trackType: AoqTrackType, fadeMs: number): number
```

打断本轮音频通话，丢弃已缓存的本轮下行数据。

**参数**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

fadeMs

number

淡出时长（毫秒）

### 音频编解码配置

```
setAudioEncoderConfig(config: AoqAudioCodecConfig): number
setAudioDecoderConfig(config: AoqAudioCodecConfig): number
```

建议在 `connect()` 之前调用。使用 Opus（`AoqEncoderTypeAudioOpus`）需 SDK 内置或随包分发 PluginOpus 插件。

### 视频设备管理

```
startVideoCapture(config: AoqVideoCaptureConfig): number
stopVideoCapture(): number
```

打开/关闭视频采集设备。macOS 需在 `Info.plist` 中声明 `NSCameraUsageDescription`。当 `config.isExternal=true` 时不打开摄像头，由 `pushExternalVideoCapturedFrame` 送帧。

**说明**Electron renderer 为 Chromium 环境，无法嵌入原生视图，因此未提供 `setLocalView / setRemoteView / switchCamera`；预览请使用「帧观察者 + YUVCanvasRenderer」（见 2.13）。

### 视频编解码与外部输入

```
setVideoEncoderConfig(config: AoqVideoCodecConfig): number
setVideoDecoderConfig(config: AoqVideoCodecConfig): number
pushExternalVideoCapturedFrame(meta: AoqExternalVideoFrameMeta, buffer: Uint8Array): number
pushExternalVideoEncodedFrame(meta: AoqExternalVideoEncodedFrameMeta, buffer: Uint8Array): number
```

**参数**

**类型**

**说明**

meta

AoqExternalVideoFrameMeta / AoqExternalVideoEncodedFrameMeta

帧元信息（尺寸、格式、时间戳）

buffer

Uint8Array

帧数据（像素数据或已编码数据）

注意：

-   `pushExternalVideoCapturedFrame` 仅在 `startVideoCapture({ isExternal: true })` 后被消费；未开启时返回 `211`，缓冲区满时返回 `210`。
-   支持 `AoqVideoPixelFormatI420` 与打包格式（NV12 / NV21 / BGRA / RGBA）；I420 时 `buffer` 必须为紧凑布局（stride = width），Y / U / V 三平面顺序拼接。
-   `pushExternalVideoEncodedFrame` 需先 `setVideoEncoderConfig({ isExternal: true })`；未开启时返回 `212`。当前仅支持 JPEG。
-   `meta.timeStamp` 为 `0` 时由 SDK 使用本地时间补齐。

### 媒体流发送控制

```
enableSendMediaStream(trackType: AoqTrackType, enable: boolean): number
```

控制本地某路媒体流是否发送。建议初始化后先 `enableSendMediaStream(trackType, false)`，待 `onConnectionStatusChange` 上报 `AoqConnectionStatusConnected` 后再开启。

### 音频文件播放

```
startAudioFile(config: AoqAudioFileMixConfig): number
stopAudioFile(fileId: string): number
pauseAudioFile(fileId: string): number
resumeAudioFile(fileId: string): number
getAudioFileDuration(fileId: string): number
getAudioFileCurrentPosition(fileId: string): number
setAudioFilePositionMillis(fileId: string, positionMs: number): number
setAudioFileVolume(fileId: string, type: AoqAudioStreamDirection, volume: number): number
getAudioFileVolume(fileId: string, type: AoqAudioStreamDirection): number
```

**参数**

**类型**

**说明**

config

AoqAudioFileMixConfig

文件混音配置，`fileId` 作为配置字段携带

fileId

string

文件标识，由调用方定义，后续接口以此定位

positionMs

number

目标播放位置（毫秒）

type

AoqAudioStreamDirection

推流音量或本地播放音量

volume

number

音量，取值范围 0-100

返回值说明：

-   `getAudioFileDuration` / `getAudioFileCurrentPosition` 返回毫秒数；
-   `getAudioFileVolume` 返回当前音量值；
-   上述 getter 在引擎未创建时返回 `-1`。

播放状态变化通过 `onAudioFileState` 事件上报。

### 外部音频流

```
addAudioExternalStream(config: AoqAudioExternalStreamConfig): number
removeAudioExternalStream(streamId: string): number
pushAudioExternalStreamData(meta: AoqAudioExternalFrameMeta, buffer: Uint8Array): number
setAudioExternalStreamVolume(streamId: string, type: AoqAudioStreamDirection, volume: number): number
getAudioExternalStreamVolume(streamId: string, type: AoqAudioStreamDirection): number
clearAudioExternalStreamBuffer(streamId: string, fadeoutMs: number): number
```

**参数**

**类型**

**说明**

config

AoqAudioExternalStreamConfig

外部音频流配置，`streamId` 作为配置字段携带

streamId

string

流标识，由调用方定义

meta

AoqAudioExternalFrameMeta

PCM 帧元信息，`streamId` 作为元信息字段携带

buffer

Uint8Array

PCM 数据

fadeoutMs

number

清空缓存时的淡出时长（毫秒）

注意：

-   `pushAudioExternalStreamData` 缓存时长超过 `maxBufferDuration` 时返回 `110`（外部音频缓冲区满）。
-   `getAudioExternalStreamVolume` 返回当前音量值；引擎未创建时返回 `-1`。
-   `clearAudioExternalStreamBuffer` native 侧无返回值，调用成功固定返回 `0`。

### 实时消息

```
sendDataMsg(data: Uint8Array | string): number
```

发送实时数据消息。传入 `string` 时内部按 UTF-8 编码为 `Buffer` 后发送。对端消息通过 `onDataMsg` 事件回调。

### 音频帧回调

```
setAudioFrameObserver(enable: boolean): number
enableAudioFrameObserver(params: AoqAudioObserverParams): number
```

**参数**

**类型**

**说明**

enable

boolean

`true` 注册内置音频帧观察者，`false` 注销

params

AoqAudioObserverParams

指定回调位置、开关与回调格式

使用步骤：先 `setAudioFrameObserver(true)` 注册观察者，再对需要的位置调 `enableAudioFrameObserver`，数据通过对应事件下发。

```
engine.setAudioFrameObserver(true)
engine.enableAudioFrameObserver({
  enabled: true,
  audioSource: AoqAudioSource.AoqAudioSourceCaptured,
  sampleRate: 48000,
  channels: 1
})
engine.on('onCapturedAudioFrame', (frame) => { /* frame.buffer 为 PCM 数据 */ })
```

**说明**Electron 侧帧观察者仅支持**只读**模式，回调中不支持回写帧数据（native 内部固定 `ReadOnly`）。

### 本地音量提示

```
enableLocalAudioVolumeIndication(config: AoqAudioVolumeIndicationConfig): number
```

开启/关闭本地采集音量提示。`config.interval <= 0` 时关闭回调；开启后按 `config.interval` 周期触发 `onLocalAudioVolumeIndication`。需在 `startAudioCapture()` 之后调用才有音量数据。

### 视频帧回调

```
setVideoFrameObserver(enable: boolean): number
enableVideoFrameObserver(params: AoqVideoObserverParams): number
```

**参数**

**类型**

**说明**

enable

boolean

`true` 注册内置视频帧观察者，`false` 注销

params

AoqVideoObserverParams

指定回调位置、开关、像素格式与对齐策略

回调数据以 `AoqVideoFrameEvent` 形式通过 `onCapturedVideoFrame` / `onPreEncodeVideoFrame` / `onRemoteVideoFrame` 下发；I420 时 `buffer` 为 Y / U / V 三平面按 stride 拼接，其余打包格式为原数据透传。同样仅支持只读模式。

### 视频渲染（YUVCanvasRenderer）

SDK 内置的软渲染器，承担移动端 `setLocalView / setRemoteView` 的预览职责。

```
import { YUVCanvasRenderer } from 'aoq-electron-sdk';

class YUVCanvasRenderer {
  bind(canvas: HTMLCanvasElement): void
  unbind(): void
  get bound(): boolean
  drawFrame(frame: AoqVideoFrameEvent): void
}
```

**接口**

**说明**

bind

绑定 canvas（重复绑定会替换 sink）

unbind

解绑并清空画面

bound

是否已绑定

drawFrame

绘制一帧；仅支持 I420，非 I420 / 尺寸或 buffer 长度不足时静默返回

```
const renderer = new YUVCanvasRenderer()
renderer.bind(document.getElementById('preview'))

engine.setVideoFrameObserver(true)
engine.enableVideoFrameObserver({
  enabled: true,
  videoSource: AoqVideoSource.AoqVideoSourceCaptured,
  format: AoqVideoPixelFormat.AoqVideoPixelFormatI420
})
engine.on('onCapturedVideoFrame', (frame) => renderer.drawFrame(frame))
```

渲染填充模式（拉伸 / 裁剪等）用 CSS `object-fit` 控制 canvas 即可。

### 引擎事件（IAoqEngineEvents）

引擎继承 `EventEmitter<IAoqEngineEvents>`，事件是 SDK 所有异步通知的统一出口，与 native `AoqEngineEventListener` 回调一一对应。不关心的事件无需注册。

```
engine.on('onError', (code, message) => {})
engine.off('onError', handler)
engine.once('onStats', (stats) => {})
engine.removeAllListeners()
```

#### onError

```
onError: (code: number, message: string) => void
```

引擎错误回调。`code` 对应 AoqErrorCode 数值（见 3.3）。

#### onWarning

```
onWarning: (code: number, message: string) => void
```

引擎警告回调。`code` 对应 AoqWarningCode 数值（见 3.3）。

#### onConnectionStatusChange

```
onConnectionStatusChange: (status: AoqConnectionStatus) => void
```

连接状态变化回调。状态流转：Disconnected -> Connecting -> Connected / Failed -> Disconnected。

#### onStats

```
onStats: (stats: AoqStats) => void
```

引擎统计信息回调。SDK 周期性上报音视频推拉流及网络统计数据，可用于实时监测通话质量、网络状态、诊断音视频问题。

**参数**

**类型**

**说明**

stats

AoqStats

包含音频 / 视频 / 数据消息的推拉流统计及网络统计

#### onAudioDeviceStateChanged

```
onAudioDeviceStateChanged: (state: AoqAudioDeviceState) => void
```

音频设备采集 / 播放操作状态变化回调。

#### onAudioDeviceRouteChanged

```
onAudioDeviceRouteChanged: (routeType: number) => void
```

音频输出路由变化回调。`routeType` 对应 AoqAudioDeviceRouteType 数值（见 3.4）。

#### onAudioFileState

```
onAudioFileState: (state: AoqAudioFileState) => void
```

音频文件播放状态回调。

#### onLocalAudioVolumeIndication

```
onLocalAudioVolumeIndication: (volume: AoqAudioVolume) => void
```

本地采集音量提示回调，需调用 `enableLocalAudioVolumeIndication` 开启。

#### onVideoDeviceStateChanged

```
onVideoDeviceStateChanged: (state: AoqVideoDeviceState) => void
```

视频设备采集操作状态变化回调。

#### onDataMsg

```
onDataMsg: (data: Uint8Array) => void
```

收到实时数据消息回调。`data` 为 native 侧拷贝后的 `Buffer`，可安全异步持有；文本消息用 `Buffer.from(data).toString()` 转字符串。

#### 音频帧事件

```
onCapturedAudioFrame:        (frame: AoqAudioFrameEvent) => void  /* 采集裸数据 */
onProcessCapturedAudioFrame: (frame: AoqAudioFrameEvent) => void  /* 3A 后数据 */
onPublishAudioFrame:         (frame: AoqAudioFrameEvent) => void  /* 推流数据 */
onPlaybackAudioFrame:        (frame: AoqAudioFrameEvent) => void  /* 播放数据 */
```

需先调 `setAudioFrameObserver(true)` 与 `enableAudioFrameObserver` 开启。

#### 视频帧事件

```
onCapturedVideoFrame:  (frame: AoqVideoFrameEvent) => void  /* 采集后（前处理前） */
onPreEncodeVideoFrame: (frame: AoqVideoFrameEvent) => void  /* 编码前（前处理后） */
onRemoteVideoFrame:    (frame: AoqVideoFrameEvent) => void  /* 远端解码后、渲染前 */
```

需先调 `setVideoFrameObserver(true)` 与 `enableVideoFrameObserver` 开启。帧事件为只读，回调中修改 `buffer` 不会写回 SDK。

**说明**事件回调中避免重计算：native 回调经异步线程投递到 JS 主线程，高频帧事件中做耗时操作会造成堆积。

## 数据类型与枚举

所有类型均从包根导出，可直接 `import { ... } from 'aoq-electron-sdk'`。枚举为 TypeScript `enum`，运行时可用；接口（`interface`）仅类型约束。标记为可选的字段缺省时取表中默认值。

### 通用类型

#### AoqCreateConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

workDir

string

否

""

SDK 工作目录（日志与临时文件）

enableDumpAudio

boolean

否

false

是否开启音频数据保存（调试用）

extras

string

否

""

扩展参数（JSON 字符串）

**说明**Android 的 `isBTScoMode` 为移动端字段，Electron 不提供。

#### AoqConnectConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

token

string

是

\-

连接鉴权 Token

sid

string

是

\-

会话 ID

certFingerprint

string

否

""

服务器证书指纹

workspaceIdHash

string

否

空

工作空间 ID Hash；空字符串等同不传

relayEndpoints

Array

是

\-

Relay 接入点列表

publishTracks

Array

是

\-

本端发布轨道列表

subscribeTracks

Array

是

\-

本端订阅轨道列表

#### AoqRelayEndpoint

**字段**

**类型**

**必填**

**默认值**

**说明**

routeIndex

number

否

\-1

路由序号

endpoint

string

是

\-

Relay 服务器域名或 IP

port

number

是

\-

Relay 服务器端口

#### AoqTrackParam

**字段**

**类型**

**必填**

**默认值**

**说明**

trackType

AoqTrackType

是

\-

轨道类型

trackMode

AoqTrackMode

否

AoqTrackModeSegment

流式 / 非流式模式，仅对音频下行生效

### 统计信息类型

#### AoqStats

引擎统计信息汇总，通过 `onStats` 周期性上报。数组字段无数据时为空数组，`networkStats` 无数据时不下发。

**字段**

**类型**

**说明**

audioPublishStats

Array

音频推流统计

videoPublishStats

Array

视频推流统计

dataMsgPublishStats

Array

数据消息推流统计

audioSubscribeStats

Array

音频拉流统计

videoSubscribeStats

Array

视频拉流统计

dataMsgSubscribeStats

Array

数据消息拉流统计

networkStats

AoqNetworkStats

网络统计信息

#### AoqAudioPublishStats

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

bitrate

number

码率（bps）

bytes

number

累计发送字节数

encodeVolume

number

推流编码音量

#### AoqAudioSubscribeStats

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

bitrate

number

码率（bps）

bytes

number

累计接收字节数

playVolume

number

播放音量

#### AoqVideoPublishStats

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

bitrate

number

码率（bps）

bytes

number

累计发送字节数

encodeFps

number

编码帧率

#### AoqVideoSubscribeStats

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

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

#### AoqDataMsgPublishStats / AoqDataMsgSubscribeStats

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

bitrate

number

码率（bps）

bytes

number

累计发送 / 接收字节数

#### AoqNetworkStats

**字段**

**类型**

**说明**

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

### 枚举类型

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

#### AoqTrackMode

**枚举值**

**值**

**说明**

AoqTrackModeSegment

0

分段：数据按语义片段（如一句话）打包送达

AoqTrackModeStream

1

流式：数据持续、连续地送达

#### AoqEncoderType

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

音频 Opus（插件化，需 PluginOpus）

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

**枚举值**

**值**

**说明**

AoqMirrorModeDisabled

0

关闭镜像

AoqMirrorModeEnabled

1

开启镜像

#### AoqOrientationMode

**枚举值**

**值**

**说明**

AoqOrientationModeAuto

0

自动适应

AoqOrientationModePortrait

1

竖屏

AoqOrientationModeLandscape

2

横屏

#### AoqErrorCode

错误码为 native 层定义，`onError` 的 `code` 与接口返回值均使用该数值（TS 层未将其导出为 `enum`）。

**枚举值**

**值**

**说明**

AoqErrorCodeOK

0

成功

AoqErrorCodeParamInvalid

1

参数非法

AoqErrorCodeStateInvalid

2

状态非法

AoqErrorCodeUnSupport

3

当前平台 / 模式不支持

AoqErrorCodeAudio

100

音频通用错误

AoqErrorCodeAudioExternalBufferFull

110

外部音频缓冲区满

AoqErrorCodeAudioDevice

120

音频设备通用错误

AoqErrorCodeAudioDeviceRecordingAuthFailed

121

录音权限未获取

AoqErrorCodeAudioDeviceRecordingOccupied

122

录音设备被占用

AoqErrorCodeAudioDeviceRecordingBackgroundStart

123

后台启动录音失败

AoqErrorCodeAudioDeviceRecordingStartFail

124

录音启动失败

AoqErrorCodeAudioDevicePlayoutOccupied

125

播放设备被占用

AoqErrorCodeAudioDevicePlayoutBackgroundStart

126

后台启动播放失败

AoqErrorCodeAudioDevicePlayoutStartFail

127

播放启动失败

AoqErrorCodeVideo

200

视频通用错误

AoqErrorCodeVideoExternalBufferFull

210

外部视频缓冲区满

AoqErrorCodeVideoExternalCaptureNotEnabled

211

外部视频采集未启用

AoqErrorCodeVideoExternalEncoderNotEnabled

212

外部视频编码未启用

AoqErrorCodeVideoDevice

220

视频设备通用错误

AoqErrorCodeVideoDeviceCameraOpenFail

221

摄像头打开失败

AoqErrorCodeVideoDeviceCameraAuthFailed

222

摄像头权限未获取

AoqErrorCodeVideoDeviceCameraOccupied

223

摄像头被占用

AoqErrorCodeVideoDeviceCameraRunningError

224

摄像头运行异常

AoqErrorCodeVideoCodec

230

视频编解码通用错误

AoqErrorCodeVideoCodecEncoderInitFail

231

视频编码器初始化失败

AoqErrorCodeVideoRender

240

视频渲染通用错误

AoqErrorCodeVideoRenderCreateFail

241

视频渲染创建失败

AoqErrorCodeVideoRenderDrawError

242

视频渲染绘制错误

**说明**除上述 native 错误码外，Electron 层还会在引擎未创建 / 已销毁、或参数不是合法 JSON 时返回 `-1`。

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

### 音频类型

#### AoqAudioCaptureConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

isExternal

boolean

否

false

是否为外部采集模式

channel

number

否

1

音频采集通道数，支持 1 / 2

#### AoqAudioPlaybackConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

isExternal

boolean

否

false

是否为外部播放模式

channel

number

否

1

音频播放通道数，支持 1 / 2

**说明**`isVoipMode` / `isDefaultSpeaker` 为移动端字段，Electron 不提供。

#### AoqAudioCodecConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

trackType

AoqTrackType

否

AoqTrackTypeAudio

轨道类型

codecType

AoqEncoderType

否

AoqEncoderTypeAudioPCM

编码格式

sampleRate

number

否

48000

采样率（Hz）。编码支持 Opus 8/16/48K、PCM 8/16/32/48K；解码额外支持 24K（仅 Segment 模式）

channel

number

否

1

声道数，支持 1 / 2

bitrate

number

否

32000

比特率（bps）

#### AoqAudioDeviceRouteType

`onAudioDeviceRouteChanged` 的 `routeType` 取值（native 定义，TS 层未导出为 `enum`）。

**枚举值**

**值**

**说明**

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

#### AoqAudioDeviceStateCode

**枚举值**

**值**

**说明**

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

**字段**

**类型**

**说明**

state

AoqAudioDeviceStateCode

设备操作状态

reason

number

错误原因代码（参考 AoqErrorCode）

### 音频文件类型

#### AoqAudioFileMixConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

fileId

string

是

\-

文件标识符，后续接口以此定位

fileName

string

是

\-

文件名（含路径）

cycles

number

否

\-1

循环次数，-1 表示无限循环

startPosMs

number

否

0

起始播放位置（毫秒）

publishVolume

number

否

100

推流音量，取值范围 0-100

playoutVolume

number

否

100

播放音量，取值范围 0-100

#### AoqAudioFileStateCode

**枚举值**

**值**

**说明**

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

`AoqAudioFileState.errorCode` 的取值（native 定义，TS 层作为 `number` 下发）。

**枚举值**

**值**

**说明**

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

**字段**

**类型**

**说明**

fileId

string

文件标识符

stateCode

AoqAudioFileStateCode

文件播放状态码

errorCode

number

文件错误码（参考 AoqAudioFileErrorCode）

### 外部音频流类型

#### AoqAudioStreamDirection

**枚举值**

**值**

**说明**

AoqAudioStreamPublish

0

发布流（推流）

AoqAudioStreamPlayout

1

播放流（本地播放）

#### AoqAudioExternalStreamConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

streamId

string

是

\-

流标识符

trackType

AoqTrackType

否

AoqTrackTypeAudio

音频轨道类型

codecType

AoqEncoderType

否

AoqEncoderTypeAudioPCM

音频流格式，当前支持 PCM

channels

number

否

1

声道数，受限推流 Codec，支持 1 / 2

sampleRate

number

否

48000

采样率（Hz），支持 8/12/16/24/32/44.1/48/64/88.2/96/176.4/192K

playoutVolume

number

否

100

播放音量，取值范围 0-100

publishVolume

number

否

100

推流音量，取值范围 0-100

maxBufferDuration

number

否

600000

最大缓冲时长（毫秒），取值范围 100 以上；超过时 push 失败

enable3A

boolean

否

false

是否对输入 PCM 做 3A 处理

#### AoqAudioExternalFrameMeta

外部音频帧元信息，PCM 数据另走 `buffer` 参数。

**字段**

**类型**

**必填**

**默认值**

**说明**

streamId

string

是

\-

目标外部音频流标识

numOfSamples

number

是

0

采样点数（单声道）

bytesPerSample

number

是

2

每个采样点的字节数

numOfChannels

number

是

1

声道数

samplesPerSec

number

是

48000

每秒采样点数（采样率）

pushSequence

number

否

0

PCM 输入轮次

timeStamp

number

否

0

时间戳

#### AoqAudioFrameEvent

音频帧观察者事件数据。

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

numOfSamples

number

采样点数（单声道）

bytesPerSample

number

每个采样点的字节数

numOfChannels

number

声道数

samplesPerSec

number

每秒采样点数（采样率）

timeStamp

number

时间戳

autoGenMute

boolean

true 表示 SDK 生成的静音数据

buffer

Uint8Array

音频 PCM 数据（native 侧已拷贝）

#### AoqAudioSource

**枚举值**

**值**

**说明**

AoqAudioSourceCaptured

0

采集的音频数据

AoqAudioSourceProcessCaptured

1

3A 处理后的音频数据

AoqAudioSourcePublish

2

推流的音频数据（需 connect 成功）

AoqAudioSourcePlayback

3

播放的音频数据

#### AoqAudioObserverParams

**字段**

**类型**

**必填**

**默认值**

**说明**

enabled

boolean

是

false

开启或关闭该位置的回调

audioSource

AoqAudioSource

是

AoqAudioSourceCaptured

回调位置

sampleRate

number

否

48000

回调音频采样率（Hz），不一致时重采样

channels

number

否

1

回调音频声道数，支持 1 / 2

**说明**回调模式固定为只读，Electron 不开放读写模式。

#### AoqAudioVolumeIndicationConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

interval

number

否

0

回调间隔（毫秒）；小于等于 0 表示关闭回调，大于 0 且小于 10 时按 10 处理

smooth

number

否

3

音量平滑系数，取值越大越平滑，取值范围 0-10

#### AoqAudioVolume

**字段**

**类型**

**说明**

volume

number

平滑后的瞬时音量，取值范围 0-255

### 视频类型

#### AoqVideoCaptureConfig

**字段**

**类型**

**必填**

**默认值**

**说明**

width

number

否

1280

采集宽度（像素），isExternal=true 时无效

height

number

否

720

采集高度（像素），isExternal=true 时无效

fps

number

否

15

采集帧率，isExternal=true 时无效（节奏由送帧决定）

isExternal

boolean

否

false

是否外部采集，true 时不打开摄像头

**说明**`cameraDirection` 为移动端字段，桌面端无此字段。

#### AoqVideoCodecConfig

编码与解码共用同一结构（`setVideoEncoderConfig` / `setVideoDecoderConfig`）。

**字段**

**类型**

**必填**

**默认值**

**说明**

isExternal

boolean

否

false

true 时 SDK 不做采集与编码，由 pushExternalVideoEncodedFrame 直推

trackType

AoqTrackType

否

AoqTrackTypeVideo

轨道类型

codecType

AoqEncoderType

否

AoqEncoderTypeVideoH264

编码格式

width

number

否

540

编码宽度（像素）

height

number

否

960

编码高度（像素）

fps

number

否

5

编码帧率

bitrate

number

否

500000

起始比特率（bps）

minBitrate

number

否

128000

最小比特率（bps）

keyframeInterval

number

否

2

关键帧间隔（秒）

mirrorMode

AoqMirrorMode

否

AoqMirrorModeDisabled

镜像模式

orientationMode

AoqOrientationMode

否

AoqOrientationModeAuto

视频方向模式

#### AoqVideoPixelFormat

Electron 侧支持的像素格式（不包含移动端的纹理 / CVPixelBuffer 格式）。

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

#### AoqExternalVideoFrameMeta

外部视频裸帧元信息，像素数据另走 `buffer` 参数。

**字段**

**类型**

**必填**

**默认值**

**说明**

trackType

AoqTrackType

否

AoqTrackTypeVideo

轨道类型

format

AoqVideoPixelFormat

是

\-

像素格式

width

number

是

\-

视频宽度（像素）

height

number

是

\-

视频高度（像素）

timeStamp

number

否

0

时间戳（毫秒）；0 时 SDK 使用本地时间补齐

**说明**`format = I420` 时 `buffer` 必须为紧凑布局（stride = width），Y / U / V 三平面顺序拼接；其余打包格式直接传整帧字节。

#### AoqVideoCodecType

**枚举值**

**值**

**说明**

AoqVideoCodecTypeJPEG

0

JPEG 编码

#### AoqExternalVideoEncodedFrameMeta

外部已编码视频帧元信息，编码数据另走 `buffer` 参数。

**字段**

**类型**

**必填**

**默认值**

**说明**

trackType

AoqTrackType

否

AoqTrackTypeVideo

轨道类型

codec

AoqVideoCodecType

否

AoqVideoCodecTypeJPEG

编码格式

width

number

是

\-

宽度（像素）

height

number

是

\-

高度（像素）

timeStamp

number

否

0

时间戳（毫秒）；0 时 SDK 使用本地时间补齐

#### AoqVideoDeviceStateCode

**枚举值**

**值**

**说明**

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

采集失败（权限拒绝、设备不可用等）

#### AoqVideoDeviceState

**字段**

**类型**

**说明**

state

AoqVideoDeviceStateCode

设备采集操作状态

reason

number

错误原因代码（参考 AoqErrorCode）

### 视频帧回调类型

#### AoqVideoSource

**枚举值**

**值**

**说明**

AoqVideoSourceCaptured

0

采集后的视频数据（前处理前）

AoqVideoSourcePreEncode

1

编码前的视频数据（前处理后）

AoqVideoSourceRemote

2

远端解码后、渲染前的视频数据

#### AoqVideoObserverAlignment

**枚举值**

**值**

**说明**

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

#### AoqVideoObserverParams

**字段**

**类型**

**必填**

**默认值**

**说明**

enabled

boolean

是

false

开启或关闭该位置的回调

videoSource

AoqVideoSource

是

AoqVideoSourceCaptured

回调位置

format

AoqVideoPixelFormat

否

AoqVideoPixelFormatI420

期望回调像素格式

alignment

AoqVideoObserverAlignment

否

AoqVideoObserverAlignmentDefault

宽度对齐策略

mirrorApplied

boolean

否

false

是否对回调数据应用镜像

**说明**回调模式固定为只读，Electron 不开放读写模式。使用内置 `YUVCanvasRenderer` 渲染时需选 I420。

#### AoqVideoFrameEvent

视频帧观察者事件数据。

**字段**

**类型**

**说明**

trackType

AoqTrackType

轨道类型

format

AoqVideoPixelFormat

像素格式

width

number

宽度（像素）

height

number

高度（像素）

strideY

number

Y 平面行跨度（仅 I420 有效）

strideU

number

U 平面行跨度（仅 I420 有效）

strideV

number

V 平面行跨度（仅 I420 有效）

timeStamp

number

时间戳（毫秒）

buffer

Uint8Array

帧数据；I420 为 Y / U / V 三平面按 stride 拼接，其余打包格式为原数据透传

### 数据消息类型

Electron 不使用 `AoqDataMsg` 包装类型，数据消息直接以二进制收发：

**方向**

**类型**

**说明**

发送

Uint8Array 或 string

`sendDataMsg(data)`；字符串按 UTF-8 编码

接收

Uint8Array

`onDataMsg(data)`；native 侧已拷贝，可异步持有
