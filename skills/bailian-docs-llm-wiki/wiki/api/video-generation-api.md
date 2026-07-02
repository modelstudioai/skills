# video generation api

百炼平台提供多种视频生成模型的 API，覆盖文生视频、图生视频、参考生视频、视频编辑、人像动画等场景。所有视频生成 API 均采用异步调用模式（创建任务 → 轮询获取结果），统一通过 DashScope 接口访问，处理时间通常为 1-5 分钟。

## 支持的模型与功能

### 万相系列（Wan）

万相是百炼自研的视频生成模型，当前最新版本为 wan2.7。主要能力包括：

- **文生视频**：基于文本提示词生成视频，支持多镜头叙事（通过 [prompt](../guides/prompt.md) 中的时间戳描述分镜）。详见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **图生视频**：wan2.7 新版协议支持首帧生视频、首尾帧生视频、视频续写三大任务，支持[多模态](../concepts/multimodal.md)输入（文本/图像/音频/视频）。详见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
- **参考生视频**：支持[多模态](../concepts/multimodal.md)输入（图片、视频、音频），生成保持角色形象和音色一致性的视频，适用于单角色表演或多角色互动。
- **视频编辑**：支持指令编辑（修改视频风格）和视频迁移（局部替换），模型为 `wan2.7-videoedit`。
- **图生动作**：将参考视频中的动作迁移到人物图片，模型为 `wan2.2-animate-move`，提供标准模式（wan-std）和专业模式（wan-pro）。
- **视频换人**：将视频中的角色替换为指定图片中的人物，模型为 `wan2.2-animate-mix`。
- **数字人**：基于单张图片和音频生成说话/唱歌/表演视频，模型为 `wan2.2-s2v`，支持肖像、全身或半身画幅。

> **注意**：万相2.7 图生视频使用新版协议，与 wan2.6 及早期版本的旧版协议不兼容。旧版模型（wan2.1-2.6）请参考对应的 Legacy API 文档。推荐优先使用 wan2.7 模型。

### HappyHorse

HappyHorse 提供四种视频生成能力：

- **文生视频**（`happyhorse-1.1-t2v`）：输入文本提示词生成视频
- **图生视频**（`happyhorse-1.1-i2v`）：以首帧图片为基础生成视频
- **参考生视频**（`happyhorse-1.1-r2v`）：传入多张参考图像融合生成视频
- **视频编辑**（`happyhorse-1.0-video-edit`）：输入视频与参考图完成风格变换、局部替换

HappyHorse 支持华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）四个地域。详见 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

### 爱诗（PixVerse）

爱诗系列模型目前仅适用于华北2（北京）地域，使用前需在控制台搜索 PixVerse 并开通服务。提供：

- **文生视频**：支持 `pixverse-c1-t2v`、`pixverse-v6-t2v`、`pixverse-v5.6-t2v` 等模型，pixverse-c1 和 v6 支持多镜头生成
- **图生视频**：基于首帧图像生成视频
- **首尾帧生视频**：基于首帧和尾帧图像生成平滑过渡视频
- **参考生视频**：传入参考图片融合生成视频

### Vidu

Vidu 系列模型目前仅适用于华北2（北京）地域，使用前需在控制台开通。提供：

- **文生视频**：支持 `viduq3-pro`、`viduq3-turbo`、`viduq2` 等版本
- **图生视频**：支持 `viduq3-pro_img2video`、`viduq3-turbo_img2video` 等
- **首尾帧生视频**：支持 `viduq3-pro_start-end2video` 等
- **参考生视频**：支持 `viduq3-mix_reference2video` 等，可传入参考图像和视频

### 可灵（Kling）

可灵视频生成模型仅适用于华北2（北京）地域，支持文生视频、图生视频、首尾帧生视频、参考生视频和视频编辑。支持模型包括 `kling-v3-omni-video-generation`、`kling-v3-video-generation` 等，支持智能分镜功能。详见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

