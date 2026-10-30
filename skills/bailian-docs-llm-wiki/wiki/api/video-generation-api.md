# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘、超分增强等核心能力。所有视频类 API 均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。开发者需确保模型、Endpoint URL 与 API Key 严格同地域部署。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同场景与性能需求：

- **万相（WanX）**：全能型多模态视频模型，支持文生视频、图生视频（首帧/首尾帧/续写）、参考生视频、视频编辑、图生动作、视频换人、数字人（s2v）、视频特效等。其中万相3.0为统一 All-in-One 模型，最长支持30秒、30fps输出；万相2.7为当前主力推荐版本，全面替代早期2.1–2.6系列 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
- **HappyHorse**：专注物理真实感与运动流畅性，提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调自然动态建模。
- **爱诗（PixVerse）**：强动作控制与多模态融合能力，除基础生成外，额外支持视频对口型、视频动作模仿、视频超清（4K固定输出）等垂直功能 [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)。
- **可灵（Kling）、Vidu、MiniMax**：均为新一代高性能模型，支持文生/图生/参考生/编辑一体化能力；其中可灵 v3-omni 支持全模态输入，Vidu 提供广告/剧集/通用多版本模型选型，MiniMax H3 支持首帧/尾帧/首尾帧灵活组合 [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)。

> **注意**：万相2.1–2.6系列（如 `wanx2.1-i2v-turbo`、`wan2.2-s2v`）已被明确标记为“早期模型”或“旧版协议”，官方文档中多次强调“推荐优先选用万相2.7及以上版本”。例如，[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md) 明确指出其功能覆盖窄于新版，且部分接口路径（如 `/api/v1/services/aigc/image2video/...`）与主流 `/video-generation/...` 不一致，存在兼容性风险，不建议新项目接入。

## 关键参数

所有视频 API 共享以下强制请求头：
- `Content-Type: application/json`
- `Authorization: Bearer <API_KEY>`
- `X-DashScope-Async: enable`（**必须显式设置**，缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：
- `model`（必选）：模型标识符，如 `wan2.7-text2video`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`。各模型支持的具体值详见对应文档。
- `input`（必选）：结构化输入对象，内容依模型而异：
  - 文生视频：`prompt`（文本提示词，长度上限因模型而异，如 Vidu 为5000字符，MiniMax 为7000字符）
  - 图生视频：`img_url`（首帧）或 `first_frame_url` + `last_frame_url`（首尾帧）
  - 参考生视频：`media` 数组，含 `image_url` / `video_url` 类型元素
  - 视频编辑/动作模仿：`media` 数组，明确指定 `type`（如 `image_url`, `video_url`, `audio_url`）
- `parameters`（可选）：控制输出规格，常见参数包括：
  - `resolution`（如 `"720P"`, `"1080P"`, `"4k"`）
  - `style`（风格重绘专用，整数枚举）
  - `video_fps`（帧率，默认15–30）
  - `animate_emotion`（表情优化开关）

## 使用方式

所有视频 API 均遵循两步异步流程：

1. **创建任务**：向地域专属 Endpoint 发送 `POST` 请求（URL 格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），传入完整请求体。成功响应返回 JSON，含唯一 `task_id`（有效期24小时）。
2. **轮询结果**：使用 `task_id` 向任务查询接口（`GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`）轮询状态。当 `status` 为 `"SUCCESS"` 时，响应中 `output.video_url` 即为生成视频的直链。

> **注意**：务必使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。虽然旧域名仍可用，但[HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md) 等多份文档明确指出新域名“能够为推理请求提供卓越的性能和更高的稳定性”，且是华北2（北京）、新加坡地域的官方推荐路径。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint URL、API Key **必须属于同一地域**，跨地域调用必然失败。开通服务、获取 API Key、选择模型均需在控制台同一地域下操作。
- **输入文件要求**：所有媒体资源（图像、视频、音频）必须为公网可访问的 HTTP/HTTPS URL。本地文件需先调用临时存储 API 获取 URL；若使用 OSS URL（`oss://`），请求头必须添加 `X-DashScope-OssResourceResolve: enable`。
- **任务管理**：`task_id` 有效期严格为24小时，过期后无法查询。禁止重复提交相同任务，应复用已有 `task_id` 轮询。
- **模型演进策略**：万相、爱诗、可灵等系列持续迭代，旧版模型（如万相2.6、爱诗v5.6）虽仍可用，但文档中已明确标注“推荐升级至v6”或“建议直接升级”，新项目应优先选用最新主干版本（如 wan2.7、pixverse-v6、kling-v3-omni）。
- **特殊流程**：数字人（s2v）需前置图像检测步骤（调用 `wan2.2-s2v-detect`），检测通过后方可提交生成任务；视频特效（仅限万相早期图生视频）需指定 `template` 字段且忽略 `prompt`。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
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
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)


