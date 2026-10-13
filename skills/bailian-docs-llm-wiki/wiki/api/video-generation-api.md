# video generation api

百炼平台的 Video Generation API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，由 HappyHorse、万相（WanX）、爱诗（PixVerse）、Vidu、可灵（Kling）、MiniMax 等多个模型系列支撑。所有接口均采用统一异步调用范式（创建任务 → 轮询获取），支持多地域部署与业务空间专属域名，适用于生产级视频生成场景。

## 支持的模型/功能

当前平台提供以下主流视频生成模型及对应能力：

- **HappyHorse**：支持文生视频、图生视频（首帧）、参考生视频、视频编辑四类任务，强调物理真实性和运动流畅性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **万相（WanX）**：覆盖全栈能力，包括万相3.0（All-in-One，统一支持文生/图生/参考生）、万相2.7（新版协议，支持首帧/首尾帧/视频续写）、以及数字人（s2v）、图生动作（animate-move）、视频换人（animate-mix）等垂直能力；早期2.1–2.6版本已归档为[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **爱诗（PixVerse）**：提供文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型（lipsync）、动作模仿（motioncontrol）、视频超清（upscale）等精细化能力。
- **Vidu**：专注高质量长时序一致性，支持文生视频、首帧/首尾帧图生视频、参考生视频（含广告/剧集/通用等细分模型）。
- **可灵（Kling）**：支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑，并提供预置主体ID（如“雷电”“魔法法阵”）用于可控元素生成 [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)。
- **MiniMax**：支持文生视频、多模态图生视频（首帧/尾帧/首尾帧）及参考生视频。
- **人像驱动类**：包括声动人像 VideoRetalk（口型替换）、视频风格重绘、数字人图像检测（wan2.2-s2v-detect）等辅助能力，详见[人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相早期模型（如 `wanx2.1-vace-plus`）使用相同 endpoint 但协议不兼容；旧版模型（2.1–2.6）的请求路径部分仍沿用 `/aigc/image2video/`（如文档15、17、18），而新版统一为 `/aigc/video-generation/` —— 开发者需严格按模型文档指定的 `model` 参数值匹配对应协议，否则将返回鉴权或参数错误。

## 关键参数

所有视频生成 API 均需以下**必选请求头**：
- `Content-Type: application/json`
- `Authorization: Bearer <API_KEY>`（除部分纯检测接口如 `wan2.2-s2v-detect` 外均需）
- `X-DashScope-Async: enable`（HTTP 异步调用强制要求；缺失将报错 `"current user api does not support synchronous calls"`）

**核心请求体字段**：
- `model`（`string`，必选）：精确指定模型标识符，例如：
  - `wan2.7-videoedit`（万相2.7视频编辑）
  - `pixverse/pixverse-v6-t2v`（爱诗文生视频）
  - `vidu/viduq3-pro_text2video`（Vidu文生视频）
  - `kling/kling-v3-omni-video-generation`（可灵全能版）
- `input`（`object`，必选）：根据任务类型结构化输入：
  - 文生视频：`{"prompt": "描述文本"}`
  - 图生视频（首帧）：`{"img_url": "https://...", "prompt": "..."}`  
  - 首尾帧：`{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`（Vidu/爱诗）
  - 参考生视频：`{"reference_urls": ["..."], "prompt": "..."}`（万相3.0、爱诗、可灵）
  - 数字人：`{"image_url": "...", "audio_url": "..."}`（wan2.2-s2v）
- `parameters`（`object`，可选）：控制输出规格，常见字段包括：
  - `resolution`（如 `"720P"`、`"1080P"`、`"4k"`）
  - `aspect_ratio`（如 `"16:9"`、`"9:16"`）
  - `style`（视频风格重绘中为整数索引；数字人中为 `"speech"`/`"singing"`）
  - `template`（仅万相早期特效模式支持，如 `"flying"`）[万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)

## 使用方式

1. **环境准备**：确保模型、Endpoint URL 与 API Key 属于同一地域；推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧版 `dashscope.aliyuncs.com`，以获得更高稳定性与性能。
2. **创建任务**：向对应地域的 endpoint 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求，携带上述关键参数。成功后返回 `task_id`（有效期 24 小时）。
3. **轮询结果**：使用 `task_id` 调用任务查询接口（各模型文档中均有说明，通常为 `GET /api/v1/tasks/{task_id}`），直至 `status` 变为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频直链。
4. **SDK 调用**：推荐安装 DashScope SDK 并配置环境变量 `DASHSCOPE_API_KEY`，可简化认证与轮询逻辑（见[Postman新手指引](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)）。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint 必须同地域（如北京地域模型不可用新加坡 API Key 调用），跨地域将直接失败。
- **异步强制性**：所有视频生成接口仅支持异步，同步调用必然报错；`X-DashScope-Async: enable` 为硬性要求。
- **输入合规性**：
  - 图片：格式（JPG/PNG/WebP/BMP）、分辨率（通常 400–7000px）、公网可访问 URL；本地文件需先调用[临时URL上传接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)。
  - 视频：格式（MP4/AVI/MOV等）、时长（通常 2–120 秒）、大小（≤300MB）、帧率（15–60fps）；数字人音频需人声清晰、无背景噪音。
- **模型时效性**：万相2.7+、爱诗、Vidu、可灵等新模型已全面替代旧版（2.1–2.6），旧模型虽仍可用但不再更新，[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md) 文档仅作兼容参考。
- **计费差异**：部分模型（如 `wan2.2-s2v-detect`、`videoretalk`）为同步接口且单独计费；数字人流程需先调用检测接口再生成，两步均计费。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)


