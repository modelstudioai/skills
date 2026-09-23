# HappyOyster Android SDK API参考

HappyOyster Android SDK 入口为单例对象 HappyOyster ，除 initialize 、 updateToken 、 attachVideo 、 sendCommand 外，业务方法均为 suspend ，失败时抛出 SDKError 。

调用方 coroutine 被取消时，SDK 会取消该调用仍在进行的 HTTP 请求（如有），原样传播 `CancellationException`，不会转换为 `SDKError`。取消不代表服务端已经受理的请求会被回滚。

接入流程、安装、最佳实践见 [HappyOyster Android SDK 接入指南](raw/_short/happyoyster-android-sdk-integration-guide-0ec60cb58a01b74a.md)。

## 核心名词概念

**名词**

**含义**

**token**

**百炼网关 API Key**：由你的 App 通过 `updateToken(token)` 注入为 Bearer token。SDK 只保存最新一个，不持久化、不刷新；Key 变化后由你再次注入。网关要求包括 `startTravel` 在内的 SDK 请求均使用此 Bearer。Bearer Key 过期或无效时，SDK 抛出 `SDKError(101002)`；此时应重新获取并注入 Bearer Key（`updateToken`），而非重新换取 ticket。**安全建议**：客户端 Bearer 宜使用服务端签发的**短期 token**，而非将长期 API Key 打包进 App 或写入代码仓库。

**ticket**

**一次性体验凭证**：由你的服务端调用开放平台换取并下发给客户端，仅用于一次 `startTravel`；体验结束（正常或异常）后即失效，不可复用。ticket 级别的凭证错误由六位服务端 code 标识（如 `401010` = ticket 无效/过期，`401011` = ticket 已使用），SDK 原样透传。

## 环境要求

**项**

**要求**

minSdk

24（Android 7.0）及以上

compileSdk

36

语言

Kotlin（协程 `suspend` API）

ABI

`arm64-v8a` / `armeabi-v7a`（实时通信引擎含 native 库）

网络

需要可访问公网

## 核心概念

**概念**

**说明**

**World**

AI 世界，包含角色、场景。由你的服务端创建与管理。

**Travel**

一次实时体验。基本生命周期：`init → pending → running → completed`（失败为 `failed`）。在实时导演与角色演绎模式下，若体验支持暂停，`running` 可通过 `pauseTravel` 进入 `paused`，再通过 `resumeTravel` 回到 `running`（实时导演另可用 `rewindTravel` 回溯，回溯成功后服务端自动恢复）；`running ⇄ paused` 可多次循环。

**模式**

`adventure`（世界探索，设备/指令交互）、`directing`（实时导演，文本驱动剧情）或 `acting`（角色演绎，文本驱动剧情，播放画幅由服务端在创建时固定）。SDK 统一以这三个值对外。

**实时视频**

`startTravel` 成功后由 SDK **自动**建立与维护，无需你手动连接/断开；`endTravel` 时自动释放。

## 概览

### HappyOyster 方法

**方法**

**说明**

`initialize(context, config)`

初始化 SDK；允许在 idle 时重新初始化，Travel 正在 starting、active 或 ending 时重新初始化会以 `103004` 拒绝。

`updateToken(token)`

注入/更新百炼网关 API Key（Bearer token）。

`startTravel(ticket)`

用一次性凭证开始一次体验，自动建立实时视频连接。

`pauseTravel()`

异步暂停体验（实时导演与角色演绎，且体验支持暂停）；受理后真正暂停以 `onStatusChanged(Paused)` 为准。

`resumeTravel()`

恢复已暂停的体验（实时导演与角色演绎）；内部含 3× 重试退避。

`rewindTravel(rewindToSec)`

回溯到指定秒数（**仅实时导演**、状态为 paused）。秒数取 4 的整数倍。角色演绎 **不支持**回溯。

`sendInstruct(content)`

发送文本指令驱动剧情（实时导演与角色演绎，running 或 paused）。

`sendCommand(command)`

发送方向/视角/动作控制指令（世界探索模式，仅 running；主线程调用）。角色演绎不可用。

`attachVideo()`

返回播放用 `SurfaceView`，挂入布局即可渲染（主线程调用）。

`endTravel()`

结束体验，自动断开实时连接并释放全部会话资源。

`VERSION`

SDK 版本字符串（SemVer），编译期常量。

### 事件

**事件**

**说明**

`onStatusChanged(status)`

体验状态变化（含实时视频生命周期），值见 `TravelStatusValue`。

`onError(error)`

内部自动流程出错时回调；致命错误会同时终止本次体验。

### 关键数据类型

**类型**

**说明**

`SDKConfig`

SDK 初始化配置（`apiHost`、`model` 均必填，以及 `logLevel`、`logcatEnabled`、`logHandler`、`callbackTimeoutMs`）。

