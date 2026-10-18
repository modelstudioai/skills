# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、视频风格重绘、对口型、动作模仿、超分等多种能力。所有视频生成任务均采用[异步调用](../concepts/asynchronous-invocation.md)模式，需通过“创建任务 → 轮询获取结果”两步完成。开发者需严格保证模型、Endpoint URL 与 API Key 的地域一致性。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景与精度需求：

- **HappyHorse**：专注高质量物理真实感视频，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。
- **万相（WanX）**：功能最全的[多模态](../concepts/multi-modal.md)视频模型家族，涵盖[万相3.0-视频生成](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)（All-in-One）、[万相2.7系列](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)（图生/文生/参考生/编辑），以及数字人（s2v）、图生动作（animate-move）、视频换人（animate-mix）等垂直能力。
- **爱诗（PixVerse）**：强调创意表达与动作控制，支持[文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)、[首尾帧生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)、[视频对口型](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)、[动作模仿](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)和[视频超清](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)。
- **Vidu / 可灵（Kling） / MiniMax**：分别提供高保真长时序建模（Vidu）、全能一体化生成（Kling）及[多模态](../concepts/multi-modal.md)强可控性（MiniMax）能力，均支持文生、图生、参考生等核心范式。

> **注意**：万相2.1–2.6系列（如`wanx2.1-i2v-turbo`）为早期模型，其API路径部分使用 `/api/v1/services/aigc/image2video/...`（如[万相-图生视频-基于首尾帧API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)），而2.7+及所有新模型统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。混用路径将导致404错误。

## 关键参数

所有视频生成 API 均需在 HTTP 请求中设置以下通用头信息：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，除部分仅北京地域模型外）
- `X-DashScope-Async: enable`（必选，所有视频类接口强制异步）

请求体（JSON）中必须包含：

- `model`（字符串，必选）：具体模型名称，如 `wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video` 等，各模型支持的取值详见对应文档。
- `input`（对象，必选）：根据任务类型不同，结构差异显著：
  - 文生视频：通常只需 `prompt` 字段（如[Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)）；
  - 图生视频：需 `img_url` 或 `first_frame`/`last_frame` 等图像URL；
  - 参考生视频：需 `media` 数组，含多张图片或视频URL；
  - 视频编辑/对口型/动作模仿：需组合 `video_url` + `image_url` + `audio_url` 等。

此外，`parameters` 对象常用于控制输出规格（如 `resolution`、`style`、`video_fps`），但并非所有模型均支持相同字段。

## 使用方式

1. **开通服务与配置环境**：在阿里云百炼控制台开通对应模型，并[获取该地域的 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，配置至环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求URL**：使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`。`{WorkspaceId}` 和 `{region}` 需替换为实际值（如 `cn-beijing`）。旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐。
3. **发起异步任务**：`POST` 请求提交任务，成功后获得 `task_id`（有效期24小时）。
4. **轮询获取结果**：使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：部分模型（如数字人 `wan2.2-s2v`）需先调用独立的图像检测接口（`/api/v1/services/aigc/image2video/face-detect`）验证输入合规性，再提交生成任务。详情见[数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。
- **异步强制性**：所有视频生成接口不支持同步调用；缺失 `X-DashScope-Async: enable` 头将报错 `"current user api does not support synchronous calls"`。
- **任务ID管理**：`task_id` 24小时内有效，且不可重复提交同一任务，应轮询而非重发创建请求。
- **输入文件要求**：图像/视频/音频必须为公网可访问的 HTTP/HTTPS URL；本地文件需先[上传获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)；部分模型（如 VideoRetalk）对 OSS URL 需额外添加 `X-DashScope-OssResourceResolve: enable` 头。
- **模型兼容性**：万相2.7+、HappyHorse、爱诗、Vidu、可灵、MiniMax 等新模型均统一使用 `/video-synthesis` 路径；而万相2.2等旧模型（如[万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)）仍使用 `/image2video/video-synthesis`，调用前务必核对文档路径。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)


