# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像（Image）、视频（Video）与3D内容生成三大核心模态的工程实现特性。对比聚焦于**生产级集成视角**：涵盖输入/输出规范、模型生态、调用机制、计费策略及落地约束，旨在支撑技术选型决策——尤其适用于需构建AIGC工作流的中大型应用（如营销创意平台、数字人引擎、游戏资产管线、电商3D展厅等）。

---

## 关键维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **核心输入格式** | 文本（`prompt`）；单图/多图 URL 或 Base64（`image`, `images`）；支持掩码（`mask_url`）、参考图列表（最多14张）；部分模型支持图文混排（`wan2.6-image`） | 文本（`prompt`）；首帧/首尾帧图片 URL；参考视频/图像集；动作驱动音频（`audio_url`，如 VideoRetalk）；严格要求公网可访问 URL（OSS需加 `X-DashScope-OssResourceResolve: enable`） | 文本（`prompt`）；单图/多图 URL（`image` / `images`，多图固定4视角：前/左/后/右）；或前序任务 `task_id`（后处理/动画链路）；**仅支持 JPEG/PNG/WebP（`ImageToSplat`）** |
| **核心输出格式** | PNG（多数支持透明通道，如 `qwen-image-2.1-pro`）、JPEG；分辨率范围广（512×512 至 4K），宽高比灵活（1:1 / 16:9 / 9:16 等） | MP4（H.264 编码）；分辨率支持 720P / 1080P / 4K；帧率可配（15/30 FPS）；输出为临时 OSS 直链（有效期数小时） | GLB（默认）、FBX（启用 `quad` 时强制）、OBJ、PLY、`.splat`（Gaussian Splatting）；面数可控（`face_limit`：50–200万）；纹理贴图（PNG）、绑定骨架（FBX）、动画文件（FBX） |
| **主力支持模型** | `qwen-image-3.0-pro`（T2I+I2I一体化）、`wan2.7-image-pro`（4K商用）、`kling/kling-v3-omni-image-generation`（多图融合）、`vidu/vidu-image-pro_reference2image`（UI/文字精准还原）、`facechain-finetune`（人脸微调） | `wan2.7-videoedit`（万相2.7全功能）、`pixverse/pixverse-v6-t2v`（动态表现力）、`happyhorse/happyhorse-t2v`（物理真实感）、`kling/kling-v3-omni-video-generation`（ID复用）、`vidu/viduq3-pro_text2video`（广告剧集优化） | `Tripo/Tripo-H3.1`（高精度网格）、`Tripo/Tripo-P1.0`（低面专业模型）、`Tripo/Tripo-ImageToSplat`（单图生成Splat）、`Tripo/Tripo-AutoRig`（自动绑骨）、`Tripo/Tripo-AnimationRetarget`（动画重定向） |
| **API 端点（标准路径）** | `POST /multimodal-generation/generation`（同步）<br>`POST /api/v1/services/aigc/multimodal-generation/generation`（异步） | `POST /api/v1/services/aigc/video-generation/video-synthesis`（统一端点，万相2.7/HappyHorse/PixVerse等均复用） | `POST /api/v1/services/aigc/video-generation/3d-generation`（**注意：路径含 `video-generation`，但实际为3D服务**） |
| **调用模式** | **混合模式**：<br>• 同步：`qwen-image-*`、`wan2.7-image-*`、`z-image-turbo`（毫秒级响应）<br>• 异步：`kling`、`vidu`、`facechain-finetune`、创意工具（返回 `task_id` 轮询） | **强制异步**：<br>所有模型均需 `X-DashScope-Async: enable`；创建任务 → 轮询 `GET /api/v1/tasks/{task_id}`；典型耗时 1–5 分钟 | **强制异步**：<br>必须携带 `X-DashScope-Async: enable`；创建任务 → 轮询 `GET /api/v1/tasks/{task_id}`；典型耗时 2–10 分钟（高面网格/重拓扑更长） |
| **地域与认证约束** | 严格地域隔离：API Key、Endpoint、模型必须同地域（北京/新加坡/弗吉尼亚）；**推荐使用业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`） | 同图像：严格地域一致；跨地域调用直接失败；专属域名性能与稳定性显著优于公共域名 | **仅支持华北2（北京）地域**；API Key 必须为北京地域；其他地域 Key 或 Endpoint 均不可用 |
| **计费方式** | • 按调用次数（`n` 张图）或按 token（部分模型）计费<br>• `qwen-image-*`、`wan2.7-image-pro` 等主流模型支持商用付费<br>• 多个创意工具（如 `wanx-x-painting`、`shoemodel-v1`）**仅限免费体验，额度用尽即停用，不支持付费** | • 按任务计费（1次请求 = 1任务），与视频长度/分辨率/模型复杂度强相关<br>• `wan2.7-videoedit`、`pixverse-v6`、`happyhorse-t2v` 等均开放商用计费<br>• 旧版 `wan2.1–2.6` 已归档，不推荐新项目接入 | • 按任务计费（1次请求 = 1任务）<br>• 所有 Tripo 模型（`H3.1`/`P1.0`/`AutoRig` 等）均支持商用付费<br>• **无免费体验模型**；全部需开通 Tripo 服务并配置北京地域 Key |
| **典型场景** | • 营销海报/电商主图批量生成<br>• UI界面/图表像素级还原（Vidu）<br>• 个性化头像/虚拟模特生成（FaceChain/WanX VirtualModel）<br>• 局部编辑与风格迁移（擦除补全、艺术重绘） | • 短视频广告/社交媒体内容生成（文生/图生）<br>• 数字人播报口型同步（VideoRetalk）<br>• 动作模仿/法术特效生成（PixVerse v6）<br>• 视频超分与风格化重绘 | • 游戏/AR/VR资产快速建模（文生/图生3D）<br>• 电商商品3D展示（单图生成GLB/Splat）<br>• 工业设计原型验证（多视角重建）<br>• 3D动画制作管线（自动绑骨 + 动画重定向） |

---

## 各方案适用场景建议

### ✅ 推荐图像生成（Image）当：
- 需要**毫秒级响应**的轻量级创意生成（如实时海报预览、聊天机器人配图）；
- 对**文字渲染精度、UI像素一致性**有硬性要求（选 `vidu/*_reference2image`）；
- 需基于少量人脸图训练专属形象（`facechain-finetune`）；
- 追求高性价比与快速迭代，且无需视频/3D深度能力。

> ⚠️ 注意：避免在生产环境使用标注“仅免费体验”的模型（如 `wanx-x-painting`, `image-erase-completion`），因其无付费路径且额度耗尽即中断服务。

### ✅ 推荐视频生成（Video）当：
- 构建**短视频内容工厂**（如营销活动自动化剪辑、教育课程片段生成）；
- 需要**物理运动合理性**（HappyHorse）或**高速动态表现力**（PixVerse v6）；
- 实现数字人驱动闭环（文本→语音→口型→动作→视频，依赖 `VideoRetalk` + `wan2.2-s2v`）；
- 支持**参考视频/首尾帧控制**以保障品牌视觉一致性（Vidu/Kling）。

> ⚠️ 注意：务必采用万相2.7或3.0协议（非2.1–2.6旧版），并严格校验地域一致性；对并发敏感场景（如 `VideoRetalk`），需自行实现任务队列管理。

### ✅ 推荐3D生成（3D）当：
- 构建**3D资产自动化管线**（如电商商品从2D图→3D模型→绑定→动画）；
- 需要**高保真网格输出**（`Tripo-H3.1`，200万面）或**轻量化交付**（`Tripo-P1.0`，≤2万面）；
- 支持**实时渲染场景**（单图生成 `.splat` 文件，用于WebGL/Unreal Engine）；
- 具备明确的**北京地域部署条件**（所有3D服务仅限华北2）。

> ⚠️ 注意：多图生3D必须提供4视角图（前必填，其余至少1张）；后处理链路（如 `AutoRig` → `AnimationRetarget`）存在兼容性限制（如 `spec=mixamo` 不支持），需严格按文档参数组合调用。

---

## 技术选型参考（面向开发者）

| 选型目标 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **最低延迟、最高吞吐** | `qwen-image-3.0-pro`（同步） | 支持 T2I/I2I 一体化、10图参考、透明通道输出；毫秒级响应；OpenAI 兼容模式便于迁移 |
| **商业级4K图像生产** | `wan2.7-image-pro` | 明确支持 4K 输出、`watermark=false` 关闭水印、`thinking_mode=true` 辅助调试；稳定商用计费 |
| **短视频内容工业化** | `wan2.7-videoedit`（万相2.7） | 全功能统一接口（文生/图生/编辑/换人）、协议成熟、文档完善、地域支持广（北京/新加坡/弗吉尼亚） |
| **高动态/特效类视频** | `pixverse/pixverse-v6-t2v` | 专为打斗、法术等高速场景优化；可控性强；支持精细风格索引（`style` 参数） |
| **端到端3D资产生成** | `Tripo/Tripo-H3.1` + `Tripo/Tripo-AutoRig` + `Tripo/Tripo-AnimationRetarget` | 高精度建模→自动绑骨→动画重定向完整链路；面数/格式/纹理全可控；北京地域内闭环稳定 |
| **轻量3D实时渲染** | `Tripo/Tripo-ImageToSplat` | 单图输入直接生成 `.splat`，适配 WebGL/Three.js，加载快、渲染效率高，适合网页3D展厅 |

> 💡 **集成提示**：  
> - 所有模态均**强烈推荐使用业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com`），避免公共域名性能波动；  
> - 异步任务务必实现健壮轮询逻辑（指数退避 + 超时熔断），`task_id` 有效期统一为 **24 小时**；  
> - 输入媒体文件（图/视/音）**必须为公网可访问 URL**；本地文件请先调用 [上传获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md) 接口；  
> - 多模态协同场景（如图→视频→3D），需自行维护 `task_id` 依赖关系与状态机，平台不提供跨模态任务编排能力。

---  
*最后更新：2024年6月*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


