# video generation api

百炼平台的 Video Generation API 提供多种视频生成能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑及风格化等场景。所有模型均采用[异步调用](../concepts/asynchronous-invocation.md)模式，通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前平台提供三大主力视频模型系列，覆盖不同精度、时长与输入模态需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类能力。
- **万相（WanX）**：功能最全的[多模态](../concepts/multimodal.md)视频模型家族，包含万相3.0（All-in-One）、万相2.7（新版协议）及早期2.1–2.6版本；支持文生视频、图生视频（首帧/首尾帧/续写）、参考生视频、视频编辑、图生动作、视频换人、数字人（s2v）、视频特效等。注意：[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)明确推荐优先选用 wan2.7 模型，其统一支持三大图生任务，而旧版仅支持首帧生视频。
- **Vidu / Kling / PixVerse / MiniMax**：均为独立品牌模型，各具特色：
  - Vidu 支持文生、首帧/首尾帧/参考生视频；
  - Kling 支持文生、首帧、首尾帧、参考生及视频编辑（omni 版本）；
  - PixVerse（爱诗）提供图生、参考生、动作模仿、对口型、超清等细分能力；
  - MiniMax 支持文生、首帧/尾帧/首尾帧及[多模态](../concepts/multimodal.md)参考生视频。

> **注意**：万相早期模型（2.1–2.6）与新版（2.7+）使用不同协议，且部分旧版接口路径为 `/api/v1/services/aigc/image2video/...`（如[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)），而新版统一使用 `/api/v1/services/aigc/video-generation/...`。混用可能导致 404 或协议不兼容错误。

## 关键参数

所有视频生成 API 均需以下通用请求头：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，除部分纯前端或特殊模型外）
- `X-DashScope-Async: enable`（**HTTP 请求必选**；缺少将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：

- `model`（string，必选）：具体模型标识符，如 `wan2.7-text2video`、`vidu/viduq3-pro_text2video`、`pixverse/pixverse-v6-t2v` 等，不同模型取值差异大，需严格按文档选择。
- `input`（object，必选）：包含任务所需输入：
  - 文生视频：`prompt`（文本提示词，长度限制因模型而异，如 Vidu 限 5000 字符，MiniMax 限 7000 字符）
  - 图生/参考生/编辑类：`media` 数组，每个元素含 `type`（如 `image_url`, `video_url`, `audio_url`）和 `url`；或直接使用 `img_url`/`image_url`/`video_url` 等扁平字段（依模型而定）
- `parameters`（object，可选）：控制输出规格，常见参数包括：
  - `resolution`（如 `"720P"`, `"1080P"`, `"4k"`）
  - `style`（视频风格重绘等场景，如 `0` 表示日式漫画）
  - `video_fps`（帧率，默认常为 15 或 30）
  - `animate_emotion`（是否优化表情）

## 使用方式

1. **开通服务与配置环境**：在百炼控制台开通对应模型，确认地域，获取该地域专属 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求 URL**：使用业务空间专属域名格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`，其中 `{WorkspaceId}` 和 `{region}`（如 `cn-beijing`）需从控制台业务空间详情页获取。
3. **发起异步任务**：`POST` 请求提交任务，获取 `task_id`。
4. **轮询结果**：使用 `task_id` 调用任务查询接口（路径通常为 `/api/v1/tasks/{task_id}`），直至返回 `status: "SUCCESS"` 及 `output.video_url`。
5. **错误处理**：关注 `task_id` 有效期（24 小时）、地域一致性、`X-DashScope-Async` 头缺失、`prompt` 超长、媒体 URL 不可达等高频错误。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)和所有万相、Vidu 等文档均反复强调此前提。
- **异步强制要求**：所有视频生成任务必须使用 `X-DashScope-Async: enable`，同步调用不被支持。
- **输入资源要求**：图像/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用临时 URL 接口上传（如 `get-temporary-file-url.md`）；部分模型（如 VideoRetalk）对 OSS URL 需额外添加 `X-DashScope-OssResourceResolve: enable` 头。
- **模型时效性**：万相2.7+、HappyHorse、Vidu、Kling 等新模型已取代旧版（如万相2.6及更早），旧版文档明确标注“推荐优先选用新版”，旧接口可能逐步下线。
- **数字人与口型替换类模型特殊性**：如 `wan2.2-s2v`、`videoretalk`、`pixverse-lipsync` 等，需先进行图像/视频合规检测（如 `wan2.2-s2v-detect`），且仅支持华北2（北京）地域，不适用业务空间专属域名迁移规则。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)


