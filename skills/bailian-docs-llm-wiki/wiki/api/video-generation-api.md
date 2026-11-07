# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、视频风格重绘、口型替换、动作模仿、超分增强等丰富能力。所有视频生成任务均采用异步调用模式，需通过“创建任务 → 轮询查询”两步完成，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景与性能需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑。
- **万相（WanX）**：功能最全的多模态视频模型家族，包含万相3.0（All-in-One统一接口）、万相2.7（新版协议，推荐优先选用）及早期2.1–2.6版本；支持文生、图生（首帧/首尾帧/视频续写）、参考生、视频编辑、图生动作、视频换人、数字人（s2v）等 [详见万相文档](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)。
- **爱诗（PixVerse）**：强调动态表现力与可控性，支持文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型、动作模仿、视频超清等细分能力，各子模型（如 `c1`/`v6`）针对打斗、法术等高速场景有专项优化。
- **可灵（Kling）、Vidu、MiniMax、数字人（wan2.2-s2v）、声动人像（VideoRetalk）等**：提供差异化能力，如可灵支持主体ID复用（见[kling-object-ids.md](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)），Vidu 提供广告/剧集专用参考生视频模型，MiniMax 支持尾帧输入等。

> **注意**：万相2.7系列（如 `wan2.7-videoedit`）与万相早期版本（2.1–2.6）使用不同协议和参数结构，二者不兼容；旧版文档明确标注“推荐优先选用”新版，实际开发应以万相2.7或万相3.0为准。

## 关键参数

所有视频生成 API 均遵循统一的基础参数规范，核心请求头与请求体字段如下：

- **必选请求头（Headers）**：
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`（除部分纯前端/检测类接口外，绝大多数生成接口必需）
  - `X-DashScope-Async: enable`（HTTP 异步调用强制要求；缺失将报错 `current user api does not support synchronous calls`）

- **必选请求体（Body）**：
  - `model`: 字符串，指定具体模型标识符（如 `wan2.7-videoedit`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v3-omni-video-generation`）。
  - `input`: 对象，内容依模型能力而异：
    - 文生视频：`{"prompt": "描述文本"}`
    - 图生视频（首帧）：`{"img_url": "https://...", "prompt": "..."}`
    - 首尾帧：`{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`
    - 参考生视频：`{"reference_images": [...], "prompt": "..."}`
    - 视频编辑：`{"video_url": "...", "prompt": "...", "reference_image_url": "..."}`

- **常用可选参数（parameters）**：
  - `resolution`: 如 `"720P"`, `"1080P"`, `"4k"`（部分模型支持）
  - `style`: 风格索引（如视频风格重绘 API 中 `0` 表示日式漫画）
  - `video_fps`: 输出帧率（如 `15`, `30`）
  - `animate_emotion`: 是否启用面部表情优化（布尔值）

## 使用方式

所有视频生成 API 均采用标准异步流程：

1. **创建任务**：向对应地域的 Endpoint 发送 `POST /api/v1/services/aigc/video-generation/video-synthesis` 请求（注意：部分早期模型如 `wan2.2-animate-move` 使用 `/api/v1/services/aigc/image2video/video-synthesis`，见[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）。成功后返回 JSON 包含 `task_id`（有效期 24 小时）。
2. **轮询结果**：使用 `GET /api/v1/tasks/{task_id}` 查询任务状态。当 `status` 为 `"SUCCESS"` 时，响应中 `output.video_url` 即为生成视频的直链（通常为临时 OSS URL，有效期数小时）。

**Endpoint 地域规则**：  
必须使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如北京为 `cn-beijing`，新加坡为 `ap-southeast-1`）。`{WorkspaceId}` 在控制台“业务空间详情”页获取。旧域名 `dashscope.aliyuncs.com` 仍可用但不推荐。

## 限制和注意事项

- **地域强一致性**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京），否则鉴权失败或服务报错。新加坡、北京等地域的 API Key 不可混用。
- **输入文件要求**：所有媒体 URL（图片、视频、音频）必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)接口转换。
- **OSS URL 特殊处理**：若使用平台临时存储生成的 `oss://` 链接，HTTP 请求头中**必须添加** `X-DashScope-OssResourceResolve: enable`，否则报错 `No connection adapters were found for 'oss://...'`。
- **任务并发与配额**：部分模型（如 VideoRetalk）有严格的 RPS 和并发任务数限制（如“同时处理中任务数量：1”），需在业务侧做好队列管理。
- **模型弃用提示**：万相2.1–2.6 等早期模型已明确标注为“legacy”，其文档中多次强调“全新推出的万相2.7…推荐优先选用”，新项目应避免接入旧版协议。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
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
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)


