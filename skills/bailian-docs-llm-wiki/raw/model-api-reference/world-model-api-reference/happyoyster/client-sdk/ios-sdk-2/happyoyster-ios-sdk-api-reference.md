# HappyOyster iOS SDK API参考

HappyOyster iOS SDK 入口为进程级单例 HappyOysterEngine.shared ，业务方法均为 async throws ，失败时抛出 OysterSDKError 。一次体验由 OysterTravel 句柄承载，支持 UIKit 与 SwiftUI。

本文档是 HappyOyster iOS SDK 的**对外功能描述 + 接口细节参考**：逐个说明公开类型与方法的**参数、使用时机、用法与简单示例**。

**完整接入流程**（工程搭建、依赖配置、服务端配合、端到端跑通）见 [HappyOyster iOS SDK 接入指南](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/ios-sdk-2/happyoyster-ios-sdk-integration-guide.md)，本文不再重复。

## 核心概念

先建立几个名词，便于阅读后文。

**概念**

**说明**

**token**

**HTTP 鉴权 token（百炼临时 API Key）**。由你的服务端调用百炼接口换取后下发，经 `updateToken(_:)` 注入；SDK 以 HTTP Bearer 方式携带它请求网关。SDK 只保存最新一个，不持久化、不刷新，过期后由你重新换取并再次注入。

**ticket**

**一次性体验凭证**。由你的服务端调用开放平台 `get-travel-credential` 换取（前缀 `tk_`，有效期 **30 分钟**，一次性），作为 `createTravel(ticket:)` 入参；体验结束或过期后即失效，不可复用。

**World**

AI 世界，含角色、场景。由你的服务端创建与管理，SDK 不涉及。

**Travel**

一次实时体验，对应一个 `OysterTravel` 句柄。**单次使用**，到达终态后失效，需经 engine 重新 `createTravel`。

**会话状态**

`OysterTravelStatus`：`idle → prepare → running → pausing → paused`（paused 经重连回 `prepare → running`），外加两终态 `ended` / `failed`（详见"事件与状态"章节）。

**模式**

`adventure`（世界探索，方向/视角/动作指令）、`directing`（实时导演，文本驱动剧情）或 `acting`（角色演绎，文本驱动人物演绎）。`start()` 返回的 `mode` 据此决定 UI，各模式可用的接口见"概览"章节。

## 概览

集成本 SDK 后，你的 App 可进入由 AI 实时生成的「世界」，以**世界探索模式（adventure）**、**实时导演模式（directing）**或**角色演绎模式（acting）**进行实时互动视频体验：开始体验 → 实时播放 → 实时互动 → 过程控制（暂停/恢复/回溯/结束）→ 状态与错误回调。

各模式可用的能力不同，请按 `start()` 返回的 `mode` 决定 UI：

**能力**

**adventure**

**directing**

**acting**

`sendCommand`（方向/视角/动作）

支持

不支持

不支持

`sendInstruct`（文本指令）

不支持

支持

**支持**

`pause()` / `resume()`

不支持

支持

**支持**

`rewind(toSec:)`

不支持

支持

**不支持，请隐藏入口**

`end()`

支持

支持

支持

`start(maxExperienceTimeSec:)`

生效

忽略

忽略

**说明**`acting` 世界为竖屏优先：`start()` 返回的 `aspectRatio` 给出本次体验的画幅（`9:16` / `16:9`），建议在拉流前据此决定播放器方向与容器尺寸（见"数据模型"章节）。

`import HappyOysterSDK`，核心入口是两个类型。

**`HappyOysterEngine`** —— 编排入口，进程级单例 `HappyOysterEngine.shared`。

**方法 / 属性**

**说明**

`initialize(config:)`

初始化运行时并自动注册实时引擎（`createTravel` 前一次）

`updateToken(_:)`

注入 / 更新 HTTP 鉴权 token

`createTravel(ticket:)`

用一次性凭证创建会话句柄

`cleanup()`

释放资源（可再 `initialize`）

`version`

当前 SDK 版本号

**`OysterTravel`** —— 一次体验的会话句柄，由 `createTravel(ticket:)` 创建。

**方法 / 属性**

**说明**

`videoView` / `OysterVideoView(travel:)`

播放视图（UIKit / SwiftUI）

`events` / `status`

状态变更 + 错误推送流 / 可观察的当前状态

`start()` / `start(maxExperienceTimeSec:)`

建连播放（可选请求世界探索模式体验的最大时长）

`sendInstruct(content:)`

实时导演模式文本指令

`sendCommand(_:)` / `flushCommands()`

世界探索模式操控

`pause()` / `resume()`

暂停 / 恢复（`directing` 与 `acting` 支持）

`rewind(toSec:)`

回溯（仅 paused）

`end()`

结束（幂等，务必调用）

`pauseLocalAudioCapture()` / `resumeLocalAudioCapture()`

临时让出 / 恢复麦克风

此外还有几个辅助导出：`OysterLog` 用于接管 SDK 内部日志；`HappyOysterEngine.version` 读取版本号；`OysterVideoView` 是 SwiftUI 播放视图（与 `videoView` 等价）。用法见后文。

