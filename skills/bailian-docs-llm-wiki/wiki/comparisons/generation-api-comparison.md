# 生成类 API 对比

百炼平台提供了三大类生成式 AI API——图像生成、3D 资产生成和视频生成。它们在输入方式、输出产物、调用模式、支持模型和适用场景上各有差异。本页对三类 API 做横向对比，帮助开发者根据业务需求快速选型。

## 关键维度对比

| 维度 | 图像生成 | 3D 生成 | 视频生成 |
| --- | --- | --- | --- |
| **输入格式** | 文本提示词（[prompt](../guides/prompt.md)）；参考图 URL（图生图/编辑）；多图参考 | 文本 [prompt](../guides/prompt.md)（≤1024 字符）；单张图像 URL；多图（固定 4 张：前/左/后/右视角） | 文本 [prompt](../guides/prompt.md)；media 多模态数组（首帧/尾帧/参考图/视频/音频）；直接 URL 字段（旧版协议） |
| **输出格式** | 图像文件（PNG/JPG），像素范围 512×512 ~ 2048×2048，1~6 张 | GLB 格式 3D 模型（PBR 材质或无贴图基础模型）+ 预览渲染图 | 视频文件，分辨率 480P~4K，时长 5~8 秒（视模型而定） |
| **调用模式** | 混合：wan2.6/2.7、z-image、qwen-image 支持同步调用；长耗时任务走异步 | 仅异步（必须 `X-DashScope-Async: enable`） | 仅异步（必须 `X-DashScope-Async: enable`） |
| **API 端点** | 多个端点（按模型系列不同）；同步与异步并存 | `POST .../aigc/video-generation/3d-generation` + `GET .../tasks/{task_id}` | `POST .../aigc/video-generation/video-synthesis` + `GET .../tasks/{task_id}` |
| **支持模型数** | 最多（Qwen-Image、万相全系列、z-image、Kling、Vidu、创意工具等 20+ 模型） | 最少（Tripo-H3.1、Tripo-P1.0 两个模型） | 较多（万相 wan2.7/2.6/2.2、HappyHorse、PixVerse、Vidu、Kling、人像动画系列等） |
| **地域限制** | 部分北京独占（创意工具、wanx-v1）；其余支持多地域 | 仅华北2（北京） | 北京、新加坡、美国（弗吉尼亚）、德国（法兰克福） |
| **task_id 有效期** | 视模型而定（异步任务一般为 24 小时） | 24 小时 | 24 小时 |
| **产物下载有效期** | 视模型而定 | 2 小时 | 视模型而定 |
| **轮询建议间隔** | 视模型而定 | 约 15 秒 | 视模型而定（查询 RPS 限制 20） |
| **计费方式** | 按张计费（如 wanx-v1 0.16 元/张）或按调用次数 | 按任务类型（text-to-3d / image-to-3d / multi-image-to-3d）计费 | 按任务类型与分辨率/时长计费 |
| **同步调用支持** | 是（wan2.6/2.7、z-image、qwen-image 系列新模型） | 否 | 否 |
| **任务状态枚举** | — | PENDING → RUNNING → SUCCEEDED / FAILED / CANCELED / UNKNOWN | PENDING → RUNNING → SUCCEEDED / FAILED / CANCELED / UNKNOWN |

## 各方案适用场景建议

### 图像生成

- **适用场景**：营销素材批量生成、商品图编辑、内容配图、创意海报、虚拟试衣、图像翻译等。
- **选型建议**：
  - 需要复杂文本渲染与段落排版 → Qwen-Image 系列。
  - 追求高性价比、轻量快速 → z-image-turbo。
  - 需要多图参考、4K 高清输出 → 万相 wan2.7-image-pro。
  - 需要风格化、去水印、超分等专项编辑 → 万相通用图像编辑 `wanx2.1-imageedit`。
  - 第三方风格偏好 → Kling 或 Vidu 系列。

### 3D 生成

- **适用场景**：游戏资产生成、电商 3D 展示、建筑可视化、教育/文物数字化的快速 3D 建模。
- **选型建议**：
  - 需要高精度、高面数模型 → Tripo-H3.1（最高 200 万面，支持 `ultra` 几何精度）。
  - 追求生成速度、对面数要求不高 → Tripo-P1.0（最高 2 万面，速度更快）。
  - 需要带贴图的 PBR 材质模型 → `pbr` 设为 `true`（默认）。
  - 只需基础白模 → `texture` 和 `pbr` 同时设为 `false`。
  - 注意：仅限北京地域 API Key 调用，需提前在控制台开通 Tripo 服务。

### 视频生成

- **适用场景**：短视频内容创作、广告生成、视频编辑、数字人/口型替换、视频超清、动作模仿等。
- **选型建议**：
  - 需要最新协议、多能力集成 → 万相 wan2.7（文生/图生/参考/编辑，推荐）。
  - 需要首尾帧、多镜头分镜 → Kling kling-v3 系列。
  - 需要 4K 超清、对口型、动作模仿 → PixVerse 系列。
  - 数字人/人像动画 → animate-anyone、emo、liveportrait 等人像动画系列。
  - 注意：所有视频 API 均为异步调用，跨地域调用会失败，务必保证模型、域名、API Key 同地域。

## 技术选型参考

| 需求特征 | 推荐方案 | 理由 |
| --- | --- | --- |
| 低延迟、即时返回 | 图像生成（同步模型） | wan2.6/2.7、z-image 等支持 HTTP 同步调用，无需轮询 |
| 批量处理、可容忍异步 | 任意（图像异步 / 3D / 视频） | 异步模式支持任务队列，适合批量场景 |
| 多模态输入（图+文+音） | 视频生成 | media 数组支持首帧/尾帧/参考图/视频/音频等多模态组合 |
| 多视角输入 | 3D 生成 | 支持前/左/后/右四视角多图生 3D |
| 需要文本渲染能力 | 图像生成（Qwen-Image） | 擅长复杂文本渲染与多行段落排版 |
| 需要多地域部署 | 视频生成 | 支持北京/新加坡/美国/德国四地域 |
| 成本敏感 | 图像生成（z-image-turbo / wanx-v1） | 轻量模型或 V1 版价格更低 |
| 高保真输出 | 3D 生成（Tripo-H3.1 ultra）或图像生成（wan2.7-image-pro 4K） | 高精度模型支持超高分辨率/面数输出 |

## 被对比主题页

- [image generation](../api/image-generation.md)
- [3d generation](../api/3d-generation.md)
- [video generation api](../api/video-generation-api.md)


