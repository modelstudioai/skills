# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在[多模态](../concepts/multimodal.md)生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与3D生成（3D Generation）三大核心能力。对比聚焦于**工程接入可行性、模型能力覆盖度、资源约束条件及业务适配性**，旨在为技术选型提供客观、可落地的决策依据。所有信息均基于2024年Q3平台最新文档（含千问图像3.0、万相2.7/3.0、可灵V3、HappyHorse、Tripo-H3.1等主力模型），不包含已归档或明确标注为“legacy”的旧版能力。

## 关键维度对比

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | 文本（[prompt](../guides/prompt.md)）、单图URL、多图URL（部分模型支持分镜参考）、Base64（仅千问3.0同步调用） | 文本（[prompt](../guides/prompt.md)）、单图URL（首帧）、双图URL（首尾帧）、多图/视频URL（参考生视频）、音频URL（数字人驱动） | 文本（[prompt](../guides/prompt.md)）、单图URL、**固定4视角图数组**（前/左/后/右，允许空占位） |
| **输出格式** | PNG/JPEG（主流）、WEBP/BMP（部分支持）；支持扩图、擦除补全等中间结果 | MP4（H.264编码，720P/1080P/4K可选）；部分模型返回预览帧序列或关键帧缩略图 | GLB（PBR材质+几何体）、GLB（无贴图基础网格）、PNG预览图；支持 `ultra` 级面数（200万）与 `detailed` 贴图 |
| **支持模型（主力）** | `qwen-image-3.0-pro`, `wan2.7-image-pro`, `kling/kling-v3-omni-image-generation`, `vidu/vidu-image-pro_reference2image`, `z-image-turbo` | `happyhorse-t2v`, `wan3`, `pixverse/pixverse-v6-t2v`, `emo-v1`, `liveportrait-v1`, `wan2.2-s2v` | `Tripo/Tripo-H3.1`（高精度）、`Tripo/Tripo-P1.0`（快速） |
| **API端点路径** | `/api/v1/services/aigc/multimodal-generation/generation`（万相2.7）<br>`/api/v1/services/aigc/text2image/image-synthesis`（万相V2）<br>`/api/v1/services/aigc/image-generation/image-synthesis`（千问3.0） | `/api/v1/services/aigc/video-generation/video-synthesis`（主流）<br>`/api/v1/services/aigc/image2video/video-synthesis`（人像驱动类专用） | `/api/v1/services/aigc/video-generation/3d-generation`（注意：路径含 `video-generation`，属历史命名，实际为3D服务） |
| **调用模式** | **混合模式**：<br>• 同步：千问3.0（≤30s）<br>• 异步：其余全部（含万相2.7、可灵、Vidu、创意工具） | **强制异步**：<br>两步流程（创建任务 + 轮询），典型耗时1–5分钟；**必须携带 `X-DashScope-Async: enable`** | **强制异步**：<br>两步流程（创建任务 + 轮询），典型耗时2–10分钟；**必须携带 `X-DashScope-Async: enable`** |
| **地域支持** | 华北2（北京）、新加坡、美东（弗吉尼亚）等多地部署；模型与Key需严格同地域 | 华北2（北京）、新加坡、美东（弗吉尼亚）等多地部署；模型与Key需严格同地域 | **仅华北2（北京）**；其他地域调用直接失败 |
| **计费方式** | 按生成张数计费（如 `wan2.7-image-pro`：1张=1次调用）；多数模型提供90天内400–500张免费额度 | 按任务成功次数计费（无论生成时长或分辨率）；人像驱动类模型（EMO/LivePortrait）需额外支付检测费用 | 按任务成功次数计费；`Tripo-H3.1`（ultra级）单价高于 `Tripo-P1.0`；无公开免费额度说明 |
| **典型场景** | 电商主图生成、营销海报设计、AI写真、文字特效、背景替换、图像修复与扩图 | 短视频内容创作、产品动态演示、数字人直播、广告片分镜动画、口型同步视频生成 | 工业零部件建模、游戏资产生成、AR/VR内容开发、电商360°商品展示、建筑可视化 |

