# 图像生成、视频生成与 3D 生成能力对比

本文档面向百炼平台开发者，旨在系统性对比图像生成（Image Generation）、视频生成（Video Generation）与 3D 生成（3D Generation）三大模态生成能力的核心技术特性、接入方式与适用边界，辅助技术选型决策。随着多模态AIGC能力快速演进，不同生成任务对输入表达力、计算时延、资源调度、输出格式及后处理链路的要求差异显著。本对比基于当前（2024年Q3）百炼平台正式发布的 API 能力，覆盖模型支持、调用范式、计费策略与典型落地场景，不涉及未公开或灰度中的实验性功能。

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 生成（3D Generation） |
|------|------------------------------|------------------------------|---------------------------|
| **核心输入格式** | 文本（prompt）、单图/多图（URL 或 Base64）、掩码（mask_url）、参考图列表（element_list）、局部编辑区域坐标等 | 文本（prompt）、单图（首帧）、双图（首尾帧）、视频片段、音频（口型同步）、参考动作视频（动作模仿）、多参考图（参考生视频） | 文本（prompt）、单图（JPEG/PNG/WebP）、四视图数组（前/左/后/右）、已有3D模型（GLB/FBX/OBJ，用于后处理） |
| **核心输出格式** | PNG/JPEG（含透明通道支持，依模型而定）、Base64 编码图像、分镜组图（grid）、带元数据的 JSON（如 mask、segmentation map） | MP4（H.264 编码，1080p–4K）、WebM（部分模型）、JSON 中返回 `video_url` 及时长、帧率、分辨率等元信息 | GLB（默认）、FBX、OBJ、PLY、`.splat`（Gaussian Splatting）、贴图纹理包（ZIP）、分割部件子模型（GLB）、绑定骨架模型（FBX） |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`、`kling/kling-v3-omni-image-generation`、`vidu/viduq2-pro_reference2image`、`wanx-virtualmodel`（体验版） | `happyhorse/happyhorse-t2v`、`wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v3-omni-video-generation`、`wan2.2-s2v`（数字人） | `Tripo/Tripo-H3.1`（高精度网格）、`Tripo/Tripo-P1.0`（快速轻量）、`Tripo/Tripo-ImageToSplat`（高保真渲染）、`Tripo/Tripo-AutoRig`（自动绑骨） |
| **API 端点（统一路径结构）** | 同步：`/api/v1/services/aigc/multimodal-generation/generation`<br>异步：`/api/v1/services/aigc/multimodal-generation/generation`（创建任务） + `/api/v1/tasks/{task_id}`（轮询） | 异步专用：<br>`/api/v1/services/aigc/video-generation/video-synthesis`（主路径）<br>少数模型使用 `/api/v1/services/aigc/image2video/video-synthesis` | 异步专用：<br>`/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation` 为历史命名，实际承载3D能力） |
| **调用模式** | **混合模式**：<br>• 同步：`wan2.7-image-pro`、`z-image-turbo` 等低延迟模型，一次请求即返回结果<br>• 异步：海报生成、FaceChain 训练、复杂编辑等耗时任务，需两步调用 | **强制异步**：<br>所有模型均要求 `X-DashScope-Async: enable`，无同步接口；必须通过 `task_id` 轮询获取结果 | **强制异步**：<br>全部任务必须创建 → 轮询；`task_id` 有效期严格为 24 小时；不支持同步响应 |
| **地域可用性** | 全地域支持：华北2（北京）、新加坡、弗吉尼亚等，但**模型、API Key、Endpoint 必须三者地域一致** | 全地域支持：同图像生成，严格遵循地域隔离原则 | **仅限华北2（北京）**：<br>所有接口、API Key、Endpoint 均强制限定于 `cn-beijing`，跨地域调用直接失败 |
| **计费方式** | • 按“调用次数”计费（如 `qwen-image-3.0-pro`）<br>• 按“生成图像张数 × 分辨率等级”计费（如 `wan2.7-image-pro` 的 1K/2K/4K 档位）<br>• 部分垂直工具（虚拟模特、海报生成）**无付费通道，额度用尽即停用**<br>• FaceChain 训练按“次”计费（2.5 元/次） | • 按“任务次数”计费（无论生成时长或帧数）<br>• 部分模型（如 PixVerse 超分）按“输入视频时长 × 输出倍率”叠加计费<br>• 所有模型均无免费额度，首次调用即触发计费（控制台可配置预算告警） | • 按“任务次数”计费（基础生成、后处理、动画各为独立计费项）<br>• `Tripo-H3.1` 高精度生成费用高于 `Tripo-P1.0`<br>• 后处理任务（如贴图、重拓扑）按输入模型面数/复杂度分级计费<br>• **暂无免费额度**，需预充值或开通后付费 |
| **典型场景** | • 营销素材：创意海报、电商主图、社交媒体配图<br>• 内容生产：插画生成、风格迁移、图文混排（千问强项）<br>• 工业应用：擦除补全、实例分割、鞋靴试穿、虚拟模特<br>• 分镜预演：可灵/Kling 支持分镜组图生成 | • 短视频创作：文生短视频、产品演示动画、营销广告片<br>• 数字人驱动：口型同步（PixVerse）、动作模仿（HappyHorse）、数字人播报（WanX s2v）<br>• 影视辅助：首尾帧生成漫剧分镜、参考视频风格迁移<br>• 视频增强：超分、去噪、慢动作生成 | • 游戏与XR：从草图/照片快速生成可导入 Unity/Unreal 的 GLB 模型<br>• 工业设计：概念建模、零部件逆向重建、多视角三维扫描补全<br>• 实时渲染：生成 `.splat` 文件用于 WebGPU/WebGL 高性能展示<br>• 动画管线：自动绑骨 + 动作重定向，打通 3D 到动画工作流 |

## 各方案适用场景建议

### ✅ 推荐选择图像生成当：
- 需要**毫秒级响应**（如实时UI图标生成、A/B测试配图），优先选用 `z-image-turbo` 或 `wan2.7-image-pro`（同步调用）；
- 要求**中英文文本精准渲染**（如海报文案、Logo文字），首选 `qwen-image-3.0-pro`（专项优化）；
- 进行**可控编辑**（局部重绘、人像风格迁移、擦除补全），使用 `wanx-x-painting`（体验版）或迁移到 `qwen-image-3.0-pro` 的 I2I+mask 流程；
- 开发**垂直行业工具**（虚拟模特、鞋靴试穿），需评估免费额度是否满足POC需求；若需长期商用，应规划替代方案（如自建微调 pipeline）。

### ✅ 推荐选择视频生成当：
- 核心目标是**动态内容交付**（非静态画面），且能接受 10–120 秒生成延迟；
- 需要**强物理一致性或运动流畅性**（如机械运转、液体流动），选 `HappyHorse`；
- 需要**精细动作控制或口型同步**（如数字人客服、教育视频），选 `PixVerse` 或 `WanX s2v`；
- 有**多模态输入需求**（音频+首帧→口型视频；双图+提示→过渡动画），`PixVerse` 与 `Vidu` 支持更完备；
- **避免**将视频生成用于单帧高质量图像需求——其单帧质量与图像专用模型存在代差，且成本更高。

### ✅ 推荐选择 3D 生成当：
- 业务流明确需要**三维网格、拓扑结构或空间属性**（如游戏资产、CAD辅助、AR商品展示）；
- 输入源为**单张产品图或四视图线稿**，且需快速获得可编辑、可渲染的 3D 模型；
- 已有传统3D管线，需**自动化后处理**（重拓扑减面、智能分割、PBR贴图生成、格式转换），`Tripo` 后处理 API 提供标准化能力；
- 目标平台为 **WebGL/Unity/Unreal**，且对加载性能敏感，可选用 `Tripo-ImageToSplat` 生成 `.splat` 实现毫秒级加载；
- **注意约束**：必须部署于华北2（北京）环境；所有任务需自主实现轮询逻辑；高面数模型（`H3.1`）生成耗时较长（3–8分钟），不适合实时交互场景。

## 技术选型参考（致开发者）

| 选型考量点 | 图像生成 | 视频生成 | 3D 生成 |
|------------|----------|----------|----------|
| **开发复杂度** | ★★☆（同步调用简单；异步需轮询；OpenAI 兼容模式降低迁移成本） | ★★★（强制异步，需健壮轮询+超时重试；媒体文件上传/下载需额外处理） | ★★★★（强制异步+地域锁定；输入格式校验严格（如四视图顺序）；后处理依赖前序 `task_id`，需状态管理） |
| **调试友好性** | ★★★★（多数模型支持即时返回错误详情；图像可直接查看；提示词效果反馈快） | ★★★（需等待任务完成才能验证；视频需下载播放，调试周期长；错误常在 `RUNNING` 后才暴露） | ★★（生成耗时长；失败原因常为输入尺寸/格式/面数越界，日志提示较抽象；需结合 [Tripo Debug Guide](../../raw/model-user-guide/debug-guides/tripo-debug-guide.md) 排查） |
| **SDK 支持度** | ★★★★（DashScope Python/Java SDK 全面覆盖主流模型；OpenAI SDK 可复用） | ★★★（SDK 支持创建与轮询，但高级参数（如 PixVerse motion control）需手动构造 JSON） | ★★（SDK 仅提供基础 HTTP 封装；无高级封装（如自动轮询、部件名提取、splat 解析）；强烈建议自行封装 task 状态机） |
| **生产稳定性** | ★★★★（同步模型 SLA ≥99.9%；异步任务失败率 <0.5%；多地域容灾可选） | ★★★（受视频解码/编码链路影响，偶发超时；建议设置 120s+ 轮询超时） | ★★（华北2 单地域部署；`H3.1` 高负载时排队明显；建议预热关键任务或错峰调用） |
| **扩展性潜力** | ★★★★（可轻松接入 RAG 增强 prompt、与 OCR/CLIP 构建多模态工作流） | ★★★（可与 ASR、TTS、动作捕捉数据融合，构建端到端视频生成 Agent） | ★★★（天然适配 3D 编辑器插件（Blender/Unity）、WebXR 框架；与物理引擎集成潜力大） |

> **最后建议**：  
> - **不要为省事复用模型**：用图像模型生成单帧代替视频模型，或用视频模型抽帧生成3D——这将导致质量下降、成本上升、版权与合规风险增加；  
> - **务必校验地域一致性**：图像/视频生成虽支持多地，但混用 Key 与 Endpoint 是 401 错误第一大来源；3D 生成则必须锁定华北2；  
> - **善用异步任务 ID 关联**：在复杂工作流（如“图→视频→抽帧→3D重建”）中，用 `task_id` 作为跨服务追踪凭证，避免 URL 传递丢失上下文；  
> - **关注模型演进公告**：`qwen-image-3.0`、`wan2.7-*`、`Tripo-H

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


