# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有视频生成 API 均采用异步调用模式，任务创建后需轮询获取结果，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

平台当前提供三大类视频生成模型体系：

- **通用视频生成模型**：  
  - `HappyHorse` 系列：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)；  
  - `万相（WanX）` 系列：涵盖 2.7/3.0 版本，支持文生视频、图生视频（首帧/首尾帧/视频续写）、参考生视频、视频编辑、图生动作、视频换人、数字人（s2v）等全栈能力；其中万相3.0为“All-in-One”统一模型，最长支持30秒、30fps输出 [万相3.0-视频生成](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；  
  - `爱诗（PixVerse）` 系列：提供文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、动作模仿、超清增强等功能，支持多版本模型选型（c1/v6/v5.6）以适配不同动态场景 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。

- **人像驱动与数字人模型**：  
  - `EMO`、`LivePortrait`、`AnimateAnyone`、`VideoRetalk`、`Emoji` 等专注人像生成，均需先通过对应图像检测模型（如 `emo-detect-v1`、`liveportrait-detect`）验证输入合规性，再提交生成任务；  
  - `万相-s2v`（数字人）需分两步：先调用 `wan2.2-s2v-detect` 检测图片，再调用 `wan2.2-s2v` 生成视频 [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)。

- **专项增强模型**：  
  - `视频风格重绘`：支持日式漫画、国风水墨等8种预设艺术风格转换；  
  - `万相-视频特效`：仅适用于早期图生视频模型（2.1–2.6），通过 `template` 参数指定特效（如 `flying`、`hanfu-1`），无需提示词 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。

> **注意**：万相2.1–2.6系列（如 `wanx2.1-i2v-turbo`）与2.7+新版协议不兼容，其 Endpoint 路径存在差异（旧版为 `/api/v1/services/aigc/image2video/...`，新版统一为 `/api/v1/services/aigc/video-generation/...`）。文档中明确标注“旧版协议”的模型（如[万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)）已逐步淘汰，强烈建议迁移至 wan2.7 或 wan3.0。

## 关键参数

所有视频生成 API 的核心请求参数结构一致，关键字段如下：

- **请求头（Headers）**（必选）：
  - `Content-Type`: 固定为 `application/json`；
  - `Authorization`: 格式为 `Bearer <API_KEY>`；
  - `X-DashScope-Async`: 必须设置为 `enable`，缺失将报错 `"current user api does not support synchronous calls"`。

- **请求体（Request Body）**（必选）：
  - `model`: 模型名称（如 `happyhorse-text-to-video`、`wan3-video-generation`、`pixverse/pixverse-v6-t2v`、`emo-v1`），不同模型有特定可选值；
  - `input`: 输入对象，结构因模型而异：
    - 文生视频：含 `prompt`（文本提示词，长度限制依模型而定，如 wan2.7 限5000字符）；
    - 图生视频：含 `img_url`（首帧图）、`prompt`（可选）；
    - 首尾帧生视频：含 `first_frame_url` 和 `last_frame_url`；
    - 参考生视频：含 `ref_image_urls` 或 `ref_video_url` 数组；
    - 数字人/EMO/LivePortrait：含 `image_url` 和 `audio_url`；
    - 视频风格重绘：含 `video_url` 和 `parameters.style`（整数0–7）；
    - 视频特效：仅需 `img_url` + `template`，忽略 `prompt`。

- **地域与业务空间**：  
  所有 Endpoint URL 均需替换 `{WorkspaceId}` 为实际业务空间 ID，并选择与模型、API Key 匹配的地域域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。

## 使用方式

所有视频生成 API 均遵循标准异步流程：

1. **创建任务**：  
   向对应地域的 Endpoint 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求，携带上述 Headers 和 Request Body。成功响应返回 `task_id`（有效期24小时）。

2. **轮询获取结果**：  
   使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}`（具体路径见各模型文档），检查 `status` 字段（`QUEUED`/`RUNNING`/`SUCCESS`/`FAILED`）。`SUCCESS` 时，响应中 `output.video_url` 即为生成视频的可访问链接。

- **SDK 支持**：万相2.7+、爱诗、HappyHorse 等主流模型均支持 DashScope SDK 调用，推荐安装最新版 SDK 并配置环境变量 `DASHSCOPE_API_KEY` [安装DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
- **新手指引**：首次调用建议使用 Postman 工具快速验证 [Postman](../../raw/model-user-guide/use-chat-client-or-development-tool/first-call-to-image-and-video-api.md)；
- **图像/视频上传**：若文件本地存储，需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口，再将返回的公网 URL 传入 `input`。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），否则直接失败。不同地域的 API Key 不可混用 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **业务空间专属域名迁移**：华北2（北京）和新加坡地域已启用 `https://{WorkspaceId}.<region>.maas.aliyuncs.com` 新域名，性能与稳定性更优，旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **输入合规性前置校验**：数字人（s2v）、EMO、LivePortrait、AnimateAnyone、Emoji 等模型**必须**先调用对应 `*-detect` 接口验证输入，否则生成任务将失败或效果异常；检测本身计费且不通过也收费。
- **资源限制**：多数模型有 QPS/RPS 限制（如万相2.7系列为1 QPS）、同时处理任务数限制（如 EMO 为1个）、免费额度（如 s2v-detect 免费200张/月），详情请查阅各模型资费文档。
- **文件格式与大小**：  
  - 图像：支持 JPG/PNG/BMP/WEBP，常见尺寸范围 400–7000 像素，文件 ≤10MB；  
  - 视频：支持 MP4/AVI/MOV 等，常见时长 ≤30秒，大小 ≤100MB（风格重绘）或 ≤300MB（VideoRetalk）；  
  - 音频：支持 WAV/MP3，时长通常 1–120 秒，需人声清晰、无背景噪音。

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
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