## 各方案适用场景建议

- **选择图像生成，当您需要**：  
  ✅ 快速产出静态视觉素材（如日更海报、A/B测试图）；  
  ✅ 对响应延迟敏感（可选用千问3.0同步接口，≤30s）；  
  ✅ 需要精细编辑控制（擦除补全、风格重绘、文字变形等垂直工具链）；  
  ❌ 不适合生成连续运动、时间维度表达或三维空间结构需求。

- **选择视频生成，当您需要**：  
  ✅ 构建动态叙事内容（如短视频脚本→成片、产品功能演示）；  
  ✅ 驱动数字人进行实时/准实时交互（需配合音频输入与检测API）；  
  ✅ 基于现有图像/视频进行风格迁移或动作复现（参考生视频）；  
  ❌ 不适合对首帧到末帧的物理一致性有严苛要求（如精确机械运动模拟）；  
  ❌ 不适合跨地域低延迟集成（因强制异步+轮询，且无同步替代方案）。

- **选择3D生成，当您需要**：  
  ✅ 从文本或图像快速构建可交付的3D资产（GLB格式，支持PBR渲染）；  
  ✅ 进入AR/VR、游戏引擎或工业仿真工作流（原生兼容标准WebGL/GLTF生态）；  
  ✅ 在可控成本下获得中高精度模型（`Tripo-H3.1`支持200万面，满足多数非影视级需求）；  
  ❌ 不适合需要多视角自由旋转但无真实几何结构的“伪3D”效果（如2.5D视差图）；  
  ❌ 不适合非北京地域部署的业务系统（无异地冗余或灾备选项）。

## 面向开发者的技术选型参考

1. **优先验证地域与密钥一致性**：  
   - 图像/视频：检查模型文档中标注的支持地域，确保 `API Key`、`Workspace ID`、`Endpoint URL` 三者地域完全一致；  
   - 3D：**直接限定为华北2（北京）**，无需多地域评估。

2. **根据延迟要求选择调用模式**：  
   - 若需 <30s 内返回结果 → 仅考虑 `qwen-image-3.0-pro` 同步调用；  
   - 若接受 1–5 分钟等待 → 视频/3D 全量可用，图像中万相2.7/可灵/Vidu也适用；  
   - 避免在视频/3D场景尝试同步调用（必报错 `"current user api does not support synchronous calls"`）。

3. **输入准备需严格遵循互斥规则**：  
   - 图像：`prompt` 与 `image_url` 可共存（图生图），但不可同时缺失；  
   - 视频：`prompt` 与 `img_url` / `first_frame_url` 等互斥，按任务类型二选一；  
   - 3D：`input.prompt`、`input.image`、`input.images` **三者严格互斥**，同时传入将直接拒绝请求（不排队）。

4. **生产环境模型选型建议**：  
   - 图像：首选 `wan2.7-image-pro`（4K+高稳定性）或 `qwen-image-3.0-pro`（强编辑能力）；避免 `wanx-v1` 等 legacy 模型；  
   - 视频：创意类选 `pixverse-v6-t2v`，物理真实感选 `happyhorse-t2v`，人像驱动选 `emo-v1`（需先检测）；  
   - 3D：时效优先选 `Tripo-P1.0`，精度优先选 `Tripo-H3.1`（注意 `geometry_quality: ultra` 需显式指定）。

5. **错误处理与可观测性**：  
   - 所有[异步任务](../concepts/asynchronous-task.md)均需实现健壮轮询逻辑（建议指数退避+超时中断）；  
   - 视频/3D任务ID有效期为24小时，结果URL有效期仅2小时，务必及时下载；  
   - 使用[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)替代高频轮询（尤其3D查询限流20 RPS）。

> **最后提醒**：本文对比基于当前平台能力。新模型（如即将发布的 `qwen-video-1.0` 或 `Tripo-S2.0`）上线后，请以控制台模型市场及对应API参考文档为准，定期更新SDK与调用逻辑。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


