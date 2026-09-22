# 图像、视频与 3D 生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文档系统对比图像生成、视频生成与 3D 生成三大核心 AIGC 能力。对比聚焦实际工程落地的关键维度——包括输入/输出规范、模型生态、调用方式、地域约束、计费逻辑及典型适用场景，旨在为技术选型提供客观、可操作的决策依据。所有信息均基于当前（2024年Q2）百炼平台正式发布的 API 文档与运行时行为整理，不包含内测或未公开能力。

## 关键能力维度对比

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
|------|----------|----------|----------|
| **核心输入格式** | 文本（[prompt](../guides/prompt.md)）、单图 URL/Base64、多图（分镜/参考）、局部掩码；支持混合输入（如文+图+掩码） | 文本、单图（首帧）、首尾帧、参考视频、参考图像集、音频（数字人）、动作模板；输入类型高度耦合模型功能 | 文本（[prompt](../guides/prompt.md)）、单张图像、四视角图像（前/左/后/右）；三者严格互斥，不可混用 |
| **核心输出格式** | JPEG/PNG 格式图像（分辨率最高 2048×2048），部分模型支持 WebP；返回直接二进制或 CDN URL | MP4 格式视频（H.264 编码），分辨率通常为 512×512 至 1024×1024，时长 2–8 秒（部分模型支持最长 16 秒）；返回 CDN `video_url` | GLB 格式 3D 模型（含几何体 + PBR 材质贴图），附带 PNG 预览图；返回 `base_model_url`（无材质）和 `pbr_model_url`（含材质），URL 有效期 2 小时 |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo`, `kling/kling-v3-omni-image-generation`, `vidu/vidu-image-pro_reference2image`, `facechain-generation`, `aitryon-plus` 等 | `wan3.0`, `wan2.7`, `happyhorse/t2v`, `pixverse/pixverse-v6-t2v`, `emo-v1`, `liveportrait-v1`, `video-style-transform`, `animate-move` 等 | `Tripo/Tripo-H3.1`（高精度，≤200 万面），`Tripo/Tripo-P1.0`（快速，≤2 万面） |
| **API 端点路径** | 同步：`/api/v1/services/aigc/image-generation`<br>异步：`/api/v1/services/aigc/image-generation/async`（部分模型） | 统一异步：<br>• 通用视频：`/api/v1/services/aigc/video-generation/video-synthesis`<br>• 图生视频/人像驱动等：`/api/v1/services/aigc/image2video/video-synthesis` | 统一异步：<br>`/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation`，但属 3D 专属） |
| **调用模式** | **混合模式**：千问3.0、万相2.7、Z-Image 等支持同步调用（低延迟）；可灵、Vidu、AI试衣、FaceChain 等需异步 | **强制异步**：全部模型必须设置 `X-DashScope-Async: enable`，两步流程（创建任务 → 轮询结果） | **强制异步**：必须设置 `X-DashScope-Async: enable`，两步流程；轮询建议间隔 ≥15 秒 |
| **地域支持范围** | 华北2（北京）、新加坡、美国（弗吉尼亚）三地；模型与 Endpoint 必须同地域（如 `qwen-image-3.0-pro` 在北京可用，在弗吉尼亚暂未开放） | 华北2（北京）、新加坡、东京、弗吉尼亚等多地；`wan3.0`/`happyhorse` 等主力模型覆盖全地域，但旧版（如 `wan2.1–2.6`）仅限北京 | **仅华北2（北京）**：Endpoint、API Key、业务空间 ID 必须全部绑定北京地域；其他地域调用将直接失败 |
| **计费方式** | 按次计费（如 `wan2.7-image-pro`: 0.32 元/张，`qwen-image-3.0-pro`: 0.48 元/张），部分垂直工具（如 `facechain-generation`）含免费额度 | 按任务计费（非按秒）：`wan3.0` 0.98 元/任务，`happyhorse/t2v` 1.28 元/任务，`emo-v1` 0.88 元/任务；同一任务内生成多段视频不额外计费 | 按任务计费：`Tripo-H3.1` 3.98 元/任务，`Tripo-P1.0` 1.98 元/任务；无论文生、单图生或多图生，均按单任务计费 |
| **典型响应耗时** | 同步：3–15 秒（取决于模型与分辨率）<br>异步：任务创建后 10–60 秒内完成（如 `kling` 分镜图约 30 秒） | 异步：20 秒 – 5 分钟（`wan3.0` 文生视频约 45 秒，`emo-v1` 口型驱动约 90 秒，复杂风格重绘可达 3 分钟） | 异步：3–12 分钟（`Tripo-P1.0` 平均 3–5 分钟，`Tripo-H3.1` 平均 8–12 分钟；多图输入比单图慢约 30%） |
| **输入合规性检查** | 图像检测非强制（除 FaceChain 等特定工具外），但推荐预检以提升成功率 | **强依赖预检**：EMO/LivePortrait/AnimateAnyone 等人像模型必须先调用对应 `detect` API（如 `emo-detect-v1`），否则直接拒绝任务 | 无独立检测 API；但多图输入要求至少 2 张有效图，且图像 URL 必须公网可访问；无效输入直接返回 `InvalidParameter` |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高并发、低延迟、强可控」的视觉内容生产
- **推荐场景**：  
  - 电商商品图批量生成与背景替换（`wan2.7-image-pro` + `image-erase-completion`）  
  - UI 设计稿辅助出图与像素级还原（`vidu-image-pro_reference2image`）  
  - 社媒创意海报、营销文案配图（`qwen-image-3.0-pro` 多轮图文协同编辑）  
  - 个性化头像/写真生成（`facechain-generation` + `wanx-style-repaint-v1`）  
- **慎用场景**：  
  - 需要精确时序控制或动态运镜的内容（应选视频生成）  
  - 需导出可交互 3D 模型用于 AR/VR 或游戏引擎（应选 3D 生成）

### ✅ 视频生成 —— 适合「表达动态过程、人物交互、跨模态驱动」的内容创作
- **推荐场景**：  
  - 数字人播报/虚拟主播（`wan3.0-s2v` 或 `emo-v1` + TTS 音频）  
  - 产品功能演示短视频（`happyhorse/image-to-video` 首帧驱动）  
  - 创意广告分镜视频化（`kling/kling-v3-omni-image-generation` 输出多图后接 `happyhorse/t2v`）  
  - 艺术风格迁移（`video-style-transform` 对现有视频做油画/赛博朋克等风格重绘）  
- **慎用场景**：  
  - 仅需静态关键帧（用图像生成更高效、成本更低）  
  - 需要物理准确的三维结构与拓扑（如工业零件建模、建筑 BIM，应选 3D 生成）

### ✅ 3D 生成 —— 适合「构建可复用、可渲染、可集成的三维资产」的专业需求
- **推荐场景**：  
  - 游戏/元宇宙场景道具快速建模（`Tripo-H3.1` + `geometry_quality: "ultra"`）  
  - 电商 360° 商品展示模型（`Tripo-P1.0` 平衡速度与质量）  
  - 建筑/家具概念设计验证（多视角图输入重建结构）  
  - AR 应用轻量化模型生成（GLB 直接嵌入 Unity/Unreal/WebGL）  
- **慎用场景**：  
  - 无明确三维结构需求的纯视觉内容（如 Banner、海报）  
  - 需要实时生成或高频迭代（3D 任务耗时长，不适合 A/B 测试类场景）  
  - 输入仅为文本描述且缺乏结构关键词（如“一个氛围感场景”效果差，需“一张现代客厅沙发，带扶手与木质底座，灰布材质”）

## 开发者技术选型参考指南

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **追求最低延迟 & 最高吞吐** | 图像生成（同步调用模型） | 同步接口平均响应 <10 秒，无轮询开销，SDK 封装成熟；适合日均万级请求的 SaaS 工具 | 避免在同步链路中调用 `kling`/`vidu` 等异步模型，会破坏性能优势 |
| **需要跨模态驱动（图+音+动）** | 视频生成（`wan3.0` 或 `emo-v1`） | `wan3.0` 统一协议支持文本/图/音频/动作多输入；`emo-v1` 对口型精度达行业领先水平 | 务必集成前置 `detect` API，且音频需满足清晰人声、无噪音、≤180 秒 |
| **交付物需进入 3D 工作流（Unity/Blender/Three.js）** | 3D 生成（`Tripo-H3.1`） | 原生输出标准 GLB，含 PBR 材质与法线贴图，无需后处理即可渲染；支持 `ultra` 档位满足专业建模精度 | 仅限北京地域；务必在 2 小时内下载 `pbr_model_url`，过期失效 |
| **预算敏感型 MVP 验证** | 图像生成（`z-image-turbo`）或视频生成（`wan2.7`） | `z-image-turbo` 0.12 元/张，`wan2.7` 0.68 元/任务，为当前性价比最高组合 | `z-image-turbo` 最高仅支持 2048×2048，不适用于印刷级输出；`wan2.7` 不支持首尾帧等高级模式 |
| **需与现有 OpenAI 生态无缝集成** | 图像生成（`qwen-image-3.0-pro`） | 完全兼容 OpenAI API 协议（`base_url` + `model` 切换），零代码改造接入已有 LangChain / LlamaIndex 流程 | 仅限北京/新加坡地域；不支持视频或 3D 的 OpenAI 兼容模式 |

> **重要提醒**：所有生成类 API 均遵循「地域强一致」原则——模型开通地域、API Key 所属地域、Endpoint URL 中的 `{WorkspaceId}` 所属地域三者必须完全相同。跨地域调用将返回明确错误（如 `RegionMismatchError`），**不可通过代理或 DNS 解析绕过**。建议新项目统一使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），避免因旧域名（`dashscope.aliyuncs.com`）引发的稳定性问题。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


