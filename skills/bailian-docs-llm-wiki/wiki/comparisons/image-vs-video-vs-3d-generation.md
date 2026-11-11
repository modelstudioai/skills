# 图像生成、视频生成与3D生成能力对比

本文旨在为开发者提供百炼平台多模态AIGC能力的横向技术选型参考，聚焦**图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）** 三大核心模态。随着AIGC从静态内容向动态、空间化演进，不同生成范式在输入表达力、输出复杂度、计算开销、工程集成方式及商业化成熟度上存在显著差异。本对比基于当前（2024年Q3）百炼平台正式商用模型能力，覆盖API调用模式、模型支持、资源约束、计费逻辑与典型落地场景，帮助技术团队快速识别适配业务需求的最佳路径。

---

## 能力维度对比表

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **核心输入格式** | 文本提示词（`prompt`）；可选单图/多图URL或Base64（支持JPG/PNG，部分支持透明通道）；支持掩码（`mask_url`）、元素列表（`element_list`）等结构化引导 | 文本提示词；首帧/首尾帧图像URL；参考视频/音频URL；数字人需图像+音频；特效类支持模板名（如`hanfu-1`） | 文本提示词；单图/四视图（`[front,left,back,right]`）URL；3D模型URL（GLB/FBX）；Gaussian Splat输入仅支持单图（WebP/JPEG/PNG） |
| **核心输出格式** | PNG（主流）、JPEG；部分模型支持带Alpha通道PNG；异步任务返回24小时有效直链 | MP4（H.264编码）；分辨率支持480P–4K；帧率15–25fps；异步任务返回24小时有效直链 | GLB/GLTF（网格）、USDZ、FBX（含绑定/动画）、`.splat`（Gaussian Splat）、PBR贴图包（ZIP）；异步任务返回多结果URL（如`base_model_url`, `pbr_model_url`, `splat_url`） |
| **主流支持模型（商用级）** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/vidu-image-pro_reference2image`, `z-image-turbo` | `wan3`, `kling/kling-v3-omni-video-generation`, `vidu/viduq3-pro_text2video`, `pixverse/pixverse-v6-t2v`, `wan2.7-videoedit` | `Tripo/Tripo-H3.1`（高精度网格）, `Tripo/Tripo-P1.0`（专业级）, `Tripo/Tripo-ImageToSplat`, `Tripo/Tripo-AutoRig`, `Tripo/Tripo-AnimationRetarget` |
| **API调用模式** | **同步为主，异步为辅**：<br>• `qwen-image-*`, `z-image-turbo`, `wan2.7-image-*` 支持同步响应（毫秒级）<br>• `kling`, `vidu`, `wanx-x-painting`（免费）等需异步轮询 | **强制异步**：<br>所有接口必须携带 `X-DashScope-Async: enable`，提交后返回 `task_id`，轮询 `GET /api/v1/tasks/{task_id}` 获取结果 | **强制异步**：<br>所有接口必须携带 `X-DashScope-Async: enable`，且**仅支持华北2（北京）地域**；轮询机制与视频一致，`task_id` 有效期24小时 |
| **典型端点（Endpoint）** | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation` | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis` | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>（注意：固定为`cn-beijing`，不随Workspace泛化） |
| **计费方式** | • 按**成功生成图片张数**计费（如1次请求`n=4` → 计4次）<br>• 部分模型（如`wan2.7-image-pro`）按**分辨率档位+张数**组合计费（如4K×1张 vs 1K×4张成本不同）<br>• 免费额度模型（如`wanx-x-painting`）无付费通道，额度耗尽即不可用 | • 按**任务成功执行次数**计费（1个`task_id` = 1次计费）<br>• 分辨率（`resolution`）和时长（`duration`）影响单价（如1080P比480P贵，30秒比5秒贵）<br>• 数字人/口型替换等垂直模型单独定价 | • 按**任务成功执行次数**计费<br>• 关键参数显著影响成本：`face_limit`（面数上限）、`pbr=true`（启用PBR贴图）、`quad=true`（四边面输出）、部件数量（`part_names`长度）均触发阶梯计价<br>• Gaussian Splat（`ImageToSplat`）为独立计费项 |
| **地域约束** | **强地域绑定**：API Key、Workspace ID、Endpoint 必须同地域（如`cn-beijing`, `ap-southeast-1`, `us-east-1`），跨域调用失败 | **强地域绑定**：同图像生成，但各模型可用地域不完全一致（如`viduq3`暂未开放全部地域） | **超严格地域锁定**：**仅支持华北2（北京）**。Workspace ID、API Key、控制台开通、Endpoint 均必须为`cn-beijing`，其他地域调用必失败 |
| **典型端到端耗时** | • 同步：300ms – 3s（轻量模型如`z-image-turbo`）<br>• 异步：5 – 30s（高分辨率/多图编辑类） | 1 – 5 分钟（取决于分辨率、时长、模型负载；`wan3` 30秒视频通常约2分钟） | 2 – 15 分钟（文生3D约3–8分钟；图生Splat约2–5分钟；重拓扑/绑骨等后处理约1–4分钟） |
| **输入资源限制** | • 文本：`kling`≤2500字符，`vidu`≤5000字符<br>• 图像：单图≤10MB，宽高∈[300,8000]px，格式JPG/PNG<br>• 多图：`kling`≤10张，`vidu`≤14张 | • 所有媒体URL需公网可访问（HTTP/HTTPS）；OSS链接需加`X-DashScope-OssResourceResolve: enable`<br>• 首帧图≤10MB；参考视频≤500MB；音频≤100MB | • 图像：≤20MB，格式JPEG/PNG/WebP（Gaussian Splat支持WebP，其余建议JPEG/PNG）<br>• 3D模型：≤150MB，仅限GLB/FBX<br>• 四视图：必须严格4张，顺序固定，空位用`{}`占位 |

---

## 适用场景建议

### ✅ 图像生成 —— 适合「高频、轻量、强可控」内容生产
- **推荐场景**：  
  - 电商商品图批量生成与背景替换（`wan2.7-image-pro` + `mask_url`）  
  - UI设计稿像素级还原（`vidu/vidu-image-pro_reference2image`）  
  - 社媒海报/营销图一键生成（`kling/kling-v3-omni-image-generation` 多图分镜）  
  - 个性化头像/写真（`facechain-finetune` 微调 + `qwen-image-3.0-pro` 批量生成）  
- **慎用场景**：  
  - 需要严格时间一致性（如系列插画角色动作连贯性）→ 应转向视频生成或人工后期  
  - 超高精度工业图纸/建筑渲染 → 当前模型物理精度与几何保真度不足  

### ✅ 视频生成 —— 适合「动态叙事、行为表达、轻量交互」内容生产
- **推荐场景**：  
  - 短视频营销素材（产品演示、活动预告）→ `wan3` 或 `viduq3-pro`  
  - 数字人播报/课程讲解 → `wan2.2-s2v`（单图+音频）+ `animate_emotion=true`  
  - 口型精准同步（配音视频）→ `videoretalk` 或 `pixverse/pixverse-lipsync`  
  - 动作迁移（舞蹈/健身教学）→ `wan2.2-animate-move`  
- **慎用场景**：  
  - 长视频（>60秒）连续生成 → 当前最长支持30秒，需拼接且存在衔接瑕疵  
  - 高精度物理仿真（流体、布料、碰撞）→ 运动真实感仍弱于专业CG流程  

### ✅ 3D生成 —— 适合「空间构建、资产复用、工业化管线」内容生产
- **推荐场景**：  
  - 游戏/AR快速原型：文生基础网格（`Tripo-H3.1`）→ 自动绑骨（`AutoRig`）→ 动画重定向（`AnimationRetarget`）  
  - 电商3D商品展示：单图生成GLB + PBR贴图（`Tripo-Texture`）→ 格式转换（`ConvertFormat`）→ 上传至Three.js/Unity  
  - 实时渲染场景重建：单图生成Gaussian Splat（`Tripo-ImageToSplat`）→ 直接导入Unreal Engine 5.3+  
  - 工业设计辅助：多视图生成网格 → 智能重拓扑（`Retopology`）→ CAD兼容导出  
- **慎用场景**：  
  - 需要毫米级几何精度的机械零件建模 → 当前生成结果需人工CAD修正  
  - 跨地域部署3D服务 → 因**仅支持华北2**，无法满足新加坡/美东客户低延迟需求  

---

## 开发者技术选型指南

| 选型考量 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **追求最低延迟 & 高并发** | ✅ 图像生成（同步模式）<br>• 选用 `qwen-image-3.0-pro` 或 `z-image-turbo`<br>• 避免 `kling`/`vidu` 异步链路 | 同步响应<1s，无轮询开销；适合实时UI预览、A/B测试图生成等场景 |
| **需要跨地域服务部署** | ✅ 图像生成 或 ✅ 视频生成<br>❌ 避免3D生成 | 3D生成强制华北2，而图像/视频模型已在新加坡、美东等多地商用，满足全球化业务SLA |
| **构建端到端AIGC管线（文→图→视→3D）** | ⚠️ 分阶段设计，**不推荐混合调用同一任务**<br>• 文→图：`qwen-image-3.0-pro`（高一致性）<br>• 图→视：`wan3`（首帧继承强）<br>• 图→3D：`Tripo-H3.1`（需统一输入图质量） | 各模态底层模型无联合训练，跨模态提示词迁移效果不稳定；建议用图像生成结果作为下一阶段**确定性输入源**，而非依赖“文生多模态”单次调用 |
| **生产环境稳定性优先** | ✅ 选用明确标注“商用”模型<br>• 图像：`qwen-image-3.0-pro`, `wan2.7-image-pro`<br>• 视频：`wan3`, `kling/kling-v3-omni-video-generation`<br>• 3D：`Tripo/Tripo-H3.1`, `Tripo/Tripo-AutoRig`<br>❌ 规避“仅免费体验”模型（如`wanx-x-painting`, `shoemodel-v1`, `wanx-virtualmodel`） | 免费模型无付费通道、额度耗尽即中断、文档无SLA承诺；商用模型提供配额管理、错误码规范、工单支持与版本长期维护 |
| **预算敏感型POC验证** | ✅ 图像生成（`z-image-turbo`） + ✅ 视频生成（`wan2.1-i2v-turbo` 旧版）<br>⚠️ 注意：`wan2.1-i2v-turbo` 属于早期协议，需确认控制台是否仍开放 | `z-image-turbo` 单次成本最低；`wan2.

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


