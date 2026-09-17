# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D内容生成（3D Generation）三大核心能力模块。对比聚焦于**工程落地关键维度**，涵盖调用方式、模型生态、输入输出约束、计费逻辑及典型适用场景，旨在为技术选型提供客观、可执行的决策依据。

---

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D内容生成（3D Generation） |
|------|------------------------------|------------------------------|-----------------------------|
| **统一 API 端点** | `POST /v1/images/generations`（所有模型共用） | 无统一端点：<br>• 通用模型：`/api/v1/services/aigc/video-generation/video-synthesis`<br>• 人像驱动类：`/api/v1/services/aigc/image2video/...`（华北2专属） | `POST /api/v1/services/aigc/video-generation/3d-generation`（仅华北2） |
| **调用模式** | 同步响应（毫秒级返回结果 URL） | **强制异步**：需创建任务 + 轮询 `GET /api/v1/tasks/{task_id}`（`task_id` 有效期 24 小时） | **强制异步**：同视频生成，轮询接口相同，`task_id` 有效期 24 小时 |
| **输入格式** | • 文本：`prompt`（≤512 字符）<br>• （部分模型支持）图生图：`image_url`（仅创意工具） | • 文本：`input.prompt`（≤5000 字符，依模型而异）<br>• 图像：`input.img_url` / `input.image_url`（JPG/PNG/WEBP，≤10MB）<br>• 视频：`input.video_url`（MP4/AVI/MOV，≤30s，≤300MB）<br>• 音频：`input.audio_url`（WAV/MP3，1s–3min） | • 文本：`input.prompt`（≤1024 字符）<br>• 单图：`input.image`（JPEG/PNG，20–6000px，≤20MB）<br>• 多图：`input.images`（长度为4的数组，按前/左/后/右顺序，空位填 `{}`） |
| **输出格式** | • `data[].url`：直链 PNG/JPG（1 小时有效期）<br>• 支持批量（`n=1–4`） | • `output.video_url`：MP4 直链（2 小时有效期）<br>• 部分模型额外返回 `output.rendered_image_url`（首帧预览） | • `pbr_model_url`：带 PBR 材质的 GLB（2 小时）<br>• `base_model_url`：无贴图基础网格 GLB（2 小时）<br>• `rendered_image_url`：渲染预览图（2 小时） |
| **支持模型（代表）** | • WanX（万相）：强中文语义 & 风格控制<br>• Kling（可灵）：长文本构图 & 一致性<br>• Z-Image：轻量实时（不支持 negative_[prompt](../guides/prompt.md)）<br>• Vidu（子模块）：高质量静态帧<br>• Creative Tools：图像增强/扩图/上色 | • WanX 系列（wan3.0 / wan2.7）：文/图/参考生视频统一支持<br>• HappyHorse：通用视频合成<br>• PixVerse（爱诗）：对口型、动作模仿、超清增强<br>• EMO / LivePortrait / AnimateAnyone：人像驱动与数字人<br>• Video Style Transform：8 种艺术风格重绘 | • `Tripo/Tripo-H3.1`：高精度（≤200 万面，支持 `ultra` 模式）<br>• `Tripo/Tripo-P1.0`：快速生成（≤2 万面） |
| **地域要求** | 无显式地域限制（API Key 与 Endpoint 匹配即可） | **强地域绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2），混用即失败 | **仅限华北2（北京）**：URL、API Key、控制台开通均须在北京地域，跨域调用必失败 |
| **前置依赖** | 无（除图生图能力已整合至 Creative Tools） | • 人像类模型（EMO/LivePortrait/AnimateAnyone/wan2.2-s2v）**必须先调用对应 detect API** 获取 `face_bbox` 等坐标信息<br>• 部分特效需模板名（`template`） | 无前置检测，但多图输入需严格按顺序提供四视角图像（空位填 `{}`） |
| **计费方式** | • 按**成功生成图片数量**计费（1 张 = 1 [Token](../concepts/token.md)）<br>• 免费额度覆盖基础尺寸（1024×1024）；超分辨率/批量生成需付费套餐 | • 按**成功生成视频任务数**计费（1 任务 = 1 [Token](../concepts/token.md)）<br>• 分辨率（720P/1080P）、时长、模型类型影响单价（如 `wan3.0` > `wan2.7`） | • 按**成功生成 3D 任务数**计费（1 任务 = 1 [Token](../concepts/token.md)）<br>• `geometry_quality=ultra` 与 `pbr=true` 会提高计算成本，对应更高单价 |
| **典型延迟** | 同步：300ms – 3s（取决于模型与尺寸） | 异步：任务排队 + 生成耗时，通常 10s – 5min（文生视频）；人像驱动类常需 30s – 2min | 异步：通常 30s – 3min（文/单图生3D）；多图生3D约 1 – 5min |

