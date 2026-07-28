# [多模态](../concepts/multimodal.md)生成 API 对比

百炼平台提供三大类[多模态](../concepts/multimodal.md)生成能力：图像生成、3D 资产生成和视频生成。三者均通过 DashScope 网关以 REST / SDK 方式调用，且由于生成耗时较长，大多采用 `X-DashScope-Async: enable` 异步"创建任务 → 轮询 task_id"的两步流程。本文从输入格式、输出格式、支持模型、API 端点、调用模式、计费与典型场景等维度对三者进行对比，帮助开发者根据业务需求做技术选型。

## 关键维度对比

| 维度 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| **输入格式** | 文本 [prompt](../guides/prompt.md)（文生图）；参考图 URL + [prompt](../guides/prompt.md)（图生图 / 图像编辑）；多图参考（部分模型支持） | 三选一：文本 [prompt](../guides/prompt.md)（文生 3D）；单图 URL（单图生 3D）；4 视角图片数组（多图生 3D） | 文本 prompt（文生视频）；首帧/首尾帧图像 URL（图生视频）；参考图 + prompt（参考生视频）；视频 URL（视频编辑/超分等） |
| **输出格式** | 静态图像（JPEG/PNG），支持 1~6 张 | GLB 格式 3D 模型（带 PBR 材质或无贴图）+ 预览渲染图 | 视频文件（MP4 等），含分辨率、时长、可选音频 |
| **支持模型** | Qwen-Image / Qwen-Image-Edit、万相 wan2.7/2.6/2.5/2.2/v1、Z-Image、Kling、Vidu、创意工具系列 | Tripo/Tripo-H3.1（高精度）、Tripo/Tripo-P1.0（专业快速） | 万相 wan2.7/2.6/2.2、HappyHorse、PixVerse、Vidu、Kling、人像动画系列 |
| **API 端点** | 文生图/编辑：`/api/v1/services/aigc/text2image/image-synthesis`（异步）或 HTTP 同步（wan2.7/2.6/z-image/qwen-image）；查询：`/api/v1/tasks/{task_id}` | 创建：`/api/v1/services/aigc/video-generation/3d-generation`；查询：`/api/v1/tasks/{task_id}` | 创建：`/api/v1/services/aigc/video-generation/video-synthesis`；查询：`/api/v1/tasks/{task_id}` |
| **调用模式** | 异步为主（`X-DashScope-Async: enable`）；wan2.7/2.6/z-image/qwen-image 支持同步 | 仅异步（`X-DashScope-Async: enable` 必选） | 仅异步（`X-DashScope-Async: enable` 必选） |
| **地域限制** | 部分模型仅北京地域（wanx-v1、创意工具系列） | 仅华北2（北京） | 需模型、Endpoint、[API Key](../concepts/api-key.md) 同一地域（北京/新加坡/美国/德国） |
| **输出分辨率** | 512×512 ~ 2048×2048（部分 4K） | 面数最高 200 万（H3.1）/2 万（P1.0） | 480P ~ 1080P，部分支持 4K |
| **产物有效期** | — | GLB 下载链接 2 小时 | task_id 有效期 24 小时 |
| **task_id 有效期** | 24 小时 | 24 小时 | 24 小时 |
| **典型计费** | 按张计费（如 wanx-v1 0.16 元/张）；部分创意工具免费体验 | 按任务类型计费 | 按视频时长/分辨率计费 |
| **典型耗时** | 秒级（同步）至数十秒（异步） | 分钟级 | 分钟级 |

## 调用流程对比

三者均遵循异步两步流程，但端点路径和请求头要求有所不同：

| 步骤 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| 创建任务 | POST 图像合成端点 | POST `/api/v1/services/aigc/video-generation/3d-generation` | POST `/api/v1/services/aigc/video-generation/video-synthesis` |
| 异步头 | 大多数需要 `X-DashScope-Async: enable` | **必选** | **必选** |
| 轮询查询 | GET `/api/v1/tasks/{task_id}` | GET `/api/v1/tasks/{task_id}` | GET `/api/v1/tasks/{task_id}` |
| 轮询建议 | — | 约 15 秒间隔 | — |
| 查询 RPS | — | 默认 20 | — |
| 状态枚举 | PENDING/RUNNING/SUCCEEDED/FAILED | PENDING/RUNNING/SUCCEEDED/FAILED/CANCELED/UNKNOWN | PENDING/RUNNING/SUCCEEDED/FAILED/UNKNOWN |

