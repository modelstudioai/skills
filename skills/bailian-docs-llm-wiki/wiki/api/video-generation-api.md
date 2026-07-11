# video generation api

百炼平台提供丰富的视频生成 API，涵盖文生视频、图生视频、参考生视频、视频编辑、人像动画等多种能力。所有视频生成接口均采用[异步调用](../concepts/async-invocation.md)模式（创建任务 -> 轮询获取结果），支持多个模型家族，开发者可根据场景需求灵活选用。

## 支持的模型家族

### 万相 (Wan) 系列

万相是百炼自研的视频生成模型，最新版本为 wan2.7，推荐优先选用。详见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md) 和 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。

**通用视频生成能力：**

| 任务类型 | wan2.7 模型示例 | 说明 |
|---------|---------------|------|
| 文生视频 | `wan2.7-t2v-2026-06-12` | 纯文本提示词生成视频，支持多镜头叙事 |
| 图生视频（首帧） | `wan2.7-i2v-2026-04-25` | 首帧图像 + 文本，支持首帧/首尾帧/视频续写 |
| 参考生视频 | `wan2.7-r2v-2026-06-12` | [多模态](../concepts/multimodal.md)输入（图片/视频/音频），支持多角色互动与音色一致性 |
| 视频编辑 | `wan2.7-videoedit` | 支持指令编辑和视频迁移 |

**特色能力：**

| 任务类型 | 模型 | 说明 |
|---------|------|------|
| 图生动作 | `wan2.2-animate-move` | 将参考视频中的动作迁移到人物图片，支持 `wan-std`/`wan-pro` 两种模式 |
| 视频换人 | `wan2.2-animate-mix` | 将视频中角色替换为图片中的人物，保留场景和光照 |
| 数字人 | `wan2.2-s2v` | 基于单张图片和音频生成说话/唱歌视频，需先调用 `wan2.2-s2v-detect` 检测图片合规性 |

> **注意**：万相 2.6 及早期版本（wan2.5/wan2.2/wanx2.1）使用旧版 API 协议，与 wan2.7 的请求参数格式有差异。新项目推荐使用 wan2.7 系列。

### HappyHorse 系列

HappyHorse 支持文生视频、图生视频（基于首帧）、参考生视频和视频编辑四种任务。详见 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

| 任务类型 | 模型 |
|---------|------|
| 文生视频 | `happyhorse-1.1-t2v` |
| 图生视频（首帧） | `happyhorse-1.1-i2v` |
| 参考生视频 | `happyhorse-1.1-r2v`（支持多张参考图像） |
| 视频编辑 | `happyhorse-1.0-video-edit` |

HappyHorse 支持华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）四个地域。

### 爱诗 (PixVerse) 系列

PixVerse 仅在华北2（北京）地域可用，使用前需在百炼控制台搜索 PixVerse 并开通服务。提供多个版本（pixverse-c1 / pixverse-v6 / pixverse-v5.6），其中 pixverse-c1 支持多镜头生成和音频生成。详见 [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)。

| 任务类型 | 模型示例 |
|---------|---------|
| 文生视频 | `pixverse/pixverse-c1-t2v` |
| 图生视频（首帧） | `pixverse/pixverse-c1-it2v` |
| 首尾帧生视频 | `pixverse/pixverse-c1-kf2v` |
| 参考生视频 | `pixverse/pixverse-c1-r2v` |

### Vidu 系列

Vidu 仅在华北2（北京）地域可用，使用前需开通 Vidu 服务。提供 pro 和 turbo 两种模式。

| 任务类型 | 模型示例 |
|---------|---------|
| 文生视频 | `vidu/viduq3-pro_text2video`、`vidu/viduq3-turbo_text2video` |
| 图生视频（首帧） | `vidu/viduq3-pro_img2video`、`vidu/viduq3-turbo_img2video` |
| 首尾帧生视频 | `vidu/viduq3-pro_start-end2video` |
| 参考生视频 | `vidu/viduq3-mix_reference2video` |

### 可灵 (Kling) 系列

可灵仅在华北2（北京）地域可用，使用前需在控制台搜索 kling 并开通服务。支持文生视频、图生视频、首尾帧生视频、参考生视频和视频编辑，详见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

