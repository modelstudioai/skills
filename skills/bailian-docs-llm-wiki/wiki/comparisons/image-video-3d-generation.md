# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态AIGC领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D内容生成（3D Generation）三大核心能力。对比聚焦实际工程落地的关键维度——包括输入输出规范、模型生态、调用协议、地域约束、计费逻辑及典型适用场景，旨在为技术选型提供客观、可执行的决策依据。所有信息均基于当前（2024年Q3）百炼平台正式发布的API文档与运行时行为。

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D内容生成（3D Generation） |
|------|------------------------------|------------------------------|------------------------------|
| **核心输入格式** | `text` + 可选 `image`（Base64 或 HTTPS URL），支持多图混合输入（如 `wan2.5-i2i-preview`）；`input.messages` 结构化数组 | `prompt`（文生视频）或 `image_url`/`image`（图生视频）或 `image`（人像驱动）；`portrait-animation` 模型需将驱动文本置于 `input.text` | 三者**严格互斥**：<br>• `prompt`（文生3D，≤1024字符）<br>• `image`（单图，JPEG/PNG，≤20MB）<br>• `images`（固定4元素数组：前/左/后/右，空视角需显式传 `{}`） |
| **核心输出格式** | PNG/JPEG 图像（URL直链），分辨率灵活（512×512 至 4K）；部分模型支持多张并行输出（`n=1–9`） | MP4 视频（H.264编码，无音频）；`portrait-animation` 例外，支持TTS合成音频；时长2–8秒（依模型而定） | GLB 格式3D模型：<br>• `pbr_model_url`（含PBR材质与贴图）<br>• `base_model_url`（无贴图基础网格）<br>• `rendered_image_url`（WebP预览图） |
| **主流支持模型** | • 千问系列：`qwen-image-3.0-pro`（全栈能力）<br>• 万相系列：`wan2.7-image-pro`（4K文生图）、`wan2.5-i2i-preview`（多图编辑）<br>• 可灵：`kling/kling-v3-omni-image-generation`（分镜组图）<br>• Vidu：`vidu/viduq2-pro_reference2image`（UI/图表像素级还原） | • 文生视频：`kling`、`vidu`、`HappyHorse`、`wanxiang`、`aishih`<br>• 图生视频：`kling`、`vidu`、`wanxiang`<br>• 人像驱动：`portrait-animation`（单图+文本/语音）<br>• 多模态控制：`vidu`（镜头语言）、`kling`（结构化运镜） | • `Tripo/Tripo-H3.1`（高精度，≤200万面，支持 `geometry_quality=ultra`）<br>• `Tripo/Tripo-P1.0`（快速生成，≤2万面） |
| **API 端点与协议** | • **同步优先**：`POST /api/v1/services/aigc/image-generation`（DashScope协议，支持Base64/URL）<br>• OpenAI兼容：`POST /v1/images/generations`（仅同步）<br>• 异步：`X-DashScope-Async: enable` 头必填 | 统一异步端点：<br>`POST /v1/videos/generations`（创建任务）<br>`GET /v1/videos/generations/{id}`（轮询结果）<br>**不支持同步调用** | 统一异步端点（**仅华北2可用**）：<br>`POST /api/v1/services/aigc/video-generation/3d-generation`（需 `X-DashScope-Async: enable`）<br>`GET /api/v1/tasks/{task_id}`（轮询） |
| **地域与隔离要求** | **强制同地域**：API Key、Endpoint、Workspace ID 必须同属北京/新加坡/弗吉尼亚；推荐使用 Workspace 专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | **强制同地域**：同图像生成，跨地域调用必然失败；各模型地域支持一致 | **严格限定华北2（北京）**：仅支持北京地域 API Key 与 Endpoint；其他地域 URL 不可用且返回明确错误 |
| **计费方式** | • 按量付费为主（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`）<br>• 部分创意工具提供免费额度（如 `facechain-generation`: 500张/90天）<br>• `wanx-x-painting` 等体验模型：免费额度用尽后**不可付费启用** | • `HappyHorse`/`wanxiang`（720p）有基础免费额度<br>• `vidu`/`kling`/`MiniMax` 默认高分辨率，需确认配额或开通付费<br>• 所有模型按**成功生成的视频条数**计费 | • 按**成功生成的3D任务次数**计费<br>• 无公开免费额度；需在控制台开通 Tripo 服务并完成授权后方可调用 |
| **典型场景** | • 营销海报、电商主图、社交媒体配图<br>• UI设计稿生成与局部重绘（Vidu）<br>• 虚拟模特、AI试衣、人物写真（FaceChain）<br>• 创意文字艺术（WordArt） | • 短视频广告脚本可视化（文生视频）<br>• 产品动态展示（图生视频）<br>• 数字人播报/虚拟主播驱动（人像驱动）<br>• 影视分镜预演（Vidu镜头语言） | • 工业设计原型快速建模（文生3D）<br>• 电商商品3D展示（单图转3D）<br>• AR/VR内容资产生成（多视角重建）<br>• 游戏资产基础网格生成 |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「静态视觉表达」高频、多样化需求  
- **首选场景**：需要快速产出高质量、高一致性静态图像的业务，如电商详情页、营销活动素材、设计协作初稿、个性化头像/海报。  
- **模型选型建议**：  
  - 追求**全能与可控性** → `qwen-image-3.0-pro`（支持复杂提示词、多图参考、局部重绘）；  
  - 需要**4K工业级精度与UI还原** → `vidu/viduq2-pro_reference2image`；  
  - 偏好**分镜叙事与创意组合** → `kling/kling-v3-omni-image-generation`；  
  - 轻量级快速迭代 → `z-image-turbo`（中英文字渲染友好）。  
- **避坑提示**：避免使用已标注“推荐升级”的旧版模型（如 `wanx-v1`），其分辨率、地域支持与功能完整性严重受限。

### ✅ 视频生成 —— 适合「动态叙事与人机交互」中低频、高价值需求  
- **首选场景**：短视频内容生产、数字人交互、产品演示动画、影视前期分镜验证。  
- **模型选型建议**：  
  - **通用文生视频** → `vidu`（支持镜头语言提示词，8秒4K）或 `kling`（结构化控制强）；  
  - **图生视频/快速演示** → `wanxiang`（兼容性好，720p免费额度充足）；  
  - **人像驱动类应用**（如客服播报、虚拟讲师）→ `portrait-animation`（仅接受单图+文本，音频合成一体化）；  
  - **轻量实验性尝试** → `HappyHorse`（4秒1080p，入门门槛低）。  
- **避坑提示**：`portrait-animation` 的输入结构（`input.text`）与其他模型不一致，集成时需独立适配；所有视频模型**不输出音频**（除人像驱动外），音画同步需自行处理。

### ✅ 3D内容生成 —— 适合「空间建模与三维资产」专业、垂直需求  
- **首选场景**：工业设计协同、电商3D商品库建设、AR营销素材生成、游戏/元宇宙基础资产管线。  
- **模型选型建议**：  
  - **高保真原型/可直接渲染** → `Tripo/Tripo-H3.1` + `pbr=true` + `geometry_quality=ultra`；  
  - **快速草图验证/轻量资产** → `Tripo/Tripo-P1.0`（2万面，生成速度快）；  
  - **无贴图轻量化模型**（如用于物理仿真）→ 显式设置 `texture=false` 且 `pbr=false`。  
- **避坑提示**：必须使用**北京地域专属配置**（API Key、Endpoint、Workspace ID）；多图模式下 `images` 数组长度**必须为4**，缺失视角需传空对象 `{}`，否则报错；所有下载链接（GLB/WebP）有效期仅**2小时**，务必及时持久化。

## 面向开发者的选型决策指南

| 决策问题 | 推荐动作 | 技术依据 |
|----------|----------|----------|
| **我的应用需要同时生成图、视、3D内容，如何统一接入？** | 采用 **DashScope SDK v2.3+**，复用认证机制（`DASHSCOPE_API_KEY`）与异步任务管理范式；但需注意：图像支持同步/异步双模式，视频与3D**强制异步**，且3D仅限北京地域。 | 三者均遵循 DashScope 异步任务生命周期（创建→轮询→获取结果），但协议细节（如输入结构、端点路径、地域约束）差异显著，不可共用同一请求模板。 |
| **我已有OpenAI Images SDK集成，能否平滑迁移？** | ✅ 可迁移至图像生成（OpenAI兼容接口）；❌ **不适用于视频与3D**（二者无OpenAI兼容层，仅提供原生RESTful异步API）。 | 图像生成提供 `/v1/images/generations` 兼容端点；视频与3D仅暴露 `/v1/videos/generations` 和 `/api/v1/services/aigc/video-generation/3d-generation` 原生路径。 |
| **我的用户对生成速度敏感，应如何优化？** | • 图像：选用 `z-image-turbo` 或 `wan2.6-t2i`（V2版）；<br>• 视频：`HappyHorse` 或 `wanxiang`（720p）平均耗时 <30s；<br>• 3D：`Tripo/Tripo-P1.0` 比 `H3.1` 快约3倍。 | `z-image-turbo` 固定单图、轻量架构；`HappyHorse` 输出4秒视频；`Tripo-P1.0` 面数上限低，计算负载小。高精度模型（`qwen-image-3.0-pro`、`vidu`、`Tripo-H3.1`）均需更长排队与生成时间。 |
| **我需要保证生成结果可商用、版权清晰，该关注什么？** | 重点核查模型服务协议：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`vidu`、`kling`、`Tripo` 均明确支持商业用途；避免使用未声明商用许可的体验模型（如 `wanx-x-painting`）。 | 百炼平台主流AIGC模型均在控制台服务开通页注明“支持商用”，其训练数据与生成内容权属条款符合阿里云《AIGC服务协议》。 |
| **我的系统需高并发调用，如何规避限流？** | • 图像：`aitryon` RPS限10，`facechain-finetune` 并发限1，需按模型粒度申请配额提升；<br>• 视频/3D：统一受 Workspace 级RPS限制，建议配置[异步回调](../../raw/model-api-reference/more-about-models/async-task-api.md)替代高频轮询。 | 限流策略按模型或服务维度独立配置；视频/3D轮询接口（`GET /v1/videos/generations/{id}` / `GET /api/v1/tasks/{task_id}`）RPS限20，高频轮询易触发限流，回调机制为官方推荐解法。 |

> **最后提醒**：所有能力均需在百炼控制台对应地域完成**服务开通与授权**（如可灵、Vid

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


