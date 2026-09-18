# HappyOyster iOS SDK 接入指南

本文是 iOS 集成方的最短上手路径：从初始化，到画面出来，到发送控制指令，再到结束体验。完整的方法签名、字段、错误码以 iOS SDK API Reference 为准。

完整的方法签名、字段、错误码以 [HappyOyster iOS SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/ios-sdk-2/happyoyster-ios-sdk-api-reference.md) 为准。

## 你将完成什么

一次「进入世界 → 实时视频体验 → 互动 → 结束」的最小闭环。运行时入口是全局的 `HappyOysterEngine.shared`，以及它创建出的单次会话句柄 `OysterTravel`。

```
OysterStream.register()
HappyOysterEngine.shared: initialize → updateToken → createTravel
OysterTravel:             videoView / events → start → sendInstruct / sendCommand → end
```

## 环境要求

**项**

**要求**

最低系统

iOS 15.0+

语言

Swift（`async/await`）

线程

公开接口 `@MainActor`，在主线程调用

引入

`import HappyOysterSDK`（聚合入口，已 `@_exported` Core + World）

**说明**实时通信（AliRTC）由 SDK 内部封装，集成方无需直接接触 RTC API。

### 通过 CocoaPods 引入 SDK

SDK 以预编译二进制（xcframework）按 subspec 分发，已发布到 CocoaPods 公开 Trunk——按版本号直接引入即可，无需本地 podspec 文件。

```
# HappyOysterSDK / AliVCSDK_ARTC 均发布在 CocoaPods 公开源。
source 'https://cdn.cocoapods.org/'

platform :ios, '15.0'
use_frameworks!

target 'YourApp' do
  # 聚合入口（Core + World），import HappyOysterSDK 一行即用。
  pod 'HappyOysterSDK'
  # 可选：默认 UI 组件（视频视图、操控 HUD）。
  pod 'HappyOysterSDK/UI'
  # 视频流 + AliRTC 引擎适配器（已依赖 Stream，无需单独声明）。
  pod 'HappyOysterSDK/StreamAliRTC'

  # RTC 厂商二进制：SDK 弱引用、不随 SDK 分发，由集成方自行引入（CocoaPods 公开源）。
  pod 'AliVCSDK_ARTC', '7.11.0'
end
```

然后执行 `pod install`，并打开生成的 `.xcworkspace`（而非 `.xcodeproj`）。

**说明**引入 `HappyOysterSDK/StreamAliRTC` 时 **`AliVCSDK_ARTC` 为必需**：缺失时 SDK 会静默回落 Loopback——能连上、状态走到 `running`，但**黑屏不报错**。

## 鉴权模型（两类凭证）

SDK 自己**不获取、不刷新**任何凭证，全部由你注入：

**凭证**

**来源**

**用途**

**注入方式**

**HTTP 鉴权 token**

你的 App 从**自家后端**获取

SDK 调用网关的通用鉴权（长期、需续期）

`updateToken(_:)`，SDK 只存最新一个

**一次性 ticket**

你的服务端经 Travel 凭证接口换取后下发

仅用于一次体验，用完即失效

作为 `createTravel(ticket:)` 入参

**说明**两者**不可混用**：`updateToken` 是通用鉴权，`ticket` 是一次性入房凭证。AK / 签名密钥只存在于你的服务端，客户端永不接触。

## 接入步骤

生命周期：**注册流引擎 → 初始化 → 注入 token → 创建会话 → 挂载视频 + 订阅事件 → start 播放 → 互动 → end**。

### Step 1：注册流引擎

出画面的唯一入口。建议 App 启动时调用一次，重复调用安全。

```
import HappyOysterSDK
import HappyOysterStream

OysterStream.register()
```

### Step 2：初始化 SDK

调用任何其他 API 前必须初始化一次。**换网关或换模型时直接再调一次即可**（空闲时以最新 config 为准，已注入的 token 保留）；仅当有进行中的体验时本调用被忽略，需先 `end()`。

