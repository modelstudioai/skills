# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动、人像动画及风格重绘等场景。所有接口均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **通用视频生成模型**：  
  - `HappyHorse` 系列（[HappyHorse-文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频、参考生视频、视频编辑）；  
  - `万相`（WanX）系列：`万相3.0`（All-in-One，统一支持文生/图生/参考生/编辑）、`万相2.7`（新版协议，推荐使用）、`万相2.1–2.6`（旧版协议，已逐步淘汰）；  
  - `爱诗`（PixVerse）系列（[爱诗-文生视频](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)、图生视频、参考生视频、动作模仿、对口型等）。

- **人像驱动与动画模型**：  
  - `数字人`（wan2.2-s2v）、`AnimateAnyone`（舞动人像）、`EMO`（悦动人像）、`LivePortrait`（灵动人像）、`VideoRetalk`（声动人像）、`Emoji`（表情包）等，均需先通过图像检测（如 `emo-detect-v1`、`liveportrait-detect`）再生成视频；  
  - `视频风格重绘`（[video-style-transform](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)）支持 8 种预设艺术风格。

- **专用功能模型**：  
  - `万相-视频换人`（wan2.2-animate-mix）、`万相-图生动作`（wan2.2-animate-move）、`爱诗-视频动作模仿`（pixverse-motioncontrol）等，聚焦特定迁移任务。

> **注意**：文档中存在协议不一致问题——`万相2.1–2.6` 早期模型（如 `legacy-image-to-video-api-reference.md`）部分使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而 `万相2.7+` 及 `HappyHorse`、`PixVerse` 全部统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。实际调用请以模型文档中标注的 `model` 名称和对应路径为准，避免混用。

## 关键参数

所有 HTTP 请求必须包含以下请求头：
- `Content-Type: application/json`  
- `Authorization: Bearer <API_KEY>`  
- `X-DashScope-Async: enable`（**强制要求**，缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：
- `model`: 字符串，**必选**，指定模型名称（如 `"wan3"`、`"pixverse/pixverse-v6-t2v"`、`"emo-v1"`）。不同模型取值差异大，须严格按文档选择；
- `input`: 对象，**必选**，结构因模型而异：
  - 文生视频：`{"prompt": "..."}`；
  - 图生视频：`{"img_url": "...", "prompt": "..."}`；
  - 数字人/EMO/LivePortrait：`{"image_url": "...", "audio_url": "..."}`；
  - 视频风格重绘：`{"video_url": "...", "parameters": {"style": 0}}`；
  - 动作模仿（PixVerse）：`{"media": [{"type": "image_url", "url": "..."}, {"type": "video_url", "url": "..."}]}`；
- `parameters`: 对象，可选，用于控制分辨率、帧率、风格等（如 `"resolution": "720P"`、`"style": 4`（国风卡通））。

## 使用方式

1. **准备环境**：  
   - 在阿里云百炼控制台开通对应模型服务；  
   - 获取并配置**同地域**的 API Key（[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
   - 替换 Endpoint 中的 `{WorkspaceId}` 为业务空间 ID（[查看 WorkspaceId](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）。

2. **发起异步任务**：  
   ```bash
   curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer sk-xxx' \
     -H 'X-DashScope-Async: enable' \
     -d '{
           "model": "wan3",
           "input": {"prompt": "一只橘猫在秋日公园奔跑"},
           "parameters": {"resolution": "720P"}
         }'
   ```
   成功响应返回 `task_id`（字符串），有效期 24 小时。

3. **轮询获取结果**：  
   使用 `GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，`status` 为 `"SUCCESS"` 时，`output.video_url` 即为生成视频直链。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint URL 必须同属一个地域（如华北2北京），跨地域调用必然失败。  
- **任务幂等性**：禁止重复提交相同请求创建任务，应复用 `task_id` 轮询，而非重发创建请求。  
- **输入合规性**：多数人像类模型（EMO、LivePortrait、AnimateAnyone、Emoji）**必须前置图像检测**（如 `emo-detect-v1`），否则生成失败或效果异常；检测通过后需将返回的 `face_bbox`、`ext_bbox` 等坐标传入生成请求。  
- **URL 访问限制**：所有 `img_url`/`video_url`/`audio_url` 必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 [临时文件上传 API](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 获取有效 URL。  
- **旧模型停用提示**：`万相2.1–2.6` 系列（如 `legacy-wan-text-to-video-api-reference.md`）已明确标注“推荐优先选用万相2.7”，且其部分 endpoint 路径（`/image2video/...`）与新版不兼容，新项目应避免使用。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)