`TravelStatusValue`

体验状态：`Init` / `Pending` / `Running` / `Paused` / `Failed` / `Completed`。

`ModeValue`

体验模式：`adventure` / `directing` / `acting`。

`CreationModelValue`

世界创建模型：`Simple`（默认，instruct 驱动）/ `ScriptList`（结构化剧本，不支持 `sendInstruct`）。

`StartTravelData`

`startTravel` 返回，含 `mode`、`version`、`creationModel`、`aspectRatio`、`maxExperienceTimeSec` 等元数据。

`AdventureCommand`

`sendCommand` 参数，含 `translation` / `rotation` / `interaction` 三字段。

`SDKError`

SDK 错误，含 `code: Int` 与可选 `raw: Any?`。

## HappyOyster.initialize

初始化 SDK，应在调用其他 API 前完成（建议在 `Application.onCreate`）。`config` 为必填参数，须携带你账号的百炼 `apiHost`，并通过 `model` 指定拆分后的模型名（`happyoyster-1.0-directing` / `happyoyster-1.0-acting` / `happyoyster-1.0-adventure`，与所用 Open API 入口一致）。SDK 按以下规则拼接请求地址：

```
https://{apiHost}/api/v2/apps/{model}/openapi/v1/{endpoint}
```

`model` 没有默认值：构造 `SDKConfig` 时遗漏该参数会编译失败；传入空白值则 `initialize` 同步抛出 `SDKError(100002)`，且不会创建或替换 runtime，也不会发起网络请求。SDK 只持有 application context，不持有 Activity。仅当上一个 runtime 为 idle 时允许重新初始化；切换模型时须在 idle 状态使用新 `model` 重新初始化。若 Travel 正在 starting、active 或 ending，须先等待 `endTravel()` 完成。

**说明**

**地域合规提示：**

-   为支持适用法律法规及数据合规要求的落实，如您的目标用户包括美国用户，您必须在 SDK 初始化时为面向该等用户的服务配置美国地区 API Host。
-   开发者应确保配置正确，并依法承担因未按上述要求配置所产生的相应责任。

### 签名

```
fun initialize(context: Context, config: SDKConfig)
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

context

Context

是

建议传 `applicationContext`。

config

SDKConfig

是

SDK 配置，须携带必填且无默认值的 `apiHost` 与 `model`。

### 返回值

无返回值。

### 错误

**code**

**说明**

`100002`

`model` 为空白；初始化同步失败，`SDKError.raw` 为 `SDKConfig.model must not be blank`，不创建或替换 runtime，也不发起网络请求。

`103004`

Travel 正在 starting、active 或 ending，拒绝重新初始化。等待 `endTravel()` 后重试。

## HappyOyster.updateToken

注入/更新百炼网关 API Key，线程安全；在 `initialize` 后可随时调用。SDK 会将最新 token 用于 `startTravel` 及后续体验控制请求。`ticket` 是一次性体验凭证，不应和 Bearer token 混用。

### 签名

```
fun updateToken(token: String)
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

token

String

是

百炼网关 API Key，作为 Bearer token 使用。

### 返回值

无返回值。

### 错误

**code**

**说明**

`100001`

SDK 尚未初始化。

## HappyOyster.startTravel

用一次性 `ticket` 开始一次体验。成功后 SDK **自动建立实时视频连接并开始内部状态轮询**，状态通过 `onStatusChanged` 透出。

-   `ticket` 为一次性凭证，调用后即视为已消费。
-   同一 App 同一时刻只允许一个并发 Travel；已有体验进行中时再次调用会抛出 `SDKError(103004)`，`SDKError.raw` 中仅包含当前活跃 ticket 的脱敏摘要供诊断，不包含完整 ticket。
-   可选传入 `maxExperienceTimeSec` 限制本次体验最大时长（**仅世界探索 / adventure 模式生效**），详见参数。

`StartTravelData.creationModel`（`CreationModelValue`，默认 `CreationModelValue.Simple`）：指示该世界的创建模型，即剧本内容的管理方式。`simple`（默认）为普通 instruct 驱动的世界，世界探索类世界也会归一化为此值。`scriptlist` 为结构化 ScriptList 世界——剧本内容不通过本 SDK 访问。在 ScriptList 模式（`creationModel == CreationModelValue.ScriptList`）下调用 `sendInstruct` 会被拒绝，抛出 `SDKError(103002)`。该字段缺省值为 `simple`。

`StartTravelData.aspectRatio`（`String?`）：服务端为本次会话分配的播放画幅，形如 `width:height`。**仅角色演绎（acting）非空**——`"9:16"`（竖屏，服务端创建时的默认值）或 `"16:9"`（横屏）；世界探索与实时导演模式、以及服务端未下发时为 `null`。SDK 原样保留未知取值（不收敛为 `null`），宿主须把不认识的值等同 `null` 处理并回退到自己的默认方向；SDK 自身不消费该字段。

