# HappyOyster Android SDK 接入指南

本文面向集成方 Android 开发者，覆盖安装、鉴权、完整接入流程、事件处理与最佳实践，说明如何稳定接入 HappyOyster Android SDK。

HappyOyster 是一个 AI 世界探索产品。通过集成 HappyOyster Android SDK，你的 App 可以进入由 AI 实时生成的「世界」，以**世界探索（adventure）**、**实时导演（directing）**或**角色演绎（acting）**三种模式进行实时互动视频体验。

本文面向集成方 Android 开发者，覆盖安装、鉴权、完整接入流程、事件处理与最佳实践，说明如何稳定接入。具体 API（签名、参数、返回、错误码、数据模型）请参考 [HappyOyster Android SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md)。

## 能做什么

-   **开始一次体验（Travel）**：用一次性凭证进入一个已就绪的世界，SDK 自动建立实时视频连接。
-   **实时播放**：SDK 返回一个视频 View，你挂载到布局即可播放 AI 实时生成的画面。
-   **实时互动**：
    -   实时导演模式（directing）：发送文本指令驱动剧情。
    -   角色演绎（acting）：同样发送文本指令；暂停 / 恢复可用；**不要**回溯，**不要** `sendCommand`。用进房回包的 `aspectRatio` 定播放器方向（详见[模式适配](#ho-android-bp-s13h)）。
    -   世界探索模式（adventure）：发送方向 / 视角 / 动作控制指令与世界交互。
-   **过程控制**：暂停 / 恢复（实时导演与角色演绎）、回溯（仅实时导演）、结束（三种模式均可）。
-   **状态与错误回调**：通过事件监听实时感知体验状态与异常。

**说明**SDK 不负责世界的创建与管理，也不直接暴露底层实时通信细节——这些由你的服务端或 SDK 内部处理。你只需聚焦「开始体验 → 播放 → 互动 → 结束」。

## 安装

HappyOyster SDK（`cn.happyoyster:opensdk`）发布在 **Maven Central**；其底层实时通信引擎（阿里云 ARTC）发布在**阿里云 Maven**。两个仓库都需要声明。

### 环境要求

**项**

**要求**

minSdk

24（Android 7.0）及以上

compileSdk

36

JDK

11 字节码目标（宿主工具链建议 JDK 11 及以上）

语言

Kotlin（协程 `suspend` API）

ABI

`arm64-v8a` / `armeabi-v7a`（实时通信引擎含 native 库）

网络

需要可访问公网

在工程根 `settings.gradle.kts` 中加入仓库：

```
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()                                       // Happy Oyster SDK（cn.happyoyster:opensdk）
        maven("https://maven.aliyun.com/repository/public")  // 实时通信引擎（阿里云 ARTC）
    }
}
```

在 [Maven Central](https://central.sonatype.com/artifact/cn.happyoyster/opensdk) 查看最新正式发布的 Release，将下方 `<version>` 替换为该具体版本号，在模块 `build.gradle.kts` 中添加依赖：

```
dependencies {
    implementation("cn.happyoyster:opensdk:<version>")
}
```

使用具体版本号锁定依赖；升级前请阅读发布说明，升级后重新编译宿主代码。

**说明**SDK 以瘦 AAR 形式发布，不内嵌任何第三方依赖；实时通信引擎等传递依赖在解析时自动从上述仓库拉取，因此**阿里云 Maven 仓库必不可少**，缺失会导致 `com.aliyun.aio:AliVCSDK_ARTC` 解析失败。

### 权限

SDK 库自身仅声明 `INTERNET`。实时通信引擎会自动合并少量网络 / 蓝牙 / 音频设置类权限，库 manifest **不包含**录音与摄像头权限。视频画面为纯订阅播放，SDK 不向远端发送真实音频。

**宿主必须自行声明**：当你的 `targetSdk` 为 33 及以上时，需在宿主 `AndroidManifest.xml` 声明通知权限（实时通信引擎包含前台服务）：

```
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

**世界探索模式（`sendCommand`）建议声明录音权限**：世界探索模式的实时控制指令通过一路**静音音频流**建立「推流者身份」并承载上行通道，SDK **不会录制或上传你的真实音频**。`RECORD_AUDIO` **并非 DataChannel 的硬前置**——即使未授予，静音流仍以推流者身份存在、上行通道通常可用。但为兼顾各机型的稳定性，仍**建议**：如果你的 App 会用到 `sendCommand`，在宿主 `AndroidManifest.xml` 声明该权限，并在调用前于运行时申请。

```
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

**关于错误码 `105004`**：`105004` 表示实时通道未就绪 / 发送失败（如 DataChannel 连接中断或实时通道异常），**并非缺少权限的必然结果**——它不由未授予 `RECORD_AUDIO` 直接触发。实时导演模式（`sendInstruct`）与视频播放不受影响。若你的 App 不使用世界探索模式，则无需该权限。

如需裁剪合并进来的权限，可用 `tools:node="remove"`。

## 鉴权模型

SDK **不获取、不刷新** token，保持轻量。鉴权分两层：

1.  **百炼网关 API Key**：由你的 App 通过 `updateToken(token)` 注入为 Bearer token。SDK 只保存最新一个，不持久化、不刷新；Key 变化后由你再次注入。网关要求包括 `startTravel` 在内的 SDK 请求均使用此 Bearer。Bearer Key 过期或无效时，SDK 抛出 `SDKError(101002)`；此时应重新获取并注入 Bearer Key（`updateToken`），而非重新换取 ticket。**验证 / Demo 阶段**可直接用主百炼 API Key 作为 Bearer（`updateToken`）跑通流程。**生产环境**务必改用你的服务端签发的**短期 token**，切勿把长期 API Key 打包进 App 分发。
2.  **一次性体验凭证 `ticket`**：由你的服务端调用开放平台换取并下发给客户端，仅用于一次 `startTravel`；体验结束（正常或异常）后即失效，不可复用。ticket 级别的凭证错误由六位服务端 code 标识（如 `401010` = ticket 无效 / 过期，`401011` = ticket 已使用），SDK 原样透传。

你的服务端负责创建 / 管理 World、换取 Travel ticket 并下发给客户端；Android SDK 只消费 token 与 ticket，不提供 World 管理接口。初始化时必须通过 `SDKConfig.apiHost` 传入你账号的百炼 **API Host**（形如 `llm-xxxx.cn-beijing.maas.aliyuncs.com`，在百炼控制台 API Key 页的「API Host」处复制），并通过无默认值的必填参数 `SDKConfig.model` 传入拆分后的模型名（`happyoyster-1.0-directing` / `happyoyster-1.0-acting` / `happyoyster-1.0-adventure`，与所用 Open API 入口一致）。SDK 将请求地址补全为 `https://{apiHost}/api/v2/apps/{model}/openapi/v1/{endpoint}`，你无需自行拼接。

构造 `SDKConfig` 时遗漏 `model` 会编译失败；传入空白 `model` 时，`initialize` 同步抛出 `SDKError(100002)`（`raw = "SDKConfig.model must not be blank"`），不会创建或替换 runtime，也不会发起网络请求。**API Host、model 与注入的 API Key 必须匹配所需的账号、区域和模型授权**，否则网关通常返回 AccessDenied（运行期以 `SDKError(106003)` 抛出，`AccessDenied` 原文见 `SDKError.raw`；排查清单见 API Reference 错误码表 `106003` 行）。出于安全，强烈建议客户端注入**服务端签发的短期 token**作为 Bearer，而非把长期 API Key 打包进 App 或写入代码仓库。

**说明**

**地域合规提示：**

-   为支持适用法律法规及数据合规要求的落实，如您的目标用户包括美国用户，您必须在 SDK 初始化时为面向该等用户的服务配置美国地区 API Host。
-   开发者应确保配置正确，并依法承担因未按上述要求配置所产生的相应责任。

## 快速开始

```
import cn.happyoyster.opensdk.*   // 入口类均在此包下：HappyOyster、SDKConfig、TravelStatusValue、ModeValue、SDKError 等

// 跟踪当前体验状态与本次 Travel 元数据，互动前据此判断是否可发送。
@Volatile private var currentStatus: TravelStatusValue? = null
@Volatile private var currentTravel: StartTravelData? = null

// 1) 初始化（建议在 Application.onCreate）
//    apiHost 必填：你账号的百炼 API Host（百炼控制台 API Key 页复制）
//    model 必填且无默认值：包含版本的完整模型名称；可用值以百炼官方 HappyOyster 系列模型文档为准
HappyOyster.initialize(
    applicationContext,
    SDKConfig(
        apiHost = "llm-xxxx.cn-beijing.maas.aliyuncs.com",
        model = "happyoyster-1.0",
    ),
)

// 2) 注入百炼网关 API Key（作为 Bearer token）
HappyOyster.updateToken(bailianApiKey)

// 3) 监听 SDK 事件：用 onStatusChanged 驱动宿主状态机与互动能力门控
HappyOyster.addListener(object : HappyOysterListener {
    override fun onStatusChanged(status: TravelStatusValue) {
        currentStatus = status
        when (status) {
            // running 才允许互动；世界探索模式的 sendCommand 仅在 running 有效。
            TravelStatusValue.Running -> markInteractionAllowed()
            // paused 是 pauseTravel 真正生效的信号（异步，见下）；此时仍可 sendInstruct。
            TravelStatusValue.Paused -> markTravelPaused()
            // 终态：SDK 已自行结束并释放资源，清理宿主侧本次体验状态。
            TravelStatusValue.Completed, TravelStatusValue.Failed -> clearActiveTravel()
            // init / pending：尚未就绪，互动不可用。
            else -> markInteractionBlocked()
        }
    }
    override fun onError(error: SDKError) {
        // 统一错误回调，见 API Reference 错误码节
    }
})

// 4) 开始体验（ticket 由你的服务端下发）
lifecycleScope.launch {
    try {
        // 同一 App 同一时刻只允许一个并发 Travel（alirtc 限制：即使换一个 ticket
        // 也无法在同一 App 内并发开始第二个 Travel）。已有体验进行中时再次调用会抛出
        // SDKError(103004)，其 raw 仅携带当前正在播放 ticket 的脱敏摘要，不包含完整 ticket。
        val travel: StartTravelData = HappyOyster.startTravel(ticket)
        currentTravel = travel

        // 先检视返回的 Travel 元数据再决定如何互动：
        //   travel.mode          —— directing / adventure / acting
        //   travel.creationModel —— Simple / ScriptList
        //   travel.aspectRatio   —— 仅 acting 有值，用于定播放器方向
        val canSendInstruct = (travel.mode == ModeValue.Directing || travel.mode == ModeValue.Acting) &&
            travel.creationModel != CreationModelValue.ScriptList
        // 注意：ScriptList 模式下调用 sendInstruct 会抛 SDKError(103002)，剧本内容不通过本 SDK 管理。

        // 5) 挂载视频 View（SDK 返回 view，你加入布局）
        //    角色演绎：先按 travel.aspectRatio 定好容器方向，再 attachVideo() 挂载（见「模式适配」）——
        //    远端视图以裁剪填充绑定，容器方向与 aspectRatio 不符会裁掉画面。
        val videoView = HappyOyster.attachVideo()
        binding.videoContainer.addView(videoView)

        // 6) 运行中互动——必须先等到 running 再发送：
        //    - sendCommand（世界探索）：仅 running 有效；init/pending/paused 调用返回 103002。
        //    - sendInstruct（实时导演 / 角色演绎）：running 或 paused 均可；init/pending 调用返回 103002。
        if (canSendInstruct && currentStatus == TravelStatusValue.Running) {
            HappyOyster.sendInstruct("突然下起了大雨")
        }
    } catch (e: SDKError) {
        // 处理开始失败（例如 103004：已有体验在播放）
    }
}

// 7) 暂停 / 恢复（实时导演与角色演绎；回溯仅实时导演）
//    pauseTravel 是异步的：方法返回只代表「受理」，真正暂停以 onStatusChanged(paused) 为准。
//    务必等到 paused 回调后再允许调用 resumeTravel。
lifecycleScope.launch {
    if ((currentTravel?.mode == ModeValue.Directing || currentTravel?.mode == ModeValue.Acting) &&
        currentStatus == TravelStatusValue.Running
    ) {
        HappyOyster.pauseTravel()        // 受理；宿主记录 pausing，等待状态回调
        // …收到 onStatusChanged(Paused) 后…
    }
}
lifecycleScope.launch {
    if (currentStatus == TravelStatusValue.Paused) {
        HappyOyster.resumeTravel()       // 仅在 paused 后调用
    }
}

// 8) 结束体验（SDK 自动断开实时连接并释放资源）
lifecycleScope.launch { HappyOyster.endTravel() }
```

## 事件订阅与错误处理

用 `onStatusChanged` 驱动宿主状态机与互动能力门控；用 `onError` 统一接收运行时错误。事件接口与完整错误码见 [HappyOyster Android SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md)。

**必须**

-   在 `HappyOyster.initialize(...)` 成功返回后立即注册监听器；`addListener` / `removeListener` 必须在 `initialize` 之后调用（在初始化前调用会抛出 `SDKError(100001)`）。
-   以 `onStatusChanged(Running)` 为门控，`running` 后才允许互动调用；`sendCommand`（世界探索模式）仅 `running` 有效。
-   同时处理 `onError`，不要只 catch `startTravel`；致命错误同时终止体验（见 API Reference 错误码节）。

**推荐**

-   在合适的生命周期（如 `onDestroy`）调用 `removeListener`，避免内存泄露。

**避免**

-   重复注册监听但不 removeListener。

## 指令发送：sendInstruct 与 sendCommand

### sendInstruct（实时导演 / 角色演绎）

`sendInstruct` 用于实时导演（directing）与角色演绎下发送文本指令驱动画面，在 `running` 或 `paused` 状态均可调用。paused 态下 SDK 不会自动 resume——由宿主决定是否先调用 `resumeTravel` 再发 instruct（节流、状态校验等契约细节见 [API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md)）。角色演绎世界的 `creationModel` 恒为 `Simple`，因此 ScriptList 限制只作用于实时导演。

### sendCommand（世界探索模式）

`sendCommand` 用于世界探索模式（adventure）下发送方向 / 视角 / 动作控制指令，仅 `running` 有效。SDK 内置 42 ms（24fps）latest-wins 节流，宿主可按游戏帧率高频调用，SDK 自动合并；无需宿主手动限速。**单次动作调用一次即可；持续动作需按帧续调、松手时显式发一次 `None` 复位**（单次 / 持续最佳实践、节流 / 失败透出等契约细节见 [API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md)）。

推荐做法：在宿主的世界探索模式互动界面提供三组独立指令入口（移动方向 + 视角方向 + 动作交互），维护三组当前按下状态，并在每次调用时发送完整的三字段快照。未按下的维度填 `"None"`；如果不同维度同时按下，必须保留并发送各维度当前值，不能因为更新一个维度就把其他维度重置为 `"None"`。

## 暂停 / 恢复 / 回溯

**适用模式**：暂停 / 恢复适用于**实时导演**与**角色演绎**，两者行为完全一致（含下面的 3 s 屏障）；**回溯仅实时导演**。世界探索模式下调用 `pauseTravel` / `resumeTravel` / `rewindTravel` 会被 SDK 以 `103003` 拒绝。此外服务端下发的 `version` 必须是本模式的 v2 标识（实时导演 `storyV2`、角色演绎 `actingV2`），否则暂停 / 恢复返回 `103002`。

**暂停是异步的**：`pauseTravel` 方法返回仅代表受理，真正暂停以 `onStatusChanged(Paused)` 为准。在「调用 `pauseTravel`」到「收到 `Paused` 回调」之间，宿主可将本地体验状态标记为 `pausing`；只有收到 `Paused` 后，才应允许调用 `resumeTravel` 或依赖 `paused` 态的 `rewindTravel`。

**SDK 内部 pause→reopen 屏障**：收到 `Paused` 后即可按契约调用 `resumeTravel` / `rewindTravel`；若调用发生在暂停确认后的 3 s settle 窗口内，SDK 的 suspend 方法会先等待剩余时间，再向服务端发送会重新打开实时房间的请求。宿主无需另加 pause→resume 延时；自然等待已满 3 s 时 SDK 不增加延迟。

**宿主侧调用冷却（建议）**：建议宿主在 `resumeTravel` 返回成功后的 3 s 内暂缓再次发起 `pauseTravel`，避免过于频繁的切换。SDK 本身不强制这个冷却。

**回溯**：`rewindTravel` 仅在 `paused` 状态可用；回溯后服务端自动 resume，SDK 自动重连 RTC，无需宿主干预。典型序列：`pause` → `wait:paused` → `rewindTravel(sec)`。回溯秒数 `rewindToSec` 应取 4 的整数倍（如 4、8、12），非整数倍由服务端向下取整（如 7→4），实际生效秒数以返回的 `resumedAtSec` 为准。**仅实时导演支持回溯**：在角色演绎与世界探索模式下调用 `rewindTravel`，会被 SDK **在本地**以 `103003` 拒绝，不会发出任何 HTTP 请求；宿主应**隐藏**回溯入口，而不是只把按钮置灰。

异步语义、3× 重试退避（resumeTravel 退避 1 s / 2 s / 3 s）等契约细节见 [HappyOyster Android SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md)。

## 日志

SDK Logcat tag：`HappyOysterSDK`。SDK 提供两路互不影响的日志输出：

-   **内置 Logcat（默认关闭）**：仅当 `SDKConfig.logcatEnabled = true` 时 SDK 才写 Logcat（默认 `false`，完全静默）。`SDKConfig.logLevel` 过滤其最低等级，默认 `INFO` 已含重建会话所需的生命周期锚点（初始化、Travel 起止 / 状态迁移、RTC 入会 / 首帧）；仅看报错可降为 `WARN`，深入排障可升到 `DEBUG` / `VERBOSE`。`logLevel` 不影响 `logHandler`。
-   **宿主回调 `logHandler`（推荐）**：接收 SDK 每一条 `LogRecord`（全量 firehose），与 `logLevel` / `logcatEnabled` 完全独立，可转发到宿主自有日志系统（Logcat、文件、崩溃平台等）。回调须**快速、非阻塞**且禁止在回调内回调 SDK；回调抛出的异常被静默捕获；`LogRecord.message` 已脱敏，不含 Bearer token、`ticket`、RTC token 等明文。

```
HappyOyster.initialize(
    context,
    SDKConfig(
        apiHost = "llm-xxxx.cn-beijing.maas.aliyuncs.com",  // 必填：你账号的百炼 API Host
        model = "happyoyster-1.0",                          // 必填且无默认值：完整模型名称及版本
        logcatEnabled = true,        // 开启内置 Logcat（默认 false）
        logLevel = LogLevel.DEBUG,   // 仅影响内置 Logcat
        logHandler = { record ->     // 可选：转发到宿主自有 Logcat tag
            android.util.Log.d("MyApp/SDK", record.message, record.throwable)
        },
    ),
)
```
```
adb logcat -s HappyOysterSDK          # 仅内置 Logcat 开启时有输出
adb logcat -s HappyOysterSDK MyApp    # 同时查看宿主 App 日志（MyApp 换成你的 tag）
```

**会话与请求对账**：日志中的 `travelId`（即 `encryptedTravelId`）以**全值**输出，是发往服务端的会话键——排查某次会话或提工单时附上它，即可对齐客户端与服务端日志。每条 HTTP 响应日志还带服务端 `requestId`（`reqId=` 字段，缺失时为 `-`）用于定位单次请求；该 ID 仅出现在日志中，不进入任何公开返回值。

## 生命周期与内存

-   在 `Application.onCreate` 调用 `initialize`，全局一次。
-   **idle 状态下再次调用 `initialize`**（例如切换 API 区域或 `model`）会关闭上一个 idle runtime 并重置已注册监听器、Feature Gate 状态；返回后请重新 `addListener`。Travel 正在 starting、active 或 ending 时再次初始化会以 **`103004` 拒绝**；务必先等待 `endTravel()` 完成。`initialize` 不会再丢弃进行中的 Travel。
-   体验与宿主生命周期绑定：在 `Activity/Fragment` 的 `onDestroy`（或 ViewModel `onCleared`）中调用 `endTravel`，确保实时连接与资源释放。
-   `attachVideo()` 返回的 View 在结束时从布局移除（`container.removeAllViews()`），并 `removeListener`。
-   SDK 只持有 application context，你也不要把 Activity 传给 SDK。

## 协程与线程

-   业务方法是 `suspend`，可在任意 coroutine context 的 `lifecycleScope` / `viewModelScope` 中调用；SDK 会在内部主 dispatcher 协调状态与 RTC 操作，HTTP 仍不阻塞主线程。
-   调用方取消 coroutine 时，SDK 会取消该调用仍在途的 HTTP 请求（如有），并原样传播 `CancellationException`，不会转换为 `SDKError`；不要把它当成业务错误捕获或吞掉。取消不代表服务端已经受理的请求会被回滚。
-   `attachVideo()`、`sendCommand()` 在主线程调用；离主线程调用会同步抛出 `IllegalStateException`。

## token 管理

-   Bearer API Key 有效期有限，建议在进入体验前确保 token 新鲜；收到 `onError(101002)`（token 过期）时重新获取 Bearer Key 并 `updateToken`，无需重新换取 ticket。

## 错误恢复

-   对致命错误：清理本次体验状态（包括移除视频 View）、提示用户、允许重新开始。
-   对网络抖动（`106001`）和上游服务临时异常（`106003`）：可做有限次重试。
-   初始化同步抛出 `100002` 时，为 `model` 空白；填写完整模型名称及版本后重新初始化。非空 `model` 的名称 / 版本错误、模型已下线、尚未发布或未授权时，网关通常返回 AccessDenied 并映射为 `106003`；结合 `SDKError.raw` 检查 `model`、API Host、API Key 的账号与区域是否匹配。

（致命 / 非致命分类见 [HappyOyster Android SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md) 错误码节。）

## 模式适配

-   用 `startTravel` 返回的 `mode` 决定可开放的交互能力：实时导演与角色演绎使用文本指令 `sendInstruct`（角色演绎额外用 `aspectRatio` 定播放器方向，隐藏回溯），世界探索模式使用控制指令 `sendCommand`。
-   世界探索模式（adventure）可选用重载 `startTravel(ticket, maxExperienceTimeSec)` 限制本次体验最大时长（秒，到时自动结束）；合法档位由服务端配置（当前 `60` / `90` / `120`，默认 `60`），实时导演与角色演绎 忽略该值（服务端忽略并回显 `null`）。传入不支持的值时服务端返回 `400000` 且本次启动失败。参数细节见 [API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md)。

### 角色演绎：按 `aspectRatio` 定播放器方向

`StartTravelData.aspectRatio` **仅角色演绎（acting）非空**：`"9:16"`（竖屏，服务端创建世界时的默认值）或 `"16:9"`（横屏）；世界探索与实时导演均为 `null`。画幅在**创建世界时**（由你的服务端通过 Open API 指定）就已确定，对客户端是只读结果。SDK **原样保留**未识别的取值，宿主须把不认识的值等同 `null` 处理，回退到自己的默认方向。

**时机**：在 `startTravel()` 返回之后、调用 `attachVideo()` 把返回的 `SurfaceView` 挂进布局**之前**确定播放容器方向。SDK 只有在宿主挂载视图后才开始绑定并渲染远端流，所以此刻定方向仍然赶在首帧之前。该值随 `startTravel()` 的返回值交付，**不保证**在 SDK 加入实时通信频道之前完成——只需保证在 `attachVideo()` 挂载前定好方向即可。

**后果**：远端视图以**裁剪填充（clip-to-fill）**方式绑定——容器方向与 `aspectRatio` 不一致会**裁掉画面**（例如把 `9:16` 竖屏流放进 16:9 容器，上下会被切掉大半），而不是留黑边。

```
// startTravel() 返回之后、attachVideo() 之前：先按 aspectRatio 定好容器方向
val ratio: Float = when (travel.aspectRatio) {   // 宽 / 高
    "9:16" -> 9f / 16f                           // 竖屏（角色演绎的服务端默认值）
    "16:9" -> 16f / 9f                           // 横屏
    else -> HOST_DEFAULT_RATIO                   // null 或未识别取值：回退宿主自己的默认方向
}
// 用 ratio 定容器方向，例如：
//   - Compose：Modifier.fillMaxWidth().aspectRatio(ratio)
//   - View 体系：容器放在 ConstraintLayout 里，宽度撑满、高度由宽高比决定（XML 中 height=0dp）
binding.videoContainer.updateLayoutParams<ConstraintLayout.LayoutParams> {
    dimensionRatio = ratio.toString()
}

// 容器方向确定后，再挂载 SDK 返回的视频 View
val videoView = HappyOyster.attachVideo()
binding.videoContainer.addView(videoView)
```

**说明**账号未开通角色演绎（acting）规格（或该规格总闸关闭）时，创建世界与进房都会被服务端拒绝：`startTravel` 以 `403007` 失败（进房前拒绝，不创建 Travel），SDK 原样透传。该码**不可**按容量不足重试，应提示联系开通。

## 完整示例（ViewModel + Activity 片段）

```
class TravelViewModel : ViewModel() {

    private val listener = object : HappyOysterListener {
        override fun onStatusChanged(status: TravelStatusValue) {
            _status.value = status
        }
        override fun onError(error: SDKError) {
            _error.value = error
        }
    }

    init { HappyOyster.addListener(listener) }

    fun start(ticket: String) = viewModelScope.launch {
        try {
            val travel = HappyOyster.startTravel(ticket)
            _travel.value = travel
        } catch (e: SDKError) {
            _error.value = e
        }
    }

    fun send(text: String) = viewModelScope.launch {
        runCatching { HappyOyster.sendInstruct(text) }
    }

    fun stop() = viewModelScope.launch { runCatching { HappyOyster.endTravel() } }

    override fun onCleared() {
        HappyOyster.removeListener(listener)
        viewModelScope.launch { runCatching { HappyOyster.endTravel() } }
    }
}

// Activity 中挂载视频
val videoView = HappyOyster.attachVideo()
binding.videoContainer.addView(videoView)
// 结束时
binding.videoContainer.removeAllViews()
```

## DevOps 排障指南

当集成过程中出现问题（无法进入 Travel、黑屏无画面、中途断流、暂停 / 恢复异常等），开放 SDK 日志是最快的定位手段。本章给出一套标准排障流程，便于你自查，也便于向我们反馈时一次性提供足够信息。

### 开启日志

排障时按需选择日志输出（详见[日志](#ho-android-bp-s8h)）：快速自查用 `logcatEnabled = true` 配合 `adb logcat`，排障建议把 `logLevel` 升到 `DEBUG` 或 `VERBOSE`（默认 `INFO` 已含完整生命周期时间线，仅关心报错可降到 `WARN`）；接入自有系统则用 `logHandler` 接收全量 `LogRecord`（不受 `logLevel` 影响），写入你的文件或崩溃平台。

### 会话相关 ID：`travelId`

SDK 日志中的 `travelId`（即 `StartTravelData.encryptedTravelId`）以**全值**输出，是贯穿一次会话的唯一标识，也是发往服务端的会话键。它是把**客户端日志**与**服务端会话记录**对齐的关键——反馈问题时请务必带上出问题会话的 `travelId`。

### 采集日志

复现问题时，把 SDK 日志落盘：

```
# 清空历史，复现问题，然后抓取 SDK 日志到文件
adb logcat -c
adb logcat -s HappyOysterSDK > happyoyster-sdk.log
# 需要同时看你自己 App 的日志时（把 MyApp 换成你的 tag）：
adb logcat -s HappyOysterSDK MyApp > happyoyster-sdk.log
```

### 反馈问题时请提供

为避免多轮往返，提交问题时请一并附上：

**项**

**说明**

SDK 版本

`HappyOyster.VERSION`

会话 `travelId`

出问题会话的 `encryptedTravelId`（见「会话相关 ID」）

发生时间

出问题的大致时间点（精确到分钟即可）

错误码

捕获到的 `SDKError.code`（错误码含义见 [API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/android-sdk/happyoyster-android-sdk-api-reference.md) 错误码表）

复现步骤

操作路径 + 期望结果 + 实际结果

运行环境

设备型号、Android 版本、网络环境（WiFi/蜂窝）

日志文件

「采集日志」步骤采集的 `HappyOysterSDK` 日志（建议 `DEBUG`/`VERBOSE`）

### 关于脱敏与日志可分享性

SDK 日志在设计上即为**可安全分享**：凭据类信息（Bearer token、Travel ticket、RTC token）、RTC 内部标识与媒体地址在写入日志前已脱敏，不会出现明文；`travelId` 属会话标识（非凭据），保留全值仅用于对账。即便如此，仍建议通过可信渠道传输日志文件，不要公开粘贴到不受控的平台。
