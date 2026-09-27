# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文档系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**工程落地关键维度**，包括调用方式、输入输出约束、模型生态、计费逻辑及典型适用场景，旨在为技术选型提供客观、可执行的决策依据。

---

## 关键能力对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **核心定位** | 单帧高质量视觉内容生成与编辑 | 时序连续的动态内容生成与人像驱动 | 空间结构化的三维网格与材质建模 |
| **输入格式** | • 纯文本 [prompt](../guides/prompt.md)（≤512 字符）<br>• 可选 `image_url`（图生图/局部重绘）<br>• 可选 `mask_url`（仅创意工具） | • 文本 [prompt](../guides/prompt.md)（≤5000 字符，依模型而异）<br>• `img_url`（首帧/首尾帧）<br>• `video_url` / `audio_url`（参考生视频、对口型等）<br>• `face_bbox` + `ext_bbox`（人像驱动类必需前置检测） | • 纯文本 [prompt](../guides/prompt.md)（≤1024 字符）<br>• 单张 `image` URL（JPEG/PNG）<br>• 四张 `images` 数组（前/左/后/右，互斥） |
| **输出格式** | • `url`：临时直链（有效期 1 小时）<br>• 格式：PNG/JPEG（由模型决定）<br>• 含 `revised_prompt`（模型优化提示词） | • 异步返回 `output.video_url`（临时直链，有效期 2 小时）<br>• 格式：MP4（H.264 编码）<br>• 部分模型支持额外元数据（如帧率、分辨率） | • `pbr_model_url`：GLB（含 PBR 材质，`pbr=true` 时返回）<br>• `base_model_url`：GLB（无贴图，需显式设 `texture=false && pbr=false`）<br>• `rendered_image_url`：WebP 预览图（有效期 2 小时） |
| **支持模型（主力）** | • 千问（Qwen2-VL 图像版）<br>• 万相（WanX-v1）<br>• Z-Image（轻量低延迟）<br>• 可灵（Kling）<br>• Vidu（单帧预览）<br>• 创意工具（图生图/涂鸦/局部重绘） | • HappyHorse（物理真实感）<br>• 万相（Wan2.7 / Wan3.0，All-in-One）<br>• 爱诗（PixVerse，细分能力强）<br>• EMO / LivePortrait / AnimateAnyone（人像驱动）<br>• 风格重绘 / 视频超清（后处理） | • `Tripo/Tripo-H3.1`（高精度，≤200 万面）<br>• `Tripo/Tripo-P1.0`（快速，≤2 万面） |
| **API 端点** | 同一同步端点：<br>`POST https://dashscope.aliyuncs.com/api/v1/images/generations` | 异步任务端点（地域强绑定）：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>（部分旧模型使用 `/image2video/video-synthesis`） | 异步任务端点（华北2专属）：<br>`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` |
| **调用模式** | **同步阻塞**（响应时间 ≤60 秒；Z-Image ≤15 秒） | **强制异步**（创建任务 → 轮询 `task_id`）<br>任务耗时：1–5 分钟<br>`task_id` 有效期：24 小时 | **强制异步**（创建任务 → 轮询 `task_id`）<br>任务耗时：通常 2–8 分钟<br>`task_id` 有效期：24 小时 |
| **地域要求** | 无强地域绑定（通用域名 `dashscope.aliyuncs.com` 可用） | **强地域绑定**：模型、Endpoint、API Key 必须同属一个地域（如 `cn-beijing`） | **强地域绑定**：仅支持 **华北2（北京）** 地域，Endpoint 与 API Key 必须匹配 |
| **计费方式** | • 按**成功生成图片数量**计费（`n` 参数值）<br>• 不同模型单价不同（如 Z-Image 更低价）<br>• 失败请求不计费 | • 按**成功完成的任务数**计费<br>• 各模型独立定价（如 EMO、VideoRetalk 单独计价）<br>• 免费额度按模型粒度分配 | • 按**成功完成的 3D 任务数**计费<br>• `H3.1`（高面数）单价高于 `P1.0`（快速）<br>• 无免费额度（需单独开通配额） |
| **典型场景** | • 营销海报/电商主图生成<br>• UI 设计稿辅助出图<br>• 社媒配图 & 风格化插画<br>• 局部编辑（换背景、修细节） | • 短视频内容批量生产（广告/教育）<br>• 数字人播报/唱演/舞蹈驱动<br>• 产品演示视频生成（图→视频）<br>• 口型同步/风格迁移后处理 | • 游戏/AR 应用资产快速建模（文→3D）<br>• 电商商品 3D 展示（单图→3D）<br>• 工业设计概念验证（多视角图→3D）<br>• 元宇宙空间构件生成 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「即时反馈、高频迭代、轻量集成」
- **推荐场景**：  
  - 前端交互式设计工具（如 AI 画布），需 <2 秒级响应 → 优先选用 **Z-Image**；  
  - 高质量艺术创作或品牌视觉输出 → 选用 **万相（WanX-v1）** 或 **千问（Qwen2-VL）**；  
  - 需要基于现有图片做局部修改（如换天空、改服饰）→ 使用 **创意工具模块**；  
  - 需要严格控制构图与主体一致性 → **可灵（Kling）** 支持长宽比自定义与多步优化。
