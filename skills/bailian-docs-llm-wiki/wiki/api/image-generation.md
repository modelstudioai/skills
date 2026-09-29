# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意文字生成及垂直场景工具（如AI试衣、人物写真、海报生成等）。所有模型均通过统一的 DashScope API 协议接入，支持同步/异步调用，并需严格匹配地域、API Key 与 Endpoint。开发者应优先选用新版模型（如 `qwen-image-3.0`、`wan2.7-image-pro`）以获得更优效果与稳定性。

## 支持的模型/功能

平台图像能力分为三大类：

- **通用生成模型**：  
  - 千问系列：`qwen-image-3.0-pro`（推荐）、`qwen-image-3.0`、`qwen-image-2.0-pro-*`，支持文生图与图生图二合一，[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 提供完整能力说明；  
  - 万相系列：`wan2.7-image-pro`（支持4K文生图）、`wan2.6-t2i`、`wan2.5-i2i-preview`，覆盖V1/V2文生图、多图融合、图文混排；  
  - Z-Image：轻量级 `z-image-turbo`，主打快速响应与中英文字渲染；  
  - 可灵与Vidu：`kling/kling-v3-omni-image-generation`（支持分镜组图）、`vidu/viduq2-pro_reference2image`（工业级稳定性），均强调UI/图表像素级还原与复杂逻辑处理。

- **创意工具与垂直模型**：  
  - 图像编辑类：万相通用编辑（`wan2.5-i2i-preview`）、千问图像编辑（`qwen-image-2.0-pro`）、图像局部重绘（`wanx-x-painting`，[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)）；  
  - 人像增强类：人像风格重绘（`wanx-style-repaint-v1`）、虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）；  
  - 生成增强类：AI试衣（`aitryon-plus`、`aitryon-refiner`）、人物写真FaceChain（`facechain-generation`）、创意海报（`wanx-poster-generation-v1`）；  
  - 文字专项：WordArt锦书（`wordart-semantic`、`wordart-texture`），支持文字变形与纹理生成。

- **辅助与预处理模型**：  
  - 人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）、背景生成（`wanx-background-generation-v2`）、AI试衣图片分割（`aitryon-parsing-v1`）等，用于构建端到端工作流。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-erase-completion`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，文档明确建议迁移到千问或万相2.1+替代方案 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

## 关键参数

所有图像API共用核心参数结构，关键字段如下：

- `model`（必选）：模型名称，如 `"wan2.7-image-pro"` 或 `"qwen-image-3.0-pro"`；
- `input.messages`（文生图）或 `input.messages.content.image`（图生图）：文本提示词（`text`）与可选参考图（`image`，支持URL或Base64）；
- `parameters.size`（可选）：输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`），不同模型约束不同：
  - 千问3.0系列：总像素 512×512 至 2048×2048；
  - 万相2.7 Pro：文生图支持4K（3840×2160），编辑/组图限2K；
  - Vidu：明确支持1K/2K/4K；
  - Z-Image：总像素 512×512 至 2048×2048；
- `parameters.n`（可选）：生成张数，范围因模型而异（如 `qwen-image-2.0-pro` 支持1–6张，`kling` 支持1–9张）；
- `X-DashScope-Async`（HTTP调用必选）：异步请求必须设为 `"enable"`，否则报错 `"current user api does not support synchronous calls"`；
- `input.generate_mode`（创意海报等专用）：指定 `"generate"`、`"sr"`（超分）或 `"hrf"`（高清修复）。

## 使用方式

### 接入协议与调用模式
- **同步调用**：适用于耗时较短（通常<30s）的模型，如 `qwen-image-3.0`、`wan2.7-image`、`z-image-turbo`，一次请求返回结果；
- **异步调用**：适用于耗时较长（1–2分钟）的模型（如万相V1/V2文生图、可灵、Vidu、所有创意工具），流程为：  
  1. `POST /generation` 创建任务，获取 `task_id`；  
  2. `GET /tasks/{task_id}` 轮询状态，成功后返回图像URL（有效期24小时）；  
  该模式在 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md) 等文档中有详细步骤说明。

### 地域与Endpoint
- **强制同地域**：模型、API Key、Endpoint URL 必须属于同一地域（北京/新加坡/弗吉尼亚等），跨地域调用将鉴权失败；
- **推荐域名**：华北2（北京）和新加坡地域已启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`，[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确建议迁移。

### SDK与HTTP
- DashScope Python/Java SDK 全面支持主流模型（同步/异步）；
- HTTP调用需严格设置 `Content-Type: application/json` 和 `Authorization: Bearer $DASHSCOPE_API_KEY`；
- 所有异步HTTP请求必须携带 `X-DashScope-Async: enable` 头。

## 限制和注意事项

- **地域隔离**：北京、新加坡、弗吉尼亚等地域的 API Key 与 Endpoint **不可混用**，尤其万相2.6+、可灵、Vidu 均明确要求独立配置；
- **免费额度规则**：  
  - 大部分模型提供90天内500张免费额度（如 `wanx-style-repaint-v1`、`facechain-generation`、`wordart-semantic`），额度由主账号与RAM子账号共享；  
  - 部分模型（如 `wanx-x-painting`）为限时免费，额度用尽即停用，无付费通道；
- **输入限制**：  
  - 图像URL需公网可访问、无中文路径（需URL编码）、格式合规（PNG/JPEG/WEBP等）；  
  - 提示词长度、图像分辨率、文件大小（如FaceChain要求人脸≥128×128像素、图像≤5MB）需符合各模型文档要求；
- **模型弃用**：万相V1（`wanx-v1`）已明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”；
- **计费差异**：AI试衣-图片精修（`aitryon-refiner`）采用阶梯计价，用量越大单价越低，而其他模型多为固定单价（如 `aitryon-plus` 0.50元/张）；
- **并发控制**：多数异步模型限制“同时处理中任务数量”为1–5个（如 `facechain-finetune` 并发限1），超出任务将排队。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)


