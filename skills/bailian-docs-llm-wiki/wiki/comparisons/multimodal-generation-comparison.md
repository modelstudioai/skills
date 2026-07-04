# 多模态生成能力对比：图像 / 3D / 视频

百炼平台在「内容生成」方向同时提供图像、3D、视频三类多模态生成 API。三者底层模型不同、调用模式不同、产物形态不同，但都通过 DashScope 网关统一鉴权、统一编排。本文把它们放在一起对比，帮助开发者根据业务诉求（静态图 / 立体资产 / 动态影像）和工程约束（延迟、地域、异步轮询成本）做出技术选型。

## 关键维度对比

| 维度 | 图像生成 (image-generation) | 3D 生成 (3d-generation) | 视频生成 (video-generation-api) |
| --- | --- | --- | --- |
| 产物形态 | 单张 / 多张静态图片（PNG/JPG 临时 URL） | 带贴图的 GLB 模型（PBR 材质）或无贴图基础模型 + 预览渲染图 | 视频文件（MP4 等，临时 URL） |
| 底层模型族 | 通义千问图像、万相、Z-Image、可灵、创意工具系列 | Tripo 系列（`Tripo/Tripo-H3.1`、`Tripo/Tripo-P1.0`） | 万相 2.7、HappyHorse、Pixverse、Vidu、Kling、AnimateAnyone、LivePortrait、EMO、Emoji 等 |
| 主要输入方式 | 文本 [prompt](../guides/prompt.md)；可选参考图、蒙版、涂鸦、商品图 | 文生 3D（[prompt](../guides/prompt.md)）、单图生 3D（image）、多图生 3D（4 视角 images） | 文生视频、图生视频（首帧/首尾帧）、参考生视频、关键帧生视频、视频编辑、音频驱动数字人 |
| 输入格式 | 文本 + 公网 URL 或 Base64 图像；JSON 承载 | 文本 + 公网 URL 图像（JPEG/PNG） | 文本 + 公网 URL 图像/视频；JSON 承载 |
| API 端点 | OpenAI 兼容 `compatible-mode/v1/images/generations`；或 DashScope 原生 `services/aigc/text2image/image-synthesis` | `POST /api/v1/services/aigc/video-generation/3d-generation` + `GET /api/v1/tasks/{task_id}` | `POST /api/v1/services/aigc/video-generation/video-synthesis`（路径因模型略异）+ `GET /api/v1/tasks/{task_id}` |
| 调用模式 | 同步（OpenAI 兼容）或异步轮询（万相/创意工具，返回 task_id 后轮询） | 仅异步：必须带 `X-DashScope-Async: enable` 头，返回 task_id 后轮询 | 仅异步：必须带 `X-DashScope-Async: enable` 头，返回 task_id 后轮询 |
| 典型耗时 | 秒级（同步）/ 十秒级（异步） | 较长，轮询间隔建议约 15 秒 | 1–5 分钟 |
| 地域限制 | 无特殊限制，按 API Key 所属地域 | **仅华北2（北京）**，需使用北京地域 API Key | 模型、Endpoint URL、API Key 必须同一地域；北京/新加坡推荐业务空间专属域名 |
| 鉴权 | `Authorization: Bearer <API_KEY>` | 同左 | 同左 |
| 产物有效期 | 临时 URL，需及时下载或转存 OSS | GLB 等下载链接有效期 **2 小时** | 视频 URL 临时链接，需及时下载 |
| 计费方式 | 按调用次数 / 图数，不同模型单价不同 | 按任务类型（text-to-3d / image-to-3d / multi-image-to-3d）与生成数量计 | 按任务次数 / 视频时长，不同模型单价不同 |
| 内容安全 | 内置审核，违规 [prompt](../guides/prompt.md)/图片返回 `DataInspectionFailed` | 内置审核，失败任务返回 `code`/`message` | 内置审核，违规输入任务转 `FAILED` |
| 典型场景 | 营销海报、电商模特、艺术风格图、图像编辑/局部重绘、试衣、写真 | 商品 3D 展示、游戏/AR 资产、设计原型、虚拟试穿立体资产 | 短视频素材、广告片、数字人播报、视频风格化、动作生成 |

## 各方案适用场景建议

### 图像生成

适合产物是**静态图片**、追求高吞吐和低延迟的业务：电商模特图、营销海报、艺术风格插画、人像写真、图像编辑（换背景/改服饰/局部重绘）等。接口数量最多、模型族最丰富，从通义千问（中文语义准确）到万相（通用文生图+编辑一体）再到 Z-Image/可灵（高美感艺术风）和创意工具（虚拟模特、AI 试衣、画面扩展等垂类业务化封装），可选范围最广。如果只需"出图"且希望秒级返回，优先选 OpenAI 兼容模式的同步接口（如千问-文生图）。

### 3D 生成

适合需要**立体可旋转资产**的场景：商品 3D 展示、游戏与 AR 资产、设计原型。当前由 Tripo 系列提供，输入灵活（文生、单图、多图），输出 PBR 材质 GLB 可直接进渲染引擎。但有几个硬约束：仅北京地域、仅异步调用、产物链接 2 小时过期、task_id 24 小时内可查。新接入建议直接用 `Tripo/Tripo-H3.1`（高精度，最高 200 万面）或 `Tripo/Tripo-P1.0`（速度更快，最高 2 万面）。

### 视频生成

适合产物是**动态影像**的场景：短视频素材、广告片、数字人播报、视频风格化、动作生成。底层模型最多元（万相 2.7 主力 + HappyHorse/Pixverse/Vidu/Kling + 数字人/动作/表情类专模型），能力覆盖文生、图生、参考生、关键帧、视频编辑、风格转换。代价是耗时最长（1–5 分钟/任务）、参数最复杂（不同模型对 `size`/`duration`/参考图数量支持差异大）、对地域与业务空间域名要求最严。需要关键帧级镜头控制选 Pixverse/Vidu；需要数字人或口型驱动选 EMO/LivePortrait/AnimateAnyone/wan-s2v；通用文/图生视频首选万相 2.7。

## 技术选型参考

1. **先定产物形态**：静态图 → 图像生成；立体资产 → 3D 生成；动态视频 → 视频生成。三者不可互相替代，但可串联（如先图像生成出商品图，再用 3D 单图生 3D，最后用图生视频做动态展示）。
2. **再看延迟容忍**：秒级 → 图像同步接口；十秒级 → 图像异步 / 3D；分钟级 → 视频。
3. **核对地域与权限**：3D 仅北京；视频需模型/Endpoint/Key 同地域；图像最宽松。投产前确认 API Key 已开通对应模型。
4. **评估工程成本**：3D 与视频都强制异步轮询，需实现任务状态机（PENDING → RUNNING → SUCCEEDED/FAILED）和产物及时下载/转存逻辑，链路比图像同步调用重得多。
5. **关注产物有效期**：图像、3D（2 小时）、视频的临时 URL 都需在拿到后立即下载或转存到 OSS，避免链接失效。
6. **内容安全合规**：三类接口都内置审核，违规输入会被拦截并返回错误码，业务侧需做好失败兜底与重试策略。

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


