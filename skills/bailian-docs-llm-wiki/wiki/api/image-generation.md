# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘及专业创意工具等场景。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 和 FaceChain 等系列，支持同步与异步调用，适配不同性能、精度与成本需求。

## 支持的模型/功能

- **千问（Qwen-Image）**：主打高质量文生图与图像编辑一体化能力，支持 `qwen-image-3.0-pro`（推荐）、`qwen-image-3.0`、`qwen-image-2.1-pro` 等版本，兼容 OpenAI Images 协议与 DashScope SDK [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **万相（WanX）**：覆盖全栈图像生成需求，包括文生图 V2（`wan2.6-t2i`）、图像生成与编辑 2.7（`wan2.7-image-pro`，支持 4K 文生图）、通用图像编辑 2.5（`wan2.5-i2i-preview`）及涂鸦作画（`wanx-sketch-to-image-lite`）等 [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)。  
- **可灵（Kling）与 Vidu**：专注高保真图文生成与参考图生图，支持分镜组图、UI/图表像素级还原及中英文字精准渲染，仅限华北2（北京）地域 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。  
- **Z-Image**：轻量级文生图模型，强调低延迟与多分辨率适配，适用于快速原型验证与高频调用场景 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。  
- **创意工具套件**：含人像风格重绘、虚拟模特、鞋靴试穿、创意海报生成、人物实例分割、图像擦除补全等垂直能力；FaceChain 支持基于 2 张照片训练专属人像模型，实现高相似度写真生成。

> **注意**：万相-文生图V1版（`wanx-v1`）已明确标注为“推荐使用全面升级的[文生图V2版模型](text-to-image-v2-api-reference.md)” [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)，V1 版仅限北京地域且不支持新域名迁移，属过时接口，应避免在新项目中采用。

## 关键参数

- **`model`**：必填字符串，指定模型名称（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`），需与所选 endpoint 地域严格匹配。  
- **`size` / `parameters.size`**：控制输出分辨率，格式为 `"宽*高"`（像素），不同模型约束不同：
  - Qwen-Image：总像素 512×512 至 2048×2048，未指定时自动推荐；
  - Wan2.6-t2i：总像素限定在 [1280×1280, 1440×1440]；
  - Wan2.7-image-pro：文生图支持 4K（3840×2160 或等效），编辑/组图限 2K；
  - Kling/Vidu：支持 1K/2K/4K，需显式指定宽高比（16:9、9:16、1:1）；
  - Z-Image：总像素 512×512 至 2048×2048。  
- **`n` / `series_amount`**：控制生成张数（`n` 用于单图模式，`series_amount` 用于 Kling 分镜组图，范围 2–9）。  
- **`input`**：图像输入字段，支持公网 URL 或 Base64 编码（部分模型如 Qwen-Image 的 OpenAI 兼容方式支持两者；万相 2.5+ 仅支持 URL）。  
- **`X-DashScope-Async`**：HTTP 调用必需头，异步请求必须设为 `"enable"`；缺失将报错 `"current user api does not support synchronous calls"`（见 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)）。

## 使用方式

- **同步调用**：适用于响应时间敏感、图像复杂度较低的场景（如 Z-Image、Qwen-Image Pro、Wan2.7-image）。请求地址统一为 `POST https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（北京/新加坡/弗吉尼亚等），需配置 `Content-Type: application/json` 与 `Authorization: Bearer <API-Key>`。  
- **异步调用**：适用于耗时较长任务（通常 1–2 分钟），如万相 2.5 编辑、可灵、Vidu、创意工具类模型。流程为两步：  
  1. `POST /api/v1/services/aigc/{service}/generation` 提交任务，获取 `task_id`；  
  2. `GET /api/v1/tasks/{task_id}` 轮询状态，成功后返回 PNG 图像 URL（有效期 24 小时）。  
- **SDK 调用**：DashScope Python/Java SDK 支持多数模型（Qwen、WanX、Z-Image），但部分创意工具（如人像风格重绘、虚拟模特）明确声明“仅提供 HTTP API，暂无 SDK” [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。  
- **地域与域名**：所有模型均要求 **API Key、Endpoint、模型部署地域三者严格一致**。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key、Endpoint、模型列表完全独立，跨地域调用必然失败。万相 2.6 明确指出“华北2（北京）、新加坡和美国（弗吉尼亚）地域拥有独立的 API Key 与请求地址，不可混用” [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。  
- **免费额度与限流**：大量创意工具模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`image-erase-completion`）仅提供 500 张免费额度，用完即停且不支持付费，文档中多次提示“推荐参考[图像编辑-千问]或[图像编辑-万相2.1]获取替代方案” [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。  
- **输入规范**：FaceChain 要求训练图像为单人脸、正面、≥128×128 像素、无遮挡；万相涂鸦作画、局部重绘等需提供精确涂抹掩码（mask）；所有图像 URL 必须公网可访问且格式为 JPEG/PNG/WEBP。  
- **输出一致性**：Qwen-Image 2.0 系列存在多个时间戳后缀模型（如 `qwen-image-2.0-pro-2026-06-22`），文档注明“当前与 `qwen-image-2.0-pro-2026-04-22` 能力相同”，表明模型能力可能滞后于命名，应以实际测试为准，而非仅依赖版本号。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)


