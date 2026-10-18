# 图像生成与视频生成对比

本页旨在为开发者提供图像生成（Image Generation）与视频生成（Video Generation）两大核心[多模态](../concepts/multi-modal.md)能力的系统性对比，帮助技术团队在产品设计、模型选型、架构集成及成本规划阶段做出更精准的决策。随着 AIGC 应用从静态内容向动态表达演进，理解二者在协议设计、计算范式、资源消耗与工程约束上的本质差异，已成为构建高性能 AI 原生应用的关键前提。

---

## 关键维度对比

| 维度 | 图像生成（Image Generation） | 视频生成（Video Generation） |
|------|------------------------------|------------------------------|
| **输入格式** | 支持纯文本（T2I）、单图/多图（I2I、参考图）、局部掩码（inpainting）、涂鸦草图等；`input.messages[].content` 可混合 `text` + `image`（URL/base64），部分模型支持最多 14 张参考图（如 Vidu） | 以任务类型强驱动：文生视频（仅 `prompt`）、图生视频（需 `first_frame`/`last_frame` URL）、参考生视频（`media` 数组含图片或视频 URL）、视频编辑（`video_url` + `image_url` + `audio_url` 等组合）；不支持纯文本+多图混合输入 |
| **输出格式** | 单帧 PNG/JPEG 图像（URL 下载链接），支持批量生成（`n=1–9`，依模型而定）；结果即时返回（同步）或 24 小时内有效（异步） | 单个 MP4 视频文件（H.264 编码），时长通常为 2–8 秒（依模型与参数而定）；**仅支持异步模式**，结果 URL 有效期 24 小时 |
| **支持模型** | • 千问系列（`qwen-image-3.0-pro` 等）<br>• 万相系列（`wan2.7-image-pro`, `wanx-x-painting` 等）<br>• 可灵/VIDU（`kling-v3-omni-image-generation`, `viduq2-pro_reference2image`）<br>• 创意工具类（虚拟模特、海报生成、FaceChain 写真等）<br>• 轻量模型（`z-image-turbo`） | • HappyHorse（物理真实感视频）<br>• 万相系列（`wan2.7-videoedit`, `wan3-video-generation` 等）<br>• 爱诗（PixVerse，支持对口型、动作模仿、超分）<br>• VIDU / 可灵（Kling）/ MiniMax（高保真长时序建模）<br>• 数字人（`wan2.2-s2v`）等垂直模型 |
| **API 端点** | • 同步调用：`POST /api/v1/services/aigc/multimodal-generation/generation`（适用于 `qwen-image-*`, `wan2.7-image-pro`, `z-image-turbo`）<br>• [异步调用](../concepts/asynchronous-invocation.md)：`POST /image-synthesis` 或 `/generation` → `GET /tasks/{task_id}`（适用于 `kling`, `vidu`, 创意工具类） | **统一异步端点**：<br>`POST /api/v1/services/aigc/video-generation/video-synthesis` → `GET /api/v1/tasks/{task_id}`<br>（所有视频模型强制使用该路径，旧版 `/image2video/...` 已弃用） |
| **调用模式** | **同步与异步双模支持**：<br>• 同步：低延迟场景（<5s），适合实时预览、UI 即时反馈<br>• 异步：高分辨率/复杂编辑任务（如 `kling` 分镜组图、`wanx-x-painting` 局部重绘） | **强制异步模式**：<br>所有视频生成任务必须通过两步完成（创建任务 + 轮询），无同步接口；典型任务耗时 15–120 秒，不可用于实时交互链路 |
| **计费方式** | • 按**成功生成的图像张数**计费（如 1 张 = 1 [Token](../concepts/token.md)）<br>• 部分模型按**分辨率档位**（1K/2K/4K）阶梯计价（如 `wan2.7-image-pro`）<br>• 免费体验额度模型（如 `shoemodel-v1`）额度用尽即停用，**不支持续购** | • 按**成功生成的视频条数**计费（1 条 = 1 [Token](../concepts/token.md)）<br>• 多数模型按**输出时长 × 分辨率**综合计价（如 `pixverse-v6-t2v` 2s@1080p vs 4s@4K 成本差异显著）<br>• **无免费体验额度**；所有视频模型均为付费调用 |
| **典型场景** | • 营销素材快速生产（海报、Banner、商品图）<br>• 人像写真与风格化（FaceChain、虚拟模特）<br>• UI 设计稿生成与像素级还原（Vidu）<br>• A/B 测试多版本图像生成<br>• 图像修复、擦除补全、局部重绘 | • 短视频内容创作（广告片、产品演示、社交动态）<br>• 数字人播报与口型同步（PixVerse Lipsync）<br>• 动作迁移与角色动画（Animate-Move/Mix）<br>• 视频超分与画质增强（PixVerse Upscale）<br>• 分镜脚本可视化（Kling 多图参考生成） |

