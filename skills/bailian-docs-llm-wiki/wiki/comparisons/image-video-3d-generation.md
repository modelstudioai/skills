# 图像、视频与 3D 内容生成能力对比

本文旨在为开发者提供百炼平台多模态内容生成能力的系统性技术选型参考。随着 AIGC 应用场景从静态图像向动态视频、可交互 3D 内容快速演进，理解各模态在输入输出、模型能力、调用范式、资源约束及成本结构上的差异，对架构设计、性能优化与长期维护至关重要。本对比聚焦图像生成（Image Generation）、视频生成（Video Generation）与 3D 内容生成（3D Generation）三大核心能力，基于当前平台（2024–2025 年度主流版本）的官方文档与 API 规范，提炼关键维度进行横向分析。

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D 内容生成（3D Generation） |
|------|------------------------------|------------------------------|------------------------------|
| **核心输入格式** | 文本（prompt）、单图 URL / Base64、掩码（mask）、多图（分镜/涂鸦）、人脸训练图（FaceChain） | 文本（prompt）、单图/首帧 URL、首尾帧 URL、参考图数组、参考视频 URL、音频（部分模型） | 文本（prompt）、单图 URL、四视角图数组（前/左/后/右）、GLB/GLTF/FBX/OBJ/STL 模型文件 URL（后处理） |
| **核心输出格式** | PNG（主流）、JPEG（部分）、WEBP（可选）；URL 直链（同步）或异步返回；支持批量（`n` 或 `series_amount`） | MP4（H.264/AAC 主流）、MOV（部分）；URL 直链（24 小时有效）；不支持帧序列直接下载 | GLB（默认）、GLTF、FBX、OBJ、STL、SPLAT（`.splat`）；URL 直链（24 小时有效）；支持贴图包（ZIP）、动画文件（FBX）等复合产物 |
| **主力支持模型/系列** | Qwen-Image（3.0-pro 等）、WanX（2.6/2.7-image-pro）、Kling/Vidu（北京专属）、Z-Image、FaceChain | HappyHorse（全链路）、WanX（3.0/2.7-video）、Kling（v4/v4-omni）、PixVerse、Vidu、MiniMax、VideoRetalk | Tripo-H3.1（高精网格）、Tripo-P1.0（快速专业）、Tripo-ImageToSplat（Gaussian Splat）、Tripo-Segmentation / Retopology / Texture / AutoRig / AnimationRetarget |
| **API 端点路径** | `POST /api/v1/services/aigc/multimodal-generation/generation`（同步/异步混用）<br>部分创意工具使用独立路径（如 `/portrait-style-redraw`） | `POST /api/v1/services/aigc/video-generation/video-synthesis`（主路径）<br>数字人/声动人像等使用 `/image2video/...` 等非标路径 | `POST /api/v1/services/aigc/video-generation/3d-generation`（唯一路径，注意命名含 `video-generation` 仅为历史兼容） |
| **调用模式** | **混合模式**：<br>• 同步：Z-Image、Qwen-Image Pro、Wan2.7-image（秒级响应）<br>• 异步：Kling/Vidu、万相编辑类、FaceChain、多数创意工具（1–2 分钟） | **强制异步**：<br>所有模型均需 `X-DashScope-Async: enable`，两步流程（提交任务 → 轮询 `task_id`） | **强制异步**：<br>全部接口必须 `X-DashScope-Async: enable`，两步流程（提交任务 → 轮询 `task_id`），无同步选项 |
| **地域支持** | 华北2（北京）、新加坡、美国（弗吉尼亚）——**三地模型与 Key 完全隔离** | 华北2（北京）、新加坡、美国（弗吉尼亚）——**三地模型与 Key 完全隔离** | **仅华北2（北京）** —— 全量接口、Key、Endpoint 均绑定该地域，跨地域调用必然失败 |
| **计费方式** | • 按次计费（主流模型）<br>• 部分创意工具（如虚拟模特、擦除补全）仅限 500 张免费额度，**不可续费**<br>• 分辨率/尺寸影响单价（如 Wan2.7 支持 4K 溢价） | • 按任务计费（基础）<br>• 部分模型按秒后付费（如 VideoRetalk）<br>• 分辨率（720p/1080p/4k）、时长（3–30 秒）、特效模板影响计费 | • 按任务计费（基础）<br>• 高精度参数显著溢价（如 `texture_quality: extreme`、`quad: true`、`model_version: v2.0`）<br>• 动画重定向按 `animations` 数组长度计费（最多 5 个）<br>• 格式转换/贴图等后处理独立计费 |
| **典型场景** | • 创意海报、电商主图、UI 设计稿<br>• 社媒配图、AIGC 艺术创作<br>• 人像写真、商品试穿（鞋靴）、局部编辑<br>• 中英文字精准渲染（Kling/Vidu） | • 短视频广告、产品演示动画<br>• 教育/培训微课、AI 数字人播报<br>• 口型同步（VideoRetalk）、动作迁移<br>• 分镜脚本可视化（HappyHorse/Kling） | • 游戏资产快速建模（文/图生 3D）<br>• AR/VR 场景实时渲染（Gaussian Splat）<br>• 工业设计原型验证、3D 打印准备（重拓扑+贴图）<br>• 角色动画管线（绑骨+重定向） |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「快速迭代、高精度控制、轻量交付」场景  
- **推荐选用**：当需求聚焦于静态视觉表达，且对生成速度、分辨率控制、文本/图像细节还原（尤其中英文）有明确要求时。例如：  
  - 电商运营需每小时生成上百张不同风格的商品主图 → 选用 `Z-Image`（低延迟）或 `Wan2.7-image-pro`（4K 输出）；  
  - UI 团队需像素级还原 Figma 设计稿 → 选用 `Kling/Vidu`（北京地域，支持 UI 图表精准重建）；  
  - 个性化营销需生成千人千面人像海报 → 选用 `FaceChain`（2 图训练专属模型）+ `Qwen-Image`（风格重绘）。  
