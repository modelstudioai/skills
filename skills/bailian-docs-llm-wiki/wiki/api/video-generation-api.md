# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、风格迁移等核心场景。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），支持多地域部署与业务空间专属域名，适用于生产级视频内容创作。

## 支持的模型/功能

当前平台提供三大主力视频生成模型系列及若干垂直能力模型：

- **HappyHorse**：专注高质量物理真实感视频生成，支持[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[HappyHorse-图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[HappyHorse-参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[HappyHorse-视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类能力。
- **万相（WanX）**：全栈视频模型家族，覆盖从2.1到3.0的多代演进。其中万相3.0为All-in-One统一模型，支持文生、图生（首帧/首尾帧）、参考生视频等；万相2.7为推荐新版协议，全面替代早期2.1–2.6模型；另提供[万相-图生动作](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)、[万相-视频换人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)、[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)等专项能力。
- **爱诗（PixVerse）**、**可灵（Kling）**、**Vidu**、**MiniMax**：第三方合作模型，各具特色。例如爱诗支持视频对口型、动作模仿与超清增强；可灵4.0支持关键帧（首/中/尾）任意组合生成；Vidu提供广告、剧集等场景化参考生视频模型；MiniMax支持多模态参考输入。

> **注意**：万相2.1–2.6系列（如`wanx2.1-i2v-turbo`）已被明确标记为“早期模型”，文档中多次强调“推荐优先选用”万相2.7或3.0 [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。旧版API路径（如`/api/v1/services/aigc/image2video/...`）与新版（`/api/v1/services/aigc/video-generation/...`）并存，但新模型仅支持新版路径。

## 关键参数

所有视频生成API共用以下核心参数结构：

- **请求头（Headers）**
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选，除部分纯前端调用场景外）
  - `X-DashScope-Async: enable`（**必选**，缺失将报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**
  - `model`（字符串，必选）：指定模型标识符，如 `pixverse/pixverse-v6-t2v`、`kling/kling-v4-omni-video-generation`、`vidu/viduq3-drama_reference2video` 等。
  - `input`（对象，必选）：根据模型类型差异较大：
    - 文生视频：`prompt`（文本提示词，长度限制因模型而异，常见5000–7000字符）
    - 图生视频：`img_url`（首帧）或 `first_frame_url` + `last_frame_url`（首尾帧）
    - 参考生视频：`media` 数组，支持混合传入 `image_url`、`video_url`、`audio_url`
    - 数字人/口型替换：`image_url` + `audio_url` 或 `video_url` + `audio_url`
  - `parameters`（对象，可选）：控制输出规格，常见字段包括：
    - `resolution`（如 `"720P"`、`"1080P"`、`"4k"`）
    - `aspect_ratio`（如 `"16:9"`、`"9:16"`）
    - `style`（风格重绘专用，整数枚举）
    - `video_fps`（帧率，默认15–30）

## 使用方式

1. **前置准备**：确保模型、Endpoint URL 和 API Key **严格属于同一地域**（如华北2北京），跨地域调用必然失败。强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代通用域名（`dashscope.aliyuncs.com`），以获得更高性能与稳定性 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)。

2. **异步调用流程**（两步）：
   - **步骤1：创建任务**  
     `POST {WorkspaceId}-maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
     成功返回 `task_id`（有效期24小时）。
   - **步骤2：轮询结果**  
     `GET {WorkspaceId}-maas.aliyuncs.com/api/v1/tasks/{task_id}`  
     持续查询直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

3. **地域与端点**：支持北京、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港等多地部署。URL 中 `{WorkspaceId}` 需替换为控制台业务空间详情页获取的真实ID。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域，否则直接报错。华北2（北京）与新加坡地域的 API Key **不可混用** [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。
- **异步强制要求**：所有视频API仅支持异步模式，`X-DashScope-Async: enable` 为硬性要求，遗漏即失败。
- **输入文件约束**：图像需公网可访问HTTP/HTTPS链接（不支持本地路径）；视频/音频有明确格式（MP4/AVI/WAV/MP3）、大小（通常≤300MB）、时长（2–120秒）及分辨率限制；上传前建议通过[临时URL服务](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)处理本地文件。
- **任务管理**：`task_id` 24小时后失效，禁止重复提交相同任务；轮询频率建议 ≥2秒/次，避免触发限流。
- **模型兼容性**：不同模型对输入模态支持差异显著（如万相3.0支持首尾帧，而部分早期模型仅支持首帧），务必查阅对应模型文档确认能力边界。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)


