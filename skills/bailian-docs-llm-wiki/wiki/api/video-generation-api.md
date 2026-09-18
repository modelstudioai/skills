# video generation api

百炼平台提供多种视频生成能力，涵盖文生视频、图生视频、参考生视频、视频编辑、数字人驱动、风格重绘等场景。所有视频生成 API 均采用异步调用模式，需通过“创建任务 → 轮询结果”两步完成，典型耗时为 1–5 分钟（部分模型如 VideoRetalk 或数字人可达 10 分钟）。统一使用 `video-synthesis` 接口路径，但不同模型对请求头、参数结构及输入模态要求存在显著差异。

## 支持的模型/功能

当前主流视频生成模型分为三大类：

- **通用视频生成模型**：  
  - `HappyHorse` 系列：支持文生视频、图生视频（首帧）、参考生视频、视频编辑 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)；  
  - `万相（Wan）` 系列：3.0 版本为 All-in-One 模型，统一支持文生、图生（首帧/首尾帧）、参考生、视频编辑；2.7 版本按功能拆分为独立接口，推荐优先选用 [万相3.0-视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan3-video-generation-api-reference.md)；  
  - `爱诗（PixVerse）`：提供图生视频（首帧/首尾帧）、参考生视频、视频对口型、动作模仿等细分能力 [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)。

- **人像驱动与数字人模型**：  
  - `EMO`、`LivePortrait`、`AnimateAnyone`、`VideoRetalk`、`Emoji` 等均属“人像驱动”范畴，需先调用对应图像检测 API（如 `emo-detect-v1`）验证输入合规性，再提交生成任务；  
  - `wan2.2-s2v`（数字人）和 `wan2.2-s2v-detect` 为配套模型，必须按检测→生成顺序调用 [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)。

- **专用功能模型**：  
  - `视频风格重绘`（`video-style-transform`）支持 8 种预设艺术风格转换；  
  - `万相视频特效` 仅适用于早期图生视频模型（2.1–2.6），通过 `template` 参数指定效果，无需提示词 [万相-图生视频-视频特效列表](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference/wanx-video-effects.md)。

> **注意**：万相 2.1–2.6 系列（如 `wanx2.1-i2v-turbo`）与 2.7+ 系列（如 `wan2.7-videoedit`）使用同一 endpoint，但协议不兼容；旧版文档明确标注“旧版协议”，新版文档强调“仅支持 wan2.7 模型”。开发者须严格按模型版本选择对应文档，混用将导致参数解析失败。

## 关键参数

### 公共请求头（所有模型必需）
| 字段 | 类型 | 值 | 说明 |
|------|------|----|------|
| `Content-Type` | string | `application/json` | 必须显式设置 |
| `Authorization` | string | `Bearer sk-xxx` | 使用对应地域的 API Key |
| `X-DashScope-Async` | string | `enable` | **所有 HTTP 调用必须设置**，否则返回 `current user api does not support synchronous calls` 错误 |

### 请求体核心字段
- `model`（string，必选）：模型标识符，例如：  
  - `happyhorse-text-to-video`、`wan2.7-videoedit`、`pixverse/pixverse-v6-it2v`、`emo-v1`、`video-style-transform`；  
  - 部分模型（如 `wan2.2-s2v`）需精确匹配名称，大小写敏感。
- `input`（object，必选）：根据模型类型结构差异大：  
  - 文生视频：`{"prompt": "a cat dancing"}`；  
  - 图生视频：`{"img_url": "https://...", "prompt": "..."}`；  
  - 数字人：`{"image_url": "...", "audio_url": "..."}`；  
  - 视频风格重绘：`{"video_url": "...", "parameters": {"style": 0}}`；  
  - 人像驱动类模型（EMO/LivePortrait/AnimateAnyone）**必须包含检测 API 返回的 `face_bbox` 和 `ext_bbox` 坐标**，否则生成失败。
- `parameters`（object，可选）：控制输出质量与格式，常见字段：  
  - `resolution`：如 `"720P"`（万相）、`"480P"`（wan2.2-s2v）；  
  - `style_level`：EMO 的动作风格强度（`"active"`/`"normal"`/`"calm"`）；  
  - `template`：万相视频特效模板 ID（如 `"flying"`）；  
  - `style`：视频风格重绘的整数风格码（0–7）。

