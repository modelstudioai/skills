# 图像、视频与3D生成对比

阿里云百炼平台提供了覆盖多模态内容生成的三大能力：**图像生成**、**视频生成**与**3D 资产生成**。三者都通过 DashScope 网关对外提供服务，共享相似的异步调用范式与鉴权体系，但在支持模型、输入输出格式、接口路径、地域可用性、计费方式和典型应用场景上存在显著差异。本文从技术选型角度对三者做横向对比，帮助开发者根据业务需求快速定位合适的能力。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 支持模型 | 千问 Qwen-Image、万相 Wan/Wanx、Z-Image、可灵 Kling、Vidu 等多家族 | 万相 Wan、HappyHorse、PixVerse、Vidu、可灵 Kling 及多种人像驱动模型 | 仅 Tripo（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`） |
| 核心功能 | 文生图、图生图、图像编辑、局部重绘、扩图、虚拟模特、AI 试衣、创意海报等 | 文生视频、图生视频（首帧/首尾帧/续写）、参考生视频、视频编辑、数字人/口型/舞蹈等 | 文生 3D、单图生 3D、多图生 3D |
| 输入格式 | `prompt` / `messages` / `images`（JPG/PNG/JPEG/BMP/WEBP，[512,4096] 像素，≤10MB） | `input.prompt` + `input.media`（`first_frame`/`last_frame`/`image_url`/`video` 等） | `prompt`（≤1024 字符）/ `image` / `images`（4 元素数组，三者互斥；JPEG/PNG，[20,6000] 像素，≤20MB） |
| 输出格式 | 图像 URL（有效期 24 小时） | 视频 URL（异步返回） | GLB 模型（`pbr_model_url` / `base_model_url`）+ 预览渲染图（下载链接有效期 2 小时） |
| 主要 API 端点 | 多路径：`.../text2image/image-synthesis`、`.../aigc/multimodal-generation/generation`、`.../image-generation/generation` 等 | `POST .../aigc/video-generation/video-synthesis`（部分模型走 `.../aigc/image2video/video-synthesis`） | `POST .../aigc/video-generation/3d-generation` |
| 调用方式 | 以异步为主（`X-DashScope-Async: enable` + 轮询）；新模型支持 HTTP 同步 | 全部异步（创建任务 → 轮询查询） | 全部异步（创建任务 → 轮询，建议 15 秒间隔） |
| 任务耗时 | 通常 1-2 分钟 | 通常 1-5 分钟 | 较长（异步） |
| 地域可用性 | 华北2（北京）、新加坡、美国（弗吉尼亚）等多地域，独立 Key 不可混用 | 万相/HappyHorse 多地域；PixVerse/Vidu/Kling/数字人/人像模型仅北京 | 仅华北2（北京），需该地域 API Key |
| 计费方式 | 仅对成功生成的输出图片计费，含 90 天免费额度 | 多为后付费按视频时长（元/秒）或按张计费 | 按任务成功结果计数（`text-to-3d`/`image-to-3d`/`multi-image-to-3d`） |
| 并发限制 | 主/子账号共享 QPS 与处理中任务数 | 同时处理中任务通常限 1（排队执行） | 查询接口默认 RPS 20 |
| 典型场景 | 电商海报、虚拟模特、AI 试衣、创意插画、图文混排 | 短视频、广告、数字人播报、动画、口型替换 | 游戏/AR/VR 资产、3D 建模、数字孪生 |

## 共性特征

- **统一网关与异步范式**：三者均通过 DashScope 网关调用，且核心流程都是「创建任务获取 `task_id` → 轮询 `GET .../api/v1/tasks/{task_id}`」。创建任务时必须携带 `X-DashScope-Async: enable`，否则报错 `current user api does not support synchronous calls`。
- **`task_id` 有效期均为 24 小时**，切勿重复创建任务，轮询获取即可。
- **地域隔离**：不同地域拥有独立的 API Key 与请求地址，跨地域调用会导致鉴权失败。百炼推荐迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
- **请求体结构**：普遍由 `model` / `input` / `parameters` 三部分组成。

## 各方案适用场景建议

- **图像生成**：适合需要静态视觉内容的场景，模型选择最丰富、地域覆盖最广、计费门槛最低（仅计成功输出图并有免费额度），是多模态生成中最成熟、门槛最低的入口。电商与创意工具（虚拟模特、AI 试衣、创意海报）尤为突出，但需注意部分创意工具模型仅提供免费体验、用尽后不可付费。
- **视频生成**：适合需要动态内容的场景，功能维度最复杂（文生/图生/参考生/编辑/数字人）。选型时优先选用走新版协议、功能最全的万相 wan2.7 系列；若使用 PixVerse、Vidu、Kling 或人像/数字人模型需注意仅限北京地域。计费按时长且并发通常限 1，需评估吞吐与排队成本。
- **3D 生成**：能力最聚焦，仅基于 Tripo 模型，产出带 PBR 材质的 GLB 模型。仅限北京地域、下载链接仅 2 小时有效期，需及时下载与转存。适合游戏、AR/VR、工业设计等对 3D 资产有需求的场景；`Tripo-H3.1` 追求高精度（最高 200 万面），`Tripo-P1.0` 追求速度。

## 技术选型参考

1. **地域约束优先评估**：3D 生成及大量第三方视频模型仅支持北京地域，若业务部署在新加坡/海外，应优先确认图像生成或万相视频系列的多地域可用性。
2. **同步 vs 异步**：仅图像生成的部分新模型（如 `wan2.6-image`、`z-image-turbo`）支持 HTTP 同步一次返回，对低延迟场景友好；视频与 3D 必须异步轮询，需在客户端实现任务状态管理。
3. **输出有效期差异**：图像/视频结果与 `task_id` 有效期 24 小时，而 3D 产物下载链接仅 2 小时，集成 3D 时务必在回调或轮询成功后立即下载转存。
4. **计费模型差异**：图像按成功输出图计费且有免费额度、门槛最低；视频按时长计费、并发受限、成本更高；3D 按成功任务计数。批量或高并发场景需据此估算成本与吞吐。
5. **接口路径不统一**：三大能力乃至同一能力内不同模型的接口路径都可能不同（尤其图像与视频），接入前务必以对应模型的官方文档为准。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


