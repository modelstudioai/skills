# video generation api

百炼平台的 Video Generation API 提供多模态视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、对口型、动作模仿、超分等多种任务。所有接口均采用统一[异步调用](../concepts/asynchronous-invocation.md)范式（创建任务 → 轮询结果），适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同精度、时长与场景需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)及[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。
- **万相（WanX）**：全能型视频模型，3.0版本为 All-in-One 架构，统一支持文生、图生（首帧/首尾帧）、参考生及编辑；2.7版本为模块化演进，各子能力独立迭代；早期2.1–2.6版本仍可使用但已标记为[legacy](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **爱诗（PixVerse）**：强调动态表现力与特效能力，支持文生、图生（首帧/首尾帧）、参考生、[视频对口型](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)、[动作模仿](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)及[视频超清](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)。
- **可灵（Kling）与 Vidu**：面向高保真与专业创作，Kling v4 支持关键帧（首/中/尾）任意组合与官方主体库调用；Vidu 提供广告级（`ad`）、剧集级（`drama`）等细分参考生视频模型。

> **注意**：万相2.7与万相3.0虽共用同一基础URL路径，但协议与参数结构存在差异——万相2.7要求 `X-DashScope-Async: enable` 且部分字段命名不同（如 `input.prompt` vs `parameters.prompt`），而万相3.0文档未明确要求该Header，实际调用需严格按对应版本文档配置，否则返回 `400 Bad Request`。

## 关键参数

所有视频API均需以下通用请求头：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，除部分仅北京地域模型外均强制要求）
- `X-DashScope-Async: enable`（必选，**几乎所有新版模型均强制要求**；缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：

- `model`: 字符串，模型标识符（如 `wan3/video-generation`, `pixverse/pixverse-v6-max-t2v`, `vidu/viduq3-pro_text2video`）。必须与所选模型能力匹配。
- `input`: 对象，承载业务输入：
  - 文生视频：`prompt`（文本提示词，长度限制因模型而异，常见5000–7000字符）
  - 图生视频：`img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）
  - 参考生视频：`image_url` 数组或 `media` 数组（含 `image_url`/`video_url` 类型元素）
  - 视频编辑/对口型：`video_url` + `prompt` 或 `audio_url`
- `parameters`: 对象（可选），控制输出规格：
  - 分辨率：`resolution`（如 `"720P"`, `"1080P"`, `"4k"`）或 `std`/`pro`
  - 宽高比：`aspect_ratio`（如 `"16:9"`, `"9:16"`）
  - 帧率：`video_fps`（如 `15`, `30`）
  - 风格/模式：`style`（整数索引）、`template`（特效模板名）

## 使用方式

1. **准备环境**：确保模型、Endpoint URL 与 API Key **同地域**（如北京地域模型必须配北京API Key与北京Endpoint）；推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧版 `dashscope.aliyuncs.com`。
2. **创建任务**：发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求，携带上述参数。成功响应含 `task_id`（有效期24小时）。
3. **轮询结果**：使用 `GET /api/v1/tasks/{task_id}` 查询状态（`status` 字段为 `SUCCESS` 时返回 `output.video_url`）；建议间隔 ≥5秒轮询，避免触发限流。
4. **错误处理**：关注HTTP状态码（4xx/5xx）及响应体 `code` 字段（如 `InvalidParameter`, `ResourceNotReady`）；任务失败时 `output` 中通常含具体原因。

## 限制和注意事项

- **地域强绑定**：跨地域调用（如用新加坡API Key调用北京Endpoint）必然失败，且部分模型（如数字人 `wan2.2-s2v`、VideoRetalk）**仅限华北2（北京）地域可用**，文档中明确标注“仅适用于北京地域”。
- **异步强制性**：所有视频任务均为异步，同步调用不被支持；`X-DashScope-Async: enable` 是硬性要求，非可选。
- **输入资源约束**：
  - 图片/视频URL须为公网可访问的HTTP(S)链接；本地文件需先调用[临时URL上传接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
  - 若使用OSS临时URL（`oss://`前缀），必须添加请求头 `X-DashScope-OssResourceResolve: enable`，否则报错 `No connection adapters were found for 'oss://'`。
- **模型兼容性**：万相2.6及更早模型（如 `wanx2.1-i2v-turbo`）使用旧版协议，其Endpoint路径在部分文档中为 `/api/v1/services/aigc/image2video/video-synthesis`（见[万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)），与主流 `/video-generation/` 路径不一致，调用前务必核对文档。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)


