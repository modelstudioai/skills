# video generation api

百炼平台的 Video Generation API 提供多模态视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、口型同步、风格重绘等核心场景。所有模型均采用统一异步调用范式，通过任务 ID 轮询获取结果，适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型系列，覆盖不同精度、速度与专业场景需求：

- **HappyHorse**：专注物理真实感与运动流畅性，提供文生视频、图生视频（基于首帧）、参考生视频和视频编辑四类能力 [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：全栈视频模型家族，包含：
  - 万相3.0（All-in-One）：统一接口支持文生、图生（首帧/首尾帧）、参考生视频，最长30秒、30fps输出；
  - 万相2.7：新版协议，明确区分 `wan2.7-text2video`、`wan2.7-i2v`、`wan2.7-videoedit` 等专用模型；
  - 早期版本（2.1–2.6）：已归档为[legacy-video-models](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)，不推荐新项目使用。
- **爱诗（PixVerse）**：强调动态表现力，支持文生、图生（首帧/首尾帧）、参考生、对口型、动作模仿、超清增强等细分能力 [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)。
- **Vidu / 可灵（Kling） / MiniMax**：各具特色，如 Vidu 强调影视级质感与多角色一致性，可灵支持主体 ID 复用（见[可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)），MiniMax 提供多尾帧输入等扩展能力。

> **注意**：万相2.7系列与万相3.0虽共用同一基础 URL `/api/v1/services/aigc/video-generation/video-synthesis`，但模型名（`model` 字段）和参数语义不兼容。混用将导致 400 错误，务必按文档指定模型名调用。

## 关键参数

所有视频 API 均需以下通用请求头：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，需与模型地域匹配）
- `X-DashScope-Async: enable`（**必选**；缺失将报错 `"current user api does not support synchronous calls"`）

请求体（JSON）核心字段：

- `model`（字符串，必选）：精确模型标识符，如 `wan2.7-text2video`、`vidu/viduq3-pro_text2video`、`pixverse/pixverse-v6-t2v`。不同模型对 `input` 结构要求严格，不可互换。
- `input`（对象，必选）：根据模型类型变化：
  - 文生视频：`{"prompt": "描述文本"}`
  - 图生视频（首帧）：`{"img_url": "https://...", "prompt": "..."}`（部分模型如 WanX 2.7 支持 `first_frame` 数组）
  - 首尾帧：`{"first_frame": "...", "last_frame": "...", "prompt": "..."}`（Vidu/可灵/MiniMax 支持）
  - 参考生视频：`{"reference_images": [...], "prompt": "..."}` 或 `{"reference_videos": [...]}`（PixVerse/Vidu/Kling 支持）
- `parameters`（对象，可选）：控制输出规格，常见字段：
  - `resolution`：`"480P"`/`"720P"`/`"1080P"`/`"4k"`（依模型而定）
  - `aspect_ratio`：`"16:9"`/`"9:16"`/`"1:1"`
  - `style`：风格重绘类模型专用（如 `video-style-transform` 的 `style: 0` 表示日式漫画）

## 使用方式

API 采用标准异步两步流程：

1. **创建任务**：`POST {WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`  
   - 替换 `{WorkspaceId}` 为业务空间 ID（控制台查看），`{region}` 为实际地域（如 `cn-beijing`）。
   - 成功响应含 `task_id`（有效期 24 小时）。
2. **轮询结果**：`GET {WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
   - 建议间隔 ≥5 秒轮询，状态为 `SUCCESS` 时返回 `output.video_url`；`FAILED` 时返回错误原因。

> **注意**：部分模型（如数字人 `wan2.2-s2v`、声动人像 `videoretalk`）使用旧版路径 `/api/v1/services/aigc/image2video/video-synthesis`，且 `videoretalk` 在[VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)中明确要求使用 `https://dashscope.aliyuncs.com` 域名而非 workspace 域名，需特别注意。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint URL、API Key 必须同属一个地域（如华北2北京），跨地域调用必然失败。
- **输入约束**：
  - 图片/视频 URL 必须公网可访问（HTTP/HTTPS），本地文件需先调用[临时URL接口](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)上传。
  - 视频文件大小通常 ≤300MB，时长 ≤120 秒；图片分辨率建议 400×400 至 2048×2048。
  - 提示词长度：Vidu/可灵限 5000 字符，MiniMax 限 7000 字符，万相2.7文生限 5000 字符。
- **计费与配额**：视频生成按秒计费（如 videoretalk 0.08元/秒），免费额度详见各模型文档；RPS 与并发任务数受账号等级限制（如 videoretalk 同时仅 1 个运行中任务）。
- **模型弃用**：万相2.1–2.6、早期 PixVerse/Vidu 版本已标记为 legacy，新项目请优先选用 2.7+ 或 3.0+ 系列。

## 来源文档

- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相](../../raw/model-api-reference/video-generation-api/wan-api-reference.md)
- [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [可灵-主体ID列表](../../raw/_short/kling-object-ids-274408d9d9ebc585.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)


