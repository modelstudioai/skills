# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术边界与工程适配特性，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**实际接入成本、调用范式一致性、资源约束刚性、模型演进趋势及生产就绪度**，旨在支撑技术选型决策——例如：是否应优先采用同步接口降低延迟？是否需为视频任务预置异步轮询逻辑？能否复用同一套地域/认证体系？哪些能力已进入稳定迭代期，哪些仍属实验性服务？

以下对比基于当前（2024年Q2）百炼平台正式发布的 API 文档与控制台能力状态，所有信息均经各模块官方文档交叉验证。

## 关键维度对比表

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|--------|-----------|-------------|------------|
| **输入格式** | 支持文本（`prompt`）、单图（`image_url`/Base64）、多图（Kling/Vidu分镜）、结构化指令（如 FaceChain 人脸坐标）；部分模型支持 OpenAI 兼容 `messages` 格式 | 严格按任务类型区分：<br>• 文生视频：`prompt`（最长5000字符）<br>• 图生视频：`img_url`（首帧）或 `first_frame_url`+`last_frame_url`<br>• 参考生视频：`ref_video_url` 或 `ref_image_urls` 数组<br>• 人像驱动：`image_url` + `audio_url`/TTS 内容<br>• 视频编辑：`video_url` | 三者**互斥**：<br>• 文生3D：`input.prompt`（≤1024字符）<br>• 单图生3D：`input.image`（JPEG/PNG URL，20–6000px）<br>• 多图生3D：`input.images`（固定4元素数组，顺序：前/左/后/右，≥2张有效） |
| **输出格式** | 主流模型统一输出 **PNG**（含千问、万相、Kling、Vidu、Z-Image）；特例：`qwen-mt-image-2.0` 输出 JPG | **MP4**（H.264 编码，720P/1080P/4K 可选），部分模型支持额外返回关键帧 PNG 序列（需参数显式开启） | **GLB**（glTF 2.0 二进制格式）：<br>• `pbr_model_url`：含 PBR 材质与贴图（默认）<br>• `base_model_url`：无贴图基础网格（需 `pbr=false && texture=false`）<br>• `rendered_image_url`：1张 WebP 预览图 |
| **支持模型（主流）** | • 通用：`qwen-image-3.0-pro`, `wan2.7-image-pro`, `z-image-turbo`, `kling-v3-omni-image-generation`, `vidu-image-pro_reference2image`<br>• 专用：`facechain-generation`, `aitryon-plus`, `wordart-semantic` | • 通用：`wan3`, `wan2.7`, `HappyHorse`, `pixverse/pixverse-v6-t2v`<br>• 人像驱动：`emo-v1`, `liveportrait-v1`, `animateanyone-gen2`, `wan2.2-s2v` | • `Tripo/Tripo-H3.1`（高精度，≤200万面）<br>• `Tripo/Tripo-P1.0`（快速，≤2万面） |
| **API 端点** | 多路径共存：<br>• 同步：`/api/v1/services/aigc/image-generation/text-to-image`（如 `qwen-image-3.0`）<br>• 异步：`/api/v1/services/aigc/image-generation/image-editing`（如 FaceChain）<br>• OpenAI 兼容：`/v1/images/generations`（需切换 base_url） | **统一异步端点**：<br>`/api/v1/services/aigc/video-generation/video-synthesis`<br>（旧模型如 `wan2.2-s2v` 使用 `/image2video/`，已不推荐） | **统一异步端点**（仅北京地域）：<br>`/api/v1/services/aigc/video-generation/3d-generation`<br>（注意：路径含 `video-generation`，属历史命名，实际为3D专属） |
| **调用模式** | **混合模式**：<br>• 同步：适用于低延迟场景（如 `z-image-turbo`, `wan2.7-image-pro`），响应含直接图像 URL<br>• 异步：适用于复杂编辑/扩图/试衣等（如 `facechain-generation`, `image-out-painting`），需轮询 `task_id` | **强制异步**：<br>所有模型必须设置 `X-DashScope-Async: enable`，否则报错；流程为 `POST → GET /tasks/{id}`；`task_id` 有效期 24 小时 | **强制异步**：<br>同视频生成，必须设置 `X-DashScope-Async: enable`；`task_id` 有效期 24 小时；结果 URL（GLB/WebP）有效期仅 **2 小时**，需及时下载 |
| **计费方式** | • 按**生成张数**计费（1次请求 `n=4` 计为4次）<br>• 分辨率影响单价（如 `4096*4096` > `1024*1024`）<br>• 垂直工具独立计费（如 FaceChain 按“写真套图”计） | • 按**视频秒数 × 分辨率系数**计费（如 10秒720P = 10单位，10秒4K ≈ 40单位）<br>• 人像驱动类额外收取音频处理费用 | • 按**任务次数**计费（1次请求 = 1次计费）<br>• `geometry_quality=ultra`（H3.1）比 `standard` 费用高约3倍<br>• `pbr=true` 不额外计费，但增加生成耗时 |
| **地域与认证约束** | **强地域隔离**：<br>模型、API Key、Endpoint URL 必须同地域（北京/新加坡/弗吉尼亚等）；跨地域调用直接鉴权失败 | **强地域隔离**：<br>同图像生成，且文档多次强调“北京 Key 无法调用新加坡 endpoint”，错误码明确为 `InvalidAuthentication` | **超严格地域锁定**：<br>**仅支持华北2（北京）地域**；控制台开通、API Key 申请、Endpoint 均必须为北京；其他地域调用返回 `RegionNotSupported` |
| **典型场景** | • 电商主图/详情页生成<br>• UI/图标/海报设计<br>• 人物写真/虚拟形象制作<br>• 创意文字艺术（WordArt）<br>• 商品背景替换（Wanx Background） | • 短视频营销内容（文/图→视频）<br>• 数字人口播/唱演/表情包生成<br>• 产品演示动画（参考生视频）<br>• 视频风格迁移（日漫/赛博朋克） | • 游戏/AR/VR 资源快速建模（概念验证）<br>• 电商360°商品展示模型生成<br>• 工业设计草图转基础3D网格<br>• 教育/科普三维可视化素材 |

