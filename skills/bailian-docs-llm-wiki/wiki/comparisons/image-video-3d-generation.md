# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**工程落地关键维度**，包括调用方式、模型生态、资源约束、计费逻辑及适用场景，旨在为技术选型提供客观、可操作的决策依据。三者虽同属AIGC生成范畴，但在计算范式（同步/异步）、输入复杂度、输出形态、地域依赖性及后处理链路深度上存在本质差异，不可简单类比或替代。

## 能力维度对比表

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | 文本（`prompt`，≤512字符）、可选图片（图生图/局部重绘）、支持分句加权（如`(cat:1.3)`） | 多样化：<br>• 文本（文生视频）<br>• 单图/首帧/首尾帧（URL，400–7000px）<br>• 参考生视频/音频（MP4/WAV等，2–120秒）<br>• 多模态组合（如`media`数组对口型） | 三类主路径：<br>• 文本（`prompt`，≤1024字符）<br>• 单图（JPEG/PNG，≤20MB，20–6000px）<br>• 多图（4视角数组：前/左/后/右）<br>• 已有3D模型（GLB/FBX/OBJ/STL，≤150MB，仅后处理） |
| **输出格式** | 同步返回：<br>• Base64 编码图像（需 `Accept: application/json+base64`）<br>• 或 `url`（有效期1小时，HTTPS可直接下载） | 异步返回：<br>• `output.video_url`（MP4，含水印，有效期24小时）<br>• 部分模型支持 `output.thumbnail_url`（封面图）<br>• 无原始帧序列或中间产物直接暴露 | 异步返回：<br>• `output.model_url`（GLB/FBX/OBJ等，有效期24小时）<br>• `output.splat_url`（`.splat` 文件，仅 `ImageToSplat` 模型）<br>• `output.texture_url`（PBR贴图包ZIP）<br>• 无实时[流式输出](../concepts/streaming-output.md) |
| **主流支持模型** | • WanX（万相）：高保真中文语义<br>• Kling（可灵）：强构图与光影逻辑<br>• Z-Image：轻量低延迟<br>• Vidu（图像模式）：高质量静态帧（白名单）<br>• Qwen-VL系列：图文混合理解 | • WanX（万相）：`wan3.0`（全能）、`wan2.7`（新版协议）、专用子模型（动作迁移/数字人）<br>• HappyHorse：物理真实+运动流畅<br>• PixVerse（爱诗）：动态特效专精（如`c1`系列）<br>• Kling/Vidu：高一致性角色生成与智能运镜 | • Tripo-H3.1：高精度网格（最高200万面）<br>• Tripo-P1.0：快速专业生成（≤2万面）<br>• Tripo-ImageToSplat：单图→Gaussian Splatting<br>• 后处理专用模型：分割（`SmartSegmentation`）、重拓扑（`Retopology v2.0`）、自动绑定（`AutoRig`）、动画重定向（`AnimationRetarget`） |
| **API端点（标准路径）** | `POST https://dashscope.aliyuncs.com/api/v1/images/generations`<br>• 全域通用，无需业务空间域名 | `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`<br>• **强地域绑定**：模型、API Key、Endpoint 必须同地域（如 `cn-beijing`） | `POST https://cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation`<br>• **仅限华北2（北京）**，URL与API Key均强制北京地域 |
| **调用模式** | **同步调用**：请求即响应（通常 <5s），适合低延迟交互场景 | **强制异步**：需 `X-DashScope-Async: enable` header；返回 `task_id` 后轮询 `GET /api/v1/tasks/{task_id}` | **强制异步**：同视频生成，必须携带 `X-DashScope-Async: enable`；轮询机制一致，`task_id` 有效期24小时 |
| **计费方式** | 按「模型 × 分辨率 × 数量」独立计量：<br>• 例：`kling-v1` 生成 `1024x1024×2` = 2单位<br>• `zimage-v1` 同尺寸 = 1单位<br>• 不支持负向提示词的模型（如Z-Image）不计费减免 | 按「模型 × 分辨率 × 时长 × 帧率」综合计费：<br>• `720P@15fps×5s` 与 `1080P@30fps×10s` 成本显著不同<br>• 参考生视频/音频输入不额外计费，但影响生成复杂度 | 按「模型 × 几何精度 × 贴图质量 × 面数上限」阶梯计费：<br>• `Tripo-H3.1` + `geometry_quality=ultra` + `texture_quality=extreme` + `face_limit=2000000` = 高积分消耗<br>• `Tripo-P1.0` 默认配置成本最低<br>• 后处理任务（如重拓扑、贴图）单独计费，不继承原生成任务积分 |
| **典型场景** | • UI/UX设计稿生成<br>• 社媒配图批量制作<br>• 线稿上色、老照片修复<br>• A/B测试多版本视觉方案 | • 短视频创意脚本可视化（文→视频）<br>• 电商商品动态展示（图→视频）<br>• 数字人口型同步（视频+音频）<br>• 影视分镜预演与广告运镜生成 | • 游戏/AR资产快速建模（文/图→3D）<br>• 工业零件逆向重建（多图→3D）<br>• 实时渲染场景构建（图→Splat）<br>• 3D打印前处理（重拓扑+格式转换+贴图烘焙） |

