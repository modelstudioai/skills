# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、视频对口型、动作模仿、风格重绘、超分等多种能力。所有视频生成任务均为异步执行，需通过“创建任务 → 轮询查询”两步完成，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域。

## 支持的模型/功能

当前主流视频生成模型按能力矩阵可分为三类：

- **全能型统一模型**：  
  `wan3.0`（万相3.0）支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长生成 30 秒、30fps 视频；`kling/kling-v3-omni-video-generation` 同样覆盖全部五种模式（文生、首帧、首尾帧、参考生、编辑），输出支持 720P/1080P/4K 及多宽高比（16:9/9:16/1:1）[万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。

- **垂直场景专用模型**：  
  - *数字人驱动*：`wan2.2-s2v`（单图+音频生成说话/唱歌视频）、`videoretalk`（人物视频+音频口型替换）；  
  - *特效增强*：`video-style-transform`（8种艺术风格重绘）、`pixverse/pixverse-upscale`（4K超分）、`wanx-video-effects`（预设模板特效，仅限 legacy 2.1–2.6 首帧/首尾帧模型）；  
  - *动作迁移*：`wan2.2-animate-move`（图+视频迁移动作）、`pixverse/pixverse-motioncontrol`（同功能，PixVerse 实现）。

- **多模态参考生成模型**：  
  `pixverse/pixverse-v6-r2v-omni`（支持图片+视频混合参考）、`vidu/viduq3-ad_reference2video`（广告专用，支持商品图直出广告视频）、`MiniMax/MiniMax-H3`（支持首帧/尾帧/首尾帧/多模态参考组合输入）。

> **注意**：万相系列存在明显版本演进断层。`wan2.7` 及 `wan3.0` 为新版协议，统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径；而早期 `wan2.1–2.6` 模型中，部分（如 `wan2.2` 首尾帧）仍使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径 [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)，调用时需严格核对文档路径，避免 404 错误。

## 关键参数

所有视频生成 API 均需以下**必选请求头**：
- `Content-Type: application/json`
- `Authorization: Bearer <your_api_key>`
- `X-DashScope-Async: enable`（缺失将报错 `"current user api does not support synchronous calls"`）

**核心请求体字段**：
- `model`（`string`，必选）：精确指定模型名称，不同模型可选值差异大（如 `vidu/viduq3-pro_text2video` vs `pixverse/pixverse-c1-t2v`），须从对应文档查阅。
- `input`（`object`，必选）：结构因模型而异：
  - 文生视频：仅需 `prompt`（文本提示词，Vidu 限 5000 字符，MiniMax 限 7000 字符）；
  - 图生视频：需 `img_url`（首帧）或 `first_frame` + `last_frame`（首尾帧）；
  - 参考生视频：需 `media` 数组，含 `image_url`/`video_url` 元素；
  - 数字人/对口型：需 `image_url` + `audio_url` 或 `lip_sync_tts_content`。
- `parameters`（`object`，可选）：常见字段包括 `resolution`（如 `"720P"`）、`style`（风格重绘索引 0–7）、`video_fps`（15–25）、`animate_emotion`（布尔值）等。

## 使用方式

1. **准备环境**：  
   - 在百炼控制台开通目标模型服务；  
   - 获取对应地域的 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`；  
   - 获取业务空间 ID（WorkspaceId），用于构造 Endpoint URL。

2. **构造请求**：  
   - 使用业务空间专属域名（推荐）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`；  
     > **注意**：旧版通用域名 `https://dashscope.aliyuncs.com` 仍可用，但华北2（北京）和新加坡地域已明确建议迁移至专属域名以获得更高稳定性 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

3. **发起异步调用**：  
   - `POST` 创建任务，获取 `task_id`（24 小时有效）；  
   - 使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 轮询状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为结果视频地址。

4. **错误处理**：  
   - `task_id` 重复提交将被拒绝（文档多次强调“请勿重复创建任务”）；  
   - 地域不一致导致鉴权失败或 `UNKNOWN` 状态；  
   - 缺失 `X-DashScope-Async` 头直接返回同步调用不支持错误。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败，且部分模型（如 `wan2.2-s2v`、`videoretalk`）**仅支持华北2（北京）地域**，无其他地域部署。
- **输入资源要求**：  
  - 图片：格式 JPG/JPEG/PNG/BMP/WEBP，分辨率 400–7000 像素；  
  - 视频：MP4/AVI/MOV 等，时长 ≤30 秒（多数模型），大小 ≤100 MB；  
  - 音频：WAV/MP3，时长 2–120 秒，需人声清晰、无背景噪音。
- **计费与限流**：  
  - 所有模型均按量计费（如 `wan2.2-s2v` 720P 0.9 元/秒，`videoretalk` 0.08 元/秒）；  
  - 免费额度有限（如 `videoretalk` 1800 秒），用尽后自动转后付费；  
  - RPS 与并发任务数受账号级别限制（如 `videoretalk` 同时仅 1 个运行中任务）。
- **模型兼容性**：  
  - `wan2.7+` 和 `kling-v3+` 模型已统一接口路径与参数范式；  
  - `pixverse` 和 `vidu` 系列虽同属文/图/参考生视频，但模型命名规则、参数细节（如 `prompt` 截断长度、`media` 数组结构）互不兼容，不可混用。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
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
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)