生命周期：**初始化 → 注入 token → 创建会话 → 挂载视频 + 订阅事件 → start 播放 → 互动 → end**。SDK 不负责世界的创建与管理（由你的服务端完成），也不暴露底层实时通信细节。

## 快速上手

一段从初始化到结束的完整流程，分步注释。各 API 的细节见"API 参考"章节。

```
import HappyOysterSDK

// 1) 初始化（App 启动后尽早，createTravel 前一次）
let engine = HappyOysterEngine.shared
engine.initialize(config: OysterConfig(
    apiHost: "[workspace-id].[region].maas.aliyuncs.com",// 网关地址获取参考百炼文档
    model: "happyoyster-1.0-adventure"                  // 已开通的模型名（含版本），必填；取值见 HappyOyster 系列模型文档
))

// 2)（可选）接管日志：设置等级 + 自定义打印
OysterLog.setMinimumLevel(.info)
OysterLog.setHandler { level, tag, message in
    print("[Oyster][\(level)][\(tag)] \(message)")
}

// 3) 注入 HTTP 鉴权 token（百炼临时 API Key，由你的服务端下发）
engine.updateToken(temporaryApiKey)

// 4) 用一次性 ticket 创建会话句柄（尚未建连）
let travel = try engine.createTravel(ticket: ticket)

Task { @MainActor in
    // 5) 挂载视频（UIKit；SwiftUI 用 OysterVideoView(travel:)）
    containerView.addSubview(travel.videoView)

    // 6) start 前就订阅事件，避免漏掉早期状态
    let eventTask = Task {
        for await event in travel.events {
            switch event {
            case .statusChanged(let status): render(status)   // 见"事件与状态"章节
            case .error(let error):          handle(error)     // 见"错误码"章节 error.code / error.kind
            }
        }
    }

    do {
        // 7) 建连播放
        let data = try await travel.start()

        // 8) 按模式互动：adventure 走操控指令，directing / acting 走文本指令
        if data.mode == .adventure {
            travel.sendCommand(OysterAdventureCommand(translation: .front))
        } else {
            _ = try await travel.sendInstruct(content: "突然下起了大雨")
        }
    } catch let error as OysterSDKError {
        handle(error)
    }

    // 9) 任意退出路径都收口到一次 end()
    _ = try? await travel.end()
    eventTask.cancel()
}

// 退出 SDK / 切换网关：await engine.cleanup()
```

**说明**工程搭建、依赖配置（含必须引入的 AliRTC 适配器与厂商二进制）、服务端配合与端到端跑通，见示例工程文档。

## 环境要求

**项**

**要求**

最低系统

iOS 15.0+（公开类型均标 `@available(iOS 15.0, *)`）

语言

Swift（`async/await`）

并发

主线程访问（入口类型标 `@MainActor`）

网络

需可访问公网

权限

`Info.plist` 须配 `NSMicrophoneUsageDescription`（见下）

**麦克风权限**：实时互动视频体验需要建立一条**双向（上行 + 下行）实时音视频通道**，因此 SDK 运行期间会占用本地麦克风——**这并非录音**。`Info.plist` 必须提供 `NSMicrophoneUsageDescription`，否则启动实时采集时会崩溃。当你需要独占麦克风（如语音识别）时，用 `pauseLocalAudioCapture()` / `resumeLocalAudioCapture()` 临时让出与恢复（见"OysterTravel"章节）。

## 引入与鉴权

### 引入与依赖

代码层面 `import HappyOysterSDK` 即可。SDK 以预编译二进制（xcframework）按 CocoaPods subspec 分发，已发布到 CocoaPods 公开 Trunk——在 `Podfile` 中声明依赖：

```
# HappyOysterSDK / AliVCSDK_ARTC 均发布在 CocoaPods 公开源。
pod 'HappyOysterSDK', '1.0.3'              # 聚合入口（Core + World）
pod 'HappyOysterSDK/UI', '1.0.3'           # 可选：默认 UI 组件（视频视图、操控 HUD）
pod 'HappyOysterSDK/StreamAliRTC', '1.0.3' # 视频流 + AliRTC 引擎适配器（已依赖 Stream）

# RTC 厂商二进制：SDK 弱引用、不随 SDK 分发，由集成方自行引入。
pod 'AliVCSDK_ARTC', '7.11.0'
```

**说明**引入 `HappyOysterSDK/StreamAliRTC` 时 **`AliVCSDK_ARTC` 为必需**：缺失时 SDK 会静默回落 Loopback——能连上、状态走到 `running`，但**黑屏不报错**。

工程搭建与端到端初始化流程由示例工程承担，见示例工程文档。本文聚焦接口本身。

### 鉴权模型

SDK **不获取、不刷新 token**，保持轻量。鉴权分两层，集成方负责生命周期管理：

