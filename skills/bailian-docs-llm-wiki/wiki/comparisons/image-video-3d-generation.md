# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D内容生成（3D Generation）三大核心能力模块。对比聚焦于**工程集成可行性、模型能力覆盖度、API使用范式及生产环境适配性**，旨在为技术选型提供客观、可落地的决策依据。所有信息均基于2024年Q3最新发布的正式文档与接口规范。

## 关键维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D内容生成（3D） |
|------|-------------------|-------------------|-------------------|
| **输入格式** | 文本（`prompt`）、Base64编码图片（PNG/JPEG，≤10 MB）、二值掩码图（`mask`） | 文本、图片URL或Base64（首帧/首尾帧）、视频URL、音频URL；支持多图输入（如参考生视频）；图片分辨率400×400–7000×7000 | 文本（`prompt`）、单张Base64图片（≤20 MB）、4视角图像数组（`[front,left,back,right]`）、或前序任务`task_id`；3D模型文件（GLB/GLTF/FBX/OBJ/STL，≤150 MB） |
| **输出格式** | PNG/JPEG图片直链（OSS临时URL，有效期1小时）；含`revised_prompt` | MP4视频直链（OSS临时URL，有效期24小时）；部分模型返回元数据（如帧率、分辨率、时长） | 多格式3D资产：GLB/GLTF/FBX/USDZ/STL（网格）、`.splat`（Gaussian Splatting）、PBR贴图包（ZIP）、骨骼绑定文件（FBX）等；全部为OSS临时URL（有效期24小时） |
| **统一API端点** | ✅ `/v1/images/generations`（所有模型共用） | ❌ 无统一端点；按模型/功能分路径：<br>• 通用视频合成：`/api/v1/services/aigc/video-generation/video-synthesis`<br>• 数字人驱动等旧模型：`/api/v1/services/aigc/image2video/...` | ❌ 无统一端点；全部走 `3d-generation` 专用路径：<br>`/api/v1/services/aigc/video-generation/3d-generation`（注意路径中仍含`video-generation`，属历史命名） |
| **调用范式** | 同步请求（HTTP POST，响应含结果URL） | ⚠️ 强制异步（创建任务 → 轮询`task_id`）；需设置`X-DashScope-Async: enable`头 | ⚠️ 强制异步（创建任务 → 轮询`task_id`）；必须设置`X-DashScope-Async: enable`头 |
| **地域约束** | ✅ 全地域可用（与API Key地域一致即可） | ⚠️ 强地域绑定：模型、API Key、Endpoint URL 必须同属一个地域（如`cn-beijing`） | ❗ 严格单地域：**仅支持华北2（北京）**；跨地域调用必然失败 |
| **支持模型（代表）** | WanX（中文艺术）、Kling（图生图）、Z-Image（轻量实时）、Vidu-image（高保真单帧）、Creative Tools（inpainting/outpainting） | WanX（3.0全能版、2.7+子模型）、HappyHorse（物理真实）、PixVerse（动态控制）、Vidu/Kling（文生视频）、MiniMax（参考生视频） | Tripo-H3.1（高精网格）、Tripo-P1.0（快速低模）、Tripo-ImageToSplat（Gaussian Splatting）、Tripo-Segmentation/Retopology/Texture/AutoRig（全链路后处理） |
| **计费方式** | 按**成功生成的图片张数**计费（`n`值）；失败请求（参数错误、鉴权失败）不计费 | 按**任务成功提交**即计费（无论后续是否检测失败或生成失败）；部分模型（如`videoretalk`）有并发/速率限制 | 按**任务成功提交**即计费；高级参数（如`face_limit>50k`、`texture_quality=extreme`、`quad=true`、`out_format=fbx`）触发阶梯计费 |
| **典型场景** | UI原型图生成、营销海报设计、AIGC插画创作、图像局部编辑（换背景/修瑕疵）、风格迁移预览 | 短视频创意生成、数字人播报、产品动态演示、口型同步广告、动作迁移教学视频、特效模板化视频生产 | 游戏资产快速建模、电商3D商品展示、AR/VR场景构建、工业零件逆向建模、动画角色绑定与重拓扑、实时渲染Splatting应用 |

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、即时反馈」场景  
- **适用**：前端UI组件占位图生成、运营活动海报批量产出、设计师灵感草图辅助、电商主图AI优化（背景替换/光影增强）、教育类插图自动化。  
- **慎用**：需严格保持多帧一致性（如连贯角色动作）、对几何精度/物理属性有硬性要求（如CAD建模）、需直接嵌入3D引擎管线。  
- **关键提示**：Z-Image适合低延迟预览（如Figma插件），WanX适合中文语义强依赖任务，Kling是图生图首选；所有模型均不支持文件URL直传，务必base64编码。

