# video generation api

百炼平台的 Video Generation API 提供多种文生视频、图生视频、参考生视频及视频编辑能力，由 HappyHorse、万相（WanX）、爱诗（PixVerse）、Vidu、可灵（Kling）、MiniMax 等多个模型系列支撑。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），支持多地域部署与业务空间专属域名，适用于生产级视频生成场景。

## 支持的模型/功能

当前平台提供以下主流视频生成模型及对应能力：

- **HappyHorse**：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实与运动流畅性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **万相（WanX）**：覆盖全栈能力，包括万相3.0（All-in-One，统一支持文/图/参考生视频，最长30秒）、万相2.7（新版协议，支持首帧/首尾帧/视频续写/指令编辑等）、以及早期2.1–2.6系列（如视频换人、图生动作、数字人s2v等）；其中万相3.0是当前推荐主力模型 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。
- **爱诗（PixVerse）**：提供文生视频、首帧/首尾帧生视频、参考生视频、视频对口型、动作模仿、超清增强等细分能力，各子模型按场景优化（如 `c1` 适配高速运动，`v6` 为通用首选）。
- **Vidu**：支持文生视频、首帧/首尾帧生视频、参考生视频，提供多档性能模型（`turbo`/`pro`/`q3`/`q2`），并针对广告、剧集等场景提供专用变体（如 `viduq3-ad_reference2video`）。
- **可灵（Kling）**：支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑五合一能力，输出支持 720P/1080P/4K 及 16:9/9:16/1:1 多种宽高比 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。
- **MiniMax**：支持文生视频、图生视频（首帧/尾帧/首尾帧）、多模态参考生视频，输入提示词长度上限达 7000 字符。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相早期模型（2.1–2.6）使用不同协议和参数结构，二者不可混用；旧版文档中部分 endpoint（如 `/api/v1/services/aigc/image2video/video-synthesis`）仅适用于数字人、VideoRetalk、图生动作等特定模型，而主流视频生成统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。

## 关键参数

所有视频生成 API 均需以下**必选请求头**：
- `Content-Type: application/json`
- `Authorization: Bearer <API_KEY>`（除部分仅限北京地域的模型外，均需此头）
- `X-DashScope-Async: enable`（**必须显式设置**，否则报错 `"current user api does not support synchronous calls"`）

**核心请求体字段**：
- `model`（`string`，必选）：具体模型标识符，如 `wanx3.0-video-generation`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v3-omni-video-generation`。
- `input`（`object`，必选）：根据任务类型差异较大：
  - 文生视频：`{ "prompt": "描述文本" }`
  - 图生视频（首帧）：`{ "img_url": "https://...", "prompt": "..." }`
  - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`
  - 参考生视频：支持 `image_url`、`video_url`、`audio_url` 数组组合
- `parameters`（`object`，可选）：控制分辨率（如 `"resolution": "720P"`）、宽高比（`"aspect_ratio": "16:9"`）、帧率（`"video_fps": 24`）、风格（`"style": 0`）等，具体字段依模型而异。

## 使用方式

1. **准备环境**：确保模型、Endpoint URL 与 API Key 属于**同一地域**（如华北2北京），跨地域调用必然失败；强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高稳定性与性能 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
2. **创建任务**：向对应地域的 `POST /api/v1/services/aigc/video-generation/video-synthesis` 发送请求，获取 `task_id`（有效期 24 小时）。
3. **轮询结果**：使用 `GET /api/v1/tasks/{task_id}` 查询任务状态（`QUEUED`/`RUNNING`/`SUCCESS`/`FAILED`），成功后返回 `output.video_url`。
4. **错误处理**：常见失败原因包括 `task_id` 过期、`X-DashScope-Async` 缺失、`model` 名称错误、输入资源 URL 不可达或格式不合规（如 Vidu 要求首帧图像边长 ≥256px）。

## 限制和注意事项

- **地域强绑定**：所有模型均严格限定地域。例如，万相数字人 `wan2.2-s2v`、VideoRetalk、爱诗全系、Vidu 全系、可灵、MiniMax 等文档均明确标注“仅适用于华北2（北京）地域”，且必须使用该地域的 API Key 和 Endpoint；新加坡、德国、日本等地域仅 HappyHorse 与万相3.0/2.7 明确支持。
- **异步强制要求**：所有视频生成任务均为异步，同步调用将直接报错；`task_id` 有效期严格为 24 小时，超时后无法查询。
- **输入资源规范**：
  - 图像：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率通常要求 400–7000px，需公网可访问；
  - 视频：MP4/AVI/MOV 等，时长 ≤30 秒（多数模型），大小 ≤100MB；
  - 音频：WAV/MP3，时长 <20s（数字人），需人声清晰、无背景噪音。
- **计费与限流**：部分模型（如 VideoRetalk）有 RPS 与并发任务数限制（如“同时处理中任务数量：1”），需在业务侧做好队列管理；数字人 `wan2.2-s2v-detect` 即使检测失败也会计费，因检测流程已执行完毕。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)


