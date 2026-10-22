# 多模态生成能力对比：图像生成、视频生成与 3D 生成 API

为帮助开发者快速理解百炼平台在多模态内容生成领域的技术布局与能力边界，本文系统对比图像生成（Image Generation）、视频生成（Video Generation）与 3D 生成（3D Generation）三类核心 API 的关键特性。对比聚焦实际工程落地维度——包括输入/输出规范、模型生态、调用机制、资源约束及成本模型，旨在为产品设计、技术选型与架构决策提供客观、可执行的参考依据。

---

## 关键能力维度对比

| 维度 | 图像生成 API | 视频生成 API | 3D 生成 API |
|------|--------------|----------------|----------------|
| **核心模态支持** | 文生图（T2I）、图生图（I2I）、局部编辑、风格迁移、多图组图、涂鸦生成、人像定制等 | 文生视频（T2V）、图生视频（I2V）、人像驱动动画（Portrait Animation）、多模态联合生成（文本+图像+音频） | 文生3D、单图生3D、四视角多图生3D（前/左/后/右） |
| **主流支持模型** | `qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling-v3-omni-image-generation`、`vidu-image-pro_reference2image`、`z-image-turbo`、`facechain-finetune` 等 | `kling`、`wanxiang`、`pixverse`（爱诗）、`portrait-animation`、`minimax`（多模态）等 | `Tripo/Tripo-H3.1`（高精度，≤200万面）、`Tripo/Tripo-P1.0`（快速，≤2万面） |
| **输入格式** | • 文本：`text`（长度上限因模型而异，如 Vidu ≤5000 字符）<br>• 图像：公网 URL 或 Base64（千问最多10张，万相/Vidu 最多14张）<br>• 多模态组合：支持 prompt + reference images + element_list（可灵） | • 文本：`input.text`（`可灵` ≤512 字符，`万相` ≤200 字符，`人像驱动` ≤100 字符）<br>• 图像：`input.image_url`（HTTPS 公网地址，≥512×512）<br>• 音频：`input.audio_url`（仅人像驱动/MiniMax）<br>• 多模态：部分模型支持 text+image+audio 联合输入 | • 三者**严格互斥**：<br> – `input.prompt`（中英文，≤1024 字符）<br> – `input.image`（JPEG/PNG 公网 URL，20–6000px，≤20MB）<br> – `input.images`（4 元素数组，按 `[前, 左, 后, 右]` 顺序，空视角用 `{}` 占位） |
| **输出格式** | • JPEG/PNG 图像二进制流（同步）或直链 URL（异步）<br>• 支持多张输出（`n` 或 `series_amount` 控制）<br>• 可选水印、思考模式、分辨率控制 | • MP4 视频直链 URL（有效期 24 小时）<br>• 无原始二进制流返回<br>• 输出含预览帧（部分模型） | • GLB 格式 3D 模型直链：<br> – `pbr_model_url`（含 PBR 材质贴图，默认启用）<br> – `base_model_url`（无贴图基础网格，需显式设 `texture=false && pbr=false`）<br>• `rendered_image_url`（渲染预览图，有效期 2 小时） |
| **调用协议** | • 同步（推荐多数场景）：`qwen-image-*`、`wan2.7-image-*`、`z-image-turbo` 等<br>• 异步（必需）：`kling/*`、`vidu/*`、`wan2.5-i2i-preview` 等<br>• OpenAI 兼容模式（仅千问同步调用） | • **全部强制异步**：<br> `POST /api/v1/video-generation` → 获取 `job_id` → `GET /api/v1/jobs/{job_id}` 轮询 | • **全部强制异步**：<br> `POST /api/v1/services/aigc/video-generation/3d-generation` → 获取 `task_id` → `GET /api/v1/tasks/{task_id}` 轮询<br>• 必须携带 `X-DashScope-Async: enable` |
| **API Endpoint 特性** | • 地域强绑定：Endpoint、API Key、Workspace ID 必须同地域（北京/新加坡/弗吉尼亚等）<br>• 域名格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com` | • 同样强地域绑定；各模型部署区域需与请求 endpoint 一致（如 `Vidu` 在华北2 部署，则不可用华东 endpoint 调用） | • **仅支持华北2（北京）地域**<br>• Endpoint 固定为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/3d-generation` |
| **计费方式** | • 按 token（文本）或 image（生成张数/分辨率）计费<br>• 部分创意工具模型（如 `shoemodel-v1`、`virtualmodel-v2`）当前限免费额度体验<br>• QPS 与并发任务数均有硬限制（如 FaceChain 并发=1） | • 按 job 计费（每成功生成一个视频任务计 1 次）<br>• 不同模型单价不同（如 `portrait-animation` 与 `kling` 分属不同计费档位）<br>• 无免费额度，失败任务不计费 | • 按 task 计费（每创建并完成一个 3D 任务计 1 次）<br>• `Tripo-H3.1`（高面数/ultra 质量）费用高于 `Tripo-P1.0`<br>• 无免费额度，任务失败不计费 |
| **典型生成耗时** | • 同步：300ms–3s（`z-image-turbo` <500ms；`qwen-image-3.0-pro` ≈1.2s）<br>• 异步：2s–90s（`kling` 组图约 30–60s；`vidu` UI 图表约 15–45s） | • 通用文生视频：15–120s（`pixverse` 较快，`kling` 中高复杂度约 60–90s）<br>• 人像驱动：20–180s（受人脸质量影响大，失败重试成本高） | • `Tripo-P1.0`：30–90s<br>• `Tripo-H3.1`：90s–5min（`geometry_quality: "ultra"` 显著延长） |
| **结果有效期** | • 同步响应：即时返回二进制流，无有效期<br>• 异步直链：URL 有效期统一为 **24 小时** | • `output.video_url` 有效期 **24 小时** | • 所有 URL（`pbr_model_url`/`base_model_url`/`rendered_image_url`）有效期 **2 小时**<br>• `task_id` 有效期 **24 小时** |

