# video generation api

百炼平台提供多种视频生成能力，覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人驱动、风格重绘等核心场景。所有视频生成 API 均采用异步调用模式，任务创建后需轮询获取结果，典型耗时为 1–5 分钟。开发者需确保模型、Endpoint URL 与 API Key 严格属于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **HappyHorse 系列**：专注高质量物理真实感视频生成，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[图生视频-基于首帧](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)、[参考生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)和[视频编辑](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)四类任务。
- **万相（WanX）系列**：提供 All-in-One 能力，万相3.0统一支持文生、图生（首帧/首尾帧）、参考生及视频编辑；万相2.7为新版协议，推荐优先选用；早期版本（2.1–2.6）已逐步归档，详见[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)。
- **爱诗（PixVerse）系列**：面向创意内容生成，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频对口型、动作模仿及超清增强等细分能力，详见[爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。

此外，**人像驱动类模型**（如 EMO、LivePortrait、VideoRetalk、AnimateAnyone、Emoji）聚焦于肖像级动态生成，均要求输入合规人像图片（需先通过对应检测模型），且全部限定在华北2（北京）地域使用。数字人 wan2.2-s2v 也属此类，其流程需先调用 `wan2.2-s2v-detect` 检测再提交生成任务。

> **注意**：部分文档存在路径不一致问题。例如，[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md) 和 [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md) 使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而其他主流视频生成模型（如 HappyHorse、万相3.0、爱诗）均使用 `/api/v1/services/aigc/video-generation/video-synthesis`。该差异非错误，而是功能域划分所致（`image2video` 专用于人像驱动类任务），但开发者需按模型类型严格匹配 endpoint。

## 关键参数

所有 HTTP 请求必须包含以下请求头：

- `Content-Type: application/json`
- `Authorization: Bearer <your_api_key>`
- `X-DashScope-Async: enable`（**必需**，缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）中必选字段为：

- `model`: 字符串，具体模型名（如 `happyhorse-t2v`, `wan3`, `pixverse/pixverse-v6-t2v`, `emo-v1`, `video-style-transform`）
- `input`: 对象，结构因模型而异：
  - 文生视频：`{"prompt": "..."}`（支持中英文，长度限制依模型而定，如 wan2.7-videoedit ≤5000 字符）
  - 图生视频：`{"img_url": "https://...", "prompt": "..."}`（首帧）或 `{"first_frame_url": "...", "last_frame_url": "...", "prompt": "..."}`（首尾帧）
  - 参考生视频：`{"reference_urls": ["https://...", "..."], "prompt": "..."}`（多图/视频）
  - 数字人/EMO/LivePortrait：`{"image_url": "...", "audio_url": "..."}`（音频需清晰人声，时长通常 <20s）
  - 视频风格重绘：`{"video_url": "...", "parameters": {"style": 0}}`（`style` 为 0–7 的整数）

部分模型支持可选参数 `negative_prompt`（反向提示词）和 `parameters.resolution`（如 `"720P"`），具体以各模型文档为准。

## 使用方式

视频生成 API 采用标准异步两步流程：

1. **创建任务**：`POST {workspace_url}/api/v1/services/aigc/.../video-synthesis`  
   成功响应返回 JSON，含 `task_id`（有效期 24 小时）。示例（北京地域）：
   ```bash
   curl -X POST "https://your-workspace-id.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
     -H "Authorization: Bearer sk-xxx" \
     -H "X-DashScope-Async: enable" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "happyhorse-t2v",
           "input": {"prompt": "a cat dancing on the moon"},
           "parameters": {"resolution": "720P"}
         }'
   ```

2. **轮询结果**：使用 `task_id` 查询任务状态，直至 `status` 为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频地址。轮询间隔建议 ≥3 秒。

> **注意**：所有模型均**禁止重复创建相同任务**。若需重试，请使用原 `task_id` 轮询，而非新建请求。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL 与 API Key 必须同属一个地域（如华北2、新加坡、美国弗吉尼亚等），否则鉴权失败。业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已取代旧版 `dashscope.aliyuncs.com`，[强烈建议迁移](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。
- **输入合规性**：人像驱动类模型（EMO、LivePortrait、VideoRetalk 等）**必须**先调用对应检测 API（如 `emo-detect-v1`）验证图片/视频，否则生成失败。检测本身计费，且不通过仍扣费。
- **文件要求**：所有媒体资源（图片、视频、音频）必须为公网可访问的 HTTP/HTTPS URL；本地文件需先调用[临时文件上传 API](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)获取 URL。
- **时效性**：`task_id` 有效期为 24 小时，超时需重新提交任务；生成视频 URL 通常有短期有效期（具体由模型决定，未在文档中统一说明）。
- **错误处理**：常见错误包括 `X-DashScope-Async` 缺失、`model` 名称错误、跨地域调用、输入 URL 不可访问或格式不符。详细状态码请查阅各模型文档。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
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
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


