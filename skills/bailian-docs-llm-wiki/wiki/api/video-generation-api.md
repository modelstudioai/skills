# video generation api

百炼平台的视频生成 API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，由 HappyHorse、万相（WanX）、爱诗（PixVerse）、可灵（Kling）、Vidu、MiniMax 等多个模型系列支持。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生成 3–30 秒、分辨率最高达 4K 的高质量视频。开发者需严格保证模型、Endpoint URL 与 API Key 同地域部署。

## 支持的模型/功能

当前平台提供以下主流视频生成模型能力：

- **HappyHorse**：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实性和运动流畅性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **万相（WanX）**：覆盖全场景，包括万相3.0（All-in-One，统一支持文/图/参考生视频）、万相2.7（新版协议，支持多模态输入与视频续写）、早期2.1–2.6系列（含特效模板、首尾帧等专用能力）；另提供数字人（s2v）、图生动作、视频换人等垂直能力 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。
- **爱诗（PixVerse）**：提供文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型、动作模仿、超清增强等细分能力，模型命名体系清晰（如 `pixverse-v6-t2v`、`pixverse-motioncontrol`）[爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)。
- **可灵（Kling）**：支持文生视频、首帧/首尾帧图生视频、参考生视频及视频编辑，提供 `kling-v3-omni-video-generation` 全能模型，并支持预设主体 ID（如“雷电”“魔法法阵”）快速调用 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。
- **Vidu**：专注高质量长时序一致性，提供 `viduq3-pro` 系列（精品剧/广告级）与 `viduq3-turbo`（快速出片）双轨模型，支持广告视频、AI漫剧等专业场景 [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)。
- **MiniMax**：支持文生视频、首帧/尾帧/首尾帧图生视频及多模态参考生视频，输入参数 `media` 类型灵活定义生成模式 [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相早期模型（2.1–2.6）使用不同协议和参数结构，且部分旧版接口（如 `legacy-image-to-video-api-reference.md`）已明确标注“推荐优先选用新版”，迁移时需注意兼容性。

## 关键参数

所有视频生成 API 均需以下核心参数：

- **请求头（Headers）**
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选，除部分仅北京地域模型外均需）
  - `X-DashScope-Async: enable`（必选，所有 HTTP 调用必须显式设置，否则报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**
  - `model`（必选）：模型标识符，如 `wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v3-omni-video-generation`。
  - `input`（必选）：结构化输入对象，内容依模型而异：
    - 文生视频：`prompt`（文本提示词，长度限制因模型而异，如 Vidu ≤5000 字符，MiniMax ≤7000 字符）
    - 图生视频：`img_url`（首帧）或 `first_frame`/`last_frame`（首尾帧）
    - 参考生视频：`media` 数组（支持 `image_url`、`video_url`、`audio_url` 混合）
    - 数字人/对口型：`image_url` + `audio_url` 或 `lip_sync_tts_content`
  - `parameters`（可选）：控制输出规格，常见字段包括：
    - `resolution` / `style` / `video_fps`（如 `720P`, `pro`, `15`）
    - `aspect_ratio`（如 `16:9`, `9:16`）
    - `duration`（部分模型支持指定秒数）

## 使用方式

所有视频生成任务均采用标准两步异步流程：

### 步骤1：创建任务
向对应地域的 Endpoint 发起 `POST` 请求：
```http
POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```
- `{WorkspaceId}`：业务空间 ID（控制台“业务空间详情”页获取）
- `{region}`：地域代码，如 `cn-beijing`、`ap-southeast-1`、`us-east-1` 等（[万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md) 列出全部支持地域）
- 成功响应返回 JSON，含 `task_id`（有效期 24 小时）

### 步骤2：轮询获取结果
使用 `task_id` 向任务查询接口发起 `GET` 请求：
```http
GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}
```
- 响应中 `status` 为 `SUCCESS` 时，`output.video_url` 即为生成视频公网直链
- 建议轮询间隔 ≥5 秒，避免触发限流

> **注意**：数字人 `wan2.2-s2v` 模型需额外前置调用图像检测接口 `POST .../api/v1/services/aigc/image2video/face-detect`，确保输入图片合规 [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)，该步骤在其他视频生成流程中不通用。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。各文档反复强调此要求，是首要排查点。
- **异步强制要求**：所有 HTTP 调用必须携带 `X-DashScope-Async: enable`，同步调用无例外。
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超时后无法查询，响应状态为 `UNKNOWN`。
- **文件与链接规范**：
  - 输入媒体（图片/视频/音频）必须为公网可访问的 HTTP/HTTPS URL；
  - 若使用 OSS 临时 URL（`oss://` 前缀），必须在请求头添加 `X-DashScope-OssResourceResolve: enable`（见 [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)）；
  - 本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口。
- **模型专属限制**：
  - 万相视频特效模式（如 `template: "flying"`）仅支持旧版图生视频模型（2.1–2.6），且 `prompt` 字段会被忽略 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)；
  - 数字人 `wan2.2-s2v` 仅支持华北2（北京）地域，且音频时长 <20 秒、图片分辨率 400–7000 像素 [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)；
  - 可灵主体 ID（`element_id`）仅在 `kling-v3-omni-video-generation` 等特定模型中生效，不可用于其他模型 [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)