---

## 适用场景建议

| 场景类型 | 推荐方案 | 理由说明 |
|----------|-----------|-----------|
| **营销素材快速生产**（Banner、海报、社交媒体配图） | ✅ 图像生成（`wan2.7-image-pro` 或 `qwen-image-3.0-pro`） | 支持高分辨率（4K）、自由宽高比、批量生成（`n=4`），同步调用低延迟，适合 CMS/MAAS 平台集成；Vidu 对中英文字渲染精准，适用于带文案的电商图。 |
| **UI/UX 设计辅助**（界面原型、图标、图表可视化） | ✅ 图像生成（`vidu/vidu-image-pro_reference2image`） | 像素级还原能力突出，支持参考图+文字双约束，可精准复现 Figma/Sketch 设计稿结构与文字排版，是设计协同工作流的理想入口。 |
| **短视频内容创作**（产品展示、知识科普、剧情短片） | ✅ 视频生成（`kling` 或 `wanxiang`） | 支持文生视频与图生视频双路径，`kling` 分镜组图能力利于脚本化生产；`wanxiang` 在运动连贯性与中文语义理解上表现稳健，适合中低复杂度叙事。 |
| **虚拟人/数字人驱动**（直播、客服、培训） | ✅ 视频生成（`portrait-animation`） | 专为人像定制优化，支持音频/文本驱动口型与微表情，输出自然流畅；但需严格预处理人脸（正脸、均匀光照、无遮挡），建议搭配人脸质检 SDK 使用。 |
| **3D 电商与元宇宙资产构建**（商品建模、虚拟展厅、AR 试穿） | ✅ 3D 生成（`Tripo/Tripo-H3.1`） | 支持单图生成高质量带 PBR 材质的 GLB 模型，兼容 Unity/Unreal/WebGL；`ultra` 模式对复杂曲面（如鞋包、家电）重建精度显著优于 `P1.0`，满足商用交付标准。 |
| **快速原型验证与内部协作**（概念草图转 3D、简易道具建模） | ✅ 3D 生成（`Tripo/Tripo-P1.0`） | 生成速度快（<90s）、成本低，适合 A/B 测试、设计评审、非核心资产填充；配合多图输入（四视角）可大幅提升拓扑准确性，降低后期修模成本。 |
| **跨模态内容联动**（图文→视频→3D 资产链） | ⚠️ 组合使用（图像 → 视频 → 3D） | 当前三类 API **无原生串联能力**，需业务层自行编排：例如用 `wan2.7-image-pro` 生成高质量产品图 → 输入 `kling` 生成 5 秒展示视频 → 再以该图作为 `Tripo-H3.1` 输入生成 3D 模型。注意各环节 URL 有效期差异（2h vs 24h）。 |

---

## 开发者技术选型参考

- **优先选择同步调用**：若业务对首屏延迟敏感（如实时作图工具、聊天机器人插件），**仅图像生成 API 提供广泛同步支持**；视频与 3D 必须异步，需提前设计轮询/回调机制，并做好前端 Loading 状态管理。
  
- **警惕地域锁定风险**：三类 API 均强制地域隔离。**切勿复用跨地域 API Key 或 Endpoint**。建议在初始化阶段校验 `region` 与 `workspace_id` 匹配性，失败时明确报错而非静默降级。

- **输入容错与降级策略**：
  - 图像生成：对长 prompt 建议截断至模型上限（如 Vidu 截至 5000 字符），并启用 `watermark=true` 防止版权争议；
  - 视频生成：人像驱动类任务失败率高，务必实现自动重试（≤3 次）+ 人脸预检（检测角度/光照/遮挡）；
  - 3D 生成：多图输入必须严格 4 元素数组，缺失视角用 `{}` 占位；避免传入模糊/低对比度图像，否则易触发 `FAILED` 状态。

- **成本与性能平衡**：
  - 图像：`z-image-turbo` 适合草稿/预览；`wan2.7-image-pro` 平衡质量与速度；`vidu` 为高保真付费场景首选。
  - 视频：`pixverse` 适合轻量文生视频；`kling` 适合需分镜/多图参考的复杂任务；避免对 `portrait-animation` 高频调用（QPS 限制严）。
  - 3D：`Tripo-P1.0` 用于 MVP 验证；`Tripo-H3.1` 用于生产交付；禁用 `texture=false && pbr=false` 组合除非明确需要无材质网格（如物理仿真）。

- **错误处理重点**：
  - 共性错误：`X-DashScope-Async` 缺失（所有异步 API 必填）、`InvalidParameter`（参数冲突或格式错误）、地域不匹配（

## 被对比主题页

- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)


