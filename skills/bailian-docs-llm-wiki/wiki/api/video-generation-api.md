# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型替换、风格重绘、超分等场景。所有接口均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前平台提供多系列视频生成模型，按能力演进和定位可分为三类：

- **全能型统一模型**：`wan3.0`（万相3.0）是 All-in-One 架构，统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长生成 30 秒、30fps 视频 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；`kling-v3-omni-video-generation` 同样覆盖全部五种模式（文生、首帧、首尾帧、参考生、编辑），支持 4K 输出 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

- **垂直场景专用模型**：  
  - *数字人驱动*：`wan2.2-s2v`（单图+音频生成说话/唱歌视频）、`videoretalk`（人物视频+音频口型替换）、`pixverse-lipsync`（爱诗对口型）；  
  - *动作迁移*：`wan2.2-animate-move`（图+参考视频复刻动作）、`pixverse-motioncontrol`（爱诗动作模仿）；  
  - *增强处理*：`pixverse-upscale`（4K超分）、`video-style-transform`（8种艺术风格重绘）。

- **历史兼容模型**：`wan2.7` 系列（如 `wan2.7-videoedit`、`wan2.7-text2video`）为过渡版本，推荐优先选用 `wan3.0`；`wan2.1–2.6` 及 `viduq2` 等早期模型仍可用，但功能受限且部分已标记为“不推荐” [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。

> **注意**：`wan2.6` 及更早的参考生视频模型（如 `wan2.6-video-to-video`）使用旧版协议，而 `wan2.7` 及 `wan3.0` 使用新版统一协议；二者请求体结构、参数命名存在差异，不可混用。

## 关键参数

所有视频生成 API 均需以下通用请求头：
- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，仅限同地域 Key）
- `X-DashScope-Async: enable`（必选，异步强制开关；缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：
- `model`（字符串，必选）：精确指定模型标识符，例如 `wan3.0-video-generation`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`。
- `input`（对象，必选）：根据模型类型动态变化：
  - 文生视频：仅需 `prompt`（文本提示词，长度上限依模型而异，如 Vidu 为 5000 字符，MiniMax 为 7000 字符）；
  - 图生视频：需 `image_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）；
  - 参考生视频：需 `reference_images` 数组或 `reference_video_url`；
  - 视频编辑/口型替换：需 `video_url` + `audio_url` 或 `lip_sync_tts_content`。
- `parameters`（对象，可选）：控制输出规格，常见字段包括：
  - `resolution`（如 `"720P"`、`"4k"`）、`aspect_ratio`（`"16:9"`、`"9:16"`）、`duration`（秒数）；
  - 特效类模型（如万相视频特效）需 `template` 字段指定预设效果 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。

## 使用方式

1. **环境准备**：在阿里云百炼控制台开通对应模型服务，获取**同地域**的 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`；确认业务空间 ID（WorkspaceId）。
2. **构造请求**：使用 `POST {WorkspaceId}.<region>.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` 发起任务创建请求（注意：`image2video/video-synthesis` 路径仅用于极少数旧模型如 `wan2.2-s2v` 和 `videoretalk`，绝大多数新模型统一使用 `video-generation/video-synthesis`）。
3. **轮询结果**：从响应中提取 `task_id`，调用 `GET /api/v1/tasks/{task_id}` 查询状态（成功时返回 `output.video_url`）。
4. **错误处理**：关注 HTTP 状态码（4xx/5xx）及响应体中的 `code`/`message` 字段；常见错误包括 `INVALID_PARAMETER`（参数格式错误）、`QUOTA_EXHAUSTED`（额度不足）、`AUTHORIZATION_FAILED`（Key/地域不匹配）。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为强制推荐方案，旧域名（`dashscope.aliyuncs.com`）虽暂支持，但性能与稳定性较低。
- **输入文件要求**：所有媒体 URL 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 `get-temporary-file-url` 接口上传并获取临时 URL；若使用 OSS URL（`oss://`），必须添加请求头 `X-DashScope-OssResourceResolve: enable`。
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询；任务创建后禁止重复提交相同请求，应持续轮询而非重试。
- **模型兼容性风险**：`wan2.6` 及更早模型（如文档45中的 `wan2.5-text2video`）与 `wan2.7+` 在参数结构上不兼容；`viduq2` 系列与 `viduq3` 的 `model` 字符串前缀、`parameters` 字段名均有差异，切换时需严格参照对应文档。
- **计费与限流**：多数模型按视频秒数或任务次数计费（如 `videoretalk` 0.08元/秒），部分含免费额度；RPS（每秒请求数）与并发任务数受账号级别限制（如 `wan2.2-s2v` 同时处理中任务上限为 100 秒）。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)


