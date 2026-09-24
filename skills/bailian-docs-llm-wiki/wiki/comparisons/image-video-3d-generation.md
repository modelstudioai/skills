# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成、视频生成与3D生成三大核心能力模块。对比聚焦实际工程落地的关键维度——包括输入/输出规范、模型生态、调用范式、资源约束及计费逻辑等，旨在为产品设计、技术选型与架构决策提供客观、可执行的参考依据。

---

## 关键能力维度对比

| 维度 | 图像生成（`/v1/images/generations`） | 视频生成（`/api/v1/services/aigc/video-generation/video-synthesis` 等） | 3D生成（`/api/v1/services/aigc/video-generation/3d-generation`） |
|------|-------------------------------------|------------------------------------------------------------------------|---------------------------------------------------------------|
| **输入格式** | 文本（`prompt`）、可选图像（`image_url` + `mask_url`）、结构化编辑指令（草图/掩码） | 文本（`prompt`/`negative_prompt`）、图像（`img_url`）、视频（`video_url`）、音频（`audio_url`）、数字人驱动参数（`face_bbox`等） | 文本（`input.prompt`）、单张图像（`input.image`）、四视角图像数组（`input.images`，前/左/后/右） |
| **输出格式** | PNG/JPEG 静态图直链（`data[0].url`），有效期 1 小时；含 `seed`、`cost_tokens` 等元信息 | MP4 视频直链（`output.video_url`），有效期 2 小时；部分模型返回预览图、关键帧或结构化元数据（如 `output.face_info`） | GLB 格式 3D 模型（`pbr_model_url` / `base_model_url`）、渲染预览图（`rendered_image_url`），所有 URL 有效期 2 小时 |
| **支持模型（主力）** | `qwen-vl-plus`（多模态理解）、`wanx-2.1`（艺术风格）、`Z-Image`（低延迟）、`kling-1.0`（复杂构图）、`Vidu`（帧级输出）、`Creative Tools`（inpainting/outpainting） | `HappyHorse`（物理真实）、`WanX` 全系列（2.7/3.0/2.2-s2v）、`PixVerse`（创意质量）、`AnimateAnyone`/`EMO`/`LivePortrait`（人像驱动） | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 端点** | 统一同步端点：<br>`POST https://dashscope.aliyuncs.com/api/v1/images/generations` | 多端点异步模式：<br>• `/api/v1/services/aigc/video-generation/video-synthesis`（文/图/参考生视频）<br>• `/api/v1/services/aigc/image2video/`（数字人/动作驱动） | 单一异步端点（仅限华北2北京）：<br>`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` |
| **调用模式** | **同步响应**（典型延迟：800ms–5s），失败/成功即时返回 | **强制异步**（创建任务 → 轮询 `task_id`），任务状态有效期 24 小时，典型耗时 1–10 分钟 | **强制异步**（创建任务 → 轮询 `task_id`），任务状态有效期 24 小时，典型耗时 2–8 分钟 |
| **地域约束** | 无显式地域绑定（API Key 通用） | **强地域绑定**：模型、Endpoint、API Key 必须同属一个地域（如华北2、新加坡） | **强地域绑定**：仅支持华北2（北京），API Key、Endpoint、Workspace ID 均需匹配 |
| **计费方式** | 按 **token 消耗量** 计费（`cost_tokens` 返回值）；免费额度仅覆盖 `qwen-vl-plus` 和 `wanx-2.1` 基础调用 | 按 **任务成功次数** + **分辨率/时长/质量参数** 组合计费（如 `resolution=4K`、`video_fps=30` 加价）；部分模型（如数字人）按分钟计费 | 按 **任务成功次数** 计费；`geometry_quality=ultra` 或 `texture_quality=detailed` 产生额外费用 |
| **典型场景** | UI 设计稿生成、营销海报制作、AIGC 插画、局部重绘修图、风格迁移、视频前导图生成 | 短视频创作、数字人播报、广告片生成、口型同步、动作模仿、视频特效增强、教育动画制作 | 电商商品建模、游戏资产生成、AR/VR 内容开发、工业设计原型、3D 打印准备、虚拟展厅搭建 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「快速迭代、轻量交互、高并发」场景  
- **推荐使用**：需要毫秒级响应的前端交互（如设计工具实时预览）、批量生成静态素材（Banner/图标/插画）、图文混合工作流中的中间产物生成（如 Vidu 的帧级图）。  
- **慎用**：对运动连续性、时间一致性有要求的任务（如角色动作序列）；需精确三维几何结构的任务（如机械零件建模）。  
- **提示**：Z-Image 是唯一支持 sub-800ms 延迟的模型，适用于对首屏体验敏感的 SaaS 应用；创意工具类操作（inpainting）需严格校验 mask 格式与分辨率。

