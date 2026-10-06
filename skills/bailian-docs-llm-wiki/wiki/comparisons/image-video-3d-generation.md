# 多模态生成能力对比：图像、视频与3D生成

本文旨在为开发者提供百炼平台三大核心多模态生成能力（图像、视频、3D）的系统性技术对比，帮助在实际业务场景中快速识别能力边界、评估接入成本、规避地域与协议陷阱，并做出高效、可持续的技术选型决策。随着AIGC从“内容可视化”向“空间可交互”演进，图像、视频与3D生成已形成互补而非替代的关系——图像承载语义表达与创意起点，视频注入时间维度与动态叙事，3D则构建可渲染、可编辑、可集成的三维数字资产。本对比基于当前（2024年Q2）百炼平台正式发布的生产级API能力，覆盖模型支持、调用机制、资源约束与工程实践等关键维度。

## 关键能力维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|------------------------------|-------------------------------|--------------------------|
| **输入格式** | 文本（`prompt`/`messages.text`）、单图（URL/Base64）、多图（部分模型如 `wan2.5-i2i-preview`）、局部掩码（`mask_image`） | 文本（≤512字符）、单图（URL/Base64）；**不支持视频/帧序列输入** | 文本（≤1024字符）、单图（URL，≤20MB）、多图（严格4张，前/左/后/右顺序） |
| **输出格式** | PNG（默认，暂不支持JPEG/WebP）；异步任务返回 `url`（有效期24小时） | MP4（H.264编码）；异步任务返回 `video_url`（有效期24小时） | GLB（标准glTF二进制格式）；含 `base_model_url`（无贴图）、`pbr_model_url`（PBR材质）、`rendered_image_url`（预览图）；所有URL有效期2小时 |
| **支持模型（代表）** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `aitryon-plus`, `kling-v3-omni-image-generation`, `facechain-generation` | `kling-v1.0`, `vidu-v2`, `wanx-v2`, `portrait-animation`, `minimax-video` | `Tripo/Tripo-H3.1`（高精度，≤200万面），`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 端点** | 多端点：<br>• 同步：`POST /api/v1/services/aigc/image-generation/generation`<br>• 异步：`POST /api/v1/services/aigc/image-generation/generation` + `GET /api/v1/tasks/{id}`（需 `X-DashScope-Async: enable`） | **统一端点**：<br>`POST https://dashscope.aliyuncs.com/api/v1/videos/generations`（OpenAI兼容）<br>轮询：`GET /v1/videos/{id}` | **专用端点（地域强绑定）**：<br>`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>轮询：`GET /api/v1/tasks/{task_id}`（必须华北2北京） |
| **调用模式** | 同步（低延迟模型如 `z-image-turbo`）与异步（高耗时任务如试衣/写真）**并存**；模型决定默认模式 | **全异步**：提交即返回 `id`，需轮询状态；无同步直出能力 | **强制异步**：`X-DashScope-Async: enable` 为必填Header；同步调用直接报错 |
| **地域要求** | **严格三地一致**：API Key、Endpoint、模型部署地域必须相同（如北京/新加坡/弗吉尼亚）；模型地域分布不均（例：`wan2.7-image-pro` 不支持弗吉尼亚） | **公共域名全域可用**：`dashscope.aliyuncs.com` 支持所有已开通地域；但模型本身可能有地域限制（需查文档） | **仅限华北2（北京）**：Endpoint、API Key、服务开通均锁定北京地域；其他地域URL不可用 |
| **计费方式** | 按生成张数计费（例：`aitryon-plus` 0.50元/张，`wordart-semantic` 0.08元/张）；共享90天500张免费额度 | 按生成视频条数计费（各模型单价不同，如 `kling-v1.0` 为2.5元/条）；免费额度独立核算 | 按成功生成任务计费（`Tripo-H3.1` 3.8元/次，`Tripo-P1.0` 0.8元/次）；无公开免费额度，需单独申请体验包 |
| **典型场景** | • 创意海报/电商主图生成<br>• UI界面/图表/Logo设计<br>• 人物写真/虚拟模特试衣<br>• 局部重绘/背景替换/风格迁移 | • 营销短视频脚本可视化<br>• 产品功能动态演示<br>• 人脸驱动口播视频<br>• 动画分镜预演（`kling-v3-omni`） | • 游戏/AR/VR资产快速建模<br>• 电商360°商品展示模型<br>• 工业零件概念原型生成<br>• 建筑/家具轻量化建模 |

## 各方案适用场景建议

