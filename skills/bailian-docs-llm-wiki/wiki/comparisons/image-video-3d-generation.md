# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力模块。对比聚焦实际工程落地的关键维度，包括调用方式、模型生态、输入输出约束、计费逻辑及典型适用场景，旨在为技术选型提供清晰、可操作的决策依据。

---

## 能力维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|-----------------------------|--------------------------|
| **统一 API 端点** | `POST /v1/images/generations`（同步） | 多端点，按模型/功能区分：<br>• `/aigc/video-generation/video-synthesis`（HappyHorse / WanX 2.7+）<br>• `/aigc/image2video/video-synthesis`（WanX 2.2 首尾帧等旧路径）<br>• 各数字人专用路径（如 `/aigc/s2v/synthesis`） | `POST /api/v1/services/aigc/video-generation/3d-generation`（同步创建任务） |
| **调用模式** | **同步响应**：请求后立即返回完整 JSON（含图片 URL），无轮询 | **强制异步**：必须 `POST` 创建任务 → `GET` 轮询 `task_id` 状态 → 获取结果；`X-DashScope-Async: enable` 为必填 Header | **强制异步**：同视频生成，需创建任务 + 轮询；`task_id` 有效期 24 小时 |
| **输入格式** | • 文本提示词（`prompt`，≤512 字符）<br>• 可选图像（图生图/局部重绘，如 Kling）<br>• 支持 `mask`（仅 Kling） | • 文本（`prompt`）<br>• 单图/首帧（`img_url`）<br>• 首尾帧/多视角图（`first_frame_url` + `last_frame_url`）<br>• 参考视频（`video_url`）<br>• 音频+人像图（数字人）<br>• **所有图像/视频需公网可访问 URL** | • 文本（`input.prompt`，≤1024 字符）<br>• 单图（`input.image`，JPEG/PNG URL）<br>• 多图（`input.images`，严格 `[前, 左, 后, 右]` 顺序，2–4 张）<br>• **三者互斥，不可混用** |
| **输出格式** | • CDN 图片 URL（`.jpg`/`.png`，24 小时有效）<br>• 响应体含 `output.images[0].url` | • CDN 视频 URL（`.mp4`，通常 24 小时有效）<br>• 部分模型额外返回预览图、关键帧或元数据 | • GLB 模型文件 URL（PBR 材质版 `pbr_model_url` 或基础版 `base_model_url`）<br>• 渲染预览图 URL（`.jpg`，2 小时有效）<br>• 所有 URL 2 小时过期，需及时下载 |
| **支持模型（主力）** | • 万相（WanX-v1）：艺术风格强<br>• Z-Image：电商/设计向（尺寸/透明背景）<br>• Kling：图生图/局部重绘<br>• Qwen-VL 分支：多模态理解优<br>• Vidu（实验性图像模式） | • WanX 2.7（推荐）：全链路支持（文/图/参考/编辑）<br>• HappyHorse 系列：稳定通用型<br>• LivePortrait / EMO / AnimateAnyone：人像驱动垂直模型 | • `Tripo/Tripo-H3.1`：高精度（≤200 万面，`ultra` 模式）<br>• `Tripo/Tripo-P1.0`：快速调试（≤2 万面） |
| **地域绑定要求** | **无强绑定**：`dashscope.aliyuncs.com` 全域通用（但建议使用专属域名提升稳定性） | **强绑定**：Endpoint 必须匹配 WorkspaceId 与地域（如 `cn-beijing.maas.aliyuncs.com`），API Key 与 URL 地域不一致将直接失败 | **强绑定**：仅支持华北2（北京）地域，URL 固定为 `cn-beijing.maas.aliyuncs.com`，API Key 必须在此地域开通 |
| **计费方式** | • 按**成功生成的图片张数**计费（`n` 参数值）<br>• 不同模型单价不同（如 WanX 与 Z-Image 独立定价）<br>• 失败请求（4xx/5xx）不计费 | • 按**成功完成的视频任务数**计费<br>• 部分模型按**视频秒数 × 分辨率系数**阶梯计费（如 WanX 3.0 30 秒 1080p 为 1 单位，720p 为 0.6 单位）<br>• 数字人模型按**音频时长 + 人像处理复杂度**计费 | • 按**成功完成的 3D 任务数**计费<br>• `Tripo-H3.1` 与 `Tripo-P1.0` 单价不同（高面数模型费用更高）<br>• 任务失败（如输入校验不通过）不计费 |
| **典型场景** | • 社媒配图、营销海报生成<br>• 电商商品图（Z-Image 透明背景）<br>• 设计稿局部修改（Kling Inpainting）<br>• 多语言图文内容创作（Qwen-VL） | • 短视频内容批量生产（文生视频）<br>• 产品演示动画（图生视频/首尾帧）<br>• 数字人直播/课程讲解（EMO/LivePortrait）<br>• 视频风格迁移与特效增强 | • 游戏/AR 应用资产快速建模（文生3D）<br>• 工业零件逆向建模（单图/多图重建）<br>• 电商 3D 商品展示（GLB 直接嵌入网页）<br>• 教育可视化教具生成 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「即时反馈、轻量迭代、高并发」场景  
- **首选当**：需要快速产出静态视觉内容，且对生成延迟敏感（如 CMS 内容自动配图、A/B 测试多版本海报）。  
- **模型选择建议**：  
  - 追求艺术表现力 → 选 **万相（WanX）**，善用 `style_preset`；  
  - 需精确尺寸/透明背景 → 选 **Z-Image**，务必显式指定 `size`；  
  - 需基于原图局部修改 → 选 **Kling**，注意 `n=1` 限制；  
  - 多语言/图文混合提示 → 选 **Qwen-VL 分支**。  
