# video generation api

百炼平台的 Video Generation API 提供多模型、多模态的视频生成能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑及风格化等核心场景。所有接口均采用异步调用模式，通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期统一为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将直接失败。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同能力边界与性能定位：

- **HappyHorse**：专注物理真实感与运动流畅性，提供[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频和视频编辑四类能力，适用于高质量内容创作。
- **万相（WanX）**：功能最全的多模态视频模型家族，包含万相2.7（新版协议）、万相3.0（All-in-One 统一模型）及早期 2.1–2.6 版本；除基础生成外，还支持视频特效、数字人（wan2.2-s2v）、图生动作、视频换人、声动人像（VideoRetalk）等垂直能力。> **注意**：万相2.7 及以后版本使用统一 endpoint `/video-synthesis`，而部分早期模型（如万相2.2-首尾帧）仍使用 `/image2video/video-synthesis`，二者路径不兼容，详见[万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)。
- **爱诗（PixVerse）**：强调动态表现力与可控性，支持文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型、动作模仿及超清增强，特别适合高动态场景（如打斗、法术）。
- **可灵（Kling）与 Vidu**：面向专业级生成需求，可灵 v3 系列支持文生、图生、参考生、视频编辑五合一；Vidu 提供多档性能模型（turbo/pro/4k），并按场景细分为广告、剧集、通用等参考生视频子模型。

此外，MiniMax、视频风格重绘、视频口型替换（VideoRetalk）等专项模型也已接入，构成完整的视频 AI 工具链。

## 关键参数

所有视频生成 API 共享以下强制性请求头与通用参数结构：

- **请求头（Headers）**
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选，仅北京/新加坡等支持业务空间的地域需配对应地域 Key）
  - `X-DashScope-Async: enable`（必选，缺失将报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**
  - `model`（string，必选）：具体模型标识符，如 `wan3-video-generation`、`vidu/viduq3-pro_text2video`、`pixverse/pixverse-v6-t2v` 等，不同模型取值差异大，需严格匹配文档。
  - `input`（object，必选）：承载核心输入数据，结构因模型而异：
    - 文生视频：通常含 `prompt`（文本提示词，长度限制多为 5000–7000 字符）；
    - 图生视频：含 `img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）；
    - 参考生视频：含 `media` 数组，支持混合传入 `image_url`、`video_url`、`audio_url`；
    - 视频编辑/风格化：含 `video_url` 及操作指令（如 `template`、`style`）。
  - `parameters`（object，可选）：控制输出规格，常见字段包括：
    - `resolution`（如 `"720P"`、`"1080P"`、`"4k"`）
    - `aspect_ratio`（如 `"16:9"`、`"9:16"`）
    - `style`（整数索引，用于风格重绘等）
    - `video_fps`（帧率，默认常为 15–30）

> **注意**：万相-视频特效模式（如 flying、hanfu-1）要求 `input` 中**仅传 `img_url` 和 `template`，禁止传 `prompt`**，否则可能被忽略或报错，详见[万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。

## 使用方式

1. **准备环境**  
   - 在百炼控制台开通对应模型服务；
   - 获取目标地域的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；
   - 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧版 `dashscope.aliyuncs.com` 域名。

2. **发起[异步任务](../concepts/asynchronous-task.md)**  
   向统一 endpoint 发起 `POST` 请求（URL 中 `{WorkspaceId}` 需替换为实际业务空间 ID）：
   ```bash
   POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
   ```
   > 所有主流模型（HappyHorse、万相2.7+/3.0、爱诗、可灵、Vidu、MiniMax）均使用此 endpoint；仅少数遗留模型（如万相2.2-s2v、VideoRetalk）仍使用 `/image2video/` 路径。

3. **轮询获取结果**  
   使用响应中的 `task_id`，向 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status` 变为 `SUCCESS`，响应中将返回 `output.video_url`。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），混用将导致鉴权失败或 403 错误。
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后无法查询，返回 `UNKNOWN` 状态。
- **输入资源要求**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率建议 400×400 至 1920×1080，需公网可访问 URL；
  - 视频：MP4/AVI/MOV 等常见格式，时长通常 ≤30 秒，大小 ≤300 MB；
  - 音频：WAV/MP3/AAC，时长 ≤120 秒，需清晰人声、无背景噪音。
- **并发与限流**：各模型有独立 RPS 与并发任务数限制（如 videoretalk 同时仅允许 1 个运行中任务），详情见各模型定价页。
- **计费说明**：图像检测类 API（如 `wan2.2-s2v-detect`）无论检测是否通过均计费；视频生成类 API 按实际生成时长或分辨率计费。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)


