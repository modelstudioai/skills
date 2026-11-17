# 多模态内容生成 API 对比：图像、视频与 3D 生成

本对比旨在为开发者提供清晰、可落地的技术选型参考，聚焦百炼平台当前主力多模态生成能力——**图像生成（Image Generation）、视频生成（Video Generation）与 3D 生成（3D Generation）**三大方向。随着 AIGC 应用从静态内容向动态化、空间化演进，不同模态在输入表达力、计算复杂度、输出交付形式及工程集成路径上存在显著差异。本文基于官方文档最新版本（截至 2024 年 Q2），从接口设计、模型能力、调用范式、资源约束与商业可用性等维度进行横向分析，帮助团队在原型验证、MVP 快速上线或工业级生产部署等不同阶段做出理性决策。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 生成（3D Generation） |
|------|------------------------------|-------------------------------|---------------------------|
| **核心输入格式** | 文本（`prompt`） + 可选 1–14 张参考图（URL/Base64，支持 JPG/PNG/WEBP/BMP）；FaceChain 等垂直模型需特定人脸图像 | 文本（`prompt`） / 首帧图（`first_frame_url`） / 首尾帧（`first_frame_url`+`last_frame_url`） / 混合媒体（`media` 数组含 image/video/audio URL）；所有输入必须公网可访问 | 文本（`prompt`） / 单图（`image`） / 四视图数组（`images: [front, left, back, right]`） / 已生成模型任务 ID（`original_model_task_id`）或模型文件 URL（GLB/FBX/OBJ ≤150MB） |
| **核心输出格式** | PNG（默认，含透明通道支持）；`qwen-mt-image-2.0` 固定输出 JPG | MP4（H.264 编码，含音频轨道）；部分模型支持纯视频流（无音频） | GLB（默认）、FBX、USDZ、OBJ、SPLAT（Gaussian Splatting）、PBR 贴图包（ZIP）、动画文件（GLB/FBX）；格式由 `parameters.format` 或 `quad=true` 等参数控制 |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/viduq2-pro_reference2image`, `z-image-turbo`, `qwen-mt-image-2.0`, FaceChain | `happyhorse/happyhorse-t2v`, `wanx/wanx3.0-video-generation`, `pixverse/pixverse-v6-t2v`, `kling/kling-v4-omni-video-generation`, `vidu/viduq3-drama_reference2video`, `wanx/wan-animate-move` | `Tripo/Tripo-H3.1`（高精网格）, `Tripo/Tripo-P1.0`（快速生成）, `Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-Segmentation`, `Tripo/Tripo-AutoRig`, `Tripo/Tripo-AnimationRetarget` |
| **API 端点（统一协议）** | 同步：`POST /api/v1/services/aigc/image-generation`<br>异步：`POST /api/v1/services/aigc/image-generation/generation`（带 `X-DashScope-Async: enable`） | 异步专用：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`<br>（强制 `X-DashScope-Async: enable`） | 异步专用：<br>`POST /api/v1/services/aigc/video-generation/3d-generation`<br>（强制 `X-DashScope-Async: enable`；注意路径中仍含 `video-generation`，属历史命名） |
| **调用模式** | **混合模式**：<br>• 同步：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo` 等（秒级返回 PNG URL）<br>• 异步：`kling`、`vidu`、创意工具类（需轮询 `GET /tasks/{task_id}`） | **强制异步**：<br>所有模型均不支持同步调用；必须两步：① 创建任务获 `task_id`；② 轮询结果（`status=SUCCESS` 后取 `output.video_url`） | **强制异步**：<br>全链路异步；必须两步：① 创建任务；② 轮询（`task_id` 有效期严格 24 小时）；后处理任务强依赖前序 `task_id` |
| **地域支持** | 华北2（北京）、新加坡、美国（弗吉尼亚）等多地；**模型与地域强绑定**，跨地域调用失败 | 华北2（北京）、新加坡、美国（弗吉尼亚）、德国（法兰克福）、日本（东京）、中国香港；**模型、Key、Endpoint 必须同地域** | **仅华北2（北京）**；控制台开通、API Key、Endpoint、模型部署全部限定该地域，跨地域请求必然失败 |
| **计费方式** | • 商用模型（如 `qwen-image-3.0-pro`, `wan2.7-image-pro`）按**生成张数 + 分辨率档位**计费（如 1K/2K/4K）<br>• 免费体验模型（如 `wanx-x-painting`, `shoemodel-v1`）额度用尽即停用，**不可付费开通** | 按**任务成功执行次数 + 输出规格**计费：<br>• 基础档（720P/15s）<br>• 高清档（1080P/30s）<br>• 专业档（4K/60s/多参考）<br>• 部分模型（如 `viduq3-drama`）按“参考视频时长×分辨率”复合计费 | 按**任务类型 + 资源消耗**计费：<br>• 基础生成：面数上限（`face_limit`）决定档位（如 `P1.0` 50–20,000 面 vs `H3.1 ultra` 最高 200 万面）<br>• 后处理：`quad=true`、`texture_quality=extreme`、`animations` 多于 1 个等触发高级计费<br>• 所有操作均以 `task_id` 为计费单元 |
| **典型场景** | • 创意海报/电商主图生成<br>• 人像写真/虚拟模特批量产出<br>• UI 设计稿辅助生成与局部重绘<br>• 多语言图像翻译（`qwen-mt-image-2.0`） | • 短视频广告/社交媒体内容生成<br>• 影视分镜预演与动态脚本可视化<br>• 数字人口型同步与动作驱动<br>• 产品演示视频（图生视频+风格迁移） | • 游戏资产快速建模（文生/图生低多边形模型）<br>• 工业零部件逆向重建（四视图→3D）<br>• 实时渲染内容生产（Gaussian Splatting）<br>• 3D 动画管线自动化（绑骨→重定向→导出） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高频、轻量、实时反馈」场景  
- **推荐选用**：当需求聚焦于**单帧视觉内容产出**，且对响应延迟敏感（如设计协作工具、AIGC 插件、营销素材平台），优先选择 `qwen-image-3.0-pro`（同步+高兼容）或 `wan2.7-image-pro`（4K+多图融合）。  
- **规避风险**：生产环境**严禁依赖免费体验模型**（如 `wanx-x-painting`, `image-instance-segmentation`），因其无续费路径，额度耗尽即服务中断。  
- **进阶提示**：需多图一致性（如角色多姿态）或工业级稳定性，选 `vidu/viduq2-pro_reference2image`（支持最多 14 张参考图+上下文锚定）；需超低延迟（<1s），选 `z-image-turbo`（轻量文生图）。

### ✅ 视频生成 —— 适合「动态叙事、跨模态协同」场景  
- **推荐选用**：当目标是**生成具备时间维度的连贯内容**（如短视频、教学演示、数字人播报），首选 `wanx/wanx3.0-video-generation`（All-in-One 统一模型，支持首尾帧+参考生视频）或 `happyhorse/happyhorse-t2v`（物理真实感强，适合产品展示）。  
- **规避风险**：避免使用已标记为“早期模型”的 `wanx2.1-i2v-turbo` 等旧版模型；务必确认所选模型支持所需输入模态（如 `kling-v4` 支持关键帧组合，而部分模型仅支持首帧）。  
- **进阶提示**：需口型同步或动作模仿，选 `pixverse/pixverse-v6-t2v`；需剧集/广告级参考一致性，选 `vidu/viduq3-drama_reference2video`（专为长时序参考优化）。

### ✅ 3D 生成 —— 适合「空间建模、工业级管线」场景  
- **推荐选用**：当需求明确指向**三维空间资产创建与加工**（如游戏开发、AR 应用、智能制造），且团队具备 3D 工程能力，应基于 `Tripo/Tripo-H3.1`（精度优先）或 `Tripo/Tripo-P1.0`（速度优先）构建端到端工作流。  
- **规避风险**：**仅限华北2（北京）地域**，若业务部署在新加坡或海外，需评估数据合规与网络延迟影响；后处理任务（如贴图、绑骨）必须引用同一账号下有效 `task_id`，跨账号或失败任务引用将直接报错。  
- **进阶提示**：需实时渲染交付，启用 `Tripo/Tripo-ImageToSplat`；需动画绑定，严格遵循 `RigCheck → AutoRig → AnimationRetarget` 三步流程，并注意 `mixamo` 绑骨规范与重定向的互斥限制。

---

## 面向开发者的选型决策指南

| 决策问题 | 推荐行动 |
|----------|----------|
| **我的应用需要毫秒级图像响应？** | ✅ 选 `qwen-image-3.0-pro` 或 `z-image-turbo`（同步调用）；❌ 避免 `kling`/`vidu` 等异步模型。 |
| **我要生成 10 秒以上、带音画同步的营销视频？** | ✅ 选 `pixverse/pixverse-v6-t2v`（口型+动作）或 `vidu/viduq3-drama_reference2video`（长参考）；❌ 不要尝试用图像生成 API 拼接视频（无时序一致性保障）。 |
| **我有 4 张产品实物照片（前/左/后/右），想快速生成 3D 模型用于网页展示？** | ✅ 用 `Tripo/Tripo-H3.1` + `images` 数组输入；✅ 输出选 `GLB` 格式；⚠️ 确保图片为 JPEG/PNG、≥256×256、≤20MB。 |
| **我的服务部署在新加坡，但需要调用 Vidu 图像生成？** | ✅ 使用新加坡地域的 Vidu 模型（如 `vidu/viduq2-pro_reference2image`）；❌ 不可复用北京 API Key 或 Endpoint。 |
| **我想在现有 OpenAI SDK 中无缝接入？** | ✅ `qwen-image-3.0-pro` 支持 OpenAI Images 兼容模式（仅需切换 `base_url` 和 `model`）；❌ 其他模型需改用 DashScope SDK 或原生 HTTP 调用。 |
| **我需要批量生成 1000 张人像写真并商用？** | ✅ 用 `FaceChain` 训练专属人像模型，再调用 `qwen-image-3.0-pro` 批量生成；✅ 确认 `watermark=false`；❌ 不要用 `wanx-x-painting`（免费体验，不可商用）。 |

> **最后提醒**：所有多模态 API 均遵循「地域强隔离」原则——**API Key、Endpoint URL、模型部署地域三者必须完全一致**。强烈建议在百炼控制台开通「业务空间」，使用专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更优性能、独立配额与 SLA 保障。技术选型不应仅看模型名称，而需结合自身基础设施、合规要求与交付节奏综合判断。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


