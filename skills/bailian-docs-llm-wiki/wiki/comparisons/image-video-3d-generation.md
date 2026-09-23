# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比基于当前（2024年Q3）正式上线的API服务，聚焦**技术实现一致性、调用范式差异性、模型生态覆盖度及工程落地适配性**，旨在为产品设计、架构选型与成本优化提供客观、可操作的技术决策依据。

---

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **输入格式** | • 文本（`prompt`/`messages`）<br>• 单图/多图（`image_url`, `images`）<br>• 模板图+目标图（如AI试衣、WordArt）<br>• 局部掩码（`mask_url`）等结构化输入 | • 文本（`prompt`）<br>• 单图（`img_url`，首帧）<br>• 首尾帧（`first_frame_url` + `last_frame_url`）<br>• 参考图/视频数组（`ref_image_urls`/`ref_video_url`）<br>• 人像图+音频（`image_url` + `audio_url`） | • 文本（`prompt`）<br>• 单图（`image`，公网URL）<br>• 多图（`images`，严格4元素数组：前/左/后/右）<br>• **三者互斥，不可混用** |
| **输出格式** | • JPEG/PNG 格式图像 URL（同步返回或异步下发）<br>• 支持批量生成（`n=1–9`）<br>• 部分工具返回结构化结果（如FaceChain返回证件照+商务照+模板图） | • MP4 格式视频 URL（H.264编码，1080p为主）<br>• 附带预览缩略图（`output.thumbnail_url`）<br>• 数字人模型额外返回音频对齐元数据 | • GLB 格式3D模型 URL（含PBR材质或基础几何体）<br>• 渲染预览图（`rendered_image_url`，PNG）<br>• **所有URL有效期仅2小时** |
| **支持模型/功能体系** | • **通用模型**：Qwen-Image 3.0、WanX 2.7/2.6、Kling v3、Vidu、Z-Image<br>• **垂直工具**：FaceChain（人像）、WordArt（文字设计）、AI试衣（服饰）、背景生成、扩图等 | • **通用模型**：HappyHorse、WanX 2.7/3.0（All-in-One）、PixVerse（爱诗）<br>• **人像驱动**：EMO、LivePortrait、AnimateAnyone、万相-s2v<br>• **专项增强**：视频风格重绘（8种艺术风）、视频特效（旧版） | • **Tripo系列专属模型**：<br> – `Tripo/Tripo-H3.1`（高精度，≤200万面）<br> – `Tripo/Tripo-P1.0`（快速验证，≤2万面）<br>• **无第三方模型接入**，全栈Tripo原生支持 |
| **API端点（典型）** | • 同步：`/api/v1/services/aigc/multimodal-generation/generation`（WanX 2.7）<br>• 异步：`/api/v1/services/aigc/image-generation/generation`（Kling/Vidu/FaceChain） | • 统一异步端点：<br>`/api/v1/services/aigc/video-generation/video-synthesis`<br>• 所有模型共用，仅`model`参数区分 | • 统一异步端点（华北2限定）：<br>`/api/v1/services/aigc/video-generation/3d-generation`<br>• 注意：路径含`video-generation`但实际为3D服务（历史兼容命名） |
| **调用模式** | • **混合模式**：<br> – 同步：Qwen-Image 3.0、Z-Image、WanX 2.7（<30s）<br> – 异步：Kling、Vidu、FaceChain训练、AI试衣等（1–2分钟） | • **强制异步**：<br>所有模型均需两步调用（创建任务 + 轮询），典型耗时1–5分钟<br>必须携带 `X-DashScope-Async: enable` | • **强制异步**：<br>标准两步流程（创建 + 轮询），典型耗时1–3分钟<br>必须携带 `X-DashScope-Async: enable` |
| **计费方式** | • 按**生成图片张数**计费（如1次请求`n=4`计为4次）<br>• 部分工具按**任务实例**计费（如FaceChain单次证件照生成）<br>• 分辨率影响单价（4K > 2K > 1K） | • 按**视频秒数 × 分辨率系数**计费：<br> – 基础：1080p视频按秒计费<br> – 高清增强（如PixVerse超清版）加权系数≥1.5<br>• 数字人任务按**音频时长+人像复杂度**综合计费 | • 按**单次任务**计费，与输入类型（文/图/多图）、模型版本（H3.1/P1.0）、质量参数（`geometry_quality`/`texture_quality`）强相关<br>• `ultra`精度与`detailed`贴图显著提高单价 |
| **典型场景** | • 营销素材生成（海报、Banner）<br>• 社交内容创作（头像、表情包）<br>• 电商应用（AI试衣、虚拟模特、鞋靴展示）<br>• 设计辅助（文字艺术、背景填充、局部编辑） | • 短视频内容生产（文生视频、图生视频）<br>• 数字人播报/直播（S2V、口型驱动）<br>• 影视预演（分镜动画、动作模拟）<br>• 教育/培训（动态知识演示） | • 工业设计原型（产品概念建模）<br>• 游戏/元宇宙资产生成（低多边形角色、道具）<br>• AR/VR内容快速构建（扫描替代方案）<br>• 电商3D商品展示（单图转3D） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— **高频、轻量、强可控性需求首选**
- **推荐场景**：  
  - 实时交互类应用（如聊天机器人配图、设计工具实时预览）→ 选用 `qwen-image-3.0-pro` 或 `z-image-turbo`（同步低延迟）；  
  - 高质量营销素材批量产出 → 选用 `wan2.7-image-pro`（4K组图）或 `vidu/vidu-image-pro_reference2image`（UI像素级还原）；  
  - 人像/文字/服饰等垂直需求 → 直接调用 `FaceChain`、`WordArt`、`aitryon-plus` 等专用工具，效果与效率远超通用模型。

