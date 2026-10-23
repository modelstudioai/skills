# video generation api

百炼平台的视频生成 API 提供多模型、多模态的视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型驱动、风格重绘、超分等多种任务类型。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。

## 支持的模型/功能

当前平台提供三大主力视频模型系列及多个垂直能力模型：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频和视频编辑四类任务。
- **万相（WanX）**：覆盖全场景，包含万相3.0（All-in-One统一模型，支持文/图/参考生视频）、万相2.7（新版协议，推荐使用）、以及早期2.1–2.6系列（已逐步归档）。另提供图生动作、视频换人、数字人（s2v）等专项能力。
- **爱诗（PixVerse）**、**可灵（Kling）**、**Vidu**、**MiniMax**：均提供文生视频、图生视频（首帧/首尾帧）、参考生视频及视频编辑能力，各具特色（如PixVerse强调动态特效，Kling支持主体ID复用，Vidu强化广告与剧集场景）。

此外，还提供独立功能模型：
- **视频口型替换（VideoRetalk）**：基于人物视频+音频生成口型同步视频；
- **视频风格重绘**：将输入视频转换为8种预设艺术风格；
- **视频超清（PixVerse Upscale）**：将输入视频升频至4K分辨率；
- **数字人（wan2.2-s2v）**：需先调用图像检测接口（`wan2.2-s2v-detect`）再提交生成任务，详见[数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)。

> **注意**：万相2.7系列（如`wan2.7-videoedit`）与万相早期版本（如`wanx2.1-vace-plus`）使用相同Endpoint但参数结构和兼容性不同，旧版文档中部分字段（如`parameters.resolution`）在新版中已移入`input`或废弃，请以[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)为准。

## 关键参数

所有视频生成 API 共享以下核心参数规范：

- **必选请求头（Headers）**：
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`（除部分仅北京地域的模型如`wan2.2-s2v`外均需）
  - `X-DashScope-Async: enable`（**必须显式设置**，否则返回“current user api does not [support](../guides/support.md) synchronous calls”错误）

- **必选请求体（Body）字段**：
  - `model`：字符串，指定模型标识符（如`wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`），不同模型能力与输入要求差异显著，选型需严格匹配任务类型。
  - `input`：对象，承载任务核心输入：
    - 文生视频：`prompt`（文本提示词，长度上限因模型而异，如Vidu为5000字符，MiniMax为7000字符）；
    - 图生视频：`img_url`（首帧）或`first_frame`/`last_frame`（首尾帧）；
    - 参考生视频：`media`数组，含`image_url`、`video_url`等多类型元素；
    - 数字人：`image_url` + `audio_url`；
    - 视频编辑/重绘/超分：`video_url`（或`media`数组）。

- **地域一致性要求**：模型、Endpoint URL 与 API Key **必须属于同一地域**（如华北2北京），跨地域调用必然失败。业务空间专属域名（如`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已全面替代旧版`dashscope.aliyuncs.com`，强烈建议迁移。

## 使用方式

所有视频生成任务均采用标准异步流程：

1. **创建任务**：向对应地域的Endpoint发送`POST /api/v1/services/aigc/video-generation/video-synthesis`（少数模型如`wan2.2-s2v`、`videoretalk`使用`/api/v1/services/aigc/image2video/video-synthesis`）；
2. **轮询结果**：使用返回的`task_id`，向`GET /api/v1/tasks/{task_id}`发起轮询（推荐间隔≥3秒），直至`status`为`SUCCESS`，响应中`output.video_url`即为生成视频地址。

> **注意**：`task_id`有效期为24小时，过期后无法查询；重复提交相同参数任务将生成新`task_id`，但不保证结果一致，**严禁重复创建任务**。

## 限制和注意事项

- **地域与密钥强绑定**：华北2（北京）与新加坡地域拥有独立API Key与Endpoint，不可混用；部分模型（如`wan2.2-s2v`、`videoretalk`、`video-style-transform`）**仅支持北京地域**，调用其他地域URL将失败。
- **输入文件要求**：所有媒体URL必须为公网可访问的HTTP/HTTPS链接；本地文件需先调用[上传获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)接口；若使用OSS临时URL，请求头需额外添加`X-DashScope-OssResourceResolve: enable`。
- **模型演进与兼容性**：万相2.7系列已取代2.1–2.6旧版，旧版文档（如`legacy-video-models`）仅作历史参考；万相3.0作为统一模型，推荐新项目优先选用。爱诗、可灵、Vidu等模型均持续迭代，具体能力请以各模型最新API参考文档为准。
- **计费与限流**：多数模型按视频秒数或任务次数计费（如`videoretalk` 0.08元/秒，`wan2.2-s2v` 480P 0.5元/秒），且存在RPS与并发任务数限制（如`videoretalk`同时处理中任务数上限为1），高并发场景需合理设计重试与排队逻辑。

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
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


