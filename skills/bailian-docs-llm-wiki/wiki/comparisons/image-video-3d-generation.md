# 图像生成、视频生成与 3D 生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与 3D 生成（3D Generation）三大核心能力。对比聚焦实际工程落地关键维度，涵盖输入/输出规范、模型生态、调用方式、资源约束及适用场景，旨在为技术选型提供客观、可操作的决策依据。

---

## 能力维度对比表

| 维度 | 图像生成 | 视频生成 | 3D 生成 |
|------|----------|----------|---------|
| **输入格式** | • 文本（[prompt](../guides/prompt.md)）<br>• 单图或双图（图生图、局部重绘、首尾帧编辑）<br>• 多图（万相2.5融合编辑）<br>• 支持 Base64 或公网 HTTPS URL（需无中文路径） | • 文本（[prompt](../guides/prompt.md)）<br>• 单图（首帧）或双图（首尾帧）<br>• 参考图集（`ref_images`）或参考视频（`ref_video_url`）<br>• 原始视频（用于编辑）<br>• 驱动图像+音频（人像驱动类）<br>• 所有 URL 必须公网可访问、HTTPS、无防盗链 | • 文本（**仅支持英文 [prompt](../guides/prompt.md)**，≤200 字符）<br>• 单张 RGB 图像（JPG/PNG，推荐 512×512 ~ 1024×1024，1:1 宽高比）<br>• `image_url` 必须公网可直连（禁止内网/私有 CDN） |
| **输出格式** | • PNG/JPEG 格式图像（单张或多张）<br>• 输出分辨率灵活（如 `1024*1024`、`4K` 预设）<br>• 异步任务返回 `output.images[]` 数组含 URL（有效期 24 小时） | • MP4 格式视频（H.264 编码）<br>• 分辨率支持 `480P`/`720P`/`1080P`/`4K`（依模型而定）<br>• 帧率可配（如 `24fps`/`30fps`）<br>• 异步返回 `output.video_url`（有效期 24 小时） | • GLB 格式 3D 模型（含几何、PBR 材质、基础光照）<br>• **不支持动画、骨骼、蒙皮、多材质分组**<br>• 文件大小 ≤ 15 MB<br>• `output.glb_url` 有效期 24 小时 |
| **支持模型** | • **通用模型**：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`、`vidu/vidu-image-pro_reference2image`<br>• **创意工具**：`aitryon-plus`（试衣）、`facechain`（写真）、`wanx-x-painting`（局部重绘）等<br>• **轻量模型**：`z-image-turbo`、`wordart-*` 系列 | • **主力模型**：`happyhorse-t2v`、`wan3`（万相3.0）、`wan2.7-t2v`/`wan2.7-i2v`/`wan2.7-videoedit`、`pixverse/pixverse-v6-t2v`、`pixverse/pixverse-c1-kf2v`<br>• **人像驱动专用**：`wan2.2-s2v`、`emo-detect-v1`、`liveportrait`（需前置检测） | • **唯一模型**：`tripo-1.0`（Tripo 官方 v1.0）<br>• **无替代模型或版本迭代计划公开说明** |
| **API 端点** | • 同步：`POST /api/v1/services/aigc/image-generation/generation`（千问/万相2.7等）<br>• 异步：`POST /api/v1/services/aigc/image-generation/generation` + `X-DashScope-Async: enable`（万相V1/V2、可灵、Vidu等）<br>• **必须同地域 Endpoint + API Key** | • 统一异步端点：<br> `POST /api/v1/services/aigc/video-generation/video-synthesis`（HappyHorse/万相2.7/3.0/爱诗）<br> `POST /api/v1/services/aigc/image2video/video-synthesis`（数字人/EMO/LivePortrait 等人像驱动）<br>• **所有调用强制启用 `X-DashScope-Async: enable`** | • 统一端点：<br> `POST /v1/models/tripo-1.0/generate`<br>• 任务查询：`GET /v1/tasks/{task_id}`<br>• **不支持同步调用** |
| **计费方式** | • 按生成图像张数计费（1 张 = 1 [Token](../concepts/token.md)）<br>• 免费额度：500 张/90 天（多数模型）<br>• 工具类模型（如 `wanx-x-painting`）额度用尽即停用，**不可付费续订**<br>• QPS/RPS 按主账号+RAM 子账号共享（如 `aitryon` RPS=10） | • 按视频秒数 × 分辨率档位计费（如 `720P×5s` = 1 单位，`4K×10s` = 4 单位）<br>• 免费额度：100 秒/90 天（全模型共享）<br>• 人像驱动类（S2V/EMO）按“驱动时长×人脸数量”单独计费<br>• RPS 限制严格（如 `happyhorse-i2v` RPS=2） | • 按成功生成任务计费（1 次 = 1 [Token](../concepts/token.md)）<br>• 免费额度：20 次/90 天<br>• **无按分辨率/复杂度分级计费，统一单价**<br>• 任务失败（如 prompt 被拒）不扣费 |
| **典型场景** | • 营销海报、电商主图、社交媒体配图<br>• UI 设计稿生成与文字渲染（Vidu）<br>• 虚拟模特上身、AI 试衣、人像写真定制<br>• 图像扩图、擦除补全、风格迁移 | • 影视预告片、短视频广告脚本可视化<br>• 产品动态演示（图生视频+动作模仿）<br>• 数字人直播/客服口型同步（LipSync）<br>• 视频特效添加、老片修复、超清增强 | • 游戏原型资产（道具、场景小物件）<br>• Web3D 展示（官网/AR 应用中的静态展品）<br>• 教育/工业可视化（简单机械结构、生物模型）<br>• **不适用于角色动画、建筑BIM、高精扫描重建** |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、强可控性」需求  
- **首选场景**：需要快速产出高质量静态视觉内容，且对分辨率、构图、文字渲染精度有明确要求（如 UI 还原、电商详情页）。  
- **优势匹配**：  
  - 支持同步调用（低延迟反馈），适合交互式设计工具集成；  
  - 局部重绘、扩图、擦除等编辑能力成熟，工作流闭环完整；  
  - 多模型覆盖广谱需求（从快速草图 `z-image-turbo` 到 4K 设计 `wan2.7-image-pro`）。  
- **规避风险**：避免依赖已标注“仅限免费体验”的模型（如 `shoemodel-v1`），新项目应选用 `qwen-image-3.0-pro` 或 `wan2.7-image-pro`。

### ✅ 视频生成 —— 推荐用于「动态表达、叙事驱动、专业级交付」需求  
- **首选场景**：需将文本/图像转化为具备时间维度的动态内容，尤其强调运动物理性、口型同步、风格一致性。  
- **优势匹配**：  
  - HappyHorse 在真实感与流畅度上表现突出，适合影视级输出；  
  - 爱诗（PixVerse）在高速动作、法术特效等复杂动态场景中具有独特优势；  
  - 万相3.0 提供 All-in-One 统一模型，降低多任务集成复杂度。  
- **规避风险**：  
  - 人像驱动类模型（S2V/EMO）必须严格遵循“先检测、再驱动”流程，遗漏 `face_bbox` 将直接失败；  
  - 避免混用万相2.7与万相3.0 的参数结构（如 `first_frame_url` vs `img_url`），务必查阅对应模型文档。

### ✅ 3D 生成 —— 推荐用于「轻量化 3D 资产快速原型」需求  
- **首选场景**：需要在 Web 或轻量引擎中快速加载展示静态 3D 模型，对拓扑精度、动画、导出格式无硬性要求。  
- **优势匹配**：  
  - GLB 输出开箱即用，兼容 Three.js、Babylon.js、Unity URP；  
  - 输入门槛低（单图/英文 prompt），适合非专业 3D 设计师协作；  
  - 任务状态清晰，调试成本低。  
- **规避风险**：  
  - **严禁用于中文 prompt**（语义解析失败率近100%），必须预翻译；  
  - 不支持复杂拓扑（如镂空结构、薄壁件）、多部件装配体或 PBR 材质精细控制；  
  - 当前无替代模型，若生成质量不满足需求，需转向专业建模工具或第三方服务。

---

## 开发者技术选型参考

| 选型目标 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| **追求最低延迟 & 实时反馈** | 图像生成（同步模式） | `qwen-image-3.0-pro` 支持毫秒级响应，适合画布实时预览 | 仅限支持同步的模型；需确保地域一致 |
| **需生成带语音驱动的数字人视频** | 视频生成（EMO / LivePortrait） | 专为人像驱动优化，唇形/微表情自然度高 | 必须调用前置检测 API 获取 bbox；仅支持 `/image2video/` 路径 |
| **需批量生成 3D 商品模型用于电商页面** | 3D 生成（Tripo） | GLB 直接嵌入网页，无需额外转换；成本可控 | 中文 prompt 必须翻译；建议用正视角白底图提升成功率 |
| **需从设计稿生成带运行动效的产品宣传视频** | 视频生成（爱诗 PixVerse + motioncontrol） | 支持“动作模仿”指令，可精准复现参考视频中的肢体节奏 | 需提供高质量参考视频（≥1080P，稳定镜头） |
| **需高保真还原 UI 界面中的文字与图标** | 图像生成（Vidu） | `vidu-image-pro_reference2image` 在文字渲染、像素级对齐上表现最优 | 仅支持 `1:1`/`16:9`/`9:16` 宽高比；需提供高清参考图 |

> **重要提醒**：所有能力均强制执行**地域隔离原则**——API Key、Endpoint、模型部署地域三者必须完全一致。跨地域调用将返回明确错误（如 `"region mismatch"`），请在初始化 SDK 或构造请求 URL 前，通过控制台确认业务空间所在地域，并使用专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以获得最佳稳定性与性能。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


