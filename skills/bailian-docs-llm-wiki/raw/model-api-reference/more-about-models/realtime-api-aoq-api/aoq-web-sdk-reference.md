# AOQ Web SDK API 参考

AOQ Web SDK 支持在浏览器中进行实时音视频和数据交互。本文介绍引擎管理、音视频采集与播放、数据消息和事件回调等 API。

## 安装 SDK

AOQ Web SDK 通过 WebTransport（HTTP/3 / QUIC）连接服务端，并在 Worker 中收发音频、视频和数据消息。使用 SDK 需要支持 WebTransport 的浏览器及 HTTPS 安全上下文，可通过 `AoqClientEngine.isAoqSupported()` 检查浏览器的基础能力。

通过 npm 安装 SDK：

```
npm install aoq-web-sdk@1.0.1-60040320
```

也可以在[SDK 下载](https://help.aliyun.com/zh/model-studio/realtime-sdk-download#sdkdl-h2-aoq-web)页面下载安装包，并在项目目录中执行以下命令。将安装包路径替换为实际路径。

```
npm install ./aoq-web-sdk-1.0.1-60040320.tgz
```

## 接口目录

### 引擎生命周期

接口

简介

[createEngine](#createengine)

创建引擎实例（单例）

[createAoqClientEngine](#createaoqclientengine)

等价的具名便捷工厂

[destroy](#destroy)

销毁引擎实例

[getVersion](#getversion)

获取 SDK 版本号

[isAoqSupported](#isaoqsupported)

检查浏览器能力

[connect](#connect)

发起连接

[disconnect](#disconnect)

断开连接

### 音频设备管理

接口

简介

[startAudioCapture](#startaudiocapture)

启动音频采集

[stopAudioCapture](#stopaudiocapture)

停止音频采集

[muteAudioCapture](#muteaudiocapture)

采集静音

[startAudioPlayer](#startaudioplayer)

启动音频播放

[stopAudioPlayer](#stopaudioplayer)

停止音频播放

[pauseAudioPlayer](#pauseaudioplayer)

暂停播放（带淡出）

[resumeAudioPlayer](#resumeaudioplayer)

恢复播放（默认淡入）

[interruptAudioPlayer](#interruptaudioplayer)

打断播放

### 音频编码配置

接口

简介

[setAudioEncoderConfig](#setaudioencoderconfig)

设置音频编码配置

[setAudioDecoderConfig](#setaudiodecoderconfig)

设置音频解码配置

### 本地音量提示

接口

简介

[enableLocalAudioVolumeIndication](#enablelocalaudiovolumeindication)

开启本地音量提示

### 视频设备管理

接口

简介

[startVideoCapture](#startvideocapture)

启动视频采集

[getCameras](#getcameras)

枚举摄像头

[switchCamera](#switchcamera)

按方向偏好或设备 ID 切换摄像头

[stopVideoCapture](#stopvideocapture)

停止视频采集

[setLocalView](#setlocalview)

设置本地视频渲染容器

[setRemoteView](#setremoteview)

设置远端视频渲染容器

### 视频编码配置

接口

简介

[setVideoEncoderConfig](#setvideoencoderconfig)

设置视频编码配置

[setVideoDecoderConfig](#setvideodecoderconfig)

设置视频解码配置

### 媒体流发送控制

接口

简介

[enableSendMediaStream](#enablesendmediastream)

启用/禁用媒体流发送

### 实时消息

接口

简介

[sendDataMsg](#senddatamsg)

发送数据消息

### 事件回调

接口

简介

[onError](#onerror)

错误回调

[onWarning](#onwarning)

警告回调

[onConnectionStatusChange](#onconnectionstatuschange)

连接状态变化

[onStats](#onstats)

统计信息

[onAudioDeviceStateChanged](#onaudiodevicestatechanged)

音频设备状态变化

[onAudioDeviceRouteChanged](#onaudiodeviceroutechanged)

音频路由变化

[onAudioFileState](#onaudiofilestate)

预留音频文件状态，当前不触发

[onLocalAudioVolumeIndication](#onlocalaudiovolumeindication)

本地音量提示

[onVideoDeviceStateChanged](#onvideodevicestatechanged)

视频设备状态变化

[onDataMsg](#ondatamsg)

数据消息

* * *

## 接口详情

### 引擎生命周期

#### createEngine

创建引擎实例。采用单例模式，重复调用返回已有实例。

```
static createEngine(config: AoqCreateConfig): AoqClientEngine | null
```

参数

类型

说明

`config`

`AoqCreateConfig`

引擎创建配置

返回值：成功返回 `AoqClientEngine` 实例，失败返回 `null`。

引擎为单例，若已存在已初始化的实例则直接返回该实例，不会重新应用配置。销毁后可重新创建。

#### createAoqClientEngine

从包入口具名导入的便捷工厂，等价于 `AoqClientEngine.createEngine(config)`，不是实例方法，也不需要二次初始化。

```
function createAoqClientEngine(config: AoqCreateConfig): AoqClientEngine | null
```

参数

类型

说明

`config`

`AoqCreateConfig`

必传，可传 `{}`；重复创建不重新应用配置

返回值：成功返回单例引擎，失败返回 `null`。

```
import { createAoqClientEngine } from 'aoq-web-sdk';

const engine = createAoqClientEngine({});
if (!engine) throw new Error('创建引擎失败');
```

#### destroy

销毁引擎实例，发起资源释放并移除全部事件监听。

```
static destroy(): number
```

返回值：`0` 表示成功，`AoqECStateInvalid(2)` 表示当前无实例。

销毁接口同步返回；日志保存、可选 dump 导出等异步收尾在后台执行，不代表返回时所有任务已完成。销毁后需重新调用 `createEngine` 才能继续使用 SDK，旧实例不可继续调用。

#### getVersion

获取 SDK 版本号。

```
static getVersion(): string
```

返回值：当前安装包的版本号字符串，与该包的版本一致；不返回文档修订号或源码提交号。

#### isAoqSupported

检查当前浏览器环境是否具备使用 AOQ 连接的基础能力。

```
static isAoqSupported(): Promise<AoqSupportResult>
```

返回值：`Promise<AoqSupportResult>`，包含是否支持及缺失能力列表。

返回 `supported: true` 不代表连接或音视频通话一定成功；不检查网络可达性、服务端配置、鉴权、设备授权及具体媒体配置的可用性。检测在 Worker 内执行 WebTransport 能力探测，超时为 5 秒。

#### connect

发起与服务端的连接。

```
connect(config: AoqConnectConfig): number
```

参数

类型

说明

`config`

`AoqConnectConfig`

连接鉴权配置，包含 token、会话 ID、接入点等

返回值：`0` 表示调用成功。

在创建引擎、注册事件及编解码配置完成后调用，正常从 `Disconnected` 发起；`Failed` 状态允许重新发起，其他状态返回 `AoqECStateInvalid(2)`。不合法的 Track/媒体配置、连接参数，或选用 Opus 但缺少所需 WebCodecs 能力，均可返回 `AoqECParamInvalid(1)`；Network Worker 不可用返回 `AoqECStateInvalid(2)`。

返回 0 仅表示连接请求已受理。连接结果通过 `onConnectionStatusChange` 异步通知，`Connected` 表示 MEDIA\_SETUP 完成且媒体轨道已绑定，不等于模型业务就绪；业务侧仍需按模型数据协议配置会话并确认就绪，再启用音视频发送。

#### disconnect

断开与服务端的连接。

```
disconnect(): number
```

返回值：`0` 表示调用成功。

断开结果通过 `onConnectionStatusChange` 事件通知，等待 `AoqConnectionStatusDisconnected` 后再修改编解码配置并重新连接。已断开时调用返回 `AoqECStateInvalid(2)`。断开不替代设备停止，结束通话还应调用对应采集/播放停止接口。

* * *

### 音频设备管理

#### startAudioCapture

启动音频采集（麦克风），异步请求设备权限。

```
startAudioCapture(config: AoqAudioCaptureConfig): Promise<number>
```

参数

类型

说明

`config`

`AoqAudioCaptureConfig`

音频采集配置

返回值：`Promise<number>`，`0` 表示成功。

首次使用或权限未授予时可能触发浏览器麦克风授权弹窗。采集状态变化通过 `onAudioDeviceStateChanged` 事件通知。

网络拥塞时，上行音频在发送队列中等待达到约 100 ms 即被丢弃，以避免延迟累积；已开始发送的音频不撤回，该值不代表端到端延迟上限。

#### stopAudioCapture

停止音频采集。

```
stopAudioCapture(): number
```

返回值：`0` 表示成功。

设备尚未启动或已停止时返回 `AoqECStateInvalid(2)`。

#### muteAudioCapture

静音或取消静音音频采集。静音后继续采集但发送静音帧。

```
muteAudioCapture(mute: boolean): number
```

参数

类型

说明

`mute`

`boolean`

`true` 静音，`false` 取消静音

返回值：`0` 表示成功。

#### startAudioPlayer

启动音频播放器，异步初始化音频输出设备。

```
startAudioPlayer(config: AoqAudioPlaybackConfig): Promise<number>
```

参数

类型

说明

`config`

`AoqAudioPlaybackConfig`

音频播放配置

返回值：`Promise<number>`，`0` 表示成功。

播放状态变化通过 `onAudioDeviceStateChanged` 事件通知。

应从用户点击事件调用并处理自动播放限制；播放器正在启动或已启动时重复调用返回 `AoqECStateInvalid(2)`。

Realtime 模式（音频下行 `trackMode` 为 Stream）下，播放器启动前收到的音频会被持续消费而不积压；每次启动（含首次）都会清除此前的音频，从之后收到的新音频开始播放，不补播启动前的语音。Segment 模式保留尚未播放的内容。

#### stopAudioPlayer

停止音频播放器。

```
stopAudioPlayer(): number
```

返回值：`0` 表示成功。

设备尚未启动或已停止时返回 `AoqECStateInvalid(2)`。

Realtime 模式停止设备输出后，SDK 仍持续消费收到的音频，视频继续播放；再次启动只播放新音频。已有的暂停或打断状态在重新启动后仍然保留。Segment 模式保留尚未播放的内容。

#### pauseAudioPlayer

暂停音频播放，淡出完成后停止输出，后续可调用 `resumeAudioPlayer` 恢复。

```
pauseAudioPlayer(fadeMs: number): number
```

参数

类型

说明

`fadeMs`

`number`

淡出时长（ms），按实际设备采样率四舍五入到样本数；0 不执行淡出，负数或非有限值使用 100 ms

返回值：`0` 表示控制请求已受理，不证明播放器正在播放或淡出已经完成。

Segment 模式冻结未播放内容及读取位置，恢复后从暂停处接续。Realtime 模式丢弃待播音频，暂停期间继续消费收到的音频，恢复后从当前实时位置播放，不补播暂停期间的内容。

#### resumeAudioPlayer

恢复暂停或打断的音频播放，使用默认淡入：Segment 为 2 ms，Realtime 为 100 ms。

```
resumeAudioPlayer(fadeMs: number): number
```

参数

类型

说明

`fadeMs`

`number`

保留参数，当前忽略传入时长；恢复使用默认淡入，不能通过传 0 取消

返回值：`0` 表示控制请求已受理，不证明恢复已经完成。

#### interruptAudioPlayer

打断当前音频播放，淡出完成后丢弃被打断的未播放余量；与 Segment 模式保留余量的暂停不同，之后恢复也不会重新播放已丢弃的部分。

```
interruptAudioPlayer(trackType: AoqTrackType, fadeMs: number): number
```

参数

类型

说明

`trackType`

`AoqTrackType`

兼容性参数，建议传 Audio；当前未按此参数区分播放流

`fadeMs`

`number`

淡出时长（ms），按实际设备采样率四舍五入到样本数；0 不执行淡出，负数或非有限值使用 100 ms

返回值：`0` 表示控制请求已受理，不证明播放器正在播放或打断已经完成。

打断后，服务端下发新一轮音频时自动恢复播放，也可调用 `resumeAudioPlayer` 恢复。

暂停状态下的打断请求会被忽略，仍可能返回 0；Segment 模式恢复后会继续播放暂停前的余量。不要将“暂停 → 打断”的调用序列当作清空播放队列。

* * *

### 音频编码配置

#### setAudioEncoderConfig

设置音频编码参数。

```
setAudioEncoderConfig(config: AoqAudioCodecConfig): number
```

参数

类型

说明

`config`

`AoqAudioCodecConfig`

音频编码配置

返回值：`0` 表示成功。

必须在 `connect()` 前、引擎处于 `Disconnected` 时调用。连接中或已连接时修改返回 `AoqECStateInvalid(2)`；需先断开并等待 `Disconnected`，再配置及重新连接。

返回 0 表示配置请求已受理；音频格式在建连时再次校验，Opus 还依赖浏览器 WebCodecs 能力。

#### setAudioDecoderConfig

设置音频解码参数。

```
setAudioDecoderConfig(config: AoqAudioCodecConfig): number
```

参数

类型

说明

`config`

`AoqAudioCodecConfig`

音频解码配置

返回值：`0` 表示成功。

必须在 `connect()` 前、引擎处于 `Disconnected` 时调用。连接中或已连接时修改返回 `AoqECStateInvalid(2)`。

* * *

### 本地音量提示

#### enableLocalAudioVolumeIndication

开启或关闭本地采集音量提示。开启后通过 `onLocalAudioVolumeIndication` 事件周期性回调音量信息。

```
enableLocalAudioVolumeIndication(config: AoqAudioVolumeIndicationConfig): number
```

参数

类型

说明

`config`

`AoqAudioVolumeIndicationConfig`

音量提示配置

返回值：`0` 表示成功。

`interval` 设置为 `0` 或负值表示关闭回调。

* * *

### 视频设备管理

#### startVideoCapture

启动视频采集（摄像头）。

```
startVideoCapture(config: AoqVideoCaptureConfig): number
```

参数

类型

说明

`config`

`AoqVideoCaptureConfig`

视频采集配置

返回值：`0` 表示成功。

返回 0 仅表示异步采集请求已受理，不能据此判定摄像头已开启。实际成功/失败通过 `onVideoDeviceStateChanged` 事件通知。

`cameraPreference` 为摄像头选择偏好，可传方向枚举或设备 ID；省略时由浏览器选择。方向或设备 ID 无法满足时，均允许浏览器选择其他可用摄像头。

#### getCameras

```
getCameras(): Promise<MediaDeviceInfo[]>
```

枚举浏览器可见的 `videoinput`，不打开摄像头或主动申请权限。未授权时设备名称或 ID 可能不完整，授权或设备插拔后可重新枚举；引擎未初始化或枚举失败时 Promise 拒绝。

#### switchCamera

```
switchCamera(cameraPreference?: AoqCameraDirection | string): number
```

参数

类型

必填

说明

`cameraPreference`

`AoqCameraDirection | string`

否

方向或设备 ID 偏好；省略时清除先前偏好，重新由浏览器选择

方向和设备 ID 使用 ideal 约束，无法满足时允许回退到其他可用摄像头。返回 0 只表示受理，状态通过 `onVideoDeviceStateChanged` 通知，失败原因通过 `onError` 报告。未采集、正在启动或正在切换时返回 `AoqECStateInvalid(2)`；非法方向或空白 ID 返回 `AoqECParamInvalid(1)`。

切换先释放旧设备，再打开目标并等待首帧，若旧采集向 Worker 转移过摄像头轨道（包括随后回退到主线程的情况），打开设备前会等待释放确认，最多等待 2 秒；确认超时则报告失败，不继续打开目标或恢复设备。每次尝试最多 15 秒。失败后尝试以原设备为偏好恢复采集一次，恢复成功仍报告本次切换失败。成功通知 `CaptureStarted(reason=0)`；失败但已恢复采集通知 `CaptureStarted(reason=失败码)`；无法恢复通知 `CaptureFail(reason=失败码)`。显式目标已满足时异步通知 `CaptureStarted`，不重开设备。状态回调不提供实际设备 ID，不能把请求偏好当作实际设备。切换不改变发送开关、编码配置和预览绑定；停止采集可取消切换，销毁后不再回调。

切换可能短暂中断画面；采集时间线保持连续，但不保证硬件级音画同步。实际设备由浏览器选择，业务 UI 不应将请求偏好直接显示为已选设备。

#### stopVideoCapture

停止视频采集。

```
stopVideoCapture(): number
```

返回值：`0` 表示成功。

设备尚未启动或已停止时返回 `AoqECStateInvalid(2)`。

#### setLocalView

设置本地视频渲染容器。SDK 会在指定容器内创建渲染元素。

```
setLocalView(trackType: AoqTrackType, canvas: AoqVideoCanvas | null): number
```

参数

类型

说明

`trackType`

`AoqTrackType`

仅支持 AoqTrackTypeVideo，其他类型返回 AoqECUnSupport(3)

`canvas`

`AoqVideoCanvas | null`

渲染容器配置，传 `null` 解除绑定

返回值：`0` 表示成功。

容器元素应具有明确尺寸，SDK 在容器内部创建实际渲染元素。

使用尺寸明确的普通 DOM 容器（例如 div），不能直接传入 video、audio、canvas、img 或空元素。容器无效、id 不存在或 renderMode 非法时返回 AoqECParamInvalid(1)，保留原绑定；返回 0 仅表示绑定受理，不保证已经渲染首帧。

#### setRemoteView

设置远端视频渲染容器。SDK 会在指定容器内创建渲染元素。

```
setRemoteView(trackType: AoqTrackType, canvas: AoqVideoCanvas | null): number
```

参数

类型

说明

`trackType`

`AoqTrackType`

仅支持 AoqTrackTypeVideo，其他类型返回 AoqECUnSupport(3)

`canvas`

`AoqVideoCanvas | null`

渲染容器配置，传 `null` 解除绑定

返回值：`0` 表示成功。

使用尺寸明确的普通 DOM 容器（例如 div），不能直接传入 video、audio、canvas、img 或空元素。容器无效、id 不存在或 renderMode 非法时返回 AoqECParamInvalid(1)，保留原绑定；返回 0 仅表示绑定受理，不保证已经渲染首帧。

* * *

### 视频编码配置

#### setVideoEncoderConfig

设置视频编码参数。

```
setVideoEncoderConfig(config: AoqVideoCodecConfig): number
```

参数

类型

说明

`config`

`AoqVideoCodecConfig`

视频编码配置

返回值：`0` 表示成功。

必须在引擎处于 `Disconnected` 时调用，连接中或已连接时返回 `AoqECStateInvalid(2)`。建议在首次连接及视频采集前完成配置；配置合并缓存用于后续建流，不立即重配已有采集或编码器。

#### setVideoDecoderConfig

设置视频解码参数。

```
setVideoDecoderConfig(config: AoqVideoCodecConfig): number
```

参数

类型

说明

`config`

`AoqVideoCodecConfig`

视频解码配置

返回值：`0` 表示成功。

必须在 `connect()` 前、引擎处于 `Disconnected` 时调用。连接中或已连接时修改返回 `AoqECStateInvalid(2)`。

* * *

### 媒体流发送控制

#### enableSendMediaStream

启用或禁用音频或视频 Track 的媒体流发送。

```
enableSendMediaStream(trackType: AoqTrackType, enable: boolean): number
```

参数

类型

说明

`trackType`

`AoqTrackType`

媒体 track 类型

`enable`

`boolean`

`true` 启用发送，`false` 禁用发送

返回值：`0` 表示成功。

当前仅控制 Audio / Video，不能控制 Data 发送；其他 Track 值即使返回 0 也不代表生效。停发不关闭采集设备；需要关闭设备时调用相应 `stop...Capture()`。

* * *

### 实时消息

#### sendDataMsg

发送以 `Uint8Array` 承载的 UTF-8 文本消息到远端，可用于业务 JSON。当前 WT 通路不支持任意二进制载荷，也不能用此接口发送 SDK 内部控制消息。

```
sendDataMsg(msg: AoqDataMsg): number
```

参数

类型

说明

`msg`

`AoqDataMsg`

消息对象，`msg.data` 为非空 UTF-8 编码字节

返回值：`0` 表示成功。

需已连接且媒体轨道就绪、`publishTracks` 包含 Data，消息不能为空。缺少消息对象或 `msg.data` 不是 `Uint8Array` 时返回 `AoqECParamInvalid(1)`；未就绪返回 `AoqECStateInvalid(2)`；发送流未激活或消息为空时当前实现返回 `-1`。返回 0 仅表示本地受理，UTF-8 校验或后续发送仍可能通过 `onError` 报告失败，不代表远端确认收到。

`msg.data` 的底层 `ArrayBuffer` 可能被转移并失效，包括共享该缓冲区的其他视图；需要保留原数据时传入 `data.slice()` 的副本。不要在前端消息或日志中发送 API Key、临时凭证等敏感信息。

```
const data = new TextEncoder().encode(JSON.stringify({ type: 'user_message', text: '你好' }));
const code = engine.sendDataMsg({ data });
if (code !== 0) console.error('消息未受理', code);
```

示例 JSON 仅用于展示编码方式，实际字段和业务就绪流程应遵循所用模型的数据消息协议。

* * *

### 事件回调

事件通过 `engine.on('eventName', callback)` 订阅，`engine.once(...)` 仅监听一次，`engine.off('eventName', callback)` 取消相同函数引用的监听；销毁引擎会移除全部监听。应在连接或启动设备前注册，并保持回调轻量。

```
import { AoqConnectionStatus } from 'aoq-web-sdk';

const handleStatus = (status: AoqConnectionStatus) => console.log('连接状态', status);
engine.on('onConnectionStatusChange', handleStatus);
engine.off('onConnectionStatusChange', handleStatus);
```

事件名

回调签名

说明

`onError`

`(code: number, message: string) => void`

错误回调

`onWarning`

`(code: number, message: string) => void`

警告回调

`onConnectionStatusChange`

`(status: AoqConnectionStatus) => void`

连接状态变化

`onStats`

`(stats: AoqStats) => void`

统计信息

`onAudioDeviceStateChanged`

`(state: AoqAudioDeviceState) => void`

音频设备状态变化

`onAudioDeviceRouteChanged`

`(routeType: AoqAudioDeviceRouteType) => void`

音频路由变化

`onAudioFileState`

`(state: AoqAudioFileState) => void`

预留，当前门面未触发

`onLocalAudioVolumeIndication`

`(volume: AoqAudioVolume) => void`

本地音量提示

`onVideoDeviceStateChanged`

`(state: AoqVideoDeviceState) => void`

视频设备状态变化

`onDataMsg`

`(msg: AoqDataMsg) => void`

数据消息

#### onError

报告同步返回值之外的异步错误或运行错误。`code` 与 `message` 用于排查问题；收到错误不等于整个连接已终结，应结合连接和设备状态判断。网络错误可能使用通用状态错误码，不应仅按数字推断错误阶段。

```
engine.on('onError', (code: number, message: string) => { /* 在此处理回调 */ });
```

参数

类型

说明

`code`

`number`

错误码，参见 `AoqErrorCode` 枚举

`message`

`string`

错误描述信息

#### onWarning

引擎警告回调，通知可忽略但需关注的异常情况。

```
engine.on('onWarning', (code: number, message: string) => { /* 在此处理回调 */ });
```

参数

类型

说明

`code`

`number`

警告码，参见 `AoqWarningCode` 枚举

`message`

`string`

警告描述信息

#### onConnectionStatusChange

连接状态变化回调。

```
engine.on('onConnectionStatusChange', (status: AoqConnectionStatus) => { /* 在此处理回调 */ });
```

参数

类型

说明

`status`

`AoqConnectionStatus`

当前连接状态

#### onStats

连接成功期间约每秒回调一次统计信息；离开 Connected 状态后停止。字段可用性见 [AoqStats](#aoqstats)，不能把占位值当成真实测量。

```
engine.on('onStats', (stats: AoqStats) => { /* 在此处理回调 */ });
```

参数

类型

说明

`stats`

`AoqStats`

统计信息对象

#### onAudioDeviceStateChanged

音频设备（采集/播放）操作状态变化回调。

```
engine.on('onAudioDeviceStateChanged', (state: AoqAudioDeviceState) => { /* 在此处理回调 */ });
```

参数

类型

说明

`state`

`AoqAudioDeviceState`

音频设备状态

#### onAudioDeviceRouteChanged

输出设备列表变化时，SDK 根据浏览器设备标签尽力推断路由类型并回调。该事件不是实际输出路由的确认，可能误判或漏报；授权前或设备信息不完整时可能返回默认类型。

```
engine.on('onAudioDeviceRouteChanged', (routeType: AoqAudioDeviceRouteType) => { /* 在此处理回调 */ });
```

参数

类型

说明

`routeType`

`AoqAudioDeviceRouteType`

根据设备标签推断的路由类型，不能据此确认实际输出设备

#### onAudioFileState

预留的音频文件状态回调。当前 AoqClientEngine 门面没有文件播放控制方法，也未触发此事件。

```
engine.on('onAudioFileState', (state: AoqAudioFileState) => { /* 在此处理回调 */ });
```

参数

类型

说明

`state`

`AoqAudioFileState`

音频文件状态

#### onLocalAudioVolumeIndication

本地采集音量提示回调。需先调用 `enableLocalAudioVolumeIndication` 开启。

```
engine.on('onLocalAudioVolumeIndication', (volume: AoqAudioVolume) => { /* 在此处理回调 */ });
```

参数

类型

说明

`volume`

`AoqAudioVolume`

音量信息

#### onVideoDeviceStateChanged

视频设备采集操作状态变化回调。

```
engine.on('onVideoDeviceStateChanged', (state: AoqVideoDeviceState) => { /* 在此处理回调 */ });
```

参数

类型

说明

`state`

`AoqVideoDeviceState`

视频设备状态

#### onDataMsg

接收远端数据消息回调。

```
engine.on('onDataMsg', (msg: AoqDataMsg) => { /* 使用 msg.data 读取消息数据 */ });
```

参数

类型

说明

`msg`

`AoqDataMsg`

接收的消息对象，使用 `TextDecoder` 读取 `msg.data` 中的 UTF-8 文本

接收数据消息需在 `subscribeTracks` 中配置 Data；回调参数是对象，不是直接的 `Uint8Array`。业务 JSON 的解析和校验由业务侧完成。

* * *

## 数据类型与枚举

### 通用类型

#### AoqCreateConfig

引擎创建配置。

字段

类型

必填

默认值

说明

`workDir`

`string`

否

—

保留字段，当前 Web 实现不使用此配置指定存储目录

`enableDumpAudio`

`boolean`

否

`false`

是否保存音频调试数据；涉及用户音频，应取得授权并控制访问

`enableDumpExport`

`boolean`

否

`false`

仅在 enableDumpAudio=true 时生效；销毁时异步导出 dump ZIP 并清理相应 OPFS 文件

`maxEncodedVideoFrameBytes`

`number`

否

`194560`（190×1024）

JPEG 单帧目标上限（byte），`0` 关闭；超限自动降质，非法值使用默认值

`enableDropOversizedVideoFrame`

`boolean`

否

`false`

最低 JPEG 质量仍超限时是否丢帧；false 时仍可能发送超限帧，上限为 0 时不因此丢帧

`extras`

`string`

否

—

JSON 对象字符串；非法 JSON、非对象或非法远端渲染策略导致 createEngine 返回 null

可使用的 `extras` 配置：

JSON 字段

类型

默认值

说明

`remoteVideoRenderer`

`'auto' | 'video' | 'canvas'`

`'auto'`

远端渲染策略；auto 优先 video，必要时回退 canvas

`user_specified_enable_av_sync`

`boolean`

`true`

是否启用音画同步；建议使用 JSON 布尔值

`user_specified_audio_playback_transport`

`'message-port'`

自动选择

指定 MessagePort 播放；省略时按环境自动选择共享内存或 MessagePort

这些字段不用于修改 HTTP 响应头或开启公共诊断 API。

#### AoqConnectConfig

连接鉴权配置。

字段

类型

必填

默认值

说明

`token`

`string`

是

—

非空客户端临时 token，对应 aoqTokenForClient，不是 API Key

`sid`

`string`

是

—

非空会话 ID，当前取鉴权响应的完整 sid 字符串

`wtBaseUrl`

`string`

否

根据 Relay 构造

单路由时优先使用的 HTTPS WT URL，多路由时忽略并按各自主机、端口连接 /aoq

`signedSid`

`string`

是（运行时）

—

完整签名 SID，通常使用鉴权响应的完整 sid；TypeScript 标为可选，当前 WT 仍要求有效值

`certFingerprint`

`string | string[]`

条件必填

—

公共 WT 证书 SHA-256 指纹；未提供独立指纹的路由必须能使用此值

`workspaceIdHash`

`string`

否

—

对应 extraInfo.workspaceIdHash，不能用原始 Workspace ID 代替

`relayEndpoints`

`AoqRelayEndpoint[]`

是

—

完整接入点列表，至少一项

`publishTracks`

`AoqTrackParam[]`

是

—

上行 Track 列表，可为空；与 subscribeTracks 不能同时为空

`subscribeTracks`

`AoqTrackParam[]`

是

—

下行 Track 列表，可为空；同一方向不能重复 Track，当前不支持 Screen

业务后端应返回完整有效的连接材料，适配层将 `clientRelayEndpoints[].route_index` 映射为 `routeIndex`，不要自行补造 SID、接入地址、路由索引或指纹。

WT 指纹必须对应实际 WebTransport 入口证书。若后端使用 `sha256/<hex>` 格式，适配层需去掉前缀并校验为 64 位十六进制。公共和路由指纹均可为单个字符串或字符串数组；数组每项均须有效，浏览器匹配任一项即可通过。路由非空指纹覆盖公共指纹，空数组视为未配置。SDK 不内置通用指纹，也不提供跳过校验选项。

缺少 `signedSid` 或有效指纹可能在异步连接阶段失败，即使 `connect()` 已返回 0，也应处理状态事件及 `onError`。

#### AoqRelayEndpoint

Relay 接入点。

字段

类型

必填

默认值

说明

`routeIndex`

`number`

是（运行时）

—

唯一的 0..2147483647 整数，初连选择最小索引；TypeScript 标为可选

`certFingerprint`

`string | string[]`

条件必填

公共指纹

当前路由指纹，非空值覆盖公共配置；无公共指纹时必须提供

`endpoint`

`string`

是

—

WT 主机名/IP，不含协议、路径、空白、用户信息或查询串；支持 IPv6

`port`

`number`

是

—

WT 端口，1..65535 的整数

#### AoqTrackParam

track 属性。

字段

类型

必填

默认值

说明

`trackType`

`AoqTrackType`

是

—

Audio、Video 或 Data；同一方向不可重复，Screen 当前不支持

`trackMode`

`AoqTrackMode`

否

音频下行为 Segment

仅控制音频下行：PCM / Opus 默认 Segment，显式 Stream 选择 Realtime；音频上行固定 Realtime，上行及视频/数据忽略此字段

#### AoqSupportResult

浏览器能力检测结果。

字段

类型

默认值

说明

`supported`

`boolean`

—

当前环境是否具备使用 AOQ 连接的基础能力

`missingFeatures`

`AoqMissingFeature[]`

—

已观察到的预检失败项列表，可能包含 `'secure-context'`、`'worker'`、`'web-transport'`

#### AoqMissingFeature

基础能力预检失败项：`'secure-context' | 'worker' | 'web-transport'`。worker 也可能表示部署策略阻止、启动/执行失败或探测超时，不一定是浏览器缺少 Worker API；失败列表不是全部媒体能力的检测结果。

* * *

### 音频类型

#### AoqAudioCaptureConfig

音频采集配置。

字段

类型

必填

默认值

说明

`channel`

`number`

否

`1`

请求采集通道数，支持 1（单声道）/ 2（立体声）；实际可能由设备轨道设置决定

#### AoqAudioPlaybackConfig

音频播放配置。

字段

类型

必填

默认值

说明

`channel`

`number`

否

`1`

请求播放通道数，支持 1 / 2；输出采样率使用实际 AudioContext 采样率

`playOnlyAndIgnoreMute`

`boolean`

否

`false`

仅播放场景使用；浏览器支持 audioSession 时设为 playback，以避免 iOS 静音开关影响。需要采集麦克风时保持 false；不支持时无法保证忽略静音开关

#### AoqAudioCodecConfig

音频编解码配置。

字段

类型

必填

默认值

说明

`trackType`

`AoqTrackType`

否

—

保留字段，当前不用于选择音频流

`codecType`

`AoqEncoderType`

否

`AoqEncoderTypeAudioPCM`

支持 PCM / Opus，需与对端协商一致

`sampleRate`

`number`

否

`48000`

采样率（Hz）；协商支持 8000、12000、16000、24000、32000、44100、48000，具体编码仍需浏览器支持

`channel`

`number`

否

`1`

声道数，1 或 2

`bitrate`

`number`

否

`32000`（Opus 编码）

单位 bps，仅 Opus 编码使用；PCM 码率由采样率、声道和位深决定，解码不使用

#### AoqAudioVolumeIndicationConfig

本地音量提示配置。

字段

类型

必填

默认值

说明

`interval`

`number`

否

`0`

回调间隔（ms）；<=0 关闭，正数小于 10 时按 10 处理

`smooth`

`number`

否

`3`

音量平滑系数，范围 0..10，越大越平滑

`reportSpeech`

`boolean`

否

`false`

是否上报语音活动状态（VAD）

#### AoqAudioVolume

本地音量信息。

字段

类型

默认值

说明

`volume`

`number`

—

平滑后的瞬时音量，取值范围 \[0-255\]

`isSpeech`

`boolean`

—

可选，语音活动标志，仅 reportSpeech=true 时有意义，调用方应处理缺省值

#### AoqAudioDeviceState

音频设备状态回调数据。

字段

类型

默认值

说明

`state`

`AoqAudioDeviceStateCode`

—

音频设备状态码

`reason`

`number`

—

原因码，参见 `AoqErrorCode`

#### AoqAudioFileState

预留的音频文件播放状态结构；当前 Web 不触发对应事件。

字段

类型

默认值

说明

`fileId`

`string`

—

音频文件标识

`stateCode`

`AoqAudioFileStateCode`

—

文件播放状态码

`errorCode`

`number`

—

错误码

* * *

### 视频类型

#### AoqVideoCaptureConfig

视频采集配置。

字段

类型

必填

默认值

说明

`width`

`number`

否

`1280`

请求采集宽度（像素，ideal 约束），实际由浏览器/设备决定

`height`

`number`

否

`720`

请求采集高度（像素，ideal 约束），实际由浏览器/设备决定

`fps`

`number`

否

`15`

请求采集帧率（ideal 和 max 约束）

`cameraPreference`

`AoqCameraDirection | string`

否

浏览器选择

摄像头方向/设备 ID 偏好，使用 ideal 约束，无法满足时允许回退；空白字符串无效

#### AoqVideoCodecConfig

视频编解码配置。

字段

类型

必填

默认值

说明

`trackType`

`AoqTrackType`

否

—

保留字段，当前不用于选择视频流

`codecType`

`AoqEncoderType`

否

`AoqEncoderTypeVideoH264`

支持 H.264 / JPEG，需与对端协商一致

`width`

`number`

否

`540`

编码目标宽度/下行协商声明宽度（像素），连接时要求正整数

`height`

`number`

否

`960`

编码目标高度/下行协商声明高度（像素），连接时要求正整数

`fps`

`number`

否

`5`

编码帧率/下行协商声明帧率，连接时要求正整数

`bitrate`

`number`

否

`500000`（编码）

编码目标码率（bps），需为正数，解码不使用

`minBitrate`

`number`

否

`128000`

编码最低目标码率（bps）；缺省或 0 使用 128000，且不超过用户目标；H.264 不因 BWE 预算归零而暂停编码；解码不使用

`keyframeInterval`

`number`

否

`2`

H.264 关键帧间隔（秒），编码时至少按 1 秒处理；JPEG/解码不使用

#### AoqVideoCanvas

视频渲染容器配置。

字段

类型

必填

默认值

说明

`view`

`HTMLElement | string`

是

—

普通容器元素或其 DOM id（不带 `#`）；不能直接使用 video、audio、canvas、img 或空元素

`renderMode`

`AoqRenderMode`

否

`AoqRenderModeAuto(0)`

画面适配方式

本地预览根据实际采集轨道的前置方向自动进行 CSS 镜像，方向未知时不镜像；这不改变编码像素。当前没有独立的镜像或方向配置项。非法替换保留原绑定；传 null 解绑仅移除 SDK 自有渲染节点，保留业务节点。

#### AoqVideoDeviceState

视频设备状态回调数据。

字段

类型

默认值

说明

`state`

`AoqVideoDeviceStateCode`

—

视频设备状态码

`reason`

`number`

—

原因码；主动停止为 `0`，Web 轨道非主动结束为 `AoqECVideoDevice(220)`

* * *

### 数据消息类型

#### AoqDataMsg

公共 `sendDataMsg` / `onDataMsg` 统一使用的消息结构，不接收直接的字符串或 `Uint8Array` 参数。当前 WT 通路以字节数组承载 UTF-8 文本。

字段

类型

必填

默认值

说明

`data`

`Uint8Array`

是

—

发送时必须非空且为有效 UTF-8；接收时使用 `msg.data` 读取

* * *

### 统计信息类型

#### AoqStats

引擎统计信息汇总。以下字段在类型定义中均为可选，读取时应处理缺省情况。

字段

类型

默认值

说明

`audioPublishStats`

`AoqAudioPublishStats[]`

—

音频推流统计列表

`audioSubscribeStats`

`AoqAudioSubscribeStats[]`

—

音频拉流统计列表

`videoPublishStats`

`AoqVideoPublishStats[]`

—

视频推流统计列表

`videoSubscribeStats`

`AoqVideoSubscribeStats[]`

—

视频拉流统计列表

`dataMsgPublishStats`

`AoqDataMsgPublishStats[]`

—

数据消息推流统计列表

`dataMsgSubscribeStats`

`AoqDataMsgSubscribeStats[]`

—

数据消息拉流统计列表

`networkStats`

`AoqNetworkStats`

—

网络统计

当前 onStats 未填充 dataMsgPublishStats / dataMsgSubscribeStats。音频数组的 bitrate / bytes 使用连接总量，尚非独立音频流量；encodeVolume / playVolume 固定为 0。视频数组的 bitrate / bytes 也固定为 0，仅帧率由视频引擎提供。总流量请读 networkStats，采集音量请使用 onLocalAudioVolumeIndication。

#### AoqAudioPublishStats

音频推流统计。

字段

类型

默认值

说明

`trackType`

`AoqTrackType`

—

track 类型

`bitrate`

`number`

—

当前取连接总上行业务码率（bps），不是独立音频码率

`bytes`

`number`

—

当前取连接总上行业务字节数，不是独立音频累计量

`encodeVolume`

`number`

`0`

当前为占位值，采集音量请使用 onLocalAudioVolumeIndication

#### AoqAudioSubscribeStats

音频拉流统计。

字段

类型

默认值

说明

`trackType`

`AoqTrackType`

—

track 类型

`bitrate`

`number`

—

当前取连接总下行业务码率（bps），不是独立音频码率

`bytes`

`number`

—

当前取连接总下行业务字节数，不是独立音频累计量

`playVolume`

`number`

`0`

当前为占位值，不能据此判断播放是否静音

#### AoqVideoPublishStats

视频推流统计。

字段

类型

默认值

说明

`trackType`

`AoqTrackType`

—

track 类型

`bitrate`

`number`

`0`

当前未提供分视频码率统计，此值为占位

`bytes`

`number`

`0`

当前未提供分视频字节统计，此值为占位

`encodeFps`

`number`

—

编码帧率

#### AoqVideoSubscribeStats

视频拉流统计。

字段

类型

默认值

说明

`trackType`

`AoqTrackType`

—

track 类型

`bitrate`

`number`

`0`

当前未提供分视频码率统计，此值为占位

`bytes`

`number`

`0`

当前未提供分视频字节统计，此值为占位

`decodeFps`

`number`

—

解码帧率

`renderFps`

`number`

—

渲染帧率

#### AoqDataMsgPublishStats

数据消息推流统计。

字段

类型

默认值

说明

`trackType`

`AoqTrackType`

—

track 类型

`bitrate`

`number`

—

当前码率（bps）

`bytes`

`number`

—

累计发送字节数

类型已定义，但当前 onStats 不填充此统计数组。

#### AoqDataMsgSubscribeStats

数据消息拉流统计。

字段

类型

默认值

说明

`trackType`

`AoqTrackType`

—

track 类型

`bitrate`

`number`

—

当前码率（bps）

`bytes`

`number`

—

累计接收字节数

类型已定义，但当前 onStats 不填充此统计数组。

#### AoqNetworkStats

网络统计信息。码率为业务载荷 bit/s，累计量为同口径字节，不含探测和传输协议开销。

字段

类型

默认值

说明

`sendBitrate`

`number`

—

上行码率（bps）

`sendBytes`

`number`

—

累计上行字节数

`recvBitrate`

`number`

—

下行码率（bps）

`recvBytes`

`number`

—

累计下行字节数

`loss`

`number`

—

可选；上行丢失比例（0–1），优先浏览器 QUIC 观测，否则使用 Relay Datagram 估计；未知时缺省

`rtt`

`number`

—

可选；往返时延（ms），未知时缺省

`bwe`

`number`

—

可选；Client→Relay 有效应用发送预算（bps），未知或过期时缺省

`audioReserveBps`

`number`

—

可选；当前编码音频的净载荷预留码率（bps），不包含 RED 冗余和传输协议开销，不等于实际音频流量

* * *

### 枚举类型

#### AoqTrackType

track 媒体类型。

枚举值

值

说明

`AoqTrackTypeAudio`

`0`

音频

`AoqTrackTypeVideo`

`1`

视频

`AoqTrackTypeData`

`2`

数据消息

`AoqTrackTypeScreen`

`3`

保留枚举，当前连接流程不支持

#### AoqTrackMode

音频传输模式。

枚举值

值

说明

`AoqTrackModeSegment`

`0`

分段模式

`AoqTrackModeStream`

`1`

实时流模式（realtime）

#### AoqEncoderType

track 媒体格式。

枚举值

值

说明

`AoqEncoderTypeUnknown`

`0`

未知

`AoqEncoderTypeAudioPCM`

`1`

音频 PCM

`AoqEncoderTypeAudioOpus`

`2`

音频 Opus

`AoqEncoderTypeVideoH264`

`3`

视频 H.264

`AoqEncoderTypeVideoJpeg`

`4`

视频 JPEG

`AoqEncoderTypeDataText`

`5`

文本数据

#### AoqConnectionStatus

引擎连接状态。

枚举值

值

说明

`AoqConnectionStatusDisconnected`

`0`

已断开

`AoqConnectionStatusConnecting`

`1`

连接中

`AoqConnectionStatusConnected`

`2`

已连接

`AoqConnectionStatusFailed`

`3`

连接失败

#### AoqErrorCode

错误码。

枚举值

值

说明

`AoqECOK`

`0`

成功

`AoqECParamInvalid`

`1`

参数无效

`AoqECStateInvalid`

`2`

状态无效

`AoqECUnSupport`

`3`

当前平台/模式未实现

`AoqECAudio`

`100`

音频通用错误

`AoqECAudioExternalBufferFull`

`110`

外部音频缓冲区已满

`AoqECAudioDevice`

`120`

音频设备通用错误

`AoqECAudioDeviceRecordingAuthFailed`

`121`

麦克风授权失败

`AoqECAudioDeviceRecordingOccupied`

`122`

麦克风被占用

`AoqECAudioDeviceRecordingBackgroundStart`

`123`

后台启动采集

`AoqECAudioDeviceRecordingStartFail`

`124`

采集启动失败

`AoqECAudioDevicePlayoutOccupied`

`125`

播放设备被占用

`AoqECAudioDevicePlayoutBackgroundStart`

`126`

后台启动播放

`AoqECAudioDevicePlayoutStartFail`

`127`

播放启动失败

`AoqECAudioDeviceEarpieceRequiresVoipMode`

`128`

听筒需要 VoIP 模式

`AoqECVideo`

`200`

视频通用错误

`AoqECVideoExternalBufferFull`

`210`

外部视频缓冲区已满

`AoqECVideoExternalCaptureNotEnabled`

`211`

外部视频采集未启用

`AoqECVideoExternalEncoderNotEnabled`

`212`

外部视频编码器未启用

`AoqECVideoDevice`

`220`

视频设备通用错误

`AoqECVideoDeviceCameraOpenFail`

`221`

摄像头打开失败

`AoqECVideoDeviceCameraAuthFailed`

`222`

摄像头授权失败

`AoqECVideoDeviceCameraOccupied`

`223`

摄像头被占用

`AoqECVideoDeviceCameraRunningError`

`224`

摄像头运行错误

`AoqECVideoCodec`

`230`

视频编解码通用错误

`AoqECVideoCodecEncoderInitFail`

`231`

视频编码器初始化失败

`AoqECVideoRender`

`240`

视频渲染通用错误

`AoqECVideoRenderCreateFail`

`241`

渲染器创建失败

`AoqECVideoRenderDrawError`

`242`

渲染绘制错误

#### AoqWarningCode

警告码。

枚举值

值

说明

`AoqWCOK`

`0`

正常

`AoqWCAudio`

`100`

音频通用警告

`AoqWCAudioHowling`

`101`

检测到啸叫

`AoqWCAudioDevice`

`120`

音频设备通用警告

`AoqWCAudioDeviceMicEnumerateError`

`121`

麦克风枚举错误

`AoqWCAudioDeviceMicStartTimeout`

`122`

麦克风启动超时

`AoqWCAudioDeviceRecordingError`

`123`

采集异常

`AoqWCAudioDeviceSpeakerEnumerateError`

`124`

扬声器枚举错误

`AoqWCAudioDeviceSpeakerStartTimeout`

`125`

扬声器启动超时

`AoqWCAudioDevicePlayoutError`

`126`

播放异常

`AoqWCAudioDeviceSilentMode`

`127`

设备处于静音模式

`AoqWCVideo`

`200`

视频通用警告

`AoqWCVideoCameraEnumerateError`

`201`

摄像头枚举错误

`AoqWCVideoEncoderSwitched`

`202`

视频编码器已切换

`AoqWCVideoRenderDowngrade`

`203`

渲染降级

#### AoqAudioDeviceStateCode

音频设备状态码。

枚举值

值

说明

`AoqAudioDeviceNone`

`0`

无状态

`AoqAudioDeviceRecordStarting`

`1`

采集启动中

`AoqAudioDeviceRecordStarted`

`2`

采集已启动

`AoqAudioDeviceRecordStopping`

`3`

采集停止中

`AoqAudioDeviceRecordStopped`

`4`

采集已停止

`AoqAudioDeviceRecordFail`

`5`

采集失败

`AoqAudioDevicePlayStarting`

`6`

播放启动中

`AoqAudioDevicePlayStarted`

`7`

播放已启动

`AoqAudioDevicePlayStopping`

`8`

播放停止中

`AoqAudioDevicePlayStopped`

`9`

播放已停止

`AoqAudioDevicePlayFail`

`10`

播放失败

#### AoqAudioDeviceRouteType

音频设备路由类型。

枚举值

值

说明

`AoqAudioDeviceRouteDefault`

`0`

默认路由

`AoqAudioDeviceRouteHeadset`

`1`

耳机

`AoqAudioDeviceRouteSpeakerPhone`

`4`

内置扬声器

`AoqAudioDeviceRouteUsb`

`5`

USB 设备

`AoqAudioDeviceRouteBluetooth`

`6`

蓝牙设备

#### AoqAudioFileStateCode

音频文件播放状态码。

枚举值

值

说明

`AoqAudioFileNone`

`0`

无状态

`AoqAudioFileStarted`

`1`

播放已开始

`AoqAudioFileStopped`

`2`

播放已停止

`AoqAudioFilePaused`

`3`

播放已暂停

`AoqAudioFileResumed`

`4`

播放已恢复

`AoqAudioFileEnded`

`5`

播放已结束

`AoqAudioFileBuffering`

`6`

缓冲中

`AoqAudioFileBufferingEnd`

`7`

缓冲结束

`AoqAudioFileFailed`

`8`

播放失败

#### AoqCameraDirection

枚举值

值

说明

`AoqCameraDirectionFront`

`0`

优先前置

`AoqCameraDirectionBack`

`1`

优先后置

#### AoqVideoDeviceStateCode

视频设备状态码。

枚举值

值

说明

`AoqVideoDeviceNone`

`0`

无状态

`AoqVideoDeviceCaptureStarting`

`1`

采集启动中

`AoqVideoDeviceCaptureStarted`

`2`

采集已启动

`AoqVideoDeviceCaptureStopping`

`3`

采集停止中

`AoqVideoDeviceCaptureStopped`

`4`

采集已停止

`AoqVideoDeviceCaptureFail`

`5`

采集失败

#### AoqMirrorMode

预留镜像模式枚举；当前 Web 没有使用该枚举的配置项或接口。

枚举值

值

说明

`AoqMirrorModeDisabled`

`0`

关闭镜像

`AoqMirrorModeEnabled`

`1`

开启镜像

#### AoqOrientationMode

预留方向模式枚举；当前 Web 没有使用该枚举的配置项或接口。

枚举值

值

说明

`AoqOrientationModeAuto`

`0`

自动

`AoqOrientationModePortrait`

`1`

竖屏

`AoqOrientationModeLandscape`

`2`

横屏

#### AoqRenderMode

视频画面适配方式。

枚举值

值

说明

`AoqRenderModeAuto`

`0`

默认等比完整显示

`AoqRenderModeStretch`

`1`

拉伸铺满容器

`AoqRenderModeFill`

`2`

等比完整显示，允许留黑边

`AoqRenderModeCrop`

`3`

等比铺满，裁剪超出部分

### 其他公开声明

`IAoqEngineEvents` 定义了 [事件回调](#web-events) 中的 10 个回调签名，其中 `onAudioFileState` 为预留事件。使用事件名订阅时可直接获得 TypeScript 参数推导。

以下类型或枚举虽由包入口导出，但当前 Web 门面没有对应控制/观察接口，不能按其他平台同名声明推断能力：

类别

公开声明

当前边界

音频文件混音

`AoqAudioFileMixConfig`、`AoqAudioFileState`、`AoqAudioFileStateCode`

无文件播放/混音控制方法，文件状态事件不触发

外部音频与观察

`AoqAudioExternalStreamConfig`、`AoqAudioExternalFrameMeta`、`AoqAudioObserverParams`、`AoqAudioSource`、`AoqAudioStreamDirection`

无外部音频输入或音频帧观察者注册方法

外部视频与观察

`AoqExternalVideoFrameMeta`、`AoqExternalVideoEncodedFrameMeta`、`AoqVideoObserverParams`、`AoqVideoSource`、`AoqVideoPixelFormat`、`AoqVideoObserverAlignment`、`AoqVideoCodecType`

无外部视频帧输入或视频帧观察者注册方法；实际编解码配置使用 `AoqEncoderType`

镜像与方向

`AoqMirrorMode`、`AoqOrientationMode`

无对应配置字段或方法；本地预览镜像由 SDK 自动处理

底层音频设备

`AoqAudioDeviceEvent`、`AudioDeviceApiError`、`AudioDeviceErrorCode`

底层设备声明，不是引擎新增事件或完整的门面返回码契约

`AOQ_TRACK_AUDIO` 和 `AOQ_TRACK_DATA` 分别为字符串常量 `'aoq_track_audio'`、`'aoq_track_data'`；不是传给连接或视图方法的 Track 选择参数，业务接口应使用 `AoqTrackType`。

错误和警告枚举保留了跨平台值，不保证所有值都会由当前 Web 实现产生。具体接口是否可用，以本文方法和其调用条件为准。