- **避坑提示**：Vidu 图像模式为实验性功能，生产环境请勿依赖。

### ✅ 视频生成 —— 适合「内容深度表达、人机交互、跨模态联动」场景  
- **首选当**：需动态叙事、人物驱动或与现有视频资产协同（如营销短视频、虚拟主播、培训课件）。  
- **模型选择建议**：  
  - 通用需求、新项目启动 → 优先选用 **WanX 2.7**（接口统一、文档完善、性能稳定）；  
  - 需要极致可控的首尾帧动画 → 评估 **WanX 2.2 首尾帧模型**（注意路径为 `/image2video/...`）；  
  - 构建数字人应用 → 严格遵循 **“检测先行”流程**（先调 `emo-detect-v1` 等），再合成；  
  - 追求高动态画面（如运动镜头）→ 选 PixVerse `c1` 版本。  
- **避坑提示**：跨地域调用必然失败；未加 `X-DashScope-Async: enable` 将报错；数字人输入未经检测将直接拒绝。

### ✅ 3D生成 —— 适合「空间建模、工业设计、沉浸式体验」场景  
- **首选当**：需生成可交互、可渲染、可集成至引擎的三维资产，且接受分钟级等待（如游戏原型、电商 3D 展示、AR 导购）。  
- **模型选择建议**：  
  - 高保真交付（如工业部件、精细角色）→ 选 **Tripo-H3.1** + `geometry_quality: "ultra"`；  
  - 快速验证概念/批量草图建模 → 选 **Tripo-P1.0**（速度快、成本低）；  
  - 需无贴图轻量模型（如 Three.js 简单加载）→ 显式设置 `texture: false` 且 `pbr: false`。  
- **避坑提示**：仅北京地域可用；多图输入顺序必须为 `[前, 左, 后, 右]`；结果 URL 2 小时失效，务必及时下载。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键验证点 |
|----------|-----------|-------------|
| **需要 1 秒内返回一张图，用于网页实时预览** | 图像生成（WanX/Z-Image） | ✅ 检查 `prompt` 长度 ≤512；✅ Z-Image 是否已指定合法 `size`；✅ 使用同步端点 `/v1/images/generations` |
| **要将客户上传的商品图转成 30 秒带口播的营销视频** | 视频生成（WanX 2.7 + EMO） | ✅ 先调 `emo-detect-v1` 校验人像；✅ `audio_url` 为公网可访问 MP3/WAV；✅ Endpoint 与 API Key 同属北京地域 |
| **根据设计师手绘线稿，生成可导入 Blender 的高面数 3D 模型** | 3D生成（Tripo-H3.1） | ✅ 输入为单张 PNG URL；✅ 设置 `geometry_quality: "ultra"`；✅ 使用 `cn-beijing.maas.aliyuncs.com` 域名 |
| **构建一个支持“文生图→图生视频→视频加数字人”的全流程 AIGC 工具** | **组合方案**：<br>• 图像：WanX（文生图）→ 输出 URL<br>• 视频：WanX 2.7（图生视频，传上一步 URL）→ 输出视频 URL<br>• 数字人：LivePortrait（传视频 URL + 音频） | ✅ 全链路使用同一地域（推荐北京）；✅ 每步输出 URL 在有效期内传递；✅ 视频生成任务轮询间隔 ≥15 秒，避免触发 RPS 限流 |
| **低成本高频测试生成效果（每天数百次）** | 图像生成（Z-Image）或 3D生成（Tripo-P1.0） | ✅ Z-Image 支持批量 `n>1`（除 Kling 外）；✅ Tripo-P1.0 任务耗时短、单价低；❌ 避免在测试中调用 WanX 3.0 或 Tripo-H3.1（高成本/高延迟） |

> **最后提醒**：所有生成类 API 均受内容安全策略约束，禁止生成暴力、色情、政治敏感及可识别人脸内容。建议在生产环境接入前，使用沙箱环境进行合规性验证，并配置错误码捕获（如 `400` 输入违规、`422` 参数不合法、`404` 模型路径错误）。

---  
*本文档依据百炼平台 2024 年 Q3 最新 API 文档整理，模型能力与参数以 [官方模型 API 参考](https://help.aliyun.com/zh/bailian) 实时版本为准。*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


