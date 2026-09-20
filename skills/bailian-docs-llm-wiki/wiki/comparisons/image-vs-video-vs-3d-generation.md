# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦实际工程落地的关键维度——包括输入/输出规范、模型生态、调用协议、地域约束、计费逻辑及典型适用场景，旨在为技术选型提供客观、可操作的决策依据。所有信息均基于2026年Q2最新发布的API文档与平台实践。

## 能力维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|------------------------------|--------------------------|
| **输入格式** | • 文本提示词（`input.prompt`）<br>• 单图/多图（Base64 或公网URL，1–3张）<br>• 涂鸦/蒙版/擦除区域（部分专项模型） | • 文本提示词（`input.prompt`）<br>• 单图（首帧）、双图（首尾帧）、参考图组（`reference_images`）<br>• 原始视频（风格重绘）、音频+人像图（数字人） | • 文本提示词（`input.prompt`）<br>• 单张图像（`input.image`）<br>• 四视角图像数组（`input.images`：前/左/后/右，缺省填 `{}`） |
| **输出格式** | • PNG/JPEG 格式图像 URL（有效期24小时）<br>• 支持多张并行生成（`n=1–9`，依模型而定） | • MP4 格式视频 URL（有效期24小时）<br>• 部分模型支持帧序列下载（如 HappyHorse） | • GLB 格式3D模型 URL（含 `pbr_model_url` 或 `base_model_url`，有效期2小时）<br>• 输出含几何体（`.glb`）与可选PBR材质贴图 |
| **主流支持模型** | • 通用：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`<br>• 轻量：`z-image-turbo`、`wanx-sketch-to-image-lite`<br>• 垂直：`facechain-generation`、`aitryon-plus`、`wordart-semantic` | • 通用：`wan3-video`、`wan2.7-t2v`、`HappyHorse-*`、`pixverse-v6-t2v`<br>• 数字人：`wan2.2-s2v`、`EMO`、`LivePortrait`、`VideoRetalk`<br>• 风格化：`video-style-transform`（8种预设） | • `Tripo/Tripo-H3.1`（高精度，≤200万面）<br>• `Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API端点（Endpoint）** | • 同步/异步混合：<br> `POST /api/v1/services/aigc/multimodal-generation/generation`<br>• 地域专属域名推荐（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`） | • **纯异步**：<br> `POST /api/v1/services/aigc/video-generation/video-synthesis`<br>• 注意：部分旧模型路径不同（如 `/image2video/video-synthesis`），需严格按文档确认 | • **纯异步**：<br> `POST /api/v1/services/aigc/video-generation/3d-generation`<br>• **仅限华北2（北京）地域**，Endpoint 必须为 `cn-beijing.maas.aliyuncs.com` |
| **调用模式** | • **同步为主**：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo` 等低延迟模型支持同步返回<br>• **异步为辅**：编辑、扩图、试衣等长耗时任务需轮询 | • **强制异步**：所有模型均需两步调用（创建任务 → 轮询结果）<br>• `X-DashScope-Async: enable` 为必填Header | • **强制异步**：所有模型均需两步调用（创建任务 → 轮询结果）<br>• `X-DashScope-Async: enable` 为必填Header，且仅北京地域有效 |
| **地域约束** | • **强地域绑定**：模型、API Key、Endpoint 必须同地域（北京/新加坡/弗吉尼亚等）<br>• 推荐使用业务空间专属域名提升稳定性 | • **强地域绑定**：同图像生成，跨地域调用鉴权失败<br>• Endpoint 路径需与模型文档严格一致（避免404） | • **唯一地域支持**：**仅华北2（北京）**<br>• API Key、Endpoint、控制台开通入口三者必须全部在北京地域，否则返回 `InvalidApiKey` 或 `UnsupportedRegion` |
| **计费方式** | • 免费额度：主账号+RAM子账号共享，90天内500张<br>• 按量付费：单价差异显著（例：`aitryon-plus` 0.50元/张，`aitryon-parsing-v1` 0.004元/张，`wordart-semantic` 0.24元/张） | • 免费额度：同图像生成（90天500次任务）<br>• 按任务计费：单价依模型与分辨率而定（如 `wan3-video` 30秒高清视频约1.2元/次，`pixverse-v6-t2v` 5秒标准视频约0.6元/次） | • 免费额度：90天内200次任务（北京地域专属）<br>• 按任务计费：`Tripo-H3.1`（高面数）0.8元/次，`Tripo-P1.0`（快速）0.3元/次；无贴图模型不降价 |
| **典型场景** | • 电商商品图生成与背景替换<br>• 社媒创意海报/配图批量生产<br>• 人物写真、AI试衣、文字艺术设计<br>• 局部重绘、图像扩图、涂鸦转图 | • 短视频营销内容（文生视频/图生视频）<br>• 数字人播报、虚拟主播、AI唱歌/说话视频<br>• 产品演示动画、广告片风格迁移<br>• 视频修复与动态特效增强 | • 工业设计原型快速建模（文生3D）<br>• 电商3D商品展示（单图转3D）<br>• 游戏/AR应用资产生成（四视角重建）<br>• 教育可视化教具制作 |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高频、轻量、多样化」视觉内容生产  
- **首选场景**：需要快速产出静态高质量图片，且对生成延迟敏感（如实时设计工具、AIGC插件、电商后台批量出图）。  
- **推荐组合**：  
  - 通用创作 → `qwen-image-3.0-pro`（图文理解强，支持复杂指令）  
  - 电商落地 → `wan2.7-image-pro`（4K输出，背景生成稳定）  
  - 成本敏感 → `z-image-turbo`（毫秒级响应，中英文字渲染佳）  