---

## 适用场景建议

### ✅ 推荐选择**图像生成**当：
- 业务需求聚焦于**静态视觉资产**：如电商主图、社交媒体配图、APP 启动页、PPT 插图；
- 需要**毫秒级响应**：例如设计工具中的“实时提示词渲染”、“画布内局部重绘”；
- 团队处于**MVP 验证阶段**：可利用 `z-image-turbo` 或免费创意模型（如 `virtualmodel-v2`）低成本试错；
- 对输出可控性要求极高：如 UI 还原、文字渲染（`qwen-image-3.0-pro` 支持中英文字精准生成）、像素级编辑。

### ✅ 推荐选择**视频生成**当：
- 核心目标是**动态表达与时间叙事**：如短视频营销、教育动画、数字人客服、游戏过场生成；
- 已具备稳定图像资产链路，并希望向上延伸至视频层：例如用 `wan2.7-image-pro` 生成高质量首帧，再交由 `wan2.7-videoedit` 生成视频；
- 需要**跨模态强控制能力**：如语音驱动口型（PixVerse Lipsync）、参考动作迁移（PixVerse MotionControl）、多图逻辑连贯性（Kling 分镜）；
- 接受异步工作流与服务端状态管理：已具备任务队列、Webhook 通知、结果缓存等后端基建。

### ⚠️ 不建议混用或强行替代：
- **勿用图像生成替代视频生成**：拼接多张图像无法保证运动连续性、时序一致性与物理合理性，且无音频/动作控制能力；
- **勿用视频生成替代图像生成**：视频模型无法输出单帧高清图（无 `n=1` 且分辨率不可控），成本高出 5–20 倍，且延迟不可接受；
- **避免跨地域调用**：二者均严格绑定地域（北京/新加坡/弗吉尼亚），混用 API Key 与 Endpoint 将直接返回 401/404。

---

## 技术选型参考（面向开发者）

| 选型维度 | 图像生成建议 | 视频生成建议 |
|----------|--------------|--------------|
| **入门集成** | 优先选用 `qwen-image-3.0-pro`（同步调用、OpenAI 兼容、文档完善）或 `z-image-turbo`（轻量、宽高比灵活）；SDK 直接调用 `dashscope.ImageGeneration.call()` | 从 `wan2.7-videoedit` 入手（功能全、文档成熟、支持图生+编辑）；务必封装标准轮询逻辑（含重试、超时、状态机） |
| **高并发低延迟** | 同步模型集群部署 + 请求批处理（如 `n=4` 批量生成）；启用 `thinking_mode=true` 辅助调试 | **必须异步解耦**：前端提交后立即返回 `task_id`；后端用消息队列（如 RocketMQ）驱动轮询与结果分发；禁用前端长轮询 |
| **成本敏感型项目** | 用 `wan2.1-turbo` 或 `z-image-turbo` 替代高阶模型；关闭水印（`watermark=false`）节省带宽；复用 base64 输入避免多次下载 | 严格限制 `parameters.resolution`（优先 720p 而非 4K）；避免冗余参考图；对口型/超分等增值能力按需开启，非默认启用 |
| **企业级稳定性要求** | 选用 `kling/kling-v3-omni-image-generation`（工业级鲁棒性）或 `vidu/viduq2-pro_reference2image`（UI 还原精度）；配置专属 Workspace 域名 | 选用 `HappyHorse`（物理真实感）或 `Vidu`（长时序一致性）；启用 `X-DashScope-Async: enable` 显式声明，避免协议误判 |
| **未来扩展性** | 千问图像模型与 Qwen-VL [多模态](../concepts/multi-modal.md)大模型共享底层架构，便于后续升级图文理解+生成联合体 | 万相 3.0 与 PixVerse v6 均支持“文本+图像+音频”三模态输入，是向[多模态](../concepts/multi-modal.md)智能体演进的优选底座 |

> 💡 **关键提醒**：图像生成与视频生成在百炼平台属于**独立服务域**，其配额、用量统计、监控告警、访问控制策略完全隔离。请在控制台分别开通服务、申请配额并配置独立告警规则。

---  
*最后更新：2024年6月*  
*文档维护：百炼平台技术文档组*

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)