该值随 `startTravel()` 的返回值交付：请在 `startTravel()` 返回后、调用 `attachVideo()` 把返回的视图挂进布局**之前**据此确定播放容器方向——SDK 只有在宿主挂载视图后才开始绑定渲染远端流，所以此刻定方向仍赶在首帧渲染之前（但**不保证**发生在 SDK 加入实时房间之前）。远端视图以**裁剪填充**（clip-to-fill）方式绑定，容器方向与该值不一致会**裁掉画面**而不是留黑边。

### 签名

```
suspend fun startTravel(ticket: String): StartTravelData
suspend fun startTravel(ticket: String, maxExperienceTimeSec: Int?): StartTravelData
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

ticket

String

是

一次性体验凭证，由你的服务端下发。

maxExperienceTimeSec

Int?

否

本次体验的最大时长（秒），到时后世界侧自动结束会话。**仅世界探索（adventure）模式生效**，实时导演与角色演绎 忽略此值。合法取值由服务端配置，当前为 `60` / `90` / `120`；传 `null` 或使用不带该参数的重载时，采用服务端默认值（当前为 `60`）。传入不支持的值将由**服务端拒绝** `startTravel` 并返回 `400000`，此时抛出 `SDKError(400000)` 且不会建立活跃体验。SDK 不在本地校验取值，允许档位以服务端为准。

### 返回值

返回 `StartTravelData`，含体验元数据（`mode`、`version`、`creationModel`、`aspectRatio` 等）。先检视返回的元数据再决定如何互动（如 `travel.mode`、`travel.creationModel`、`travel.version`），角色演绎还需按 `travel.aspectRatio` 定播放容器方向。

### 错误

**code**

**说明**

`401010`

`ticket` 无效或已过期

`401011`

`ticket` 已被使用

`400000`

入参非法（如 `maxExperienceTimeSec` 取值不在服务端允许档位内），本次 `startTravel` 启动失败

`403002`

世界状态非就绪

`500001`

资源分配/服务内部失败

`103004`

已有 Travel 正在 starting、active 或 ending，或并发调用 `startTravel`（同一时刻只允许一个 Travel；`SDKError.raw` 仅含当前活跃 ticket 的脱敏摘要）

## HappyOyster.pauseTravel / HappyOyster.resumeTravel

暂停 / 恢复体验。SDK 同时只管理一个 Travel，`encryptedTravelId` 由 SDK 内部自动取得，调用方无需传入。

**前置条件**：

-   `pauseTravel`：仅**实时导演（directing）或角色演绎（acting）**、且状态为 `running` 时可调用。
-   `resumeTravel`：仅**实时导演（directing）或角色演绎（acting）**、状态为 `paused` 时可调用。

并非所有体验都支持暂停 / 恢复：体验须报告本模式要求的版本标识（`StartTravelData.version`，实时导演为 `storyV2`、角色演绎为 `actingV2`；比较时忽略首尾空白与大小写），否则 `pauseTravel` 与 `resumeTravel` 都返回 `103002`。角色演绎支持暂停 / 恢复，但 **不支持** `rewindTravel`。

**暂停是异步的（重要）**：`pauseTravel` 是一个「重」操作——调用成功（方法返回）只代表**暂停已受理**，此刻体验**还未真正暂停**。**只有当 `onStatusChanged` 回调报告 `paused` 时，才算真正暂停。**因此请以该回调驱动宿主状态机和调用门控：在「调用 `pauseTravel`」到「收到 `paused` 回调」之间可将本地状态标记为 `pausing`；收到 `paused` 后才允许发起 `resumeTravel` 或 `rewindTravel`。不要把 `pauseTravel` 的返回当作已暂停。

**实时连接的处理**：真正暂停后 SDK 会断开实时连接；恢复时 SDK 会用**同一次 startTravel 时下发的凭证**自动重新入会并恢复画面，无需宿主干预。

**暂停拆房有序屏障**：收到 `Paused` 后，服务端实时房间的拆除仍可能短暂滞后。SDK 会从暂停确认时刻起建立 3 s settle 窗口；窗口内调用 `resumeTravel` 或 `rewindTravel` 时，suspend 调用先非阻塞等待剩余时间，再发送会重新开房的 API。若收到 `Paused` 后已自然等待满 3 s，则不增加延迟。这样可避免迟到的 pause teardown 关闭刚重开的房间并触发 `105001`。

**resume API 重试**：`resumeTravel` 内部会在失败时最多重试 3 次（退避 1 s / 2 s / 3 s），以应对暂停后服务短暂不可用的情况；只有 3 次全部失败才会向上抛出错误。

**说明**建议宿主在 `resumeTravel` 返回成功后 3 s 内暂缓再次发起 `pauseTravel`，避免过于频繁的切换。此为宿主侧调用冷却建议，SDK 本身不强制。详见 [HappyOyster Android SDK 接入指南](raw/_short/happyoyster-android-sdk-integration-guide-0ec60cb58a01b74a.md)。

### 签名

```
suspend fun pauseTravel(): TravelStateData
suspend fun resumeTravel(): TravelStateData
```

### 参数

无参数。

### 返回值

返回 `TravelStateData`（含 `encryptedTravelId`、`status`）。

### 错误

**code**

**说明**

`103001`

无活跃体验

`103002`

状态不允许，或该体验不支持暂停 / 恢复

`103003`

在世界探索模式下调用，仅实时导演与角色演绎 支持暂停 / 恢复

## HappyOyster.rewindTravel

回溯到指定秒数。`encryptedTravelId` 由 SDK 内部自动取得。

**前置条件**：仅**实时导演（directing）模式**、且状态为 `paused` 时可调用（不允许在 `running` 状态下回溯）；并非所有实时导演体验都支持回溯，不支持时返回 `103002`。回溯成功后体验会自动恢复，SDK 会自动重连 RTC，无需宿主干预。

**角色演绎完全没有回溯能力**：在角色演绎下调用会被 SDK 在**本地**以 `103003` 拒绝，不发出任何请求。宿主在角色演绎下应**隐藏**回溯入口，而不仅是禁用按钮。

### 签名

```
suspend fun rewindTravel(rewindToSec: Double): RewindTravelData
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

