# 多模态生成 API 对比：图像、视频与 3D 生成

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术能力边界与工程适配要点，本文系统对比图像生成、视频生成与 3D 生成三类核心 API 的关键特性。对比聚焦于**实际开发落地中高频关注的技术维度**，包括调用模式、输入/输出约束、模型生态、地域与协议一致性要求、计费逻辑及典型适用场景，旨在为技术选型提供可操作的决策依据。

---

## 关键维度对比表

| 维度 | 图像生成（`/image-generation`） | 视频生成（`/video-generation`） | 3D 生成（`/3d-generation`） |
|------|-------------------------------|------------------------------|---------------------------|
| **核心调用模式** | 同步为主（`qwen-image-3.0-pro`、`wan2.7-image-pro` 等），异步为辅（`kling`、`vidu`、创意工具类） | **强制异步**（所有模型均需 `X-DashScope-Async: enable`，两步调用：创建任务 + 轮询） | **强制异步**（统一 `/3d-generation` 接口，必须轮询 `task_id`） |
| **输入格式支持** | 文本（prompt）、单图/多图（URL 或 Base64）、涂鸦草图；支持透明通道输入（PNG）；万相2.5支持最多14张参考图 | 文本、首帧图、首尾帧图、参考视频/图片混合数组、音频（数字人场景）；图片支持 JPG/JPEG/PNG/BMP/WEBP；视频支持 MP4/AVI/MOV（≤30s） | 文本（prompt）、单图、四视角图组（前/左/后/右）、GLB/GLTF/FBX/OBJ/STL 模型；仅支持 PNG/JPEG/WebP（≤20MB） |
| **输出格式** | JPG、PNG（部分模型如 `qwen-image-3.0-pro` 默认带 Alpha 通道）；分辨率支持 1K/2K/4K 或像素值（如 `1024×1024`） | MP4（H.264 编码），分辨率支持 720P/1080P/4K，宽高比支持 16:9 / 9:16 / 1:1；帧率 15–25 fps | GLB、FBX、OBJ、STL、`.splat`（Gaussian Splatting）；支持面数控制（`face_limit`）、PBR 贴图、重拓扑四边面（`quad`）等高级导出选项 |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`、`vidu/viduq2-pro_reference2image`、`z-image-turbo`、`facechain-finetune` | `wan3.0`、`kling/kling-v3-omni-video-generation`、`vidu/viduq3-ad_reference2video`、`pixverse/pixverse-v6-r2v-omni`、`wan2.2-s2v`（数字人）、`videoretalk`（口型驱动） | `Tripo/Tripo-H3.1`（高精度网格）、`Tripo/Tripo-P1.0`（轻量级）、`Tripo/Tripo-ImageToSplat`（Gaussian）、`Tripo/Tripo-AutoRig`（自动绑骨） |
| **API 端点（推荐）** | `/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>`/image-synthesis` 或 `/generation`（异步） | `/api/v1/services/aigc/video-generation/video-synthesis`（`wan3.0`/`kling-v3+` 新协议）<br>旧版路径仍存在（如 `/api/v1/services/aigc/image2video/video-synthesis`） | `/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation` 是历史命名，实际为 3D 专用） |
| **地域限制** | **强地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等独立部署；API Key、Endpoint、WorkspaceId 必须同地域 | **强地域隔离**：所有模型均要求严格同地域；`wan2.2-s2v`、`videoretalk` 等仅支持华北2（北京） | **仅限华北2（北京）**：全链路（开通、调用、结果存储）均绑定北京地域，无其他地域部署 |
| **计费方式** | 按次计费（如 `qwen-image-3.0-pro` 4K 输出 0.3 元/张）；部分创意工具（`virtualmodel-v2` 等）**仅限免费体验，无付费通道** | 按秒计费（如 `wan2.2-s2v` 720P 0.9 元/秒，`videoretalk` 0.08 元/秒）；免费额度明确（如 `videoretalk` 1800 秒） | 按积分计费：基础生成消耗固定积分，启用 `texture_quality=extreme`、`geometry_quality=ultra`、`quad=true` 等高级参数将显著增加积分消耗；无按次/按时长直接计价 |
| **典型响应耗时** | 同步：3–15 秒（`z-image-turbo` <3s，`qwen-image-3.0-pro` 4K ≈12s）<br>异步：10–60 秒（任务排队+执行） | 异步：1–5 分钟（文生视频平均 2.5 分钟；图生视频/数字人约 1–3 分钟） | 异步：2–10 分钟（文生/图生基础网格约 3–5 分钟；Gaussian Splatting、智能分割、动画重定向可达 8–10 分钟） |
| **OpenAI 兼容性** | ✅ 支持 OpenAI 兼容模式（`/images/generations`），通过 `image` 字段有无自动区分 T2I/I2I | ❌ **不支持** OpenAI 兼容协议；必须使用 DashScope 原生异步接口 | ❌ **不支持** OpenAI 兼容协议；仅 DashScope 原生接口 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合**高吞吐、低延迟、多样化编辑需求**  
- **快速原型与 A/B 测试**：使用 `z-image-turbo` 或 `qwen-image-3.0` 进行文案配图、Banner 初稿生成（毫秒级响应）。  
- **工业级图像生产**：选用 `wan2.7-image-pro`（4K 输出+推理可视化）或 `vidu/viduq2-pro_reference2image`（复杂逻辑稳定输出），用于电商主图、广告素材、设计资产交付。  
- **个性化内容创作**：`facechain-finetune`（2照训练专属形象）+ `wanx-style-repaint-v1`（人像风格迁移）组合，支撑虚拟偶像、定制化营销内容。  
- ⚠️ **避坑提示**：避免将 `virtualmodel-v2`、`shoemodel-v1` 等“仅限免费体验”模型纳入生产依赖链；其无付费通道且额度用尽即不可用。

