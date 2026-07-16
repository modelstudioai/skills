# video generation api

阿里云百炼平台提供覆盖多家厂商（万相 Wan、爱诗 PixVerse、Vidu、可灵 Kling、HappyHorse 等）的视频生成 API，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人、人像驱动、视频超清与对口型等能力。所有视频生成任务均通过统一的异步调用模式完成，开发者先提交任务拿到 `task_id`，再轮询查询结果。

## 统一调用模式：异步「创建任务 → 轮询获取」

由于视频生成耗时较长（通常 1-5 分钟，个别统一编辑模型约 5-10 分钟），API 全部采用异步方式，流程分两步：

1. **创建任务**：向 `video-synthesis` 端点发起 `POST` 请求，请求头必须带 `X-DashScope-Async: enable`（缺少会报错 `current user api does not support synchronous calls`），返回一个 `task_id`。
2. **轮询获取**：用 `task_id` 发起 `GET https://<endpoint>/api/v1/tasks/{task_id}` 查询任务状态，直到完成并拿到视频 URL。

其余通用约定：

- `task_id` 有效期为 **24 小时**，过期无法查询（返回状态 `UNKNOWN`）；请勿重复创建任务，轮询即可。
- 请求头 `Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY` 为必填。
- 新手可参考 [Postman 首次调用指引](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。

> **注意**：绝大多数视频生成模型使用端点路径 `/api/v1/services/aigc/video-generation/video-synthesis`，但部分数字人/换人/图生动作类模型（[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)、[万相-图生动作](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)、[万相-视频换人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)、[万相2.2-首尾帧](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)）使用的是 `/api/v1/services/aigc/image2video/video-synthesis`。接入时请以对应文档端点为准。

## 支持的模型与功能

按厂商与任务类型划分，主要能力如下：

- **万相 Wan（2.7 新版协议）**：
  - 文生视频（`wan2.7-t2v-*`），支持通过 `prompt` 自然语言控制单/多镜头。
  - 图生视频（`wan2.7-i2v-*`），支持多模态输入（文本/图像/音频/视频），可完成首帧生视频、首尾帧生视频、视频续写三大任务。
  - 参考生视频（`wan2.7-r2v-*`），多主体参考（图像+视频+音色）。
  - 视频编辑（`wan2.7-videoedit`），指令编辑与视频迁移。
- **万相 Wan（旧版协议，2.1-2.6）**：文生视频、图生视频-基于首帧、参考生视频（`wan2.6-r2v-flash`）、首尾帧生视频（`wan2.2-kf2v-flash`）、视频编辑统一模型（`wanx2.1-vace-plus`，支持多图参考、视频重绘等 `function`）。
- **万相人物/数字人系列**：数字人 `wan2.2-s2v`（图片+音频，需先用 `wan2.2-s2v-detect` 检测图片）、图生动作 `wan2.2-animate-move`、视频换人 `wan2.2-animate-mix`（均含 `wan-std`/`wan-pro` 两种模式）。
- **爱诗 PixVerse**：文生视频、图生视频、首尾帧生视频（`pixverse/pixverse-c1-*`、`-v6-*`、`-v5.6-*`）、参考生视频（`-r2v`）、视频超清（`pixverse/pixverse-upscale`，固定输出 4K）、视频对口型（`pixverse/pixverse-lipsync`，支持音频驱动或 TTS 文本）、视频动作模仿（`pixverse/pixverse-motioncontrol`）。
- **Vidu**：文生视频、图生视频、首尾帧生视频、参考生视频（`vidu/viduq3-*`、`viduq2_*`）。
- **可灵 Kling**：一个模型（`kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`）统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑，并支持智能分镜/多镜头（`multi_shot`、`shot_type`、`multi_prompt`）。
- **HappyHorse**：文生视频、图生视频-基于首帧、参考生视频（多图像）、视频编辑。
- **人像驱动系列（两步调用：先检测后生成）**：舞动人像 AnimateAnyone（图生舞蹈）、悦动人像 EMO（图生唱演，`style_level` 控制风格强度）、灵动人像 LivePortrait（图生播报）、表情包 Emoji（预设模板 `driven_id`）、声动人像 VideoRetalk（口型替换）、视频风格重绘 `video-style-transform`（8 种预设风格）。

## 关键参数

请求体主要由 `model`、`input`、`parameters` 三部分构成：

- `model`：模型名称，决定能力与协议版本。
- `input`：任务输入。文生类用 `prompt`；图生/参考/编辑类多用 `media` 数组（`type` 可为 `image_url`/`first_frame`/`last_frame`/`video_url`/`audio_url`/`reference_image` 等），部分旧版模型用 `image_url`/`video_url`/`audio_url`/`first_frame_url`/`last_frame_url`/`ref_images_url` 等独立字段。
- `parameters`：常见有 `resolution`（如 `480P`/`540P`/`720P`/`1080P`）、`size`（如 `1280*720`）、`duration`（秒）、`watermark`、`prompt_extend`（智能改写）、`audio`、`shot_type`/`multi_shot`（分镜）、`seed`、`style`/`style_level` 等，具体取值随模型不同。

> **注意**：多镜头控制方式在不同模型间不一致。万相 2.7 与 PixVerse-c1 通过 `prompt` 自然语言描述控制，设置 `shot_type` 不生效；而旧版万相 2.6（见 [万相-文生视频（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)）需显式设置 `shot_type: "multi"` 且 `prompt_extend: true` 才能启用多镜头。接入前务必确认所用模型的具体协议。

## 地域与域名

- **必须保证模型、Endpoint URL 与 API Key 属于同一地域**，跨地域调用会失败（鉴权失败或服务报错）。
- 多数第三方模型（PixVerse、Vidu、Kling、数字人等）**仅支持华北2（北京）地域**；万相与 HappyHorse 部分能力还支持新加坡、美国（弗吉尼亚）、德国（法兰克福）等地域。
- 百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，提供更高性能与稳定性，建议迁移：
  - 华北2（北京）：`https://dashscope.aliyuncs.com` → `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://dashscope-intl.aliyuncs.com` → `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
  - `{WorkspaceId}` 为业务空间 ID，可在控制台「业务空间详情」查看；现有域名仍可正常使用。

## 限制与注意事项

- **版本选型**：万相已推出 2.7 新版协议，[万相2.7-图生视频](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md) 支持首帧/首尾帧/续写三大任务，官方推荐优先选用；旧版 wan2.6 及更早模型仅支持首帧生视频。新旧协议接口不通用，`wan2.7-*` 只走新版协议。
- **服务开通**：PixVerse、Vidu、Kling 等第三方模型需先在百炼控制台模型广场搜索并「立即开通」授权后方可调用。
- **两步式模型**：数字人、AnimateAnyone、EMO、LivePortrait、Emoji 等需先调用对应的 `-detect` 检测模型确认图片合规（如清晰度、单人、正面），再调用生成模型。检测模型多为同步调用（如 `wan2.2-s2v-detect` 0.004 元/张）。
- **限流**：视频生成模型通常「同时处理中任务数量」限制较低（多为 1，即同一时刻仅 1 个作业运行，其余排队），任务下发接口 RPS/QPS 约为 5，接入时需做好排队与重试。
- **计费**：多按生成视频时长计费（如 LivePortrait 0.02 元/秒、EMO/VideoRetalk/AnimateAnyone 0.08 元/秒、数字人 720P 0.9 元/秒），`wan-pro` 等专业模式价格高于标准模式。
- VideoRetalk 目前仅支持 API 调用，不支持控制台在线体验。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)


