# video generation api

百炼平台视频生成 API 覆盖文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、视频风格重绘、视频超清、对口型、动作模仿、数字人/人像动画等任务，统一采用异步任务模式（创建任务 → 轮询结果）。本页汇总各模型家族的能力差异、接入地址、关键参数与注意事项，供开发者选型与集成参考。

## 支持的模型与功能

### 万相（Wan）系列

- **wan2.7（新版协议，推荐）**：
  - 图生视频：支持[多模态](../concepts/multimodal.md)输入（文本/图像/音频/视频），可完成首帧生视频、首尾帧生视频、视频续写，详见[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
  - 文生视频：支持自然语言控制单/多镜头叙事（通过 [prompt](../guides/prompt.md) 描述分镜，无需 `shot_type`），详见[万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
  - 参考生视频（wan2.7-r2v）：[多模态](../concepts/multimodal.md)输入（图片/视频/音频），保持角色形象与音色一致性，支持多主体参考，详见[万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)。
  - 视频编辑（wan2.7-videoedit）：支持纯指令编辑（如风格转换）与视频迁移，详见[万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)。
- **旧版模型（2.1–2.6，旧版协议）**：wan2.6/2.5/2.2/wanx2.1 的文生视频、图生视频（首帧）、首尾帧生视频（wan2.2-kf2v）、参考生视频（wan2.6）、视频编辑统一模型（wanx2.1-vace-plus，通过 `function` 字段区分任务，如 `image_reference`）。
- **人像/动作类**：
  - wan2.2-animate-move（图生动作）：将参考视频的动作与表情迁移到人物图片，提供标准模式 `wan-std` 与专业模式 `wan-pro`，详见[万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)。
  - wan2.2-animate-mix（视频换人）：保留原视频场景/光照/动作，替换主角，详见[万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)。
  - wan2.2-s2v（数字人）：单张图片 + 音频生成说话/唱歌/表演视频；须先调用 `wan2.2-s2v-detect` 检测图像合规，详见[万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)。

### HappyHorse 系列

支持文生视频（happyhorse-1.1-t2v）、图生视频（首帧）、参考生视频（多张参考图像 + 提示词）、视频编辑（视频 + 参考图 + 文本指令，完成风格变换/局部替换），详见[HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)与[HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)。

### 爱诗（PixVerse）系列

- 文生视频：`pixverse/pixverse-c1-t2v`、`pixverse/pixverse-v6-t2v`、`pixverse/pixverse-v5.6-t2v`，c1 支持 [prompt](../guides/prompt.md) 描述多镜头。
- 图生视频（首帧）：`pixverse-c1-it2v`、`pixverse-v6-it2v`、`pixverse-v5.6-it2v`。
- 首尾帧生视频：`pixverse-c1-kf2v`、`pixverse-v6-kf2v`、`pixverse-v5.6-kf2v`，通过 `media` 中 `first_frame` / `last_frame` 传入。
- 参考生视频：`pixverse-c1-r2v`。
- 视频增强类：`pixverse-upscale`（固定输出 4K 超清）、`pixverse-lipsync`（音频或 TTS 文本驱动对口型）、`pixverse-motioncontrol`（动作模仿）。
- 调用前需在控制台搜索 PixVerse 并开通，详见[爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)。

### Vidu 系列

- 文生视频：`vidu/viduq3-turbo_text2video` 等。
- 图生视频（首帧）：`vidu/viduq3-pro-fast_img2video` 等。
- 首尾帧生视频：`vidu/viduq3-turbo_start-end2video`。
- 参考生视频：`vidu/viduq3-ad_reference2video`（广告场景）等。
- 调用前需在控制台搜索 Vidu 并开通，详见[Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)。

### 可灵（Kling）

支持文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑，模型如 `kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation`（支持智能分镜），参数含 `mode`（std）、`aspect_ratio`、`duration`、`audio`，详见[可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

### 人像动画与风格类

- 舞动人像 AnimateAnyone：detect → template → 生成三步流程，支持后付费调用与独立部署，详见[图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)。
- 悦动人像 EMO：肖像 + 人声音频生成唱演视频，`style_level` 可选 active/normal/calm。
- 灵动人像 LivePortrait：肖像 + 音频快速生成播报视频。
- 声动人像 VideoRetalk：视频 + 音频替换口型。
- 表情包 Emoji：肖像 + 预设模板（driven_id）生成表情视频。
- 视频风格重绘（video-style-transform）：8 种预设风格（日式漫画、3D 卡通、国风水墨等），参数 `style`（0–7）与 `video_fps`，详见[视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)。

## 调用方式

所有视频生成/编辑任务耗时较长（通常 1–5 分钟，wanx2.1-vace 约 5–10 分钟），均采用异步两步流程：

1. **创建任务**：`POST` 提交请求，必须携带请求头 `X-DashScope-Async: enable`（缺失会报 "current user api does not [support](../guides/support.md) synchronous calls"）与 `Authorization: Bearer $DASHSCOPE_API_KEY`，返回 `task_id`（有效期 24 小时）。请勿重复创建任务。
2. **轮询结果**：`GET /api/v1/tasks/{task_id}` 查询状态，成功后获取视频 URL。

**Endpoint 路径**（按模型而异）：

- 通用路径 `/api/v1/services/aigc/video-generation/video-synthesis`：wan2.7、HappyHorse、PixVerse、Vidu、可灵、视频风格重绘等。
- 旧路径 `/api/v1/services/aigc/image2video/video-synthesis`：wan2.2-animate-move/mix、wan2.2-s2v、wan2.2 首尾帧（wan2.2-kf2v）等，详见[万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)。

**地域与域名**：模型、Endpoint URL、[API Key](../concepts/api-key.md) 必须属于同一地域，跨地域调用会失败。

- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- 美国（弗吉尼亚）：`https://dashscope-us.aliyuncs.com`（HappyHorse 与旧版万相支持）
- 德国（法兰克福）：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com`
- 日本（东京）：`https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com`（HappyHorse 支持）

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID。旧域名 `dashscope.aliyuncs.com` / `dashscope-intl.aliyuncs.com` 仍可用，但官方建议迁移至[业务空间](../concepts/workspace.md)专属域名以获得更好的性能与稳定性。

**请求体结构**（新版协议示例）：

```json
{
  "model": "wan2.7-t2v-2026-06-12",
  "input": {
    "prompt": "...",
    "media": [{ "type": "image_url", "url": "..." }]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 5,
    "watermark": true
  }
}
```

## 关键参数

| 参数 | 说明 |
| --- | --- |
| `model` | 模型名称，决定协议版本与能力（如 `wan2.7-*` 为新版协议，`wanx2.1-*` 为旧版） |
| `input.prompt` | 文本提示词；wan2.7 与 pixverse-c1 可在 [prompt](../guides/prompt.md) 中用自然语言/时间戳描述多镜头 |
| `input.media` | [多模态](../concepts/multimodal.md)素材数组，`type` 取值如 `image_url`、`image`、`first_frame`、`last_frame`、`video`、`video_url`、`audio_url`、`reference_image` |
| `parameters.resolution` / `size` | 分辨率（如 `720P`、`1080P`）或尺寸（如 `1280*720`），不同模型支持的档位不同 |
| `parameters.duration` | 视频时长（秒），常见 5 |
| `parameters.watermark` | 是否添加水印 |
| `parameters.audio` | 是否生成音频（wan2.7、可灵等支持） |
| `parameters.seed` | 随机种子，用于结果复现 |
| `parameters.shot_type` | 仅旧版 wan2.6 系列支持（`multi` 多镜头）；wan2.7 与 pixverse-c1 通过 [prompt](../guides/prompt.md) 控制，设置该参数不生效 |

## 限制与注意事项

> **注意**：wan2.7 系列使用**新版协议**（`media` 数组传参），旧版 wan2.6/2.5/2.2/wanx2.1 使用**旧版协议**（如 `img_url`、`reference_urls`、`function` 等字段），两套协议不兼容；选型时请优先使用 wan2.7 新版接口（参见[万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)中的迁移说明）。

- **地域限制**：PixVerse、Vidu、可灵、人像动画系列（EMO/LivePortrait/VideoRetalk/Emoji/AnimateAnyone）、视频风格重绘、wan2.2-s2v 等**仅支持华北2（北京）地域**；万相 2.7 支持北京与新加坡；HappyHorse 与旧版万相支持更多海外地域。
- **服务开通**：PixVerse、Vidu、可灵为第三方模型，需先在模型广场搜索并单击"立即开通"。
- **task_id 有效期 24 小时**，过期查询返回 `UNKNOWN`。
- **[限流](../concepts/rate-limit.md)**：多数视频模型任务下发 RPS/QPS 限制为 5，同时处理中任务数为 1（排队机制）；检测类接口（detect）为同步接口、无并发限制。
- **人像类模型需先检测**：AnimateAnyone、EMO、LivePortrait、Emoji、wan2.2-s2v 均须先调用对应 `-detect` 模型确认图像合规，再提交生成任务。
- **计费**：按生成视频时长计费（如 0.02–0.16 元/秒不等）或按张计费（detect 0.004 元/张）；部分模型提供免费额度，详见各文档的资费表。
- **输出说明**：AnimateAnyone 生成的视频不含音频；视频超清固定输出 4K（3840×2160）。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [爱诗-视频超清API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-upscale-api-reference.md)
- [爱诗-视频对口型API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-lipsync-api-reference.md)
- [爱诗-视频动作模仿API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-motioncontrol-api-reference.md)