## 输入参数对比

| 参数类型 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| **prompt** | 支持，中英文文本 | 支持，最大 1024 字符 | 支持，中英文 |
| **图像输入** | 参考图 URL（图生图/编辑） | 单图 URL 或 4 视角图片数组 | 首帧/尾帧 URL（图生视频）；参考图（参考生视频） |
| **[多模态](../concepts/multimodal.md)数组** | 部分模型支持多图参考 | images 数组（固定 4 元素，视角顺序前/左/后/右） | media 数组（first_frame/last_frame/image_url/video/audio_url/reference_image） |
| **分辨率参数** | 宽高自由设置 | texture_quality / geometry_quality | resolution / size（480P~4K） |
| **数量参数** | 1~6 张 | count 固定 1 | duration（秒）、seed、watermark 等 |

## 适用场景建议

### 图像生成

- **需要高文本渲染质量**（海报、配图含文字排版）→ 优先选择 Qwen-Image 系列。
- **追求高性价比的通用文生图** → Z-Image-Turbo 或万相 wan2.6 系列。
- **图像编辑需求**（改字、增删物体、风格迁移）→ Qwen-Image-Edit 或万相 wan2.7-image 编辑能力。
- **创意工具场景**（虚拟模特、涂鸦作画、创意海报）→ 对应专项工具模型，但注意部分仅北京地域或免费体验。
- **需要 HTTP 同步调用简化集成** → 选择 wan2.7 / wan2.6 / z-image / qwen-image 等支持同步的模型。

### 3D 生成

- **游戏/影视高精度 3D 资产** → Tripo/Tripo-H3.1，最高 200 万面，支持 PBR 材质。
- **快速原型/预览** → Tripo/Tripo-P1.0，面数较低但速度更快。
- **无贴图基础模型需求** → 同时将 `texture` 和 `pbr` 设为 `false`，获取 `base_model_url`。
- **注意**：仅限北京地域 [API Key](../concepts/api-key.md)，开通前需在控制台模型市场搜索 Tripo 并完成授权。

### 视频生成

- **最新推荐体验** → 万相 wan2.7（新版协议），支持图生视频首帧/首尾帧/续写、文生视频、参考生视频及视频编辑。
- **旧版项目兼容** → wan2.6 及早期模型走旧版协议（图生视频仅首帧）。
- **需要 4K 超清或对口型/动作模仿** → PixVerse 系列（pixverse-c1/v6/upscale/lipsync/motioncontrol）。
- **智能分镜、多主体参考** → 可灵 Kling（kling-v3 / kling-v3-omni）。
- **人像动画/数字人** → animate-anyone / emo / liveportrait / wan2.2-s2v 等系列。
- **注意路径差异**：万相图生动作（wan2.2-animate-move）、视频换人（wan2.2-animate-mix）、数字人（wan2.2-s2v）使用 `image2video/video-synthesis` 路径，而非 `video-generation/video-synthesis`。

## 技术选型总结

| 选型场景 | 推荐方案 | 关键考量 |
| --- | --- | --- |
| 静态营销素材 / 产品配图 | 图像生成（Qwen-Image / Z-Image） | 文本渲染质量、输出张数、同步调用可用性 |
| 电商虚拟模特 / 创意海报 | 图像生成创意工具（wanx-virtualmodel / wanx-poster） | 地域限制、部分免费体验 |
| 游戏/影视 3D 资产 | 3D 生成（Tripo-H3.1） | 面数精度、PBR 材质、仅北京地域 |
| 快速 3D 原型验证 | 3D 生成（Tripo-P1.0） | 速度优先、面数较低 |
| 短视频/广告素材 | 视频生成（wan2.7 / Kling） | 分辨率、时长、多镜头分镜 |
| 人像动画 / 数字人 | 视频生成（animate-anyone / wan2.2-s2v） | 口型同步、动作模仿、路径差异 |
| 超清/对口型视频 | 视频生成（PixVerse upscale / lipsync） | 4K 超分、对口型能力 |

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


