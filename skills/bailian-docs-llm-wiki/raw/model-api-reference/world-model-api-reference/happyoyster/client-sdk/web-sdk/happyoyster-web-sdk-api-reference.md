# HappyOyster Web SDK API参考

HappyOysterEngine 负责配置 Open Platform host 与模型、更新百炼临时 API Key token，并创建 Travel 会话。 Travel 是 createTravel() 返回的会话对象，调用 travel.start() 后才会进入并启动会话。

## 核心名词概念

**名词**

**含义**

**备注**

**token**

**百炼临时 api-key token：**在浏览器、移动 App 等不可信环境中调用百炼模型服务时，通过安全的后端服务生成临时 API Key，避免永久 API Key 泄露。SDK 以 HTTP Bearer 方式携带该 token 请求 Open Platform。

[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)

**ticket**

**HappyOyster 世界体验凭证：**三方服务端通过 AK 鉴权（网关 Header）调用此接口，换取一个短时效的体验凭证（`ticket`），供客户端进入房间使用。此接口完成世界归属校验，不创建实际 Travel 记录。

[获取鉴权凭证](raw/model-api-reference/world-model-api-reference/happyoyster/happyoyster-quick-start/happyoyster-auth-setup.md)

## 方法概览

本 SDK 主要对象如下：

### HappyOysterEngine

**API**

**描述**

`new HappyOysterEngine(config)`

创建 Engine 实例。

`updateToken(token)`

更新后续 Open Platform API 请求使用的百炼临时 api-key token。

`createTravel(config)`

创建一次 Travel 会话。

`HappyOysterEngine.version`

当前 SDK 版本号。

`HappyOysterEngine.metadata`

当前 SDK 包名、版本和包渠道。

### Travel

**API**

**描述**

`start()`

启动当前 Travel 会话。

`on("statusChanged", handler)`

订阅会话状态变化。

`on("firstFrameGenerated", handler)`

订阅首帧 URL 生成通知。

`on("travelInfoReady", handler)`

订阅进入会话后即可获得的会话元信息。

`onError(handler)`

订阅会话运行时错误。

`can(action)`

判断当前是否可以调用指定动作。

`getInfo()`

获取已返回的会话元信息；尚未返回时为 `null`。

`sendCommand(params)`

发送实时操控指令。

`sendInstruct(params)`

发送实时导演或提示词内容。

`pause()`

暂停当前会话。

`resume()`

恢复已暂停的会话。

`rewind(params)`

将 Directing 会话回退到指定秒数。

`end()`

结束当前会话并释放相关资源。

### 其他导出

**导出**

**描述**

`ErrorCode`

SDK 对外暴露的错误码常量对象。

`isSdkError(error)`

判断未知错误是否为 SDK 标准错误。

Types

`SDKConfig`、`Travel`、`StartTravelResult`、`AdventureCommand` 等公开类型。

## 示例

```
import { HappyOysterEngine, isSdkError } from '@happy-oyster/js-sdk'

const engine = new HappyOysterEngine({
  APIHost: 'open-platform.example.com',
  model: 'happyoyster-1.0-adventure', // 必填；此处以 Adventure 模型为例
  token: 'bailian-temporary-api-key-token',
  logLevel: 'warn',
  streamReadyTimeout: 15_000,
})

const videoElement = document.getElementById('player') as HTMLVideoElement
const travel = engine.createTravel({
  ticket: 'travel-ticket',
  videoElement,
  maxExperienceTimeSec: 90,
})

const unsubscribeStatus = travel.on('statusChanged', (status) => {
  console.log('Travel status:', status)
})

const unsubscribeFirstFrame = travel.on('firstFrameGenerated', (firstFrame) => {
  console.log('First frame URL:', firstFrame)
})

const unsubscribeInfo = travel.on('travelInfoReady', (info) => {
  console.log('Travel info is ready before RTC playback:', info)
})

const unsubscribeError = travel.onError((error) => {
  console.error('Travel error:', error)
})

try {
  const { encryptedTravelId, mode, creationModel, firstFrame, maxExperienceTimeSec, aspectRatio } = await travel.start()

  // Adventure（模式 1）
  await travel.sendCommand({
    translation: 'Front',
    rotation: 'Mouse_Left',
    interaction: 'Jump',
  })

  // Directing（模式 2）或角色演绎（模式 3；非 scriptlist）
  await travel.sendInstruct({ content: '镜头转向城堡，主角开始奔跑' })

  await travel.pause()
  await travel.resume()
} catch (err) {
  if (isSdkError(err)) {
    console.error('SDK error:', err.code, err.message)
  } else {
    console.error('Unexpected error:', err)
  }
} finally {
  unsubscribeStatus()
  unsubscribeFirstFrame()
  unsubscribeInfo()
  unsubscribeError()
  await travel.end()
}

engine.updateToken('new-bailian-temporary-api-key-token')
```

