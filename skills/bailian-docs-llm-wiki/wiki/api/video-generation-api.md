# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑及人像驱动等场景。所有视频生成 API 均采用异步调用模式（创建任务 → 轮询结果），任务耗时通常为 1–5 分钟，`task_id` 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前支持三大主力模型系列及专用人像驱动模型：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，物理真实感强、运动流畅 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：覆盖全链路视频生成需求，包括：
  - `wan3.0`：全能参考视频生成模型，统一支持文生视频、首帧/首尾帧图生视频、参考生视频，最长输出 30 秒、30fps [万相3.0-视频生成](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；
  - `wan2.7`：新版协议模型，支持图生视频（首帧/首尾帧/视频续写）、文生视频、参考生视频、视频编辑四大任务，推荐优先选用 [万相2.7-图生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)；
  - 早期模型（2.1–2.6）已标记为 Legacy，仅限特定场景使用，不推荐新项目接入 [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **爱诗（PixVerse）**：专注高动态表现，提供文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型、动作模仿、超清增强等细分能力，支持多版本模型选型（如 `c1` 适配打斗特效，`v6` 为通用推荐） [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **人像驱动系列**（华北2专属）：均需先调用图像检测模型（如 `emo-detect-v1`、`liveportrait-detect`），再调用生成模型，包括：
  - `EMO`（唱演）、`LivePortrait`（播报）、`AnimateAnyone`（舞蹈）、`VideoRetalk`（口型替换）、`Emoji`（表情包）、`VideoStyleTransform`（风格重绘）。

> **注意**：部分文档存在 endpoint 路径不一致问题。例如，万相2.2系列的图生动作（`wan2.2-animate-move`）、视频换人（`wan2.2-animate-mix`）、数字人（`wan2.2-s2v`）及多数人像驱动模型（如 `AnimateAnyone`、`EMO`）均使用 `/api/v1/services/aigc/image2video/...` 路径；而 HappyHorse、万相2.7/3.0、爱诗等主流视频生成模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。开发者务必根据所选模型查阅对应文档路径，不可混用。

## 关键参数

所有 HTTP 请求必须包含以下请求头：

- `Content-Type: application/json`
- `Authorization: Bearer <API_KEY>`
- `X-DashScope-Async: enable`（**强制要求**，缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：

| 字段 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 模型标识符，如 `wan3.0`、`pixverse/pixverse-v6-t2v`、`emo-v1` 等，不同模型系列值不同 |
| `input` | object | ✅ | 输入数据容器，结构因模型而异：<br>• 文生视频：含 `prompt`（文本提示词）<br>• 图生视频：含 `img_url`（首帧图）或 `first_frame_url` + `last_frame_url`<br>• 参考生视频：含 `ref_images` 或 `ref_video_url`<br>• 人像驱动：含 `image_url` + `audio_url`（或 `face_bbox`/`ext_bbox` 等检测返回坐标）<br>• 视频编辑/风格重绘：含 `video_url` |
| `parameters` | object | ❌ | 可选配置，常见项：<br>• `resolution`: 如 `"720P"`<br>• `style`: 风格重绘中指定风格 ID（0–7）<br>• `video_fps`: 输出帧率（15–25）<br>• `style_level`: EMO 动作风格强度（`"calm"`/`"normal"`/`"active"`） |

## 使用方式

1. **开通服务并获取凭证**：在百炼控制台开通对应模型，获取该地域的 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求 URL**：使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/...`，其中 `{WorkspaceId}` 为控制台“业务空间详情”中查看的 ID；旧域名（如 `dashscope.aliyuncs.com`）仍可用但性能与稳定性较低。
3. **发起异步任务**：`POST` 请求提交任务，成功后获得 `task_id`。
4. **轮询获取结果**：使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}` 查询状态，`status` 为 `"SUCCESS"` 时返回 `output.video_url`。

> **注意**：所有视频生成任务均需严格遵循“地域一致性”原则。例如，若模型在华北2（北京）开通，则必须使用北京地域的 API Key、北京地域的 WorkspaceId 和北京地域的 Endpoint URL。新加坡、美国等其他地域同理，且各地域凭证不可复用 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

## 限制和注意事项

- **地域隔离**：模型、API Key、Endpoint URL 必须同属一个地域，跨地域调用必然失败，错误码通常为鉴权失败或 404。
- **输入格式约束**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，尺寸通常要求宽高 ≥400px 且 ≤7000px，文件大小 ≤10MB；
  - 视频：MP4/AVI/MOV 等常见格式，时长 ≤30 秒（部分模型如 `VideoStyleTransform`），大小 ≤100MB；
  - 音频：WAV/MP3，时长 ≤20 秒（`wan2.2-s2v`）或 ≤3 分钟（`LivePortrait`），需人声清晰、无背景噪音。
- **预处理依赖**：人像驱动类模型（`EMO`、`LivePortrait`、`AnimateAnyone`、`Emoji`）**必须先调用对应图像检测 API**（如 `emo-detect-v1`），并将返回的 `face_bbox`、`ext_bbox` 等坐标作为生成请求的入参，否则任务会失败。
- **计费与限流**：多数模型按秒计费（如 `wan2.2-s2v` 0.5 元/秒），部分按次（如 `emo-detect-v1` 0.004 元/张）。各模型有独立 QPS/RPS 限制及并发任务数上限（如 `liveportrait` 同时处理中任务数为 1），详见各模型文档。
- **URL 编码**：若 `video_url` 或 `audio_url` 包含中文等非 ASCII 字符，必须进行 URL 编码，否则请求可能被拒绝。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
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
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
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
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)