1.  **HTTP 鉴权 token（百炼临时 API Key）**：由你的服务端调用百炼接口换取后下发，经 `updateToken(_:)` 注入。SDK 内部部分服务**直接调用百炼网关**，携带该 token 鉴权——因此它必须是百炼侧签发的临时 API Key，而非你自有业务服务的 token。SDK 只保存最新一个，不持久化、不刷新；过期后由你重新换取并再次注入。
2.  **一次性体验凭证** `ticket`：由你的服务端调用开放平台 `get-travel-credential` 换取（前缀 `tk_`，有效期 **30 分钟**，一次性），作为 `createTravel(ticket:)` 入参；体验结束（正常或异常）或过期后即失效，不可复用。

**说明**AK、签名密钥等高权限只存在于你的服务端，客户端 SDK 永不接触；客户端拿到的始终是短时效临时 API Key。

**说明****Feature Gate（远程开关 / 强制升级）**：服务端可远程关停 SDK 或设定最低支持版本。被禁用时，受控调用（`start` / `pause` / `resume` / `rewind` / `sendInstruct` / `sendCommand`）会拒绝并透出 `108001`，进行中的体验会被 SDK 主动终止（见"错误码"章节）；`OysterSDKError.raw` 里带可读的禁用原因，版本过低时请引导用户升级。

**处理 token 过期**：上述 HTTP 鉴权 token 过期后，需立即向你的服务端重新请求 token，再通过 `updateToken(_:)` 注入。有两处需判断 token 是否过期：

1.  调用 `engine.createTravel`、`travel.start` 等 API 时，处理 error，判断 token 过期/无效的 error 类型（`101001` / `101002`），注入新 token 后重新调用对应 API。
2.  监听 `OysterTravelEvent` 的 `.error` 事件时，判断 token 过期/无效的 error 类型，重新请求 token 并注入。

## API 参考

入口为两个类型，均 `@MainActor`、`@available(iOS 15.0, *)`。业务方法为 `async throws`，失败抛 `OysterSDKError`；有返回值的方法均标 `@discardableResult`。

### HappyOysterEngine

进程级单例，编排入口。`init` 非 public——统一用 `HappyOysterEngine.shared`，不要自行实例化（底层实时引擎也是进程单例）。

```
@MainActor @available(iOS 15.0, *)
public final class HappyOysterEngine {
    public static let shared: HappyOysterEngine            // 进程级唯一实例
    public static let version: String                      // 当前 SDK 版本号

    @discardableResult
    public func initialize(config: OysterConfig) -> Bool   // 初始化（createTravel 前一次）
    public func updateToken(_ token: String)               // 注入/更新 HTTP 鉴权 token
    public func createTravel(ticket: String) throws -> OysterTravel  // 用一次性凭证创建会话句柄
    public func cleanup() async                            // 释放资源（可再 initialize）
}
```

#### initialize(config:)

初始化运行时并**自动注册实时引擎**（无需宿主手动注册）。

**使用时机**：`createTravel` 前调用一次，App 启动后尽早调用。

**注意**：空闲时再调即以新 config 重新装配（换 `apiHost` / `model` 都不必先 `cleanup()`，已注入的 token 保留）；仅当有进行中的 Travel 时为 no-op 并告警，需先 `end()`。config 非法时保持现状，已生效的运行时不受影响。

##### 签名

```
@discardableResult
public func initialize(config: OysterConfig) -> Bool
```

##### 返回值

`Bool` —— 本次传入的 `config` 是否已生效。`false` 有两种情况：config 非法（`apiHost` / `model` 为空或拼不出合法网关 URL），或有进行中的 Travel 导致本次调用被忽略；两种情况下运行时都保持原状。

**说明****换 config 时不要用 `isReady` 判断成败**：重新 `initialize` 若被拒，之前那份 config 仍在生效，`isReady` 照样是 `true`。`isReady` 回答"引擎现在可用吗"，本返回值回答"我刚传的这份 config 生效了吗"。

##### 参数

**字段**

**类型**

**是否必填**

**描述**

`config`

`OysterConfig`

是

`config.apiHost` 是**百炼网关地址，不是你的业务服务器**，**必填**；预发/试用环境必须显式传入对应网关，否则请求失败（如 `106001` 域名无法解析）。`config.model` 是**已开通的模型名（含版本）**，同样**必填、无默认值**——HappyOyster 按模式拆成了不同子模型，SDK 无从推断该用哪个。两者须与注入的 token **同账号、同区域、成套**使用。其余字段见"数据模型"章节 `OysterConfig`。

**说明****模型与 `mode` 一一对应**：按模式拆分后，每个模型是一条独立的网关路由，**一次 `initialize` 只服务一种 `mode` 的世界**。若你的 App 同时提供多种模式的世界，在进入不同模式的世界前用对应模型再 `initialize()` 一次即可——空闲时以最新 config 为准，不需要 `cleanup()`，已注入的 token 也保留；有进行中的 Travel 时该调用被忽略，需先 `end()`。模型与世界 `mode` 不匹配时，网关以 `AccessDenied` 拒绝并归一为 `106003`。

#### OysterLog

配置并接管 SDK 内部的日志，打印到你自己的日志模块中。提供 `setMinimumLevel(_:)` 设置等级、`setHandler(_:)` 自定义打印（见"快速上手"示例）。

#### updateToken(\_:)

注入 / 更新 HTTP 鉴权 token（百炼临时 API Key，见"鉴权模型"章节）。