rewindToSec

Double

是

回溯到的目标秒数，应为 **4 的整数倍**（如 4、8、12）。非 4 的整数倍由服务端向下取整到最近的较小 4 的倍数（如传 7 取 4）。

### 返回值

返回 `RewindTravelData`（含 `encryptedTravelId`、`status`、`resumedAtSec`）。其中 `resumedAtSec` 为服务端实际回溯到的秒数（已按 4 的整数倍向下取整）。

### 错误

**code**

**说明**

`103001`

无活跃体验

`103002`

状态不是 `paused`，或该体验不支持回溯

`103003`

在世界探索或角色演绎下调用，仅实时导演模式支持回溯

## HappyOyster.sendInstruct

发送文本指令驱动剧情，仅在**实时导演（directing）或角色演绎（acting）**且体验状态为 `running` 或 `paused` 时有效。`encryptedTravelId` 由 SDK 内部自动取得。

**paused 态行为**：SDK **不会**在 paused 时自动 resume，instruct 直接发送。由宿主决定是否先调用 `resumeTravel` 再发 instruct。

### 签名

```
suspend fun sendInstruct(content: String): SendInstructData
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

content

String

是

要发送的文本指令内容。

### 返回值

返回 `SendInstructData`（含 `encryptedTravelId`、`content`、`accepted`）。

### 错误

**code**

**说明**

`103001`

无活跃体验（未调用 `startTravel` 或已结束）

`103003`

当前模式非实时导演或角色演绎（在世界探索模式下调用）

`103002`

体验状态既不是 `running` 也不是 `paused`（如尚在 `init`/`pending` 阶段）；或当前世界处于 ScriptList 模式（`StartTravelData.creationModel == CreationModelValue.ScriptList`）——ScriptList 模式下不允许发送 instruct，剧本由百炼平台 API 管理

`403004`

内容安审拦截

`404000`

Travel 不存在

## HappyOyster.sendCommand

发送方向/视角/动作控制指令。仅在**世界探索模式**、`running` 时有效。

-   请在主线程调用；离主线程调用会同步抛出 `IllegalStateException`。
-   无活跃体验报 `103001`。
-   在**非世界探索模式**（实时导演 / 角色演绎）下调用会报 `103003`。
-   状态不允许报 `103002`。
-   上行通过一路**静音音频流**建立（SDK 不录制、不上传真实音频）；`RECORD_AUDIO` 并非 DataChannel 硬前置，为兼容各机型**建议**声明并授予（见 [HappyOyster Android SDK 接入指南](raw/_short/happyoyster-android-sdk-integration-guide-0ec60cb58a01b74a.md) § 安装 · 权限）。`105004` 表示实时通道未就绪 / 发送失败（如 DataChannel 连接中断或实时通道异常），不由缺少权限直接触发。

**内置 42 ms 节流（24fps，latest-wins）**：`sendCommand` 内部对 DataChannel 写入做了以 42 ms（约 24fps）为周期的节流。状态校验**同步、立即**执行并在非法调用时立即抛出；DataChannel 实际写入是异步节流的：若距上次发送已过 42 ms 则立即发出（首次立即发），否则将命令更新为最新值（latest-wins）并在当前 42 ms 周期结束时延迟发出一次。同一周期内多次调用等同于一次、以最后一次为准。这意味着宿主可以按游戏帧率高频调用 `sendCommand`，SDK 会稳定合并为约每 42 ms 一次上链，无需宿主手动限速。

**节流期间的发送失败**：节流 flush 是异步的，发送失败无法抛给调用方——错误会通过 `onError` 回调（非致命，`105004`）透出。Session 结束时 pending 的命令会被丢弃（不会在结束后发送）。

### 签名

```
fun sendCommand(command: AdventureCommand)
```

### 参数

**字段**

**类型**

**是否必填**

**描述**

command

AdventureCommand

是

含 `translation`、`rotation`、`interaction` 三字段的指令对象。

#### AdventureCommand 字段与取值

##### `translation` — 移动

前/左/后/右/斜向/静止。

**值**

**方向**

`W`

前

`A`

左

`S`

后

`D`

右

`W_A`

左前

`W_D`

右前

`S_A`

左后

`S_D`

右后

`None`

静止

##### `rotation` — 视角

上/下/左/右/斜向/无。

**值**

**方向**

`Mouse_Up`

上

`Mouse_Down`

下

`Mouse_Left`

左

`Mouse_Right`

右

`Mouse_Up_Left`

左上

`Mouse_Up_Right`

右上

`Mouse_Down_Left`

左下

`Mouse_Down_Right`

右下

`None`

无

##### `interaction` — 交互

跳跃/攻击/蹲下/冲刺/无。

**值**

**动作**

`Jump`

跳跃

`Attack`

攻击

`Squat`

蹲下

`Sprint`

冲刺

`None`

无

三字段彼此独立，各自对应一组互斥指令；斜向移动/视角使用**单个**组合值（如同时前+左发 `W_A`，而非同字段并发 `W` 与 `A`）。每次调用传入当前完整状态即可。

#### 最佳实践：单次动作 vs 持续动作

以 42 ms 周期为心智模型，区分两类用法：

**单次动作**（如点一下跳跃/攻击、走一步）：**调用一次即可**。SDK 会在最近的周期把它上链，动作即生效；无需持续发送，也无需补发 `None`。

```
// 跳一下
HappyOyster.sendCommand(AdventureCommand("None", "None", "Jump"))
```

**持续动作**（如按住持续移动、持续转视角）：**按住期间按帧持续调用**，SDK 每约 42 ms 上链一次，持续输出该指令，角色即持续动作；**松手时显式发送一次带 `None` 的指令**复位停止。SDK 不会自动代发 `None`——不持续调用就没有后续上链、动作会停下，但不发 `None` 就不会主动复位。

```
// 按住：每帧持续调用（宿主自行驱动帧循环）
HappyOyster.sendCommand(AdventureCommand("W", "None", "None"))
// 松手：显式复位一次
HappyOyster.sendCommand(AdventureCommand("None", "None", "None"))
```

### 返回值

无返回值（同步）。状态校验同步立即执行；DataChannel 写入异步节流。

### 错误

**code**

**说明**

`103001`

无活跃体验

`103002`

状态不允许

`103003`

在非世界探索模式（实时导演 / 角色演绎）下调用

`105004`（via `onError`）

节流 flush 发送失败（非致命，异步回调）

## HappyOyster.attachVideo

返回一个用于播放的 `SurfaceView`，由你加入布局；SDK 内部完成与远端流的渲染绑定。

-   请在主线程调用；离主线程调用会同步抛出 `IllegalStateException`。
-   SDK 对返回的 View 仅持弱引用，体验结束时释放渲染绑定；你需自行将 View 从布局移除。
-   角色演绎体验请先按 `StartTravelData.aspectRatio` 定好播放容器方向，再把返回的视图挂进布局：渲染以**裁剪填充**方式绑定，方向不符会裁掉画面（见 `startTravel`）。

### 签名

```
fun attachVideo(): SurfaceView
```

### 参数

无参数。

### 返回值

返回 `SurfaceView`，加入布局后即可播放实时视频。

### 错误

**code**

**说明**

`100001`

SDK 未初始化

## HappyOyster.endTravel

结束体验。`encryptedTravelId` 由 SDK 内部自动取得。调用成功（或异常退出）后，SDK **自动断开实时连接、停止内部轮询、释放全部会话资源**，本次 `ticket` 同时失效。

### 签名

```
suspend fun endTravel(): EndTravelData
```

### 参数

无参数。

### 返回值

返回 `EndTravelData`（含 `encryptedTravelId`、`status`、`endedAt`、`durationSec`）。

### 错误

**code**

**说明**

`100001`

SDK 未初始化

`103001`

无活跃体验

## HappyOyster.VERSION

返回 SDK 版本字符串（SemVer），如 `"x.y.z"`。该值是编译期常量，由 `VERSION_NAME` Gradle 属性注入；无需先调用 `initialize` 即可安全读取。

### 签名

```
val VERSION: String
```

### 返回值

SDK 版本字符串，如 `"x.y.z"`。

```
Log.d("MyApp", "SDK version: ${HappyOyster.VERSION}")
```

## 事件监听

```
interface HappyOysterListener {
    fun onStatusChanged(status: TravelStatusValue) {}
    fun onError(error: SDKError) {}
}

