# 图像、视频与3D内容生成能力对比

本页旨在为开发者提供百炼平台在**图像生成（Image Generation）、视频生成（Video Generation）与3D内容生成（3D Generation）** 三大模态上的系统性能力对比，帮助技术团队基于业务需求（如响应时效、输入灵活性、输出精度、部署约束、成本结构等）快速完成模型选型与架构决策。对比依据为截至2024年Q2正式发布的API文档与控制台能力说明，覆盖模型能力边界、调用范式、地域限制、计费逻辑及典型落地场景。

---

## 关键维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **核心输入格式** | 文本（prompt）；单图/多图URL或Base64（≤10–14张）；支持参考图+文本混合输入 | 文本（prompt）；单帧/首尾帧图像；参考图/视频/音频混合媒体数组；数字人需`image_url`+`audio_url` | 文本（prompt）；单图（`.jpg/.png/.webp`）；四视角图组（前/左/后/右）；或已有3D模型（`.glb/.gltf/.fbx/.obj/.stl`） |
| **核心输出格式** | PNG/JPEG（带可选水印），分辨率最高支持 `4K`（3840×2160）；部分模型支持语义尺寸（`"2K"`/`"4K"`） | MP4（H.264编码），分辨率支持 `720P`/`1080P`/`4K`；帧率默认15fps（可调）；输出含24小时有效期直链 | 网格：`.glb`/`.fbx`/`.obj`（支持四边面）；Gaussian Splat：`.splat`；贴图：`.png`；动画：`.fbx` + `.json`动作文件；所有资源均通过`task_id`轮询获取直链 |
| **主力支持模型** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling-v3-omni-image-generation`, `vidu-image-pro_reference2image`, `z-image-turbo`, `facechain-finetune` | `wan2.7-t2v`/`wan3.0-t2v`, `happyhorse-t2v`, `pixverse-v6-t2v`, `viduq3-pro_text2video`, `kling-v3-omni-video-generation`, `wan2.2-s2v`（数字人） | `Tripo/Tripo-H3.1`（高精网格）, `Tripo/Tripo-P1.0`（快速网格）, `Tripo/Tripo-ImageToSplat`（高斯泼溅）, `Tripo-AutoRig`, `Tripo-AnimationRetarget` |
| **API端点（统一域名结构）** | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（同步/异步共用） | `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`（强制异步） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`（强制异步，仅北京） |
| **调用模式** | **混合模式**：<br>• 同步：千问系、Z-Image、`wan2.7-image-pro`（文生图）<br>• 异步：万相V1/V2编辑、可灵、Vidu、创意工具类（虚拟模特/海报） | **强制异步**：<br>① `POST /video-synthesis` 创建任务 → 获取 `task_id`<br>② `GET /tasks/{task_id}` 轮询（24小时有效期） | **强制异步**：<br>① `POST /3d-generation` 创建任务 → 获取 `task_id`<br>② `GET /tasks/{task_id}` 轮询（24小时有效期，建议首次延迟10秒，后续15–30秒间隔） |
| **地域支持** | • 千问/Z-Image：华北2（北京）、新加坡<br>• 万相/可灵/Vidu：华北2、新加坡、弗吉尼亚<br>• 创意工具类：仅华北2（北京） | • 全系列模型：华北2（北京）、新加坡、弗吉尼亚<br>• 数字人（wan2.2-s2v）等部分模型：仅华北2（北京） | **仅华北2（北京）**，全链路（生成、后处理、动画）均强绑定该地域，跨地域调用必失败 |
| **计费方式** | • 按**生成张数**（`n`）计费（如 `qwen-image-3.0-pro` 1张=1次调用）<br>• 部分模型按**分辨率档位**加权（如 `4K` 比 `1K` 费用高）<br>• 创意工具类（虚拟模特/海报）为**免费额度制**，用尽即停，不支持付费续订 | • 按**视频秒数**计费（如 VideoRetalk 0.08元/秒）<br>• 或按**任务次数**计费（如 `wan2.7-t2v` 1次任务=1次调用，无论时长）<br>• 高清/高帧率/长时长任务触发阶梯加价 | • 按**任务积分**计费（非固定单价）<br>• 积分消耗受参数显著影响：<br> ✓ `geometry_quality=ultra` / `face_limit=2000000` → 高积分<br> ✓ `texture_quality=extreme` / `quad=true` / `out_format=fbx` → 额外积分<br> ✗ `Tripo-P1.0`（50–20,000面）为性价比首选 |
| **典型场景** | • 电商主图/营销海报生成<br>• UI界面/图表像素级还原（Vidu）<br>• 个性化写真（FaceChain）<br>• 分镜草图批量产出（可灵）<br>• 快速原型图（Z-Image） | • 广告短片/剧集分镜视频化（Vidu/Kling）<br>• 产品动态展示（HappyHorse物理真实感）<br>• 数字人播报（S2V+Audio）<br>• 口型同步视频（VideoRetalk）<br>• 动作迁移/风格重绘（PixVerse） | • 游戏资产快速建模（`Tripo-P1.0` + `face_limit=5000`）<br>• 工业零件扫描重建（多视角图→高精网格）<br>• 实时渲染素材生成（单图→`.splat`）<br>• 3D角色动画管线（AutoRig + AnimationRetarget）<br>• AR/VR内容生产（GLB导出+贴图） |

