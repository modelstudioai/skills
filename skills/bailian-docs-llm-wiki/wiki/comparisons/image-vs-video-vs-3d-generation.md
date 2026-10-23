# 图像生成、视频生成与3D生成对比

为帮助开发者快速理解百炼平台多模态生成能力的定位差异，明确技术选型边界，本文从输入输出、模型生态、调用方式、计费逻辑及业务适配性等维度，系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。本对比基于当前（2024年Q3）平台正式发布的API能力，适用于新项目架构设计、已有服务迁移评估及跨模态方案整合决策。

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | 文本（`prompt`） + 可选参考图（最多10–14张，支持PNG/JPEG/WEBP；部分模型如 `qwen-mt-image-2.0` 仅支持JPG） | 文本（`prompt`）或单图（`img_url`）或首尾帧（`first_frame`/`last_frame`）或参考媒体数组（含`image_url`/`video_url`）；所有URL需公网可访问 | **二选一**：<br>• 纯文本描述（`prompt`，≤100字，中英文）<br>• 单张RGB图像（`image_url`，JPG/PNG，建议512×512+，禁止人脸/文字/Logo） |
| **输出格式** | PNG/JPEG格式图像URL（同步返回）或临时URL（[异步任务](../concepts/asynchronous-task.md)）；支持水印控制（`watermark: true/false`） | MP4格式视频URL（异步返回，有效期24小时）；无水印选项（默认无水印，部分模型如Vidu可配置品牌标识） | `.glb` 格式3D模型文件URL（异步返回，有效期24小时）；含基础几何、材质与光照，**不支持动画、骨骼、PBR高级材质** |
| **支持模型（主力）** | • 千问系列：`qwen-image-3.0-pro`、`qwen-mt-image-2.0`<br>• 万相系列：`wan2.7-image-pro`、`wan2.5-i2i-preview`、`wanx-style-repaint-v1`<br>• 可灵/Vidu：`kling/kling-v3-omni-image-generation`、`vidu/viduq2-pro_reference2image`<br>• 创意工具：`virtualmodel-v2`、`facechain-finetune`（需训练）等 | • HappyHorse：文/图/参考生视频、视频编辑<br>• 万相：`wan2.7-videoedit`、`wan2.7-t2v`、`wan3.0-video-all-in-one`<br>• 第三方模型：`pixverse/pixverse-v6-t2v`、`kling/kling-v3-t2v`、`vidu/viduq3-pro_text2video`、`minimax/minimax-v2-t2v`<br>• 垂直能力：`videoretalk`（口型驱动）、`video-style-transform`（风格重绘）、`wan2.2-s2v`（数字人） | • **仅 Tripo-3D**（`tripo-3d-generation`）<br>• 不支持其他3D模型（如Luma、Stable Diffusion 3D等） |
| **API 端点** | 同步模型（如`qwen-image-3.0-pro`）：<br>`POST /api/v1/services/aigc/multimodal-generation/generation`<br>异步模型（如`kling`/`vidu`）：<br>`POST /api/v1/services/aigc/image-generation/generation` → 轮询 `/tasks/{task_id}` | **统一异步端点**：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`（主用）<br>少数模型（如`wan2.2-s2v`）使用：<br>`POST /api/v1/services/aigc/image2video/video-synthesis`<br>→ 全部轮询 `/api/v1/tasks/{task_id}` | **专用端点**：<br>`POST /v1/models/tripo-3d-generation:generate`<br>→ 轮询 `/v1/tasks/{task_id}` |
| **调用范式** | • **混合范式**：低延迟模型（千问3.0+/万相2.7+）支持**同步调用**（秒级返回）；高保真/复杂编辑类（可灵/Vidu/FaceChain）强制**异步调用**（需轮询） | • **强制异步**：所有模型均需 `X-DashScope-Async: enable` 头；创建任务后必须轮询，**不支持同步响应** | • **强制异步**：固定流程：提交 → 获取`task_id` → 轮询 → 下载`.glb`；**不支持同步、无Webhook回调** |
| **计费方式** | • 按**调用次数**（如`qwen-image-3.0-pro` 1次=1张图）<br>• 部分模型按**分辨率档位**（如`wan2.7-image-pro`选`4K`比`2K`贵）<br>• 创意工具多数**仅限免费体验**（额度用尽即停） | • 主流按**视频时长（秒）** 计费（如`videoretalk` 0.08元/秒，`wan2.2-s2v` 480P 0.5元/秒）<br>• 部分模型按**任务次数**（如`pixverse/pixverse-v6-t2v`）<br>• 所有模型存在并发数与RPS硬限制（如`videoretalk`最大并发=1） | • 按**单次任务**计费（无论文本/图像输入）<br>• 分辨率选项（`low`/`medium`/`high`）**不影响单价**<br>• 无免费额度，**无创意工具类“限时免费”模型** |
| **典型场景** | • 广告素材批量生成（Banner/海报）<br>• 电商AI试穿/虚拟模特展示<br>• 多语言图文翻译（`qwen-mt-image-2.0`）<br>• 设计稿局部重绘与风格迁移<br>• 漫画分镜图生成（Kling多图输入） | • 短视频内容创作（抖音/小红书）<br>• 数字人口播视频生成（`videoretalk`+`wan2.2-s2v`）<br>• 产品广告片制作（Vidu工业级一致性）<br>• 游戏过场动画原型（HappyHorse物理真实感）<br>• 视频超分与艺术风格化（PixVerse Upscale/Style Transform） | • Web端3D商品预览（电商/AR导购）<br>• 游戏资产快速原型（低多边形角色/道具）<br>• 工业设计概念验证（简单机械结构/家居摆件）<br>• 教育可视化模型（分子/地理/建筑简模） |
| **地域隔离要求** | ✅ 强制：API Key、Endpoint、Workspace ID 必须同地域（北京/新加坡/美东）；跨地域调用必然失败 | ✅ 强制：同图像生成；**额外注意**：`wan2.2-s2v`、`videoretalk`、`video-style-transform` **仅支持北京地域** | ✅ 强制：同属百炼地域体系，需使用对应地域专属域名（如`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） |

