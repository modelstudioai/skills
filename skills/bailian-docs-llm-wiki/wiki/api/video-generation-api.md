# video generation api

百炼平台提供丰富的视频生成 API，覆盖文生视频、图生视频、参考生视频、视频编辑、数字人等多种场景。平台聚合了万相（Wan）、HappyHorse、爱诗（PixVerse）、可灵（Kling）、Vidu 等多家模型，统一通过[异步任务](../concepts/async-task.md)接口调用。

## 调用流程

所有视频生成 API 均采用**异步调用**模式，耗时通常为 1-5 分钟。流程分两步：

1. **创建任务**：通过 `POST` 请求提交参数，返回 `task_id`。请求头必须设置 `X-DashScope-Async: enable`，否则报错 "current user api does not [support](../guides/support.md) synchronous calls"。
2. **轮询结果**：通过 `GET` 请求查询 `task_id` 状态，直到任务完成获取视频 URL。`task_id` 有效期为 24 小时，**请勿重复创建任务**。

统一接口端点为：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

必选请求头包括 `Content-Type: application/json`、`Authorization: Bearer $DASHSCOPE_API_KEY` 和 `X-DashScope-Async: enable`。详细调用流程参见 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)。

## 支持的模型与功能

### 万相系列（Wan）

万相是百炼自研的视频生成模型，覆盖功能最全面：

| 功能 | 推荐模型（wan2.7） | 旧版模型 |
|------|-------------------|---------|
| 文生视频 | `wan2.7-t2v` | `wan2.6-t2v` / `wan2.5-t2v` |
| 图生视频（首帧/首尾帧/续写） | `wan2.7-i2v-*` | `wan2.6-i2v-*`（仅首帧） |
| 参考生视频 | `wan2.7-r2v` | `wan2.6-r2v-*` |
| 视频编辑 | `wan2.7-videoedit` | `wanx2.1-vace-plus` |
| 图生动作 | `wan2.2-animate-move` | - |
| 视频换人 | `wan2.2-animate-mix` | - |
| 数字人 | `wan2.2-s2v` | - |

> **注意**：wan2.7 系列使用新版 API 协议，wan2.6 及更早版本使用旧版协议，两者在 `input` 参数结构上有差异。推荐优先使用 wan2.7 系列模型。详情参见 [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)。

wan2.7 文生视频支持**多镜头叙事**——在 `prompt` 中用时间戳描述分镜（如"第1个镜头[0-3秒] 全景：..."），模型自动理解镜头结构。wan2.7 图生视频支持传入 `driving_audio` 音频素材驱动视频生成。wan2.7 参考生视频支持多主体参考（图像+视频+音色），可通过 `reference_voice` 指定角色音色。

### HappyHorse 系列

HappyHorse 提供文生视频、图生视频、参考生视频和视频编辑四种能力：

- `happyhorse-1.0-t2v`：文生视频
- `happyhorse-1.0-i2v`：图生视频（基于首帧）
- `happyhorse-1.0-r2v`：参考生视频（支持多张参考图像）
- `happyhorse-1.0-video-edit`：视频编辑（指令+参考图）

HappyHorse 支持多地域部署（北京、新加坡、弗吉尼亚、法兰克福），具体可参见 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)。

### 爱诗 PixVerse 系列

PixVerse 提供多个版本（c1/v6/v5.6）的文生视频、图生视频、首尾帧生视频和参考生视频：

- `pixverse/pixverse-c1-t2v`：文生视频（c1 支持多镜头叙事）
- `pixverse/pixverse-c1-it2v`：图生视频
- `pixverse/pixverse-c1-kf2v`：首尾帧生视频
- `pixverse/pixverse-c1-r2v`：参考生视频

PixVerse 使用前需在控制台搜索"PixVerse"并手动开通服务。目前仅适用于北京地域。尺寸参数使用 `size`（如 `"1280*720"`）而非 `resolution`。

### 可灵 Kling 系列

可灵支持文生视频、图生视频、首尾帧生视频、参考生视频和视频编辑：

- `kling/kling-v3-video-generation`：通用视频生成
- `kling/kling-v3-omni-video-generation`：增强版

可灵特色功能包括**智能分镜**（设置 `multi_shot: true`，通过 `multi_prompt` 数组精确控制每个镜头内容和时长）以及 `mode` 参数选择生成质量（`std` 标准 / `pro` 专业）。仅适用于北京地域，需先在控制台开通。

### Vidu 系列

Vidu 提供文生视频、图生视频、首尾帧生视频和参考生视频：

- `vidu/viduq3-turbo_text2video` / `vidu/viduq3-pro_text2video`：文生视频
- `vidu/viduq3-pro_img2video` / `vidu/viduq3-turbo_img2video`：图生视频
- `vidu/viduq3-turbo_start-end2video`：首尾帧生视频
- `vidu/viduq3-mix_reference2video`：参考生视频

Vidu 同样仅适用于北京地域，需先在控制台开通。

## 数字人与人像驱动模型

百炼提供多个专门的人像视频生成模型：

