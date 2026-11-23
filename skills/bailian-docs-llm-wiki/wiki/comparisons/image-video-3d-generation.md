# 图像、视频与 3D 内容生成能力对比

本文档面向百炼平台开发者，旨在系统性对比图像（Image）、视频（Video）与 3D 内容生成三大模态的核心能力，帮助技术团队在项目初期快速完成模型选型、架构设计与资源规划。随着多模态生成技术从单帧静态内容向时序动态、空间立体演进，理解各模态在输入表达力、输出可控性、工程集成复杂度及成本效益上的差异，已成为构建高质量 AIGC 应用的关键前提。

以下对比基于百炼平台当前（2024年Q3）正式 GA 的主流模型与 API 规范，覆盖能力边界、调用范式、地域约束、计费逻辑等关键维度，不包含实验性（Beta）或已归档（Legacy）模型。

## 核心能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 生成（3D Generation） |
|------|------------------------------|------------------------------|---------------------------|
| **输入格式** | 文本（prompt）、单图/多图 URL 或 Base64；支持混合输入（如文+图+风格图）；Kling/Vidu 对参考图 URL 编码有特殊要求（禁中文） | 文本、单图（首帧）、双图（首尾帧）、多图（参考图组）、视频文件（MP4/AVI/MOV ≤30s）、音频（WAV/MP3，仅数字人驱动） | 文本（≤1024 字符）、单图（PNG/JPEG/WebP）、四视图数组（前/左/后/右）、已有 3D 模型（GLB/FBX/OBJ ≤150MB）；Gaussian Splat 仅支持单图 |
| **输出格式** | PNG（Base64 或公网 URL），部分模型支持 WebP；创意工具可输出带 Alpha 通道、分层 PSD（需申请） | MP4（H.264 编码，720P–4K），部分模型支持 MOV；无音频轨道（除对口型类任务外） | GLB（默认）、FBX/OBJ/STL（格式转换）、`.splat`（Gaussian Splatting）、纹理贴图包（ZIP）、骨骼绑定文件（FBX + animation） |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/viduq3.1-fast_reference2image`, `z-image-turbo`, `facechain-finetune` | `wan3.0`, `wan2.7-videoedit`, `happyhorse/happyhorse-t2v`, `pixverse/pixverse-v6-max-t2v`, `vidu/viduq3-pro_text2video`, `kling/kling-v4-omni-reference-video-generation` | `Tripo/Tripo-H3.1`, `Tripo/Tripo-P1.0`, `Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-AutoRig`, `Tripo/Tripo-Texture`, `Tripo/Tripo-Retopology` |
| **API 端点路径** | `/api/v1/services/aigc/image-generation/generation`（同步）<br>`/api/v1/services/aigc/image-generation/async-generation`（异步） | `/api/v1/services/aigc/video-generation/video-synthesis`（统一异步端点） | `/api/v1/services/aigc/video-generation/3d-generation`（统一异步端点，注意路径含 `video-generation` 为历史兼容命名） |
| **调用模式** | **混合模式**：<br>• 同步：千问（DashScope 同步）、万相 2.6+/2.7、Z-Image（秒级返回）<br>• 异步：万相 V2.5 及以下、Kling、Vidu、FaceChain、所有创意工具（需轮询 `task_id`） | **强制异步**：<br>全部模型均仅支持异步（`X-DashScope-Async: enable` 必填），无同步接口；任务平均耗时 1–5 分钟 | **强制异步**：<br>全部模型均仅支持异步（`X-DashScope-Async: enable` 必填）；基础生成约 2–8 分钟，后处理（如重拓扑、贴图）可达 10–20 分钟 |
| **地域支持** | 北京、新加坡、弗吉尼亚（三地全量支持主流模型）；万相 V1 仅限北京（已废弃） | 北京、新加坡、美国（弗吉尼亚/俄亥俄）、德国（法兰克福）、日本（东京）、中国香港（多地扩展中） | **仅华北2（北京）地域**；所有文档（除主生成页外共14篇）明确限定，Workspace ID、API Key、Endpoint 必须严格匹配北京地域 |
| **计费方式** | • 按「生成张数」计费（如 `n=4` 计为 4 次）<br>• 创意工具（海报/擦除/试穿等）多数提供**有限免费额度（500次/50张）且不可续订**<br>• FaceChain 训练按「人脸检测+训练任务」双计费 | • 按「任务次数」计费（无论输出时长/分辨率）<br>• 部分模型（如 `videoretalk`）叠加 RPS 与并发任务数限制（如 RPS=1，最大并发=1）<br>• 无通用免费额度，新用户需单独申请体验包 | • 按「任务类型 + 参数等级」阶梯计费：<br> - 基础生成：`H3.1-standard` vs `H3.1-ultra` 差 2.5× 积分<br> - 贴图质量：`standard`/`detailed`/`extreme`（8K）逐级加价<br> - 重拓扑/动画绑定等高级操作额外计费<br>• 无公开免费额度，需预充值或开通企业账期 |
| **典型场景** | • 营销素材批量生成（电商主图、信息流广告）<br>• UI/UX 设计稿辅助（图标、Banner、组件）<br>• 个性化头像/虚拟模特/鞋靴试穿<br>• 社交媒体配图、AIGC 艺术创作 | • 短视频内容生产（抖音/快手/小红书竖屏视频）<br>• 数字人播报/课程讲解视频生成<br>• 产品演示动画（图生视频+动作迁移）<br>• 影视分镜预演、广告脚本可视化 | • 游戏资产快速原型（角色/道具/场景白模）<br>• AR/VR 应用 3D 内容供给（WebGL/GLB 直播）<br>• 工业设计验证（机械结构、家具摆件）<br>• Gaussian Splatting 实时渲染场景（元宇宙展厅、虚拟拍摄） |

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高吞吐、低延迟、强可控」场景  
- **适用项目**：电商自动化上新（千问同步生成+水印控制）、营销活动海报流水线（创意海报 API）、轻量级设计协作（万相局部重绘）、实时人像风格化（FaceChain 端到端写真）。  
- **慎用场景**：需严格像素级一致性的印刷品（如包装盒展开图），因模型对复杂几何/文字排版仍存在渲染偏差；高精度工业图纸生成（缺乏 CAD 语义理解）。  
- **工程提示**：优先选用 `qwen-image-3.0-pro`（同步+4K+OpenAI 兼容）或 `wan2.7-image-pro`（异步但支持自定义宽高比），避免接入已标记“推荐升级”的旧版模型（如 `wanx-v1`）。

### ✅ 视频生成 —— 推荐用于「中等时长、强调运动连贯性与叙事性」场景  
- **适用项目**：短视频平台内容工厂（HappyHorse 物理真实感）、数字人客服/讲师视频（万相 s2v + 对口型）、产品功能演示（图生视频+动作迁移）、品牌广告分镜预演（Kling 多参考帧融合）。  
- **慎用场景**：超长视频（>30s）连续生成（当前所有模型硬性截断）、高帧率慢动作（仅部分模型支持 60fps 输出）、专业影视级特效合成（缺乏多轨道编辑能力）。  
- **工程提示**：务必使用 `wan3.0` 或 `wan2.7`（统一 `/video-generation/` 路径），规避 `wan2.1–2.6` 的 legacy 路径（`/image2video/`）；轮询策略建议采用指数退避（初始 10s → 15s → 30s → 60s）。

### ✅ 3D 生成 —— 推荐用于「空间建模需求明确、接受较长生成周期」场景  
- **适用项目**：游戏开发前期资产探查（Tripo-H3.1 生成+AutoRig 绑骨）、AR 商品展示（GLB 直出+Texture 贴图）、建筑可视化草模（多图生3D）、实时渲染应用（ImageToSplat → `.splat` 查看器）。  
- **慎用场景**：需要精确拓扑结构的 CAD/CAE 工程仿真（Tripo 输出为近似网格，非参数化建模）、高频迭代的 UI 动效原型（生成耗时远高于 Figma 插件）、移动端轻量 3D（GLB 体积优化需额外压缩步骤）。  
- **工程提示**：必须锁定北京地域；后处理链路强烈建议使用 `original_model_task_id` 引用前序任务（避免重复上传大文件）；动画流程需严格遵循 `RigCheck → AutoRig → AnimationRetarget` 顺序，Mixamo 绑定模型不可跨入重定向环节。

## 技术选型决策指南（面向开发者）

| 决策问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **我的应用需要毫秒级响应（如设计工具实时预览）？** | ✅ 图像生成（同步模式）<br>❌ 视频/3D（强制异步，最低延迟 >60s） | 千问/万相同步接口平均响应 <1.5s（4K），满足交互式体验；视频/3D 最短任务耗时仍达 2 分钟级。 |
| **我需生成带语音/口型同步的数字人视频？** | ✅ 视频生成（`wan2.2-s2v` + `wan2.2-lip-sync`）<br>❌ 图像/3D（无原生音频处理能力） | HappyHorse/PixVerse 支持音画对齐，Tripo 仅支持骨骼动画，无语音驱动模块。 |
| **我要为 Unity/Unreal 引擎批量导入 3D 模型？** | ✅ 3D 生成（Tripo-ConvertFormat + Texture）<br>⚠️ 图像生成（仅能输出 2D 参考图） | Tripo 原生支持 FBX 导出、PBR 贴图生成、LOD 网格简化，直接对接引擎管线；图像生成无法提供空间数据。 |
| **我的业务部署在新加坡地域，能否使用全部能力？** | ✅ 图像 & 视频（全功能支持）<br>❌ 3D（完全不可用） | 3D 服务硬性绑定北京地域，跨地域调用必失败；图像/视频在新加坡已 GA 所有主力模型。 |
| **我需要低成本验证创意可行性？** | ✅ 图像生成（大量免费额度）<br>⚠️ 视频（需申请体验包）<br>❌ 3D（无免费额度） | 创意海报、图像擦除、风格重绘等图像工具提供 500 次免费调用；视频/3D 均需预充值，试错成本显著更高。 |

> **最后建议**：对于复合型需求（如「生成商品图 → 合成商品视频 → 构建3D展示页」），应采用**分阶段流水线设计**：以图像生成作为前端快速反馈层，视频生成作为中台内容生产层，3D 生成作为后台高价值资产沉淀层，并通过统一任务 ID 与对象存储（OSS）实现跨模态结果复用。避免强行用单一模态覆盖全链路——这既违背技术合理性，也导致资源浪费与体验劣化。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