## 各方案适用场景建议

### ✅ 图像生成 —— 优先选择当：
- 需要**毫秒级响应**与**同步阻塞式集成**（如Web应用实时预览、设计工具插件）；
- 任务以**静态视觉表达**为核心，无需时间维度信息（如Banner、海报、图标、概念草图）；
- 对**中文提示词理解深度**和**艺术风格控制**（水墨、国风、赛博朋克）有强需求；
- 资源受限需轻量模型（如Z-Image用于移动端SDK内嵌）；
- 需高频调用且预算敏感（Z-Image单位成本最低，但功能受限）。

### ✅ 视频生成 —— 优先选择当：
- 核心目标是**动态叙事**或**行为表达**（如产品演示、教学动画、虚拟主播口播）；
- 输入具备**时空锚点**：已有首帧图、参考视频片段、或多模态信号（音视频对齐）；
- 需要**跨地域灵活部署**（支持北京、上海、新加坡等多Region，适配全球化业务）；
- 场景强调**物理合理性**（HappyHorse）或**特效表现力**（PixVerse c1系列）；
- 可接受**1–5分钟异步等待**，并具备任务状态管理能力（轮询/回调通知）。

### ✅ 3D生成 —— 优先选择当：
- 输出目标为**可交互、可渲染、可工程化**的3D资产（非仅视觉呈现）；
- 流程需覆盖**生成→分割→优化→绑定→动画**全链路（如游戏NPC开发、工业数字孪生）；
- 输入为**结构化多视角图像**或需从**单图重建几何体**（Tripo-ImageToSplat适用于WebGL实时场景）；
- 严格限定在**华北2（北京）环境**，且已建立对应地域的API密钥与业务空间；
- 对**网格质量、面数控制、PBR材质精度**有明确工程指标（如游戏引擎导入要求≤5万面+4K贴图）。

## 技术选型参考（面向开发者）

| 选型考量 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **追求最快上线 & 最低接入成本** | 图像生成 | 仅需一个全局Endpoint、同步调用、无地域限制、文档最成熟；适合MVP验证与轻量应用。 |
| **需要“所见即所得”的动态内容** | 视频生成（Wan3.0 或 HappyHorse） | 支持首帧控制+物理模拟，生成结果更易预测；专属域名保障稳定性，多Region容灾能力强。 |
| **构建3D资产生产管线** | 3D生成（Tripo-H3.1 + 后处理模型组合） | 唯一提供端到端3D工作流的方案；`generate_parts` + `Retopology v2.0` + `AutoRig` 可支撑专业游戏开发流程。 |
| **中文语义理解与文化元素渲染** | 图像生成（WanX）或 视频生成（Wan3.0） | WanX系列在中文提示词解析、传统美学（山水、工笔、汉服）建模上显著优于其他模型。 |
| **实时性敏感（<1s响应）** | 图像生成（Z-Image） | 唯一明确标注“轻量级实时”的模型，但放弃图生图与负向提示词，需权衡功能完整性。 |
| **需与现有3D工具链集成** | 3D生成（Tripo-ConvertFormat + Tripo-Texture） | 支持FBX/GLB双向转换、PBR贴图烘焙、对称/压平/法线重算等工程化参数，直通Unity/Unreal。 |
| **规避地域锁定风险** | 图像生成 或 视频生成（避开3D） | 3D生成强制北京地域，若业务需多云/混合云部署，应避免将其作为核心依赖。 |

> **重要提醒**：  
> - **不要混用地域凭证**：视频/3D生成中，API Key、Endpoint、模型服务必须严格同Region；跨地域调用将返回鉴权失败或`404 Not Found`。  
> - **警惕历史接口**：视频生成中 `/api/v1/services/aigc/image2video/...` 为Legacy路径，新项目务必使用统一 `/video-generation/video-synthesis`；3D生成无历史路径，但`task_id`过期即失效，不可复用。  
> - **安全策略一致**：三类生成均禁止暴力、色情、政治敏感及可识别真人内容，违规请求计入失败配额且无预警。  
> - **调试建议**：图像生成可先用`size=512x512`快速验证；视频生成建议从`720P@15fps×3s`起步；3D生成务必先用`Tripo-P1.0`测试输入兼容性，再升级至H3.1。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


