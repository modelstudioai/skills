# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全栈场景。核心模型包括千问图像系列、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列垂直创意工具（如FaceChain、WordArt、AI试衣等），支持同步/异步调用、多地域部署与业务空间专属域名接入。

## 支持的模型/功能

- **通用文生图与编辑**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0`（支持T2I/I2I一体化，推荐使用）[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - `wan2.7-image-pro`（支持4K文生图）、`wan2.6-t2i`（V2版，自由尺寸）；  
  - `z-image-turbo`（轻量快速模型，适合高频低延迟场景）；  
  - `kling/kling-v3-omni-image-generation`（支持多图参考与分镜组图）；  
  - `vidu/vidu-image-pro_reference2image`（强文字渲染与UI/图表像素级还原）。

- **专业图像编辑与增强**：  
  - `qwen-image-edit-max`、`wan2.5-i2i-preview`（多图融合与精确指令编辑）；  
  - `image-out-painting`（画面扩展/扩图）、`image-erase-completion`（擦除补全）；  
  - `wanx-style-repaint-v1`（人像风格重绘）、`wanx-background-generation-v2`（背景生成）。

- **垂直创意工具**：  
  - `facechain-generation`（人物写真，支持免训练trainfree模式）；  
  - `wordart-semantic`（文字变形）、`wordart-texture`（文字纹理）；  
  - `aitryon-plus`（高质AI试衣）、`shoemodel-v1`（鞋靴模特）；  
  - `virtualmodel-v2`（虚拟模特，支持2048px短边与多比例输出）。

> **注意**：部分早期模型（如 `wanx-v1`、`qwen-image-2.0` 系列）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”或“当前与新版能力相同”，实际开发应优先选用带 `-pro`、`-v3` 或 `2.7+` 后缀的模型，避免依赖已归档能力。

## 关键参数

- **`size`**：指定输出分辨率（如 `"1024*1024"`），单位像素。不同模型约束不同：  
  - 千问系列：总像素需在 `512×512` 至 `2048×2048` 之间；  
  - 万相V2.7：`wan2.7-image-pro` 文生图支持4K（如 `3840*2160`），编辑场景限2K；  
  - Vidu/可灵：明确支持 `1K`/`2K`/`4K` 分辨率及 `16:9`/`9:16`/`1:1` 宽高比；  
  - Z-Image：同千问，`[512×512, 2048×2048]` 总像素范围。

- **`n`**：控制生成张数（仅部分模型支持）：  
  - `kling/kling-v3-image-generation`：`n=1~9`；  
  - `wordart-semantic`：`n=1~4`（默认4）；  
  - 多数编辑类模型（如 `wan2.5-i2i-preview`）默认单张，不支持批量。

- **`input.messages[].content`**：统一输入结构，支持混合文本（`text`）与图像（`image`，URL或Base64）。例如Vidu和可灵均要求 `messages` 数组仅含一个对象，其 `content` 为文本+图像列表。

- **`X-DashScope-Async`**：HTTP调用必需头字段。值必须为 `"enable"`，否则报错 `"current user api does not support synchronous calls"` —— 此规则在 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md) 和 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md) 中被严格强调。

## 使用方式

- **接入协议**：  
  - 推荐使用 **DashScope同步调用**（功能最完整，支持Base64/URL双输入）或 **OpenAI兼容协议**（仅限千问3.0系列，需切换 `base_url` 和 `model`）；  
  - 异步调用适用于耗时较长任务（如编辑、扩图、海报生成），流程为 **创建任务 → 轮询结果**；同步调用适用于T2I等中低延迟场景（如 `wan2.7-image-pro`、`z-image-turbo`）。

- **地域与域名**：  
  - 必须保证 **模型、Endpoint URL、API Key 属于同一地域**，跨地域调用将失败；  
  - 强烈建议迁移至 **业务空间专属域名**（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 —— 该要求在 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)、[万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md) 等多篇文档中重复强调。

- **认证与配置**：  
  - 所有调用需配置 `Authorization: Bearer $DASHSCO_API_KEY`；  
  - SDK用户需安装 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md) 并设置环境变量；  
  - HTTP用户需确保 `Content-Type: application/json`。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与 Endpoint **不可混用**。例如万相2.6明确说明三地独立鉴权，跨地域将导致“鉴权失败或服务报错”；而万相2.5仅支持北京/新加坡，弗吉尼亚未列支持。

- **免费额度与限流**：  
  - 多数创意工具（如 `wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1`）为“**仅供免费体验**”，额度用尽后不可调用且不支持付费；  
  - 限流按 **主账号与RAM子账号共用**，例如 `aitryon` 的RPS限制为10，`facechain-finetune` 的并发任务数上限为1；  
  - 免费额度有效期统一为 **90天**（自开通或审批通过后下一个整点生效）。

- **输入规范**：  
  - 图像URL需公网可访问、无中文路径（需URL编码），格式限 `jpg/png/jpeg/webp/bmp/avif`；  
  - FaceChain人脸检测要求单人脸、正面、≥128×128像素、无遮挡；  
  - WordArt文字变形对 `input.text` 长度无硬性限制，但 `input.prompt` 严格限定为1–200字。

- **模型弃用风险**：  
  > **注意**：文档中多次出现“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”、“当前与qwen-image-2.0-pro-2026-04-22能力相同”等表述，表明 `wanx-v1`、`qwen-image-2.0` 等旧版模型已进入维护期，新项目应避免直接依赖其文档细节，而以新版API为准。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
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
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片精修API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/ai-fitting-picture-finishing-api-details.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)
- [人物形象训练API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)
- [人物写真生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)
- [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)
- [快速开始](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-quick-start.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [文字纹理生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/fill-texture-effect-api.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)


