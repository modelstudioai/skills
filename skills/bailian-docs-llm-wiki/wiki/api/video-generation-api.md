# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频、参考生视频、视频编辑、人像驱动、风格重绘等核心场景。所有视频类 API 均采用异步调用模式（创建任务 → 轮询结果），任务耗时通常为 1–5 分钟，`task_id` 有效期为 24 小时。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

平台当前提供三大主力视频生成系列，以及多类垂直人像驱动与后处理模型：

- **HappyHorse 系列**：支持文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类任务，强调物理真实感与运动流畅性 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）系列**：
  - `wan3.0` 为全能 All-in-One 模型，统一支持文生、图生（首帧/首尾帧）、参考生视频，最长生成 30 秒、30fps 视频 [万相3.0-视频生成](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；
  - `wan2.7` 为新版协议模型，各子任务（文生、图生、参考生、视频编辑）均独立优化，推荐优先选用；而 `wan2.1–2.6` 为早期版本，功能受限且部分接口路径不同（如首尾帧生视频使用 `/image2video/video-synthesis`）[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **爱诗（PixVerse）系列**：提供文生、图生（首帧/首尾帧）、参考生、对口型、动作模仿、超清等细分能力，支持多版本模型选型（如 `c1` 适配高速动态，`v6` 为通用推荐）[爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **人像驱动类**：包括 EMO（唱演）、LivePortrait（播报）、AnimateAnyone（舞蹈）、VideoRetalk（口型替换）、Emoji（表情包）等，均需先通过对应图像检测 API 验证输入合规性 [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)。
- **后处理类**：视频风格重绘（8 种预设艺术风格）、视频超清（输出 4K）等。

> **注意**：万相 `wan2.7-图生视频`（文档8）明确声明其新版协议仅支持 `wan2.7` 模型，而 `wan2.6` 及更早版本（文档11–15）使用旧版协议及部分不同路径（如文档15中首尾帧生视频使用 `/image2video/video-synthesis`），二者不兼容。开发者应根据实际选用模型版本严格匹配对应文档。

## 关键参数

所有视频生成 API 的通用关键参数如下：

- **请求头（Headers）**
  - `Content-Type`: 必须为 `application/json`
  - `Authorization`: 格式为 `Bearer <API_KEY>`，需与模型所在地域匹配
  - `X-DashScope-Async`: 必须设置为 `enable`，否则报错 “current user api does not [support](../guides/support.md) synchronous calls”

- **请求体（Request Body）**
  - `model`: 字符串，必需。具体值依模型而定（如 `wan2.7-videoedit`, `pixverse/pixverse-v6-t2v`, `emo-v1`）
  - `input`: 对象，必需。结构因任务类型差异显著：
    - 文生视频：含 `prompt`（文本提示词，长度限制依模型而异，如 wan2.7 限 5000 字符）
    - 图生/参考生视频：含 `img_url` 或 `media` 数组（含 `image_url`/`video_url`/`audio_url` 等）
    - 人像驱动类（EMO/LivePortrait/AnimateAnyone）：需传入经检测 API 返回的 `face_bbox` 和 `ext_bbox` 坐标
    - 视频风格重绘：含 `video_url` 和 `parameters.style`（0–7 整数）
  - `parameters`: 对象，可选。常见字段包括 `resolution`（如 `"720P"`）、`style_level`（EMO 动作风格）、`video_fps`（帧率）等

## 使用方式

标准异步流程分为两步：

1. **创建任务**：向对应地域的 Endpoint 发送 `POST` 请求。
   - 统一路径（绝大多数模型）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`
     - `{WorkspaceId}` 为业务空间 ID，可在控制台查看；
     - `{region}` 如 `cn-beijing`、`ap-southeast-1` 等；
     - **例外**：万相 `wan2.2-首尾帧生视频`（文档15）和部分人像驱动模型（如 `animate-anyone-gen2`, `emo-v1`, `videoretalk`）使用 `/image2video/video-synthesis` 路径；`animate-anyone-detect-gen2` 使用 `/aa-detect`（文档21）；`emo-detect-v1` 使用 `/face-detect`（文档25）。
   - 成功响应返回 `task_id`，用于后续轮询。

2. **轮询获取结果**：使用 `task_id` 调用查询接口（具体路径见各模型文档），直至 `status` 为 `SUCCESS`，响应中 `output.video_url` 即为生成视频地址。

> **注意**：所有文档均强调“请勿重复创建任务”，`task_id` 有效期为 24 小时，应复用该 ID 进行轮询。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），混用将导致鉴权失败或服务报错。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已成主流推荐，旧域名（如 `dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **输入合规性**：人像驱动类模型（EMO、LivePortrait、AnimateAnyone、Emoji）**必须前置调用对应图像检测 API**（如 `emo-detect-v1`, `liveportrait-detect`），并使用其返回的 `face_bbox`/`ext_bbox` 坐标作为视频生成 API 的入参，否则生成效果不可控或失败。
- **文件要求**：所有媒体资源（图片、视频、音频）必须为公网可访问的 HTTP/HTTPS URL；本地文件需先调用 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口转换。
- **计费与限流**：各模型有独立的免费额度、单价及并发限制（如 `emo-v1` 同时处理中任务数为 1），详情需查阅对应资费文档；部分模型（如 VideoRetalk）在使用 OSS 临时 URL 时，请求头需额外添加 `X-DashScope-OssResourceResolve: enable`。
- **模板与特效**：万相早期模型（2.1–2.6）支持视频特效（如 `flying`, `hanfu-1`），需通过 `template` 参数指定，且 `prompt` 字段将被忽略 [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)。

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
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [AnimateAnyone 图像检测API参考](../../raw/_short/animate-anyone-detect-api-55e09ae4e0a18b6e.md)
- [AnimateAnyone动作模板生成API参考](../../raw/_short/animate-anyone-template-api-e8864f515e08488f.md)
- [AnimateAnyone 视频生成API参考](../../raw/_short/animateanyone-video-generation-api-5a2827f4de69f8c0.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait 视频生成API参考](../../raw/_short/liveportrait-api-aed61e9b5a74b8a5.md)
- [LivePortrait图像检测API参考](../../raw/_short/liveportrait-detect-api-21701ab5bd145794.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)


