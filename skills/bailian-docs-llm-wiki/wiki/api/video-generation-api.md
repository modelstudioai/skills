# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、数字人驱动等核心能力。所有视频生成任务均采用异步调用模式，需通过“创建任务 → 轮询查询”两步完成，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型按厂商分为四类，能力覆盖全面：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四大基础能力，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：支持全场景视频生成，包括万相3.0（All-in-One统一模型，支持文/图/参考生视频，最长30秒）、万相2.7（新版协议，含图生视频、参考生视频、视频编辑）、以及早期2.1–2.6系列（如首尾帧生视频、视频特效、图生动作、视频换人等）[万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)。
- **爱诗（PixVerse）**：聚焦高动态表现，提供文生视频、首帧/首尾帧生视频、参考生视频、视频对口型、动作模仿、视频超清等细分能力，v6-max 和 c1 系列模型针对打斗、法术等高速场景优化 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **可灵（Kling）、Vidu、MiniMax**：均支持文生视频与[多模态](../concepts/multi-modal.md)图生视频；其中可灵 v4 支持关键帧（首/中/尾）任意组合及官方主体库调用；Vidu 提供广告（ad）、剧集（drama）、通用（mix）等垂直场景模型；MiniMax H3 支持首帧/尾帧/首尾帧及[多模态](../concepts/multi-modal.md)参考生视频。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相2.6及早期模型（如 `wanx2.1-i2v-turbo`）使用不同协议，且部分旧版接口路径不一致（例如文档16中首尾帧模型使用 `/api/v1/services/aigc/image2video/video-synthesis`，而新版统一为 `/api/v1/services/aigc/video-generation/video-synthesis`），混用将导致调用失败。

## 关键参数

所有视频生成 API 均需在请求头（Headers）中设置以下必选字段：
- `Content-Type: application/json`
- `Authorization: Bearer <API_KEY>`（API Key 需与模型所在地域匹配）
- `X-DashScope-Async: enable`（**必须显式设置**，否则报错 `"current user api does not support synchronous calls"`）

请求体（Body）中必填字段为：
- `model`: 模型名称（如 `pixverse/pixverse-v6-max-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v4-omni-reference-video-generation`），具体取值需查阅各模型文档。
- `input`: 根据任务类型提供对应输入：
  - 文生视频：`prompt`（文本提示词，长度限制因模型而异，如 Vidu ≤5000 字符，MiniMax ≤7000 字符）
  - 图生视频：`img_url`（首帧）或 `first_frame_url` + `last_frame_url`（首尾帧）
  - 参考生视频：`reference_images` 数组或 `reference_video_url`
  - 视频编辑/动作模仿：`media` 数组，明确指定 `type`（`video_url`/`image_url`/`audio_url`）和 `url`

可选参数 `parameters` 常见字段包括：
- `resolution`: 如 `"720P"`、`"1080P"`、`"4k"`（部分模型如 Kling v4 不支持 4k）
- `style`: 风格重绘类模型专用（如 `video-style-transform` 的 `style: 0` 表示日式漫画）
- `video_fps`: 输出帧率（如 15–25 fps）

## 使用方式

1. **开通服务并配置环境**：在百炼控制台开通对应模型，获取该地域的 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求 URL**：使用业务空间专属域名格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`，其中 `{WorkspaceId}` 为控制台「业务空间详情」中查看的 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1`。
3. **发起[异步任务](../concepts/asynchronous-task.md)**：发送 `POST` 请求，携带上述 Headers 和 Body，成功后获得 `task_id`（有效期 24 小时）。
4. **轮询获取结果**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：数字人模型（如 `wan2.2-s2v`）需额外调用图像检测接口（`/api/v1/services/aigc/image2video/face-detect`）预检输入图片合规性，否则可能生成失败 [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败，且部分模型（如 `wan2.2-s2v`、`videoretalk`）仅限华北2（北京）地域可用。
- **异步强制要求**：所有视频 API 均不支持同步调用，`X-DashScope-Async: enable` 为硬性要求，缺失即报错。
- **输入资源要求**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率通常要求 400–7000 像素；
  - 视频：常见格式 MP4/AVI/MOV，时长 ≤30 秒，大小 ≤100 MB（Vidu 首尾帧要求 2–120 秒）；
  - 音频：WAV/MP3/AAC，时长 2–120 秒，需人声清晰、无背景噪音。
- **URL 访问性**：所有 `xxx_url` 字段（如 `img_url`, `video_url`）必须为公网可访问的 HTTP/HTTPS 链接；若使用临时 OSS URL（`oss://...`），需额外添加请求头 `X-DashScope-OssResourceResolve: enable`。
- **任务管理**：`task_id` 24 小时后失效，不可重复创建相同任务，应轮询而非重发请求。
- **模型演进提示**：万相2.7系列已取代2.6及早期模型成为推荐版本；爱诗、Vidu、可灵均持续迭代，新模型（如 PixVerse v6、Vidu Q3、Kling v4）在画质、时长、帧率上均有提升，旧模型（如 WanX 2.1）功能受限且可能下线。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


