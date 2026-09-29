# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有 API 均采用统一异步调用范式（创建任务 → 轮询结果），支持多地域部署与业务空间专属域名，面向开发者提供稳定、可扩展的视频生成服务。

## 支持的模型/功能

百炼当前提供三大主力视频生成模型系列，以及多类垂直场景专用模型：

- **HappyHorse**：支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频（基于首帧）](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类基础能力。
- **万相（WanX）**：提供全栈视频能力，包括[万相3.0-视频生成](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)（统一支持文/图/参考生视频）、[万相2.7系列](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)（图生视频、文生视频、参考生视频、视频编辑），以及[早期2.1–2.6模型](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)（已逐步归档，不推荐新接入）。
- **爱诗（PixVerse）**：专注高动态质量生成，支持[文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)、[图生视频（首帧/首尾帧）](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)、[视频对口型](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)和[视频动作模仿](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)。
- **数字人与人像驱动**：包含[万相数字人 wan2.2-s2v](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)（图片+音频生成说话视频）、[AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)（图片+动作模板生成舞蹈视频）、[EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)（图片+音频生成唱演视频）、[LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)（轻量级口型同步）、[VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)（视频口型替换）及[Emoji表情包](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)等。
- **其他**：[视频风格重绘](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)（8种艺术风格转换）、[可灵（Kling）](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)（独立模型，文档待补充）。

> **注意**：万相2.7系列与万相3.0均支持“图生视频”能力，但协议与输入结构不同。[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)明确指出其支持首帧/首尾帧/视频续写三类任务，而[万相-图生视频-基于首帧（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)仅支持首帧生视频，且已标注为“推荐优先选用新版”。开发者应以2.7及以上版本为准。

## 关键参数

所有视频生成 API 的核心请求参数结构高度一致，关键字段如下：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API Key>`，需与模型所在地域匹配
  - `X-DashScope-Async`: **必须设置为 `enable`**；缺失将报错 `current user api does not support synchronous calls`（见[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)）

- **请求体（Request Body）**
  - `model`: 模型名称（如 `wan2.7-t2v`, `pixverse/pixverse-v6-t2v`, `emo-v1`, `video-style-transform`），具体值需查阅对应模型文档
  - `input`: 输入数据对象，结构因模型而异：
    - 文生视频：含 `prompt`（文本提示词，长度限制依模型而定，如 wan2.7-t2v ≤5000字符）
    - 图/参考生视频：含 `img_url` 或 `media` 数组（含 `image_url`/`video_url`/`audio_url` 等）
    - 数字人/人像驱动：含 `image_url` + `audio_url`（EMO、LivePortrait、s2v）或 `video_url`（VideoRetalk）或 `driven_id`（Emoji）
    - 视频风格重绘：含 `video_url` + `parameters.style`（0–7整数）
  - `parameters`: 可选配置项，常见如 `resolution`（如 `"720P"`）、`style_level`（EMO）、`video_fps`（风格重绘）

## 使用方式

所有视频生成 API 均采用**标准异步流程**，无同步接口：

1. **创建任务**：`POST {WorkspaceId}.{Region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（或 `image2video/video-synthesis`，见下文说明）
   - 各地域 Endpoint 已标准化（北京、新加坡、东京、法兰克福、弗吉尼亚、中国香港、德国），URL 中 `{WorkspaceId}` 需替换为实际业务空间ID
   - **重要**：华北2（北京）与新加坡地域已启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），[官方强烈建议迁移](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)，以获得更高性能与稳定性

2. **轮询结果**：使用返回的 `task_id`（有效期24小时）调用 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS` 并获取 `output.video_url`

> **注意**：部分模型（如万相数字人 s2v、AnimateAnyone、EMO、LivePortrait、VideoRetalk、Emoji）使用 `/api/v1/services/aigc/image2video/...` 路径而非 `/video-generation/...`。例如，[万相数字人 wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md) 和 [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md) 均明确使用 `image2video/video-synthesis`。开发者需严格按各模型文档指定路径调用，不可统一套用 `/video-generation`。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL 与 API Key **必须属于同一地域**，跨地域调用必然失败（所有文档均强调此点，如[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)）。
- **任务管理**：`task_id` 有效期为24小时；**禁止重复创建相同任务**，应复用 `task_id` 轮询（所有文档均明确警示）。
- **输入格式约束**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP；分辨率通常要求宽高 ≥400px 且 ≤7000px（如[EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)）；需公网可访问 URL。
  - 视频：格式多为 MP4/AVI/MOV；时长通常 ≤30–120秒；大小 ≤100–300MB（如[VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)）。
  - 音频：格式多为 WAV/MP3；时长通常 ≤20–120秒；需清晰人声、无背景噪音（如[万相数字人 wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)）。
- **前置检测要求**：数字人与人像驱动类模型（s2v、AnimateAnyone、EMO、LivePortrait、Emoji）**必须先通过对应图像检测API**（如 `s2v-detect`, `animate-anyone-detect-gen2`, `emo-detect-v1`），否则生成失败或效果不佳。
- **计费与限流**：各模型独立计费（按秒/张/任务），免费额度与RPS/QPS限制差异显著（如[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)中 `wan2.2-s2v` 限流为“同时处理中任务数量：100秒”，而 `wan2.2-s2v-detect` 为“同步接口无限制”）。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)


