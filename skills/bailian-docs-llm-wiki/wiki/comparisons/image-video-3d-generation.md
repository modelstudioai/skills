# 图像、视频与 3D 内容生成能力对比

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术边界与工程适配特性，本文系统对比图像（Image）、视频（Video）与 3D 内容生成三大能力模块。对比聚焦于**实际集成所需的工程要素**——包括输入/输出规范、调用范式、模型生态、计费逻辑及部署约束，旨在支撑技术选型决策，避免因协议不一致、地域错配或生命周期误判导致的线上故障。

---

## 关键维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D 生成（3D） |
|------|-------------------|-------------------|----------------|
| **核心输入格式** | 文本（`prompt`）<br>可选：单图/多图 URL 或 Base64（图生图/编辑）<br>支持局部区域坐标（`mask`）、涂鸦草图等结构化输入 | 文本（`prompt`）<br>可选：首帧图（`image_url`）、首尾帧图、参考视频（`video_url`）、音频（`audio_url`）、多模态数组（如 PixVerse 动作模仿）<br>部分模型需人脸检测前置（如 `wan2.2-s2v-detect`） | 文本（`text`，≤200 字符）<br>**或** 单张参考图（`image_url`，JPEG/PNG，建议 ≥512×512，1:1 宽高比）<br>二者可共存，但不可同时为空 |
| **核心输出格式** | PNG/JPEG（带透明通道可选）<br>支持 `1K`/`2K`/`4K` 或自定义宽高（如 `"1024*1024"`）<br>批量生成（`n=1–9`） | MP4（H.264 编码）<br>分辨率：`480P`/`720P`/`1080P`/`4K`（依模型而定）<br>时长：通常 2–8 秒（Vidu/Kling ≤15 秒）<br>仅返回直链 URL（有效期 24 小时） | `.glb`（GL Transmission Format）<br>拓扑简化（默认 5k–50k 面片）<br>含 SHA256 校验值（`file_hash`）<br>直链 URL（有效期 24 小时） |
| **主流支持模型** | • 千问系列：`qwen-image-3.0-pro`（双模态+透明通道）<br>• 万相系列：`wan2.7-image-pro`（4K 输出）、`wan2.6-t2i`<br>• 可灵/Vidu：`kling/kling-v3-omni-image-generation`（分镜组图）、`vidu/viduq3.1-fast_reference2image`（精准画幅）<br>• 轻量/专用：`z-image-turbo`、`facechain-finetune` | • 万相：`wan2.7-text2video`（推荐）、`wan3.0`（All-in-One）<br>• HappyHorse：物理真实感强<br>• PixVerse：高速运动/特效表现优<br>• 可灵/Vidu：4K+官方主体库+广告运镜<br>• 垂直模型：`VideoRetalk`（口型）、`wan2.2-s2v`（数字人） | • **Tripo（唯一支持）**<br>• 仅提供 text-to-3D 与 image-to-3D 两种模式<br>• 不支持点云、网格编辑、多视角重建等高级 3D 操作 |
| **API 端点路径** | 多路径：<br>• 文生图：`/api/v1/services/aigc/text2image/image-synthesis`<br>• 图生图/编辑：`/api/v1/services/aigc/image2image/image-synthesis`<br>• 万相 2.6+/2.7：`/api/v1/services/aigc/multimodal-generation/generation` | **统一路径**：<br>`/api/v1/services/aigc/video-generation/video-synthesis`<br>（注：数字人等少数模型使用 `/api/v1/services/aigc/image2video/...`，需单独确认） | **统一路径**：<br>`/v1/3d/generation`（创建任务）<br>`/v1/3d/generation/{task_id}`（轮询状态） |
| **调用范式** | **混合范式**：<br>• 同步：`qwen-image-*`、`z-image-turbo`、`wan2.6/2.7-image`（秒级响应）<br>• 异步：`kling/*`、`vidu/*`、`wan2.5-*`、创意工具类（需轮询 `GET /tasks/{task_id}`）<br>• OpenAI 兼容：`qwen-image-3.0-pro` 支持 `/v1/images/generations` | **强制异步**：<br>所有模型均需两步：<br>1. `POST /video-synthesis` → 获取 `task_id`<br>2. 轮询 `GET /tasks/{task_id}`（间隔 ≥3 秒）<br>**必须携带请求头 `X-DashScope-Async: enable`** | **强制异步**：<br>1. `POST /v1/3d/generation` → 获取 `task_id`<br>2. 轮询 `GET /v1/3d/generation/{task_id}`（间隔 ≥2 秒，最多 50 次）<br>支持可选 `callback_url`（需公网可达且返回 2xx） |
| **计费方式** | • 按**调用次数**（如 `qwen-image-3.0-pro`）<br>• 按**输出分辨率档位**（如 `wan2.7-image-pro` 的 4K 档位溢价）<br>• 免费体验模型（如 `wanx-style-repaint-v1`）额度用尽即停用，**不可续费** | • 按**视频时长（秒）**（如 `VideoRetalk` 0.08 元/秒）<br>• 按**任务数**（如 `wan2.7-text2video`）<br>• 部分模型提供免费额度（如数字人检测）<br>• **人脸相关模型即使检测失败也计费**（如 `wan2.2-s2v-detect`） | • 按**任务数**计费<br>• 无分辨率/精度档位区分（默认简化拓扑）<br>• 高精度 GLB（>50k 面片）属灰度功能，需白名单开通，不公开计费策略 |
| **典型场景** | • 创意海报、电商主图、营销素材批量生成<br>• 人像写真风格化（FaceChain LoRA 微调）<br>• 局部重绘（商品换背景/去水印）<br>• 分镜草图→高清图（Kling 多图参考） | • 短视频广告脚本可视化（文生视频）<br>• 产品演示动画（图生视频+运镜）<br>• 数字人口播（视频口型替换 + 动作模仿）<br>• 游戏特效生成（PixVerse 法术/爆炸） | • 游戏原型资产快速建模（如道具、场景小物件）<br>• AR/VR 应用中的轻量化 3D 内容填充<br>• 工业设计概念验证（从草图生成基础 mesh） |