### ✅ 视频生成 —— **中长周期、动态表达、人机协同场景核心载体**
- **推荐场景**：  
  - 快速制作短视频广告/教育短片 → `wan3-video-generation`（All-in-One，30秒/30fps，提示词直出）；  
  - 数字人客服/讲师 → `wan2.2-s2v`（需先检测）或 `emo-v1`（音频驱动，自然微表情）；  
  - 动态风格化内容（如水墨动画、漫画分镜）→ `pixverse/pixverse-v6-t2v` + 风格参数，或 `happyhorse-text-to-video`（物理运动保真）；  
  - **避坑提示**：避免使用已标注“旧版协议”的 WanX 2.1–2.6 模型，其Endpoint与参数体系不兼容新SDK。

### ✅ 3D生成 —— **专业领域、结构化输出、跨平台复用刚需**
- **推荐场景**：  
  - 从产品草图/参考图快速生成可导入Blender/Unity的GLB模型 → `Tripo/Tripo-P1.0`（快速验证） + `geometry_quality=standard`；  
  - 需要高精度工业级模型（如机械零件、建筑构件）→ `Tripo/Tripo-H3.1` + `geometry_quality=ultra` + `pbr=true`；  
  - 电商卖家无专业建模能力 → 单张商品图输入，启用 `texture_quality=detailed` 获取带纹理的可渲染模型；  
  - **关键约束**：必须部署于华北2（北京）地域，且所有资源（API Key、Workspace、Endpoint）严格同地域；多图输入务必补全4视角（空位填`{}`）。

---

## 面向开发者的选型决策指南

| 决策维度 | 技术选型建议 |
|----------|--------------|
| **响应时效敏感型应用**（如实时UI反馈、聊天机器人） | 优先选择**图像生成**中的同步模型（`qwen-image-3.0`、`z-image-turbo`）。视频与3D均为强制异步，无法满足亚秒级响应。 |
| **内容动态性要求高**（需时间维度表达：运动、变化、叙事） | 必选**视频生成**。图像生成无法表达时序信息；3D生成输出静态模型，需额外引擎驱动动画。 |
| **输出需跨平台复用/集成到3D引擎**（Unity/Unreal/WebGL） | 必选**3D生成**。图像与视频均为平面媒体，无法直接用于3D管线；Tripo输出的GLB是行业标准格式，开箱即用。 |
| **输入资源受限**（仅有1张产品图/1段文案） | • 单图 → 图像生成（局部编辑/背景替换）或3D生成（单图转模型）<br>• 文案 → 图像生成（文生图）或视频生成（文生视频）<br>• **避免强行用视频模型处理单图需求**：图生视频成本高、控制弱，不如先用图像生成优化首帧再驱动视频。 |
| **成本敏感型批量任务** | • 图像：选用 `wan2.6-t2i`（自由宽高比+低成本）或 `z-image-turbo`（极速低价）<br>• 视频：选用 `wan2.7` 基础版而非 `wan3.0 ultra`，或 `pixverse-c1`（轻量版）<br>• 3D：默认 `Tripo-P1.0`，仅在精度不可妥协时升 `H3.1`。 |
| **地域与架构约束** | • 若业务已部署在新加坡/弗吉尼亚 → **3D生成不可用**（仅限华北2）；<br>• 若需多地域容灾 → 视频/图像生成可跨地域部署，3D必须单点华北2；<br>• 所有服务均**强制要求模型、API Key、Endpoint同地域**，跨域调用必然失败。 |

> **最后提醒**：  
> - 所有异步任务（视频/3D/部分图像）请务必实现**健壮轮询逻辑**（指数退避+超时终止），并配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)以降低轮询压力；  
> - 首次集成强烈推荐使用 **Postman + DashScope SDK** 进行端到端验证，避免因URL拼写、Header缺失、地域错配等基础问题阻塞调试；  
> - 模型迭代迅速，本文所列模型名与参数以各模块最新API参考文档为准，生产环境请订阅[模型更新公告](../../raw/model-api-reference/preparations/model-update-notices.md)。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


