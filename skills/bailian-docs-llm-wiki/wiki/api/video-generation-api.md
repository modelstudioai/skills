# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、人像驱动及风格迁移等场景。所有视频生成 API 均采用统一异步调用范式（创建任务 → 轮询获取），支持多地域部署与业务空间专属域名，适用于生产级视频内容创作与编辑需求。

## 支持的模型/功能

当前平台提供三大主力视频生成模型系列，各具定位与能力边界：

- **HappyHorse**：专注高物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频（基于首帧）](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类核心能力，适用于影视级内容生成。

- **万相（WanX）**：提供全栈视频生成能力，包含：
  - **万相3.0**：All-in-One 统一模型，支持文生视频、首帧/首尾帧图生视频、参考生视频，最长输出30秒、30fps视频；
  - **万相2.7**：新版协议模型，覆盖文生、图生、参考生、视频编辑四大任务，推荐优先选用；
  - **早期模型（2.1–2.6）**：已逐步归档，仅限存量调用，[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)文档明确标注其功能局限（如仅支持首帧生视频）；
  - **垂直能力**：图生动作、视频换人、数字人（s2v）、视频特效等，均需按独立模型名调用。

- **爱诗（PixVerse）**：强调动态表现力与多模态融合，支持[文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)、[首帧/首尾帧图生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)、[视频对口型](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)、[视频动作模仿](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)及[视频超清](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)，尤其在打斗、法术等高速动态场景中推荐 `c1` 系列模型。

> **注意**：万相2.7系列与万相3.0虽共用同一 endpoint `/api/v1/services/aigc/video-generation/video-synthesis`，但模型名（如 `wan2.7-t2v` vs `wan3`）和参数结构存在差异，不可混用；旧版万相2.6及更早模型（如 `wanx2.1-i2v-turbo`）使用不同协议，部分接口路径为 `/api/v1/services/aigc/image2video/video-synthesis`，需严格区分。

## 关键参数

所有视频生成 API 共享以下必需请求头与基础结构：

- **请求头（Headers）**
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选，需与模型地域匹配）
  - `X-DashScope-Async: enable`（必选，所有 HTTP 调用必须启用异步）

- **请求体（Request Body）**
  - `model`（必选）：模型名称，例如：
    - HappyHorse：`happyhorse-t2v`, `happyhorse-i2v`
    - 万相3.0：`wan3`
    - 万相2.7：`wan2.7-t2v`, `wan2.7-i2v`, `wan2.7-r2v`, `wan2.7-videoedit`
    - 爱诗：`pixverse/pixverse-v6-t2v`, `pixverse/pixverse-c1-kf2v`, `pixverse/pixverse-motioncontrol`
  - `input`（必选，结构因模型而异）：
    - 文生视频：`{"prompt": "描述文本"}`
    - 图生视频（首帧）：`{"img_url": "https://...", "prompt": "可选描述"}`
    - 首尾帧图生视频：`{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`（爱诗）或 `{"img_url": "...", "last_img_url": "..."}`（万相2.7）
    - 参考生视频：`{"ref_images": ["url1", "url2"], "prompt": "..."}` 或 `{"ref_video_url": "..."}`（万相/爱诗）
    - 视频编辑：`{"video_url": "...", "prompt": "编辑指令"}`（HappyHorse/Wan2.7）
    - 人像驱动（EMO/LivePortrait）：`{"image_url": "...", "audio_url": "...", "face_bbox": [...], "ext_bbox": [...]}`（需先经图像检测）
  - `parameters`（可选）：常见字段包括 `resolution`（如 `"720P"`）、`style`（风格重绘）、`video_fps`（帧率）、`animate_emotion`（表情优化）等。

> **注意**：数字人（wan2.2-s2v）、AnimateAnyone、EMO、LivePortrait、VideoRetalk 等人像驱动模型**不使用 `/video-generation/` 路径，而统一使用 `/image2video/` 路径**，且必须先调用对应图像检测 API（如 `wan2.2-s2v-detect`、`emo-detect-v1`）并传入检测返回的 `face_bbox` 和 `ext_bbox` 坐标，否则会失败。详见[数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)。

## 使用方式

1. **环境准备**  
   - 确保模型、Endpoint URL 与 API Key 属于**同一地域**（跨地域调用必然失败）；
   - 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于通用域名 `dashscope.aliyuncs.com`；
   - 获取业务空间 ID：控制台 → 业务空间详情页。

2. **异步调用流程**  
   所有视频生成任务均需两步：
   - **步骤1：创建任务**  
     `POST {workspace_url}/api/v1/services/aigc/{service_path}/video-synthesis`  
     （`service_path` 通常为 `video-generation`，但人像驱动类为 `image2video`）  
     成功响应含 `task_id`（有效期24小时）。
   - **步骤2：轮询结果**  
     `GET {workspace_url}/api/v1/tasks/{task_id}`  
     直至 `status` 为 `SUCCESS`，`output.video_url` 字段返回可下载视频地址。

3. **SDK 调用**  
   DashScope SDK 已封装上述流程，开发者可直接调用 `Generation.call()` 并设置 `async_req=True`，SDK 自动处理任务提交与轮询。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京），否则鉴权失败或服务报错。[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)明确强调“华北2（北京）和新加坡地域拥有独立的 API Key 与请求地址，不可混用”。

- **输入合规性前置检查**：  
  - 数字人（s2v）、EMO、LivePortrait、Emoji、AnimateAnyone 等人像驱动模型**必须先调用图像检测 API**（如 `wan2.2-s2v-detect`、`emo-detect-v1`），检测通过后方可提交生成任务；  
  - 检测不通过仍计费（见[数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)）；  
  - 图像要求严格：单人正面、无遮挡、清晰人脸、宽高比≤2、边长400–7000像素。

- **文件与内容限制**：  
  - 视频：时长≤30秒（风格重绘）、≤120秒（VideoRetalk），大小≤100MB（风格重绘）、≤300MB（VideoRetalk），格式支持 MP4/AVI/MOV 等；  
  - 图像：URL 必须公网可访问，本地文件需先调用 [get-temporary-file-url](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 获取临时链接；  
  - 音频：时长1s–3min（LivePortrait）、2s–120s（VideoRetalk），格式 WAV/MP3，需纯净人声。

- **模型版本演进**：  
  - 万相2.7 已取代 2.6 及更早版本，[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)明确提示“原[图生视频-基于首帧](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)（wan2.6及早期模型）仅支持首帧生视频”，旧版文档仅作兼容参考；  
  - 爱诗模型推荐使用 `v6` 系列，`v5.6` 已不建议选用。

- **错误处理**：缺失 `X-DashScope-Async: enable` 请求头将报错 “current user api does not [support](../guides/support.md) synchronous calls”，此为高频失败原因，务必校验。

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
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)


