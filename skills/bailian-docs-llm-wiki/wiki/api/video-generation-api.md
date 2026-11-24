# video generation api

百炼平台的 Video Generation API 提供多模型、多模态的视频生成与编辑能力，支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、对口型、动作模仿、风格重绘、超分等多种任务。所有接口均采用统一异步调用范式（创建任务 → 轮询结果），适用于生产环境集成。

## 支持的模型/功能

当前平台提供四大主力视频模型家族，覆盖不同场景与精度需求：

- **HappyHorse**：专注物理真实感与运动流畅性，支持[文生视频](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)、图生视频（基于首帧）、参考生视频及视频编辑四类任务。
- **万相（WanX）**：功能最全的通用视频模型系列，包含：
  - 全能型 `wan3.0`（All-in-One），统一支持文生、图生、参考生；
  - 迭代型 `wan2.7`（推荐优先选用），明确区分文生、图生、参考生、视频编辑等子模型；
  - 早期 `wan2.1–2.6` 模型（已逐步归档），如[万相-图生视频-基于首帧（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)，仅支持单一模式，不建议新项目接入。
- **爱诗（PixVerse）**：强动态表现力，特别适合高速运动、法术特效等复杂场景，支持文生、图生（首帧/首尾帧）、参考生、对口型、动作模仿、视频超清六类能力。
- **可灵（Kling）与 Vidu**：面向高保真与工业化生产，支持4K输出、官方主体库调用（如[可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)）、广告级运镜（Vidu Q3-ad）等专业特性。
- **其他专用模型**：包括数字人（wan2.2-s2v）、视频口型替换（VideoRetalk）、视频风格重绘、图生动作（wan-animate-move）、视频换人（wan-animate-mix）等垂直能力。

> **注意**：万相2.7系列文档明确指出其为“新版协议”，而万相2.1–2.6系列被标注为“旧版协议”且[万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)已进入维护期；开发者应优先选用 `wan2.7` 或 `wan3.0`。

## 关键参数

所有视频生成 API 均需以下基础参数：

- **请求头（Headers）**
  - `Content-Type: application/json`（必选）
  - `Authorization: Bearer <API_KEY>`（必选，除部分地域限制模型外）
  - `X-DashScope-Async: enable`（**必选**，所有 HTTP 调用均强制异步；缺失将报错 `"current user api does not support synchronous calls"`）

- **请求体（Request Body）**
  - `model`（字符串，必选）：精确指定模型标识符，例如：
    - `wan2.7-text2video`
    - `pixverse/pixverse-v6-max-t2v`
    - `vidu/viduq3-pro_text2video`
    - `kling/kling-v4-omni-reference-video-generation`
  - `input`（对象，必选）：根据任务类型结构化输入，常见字段包括：
    - `prompt`（文本提示词，长度限制因模型而异：wan2.7 ≤5000字符，MiniMax ≤7000字符，Vidu ≤5000字符）
    - `image_url` / `video_url` / `audio_url`（公网可访问的 HTTPS/HTTP 链接）
    - `media`（数组，用于多模态输入，如 PixVerse 动作模仿要求 `[{ "type": "image_url", "url": "..." }, { "type": "video_url", "url": "..." }]`）
  - `parameters`（对象，可选）：控制输出规格，如：
    - `resolution`（`480P`, `720P`, `1080P`, `4k`）
    - `style`（视频风格重绘中取值 0–7）
    - `template`（万相视频特效专用，仅限 legacy 图生视频模型）

## 使用方式

所有视频生成 API 均遵循标准异步两步流程：

### 步骤 1：创建任务
向对应地域的 Endpoint 发起 `POST` 请求：
```http
POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```
- `{WorkspaceId}`：业务空间 ID（控制台「业务空间详情」页获取）
- `{region}`：地域代码，如 `cn-beijing`、`ap-southeast-1`、`us-east-1` 等  
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐（见[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)说明）。

成功响应返回 JSON，含 `task_id`（有效期 24 小时）。

### 步骤 2：轮询获取结果
使用 `task_id` 向任务查询接口发起 `GET` 请求：
```http
GET https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/tasks/{task_id}
```
轮询间隔建议 ≥3 秒，直至 `status` 字段为 `"SUCCESS"`，响应中 `output.video_url` 即为生成视频直链。

> **注意**：部分模型（如数字人 `wan2.2-s2v`、视频口型替换 `VideoRetalk`）使用 `/api/v1/services/aigc/image2video/...` 路径（见[数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)），路径不统一，需严格按各模型文档执行。

## 限制和注意事项

- **地域强一致性**：模型、Endpoint URL 与 API Key **必须属于同一地域**，跨地域调用必然失败（所有文档均强调此点，如[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)）。
- **输入文件要求**：
  - 图像：支持 JPG/JPEG/PNG/BMP/WEBP，分辨率通常要求 400–7000 像素；
  - 视频：MP4/AVI/MOV 等主流格式，时长 ≤30 秒（Vidu/Kling ≤15秒），大小 ≤100MB；
  - 音频：WAV/MP3/AAC，时长 2–120 秒，需人声清晰、无背景噪音。
- **计费与配额**：多数模型按视频时长或任务数计费（如 VideoRetalk 0.08元/秒），部分提供免费额度（见[VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)）；数字人 `wan2.2-s2v-detect` 即使检测不通过也计费。
- **安全与合规**：数字人、视频口型替换等涉及人脸的模型，需先调用图像检测接口（如 `wan2.2-s2v-detect`）确认输入合规，否则任务可能失败。
- **SDK 支持**：推荐使用 DashScope SDK（需[安装](../../raw/model-api-reference/preparations/install-sdk.md)），可自动处理认证、重试与轮询逻辑，降低集成复杂度。

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
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相-图生视频-视频特效列表](../../raw/_short/wanx-video-effects-5b23bdd72b8e7944.md)
- [万相-早期视频模型（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/_short/legacy-image-to-video-api-reference-8b02dd673da405f1.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/_short/legacy-wan-text-to-video-api-reference-9b1be2a560b41925.md)
- [万相-参考生视频API参考（2.6）](../../raw/_short/legacy-wan-reference-to-video-api-reference-e16a85c0479460c3.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/_short/legacy-image-to-video-by-first-and-last-frame-ap-524bb66cfed1f5de.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
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
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [可灵-官方主体与音色库](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-object-ids.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


