# 图像生成、视频生成与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**工程接入可行性、模型能力覆盖度、服务约束条件及生产就绪程度**，旨在为产品设计、技术选型与架构决策提供客观、可落地的参考依据。

---

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | • 文本提示词（T2I）<br>• PNG/JPEG/JPG 图像（I2I/编辑）<br>• 多图参考（最多10张，部分模型支持）<br>• 涂鸦草图（`wanx-sketch-to-image-lite`） | • 文本提示词（T2V）<br>• 首帧/首尾帧图像（URL）<br>• 参考图像/视频数组（`media`）<br>• 音频文件（对口型场景）<br>• *所有输入需为公网可访问 HTTP(S) URL 或 OSS 临时链接* | • 文本提示词（文生3D）<br>• 单张/四视图图像（前/左/后/右，URL）<br>• 已有3D模型（GLB/FBX/OBJ，≤150MB）<br>• *仅支持 JPEG/PNG/WebP 输入图（≤20MB）* |
| **输出格式** | • PNG/JPEG（含透明通道支持，依模型而定）<br>• Base64 编码或公网可访问 URL<br>• 分镜组图（`kling-v3-omni` 返回多图数组） | • MP4（H.264 编码，标准封装）<br>• 公网可访问 URL（异步返回）<br>• *不直接返回二进制流或 Base64* | • GLB（默认）、USDZ、FBX、STL、SPLAT（Gaussian）等<br>• 网格、贴图、骨骼、动画分文件 ZIP 包<br>• *全部通过 `task_id` 异步获取下载 URL* |
| **主流支持模型** | • `qwen-image-3.0-pro`（T2I+I2I 二合一）<br>• `wan2.7-image-pro`（4K 输出+推理过程）<br>• `kling/kling-v3-omni-image-generation`（多图分镜）<br>• `z-image-turbo`（低延迟轻量）<br>• *注意：`wanx-poster-generation-v1` 等为免费体验模型，无付费通道* | • `wan3/video-generation`（All-in-One，万相3.0）<br>• `happyhorse/happyhorse-t2v`（物理真实感）<br>• `pixverse/pixverse-v6-max-t2v`（动态特效强）<br>• `vidu/viduq3-pro_text2video`（广告/剧集级）<br>• *万相2.7需显式设置 `X-DashScope-Async: enable`* | • `Tripo/Tripo-H3.1`（高精度网格生成）<br>• `Tripo/Tripo-P1.0`（轻量级网格）<br>• `Tripo/Tripo-ImageToSplat`（Gaussian Splatting）<br>• `Tripo/Tripo-Retopology`（重拓扑 v2.0）<br>• *全部基于 Tripo 模型体系，无第三方替代选项* |
| **API 端点协议** | • 支持同步调用（`qwen-image-*`、`wan2.7-image-*`、`z-image-turbo`）<br>• 支持[异步调用](../concepts/asynchronous-invocation.md)（`kling`、`vidu`、创意工具类）<br>• OpenAI 兼容模式（仅 `qwen-image-*` 系列） | • **强制[异步调用](../concepts/asynchronous-invocation.md)**（所有模型）<br>• 统一端点：`/api/v1/services/aigc/video-generation/video-synthesis`<br>• 必须携带请求头 `X-DashScope-Async: enable` | • **强制[异步调用](../concepts/asynchronous-invocation.md)**（所有模型）<br>• 统一端点：`/api/v1/services/aigc/video-generation/3d-generation`<br>• 必须携带请求头 `X-DashScope-Async: enable`<br>• *注意：3D端点路径含 `video-generation` 字样，属历史兼容命名，非功能归属* |
| **计费方式** | • 按调用次数 + 输出分辨率/张数计费<br>• `qwen-image-*` / `wan2.7-image-pro` / `kling` 等为主力付费模型<br>• `image-erase-completion`、`wanx-x-painting` 等**仅限免费额度，用尽即停，不可续费** | • 按任务计费（单次生成任务为1次计费单元）<br>• 分辨率（`720P`/`1080P`/`4K`）、时长（默认2–4秒）、帧率影响单价<br>• 万相3.0、PixVerse V6、Vidu Pro 均属高阶付费模型 | • 按任务计费（含生成+后处理）<br>• `geometry_quality`（面数）、`texture_quality`（8K）、`quad`（四边形重拓）、`smart_low_poly` 等参数显著提升单价<br>• `Tripo-P1.0`（≤2万面）为经济型；`Tripo-H3.1`（≤200万面）为专业型 |
| **典型场景** | • 创意海报/营销配图生成<br>• 虚拟模特换装与背景替换<br>• 局部重绘（擦除/补全/风格迁移）<br>• UI/UX 设计稿辅助出图 | • 短视频广告/社交媒体内容生成<br>• 教育课件动画化（图→视频）<br>• 影视分镜预演与动作参考<br>• 数字人对口型驱动与动作模仿 | • 游戏资产快速建模（文/图→3D）<br>• AR/VR 应用中实时渲染素材生成（Gaussian Splat）<br>• 工业零件逆向建模与网格优化<br>• 3D 打印前处理（重拓扑+封口+绑骨） |
| **地域限制** | • 严格地域隔离：北京/新加坡/弗吉尼亚等独立部署<br>• API Key、Endpoint、Workspace ID 必须同地域 | • 严格地域隔离：北京/新加坡/弗吉尼亚等独立部署<br>• *部分模型（如 `wan2.2-s2v`）仅限北京地域* | • **仅支持华北2（北京）地域**<br>• Endpoint、API Key、控制台开通、Workspace ID 均必须在北京地域配置<br>• 跨地域调用必然失败（403 或鉴权错误） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、多样化视觉输出」场景  
- **适用**：营销自动化（每日百张海报）、电商主图生成、UI组件库扩展、AIGC辅助设计、轻量级虚拟人形象创建（`facechain-finetune`）。  
- **慎用**：需长期稳定服务的生产系统若依赖 `wanx-poster-generation-v1` 等免费模型，存在突然中断风险；高一致性多图需求（如角色全身多角度）应优先选用 `kling-v3-omni` 而非单图模型。  
- **最佳实践**：对延迟敏感业务（如实时设计工具）选用 `qwen-image-3.0-pro` 同步接口；对画质与可控性要求高者，启用 `wan2.7-image-pro` 的 `thinking_mode` 辅助调试。

