# video generation api

百炼平台的视频生成 API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，由 HappyHorse、万相（WanX）、爱诗（PixVerse）、数字人及人像驱动系列模型共同支撑。所有接口均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格同地域，否则调用将失败。

## 支持的模型/功能

当前支持三大主力模型家族及细分能力：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：覆盖全栈视频生成场景，包括：
  - 万相3.0（All-in-One）：统一支持文生视频、首帧/首尾帧图生视频、参考生视频，最长生成30秒、30fps视频 [万相3.0-视频生成](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；
  - 万相2.7系列：分模型提供图生视频（支持首帧/首尾帧/视频续写）、参考生视频、视频编辑等增强能力；
  - 早期模型（2.1–2.6）已标记为**过时**，文档明确提示“推荐优先选用”新版协议 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
- **爱诗（PixVerse）**：聚焦高动态质量生成，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、动作模仿、超清增强等功能，提供 c1/v6/v5.6 多版本模型选型 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **数字人与人像驱动**：专注单图+音频驱动的肖像视频生成，含 EMO（唱演）、LivePortrait（播报）、VideoRetalk（口型替换）、AnimateAnyone（舞蹈）、Emoji（表情包）等垂直模型，均需先通过图像检测 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。

> **注意**：万相2.2-s2v（数字人）、AnimateAnyone、EMO、LivePortrait 等人像驱动模型**仅支持华北2（北京）地域**，且必须使用该地域专属 API Key；而 HappyHorse、万相3.0、爱诗等通用视频模型支持北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港等多地域。

## 关键参数

所有视频生成 API 均需以下通用请求头：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选）
- `X-DashScope-Async: enable`（**必选**；缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：

- `model`（string，必选）：模型标识符，如 `happyhorse-text2video`、`wan3-video-generation`、`pixverse/pixverse-v6-t2v`、`emo-v1` 等。
- `input`（object，必选）：根据模型类型差异较大：
  - 文生视频：`prompt`（文本提示词，长度≤5000字符）
  - 图生视频：`img_url`（首帧图公网URL），部分支持 `template`（特效模板，见[万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)）
  - 参考生视频：`ref_img_urls` 或 `ref_video_url`（数组或单URL）
  - 数字人/人像驱动：`image_url` + `audio_url`（或 `lip_sync_tts_content`）
- `parameters`（object，可选）：控制生成质量，常见参数包括：
  - `resolution`（如 `"720P"`）
  - `style`（风格ID，如视频风格重绘中 `0` 表示日式漫画）
  - `video_fps`（帧率，默认15，范围15–25）
  - `animate_emotion`（是否优化面部表情）

## 使用方式

1. **准备环境**：开通对应模型服务 → 获取同地域 API Key → 配置至环境变量 `DASHSCOPE_API_KEY` → 确认业务空间 ID（WorkspaceId）。
2. **构造请求**：使用地域专属 Endpoint，例如北京地域为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（注意：数字人/人像驱动部分模型仍使用旧路径 `.../image2video/video-synthesis`，详见各模型文档）。
3. **提交任务**：`POST` 请求创建任务，获取 `task_id`。
4. **轮询结果**：使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status == "SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：万相2.2-s2v（数字人）流程特殊，需**先调用 `wan2.2-s2v-detect` 检测图片合规性**，再调用 `wan2.2-s2v` 生成视频；类似地，EMO、LivePortrait、AnimateAnyone、Emoji 等均要求前置图像检测步骤，不可跳过 [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同地域，跨地域调用必然失败（所有文档均强调此点）。
- **异步时效性**：`task_id` 有效期 24 小时，超时需重提任务；轮询间隔建议 ≥3 秒。
- **输入格式限制**：
  - 图片：支持 JPG/PNG/BMP/WEBP，尺寸通常要求 400–7000 像素，文件 ≤10MB；
  - 视频：MP4/AVI/MOV 等，时长 ≤30–120 秒，大小 ≤100–300MB；
  - 音频：WAV/MP3，时长 ≤20–120 秒，需清晰人声、无背景噪音。
- **模型兼容性**：万相2.7+、爱诗、HappyHorse 新版均使用 `/video-generation/video-synthesis` 统一路径；而万相2.2-s2v、VideoRetalk、AnimateAnyone 等仍沿用 `/image2video/xxx` 路径，不可混用。
- **计费与限流**：多数模型按秒计费（如 wan2.2-s2v 720P 0.9元/秒），并设免费额度与并发数限制（如 LivePortrait 同时处理中任务数上限为 1），详情需查阅各模型价格文档。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)


