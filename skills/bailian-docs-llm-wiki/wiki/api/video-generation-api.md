# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘、超分增强等核心能力。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。开发者需严格保证模型、Endpoint URL 与 API Key 的地域一致性。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑四类任务。
- **万相（WanX）**：功能最全的多模态视频模型家族，包含：
  - 万相2.7：统一新版协议，支持图生视频（首帧/首尾帧/续写）、文生视频、参考生视频、视频编辑；
  - 万相3.0：All-in-One 全能模型，单接口支持文生、图生（首帧/首尾帧）、参考生、视频编辑五种模式；
  - 早期版本（2.1–2.6）：已归档为[legacy-video-models](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)，仅建议存量系统维护使用。
- **爱诗（PixVerse）**：强动态表现力，支持文生、图生（首帧/首尾帧）、参考生、视频对口型、动作模仿、视频超清六类任务，各子模型按场景优化（如 `c1` 专精高速运动）。
- **Vidu / 可灵（Kling） / MiniMax / 数字人（S2V） / 视频口型替换（VideoRetalk） / 视频风格重绘**：面向垂直场景的专用模型，例如 Vidu 强调广告与剧集生成，可灵支持主体 ID 复用，数字人 wan2.2-s2v 专用于音视频驱动肖像动画。

> **注意**：万相2.7 图生视频 API（[image-to-video-general-api-reference.md](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)）明确声明其为“全新推出的图生视频 API”，并推荐优先选用；而旧版图生视频（如 [legacy-image-to-video-api-reference.md](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)）仅支持首帧生视频，功能受限。

## 关键参数

所有视频生成 API 均需以下通用请求头（Headers）：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，部分模型如数字人 wan2.2-s2v 限定华北2 地域）
- `X-DashScope-Async: enable`（必选，HTTP 调用必须启用异步）

请求体（Request Body）核心字段：

- `model`（必选）：模型标识符，如 `wan2.7-t2v`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v3-omni-video-generation` 等，具体值需查阅对应模型文档。
- `input`（必选）：输入内容对象，结构因模型而异：
  - 文生视频：含 `prompt`（文本提示词，长度限制见各模型，如 Vidu 限 5000 字符，MiniMax 限 7000 字符）；
  - 图生视频：含 `img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）；
  - 参考生视频：含 `reference_images` 或 `media` 数组（支持图片/视频混合）；
  - 数字人：含 `image_url` 和 `audio_url`；
  - 视频编辑/动作模仿：含 `media` 数组，指定 `type`（`video_url`/`image_url`/`audio_url`）。
- `parameters`（可选）：控制输出规格，常见参数包括：
  - `resolution`（如 `"720P"`、`"1080P"`、`"4k"`）；
  - `style`（视频风格重绘中指定 0–7 的整数）；
  - `video_fps`（帧率，默认 15）；
  - `animate_emotion`（是否优化表情）。

## 使用方式

所有视频生成 API 均遵循标准异步流程：

1. **创建任务**：向 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` 发送请求（各地域 Endpoint 见各模型文档），获取 `task_id`。
   - `task_id` 有效期为 **24 小时**，请勿重复提交相同任务。
   - 必须使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐（详见 [happyhorse-text-to-video-api-reference.md](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)）。
2. **轮询结果**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询任务状态，直至返回 `"status": "SUCCESS"` 并附带 `output.video_url`。

> **注意**：部分模型（如数字人 wan2.2-s2v）要求**先调用图像检测接口** `face-detect`（[wan-s2v-detect-api.md](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)）验证输入图片合规性，再提交生成任务，此为强制前置步骤。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL 与 API Key **必须属于同一地域**（如华北2 北京），跨地域调用必然失败。业务空间 ID（`{WorkspaceId}`）需在控制台“业务空间详情”中获取。
- **输入格式约束**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率通常要求 400–7000 像素；
  - 视频：MP4/AVI/MOV 等，时长 ≤30 秒（部分模型如 VideoRetalk 支持 ≤120 秒），大小 ≤300 MB；
  - 音频：WAV/MP3，时长 ≤20 秒（数字人）或 ≤120 秒（VideoRetalk），需纯净人声。
- **计费与限流**：多数模型按视频秒数或任务次数计费（如 VideoRetalk 0.08 元/秒），且存在 RPS（每秒请求数）与并发任务数限制（如 VideoRetalk 同时处理中任务数上限为 1），详情见各模型资费文档。
- **URL 访问要求**：所有媒体资源（图片、视频、音频）必须为公网可访问的 HTTP/HTTPS URL；若使用 OSS 临时 URL，需额外添加请求头 `X-DashScope-OssResourceResolve: enable`（见 [videoretalk-api.md](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)）。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)


