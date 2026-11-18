# video generation api

百炼平台提供多种视频生成模型的 API 接口，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、动作迁移、口型同步、风格重绘、超分增强等核心能力。所有视频生成任务均采用异步调用模式，需通过“创建任务 → 轮询获取结果”两步完成。开发者需确保模型、Endpoint URL 与 API Key 严格处于同一地域，跨地域调用将失败。

## 支持的模型/功能

当前平台提供四大主力视频生成模型系列，覆盖不同场景与精度需求：

- **HappyHorse**：提供文生视频、图生视频（基于首帧）、参考生视频、视频编辑四类能力，强调物理真实性和运动流畅性 [HappyHorse (raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)。
- **万相（WanX）**：功能最全的多模态视频模型家族，包含：
  - 全能型 `wan3.0`（统一接口支持文/图/参考生视频，最长30秒，30fps）；
  - 迭代型 `wan2.7`（新版协议，支持图生视频、文生视频、参考生视频、视频编辑）；
  - 专用型（如 `wan2.2-animate-move` 动作迁移、`wan2.2-animate-mix` 视频换人、`wan2.2-s2v` 数字人驱动）；
  - 早期模型（2.1–2.6）已标记为 Legacy，[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md) 明确建议优先选用 wan2.7 或 wan3.0。
- **爱诗（PixVerse）**：专注高质量动态表现，提供文生视频、首帧/首尾帧/参考生视频、对口型、动作模仿、视频超清等细分能力，各模型按场景优化（如 `c1` 系列专攻打斗/法术特效）。
- **可灵（Kling）与 Vidu**：分别提供 `kling-v4-omni-reference-video-generation` 和 `viduq3-drama_reference2video` 等高一致性角色视频生成能力；Vidu 同时支持广告级智能运镜（`viduq3-ad`）与国风等垂直风格。

> **注意**：部分模型存在路径不一致问题。例如，`万相-首尾帧生视频API参考（2.2）`（文档16）使用 `/api/v1/services/aigc/image2video/video-synthesis` 路径，而其他主流模型（包括 wan2.7、wan3.0、HappyHorse、PixVerse 等）均统一使用 `/api/v1/services/aigc/video-generation/video-synthesis`。该差异表明文档16为历史遗留接口，新开发应避免使用。

## 关键参数

所有视频生成 API 均需以下通用请求头（Headers）：

- `Content-Type: application/json`（必选）
- `Authorization: Bearer <API_KEY>`（必选，除部分仅限北京地域的模型外）
- `X-DashScope-Async: enable`（**必选**，缺失将报错 `"current user api does not support synchronous calls"`）

请求体（Request Body）核心字段：

- `model`（字符串，必选）：具体模型标识符，如 `wan3.0-video-generation`、`pixverse/pixverse-v6-max-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v4-omni-reference-video-generation`。
- `input`（对象，必选）：根据模型类型结构化输入：
  - 文生视频：`{ "prompt": "..." }`
  - 图生视频（首帧）：`{ "img_url": "...", "prompt": "..." }`
  - 首尾帧：`{ "first_frame_url": "...", "last_frame_url": "...", "prompt": "..." }`
  - 参考生视频：`{ "reference_urls": ["..."], "prompt": "..." }`
  - 对口型：`{ "media": [{ "type": "video_url", "url": "..." }, { "type": "audio_url", "url": "..." }] }`
- `parameters`（对象，可选）：控制输出规格，常见参数包括：
  - `resolution`（如 `"720P"`, `"1080P"`, `"4k"`）
  - `aspect_ratio`（如 `"16:9"`, `"9:16"`, `"1:1"`）
  - `style`（风格重绘专用，整数 0–7）
  - `video_fps`（帧率，默认15–25）

## 使用方式

1. **开通服务与配置环境**：在百炼控制台开通对应模型，获取并配置**同地域**的 API Key 到环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求 URL**：使用业务空间专属域名（推荐）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`，其中 `{WorkspaceId}` 为控制台业务空间详情页所见 ID，`{region}` 如 `cn-beijing`、`ap-southeast-1`。
3. **发起异步任务**：`POST` 请求提交任务，成功后获得 `task_id`（有效期24小时）。
4. **轮询获取结果**：使用 `GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，直至返回 `"status": "SUCCESS"` 并附带 `output.video_url`。

> **注意**：`视频风格重绘API参考`（文档40）示例中仍使用旧域名 `https://dashscope.aliyuncs.com`，而其余44篇文档（如 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、[万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)）均明确推荐并给出专属域名格式。新项目必须使用专属域名以保障性能与稳定性。

## 限制和注意事项

- **地域强绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2北京），混用将导致鉴权失败或服务报错，此要求在所有模型文档中反复强调。
- **异步强制性**：所有视频 API 仅支持异步，`X-DashScope-Async: enable` 为硬性要求；同步调用会直接报错。
- **输入资源要求**：
  - 图片：支持 JPG/JPEG/PNG/BMP/WEBP，宽高 400–7000 像素，需公网可访问 URL。
  - 视频：MP4/AVI/MOV 等，时长通常 2–120 秒，大小 ≤300MB，需清晰正面人物镜头（如 VideoRetalk）。
  - 音频：WAV/MP3/AAC，时长 2–120 秒，需纯净人声（无背景音乐/噪音）。
- **任务管理**：`task_id` 有效期严格为 24 小时，过期无法查询；禁止重复创建相同任务，应复用已有 `task_id` 轮询。
- **模型兼容性**：`万相-图生视频-视频特效列表`（文档14）明确指出，特效模板（如 `flying`, `hanfu-1`）**仅适用于 legacy 模型（2.1–2.6）**，不适用于 wan2.7 或 wan3.0，开发者需按模型版本选择是否启用特效。

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
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)