## HappyOysterEngine

`HappyOysterEngine` 是 Web SDK 的入口对象，用于配置 Open Platform host、维护后续请求使用的百炼临时 api-key token，并创建 `Travel` 会话。

**说明**一个 Engine 实例同一时间只管理一个 active `Travel`（当前限制）。如果需要开始新的会话，请先结束当前 `Travel`。

设置 token（构造时或通过 `updateToken()`）后，SDK 内部会自动拉取功能开关（Feature Gate）。该能力用于远程关停 SDK 或强制升级旧版本；请求失败时 SDK 会 fail-open，不阻塞正常体验。

**API**

**描述**

`new HappyOysterEngine(config)`

创建 Engine 实例，配置必填的 API host、模型及可选的 token 和日志等级。

`updateToken(token)`

更新后续 Open Platform 请求使用的百炼临时 api-key token。

`createTravel(config)`

创建一次尚未启动的 Travel 会话。

## new HappyOysterEngine

创建一个 `HappyOysterEngine` 实例。

### 签名

```
new HappyOysterEngine(config: SDKConfig)
```

### 参数

#### SDKConfig

**字段**

**类型**

**是否必填**

**描述**

APIHost

string

是

Open Platform API host，必须是裸 host，例如 `open-platform.example.com`；不能包含 `https://`、协议头或路径。

model

string

是

要使用的 Open Platform 模型标识。必填，无默认值；在 Engine 创建时固定，其所有 Travel 共用此配置。

token

string

否

构造时设置的百炼临时 api-key token。也可之后通过 `updateToken()` 设置。

logLevel

LogLevel

否

SDK 日志等级，默认 `none`。

streamReadyTimeout

number

否

等待 `<video>` 可播放、停止或恢复的超时时间，单位毫秒，默认 `15000`。

`model` 应填写模型标识，例如 Adventure 模型 `happyoyster-1.0-adventure`；实际值应与目标服务环境一致。SDK 不会根据体验 `mode` 自动选择模型，也不会解析 ticket 推断模型。

一个 Engine 固定对应 `APIHost + model`，可复用于同一服务和模型的多次 Travel。切换任一配置前，先结束当前 Travel，再使用目标配置的 Engine；世界创建和 ticket 签发也应指向同一服务目标。

### 返回值

返回 `HappyOysterEngine` 实例。

### 错误

`config` 缺失，或 `APIHost`、`model`、`token`、`logLevel`、`streamReadyTimeout` 类型/取值不合法时，会同步抛出 `SdkError`，错误码为 `ErrorCode.INVALID_ARGUMENT`（`10010001`）。`APIHost` 传入完整 URL、空字符串或带路径的字符串都属于非法入参。

`model` 为必填项，必须是去除首尾空白后非空的字符串；`null`、非字符串和纯空白字符串均为非法值。省略或传 `undefined` 同样会报参数错误；SDK 不提供默认模型。

## updateToken

更新后续 Open Platform API 请求使用的百炼临时 api-key token。

### 签名

