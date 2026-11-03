# video generation api

百炼平台的 Video Generation API 提供统一的异步调用接口，支持多种视频生成范式（文生视频、图生视频、参考生视频、视频编辑等），由 HappyHorse、万相（WanX）、爱诗（PixVerse）、可灵（Kling）、Vidu、MiniMax 等多个模型提供底层能力。所有请求均通过 `POST /api/v1/services/aigc/video-generation/video-synthesis` 统一入口提交，需严格保证模型、Endpoint URL 与 API Key 同地域，并使用业务空间专属域名以获得最佳性能与稳定性。

## 支持的模型/功能

当前 API 支持以下主流视频生成模型及对应能力：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调物理真实性和运动流畅性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **万相（WanX）**：覆盖全栈能力，包括万相3.0（All-in-One，统一支持文/图/参考生视频）、万相2.7（新版协议，支持首帧/首尾帧/视频续写/指令编辑）、以及早期2.1–2.6系列（如图生动作、视频换人、数字人s2v等）[万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。
- **爱诗（PixVerse）**：支持文生视频、首帧/首尾帧图生视频、参考生视频、视频对口型、动作模仿、超清增强等细分场景，模型命名体系清晰（如 `pixverse-v6-t2v`, `pixverse-motioncontrol`）[爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)。
- **可灵（Kling）**：提供多版本模型（`kling-v3-turbo`, `kling-v3-omni`），其中 `omni` 版本支持文生视频、首帧/首尾帧图生视频、参考生视频及视频编辑五合一能力。
- **Vidu**：专注高质量长时序一致性，提供 `q3-pro`（精品剧）、`q3-ad`（广告）、`q3-drama`（漫剧）等垂直场景优化模型。
- **MiniMax**：支持文生视频及[多模态](../concepts/multi-modal.md)参考生视频（图片+视频融合），模型标识为 `MiniMax-H3`。

> **注意**：万相2.7系列与万相早期（2.1–2.6）模型使用不同协议；前者强制要求 `X-DashScope-Async: enable` 头，而部分早期文档（如[万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，该路径已废弃，应统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。

## 关键参数

所有视频生成请求均需包含以下核心参数：

### 请求头（Headers）
- `Content-Type`: 必须为 `application/json`
- `Authorization`: 格式为 `Bearer <API_KEY>`，需与模型所在地域匹配
- `X-DashScope-Async`: **必须设置为 `enable`**，HTTP 请求不支持同步模式；缺失将报错 `"current user api does not support synchronous calls"`（见[万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)）

### 请求体（Request Body）
- `model`: 字符串，模型唯一标识（如 `wanx3.0-video-generation`, `vidu/viduq3-pro_text2video`, `pixverse/pixverse-v6-t2v`）
- `input`: 对象，结构因模型类型而异：
  - 文生视频：`{ "prompt": "..." }`
  - 图生视频（首帧）：`{ "img_url": "...", "prompt": "..." }`
  - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`
  - 参考生视频：`{ "reference_media": [...], "prompt": "..." }`
- `parameters`: 对象（可选），用于控制分辨率（`"resolution": "720P"`）、宽高比（`"aspect_ratio": "16:9"`）、帧率（`"video_fps": 24`）等输出规格

## 使用方式

API 采用标准异步两步流程：

1. **创建任务**：发送 `POST` 请求至对应地域的 Endpoint（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），携带上述参数。成功后返回 JSON 响应，含 `task_id` 字段。
2. **轮询获取结果**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 定期查询任务状态（建议间隔 ≥5 秒）。当 `status` 为 `"SUCCESS"` 时，响应中 `output.video_url` 即为生成视频的直链（有效期通常为 24 小时）。

> **注意**：`task_id` 有效期为 24 小时，过期后无法查询；重复提交相同请求会创建新任务，**请勿重复创建任务**，仅轮询即可（见[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)）。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint URL、API Key **必须属于同一地域**（如华北2北京），跨地域调用必然失败。
- **域名迁移**：华北2（北京）与新加坡地域已启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但官方**强烈建议迁移**以获得更高性能与稳定性。
- **输入文件要求**：所有图像/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用临时 URL 接口上传（见[上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)）。
- **计费与限流**：各模型独立计费（按秒/张/次），并有 RPS 及并发任务数限制（如 wan2.2-s2v 检测接口限流 5 QPS），详情需查阅具体模型文档。
- **错误处理**：常见错误包括 `X-DashScope-Async` 缺失、`model` 名称错误、`prompt` 超长（如 Vidu 限 5000 字符，MiniMax 限 7000 字符）、媒体 URL 不可达等，需根据返回错误码精准定位。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
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
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)


