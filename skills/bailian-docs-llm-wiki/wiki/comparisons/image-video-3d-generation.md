# 图像生成、视频生成与 3D 生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术边界与工程适配要点，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与 3D 生成（3D Generation）三大核心能力。对比聚焦实际落地的关键技术维度——包括输入/输出规范、模型生态、调用协议、地域约束、计费逻辑及典型适用场景，旨在为新项目选型、架构设计与成本预估提供可操作的技术决策依据。

> **说明**：所有能力均需通过百炼平台统一 API 网关接入，严格遵循「地域隔离」原则（API Key、Endpoint、Workspace ID 必须同属一个地域），跨地域调用将直接失败。本文所列信息基于截至 2024 年 Q3 的最新稳定版本（如 `wan2.7-image-pro`、`wan2.7-text2video`、`Tripo/Tripo-H3.1`）。

## 关键能力维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
|------|----------|----------|---------|
| **核心输入格式** | 文本（`prompt`）或 Base64/公网 URL 图像（支持单图、多图参考、局部掩码）；提示词建议 ≤200 字 | 文本（`prompt`）、首帧图（`first_frame_url`）、首尾帧（`first_frame_url` + `last_frame_url`）、参考视频（`ref_video_url`）、音频（`audio_url`）或检测后人像坐标（`face_bbox`）；提示词长度上限因模型而异（如 `wan2.7-text2video` ≤5000 字符） | 文本（`input.prompt`）、单张图像（`input.image`）、或多张图像（`input.images`，严格按 `[前, 左, 后, 右]` 顺序，空位填 `{}`）；三者互斥；提示词 ≤1024 字符；单图 ≤20MB，分辨率 20–6000px |
| **标准输出格式** | PNG/JPEG/WebP 图像 URL（同步返回）或异步任务结果中的 `output.image_url`；支持多张输出（`n=1–9`） | MP4 视频 URL（`output.video_url`），含预设分辨率（720P/1080P/4K）与帧率（15–25 fps）；部分模型额外返回预览图（`output.preview_url`） | GLB 格式 3D 模型（含 PBR 材质或无贴图基础模型）+ WebP 预览渲染图；产物分 `pbr_model_url`（带材质）、`base_model_url`（无贴图）和 `rendered_image_url`；所有 URL 有效期 **2 小时** |
| **主流支持模型** | `wan2.7-image-pro`（4K文生图/组图）、`qwen-image-3.0-pro`（强文本渲染）、`vidu/vidu-image-pro_reference2image`（UI像素级还原）、`z-image-turbo`（轻量快响应）、`kling/kling-v3-omni-image-generation`（分镜组图） | `wan2.7-text2video`（全栈编辑）、`HappyHorse`（物理真实/流畅运动）、`pixverse/pixverse-v6-t2v`（创意质量）、`wan2.2-s2v`（数字人说话）、`emo-v1`（唱演）、`animate-anyone-gen2`（动作迁移）、`video-style-transform`（风格重绘） | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速调试，≤2万面）；仅 Tripo 系列，无其他第三方模型接入 |
| **API 端点（推荐）** | 同步：`POST /api/v1/services/aigc/image-generation/generation`<br>异步：`POST /api/v1/services/aigc/image-generation/generation`（带 `X-DashScope-Async: enable`） | 异步专用：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`（万相2.7/HappyHorse/爱诗）<br>`POST /api/v1/services/aigc/image2video/video-synthesis`（万相2.1–2.6旧版） | 异步专用：<br>`POST /api/v1/services/aigc/video-generation/3d-generation`（仅北京地域） |
| **调用模式** | **混合模式**：<br>• 同步：`wan2.7-image-pro`、`qwen-image-3.0-pro`、`z-image-turbo`（<30s）<br>• 异步：`kling/kling-v3-image-generation`、`facechain-finetune`（1–2分钟） | **强制异步**：<br>所有模型必须携带 `X-DashScope-Async: enable` 请求头；任务耗时 1–5 分钟；`task_id` 有效期 24 小时 | **强制异步**：<br>必须携带 `X-DashScope-Async: enable`；任务耗时通常 2–8 分钟；`task_id` 有效期 24 小时；产物 URL 有效期 2 小时 |
| **地域支持** | 北京、新加坡、弗吉尼亚（多地域） | 北京、新加坡、弗吉尼亚（多地域） | **仅华北2（北京）**（硬性限制，不支持其他地域） |
| **计费方式** | 按生成张数计费；主账号与 RAM 子账号共享免费额度（90天内500张）；单价差异大：<br>• `wanx2.1-t2i-turbo`：0.16元/张<br>• `aitryon-plus`（AI试衣）：0.50元/张<br>• `facechain-finetune`：2.5元/次 | 按任务成功次数计费；无通用免费额度（部分模型提供试用额度）；单价依模型复杂度浮动：<br>• `wan2.7-text2video`（10s/720P）：约 1.2 元/次<br>• `pixverse/pixverse-lipsync`（对口型）：约 0.8 元/次<br>• `emo-v1`（唱演）：约 3.5 元/次 | 按任务成功次数计费；无免费额度；单价固定：<br>• `Tripo/Tripo-H3.1`：8.0 元/次<br>• `Tripo/Tripo-P1.0`：2.5 元/次 |
| **典型场景** | • 营销海报/电商主图批量生成<br>• UI 设计稿像素级还原与迭代<br>• 社交内容配图、文字艺术创作<br>• AI 试衣、虚拟模特写真<br>• 图像翻译（保留排版） | • 短视频广告脚本可视化（文→视频）<br>• 产品演示动画（图→视频）<br>• 数字人播报/直播/唱演内容生产<br>• 动作迁移（舞蹈/手势复现）<br>• 视频风格化重绘（日漫/油画/赛博朋克） | • 工业零件/消费电子外观建模（文→3D）<br>• 电商商品 3D 展示（单图→3D）<br>• 游戏资产快速原型（多视角图→3D）<br>• AR 应用素材生成（GLB 直接嵌入） |

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、强语义控制」场景  
- **优先选择**：当需求聚焦于静态视觉内容，且对生成速度、提示词精准度、多轮迭代效率有较高要求时（如每日生成数百张营销图、UI 设计师实时调整风格）。  
- **关键优势**：同步调用降低客户端延迟；支持局部重绘、文字渲染等精细化编辑；多模型覆盖从轻量到专业全光谱。  
- **规避场景**：无需动态表达、无时间维度需求的纯 3D 或视频类任务。

### ✅ 视频生成 —— 推荐用于「动态叙事、人机交互、跨模态驱动」场景  
- **优先选择**：当核心目标是生成具有时间连续性、运动逻辑或语音驱动行为的内容时（如数字人客服视频、短视频脚本转动画、产品功能演示动效）。  
- **关键优势**：原生支持音频驱动（TTS/录音）、动作迁移、首尾帧控制等高级编排能力；HappyHorse 与 PixVerse 在物理真实性和创意表现力上形成互补。  
- **规避场景**：仅需单帧高质量图像；对生成耗时极度敏感（无法接受 1–5 分钟等待）；无专业视频后期能力却期望电影级运镜。

### ✅ 3D 生成 —— 推荐用于「空间建模、工业/电商/AR 原型」场景  
- **优先选择**：当业务需要可交互、可测量、可集成至三维引擎（Unity/Unreal/Three.js）的几何模型时（如电商 3D 商品页、AR 试戴、工业设计初稿）。  
- **关键优势**：输出标准 GLB（含 PBR 材质），开箱即用；支持从文本、单图、四视图三种路径建模，适配不同数据准备条件；高精度模型满足工程级需求。  
- **规避场景**：仅需 2D 渲染图（应选图像生成）；需实时渲染或物理仿真（需对接专业 CAD/CAE 工具链）；部署环境不在北京地域（当前无替代方案）。

## 面向开发者的选型决策指南

| 决策问题 | 推荐答案 | 技术依据 |
|----------|----------|----------|
| **我的应用需要快速响应（<1s）生成一张海报，该选哪个？** | 选用 `wan2.7-image-pro` 或 `qwen-image-3.0-pro` 同步接口 | 二者均支持同步调用，平均耗时 <25s；`qwen-image-3.0-pro` 对中英文文字渲染更鲁棒；`wan2.7-image-pro` 支持更高分辨率（4K）与组图生成 |
| **我要为电商网站批量生成商品 3D 模型，但只有正面图，怎么办？** | 选用 `Tripo/Tripo-H3.1` 单图生3D 模式，并配置 `geometry_quality=ultra` & `pbr=true` | Tripo 明确支持单图输入；`ultra` 模式保障模型面数（≤200万）与细节；PBR 材质确保 Web 端渲染质感；注意：务必使用北京地域 Endpoint |
| **我想用客户提供的语音和一张照片生成数字人讲解视频，是否可行？** | 可行，但需两步：先调用 `emo-detect-v1` 获取人脸坐标，再调用 `emo-v1` 生成视频 | 所有数字人模型强制依赖前置检测；`emo-v1` 支持语音驱动唱演，输出 MP4 可直接嵌入网页；注意音频时长 <120s，图片需清晰正脸 |
| **我正在构建一个跨地域 SaaS 应用，用户分布在北京、新加坡、美国，能否统一调用？** | 图像/视频生成：可以（各区域独立配置 Workspace + Key）；3D 生成：**不可行**（仅北京支持） | 图像与视频模型已全域部署；3D 生成文档明确限定“仅华北2（北京）”，无新加坡/弗吉尼亚 endpoint，跨地域调用必失败 |
| **如何控制成本？哪些模型性价比最高？** | • 图像：`z-image-turbo`（0.16元/张，快且支持中英文字）<br>• 视频：`wan2.7-text2video`（基础文生视频，1.2元/次）<br>• 3D：`Tripo/Tripo-P1.0`（2.5元/次，适合原型验证） | 单价见上表；`z-image-turbo` 与 `Tripo-P1.0` 专为高频、低成本场景设计；避免在简单任务中误用 `facechain-finetune`（2.5元/次）或 `emo-v1`（3.5元/次） |

> **最后提醒**：所有能力均需通过百炼平台业务空间专属域名调用（非 `dashscope.aliyuncs.com`），请务必在控制台开通对应地域的 Workspace，并使用其专属 Endpoint。SDK 配置时，需显式设置 `DASHSCOPE_API_HOST` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