- **避坑提示**：避免在非目标地域调用；旧模型（如 `wanx-v1`）已淘汰，务必升级至V2/V3系列。

### ✅ 视频生成 —— 适合「动态表达、人机交互、品牌叙事」需求  
- **首选场景**：需生成具备时间维度的动态内容，尤其适用于营销、教育、虚拟人等强调表现力与真实感的领域。  
- **推荐组合**：  
  - 全能型文/图/参考生视频 → `wan3-video`（统一接口，最长30秒，30fps）  
  - 高质量物理仿真 → `HappyHorse` 系列（运动自然，细节丰富）  
  - 快速数字人 → `wan2.2-s2v`（单图+音频，5秒内生成说话视频）  
- **避坑提示**：必须启用异步流程；注意 `input` 结构因模型类型差异极大（首帧 vs 首尾帧 vs 参考图组），需严格校验字段；路径混淆是404主因。

### ✅ 3D生成 —— 适合「空间建模、工业协同、沉浸式体验」专业场景  
- **首选场景**：需将概念或实物快速转化为可交互、可渲染的3D资产，面向WebGL、Unity、AR/VR等下游引擎。  
- **推荐组合**：  
  - 高保真建模（如工业零件、角色模型）→ `Tripo/Tripo-H3.1` + `geometry_quality: "ultra"`  
  - 快速原型验证（如电商SKU预览）→ `Tripo/Tripo-P1.0`（2万面，秒级生成）  
  - 多视角重建（如小商品360°展示）→ `input.images` 四图输入（严格按【前/左/后/右】顺序）  
- **避坑提示**：**仅北京地域可用**，其他地域配置必然失败；多图输入必须为长度=4的数组，缺省位填 `{}`；无贴图模型需同时禁用 `texture` 和 `pbr`。

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键理由 |
|----------|-----------|-----------|
| **追求最低延迟 & 高并发响应** | 图像生成（`qwen-image-3.0-pro` 或 `z-image-turbo`） | 同步调用，平均响应 <1.5s；支持高RPS，适合SaaS嵌入式服务 |
| **需构建端到端AIGC工作流（文→图→视频）** | 图像生成 + 视频生成（`wan3-video`）组合 | 模型提示词语法高度兼容（如“一只猫跳舞”既可生图也可生视频），降低提示工程成本；共享DashScope协议与认证体系 |
| **面向Web/小程序交付3D可视化能力** | 3D生成（`Tripo-P1.0`） + GLB前端加载库（如Three.js） | 输出标准GLB，免格式转换；`P1.0`生成快、成本低，适配轻量级3D展示场景 |
| **企业级合规与稳定性优先** | 全部选用业务空间专属域名 + 同地域API Key + 异步轮询兜底机制 | 避免公共域名抖动；异步模式天然容错，配合回调机制（非轮询）可进一步提升可靠性 |
| **预算受限但需覆盖多模态能力** | `z-image-turbo`（图） + `pixverse-v6-t2v`（视频） + `Tripo-P1.0`（3D）组合 | 三者均为各品类中单位成本最低的主力模型，免费额度叠加使用可支撑中小规模POC验证 |

> **最后提醒**：所有生成类API均要求 `X-DashScope-Async: enable` 显式声明（即使图像生成支持同步，该Header仍为HTTP调用必填项）；务必通过[百炼控制台](https://bailian.console.aliyun.com)开通对应模型服务，并在代码中注入匹配地域的API Key。跨地域调试失败是新手最高频问题，请优先检查地域一致性。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