fun addListener(listener: HappyOysterListener)
fun removeListener(listener: HappyOysterListener)
```

SDK 事件是对你的**主动推送通道**，用于回调那些非你主动调用触发的情况（如 SDK 内部自动维护的实时连接或状态轮询出现问题）。

**事件**

**说明**

`onStatusChanged`

体验状态变化（含实时视频生命周期），值见 `TravelStatusValue`。

`onError`

内部自动流程出错时回调；致命错误会同时终止本次体验（见错误码节）。

**说明**`addListener` / `removeListener` 必须在 `initialize` 之后调用；在初始化前调用会抛出 `SDKError(100001)`。建议在 `HappyOyster.initialize(...)` 成功返回后立即注册监听器。

## 数据模型

```
// 配置
data class SDKConfig(
    // 必填：你账号的百炼 API Host（如 llm-xxxx.cn-beijing.maas.aliyuncs.com），百炼控制台 API Key 页复制；
    // 须与注入的 API Key 同账号/区域，否则网关返回 AccessDenied。
    val apiHost: String,
    // 必填且无默认值：包含版本的完整 HappyOyster 模型名称（如 happyoyster-1.0-directing）；
    // 可用值以百炼官方 HappyOyster 系列模型文档为准。
    val model: String,
    // 内置 Logcat 输出的最低等级（不影响 logHandler）；默认 INFO，含重建会话时间线所需的
    // 生命周期锚点（初始化、Travel 起止/状态、RTC 入会/首帧）。仅需报错可降为 WARN，排障可升到 DEBUG/VERBOSE。
    val logLevel: LogLevel = LogLevel.INFO,
    // RTC 入会（超时触发 105002）、首帧等待（超时触发 105003）与 SDK 网关 HTTP 信令调用（超时触发 105005）的超时；
    // 两个 RTC 阶段串行，最坏等待 2×callbackTimeoutMs（60s）。
    val callbackTimeoutMs: Long = SDKConfig.DEFAULT_CALLBACK_TIMEOUT_MS, // 30_000ms
    // SDK 是否将自身日志写入 Android Logcat（tag HappyOysterSDK）；默认 false（静默）。
    val logcatEnabled: Boolean = false,
    // 宿主日志回调；接收全量 SDK LogRecord，不受 logLevel 影响；默认 null。
    val logHandler: HappyOysterLogHandler? = null,
) {
    companion object {
        /** 默认回调超时（毫秒）。公开常量，可用于对比或显示。 */
        const val DEFAULT_CALLBACK_TIMEOUT_MS: Long = 30_000
    }
}

