# video generation api

阿里云百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘、超分增强等丰富能力。所有视频生成类 API 均采用统一异步调用范式，适用于开发者集成至生产环境。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景与精度需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑。
- **万相（WanX）**：全模态视频生成平台，包含万相3.0（All-in-One统一模型）、万相2.7（新版协议，推荐优先选用）及早期2.1–2.6系列；支持图生视频（含首帧/首尾帧/视频续写）、文生视频、参考生视频、视频编辑、图生动作、视频换人、数字人（s2v）、视频特效等。> **注意**：万相2.7系列已取代旧版协议，文档中明确提示“[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)推荐优先选用”，旧版（2.1–2.6）仅作兼容，不建议新项目接入。
- **爱诗（PixVerse）**：强调动态表现力与多任务泛化能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、视频动作模仿、视频超清等。各子模型（如 `pixverse-c1` 与 `pixverse-v6`）针对打斗/法术等高速场景或通用场景有明确选型建议。
- **可灵（Kling）与 Vidu**：面向高保真创作，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑；可灵提供主体ID复用能力（如代码雨、雷电等预设元素），Vidu 提供广告级（`ad_reference2video`）、剧集级（`drama_reference2video`）等垂直场景优化模型。

此外，还提供专用能力模型：
- **VideoRetalk**（人像驱动）：专注视频口型替换，需人物视频+人声音频输入；
- **视频风格重绘**：支持8种艺术风格（日式漫画、国风水墨等）；
- **数字人 wan2.2-s2v**：需先调用图像检测接口（`wan2.2-s2v-detect`）校验输入合规性，再提交生成任务。

## 关键参数

所有视频生成 API 共享以下核心请求结构与必填参数：

- **HTTP 方法与路径**：`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（部分旧模型如 `wan2.2-animate-move` 使用 `/api/v1/services/aigc/image2video/video-synthesis`，见[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）。
- **请求头（Headers）**：
  - `Content-Type: application/json`（强制）
  - `Authorization: Bearer <API_KEY>`（强制，除部分纯前端调用场景外）
  - `X-DashScope-Async: enable`（强制，所有视频生成 HTTP 调用必须启用异步）
- **请求体（Request Body）**：
  - `model`（字符串，必选）：具体模型标识符，如 `wan2.7-videoedit`、`vidu/viduq3-pro_text2video`、`pixverse/pixverse-lipsync` 等。
  - `input`（对象，必选）：根据模型类型差异较大：
    - 文生视频：`prompt`（文本提示词，长度限制因模型而异，如 Vidu 限5000字符，MiniMax 限7000字符）
    - 图生视频：`img_url` 或 `first_frame`/`last_frame` 图片 URL
    - 参考生视频：`media` 数组，含 `image_url`/`video_url` 等
    - 视频编辑/动作模仿：`media` 数组，明确指定 `type`（如 `video_url`, `image_url`）
  - `parameters`（对象，可选）：控制输出规格，常见字段包括：
    - `resolution` / `style` / `video_fps`（如视频风格重绘API中 `style: 0` 表示日式漫画）
    - `aspect_ratio`（如可灵支持 `16:9`, `9:16`, `1:1`）
    - `duration`（部分模型支持指定时长，如可灵为3–15秒）

> **注意**：`X-DashScope-Async: enable` 是硬性要求，缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”。此设计与数字人 `wan2.2-s2v` 的同步检测接口（`/api/v1/services/aigc/image2video/face-detect`）形成明确区分。

## 使用方式

所有视频生成 API 均遵循标准两步异步流程：

1. **创建任务**：发送 `POST` 请求至对应 endpoint，携带完整请求头与 body。成功响应返回 JSON，含 `task_id` 字段（有效期24小时）。
2. **轮询获取结果**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 定期查询任务状态（建议间隔 ≥5 秒）。当 `status` 为 `SUCCESS` 时，响应中 `output.video_url` 即为生成视频的直链（临时有效，建议及时下载）。

关键实践要点：
- **地域一致性**：模型、Endpoint URL 与 API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。
- **业务空间域名**：强烈推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性。
- **媒体资源要求**：所有图片/视频/音频 URL 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口转换。
- **错误处理**：关注 `status` 字段（`QUEUED`/`RUNNING`/`SUCCESS`/`FAILED`），`FAILED` 时检查 `output.error_msg` 获取具体原因（如提示词超长、URL 不可达、图像不合规等）。

## 限制和注意事项

- **地域限制**：绝大多数视频模型（HappyHorse、万相、爱诗、可灵、Vidu、MiniMax）**仅支持华北2（北京）地域**；万相3.0、HappyHorse 及部分万相2.7 模型在新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港等地域亦有部署，但需确认模型市场中该地域是否已上架。
- **输入规范**：
  - 图像：分辨率通常要求宽高均在 `[400, 7000]` 像素内（如 wan2.2-s2v），格式支持 JPG/JPEG/PNG/BMP/WEBP。
  - 视频：时长多限制在 2–30 秒（如 VideoRetalk 限 2–120 秒，视频风格重绘限 ≤30 秒），大小 ≤100 MB，格式支持 MP4/AVI/MOV 等主流编码。
  - 音频：需清晰人声，无背景音乐/噪音，时长通常 ≤20 秒（如 wan2.2-s2v）或 ≤120 秒（如 VideoRetalk）。
- **计费与配额**：
  - 所有生成任务按实际输出视频秒数或任务次数计费（如 wan2.2-s2v 为 0.5元/秒@480P）。
  - 图像检测（`wan2.2-s2v-detect`）为同步接口，按次计费（0.004元/张），无论检测是否通过。
  - 免费额度存在且有限（如 videoretalk 为 1800 秒），用尽后自动转为后付费。
- **模型弃用风险**：万相2.1–2.6 系列、Vidu v2 等旧模型虽仍可用，但官方文档已明确标注为“早期”或“旧版协议”，新项目应优先选用万相2.7、Vidu v3、可灵 v3 等新版模型以保障长期支持与功能演进。

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
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)