## 各方案适用场景建议

- **选择图像生成，当您需要**：  
  ✅ 快速获得高质量静态视觉资产（如 Banner、LOGO、商品图）；  
  ✅ 构建低延迟交互式应用（如设计助手实时预览）；  
  ✅ 复用现有提示词工程或 OpenAI 生态工具链；  
  ❌ 避免用于需物理运动、时间序列或空间深度表达的场景（如动作演示、装配说明）。

- **选择视频生成，当您需要**：  
  ✅ 生成具备时间维度与动态表现力的内容（如广告片、教学演示、数字人播报）；  
  ✅ 复用已有图像/音频资产进行二次创作（图生视频、口型驱动）；  
  ✅ 接受 10–120 秒级生成耗时，并已集成异步任务管理模块；  
  ❌ 避免用于对首帧到末帧精确控制要求极高的专业影视制作（当前模型不支持关键帧编辑）。

- **选择3D生成，当您需要**：  
  ✅ 从文本或单图快速获取可导入 Unity/Unreal/Blender 的基础3D网格（GLB）；  
  ✅ 构建轻量级3D应用原型（如WebAR商品展示、教育模型库）；  
  ✅ 接受北京地域部署限制，且业务对3D精度要求处于中等（H3.1 可满足展示级，非工业CAD级）；  
  ❌ 避免用于需拓扑优化、UV展开、骨骼绑定等专业后期流程的场景；也**不适用于实时3D渲染需求**（生成耗时长，非流式）。

## 面向开发者的选型参考

| 选型关注点 | 推荐方案 | 关键依据 |
|-------------|------------|-----------|
| **最低接入门槛 & 最快上线** | ✅ 图像生成（同步接口） | 支持同步调用，无需实现轮询逻辑；OpenAI 兼容协议可复用现有 SDK；免费额度覆盖初期验证。 |
| **需严格控制生成耗时（<2s）** | ✅ 图像生成（`z-image-turbo` 或 `wan2.7-image-pro` 同步） | 明确标注“轻量级”“低延迟”；实测 P95 响应 <1.5s（1024×1024）；视频/3D 均为异步，无法满足。 |
| **必须支持多地域部署（如全球用户）** | ✅ 图像生成 或 ✅ 视频生成 | 两者均支持北京/新加坡/弗吉尼亚等多地域；**3D生成仅限北京，排除全球化架构选项**。 |
| **需复用同一套认证与域名体系** | ⚠️ 需谨慎规划 | 图像/视频/3D 均要求“Key-Endpoint-模型”地域一致，但**3D的Endpoint路径（`/video-generation/3d-generation`）易被误认为视频子集**，建议在代码中显式注释并封装地域校验逻辑。 |
| **面向生产环境的长期稳定性** | ✅ 图像生成（`qwen-image-3.0-pro` / `wan2.7-image-pro`） > ✅ 视频生成（`wan3` / `wan2.7`） > ⚠️ 3D生成（`Tripo-H3.1`） | 图像模型迭代最成熟（V3.0/V2.7 均为GA版本）；视频模型正快速收敛（2.7/3.0 替代早期2.x）；3D依赖 Tripo 第三方模型，更新节奏与百炼平台解耦，文档未标注 GA 状态。 |
| **需处理敏感内容（如人脸/服饰）** | ✅ 图像生成（FaceChain / AITryOn） | 提供专用检测API（`facechain-facedetect`, `aitryon-parsing-v1`）和合规输入规范；视频/3D 的人像类模型虽有检测要求，但文档分散，工程落地风险更高。 |

> **重要提醒**：所有能力均遵循**地域强隔离原则**。建议在项目初始化阶段即确定目标地域，并在 CI/CD 流程中加入地域一致性校验（如：`workspace_id` 与 `api_key_region` 字符串匹配）。避免因混用导致的静默失败——此类错误通常表现为 `401 Unauthorized` 或 `403 Forbidden`，而非明确的地域错误码。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


