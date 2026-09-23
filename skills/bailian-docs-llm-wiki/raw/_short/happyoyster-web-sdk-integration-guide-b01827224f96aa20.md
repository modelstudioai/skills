# HappyOyster Web SDK 接入指南

本文面向前端 / 全栈开发者，说明如何在生产环境中稳定接入 HappyOyster Web SDK 。

具体 API 需参考 [HappyOyster Web SDK API Reference](raw/model-api-reference/world-model-api-reference/happyoyster/client-sdk/web-sdk/happyoyster-web-sdk-api-reference.md)。

## 最小接入示例

如果你已经从服务端拿到了百炼临时 api-key `token` 和 Travel `ticket`，前端接入 SDK 的最小链路大致如下：

```
import { HappyOysterEngine, isSdkError } from "@happy-oyster/js-sdk";

const engine = new HappyOysterEngine({
  APIHost: "open-platform.example.com",
  model: "happyoyster-1.0-adventure", // 必填；此处以 Adventure 模型为例
  logLevel: "warn",
});

engine.updateToken(token);

const videoElement = document.querySelector("video") as HTMLVideoElement;
const travel = engine.createTravel({
  ticket,
  videoElement,
  maxExperienceTimeSec: 90, // 可选，仅 Adventure 生效：60 / 90 / 120
});

const offStatus = travel.on("statusChanged", (status) => {
  // 用 status 驱动 loading、按钮禁用、播放器状态等 UI。
});

const offError = travel.onError((error) => {
  // 这里通常做日志、toast；如果是 token 过期，重新向服务端申请 token 后 updateToken。
  if (isSdkError(error)) console.error(error.code, error.message);
});

try {
  await travel.start();
  // running 后再通过 travel.can(action) 开放操控或 Directing 输入。
} finally {
  offStatus();
  offError();
  await travel.end();
}
```

这段代码只覆盖 SDK 侧。创建世界、等待世界 ready、申请 `ticket`、申请百炼临时 api-key `token` 都应该在业务服务端或经由业务服务端完成。

## 端到端链路 Overview

一次完整的体验主要涉及以下参与方。

### 参与方

**参与方**

**职责**

业务前端

UI、`<video>`、会话编排、调用 SDK

业务服务端

保管主 API Key、代调开放平台世界类 API、下发百炼平台临时凭证

HappyOyster OpenApi

提供 HappyOyster 世界模型所需 API 的对外接口。

HappyOyster SDK

业务前端所调用的 SDK，主要负责客户端侧管理 Travel 会话，视频流接入等。