enum class LogLevel { VERBOSE, DEBUG, INFO, WARN, ERROR, NONE }

// 宿主日志接收器；通过 SDKConfig.logHandler 注入；全量 firehose，不受 logLevel 影响。
fun interface HappyOysterLogHandler {
    fun onLog(record: LogRecord)
}

// SDK 结构化日志记录；交付给 HappyOysterLogHandler；不含敏感值（Bearer / ticket / RTC token、
// RTC 标识与媒体 URL 均已脱敏）。travelId（encryptedTravelId）保留全值,可用于与服务端会话日志对账。
data class LogRecord(
    val level: LogLevel,
    val tag: String,        // 固定为 "HappyOysterSDK"
    val message: String,    // 可读日志行（含事件名与详情）
    val throwable: Throwable?,
    val timestampMs: Long,  // 发出时的 epoch 毫秒
)

// 状态与模式（保留未知值，便于服务扩展）
@JvmInline value class TravelStatusValue(val rawValue: String) {
    companion object {
        val Init = TravelStatusValue("init")
        val Pending = TravelStatusValue("pending")
        val Running = TravelStatusValue("running")
        val Paused = TravelStatusValue("paused")
        val Failed = TravelStatusValue("failed")
        val Completed = TravelStatusValue("completed")
    }
}
@JvmInline value class ModeValue(val rawValue: String) {
    companion object {
        val Adventure = ModeValue("adventure")
        val Directing = ModeValue("directing")
        val Acting = ModeValue("acting")
    }
}
@JvmInline value class CreationModelValue(val rawValue: String) {
    companion object {
        val Simple = CreationModelValue("simple")         // 默认；prompt/instruct 驱动，世界探索类世界归一化为此值
        val ScriptList = CreationModelValue("scriptlist") // 结构化 ScriptList 世界；不支持 sendInstruct（抛 103002）
    }
}