**使用时机**：`initialize` 之后、可随时调用；token 过期或收到鉴权类错误（`101001` / `101002`）后重新换取并再次调用。

**注意**：未 `initialize` 时为 no-op 并告警。

##### 签名

```
public func updateToken(_ token: String)
```

##### 参数

**字段**

**类型**

**是否必填**

**描述**

`token`

`String`

是

HTTP 鉴权 token（百炼临时 API Key，见"鉴权模型"章节）。

#### createTravel(ticket:)

用一次性 `ticket` 创建一次会话句柄。

**使用时机**：每次开始新体验前调用；返回的句柄**尚未建连**，需再调 `travel.start()`。视频从返回句柄取（见"OysterTravel"章节）。

**注意**（同步 `throws`）：未 `initialize` 抛 `100001`；上一个 Travel 未 `end()` 前再次调用抛 `103004`（每个 engine 同时只允许一个 active Travel）。

##### 签名

```
public func createTravel(ticket: String) throws -> OysterTravel
```

##### 参数

**字段**

**类型**

**是否必填**

**描述**

`ticket`

`String`

是

一次性凭证，创建后即视为本次体验占用。

##### 返回值

返回 `OysterTravel` 会话句柄；**尚未建连**，需再调 `start()`。

##### 错误

**code**

**说明**

`100001`

未 `initialize`

`103004`

上一个 Travel 未 `end()` 前再次调用（每个 engine 同时只允许一个 active Travel）

#### cleanup()

释放 SDK 资源（结束 active travel、运行时配置、token）。

**使用时机**：彻底退出 SDK 或需要更换 `config` 时。

**注意**：`async`——内部先确定性地 `end()` 当前 active travel，再拆运行时，不留 fire-and-forget。释放后可再次 `initialize`。

##### 签名

```
public func cleanup() async
```

### OysterTravel

由 `createTravel` 创建的会话句柄；**单次使用**，到达终态（`end` / 服务端结束 / 失败）后失效，需经 engine 重新 `createTravel`。同时是 `ObservableObject`（`@Published status`，可直接驱动 SwiftUI）。

```
@MainActor @available(iOS 15.0, *)
public final class OysterTravel: ObservableObject {
    @Published public private(set) var status: OysterTravelStatus   // 当前对外状态（可观察）
    public var isEnded: Bool { get }                                // 是否已到达终态（同步可读）
    public var videoView: UIView { get }                            // UIKit 播放视图；SwiftUI 用 OysterVideoView(travel:)
    public var events: AsyncStream<OysterTravelEvent> { get }       // 状态变更 + 错误，多订阅

    @discardableResult public func start() async throws -> OysterStartTravelData   // 建连播放
    @discardableResult public func start(maxExperienceTimeSec: Int?) async throws -> OysterStartTravelData  // 建连播放 + 请求最大体验时长（仅世界探索模式）
    @discardableResult public func pause() async throws -> OysterTravelStateData   // 暂停（directing / acting）
    @discardableResult public func resume() async throws -> OysterTravelStateData  // 恢复
    @discardableResult public func rewind(toSec: TimeInterval) async throws -> OysterRewindTravelData  // 回溯（仅 paused）
    @discardableResult public func end() async throws -> OysterEndTravelData       // 结束（幂等，务必调用）
    @discardableResult public func sendInstruct(content: String) async throws -> OysterSendInstructData  // 实时导演模式文本指令

    public func sendCommand(_ command: OysterAdventureCommand)      // 世界探索模式操控（fire-and-forget）
    public func flushCommands()                                     // 松键时补发最后一帧
    public func pauseLocalAudioCapture() async                      // 临时让出麦克风
    public func resumeLocalAudioCapture() async                     // 恢复麦克风占用
}
```

#### videoView / OysterVideoView(travel:)

远端画面渲染入口，「SDK 出视图、宿主摆放」。UIKit 取 `travel.videoView`；SwiftUI 用 `OysterVideoView(travel:)`。

**使用时机**：句柄创建后即可取（多次访问返回同一视图），挂进任意层级，引擎就绪**自动渲染**，`start()` 前后挂载均可、不黑屏。

**注意**：会话结束时 SDK 自动释放渲染绑定，你按需把视图移出层级。

##### 签名

```
public var videoView: UIView { get }
```

#### events / status / isEnded

`events` 是状态变更 + 错误的推送流；`status` 是可观察的当前对外状态；`isEnded` 同步可读是否终态。

**使用时机**：`events` 建议在 `start()` **之前**就开始消费，避免漏掉早期状态。

**注意**：每次访问 `events` 返回一条独立流，支持多订阅；取消订阅 = 结束 `for await` 迭代（或销毁持有的 `Task`）。SwiftUI 可直接 `@StateObject`/`@ObservedObject` 观察 `status`（错误仍走 `events`）。详见"事件与状态"章节。

##### 签名

```
@Published public private(set) var status: OysterTravelStatus
public var isEnded: Bool { get }
public var events: AsyncStream<OysterTravelEvent> { get }
```

#### start() / start(maxExperienceTimeSec:)

