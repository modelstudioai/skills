# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力模块。对比聚焦于实际工程落地的关键维度——包括输入/输出规范、模型生态、调用方式、地域约束、计费逻辑及典型适用场景，旨在为技术选型提供清晰、可操作的决策依据。

---

## 能力维度对比表

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|------------------|-------------------|--------------|
| **核心任务类型** | 文生图（T2I）、图生图（I2I）、局部重绘、风格迁移、图像翻译、虚拟模特、人脸写真等 | 文生视频（T2V）、图生视频（I2V，首帧/首尾帧）、参考生视频、视频编辑、风格化、对口型、动作模仿等 | 文生3D、单图/多图生3D网格、Gaussian Splatting、网格分割、重拓扑、格式转换、自动绑骨、动画重定向等 |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`、`kling/kling-v3-omni-image-generation`、`facechain-finetune`、`qwen-mt-image-2.0` | `wan3-video-generation`、`happyhorse-t2v`、`pixverse-v6-t2v`、`vidu/viduq3-pro_text2video`、`kling/kling-v3-omni-video-generation` | `Tripo/Tripo-H3.1`（高精度）、`Tripo/Tripo-P1.0`（专业级）、`Tripo/Tripo-ImageToSplat`、`Tripo/Tripo-Retopology-v2.0`、`Tripo/Tripo-AutoRig` |
| **输入格式** | 文本（[prompt](../guides/prompt.md)）、图像 URL 或 Base64（JPG/PNG/WEBP）、掩码图（mask_url）、多图参考（最多14张）；图像尺寸：宽高比 1:10–10:1，单边 300–8192 px，≤10 MB | 文本（[prompt](../guides/prompt.md)，5000–7000 字符）、图像 URL（首帧/首尾帧）、视频/音频 URL（参考媒体）、模板参数（template）；图像需公网可访问，Vidu 要求单边 ≥256 px；视频支持 MP4/AVI/MOV 等 | 文本（[prompt](../guides/prompt.md)）、单图/四视图 URL（`[front, left, back, right]`）、GLB/FBX/OBJ 等 3D 模型文件；图像 ≤20 MB（≥256×256 px），3D 文件 ≤150 MB |
| **输出格式** | PNG（默认）、JPG（图像翻译）、WEBP；支持水印开关（`watermark=false`）；分镜图支持 `series_amount=2–9` | MP4（H.264 编码，1080p 主流分辨率）；直链 HTTPS URL，有效期 24 小时 | GLB（默认）、FBX（启用 `quad=true` 时强制）、USDZ、STL、`.splat`（Gaussian）、PBR 贴图包（JPEG/PNG）；产物含 `base_model_url`、`pbr_model_url`、`splat_url` 等字段 |
| **调用模式** | **同步 + 异步双模支持**：<br>• 同步：`qwen-image-*`、`wan2.7-image-pro` 等低延迟模型（<3s）<br>• 异步：FaceChain 训练、局部重绘、海报生成等（轮询 `task_id`） | **强制异步**：<br>所有接口必须设置 `X-DashScope-Async: enable`；<br>流程：`POST /video-synthesis` → 轮询 `GET /tasks/{id}`；耗时通常 1–5 分钟 | **强制异步**：<br>统一使用 `/3d-generation` 端点；<br>流程同视频：提交 → 轮询；耗时因任务复杂度差异大（数秒至数十分钟） |
| **API 端点（典型）** | • 同步：`/api/v1/services/aigc/multimodal-generation/generation`（千问/万相/Z-Image）<br>• 异步：`/api/v1/services/aigc/image-generation/image-synthesis`（可灵/Vidu/FaceChain） | `/api/v1/services/aigc/video-generation/video-synthesis`（全系列统一路径） | `/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation`，属历史命名，实际为 3D 专用） |
| **地域支持** | 全地域支持：华北2（北京）、新加坡、美国（弗吉尼亚）等，**但 API Key、Endpoint、Workspace ID 必须严格同地域** | 全地域支持：北京、新加坡、东京、法兰克福、弗吉尼亚、中国香港；**三者同地域为硬性前提** | **仅支持华北2（北京）地域**；API Key、Workspace ID、Endpoint 均须为北京地域，跨地域调用必然失败 |
| **计费方式** | • 按**调用次数 + 分辨率档位**计费（如 `1K`/`2K`/`4K`）<br>• 高阶参数触发加价：`thinking_mode=true`、关闭水印、超大分辨率（>2048×2048）<br>• FaceChain 训练按 GPU 小时计费 | • 按**视频时长 × 分辨率 × 模型等级**计费（如 5s@1080p vs. 10s@4K）<br>• 参考生视频中每增加 1 个媒体 URL 可能产生附加费用<br>• 特殊能力（如对口型、动作模仿）单独计费 | • 按**任务类型 + 面数/精度档位**计费：<br>  – `Tripo-H3.1`（200 万面）＞ `Tripo-P1.0`（2 万面）<br>  – `face_limit` 非默认值、`quad=true`、`texture_size≠4096`、`pbr=true` 等均触发额外费用<br>• Gaussian Splatting、自动绑骨、动画重定向为独立计费项 |
| **典型场景** | • 社媒配图、电商主图生成与换背景<br>• 多语种图文翻译（保留排版）<br>• 虚拟模特试衣、鞋靴展示<br>• 人脸写真定制（LoRA 微调）<br>• UI/图表像素级还原（多图参考） | • 短视频内容创作（广告/剧情/知识类）<br>• 产品动态演示（首帧→3s视频）<br>• 口播视频生成（文本+对口型）<br>• 影视分镜预演（参考图→动态镜头）<br>• 视频风格迁移（如实拍→水墨风） | • 游戏/AR 应用资产快速建模（文/图→GLB）<br>• 工业设计原型可视化（多视角图→可编辑网格）<br>• 实时渲染素材生成（图→Gaussian Splat）<br>• 3D 打印前处理（重拓扑+封口+STL导出）<br>• 数字人驱动准备（自动绑骨+动画重定向） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「静态表达」与「轻量交互」场景  
- **推荐选用当**：需要快速产出高质量静态视觉内容，且对实时性有要求（如后台管理界面预览、A/B 测试图批量生成）；或需深度定制（如人脸 LoRA 训练、多语言图文翻译）。  
- **慎用当**：需表达时间维度信息（运动、过渡、节奏）；或输入强依赖三维空间结构（如需保持物体前后遮挡关系、透视一致性）。

### ✅ 视频生成 —— 适合「动态叙事」与「行为表达」场景  
- **推荐选用当**：内容本质是时间序列（如产品演示、教学过程、剧情短片）；或需融合多模态输入（图像+音频+文本联合驱动）；或对物理运动真实感、唇形同步、动作连贯性有明确要求。  
- **慎用当**：仅需单帧关键画面；或对生成时延极度敏感（无法接受 1 分钟以上等待）；或输入资源难以公网托管（如内网图片需先走临时存储 API）。

### ✅ 3D生成 —— 适合「空间建模」与「生产就绪」场景  
- **推荐选用当**：下游为 3D 引擎（Unity/Unreal）、AR 应用、CAD/CAM 或 3D 打印；需获得可编辑网格、带材质贴图、支持绑定与动画的工业级资产；或多视角输入已具备明确空间语义（前/左/后/右）。  
- **慎用当**：仅需二维呈现效果（可用图像/视频替代）；或输入仅为单张模糊/非正交照片（几何重建质量受限）；或项目部署地域非北京（无替代方案）。

---

## 开发者技术选型参考

| 选型考量点 | 推荐策略 |
|------------|----------|
| **首次集成优先级** | ✅ **从图像生成切入**：API 最成熟、同步调用友好、调试成本最低、文档最完备；可快速验证提示词工程与工作流集成。 |
| **多模态协同设计** | 🔗 **组合使用是常态**：<br>• 图像 → 视频：用 `wan2.7-image-pro` 生成高质量首帧，再送入 `wan3-video-generation`；<br>• 图像 → 3D：用 `Tripo/Tripo-ImageToSplat` 直接生成实时渲染素材；<br>• 视频 → 3D：需自行抽帧+筛选关键视角，再调用 Tripo 多图生模。 |
| **地域架构规划** | 🌐 **务必前置确认地域**：<br>• 若业务需全球部署 → 图像/视频可多地域冗余，**3D 必须集中在北京**；<br>• 建议为 3D 任务单独申请北京 Workspace，并配置独立 API Key 与监控告警。 |
| **异步任务治理** | ⚙️ **统一抽象轮询层**：<br>视频与 3D 均强制异步，建议封装通用 `TaskPoller` SDK 模块，支持：<br>• 自动重试（指数退避）<br>• 超时熔断（如 10 分钟未完成则告警）<br>• 产物 URL 自动缓存与生命周期管理（24 小时有效期需主动续期或下载） |
| **成本优化实践** | 💰 **精细化控制参数**：<br>• 图像：避免无意义高分辨率（`2048×2048` 较 `1024×1024` 费用翻倍）；关闭水印需评估合规风险；<br>• 视频：优先用 `wan3-video-generation`（All-in-One 降低模型切换开销）；控制 prompt 长度，避免触发字符超限降级；<br>• 3D：`Tripo-P1.0` 足够满足多数 Web/移动端需求，`H3.1` 仅用于影视级资产；启用 `quad=true` 前确认下游引擎兼容 FBX 四边面。 |
| **模型演进应对** | 🔄 **关注文档中的“推荐升级”提示**：<br>• 图像：弃用 `wan2.5-i2i-preview`，迁移到 `wan2.7-image-pro`；<br>• 视频：万相 2.x 模型逐步下线，新项目直接采用 `wan3-video-generation`；<br>• 3D：Tripo 模型版本迭代快，建议订阅 [Tripo Release Notes](../../raw/model-api-reference/3d-generation/tripo-api-reference.md) 并定期验证 `face_limit`/`texture_seed` 等关键参数兼容性。 |

> **最后提醒**：所有能力均遵循百炼平台统一安全与合规框架——输入内容需符合《生成式人工智能服务管理暂行办法》，禁止生成违法、侵权、歧视性内容；图像/视频/3D 输出默认含百炼水印（部分模型支持关闭），商用前请确认水印策略与品牌规范一致性。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


