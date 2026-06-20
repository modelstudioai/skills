# video generation api

阿里云百炼平台提供多种视频生成模型的 API，覆盖文生视频、图生视频、参考生视频、视频编辑、人像动画等场景。所有视频生成 API 均采用异步调用模式，通过"创建任务 -> 轮询获取结果"两步完成调用，任务耗时通常为 1-5 分钟。

## 支持的模型与功能概览

百炼平台的视频生成能力按模型厂商可分为以下几大系列：

### 万相（Wan）系列

万相是阿里自研的视频生成模型，当前最新版本为 **wan2.7**，推荐优先使用。主要功能包括：

- **文生视频**：通过文本提示词生成视频，支持多镜头叙事，模型名称为 `wan2.7-t2v`。详见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)。
- **图生视频**：支持首帧生视频、首尾帧生视频、视频续写三大任务，模型名称如 `wan2.7-i2v-2026-04-25`。详见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)。
- **参考生视频**：支持多模态输入（图片、视频、音频），生成保持角色形象和音色一致性的视频，模型名称为 `wan2.7-r2v`。详见 [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)。
- **视频编辑**：支持指令编辑和视频迁移，模型名称为 `wan2.7-videoedit`。
- **图生动作**：将参考视频中的动作迁移到人物图片，模型名称为 `wan2.2-animate-move`，提供标准模式 `wan-std` 和专业模式 `wan-pro`。
- **视频换人**：将视频中的角色替换为指定图片中的人物，模型名称为 `wan2.2-animate-mix`。
- **数字人**：基于单张图片和音频生成说话/唱歌视频，模型名称为 `wan2.2-s2v`，需先调用 `wan2.2-s2v-detect` 进行图像检测。

> **注意**：万相 2.7 系列使用新版协议，与 wan2.6 及更早版本的旧版协议不兼容。旧版模型（wan2.1-2.6）的 API 文档仍然可用，但建议迁移到 2.7 版本以获得更好的效果。

### HappyHorse 系列

HappyHorse 提供四种视频生成能力：

- **文生视频**：模型名称 `happyhorse-1.0-t2v`
- **图生视频（基于首帧）**：模型名称 `happyhorse-1.0-i2v`
- **视频编辑**：模型名称 `happyhorse-1.0-video-edit`，支持风格变换和局部替换
- **参考生视频**：模型名称 `happyhorse-1.0-r2v`，支持传入多张参考图像

### 可灵（Kling）系列

可灵模型支持文生视频、图生视频（首帧/首尾帧）、参考生视频和视频编辑。需在百炼控制台搜索"kling"并开通服务后使用。主要模型包括：

- `kling/kling-v3-video-generation`
- `kling/kling-v3-omni-video-generation`

支持智能分镜（`multi_shot` + `shot_type`）和标准/专业模式（`mode: std/pro`）。详见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)。

### 爱诗（PixVerse）系列

PixVerse 提供文生视频、图生视频、首尾帧生视频和参考生视频能力，需开通后使用。主要模型版本包括 `pixverse-c1`、`pixverse-v6`、`pixverse-v5.6`，模型名称格式为 `pixverse/pixverse-{version}-{task}`。

### Vidu 系列

Vidu 提供文生视频、图生视频、首尾帧生视频和参考生视频能力。模型分为 `pro` 和 `turbo` 两个档次，命名格式为 `vidu/viduq3-{tier}_{task}`（如 `vidu/viduq3-pro_text2video`）。

### 人像动画模型

百炼还提供一系列专注于人像动画的模型：

