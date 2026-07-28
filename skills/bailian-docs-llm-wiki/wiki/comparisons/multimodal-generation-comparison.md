# 图像、视频与3D生成对比

百炼平台在[多模态](../concepts/multimodal.md)内容生成方向提供了三大类 API：**图像生成与编辑**、**视频生成**和 **3D 模型生成**。三者在底层模型生态、输入输出形态、调用模式（同步/异步）、接口路径与计费方式上差异明显。本页从开发者技术选型的角度，对这三类能力做横向对比，帮助你快速判断应接入哪类 API、选择哪个模型系列，以及集成时需要注意哪些约束。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
| --- | --- | --- | --- |
| 核心任务 | 文生图、图像编辑、图像翻译、局部重绘、虚拟模特、试衣、海报、扩图、擦除补全等 | 文生视频、图生视频（首帧/首尾帧）、参考生视频、视频编辑、风格重绘、超清、对口型、数字人/人像动画 | 文生3D、单图生3D、多图生3D |
| 模型生态 | 千问图像（Qwen-Image）、万相（Wan）、Z-Image、可灵（Kling）、Vidu 及多种创意工具类模型 | 万相（wan2.1–2.7）、HappyHorse、爱诗（PixVerse）、Vidu、可灵（Kling）、AnimateAnyone/EMO/LivePortrait 等人像动画模型 | Tripo 系列（Tripo-H3.1、Tripo-P1.0） |
| 输入格式 | 文本提示词、图像（单图/多图）、涂抹区域、手绘草图等 | 文本提示词、图像（首帧/首尾帧/参考图）、音频、视频（[多模态](../concepts/multimodal.md)组合） | 文本提示词，或单图（JPEG/PNG），或固定 4 视角多图（前/左/后/右，`prompt`/`image`/`images` 三选一互斥） |
| 输出格式 | PNG 图像，1–9 张，分辨率 512×512~2048×2048 或 1K/2K/4K | 视频文件（各系列时长、分辨率、镜头能力不同，PixVerse 可 4K 超清） | GLB 三维模型（PBR 材质或无贴图）+ 预览渲染图 |
| 调用模式 | 同步（千问图像、万相 2.6+、Z-Image 推荐）与异步（万相 2.5 及以下、可灵、Vidu、创意工具类）并存 | 统一异步（创建任务 → 轮询结果） | 强制异步，必须携带 `X-DashScope-Async: enable` |
| 典型 API 端点 | 同步：`/services/aigc/multimodal-generation/generation`；异步：`/services/aigc/text2image/image-synthesis`、`/services/aigc/image2image/image-synthesis` 等（按功能细分） | 各模型家族对应的视频生成任务端点（异步创建 + `GET /api/v1/tasks/{task_id}` 轮询） | `POST /services/aigc/video-generation/3d-generation` + `GET /api/v1/tasks/{task_id}` |
| 地域限制 | 常规地域可用 | 部分三方模型（PixVerse、Vidu、Kling）需在控制台先开通 | 仅华北2（北京）地域，必须使用北京地域 API Key |
| 结果有效期 | 图像 URL 有效期 24 小时（异步 task_id 24 小时） | task_id 24 小时，结果 URL 需及时下载 | task_id 24 小时；模型文件/渲染图 URL 仅 2 小时 |
| 计费方式 | 按张计费；部分创意工具类模型仅免费体验（额度用完不可付费续用） | 按任务/时长计费，不同模型家族价格不同；三方模型需单独开通 | 按任务计费，Tripo 服务需在控制台开通 |
| 关键参数 | `prompt`、`negative_prompt`、`size`、`n`、`style`、`watermark`、`prompt_extend` | `prompt`、首帧/首尾帧图像、`mode`、`aspect_ratio`、`duration`、`audio`、`function`（旧版统一编辑模型） | `texture_quality`、`geometry_quality`（仅 H3.1）、`pbr`、`texture` |

## 能力与复杂度差异

- **图像生成**能力矩阵最宽：除基础文生图/编辑外，还覆盖图像翻译、虚拟模特、AI 试衣、海报生成等垂直场景，且新版模型（千问图像、万相 2.6+、Z-Image）支持同步调用，集成最简单、延迟最低。
- **视频生成**模型家族最多、任务类型最细：从通用文生/图生视频到参考生视频、视频编辑、对口型、动作迁移、数字人均有覆盖，但全部走异步任务模式，需要实现轮询逻辑；部分能力（如万相数字人 wan2.2-s2v）还有前置检测步骤。
- **3D 生成**接口最收敛：仅 Tripo 两个模型、三种输入方式，但限制最多——地域锁定北京、强制异步、产物 URL 仅 2 小时有效，工程上必须做好即时下载与持久化。

## 适用场景建议

| 场景 | 推荐方案 |
| --- | --- |
| 电商主图、海报、社媒配图、文字渲染 | 图像生成（千问图像擅长复杂文字渲染，万相支持多种艺术风格） |
| 已有图片的修改、多图融合、去水印、扩图、超分 | 图像编辑（千问图像编辑 / 万相图像编辑） |
| 短视频创作、广告分镜、单/多镜头叙事 | 视频生成（wan2.7 文生视频支持自然语言分镜，可灵 v3-omni 支持智能分镜） |
| 角色一致性的系列视频、IP 内容 | 参考生视频（wan2.7-r2v、pixverse-c1-r2v、vidu reference2video） |
| 数字人播报、口播、唱演 | wan2.2-s2v、EMO、LivePortrait、pixverse-lipsync 等人像动画类模型 |
| 游戏资产、AR/VR、商品三维展示 | 3D 生成（高精度选 Tripo-H3.1 ultra 模式，追求速度选 Tripo-P1.0） |

## 选型要点

1. **延迟敏感选同步图像生成**：只有图像类新版模型提供同步调用；视频与 3D 一律异步，需按 15 秒左右间隔轮询任务状态。
2. **统一轮询逻辑可复用**：视频与 3D 的异步协议一致（创建任务拿 `task_id` → `GET /api/v1/tasks/{task_id}`，状态 PENDING → RUNNING → SUCCEEDED/FAILED），可以抽象成同一套任务轮询组件。
3. **注意产物时效**：三类结果 URL 都有有效期，3D 的 2 小时最短，务必在回调/轮询成功后立即转存到自有存储（如 OSS）。
4. **确认开通与地域**：三方视频模型（PixVerse、Vidu、Kling）和 Tripo 均需先在控制台开通；3D 生成还要求北京地域 API Key，跨地域调用会直接失败。
5. **免费体验模型不适合生产**：图像类的部分创意工具模型（虚拟模特、海报生成、擦除补全等）仅提供免费额度且不可付费续用，生产环境应优先选择千问图像编辑或万相 2.1+ 图像编辑等付费模型。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