| 任务类型 | 模型示例 |
|---------|---------|
| 文生视频 | `kling/kling-v3-video-generation`、`kling/kling-v3-omni-video-generation` |
| 图生视频等 | 同一模型卡片内支持多种任务 |

可灵支持 `std` 和 `pro` 两种模式，以及智能分镜功能。

### 人像动画模型

百炼还提供一组人像动画模型，适用于特定的人物视频生成场景：

| 模型 | 功能 | 输入 |
|------|------|------|
| 舞动人像 AnimateAnyone | 基于人物图片和动作模板生成舞蹈视频 | 图片 + 动作视频 |
| 悦动人像 EMO | 基于肖像图片和音频生成唱演视频 | 肖像 + 音频 |
| 灵动人像 LivePortrait | 快速轻量的人物播报视频生成 | 肖像 + 音频 |
| 声动人像 VideoRetalk | 视频口型替换，使口型匹配新音频 | 视频 + 音频 |
| 表情包 Emoji | 基于人物肖像和预设模板生成表情包视频 | 肖像 + 模板ID |
| 视频风格重绘 | 将视频转换为 8 种预设艺术风格 | 视频 + 风格参数 |

> **注意**：AnimateAnyone 和 EMO 等人像动画模型需先调用对应的 detect 接口检测图片合规性，通过后才能提交视频生成任务。详见 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md) 和 [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)。

## 调用方式

所有视频生成 API 均采用**[异步调用](../concepts/async-invocation.md)**，流程分为两步：

### 步骤 1：创建任务

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

必须携带请求头 `X-DashScope-Async: enable`，否则会报错 `current user api does not support synchronous calls`。

请求成功后返回 `task_id`，有效期 24 小时。

### 步骤 2：轮询获取结果

```
GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}
```

轮询直到任务状态为 `SUCCEEDED` 或 `FAILED`。

> **注意**：部分旧版模型（如图生动作 `wan2.2-animate-move`、视频换人 `wan2.2-animate-mix`、首尾帧 `wan2.2-kf2v-*`）使用的端点路径为 `/api/v1/services/aigc/image2video/video-synthesis`，与通用的 `/video-generation/video-synthesis` 不同。

## 关键参数

各模型的参数名称基本一致，但取值范围有差异：

| 参数 | 说明 | 常见取值 |
|------|------|---------|
| `model` | 模型名称（必选） | 因模型而异 |
| `prompt` | 文本提示词 | 中英文均可，长度上限因模型而异 |
| `media` / `input.media` | 输入媒体（图片/视频/音频） | 通过 `type` 字段区分 `first_frame`、`last_frame`、`reference_image`、`video` 等 |
| `resolution` | 输出分辨率 | `480P`、`540P`、`720P`、`1080P`（因模型而异） |
| `duration` | 视频时长（秒） | 通常 5 或 10 |
| `prompt_extend` | 是否开启提示词智能扩写 | `true` / `false` |
| `watermark` | 是否添加水印 | `true` / `false` |
| `audio` | 是否生成音频 | `true` / `false`（部分模型支持） |
| `shot_type` | 镜头模式 | `single` / `multi` / `customize`（多镜头叙事时使用） |

## 地域与端点

| 地域 | 端点 URL |
|------|---------|
| 华北2（北京） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台的[业务空间](../concepts/workspace.md)详情页面查看。

> **注意**：不同地域拥有独立的 API Key 与请求地址，不可混用，跨地域调用将导致鉴权失败。部分模型（如 PixVerse、Vidu、Kling、人像动画类）仅支持华北2（北京）地域。万相和 HappyHorse 系列支持多地域部署。

## 注意事项

- 模型、Endpoint URL 和 API Key 必须属于同一地域，跨地域调用会失败。
- 视频生成任务通常耗时 1-5 分钟（wanx2.1-vace 编辑模型约 5-10 分钟），请勿重复创建任务，用 `task_id` 轮询即可。
- 百炼推荐使用[业务空间](../concepts/workspace.md)专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），相比旧域名（`dashscope.aliyuncs.com`）有更好的性能和稳定性。
- 人像动画模型（AnimateAnyone、EMO、LivePortrait）支持模型调用（后付费）和模型独立部署（预付费）两种模式。
- 数字人模型 `wan2.2-s2v` 与悦动人像 EMO 的选型建议：需要全身/大半身视频选 s2v，追求性价比且以肖像特写为主选 EMO。

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



