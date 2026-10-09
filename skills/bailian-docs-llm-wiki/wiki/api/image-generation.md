# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意文字生成及垂直场景工具（如虚拟模特、AI试衣、人物写真等）。所有模型均通过统一的 DashScope API 协议接入，支持同步与异步调用模式，开发者可根据任务耗时和业务需求灵活选择。

## 支持的模型/功能

平台当前提供三大类图像模型：

- **通用生成与编辑模型**：包括千问系列（`qwen-image-*`）和万相系列（`wan*`），支持文生图、图生图、多图融合、图文混排、4K高清输出等。其中 `qwen-image-3.0-pro` 和 `wan2.7-image-pro` 为最新主力模型，兼顾语义遵循、文字渲染与细节还原能力；`wan2.6-t2i` 是文生图V2版推荐模型，支持自由尺寸与宽高比 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **垂直场景工具模型**：覆盖电商、设计、内容创作等高频需求，例如：
  - 虚拟模特（`wanx-virtualmodel`, `virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）
  - AI试衣（`aitryon`, `aitryon-plus`, `aitryon-refiner`）与配套分割（`aitryon-parsing-v1`）
  - 人物写真（`facechain-generation`，支持免训练trainfree模式）[原文标题](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
  - 创意文字（`wordart-semantic`, `wordart-texture`），专精汉字变形与纹理生成
- **轻量与专用模型**：如 `z-image-turbo`（快速轻量文生图）、`kling/kling-v3-*`（支持分镜组图）、`vidu/*_reference2image`（强UI/图表像素级还原）等。

> **注意**：部分早期模型（如 `wanx-v1`, `qwen-image-2.0` 等）已明确标注为“推荐使用升级版”，其能力、分辨率限制与计费策略可能与新版不一致，应优先选用 `qwen-image-3.0-pro` 或 `wan2.7-image-pro` 等新模型 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)。

## 关键参数

核心参数因模型类型而异，但共性字段如下：

- `model`：必填，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`）。
- `input.messages`：必填（多数模型），格式为 `[{"role": "user", "content": [...] }]`，`content` 数组可包含 `text`（提示词）和 `image`（Base64 或公网 URL）。
- `size`：控制输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。不同模型约束不同：
  - 千问系列：总像素需在 `512×512` 至 `2048×2048` 之间；
  - 万相V2（`wan2.6-t2i`）：宽高比 `1:4` 至 `4:1`，总像素在 `[1280×1280, 1440×1440]`；
  - 可灵（`kling`）：仅支持预设分辨率（`1k`/`2k`/`4k`）与宽高比（`16:9`/`9:16`/`1:1`）。
- `n`：生成图片张数（通常 `1–9`），部分模型（如 `qwen-image-2.1-pro`）支持 `1–6` 张。
- `parameters`：扩展参数对象，常见子字段：
  - `steps`（如 `wordart-semantic`）：变形迭代次数，默认 `30`，范围 `10–100`；
  - `font_name`（如 `wordart-texture`）：指定字体（如 `"puhuiti_m"`）；
  - `generate_mode`（如 `wanx-poster-generation-v1`）：海报生成模式（`"generate"`/`"sr"`/`"hrf"`）。

## 使用方式

### 接入协议与域名
- 所有模型均支持 **DashScope SDK（Python/Java）** 和 **HTTP API**。
- **强烈推荐使用业务空间专属域名**（性能与稳定性更优）：
  - 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
  - `{WorkspaceId}` 在控制台「业务空间详情」中获取。
- 跨地域调用必然失败，API Key、Endpoint、模型必须属同一地域 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

### 同步 vs 异步调用
- **同步调用**：适用于耗时较短（通常 <30s）的任务，如 `qwen-image-3.0-pro`、`wan2.7-image-pro`（文生图）、`z-image-turbo`。一次请求即返回结果。
- **异步调用**：适用于耗时较长（1–2分钟）的任务，如图像编辑、扩图、虚拟模特、AI试衣等。流程为：
  1. `POST /generation` 创建任务 → 获取 `task_id`；
  2. 定期 `GET /tasks/{task_id}` 查询状态 → 返回图像 URL（有效期 24 小时）。
- **关键请求头**：异步调用必须携带 `X-DashScope-Async: enable`，否则报错 `"current user api does not support synchronous calls"`。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key 与 Endpoint **完全独立，不可混用**。万相2.6、可灵、Vidu 等模型明确列出多地域支持，而千问、Z-Image 等文档仅提北京/新加坡，调用前务必核对 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。
- **免费额度与限流**：
  - 免费额度按“成功生成的图片张数”计算，有效期 90 天，主账号与 RAM 子账号共享；
  - 多数模型 QPS 限制为 `2`，并发任务数 `1–5`（如 `facechain-finetune` 并发限 `1`，`aitryon` 限 `5`）；
  - 部分模型（如 `wanx-x-painting`, `shoemodel-v1`, `wanx-poster-generation-v1`）为“限时免费”，额度用尽后不可调用且不支持付费。
- **输入规范**：
  - 图像 URL 必须公网可访问、支持 HTTP/HTTPS，含中文路径需 URL 编码；
  - 图像格式支持 JPG/PNG/WEBP/BMP/AVIF，单图大小通常 ≤5MB（部分 ≤10MB），分辨率常限 `512×512` 至 `4096×4096`；
  - 提示词长度建议 ≤200 字，避免冗余描述影响效果。
- **模型能力边界**：复杂逻辑（如多物体空间关系精确控制）、超长文本渲染（>200字符）、极高精度 UI 元素（如代码截图级还原）仍存在局限，建议结合 `vidu/viduq2-pro_reference2image` 或人工后处理。

## 来源文档

- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)


