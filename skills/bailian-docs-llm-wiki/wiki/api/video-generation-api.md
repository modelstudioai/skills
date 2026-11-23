# video generation api

百炼平台的 Video Generation API 提供多模态视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、对口型、风格重绘等十余种任务类型。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。模型按地域隔离，需严格保证模型、Endpoint URL 与 API Key 同属一个地域。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同精度、时长与场景需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑四类任务。
- **万相（WanX）**：功能最全的通用视频模型家族，含 `wan2.7`（推荐新版协议）、`wan3.0`（All-in-One，统一接口支持文/图/参考生视频，最长30秒）、`wan2.2-s2v`（数字人驱动）、`wan2.2-animate-move`（图生动作）及 `wan2.2-animate-mix`（视频换人）。早期 `wan2.1–2.6` 模型已归档为[legacy-video-models](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)，不建议新项目接入。
- **爱诗（PixVerse）**：强调动态表现力与特效能力，支持文生视频、首帧/首尾帧生视频、参考生视频、视频动作模仿、对口型、超清（4K）及风格化处理。
- **Vidu / 可灵（Kling） / MiniMax**：分别提供高保真文图生成、关键帧灵活组合（支持中间帧）、多模态参考融合等差异化能力。

> **注意**：万相 `wan2.7` 系列与 `wan3.0` 均使用 `/api/v1/services/aigc/video-generation/video-synthesis` 统一路径，但 `wan2.7` 要求 `X-DashScope-Async: enable` 头，而 `wan3.0` 文档未明确要求该头——实际调用中必须显式设置，否则报错“current user api does not [support](../guides/support.md) synchronous calls”，此为文档遗漏，以[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)为准。

## 关键参数

所有视频 API 共享以下核心参数结构：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: Bearer + API Key（部分旧模型如 `wan2.1–2.6` 的 `image2video` 接口在文档中未体现此头，但实测必需）
  - `X-DashScope-Async`: **必须设为 `enable`**，所有视频任务仅支持异步模式，缺失将直接报错。

- **请求体（Request Body）**
  - `model`: 字符串，模型标识符（如 `wan2.7-videoedit`, `pixverse/pixverse-v6-max-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v4-omni-reference-video-generation`）
  - `input`: 对象，内容依模型而异：
    - 文生视频：`{ "prompt": "..." }`
    - 图生视频（首帧）：`{ "img_url": "...", "prompt": "..." }`
    - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`
    - 参考生视频：`{ "reference_images": [...], "prompt": "..." }`
    - 视频编辑/动作模仿：`{ "media": [{ "type": "video_url", "url": "..." }, { "type": "image_url", "url": "..." }] }`
  - `parameters`: 可选对象，用于控制分辨率（如 `"resolution": "720P"`）、帧率、风格（如 `style: 0` for 日式漫画）、音色 ID 等。

## 使用方式

1. **开通服务与配置**：在百炼控制台模型市场开通对应模型（如 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md) 或 [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)），获取所属地域的 API Key，并配置至环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求**：
   - Endpoint URL 格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
   - 替换 `{WorkspaceId}` 为业务空间 ID，`{region}` 为地域代码（如 `cn-beijing`, `ap-southeast-1`）。
3. **发起异步任务**：`POST` 请求提交任务，获取 `task_id`（有效期 24 小时）。
4. **轮询结果**：使用 `task_id` 向 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至 `status` 为 `SUCCESS`，响应中 `output.video_url` 即为生成视频地址。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。新加坡、美国、德国、日本、中国香港等多地已支持，详见各模型文档。
- **异步时效性**：任务平均耗时 1–5 分钟，`task_id` 有效期严格为 24 小时，超时需重提。
- **输入约束**：
  - 图像：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率通常要求 400–7000 像素。
  - 视频：MP4/AVI/MOV 等，时长 ≤30 秒（Vidu/Kling 4.0 最长 30 秒，wan3.0 最长 30 秒，多数模型为 15 秒），大小 ≤100 MB。
  - 音频：WAV/MP3，时长 <20 秒（数字人 s2v），需人声清晰无背景噪音。
- **模型兼容性**：`wan2.1–2.6` 系列部分接口（如 `legacy-image-to-video-by-first-and-last-frame-api-reference.md`）使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，与主流 `/video-generation/` 路径不一致，新项目应优先选用 `wan2.7+` 或 `wan3.0`。
- **计费与限流**：部分模型（如 `videoretalk`）有 RPS 与并发任务数限制（如 RPS=1，同时运行中任务数=1），详见各模型资费说明文档。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)


