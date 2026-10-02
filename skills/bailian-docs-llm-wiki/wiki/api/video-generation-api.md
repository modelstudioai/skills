# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有视频类 API 均采用异步调用模式（创建任务 → 轮询获取结果），任务耗时通常为 1–5 分钟，`task_id` 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

平台当前提供三大主力视频模型系列及配套能力：

- **HappyHorse**：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：覆盖全栈视频生成编辑能力，包括万相2.7（推荐新版协议）和早期2.1–2.6系列。2.7版本统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 接口，支持文生、图生（首帧/首尾帧/续写）、参考生、视频编辑等多模态任务；早期版本（如 wan2.1–2.6）部分接口路径不同（如 `/api/v1/services/aigc/image2video/video-synthesis`），且功能受限 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **爱诗（PixVerse）**：专注高质量创意视频生成，提供文生、图生（首帧/首尾帧）、参考生、对口型（lipsync）、动作模仿、超清（upscale）等细分能力，各任务类型对应独立模型标识（如 `pixverse/pixverse-v6-t2v`、`pixverse/pixverse-lipsync`） [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)。

此外，还提供专用人像驱动模型：
- **数字人系列**：`wan2.2-s2v`（单图+音频生成说话/唱歌视频）、`emo-v1`（肖像+音频生成唱演视频）、`liveportrait`（轻量级播报视频）、`videoretalk`（视频口型替换）、`emoji-v1`（表情包模板驱动）；
- **动作迁移系列**：`animate-anyone-gen2`（图片+动作模板生成舞蹈视频）；
- **后处理系列**：`video-style-transform`（8种预设艺术风格重绘）。

> **注意**：万相2.7与早期万相（2.1–2.6）存在协议不兼容。例如，万相2.7图生视频要求 `X-DashScope-Async: enable` 头且仅支持新 endpoint，而万相2.2首尾帧生视频文档中明确使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径 [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)，与2.7路径不同，不可混用。

## 关键参数

所有主流视频 API（HappyHorse、万相2.7、爱诗）共用以下核心请求结构：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API_KEY>`
  - `X-DashScope-Async`: 必须为 `enable`（缺失将报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**
  - `model`: 字符串，指定模型标识（如 `wan2.7-text2video`, `pixverse/pixverse-v6-t2v`, `emoji-v1`）
  - `input`: 对象，内容依任务类型而异：
    - 文生视频：`prompt`（文本提示词，长度限制因模型而异，如 wan2.7-text2video ≤5000字符）
    - 图生视频：`img_url`（首帧图URL）或 `first_frame_url` + `last_frame_url`（首尾帧）
    - 参考生视频：`ref_images` 数组或 `ref_video_url`
    - 视频编辑/对口型：`media` 数组，含 `video_url` 及 `audio_url` 或 TTS 参数
    - 数字人/EMO/LivePortrait：`image_url` + `audio_url`
    - 表情包：`image_url` + `face_bbox` + `ext_bbox`（需先经检测API获取）
  - `parameters`: 可选对象，常见字段包括：
    - `resolution`: 如 `"720P"`、`"4K"`
    - `style`: 风格类型（如 `video-style-transform` 的 `style: 0` 表示日式漫画）
    - `fps`: 输出帧率（如 `15`–`25`）

## 使用方式

1. **地域对齐**：在控制台确认模型所属地域（如华北2北京），获取该地域的 API Key，并配置对应 endpoint（推荐使用业务空间专属域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
2. **创建任务**：向 `POST /api/v1/services/aigc/video-generation/video-synthesis`（或少数旧模型的 `/image2video/video-synthesis`）发送请求，携带上述 Headers 和 Body，获得 `task_id`。
3. **轮询结果**：使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}`（具体路径见各模型文档）查询状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：数字人 `wan2.2-s2v`、`emo-v1`、`liveportrait` 等模型必须前置图像检测步骤（如调用 `wan2.2-s2v-detect` 或 `emo-detect-v1`），并将检测返回的 `face_bbox`/`ext_bbox` 作为视频生成请求的入参，否则会失败。

## 限制和注意事项

- **地域强约束**：模型、API Key、Endpoint URL 必须同属一个地域（如北京），混用将导致鉴权失败或服务报错。
- **异步强制性**：所有视频 API 仅支持异步，`X-DashScope-Async: enable` 为必填头，同步调用不被支持。
- **资源限制**：
  - 输入媒体格式与大小有严格要求（如视频 ≤300MB、图像边长 400–7000px、音频时长 <120s），详见各模型文档。
  - `task_id` 有效期为 24 小时，超时需重新提交任务。
- **模型演进**：万相2.7为当前推荐版本，旧版（2.1–2.6）已标记为“早期模型”，功能与协议均落后，应优先迁移 [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **预检依赖**：数字人、EMO、LivePortrait、Emoji 等人像驱动模型，必须先调用对应 `detect` API 验证输入合规性并获取坐标参数，不可跳过。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
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
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)