---

## 各方案适用场景建议

### ✅ 图像生成（Image Generation）适合：
- **高频、低延迟图文内容生产**：电商主图、营销海报、社交媒体配图、AIGC 设计初稿。
- **可控风格化创作**：艺术插画、IP 形象设计、UI 元素生成（万相/Kling 对 [prompt](../guides/prompt.md) 结构化支持好）。
- **轻量图像增强与编辑**：扩图、局部重绘、线稿上色（Creative Tools 模块）。
- **不适合**：需要动态表达、时间序列一致性、或三维空间结构的场景。

### ✅ 视频生成（Video Generation）适合：
- **短视频内容工业化生产**：广告片头、产品演示动画、教育微课片段。
- **人像驱动应用**：数字人播报、虚拟主播、AI 口播视频（需配合 detect 流程）。
- **视频再创作**：风格迁移（8 种预设）、图生动作、视频换人、首尾帧补间。
- **不适合**：对实时性要求极高（如直播推流）、无公网可访问输入资源、或跨地域混合部署的场景。

### ✅ 3D内容生成（3D Generation）适合：
- **快速原型构建**：游戏资产草稿、工业设计概念模型、AR/VR 场景组件。
- **电商与展示应用**：商品 3D 展示页、线上展厅模型、社交媒体 3D 贴纸。
- **多视角建模需求**：已有四视角照片（前/左/后/右）快速重建三维模型。
- **不适合**：需要精确拓扑/UV/骨骼绑定的生产级建模、实时渲染集成（需自行导入引擎）、或非北京地域部署。

---

## 开发者技术选型参考指南

| 选型目标 | 推荐方案 | 关键理由与注意事项 |
|----------|----------|----------------------|
| **追求最低接入成本与最快上线** | 图像生成 | 单一同步端点、无地域强约束、无需轮询、文档最成熟；Z-Image 适合低延迟实验，万相/Kling 适合生产。 |
| **需生成带时间维度的内容（运动、叙事、节奏）** | 视频生成 | 唯一支持原生视频输出的能力；优先选用 `wan3.0`（统一接口）或 `PixVerse`（对口型/动作强）；务必规划 detect → synthesis 两阶段流程。 |
| **需输出可交互、可渲染、具空间结构的资产** | 3D生成 | Tripo 是当前唯一开箱即用的 3D 生成服务；必须锁定华北2地域；多图输入可显著提升几何精度，建议优先采用。 |
| **需混合多种模态（如：图→视频→3D）** | 组合使用 | 注意地域对齐：若视频/3D 均用华北2，则图像也建议统一；避免跨地域 Key 复用；各模块 token 不互通，需独立配额管理。 |
| **对成本敏感且需批量处理** | 图像生成（`n=4`）或视频生成（批量任务） | 图像支持单次多图；视频/3D 通过并发任务实现批量，但需注意 RPS 限流（如 3D 轮询默认 20 RPS），建议启用[异步回调](../../raw/model-api-reference/more-about-models/async-task-api.md)替代轮询。 |
| **需长期稳定服务与企业级 SLA** | 视频生成（WanX/HappyHorse）或图像生成（Kling/WanX） | 这两类模型服务成熟度最高、文档最全、错误码体系完善；3D 生成目前仅 Tripo 单一模型，扩展性与容灾能力相对有限。 |

> **重要提醒**：所有生成服务均禁止暴力、政治、成人等违规内容，请求将被风控拦截并计入日志；临时 URL（图像/视频/3D）**不可长期缓存**，务必在有效期内下载或转存至自有存储。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