### 人像动画与特效

- **舞动人像 AnimateAnyone**：基于人物图片和动作模板生成舞蹈视频。需依次调用 detect → template → 生成三个模型。支持模型调用和模型独立部署两种模式。
- **悦动人像 EMO**：基于人物肖像图片和音频生成唱演视频，支持活泼/适中/平静三种动作风格。需先调用 detect 再调用生成。
- **灵动人像 LivePortrait**：快速轻量地基于人物肖像和音频生成播报视频。
- **声动人像 VideoRetalk**：将视频中人物的口型替换为匹配输入音频的口型。
- **表情包 Emoji**：基于人物肖像和预设动态模板生成表情包视频。
- **视频风格重绘**：将视频转换为预设艺术风格（日式漫画、美式漫画、3D卡通等 8 种），模型为 `video-style-transform`。

## 调用方式

### 统一接口

所有视频生成模型使用统一的异步调用流程：

**步骤 1：创建任务**

```
POST https://{endpoint}/api/v1/services/aigc/video-generation/video-synthesis
```

必须携带请求头 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。

**步骤 2：轮询结果**

```
GET https://{endpoint}/api/v1/tasks/{task_id}
```

`task_id` 有效期为 24 小时，请勿重复创建任务。

> **注意**：部分早期模型（如 AnimateAnyone、图生动作、视频换人、首尾帧生视频 wan2.2）使用 `/api/v1/services/aigc/image2video/video-synthesis` 端点，与主流端点不同。

### 地域与端点

| 地域 | Endpoint |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` 或 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（推荐） |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（推荐） |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

其中 `{WorkspaceId}` 为[业务空间](../concepts/workspace.md) ID，可在百炼控制台的[业务空间](../concepts/workspace.md)详情页面查看。建议迁移至[业务空间](../concepts/workspace.md)专属域名以获得更好的性能和稳定性。

> **注意**：模型、Endpoint URL 和 [API Key](../concepts/api-key.md) 必须属于同一地域，跨地域调用将失败。不同模型支持的地域范围不同：万相 wan2.7 和 HappyHorse 支持多地域，而 PixVerse、Vidu、可灵、人像动画类模型仅支持华北2（北京）地域。

### 认证方式

所有请求通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 进行身份认证。[API Key](../concepts/api-key.md) 需在百炼控制台获取，且必须与请求端点属于同一地域。

## 关键参数

各模型的通用参数包括：

| 参数 | 说明 |
|------|------|
| `model` | 模型名称，决定使用的模型和版本 |
| `input.prompt` | 文本提示词，描述期望的视频内容 |
| `input.media` | 输入媒体列表（图像、视频、音频），wan2.7 新版协议使用 |
| `parameters.resolution` | 视频分辨率，常见值为 `480P`、`540P`、`720P` |
| `parameters.duration` | 视频时长（秒） |
| `parameters.prompt_extend` | 是否开启提示词智能改写 |
| `parameters.watermark` | 是否添加水印 |

> **注意**：不同模型对参数的支持范围不同。部分模型使用 `size`（如 `1280*720`）而非 `resolution` 来设置分辨率；万相旧版协议使用 `input.img_url` / `input.video_url` 等字段，与新版协议的 `input.media` 数组格式不同。

## 限制与注意事项

- 视频生成任务通常耗时 1-5 分钟（万相2.1 视频编辑约 5-10 分钟），请通过轮询获取结果。
- 各模型的并发限制不同，人像动画类模型（EMO、AnimateAnyone、LivePortrait）同时处理中任务数通常仅为 1。
- PixVerse 和 Vidu 需在控制台手动开通服务后才能调用。
- 数字人模型（wan2.2-s2v）需先调用 detect 接口检查图片合规性，再提交视频生成任务。
- 万相旧版模型（wan2.1-2.6）与新版 wan2.7 使用不同的 API 协议，迁移时需注意请求体结构差异。

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