```
updateToken(token: string): void
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

token

string

是

百炼临时 api-key token。传入空白字符串会清空当前 token。

### 返回值

无返回值。

### 错误

`token` 不是字符串时，会同步抛出 `SdkError`，错误码为 `ErrorCode.INVALID_ARGUMENT`（`10010001`）。

## createTravel

创建一次 Travel 会话实例，但不启动会话。

### 签名

```
createTravel(config: CreateTravelConfig): Travel
```

### 参数

#### CreateTravelConfig

**字段**

**类型**

**是否必填**

**描述**

ticket

string

是

用于之后启动 Travel 的 ticket。

videoElement

HTMLVideoElement

是

用于渲染会话视频的 `<video>` 元素。须在创建 Travel 时传入。

maxExperienceTimeSec

60 | 90 | 120

否

Adventure 最大体验时间，单位秒；Directing 和角色演绎会忽略该字段，省略时由服务端使用默认值。

### 返回值

返回已创建但尚未启动的 `Travel` 会话对象。调用方需要再执行 `await travel.start()` 才会正式进入会话并等待视频可播放。

每个 `HappyOysterEngine` 实例同一时间只允许存在一个 active `Travel`。如需创建下一次 Travel，请先调用 `await travel.end()`。

### 错误

`createTravel()` 会在以下情况同步抛出 `SdkError`：

**ErrorCode**

**描述**

`10010001`

`config`、`ticket`、`videoElement` 或 `maxExperienceTimeSec` 不合法

`10010101`

当前已有进行中的 Travel，需先调用 `travel.end()`

启动阶段的错误由 `travel.start()` 暴露。

## Travel

`Travel` 表示一次由 `HappyOysterEngine.createTravel()` 创建的会话。创建后会话尚未启动，调用 `travel.start()` 后，SDK 会进入会话并等待视频可播放。

Travel 提供会话启动、暂停、恢复、回退、结束、实时操控指令和提示词发送能力，也提供状态变化和运行时错误订阅。

### 方法

**方法**

**描述**

`start()`

启动当前 Travel 会话。

`on("statusChanged", handler)`

订阅会话状态变化。

`on("firstFrameGenerated", handler)`

订阅首帧 URL 生成通知。

`on("travelInfoReady", handler)`

订阅进入会话后即可获得的会话元信息。

`onError(handler)`

订阅会话运行时错误。

`can(action)`

判断当前是否可以调用指定动作。

`getInfo()`

获取已返回的会话元信息；尚未返回时为 `null`。

`sendCommand(params)`

发送实时操控指令。

`sendInstruct(params)`

发送实时导演或提示词内容。

`pause()`

暂停当前会话。

`resume()`

恢复已暂停的会话。

`rewind(params)`

将当前会话回退到指定秒数。

`end()`

结束当前会话并释放相关资源。

### 状态

**状态**

**描述**

`idle`

会话尚未启动。

`prepare`

会话正在启动并等待视频可播放。

`running`

会话正在运行。

`paused`

会话已暂停，可继续恢复或回退。

`completed`

会话已正常结束并释放资源。

### 事件

通过 `travel.on(event, handler)` 订阅事件。订阅方法返回取消订阅函数。

**事件**

**回调**

**描述**

statusChanged

(status: TravelStatus) => void

会话状态变化。

firstFrameGenerated

(firstFrame: string) => void

在 `start()` 过程中，Open Platform 返回非空首帧 URL 时触发；早于 `start()` resolve 和视频可播放。

travelInfoReady

(info: TravelInfo) => void

enter-travel 返回后、RTC 连接前触发。可通过 `getInfo()` 读取同一份数据；若有首帧，随后仍会触发 `firstFrameGenerated`。

error

(error: unknown) => void

会话运行时错误。

## Travel.can

判断当前状态和会话能力下是否可以调用指定动作。

### 签名

```
can(action: TravelAction): boolean
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

action

TravelAction

是

要检查的动作：`start` / `sendCommand` / `sendInstruct` / `pause` / `resume` / `rewind` / `end`。

### 返回值

返回 `boolean`。`true` 表示当前可以调用该动作；`false` 表示当前状态、模式或会话能力不满足前置条件。