- **避坑提示**：避免用 Z-Image 处理图生图需求（明确不支持 `image_url`）；Vidu 的 `size` 参数仅接受 `"1024x1024"` 字符串，不可传数组。

### ✅ 视频生成 —— 适合「内容规模化、人机协同、专业表达」
- **推荐场景**：  
  - 批量生成营销短视频 → **万相 Wan3.0**（All-in-One，协议统一）或 **HappyHorse**（物理真实）；  
  - 数字人业务（播报、唱跳、表情包）→ 严格按流程：先调用 `xxx-detect` API 获取 bbox，再调用对应驱动模型（如 `emo-v1`）；  
  - 需要精细控制运动节奏或特效 → **万相 Wan2.7+ 模板参数**（如 `template: "hanfu-1"`）；  
  - 对口型/动作模仿等垂直需求 → **爱诗（PixVerse）系列**（`c1` 动态强，`v6` 通用稳）。
- **避坑提示**：务必校验地域一致性；人像类模型缺失检测坐标将导致失败；所有媒体资源必须为公网可访问 URL（本地文件需先调用上传接口获取临时链接）。

### ✅ 3D生成 —— 适合「空间数字化、工业级交付、跨平台复用」
- **推荐场景**：  
  - 快速构建轻量 3D 资产（如 AR 商品预览）→ **Tripo-P1.0**（2 万面，秒级生成）；  
  - 高精度建模需求（游戏角色、工业零件）→ **Tripo-H3.1**（200 万面，支持 `geometry_quality: "ultra"`）；  
  - 从产品实物照片生成 3D 模型 → 使用 **四视图输入**（前/左/后/右），注意视角一致性；  
  - 需嵌入 Web 应用 → 直接加载 GLB 文件（兼容 Three.js / Babylon.js）。
- **避坑提示**：仅限华北2地域；三类输入（prompt/image/images）**严格互斥**，同时传入将直接报错；若需无贴图模型，必须同时设置 `texture=false` 和 `pbr=false`。

---

## 开发者技术选型参考

| 选型目标 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| **追求最低延迟 & 高并发** | 图像生成（Z-Image） | P95 延迟 <800ms，同步响应，无轮询开销，适合实时交互场景 |
| **需要多模态理解与复杂编辑** | 图像生成（千问 Qwen2-VL 图像版） | 支持图文多轮对话驱动生成/编辑，语义理解深度优于纯扩散模型 |
| **构建数字人应用闭环** | 视频生成（EMO/LivePortrait + 检测 API） | 提供完整人像驱动管线，含人脸检测、关键点提取、驱动合成三阶段 |
| **生成可商用 3D 资产** | 3D生成（Tripo-H3.1 + `pbr=true`） | 输出带 PBR 材质的 GLB，符合 Unity/Unreal/Three.js 生产标准，免二次烘焙 |
| **低成本试错 & 快速验证** | 图像生成（万相 WanX-v1） | 免费额度充足，API 简单，调试成本低，适合 MVP 阶段验证提示词效果 |
| **跨模态工作流编排** | 组合使用：图像 → 视频 → 3D | 示例：用万相生成产品图 → 输入 HappyHorse 生成展示视频 → 用 Tripo 生成 3D 模型用于 AR；注意各环节地域与凭证隔离 |

> **重要提醒**：所有生成类服务均受内容安全策略约束，禁止生成暴力、色情、政治敏感或侵权内容。违规请求将被拦截并记录审计日志。建议在生产环境启用 `prompt` 安全过滤中间件，并对用户输入做预审。

---  
*最后更新：2024年6月*  
*文档版本：v2.3（基于百炼平台 API v1.2.0）*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