用 create 时捕获的 `ticket` 换取 travel + RTC 入会配置并建连播放。成功后 SDK **自动建立实时连接并开始内部状态轮询**，状态经 `events` 透出。

**注意（无推流自动结束）**：服务端下发「无推流超时」（默认约 30s）。若建连后在该时长内仍未收到推流（迟迟不进 `running`），SDK **自动结束本次体验**，状态转 `failed`、经 `events` 的 `.error` 透出 **`105006`**（致命，按回到开始前界面处理，无需自行计时）。

##### 签名

```
@discardableResult public func start() async throws -> OysterStartTravelData
@discardableResult public func start(maxExperienceTimeSec: Int?) async throws -> OysterStartTravelData
```

##### 参数

**字段**

**类型**

**是否必填**

**描述**

`maxExperienceTimeSec`

`Int?`

否

（可选）——请求本次**世界探索（adventure）体验的最大持续时长（秒）**。参数原样发给服务端，**允许值、实际生效时长与到期自动结束时机均由服务端决定**，SDK 不做本地校验；传 `nil`（或调用无参 `start()`）时使用服务端默认时长。**实时导演（directing）模式忽略该参数**。到期后由服务端结束体验，宿主经 `events` 收到 `ended` 终态（同服务端主动结束，见"事件与状态"章节）。

##### 返回值

`OysterStartTravelData`（`mode` / `version` / `encryptedTravelId` 等，见"数据模型"章节），据此决定互动 UI。

**说明****`ticket` 的世界 `mode` 必须与 `initialize` 传入的 `model` 匹配（调用方保证）**：模型按 mode 拆分后，每个模型是一条独立的网关路由，`start()` 是把 `ticket` 发往**当前模型**那条路由。SDK **不会也无法**在调用前替你校验这一点——`mode` 由本次 `start()` 的响应下发（即 `OysterStartTravelData.mode`），调用前 SDK 手里只有不透明的 `ticket` 和模型名，没有可比对的 mode；而从模型名反推 mode 属于对服务端命名的猜测，SDK 不做。

因此：**换一种 mode 的世界之前，用对应模型再 `initialize()` 一次**（空闲时以最新 config 为准，无需 `cleanup()`，token 保留；有进行中的 Travel 时该调用被忽略，需先 `end()`）。不匹配时本次 `start()` 会在网关侧失败，排查时请优先核对"当前 `model` 与本次 `ticket` 所属世界的 `mode` 是否成套"，再看下表的凭证类错误码。

##### 错误

**code**

**说明**

`401010`

凭证无效（也包括：凭证有效，但所属世界的 `mode` 与当前 `model` 不是同一条网关路由）

`401011`

凭证已用

`403002`

世界未就绪

`403007`

当前规格未开通（如角色演绎（acting）规格）

`429001` / `429002`

并发已满 / 可用容量不足

`500001`

资源/服务端失败

`103004`

并发开始

#### pause() / resume()

暂停 / 恢复体验（幂等）。

**使用时机**：**`directing`（实时导演）与 `acting`（角色演绎）世界支持**，`adventure` 不支持。可用 `start()` 返回的 `mode` 提前决定是否展示暂停按钮。`pause` 要求当前 `running`；`resume` 要求 `paused`。

##### 签名

```
@discardableResult public func pause() async throws -> OysterTravelStateData
@discardableResult public func resume() async throws -> OysterTravelStateData
```

##### 返回值

返回 `OysterTravelStateData`（字段见"数据模型"章节）。

##### 错误

**code**

**说明**

`103001`

无活跃体验

`103002`

状态/版本不允许

`103003`

模式不匹配

#### rewind(toSec:)

回溯到指定秒数。成功后 SDK 自动用原始 rtcConfig 重新入会回到播放。

**使用时机**：**仅** `paused` 状态可发起，且**只有 `directing`（实时导演）世界支持**——`acting` 与 `adventure` 均不支持回溯，请在这两种模式下隐藏回溯入口，不要调用。

##### 签名

```
@discardableResult public func rewind(toSec: TimeInterval) async throws -> OysterRewindTravelData
```

##### 参数

**字段**

**类型**

**是否必填**

**描述**

`toSec`

`TimeInterval`

是

回溯到的目标秒数。

##### 返回值

返回 `OysterRewindTravelData`（字段见"数据模型"章节）。

##### 错误

**code**

**说明**

`103001`

无活跃体验

`103002`

状态不允许

#### end()

结束体验（幂等，可重复调用）。调用成功或异常退出后，SDK **自动断开实时连接、停止轮询、释放全部会话资源**，`ticket` 同时失效，句柄进入终态。

**使用时机 / 注意**：无论用户主动退出还是被动结束（计时到期、收到 `.ended`/`.failed`、页面销毁），都要确保走到一次 `end()`，否则远端资源释放可能不及时。建议把所有退出路径收口到同一个幂等清理方法。

##### 签名

```
@discardableResult public func end() async throws -> OysterEndTravelData
```

##### 返回值

返回 `OysterEndTravelData`（字段见"数据模型"章节）。

#### sendInstruct(content:)（实时导演模式）

发送文本指令驱动剧情。