### 可用条件

**action**

**可用条件**

`start`

Travel 仍为 `idle`，未关闭，且尚未启动过。

`sendCommand`

`running` 且 Travel mode 为 Adventure（`1`）。

`sendInstruct`

`running` 或 `paused`，且 mode 为 Directing（`2`）或角色演绎（`3`），并且不是 `scriptlist`。

`pause`

`running`，且当前会话支持暂停。

`resume`

`paused`，且当前会话支持恢复。

`rewind`

`paused`，且为支持回退的 Directing 会话；角色演绎不支持。

`end`

Travel 未关闭。

### 错误

当前方法不会主动抛出业务错误；未知动作会返回 `false`。

## Travel.start

启动当前 Travel 会话。

### 签名

```
start(): Promise<StartTravelResult>
```

### 参数

无参数。

### 返回值

返回 `Promise<StartTravelResult>`。Promise 在会话启动完成、视频可播放后 resolve。

enter-travel 返回后，SDK 会在连接 RTC 前触发 `travelInfoReady`。晚订阅方可调用 `travel.getInfo()`；尚未返回时为 `null`。若响应中含非空 `firstFrame`，仍会紧随该事件触发 `firstFrameGenerated`。

#### StartTravelResult

**字段**

**类型**

**描述**

encryptedTravelId

string

当前 Travel 会话 ID。

mode

number

会话模式：`1` = Adventure（漫游），`2` = Directing（剧情），`3` = 角色演绎。

creationModel

string

世界创建模型，常见值为 `simple` 或 `scriptlist`。

firstFrame

string | null

首帧图片 URL；服务端未返回时为 `null`。

maxExperienceTimeSec

60 | 90 | 120 | null

Adventure 最大体验时间（秒）；Directing、角色演绎或服务端未返回该字段时为 `null`。

aspectRatio

"9:16" | "16:9" | null

角色演绎画幅；其他模式或服务端未返回该字段时为 `null`。

### 错误

`start()` 会在以下情况 reject，并触发 `error` 事件。可通过 `isSdkError(err)` 判断，并读取 `err.code` 与 `err.message`。

**ErrorCode**

**描述**

`10010002`

SDK 功能开关关闭（`SDK_FEATURE_DISABLED`）

`10020101`

无法启动：当前状态不允许、Open Platform 未配置，或进入会话失败

`10020102`

无法启动：服务端返回的会话配置不完整

`10020103`

无法启动：建立视频流连接失败，或 SDK 功能开关请求失败

`10020104`

无法启动：等待视频流就绪超时（取 `streamReadyTimeout` 与服务端 `noStreamAutoEndTimeoutSec` 的较大值）

`10020105`

无法启动：等待视频可播放超时（受 `streamReadyTimeout` 控制，默认 15 秒）

`10000001`–`10000012`

Open Platform 参数、资源或服务端错误

## Travel.on("statusChanged")

订阅会话状态变化。

### 签名

```
on("statusChanged", handler: (status: TravelStatus) => void): () => void
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

handler

(status: TravelStatus) => void

是

状态变化时调用的回调。

### 返回值

返回取消订阅函数。`TravelStatus` 取值为 `idle` / `prepare` / `running` / `paused` / `completed`。

### 错误

当前方法不会主动抛出业务错误。

## Travel.on("firstFrameGenerated")

订阅首帧 URL 生成通知。

### 签名

```
on("firstFrameGenerated", handler: (firstFrame: string) => void): () => void
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

handler

(firstFrame: string) => void

是

首帧 URL 可用时调用的回调。

### 返回值

返回取消订阅函数。

### 行为

仅在 `travel.start()` 过程中触发。SDK 调用 Open Platform enter-travel 并拿到非空 `firstFrame` 后立即 emit，通常发生在 `statusChanged("prepare")` 之后、`start()` resolve 和视频可播放之前。若响应未返回首帧 URL，则不会触发。

### 错误

当前方法不会主动抛出业务错误。

## Travel.onError

订阅会话运行时错误。

### 签名

