# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文对**图像生成（Image Generation）、视频生成（Video Generation）和3D生成（3D Generation）**三大核心能力进行系统性横向对比。对比聚焦于实际工程落地的关键维度——包括输入/输出规范、模型生态、调用方式、计费逻辑及典型适用场景，旨在为技术选型提供清晰、可操作的决策依据。

---

## 关键能力维度对比

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | • 文本（[prompt](../guides/prompt.md)，≤2500–5000字符）<br>• 图像 URL（PNG/JPG/WEBP/BMP，≤10 MB，分辨率 300–8192px）<br>• 多图参考（最多14张，如Vidu）<br>• Mask（局部重绘/擦除补全） | • 文本（[prompt](../guides/prompt.md)，≤5000–7000字符）<br>• 首帧/首尾帧图像 URL（JPG/PNG/WEBP，400–7000px）<br>• 参考视频 URL（MP4/AVI/MOV，≤30秒，≤100MB）<br>• 参考图像数组（多图驱动）<br>• 音频（WAV/MP3，用于口型替换） | • 文本（[prompt](../guides/prompt.md)，≤1024字符）<br>• 单图 URL（JPEG/PNG，≤20MB）<br>• 四视图数组（前/左/后/右，固定顺序）<br>• 前序任务 ID（`original_model_task_id`）或模型文件 URL（GLB/FBX/OBJ，≤150MB） |
| **输出格式** | • PNG/JPEG（主流）<br>• WEBP（部分模型支持）<br>• 多张并行输出（`n=1–9`） | • MP4（H.264 编码，标准交付格式）<br>• 无原始帧序列或中间缓存（需自行解帧） | • GLB（默认，含几何+基础贴图）<br>• FBX（启用 `quad=true` 或格式转换时）<br>• `.splat`（Gaussian Splatting 专用）<br>• PBR材质包（ZIP，含BaseColor/Normal/Roughness等贴图） |
| **支持模型（代表性）** | • `qwen-image-3.0-pro`（T2I+I2I全能）<br>• `wan2.7-image-pro`（4K/组图/多图编辑）<br>• `kling/kling-v3-omni-image-generation`（分镜/漫剧）<br>• `vidu/viduq2-pro_reference2image`（UI/工业级稳定）<br>• `facechain-finetune`（LoRA写真） | • `wanx3.0-video-generation`（All-in-One统一接口）<br>• `pixverse/pixverse-v6-t2v`（强动态表现）<br>• `vidu/viduq3-drama_reference2video`（角色一致性）<br>• `kling/kling-v3-omni-video-generation`（五合一可控生成）<br>• `MiniMax/MiniMax-H3`（多模态参考） | • `Tripo/Tripo-H3.1`（高精度网格，≤200万面）<br>• `Tripo/Tripo-P1.0`（专业级轻量网格，≤2万面）<br>• `Tripo/Tripo-ImageToSplat`（单图→Gaussian Splat）<br>• `Tripo/Tripo-AutoRig` / `Tripo/Tripo-RigCheck`（动画绑定） |
| **API 端点（协议）** | • 同步为主：`POST /api/v1/services/aigc/image-generation/generation`<br>• 异步为辅（Kling/Vidu等）：`POST /api/v1/services/aigc/image-generation/generation?async=true` → 轮询 `GET /api/v1/tasks/{task_id}` | • **强制异步**：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis`<br>→ 轮询 `GET /api/v1/tasks/{task_id}`<br>• 请求头必须含 `X-DashScope-Async: enable` | • **强制异步**：<br>`POST /api/v1/services/aigc/video-generation/3d-generation`<br>→ 轮询 `GET /api/v1/tasks/{task_id}`<br>• 请求头必须含 `X-DashScope-Async: enable` |
| **地域约束** | • 模型、API Key、Endpoint 必须同地域（华北2/新加坡/美东）<br>• 推荐使用业务空间专属域名（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`） | • 同图像生成：严格地域一致<br>• **禁用公共域名 `dashscope.aliyuncs.com`**（性能与稳定性无保障） | • **仅支持华北2（北京）地域**<br>• API Key、Endpoint、WorkspaceId 必须全部为华北2配置<br>• 其他地域调用必然失败 |
| **计费方式** | • 按**生成图片张数**计费（如1张 = 1次调用）<br>• 部分模型按分辨率分级（如 `2K` vs `4K`）<br>• 免费额度模型（如 `wanx-x-painting`）额度用尽即停服，不支持付费扩容 | • 按**视频秒数 × 分辨率权重**计费（如 `720P×10s` = 1单位，`4K×10s` ≈ 4–8单位）<br>• 部分模型按任务次数计费（如 VideoRetalk）<br>• 无通用免费额度，需开通服务后按用量结算 | • 按**任务类型 + 输出质量**计费：<br> – 基础生成（`Tripo-H3.1`）：按面数等级（`standard`/`ultra`）计费<br> – 后处理（贴图/重拓扑）：按输入模型复杂度与参数（`texture_quality`, `face_limit`）计费<br> – 动画绑定：按骨骼类型与动作复杂度计费<br>• 无免费额度，全部按量付费 |
| **典型场景** | • 营销海报/电商主图批量生成<br>• UI设计稿风格迁移与迭代<br>• 虚拟模特/鞋靴试穿<br>• 社媒配图、AIGC插画创作<br>• 局部编辑（擦除/重绘/扩图） | • 短视频广告创意脚本可视化（文→视频）<br>• 产品演示动画（图→视频）<br>• 漫剧分镜动态化（多图→视频）<br>• 数字人口型同步（音频+首帧→说话视频）<br>• 视频风格重绘（老片→赛博朋克风） | • 游戏资产快速原型（文/图→可导入Unity/Unreal的GLB）<br>• 电商3D商品展示（单图→带PBR贴图的FBX）<br>• AR/VR内容生产（Gaussian Splat用于实时渲染）<br>• 工业设计验证（四视图→高精度网格+重拓扑）<br>• 3D角色动画管线（自动绑骨+动作重定向） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「静态视觉内容」高频、轻量、多样化需求  
- **推荐场景**：营销素材批量产出、UI/UX设计辅助、社交媒体配图、个性化头像/写真、电商详情页优化。  
- **慎用场景**：需时间维度表达（如动作、流程）、强物理真实感（如流体/布料模拟）、跨视角一致性要求极高（如360°产品展示）。  
- **选型提示**：优先选用 `qwen-image-3.0-pro`（平衡效果与速度）或 `wan2.7-image-pro`（高分辨率/组图需求）；避免依赖已标注“仅限免费体验”的模型（如 `shoemodel-v1`），因其无付费通道且额度耗尽即不可用。

