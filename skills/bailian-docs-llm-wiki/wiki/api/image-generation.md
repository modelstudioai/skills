# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、创意工具及专业领域模型（如试衣、写真、文字艺术等）。所有服务均通过统一的 API 接口调用，支持同步与异步两种模式，需严格遵循地域隔离原则（模型、API Key、Endpoint 必须同地域）。

## 支持的模型/功能

平台图像能力分为三大类：

- **通用生成与编辑模型**：  
  - 千问系列：`qwen-image-3.0-pro`、`qwen-image-3.0`（同时支持 T2I 和 I2I），[千问-图像生成与编辑3.0](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；早期模型如 `qwen-image-2.0-pro` 仍可调用，但推荐迁移至 3.0 系列。  
  - 万相系列：`wan2.7-image-pro`（支持 4K 文生图）、`wan2.6-t2i`（V2 文生图主力模型）、`wan2.5-i2i-preview`（多图融合编辑），详见 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。  
  - 可灵与 Vidu：`kling/kling-v3-omni-image-generation`（支持分镜组图）、`vidu/vidu-image-pro_reference2image`（强文字渲染与 UI 还原），二者均聚焦高精度设计场景。

- **创意工具与垂直模型**：  
  包括人像风格重绘、虚拟模特、鞋靴模特、AI试衣（`aitryon-plus`）、人物写真 FaceChain、图像背景生成、画面扩展（扩图）、擦除补全等。其中部分模型（如 `wanx-x-painting`、`shoemodel-v1`、`wanx-virtualmodel`）当前仅限免费体验，额度用尽后不可调用，[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md) 明确提示此限制。

- **轻量与专用模型**：  
  `z-image-turbo`（快速生图，支持灵活分辨率）、`wordart-semantic`（文字变形）、`wordart-texture`（文字纹理生成）等，适用于对延迟敏感或特定设计需求的场景。

> **注意**：文档中存在模型命名不一致问题。例如文档 3 和 6 均提及 `qwen-image-2.0-pro-2026-04-22`，但文档 3 称其“当前与 `qwen-image-2.0-pro` 能力相同”，而文档 6 未明确该映射关系；实际调用时应以最新版 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 中列出的 `qwen-image-3.0-pro` 为准，避免使用已标注为“早期”的模型变体。

## 关键参数

- **`model`**：必填，指定模型名称（如 `"qwen-image-3.0-pro"` 或 `"wan2.7-image-pro"`），不同模型能力差异显著，不可混用。
- **`size`**：控制输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。各模型约束不同：
  - 千问系列：总像素需在 `512×512` 至 `2048×2048` 之间；
  - 万相 V2 (`wan2.6-t2i`)：宽高比限定 `[1:4, 4:1]`，总像素在 `[1280×1280, 1440×1440]`；
  - 可灵/ Vidu：支持 `1K/2K/4K` 预设档位，宽高比限 `16:9`、`9:16`、`1:1`。
- **`n`**：生成图像张数，多数模型支持 `1–9` 张（如可灵），但 `z-image-turbo` 固定为 1 张。
- **`input` 结构**：  
  - 文生图：`{"messages": [{"role": "user", "content": [{"text": "prompt"}]}]}`；  
  - 图生图/编辑：`content` 数组中需包含 `{"image": "url_or_base64"}` 和可选 `{"text": "edit_instruction"}`；  
  - 多图输入（如万相 2.5 编辑）：`content` 中可传入多个 `image` 对象。
- **异步必需头**：HTTP 调用时，`X-DashScope-Async: enable` 为强制要求，缺失将报错 `"current user api does not support synchronous calls"`。

## 使用方式

- **接入协议**：支持 OpenAI 兼容协议（仅同步）、DashScope 同步调用（推荐，功能最全）和 DashScope 异步调用（适用于耗时 >1 分钟的任务）。
- **地域与域名**：必须确保模型、API Key、Endpoint 同地域。强烈建议迁移至业务空间专属域名（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确指出其“提供卓越性能和更高稳定性”。
- **调用流程**：  
  - 同步调用（如千问、万相 2.7）：单次 POST 请求，直接返回结果；  
  - 异步调用（如万相 V1/V2、可灵、Vidu、多数创意工具）：需两步——① 创建任务获取 `task_id`，② 轮询 `task_id` 查询结果（URL 有效期 24 小时）。
- **SDK 依赖**：推荐安装 DashScope SDK（Python/Java），但部分模型（如人像风格重绘）明确声明“仅提供 HTTP API，暂无 SDK”。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key 与 Endpoint **不可混用**，跨地域调用必然失败（文档 9、10、11 多次强调）。
- **免费额度与限流**：  
  - 多数模型提供 500 张免费额度（90 天），但部分工具模型（如 `wanx-x-painting`、`shoemodel-v1`）额度用尽即停用，且不支持付费；  
  - QPS/RPS 限制以主账号+RAM 子账号为单位共享（如 `aitryon` RPS=10，`facechain-finetune` QPS=2）。
- **输入规范**：  
  - 图像 URL 必须公网可访问、支持 HTTPS、无中文路径（需 URL 编码）；  
  - 提示词长度、图像分辨率、文件大小均有硬性限制（如 FaceChain 检测要求人脸 ≥128×128 像素，图像 ≤5MB）。
- **模型状态**：V1 版本模型（如 `wanx-v1`）已明确标注“推荐使用全面升级的 V2 版”，应避免新项目接入。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


