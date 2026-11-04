# video generation api

百炼平台的 Video Generation API 提供多种视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、动作模仿、风格重绘、超分等场景。所有模型均采用统一[异步调用](../concepts/asynchronous-invocation.md)范式，通过 `task_id` 轮询获取结果，适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型系列及配套工具模型：

- **HappyHorse**：专注物理真实与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类能力。
- **万相（WanX）**：覆盖全链路视频创作，含万相3.0（All-in-One统一模型）、万相2.7（新版协议，推荐使用）、早期2.1–2.6系列（已逐步归档）。除基础生成外，还提供[图生动作](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)、[视频换人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)、[数字人（s2v）](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)等垂直能力。
- **爱诗（PixVerse）**：强于动态表现与特效控制，支持[文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)、[首尾帧生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)、[视频对口型](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)、[动作模仿](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)、[视频超清](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)等。
- **Vidu / 可灵（Kling） / MiniMax**：分别提供高保真长时序建模（Vidu）、多模态融合与编辑（Kling）、以及灵活输入组合（MiniMax）能力，均支持文生视频、图生视频（首帧/首尾帧）、参考生视频等核心路径。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相2.6及更早版本（如 `wanx2.1-vace-plus`）使用不同协议，参数结构与模型名不兼容；旧版文档明确标注“推荐优先选用”新版，开发者应避免混用 [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md) 与 [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)。

## 关键参数

所有视频生成 API 均需以下通用请求头：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，需与模型地域匹配）
- `X-DashScope-Async: enable`（**必选**；缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）中必须包含：

- `model`: 字符串，具体模型名（如 `wan2.7-videoedit`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v3-omni-video-generation`），详见各模型文档。
- `input`: 对象，结构因任务类型而异：
  - 文生视频：`{ "prompt": "..." }`
  - 图生视频（首帧）：`{ "img_url": "...", "prompt": "..." }`
  - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`
  - 参考生视频：`{ "reference_urls": ["..."], "prompt": "..." }`
  - 视频编辑/口型同步等：按媒体类型数组传入 `media: [{ "type": "video_url", "url": "..." }, { "type": "audio_url", "url": "..." }]`

部分模型支持 `parameters` 对象配置分辨率、帧率、风格等（如 Vidu 的 `style` 参数、视频风格重绘的 `style` 整数枚举）。

## 使用方式

所有视频生成任务均为**[异步调用](../concepts/asynchronous-invocation.md)**，流程严格分为两步：

1. **创建任务**：发送 `POST` 请求至对应地域的 Endpoint URL，获取 `task_id`。  
   统一路径为：  
   `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   （注：少数模型如 `wan2.2-s2v` 和 `VideoRetalk` 使用 `/api/v1/services/aigc/image2video/video-synthesis`，见 [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md) 和 [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)）

2. **轮询结果**：使用返回的 `task_id` 向 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：`task_id` 有效期为 **24 小时**，超时后无法查询；同一任务不可重复提交，否则可能触发限流或返回错误。

## 限制和注意事项

- **地域一致性强制要求**：模型、Endpoint URL 与 API Key **必须属于同一地域**（如华北2北京），跨地域调用必然失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已成标准，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移以获得更高稳定性。
- **输入文件约束**：所有图片/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 [临时存储接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 获取有效 URL；OSS 链接（`oss://`）需额外添加请求头 `X-DashScope-OssResourceResolve: enable`。
- **模型时效性**：万相2.1–2.6、Vidu Q2 等早期模型已进入维护期，新项目应优先选用万相3.0、Vidu Q3、PixVerse v6 或 Kling v3 系列；其文档中明确提示“推荐优先选用”新版协议。
- **免费额度与计费**：多数模型按任务或秒级计费（如 `videoretalk` 0.08元/秒，`wan2.2-s2v` 0.5–0.9元/秒），且检测类接口（如 `wan2.2-s2v-detect`）无论结果是否通过均计费，详情参见各模型价格说明。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
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
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)