- **悦动人像 EMO**：基于人物肖像图片和音频生成唱演视频，模型名称 `emo-v1`，需先用 `emo-detect-v1` 检测图片。详见 [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)。
- **舞动人像 AnimateAnyone**：基于人物图片和动作模板生成舞蹈视频，需依次调用 detect -> template -> 生成三个模型。
- **灵动人像 LivePortrait**：基于人物肖像和音频快速生成播报视频。
- **声动人像 VideoRetalk**：替换视频中人物的口型，使其匹配新的音频。
- **表情包 Emoji**：基于人物肖像和预设模板生成表情包视频。
- **视频风格重绘**：将视频转换为 8 种预设艺术风格（日式漫画、3D 卡通等），模型名称 `video-style-transform`。

## 统一调用方式

所有视频生成 API 采用相同的异步调用模式：

### 步骤 1：创建任务

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

必须设置以下请求头：

| 请求头 | 值 | 说明 |
|--------|------|------|
| `Content-Type` | `application/json` | 固定值 |
| `Authorization` | `Bearer $DASHSCOPE_API_KEY` | API Key 认证 |
| `X-DashScope-Async` | `enable` | 必须设置，否则报错 |

请求体基本结构：

```json
{
  "model": "模型名称",
  "input": {
    "prompt": "文本提示词",
    "media": [...]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 5
  }
}
```

### 步骤 2：轮询获取结果

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

使用步骤 1 返回的 `task_id` 查询任务状态，`task_id` 有效期为 24 小时。

> **注意**：部分旧版模型（如 `wan2.2-animate-move`、`wan2.2-animate-mix`、`wan2.2-kf2v-flash`）使用 `/api/v1/services/aigc/image2video/video-synthesis` 端点，与主流的 `/video-generation/video-synthesis` 端点不同，调用时需注意区分。

## 多地域支持

视频生成 API 在以下地域可用（不同模型支持的地域不同）：

| 地域 | Endpoint |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com` |

**必须确保模型、Endpoint URL 和 API Key 属于同一地域**，跨地域调用将失败。万相 2.7 和 HappyHorse 系列支持多地域，而可灵、PixVerse、Vidu 及人像动画模型目前仅支持北京地域。

## 关键参数说明

| 参数 | 说明 | 常见值 |
|------|------|--------|
| `resolution` | 视频分辨率 | `480P`、`540P`、`720P`、`1080P` |
| `duration` | 视频时长（秒） | `5`、`10`、`15`（因模型而异） |
| `ratio` / `size` | 画面比例或尺寸 | `16:9`、`9:16`、`1:1`、`1280*720` |
| `prompt_extend` | 是否开启提示词智能扩写 | `true` / `false` |
| `watermark` | 是否添加水印 | `true` / `false` |
| `mode` | 生成模式 | `std`（标准）、`pro`（专业） |
| `shot_type` | 镜头类型 | `single`、`multi`、`customize` |

> **注意**：不同模型对参数的支持范围不同。例如 `resolution` 和 `size` 参数在不同模型中可能不共存，部分模型使用 `ratio` 控制画面比例，部分模型使用 `size` 指定像素尺寸。具体请参阅各模型的 API 文档。

## 注意事项

1. **请勿重复创建任务**：创建任务后使用 `task_id` 轮询获取结果即可。
2. **API Key 配置**：建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码。
3. **第三方模型需开通**：可灵、PixVerse、Vidu 等第三方模型需在百炼控制台搜索并开通服务后才能调用。
4. **人像动画类模型需先检测**：EMO、AnimateAnyone、LivePortrait、Emoji 等模型在生成视频前需先调用对应的 detect 模型检测图片合规性。
5. **新加坡地域迁移**：新加坡地域推荐使用[业务空间](../concepts/workspace.md)专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，以获得更好的性能和稳定性。

## 来源文档

- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-video-edit-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-reference-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-video-editing-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/text-to-video-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-s2v-overview.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emo-quick-start.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/animateanyone-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/liveportrait-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/videoretalk.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/emoji-quick-start.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-api-reference/kling-video-generation-api-reference.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/portrait-animation-api-reference/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-keyframe-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-api-reference/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/wan-api-reference/legacy-video-models/legacy-wanx-vace-api-reference.md)



