# 图像、视频与3D内容生成能力对比

为帮助开发者快速理解百炼平台在多模态生成领域的技术布局与能力边界，本文系统对比图像（Image）、视频（Video）与3D内容生成三大核心能力模块。对比聚焦实际工程落地的关键维度——包括输入/输出规范、模型生态、调用方式、地域约束、计费逻辑及典型适用场景，旨在为技术选型提供客观、可操作的决策依据。所有信息均基于百炼平台当前（2024年Q2）正式发布的API文档与运行实践整理，不包含内测或已下线能力。

## 关键能力维度对比

| 维度 | 图像生成（Image） | 视频生成（Video） | 3D生成（3D） |
|------|-------------------|-------------------|--------------|
| **核心输入格式** | 文本（`prompt`）、单图（URL/Base64）、多图（1–3张参考图）、图像区域坐标（局部编辑）、语言对（翻译）等，支持高度混合输入 | 文本（`prompt`）、单帧图（首帧/首尾帧）、视频（源视频）、音频（驱动口型）、检测坐标（`face_bbox`/`ext_bbox`）等，**强依赖前置检测步骤（人像类）** | 文本（`prompt`）、单张图像（`image_url`）、四视角图像数组（`images: [front, left, back, right]`），三者**严格互斥** |
| **核心输出格式** | PNG（主流）、JPG（部分专用模型如 `qwen-mt-image-2.0`）；支持 Base64 或公网 URL 返回；异步任务返回 `output.image_url` | MP4（主流，H.264编码）；全部为异步返回 `output.video_url`；无 Base64 直传选项 | GLB（PBR材质模型，`pbr_model_url`）、GLB（基础网格，`base_model_url`）、WebP预览图（`rendered_image_url`）；所有 URL **2小时有效期** |
| **主流支持模型** | `qwen-image-3.0-pro`（T2I/I2I统一）、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`、`aitryon-plus`（AI试衣）、`facechain-generation`（写真）等；含通用+垂直+创意工具三层架构 | `wan3.0`（All-in-One）、`wan2.7-videoedit`、`HappyHorse`、`pixverse/pixverse-v6-t2v`、`EMO`、`LivePortrait`、`Emoji` 等；**人像驱动类需耦合检测模型（如 `emo-detect-v1`）** | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速，≤2万面）；仅 Tripo 官方模型，无第三方替代方案 |
| **API 端点（华北2示例）** | 同步：`POST /api/v1/services/aigc/multimodal-generation/generation`<br>异步：同上 + `X-DashScope-Async: enable` 头 | 异步专用：`POST /api/v1/services/aigc/video-generation/video-synthesis`<br>**所有视频API强制要求 `X-DashScope-Async: enable`** | 异步专用：`POST /api/v1/services/aigc/video-generation/3d-generation`<br>**路径归属 `/video-generation/` 下，但功能独立；强制 `X-DashScope-Async: enable`** |
| **调用模式** | **同步与异步双模支持**：<br>• 同步：`qwen-image-3.0-pro`、`wan2.6-t2i`、`z-image-turbo`（直返结果）<br>• 异步：`wan2.5-i2i-preview`、`aitryon-plus`、`facechain-finetune`（需轮询） | **纯异步模式**：<br>• 所有模型均需两步：创建任务 → 轮询 `GET /api/v1/tasks/{task_id}`<br>• 任务 ID 有效期：**24 小时** | **纯异步模式**：<br>• 创建任务 → 轮询 `GET /api/v1/tasks/{task_id}`<br>• 任务 ID 有效期：**24 小时**；结果 URL 有效期：**2 小时** |
| **地域约束** | 模型部署地域、API Key、Endpoint **三者必须严格一致**；万相/可灵/Vidu 等模型在弗吉尼亚、法兰克福等地域支持不一，需查文档确认 | 模型、API Key、Endpoint **三者必须严格一致**；`wan2.2-s2v` 等数字人模型**仅限北京地域**；旧版路径（如 `/api/v1/services/aigc/image2video/...`）已废弃 | **仅支持华北2（北京）地域**；控制台开通、API Key 配置、请求 URL 均须匹配北京；跨地域调用必然失败 |
| **计费方式** | 按“成功生成的图片张数”计费；失败请求不扣费；新人享 **500 张/90 天** 免费额度；AI试衣精修（`aitryon-refiner`）采用阶梯定价 | 按“成功生成的视频条数”计费；失败不扣费；新人免费额度未统一说明，以控制台实时配额为准；高分辨率/长时长任务单价更高 | 按“成功生成的3D模型个数”计费；失败不扣费；新人免费额度未明确说明；`Tripo-H3.1`（`ultra`精度）单价高于 `Tripo-P1.0` |
| **典型延迟（端到端）** | 同步：3–8 秒（`z-image-turbo`）至 15–30 秒（`qwen-image-3.0-pro` 高分辨率）<br>异步：任务排队+生成，通常 30–120 秒 | 异步：文生视频约 60–300 秒；图生/参考生视频约 90–420 秒；数字人驱动（含检测）约 120–600 秒 | 异步：文生3D约 120–600 秒；单图生3D约 90–480 秒；多图生3D约 150–720 秒（`Tripo-H3.1` 更长） |
| **关键限制** | • 输入图 URL 需公网可访问且无中文路径<br>• 输出尺寸硬性约束（如 `qwen-image-3.0-pro`: 512×512 至 2048×2048）<br>• 部分模型（如 `facechain-facedetect`）输入上限 4096×4096 | • 人像类模型**必须前置调用检测 API** 获取 bbox<br>• `wan2.7` 及以上为唯一推荐协议，禁用旧版 `/image2video/` 路径<br>• 音频输入需为 PCM/WAV/MP3，时长 ≤30s | • `prompt`/`image`/`images` 三者互斥，同时传入任两者报错<br>• `images` 数组长度必须为 4，空位需用 `{}` 占位<br>• `Tripo-P1.0` 不支持 `geometry_quality` 参数 |

## 各方案适用场景建议

### ✅ 图像生成 —— 推荐用于：
- **高频、低延迟、轻量交互场景**：如电商商品图实时生成、营销海报A/B测试、UI组件像素级还原（`vidu-image-pro_reference2image`）、AI试衣初稿（`aitryon-plus`）；
- **多模态混合编辑需求**：需结合参考图、局部重绘、背景替换、文字纹理（WordArt）等链式操作的任务；
- **成本敏感型批量生产**：利用同步接口实现高吞吐生成（如每日千张产品图），或通过异步队列管理复杂编辑任务。

### ✅ 视频生成 —— 推荐用于：
- **动态内容规模化生产**：如短视频平台的文生视频脚本成片、电商商品动效展示（图生视频）、营销分镜视频（`kling` 多图输入）；
- **人像驱动与数字人应用**：虚拟主播口型同步（`pixverse-lipsync`）、表情包生成（`Emoji`）、会议数字分身（`LivePortrait`），**务必规划检测→生成的完整流水线**；
- **风格化与后处理需求**：对已有视频进行艺术风格迁移（8种预设）、超清增强、动作模仿等二次创作。

### ✅ 3D生成 —— 推荐用于：
- **工业与设计领域原型构建**：基于文本描述快速生成机械零件、家具、灯具等概念模型（`Tripo-H3.1`）；
- **电商与AR场景轻量化资产生产**：单图生成可直接嵌入WebGL/ARKit的GLB模型（`Tripo-P1.0`），适配手机端实时渲染；
- **多视角建模辅助**：提供前/左/后/右四图，显著提升生成模型拓扑完整性与几何精度，适用于产品摄影棚标准化流程。

> ⚠️ **不推荐交叉替代**：  
> - 勿用视频生成替代3D生成（视频无真实几何结构，无法导出网格）；  
> - 勿用图像生成替代视频关键帧生成（缺乏时序一致性，无法直接合成视频）；  
> - 勿用3D生成替代图像/视频（无纹理/光照/动画控制能力，非渲染引擎）。

## 面向开发者的选型决策指南

| 决策问题 | 推荐方案 | 关键依据 |
|----------|----------|----------|
| **我的业务需要实时预览（<5秒响应）？** | ✅ 图像生成（同步模式） | `z-image-turbo` / `qwen-image-3.0-pro` 支持直返Base64或URL；视频与3D均为异步，无法满足实时性 |
| **我要为1000件服装生成模特上身效果图？** | ✅ 图像生成（AI试衣链路） | `aitryon-plus` + `aitryon-parsing-v1` + `aitryon-refiner` 是专为该场景优化的端到端方案，视频/3D无对应能力 |
| **我有一段产品介绍文案，想自动生成30秒宣传短视频？** | ✅ 视频生成（`wan3.0` 或 `HappyHorse`） | 文生视频是核心能力；3D生成仅输出静态模型，图像生成仅输出单帧 |
| **我有4张标准角度的产品照片，需生成高精度3D模型用于AR展示？** | ✅ 3D生成（`Tripo/Tripo-H3.1`） | 多图输入是Tripo核心优势；图像/视频生成无法输出可交互3D网格 |
| **我的服务部署在新加坡地域，需调用数字人功能？** | ⚠️ 视频生成（需确认 `wan2.2-s2v` 是否支持）→ 否则 ❌ | `wan2.2-s2v` 明确仅限北京；其他数字人模型（如 `EMO`）需查新加坡地域支持列表；图像/3D在新加坡支持更广 |
| **我需要最低成本启动MVP验证？** | ✅ 图像生成（新人500张免费额度） | 视频/3D无明确新人免费额度说明；图像生成免费额度覆盖多数初期验证场景 |

**最后提醒**：  
- **始终校验地域一致性**：Key、Endpoint、模型三者地域不匹配是80%以上调用失败的根源；  
- **优先使用业务空间专属域名**：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，而非 `dashscope.aliyuncs.com`；  
- **异步任务务必实现幂等轮询**：设置合理间隔（≥15秒）、超时退出、结果URL及时下载（尤其3D的2小时有效期）；  
- **关注模型演进节奏**：`qwen-image-3.0-pro`、`wan3.0`、`Tripo-H3.1` 为当前主力推荐版本，避免使用文档中标注“已不推荐”的旧模型（如 `wan2.1–2.6`、`qwen-image-2.0-pro` 旧变体）。  

> 文档更新日期：2024年6月  
> 技术支持入口：百炼控制台 → 帮助中心 → API文档 → 对应模块

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


