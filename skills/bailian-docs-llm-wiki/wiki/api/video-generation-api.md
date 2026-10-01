# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑、人像驱动、风格重绘等场景。所有视频生成 API 均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **通用视频生成模型**：  
  - `HappyHorse`：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实性和运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。  
  - `万相3.0`（`wan3`）：All-in-One 模型，统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频，最长输出 30 秒、30fps 视频 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)。  
  - `万相2.7`：新版协议模型，覆盖文生视频、图生视频（多模态输入，支持首帧/首尾帧/视频续写）、参考生视频、视频编辑四大能力，推荐优先选用 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

- **人像驱动与数字人模型**：  
  - `AnimateAnyone`：基于单张人物图 + 动作模板生成舞蹈视频，需配合 `animate-anyone-detect-gen2` 和 `animate-anyone-template-gen2` 使用。  
  - `EMO` / `LivePortrait` / `VideoRetalk` / `Emoji`：均属人像驱动系列，分别面向唱演、播报、口型替换、表情包生成，均要求先通过对应图像检测 API（如 [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)）验证输入合规性。  
  - `wan2.2-s2v`：数字人模型，输入单张图片 + 音频生成说话/唱歌/表演视频。

- **爱诗（PixVerse）系列**：  
  提供细粒度模型选型（如 `c1` 专用于高速动态场景，`v6` 为通用推荐），覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、视频动作模仿、视频超清等能力 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。

> **注意**：万相早期模型（2.1–2.6）已逐步被 2.7 及 3.0 版本替代；文档中明确提示“推荐优先选用”新版协议，旧版接口（如 `wan2.6` 文生视频）仅作兼容保留，不建议新项目接入。

## 关键参数

所有视频生成 API 的核心请求参数结构一致，关键字段如下：

- **必选请求头（Headers）**：  
  `Content-Type: application/json`  
  `Authorization: Bearer <your_api_key>`  
  `X-DashScope-Async: enable` —— **缺失将报错**：“current user api does not [support](../guides/support.md) synchronous calls”。

- **必选请求体（Body）字段**：  
  - `model`: 字符串，指定模型名称（如 `"wan3"`、`"pixverse/pixverse-v6-t2v"`、`"emo-v1"`）。  
  - `input`: 对象，内容依模型而异：  
    - 文生视频：`prompt`（文本提示词，长度限制因模型而异，如 wan2.7 最长 5000 字符）；  
    - 图生视频：`img_url`（首帧图公网 URL）；  
    - 首尾帧生视频：`first_frame_url` + `last_frame_url`；  
    - 参考生视频：`ref_image_urls`（数组）或 `ref_video_url`；  
    - 人像驱动：`image_url` + `audio_url`（或 `lip_sync_tts_content`）；  
    - 视频编辑/风格重绘：`video_url`。  
  - `parameters`（可选）：控制分辨率（如 `"resolution": "720P"`）、帧率、风格类型（如 `video-style-transform` 的 `style: 0` 表示日式漫画）等。

- **地域与业务空间**：  
  所有 Endpoint URL 均含 `{WorkspaceId}` 占位符，需替换为控制台获取的真实业务空间 ID；URL 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（部分旧模型如 `wan2.2-animate-move` 使用 `/image2video/` 路径，见 [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)）。

## 使用方式

1. **前置准备**：  
   - 在百炼控制台开通对应模型服务；  
   - 确认模型、API Key、Endpoint URL 三者地域一致（北京、新加坡、东京等）；  
   - 获取并配置 API Key 到环境变量（`DASHSCOPE_API_KEY`）；  
   - （可选）安装 DashScope SDK 并初始化客户端。

2. **发起异步任务**：  
   ```bash
   curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer sk-xxx' \
     -H 'X-DashScope-Async: enable' \
     -d '{
           "model": "wan3",
           "input": {"prompt": "一只橘猫在阳光下打滚"},
           "parameters": {"resolution": "720P"}
         }'
   ```
   成功响应返回 `{"task_id": "xxx"}`。

3. **轮询获取结果**：  
   使用 `task_id` 调用 `GET /api/v1/tasks/{task_id}`（具体路径见各模型文档），直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。

## 限制和注意事项

- **地域强绑定**：模型、API Key、Endpoint 必须同地域，北京与新加坡的 API Key 不互通，跨地域调用必然失败。  
- **任务生命周期**：`task_id` 有效期为 24 小时，超时后无法查询结果；**禁止重复创建相同任务**，应复用 task_id 轮询。  
- **输入合规性**：人像类模型（EMO/LivePortrait/AnimateAnyone/Emoji）**必须先调用对应图像检测 API**，否则生成质量不可控或失败；检测通过后需将返回的 `face_bbox`、`ext_bbox` 等坐标值传入生成请求。  
- **URL 限制**：所有媒体资源（图/视/音）必须为公网可访问的 HTTP/HTTPS 链接；本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口转换。  
- **路径差异**：多数模型使用 `/video-generation/video-synthesis`，但部分旧模型（如 `wan2.2-s2v`、`AnimateAnyone`、`VideoRetalk`）使用 `/image2video/` 路径，调用时需核对文档。  
- **计费与限流**：各模型独立计费（按秒/张/任务），免费额度有限；QPS/RPS 限制因模型而异（如 `emo-v1` QPS=1），超出将触发限流错误。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
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
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
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
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)


