# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等场景。所有视频生成 API 均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，任务 ID 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **通用视频生成模型**：  
  - `HappyHorse` 系列（[HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)）：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务；  
  - `万相`（WanX）系列（[万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)）：覆盖全栈能力，其中 `wan3.0` 为 All-in-One 统一模型，支持文生、图生（首帧/首尾帧）、参考生视频；`wan2.7` 各子模型（如 `wan2.7-videoedit`）已明确区分协议与能力边界；早期 `wan2.1–2.6` 模型（[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)）功能受限且已不推荐使用。  
- **人像驱动与数字人模型**：  
  - `AnimateAnyone`、`EMO`、`LivePortrait`、`VideoRetalk`、`Emoji` 等（[人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)）：均需先调用图像检测 API（如 `emo-detect-v1`），再生成视频，流程强耦合；  
  - `wan2.2-s2v`（[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)）：依赖 `wan2.2-s2v-detect` 预检，仅支持北京地域。  
- **垂直场景模型**：  
  - `爱诗`（PixVerse）（[爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)）：提供文生、图生（首帧/首尾帧）、参考生视频、对口型（`pixverse-lipsync`）、动作模仿、超清增强等细分能力；  
  - `视频风格重绘`（[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)）：支持 8 种预设艺术风格转换，输入为视频，输出为同构风格化视频。

> **注意**：`万相2.7-图生视频`（[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)）明确声明支持“首帧生视频、首尾帧生视频、视频续写”三大任务，而 `万相-首尾帧生视频API参考（2.2）`（文档15）所用 endpoint 为 `/api/v1/services/aigc/image2video/video-synthesis`（非 `/video-generation/`），路径不一致且模型版本过旧，**实际开发中应以 wan2.7 及以上新版协议为准，避免混用旧路径**。

## 关键参数

所有视频生成 API 的核心请求参数结构高度统一，关键字段如下：

- **请求头（Headers）**（必选）：  
  - `Content-Type: application/json`；  
  - `Authorization: Bearer <API_KEY>`；  
  - `X-DashScope-Async: enable` —— **此头在绝大多数视频 API 中为强制要求**（如 [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)、[EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)、[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md) 均明确强调缺失将报错 `"current user api does not support synchronous calls"`）；  
- **请求体（Request Body）**（必选）：  
  - `model`: 字符串，具体模型名（如 `"wan2.7-videoedit"`、`"pixverse/pixverse-v6-t2v"`、`"emoji-v1"`），不同模型取值严格固定；  
  - `input`: 对象，内容依模型而异：  
    - 文生视频：含 `prompt`（文本提示词）；  
    - 图生/参考生视频：含 `image_url` 或 `video_url`、`prompt`；  
    - 数字人/口型替换：含 `image_url` + `audio_url` 或 `video_url` + `audio_url`；  
    - 表情包：含 `image_url`、`face_bbox`、`ext_bbox`（来自检测 API 输出）及 `driven_id`（模板 ID）；  
  - `parameters`: 对象（可选），用于控制生成细节（如 `video-style-transform` 的 `style` 参数指定 0–7 风格类型）。

## 使用方式

1. **环境准备**：  
   - 在阿里云百炼控制台开通对应模型服务；  
   - 获取并配置**与模型同地域**的 API Key（[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）；  
   - 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`（[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md) 等多份文档强调其性能与稳定性优势）。  

2. **异步调用流程**：  
   - **步骤1：创建任务**  
     发送 `POST` 请求至对应 endpoint（如北京地域：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`），携带上述 Headers 和 Body，获得 `task_id`；  
   - **步骤2：轮询结果**  
     使用 `task_id` 定期调用 `GET /api/v1/tasks/{task_id}`（具体路径见各模型文档）查询状态，直至返回 `"status": "SUCCESS"` 并附带 `output.video_url`。  

3. **特殊前置步骤（人像类模型）**：  
   - `AnimateAnyone`、`EMO`、`LivePortrait`、`Emoji`、`wan2.2-s2v` 等均需**先调用图像检测 API**（如 `emo-detect-v1`），传入 `image_url`，获取 `face_bbox` 和 `ext_bbox` 后，再在视频生成请求的 `input` 中复用这些坐标值。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（北京、新加坡、东京等），跨地域调用必然失败（[HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md) 等均反复强调）；  
- **URL 协议差异**：多数模型使用 `/api/v1/services/aigc/video-generation/video-synthesis`，但部分旧模型或特定功能使用 `/image2video/` 路径（如 `wan2.2-s2v`、`AnimateAnyone`、`VideoRetalk`），务必核对文档；  
- **文件上传要求**：所有媒体资源（图片、视频、音频）必须提供公网可访问的 HTTP/HTTPS URL；本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) API 转换；  
- **计费与限流**：  
  - 多数模型按秒/张/次计费（如 `wan2.2-s2v` 480P 0.5元/秒，`emoji-detect-v1` 0.004元/张）；  
  - 免费额度有限（通常 200 张检测或 1800 秒生成），用尽后自动转为后付费；  
  - QPS/RPS 限制严格（常见为 1–5），高并发需申请提升配额；  
- **输入合规性**：人像类模型对输入图像质量要求极高（正面、单人、无遮挡、光照充足），检测不通过仍计费（[EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md) 明确说明）；  
- **任务时效性**：`task_id` 有效期统一为 24 小时，超时需重新提交任务。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)