### ✅ 视频生成 —— 适合**中等时延容忍、强语义/动作表达需求**  
- **营销短视频自动化**：`vidu/viduq3-ad_reference2video`（商品图直出广告视频）或 `wan3.0`（文生+首帧增强），适用于电商详情页、社媒种草视频批量生成。  
- **数字人内容生产**：`wan2.2-s2v`（单图+音频生成说话视频）搭配 `videoretalk`（已有视频口型替换），构建客服、培训、新闻播报等数字人应用。  
- **创意视频增强**：`video-style-transform`（8种艺术风格）+ `pixverse/pixverse-upscale`（4K超分），用于短视频二次创作与画质升级。  
- ⚠️ **避坑提示**：`wan2.1–2.6` 旧版模型路径与参数范式与新版不兼容，务必核对文档路径；跨地域调用 `wan2.2-s2v` 将直接失败。

### ✅ 3D 生成 —— 适合**高精度资产交付、游戏/AR/仿真等专业工作流集成**  
- **3D 内容快速建模**：`Tripo/Tripo-H3.1`（文生/图生高面数网格）用于游戏道具、工业零件概念建模；`Tripo/Tripo-P1.0` 用于轻量预览与快速迭代。  
- **实时渲染与重建**：`Tripo/Tripo-ImageToSplat` 直出 `.splat` 文件，无缝接入 Unreal/Unity 实时引擎，适用于 AR 场景、数字孪生快速建模。  
- **3D 生产管线自动化**：组合调用 `Tripo-SmartSegmentation`（智能部件分割）→ `Tripo-Retopology`（四边面重拓扑）→ `Tripo-AutoRig`（自动绑骨）→ `Tripo-AnimationRetarget`（动作迁移），构建角色动画工业化流水线。  
- ⚠️ **避坑提示**：所有 3D 接口仅在北京地域可用；`AutoRig` 不支持 STL 输入；`generate_parts` 与贴图/材质参数互斥，配置错误将导致静默降级。

---

## 面向开发者的选型参考指南

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| **需要 1 秒内返回结果，且只需静态图** | `z-image-turbo` 或 `qwen-image-3.0`（同步调用） | 轻量模型响应最快，OpenAI 兼容零改造迁移 | `z-image-turbo` 不支持多图参考；`qwen-image-3.0` 无 4K 输出 |
| **需生成带透明通道的 PNG 用于 UI 组件** | `qwen-image-3.0-pro` | 默认输出含 Alpha 通道，支持最多 10 张参考图引导精细编辑 | 需显式指定 `size="1024*1024"` 等像素值，不支持 `"4K"` 字符串 |
| **要批量生成 30 秒以内营销短视频** | `wan3.0` 或 `kling/kling-v3-omni-video-generation` | 全能型模型，统一接口，支持文/图/参考生视频，16:9/9:16 自适应 | 必须设置 `X-DashScope-Async: enable`；轮询间隔建议 ≥15 秒 |
| **已有真人视频，需替换口型并匹配新语音** | `videoretalk` | 专精口型驱动，北京地域独占，计费最经济（0.08 元/秒） | 仅支持华北2（北京）；音频需人声清晰、无背景噪音；并发任务上限为 1 |
| **从产品照片生成可编辑的 3D 模型用于电商展示** | `Tripo/Tripo-H3.1` → `Tripo-Texture` → `Tripo-ConvertFormat` | 高精度网格 + PBR 贴图 + FBX 导出，满足 WebGL/Three.js 直接加载 | 四视角图组非必需（单图即可），但单图质量需高；`texture_quality=detailed` 可平衡效果与耗时 |
| **需将 3D 模型快速绑定骨骼并驱动行走动画** | `Tripo-RigCheck` → `Tripo-AutoRig`（`rig_type=biped`）→ `Tripo-AnimationRetarget`（`preset:biped:walk`） | 全链路自动化，支持 Mixamo 骨骼标准；动画重定向精准匹配体型 | `AutoRig` 输出模型不可直接用于 `AnimationRetarget`，需先通过 `RigCheck` 校验 |

> **终极建议**：  
> - **优先使用业务空间专属域名**（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非通用 `dashscope.aliyuncs.com`，可显著提升稳定性与成功率；  
> - **所有多模态 API 均强制要求地域一致**——这是百炼平台最常被忽略、也最易引发 401/404/UNKNOWN 错误的根本原因，请在初始化 SDK 或构造请求前严格校验；  
> - **[异步任务](../concepts/asynchronous-task.md)务必妥善管理 `task_id` 生命周期**：有效期统一为 24 小时，建议服务端持久化存储，并设置失败重试与超时熔断机制。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


