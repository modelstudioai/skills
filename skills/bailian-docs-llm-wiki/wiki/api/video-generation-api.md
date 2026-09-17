# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、表情包生成及风格重绘等场景。所有 API 均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

百炼当前提供三大类视频生成模型体系：

- **通用视频生成模型**：  
  - `HappyHorse` 系列（[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频、参考生视频、视频编辑）  
  - `万相`（WanX）系列：包括全能型 `wan3.0`（统一支持文生/图生/参考生），以及 `wan2.7` 各子模型（文生、图生、参考生、视频编辑），并兼容早期 `wan2.1–2.6` 模型（如首尾帧生视频、视频换人、图生动作等）。  
  - `爱诗`（PixVerse）系列：支持文生视频、首帧/首尾帧图生视频、参考生视频、对口型、动作模仿与超清增强等细分能力。

- **人像驱动与数字人模型**：  
  - `数字人 wan2.2-s2v`（需先调用 `wan2.2-s2v-detect` 检测图像合规性）  
  - `AnimateAnyone`（含 detect/template/gen2 三阶段流程）  
  - `EMO`、`LivePortrait`、`VideoRetalk`、`Emoji` 等专注人像动态生成的模型，均要求前置图像检测（如 [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)）  
  - `视频风格重绘`（支持 8 种预设艺术风格）

- **专用功能模型**：  
  - `万相-视频特效`（仅限 legacy 图生视频模型使用，见 [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)）  
  - `万相-图生动作`、`万相-视频换人`（均属 `wan2.2-animate-*` 子系列）

> **注意**：`wan2.7` 及以上版本已统一使用 `/api/v1/services/aigc/video-generation/video-synthesis` 路径；而 `wan2.2-s2v`、`AnimateAnyone`、`EMO`、`LivePortrait`、`VideoRetalk`、`Emoji` 等华北2专属模型仍使用 `/api/v1/services/aigc/image2video/` 路径（如 `face-detect` 或 `video-synthesis`），二者 endpoint 不互通。

## 关键参数

所有 HTTP 请求必须包含以下请求头：
- `Content-Type: application/json`（必选）  
- `Authorization: Bearer <API_KEY>`（必选）  
- `X-DashScope-Async: enable`（**必选**；缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：
- `model`（字符串，必选）：具体模型名，例如 `wan3.0`、`pixverse/pixverse-v6-t2v`、`emo-v1`、`video-style-transform`。不同模型系列命名规则差异显著，需严格按文档指定。
- `input`（对象，必选）：根据模型类型差异较大：
  - 文生视频：`prompt`（文本提示词，长度限制依模型而异，如 wan2.7 最多 5000 字符）
  - 图生/参考生视频：`img_url` 或 `image_url`（首帧图）、`video_url`（参考视频）、`audio_url`（音频）等
  - 数字人/口型替换：`image_url` + `audio_url`（或 `lip_sync_tts_content`）
  - 表情包：`image_url` + `face_bbox` + `ext_bbox`（需由检测 API 返回）
- `parameters`（对象，可选）：常见参数包括 `resolution`（如 `"720P"`）、`style`（风格重绘中取值 0–7）、`video_fps`（帧率，默认 15）、`template`（万相特效模板名，仅 legacy 模型支持）

## 使用方式

1. **环境准备**：  
   - 在阿里云百炼控制台开通对应模型服务（如 [爱诗-文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)）  
   - 获取并配置**同地域**的 API Key（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）  
   - 推荐迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优  

2. **发起异步任务**：  
   ```bash
   curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
     -H "Content-Type: application/json" \
     -H "X-DashScope-Async: enable" \
     -d '{
           "model": "wan3.0",
           "input": {"prompt": "一只橘猫在阳光下伸懒腰"},
           "parameters": {"resolution": "720P"}
         }'
   ```
   成功响应返回 `task_id`（字符串），有效期 24 小时。

3. **轮询获取结果**：  
   使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}`（具体路径依模型而异，部分模型需拼接完整 URL），直至 `status` 为 `"SUCCESS"`，`output.video_url` 即为生成视频地址。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint、API Key 必须同属一个地域（如华北2），混用将直接失败。  
- **异步强制性**：所有视频 API 仅支持异步，同步调用必然报错；`X-DashScope-Async: enable` 为硬性要求。  
- **输入资源要求**：  
  - 图像：格式（JPG/PNG/WEBP 等）、分辨率（通常 400–7000px）、大小（≤10MB）、公网可访问  
  - 视频：格式（MP4/AVI/MOV）、时长（多数 ≤30s）、大小（≤300MB）、帧率（15–60fps）  
  - 音频：格式（WAV/MP3）、时长（1s–3min）、人声清晰无背景噪音  
- **前置检测依赖**：`EMO`、`LivePortrait`、`AnimateAnyone`、`Emoji`、`wan2.2-s2v` 等模型**必须先调用对应 detect API**（如 [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)），并将返回的 `face_bbox` 等坐标作为生成请求入参，否则生成失败。  
- **模型路径差异**：  
  > **注意**：通用视频模型（HappyHorse/WanX/PixVerse）使用 `/video-generation/video-synthesis`；而人像驱动类模型（EMO/LivePortrait/VideoRetalk/Emoji）及数字人 `wan2.2-s2v` 使用 `/image2video/` 下的专用路径（如 `/face-detect` 或 `/video-synthesis`），二者不可混用。  
- **计费与限流**：各模型单价、免费额度、QPS/RPS 限制差异大（如 `emo-v1` 0.08元/秒，`wan2.2-s2v` 720P 0.9元/秒），详见各模型价格说明文档。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