![端到端参与方示意图](https://adoc-prod-media.oss-cn-shanghai.aliyuncs.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9fd8.png)

### 故事链路

**阶段**

**执行方**

**动作**

**说明**

① 创建世界

业务服务端 → HappyOyster OpenApi

`POST /openapi/v1/worlds`

返回 `encryptedWorldId`、`status`、`firstFrame`

② 等待就绪

业务服务端 → HappyOyster OpenApi

`GET /openapi/v1/worlds/build-status`

轮询至 `status === ready`（创建时已 ready 可跳过）

③ 体验凭证

业务服务端 → HappyOyster OpenApi

`POST /openapi/v1/worlds/get-travel-credential`

返回 `ticket`（一次性，供 enter-travel）

④ 申请临时 api-key token

业务服务端 → HappyOyster OpenApi

`POST /api/v1/tokens?expire_in_seconds=1800`

返回临时 api-key `token`，过期时间建议不要过短，否则可能无法完成整套体验或频繁更新 `token`

⑤ 下发临时 api-key token 以及体验凭证

业务前端 → 业务服务端 → 业务前端

申请临时 api-key 和 体验凭证

前端拿到 `token` 和 `ticket` 后，进入 SDK 启动流程

⑥ 进入体验

业务前端 → HappyOyster SDK

见下文「SDK 启动子链路」

`new HappyOysterEngine/updateToken` → `createTravel` → `start()`

### SDK 游玩子链路（阶段 ⑥ 展开）

#### 启动一个 Travel

![Travel 启动流程](https://adoc-prod-media.oss-cn-shanghai.aliyuncs.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9fdf.png) **调用顺序要点**

**步骤**

**API**

**说明**

1

`new HappyOysterEngine()`

同一 `APIHost + model` 建议复用实例

2

`updateToken()`

在 `start()` 前完成

3

`createTravel()`

必须传入 `videoElement`

4

`travel.on(...)`

建议在 `start()` 前注册

5

`await travel.start()`

成功后进入 `running`

#### 在 Adventure 模式下进行游玩

![Adventure 实时操控流程](https://adoc-prod-media.oss-cn-shanghai.aliyuncs.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9fde.png)

#### 在 Directing / 角色演绎模式下进行游玩

![Directing / 角色演绎 指令流程](https://adoc-prod-media.oss-cn-shanghai.aliyuncs.com/media/maas_docs/sfm/zh/images/6a4b3c2d1e0f9fdd.png)

Adventure、Directing 和角色演绎可以先按下表理解：

**模式**

**主要能力**

**常见场景**

**注意点**

Adventure（`1`）

`sendCommand()`

键盘、摇杆、按钮等实时操控

只在 `running` 后发送；`maxExperienceTimeSec` 仅对该模式生效

Directing（`2`）

`sendInstruct()`、`pause()`、`resume()`、`rewind()`

用自然语言推进剧情、控制播放节奏

暂停、恢复和回退由会话能力决定；先用 `travel.can(action)` 判断

角色演绎（`3`）

`sendInstruct()`、`pause()`、`resume()`

演出型体验与画幅配置

暂停、恢复由会话能力决定；不支持 `rewind()`，且 `scriptlist` 不支持 `sendInstruct()`

### 业务服务端相关实践（概要）

服务端这边只抓住几件事就好：

-   **主 API Key 仅驻留业务服务端**，浏览器只拿短效 `token`（Demo：`POST /server-api/temp-api-key`）
-   **体验凭证由服务端代申请**，按世界 / 用户鉴权后再下发 `ticket`；不要在前端硬编码或长期缓存
-   **世界未 ready 不要签发凭证**，否则 enter-travel 可能失败或体验不完整
-   **业务服务端与 SDK 指向同一开放平台环境**：业务服务端可使用完整 OpenAPI 地址；SDK 的 `APIHost` 只传裸 host，例如 `open-platform.example.com`

## SDK 核心概念

在端到端链路中，SDK 只承担「进入 Travel → 播放 → 操控 → 结束」段。两个核心对象：

**对象**

**作用**

`HappyOysterEngine`

配置 `APIHost` 和 `model`、百炼临时 api-key token（`updateToken`）、创建 Travel

`Travel`

一次会话：`start` 连 RTC，`sendCommand` / `sendInstruct` / 生命周期方法

**会话状态**（`statusChanged`）：

```
idle ──start()──► prepare ──video 可播放──► running ⇄ paused ──end()──► idle
```

**三条约束**（后文展开）：

-   每个 Engine 同时只允许一个 active Travel
-   `videoElement` 必须在 `createTravel` 时传入
-   百炼临时 api-key token 与 travel ticket 用途不同（见「故事链路」阶段 ④⑤ 与「双凭证模型」）

## 初始化与 Token 管理

### Engine 实例化

**必须**

-   配置 `APIHost`（开放平台裸 host，不含 `https://`、协议头或路径，例如 `open-platform.example.com`）
-   同一 `APIHost + model` 复用一个 `HappyOysterEngine`；切换 host 或模型前，先结束当前 Travel，再使用目标配置的 Engine

**推荐**

-   开发环境 `logLevel: 'debug'`，生产环境 `'warn'` 或 `'none'`
-   Engine 在会话编排层创建，不用每次 start 都 new

常用配置可以先按这张表理解：

**配置项**

**必填**

**建议**

`APIHost`

是

只传裸 host，例如 `open-platform.example.com`；不要带 `https://` 或路径

`model`

是

必填，无默认值；与业务服务端创建世界、签发 ticket 使用的模型保持一致。Engine 创建后固定，不会根据 `mode` 或 ticket 自动推断

`token`

否

可以构造时传，也可以后续用 `updateToken(token)` 设置；token 过期后也用 `updateToken` 刷新

`logLevel`

否

开发环境用 `debug`，生产环境用 `warn` 或 `none`

`streamReadyTimeout`

否

网络或渲染链路较慢时可调大；超时后建议给用户重试入口

**避免**

-   在 render / 热路径中重复 `new HappyOysterEngine()`
-   传入完整 URL（例如带 `https://`）或省略 `APIHost` 后再调用 SDK 后端接口

### 双凭证模型

对应故事链路阶段 ③④⑤：

**凭证**

**来源**

**设置方式**

**用途**

百炼临时 api-key token

业务服务端下发短效 Key

`sdk.updateToken(token)`

SDK 与开放平台请求认证

Travel ticket

业务服务端代申请体验凭证

`createTravel({ ticket })`

Travel 的单次游玩凭证

**必须**

-   在 `travel.start()` 之前完成两者准备
-   SDK **不持久化、不自动刷新** token

**推荐**

-   token 过期或心跳 `onError` 后，经业务服务端重新申请并 `updateToken`

**避免**

-   混用两种 token
-   把主 API Key 放到业务前端

## Travel 生命周期

### 创建与启动

**必须**

-   `createTravel({ ticket, videoElement })` — `ticket` 为单次 Travel 凭证，`videoElement` 在此时传入
-   先注册 `statusChanged` / `onError`，再 `await travel.start()`，保证错误和状态感知

**推荐**

-   `prepare` 阶段展示 connecting UI，防止重复点击；监听 `travelInfoReady` 尽早读取会话信息，`firstFrameGenerated` 可用于展示首帧占位图

**避免**

-   DOM 元素尚未就绪时 create Travel

### 运行中

-   `statusChanged` 驱动 UI：`prepare` = 等待画面，`running` = 可交互
-   `pause` / `resume` / `rewind` 的使用场景与前置条件（由会话能力决定；`rewind` 需在 `paused` 且流已中断）

### 结束与重建

**必须**

-   结束会话：`await travel.end()`
-   创建新 Travel 前确保上一次已 end
-   页面卸载 / 路由离开时在 cleanup 中 `travel.end()`

**推荐**

-   失败后走「end → 清理监听 → 从故事链路 ③ 或 ⑤ 重试」
-   重试时重新申请体验凭证（若一次性）

**避免**

-   不 end 就 createTravel 第二次（同步 throw）
-   页面离开未 cleanup，导致 RTC 资源泄漏

## 视频元素与浏览器策略

**必须**

-   `<video>` 设置 `playsInline`（iOS 必需）
-   了解浏览器自动播放策略对 `autoPlay` / `muted` 的影响

**推荐**

-   `prepare` 阶段用首帧图 + 遮罩，`running` 后隐藏
-   按需配置 `streamReadyTimeout`（默认 15000ms），超时给出重试入口
-   播放器容器预留固定宽高比

**避免**

-   video 未挂载到 DOM 时传入元素引用
-   忽略 `paused` / 断流，UI 仍显示可交互

## 事件订阅与错误处理

### 事件订阅

**必须**

-   事件挂在 `Travel` 上，不是 `HappyOysterEngine` 上
-   保存 `travel.on(...)` / `travel.onError(...)` 返回的 unsubscribe 函数

**推荐**

-   集中注册、集中清理；切换 Travel 前先取消旧监听

**事件**

**用途**

`statusChanged`

状态展示、画面就绪判断（`running`）、按钮 enable/disable

`travelInfoReady`

RTC 连接前获取 `encryptedTravelId`、模式、首帧、体验时长与 角色演绎画幅；也可用 `travel.getInfo()` 读取

`firstFrameGenerated`

有非空首帧时，在 `travelInfoReady` 后触发；可用于在 `prepare` 阶段展示占位图

`error`（via `onError`）

日志、toast、触发 token 刷新

### 错误分层

-   **启动失败**：`travel.start()` reject（enter-travel / RTC / 超时）
-   **运行时错误**：`travel.onError`（RTC、心跳鉴权失败等）
-   业务服务端 / 开放平台错误在故事链路 ①–④ 阶段由业务层处理，不进 SDK

**避免**

-   只 catch `start()` 不监听 `onError`
-   重复注册监听但不 unsubscribe

## 指令发送：Command 与 Instruct

### sendCommand（实时操控）

`sendCommand()` 用于 Adventure（模式 `1`）下的实时操控，经 RTC DataChannel 发送，仅在会话处于 `running` 状态时可用。

SDK 最多约每 42ms（约 24FPS）发送一次指令：距上次发送已超过一个周期时立即发送；同一周期内调用多次时，只发送最后一次调用的完整指令。`translation`、`rotation`、`interaction` 是三个独立的控制维度，未传字段按 `None` 发送，SDK 不会跨调用合并字段，也不会周期性重复上一条指令或自动发送 `None`。

**单次动作**

跳跃、攻击等单次触发动作调用一次即可：

```
await travel.sendCommand({ interaction: "Jump" });
```
**持续动作**

移动、持续转动视角等动作，按住期间应持续调用。前端应用无需自行按 42ms 节流，SDK 会将高频调用合并为约 24FPS 的发送频率；松开时应显式发送一次 `None` 复位：

```
// 按住期间持续调用
void travel.sendCommand({ translation: "Front" });

// 松开时停止移动
void travel.sendCommand({ translation: "None" });
```
**避免**

-   `prepare` 阶段大量发送
-   用 sendCommand 发送自然语言实时导演内容

### sendInstruct（实时导演指令）

**必须**

-   Directing（模式 `2`）或 角色演绎（模式 `3`，非 `scriptlist`）会话；`await travel.sendInstruct({ content })`

**推荐**

-   发送前检查 content 非空，防止重复提交
-   根据返回的 `accepted` 等字段反馈用户

## 常见问题与排障

**现象**

**常见原因**

**建议处理**

初始化就报参数错误

`APIHost` 传了完整 URL，例如带 `https://` 或路径

只传裸 host，例如 `open-platform.example.com`

`travel.start()` 失败，提示 ticket 无效或已使用

`ticket` 是一次性凭证，可能过期、重复使用，或世界还没 ready

重新从服务端申请 `ticket`；确保世界状态为 ready 后再进入

运行一段时间后 `onError` 收到鉴权错误

百炼临时 api-key `token` 过期

前端向业务服务端重新申请 token，然后调用 `engine.updateToken(newToken)`

画面一直 loading 或 `start()` 超时

远端推流未就绪、网络慢、`streamReadyTimeout` 太短

给用户重试入口；必要时调大 `streamReadyTimeout`，并检查服务端/RTC 日志

第二次 `createTravel()` 报已有会话

上一次 Travel 没有 `end()`

页面切换、重试、退出时都调用 `await travel.end()` 并清理监听

按键或指令没有反应

当前状态不是 `running`，或 Adventure / Directing / 角色演绎模式用错 API

用 `statusChanged` 控制按钮可用性；调用前用 `travel.can(action)` 判断

排查问题时建议同时记录三类信息：SDK `ErrorCode`、当前 `TravelStatus`、业务服务端请求日志。这样基本可以判断问题是在凭证、状态、网络，还是渲染链路上。
