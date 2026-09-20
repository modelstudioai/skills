# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑、数字人及风格化处理等场景。所有视频生成 API 均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **通用视频生成模型**：  
  - `HappyHorse` 系列（[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[HappyHorse-图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[HappyHorse-参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)、[HappyHorse-视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)）支持物理真实、运动流畅的高质量视频生成；  
  - `万相3.0` 是全能参考视频生成模型（All-in-One），统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频等多种用法，最长可生成 30 秒、30fps 视频 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；  
  - `万相2.7` 系列（[万相2.7-文生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)、[万相2.7-图生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)、[万相2.7-参考生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)、[万相2.7-视频编辑](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)）为新版协议模型，推荐优先选用，旧版（2.1–2.6）已归档为[早期视频模型](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。

- **人像驱动与数字人模型**：  
  - `万相-s2v`（[数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)）基于单张图片+音频生成说话/唱歌视频；  
  - `AnimateAnyone`、`EMO`、`LivePortrait`、`VideoRetalk`、`Emoji` 等构成[人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)体系，均需先通过对应图像检测模型（如 `emo-detect-v1`、`liveportrait-detect`）验证输入合规性；  
  - `视频风格重绘` 支持 8 种预设艺术风格转换 [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)。

- **爱诗（PixVerse）系列**：  
  提供 `pixverse-c1`（强动态特效）、`pixverse-v6`（通用推荐）、`pixverse-v5.6`（已建议升级）三类模型变体，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型等完整链路 [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)。

> **注意**：部分文档存在 endpoint 路径不一致问题。例如，`万相-图生动作`（文档17）和`万相-视频换人`（文档18）使用 `/api/v1/services/aigc/image2video/video-synthesis`，而绝大多数视频生成模型（如 HappyHorse、万相3.0、爱诗）使用 `/api/v1/services/aigc/video-generation/video-synthesis`。实际调用请以各模型最新文档为准，避免路径混淆导致 404 错误。

## 关键参数

所有视频生成 API 共享以下核心请求参数结构：

- **请求头（Headers）必选**：
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`
  - `X-DashScope-Async: enable`（**必须显式设置**；缺失将报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）必选字段**：
  - `model`: 字符串，指定模型名称（如 `"wan2.7-t2v"`、`"pixverse/pixverse-v6-t2v"`、`"emoji-v1"`）
  - `input`: 对象，内容因模型而异：
    - 文生视频：`{"prompt": "a cat dancing"}`  
    - 图生视频（首帧）：`{"img_url": "https://...", "prompt": "..."}`
    - 首尾帧：`{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`  
    - 参考生视频：`{"reference_images": [...], "prompt": "..."}`  
    - 数字人/人像驱动：`{"image_url": "...", "audio_url": "..."}`  
    - 视频风格重绘：`{"video_url": "...", "parameters": {"style": 0}}`

- **通用可选参数**：
  - `parameters.resolution`: 如 `"720P"`（部分模型支持）  
  - `parameters.negative_prompt`: 反向提示词，用于排除不良内容（如万相2.7-videoedit）  
  - `parameters.style_level`: 动作风格强度（如 EMO 的 `"active"`/`"normal"`/`"calm"`）

## 使用方式

1. **前置准备**：  
   - 在阿里云百炼控制台开通对应模型服务；  
   - 确认模型、Endpoint URL 和 API Key 属于**同一地域**（如华北2北京）；  
   - 获取业务空间 ID，并将旧域名（如 `https://dashscope.aliyuncs.com`）迁移至新业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高稳定性与性能 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。

2. **步骤1：创建任务**  
   向对应地域的 Endpoint 发起 `POST /api/v1/services/aigc/video-generation/video-synthesis`（或 `/image2video/video-synthesis`，依模型而定），传入完整请求头与 body，成功后返回 JSON 包含 `task_id`。

3. **步骤2：轮询获取结果**  
   使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}`（具体路径见各模型文档），轮询状态直至 `status == "SUCCESS"`，响应中 `output.video_url` 即为生成视频直链。

4. **特殊流程**（仅限人像驱动类模型）：  
   - 必须先调用对应图像检测 API（如 `emo-detect-v1`、`liveportrait-detect`）验证输入图片；  
   - 检测通过后，将返回的 `face_bbox` 与 `ext_bbox` 坐标作为后续视频生成 API 的入参。

## 限制和注意事项

- **地域强一致性要求**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败，且不同地域的 API Key 不可混用 [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)。  
- **异步强制约束**：所有视频生成任务均为异步，`X-DashScope-Async: enable` 请求头为硬性要求，同步调用不被支持。  
- **输入资源要求**：  
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，通常要求最小边长 ≥400px，最大边长 ≤7000px；  
  - 视频：MP4/AVI/MOV 等常见格式，大小 ≤300MB，时长 2–120 秒，分辨率适配模型要求；  
  - 音频：WAV/MP3，清晰人声，无背景噪音，时长 1–120 秒；  
  - 所有媒体文件必须为公网可访问的 HTTP/HTTPS URL；本地文件需先调用[临时文件上传接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)获取有效链接。  
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询；请勿重复提交相同任务，应复用已有 `task_id` 轮询。  
- **计费与限流**：多数模型按秒/次计费（如 `wan2.2-s2v` 为 0.5 元/秒），并设有免费额度与 QPS/RPS 限制，详情参见各模型资费说明。  
- **模板与特效**：万相早期模型（2.1–2.6）支持视频特效（如 `flying`、`hanfu-1`），但仅适用于特定模型（如 `wanx2.1-i2v-turbo`），且无需传入 `prompt` [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)


