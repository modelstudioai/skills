# 图像生成、视频生成与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦实际工程落地的关键维度——包括输入/输出形态、调用范式、模型生态、地域约束、计费逻辑与典型适用场景，旨在为技术选型提供客观、可操作的决策依据。

> **说明**：所有能力均基于百炼平台当前（2024年Q3）正式发布的API服务，不包含内测、灰度或已下线模型；对比以主流生产就绪模型为准，已明确标注“仅限免费体验”“旧版淘汰”“北京地域独占”等关键限制项。

## 能力维度对比表

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **核心输入格式** | 文本（prompt）、单图（Base64 或公网 URL）、多图（≤10 张，部分模型支持）、涂鸦草图、人脸图像（FaceChain） | 文本（prompt）、单图（首帧）、双图（首尾帧）、参考视频/音频/图片混合媒体（`media` 数组）、数字人驱动音频 | 文本（prompt）、单图、多图（≤6 张）、已有3D模型（GLB/FBX/OBJ 公网 URL）、前序任务 `task_id` |
| **核心输出格式** | JPEG/JPG/PNG（主流）、WebP（部分模型）、带水印/无水印可选；创意工具支持 SVG（海报）、JSON（实例分割掩码） | MP4（H.264 编码，主流）、部分模型支持 MOV；输出含元信息（分辨率、FPS、时长）；URL 有效期 24 小时 | GLB（默认，通用）、FBX（带骨骼/四边面）、OBJ、STL、SPLAT（Gaussian Splatting）、ZIP（含贴图+网格）；URL 有效期 24 小时 |
| **主流支持模型** | `qwen-image-3.0-pro`（文图双模）、`wan2.7-image-pro`（4K）、`kling/kling-v3-omni-image-generation`（分镜组图）、`vidu/viduq3.1-fast_reference2image`（精准画幅）、`facechain-finetune`（人脸定制） | `wan2.7-videoedit`（All-in-One）、`pixverse/pixverse-v6-max-t2v`（高质量）、`kling/kling-v4-text2video`（主体音色库）、`vidu/viduq3-pro_text2video`（广告/剧集细分）、`happyhorse/t2v-pro`（物理真实） | `Tripo/Tripo-H3.1`（高精网格）、`Tripo/Tripo-P1.0`（专业轻量）、`Tripo/Tripo-ImageToSplat`（实时渲染）、`Tripo/Tripo-AutoRig`（自动绑骨） |
| **API 端点（统一路径）** | `/api/v1/services/aigc/multimodal-generation/generation`（同步）<br>`/api/v1/services/aigc/multimodal-generation/generation` + `X-DashScope-Async: enable`（异步） | `/api/v1/services/aigc/video-generation/video-synthesis`（强制异步） | `/api/v1/services/aigc/video-generation/3d-generation`（强制异步） |
| **调用模式** | **混合模式**：<br>• 同步：千问、Z-Image、万相2.6/2.7文生图等（秒级返回）<br>• 异步：可灵、Vidu、FaceChain、创意工具全系（需轮询） | **强制异步**：<br>所有模型必须携带 `X-DashScope-Async: enable`，提交后返回 `task_id`，轮询 `/tasks/{task_id}` 获取结果 | **强制异步**：<br>全部接口强制异步，流程与视频生成一致，`task_id` 有效期 24 小时 |
| **地域约束** | **强地域绑定**：<br>华北2（北京）、新加坡、美国（弗吉尼亚）等独立部署；Endpoint、API Key、Workspace ID 必须同地域；旧域名 `dashscope.aliyuncs.com` 不推荐 | **强地域绑定 + 北京特例突出**：<br>全模型严格同地域；但 VideoRetalk、可灵、Vidu、爱诗、数字人等**仅支持华北2（北京）**；其他地域仅开放 HappyHorse、MiniMax 等有限模型 | **单一地域锁定**：<br>**全部能力仅支持华北2（北京）**；无跨地域部署；开通需在控制台单独授权 “Tripo” 服务 |
| **计费方式** | • 按**调用次数**（如 `qwen-image-3.0-pro` 单次请求生成 1–9 张计 1 次）<br>• 按**分辨率/质量档位**（如 `wan2.7-image-pro` 开启 `thinking_mode` 或 `watermark=false` 可能加价）<br>• 创意工具类（虚拟模特、海报生成等）为**限时免费额度制**，用尽即停 | • 按**任务计费**（1 次 `POST /video-synthesis` = 1 次计费）<br>• 按**输出规格加权**（`1080P` 比 `720P` 贵，`30fps` 比 `15fps` 贵）<br>• 部分能力叠加计费（如 `wan2.2-s2v` 数字人需前置人脸检测，检测本身单独计费） | • 按**任务类型分级计费**：<br> - 基础生成（H3.1/P1.0）：按面数上限（`face_limit`）与精度参数浮动<br> - 后处理（重拓扑/贴图/分割）：按输入模型复杂度与参数组合计费<br> - 动画（AutoRig/Retarget）：按骨骼类型（biped/quadruped）与动作复杂度计费<br>• 所有高级参数（`quad=true`, `texture_quality=extreme`）触发积分上浮 |
| **典型场景** | • 电商主图/详情页批量生成<br>• 社媒配图、营销海报、AIGC创意设计<br>• 人脸写真定制（FaceChain）、局部修图（擦除补全）<br>• 虚拟模特换装、鞋靴产品可视化 | • 短视频脚本分镜视频化（T2V）<br>• 产品广告片（首帧→15s视频）<br>• 数字人口播（图+音频→说话视频）<br>• 视频风格迁移、老片超分修复 | • 游戏/AR/VR资产快速建模（文/图→GLB）<br>• 工业零件扫描补全与重拓扑<br>• 实时渲染场景构建（Image→Splat）<br>• 3D角色动画管线（生成→绑骨→重定向→导出FBX） |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高频、轻量、强可控」需求  
- **推荐场景**：需要快速产出大量静态视觉素材，且对输出一致性、编辑灵活性、成本敏感度高的业务。例如：  
  - 电商平台每日上千款商品的AI主图生成（使用 `qwen-image-3.0-pro` + `size=1024x1024` + `n=4`）；  
  - 品牌社媒运营中“一图多版”风格适配（用 `wanx-style-repaint-v1` 对同一人像批量应用油画/水墨/赛博朋克风格）；  
  - 内部设计工具集成，支持用户上传草图即时转高清图（`wanx-sketch-to-image-lite`）。  