**使用时机**：实时导演模式；`running` 时直发，`paused` 时缓存、待 resume 重连进 `running` 后随首帧补发。

##### 签名

```
@discardableResult public func sendInstruct(content: String) async throws -> OysterSendInstructData
```

##### 参数

**字段**

**类型**

**是否必填**

**描述**

`content`

`String`

是

要发送的文本指令内容。

##### 返回值

返回 `OysterSendInstructData`（字段见"数据模型"章节）。

##### 错误

**code**

**说明**

`103001`

无活跃体验

`103002`

状态不允许

`103003`

在世界探索模式下调用

`403004`

输入内容违规（内容安审）

`404000`

Travel 不存在

#### sendCommand(\_:) / flushCommands()（世界探索模式）

-   `sendCommand`：发送方向/视角/动作控制指令（见"数据模型"章节 `OysterAdventureCommand`，fire-and-forget，无返回、不 throws）。仅**世界探索模式**、`running` 时有效。**外部可每帧高频持续输入，SDK 内部做节流**（latest-wins 采样、按 RTC 线速合帧），宿主无需自行节流。注意服务端对指令的响应本身有延迟，实际生效时间不固定。
-   `flushCommands`：「松键 / 输入释放」瞬间调用，立即补发队列里**已等待的最后一条**指令；无待发指令时为纯 no-op，不生成新指令。

##### 签名

```
public func sendCommand(_ command: OysterAdventureCommand)
public func flushCommands()
```

##### 错误

**code**

**说明**

`103001`

无活跃体验

`103003`

在实时导演模式下调用

`105004`

实时通道未就绪/发送失败

（均经 `events` 的 `.error` 透出，非 `throws`。）

#### pauseLocalAudioCapture() / resumeLocalAudioCapture()

临时释放 / 恢复 SDK 对本地麦克风采集的占用。

**使用时机**：语音识别等需要独占麦克风时先 `pause`，结束后 `resume`。

##### 签名

```
public func pauseLocalAudioCapture() async
public func resumeLocalAudioCapture() async
```

## 事件与状态

事件挂在 `OysterTravel.events` 上，是 SDK 对你的**主动推送通道**，用于透出非你主动调用触发的情况（如内部自动维护的实时连接或状态轮询出现问题）。

```
var events: AsyncStream<OysterTravelEvent> { get }

@available(iOS 15.0, *)
public enum OysterTravelEvent {
    case statusChanged(OysterTravelStatus)
    // SDK 内部流程出错，例如内部接口请求出错、推流出错，注意这里必须判断 token 过期并重新请求 token
    case error(OysterSDKError)
}
```

消费方式二选一：

-   **SwiftUI**：`OysterTravel` 是 `ObservableObject`，直接 `@StateObject`/`@ObservedObject` 观察 `status` 驱动 UI；错误仍从 `events` 取。
-   **命令式 / UIKit**：在 `Task` 中 `for await event in travel.events { ... }`，`switch` 处理 `.statusChanged` / `.error`；结束时取消持有的 `Task`。

```
let task = Task {
    for await event in travel.events {
        switch event {
        case .statusChanged(let status): render(status)   // 见下表
        case .error(let error):          handle(error)     // error.code / error.kind，见"错误码"章节
        }
    }
}
// 结束时：task.cancel()
```

`OysterTravelStatus`（5 个过程态 + 2 个终态）：

**状态**

**说明**

**典型处理**

`idle`

create 后、start 前

—

`prepare`

建连 / 重连中（内部 connecting / reconnecting）

展示连接 / 重连提示

`running`

流已就绪、可交互（内部 playing）

显示画面与操控

`pausing`

暂停已受理、等待服务端确认

展示「暂停中…」

`paused`

已暂停（确认）

展示暂停态（仅 `directing` 展示回溯入口）

`ended`

已结束（主动 end 或服务端结束）。终态

收尾并关闭页面

`failed`

失败。终态

展示错误并收尾

**说明**进入 `ended` / `failed` 后会话已终止，所有会话操作（pause/resume/sendCommand…）都不再生效。回调可能在主线程触发，更新 UI 可直接使用。

**说明**SDK 内部状态轮询时会**自动上报客户端拉流/播放态心跳**（connecting / playing / paused / reconnecting / disconnected），供服务端区分推流侧与客户端侧状态——纯 SDK 内部行为，宿主无需感知或参与。

## 数据模型

**说明**所有公开类型均标 `@available(iOS 15.0, *)`。下列返回值/参数是 **SDK 出参**，由内部就地构造、用 Swift 原生类型（`Date` / `TimeInterval` / `OysterTravelStatus`），**不是** `Codable`、不暴露 wire（snake\_case）细节——wire 解码发生在 SDK 内部。

