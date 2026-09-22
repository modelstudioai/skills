# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有视频生成 API 均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **通用视频生成模型**：  
  - `HappyHorse` 系列（[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频、参考生视频、视频编辑）  
  - `万相`（Wan）系列：`wan3.0`（All-in-One，统一支持文/图/参考生视频）、`wan2.7`（新版协议，推荐使用）及早期 `wan2.1–2.6`（已逐步淘汰）  
  - `爱诗`（PixVerse）系列：支持文生视频、首帧/首尾帧生视频、参考生视频、对口型、动作模仿、超清增强等细分能力  

- **人像驱动与数字人模型**：  
  - `万相-s2v`（单图+音频生成说话/唱歌视频）  
  - `AnimateAnyone`（图+动作模板生成舞蹈视频）  
  - `EMO`、`LivePortrait`、`VideoRetalk`、`Emoji`（均属[人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)体系，专注肖像动态生成）  
  - `视频风格重绘`（8种预设艺术风格转换）  

- **专用能力模型**：  
  - `万相-图生动作`（animate-move）、`万相-视频换人`（animate-mix）、`万相-视频特效`（仅限 legacy 图生视频）等  

> **注意**：`wan2.1–2.6` 系列（如 [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)）为旧版协议，已不推荐新项目接入；`wan3.0` 和 `wan2.7` 为当前主力版本，功能更全、稳定性更高。

## 关键参数

所有视频生成 API 的通用关键参数如下：

- **请求头（Headers）**（必选）：
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <your_api_key>`
  - `X-DashScope-Async`: `enable`（**必须显式设置**，否则报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**（必选）：
  - `model`: 模型名称（如 `wan3.0`、`pixverse/pixverse-v6-t2v`、`emo-v1`、`video-style-transform` 等）
  - `input`: 输入对象，结构因模型而异：
    - 文生视频：`prompt`（文本提示词，≤5000字符）
    - 图生视频：`img_url`（首帧图）、`first_frame_url` + `last_frame_url`（首尾帧）
    - 参考生视频：`reference_images` 或 `reference_video_url`
    - 数字人/口型驱动：`image_url` + `audio_url`（或 TTS 参数）
    - 风格重绘：`video_url` + `parameters.style`（0–7 整数）

- **地域与业务空间**：  
  Endpoint URL 中的 `{WorkspaceId}` 必须替换为真实业务空间 ID（见 [业务空间详情](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)），且该空间需与所选模型、API Key 所在地域一致。

## 使用方式

1. **开通服务并配置环境**：  
   在 [百炼控制台模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market) 开通对应模型，获取该地域的 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。

2. **构造异步请求**：  
   向对应地域的 Endpoint 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis`（或 `/image2video/video-synthesis`，见下文限制说明）请求，携带上述关键参数。

3. **轮询获取结果**：  
   使用返回的 `task_id` 调用 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，从 `output.video_url` 获取最终视频地址。

> **注意**：部分模型（如 `万相-首尾帧生视频（2.2）`、`AnimateAnyone`、`EMO`、`LivePortrait`、`VideoRetalk`、`Emoji`、`视频风格重绘`）使用 `/image2video/` 路径而非 `/video-generation/`，详见各模型文档。例如 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md) 明确要求 `POST .../aigc/image2video/video-synthesis`。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京、新加坡、东京等），否则直接失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为推荐路径，旧域名（如 `dashscope.aliyuncs.com`）仍可用但性能与稳定性较低。

- **异步强制要求**：所有视频生成任务均不支持同步调用，`X-DashScope-Async: enable` 为硬性 Header，缺失即报错。

- **输入合规性检查**：多数人像类模型（如 `EMO`、`LivePortrait`、`Emoji`、`AnimateAnyone`、`wan2.2-s2v`）要求先调用独立的图像检测 API（如 `emo-detect-v1`、`liveportrait-detect`）验证输入图片质量，检测通过后方可进入视频生成流程。

- **文件与内容限制**：  
  - 图片：格式 JPG/PNG/WEBP，分辨率 400–7000px，大小 ≤10MB  
  - 视频：格式 MP4/AVI/MOV，时长 ≤30–120s，大小 ≤100–300MB，帧率 15–60fps  
  - 音频：格式 WAV/MP3，时长 ≤20–180s，需人声清晰、无背景噪音  

- **任务管理**：`task_id` 有效期 24 小时，禁止重复提交相同任务；轮询间隔建议 ≥2 秒，避免触发限流。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
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
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)


