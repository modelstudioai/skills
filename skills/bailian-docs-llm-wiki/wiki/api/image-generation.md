# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、背景生成、创意文字等场景。核心能力由千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列垂直创意工具（如 FaceChain、WordArt、AI试衣等）共同支撑，支持同步与异步调用，适配不同性能、质量与成本需求。

## 支持的模型/功能

平台图像生成能力分为通用基础模型与垂直领域工具两类：

- **通用基础模型**：  
  - **千问系列**：`qwen-image-3.0-pro` 和 `qwen-image-3.0` 同时支持文生图与图生图/图像编辑，具备强文本渲染与语义遵循能力 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；早期模型如 `qwen-image-2.0-pro` 仍被部分文档引用，但官方明确推荐迁移到 3.0 系列。  
  - **万相系列**：`wan2.7-image-pro` 支持文生图（最高4K）、组图生成与多图编辑；`wan2.6-t2i` 专注文生图，支持自由宽高比（1:4 至 4:1）与大尺寸输出；`wan2.5-i2i-preview` 支持单图编辑与多图融合 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。  
  - **可灵（Kling）**：`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成，分辨率可达4K；`kling/kling-v3-image-generation` 仅支持单图参考 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。  
  - **Vidu**：`vidu/vidu-image-pro_reference2image` 等系列强调UI/图表像素级还原与工业级稳定性；`vidu/viduq3-fast_reference2image` 在成本降低约50%前提下保持高速高质。  
  - **Z-Image**：轻量级模型 `z-image-turbo`，主打快速响应，适用于对延迟敏感的场景。

- **垂直创意工具**：  
  - **FaceChain**：基于LoRA微调或免训练模式生成人物写真，支持证件照、商务风、复古风等预设及自定义模板 [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)。  
  - **WordArt锦书**：专精汉字创意设计，含文字变形（`wordart-semantic`）与文字纹理生成（`wordart-texture`）两大能力，支持预设风格与提示词驱动自定义。  
  - **AI试衣（OutfitAnyone）**：提供 `aitryon`（基础版）、`aitryon-plus`（高质版）及后处理 `aitryon-refiner`，支持上下装组合、人脸保留/替换等精细化控制。  
  - 其他包括虚拟模特、鞋靴模特、人像风格重绘、图像擦除补全、背景生成、画面扩展（扩图）等，均面向特定业务场景优化。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`、`image-instance-segmentation`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议参考千问或万相2.1等替代方案 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

## 关键参数

各模型共性关键参数如下（具体以模型文档为准）：

- **`model`**：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`、`"kling/kling-v3-omni-image-generation"`）。  
- **`input`**：必填对象，结构因任务类型而异：  
  - 文生图：通常含 `prompt` 字符串（V2版万相、Z-Image等）或 `messages` 数组（千问3.0、可灵、Vidu等，首项 `text` 为提示词）；  
  - 图生图/编辑：需提供 `image_url` 或 `image`（Base64），部分模型（如万相2.5）支持多图输入；  
  - 工具类模型（如FaceChain、WordArt）有专用字段，如 `input.text` + `input.prompt`（文字变形）、`template_image_url` + `shoe_image_url`（鞋靴模特）。  
- **`size`**：可选字符串，指定输出分辨率（如 `"1024*1024"`、`"1280*1280"`）。约束因模型而异：  
  - 千问3.0：总像素需在 `512*512` 至 `2048*2048` 之间；  
  - 万相2.6-t2i：宽高比限于 `[1:4, 4:1]`，总像素在 `[1280*1280, 1440*1440]`；  
  - 可灵/Vidu：支持 `1K`/`2K`/`4K`，对应具体像素值（如 `1024*1024`、`2048*2048`、`3840*3840`）。  
- **`n`**：可选整数，指定生成图片张数（如万相V2、可灵文生图默认为1，上限9）。  
- **`parameters`**：可选对象，承载模型特有配置（如 `steps` 控制迭代次数、`font_name` 指定字体、`generate_mode` 选择海报生成模式等）。

## 使用方式

调用方式分为 **同步** 与 **异步** 两类，选择依据是任务耗时与业务容忍度：

- **同步调用**：适用于响应时间较短（通常 < 30s）的模型，如 `qwen-image-3.0`（DashScope同步）、`z-image-turbo`、`wan2.7-image-pro`（HTTP同步）、`wan2.6-t2i`（HTTP同步）。请求直接返回结果，无需轮询。Endpoint 示例：  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（万相2.7）  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`（万相V2）  

- **异步调用**：适用于耗时较长（通常 1–2 分钟）的任务，如可灵、Vidu、万相2.5编辑、FaceChain训练、AI试衣等。流程为两步：  
  1. **创建任务**：发送 POST 请求至任务创建接口（如 `/api/v1/services/aigc/image-generation/generation`），获取 `task_id`；  
  2. **轮询结果**：使用 `task_id` 调用查询接口（如 `/api/v1/tasks/{task_id}`），直至状态为 `SUCCESS`，返回图像 URL（有效期通常 24 小时）。  
  > **重要**：所有异步 HTTP 调用必须在请求头中包含 `X-DashScope-Async: enable`，否则报错 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

**地域与认证**：所有调用必须确保模型、API Key、Endpoint URL 属于同一地域（华北2北京、新加坡、弗吉尼亚等）。强烈推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧域名（`dashscope.aliyuncs.com`），以获得更高性能与稳定性。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立的 API Key 与 Endpoint，跨地域调用将导致鉴权失败或服务报错。务必核对地域一致性。  
- **输入限制**：  
  - 图像 URL 必须公网可访问，且不含中文等非 ASCII 字符（需 URL 编码）；  
  - 图像格式支持 PNG、JPG、JPEG、WEBP、BMP（部分模型如 Z-Image 仅限 PNG，图像翻译 `qwen-mt-image-2.0` 仅限 JPG）；  
  - 分辨率与大小有硬性约束（如人物实例分割要求 `512×512` 至 `4096×4096`，文件 ≤ 10MB）。  
- **免费额度与计费**：  
  - 大部分模型提供 500 张/90 天免费额度（主账号与 RAM 子账号共享）；  
  - 部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`）为限时免费，额度用尽即停用；  
  - 计费按成功生成的图片张数结算，失败不计费；  
  - 阶梯计价仅适用于 `aitryon-refiner`（AI试衣精修），用量越大单价越低。  
- **并发与速率限制**：  
  - QPS（每秒任务下发）与并发任务数（同时处理中任务）以主账号为单位限制（如 FaceChain 训练 QPS=2，并发=1；万相编辑 QPS=2，并发=1）；  
  - 超出限制的请求将被拒绝或排队，不会丢失。  
- **模型弃用提示**：万相 V1 版（`wanx-v1`）已明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，开发者应避免新项目接入。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)