- **规避风险**：避免在新项目中使用已归档的 `wanx-v1`（文生图 V1）或跨地域混用 Key/Endpoint；慎用无付费通道的创意工具（如 `wanx-virtualmodel`），应优先评估 `Qwen-Image` 编辑替代方案。

### ✅ 视频生成 —— 适合「动态叙事、跨模态联动、中长周期生产」场景  
- **推荐选用**：当内容需时间维度表达（运动、变化、节奏），且接受 1–3 分钟生成延迟时。例如：  
  - 教育机构制作知识短视频 → 选用 `HappyHorse`（物理运动建模稳定）或 `WanX 3.0`（全链路统一协议）；  
  - 品牌方发布新品宣传短片 → 选用 `Kling v4-omni`（支持 30 秒长视频 + 主体库复用）；  
  - 客服系统集成数字人播报 → 选用 `VideoRetalk`（口型同步 + 音色库驱动）。  
- **规避风险**：务必校验 `input` 结构与模型能力严格匹配（如 `first_frame_url` 与 `last_frame_url` 仅 WanX 2.7+/Vidu/PixVerse 支持）；避免误用旧版 `/image2video/` 路径调用主流视频模型。

### ✅ 3D 内容生成 —— 适合「三维空间构建、工业级精度、管线化协作」场景  
- **推荐选用**：当目标为可导入引擎（Unity/Unreal）、可打印、可绑定动画的三维资产，且团队具备基础 3D 工作流认知时。例如：  
  - 游戏工作室快速生成 NPC 道具原型 → `Tripo-P1.0`（2 万面，快）→ `Tripo-Retopology`（重拓扑）→ `Tripo-Texture`（贴图）；  
  - AR 应用需真实感实时渲染 → `Tripo-ImageToSplat`（单图生成 `.splat`）→ 直接加载至 Three.js；  
  - 动画工作室构建角色管线 → `Tripo-H3.1`（高精模型）→ `Tripo-AutoRig`（`spec: tripo`）→ `Tripo-AnimationRetarget`（预设动作库）。  
- **规避风险**：**必须锁定华北2（北京）地域**；严格遵循 `spec` 约束（`mixamo` 绑骨 ≠ `tripo` 绑骨，后者才支持重定向）；后处理输入需确保前序任务成功且格式兼容（如 `Tripo-Texture` 要求 `texture_prompt` 在非 Tripo 原生生成时必填）。

## 技术选型决策指南（面向开发者）

| 决策问题 | 推荐行动 |
|----------|----------|
| **“我的应用需要最快响应”** | 优先评估图像生成中的同步能力：`Z-Image`（毫秒级）、`Qwen-Image-3.0-pro`（秒级）。视频与 3D 均为强制异步，无法满足亚秒级响应。 |
| **“我需要跨地域部署服务”** | 图像/视频生成：可分别在华北2、新加坡、弗吉尼亚开通对应 Key 与 Endpoint，但需独立管理模型列表与配额；3D 生成：**不可跨地域**，必须将业务中心收敛至北京。 |
| **“我已有大量图片/视频/3D 模型需批量处理”** | 图像：利用 `n` 参数批量生成（同步）或 `series_amount`（Kling 分镜）；视频/3D：需自行实现并发任务提交 + 轮询调度器（注意 `task_id` 24 小时有效期）；3D 后处理强烈推荐使用 `original_model_task_id` 链式调用，避免重复上传大文件。 |
| **“我关注长期成本与可维护性”** | 避免依赖无付费通道的免费额度模型（如万相创意工具）；优先选用 SDK 支持完善的模型（Qwen/WanX/Z-Image 图像；HappyHorse/WanX 视频）；3D 全量 HTTP API，需封装健壮的轮询与错误重试逻辑。 |
| **“我需要与现有工作流集成（Figma/Blender/Unreal）”** | 图像：输出 PNG/JPEG 可直连设计工具；视频：MP4 通用性强；3D：GLB/GLTF 为 Web 标准，FBX/OBJ 适配 DCC 工具，需确认 `Tripo-ConvertFormat` 是否启用高级参数（影响计费）。 |

> **最后提醒**：所有能力均要求 **API Key、Endpoint 地域、模型部署地域三者严格一致**。百炼平台持续演进，建议通过控制台「模型市场」实时查看各地域可用模型，并订阅 [DashScope SDK 更新日志](https://help.aliyun.com/zh/dashscope/developer-reference/sdk-release-notes) 获取兼容性变更。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


