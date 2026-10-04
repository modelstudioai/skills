# video generation api

百炼平台提供多种视频生成与编辑能力，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格归属同一地域，跨地域调用将失败。

## 支持的模型/功能

当前支持三大主力视频模型系列及配套工具链：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：覆盖全栈视频生成需求，包括万相3.0（All-in-One统一模型，支持文/图/参考生视频）、万相2.7（新版协议，含图生视频、文生视频、参考生视频、视频编辑）、早期版本（2.1–2.6，已逐步归档），以及专项能力如图生动作、视频换人、数字人（s2v）、视频特效等 [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)。
- **爱诗（PixVerse）**：专注高质量创意视频生成，支持文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型、动作模仿、超清增强等 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **人像驱动系列**：包含 EMO（唱演）、LivePortrait（播报）、AnimateAnyone（舞蹈）、VideoRetalk（口型替换）、Emoji（表情包）、视频风格重绘等轻量级、高时效性人像动画模型，均需前置图像检测 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)。

> **注意**：万相2.7系列与万相3.0虽共用 `/api/v1/services/aigc/video-generation/video-synthesis` 端点，但协议细节与参数要求不同；旧版万相2.1–2.6部分接口（如 `image2video/video-synthesis`）路径已弃用，新项目应优先选用万相3.0或万相2.7。

## 关键参数

所有视频生成 API 的通用关键参数如下：

- **请求头（Headers）**
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选）
  - `X-DashScope-Async: enable`（**HTTP调用必选**；缺失将报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**
  - `model`（字符串，必选）：模型标识符，例如 `wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`emo-v1`。
  - `input`（对象，必选）：承载核心输入数据，结构因模型而异：
    - 文生视频：`prompt`（文本提示词，长度通常 ≤5000 字符）
    - 图生视频：`img_url`（首帧图链接）或 `first_frame_url` + `last_frame_url`
    - 参考生视频：`reference_images`（图片URL数组）或 `reference_video_url`
    - 数字人/EMO/LivePortrait：`image_url` + `audio_url`
    - VideoRetalk：`video_url` + `audio_url` + `face_image_url`
    - Emoji：`image_url` + `face_bbox` + `ext_bbox` + `driven_id`（模板ID）
  - `parameters`（可选对象）：控制输出质量，常见字段：
    - `resolution`（如 `"720P"`）
    - `style`（风格类型，如 `video-style-transform` 的 `style: 4` 表示国风卡通）
    - `video_fps`（帧率，默认15）
    - `animate_emotion`（是否优化面部表情）

## 使用方式

1. **环境准备**  
   - 在阿里云百炼控制台开通对应模型服务，并确认其所属地域。
   - 获取该地域专属的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并配置至环境变量 `DASHSCOPE_API_KEY`。
   - 获取业务空间 ID（WorkspaceId），用于构造 Endpoint URL。

2. **构造请求 URL**  
   统一使用业务空间专属域名（推荐）：  
   `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   其中 `{region}` 示例：`cn-beijing`（华北2）、`ap-southeast-1`（新加坡）、`us-east-1`（美国弗吉尼亚）等。  
   > **注意**：部分早期文档（如 [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)）仍引用旧路径 `/api/v1/services/aigc/image2video/video-synthesis`，该路径已不适用于主流视频生成模型，请以新版 `/video-generation/` 路径为准。

3. **发起异步调用**  
   - `POST` 请求提交任务，获取 `task_id`。
   - 使用 `task_id` 轮询 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 获取状态与结果（具体轮询接口由各模型文档定义）。

4. **结果解析**  
   成功响应中 `output.video_url` 字段为生成视频的直连下载地址（有效期通常为24小时）。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2），否则鉴权失败或返回空结果。此规则适用于所有视频模型，包括 HappyHorse、万相、爱诗及人像驱动系列。
- **输入资源约束**：
  - 图片：格式支持 JPG/JPEG/PNG/BMP/WEBP；分辨率宽高均在 [400, 7000] 像素；文件大小 ≤10MB。
  - 视频：格式支持 MP4/AVI/MOV/FLV 等；时长 ≤30秒（风格重绘）或 ≤120秒（VideoRetalk）；文件大小 ≤300MB。
  - 音频：格式支持 WAV/MP3；时长 1s–3min；需人声清晰、无背景噪音。
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询结果；请勿重复提交相同任务。
- **计费与限流**：多数模型按秒计费（如 wan2.2-s2v 720P 为 0.9元/秒），且存在 QPS/RPS 限制（如 emo-v1 为 1 QPS）。免费额度详情参见各模型定价页。
- **预检必要性**：数字人（s2v）、EMO、LivePortrait、AnimateAnyone、Emoji 等模型**必须先调用对应图像检测 API**（如 `wan2.2-s2v-detect`、`emo-detect-v1`），仅当 `output.check_pass == true` 时方可进入视频生成流程。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
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
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)


