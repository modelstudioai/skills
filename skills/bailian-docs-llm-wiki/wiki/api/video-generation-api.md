# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、对口型、动作模仿、超清增强等核心场景。所有模型均采用统一异步调用范式（创建任务 → 轮询获取），适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同能力边界与演进阶段：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类基础能力，全部使用 `video-generation/video-synthesis` 统一端点 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **万相（WanX）**：能力最全的多模态视频模型家族，包含：
  - **万相3.0**：All-in-One 模型，统一支持文生、首帧/首尾帧生、参考生视频，最长30秒，30fps [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；
  - **万相2.7**：新版协议，支持首帧/首尾帧/视频续写三大图生任务，以及视频编辑、参考生视频等 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)；
  - **早期版本（2.1–2.6）**：已归档为 Legacy 模型，仅限存量用户维护，不推荐新接入 [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **爱诗（PixVerse）**：专注高表现力生成，支持文生、首帧/首尾帧生、参考生、对口型、动作模仿、超清六种能力，全部使用北京地域专属 endpoint。
- **可灵（Kling）与 Vidu**：分别提供 v3/v4 多代模型，v4 系列支持关键帧任意组合（首/中/尾帧）及官方主体库调用；Vidu 则聚焦首帧/首尾帧/参考生三类标准能力。

> **注意**：部分模型（如 `wan2.2-animate-move`、`wan2.2-animate-mix`、`videoretalk`、`video-style-transform`）使用 `/aigc/image2video/` 路径而非 `/aigc/video-generation/`，例如 `image2video/video-synthesis` 或 `image2video/face-detect`。该路径差异反映其底层架构归属图像驱动类模型，与纯视频生成模型路径不一致，开发者需按模型文档严格匹配 endpoint。

## 关键参数

所有视频 API 均遵循以下通用参数规范：

- **必选请求头**：
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`
  - `X-DashScope-Async: enable`（缺失将报错 `current user api does not support synchronous calls`）
- **必选请求体字段**：
  - `model`: 字符串，精确指定模型名称（如 `"wan3"`、`"kling/kling-v4-video-generation"`、`"vidu"`），**不可省略或拼写错误**；
  - `input`: 对象，结构依模型而异（如文生视频含 `prompt`；图生视频含 `image_url`；参考生视频含 `reference_images` 数组）；
  - `parameters`: 可选对象，用于控制生成细节（如 `size`、`duration`、`style`）。
- **地域强约束**：`model`、`endpoint URL`、`API Key` 必须同属一个地域（如华北2北京），跨地域调用必然失败。业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为强制推荐方案，旧域名（`dashscope.aliyuncs.com`）虽仍可用但性能与稳定性较低。

## 使用方式

所有视频生成任务均采用**标准两步异步流程**：

1. **创建任务**：发送 `POST` 请求至对应 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），携带完整参数。成功响应返回 JSON，含唯一 `task_id`（有效期 24 小时）。
2. **轮询结果**：使用 `GET https://.../api/v1/tasks/{task_id}` 定期查询（建议间隔 ≥5s），直至 `status` 为 `"SUCCESS"`，响应体中 `output.video_url` 即为生成视频直链。

> **注意**：`task_id` 全局唯一且不可复用，**严禁重复提交相同参数创建新任务**。轮询是唯一合法获取结果的方式，同步等待会导致超时失败。

## 限制和注意事项

- **地域与密钥绑定**：华北2（北京）与新加坡地域的 API Key 和 endpoint 完全隔离，混用将导致鉴权失败。其他地域（如东京、法兰克福、弗吉尼亚）仅部分模型支持，需查阅具体文档确认 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。
- **输入文件要求**：所有图片/视频/音频必须通过公网可访问的 HTTP/HTTPS URL 提交；本地文件需先调用临时存储接口获取 URL，且若使用 `oss://` 链接，必须添加请求头 `X-DashScope-OssResourceResolve: enable`，否则报错 `No connection adapters were found for 'oss://'`。
- **模型协议演进**：万相 2.7+、爱诗、可灵、Vidu 等新模型均使用新版统一协议；而万相 2.6 及更早、数字人 `wan2.2-s2v`、视频换人 `wan2.2-animate-mix` 等仍沿用旧版协议，二者在参数结构与 endpoint 路径上存在不兼容，迁移前务必验证。
- **免费额度与计费**：多数模型按视频秒数后付费（如 VideoRetalk 0.08元/秒），部分提供初始免费额度（如 VideoRetalk 1800秒）。详细资费请查阅各模型文档的“资费与限流”章节。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)


