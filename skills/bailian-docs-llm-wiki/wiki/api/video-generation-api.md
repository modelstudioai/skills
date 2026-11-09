# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘等核心能力。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。开发者需严格保证模型、Endpoint URL 与 API Key 的地域一致性。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景与精度需求：

- **HappyHorse**：专注物理真实感与运动流畅性，提供[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑四类能力。
- **万相（WanX）**：功能最全的多模态视频模型家族，包含：
  - 全能型 `wan3.0`（All-in-One），统一支持文生、图生（首帧/首尾帧）、参考生视频；
  - 专业子模型：`wan2.7-videoedit`（视频编辑）、`wan2.2-animate-move`（图生动作）、`wan2.2-animate-mix`（视频换人）、`wan2.2-s2v`（数字人驱动）；
  - 特效增强能力：支持通过 `template` 参数调用预设视频特效（如 `flying`、`hanfu-1`），详见[万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。
- **爱诗（PixVerse）**：强调动态表现力与创意控制，支持文生、图生（首帧/首尾帧）、参考生视频、视频对口型（`pixverse-lipsync`）、视频动作模仿（`pixverse-motioncontrol`）、视频超清（`pixverse-upscale`）等细分能力。
- **Vidu / 可灵（Kling） / MiniMax**：分别提供高保真文生视频（Vidu）、全能 Omni 模型（Kling v3-omni）、以及多模态参考生视频（MiniMax-H3）等差异化能力。

> **注意**：万相早期模型（2.1–2.6）与新版（2.7+）协议不兼容。例如，[万相-图生视频-基于首帧（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md) 仅支持首帧输入且无 `X-DashScope-Async` 头要求；而 [万相2.7-图生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 强制要求该头且支持首尾帧/续写。请务必按模型版本选用对应文档。

## 关键参数

所有视频生成 API 均需在请求头（Headers）中设置以下必选字段：

- `Content-Type: application/json`
- `Authorization: Bearer <your_api_key>`
- `X-DashScope-Async: enable`（**除部分 Legacy 模型外，绝大多数新模型强制要求**）

请求体（Request Body）核心字段：

| 字段 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wan3.0`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`。具体值见各模型文档。 |
| `input` | object | 是 | 输入数据容器，结构因模型而异：<br>- 文生：含 `prompt`（文本提示词）；<br>- 图生：含 `img_url` 或 `first_frame`/`last_frame`；<br>- 参考生：含 `image_url` 数组或 `video_url`；<br>- 动作/口型：含 `image_url` + `video_url` 或 `audio_url`。 |
| `parameters` | object | 否 | 可选配置项，常见参数：<br>- `resolution`: `"480P"`/`"720P"`/`"1080P"`/`"4k"`；<br>- `style`: 风格类型（如 `video-style-transform` 的 `style: 0` 表示日式漫画）；<br>- `template`: 视频特效模板名（仅万相 Legacy 图生视频支持）。 |

## 使用方式

所有视频生成任务均采用**标准异步两步流程**：

1. **创建任务**：发送 `POST` 请求至对应地域的 Endpoint，获取 `task_id`。
   - Endpoint 格式统一为：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
     - `{WorkspaceId}`：业务空间 ID（控制台查看）；
     - `{region}`：如 `cn-beijing`、`ap-southeast-1` 等；
     - **注意**：部分模型（如 `wan2.2-s2v`、`videoretalk`）使用旧路径 `/api/v1/services/aigc/image2video/...`，详见对应文档。
2. **轮询结果**：使用返回的 `task_id`，向 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 发起轮询（建议间隔 ≥5s），直至响应中 `status` 为 `"SUCCESS"`，`output.video_url` 即为生成视频地址。

> **注意**：`task_id` 有效期为 **24 小时**，超时后无法查询。请勿重复提交相同任务，否则将产生冗余计费。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL **必须同属一个地域**（如华北2北京），跨地域调用必然失败。业务空间专属域名（如 `xxx.cn-beijing.maas.aliyuncs.com`）是推荐且稳定的接入方式。
- **输入文件要求**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率 400×400 至 7000×7000 像素；
  - 视频：支持 MP4/AVI/MOV 等，时长通常 ≤30 秒，大小 ≤300MB；
  - 音频：支持 WAV/MP3/AAC，时长 2–120 秒，需人声清晰、无背景噪音。
- **计费与限流**：
  - 所有任务成功提交即计费（即使检测不通过，如 `wan2.2-s2v-detect`）；
  - 部分模型（如 `videoretalk`）有严格的 RPS 与并发任务数限制（如 1 RPS，1 个运行中任务）。
- **安全与合规**：输入内容需符合中国法律法规，禁止生成违法、色情、暴力、侵权内容。数字人模型（如 `wan2.2-s2v`）需先通过图像检测接口验证人脸合规性。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)


