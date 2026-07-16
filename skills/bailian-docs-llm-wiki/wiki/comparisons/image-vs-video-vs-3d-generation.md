# 图像、视频与 3D 生成对比

阿里云百炼平台在 DashScope 网关上提供了图像、视频与 3D 三大类视觉内容生成能力。三者虽同属「生成式媒体」范畴、共用同一套鉴权与任务模型，但在输入输出格式、可用模型、调用协议、地域限制与产物形态上差异明显。本文面向开发者，横向梳理三类方案的关键维度，帮助在技术选型时快速判断该用哪一类 API。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 主要能力 | 文生图、图像编辑、图像翻译、垂直创意工具（虚拟模特、扩图、擦除补全、海报等） | 文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、数字人、人像驱动、超清、对口型 | 文生 3D、单图生 3D、多图生 3D |
| 典型输入 | `prompt` / `negative_prompt`；编辑类传 `image_url`/`images`/`mask_image_url`；新版用 `messages` 多模态结构 | 文生用 `prompt`；图生/参考/编辑用 `media` 数组或 `image_url`/`video_url`/`audio_url`/`first_frame`/`last_frame` 等 | `prompt`（≤1024 字符）/ `image`（单图）/ `images`（4 元数组：前左后右），三者互斥 |
| 输出格式 | 图像 URL（有效期 24 小时），分辨率随模型而异（如 512×512~2048×2048、1K/2K/4K） | 视频 URL，分辨率 480P/540P/720P/1080P、可设 `duration` | 带贴图 PBR 材质 GLB（`pbr_model_url`）或无贴图基础模型（`base_model_url`）+ 预览渲染图，下载链接**仅 2 小时** |
| 代表模型 | Qwen-Image、万相 Wan/WanX（t2i/imageedit）、Z-Image、可灵、Vidu 等 | 万相 Wan 2.1-2.7、PixVerse、Vidu、可灵 Kling、HappyHorse、EMO/LivePortrait 等 | `Tripo/Tripo-H3.1`（最高 200 万面）、`Tripo/Tripo-P1.0`（最高 2 万面，速度更快） |
| 调用协议 | 异步（主流）+ **HTTP 同步**（仅 wan2.6/2.7、z-image 等新版） | **全部异步**（创建任务 → 轮询），无同步 | **全部异步**（创建任务 → 轮询），无同步 |
| 典型端点 | `text2image/image-synthesis`、`image2image/image-synthesis`、`multimodal-generation/generation`、`virtualmodel/generation` 等多种 | `video-generation/video-synthesis`（主）、部分数字人用 `image2video/video-synthesis` | `video-generation/3d-generation`（单一端点） |
| 生成耗时 | 通常 1-2 分钟 | 通常 1-5 分钟（统一编辑约 5-10 分钟） | 较长，建议轮询间隔约 15 秒 |
| 地域可用性 | 华北2（北京）为主，部分模型也支持新加坡/美国；大量创意工具**仅北京** | 华北2（北京）为主，第三方模型多**仅北京**，万相等部分支持新加坡/美国/德国 | **仅华北2（北京）** |
| 计费方式 | 仅对成功输出图片计费，含免费额度（通常 500 张/90 天），主子账号共享 | 按成功任务计费，随模型与分辨率/时长而异 | 仅对成功结果计数，`usage` 记录任务类型/数量/质量 |
| 关键请求头 | `Authorization`、`Content-Type`；异步需 `X-DashScope-Async: enable` | 同左，异步必带 `X-DashScope-Async: enable` | 同左，异步必带 `X-DashScope-Async: enable` |
| 任务状态 | `PENDING`/`RUNNING`/`SUSPENDED`/`SUCCEEDED`/`FAILED` | 同类异步枚举，过期返回 `UNKNOWN` | `PENDING`/`RUNNING`/`SUCCEEDED`/`FAILED`/`CANCELED`/`UNKNOWN` |

## 共性与差异要点

**共性**：三者都基于 DashScope 网关，共用 `Authorization: Bearer $DASHSCOPE_API_KEY` 鉴权、`model`/`input`/`parameters` 的请求体结构，异步模式均为「创建任务拿 `task_id` → 轮询查询」，且 `task_id` 有效期统一为 24 小时、创建异步任务必须携带 `X-DashScope-Async: enable`。地域隔离规则也一致：模型、Endpoint 与 API Key 必须同地域，跨地域会鉴权失败。

**核心差异**：

- **协议丰富度**：只有图像生成的部分新版模型（wan2.6/2.7、z-image）支持一次请求返回结果的 HTTP 同步调用；视频与 3D **全部只能异步**。
- **地域自由度**：图像与视频在北京之外还有一定跨地域支持，而 3D 生成**只有华北2（北京）**可用，选型时需特别注意。
- **产物时效**：图像/视频 URL 有效期 24 小时，而 3D 模型下载链接**仅 2 小时**，需在生成后尽快下载并转存。
- **输入约束**：3D 的 `prompt`/`image`/`images` 三者互斥，多图必须是固定 4 元数组（前左后右）；图像与视频则允许更灵活的多模态、多图输入组合。

## 适用场景建议

- **图像生成**：适合海报、电商主图、创意配图、虚拟模特试衣、图像翻译/编辑等静态视觉需求。追求低延迟、希望一次请求出结果时，优先选支持 HTTP 同步的新版模型（wan2.6/2.7、z-image-turbo）；需要精细编辑（改文字、局部重绘、扩图、去水印）则用千问/万相编辑系列。
- **视频生成**：适合短视频、广告片、数字人播报、口播/对口型、人像驱动等动态内容。需明确任务类型（文生/图生/首尾帧/参考/编辑）选择对应模型，注意多镜头控制方式在不同模型间不一致（万相 2.7、PixVerse-c1 用自然语言 `prompt`，旧版万相 2.6 需显式 `shot_type: "multi"` + `prompt_extend: true`）。
- **3D 生成**：适合游戏/电商/XR 场景的 3D 资产快速建模。需要高精度、高面数选 `Tripo/Tripo-H3.1`（可用 `geometry_quality: ultra` 达 200 万面）；追求速度、面数需求不高选 `Tripo/Tripo-P1.0`。务必在北京地域开通 Tripo 服务并及时下载 2 小时时效的产物。

## 技术选型参考

1. **先按产物形态定类别**：要静态图片 → 图像；要动态视频 → 视频；要可交互 3D 模型（GLB） → 3D。
2. **再评估延迟要求**：对响应速度敏感的图像场景可用同步协议；视频与 3D 必须做好异步轮询与任务状态处理（含 `FAILED`/`UNKNOWN`）。
3. **确认地域与开通**：3D 与多数第三方视频/图像创意模型只在北京可用，需保证模型、Endpoint、API Key 同地域，并提前在控制台开通授权（如 Tripo）。
4. **规划产物存储**：所有产出均为限时 URL，建议生成后立即转存至 OSS，其中 3D 仅 2 小时窗口最需注意。
5. **统一工程实现**：三类 API 共用鉴权、请求头与异步模型，可复用同一套任务提交/轮询/重试封装，仅按 `model` 与端点差异做分支。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


