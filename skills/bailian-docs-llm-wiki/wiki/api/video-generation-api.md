# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、对口型、风格重绘等核心能力。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。开发者需严格保证模型、Endpoint URL 与 API Key 的地域一致性。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景与性能需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[HappyHorse-图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[HappyHorse-参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)及[HappyHorse-视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。
- **万相（WanX）**：功能最全的多模态视频模型家族，涵盖万相3.0（All-in-One）、万相2.7（新版协议）、早期2.1–2.6系列，支持图生视频（首帧/首尾帧/续写）、文生视频、参考生视频、视频编辑、图生动作、视频换人、数字人（s2v）等。其中[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)明确推荐为首选新版协议。
- **爱诗（PixVerse）**：强调动态表现力与特效能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、视频动作模仿、视频超清等细分能力。
- **Vidu / 可灵（Kling） / MiniMax**：分别提供高保真文生视频、全能型多任务（如可灵kling-v3-omni-video-generation支持全部5类输入）、以及多模态参考生视频能力。

> **注意**：万相2.1–2.6系列（如[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)）与2.7+系列使用不同协议，且部分旧版接口路径存在差异（例如文档15中`/api/v1/services/aigc/image2video/video-synthesis`），新项目应优先选用2.7及以上版本。

## 关键参数

所有视频生成 API 均需以下通用请求头：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，除少数纯前端检测接口外）
- `X-DashScope-Async: enable`（**HTTP调用必选**；缺少将报错“current user api does not [support](../guides/support.md) synchronous calls”）

请求体（JSON）中必含字段：
- `model`: 字符串，指定具体模型标识符（如 `wan2.7-i2v`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`）。
- `input`: 对象，结构因模型而异：
  - 文生视频：通常含 `prompt`（文本提示词，长度限制依模型而定，常见5000字符）；
  - 图生视频：含 `img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）；
  - 参考生视频：含 `media` 数组，支持混合传入 `image_url`/`video_url`；
  - 数字人（s2v）：含 `image_url` 和 `audio_url`；
  - 视频风格重绘：含 `video_url` 和 `style` 参数。

## 使用方式

所有视频生成任务均采用**标准异步两步流程**：

1. **创建任务**：向 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` 发送请求（各模型文档均指向此统一路径），获取 `task_id`。
2. **轮询结果**：使用 `task_id` 向 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至返回 `"status": "SUCCESS"` 并附带 `output.video_url`。

> **注意**：`{WorkspaceId}` 为业务空间ID，需在控制台获取；`{region}` 如 `cn-beijing`、`ap-southeast-1` 等，必须与模型、API Key 地域严格一致。文档中多次强调跨地域调用必然失败，例如[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)明确指出“为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于同一地域”。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），混用将直接鉴权失败或服务报错。
- **任务时效性**：`task_id` 有效期统一为 **24 小时**，超时后无法查询结果。
- **资源要求**：
  - 输入图像：分辨率通常要求宽高在 [400, 7000] 像素间（如 wan2.2-s2v）；
  - 输入视频：时长多限制在 2–120 秒，大小 ≤300MB（如 VideoRetalk）；
  - 输入音频：时长 <20s，格式为 wav/mp3（如 wan2.2-s2v）。
- **URL 访问性**：所有 `xxx_url` 字段（图片、视频、音频）必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)接口。
- **计费与限流**：部分模型（如 VideoRetalk）有明确 RPS 限制（1 QPS）和并发任务数限制（1），详见各模型资费说明。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)


