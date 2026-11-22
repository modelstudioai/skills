# 图像、视频与 3D 内容生成能力对比

为帮助开发者快速理解百炼平台在[多模态](../concepts/multi-modal.md)内容生成领域的技术布局与能力边界，本文系统对比图像（Image）、视频（Video）与 3D 内容生成三大核心能力模块。对比聚焦实际工程落地的关键维度——包括输入/输出形态、模型生态、调用协议、地域约束、计费策略及典型适用场景，旨在为技术选型提供清晰、可操作的决策依据。所有信息均基于当前（2024年Q3）百炼平台正式发布的 API 文档与运行规范。

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 生成（3D Generation） |
|------|------------------------------|------------------------------|---------------------------|
| **核心能力** | 文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、垂直工具（虚拟模特/海报/擦除等） | 文生视频（T2V）、图生视频（I2V）、参考生视频、视频编辑、动作迁移、数字人驱动 | 文/图生3D网格、Gaussian Splatting、贴图生成、网格分割/补全/重拓扑、格式转换、自动绑骨与动画重定向 |
| **输入格式** | ✅ 文本（`prompt`）<br>✅ 单图/多图（URL 或 Base64，PNG/JPEG）<br>⚠️ 可灵不支持透明通道；万相 V2 要求宽高比 ∈ [1:4, 4:1] | ✅ 文本（`prompt`）<br>✅ 首帧/首尾帧图像（URL）<br>✅ 参考视频/图像集（`reference_video_url`, `reference_images`）<br>✅ 音频（WAV/MP3，用于对口型）<br>⚠️ 所有 URL 必须公网可访问；OSS 路径需加 `X-DashScope-OssResourceResolve: enable` | ✅ 文本（`prompt`，≤1024 字符）<br>✅ 单图（JPEG/PNG，≤20MB）<br>✅ 多图（严格4视角：前/左/后/右）<br>✅ 已生成3D模型（GLB/FBX/OBJ，≤150MB，通过 `model_url` 或 `original_model_task_id` 引用） |
| **输出格式** | ✅ Base64 编码图像（同步）<br>✅ 公网可访问 URL（同步/异步）<br>✅ 支持水印开关（`watermark: false`） | ✅ 公网可访问 MP4 视频 URL（异步）<br>✅ 输出含元数据（分辨率、时长、FPS）<br>❌ 不直接返回二进制流或帧序列 | ✅ GLB（默认）、FBX、OBJ、USDZ、PLY 等格式 URL<br>✅ Gaussian Splatting 的 `.splat` 文件<br>✅ 分割结果 JSON（含部件名与 mesh URL）<br>✅ 绑骨模型（`.fbx` + `.json` 动画配置） |
| **主流支持模型** | • 千问系列：`qwen-image-3.0-pro`（主力推荐）<br>• 万相系列：`wan2.7-image-pro`（4K）、`wan2.6-t2i`（V2文生图）<br>• 可灵/Vidu：`kling-v3-omni-image-generation`、`vidu-image-pro_reference2image`<br>• 轻量/垂直：`z-image-turbo`、`facechain-finetune`、`wanx-poster-generation-v1`（免费体验） | • HappyHorse：物理真实运动建模<br>• 万相：`wan2.7-videoedit`（All-in-One）、`wan2.2-s2v`（数字人）<br>• 爱诗（PixVerse）：`pixverse-v6-max-t2v`（高速动态）<br>• 可灵/Vidu/MiniMax：[多模态](../concepts/multi-modal.md)参考生视频支持 | • Tripo 基础模型：`Tripo-H3.1`（高精度）、`Tripo-P1.0`（快速专业版）<br>• Tripo 后处理：`Tripo-Texture`、`Tripo-Segmentation`、`Tripo-Retopology`<br>• Tripo 动画：`Tripo-AutoRig`、`Tripo-AnimationRetarget` |
| **API 端点协议** | • 同步调用：千问、万相 `wan2.7-image-pro`、Z-Image 等低延迟模型<br>• 异步调用：可灵、Vidu、万相 I2I 编辑类、所有创意工具模型<br>• OpenAI 兼容模式：仅千问系列（切换 `base_url` + `model`） | ❌ **全部强制异步**<br>• 必须设置请求头 `X-DashScope-Async: enable`<br>• 任务创建 → 轮询 `task_id` → 获取 `output.video_url` | ❌ **全部强制异步**<br>• 必须设置请求头 `X-DashScope-Async: enable`<br>• 统一端点：`/api/v1/services/aigc/video-generation/3d-generation`（注意路径含 `video-generation`，属历史命名）<br>• 轮询 `task_id` 获取结构化结果 |
| **地域与部署约束** | • 模型、API Key、Endpoint **三者必须同地域**（华北2/新加坡/弗吉尼亚等）<br>• `wan2.7-image-pro` 仅限北京/新加坡；`wan2.6-t2i` 在弗吉尼亚可用<br>• 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | • 模型、API Key、Endpoint **三者必须同地域**<br>• 部分模型地域受限：`wan2.2-s2v`、`videoretalk` 仅限华北2（北京）<br>• 无跨地域代理方案，混用必失败 | • **全域仅支持华北2（北京）地域**<br>• Workspace ID、API Key、服务开通、Endpoint 均须在北京完成<br>• 使用固定域名：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` |
| **计费方式** | • 主力模型（千问 Pro、万相 Pro、可灵、Vidu）：按 token/图片张数/分辨率阶梯计费<br>• 轻量/垂直模型（`z-image-turbo`、`shoemodel-v1`、`wanx-poster-generation-v1` 等）：**免费额度用完即不可调用，且不支持付费开通**<br>• 注意：免费模型稳定性与长期维护性低于主力模型 | • 所有模型均按 **任务成功执行次数 + 分辨率/时长/帧率** 计费<br>• 无“免费额度”概念：任务失败不扣费，但轮询、重试不产生费用<br>• 高阶能力（如数字人、超清、长时视频）单价显著高于基础 T2V | • 按 **任务类型 + 输入复杂度 + 输出质量** 计费<br>• 基础生成（文/图生3D）：按 `geometry_quality`（standard/ultra）和面数上限计费<br>• 后处理/动画：独立计费（如贴图生成按 `texture_quality` 分档）<br>• 无免费额度，但支持预估费用接口（`/estimate-cost`） |
| **典型响应耗时** | • 同步：300–2000 ms（千问/万相 Pro）<br>• 异步：2–15 秒（多数编辑类），最长 ≤60 秒 | • 异步：**1–5 分钟**（标准 T2V/I2V）<br>• 复杂任务（如参考生视频+超清+长时）可达 8–12 分钟<br>• 数字人驱动需额外人脸检测前置步骤（+2–5 秒） | • 异步：**2–8 分钟**（文/图生3D）<br>• 后处理任务：10–90 秒（贴图/分割）至 3–5 分钟（重拓扑/动画重定向）<br>• Gaussian Splatting 生成约 1–3 分钟 |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高频、轻量、强可控」需求  
- **推荐场景**：营销素材批量生成（海报/ Banner/ 社媒配图）、AIGC 辅助设计（UI 原型图、电商主图）、个性化头像/虚拟模特定制、图像修复与编辑（擦除/扩图/风格迁移）。  
- **选型建议**：  
  - 追求**开箱即用 & 生产稳定** → 优先选用 `qwen-image-3.0-pro`（OpenAI 兼容、参数丰富、水印可关）；  
  - 需要**4K 高清输出 & 中英文字精准渲染** → `wan2.7-image-pro`（万相）或 `vidu-image-pro_reference2image`（Vidu）；  
  - 快速原型验证或低预算项目 → `z-image-turbo`（注意：仅限非关键链路）；  
  - **避免在生产环境依赖** `wanx-poster-generation-v1` 等免费创意工具模型（无付费通道，额度耗尽即中断）。

### ✅ 视频生成 —— 适合「中低频、高价值、需时序表达」需求  
- **推荐场景**：短视频广告生成、产品演示动画、教育课件视频化、数字人直播/客服、游戏过场动画辅助制作、AIGC 影视分镜预演。  
- **选型建议**：  
  - 平衡**画质、时长与成本** → `wan2.7-videoedit`（万相 All-in-One，支持 30 秒，协议统一）；  
  - 强调**物理真实感与运动连贯性**（如工业仿真、建筑漫游）→ `HappyHorse`；  
  - 需要**高速动态表现**（打斗、法术、粒子特效）→ `pixverse-v6-max-t2v`（爱诗）；  
  - 构建**品牌数字人形象** → `wan2.2-s2v`（万相数字人）+ 配套人脸检测接口；  
  - **切勿尝试同步调用**：所有视频 API 均强制异步，缺失 `X-DashScope-Async: enable` 将直接报错。

### ✅ 3D 生成 —— 适合「专业级、长流程、需下游集成」需求  
- **推荐场景**：游戏资产快速原型（角色/道具/场景）、电商 3D 商品展示（AR 试穿/旋转查看）、工业设计可视化（零件建模/装配模拟）、AIGC 动画制作（绑定+重定向驱动）、数字孪生基础建模。  
- **选型建议**：  
  - 首选 `Tripo-H3.1`：需高精度网格（≤200 万面）、支持重拓扑与 PBR 贴图；  
  - 快速验证或轻量应用 → `Tripo-P1.0`（2 万面限制，响应更快）；  
  - 需要**即时渲染效果**（如 Web 端预览）→ 优先生成 Gaussian Splatting（`Tripo-ImageToSplat`）；  
  - 构建可动画角色 → 必须串联 `Tripo-AutoRig` → `Tripo-AnimationRetarget` 流程，并确保输入模型未使用 Mixamo 绑骨；  
  - **关键约束**：所有环节必须在北京地域闭环，不可跨地域组合调用（如用新加坡 Key 请求北京 3D 接口）。

## 面向开发者的选型决策指南

| 决策问题 | 推荐答案 | 技术依据 |
|----------|----------|----------|
| **我的应用需要实时返回图像（<1s），能否用视频/3D 模块？** | ❌ 否。视频与 3D 全部强制异步（分钟级），仅图像生成中的千问/万相 Pro 支持同步低延迟响应。 | 视频/3D 文档明确要求 `X-DashScope-Async: enable`，且无同步端点；图像文档明确列出同步模型列表。 |
| **我已有大量 PNG 图片，想批量生成对应 3D 模型并导出 FBX 供 Unity 使用，如何设计流程？** | ✅ 可行。1) 调用 `Tripo/Tripo-ImageTo3D`（单图）→ 2) 调用 `Tripo/Tripo-Retopology`（优化拓扑）→ 3) 调用 `Tripo/Tripo-ConvertFormat

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