// startTravel 返回
data class StartTravelData(
    val encryptedTravelId: String, // 后续控制接口的标识
    val encryptedWorldId: String,
    val mode: ModeValue,           // adventure / directing / acting
    val creationModel: CreationModelValue = CreationModelValue.Simple, // 世界创建模型；Simple（默认）为 instruct 驱动，ScriptList 不支持 sendInstruct
    val playUrl: String?,
    val firstFrame: String?,       // 首帧图地址，可能异步产生
    val bgmUrl: String?,
    val version: String,           // 世界版本标识；角色演绎的 version 为 actingV2
    val aspectRatio: String? = null, // 仅角色演绎返回 9:16 / 16:9；其余模式 null。用于定播放器方向
    val maxExperienceTimeSec: Int? = null, // 服务端回显的本次最大体验时长（秒）；仅 adventure 非 null，directing / acting 为 null
)

// 控制接口参数与返回
data class AdventureCommand(
    val translation: String, // 移动：前/左/后/右/斜向（W_A 等）/静止
    val rotation: String,    // 视角：上/下/左/右/斜向（Mouse_Up_Left 等）/无
    val interaction: String, // 交互：跳跃/攻击/蹲下/冲刺/无
)
data class TravelStateData(val encryptedTravelId: String, val status: TravelStatusValue)
data class RewindTravelData(val encryptedTravelId: String, val status: TravelStatusValue, val resumedAtSec: Double)
data class EndTravelData(val encryptedTravelId: String, val status: TravelStatusValue, val endedAt: String, val durationSec: Int)
data class SendInstructData(val encryptedTravelId: String, val content: String, val accepted: Boolean)