```
onError(handler: (error: unknown) => void): () => void
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

handler

(error: unknown) => void

是

运行时错误发生时调用的回调。

### 返回值

返回取消订阅函数。错误对象可通过 `isSdkError` 收窄为 `SdkError`。

### 错误

当前方法不会主动抛出业务错误。

## Travel.sendCommand

发送实时操控指令。

### 签名

```
sendCommand(params: AdventureCommand): Promise<void>
```

### 参数

#### AdventureCommand

**字段**

**类型**

**是否必填**

**描述**

translation

string

否

移动方向。未传时按 `None` 发送。

rotation

string

否

视角旋转。未传时按 `None` 发送。

interaction

string

否

交互动作。未传时按 `None` 发送。

#### 控制指令参考

##### `translation` — 移动方向

描述角色的移动方向，支持 8 个方向及组合。

**值**

**方向**

`"Front"`

前

`"Back"`

后

`"Left"`

左

`"Right"`

右

`"Front_Left"`

左前

`"Front_Right"`

右前

`"Back_Left"`

左后

`"Back_Right"`

右后

`"None"`

静止

##### `rotation` — 视角旋转

模拟鼠标方向的视角转动，支持 8 个方向。

**值**

**方向**

`"Mouse_Up"`

上

`"Mouse_Down"`

下

`"Mouse_Left"`

左

`"Mouse_Right"`

右

`"Mouse_Up_Left"`

左上

`"Mouse_Up_Right"`

右上

`"Mouse_Down_Left"`

左下

`"Mouse_Down_Right"`

右下

`"None"`

无

##### `interaction` — 交互动作

**值**

**动作**

`"Jump"`

跳跃

`"Attack"`

攻击

`"Crouch"`

蹲下

`"Sprint"`

冲刺

`"None"`

无

### 返回值

返回 `Promise<void>`。指令提交完成后 resolve。

### 错误

`sendCommand()` 会在以下情况 reject：

**ErrorCode**

**描述**

`10010001`

`params`、移动、视角旋转或交互动作参数不合法

`10020501`

当前状态/会话模式不允许发送指令，或视频流侧指令发送失败

## Travel.sendInstruct

发送实时导演或提示词内容。

### 签名

```
sendInstruct(params: InstructData): Promise<void>
```

### 参数

#### InstructData

**字段**

**类型**

**是否必填**

**描述**

content

string

是

要发送的提示词内容。

### 返回值

返回 `Promise<void>`。Open Platform 接收并处理完成后 resolve。

### 错误

`sendInstruct()` 会在以下情况 reject，并触发 `error` 事件：

**ErrorCode**

**描述**

`10020101`

会话尚未启动

`10020601`

发送实时导演指令失败

`10000001`–`10000012`

Open Platform 参数、资源或服务端错误

## Travel.pause

暂停当前会话。

### 签名

```
pause(): Promise<void>
```

### 参数

无参数。

### 返回值

返回 `Promise<void>`。视频停止播放后 resolve。

### 错误

`pause()` 会在以下情况 reject：

**ErrorCode**

**描述**

`10020201`

当前状态、会话模式或会话能力不允许暂停，或暂停请求失败

`10020202`

等待 backend 上报视频流状态为 paused 超时（15 秒）

`10000001`–`10000012`

Open Platform 参数、资源或服务端错误

## Travel.resume

恢复已暂停的会话。

### 签名

```
resume(): Promise<void>
```

### 参数

无参数。

### 返回值

返回 `Promise<void>`。视频恢复可播放后 resolve。

### 错误

`resume()` 会在以下情况 reject：

**ErrorCode**

**描述**

`10020301`

当前状态、会话模式或会话能力不允许恢复，或恢复请求失败

`10020302`

等待视频恢复可播放超时（15 秒）

`10000001`–`10000012`

Open Platform 参数、资源或服务端错误

## Travel.rewind

将当前会话回退到指定秒数。

### 签名

```
rewind(params: RewindTravelParams): Promise<RewindTravelResult>
```

### 参数

#### RewindTravelParams

**字段**

**类型**

**是否必填**

**描述**

rewindToSec

number

是

要回退到的秒数，仅支持 4 的整数倍（如 `4`、`8`、`12`）。非整数倍由服务端向下取整（如传 `7` 取 `4`）。

### 返回值

返回 `Promise<RewindTravelResult>`。回退完成并恢复播放后 resolve。

#### RewindTravelResult

**字段**

**类型**

**描述**

resumedAtSec

number

服务端实际恢复播放的秒数。

### 错误

`rewind()` 会在以下情况 reject，并触发 `error` 事件：

**ErrorCode**

**描述**

`10020101`

会话尚未启动

`10020401`

无法回退：须先暂停且视频已停止播放，或回退请求/重连 RTC 失败

`10020402`

回退后等待视频恢复超时（15 秒）

`10000001`–`10000012`

Open Platform 参数、资源或服务端错误

## Travel.end

结束当前会话并释放相关资源。

### 签名

```
end(): Promise<void>
```

### 参数

无参数。

### 返回值

返回 `Promise<void>`。清理流程结束后 resolve。

### 错误

清理过程中的错误不会向调用方抛出；`end()` 会尽量完成资源释放。

## 错误处理

SDK 通过 Promise reject 或 `error` 事件暴露运行时错误。错误对象为 `SdkError`，可通过 `isSdkError(err)` 判断，并读取 `err.code` 与 `err.message`。

Open Platform 返回的可识别错误会映射到 `10000001`–`10000012` 区间；`err.message` 为平台返回的说明文案。各 Travel 方法特有的错误码见对应 API 的错误小节。

### ErrorCode 一览

错误码分段约定：

-   `100000xx`：Open Platform 映射错误
-   `1001xxxx`：Engine 客户端错误
-   `1002xxxx`：Travel 客户端错误

**code**

**name**

**描述**

`10000001`

`OPEN_PLATFORM_PARAM_INVALID`

请求参数无效（Open Platform 返回）

`10000002`

`OPEN_PLATFORM_RESOURCE_NOT_FOUND`

资源不存在（Travel 不存在 / 不归属 / 跨 workspace / 产物未就绪）

`10000003`

`OPEN_PLATFORM_WORLD_NOT_OWNED`

世界不存在、已删除或不属于当前开发者

`10000004`

`OPEN_PLATFORM_SYSTEM_ERROR`

系统错误

`10000005`

`OPEN_PLATFORM_TICKET_INVALID`

ticket 无效或已过期

`10000006`

`OPEN_PLATFORM_TICKET_USED`

ticket 已使用（一次性凭证）

`10000007`

`OPEN_PLATFORM_WORLD_NOT_READY`

世界状态非 ready，不可进入

`10000008`

`OPEN_PLATFORM_INFERENCE_ALLOCATE_FAILED`

推理资源分配失败（席位不足、推流创建失败、Session 初始化失败等）

`10000009`

`OPEN_PLATFORM_MAIN_API_KEY_REQUIRED`

当前接口仅允许主 API Key（临时 API Key 不可用）

`10000010`

`OPEN_PLATFORM_CONTENT_MODERATION`

输入内容违规（内容安审拦截）

`10000011`

`OPEN_PLATFORM_CONTENT_COPYRIGHT`

输入图片版权 / IP 违规

`10000012`

`OPEN_PLATFORM_STATE_CONFLICT`

请求与当前资源状态冲突

`10010001`

`INVALID_ARGUMENT`

SDK 客户端入参校验失败（非 Open Platform 映射）

`10010002`

`SDK_FEATURE_DISABLED`

SDK 功能开关关闭

`10010101`

`ACTIVE_TRAVEL_EXISTS`

已有进行中的 Travel

`10020001`

`STREAM_DISCONNECTED_WHILE_PLAYING`

播放中视频流断流

`10020101`

`START_REQUEST_FAILED`

启动会话请求失败

`10020102`

`START_RTC_CONFIG_MISSING`

启动时视频流配置缺失

`10020103`

`START_JOIN_CHANNEL_FAILED`

视频流连接失败

`10020104`

`START_REMOTE_USER_TIMEOUT`

等待视频流就绪超时

`10020105`

`START_STREAM_TIMEOUT`

等待视频可播放超时

`10020201`

`PAUSE_REQUEST_FAILED`

暂停请求失败

`10020202`

`PAUSE_STREAM_TIMEOUT`

等待视频暂停超时

`10020301`

`RESUME_REQUEST_FAILED`

恢复请求失败

`10020302`

`RESUME_STREAM_TIMEOUT`

等待视频恢复超时

`10020401`

`REWIND_REQUEST_FAILED`

回退请求失败

`10020402`

`REWIND_STREAM_TIMEOUT`

回退后等待视频恢复超时

`10020501`

`SEND_COMMAND_FAILED`

发送实时操控指令失败

`10020601`

`INSTRUCT_REQUEST_FAILED`

发送实时导演指令失败

`10020701`

`END_REQUEST_FAILED`

结束会话请求失败

## 其他导出

### Runtime exports

**导出**

**类型**

**描述**

`HappyOysterEngine`

class

SDK client，负责配置 Open Platform、更新 token 和创建 Travel。

`HappyOysterEngine.version`

string

当前 SDK 版本号。

`HappyOysterEngine.metadata`

SDKMetadata

当前 SDK 包名、版本和包渠道。

`ErrorCode`

const

SDK 对外暴露的错误码常量对象。

`isSdkError`

function

判断未知错误是否为 SDK 标准错误。

### ErrorCode

SDK 对外暴露的错误码常量对象。调用方可以用它和 `SdkError.code` 做稳定比较，避免在业务代码里散落数字字面量。

```
import { ErrorCode } from '@happy-oyster/js-sdk'
```

### isSdkError

判断未知错误是否为 SDK 标准错误。返回 `true` 后，TypeScript 会把错误收窄为 `SdkError`，可以安全读取 `code` 与 `message`。

```
isSdkError(error: unknown): error is SdkError
```
```
try {
  await travel.start()
} catch (err) {
  if (isSdkError(err) && err.code === ErrorCode.OPEN_PLATFORM_TICKET_INVALID) {
    // Request a new Travel ticket, then create a new Travel.
  }
}
```

## 公开类型

以下类型从 package entry 导出，可直接从 `@happy-oyster/js-sdk` 引入。它们只在 TypeScript 编译期存在，不会产生运行时代码。

**类型**

**描述**

`SDKConfig`

`HappyOysterEngine` 构造参数类型。

`LogLevel`

SDK 日志等级：`verbose` / `debug` / `info` / `warn` / `error` / `none`。

`SDKMetadata`

SDK 包元信息：`version`、`packageName`、`packageChannel`。

`SDKPackageChannel`

SDK 包渠道：`internal` / `public` / `unknown`。

`CreateTravelConfig`

`createTravel(config)` 的参数类型。

`StartTravelResult`

`start()` resolve 后返回的会话元信息。

`TravelInfo`

在 `travelInfoReady` 事件、`getInfo()` 和 `StartTravelResult` 中使用的会话元信息。

`TravelAspectRatio`

角色演绎画幅：`"9:16"` / `"16:9"`。

`Travel`

`createTravel()` 返回的 public session contract。

`TravelStatus`

SDK 本地会话状态：`idle` / `prepare` / `running` / `paused` / `completed`。

`TravelAction`

`can(action)` 支持的动作名。

`AdventureCommand`

`sendCommand(params)` 的参数类型。

`InstructData`

`sendInstruct(params)` 的参数类型。

`RewindTravelParams`

`rewind(params)` 的参数类型。

`RewindTravelResult`

`rewind(params)` resolve 后返回的数据类型。

`SDKError`

包含 `code` 和 `message` 的 SDK 错误形状。

`SdkError`

运行时 `Error` 与 `SDKError` 组合后的错误类型。

`ErrorCodeValue`

`ErrorCode` 对象中所有错误码值的联合类型。