## 使用方式

### 1. 地域与环境准备
- **三要素同地域**：模型、Endpoint URL、API Key 必须属于同一地域（如华北2北京），跨地域调用必然失败 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)；  
- **推荐使用业务空间专属域名**：华北2（北京）和新加坡地域已启用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 等新域名，性能与稳定性优于旧域名 `dashscope.aliyuncs.com`；  
- **获取 WorkspaceId**：在阿里云百炼控制台“业务空间详情”页面查看，替换 URL 中的 `{WorkspaceId}`。

### 2. 异步调用流程
```bash
# 步骤1：创建任务（返回 task_id）
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-xxx" \
  -H "X-DashScope-Async: enable" \
  -d '{
        "model": "wan2.7-videoedit",
        "input": { "prompt": "change clothes to red dress" },
        "parameters": { "resolution": "720P" }
      }'

# 步骤2：轮询结果（task_id 有效期 24 小时）
curl "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}"
```

### 3. 特殊前置步骤
- **人像类模型（EMO/LivePortrait/AnimateAnyone/Emoji）**：必须先调用对应 `*-detect` API（如 `emo-detect-v1`），将返回的 `face_bbox` 和 `ext_bbox` 作为生成请求的 `input` 字段传入；  
- **数字人 wan2.2-s2v**：必须先调用 `wan2.2-s2v-detect`，仅当 `output.check_pass == true` 时才可提交生成任务；  
- **万相视频特效**：仅支持 `wanx2.1-i2v-turbo` 等旧版图生视频模型，且 `input` 中**不可传 `prompt`**，只传 `img_url` 和 `template`。

## 限制和注意事项

- **地域强约束**：所有模型均严格校验地域一致性，华北2（北京）的 API Key 无法调用新加坡地域的模型，反之亦然；  
- **输入文件限制**：  
  - 图片：URL 必须公网可访问，格式 JPG/PNG/WEBP，边长 400–7000 像素（EMO/LivePortrait 等要求 ≤4096）；  
  - 视频：MP4/AVI/MOV，≤300MB（VideoRetalk），≤100MB（风格重绘），时长 2–120 秒；  
  - 音频：WAV/MP3，≤15MB，人声清晰无背景噪音；  
- **任务管理**：`task_id` 有效期 24 小时，超时后无法查询；禁止重复创建相同任务，应轮询而非重试；  
- **计费与限流**：  
  - 多数模型按秒计费（如 `wan2.2-s2v` 720P 0.9 元/秒），数字人检测类模型按张计费（0.004 元/张）；  
  - 各模型有独立 RPS/QPS 限制（通常为 1–5），超出将返回 `429 Too Many Requests`；  
- **错误排查**：  
  - 缺少 `X-DashScope-Async: enable` → `current user api does not support synchronous calls`；  
  - 地域不匹配 → `Unauthorized` 或 `InvalidRegionId`；  
  - 图像检测未通过 → 生成任务直接失败，需先修复图片再重试。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
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
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [数字人wan2.2-s2v图像检测API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-detect-api.md)
- [数字人wan2.2-s2v视频生成API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview/wan-s2v-api.md)
- [人像驱动](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference.md)
- [AnimateAnyone 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-detect-api.md)
- [AnimateAnyone动作模板生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animate-anyone-template-api.md)
- [AnimateAnyone 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start/animateanyone-video-generation-api.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [EMO图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-detect-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [LivePortrait图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-detect-api.md)
- [LivePortrait 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start/liveportrait-api.md)
- [VideoRetalk 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk/videoretalk-api.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Emoji 视频生成API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-api.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗](../../raw/model-api-reference/video-generation-api/pixverse-api-reference.md)
- [EMO 视频生成 API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start/emo-api.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [可灵](../../raw/model-api-reference/video-generation-api/kling-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [可灵-主体ID列表](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference/kling-object-ids.md)
- [表情包Emoji 图像检测API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start/emoji-detect-api.md)
- [Vidu](../../raw/model-api-reference/video-generation-api/vidu-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [MiniMax](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [MiniMax-视频生成API文档](../../raw/model-api-reference/video-generation-api/minimax-video-api-reference/minimax-video-generation-api-reference.md)