### ✅ 视频生成 —— 适合「短时长动态表达」与「多模态驱动」内容生产  
- **推荐场景**：15–30秒短视频创意生成、AI广告脚本可视化、数字人播报、教育动画片段、游戏过场预演。  
- **慎用场景**：超长视频（>30秒）、电影级叙事（需多镜头剪辑逻辑）、高精度物理仿真（如爆炸/烟雾）、无参考的自由运镜控制。  
- **选型提示**：统一采用万相3.0（`wanx3.0-video-generation`）作为首选入口；若强调角色一致性与情绪表达，选用 `vidu/viduq3-drama_*`；若需口型精准同步，务必搭配 `VideoRetalk` 专用服务。

### ✅ 3D生成 —— 适合「三维资产构建」与「专业工作流集成」需求  
- **推荐场景**：游戏/AR/VR内容快速建模、电商3D商品库建设、工业设计概念验证、AIGC驱动的3D动画制作。  
- **慎用场景**：纯2D内容需求、实时交互式建模（非批处理）、超高精度CAD级建模（如公差±0.01mm）、无纹理/无光照的线框级输出。  
- **选型提示**：**必须部署于华北2（北京）环境**；文生3D首选 `Tripo-H3.1`（兼顾精度与可用性），图生3D优先 `Tripo-P1.0`（轻量高效）；所有后处理任务应通过 `original_model_task_id` 构建任务链，避免重复上传大模型文件。

---

## 面向开发者的选型决策指南

| 决策问题 | 推荐答案 | 技术依据 |
|----------|----------|----------|
| **我的应用需要快速生成100张不同风格的海报图，QPS要求高** | ✅ 选用 `qwen-image-3.0-pro` 或 `z-image-turbo`，走**同步调用** | 同步响应延迟低（通常 <3s），支持 `n=4` 批量生成，`z-image-turbo` 更适合中英文字渲染场景 |
| **我要把一段产品文案转成30秒广告视频，且需匹配品牌VI色调** | ✅ 选用 `vidu/viduq3-ad_text2video` + `vidu/viduq3-ad_style2video` 两阶段调用 | Vidu系列专为广告优化，支持色彩锚定与品牌元素注入，且 `ad` 子模型对商业语义理解更强 |
| **我有一张手机拍摄的产品照片，想生成可360°查看的3D模型用于网页展示** | ✅ 选用 `Tripo/Tripo-P1.0`（单图生3D）→ `Tripo/Tripo-Texture`（PBR贴图）→ `Tripo/Tripo-ConvertFormat`（转GLB） | `P1.0` 对单图鲁棒性好，`Texture` 支持 `pbr=true` 输出标准材质，GLB为WebGL/Three.js原生支持格式 |
| **我的服务部署在新加坡，能否调用Vidu视频生成？** | ❌ 不可以。必须将服务、API Key、Endpoint全部切换至**新加坡地域**，并使用对应 WorkspaceId 的专属域名 | 所有文档明确强调“模型、Key、Endpoint三者地域必须一致”，跨域调用返回 `401` 或 `400` 错误 |
| **我想做AI虚拟主播，需口型+表情+动作一体化生成** | ✅ 组合方案：`pixverse/pixverse-c1-t2v`（文生基础视频） + `VideoRetalk`（音频驱动口型） + `Tripo/Tripo-AutoRig`（绑定骨骼后接入动作库） | PixVerse擅长动态表现，VideoRetalk专注唇形同步，Tripo提供专业级绑定能力，三者能力互补且均支持异步任务链 |

> **重要提醒**：  
> - 所有异步任务（视频/3D/部分图像模型）的 `task_id` 有效期均为 **24小时**，请务必在有效期内完成轮询；  
> - **业务空间专属域名是性能与稳定性的底线要求**，切勿在生产环境使用 `dashscope.aliyuncs.com`；  
> - 免费额度模型（如 `wanx-x-painting`、`image-erase-completion`）不具备长期服务保障，请在架构设计初期规避依赖。  

---  
*本文档基于百炼平台2024年Q3最新API文档整理

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