```
// 配置
public struct OysterConfig: Sendable {
    public let apiHost: String             // 百炼网关地址（非业务 Server），必填、由宿主显式传入
    public let model: String               // 模型名含版本（如 "happyoyster-1.0-adventure"），必填、无默认值
    public let logLevel: OysterLogLevel?   // .debug/.info/.warning/.error；nil 时默认 .warning
    public let callbackTimeoutMs: Int      // 全局回调超时，默认 30000；超时按 105005 透出
    public init(apiHost: String, model: String, logLevel: OysterLogLevel? = nil, callbackTimeoutMs: Int = 30_000)
}

public enum OysterLogLevel: Int, Comparable, CaseIterable, Sendable {
    case debug, info, warning, error
}

// 对外会话状态（见"事件与状态"章节）
public enum OysterTravelStatus: String, Equatable, Sendable, CustomStringConvertible {
    case idle      // create 后、start 前
    case prepare   // 建连 / 重连中
    case running   // 流已就绪、可交互
    case pausing   // 暂停已受理、等待服务端确认
    case paused    // 已暂停（确认）
    case ended     // 终态：主动 end 或服务端结束
    case failed    // 终态：失败
}

// 开放字符串值（保留未知值，便于服务端扩展；编解码为裸 JSON 字符串 "running"）
public struct OysterRawValue: RawRepresentable, Equatable, Hashable, Codable, Sendable {
    public let rawValue: String
    public init(rawValue: String) { self.rawValue = rawValue }
}
public typealias OysterModeValue = OysterRawValue
public extension OysterModeValue {
    static let adventure = OysterModeValue(rawValue: "adventure")
    static let directing  = OysterModeValue(rawValue: "directing")
    static let acting     = OysterModeValue(rawValue: "acting")
}

// start() 返回（SDK 出参，非 Codable）
public struct OysterStartTravelData: Equatable, Sendable {
    public let encryptedTravelId: String  // 本次体验标识
    public let encryptedWorldId: String
    public let mode: OysterModeValue       // adventure / directing / acting
    public let playUrl: String?            // 当前服务端固定返回 null
    public let firstFrame: String?         // 首帧图地址，可能为 null（异步产生）
    public let version: String             // 世界版本标识（诊断用；互动 UI 请按 mode 决策）
    public let aspectRatio: String?        // 画幅（"9:16" / "16:9"）；仅 acting 有值，其余模式为 nil
}

// 控制接口返回（SDK 出参，非 Codable；status 为对外枚举 OysterTravelStatus）
public struct OysterTravelStateData: Equatable, Sendable { public let encryptedTravelId: String; public let status: OysterTravelStatus }
public struct OysterRewindTravelData: Equatable, Sendable { public let encryptedTravelId: String; public let status: OysterTravelStatus; public let resumedAtSec: TimeInterval }
public struct OysterEndTravelData: Equatable, Sendable { public let encryptedTravelId: String; public let status: OysterTravelStatus; public let endedAt: Date; public let duration: TimeInterval }
public struct OysterSendInstructData: Equatable, Sendable { public let encryptedTravelId: String; public let content: String; public let accepted: Bool }

// 世界探索模式操控指令（强类型枚举；取值与内部 WorldControlParams 对齐）
public struct OysterAdventureCommand: Equatable, Sendable {
    public enum Translation: String { case none, front, back, left, right, frontLeft, frontRight, backLeft, backRight }
    public enum Rotation: String { case none, mouseUp, mouseDown, mouseLeft, mouseRight, mouseUpLeft, mouseUpRight, mouseDownLeft, mouseDownRight }
    public enum Interaction: String { case none, jump, attack, crouch, sprint }
    public let translation: Translation   // 本条指令的移动方向；持续移动时按帧提交，松开后停止提交
    public let rotation: Rotation          // 本条指令的视角方向；持续转动时按帧提交，松开后停止提交
    public let interaction: Interaction    // 本条指令的单次动作；调用一次即可
    public init(translation: Translation = .none, rotation: Rotation = .none, interaction: Interaction = .none)
    public init(_ params: WorldControlParams)   // 由默认控件 WorldControlParams 便捷桥接（rawValue 一致）
}

// 统一错误（见"错误码"章节）
public struct OysterSDKError: Error {
    public let code: Int
    public let raw: Any?                  // 原始信息（内部 OysterError、网关 request_id 等），不承诺结构稳定
    public var kind: OysterErrorKind      // 数字 code 的类型化视图，便于穷尽 switch（计算属性）
    public init(code: Int, raw: Any? = nil)
    // 错误码常量见嵌套的 OysterSDKError.Code（如 .notInitialized = 100001）
}

// 错误码的类型化语义视图：本地码为具名 case，服务端 4xxxxx/5xxxxx 收敛为 .server(code:)
public enum OysterErrorKind: Equatable, Sendable {
    case notInitialized, tokenMissing, tokenInvalid, noActiveTravel, invalidState, sendCommandInDirecting
    case concurrentTravel, realtimeConnectFailed, realtimeJoinTimeout, firstFrameTimeout
    case channelNotReady, callbackTimeout, localNetwork, responseDecodeFailed
    case streamAutoEnd, proxyOrUnrecognized, featureGateDisabled
    case server(code: Int), unknown(code: Int)
}
```

**说明**

-   操控指令 rawValue 为小写驼峰（如 `front` / `mouseLeft` / `jump`），以上述枚举取值为准。
-   `mode` 对外取值为 `adventure`（世界探索）/ `directing`（实时导演）/ `acting`（角色演绎），以 `OysterModeValue` 定义为准。
-   `aspectRatio` 为开放字符串（当前 `9:16` / `16:9`，后续可能扩展）。判断横竖屏请按 `宽:高` 解析比值，不要穷举已知取值。

