# 多模态生成能力对比：图像、视频与3D生成

本对比旨在为开发者提供清晰、可落地的技术选型参考，帮助在实际业务场景中快速判断应选用图像生成、视频生成还是3D生成能力。随着AIGC技术演进，三类多模态生成服务在输入范式、输出形态、计算范式、地域约束及工程集成复杂度上已形成显著差异。本文基于百炼平台当前（2024年Q3）正式发布的API能力，从开发者视角出发，系统梳理关键维度差异，并给出分场景的选型建议。

## 关键维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） | 3D生成（3D Generation） |
|------|-----------------------------|------------------------------|--------------------------|
| **核心输入格式** | 文本（`prompt`）、单图URL/Base64（`image_url`/`image`）、多参考图（最多10张）、涂鸦草图、人脸训练集（FaceChain） | 文本（`prompt`）、首帧/首尾帧图像URL、参考图像数组（`reference_images`）、原始视频URL、音频URL（对口型）、动作参考视频（动作模仿） | 文本（`prompt`）、单图URL（`image`）、四视角图数组（`images`，固定顺序 `[front,left,back,right]`）、已有3D模型URL（后处理） |
| **核心输出格式** | PNG/JPEG Base64（同步）或公网可访问URL（异步），支持1K/2K/4K分辨率及多种宽高比（1:1, 16:9, 9:16） | MP4视频URL（H.264编码，30fps），时长通常为2–30秒；部分模型支持关键帧序列导出 | GLB/FBX（网格模型）、`.splat`（Gaussian Splatting）、USDZ、STL等；贴图包（PBR材质）、分割掩码、骨骼绑定文件（FBX+动画） |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`、`vidu/viduq2-pro_reference2image`、`virtualmodel-v2`（限免） | `wan3`（万相3.0）、`kling/kling-v4-video-generation`、`vidu`、`pixverse`（爱诗）、`happyhorse` | `Tripo/Tripo-H3.1`（主生成）、`Tripo/Tripo-P1.0`、`Tripo/Tripo-ImageToSplat`、`Tripo/Tripo-Animation`（绑骨/重定向） |
| **API端点路径** | `POST /api/v1/services/aigc/multimodal-generation/generation`（同步/异步混用）<br>部分创意工具使用 `/aigc/image-synthesis` | `POST /api/v1/services/aigc/video-generation/video-synthesis`（统一主路径）<br>部分旧模型使用 `/aigc/image2video/`（如 `image2video/video-synthesis`） | `POST /api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation`，属历史命名，实际为3D专属） |
| **调用模式** | **混合模式**：<br>• 同步：`qwen-image-3.0-pro`、`z-image-turbo` 等快响应模型（<5s）<br>• 异步：万相编辑、可灵、Vidu、所有创意工具（需轮询） | **强制异步**：<br>全部模型均需两步流程（创建任务 → 轮询 `tasks/{task_id}`），无同步选项。典型耗时：30s–5分钟。 | **强制异步**：<br>全部接口均为异步，任务生命周期长（生成：2–10分钟；后处理：1–8分钟；动画：3–15分钟）。`task_id` 有效期24小时。 |
| **地域约束强度** | ⚠️ 强绑定：模型、API Key、Endpoint 必须同地域（北京/新加坡/弗吉尼亚等），跨域调用100%失败 | ⚠️ 强绑定：同图像生成，且部分模型（如PixVerse）仅限北京地域 | ❗️ 极强绑定：**仅支持华北2（北京）地域**，API Key、Endpoint、控制台开通均必须在北京，其他地域Key完全不可用。 |
| **计费方式** | • 按次计费（如 `qwen-image-3.0-pro`：0.02元/张）<br>• 部分创意工具（`virtualmodel-v2`, `shoemodel-v1`）为**500次免费额度，用尽即停，不支持付费**<br>• FaceChain训练：2.5元/次（检测限时免费） | • 按视频秒数计费（主流）：如 `wan3` 0.15元/秒，`pixverse` 0.20元/秒<br>• 部分能力按任务计费（如 `videoretalk` 0.08元/秒）<br>• 多数模型提供初始免费额度（如1800秒） | • 按任务类型分层计费：<br>  - 基础生成：`Tripo-H3.1` 1.2元/次（文生/图生）<br>  - Gaussian Splat：0.8元/次<br>  - 后处理：贴图（0.5–3.0元）、重拓扑（1.0–5.0元）、动画（2.0–8.0元）<br>• 所有高级参数（`quad=true`, `face_limit≠default`, `texture_size>4096`）触发额外费用 |
| **典型场景** | • UI/海报/电商图生成与编辑<br>• 虚拟模特换装、鞋靴展示<br>• 文档图表像素级还原（Vidu）<br>• 人像风格迁移与写真生成（FaceChain） | • 短视频营销内容批量生成（文生/图生）<br>• 产品演示视频（参考生视频）<br>• 数字人口播（对口型+动作模仿）<br>• 视频风格化与超清增强 | • 游戏/AR/VR资产快速建模（文生/图生3D）<br>• 工业设计原型验证（四视角图→3D）<br>• 实时渲染场景构建（Gaussian Splatting）<br>• 3D电商展示（GLB+PBR贴图+自动绑骨） |

## 各方案适用场景建议

### ✅ 优先选择图像生成，当：
- 需要**毫秒级响应**或低延迟集成（如实时UI预览、设计协作工具）；
- 任务以**静态视觉表达为核心**（Banner、LOGO、商品主图、社交媒体配图）；
- 需高频调用轻量编辑能力（局部重绘、擦除补全、风格迁移），且预算敏感；
- 使用虚拟模特、鞋靴模特等垂直创意工具（注意：仅限免费额度内使用）；
- 输入为高质量单图，目标是**保形保结构的精细编辑**（如Vidu的UI还原、可灵的中英文字渲染）。

### ✅ 优先选择视频生成，当：
- 核心交付物是**15–30秒短视频**，用于信息流广告、电商详情页、社交媒体传播；
- 具备**首帧/首尾帧图像**，需生成连贯动态内容（如产品旋转、场景过渡）；
- 需结合**语音/动作参考**实现数字人播报或角色动画（PixVerse对口型、Kling动作模仿）；
- 业务已建立视频素材库，希望基于**参考视频生成新内容**（HappyHorse/Vidu参考生视频）；
- 可接受**分钟级任务延迟**，且能稳定维护异步轮询逻辑。

### ✅ 优先选择3D生成，当：
- 最终目标是**可交互、可渲染、可导入引擎的3D资产**（非视频帧序列）；
- 输入为**文本描述或单张产品图/四视角图**，需生成带拓扑结构的网格模型（非点云）；
- 需进入专业工作流：如Unity/Unreal导入、Blender再编辑、WebGL实时展示；
- 要求**物理可信的材质表现**（PBR贴图）、**轻量化适配移动端**（智能重拓扑）、**支持骨骼绑定与动画**；
- 项目已锁定在北京地域部署，且能接受**严格的任务依赖链**（如：生成→贴图→分割→绑骨→重定向）。

## 面向开发者的选型参考指南

1. **先验检查：地域与认证**  
   - 若项目部署在**新加坡/弗吉尼亚等地域** → 排除3D生成；图像/视频需确保Key与Endpoint同域。  
   - 若使用**北京地域但需跨账号协作** → 注意3D后处理任务（`original_model_task_id`）仅限同账号引用，视频/图像无此限制。

2. **输入准备成本评估**  
   - 文本输入 → 三者均支持，但3D对prompt语义精度要求更高（需明确“工业风”“低多边形”“PBR材质”等）；  
   - 单图输入 → 图像生成最灵活（支持Base64）；视频/3D**强制要求公网URL**，需额外上传步骤；  
   - 多图输入 → 3D要求严格四视角（`[front,left,back,right]`），视频仅需首帧/首尾帧，图像最多支持10张参考图。

3. **工程集成复杂度排序（由低到高）**  
   ```mermaid
   graph LR
     A[图像生成] -->|同步调用简单| B[视频生成]
     B -->|强制异步+长轮询| C[3D生成]
     C -->|任务强依赖+多阶段串联| D[3D动画流水线]
   ```
   - 图像生成：同步模型可单请求返回Base64，适合前端直调；  
   - 视频生成：必须实现健壮轮询（含重试、超时、状态机），建议封装为SDK任务管理器；  
   - 3D生成：需构建**任务图谱**（DAG），例如：`generate → texture → retopology → rig → retarget`，每个节点失败需回滚或降级。

4. **成本敏感型选型提示**  
   - 避免误用免费额度模型：`virtualmodel-v2`等创意工具**无付费通道**，额度用尽即中断服务，生产环境请迁移到`qwen-image-3.0-pro`或`wan2.7-image-pro`；  
   - 视频按秒计费，生成30秒视频 ≈ 4.5元（wan3），若只需关键帧，可考虑“图像生成+前端插帧”替代；  
   - 3D生成中，`Tripo-P1.0`比`H3.1`便宜约40%，但不支持`geometry_quality`等高级参数，需权衡精度与成本。

5. **未来演进关注点**  
   - 图像：千问图像系列正强化多图融合编辑与3D一致性（如生成带深度图的图像）；  
   - 视频：Kling/Vidu v4已支持“任意关键帧组合”，为分镜脚本驱动视频生成铺路；  
   - 3D：Tripo H3.1已支持`smart_low_poly`智能减面，后续将开放NeRF导出与物理仿真接口。

> **最后建议**：首次接入请严格遵循各文档中的「地域专属域名」（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），禁用旧版`dashscope.aliyuncs.com`。所有异步模型务必显式设置请求头 `X-DashScope-Async: enable` —— 这是百炼平台最常被忽略却导致100%失败的配置项。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


