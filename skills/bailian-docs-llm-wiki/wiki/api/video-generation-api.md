# video generation api

阿里云百炼平台提供丰富的视频生成 API，涵盖通用视频生成（文生视频、图生视频、首尾帧生视频、参考生视频、视频编辑）与人物驱动视频（数字人、动作迁移、口型替换、唱演/播报/表情包）以及视频风格重绘等能力。平台聚合了万相（Wan）、HappyHorse、爱诗 PixVerse、可灵 Kling、Vidu 等多家模型，所有接口统一通过 DashScope [异步任务](../concepts/async-task.md)协议调用。

## 通用调用协议

所有视频生成 API 均采用**[异步任务](../concepts/async-task.md)协议**，整个流程分两步：

1. **创建任务**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（部分人物类模型使用 `/image2video/video-synthesis`）。请求头必须带 `X-DashScope-Async: enable`、`Authorization: Bearer $DASHSCOPE_API_KEY`、`Content-Type: application/json`。
2. **轮询结果**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`。`task_id` 有效期 24 小时，**切勿重复创建任务**。

任务耗时通常为 1–5 分钟（视频编辑统一模型约 5–10 分钟）。请求体核心字段：

- `model`：模型名（如 `wan2.7-t2v`、`happyhorse-1.0-t2v`、`kling/kling-v3-video-generation`）
- `input.prompt`：文本提示词
- `input.media`：媒体素材数组，元素 `type` 可选 `first_frame` / `last_frame` / `reference_image` / `reference_video` / `video` / `image_url` / `driving_audio` 等
- `parameters`：`resolution`（480P/540P/720P/1080P）、`ratio` 或 `size`、`duration`、`prompt_extend`、`watermark`、`audio`、`shot_type` 等

详见 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md) 与 [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)。

## 多地域 Endpoint

模型、Endpoint URL、API Key **必须属于同一地域**，跨地域调用会失败。

| 地域 | HTTP Endpoint |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/api/v1/...` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/...`（旧版 `dashscope-intl.aliyuncs.com` 即将下线） |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/api/v1/...` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/...` |

新加坡/法兰克福 URL 中 `{WorkspaceId}` 需替换为真实 [Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

## 通用视频生成模型

### 万相 Wan（推荐首选）

万相是阿里云自研视频生成大模型，当前主推 **wan2.7 系列**（新版协议），早期 wan2.6 / wan2.5 / wan2.2 / wanx2.1 走旧版协议。

| 能力 | 模型 | 文档 |
| --- | --- | --- |
| 文生视频 | `wan2.7-t2v`、`wan2.6-t2v` 等 | [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md) |
| 图生视频（首帧 / 首尾帧 / 续写统一） | `wan2.7-i2v-*` | [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md) |
| 参考生视频（多模态多角色） | `wan2.7-r2v` | [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md) |
| 视频编辑（指令编辑 / 视频迁移） | `wan2.7-videoedit` | [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md) |
| 视频编辑统一模型（多图参考/重绘等） | `wanx2.1-vace-plus` | [万相-视频编辑API参考（2.1）](../../raw/model-api-reference/video-generation-api/legacy-video-models/legacy-wanx-vace-api-reference.md) |

**wan2.7 关键特性**：

- 文生视频支持**多镜头叙事**：在 `prompt` 中用自然语言描述分镜（如"第1个镜头[0-3秒] 全景：…"）或写"生成多镜头视频"，无需配置 `shot_type`。
- 图生视频新版协议统一支持首帧生视频、首尾帧生视频、视频续写三种任务，**推荐优先使用**，旧版 `legacy-image-to-video-api-reference` 仅支持首帧。
- 支持 `input.audio_url` 传入自定义音频。
- 参考生视频支持 `reference_voice` 为每个参考主体绑定独立音色。

> **注意**：wan2.7 模型必须使用**新版协议**，旧版协议（`wan2.6-t2v` / `wan2.6-i2v-flash` / `wan2.6-r2v-flash` 等）仅支持 wan2.6 及更早模型。两者 Endpoint 相同但 `media` 结构与参数有差异，不要混用。

### HappyHorse

HappyHorse 系列覆盖文生视频、图生视频（首帧）、参考生视频（多图）、视频编辑（指令+参考图）四种能力，模型名：

- `happyhorse-1.0-t2v` / `happyhorse-1.0-i2v` / `happyhorse-1.0-r2v` / `happyhorse-1.0-video-edit`

详见 [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md) 至 [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)。参考生视频支持 `[Image 1]`、`[Image 2]` 占位符在 [prompt](../guides/prompt.md) 中引用 media 数组中的参考图。

### 爱诗 PixVerse

PixVerse 提供 c1 / v6 / v5.6 三个档位，覆盖文生视频、图生视频（首帧 / 首尾帧 / 参考生视频），部分场景支持**多镜头**与**自带音频**（`audio: true`）。

| 能力 | 模型示例 |
| --- | --- |
| 文生视频 | `pixverse/pixverse-c1-t2v`、`pixverse/pixverse-v6-t2v` |
| 图生视频（首帧） | `pixverse/pixverse-c1-it2v` |
| 首尾帧生视频 | `pixverse/pixverse-c1-kf2v` |
| 参考生视频（支持 `ref_name`） | `pixverse/pixverse-c1-r2v` |

需先在百炼控制台搜索 **PixVerse** 开通服务。详见 [爱诗-文生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-text-to-video-api-reference.md) 至 [爱诗-参考生视频API参考](../../raw/model-api-reference/video-generation-api/pixverse-reference-to-video-api-reference.md)。

### 可灵 Kling

可灵视频生成统一接口支持文生视频、图生视频（首帧 / 首尾帧）、参考生视频、视频编辑五种能力：

- `kling/kling-v3-omni-video-generation`、`kling/kling-v3-video-generation`

文生视频支持 `multi_shot: true` + `shot_type: customize` + `multi_prompt` 数组实现**智能分镜**，每个分镜可独立设置 `prompt` 与 `duration`。需先在控制台搜索"可灵 AI"开通。详见 [可灵-视频生成API文档](../../raw/model-api-reference/video-generation-api/kling-video-generation-api-reference.md)。

### Vidu

Vidu 提供 q3-pro / q3-turbo / q2 系列，覆盖文生视频、图生视频（首帧 / 首尾帧）、参考生视频：

- 文生视频：`vidu/viduq3-pro_text2video`、`vidu/viduq3-turbo_text2video`、`vidu/viduq2_text2video`
- 图生视频：`vidu/viduq3-pro_img2video` 等
- 首尾帧：`vidu/viduq3-pro_start-end2video` 等
- 参考生视频：`vidu/viduq3-mix_reference2video`（仅图像）、`vidu/viduq2-pro_reference2video`（图像+视频）

[prompt](../guides/prompt.md) 支持中英文，最长 5000 字符，超出自动截断。需先在控制台搜索 **Vidu** 开通。详见 [Vidu-文生视频API参考](../../raw/model-api-reference/video-generation-api/vidu-text-to-video-api-reference.md) 至 [Vidu-参考生视频 API 参考](../../raw/model-api-reference/video-generation-api/vidu-reference-to-video-api-reference.md)。

## 人物驱动视频

以下模型聚焦"以人物为中心"的视频生成，**多数仅限华北2（北京）地域**，调用前务必确认地域匹配。

### 数字人 / 说话视频

| 模型 | 输入 | 能力 | 文档 |
| --- | --- | --- | --- |
| `wan2.2-s2v` + `wan2.2-s2v-detect` | 单张图片 + 音频 | 说话 / 唱歌 / 表演视频，支持肖像、半身、全身画幅，卡通形象 | [万相-数字人](../../raw/model-api-reference/video-generation-api/wan-s2v-overview.md) |
| `emo-v1` + `emo-detect-v1` | 肖像图 + 人声音频 | 悦动人像 EMO，擅长人物特写，口型表情自然；三种风格强度 `calm/normal/active` | [图生唱演视频-悦动人像EMO](../../raw/model-api-reference/video-generation-api/emo-quick-start.md) |
| `liveportrait` + `liveportrait-detect` | 肖像图 + 人声音频 | 灵动人像 LivePortrait，轻量快速生成肖像播报视频 | [图生播报视频-灵动人像LivePortrait](../../raw/model-api-reference/video-generation-api/liveportrait-quick-start.md) |
| `videoretalk` | 人物视频 + 人声音频 | 声动人像 VideoRetalk，**替换原视频口型**使之匹配新音频 | [视频口型替换-声动人像VideoRetalk](../../raw/model-api-reference/video-generation-api/videoretalk.md) |

**选型建议**：需要全身/大半身、动作幅度大或卡通形象 → `wan2.2-s2v`；追求肖像特写且口型自然 → EMO；轻量播报 → LivePortrait；已有视频换配音 → VideoRetalk。

数字人调用流程通常需先调 detect 接口校验图片合规，再用异步接口提交生成任务。

### 动作迁移与视频换人

| 模型 | 能力 | 文档 |
| --- | --- | --- |
| `wan2.2-animate-move`（`wan-std` / `wan-pro`） | 图生动作：将参考视频中的动作/表情迁移到人物图片，适用于舞蹈/肢体/影视复刻 | [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-animate-move-api.md) |
| `wan2.2-animate-mix`（`wan-std` / `wan-pro`） | 视频换人：保留原视频场景/动作/光照，把主角替换为图片中的人物 | [万相-视频换人API参考](../../raw/model-api-reference/video-generation-api/wan-animate-mix-api.md) |
| `animate-anyone-gen2` + template + detect | 舞动人像 AnimateAnyone：基于人物图片+动作模板生成舞蹈视频，支持模型调用与独占部署两种模式 | [图生舞蹈视频-舞动人像AnimateAnyone](../../raw/model-api-reference/video-generation-api/animateanyone-quick-start.md) |

### 表情包视频

`emoji` 系列基于肖像图与**预设动态模板**生成表情包视频，流程：

1. 调 `emoji-detect` 获取人脸区域与表情包动态区域坐标
2. 调 `emoji` 视频生成接口，传入检测通过的图片、坐标与模板 ID（如 `jingdian_xianqi`、`mengwa_kaixin`）

详见 [图生表情包视频-表情包Emoji](../../raw/model-api-reference/video-generation-api/emoji-quick-start.md)。

## 视频风格重绘

`video-style-transform` 模型可将输入视频转换为 8 种预设艺术风格，保持画面动态流畅与内容连贯：

- 日式漫画、美式漫画、清新漫画、3D 卡通、国风卡通、纸艺风格、简易插画、国风水墨

请求体：`input.video_url` 传入原视频 URL，`parameters.style` 为风格编号（0–7），`parameters.video_fps` 控制帧率。支持 720P / 540P 输出。详见 [视频风格重绘API参考](../../raw/model-api-reference/video-generation-api/video-style-transform-api-reference.md)。

## 关键参数速查

| 参数 | 说明 |
| --- | --- |
| `resolution` | 输出分辨率：`480P` / `540P` / `720P` / `1080P`，不同模型支持档位不同 |
| `ratio` / `size` | 宽高比（如 `16:9`）或像素尺寸（如 `1280*720`），不同模型字段名不同 |
| `duration` | 视频时长，单位秒，常见 5 / 10 / 15 |
| `prompt_extend` | 是否开启智能改写（优化 [prompt](../guides/prompt.md)、多镜头必填 `true`） |
| `shot_type` | `multi` 启用多镜头（旧版模型），wan2.7 由 [prompt](../guides/prompt.md) 自然语言控制 |
| `watermark` | 是否添加水印 |
| `audio` | PixVerse 等支持自动生成配乐 |
| `multi_shot` + `multi_prompt` | Kling 专用智能分镜，每个子项独立 `prompt` 和 `duration` |
| `mode` | 模式档位：`wan-std` / `wan-pro`（animate-move/animate-mix）、`std` / `pro`（Kling）、Vidu 的 `pro` / `turbo` |

## 计费与限流要点

- 所有模型按**生成视频时长**或**图片张数**后付费计费，单价差异较大（如 `liveportrait` 0.02 元/秒、`wan2.2-s2v` 720P 0.9 元/秒、`videoretalk` 0.08 元/秒）。
- 大多数生成接口**同一时刻只允许 1 个作业实际运行**，其余排队；RPS 一般在 1–5。
- 舞动人像 AnimateAnyone、悦动人像 EMO 等除"模型调用"外还支持**独占部署**模式（预付费算力单元），适合高并发场景。
- 各模型均有免费额度，详见百炼控制台的[新免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)说明。

## 常见注意事项

- **必须异步**：HTTP 接口不支持同步，缺 `X-DashScope-Async: enable` 会报 "current user api does not [support](../guides/support.md) synchronous calls"。
- **同地域三要素一致**：模型、Endpoint URL、API Key 必须都属于同一地域。
- **task_id 24 小时有效**：过期查询会返回 `UNKNOWN`；已创建的任务**不要重复提交**，只需轮询。
- **新加坡旧域名迁移**：`dashscope-intl.aliyuncs.com` 即将下线，需迁移到 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。
- **图片/视频 URL 可访问性**：媒体 URL 必须公网可达，部分模型也支持 Base64 编码（如 wan2.2 首尾帧）。
- **人物类模型多需 detect 前置**：EMO / LivePortrait / Emoji / AnimateAnyone / 数字人均需先调检测接口确认图片合规，再用生成接口提交任务。
- **PixVerse / Kling / Vidu 需单独开通**：这三家为第三方模型，需在百炼控制台搜索对应模型卡片点"立即开通"。

## 来源文档

- [HappyHorse-文生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-text-to-video-api-reference.md)
- [HappyHorse-图生视频-基于首帧API参考](../../raw/model-api-reference/video-generation-api/happyhorse-image-to-video-api-reference.md)
- [HappyHorse-参考生视频API参考](../../raw/model-api-reference/video-generation-api/happyhorse-reference-to-video-api-reference.md)
- [HappyHorse-视频编辑API参考](../../raw/model-api-reference/video-generation-api/happyhorse-video-edit-api-reference.md)
- [万相2.7-文生视频API参考](../../raw/model-api-reference/video-generation-api/text-to-video-api-reference.md)
- [万相2.7-图生视频API参考](../../raw/model-api-reference/video-generation-api/image-to-video-general-api-reference.md)
- [万相2.7-参考生视频API参考](../../raw/model-api-reference/video-generation-api/wan-video-to-video-api-reference.md)
- [万相2.7-视频编辑API参考](../../raw/model-api-reference/video-generation-api/wan-video-editing-api-reference.md)
- [万相-图生动作API参考](../../raw/model-api-reference/video-generation-api/wan-animate-move-api.md)
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