### ✅ 视频生成 —— 适合「时间维度表达、人物驱动、跨模态协同」场景  
- **推荐使用**：企业数字人客服/讲师、短视频平台 AIGC 创作、教育课程动画生成、广告脚本可视化、音视频口型/表情同步。  
- **慎用**：超长视频（>120 秒）、高帧率实时流（>30fps）、无参考源的复杂物理模拟（如流体/布料动力学）；对首帧控制精度要求极高的工业仿真。  
- **提示**：万相3.0 与 HappyHorse 在物理真实性上表现更优；PixVerse 更适合强创意导向的影视级表达；人像驱动类模型（EMO/LivePortrait）必须前置人脸检测，否则易失败。

### ✅ 3D生成 —— 适合「空间结构建模、可交互资产、下游工程集成」场景  
- **推荐使用**：电商商家一键生成商品 3D 展示模型、独立游戏开发者快速构建环境资产、AR 应用中用户上传图片转 3D 模型、工业设计概念验证。  
- **慎用**：需要拓扑优化/可编辑网格（如 Blender 可编辑层级）、高精度 UV 展开、PBR 材质精细调控（当前仅支持开关级控制）、动态骨骼绑定（无 Rigging 输出）。  
- **提示**：多图输入（四视角）显著提升几何精度，但必须严格按顺序传入且补全空位 `{}`；`Tripo-H3.1` 的 `ultra` 模式适用于打印/仿真，但生成耗时增加 40%+；所有下载链接 2 小时过期，务必及时持久化。

---

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|-----------|-----------|-----------|
| **最低延迟 & 高并发** | 图像生成（`Z-Image`） | 同步 API，平均延迟 <800ms，支持 `n=1` 高频调用 | 不支持 `n>1`，不支持 `size="768x1344"`，对 [prompt](../guides/prompt.md) 标点敏感 |
| **最高视觉质量 & 艺术表现力** | 图像生成（`wanx-2.1`）或 视频生成（`PixVerse`） | 万相提供 12 种预设艺术风格；PixVerse 支持超清增强与首尾帧控制 | 万相不支持竖版尺寸；PixVerse 对 [prompt](../guides/prompt.md) 长度容忍度高（≤5000 字符） |
| **强人物驱动 & 实时交互** | 视频生成（`LivePortrait` / `EMO`） | 专为人像优化，支持音频驱动口型、单图生成播报视频，延迟可控（<3s 首帧） | 必须调用 `face-detect` 预检，`face_bbox` 为必填参数；仅支持单人正面照 |
| **三维几何精度 & 工程可用性** | 3D生成（`Tripo/Tripo-H3.1` + `geometry_quality=ultra`） | 输出 ≤200 万面高精度网格，支持 PBR 材质，GLB 格式可直接导入 Unity/Unreal | 仅限华北2北京地域；输入图像需 ≥400px，多图模式必须四视角完整 |
| **低成本快速验证** | 图像生成（`qwen-vl-plus` 或 `wanx-2.1`） | 免费额度覆盖基础调用，文档完善，调试门槛低 | 免费额度不覆盖 `kling`/`Vidu`/创意工具等高级能力 |
| **跨模态流水线整合** | 组合使用：`图像生成 → 视频生成 → 3D生成` | 例如：用 `kling-1.0` 生成高质量首帧 → 输入 `HappyHorse` 图生视频 → 提取关键帧送 `Tripo` 多图建模 | 注意各环节 URL 有效期（1h/2h/2h），需设计临时存储与自动续传机制 |

> **重要提醒**：所有能力均需通过 [DashScope 控制台](https://dashscope.console.aliyun.com) 开通对应服务并获取 API Key；跨地域调用（尤其视频/3D）是高频失败主因，务必在代码中硬编码地域校验逻辑（如 `region == "cn-beijing"`）。

---  
*最后更新：2025年4月*  
*文档版本：BL-GEN-COMPARE-202504-v1.2*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


