# image generation

百炼平台提供多种图像生成与编辑能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、文字渲染等核心场景。所有服务均通过统一的 API 接口接入，支持同步/异步调用，并需严格遵循地域隔离原则（API Key、Endpoint、Workspace ID 必须同属一地域）。开发者应优先选用 `wan2.7-image-pro`、`qwen-image-3.0-pro` 或 `vidu/vidu-image-pro_reference2image` 等新一代模型，其在分辨率、语义一致性与多模态理解上具备显著优势。

## 支持的模型/功能

平台图像能力分为通用生成、专业编辑与垂直工具三大类：

- **通用文生图与编辑**：  
  - `wan2.7-image-pro` / `wan2.7-image`（万相2.7）：支持4K文生图、组图生成、多图参考生成，[万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)  
  - `qwen-image-3.0-pro` / `qwen-image-3.0`（千问3.0）：同时支持T2I与I2I，强调复杂文本渲染与真实质感，[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)  
  - `vidu/vidu-image-pro_reference2image`（Vidu Pro）：专注UI/图表像素级还原与工业级稳定性，适合专业设计场景，[Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)

- **轻量与专项模型**：  
  - `z-image-turbo`：轻量级文生图，响应快，支持中英文字渲染；  
  - `kling/kling-v3-omni-image-generation`：支持多图输入与分镜组图生成；  
  - `qwen-mt-image-2.0`：专用于图像翻译，保留原始排版，[千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

- **创意工具与垂直能力**：  
  包括虚拟模特、AI试衣（`aitryon-plus`）、人物写真（`facechain-generation`）、文字艺术（`wordart-semantic`）、背景生成、擦除补全等，均以独立API提供，详见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：`wanx-v1`（万相V1）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，且其文档注明“仅适用于华北2（北京）地域”，而V2及后续版本（如wan2.6-t2i、wan2.7）已支持多地域（北京、新加坡、弗吉尼亚），功能与性能全面超越V1，故V1不应作为新项目选型。

## 关键参数

所有图像API共用以下核心参数结构（以JSON Body形式提交）：

- `model`（必选）：字符串，指定模型名称，如 `"wan2.7-image-pro"`、`"qwen-image-3.0-pro"`；
- `input`（必选）：对象，包含：
  - `messages`（数组）：单轮对话格式，`content` 中含 `text`（提示词）和可选 `image`（Base64或公网URL）；
  - `prompt`（部分旧模型如`wanx-v1`）：直接传入字符串提示词；
- `parameters`（可选）：控制生成行为：
  - `size`：字符串，格式 `"宽*高"`（如 `"1024*1024"`），单位像素；各模型约束不同：
    - 千问系列：总像素需在 `512*512` 至 `2048*2048` 之间；
    - 万相V2.6+：宽高比范围 `[1:4, 4:1]`，总像素在 `[1280*1280, 1440*1440]`；
    - Vidu/可灵：支持 `1K/2K/4K` 分辨率，宽高比限 `16:9`、`9:16`、`1:1`；
  - `n`：整数，生成图像张数（通常 `1–9`，部分模型如`z-image-turbo`固定为1）；
  - `seed`：整数，用于结果复现（非所有模型支持）。

## 使用方式

### 调用协议与流程
- **同步调用**：适用于耗时较短（通常 < 30s）的模型，如 `wan2.7-image-pro`、`qwen-image-3.0-pro`（DashScope同步模式）、`z-image-turbo`。一次HTTP POST即可返回图像URL。
- **异步调用**：适用于耗时较长（通常 1–2分钟）的模型，如 `wan2.5-i2i-preview`、`kling/kling-v3-image-generation`、`facechain-finetune`。必须包含请求头 `X-DashScope-Async: enable`，流程为：
  1. 提交任务 → 获取 `task_id`；
  2. 轮询 `GET /api/v1/tasks/{task_id}` → 直至状态为 `SUCCESS`，返回图像URL（有效期24小时）。

### 地域与域名配置
- **强制同地域**：API Key、Endpoint URL、Workspace ID 必须属于同一地域（北京、新加坡、弗吉尼亚等），跨地域调用必然失败。
- **推荐域名**：务必迁移至业务空间专属域名（非 `dashscope.aliyuncs.com`）：
  - 北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
  - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
  - （详情见 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）

### SDK与环境
- 安装 `dashscope` Python/Java SDK（[安装指南](../../raw/model-api-reference/preparations/install-sdk.md)）；
- 配置环境变量 `DASHSCOPE_API_KEY`（[配置方法](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)）；
- 示例代码中需替换 `DASHSCOPE_API_HOST` 为实际业务空间域名。

## 限制和注意事项

- **地域隔离**：所有模型均严格绑定地域。例如，`wan2.5-i2i-preview` 文档明确指出“华北2（北京）和新加坡地域拥有独立的 API Key 与请求地址，不可混用”，违反将导致鉴权失败。
- **免费额度与计费**：多数模型提供90天内500张免费额度（主账号与RAM子账号共享），用尽后按量付费。单价差异显著：
  - 基础文生图（`wanx2.1-t2i-turbo`）：0.16元/张；
  - AI试衣Plus（`aitryon-plus`）：0.50元/张；
  - FaceChain训练（`facechain-finetune`）：2.5元/次；
  - （详见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md) 与各模型计量计费文档）
- **输入限制**：
  - 图像URL必须公网可访问、无中文路径（需URL编码），格式支持 JPG/PNG/WEBP/BMP；
  - 提示词长度建议 ≤ 200 字，避免冗余描述；
  - 多图输入时，千问3.0支持1–3张参考图，Vidu/可灵支持更多。
- **特殊限制**：
  - `wanx-x-painting`（局部重绘）、`wanx-poster-generation-v1` 等模型明确标注“免费体验，额度用完后不可调用且不支持付费”，生产环境应规避；
  - `facechain-generation` 需先[申请体验](https://bailian.console.aliyun.com/model/market/detail/facechain-generation)审批通过方可调用。

## 来源文档

- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)