| 模型 | 功能 | 输入 | 适用画幅 |
|------|------|------|---------|
| wan2.2-s2v（数字人） | 说话/唱歌/表演视频生成 | 单张图片 + 音频 | 全身/半身/肖像 |
| 悦动人像 EMO | 唱演视频（口型匹配） | 肖像图片 + 音频 | 肖像/半身 |
| 灵动人像 LivePortrait | 播报视频（轻量快速） | 肖像图片 + 音频 | 肖像 |
| 声动人像 VideoRetalk | 视频口型替换 | 人物视频 + 音频 | 原视频画幅 |
| 舞动人像 AnimateAnyone | 舞蹈/动作迁移 | 人物图片 + 动作模板 | 按模板 |
| 表情包 Emoji | 表情包视频 | 肖像图片 + 预设模板 | 肖像 |

数字人 wan2.2-s2v 和 EMO、LivePortrait、AnimateAnyone 均需先调用对应的 **detect** 模型检测图片合规性，再提交视频生成任务。详见 [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md)。

## 其他视频处理能力

- **视频风格重绘**（`video-style-transform`）：将视频转换为日式漫画、3D卡通、国风水墨等 8 种预设风格，通过 `style` 参数（0-7）选择，参见 [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)。

## 关键参数说明

各模型的参数名称和取值范围不完全一致，以下为常见参数：

| 参数 | 说明 | 备注 |
|------|------|------|
| `model` | 模型名称（必选） | 不同厂商前缀不同 |
| `input.prompt` | 文本提示词 | 支持中英文 |
| `input.media` | 多媒体输入数组（新版协议） | type 可为 `first_frame`/`last_frame`/`video`/`reference_image`/`image_url`/`driving_audio` 等 |
| `parameters.resolution` | 输出分辨率 | 常见值：`480P`/`540P`/`720P`/`1080P`，各模型支持范围不同 |
| `parameters.duration` | 视频时长（秒） | 常见值：5/10/15，部分模型支持更长 |
| `parameters.ratio` / `aspect_ratio` | 宽高比 | 如 `16:9`/`9:16`/`1:1` |
| `parameters.prompt_extend` | 智能改写提示词 | 布尔值，部分模型多镜头必须开启 |
| `parameters.watermark` | 是否添加水印 | 布尔值 |

> **注意**：PixVerse 使用 `size`（如 `"1280*720"`）而非 `resolution` 控制分辨率；可灵使用 `aspect_ratio` 而非 `ratio`；万相旧版协议中图生视频使用 `image_url` / `video_url` 直接字段而非 `media` 数组。选型时务必参照对应模型的 API 文档。

## 地域与端点

| 地域 | 端点 URL |
|------|---------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| 弗吉尼亚 | `https://dashscope-us.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |
| 法兰克福 | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` |

> **注意**：并非所有模型都支持全部地域。PixVerse、Kling、Vidu、数字人系列及人像驱动模型仅支持北京地域。HappyHorse 和万相系列支持多地域。新加坡和法兰克福需将 `{WorkspaceId}` 替换为实际的 Workspace ID。新加坡旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到新版域名。

## 限制与注意事项

- **异步必选**：所有视频生成接口仅支持异步调用，必须设置 `X-DashScope-Async: enable` 请求头。
- **地域一致性**：模型、Endpoint URL 和 API Key 必须属于同一地域，跨地域调用将失败。
- **task_id 有效期**：24 小时内有效，过期后查询返回 `UNKNOWN` 状态。
- **并发限制**：数字人、EMO、LivePortrait 等模型同时处理任务数为 1，其余任务排队等待。
- **第三方模型开通**：PixVerse、Kling、Vidu 需在控制台手动搜索并开通服务后方可调用。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-api-reference/wan-animate-move-api.md)
- [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md)
- [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-animate-mix-api.md)
- [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/animateanyone-quick-start.md)
- [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/emo-quick-start.md)
- [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/liveportrait-quick-start.md)
- [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/emoji-quick-start.md)
- [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/videoretalk.md)
- [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)
- [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-text-to-video-api-reference.md)
- [爱诗-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-image-to-video-api-reference.md)
- [爱诗-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/pixverse-keyframe-to-video-api-reference.md)
- [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-api-reference/pixverse-reference-to-video-api-reference.md)
- [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)
- [Vidu-图生视频-基于首尾帧API参考](../../raw/model-api-reference/video-generation-api/vidu-keyframe-to-video-api-reference.md)
- [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-text-to-video-api-reference.md)
- [Vidu-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/vidu-image-to-video-api-reference.md)
- [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-reference-to-video-api-reference.md)
- [万相-图生视频-基于首帧API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-api-reference.md)
- [万相-首尾帧生视频API参考（2.2）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-image-to-video-by-first-and-last-frame-api-reference.md)
- [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md)
- [万相-文生视频API参考（2.1-2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-text-to-video-api-reference.md)
- [万相-参考生视频API参考（2.6）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wan-reference-to-video-api-reference.md)



