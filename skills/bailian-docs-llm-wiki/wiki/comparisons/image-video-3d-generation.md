# 多模态生成能力对比：图像、视频与3D生成

本文旨在为开发者提供百炼平台多模态生成能力的横向技术对比，聚焦**图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）**三大核心模态。随着AIGC应用从静态内容向动态化、空间化演进，准确理解各模态在输入表达力、输出可控性、工程集成复杂度及成本效益上的差异，是构建高质量AI原生应用的关键前提。本对比基于当前（2024年Q2）平台正式发布的稳定API能力，覆盖模型选型、调用范式、地域约束、计费逻辑与典型适用场景，助力技术团队高效完成多模态技术栈选型。

---

## 关键维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **核心输入格式** | 文本（`prompt`）、单图/多图URL或Base64（支持图文混排、参考图融合）；部分模型支持涂鸦（`sketch`） | 文本（`prompt`）、首帧图（`img_url`）、首尾帧（`first_frame`+`last_frame`）、参考图/视频/音频URL（`media`数组）；数字人需前置人脸检测 | 文本（`prompt`）、单图（`image`）、四视图（`images`数组：前/左/后/右）、或已有3D模型URL（`model_url`）；不支持音频/视频直接输入 |
| **核心输出格式** | JPG/PNG（含透明通道支持，如Qwen-Image）；分辨率灵活（512×512 至 4K）；支持批量生成（`n`/`series_amount`） | MP4（H.264编码）；分辨率档位化（如720P/1080P/4K）；时长可控（最长30秒）；帧率可调（15–25fps）；输出为公网直链 | GLB/GLTF/FBX/OBJ/STL（网格）或 `.splat`（Gaussian Splatting）；面数/精度/拓扑结构可编程（`face_limit`, `geometry_quality`, `quad`）；贴图支持PBR/8K纹理 |
| **主流支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/viduq2-pro_reference2image`, `z-image-turbo`, `facechain-finetune` | `wan3.0`, `kling/kling-v3-omni-video-generation`, `pixverse/pixverse-v6-t2v`, `vidu/viduq3-pro_text2video`, `video-style-transform`, `videoretalk` | `Tripo/Tripo-H3.1`（高精网格）, `Tripo/Tripo-P1.0`（快速轻量）, `Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-AutoRig`, `Tripo/Tripo-Texture` |
| **API端点（统一风格）** | 同步为主：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/image-generation`<br>（异步模型需显式加 `X-DashScope-Async: enable`） | **强制异步**：<br>`POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>（必须带 `X-DashScope-Async: enable`） | **强制异步**：<br>`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>（仅限北京地域，必带 `X-DashScope-Async: enable`） |
| **调用模式** | 混合模式：千问/Z-Image/万相2.7+ 支持同步；万相2.5/可灵/Vidu/创意工具类**强制异步** | **全系列强制异步**：创建任务 → 轮询 `task_id` → 获取 `output.video_url` | **全系列强制异步**：创建任务 → 轮询 `task_id` → 获取 `output.model_url` 或 `output.splat_url` |
| **地域支持** | 华北2（北京）、新加坡、美国（弗吉尼亚）、中国香港等多地域（需Key/Endpoint/模型同域） | 华北2（北京）、新加坡、东京、法兰克福、弗吉尼亚、中国香港等多地域（`wan2.2-s2v`/`videoretalk` 仅限北京） | **仅华北2（北京）地域**；跨地域调用必然失败 |
| **计费方式** | 按**生成张数**（如 `qwen-image-3.0-pro`：0.02元/张）或**计算时长**（如FaceChain训练：2.5元/次）；部分工具类限时免费（额度用尽即停） | 按**视频秒数**（如 `wan2.2-s2v`：0.5元/秒@480P）或**任务次数**（如 `videoretalk`：0.8元/次）；免费额度优先抵扣 | 按**任务次数**（如 `Tripo-H3.1`：8.0元/次）或**后处理模块单独计费**（如 `Tripo-Texture`：3.5元/次）；无通用免费额度 |
| **典型场景** | 社媒配图、电商主图、UI设计稿、艺术创作、人像精修、海报生成、虚拟模特初稿 | 短视频营销、产品演示动画、数字人直播、口型同步配音、视频风格迁移、AI课程微课制作 | 游戏资产建模、AR/VR内容生成、工业零件逆向建模、电商3D商品展示、动画角色绑定与重定向、实时渲染点云重建 |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高并发、低延迟、强语义控制」需求  
- **首选场景**：需要毫秒级响应的前端交互（如设计工具实时预览）、大批量标准化图片生成（如千款商品图批量生成）、对中文文本渲染与细节还原要求极高的创意工作流（如古风海报、手写体LOGO）。  
- **推荐组合**：  
  - 快速原型：`z-image-turbo`（轻量、快、中英均衡）  
  - 工业级质量：`qwen-image-3.0-pro`（强语义遵循+透明通道）或 `wan2.7-image-pro`（4K输出+推理可视化）  
  - 专业人像：`facechain-finetune`（专属形象） + `wanx-style-repaint-v1`（艺术重绘）  