```
let engine = HappyOysterEngine.shared
engine.initialize(config: OysterConfig(
    apiHost: "[workspace-id].[region].maas.aliyuncs.com",  // 百炼网关地址
    model: "happyoyster-1.0-adventure"                     // 已开通的模型名（含版本），必填
))
// 可选：覆盖日志级别 / 信令回调超时
// OysterConfig(apiHost: "…", model: "…", logLevel: .debug, callbackTimeoutMs: 30_000)

// apiHost 与 model 都必填、都没有默认值：HappyOyster 按模式拆成了不同子模型，
// 模型名（含版本）取值见 HappyOyster 系列模型文档，须与 token 同账号、同区域。
```

### Step 3：注入 HTTP 鉴权 token（push）

从你自己的后端取百炼临时 API Key 后注入。过期后重新获取并再次注入即可。

```
let token = await fetchTokenFromYourBackend()
engine.updateToken(token)
```

### Step 4：创建会话句柄

用一次性 `ticket` 创建 `OysterTravel`。**此时尚未建连**，视频视图已可取用。

```
let travel = try engine.createTravel(ticket: ticket)
```

### Step 5：挂载视频 + 订阅事件

SDK 出视图、宿主摆放；`start()` 前就订阅事件，避免漏掉早期状态。

```
containerView.addSubview(travel.videoView)     // SwiftUI 用 OysterVideoView(travel:)

let eventTask = Task {
    for await event in travel.events {
        switch event {
        case .statusChanged(let status): render(status)   // running / paused / ended / failed…
        case .error(let error):          handle(error)    // error.code / error.kind 见 API Reference
        }
    }
}
```

### Step 6：开始体验

建连并开始播放。成功后 SDK **内部自动**维持实时连接与状态轮询，状态经 `events` 透出。

```
let data = try await travel.start()
// data.encryptedTravelId —— 本次体验的标识，问题排查 / 服务端对账时使用
// data.encryptedWorldId  —— 本次进入的世界标识
// data.mode              —— adventure（世界探索）/ directing（实时导演）/ acting（角色演绎），决定交互 UI
// data.aspectRatio       —— 画幅（"9:16" / "16:9"）；仅 acting 有值，用于决定播放器方向
```

**说明**`start(maxExperienceTimeSec:)` 只对 `adventure` 生效，`directing` 与 `acting` 忽略该参数。

本次 travel 的世界 mode 必须与 Step 2 `initialize` 传入的 `model` 匹配。模型按 mode 拆分后（`happyoyster-1.0-adventure` / `-directing` / `-acting`），每个模型是一条独立的网关应用路由，一次 `initialize` 只服务一种 mode 的世界；`ticket` 由你的服务端在「该世界 mode 对应的模型」路由下签发，`start()` 会把它发往当前 `model` 那条路由，两者不一致时本步失败。

进入另一种 mode 的世界之前，用对应模型再 `initialize()` 一次——不需要 `cleanup()`，也不需要重新 `updateToken`：

```
HappyOysterEngine.shared.initialize(config: OysterConfig(
    apiHost: "…", model: "happyoyster-1.0-acting"))   // 换成本次世界 mode 对应的模型
```

空闲（没有进行中的体验）时以最新 config 为准，已注入的 token 保留。SDK 不会替你提前校验模型与世界是否匹配：`mode` 要等本步的响应（`data.mode`）才知道，调用前 SDK 只有不透明的 `ticket` 和模型名。只提供一种 mode 的 App 不受影响，初始化一次即可。

**说明**若有进行中的体验，重复调用 `initialize()` 会被忽略并告警，需先 `end()` 再切。

### Step 7：实时互动（按模式选择）

用 `data.mode` 决定交互方式：

```
if data.mode == .adventure {
    // 世界探索：方向/视角/动作控制（fire-and-forget，不抛错，失败经 events 透出）
    travel.sendCommand(OysterAdventureCommand(translation: .front, interaction: .jump))
} else {
    // 实时导演（directing）与角色演绎（acting）：文本指令驱动
    _ = try await travel.sendInstruct(content: "镜头转向城堡，主角开始奔跑")
}
```

`sendCommand` 内部按 42ms（24FPS）周期做 latest-wins 节流，宿主可以高频调用：

-   跳跃、攻击、蹲下、冲刺等单次动作只调用一次。
-   移动和视角在按住期间持续调用，松开时直接停止调用。
-   不需要在松开时发送 `none` 或调用 `flushCommands()`；SDK 也不会主动生成停止指令，服务端会在实时通道不再收到消息后自行结束动作。