### ✅ 视频生成 —— 推荐用于「动态表达、叙事驱动、多模态协同」场景  
- **适用**：短视频平台内容工厂、企业数字人客服/培训视频、教育动画制作、广告创意脚本可视化、虚拟直播背景生成、AI口播视频合成。  
- **慎用**：超长视频（>30秒）、毫秒级实时生成（如游戏内实时视频流）、超高精度物理仿真（如流体动力学）。  
- **关键提示**：务必校验地域一致性（Workspace ID + region + API Key）；万相2.7+与旧版协议不兼容，升级需重构；HappyHorse在运动自然度上表现突出，PixVerse在创意控制（如口型/动作）上更灵活。

### ✅ 3D生成 —— 推荐用于「空间建模、工业级精度、引擎集成」场景  
- **适用**：游戏开发中的道具/场景快速建模、电商平台3D商品展示（支持WebGL/AR查看）、制造业零部件逆向建模、建筑可视化、动画工作室角色绑定与重拓扑、实时渲染项目Splatting资产生成。  
- **慎用**：纯2D平面设计、无需三维空间信息的简单图形、对生成速度要求极高的实时交互（如Web端即时建模）。  
- **关键提示**：**仅限华北2（北京）地域**，不可绕过；H3.1适合高精度需求（面数上限200万），P1.0适合快速迭代（面数上限2万）；后处理任务（如贴图、绑定）必须引用同一账号的前序`task_id`。

## 开发者技术选型参考

| 选型目标 | 推荐方案 | 理由与注意事项 |
|----------|----------|----------------|
| **追求最低接入成本与最快上线** | 图像生成（WanX 或 Z-Image） | 单一同步端点、无地域强约束、无需轮询逻辑；Z-Image延迟<800ms，适合交互式应用；WanX中文提示词理解最优。 |
| **需生成带时间维度的动态内容** | 视频生成（WanX 3.0 或 HappyHorse） | WanX 3.0支持文/图/参考三模式统一调用，降低多模型管理复杂度；HappyHorse在物理运动保真度上更优，适合产品演示类视频。 |
| **需交付可导入Unity/Unreal/Blender的3D资产** | 3D生成（Tripo-H3.1 + Tripo-ConvertFormat + Tripo-Texture） | H3.1生成高精度网格，`ConvertFormat`支持FBX/GLTF导出并烘焙，`Texture`生成PBR贴图；注意`quad=true`强制四边面且仅FBX有效。 |
| **需从单张图片生成实时渲染友好资产** | 3D生成（Tripo-ImageToSplat） | 直接输出`.splat`文件，体积小、加载快，天然适配Three.js/Spectacle等Splatting渲染器；比网格生成更快，但不可编辑拓扑。 |
| **需在现有图像上做精细化编辑（非重绘）** | 图像生成（Creative Tools：inpainting/outpainting） | 利用`mask`精准控制修改区域，支持扩展画布（outpainting）和局部重绘（inpainting），是PS工作流的理想AI替代。 |
| **需构建端到端3D动画管线** | 3D生成（Tripo-RigCheck → Tripo-AutoRig → Tripo-AnimationRetarget） | 三步流程覆盖检测→绑定→重定向，支持人形与非人形；注意`AutoRig`的`spec`参数决定骨骼规范（如`"mixamo"`不兼容后续重定向）。 |

> **重要提醒**：  
> - 所有生成服务均需遵守中国法律法规，禁止生成违法、暴力、色情、侵权内容；违规调用将触发实时拦截并计入风控指标。  
> - 临时资源URL（图片/视频/3D文件）均为OSS直链，**有效期严格受限**（图像1小时，视频/3D为24小时），生产环境务必及时下载并持久化存储。  
> - 模型能力持续演进，新版本可能引入参数变更或废弃旧模型（如已下线的`Tongyi-Illustration`），请定期查阅各模型文档更新日志。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