// 错误（以 code 标识，原始信息见 raw）
// 注意：SDKError 不是 data class（无 copy()/解构），是普通 class。
class SDKError(val code: Int, val raw: Any? = null) : Exception("Happy Oyster SDK error: $code")
```

## 错误码

错误以数字 `code` 标识。SDK 会透传可由调用方处理的业务错误码（常见为 `4xxxxx` / `5xxxxx`），本地 SDK 错误码为 `1xxxxx`。

### 业务错误码（常见）

**code**

**含义**

**建议处理**

`400000`

参数非法（枚举非法等）

检查请求参数或 SDK 版本

`401010`

`ticket` 无效或已过期

让服务端重新下发凭证

`401011`

`ticket` 已被使用

凭证一次性，重新下发

`403001`

World 不存在、已删除或不属于当前开发者（含 `startTravel` 凭证内世界已删除）

重新选择有效 World

`403002`

世界状态非就绪

等世界就绪后再开始

`403004`

输入内容违规（内容安审）；适用于 `sendInstruct` 文本指令

修改输入内容后重试

`403007`

当前规格未开通

**不可按容量满重试**；换已开通规格或联系开通

`403008`

容量配置暂不可用

稍后重试

`404000`

Travel 资源不存在或 ID 不归属当前账号

重新开始 Travel

`409000`

请求与当前资源状态冲突

检查 Travel 状态

`429001`

当前规格并发已满

等已有会话结束后重试（勿与 `500001` 混淆）

`429002`

当前可用容量不足

稍后重试

`500001`

推理资源分配/服务内部失败

稍后重试

`500000`

系统内部错误

稍后重试 / 反馈

### 客户端本地错误码

**说明**「是否致命」专指**是否触发 SDK 自动终止本次体验**：

-   `100001` / `100002` / `103xxx` 这类同步校验错误只会拒绝/抛出该次调用（`100002` 直接使初始化失败），不会终止体验。
-   SDK 自动终止本次体验分为四类：① 内部轮询读到 `failed`；② 实时连接致命（`105001` / `105002` / `105003`）；③ 无推流自动结束（`105006`）；④ SDK 被远程禁用（`108001`）。

**code**

**含义**

**是否致命**

**建议处理**

`100001`

SDK 未初始化即调用

调用拒绝

先 `initialize`

`100002`

SDK 初始化时 `model` 为空白；同步抛出，`SDKError.raw` 为 `SDKConfig.model must not be blank`，不会创建或替换 runtime，也不会发起网络请求

初始化失败

传入非空的完整模型名称及版本后重新 `initialize`；可用值以百炼官方 HappyOyster 系列模型文档为准

`101001`

未注入百炼网关 API Key

否

`updateToken` 后重试

`101002`

百炼网关 Bearer API Key 已过期或被拒绝。**注意**：这是网关 Bearer Key，不是一次性 ticket；ticket 级别的凭证错误由六位服务端 code 标识（如 `401010`/`401011`）

否

重新获取 Bearer Key 后 `updateToken`，无需重新换取 ticket

`103001`

当前无活跃体验

调用拒绝

先 `startTravel`

`103002`

当前状态不允许该操作（含：状态不符、`pauseTravel`/`resumeTravel`/`rewindTravel` 的体验不支持暂停 / 恢复 / 回溯（`version` 不是本模式要求的 v2 标识）、`rewindTravel` 时状态非 `paused`、`sendInstruct` 时 `creationModel == ScriptList`）

调用拒绝

检查体验状态与模式；ScriptList 模式（`creationModel == CreationModelValue.ScriptList`）下不可用 `sendInstruct`，剧本内容不通过本 SDK 管理

`103003`

模式不匹配：实时导演或角色演绎 下调用了 `sendCommand`，或世界探索模式下调用了 `pauseTravel` / `resumeTravel` / `rewindTravel` / `sendInstruct`，或角色演绎下调用了 `rewindTravel`

调用拒绝

检查当前模式是否匹配接口要求

`103004`

并发调用 `startTravel`，或 Travel 正在 starting、active、ending 时重新初始化（同一时刻只允许一个 Travel；并发 start 的 `SDKError.raw` 仅含 ticket 脱敏摘要）

调用拒绝

等待 `endTravel()` 后重试

`105001`

实时连接失败

是

结束并重新开始

`105002`

实时入会超时

是

结束并重新开始

`105003`

等待视频首帧超时

是

结束并重新开始

`105004`

实时通道未就绪/发送失败（如 DataChannel 连接中断或实时通道异常）

否

确认实时通道已就绪，`running` 后重试 `sendCommand`；若个别机型异常，可尝试声明并授予 `RECORD_AUDIO`（见 [HappyOyster Android SDK 接入指南](raw/_short/happyoyster-android-sdk-integration-guide-0ec60cb58a01b74a.md) § 安装 · 权限）

`105005`

SDK 网关 HTTP 信令调用在 `callbackTimeoutMs` 内未返回（默认 30s）；RTC 入会与首帧等待超时分别使用 `105002` / `105003`

否

建议重试，或调大 `callbackTimeoutMs`

`105006`

无推流自动结束：首帧从未到达，或运行中推流中断且超时未恢复。SDK 会主动结束本次体验

是

结束并重新开始

`106001`

本地网络错误

否

可重试

`106002`

响应解析失败

否

用户主动调用时抛给调用方；内部状态轮询时仅 `onError`、不终止体验

`106003`

上游服务返回无法识别的错误响应，SDK 已将原始信息保留在 `SDKError.raw`（含网关边缘拒绝，如 `AccessDenied`）

否

可重试；若持续出现，结合 `raw` 排查服务可用性。**若 `raw` 含 `AccessDenied`（多见于初始化后首次请求）**，属网关配置问题，按序排查：① `model` 名称与版本是否正确、是否已下线、是否已发布及授权；② `apiHost` 拼写；③ `apiHost`、`model` 与 `updateToken` 注入的 Key 是否属于匹配的账号和区域；④ 账号是否已加入应用白名单

`108001`

SDK 被远程禁用（整体关停或版本过低）；原因在 `SDKError.raw`（String）

是（SDK 感知到禁用结果时会自动结束进行中的体验；恢复后可重新开始）

按 `raw` 中的原因提示用户；版本过低时引导升级

### 致命 vs 非致命

**致命错误**：SDK 会自动终止本次体验（断开实时连接、释放资源、调用 `endTravel`），并通过 `onError` 透出；宿主应清理本次体验状态并允许重新开始。共四类：

-   ① 内部状态轮询读到体验状态 `failed`（如 `500001` 推理失败）
-   ② 实时连接致命（`105001` / `105002` / `105003`）
-   ③ 无推流自动结束（`105006`：首帧从未到达，或运行中推流中断且超时未恢复，SDK 主动结束）
-   ④ SDK 被远程禁用（`108001`）

**非致命错误**：不终止体验，仅通过 `onError` 透出；你可重新 `updateToken` 或等待服务 / 实时通道恢复后继续。**内部状态轮询自身的单次请求失败**（网络 `106001`、解析 `106002`、上游异常 `106003`、业务错误 `5xxxxx`）属于此类——轮询会在下一周期继续，只有它读到状态 `failed` 才会结束体验；鉴权失败 `101001`、`sendCommand` 节流 flush 的异步发送失败 `105004` 同样为非致命。注：SDK 不会自行向实时通道发送任何保活报文，因此空闲期不会出现 `105004`——该错误只可能由你主动调用 `sendCommand` 触发。