### Step 8：暂停 / 恢复 / 回溯（按模式）

```
_ = try await travel.pause()          // directing / acting 支持
_ = try await travel.resume()
_ = try await travel.rewind(toSec: 10) // 仅 directing 支持
```

**说明**`adventure` 不支持这三个接口；`acting` 支持暂停 / 恢复但**不支持回溯**——请在这两种模式下隐藏回溯入口，不匹配的调用会被 SDK 本地拒绝（`103003` / `103002`）。

### Step 9：结束体验

断开实时连接、停止轮询、释放全部会话资源；本次 `ticket` 同时失效。幂等，**任意退出路径都要收口到它**。

```
_ = try? await travel.end()
eventTask.cancel()
```

**说明**退出 SDK 或切换网关时再调 `await engine.cleanup()`。

## 完整示例（SwiftUI）

```
import SwiftUI
import HappyOysterSDK
import HappyOysterStream

@main
struct MyApp: App {
    init() {
        OysterStream.register()                                     // Step 1
        HappyOysterEngine.shared.initialize(config: OysterConfig(   // Step 2
            apiHost: "[workspace-id].[region].maas.aliyuncs.com",
            model: "happyoyster-1.0-adventure"
        ))
    }
    var body: some Scene { WindowGroup { TravelScreen() } }
}

struct TravelScreen: View {
    @State private var travel: OysterTravel?
    @State private var eventTask: Task<Void, Never>?

    var body: some View {
        ZStack {
            if let travel {
                OysterVideoView(travel: travel)      // Step 5：SDK 出视图、宿主摆放
                    .ignoresSafeArea()
            } else {
                Color.black.ignoresSafeArea()
            }
        }
        .task { await start() }
        .onDisappear { Task { await end() } }
    }

    @MainActor private func start() async {
        let engine = HappyOysterEngine.shared
        engine.updateToken(await fetchToken())                      // Step 3
        do {
            let ticket = await fetchTicket()                        // 由你的服务端下发
            let travel = try engine.createTravel(ticket: ticket)    // Step 4
            self.travel = travel

            eventTask = Task {                                      // Step 5
                for await event in travel.events {
                    switch event {
                    case .statusChanged(let status): print("status: \(status)")
                    case .error(let error):          print("error: \(error.code)")
                    }
                }
            }

            let data = try await travel.start()                     // Step 6
            if data.mode == .adventure {                            // Step 7
                travel.sendCommand(OysterAdventureCommand(translation: .front))
            } else {
                _ = try await travel.sendInstruct(content: "突然下起了大雨")
            }
        } catch let error as OysterSDKError {
            // 处理开始失败（error.code 见 API Reference 错误码表）
        } catch {}
    }

    @MainActor private func end() async {
        _ = try? await travel?.end()                                // Step 9
        eventTask?.cancel()
        travel = nil
    }
}
```

## 最佳实践

-   **生命周期**：App 启动尽早 `OysterStream.register()` + `initialize()`，全局各一次；离开体验页时务必 `end()`，确保实时连接与资源释放；`OysterTravel` 是**单次使用**的，到终态后需重新 `createTravel`。
-   **token 续期**：进体验前确保 HTTP token 新鲜；收到鉴权类错误（`101001` / `101002`）后重新获取并 `updateToken`（非致命，不终止体验）。
-   **错误分级**：致命错误 SDK 会自动终止本次体验，经 `events` 的 `.error` 透出、并以状态机终态（`failed`）收尾，你应回到「开始体验」前的界面；非致命错误仅透出，可重试。错误码总表见 [API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/ios-sdk-2/happyoyster-ios-sdk-api-reference.md)。
-   **模式适配**：实时导演与角色演绎模式展示文本输入（`sendInstruct`），世界探索模式展示操控控件（`sendCommand`）；回溯入口只在实时导演模式展示。角色演绎世界按 `aspectRatio` 决定播放器方向（默认竖屏 `9:16`）。

## 下一步

-   完整 API（`pause()` / `resume()` / `rewind(toSec:)`、数据模型、错误码）→ [iOS SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/ios-sdk-2/happyoyster-ios-sdk-api-reference.md)