- **避坑提示**：避免在生产环境使用已标注“仅限免费体验”的模型（如 `wanx-virtualmodel`），应切换至Qwen或万相2.1+编辑方案。

### ✅ 视频生成 —— 适合「动态叙事、跨模态协同、实时交互延伸」需求  
- **首选场景**：短视频内容工厂（文生视频→自动剪辑→加字幕）、企业数字人客服（图生视频+口型替换+风格重绘）、教育/培训类动态知识讲解（首尾帧控制动作起止）、AIGC广告片自动化生产。  
- **推荐组合**：  
  - 全能主力：`wan3.0`（多模态统一、多地域支持、协议新）或 `kling/kling-v3-omni-video-generation`（4K+分镜逻辑强）  
  - 垂直提效：`pixverse/pixverse-lipsync`（精准口型） + `video-style-transform`（油画/赛博朋克等一键转译）  
  - 成本敏感：`wan2.7-videoedit`（图生视频编辑，比文生视频便宜约40%）  
- **避坑提示**：务必校验输入媒体URL的公网可访问性；数字人流程必须前置 `face-detect`；避免混用新旧Endpoint路径（如 `/video-synthesis` vs `/image2video/video-synthesis`）。

### ✅ 3D生成 —— 适合「空间建模、工业级精度、管线集成」需求  
- **首选场景**：游戏开发中快速生成NPC道具原型、电商平台3D商品展示（从单图生成可交互GLB）、AR试戴应用（眼镜/饰品单图→3D模型→自动绑骨→驱动动画）、制造业逆向建模（多视图→高精网格→CAD导出）。  
- **推荐组合**：  
  - 高保真资产：`Tripo/Tripo-H3.1`（200万面+`ultra`精度+部件生成） + `Tripo/Tripo-Texture`（8K PBR贴图） + `Tripo/Tripo-AutoRig`（biped骨骼）  
  - 快速验证：`Tripo/Tripo-P1.0`（2万面以内，秒级返回）用于概念筛选  
  - 实时渲染：`Tripo/Tripo-ImageToSplat`（单图→`.splat`，免网格拓扑，Unity/Unreal原生友好）  
- **避坑提示**：所有请求必须在北京地域；后处理任务严格依赖前序成功任务ID；`generate_parts=true` 时禁止启用纹理生成，否则报错。

---

## 面向开发者的技术选型参考

| 选型维度 | 推荐策略 |
|----------|----------|
| **首次集成优先级** | ✅ **图像生成 > 视频生成 > 3D生成**<br>理由：图像API最成熟（同步/异步双模式、多地域、文档最全），调试成本最低，可快速验证平台能力与业务匹配度。 |
| **性能敏感型应用** | ▪ 图像：选用 `z-image-turbo` 或 `qwen-image-3.0-turbo`（响应 <1s）<br>▪ 视频：避开 `wan2.2-s2v`（北京单点瓶颈），优选 `wan3.0` 或 `pixverse`（多地域负载均衡）<br>▪ 3D：`Tripo-P1.0` 是唯一亚秒级选项；`H3.1` 任务平均耗时 2–8 分钟，需合理设计前端等待态。 |
| **成本优化关键点** | ▪ 图像：批量生成时复用同一Prompt+不同`seed`，比多次调用更经济；禁用非必要水印（`watermark=false`）<br>▪ 视频：优先用图生视频（比文生视频便宜30–50%）；控制输出时长（每减1秒≈降费5–10%）<br>▪ 3D：`P1.0` 生成后接 `Retopology` 减面，比直接 `H3.1` 低面数生成更便宜；慎用 `generate_parts`（丧失纹理能力，需额外后处理）。 |
| **工程集成复杂度** | ▪ 图像：同步调用可直接嵌入HTTP服务；异步需自建任务状态机<br>▪ 视频/3D：**必须实现标准轮询机制**（指数退避+超时熔断），建议封装为SDK级 `wait_for_task(task_id)` 方法；`task_id` 有效期24小时，需持久化存储。 |
| **合规与风控** | ▪ 所有模态均需确保输入内容符合《生成式人工智能服务管理暂行办法》；<br>▪ 图像/视频生成结果建议添加平台水印（`watermark=true`）；<br>▪ 3D模型若用于商业发布，需确认 `Tripo` 输出的GLB/FBX无第三方版权依赖（Tripo模型已内置商用授权）。 |

> **最后建议**：对于复合型应用（如“文案→海报→短视频→3D商品页”），建议采用**分阶段渐进式集成**：先打通图像生成闭环，再扩展视频能力，最后接入3D管线。百炼平台提供统一DashScope SDK与OpenAI兼容层（仅图像），可显著降低多模态API的维护成本。详细参数说明、错误码解析与地域Endpoint列表，请查阅各模态对应API参考文档。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