---

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于「高频、轻量、强可控」的视觉内容生产
- **选千问系（`qwen-image-3.0-pro`）**：当需要**文生图+图生图双模能力统一管理**、支持语义尺寸（`"2K"`）、且对中文提示词理解与构图稳定性要求高时（如电商文案配图、教育插画）。
- **选万相2.7（`wan2.7-image-pro`）**：当需**4K超高清输出**、或进行**局部重绘/涂鸦转图**等精细编辑操作，且接受异步流程时（如设计稿终稿优化）。
- **选Vidu**：当任务涉及**中英文混合文字渲染**（如APP界面截图生成）、**图表/LOGO像素级还原**等专业设计场景。
- **避坑提示**：避免在新项目中使用 `wan2.5-i2i-preview` 等早期模型；创意工具类（`shoemodel-v1`, `wanx-poster-generation-v1`）无付费通道，额度耗尽即失效，应提前规划迁移到千问/万相主模型。

### ✅ 视频生成 —— 推荐用于「中低频、高价值、需时序表达」的内容创作
- **选万相3.0（`wan3.0-t2v`）**：当需**单一接口覆盖全部视频生成模式**（文生/图生/参考生/编辑），降低集成复杂度，适合通用型视频SaaS平台。
- **选HappyHorse**：当强调**物理运动真实性与流畅性**（如机械运转、液体流动、布料模拟），且对首帧到成片的连贯性要求严苛。
- **选PixVerse**：当需**强动态表现力与细分场景优化**（如高速运动用`c1`子模型、口型同步用`retalk`子模型），适合短视频特效工具。
- **避坑提示**：数字人（`wan2.2-s2v`）必须前置调用`face-detect`接口校验人脸质量；所有视频输入媒体（图/视/音）必须为**公网可访问URL**，OSS临时链接需额外添加请求头 `X-DashScope-OssResourceResolve: enable`。

### ✅ 3D生成 —— 推荐用于「专业垂直、长周期、强工程属性」的三维内容构建
- **选`Tripo-P1.0`**：当目标为**游戏/AR快速建模**，需平衡速度（秒级生成）与面数控制（50–20,000三角面），适配Unity/Unreal实时渲染管线。
- **选`Tripo-H3.1`**：当需**工业级精度建模**（≤200万面）、支持四边面拓扑（`quad=true`）、或需后续导入Maya/Blender深度编辑。
- **选`Tripo-ImageToSplat`**：当目标为**Web端实时渲染**（Three.js/Deck.gl）、无需传统DCC工具介入，追求单图→高真实感3D的极简路径。
- **避坑提示**：**全链路仅支持华北2（北京）**，务必确认业务空间、API Key、Endpoint三者地域一致；`generate_parts=true` 与 `texture=true` 等高级参数互斥，错误组合将直接返回400；Gaussian Splat（`.splat`）不兼容传统建模软件，需专用渲染器。

---

## 技术选型参考指南（面向开发者）

| 决策维度 | 推荐行动 |
|----------|----------|
| **✅ 响应时效敏感（<3秒）** | 优先选用**图像同步调用**（千问/Z-Image）；避免视频/3D（强制异步，通常需10–120秒）；若必须生成视频，可预生成热门模板并缓存。 |
| **✅ 输入源受限（仅有单图/无文本）** | 图像：用万相/可灵的图生图能力；视频：用万相2.7/3.0的首帧生视频；3D：用`Tripo-ImageToSplat`或`Tripo-P1.0`（单图模式）。 |
| **✅ 需要多地域部署** | 图像/视频：选择支持**新加坡/弗吉尼亚**的模型（如万相/可灵/Vidu）；3D：**不可跨地域**，需在北京部署独立服务实例。 |
| **✅ 成本敏感型项目** | 图像：用`z-image-turbo`（低价快响应）或`wan2.7-image-pro`（4K性价比高）；视频：选`wan2.7-t2v`（任务计费）而非秒数计费模型；3D：严格控制`face_limit`与`texture_quality`，避免`ultra`/`extreme`档位。 |
| **✅ 需对接现有工作流** | 图像：千问支持OpenAI Images协议，零改造接入；视频/3D：必须适配百炼异步任务轮询范式，建议封装SDK统一处理`task_id`生命周期。 |
| **✅ 合规与水印要求** | 所有图像模型默认添加水印（`watermark=true`），仅`wan2.7-image-pro`等少数支持设为`false`；视频/3D输出无内置水印，需业务层自行叠加。 |

> **最后提醒**：所有能力均需通过[百炼控制台](https://bailian.console.aliyun.com)开通对应地域的服务，并获取匹配的`API Key`与`WorkspaceId`。旧域名 `dashscope.aliyuncs.com` 已不推荐，新项目请务必使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）以保障性能与稳定性。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


