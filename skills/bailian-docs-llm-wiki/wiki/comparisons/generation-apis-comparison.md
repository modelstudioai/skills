# 多模态生成 API 对比：图像、视频与3D生成

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术能力边界与工程适配要点，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心API能力。对比聚焦实际开发中高频关注的**输入/输出规范、模型生态、调用模式、地域约束、计费策略及典型落地场景**，旨在提供可操作的技术选型决策依据，避免因配置错配、地域混淆或模型误用导致的集成失败与业务中断。

---

## 关键维度对比表

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|-----------------------------|-----------------------------|--------------------------|
| **核心输入格式** | 文本（prompt）、图像URL/Base64（支持T2I/I2I/局部编辑）、多图参考（如可灵分镜） | 文本（prompt）、图像URL（图生视频）、音频URL/文本（人像驱动）、多镜头描述（可灵） | 文本（prompt）、单张图像URL、或多张按 `[前, 左, 后, 右]` 顺序排列的图像URL（2–4张） |
| **核心输出格式** | JPEG/PNG 图像（Base64 或 24小时有效公网URL）；部分模型支持返回推理过程（`thinking_mode`） | MP4 视频（H.264编码，24小时有效URL）；Vidu 默认带角标水印（付费用户可关闭） | GLB 格式 3D 模型（含 PBR 材质贴图）；返回 `pbr_model_url`（含材质）或 `base_model_url`（无贴图），有效期2小时 |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/viduq2-pro_reference2image`, `z-image-turbo` | `vidu`, `kling`（企业权限）、`happyhorse`, `wanx-video`, `portrait-animation`（人像驱动）、`pixverse`（爱诗）、`minimax`（轻量实时） | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速调试，≤2万面） |
| **API 端点协议** | 同步（`/images/generations`）与异步（`/generation` → `/task/{id}`）双模式；千问系列支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) | **统一异步模式**：`POST /v1/videos/generate` → `GET /v1/tasks/{task_id}`；不支持同步调用 | **强制异步模式**：`POST /api/v1/services/aigc/video-generation/3d-generation`（需 `X-DashScope-Async: enable` 头）→ `GET /api/v1/tasks/{task_id}` |
| **地域与域名要求** | **强地域绑定**：API Key、Workspace ID、Endpoint 必须同地域（北京/新加坡/弗吉尼亚）；推荐使用 Workspace 专属域名（如 `{ws}.cn-beijing.maas.aliyuncs.com`） | 同图像生成：严格地域隔离；各模型 Endpoint 均需匹配对应地域的 API Key 与 Workspace | **仅限华北2（北京）地域**：硬性限制，跨地域调用直接报错；必须使用北京地域 API Key 与专属域名 |
| **计费方式** | 按调用次数（per request）或生成图片张数（`n`/`series_amount`）计费；免费体验模型（如 `wanx-virtualmodel`）额度用尽即停用且不可续费 | 按视频时长（秒）× 分辨率档位计费（如 Vidu 4s/8s/12s 档）；HappyHorse/万相/Vidu 提供免费额度；MiniMax/可灵需单独购配额 | 按任务成功次数计费；`Tripo-H3.1`（高面数）单价高于 `Tripo-P1.0`（低面数）；无免费额度，全部按量付费 |
| **典型场景** | 营销海报自动生成、电商商品图渲染、AI写真（FaceChain）、UI设计稿还原、风格化艺术创作、局部图像修复 | 短视频脚本可视化、电商产品动态展示、虚拟人播报视频、赛博朋克/国风等艺术运镜视频、直播互动实时动画 | 电商3D商品建模（单图转3D）、工业零件概念建模、游戏资产快速原型、AR/VR内容预研、3D打印前模型生成 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高精度、强可控、多形态」图文内容生产  
- **首选场景**：需要精细控制构图、风格、主体一致性（如 `element_list`）、局部编辑（擦除重绘）、或需对接专业工作流（如 Photoshop 插件、CMS 图床自动上传）。  
- **推荐模型组合**：  
  - 通用高质量：`qwen-image-3.0-pro`（T2I+I2I一体化，OpenAI兼容）  
  - 中文营销强适配：`wan2.7-image-pro`（4K输出、组图生成、`thinking_mode`调试友好）  
  - 快速迭代/文字渲染：`z-image-turbo`（512×512～2048×2048，响应快）  
- **避坑提示**：避免依赖已标注“仅限免费体验”的模型（如 `wanx-x-painting`），生产环境务必迁移至千问3.0或万相2.1+商用模型。

### ✅ 视频生成 —— 适合「中短时长、语义驱动、轻交互」动态内容生成  
- **首选场景**：广告创意预演、社交媒体短视频批量生成、虚拟人数字分身播报、UI动效原型验证。  
- **推荐模型组合**：  
  - 平衡质量与成本：`vidu`（中文语义强、支持 `hide_watermark`、免费额度可用）  
  - 高自由度分镜：`kling`（需企业权限，支持120秒+多镜头逻辑）  
  - 实时互动需求：`minimax`（<3s延迟，适用于直播弹幕触发动画）  
- **避坑提示**：人像驱动模型对输入图质量敏感（正脸/无遮挡/光照均匀），务必前置图像质检；`kling` 未开通权限时调用将返回 `403`，不可仅靠错误码判断模型可用性。

### ✅ 3D生成 —— 适合「结构明确、几何优先、专业下游」三维资产构建  
- **首选场景**：无需专业建模师的轻量级3D资产生成、电商SKU快速3D化（尤其家居/饰品/玩具类）、AR试穿/试摆前期验证、游戏场景概念草模。  
- **推荐模型组合**：  
  - 高保真交付：`Tripo/Tripo-H3.1` + `geometry_quality: "ultra"` + `pbr: true`（用于渲染/AR发布）  
  - 快速原型验证：`Tripo/Tripo-P1.0`（2万面以内，生成快，适合A/B测试）  
- **避坑提示**：多图输入**必须严格按 `[前,左,后,右]` 顺序传参**，缺位需用 `{}` 占位；`pbr: true` 会强制启用贴图（`texture: true`），若需纯网格模型，必须同时设 `pbr: false` 且 `texture: false`。

---

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| **追求最低接入门槛与调试效率** | 图像生成（`qwen-image-3.0-pro` 同步调用） | 支持 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，SDK 无缝迁移；同步响应便于前端实时预览；文档示例丰富，错误反馈明确。 |
| **需要端到端可控的异步任务管理** | 视频生成（统一 `/v1/videos/generate` + `/v1/tasks/{id}`） | 所有模型共用同一套异步协议，回调/轮询逻辑可复用；错误码体系统一（`invalid_input`, `quota_exhausted` 等），利于统一监控告警。 |
| **必须保障生产环境连续性与SLA** | 图像/视频生成 → 选用 `qwen-image-3.0-pro` / `vidu`；3D生成 → 仅用 `Tripo-H3.1` | 上述均为正式商用模型，无免费额度清零风险；支持企业级配额包购买、用量预警与独立QoS保障；文档明确标注弃用路径（如万相V1已淘汰）。 |
| **涉及跨地域多中心部署** | **仅图像与视频生成支持**（北京/新加坡/弗吉尼亚三地全量覆盖）；**3D生成不可跨地域** | 若业务需全球用户就近访问，3D能力必须集中部署于北京节点，并通过CDN缓存GLB文件；图像/视频服务可按用户地域就近调度Endpoint。 |
| **需与现有AI工作流深度集成（如LangChain、LlamaIndex）** | 图像生成（千问系列） + 视频生成（Vidu） | 千问图像API完全兼容 OpenAI SDK；Vidu 视频API参数设计简洁（`input.text`, `parameters.duration`），易于封装为Tool；二者均提供稳定Webhook回调，适配Agent编排。 |

> **最后提醒**：所有多模态API均强制要求 **API Key、Workspace ID 与 Endpoint 地域一致**。这是百炼平台最常见集成失败原因——请在初始化客户端时显式校验三者地域标签（如 `cn-beijing`），并在CI/CD流程中加入地域配置检查脚本。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