---

## 各方案适用场景建议

| 场景需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| **需要毫秒级响应、低延迟预览**（如设计工具实时渲染） | ✅ 图像生成（同步模型）<br>• `qwen-image-3.0-pro`<br>• `z-image-turbo` | 同步调用无需轮询，适合前端直连；`z-image-turbo` 专为速度优化，适用于草稿生成。 |
| **需生成动态叙事内容，强调时间连续性与动作逻辑** | ✅ 视频生成<br>• `wan2.7-text2video`（通用首选）<br>• `HappyHorse`（物理真实感优先）<br>• `PixVerse`（强动态/特效） | 视频模型原生建模时序关系；万相 2.7 协议成熟、文档完善、错误反馈明确，新项目应优先选用。 |
| **需构建可交互、可导入引擎的三维资产** | ✅ 3D 生成（Tripo） | 当前唯一官方支持的 3D 生成能力，输出标准 GLB 格式，开箱即用于 Three.js、Unity、Unreal 等；适合非专业建模团队快速获取基础几何体。 |
| **需高保真、工业化级输出（4K+运镜+主体库）** | ✅ 视频生成（Vidu/Kling）<br>✅ 图像生成（Vidu/Kling 图像模型） | Vidu 与 Kling 在图像/视频双领域均提供 4K 输出、官方主体 ID 调用、广告级运镜模板，是品牌级内容生产的首选栈。 |
| **需人脸专属内容（写真/数字人）** | ⚠️ **组合方案**<br>• 图像：`facechain-finetune`（训练 LoRA）→ 批量生成写真<br>• 视频：`wan2.2-s2v`（数字人） + `VideoRetalk`（口型） | FaceChain 解决“个性化人脸生成”，数字人模型解决“人格化表达”；二者需配合使用，且均需严格人脸合规检测。 |
| **需低成本试错或原型验证** | ✅ 图像生成（免费体验模型）<br>• `wanx-style-repaint-v1`（人像重绘）<br>• `shoemodel-v1`（鞋靴模特） | 提供有限额度免费调用，适合 UI/UX 快速验证创意；但**务必设计降级路径**（如自动切换至 `qwen-image-3.0`），避免额度耗尽后服务中断。 |

---

## 开发者技术选型参考

1. **优先校验地域一致性**  
   所有三类能力均**强制要求 API Key、Workspace ID、Endpoint 三者同地域**（北京/新加坡/弗吉尼亚）。跨地域调用 100% 失败，且错误信息模糊（常报 “Unauthorized” 或 “Invalid endpoint”）。建议在初始化 SDK 时显式校验 `region` 参数，并在 CI/CD 中加入地域配置检查。

2. **异步任务管理是视频/3D 的必修课**  
   视频与 3D 全量异步，需自行实现健壮轮询逻辑：  
   - 设置合理超时（视频任务建议 ≤120 秒，3D 任务 ≤180 秒）  
   - 实现指数退避（如 3s → 6s → 12s）避免高频请求  
   - 记录 `task_id` 与业务上下文映射，便于问题追溯  

3. **模型生命周期管理不可忽视**  
   - 图像领域存在大量“免费体验模型”（如 `wanx-*` 工具类），**额度用尽即永久不可用**，且不支持续费。生产环境应避免依赖此类模型。  
   - 视频领域旧版模型（`wan2.1–2.6`）已归档，新项目必须选用 `wan2.7` 或 `wan3.0`。  
   - 3D 领域当前仅 Tripo，暂无替代选项，需接受其精度与输入限制。

4. **输入合规性是安全底线**  
   - 图像/视频中涉及人脸，必须调用前置检测接口（如 `wan2.2-s2v-detect`），否则任务失败且可能计费。  
   - 3D 输入禁止人脸、证件、版权资产，违规将直接失败，无补偿机制。

5. **输出交付链路需端到端验证**  
   - 图像：校验 `watermark` 参数是否生效，确认透明通道（PNG）或 Alpha 通道（WebP）可用性。  
   - 视频：下载 MP4 后验证关键帧、音频同步、编码兼容性（尤其移动端 H.264 baseline profile）。  
   - 3D：下载 GLB 后用 [glTF Validator](https://github.com/KhronosGroup/glTF-Validator) 校验格式，并加载至 Three.js 查看渲染效果与面片数。

> **最后建议**：对于复合需求（如“将生成的图像作为视频首帧”），务必通过 `model` 字段精确指定跨模态模型（如 `kling/kling-v3-omni-image-generation` → `kling/kling-v4-omni-reference-video-generation`），避免因模型语义

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