## 各方案适用场景建议

### ✅ 优先选择图像生成，当：
- 需要**毫秒级响应**（如实时UI组件渲染、A/B测试图生成），且任务复杂度适中（推荐千问3.0+/万相2.7+同步模型）；
- 输入依赖**多图参考**（如分镜草图+风格图+人物图），需强上下文对齐（Vidu/Kling支持14图输入）；
- 涉及**多语言图文排版保留**（如海外电商详情页本地化），必须使用 `qwen-mt-image-2.0`；
- 业务已深度集成图像工作流（如PS插件、Figma AI助手），需最小改造接入。

### ✅ 优先选择视频生成，当：
- 核心交付物是**动态内容**（非静态截图），且对运动连贯性、物理合理性有要求（HappyHorse首选）；
- 需复用**已有数字人形象或口播音频**（`wan2.2-s2v` + `videoretalk` 组合方案）；
- 面向**专业影视/广告场景**，强调分镜一致性与品牌视觉规范（Vidu系列）；
- 需对存量视频进行**增强处理**（超分至4K、转换油画/赛博朋克风格），而非从零生成。

### ✅ 优先选择3D生成，当：
- 目标是生成**可交互、可嵌入WebGL/Three.js的轻量3D资产**（`.glb`直接加载）；
- 输入源为**清晰单视角产品图或简洁文本描述**（如“不锈钢保温杯，圆柱形，带硅胶底座”）；
- 对模型精度要求为**原型级/展示级**（三角面数≤10k），无需骨骼绑定、动画或PBR材质；
- 业务链路已具备3D渲染能力（如Unity WebGL导出、Babylon.js前端展示），只需补充生成环节。

### ⚠️ 需谨慎评估或规避的场景：
- **跨模态强耦合需求**（如“生成一段3秒视频，其中主角是刚生成的3D模型”）：平台当前**无原生跨模态流水线**，需自行编排图像→3D→视频（但Tripo输出无法直接驱动视频模型，需人工重建）；
- **高精度工业/医疗3D建模**：Tripo-3D不支持CAD级精度、拓扑约束或参数化建模，应转向专业软件（Blender+Geometry Nodes）或专用SaaS；
- **超长视频生成（>15秒）或高帧率（>30fps）需求**：所有视频模型均以10–15秒/16fps为标准输出，延长需拼接，质量下降风险高；
- **图像生成中依赖“免费创意工具”构建核心功能**：如`wanx-x-painting`、`shoemodel-v1`等已明确标注“免费额度用尽即停”，不可用于生产环境。

## 面向开发者的选型决策指南

1. **从输出定义起点**：  
   明确业务最终需要交付的是**静态画面**（→ 图像生成）、**动态序列**（→ 视频生成）还是**可旋转/可交互的三维网格**（→ 3D生成）。此为不可妥协的第一判断。

2. **检查输入约束匹配度**：  
   - 若输入含**多张参考图/复杂布局图** → 图像生成（Vidu/Kling）；  
   - 若输入含**音频文件或需口型同步** → 视频生成（`videoretalk`）；  
   - 若输入仅为**单张正视图或短文本** → 3D生成（Tripo）；  
   - 若输入需**严格保留原始文字排版** → 图像生成（`qwen-mt-image-2.0`）。

3. **评估延迟与架构适配性**：  
   - 要求**<2秒端到端响应** → 仅图像生成中的同步模型可行；  
   - 可接受**10–120秒异步等待** → 三者均可，但需统一轮询逻辑（推荐封装通用Task Poller SDK）；  
   - 已有**[异步任务](../concepts/asynchronous-task.md)队列（如Celery/RabbitMQ）** → 视频/3D生成天然契合；  
   - 使用**Serverless函数（如FC）** → 注意冷启动与超时（3D生成最大300秒，视频生成通常60–90秒）。

4. **成本与稳定性兜底**：  
   - 避免将**免费额度模型**纳入核心链路（查看文档中“仅限免费体验”标注）；  
   - 高并发场景必做**限流降级**：图像生成QPS上限2，视频生成并发任务上限1–3，3D生成无明确并发限制但单任务耗时波动大；  
   - 所有[异步任务](../concepts/asynchronous-task.md)必须实现**幂等轮询**（`task_id`唯一，重复查询安全）与**过期清理**（24小时URL失效，需提前下载并持久化）。

5. **地域与密钥治理**：  
   - 新项目**必须使用业务空间专属域名**（`{WorkspaceId}.<region>.maas.aliyuncs.com`），禁用旧版`dashscope.aliyuncs.com`；  
   - 北京地域覆盖最全（含`s2v`/`videoretalk`），新加坡/美东暂不支持

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


