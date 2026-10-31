# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型替换、风格重绘、超分等核心场景。所有模型均采用统一异步调用范式，通过任务 ID 轮询获取结果，适用于生产环境集成。

## 支持的模型/功能

当前平台提供多系列视频生成模型，按能力演进和定位可分为三类：

- **全能型统一模型**：`wan3.0`（万相3.0）支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长输出30秒、30fps；`kling/kling-v3-omni-video-generation`（可灵）同样覆盖全部五种模式（文生、首帧、首尾帧、参考生、视频编辑），支持4K输出；`pixverse`（爱诗）和 `vidu`（Vidu）也提供全栈能力，但各子模型有明确分工（如 `pixverse/pixverse-lipsync` 专用于对口型，`pixverse/pixverse-upscale` 专用于超分）[原文标题](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

- **垂直场景专用模型**：包括 `video-style-transform`（视频风格重绘，支持8种预设艺术风格）[原文标题](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)、`videoretalk`（声动人像，仅支持口型替换）、`wan2.2-s2v`（数字人，需先调用 `wan2.2-s2v-detect` 检测图片合规性）[原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)、`pixverse/pixverse-motioncontrol`（动作模仿）等。

- **历史兼容模型**：`wan2.1`–`wan2.6` 系列（如 `wanx2.1-i2v-turbo`）及部分 `legacy-video-models` 仍可用，但官方明确推荐优先选用 `wan2.7` 及以上新版协议模型 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

> **注意**：`wan2.2-s2v`（数字人）与 `videoretalk` 均限定仅支持华北2（北京）地域，且必须使用该地域专属 API Key；而 `wan3.0`、`kling`、`pixverse` 等主流模型已支持北京、新加坡、东京、法兰克福、弗吉尼亚、中国香港等多地域，调用前须严格保证模型、Endpoint URL 和 API Key 地域一致。

## 关键参数

所有视频生成 API 均遵循统一请求结构，关键参数如下：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API_KEY>`，值来自对应地域的密钥
  - `X-DashScope-Async`: **必填且固定为 `enable`**；缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”

- **请求体（Request Body）**
  - `model`: 字符串，指定具体模型名（如 `wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`）
  - `input`: 对象，内容依模型而异：
    - 文生视频：`prompt`（文本提示词，长度上限因模型而异，如 Vidu 为5000字符，MiniMax 为7000字符）
    - 图生视频：`img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）
    - 参考生视频：`media` 数组，含 `image_url` 或 `video_url` 类型元素
    - 视频编辑/口型替换：`media` 数组，明确指定 `video_url`、`audio_url` 等类型
  - `parameters`: 可选对象，用于控制输出规格：
    - 分辨率：`resolution`（如 `"720P"`）、`style`（风格重绘编号 0–7）、`video_fps`（帧率 15–25）
    - 宽高比：`aspect_ratio`（如 `"16:9"`，部分模型如 Kling 显式支持）
    - 特效模板：`template`（仅限万相早期图生视频的特效模式，见 [原文标题](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)）

## 使用方式

API 采用标准异步两步流程：

1. **创建任务**：发送 `POST` 请求至统一 endpoint  
   `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   （`{WorkspaceId}` 为业务空间 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1`）  
   成功响应返回 JSON，含 `task_id`（有效期 24 小时）。

2. **轮询结果**：使用 `task_id` 向任务查询接口发起 `GET` 请求  
   `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   响应中 `status` 为 `SUCCESS` 时，`output.video_url` 即为生成视频直链。

> **注意**：部分模型（如 `wan2.2-s2v`）在提交生成任务前，**必须先调用独立的图像检测接口** `.../api/v1/services/aigc/image2video/face-detect` 验证输入图片合规性，否则生成任务将失败 [原文标题](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如北京、新加坡等），跨地域调用必然失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已成推荐标准，旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。
- **任务生命周期**：`task_id` 有效期严格为 24 小时，超期后无法查询；禁止重复提交相同任务，应复用已有 `task_id` 轮询。
- **输入文件要求**：所有媒体资源（图片、视频、音频）必须为公网可访问的 HTTP/HTTPS URL；本地文件需先调用 `get-temporary-file-url` 接口上传获取临时链接，且若使用 `oss://` 链接，请求头必须添加 `X-DashScope-OssResourceResolve: enable`。
- **计费与配额**：多数模型按秒/张/次计费（如 `wan2.2-s2v` 480P 0.5元/秒，`wan2.2-s2v-detect` 0.004元/张），免费额度优先抵扣；部分模型（如 `videoretalk`）有严格的并发限制（同时处理中任务数 ≤1）。
- **模型协议差异**：`wan2.7+`、`kling`、`pixverse`、`vidu` 等新模型统一使用 `/video-synthesis` endpoint；而 `wan2.2-animate-move`、`wan2.2-animate-mix` 等部分老模型仍使用 `/image2video/video-synthesis`，调用时需核对文档路径。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
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
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)