- **慎用场景**：需生成带时间维度内容（如动态效果示意）、或需精确几何结构（如CAD兼容模型）——应转向视频或3D生成。

### ✅ 视频生成 —— 适合「叙事性、表现力、中等时长」需求  
- **推荐场景**：需将抽象概念、产品功能或人物表达转化为动态视听内容，且接受分钟级等待周期。例如：  
  - 教育类App中“知识点动画化”（输入“牛顿第一定律示意图” → `happyhorse/t2v-pro` 生成10s物理演示视频）；  
  - 跨境卖家为新品制作多语种口播短视频（`wan2.2-s2v` + 多语言音频 → 数字人说话视频）；  
  - 影视公司预演分镜节奏（`kling/kling-v4-text2video` 输入分镜脚本 + 关键帧描述 → 生成3段3s视频串联）。  
- **慎用场景**：要求毫秒级响应（如实时滤镜）、超长视频（>60s）、或需逐帧像素级编辑——当前API不支持流式生成与帧序列下载。

### ✅ 3D生成 —— 适合「结构化、可交互、工业化」需求  
- **推荐场景**：下游依赖标准3D资产进行开发、仿真、渲染或制造，且能接受较长任务耗时（数分钟至数十分钟）。例如：  
  - 游戏工作室用产品照片批量生成低多边形角色资产（`Tripo/Tripo-P1.0` + `face_limit=5000` → FBX导入Unity）；  
  - AR家装App实现“手机拍沙发→生成可放置3D模型”（`Tripo/Tripo-H3.1` + `generate_parts=true` → 分部件GLB）；  
  - 汽车零部件厂商对CT扫描数据做AI补全与重拓扑（`Tripo/Tripo-MeshCompletion` + `Tripo/Tripo-Retopology` → 导出STL用于3D打印）。  
- **慎用场景**：仅需简单3D图标（可用SVG替代）、或对实时性要求极高（如WebGL实时生成）——当前Tripo非实时推理架构。

## 面向开发者的技术选型参考

| 决策问题 | 推荐动作 | 关键验证点 |
|----------|----------|------------|
| **我的输入是文本+单张图，目标是快速获得10张不同风格的高清图** | 选用 **图像生成**，模型优先 `qwen-image-3.0-pro`（同步调用）或 `wan2.7-image-pro`（异步，支持4K+无水印） | ✅ 检查地域是否开通对应模型<br>✅ 提示词长度 ≤2048 字符（千问）/ ≤2500 字符（可灵）<br>✅ 图像尺寸在 `[512, 4096]` 像素区间内 |
| **我需要把一段15秒的产品介绍文案转成带配音的数字人视频** | 选用 **视频生成**，链路：`pixverse/pixverse-v6-max-t2v`（文生视频）→ `wan2.2-s2v`（若需换数字人）→ `vidu/viduq3-pro_audio2lip`（对口型优化） | ✅ 全链路必须使用 **华北2（北京）地域** Endpoint 与 API Key<br>✅ 音频文件需为公网可访问 HTTPS URL，且格式为 WAV/MP3（≤100MB）<br>✅ `wan2.2-s2v` 前需调用 `/face-detect` 并传入检测结果 |
| **我想用一张工业阀门照片生成可用于CAE仿真的网格模型，并自动添加法兰连接面** | 选用 **3D生成**，链路：`Tripo/Tripo-H3.1`（图生3D）→ `Tripo/Tripo-SmartSegmentation`（智能分割法兰区域）→ `Tripo/Tripo-MeshCompletion`（补全缺失面）→ `Tripo/Tripo-ConvertFormat`（导出STEP兼容FBX） | ✅ 仅支持 **华北2（北京）**，且需提前在控制台开通 Tripo 服务授权<br>✅ 输入图建议 ≥1024×1024，PNG无损格式<br>✅ `Tripo/Tripo-H3.1` 输出后，需解析 GLB 中节点名作为 `part_names` 输入后续任务 |
| **我的应用需要支持用户上传任意图片，实时生成同构图风格的动效海报（GIF）** | ❌ 当前无原生支持方案。需组合方案：<br>① 图像生成：`qwen-image-3.0-pro` 生成多帧静态图（`n=12`, `size=512x512`）<br>② 自行合成GIF（客户端或服务端FFmpeg） | ✅ 注意 `qwen-image-3.0-pro` 不支持 GIF 输出，需自行拼接<br>✅ 若追求

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


