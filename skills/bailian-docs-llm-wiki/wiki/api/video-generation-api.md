# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动及风格重绘等场景。所有接口均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前支持三大类视频模型体系：

- **HappyHorse 系列**：提供文生视频、图生视频（基于首帧）、参考生视频和视频编辑四类能力，统一使用 `video-synthesis` 接口路径，模型名如 `happyhorse-text-to-video`、`happyhorse-image-to-video` 等 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **万相（WanX）系列**：覆盖全链路视频生成需求，包括：
  - 万相3.0（All-in-One）：统一支持文生、图生（首帧/首尾帧）、参考生视频，最长30秒，30fps [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；
  - 万相2.7：新版协议，支持图生视频（含首帧/首尾帧/视频续写）、文生视频、参考生视频、视频编辑等，推荐优先选用；
  - 早期模型（2.1–2.6）：已逐步归档，仅限特定场景（如特效模板），详见 [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **人像驱动与垂直模型**：包括数字人（wan2.2-s2v）、舞动人像（AnimateAnyone）、悦动人像（EMO）、灵动人像（LivePortrait）、声动人像（VideoRetalk）、表情包（Emoji）及视频风格重绘等，均需先通过对应图像检测模型（如 `wan2.2-s2v-detect`、`emo-detect-v1`）校验输入合规性。

> **注意**：万相2.7 图生视频与万相2.2 首尾帧生视频虽功能重叠，但接口路径不一致：前者使用 `/aigc/video-generation/video-synthesis`，后者使用 `/aigc/image2video/video-synthesis`（见 [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)）。混用可能导致 404 错误。

## 关键参数

- **必选请求头**：
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`
  - `X-DashScope-Async: enable`（所有 HTTP 视频 API 均强制要求，缺失将报错 `"current user api does not support synchronous calls"`）
- **必选请求体字段**：
  - `model`: 字符串，指定模型名称（如 `wan2.7-text2video`、`pixverse/pixverse-v6-t2v`、`liveportrait`），不同模型系列命名规则差异显著；
  - `input`: 对象，结构依模型而异（如文生视频含 `prompt`；图生视频含 `img_url`；数字人含 `image_url` 和 `audio_url`；视频风格重绘含 `video_url`）。
- **地域与 WorkspaceId**：Endpoint URL 必须包含业务空间 ID（`{WorkspaceId}`），例如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`。旧域名 `dashscope.aliyuncs.com` 仍可用，但官方强烈建议迁移至专属域名以获得更高稳定性与性能 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。

## 使用方式

1. **前置准备**：在百炼控制台开通对应模型服务，获取并配置该地域的 API Key，确认模型、URL、Key 三者地域一致；
2. **创建任务**：向对应地域的 `POST /api/v1/services/aigc/.../video-synthesis`（或 `/image2video/video-synthesis`）发送请求，携带 `model`、`input` 及必要 headers，成功返回 `task_id`；
3. **轮询结果**：使用 `task_id` 调用任务查询接口（具体路径依模型文档而定），直至状态为 `SUCCESS` 并返回视频 URL；
4. **特殊流程**：数字人（s2v）、EMO、LivePortrait 等模型需额外调用图像检测接口（如 `face-detect`）预检输入，且检测结果中的 `face_bbox`/`ext_bbox` 须作为后续生成请求的入参。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡等地域拥有独立 API Key 与 Endpoint，不可混用；跨地域调用必然失败；
- **异步时效性**：任务创建后立即返回 `task_id`，但处理耗时通常为 1–5 分钟（部分模型如 `wanx2.1-vace-plus` 达 5–10 分钟），`task_id` 仅在 24 小时内有效；
- **输入合规性**：多数人像驱动模型（EMO、LivePortrait、AnimateAnyone、Emoji）强制要求先调用专用检测 API（如 `emo-detect-v1`），未检测或检测失败的图片不可直接用于生成；
- **文件限制**：图像需公网可访问 URL，支持 JPG/PNG/WEBP 等格式，分辨率通常要求 ≥400px 且 ≤7000px；视频文件大小多限制在 100–300MB，时长 ≤30–120 秒；
- **模型演进提示**：万相2.7 已取代早期 2.1–2.6 版本成为主力，旧版文档明确标注“推荐优先选用”新版 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)；爱诗（PixVerse）各子模型（t2v/it2v/kf2v/r2v）均需按场景选择 `c1`（高动态）或 `v6`（通用）版本。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
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
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)


