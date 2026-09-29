# 图像、视频与3D生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像生成、视频生成与3D生成三大核心AIGC能力。对比基于当前（2024年Q2）正式发布的API能力，聚焦**可用性、接入复杂度、模型生态、工程约束与业务适配性**，旨在为产品设计、技术选型与架构决策提供客观、可落地的参考依据。

| 维度 | 图像生成 | 视频生成 | 3D生成 |
|------|----------|----------|--------|
| **输入格式** | 文本（`prompt`）、单图URL/Base64（文生图/图生图）、多图（分镜组图）、局部掩码（编辑类）；支持中英文混合提示词 | 文本（`prompt`）、单图/首帧/首尾帧URL、参考视频/音频URL、人物图片+音频（数字人）；部分模型支持图文混排输入 | **三者互斥**：<br>• 文本（`input.prompt`，≤1024字符）<br>• 单图URL（JPEG/PNG，20–6000px，≤20MB）<br>• 多图URL数组（固定4元素，有效图2–4张，按「前/左/后/右」顺序） |
| **输出格式** | PNG/JPEG/WEBP 格式图像（URL下载，有效期24小时）；部分工具返回Base64或结构化JSON（如分割掩码） | MP4格式视频（URL下载，有效期24小时）；数字人等模型额外返回音频同步元数据、关键帧序列；无原始帧流式返回 | GLB格式三维模型：<br>• `pbr_model_url`（含PBR材质与贴图，推荐）<br>• `base_model_url`（纯几何，需显式禁用贴图与PBR）<br>• `rendered_image_url`（WebP预览图）<br>**所有URL有效期均为2小时** |
| **主流支持模型** | • 通用：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`、`vidu/viduq2-pro_reference2image`<br>• 垂直：`facechain-generation`、`aitryon-plus`、`wanx-poster-generation-v1`、`wordart-semantic` | • 通用视频：`happyhorse-t2v`、`wan3-video-generation`、`pixverse/pixverse-v6-t2v`<br>• 数字人：`emo-v1`、`liveportrait`、`wan2.2-s2v`、`animateanyone`<br>• 风格/编辑：`video-style-transform`、`wan2.7-video-edit` | • `Tripo/Tripo-H3.1`（高精度，≤200万面，支持`geometry_quality=ultra`）<br>• `Tripo/Tripo-P1.0`（快响应，≤2万面） |
| **API端点与调用模式** | • **混合模式**：<br>  - 同步：`qwen-image-3.0`、`z-image-turbo` 等轻量模型（<30s）<br>  - 异步：`wan2.7-image-pro`、`kling`、`vidu` 及所有创意工具（需轮询）<br>• Endpoint：必须与API Key同地域（北京/新加坡/弗吉尼亚），推荐业务空间专属域名 | • **强制异步**：<br>  所有模型均仅支持异步调用（`X-DashScope-Async: enable`）<br>• Endpoint：支持多地域（北京/新加坡/弗吉尼亚等），需严格匹配API Key地域 | • **强制异步**：<br>  仅支持华北2（北京）地域，Endpoint与API Key必须同属北京<br>• 固定路径：`/api/v1/services/aigc/video-generation/3d-generation`（注意路径含`video-generation`，属历史命名惯例） |
| **计费方式** | • 按生成张数计费（如1张=1 Token）<br>• 免费额度：主账号+RAM子账号共享90天500张（多数模型）<br>• 特殊限制：`wanx-x-painting`等限时免费模型无付费通道，额度用尽即停用 | • 按生成视频秒数或任务次数计费（依模型而异，如HappyHorse按秒、PixVerse按任务）<br>• 免费额度：各模型独立配置，通常为90天内若干次任务（如万相3.0视频生成赠50次）<br>• 数字人模型（EMO/LivePortrait）按音频时长+分辨率阶梯计费 | • 按任务次数计费（1次请求=1 Token）<br>• 免费额度：Tripo系列统一提供90天100次任务<br>• **无按面数/分辨率阶梯计费**；`H3.1`与`P1.0`单价相同，精度差异不额外加价 |
| **典型场景** | • 营销素材：海报、Banner、电商主图<br>• 内容创作：插画、概念图、AI写真、风格迁移<br>• 工业辅助：UI像素级还原、图表生成、背景补全、试衣效果渲染 | • 短视频内容：文/图生短视频、营销广告片<br>• 数字人应用：客服播报、课程讲解、虚拟主播<br>• 影视辅助：动作模仿、口型同步、风格化重绘、视频续写 | • 快速建模：产品原型、游戏资产、AR/VR场景构件<br>• 电商展示：商品3D看图、旋转展示页<br>• 设计协同：从草图/照片一键生成可编辑GLB模型供Blender/Unity导入 |

## 各方案适用场景建议

- **选图像生成，当您需要**：  
  ✅ 高频、低延迟交付静态视觉内容（如日更海报、千人千面营销图）；  
  ✅ 对像素级细节、文字渲染、构图逻辑有强要求（Vidu/Qwen-Image 3.0 Pro优势显著）；  
  ❌ 不适合需时间维度表达的场景（如动作、过渡、叙事）。

- **选视频生成，当您需要**：  
  ✅ 构建动态人机交互界面（数字人客服、虚拟讲师）；  
  ✅ 将静态创意转化为短视频内容（营销号、信息流广告）；  
  ✅ 实现专业级视频处理（对口型、动作迁移、风格转换）；  
  ❌ 不适合超低延迟场景（所有模型异步，平均耗时1–3分钟）；  
  ❌ 避免跨地域混用——尤其数字人模型对音频采样率、唇形驱动精度敏感，务必验证地域一致性。

- **选3D生成，当您需要**：  
  ✅ 快速将文本/草图/实物照片转化为可交付GLB模型（无需建模师介入）；  
  ✅ 构建轻量级3D电商页面、AR试穿底层资产、教育可视化模型；  
  ✅ 对模型面数有明确分级需求（`P1.0`用于实时渲染，`H3.1`用于离线渲染/打印）；  
  ❌ **不可用于**：需要物理仿真、骨骼绑定、动画序列导出的场景（当前Tripo不输出FBX/USDZ或动画数据）；  
  ❌ **地域锁定严格**：仅北京地域可用，海外业务需代理或等待地域扩展。

## 面向开发者的技术选型参考

1. **优先验证地域与Endpoint匹配性**：  
   - 图像/视频：确认API Key、Endpoint、代码中`region`参数三者同属北京/新加坡/弗吉尼亚；  
   - 3D：**硬性要求北京地域**，其他地域Endpoint调用必失败，且错误码不友好（常报`InvalidApiKey`而非明确地域错误）。

2. **异步任务治理是共性挑战**：  
   - 三者均需实现健壮的轮询机制（建议指数退避+最大重试次数）；  
   - 视频与3D生成结果URL有效期短（2–24小时），**务必在轮询成功后立即下载并持久化存储**；  
   - 图像生成中部分模型（如`wanx-x-painting`）无付费通道，上线前须检查模型状态，避免因免费额度耗尽导致服务中断。

3. **输入校验策略差异化**：  
   - 图像：URL需公网可达、无中文路径、格式合规（PNG/JPEG/WEBP）；FaceChain等模型对人脸尺寸有硬性要求（≥128×128px）；  
   - 视频：音频需为PCM/WAV/MP3，采样率16kHz–48kHz；首帧图建议≥720p以保障动作识别精度；  
   - 3D：多图输入必须严格4元素数组，空视角填`{}`；单图分辨率下限20px，低于此值直接报错`InvalidParameter`。

4. **模型演进路线建议**：  
   - 图像：弃用万相V1/V2旧模型，统一迁移到`qwen-image-3.0-pro`或`wan2.7-image-pro`；  
   - 视频：新项目首选`wan3-video-generation`（统一协议）或`pixverse-v6-t2v`（高动态质量），避免接入已归档的2.1–2.6系列；  
   - 3D：`Tripo-P1.0`适用于MVP验证与WebGL轻量展示；`Tripo-H3.1`用于需高保真渲染的工业/设计场景，但需预留更长生成时间（平均2–5分钟）。

5. **成本优化提示**：  
   - 图像：使用`z-image-turbo`替代通用模型处理简单文字图，成本降低约40%；  
   - 视频：数字人场景优先选用`liveportrait`（轻量口型同步）而非`emo-v1`（唱演全模态），可节省30%+费用；  
   - 3D：若仅需几何轮廓（无贴图），显式设置`"texture": false, "pbr": false`，避免冗余计算与带宽消耗。

> **最后提醒**：所有能力均依赖DashScope统一鉴权体系。请始终通过[DashScope SDK](https://help.aliyun.com/zh/dashscope/developer-reference/quick-start)接入，避免手动拼接HTTP请求——SDK已内置地域校验、异步重试、Token自动刷新等关键能力，可显著降低集成风险。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


