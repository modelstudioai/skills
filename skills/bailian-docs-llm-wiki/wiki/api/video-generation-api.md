# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、人像驱动、风格重绘等核心场景。所有视频生成 API 均采用统一异步调用范式（创建任务 → 轮询获取结果），支持多地域部署与业务空间专属域名，适用于生产级视频内容创作与编辑需求。

## 支持的模型/功能

百炼当前提供三大主力视频生成模型系列，以及面向特定场景的垂直能力模型：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频（基于首帧）](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类基础能力。
- **万相（WanX）**：全能型视频模型家族，其中 **万相3.0** 为 All-in-One 统一模型，原生支持文生、图生（首帧/首尾帧）、参考生等多种输入模式；**万相2.7** 系列则按功能细分为独立 API，如[图生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)、[文生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)、[视频编辑](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)等；此外还提供[图生动作](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)、[视频换人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)、[数字人（s2v）](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)等专业能力。
- **爱诗（PixVerse）**：强调创意表达与动态表现力，提供[文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)、[图生视频（首帧/首尾帧）](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)、[视频对口型](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)和[视频动作模仿](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)等能力。
- **人像驱动系列**：聚焦单张人像的轻量级动态化，包括[AnimateAnyone（舞动人像）](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)、[EMO（悦动人像）](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)、[LivePortrait（灵动人像）](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)、[VideoRetalk（声动人像）](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)、[Emoji（表情包）](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)等，均需先通过图像检测再生成视频。
- **视频风格重绘**：提供8种预设艺术风格（日式漫画、国风水墨等）的批量视频转换能力，详见[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)。

> **注意**：万相2.1–2.6系列（如`wanx2.1-i2v-turbo`）属于早期模型，其 API 路径、参数结构与新版 `wan2.7` 不兼容；文档中明确提示“推荐优先选用”万相2.7及万相3.0，旧版模型仅作兼容性保留，不建议新项目接入。

## 关键参数

所有视频生成 API 的核心请求参数高度一致，关键字段如下：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <your_api_key>`，需与模型所在地域匹配
  - `X-DashScope-Async`: **必须设置为 `enable`**，否则返回错误 `"current user api does not support synchronous calls"`（见[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)）

- **请求体（Request Body）**
  - `model`: 字符串，指定具体模型名称（如 `wan2.7-videoedit`, `pixverse/pixverse-v6-t2v`, `liveportrait`）。不同模型系列命名规则不同，需严格按文档填写。
  - `input`: 对象，承载核心输入数据：
    - 文生类：`prompt`（文本提示词，长度限制因模型而异，如 wan2.7-videoedit ≤5000字符）
    - 图生/人像类：`image_url`（公网可访问的图片链接，格式支持 jpg/png/webp 等）
    - 视频类：`video_url`（公网可访问的视频链接，格式支持 mp4/mov 等）、`audio_url`（音频链接）
    - 参考生类：`media` 数组，可混合传入 `image_url` 和 `video_url`
    - 特效类（如万相视频特效）：`template`（字符串模板ID，无需 `prompt`）
  - `parameters`: 对象，控制生成细节（可选）：
    - 分辨率：`resolution`（如 `"720P"`）或 `style`（风格重绘中的整数ID）
    - 帧率：`video_fps`（范围 15–25）
    - 动作风格：`style_level`（如 EMO 的 `"active"`/`"calm"`）

## 使用方式

所有视频生成 API 均遵循标准异步流程，无同步调用支持：

1. **创建任务**  
   向对应地域的 Endpoint 发送 `POST` 请求（URL 中 `{WorkspaceId}` 需替换为实际业务空间ID）：  
   `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   > **注意**：部分模型（如万相数字人 s2v、AnimateAnyone、VideoRetalk）使用 `/image2video/` 路径而非 `/video-generation/`，例如 `https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis`（见[数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)）。路径差异需严格按各模型文档确认。

2. **轮询获取结果**  
   使用响应中返回的 `task_id`，向 `GET /api/v1/tasks/{task_id}` 接口轮询（间隔建议 ≥3s）。任务状态为 `SUCCESS` 时，响应中 `output.video_url` 即为生成视频的直链（有效期通常为24小时）。

3. **地域与认证一致性**  
   模型、Endpoint URL、API Key **三者必须属于同一地域**（如华北2北京），跨地域调用必然失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）为推荐配置，性能与稳定性优于通用域名 `dashscope.aliyuncs.com`。

## 限制和注意事项

- **地域强绑定**：所有模型均强制要求模型、Endpoint、API Key 同地域。华北2（北京）与新加坡地域拥有独立的 API Key 体系，不可混用（见[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）。
- **输入合规性前置检查**：人像驱动类模型（EMO、LivePortrait、AnimateAnyone、Emoji、s2v）**必须先调用对应图像检测 API**（如 `emo-detect-v1`, `liveportrait-detect`），并将检测返回的 `face_bbox`、`ext_bbox` 等坐标参数作为视频生成请求的输入。跳过检测将导致生成失败。
- **资源与配额**：多数模型存在免费额度（如 200 张图像检测、1800 秒视频生成），超出后按量计费。同时处理中任务数量有限制（如 EMO 为 1 个），排队任务需等待（见[EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)）。
- **媒体文件要求**：  
  - 图片：格式 JPG/PNG/WEBP，分辨率 400–7000 像素，文件大小 ≤10MB；  
  - 视频：格式 MP4/AVI/MOV，时长 ≤30 秒，大小 ≤100MB，单边尺寸 256–4096 像素；  
  - 音频：格式 WAV/MP3，时长 1s–3min，文件大小 <15MB，需人声清晰、无背景噪音。
- **任务生命周期**：`task_id` 有效期统一为 **24 小时**，超时后无法查询结果，需重新提交任务。

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
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