### ✅ 视频生成 —— 推荐用于「中低时长、强表现力、需运动逻辑」场景  
- **适用**：短视频平台内容工厂、教育动画脚本可视化、数字人直播预演、品牌广告分镜测试。  
- **慎用**：超长视频（>8秒）、电影级运镜、复杂物理交互（如流体/布料仿真）当前尚不成熟；对口型任务需严格校验音频采样率与静音段长度（PixVerse 文档明确要求 ≥0.5s 有效语音）。  
- **最佳实践**：万相3.0 是通用首选（All-in-One 架构降低集成复杂度）；追求电影质感可组合使用 Vidu（参考生视频）+ PixVerse（超分+特效）；务必预置OSS临时URL上传逻辑以应对本地文件输入。

### ✅ 3D生成 —— 推荐用于「专业工作流闭环、需几何精度与下游兼容性」场景  
- **适用**：游戏开发管线（概念图→低模→绑定→动画）、工业AR巡检模型生成、3D打印前处理、元宇宙空间资产构建。  
- **慎用**：实时交互类应用（如WebGL即时生成）因异步延迟（通常30s–5min）无法满足；单图生成3D对视角单一物体（如球体、圆柱）效果不稳定，建议优先使用四视图输入。  
- **最佳实践**：采用“生成→分割→重拓→贴图”链式任务，通过 `original_model_task_id` 复用中间结果，避免重复上传与计费；高面数需求务必选用 `Tripo-H3.1` 并显式设置 `geometry_quality: ultra`；Gaussian Splatting 输出适用于Three.js/Unreal Engine 5.3+ 实时渲染管线。

---

## 面向开发者的技术选型参考

| 选型目标 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| **最低接入门槛 & 快速验证** | 图像生成（`qwen-image-3.0-pro` 同步调用） | 支持 OpenAI 兼容模式，SDK 无缝迁移；响应快（<3s），调试友好；文档最完善。 |
| **最高输出质量与可控性** | 视频生成（`vidu/viduq3-pro_text2video`） + 3D生成（`Tripo/Tripo-H3.1`） | Vidu 在广告级语义理解与镜头语言上领先；Tripo-H3.1 提供行业少有的百万面网格与完整PBR贴图链。二者均需北京地域，但质量溢价显著。 |
| **成本敏感型规模化应用** | 图像生成（`z-image-turbo`） + 视频生成（`wan3/video-generation` 基础版） | `z-image-turbo` 单次成本约为 `wan2.7-image-pro` 的 1/3；万相3.0 统一模型降低维护成本，且无隐藏参数陷阱。 |
| **需与现有3D引擎深度集成** | 3D生成（`Tripo/Tripo-ImageToSplat` + `Tripo/Tripo-Retopology`） | Gaussian Splatting 直接适配 UE5.3+ 和 Three.js，免去传统网格渲染管线；重拓扑 v2.0 输出标准 FBX，支持 Unity/Blender 一键导入。 |
| **规避服务中断风险** | **全程避开所有标注“仅提供免费体验”的模型**（如 `wanx-poster-generation-v1`, `image-erase-completion`, `shoemodel-v1`） | 这些模型无 SLA、无付费通道、无故障兜底，生产环境使用等于引入单点故障。应以 `qwen-image-3.0-pro` 或 `wan2.7-image-pro` 替代。 |

> **重要提醒**：三类生成能力均**强制要求地域一致性**。建议在项目初始化阶段即完成 Workspace 创建、API Key 申请与 Endpoint 域名绑定，并将地域信息作为环境变量（如 `DASHSCOPE_REGION=cn-beijing`）注入CI/CD流程，从源头杜绝混用错误。

---  
*最后更新：2025年4月*  
*本文档依据百炼平台 v2025.04 版本 API 行为编写，模型能力与参数细节请以各模块最新官方 API 参考文档为准。*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


