# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**工程接入可行性、模型能力特征、资源约束条件及商业化适配性**，旨在为产品设计、技术选型与架构决策提供客观、可落地的参考依据。

---

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | 文本（`text`） + 可选图像（Base64 或公网 URL），支持图文混合提示；支持单图/多图输入（如 FaceChain、AITryOn） | 文本（`prompt`）、单帧图（`first_frame_url`）、首尾帧图、参考图数组（`reference_images`）、参考视频（`reference_video_url`）、音频（`audio_url`）+ 人像图（`image_url`/`face_image_url`）等，按模型类型动态组合 | 三者**严格互斥**：<br>• 文本（`input.prompt`，≤1024 字符）<br>• 单图（`input.image`，JPEG/PNG，≤20MB）<br>• 四视角图（`input.images`，长度固定为4，按「前/左/后/右」顺序，空视角传 `{}`） |
| **输出格式** | PNG/JPEG 格式图像（URL 下载链接），部分工具返回多图（如 `n=4`）或图文混排结果 | MP4 格式视频（`output.video_url`），有效期 24 小时；部分模型额外返回预览图、关键帧或元数据（如 `output.audio_sync_score`） | GLB 格式 3D 模型（`pbr_model_url` / `base_model_url`） + 预览图（`rendered_image_url`），所有 URL 有效期 **2 小时** |
| **支持模型（代表性）** | • 通用：`qwen-image-3.0-pro`、`wan2.7-image-pro`<br>• 轻量：`z-image-turbo`、`kling/kling-v3-omni-image-generation`<br>• 垂直：`aitryon-plus`、`facechain-generation`、`wordart-semantic` | • 全栈：`wan2.7-videoedit`、`wan3.0-all-in-one`<br>• 创意：`pixverse/pixverse-v6-t2v`<br>• 人像驱动：`emo-v1`、`liveportrait-v1`、`video-retalk-v1`、`emoji-v1`<br>• 物理仿真：`happyhorse-h3.0-t2v` | • `Tripo/Tripo-H3.1`（高精度，≤200 万面，支持 `geometry_quality=ultra`）<br>• `Tripo/Tripo-P1.0`（快速生成，≤2 万面） |
| **API 端点** | 同步/异步统一端点：<br>`POST /api/v1/services/aigc/multimodal-generation/generation`<br>（通过 `X-DashScope-Async` 头控制模式） | 异步专用端点：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`<br>（`X-DashScope-Async: enable` 强制） | 异步专用端点：<br>`POST /api/v1/services/aigc/video-generation/3d-generation`<br>（注意路径含 `video-generation`，属历史命名，实际为 3D 服务） |
| **调用模式** | ✅ 支持同步（低延迟，适用于文生图/简单编辑）<br>✅ 支持异步（推荐用于扩图、AI试衣、复杂编辑）<br>✅ OpenAI 兼容协议（千问系列） | ❌ **仅支持异步**（两步流程：创建任务 → 轮询结果）<br>• 任务 ID 有效期：24 小时<br>• 建议轮询间隔 ≥1 秒（受 RPS 限流约束） | ❌ **仅支持异步**（两步流程：创建任务 → 轮询结果）<br>• `task_id` 有效期：24 小时<br>• 结果 URL 有效期：**2 小时**（需及时下载）<br>• 建议轮询间隔 ≥15 秒 |
| **地域支持** | 全地域支持（华北2、新加坡、美国弗吉尼亚等），但**模型、API Key、Endpoint 必须同地域** | 全地域支持，**严格地域隔离**（跨地域调用鉴权失败或返回空结果） | ⚠️ **仅支持华北2（北京）地域**<br>• 控制台开通、API Key 获取、Endpoint 均需匹配该地域<br>• 其他地域调用将直接报错 |
| **计费方式** | 按**生成张数**计费（例：`aitryon-plus` 0.50 元/张，`wordart-semantic` 0.08 元/张）<br>• 各模型独立免费额度（通常 500 张/90 天） | 按**视频秒数**或**任务次数**计费（例：`wan2.2-s2v` 720P 为 0.9 元/秒；`emo-v1` 按次计费）<br>• 多数模型提供免费额度（具体见各模型定价页） | 按**任务次数**计费（未公开单价，以控制台实时计费页为准）<br>• 当前无公开免费额度说明，建议开通后查看配额详情 |
| **典型场景** | • 营销素材批量生成（海报、Banner）<br>• UI 设计辅助（图标、组件渲染）<br>• 电商商品图优化（背景替换、AI试衣）<br>• 个性化内容（写真、文字艺术） | • 短视频创意生产（文/图生视频）<br>• 数字人播报与唱演（EMO/LivePortrait）<br>• 视频口型同步（VideoRetalk）<br>• 动作迁移与风格重绘（AnimateAnyone、HappyHorse） | • 工业设计原型（文生3D 快速建模）<br>• 电商 3D 商品展示（单图/四视图重建）<br>• 游戏资产生成（基础网格+PBR贴图）<br>• AR/VR 内容预研（GLB 直接加载） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— **首选“快速验证”与“高频轻量”需求**
- 适合需要**毫秒级响应**的交互场景（如设计工具实时预览、AIGC插件嵌入）；
- 推荐用于**标准化输出**（固定尺寸、单图为主）和**文本强依赖**任务（如文案配图、广告图生成）；
- 垂直工具链（FaceChain、AITryOn）大幅降低人像/服装类应用开发门槛，适合电商、社交 App 快速集成。

### ✅ 视频生成 —— **专注“动态表达”与“人机交互”场景**
- 适合对**时间维度语义**有明确要求的任务（如数字人播报、短视频营销、教育动画）；
- 人像驱动类模型（EMO、LivePortrait）需**前置检测**，务必纳入端到端流程设计；
- 高质量视频（如 PixVerse、HappyHorse）生成耗时较长（30–120 秒），需合理设计用户等待体验（进度提示、Webhook 回调）。

### ✅ 3D生成 —— **面向“空间建模”与“工业级交付”场景**
- 仅限华北2 地域，**不适用于全球分布式业务**，需提前规划部署架构；
- 输入质量敏感度高：单图需清晰正向，四视图需视角规范、光照一致，否则几何重建易失真；
- 输出为标准 GLB，可直接集成至 Three.js、Babylon.js、Unity 等引擎，适合构建 Web3D 展示页、配置器、AR 应用；
- `Tripo-H3.1` 适合对精度要求高的专业场景（如工业零件示意），`Tripo-P1.0` 更适合快速原型与概念验证。

---

## 开发者技术选型参考

| 选型考量 | 推荐方案 | 说明 |
|----------|----------|------|
| **追求最低延迟 & 最简集成** | 图像生成（同步模式 + `qwen-image-3.0-pro`） | 无需轮询、无回调依赖，适合前端直连或 Serverless [函数调用](../concepts/function-calling.md) |
| **需生成带语音/动作的数字人内容** | 视频生成（`emo-v1` 或 `liveportrait-v1`） | 注意必须先调用对应 `*-detect` 接口，且音频需人声清晰、无噪音 |
| **构建电商 3D 商品库** | 3D生成（`Tripo/Tripo-H3.1` + 四视图输入） | 建议搭配自动化拍摄方案获取标准四视角图，启用 `pbr=true` 获取带材质模型 |
| **多模态混合工作流（如图→视频→3D）** | 分阶段调用 + 统一地域管理 | 所有环节必须使用同一地域的 API Key 与 WorkspaceId；视频与3D均强制异步，需统一任务状态管理机制 |
| **成本敏感型 MVP 项目** | 图像生成（`z-image-turbo` 或 `wan2.6-t2i`） + 视频生成（`wan2.7-videoedit` 基础版） | 轻量模型单价低、免费额度充足；避免早期已归档模型（如 `wanx-v1`） |
| **需 OpenAI 生态兼容** | 图像生成（千问系列） | 仅需切换 `base_url` 和 `model`，零代码改造即可迁移现有 DALL·E 集成 |

> **重要提醒**：  
> - 所有生成服务均**强制要求地域一致性**，跨地域调用是第一大失败原因，请在初始化阶段校验 `API Key`、`WorkspaceId`、`region` 三者匹配；  
> - 异步任务务必实现健壮的轮询或回调机制，避免因超时导致结果丢失；  
> - 图像/视频 URL 有效期短（2–24 小时），生产环境应立即下载并托管至自有 CDN 或对象存储。  

---  
*本文档基于百炼平台 2024Q2 发布能力整理，模型列表与参数细节请以各模块最新 API 参考文档为准。*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