## 错误码

SDK **统一以** `OysterSDKError` 报错，类型一律通过 `code` 区分，**不要依据「从哪条路径拿到的错误」判断类型**——同一个 `code` 既可能从业务方法（`async throws`）抛出、也可能经 `events` 的 `.error` 透出。需要类型化匹配时用 `error.kind`（见"数据模型"章节 `OysterErrorKind`）。

错误码：**服务端**`4xxxxx`/`5xxxxx`，**客户端本地**`1xxxxx`。

### 服务端错误码（常见）

**code**

**含义**

**建议处理**

`400000`

参数非法（枚举非法等）

检查请求参数或 SDK 版本

`401010`

体验凭证（`ticket`）无效或已过期

让服务端重新下发凭证

`401011`

体验凭证（`ticket`）已被使用

凭证一次性，重新下发

`403001`

World 不存在、已删除或不属于当前开发者（含凭证内世界已删除）

重新选择有效 World

`403002`

世界状态非就绪

等世界就绪后再开始

`403003`

当前接口仅允许主 API Key

临时 Key 不可用于该接口

`403004`

输入内容违规（内容安审）；适用于 `sendInstruct` 文本指令

修改输入内容后重试

`403007`

当前规格未开通

**不可按容量满重试**；换已开通规格或联系开通（典型：账号未开通角色演绎（acting）规格）

`403008`

容量配置暂不可用

稍后重试

`404000`

资源不存在（世界 / Travel 归属或无产物）

核对 ID / 状态

`409000`

请求与当前资源状态冲突

检查体验状态

`429001`

当前规格并发已满

等已有会话结束后重试（勿与 `500001` 混淆）

`429002`

当前可用容量不足

稍后重试

`500000`

系统内部错误

稍后重试 / 反馈

`500001`

推理资源分配/服务内部失败

稍后重试

### 客户端本地错误码

**code**

**含义**

**SDK 是否自动终止会话**

**建议处理**

`100001`

SDK 未初始化即调用；也包括 `initialize` 因 `apiHost`/`model` 为空或非法而未生效的情况

否（同步抛出，拒绝该次调用）

先 `initialize`，并确认 `apiHost` 与 `model` 都已正确填写

`101001`

未注入 HTTP 鉴权 token

否

`updateToken` 后重试

`101002`

HTTP 鉴权 token 无效 / 被拒

否

重新换取 token 后 `updateToken` 重试

`103001`

当前无活跃体验

否（拒绝该次调用）

先 `createTravel` + `start`

`103002`

当前状态/版本不允许该操作

否（拒绝该次调用）

检查体验状态 / `version`

`103003`

模式不匹配（如非 `adventure` 世界调用 `sendCommand`）

否（拒绝该次调用）

按 `mode` 选对应接口，见"概览"章节能力表

`103004`

并发创建/开始体验

否（同步抛出）

串行化调用，先 `end` 旧会话

`105001`

实时连接失败

**是**

结束并重新开始

`105002`

实时入会超时

**是**

结束并重新开始

`105003`

等待视频首帧超时

**是**

结束并重新开始

`105004`

实时通道未就绪/发送失败

按场景（主动发送失败；心跳仅上报）

待 `running` 后再发送

`105005`

回调超时（默认 30s）

否

重试，必要时调大 `callbackTimeoutMs`

`105006`

入会后无推流，SDK 自动结束体验

**是**

结束并重新开始

`106001`

本地网络错误

否

可重试

`106002`

响应解析失败

按场景

升级 SDK / 反馈

`106003`

未携带可识别错误码 / 代理字符串错误码

否

可重试

`108001`

被服务端功能开关远程禁用（整体关停或版本过低；原因见 `raw`）

**是**

按 `raw` 提示用户；版本过低时引导升级

**致命性怎么判断**：致命性**不再以布尔字段暴露**（`OysterSDKError` 没有 `isFatal`）。语义上「致命」专指 **SDK 是否主动终止会话**（断开 RTC、释放整次会话）——

-   **会自动终止会话的错误**（如 `105001/105002/105003/105006/108001`）：宿主从**状态机终态**感知（`status → failed`，经 `events` 的 `.statusChanged` 透出），据此回到「开始体验」前的界面即可，无需自行判定致命性。
-   **调用拒绝类错误**（`100001/103001/103002/103003/103004`）：在你主动调用时同步抛出 / 拒绝该次调用，**不**终止会话。
-   **其余非致命错误**（如 `101001/101002/105005/106001/106003`）：不终止会话，按建议重试或重新注入 token 后继续。

**说明****`106001`** 可能有两种原因：本地网络错误，或 `apiHost` 配置错误。若重试无法恢复，检查 `apiHost` 是否配置正确。

**说明****`106003`** 若在填写 `model` 后出现，优先检查模型名称及版本是否正确、是否已为当前账号开通，并确认 `apiHost`、token 与模型属于同一账号和区域——不匹配时网关以 `AccessDenied` 拒绝并归一到本码。
