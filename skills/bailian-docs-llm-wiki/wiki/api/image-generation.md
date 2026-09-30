# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意文字生成及垂直场景工具（如虚拟模特、AI试衣、人物写真等）。核心模型包括千问图像系列、万相系列、Z-Image、可灵、Vidu、FaceChain 和 WordArt 锦书等，支持同步/异步调用、多地域部署及 OpenAI 兼容协议。所有服务均需严格匹配模型、API Key 与 Endpoint 的地域。

## 支持的模型/功能

- **通用文生图与编辑**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0`（千问-图像生成与编辑3.0）同时支持 T2I 和 I2I，具备强文本渲染与语义遵循能力 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - `wan2.7-image-pro`（万相2.7）支持文生图（最高4K）、组图生成、多图参考生成；`wan2.6-t2i`（万相2.6文生图V2）支持自由尺寸选择（总像素 1280×1280 至 1440×1440）；  
  - `z-image-turbo` 是轻量级文生图模型，强调快速响应与中英文字渲染。

- **专业图像编辑与增强**：  
  - `qwen-image-edit-max`、`wan2.5-i2i-preview`、`wanx2.1-imageedit` 支持指令编辑、局部重绘、风格迁移、去水印等；  
  - `image-out-painting`（图像画面扩展）支持按方向/比例扩图；`image-erase-completion` 支持精准擦除补全；  
  - `vidu/vidu-image-pro_reference2image` 等 Vidu 系列在 UI/图表像素级还原与上下文一致性方面表现突出。

- **垂直场景工具**：  
  - `aitryon-plus`（AI试衣-Plus版）提升布料纹理与 Logo 还原效果；`facechain-generation` 支持基于 2 张照片训练专属人像并批量生成写真；  
  - `wordart-semantic`（文字变形）与 `wordart-texture`（文字纹理生成）专用于汉字创意设计；  
  - `wanx-background-generation-v2` 面向电商场景，支持文本/图像/边缘引导的背景生成。

> **注意**：文档中 `wanx-v1`（万相V1）明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，且其仅限北京地域、不支持新业务空间域名，属已逐步淘汰的旧版模型，实际开发应优先选用 V2 或更高版本。

## 关键参数

- **`size`**：控制输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。不同模型约束不同：  
  - 千问系列要求总像素在 `512×512` 至 `2048×2048` 之间；  
  - 万相 V2.6 要求总像素在 `[1280×1280, 1440×1440]` 区间；  
  - 可灵与 Vidu 支持 `1K/2K/4K` 分辨率档位，宽高比限定为 `16:9`、`9:16` 或 `1:1`；  
  - 若未指定 `size`，多数模型按输入图宽高比或默认值（如 `1024×1024` 或 `1280×1280`）生成。

- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图任务（如 `qwen-image-3.0-pro`、`kling/kling-v3-image-generation`），取值 `1–9`；`series_amount` 专用于可灵 `omni` 模式下的分镜组图生成（`2–9`）。

- **`input.messages` 结构**：统一采用消息数组格式（即使单轮），`content` 字段内嵌 `text`（提示词）和 `image`（参考图 URL 或 base64），例如 Vidu 和可灵均要求 `messages` 数组有且仅有一个对象 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。

- **`X-DashScope-Async`**：HTTP 异步调用必需头字段，值必须为 `"enable"`；缺失将报错 “current user api does not [support](../guides/support.md) synchronous calls”。

## 使用方式

- **接入协议**：千问图像 3.0 支持 OpenAI 兼容协议（切换 `base_url` 和 `model` 即可迁移），也支持 DashScope 同步/异步调用；其余模型（如万相、可灵、Vidu）主要通过 DashScope HTTP API 接入。

- **调用模式**：  
  - **同步调用**：适用于低延迟场景（如 `qwen-image-3.0`、`wan2.7-image-pro` 文生图、`z-image-turbo`），一次请求即返回结果；  
  - **异步调用**：适用于耗时较长任务（如图像编辑、扩图、AI试衣、FaceChain 训练），流程为 **创建任务 → 轮询查询结果**，任务 ID 有效期通常为 24 小时。

- **地域与域名**：  
  - 所有模型、API Key、Endpoint 必须同地域（华北2/北京、新加坡、美国弗吉尼亚等），跨地域调用将失败；  
  - **强烈建议迁移至业务空间专属域名**：如北京地域使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` 替代 `https://dashscope.aliyuncs.com`，以获得更高性能与稳定性 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

- **SDK 与环境配置**：推荐安装 DashScope SDK（Python/Java），并配置 `DASHSCOPE_API_KEY` 环境变量；若直接 HTTP 调用，需确保 `Authorization: Bearer <key>` 头正确设置。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key 与请求地址，不可混用。例如，万相 2.6 图像编辑模型明确说明“华北2（北京）、新加坡和美国（弗吉尼亚）地域拥有独立的 API Key 与请求地址，不可混用” [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。

- **免费额度与计费**：  
  - 多数模型（如 `wanx-style-repaint-v1`、`aitryon`、`facechain-generation`）提供 90 天内 400–500 张免费额度，额度用尽后自动转为按量付费；  
  - 部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`、`image-instance-segmentation`）明确标注“仅供免费体验，额度用完后不可调用且不支持付费”，需提前规划替代方案。

- **输入限制**：  
  - 图像 URL 必须公网可访问、支持 HTTP/HTTPS，且不含中文字符（否则需 URL 编码）；  
  - 文件格式常见支持 JPG/PNG/WEBP/BMP，尺寸上限多为 `4096×4096` 像素、大小 ≤10 MB；  
  - FaceChain 训练要求人脸正面、无遮挡、分辨率 ≥256×256，且需上传 1–10 张合规图片 [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)。

- **模型弃用风险**：早期模型（如 `wanx-v1`、`qwen-image-2.0` 系列部分旧版本）虽仍可调用，但文档中已多次提示“推荐使用新版”，且其功能、性能、地域支持均受限，生产环境应避免依赖。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)


