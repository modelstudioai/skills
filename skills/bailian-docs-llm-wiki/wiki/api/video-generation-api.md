# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

平台当前提供三大主力视频生成模型系列，以及多类垂直场景专用模型：

- **HappyHorse**：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：提供全栈能力，包括万相3.0（All-in-One统一模型，支持文/图/参考生视频）、万相2.7（新版协议，覆盖图生视频、参考生视频、视频编辑）、早期版本（2.1–2.6）及专项模型（图生动作、视频换人、数字人 s2v）[万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)。
- **爱诗（PixVerse）**：专注高质量创意视频生成，支持文生视频、首尾帧生视频、参考生视频、视频对口型、动作模仿、超清增强等 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **人像驱动系列**：聚焦人物动态生成，包含 AnimateAnyone（舞蹈）、EMO（唱演）、LivePortrait（播报）、VideoRetalk（口型替换）、Emoji（表情包）及视频风格重绘等 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)。

> **注意**：万相2.7系列与万相3.0虽均使用 `/api/v1/services/aigc/video-generation/video-synthesis` 统一路径，但协议细节与参数要求不同；而万相2.2-s2v（数字人）及 AnimateAnyone 等模型则使用 `/api/v1/services/aigc/image2video/` 路径，二者不可混用。

## 关键参数

所有视频生成 API 的通用关键参数如下：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API Key>`，需与模型地域匹配
  - `X-DashScope-Async`: 必须设置为 `enable`，否则返回 `"current user api does not support synchronous calls"` 错误（见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)）

- **请求体（Request Body）**
  - `model`: 字符串，必需，指定具体模型名（如 `wan2.7-text2video`, `pixverse/pixverse-v6-t2v`, `liveportrait`）
  - `input`: 对象，必需，结构因模型而异：
    - 文生视频：含 `prompt`（文本提示词，长度≤5000字符）和可选 `negative_prompt`
    - 图/参考生视频：含 `img_url` 或 `media` 数组（含 `image_url`/`video_url`/`audio_url`）
    - 数字人/口型替换：必须含 `image_url` 和 `audio_url`（或 `video_url`）
  - `parameters`: 对象，可选，用于控制输出质量（如 `resolution`, `style`, `video_fps`）

## 使用方式

1. **准备环境**：开通对应模型服务，获取并配置该地域的 API Key，确认业务空间 ID（WorkspaceId）。
2. **构造请求**：使用业务空间专属域名（推荐）或通用域名，向 `POST /api/v1/services/aigc/{service}/video-synthesis` 提交任务（`{service}` 为 `video-generation` 或 `image2video`）。
3. **轮询结果**：用返回的 `task_id` 调用 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，从 `output.video_url` 获取结果。

> **注意**：部分模型（如万相2.2-s2v、EMO、LivePortrait）要求先调用图像检测 API（如 `face-detect`）验证输入合规性，并将检测返回的 `face_bbox`/`ext_bbox` 作为后续生成请求的入参，否则可能失败 [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL 与 API Key 必须同属一个地域（如华北2北京、新加坡），跨地域调用必然失败，且不同地域的 API Key 不可复用。
- **异步时效性**：所有视频任务均为异步，典型耗时 1–5 分钟（数字人、风格重绘等可达 10 分钟），`task_id` 仅在 24 小时内有效。
- **输入格式约束**：
  - 图像：支持 JPG/PNG/WEBP/BMP，分辨率通常要求 400–7000 像素，文件 ≤10MB；
  - 视频：支持 MP4/AVI/MOV，时长 ≤30–120 秒，大小 ≤100–300MB，帧率 ≥15fps；
  - 音频：支持 WAV/MP3，时长 1–120 秒，需清晰人声、无背景噪音。
- **URL 访问要求**：所有 `*_url` 字段必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口转换。
- **模板与特效**：万相早期模型（2.1–2.6）支持视频特效（如 `flying`, `hanfu-1`），但仅限于“图生视频-基于首帧”和“基于首尾帧”两类模型，且 `prompt` 字段在特效模式下会被忽略 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


