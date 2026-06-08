# video generation api

百炼平台聚合了通义万相（Wan/HappyHorse）、爱诗 Pixverse、可灵 Kling、Vidu 以及一系列数字人 / 特效模型，提供统一的视频生成 HTTP 与 SDK 调用入口。所有视频生成任务均为**[异步任务](../concepts/async-task.md)**——客户端先提交任务获取 `task_id`，再轮询 / WebSocket 查询任务结果，最终拿到可下载的视频 URL（默认 24 小时有效，需自行转存）。

## 支持的能力分类

按"输入形态 → 输出视频"维度划分，主要包含以下几类：

- **文生视频（text-to-video）**：仅文本提示词驱动。覆盖 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)、[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)、[爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-text-to-video-api-reference.md)、[Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-text-to-video-api-reference.md)、[可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)。
- **图生视频（image-to-video）**：基于首帧或首尾帧图片生成。包含 [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-image-to-video-api-reference.md)、[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)、[爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-image-to-video-api-reference.md)、[爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-keyframe-to-video-api-reference.md)、[Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-image-to-video-api-reference.md)、[Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-keyframe-to-video-api-reference.md)。
- **参考生视频（reference-to-video）**：用一张或多张参考图（角色 / 物体 / 风格）控制生成。包含 [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-reference-to-video-api-reference.md)、[万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md)、[爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-reference-to-video-api-reference.md)、[Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-reference-to-video-api-reference.md)。
- **视频编辑（video-editing）**：基于原视频做局部重绘 / 扩展 / 风格化。包含 [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)、[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md)、[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)。
- **数字人 / 人像驱动**：把静态图像或音频驱动成可动视频。包含 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-animate-move-api.md)（图生动作）、[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md)（语音驱动数字人）、[万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-animate-mix-api.md)、[图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/animateanyone-quick-start.md)、[图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/emo-quick-start.md)、[图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/liveportrait-quick-start.md)、[图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/emoji-quick-start.md)、[视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/videoretalk.md)。
- **历史版本（万相 2.1–2.6，仅维护，不再新增能力）**：[万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-api-reference.md)、[万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)、[万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md)、[万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-text-to-video-api-reference.md)、[万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)。

> **注意**：新业务请直接使用万相 2.7 / HappyHorse / 爱诗 / Vidu / 可灵 的当前版本 API；`legacy-video-models/` 目录下的接口仅供老业务兼容，参数与字段定义已与新版本分叉，**不要混用**。

## 统一调用范式

所有视频生成模型在百炼上都遵循"提交任务 → 查询结果"的两阶段异步范式：

1. **提交任务**：`POST {endpoint}/api/v1/services/aigc/video-generation/video-synthesis`（或具体模型对应的路径），请求 header 必须带 `X-DashScope-Async: enable`，响应里拿到 `output.task_id` 和 `output.task_status`（一般为 `PENDING`）。
2. **查询任务**：`GET {endpoint}/api/v1/tasks/{task_id}`，轮询直至 `task_status` 为 `SUCCEEDED`（成功，`output.video_url` 可下载）/ `FAILED`（失败，`output.message` 含错误信息）/ `CANCELED`。
3. **下载视频**：`SUCCEEDED` 时 `output.video_url` 默认有效期 24 小时，请尽快转存到自有 OSS / 本地。

不同地域使用不同 Endpoint，需保证**模型、Endpoint URL 与 API Key 属于同一地域**，跨地域调用会失败。常见地域：

- 华北2（北京）：`https://dashscope.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

> **注意**：新加坡旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，国际站调用必须迁到新版 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，并在路径里显式带上 `WorkspaceId`。

## 关键请求字段

各家模型的请求体在外层结构上是一致的，差异主要集中在 `parameters`：

| 字段 | 位置 | 说明 |
| --- | --- | --- |
| `model` | top-level | 模型 ID，如 `wanx2.7-t2v-plus`、`happyhorse-text2video`、`pixverse-t2v` 等，必须与 Endpoint 同地域可见。 |
| `input.prompt` | input | 文本提示词，描述画面内容、运镜、风格。多数模型支持中英文混合，建议不超过 800 字符。 |
| `input.negative_prompt` | input | 反向提示词（部分模型支持）。 |
| `input.img_url` / `input.first_frame_url` / `input.last_frame_url` | input | 图生视频 / 首尾帧生视频用的图片公网 URL，支持 jpg/png/webp。 |
| `input.ref_images_url` | input | 参考生视频用的多张参考图。 |
| `input.video_url` | input | 视频编辑 / 风格重绘的源视频 URL。 |
| `parameters.size` / `resolution` | parameters | 输出分辨率，如 `1280*720`、`720*1280`、`1920*1080`，各模型支持的档位不同。 |
| `parameters.duration` | parameters | 生成时长（秒），常见档位 5s / 10s。万相系列默认 5s。 |
| `parameters.seed` | parameters | 随机种子，相同输入 + seed 可获得可复现的结果。 |
| `parameters.prompt_extend` | parameters | 是否开启自动提示词增强（万相系列），默认 `true`。 |
| `parameters.fps` | parameters | 输出帧率，部分模型支持 16 / 24 / 30。 |

## 调用方式

百炼视频生成接口提供以下几种调用方式：

- **HTTP REST**：见各篇 API 参考中的"HTTP调用"章节，可用任意语言通过标准 HTTP 客户端调用。
- **DashScope Python / Java SDK**：封装了任务提交、轮询、回调等模板逻辑，推荐生产使用。
- **OpenAI 兼容协议**：部分文生视频模型可通过百炼的 OpenAI 兼容端点调用，便于从其他平台迁移。

## 限制与注意事项

- **任务耗时**：单条视频生成通常 1–5 分钟，长视频 / 高分辨率可能达 10 分钟。客户端轮询间隔建议 ≥ 5s，避免触发限流。
- **配额与限流**：各模型按地域有独立的 QPS / 并发 / 月配额，超出会返回 `Throttling.RateQuota` 错误。需要更高配额请通过工单申请。
- **视频 URL 时效**：`output.video_url` 默认 **24 小时**有效，必须及时下载或转存到自己的对象存储。
- **图片 / 视频输入限制**：图片建议长宽 ≥ 360px、≤ 5MB；输入视频时长一般 ≤ 30s、分辨率 ≤ 1080p，具体见各模型文档（不同厂家差异较大，如可灵和 Vidu 的限制与万相不同）。
- **内容安全**：提交的提示词、图片、视频均会过 NSFW / 风险审核，命中后任务直接 `FAILED` 并返回 `DataInspectionFailed`。
- **计费**：按"生成成功的秒数 × 模型档位单价"扣费，`FAILED` 任务不扣费；具体单价以[模型广场](https://bailian.console.aliyun.com/?tab=model)展示为准。

> **注意**：以上"统一调用范式"与"关键字段"是对各家厂商接口的归纳——具体每个模型的字段名、必填项、可选值范围可能存在差异（例如可灵、Vidu 的部分字段名与万相不一致），**对接前请以对应模型的 API 参考为准**，本主题页只用于快速建立心智模型。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/emoji-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)




