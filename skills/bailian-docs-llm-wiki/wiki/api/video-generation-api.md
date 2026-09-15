# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等场景。所有视频生成 API 均采用异步调用模式，需先创建任务获取 `task_id`，再轮询查询结果。调用前必须确保模型、Endpoint URL 与 API Key 三者地域一致。

## 支持的模型/功能

视频生成 API 覆盖三大技术路径：

- **通用视频生成模型**：  
  - `HappyHorse` 系列（[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)）支持文生视频、图生视频（基于首帧）、参考生视频及视频编辑；  
  - `万相`（WanX）系列提供多代演进模型：`万相3.0-视频生成`为 All-in-One 统一模型，支持文生、图生（首帧/首尾帧）、参考生视频；`万相2.7`各子模型（文生、图生、参考生、视频编辑）为新版协议主力；早期 `2.1–2.6` 模型已标记为 legacy，[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md) 文档明确建议优先选用 2.7+ 版本。

- **人像驱动与数字人模型**：  
  - `数字人 wan2.2-s2v`（[数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)）基于单图+音频生成说话/唱歌视频；  
  - `AnimateAnyone`、`EMO`、`LivePortrait`、`VideoRetalk`、`Emoji` 等均属人像驱动类，需先通过对应图像检测 API（如 `emo-detect-v1`）验证输入合规性，再生成视频。

- **垂直功能模型**：  
  - `爱诗`（PixVerse）提供文生、图生（首帧/首尾帧）、视频对口型、动作模仿、超清等能力；  
  - `视频风格重绘` 支持 8 种预设艺术风格转换；  
  - `万相-图生动作`、`万相-视频换人`、`万相-视频特效` 等面向特定编辑需求。

> **注意**：部分模型（如 `万相-首尾帧生视频API参考（2.2）`）使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而主流视频生成模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。路径不一致可能引发调用失败，务必按具体模型文档确认 endpoint。

## 关键参数

所有视频生成请求均需以下基础参数：

- **请求头（Headers）**：
  - `Content-Type: application/json`（必选）；
  - `Authorization: Bearer <API_KEY>`（必选）；
  - `X-DashScope-Async: enable`（必选，异步模式强制要求，缺失将报错 `"current user api does not support synchronous calls"`）。

- **请求体（Request Body）**：
  - `model`（string，必选）：模型名称，如 `wan2.7-t2v`、`happyhorse-t2v`、`pixverse/pixverse-v6-t2v`、`emoji-v1` 等；
  - `input`（object，结构因模型而异）：
    - 文生视频：`prompt`（文本提示词）；
    - 图生视频：`img_url`（首帧图）或 `first_frame_url` + `last_frame_url`（首尾帧）；
    - 参考生视频：`ref_images`（图片数组）或 `ref_video_url`；
    - 数字人/人像驱动：`image_url` + `audio_url`；
    - 视频编辑/对口型：`video_url` + `audio_url` 或 `tts_content`；
  - `parameters`（object，可选）：常见字段包括 `resolution`（如 `"720P"`）、`style`（风格重绘）、`duration`（时长）、`fps`（帧率）等。

- **地域与业务空间**：所有 `POST` 请求 URL 中的 `{WorkspaceId}` 必须替换为真实业务空间 ID，且该 ID 所属地域须与所选模型、API Key 严格一致。

## 使用方式

标准流程为两步异步调用：

1. **创建任务**：发送 `POST` 请求至对应地域的 endpoint（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），携带上述参数，成功后返回 `task_id`；
2. **轮询结果**：使用 `task_id` 调用任务状态查询接口（具体路径见各模型文档），直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：`task_id` 有效期为 24 小时，过期后无法查询结果；重复创建相同任务将导致冗余计费，应避免。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京、新加坡等），跨地域调用必然失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已成推荐标准，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。
- **输入资源要求**：  
  - 图片：格式（JPG/PNG/WEBP等）、尺寸（宽高通常 ≥400px 且 ≤7000px）、大小（≤5–10MB）、公网可访问；  
  - 视频：格式（MP4/AVI/MOV等）、时长（通常 ≤30–120s）、大小（≤100–300MB）、分辨率（单边 ≥256px 且 ≤4096px）；  
  - 音频：格式（WAV/MP3）、时长（通常 1–120s）、清晰人声、无背景噪音。
- **前置检测要求**：`EMO`、`LivePortrait`、`AnimateAnyone`、`Emoji`、`wan2.2-s2v` 等模型必须先调用对应 `detect` 接口（如 `emo-detect-v1`）验证输入合规性，否则生成任务将失败。
- **计费与限流**：多数模型按秒/次计费，免费额度有限；QPS/RPS 与并发任务数受账号级别限制（如 `emo-v1` 同时处理中任务数上限为 1），超出将触发限流错误。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)