### ✅ 图像生成 —— 适合「高频率、细粒度、强可控」的内容生产
- **推荐场景**：  
  - 需要批量生成大量静态素材（如千张商品图、百套海报变体）；  
  - 对提示词遵循度、文本渲染（如Logo文字）、局部编辑（如换背景、改服饰）有明确要求；  
  - 开发者需灵活切换模型（如用 `qwen-image-3.0-pro` 做语义理解，再用 `aitryon-plus` 做试衣）；  
  - 已有成熟图像工作流，希望以最小改造接入AIGC能力（支持OpenAI兼容协议）。  
- **慎选场景**：  
  - 需要实时预览（>1s延迟敏感）且无法接受异步轮询；  
  - 输入源为视频或长序列帧（需先抽帧转图）；  
  - 要求输出JPEG/WebP等压缩格式（当前仅PNG）。

### ✅ 视频生成 —— 适合「动态叙事、人机交互、轻量动画」需求
- **推荐场景**：  
  - 将文案/脚本一键转为3–4秒短视频（营销、教育、社交）；  
  - 为人脸照片生成口播/表情动画（`portrait-animation`）；  
  - 基于单张产品图生成旋转展示视频（`wanx-v2`）；  
  - 需要统一API管理多模型（`kling`重质量、`vidu`重速度、`minimax`重语音驱动）。  
- **慎选场景**：  
  - 需要生成>4秒长视频（当前模型最大支持4秒）；  
  - 输入为复杂多视角图像集（3D重建类需求应转向3D生成）；  
  - 要求精确控制每一帧内容（无逐帧编辑API）；  
  - 对负向提示词（`negative_prompt`）有强依赖（仅 `minimax-video` 支持）。

### ✅ 3D生成 —— 适合「空间构建、资产复用、跨平台集成」目标
- **推荐场景**：  
  - 从产品描述或参考图快速生成可导入Unity/Unreal/Three.js的GLB模型；  
  - 构建电商360°展示页所需的轻量级（`P1.0`）或高保真（`H3.1`）模型；  
  - 需要PBR材质贴图支持（设 `pbr: true`）实现物理渲染效果；  
  - 已有四视图拍摄流程（前/左/后/右），追求高精度重建。  
- **慎选场景**：  
  - 非北京地域团队且无法迁移基础设施；  
  - 需要生成非GLB格式（如OBJ/FBX/STL）；  
  - 输入为单张非正向人脸图（易失败，非其设计目标）；  
  - 要求实时生成（任务平均耗时2–8分钟，需合理设计轮询策略）。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **首次集成，追求最快上线** | 图像生成（`qwen-image-3.0-pro` 或 `z-image-turbo`） | 支持同步调用、OpenAI兼容、文档最完善、免费额度通用；调试成本最低 |
| **需统一API管理多模态能力** | 视频生成（统一 `/v1/videos/generations` 端点） | 所有模型共用同一请求结构与轮询逻辑，SDK封装成熟，降低多模型运维复杂度 |
| **构建三维数字资产管线** | 3D生成（`Tripo/Tripo-P1.0` 入门 → `H3.1` 进阶） | 唯一提供标准GLB输出的官方能力；PBR支持满足工业级渲染需求；多图输入适配专业建模流程 |
| **高并发、低延迟任务（如实时UI生成）** | 图像生成（`z-image-turbo` 同步模式） | QPS上限达10，响应时间<800ms；明确标注“轻量级快速生图” |
| **严格合规场景（如金融/政务可视化）** | 图像生成（`qwen-image-3.0-pro` + 专属Workspace域名） | 支持业务空间专属Endpoint（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），满足私有化部署与数据隔离要求 |
| **需与现有3D引擎深度集成** | 3D生成（启用 `pbr: true` + `texture_quality: "detailed"`） | 输出含完整PBR材质集（albedo/normal/roughness/metallic），可直接拖入Unity HDRP或Unreal Engine 5.3+ |

> **重要提醒**：  
> - **地域是第一道关卡**：务必在控制台确认目标模型在你所在地域是否可用，切勿假设“全地域支持”。  
> - **异步不是可选项，而是必选项**：除少数图像模型外，视频与3D生成**必须**采用轮询或回调机制；高频轮询请启用[异步回调](../../raw/model-api-reference/more-about-models/async-task-api.md)避免QPS超限。  
> - **输入校验极严格**：图像Base64需去前缀、URL需公网可访问且无中文路径；3D多图必须4元素数组；视频prompt超512字符将被静默截断——建议前置长度检查。  
> - **模型演进快，文档须常新**：万相V1、千问旧版图像模型等已明确标记为“不推荐”，接入前请核对[最新模型列表](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)及各子文档更新时间戳。  

通过本对比，开发者可清晰识别：图像生成是多模态的“基石入口”，视频生成是“动态延伸”，而3D生成则是“空间锚点”。三者协同，方能支撑从平面创意到沉浸式体验的全栈AIGC应用落地。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


