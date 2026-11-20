# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、对口型、风格重绘、超分等多种能力。所有接口均采用统一[异步调用](../concepts/asynchronous-invocation.md)范式：先创建任务获取 `task_id`，再轮询查询结果。开发者需确保模型、Endpoint URL 与 API Key 严格同地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型包括：
- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调物理真实与运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)；
- **万相（WanX）**：覆盖全场景，含万相3.0（All-in-One统一模型，支持文/图/参考生视频）、万相2.7系列（新版协议，推荐使用）、早期2.1–2.6模型（已逐步淘汰），以及图生动作、视频换人、数字人等垂直能力 [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)；
- **爱诗（PixVerse）**：专注高质量生成，支持文生视频、首帧/首尾帧/参考生视频、对口型、动作模仿、视频超清等，提供 v6/c1 等多档模型选型 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)；
- **可灵（Kling）**：支持文生视频、关键帧（首/中/尾）生视频、参考生视频及视频编辑，4.0 版本引入主体与音色库，仅限北京地域 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)；
- **Vidu**：提供文生视频、首帧/首尾帧/参考生视频三类核心能力，按广告、剧集、通用等场景细分为多个子模型 [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)；
- **MiniMax**：支持文生视频、首帧/尾帧/首尾帧生视频及多模态参考生视频 [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)；
- **人像驱动类**：包括 VideoRetalk（口型替换）、视频风格重绘、数字人 wan2.2-s2v（单图+音频生成说话视频）等 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)。

> **注意**：万相2.6及更早模型（如 `wanx2.1-i2v-turbo`）与万相2.7+ 新版协议不兼容；旧版接口路径、参数结构及支持地域存在差异，[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md) 文档明确提示“推荐优先选用”新版。

## 关键参数

所有视频生成 API 均需以下**必选请求头**：
- `Content-Type: application/json`
- `Authorization: Bearer <API_KEY>`（除部分仅限北京地域的模型外，均需此头）
- `X-DashScope-Async: enable`（**必须显式设置**，否则报错 `"current user api does not support synchronous calls"`）

**请求体（Request Body）核心字段**：
- `model`（`string`，必选）：模型标识符，如 `wan2.7-videoedit`、`pixverse/pixverse-v6-max-t2v`、`vidu/viduq3-pro_text2video`；
- `input`（`object`，必选）：承载输入内容，结构因模型而异：
  - 文生视频：通常含 `prompt`（文本提示词，长度限制依模型而定，如 Vidu ≤5000 字符，MiniMax ≤7000 字符）；
  - 图生视频：含 `img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）；
  - 参考生视频：含 `media` 数组，支持混合传入图片、视频、音频；
  - 对口型/动作模仿：含 `media` 数组，指定 `image_url` + `audio_url` 或 `video_url`；
- `parameters`（`object`，可选）：控制输出规格，常见参数包括：
  - `resolution`（如 `"720P"`、`"1080P"`、`"4k"`）；
  - `style`（如视频风格重绘的 `0`–`7` 风格码）；
  - `video_fps`（帧率，默认 15–30）；
  - `animate_emotion`（是否优化表情）。

## 使用方式

1. **开通服务与配置环境**：在百炼控制台开通对应模型，获取并配置**同地域**的 API Key 到环境变量 `DASHSCOPE_API_KEY`；
2. **构造请求 URL**：使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`，其中 `{WorkspaceId}` 为控制台业务空间详情页所见 ID，`{region}` 如 `cn-beijing`；
3. **发起异步任务**：`POST` 请求，携带上述必选 Header 与 Body，成功后获得 `task_id`（有效期 24 小时）；
4. **轮询获取结果**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：部分模型（如数字人 `wan2.2-s2v`）需**前置图像检测**（调用 `/api/v1/services/aigc/image2video/face-detect`），且该检测本身即计费，即使不通过 [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），混用将导致鉴权失败或服务报错；
- **异步强制要求**：所有视频 API 仅支持异步，`X-DashScope-Async: enable` 为硬性要求，缺失即报错；
- **任务 ID 时效性**：`task_id` 有效期严格为 24 小时，超时无法查询，需及时轮询；
- **输入资源要求**：媒体文件（图/视/音）必须为公网可访问的 HTTP/HTTPS URL；若使用 OSS 临时 URL，需额外添加请求头 `X-DashScope-OssResourceResolve: enable`；
- **模型演进策略**：万相、爱诗、Vidu 等均明确标注新旧模型迭代关系（如万相2.7替代2.6，爱诗v6替代v5.6），旧版文档虽仍可查，但**生产环境应优先选用新版协议模型**；
- **北京地域特例**：VideoRetalk、数字人 `wan2.2-s2v`、可灵、Vidu、爱诗等多数模型**仅支持华北2（北京）地域**，其文档均以“本文档仅适用于华北2（北京）地域”开头，调用时不可使用其他地域 Endpoint。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
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
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)


