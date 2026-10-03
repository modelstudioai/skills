# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景能力。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列垂直创意工具（如 FaceChain、WordArt、AI试衣等），支持同步与异步调用，适配不同性能与质量需求。

## 支持的模型/功能

平台图像生成能力分为通用基础模型与垂直创意工具两大类：

- **通用基础模型**：  
  - **千问系列**：`qwen-image-3.0-pro`（推荐）同时支持文生图与图生图/编辑，支持最多10张参考图输入；`qwen-image-2.1-pro` 支持自动透明通道输出 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
  - **万相系列**：`wan2.7-image-pro` 支持文生图4K高清输出；`wan2.5-i2i-preview` 支持单图编辑与多图融合；`wanx-sketch-to-image-lite` 专用于涂鸦作画 [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。  
  - **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/viduq2-pro_reference2image` 擅长复杂逻辑与工业级稳定性。  
  - **Z-Image**：`z-image-turbo` 是轻量级文生图模型，强调快速响应与中英文字渲染 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。

- **垂直创意工具**：  
  - **人物相关**：FaceChain 支持基于2张照片训练专属形象并批量生成写真；虚拟模特、鞋靴模特实现商品图AI换模；人像风格重绘支持艺术化转换。  
  - **文字与设计**：WordArt 锦书提供文字变形与纹理生成；创意海报生成、图像背景生成、图像画面扩展（扩图）满足电商与营销需求。  
  - **图像处理**：图像擦除补全、人物实例分割、图像局部重绘（`wanx-x-painting`）等辅助能力均以异步方式提供。

> **注意**：部分模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`wanx-x-painting`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议使用[图像编辑-千问](../../raw/model-user-guide/model-experience/image-model/image-edit-guide/qwen-image-edit-guide.md)或[图像编辑-万相2.1](../../raw/model-user-guide/model-experience/image-model/image-edit-guide/wanx-image-edit.md)作为替代方案。

## 关键参数

各模型共性关键参数如下（具体取值范围依模型而异）：

- **`model`**：必选字符串，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`）。  
- **`input`**：必选对象，结构因任务类型而异：  
  - 文生图：通常含 `prompt` 字段（文本提示词）；  
  - 图生图/编辑：含 `image_url` 或 `base64` 图像数据，及可选 `prompt` 编辑指令；  
  - 多模态任务（如 FaceChain、WordArt）：含 `text`、`image`、`prompt` 等组合字段。  
- **`size`**：可选字符串，指定输出分辨率（格式如 `"1024*1024"`）。约束因模型而异：  
  - 千问系列：总像素需在 `512*512` 至 `2048*2048` 之间；  
  - 万相 V2：宽高比支持 `[1:4, 4:1]`，总像素在 `[1280*1280, 1440*1440]`；  
  - Wan2.7 Pro 文生图支持4K（如 `3840*2160`），但编辑与组图限2K。  
- **`n`**：可选整数，指定生成图片张数（常见于文生图，如 `1–9`）；部分模型（如 `image-out-painting`）通过 `parameters.n` 控制。  
- **`parameters`**：可选对象，承载模型特有参数（如 WordArt 的 `steps` 迭代次数、`font_name`；FaceChain 的 `style_type`）。

## 使用方式

所有图像生成 API 均要求严格地域对齐：**模型、Endpoint URL 与 API Key 必须属于同一地域**（如华北2北京、新加坡、美国弗吉尼亚），跨地域调用将失败 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

- **同步调用**：适用于低延迟场景（如实时预览），支持 DashScope SDK 与 HTTP（部分模型）。  
  - 示例（万相2.7）：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`，需配置 `X-DashScope-Async: disable`（默认）。  
  - 注意：Z-Image、千问 DashScope 同步调用均支持 Base64 与公网 URL 输入。

- **异步调用**：适用于耗时较长任务（通常 1–2 分钟），为绝大多数图像编辑、扩图、精修等模型的**唯一支持方式**。流程为两步：  
  1. **创建任务**：发送请求获取 `task_id`；  
  2. **轮询结果**：用 `task_id` 查询状态，成功后返回图像 URL（有效期 24 小时）。  
  - 所有异步请求必须携带 `X-DashScope-Async: enable` 请求头，缺失将报错：“current user api does not [support](../guides/support.md) synchronous calls”。

- **SDK 与环境配置**：  
  - 推荐安装 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，支持 Python/Java；  
  - API Key 需配置至环境变量 `DASHSCOPE_API_KEY`；  
  - 业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）已全面推广，性能与稳定性优于旧域名，强烈建议迁移。

## 限制和注意事项

- **地域与密钥隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）、法兰克福等地域拥有独立 API Key 与 Endpoint，不可混用。例如，万相2.6 在美国地域支持 HTTP 同步调用，而法兰克福仅支持异步 [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。  
- **免费额度与计费**：  
  - 免费额度按“成功生成的图片张数”计算，有效期 90 天，主账号与 RAM 子账号共享；  
  - 计费单价差异显著：`wordart-semantic`（0.24元/张） > `aitryon-plus`（0.50元/张） > `wanx-background-generation-v2`（0.08元/张）；  
  - AI试衣-图片精修（`aitryon-refiner`）采用阶梯定价，用量越大单价越低。  
- **输入限制**：  
  - 图像 URL 需公网可访问、支持 HTTP/HTTPS，含中文路径需 URL 编码；  
  - 文件大小：多数模型限制 ≤5MB（如 FaceChain 检测）或 ≤10MB（如人物实例分割）；  
  - 格式：主流支持 JPG/PNG/WEBP/BMP，部分模型（如鞋靴模特）明确排除 AVIF。  
- **模型能力边界**：  
  - 文字渲染能力因模型而异，`qwen-image-3.0-pro` 与 `vidu/viduq2-pro` 对中英文 UI/图表还原最强；  
  - `wanx-sketch-to-image-lite` 仅支持涂鸦引导，不支持纯文本生成；  
  - FaceChain 人物写真需先完成图像检测与形象训练（或使用免训练模式），非开箱即用。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)


