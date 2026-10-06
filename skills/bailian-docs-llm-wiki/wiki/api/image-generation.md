# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意文字生成等核心场景。所有服务均通过统一的 API 接口接入，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到生产级集成的各类开发者需求。

## 支持的模型/功能

百炼当前提供四大类图像生成模型体系：

- **千问系列**：`qwen-image-3.0-pro` 和 `qwen-image-3.0` 同时支持高质量文生图与图生图/编辑，具备强文本渲染与语义遵循能力；早期模型如 `qwen-image-2.0-pro` 仍可调用，但[已明确标注为旧版](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)。  
- **万相系列**：覆盖全栈能力，包括 `wan2.7-image-pro`（支持4K文生图）、`wan2.6-t2i`（V2文生图主力模型）、`wan2.5-i2i-preview`（多图融合编辑）及 `wanx-background-generation-v2`（背景生成）等。其中万相V1模型已不推荐使用，官方明确建议迁移到[V2版](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。  
- **垂直工具类模型**：聚焦特定任务，如 `facechain-generation`（人物写真）、`aitryon-plus`（AI试衣Plus）、`wordart-semantic`（文字变形）、`image-out-painting`（画面扩展）等，均需按场景独立开通与调用。  
- **其他模型**：`vidu/vidu-image-pro_reference2image`（高精度UI/图表生成）、`kling/kling-v3-omni-image-generation`（支持分镜组图）、`z-image-turbo`（轻量级快速生图）等，各具分辨率、速度或领域优势。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，详见对应文档说明。

## 关键参数

所有图像生成API共用以下核心参数结构（具体字段依模型略有差异）：

- `model`（必选）：模型标识符，如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`。
- `input`（必选）：包含提示词与输入图像：
  - `messages` 数组（DashScope协议）：首条 `text` 字段为正向提示词；`image` 字段支持公网URL或Base64编码（部分模型支持多图）。
  - `prompt` 字符串（旧版协议）：直接传入文本提示词。
- `parameters`（可选）：
  - `size`：输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。不同模型约束不同：`qwen-image-3.0-pro` 要求总像素在 `512×512` 至 `2048×2048` 之间；`wan2.6-t2i` 限定在 `[1280×1280, 1440×1440]`；`vidu` 系列支持 `1K/2K/4K` 预设档位。
  - `n`：生成张数，默认为1，范围通常为 `1–9`（如 `kling-v3-omni` 支持组图模式 `series_amount`）。
  - `style` / `font_name` / `generate_mode`：模型特有控制参数，详见各功能文档。

## 使用方式

### 接入前提
- 必须确保 **模型、Endpoint URL 与 API Key 属于同一地域**（如华北2北京、新加坡、美国弗吉尼亚），跨地域调用将失败。  
- 强烈推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），其性能与稳定性优于公共域名 `dashscope.aliyuncs.com` [详见迁移指南](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

### 调用模式
- **同步调用**：适用于 `qwen-image-3.0`、`wan2.7-image-pro`、`z-image-turbo` 等低延迟模型，单次HTTP请求返回结果。  
- **异步调用**：适用于耗时较长的任务（如扩图、试衣、写真生成），流程为：  
  1. `POST /api/v1/services/.../generation` 提交任务 → 获取 `task_id`；  
  2. `GET /api/v1/tasks/{task_id}` 轮询状态 → 返回 `output.results[].url`（有效期24小时）。  
  所有异步接口必须携带请求头 `X-DashScope-Async: enable`，否则报错。

### SDK 与协议
- DashScope Python/Java SDK 全面支持主流模型（除少数工具类模型如 `wanx-style-repaint-v1` 明确声明“仅提供 HTTP API”）。  
- OpenAI 兼容模式仅支持 `qwen-image-3.0` 系列，需切换 `base_url` 并指定 `model="qwen-image-3.0"`。

## 限制和注意事项

- **地域隔离**：API Key、Endpoint、模型三者必须同地域。例如 `wan2.6-t2i` 在弗吉尼亚可用，但 `wan2.7-image-pro` 仅限北京/新加坡，详见各地域[模型列表](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。  
- **免费额度与计费**：所有模型均提供90天内500张免费额度（主账号与RAM子账号共享），额度用尽后按量计费（如 `aitryon-plus` 为0.50元/张，`wordart-texture` 为0.08元/张）。详细计费规则见[计量计费文档](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)。  
- **输入限制**：  
  - 图像URL需公网可访问、无中文路径（需URL编码）；  
  - Base64数据需为标准格式（无 `data:image/png;base64,` 前缀）；  
  - 单图大小通常 ≤5MB（`image-instance-segmentation` 支持≤10MB）。  
- **输出格式**：默认为 PNG，暂不支持 JPEG 或 WebP 输出。  
- **并发与QPS**：各模型独立限流，典型值为 QPS=2、并发任务数=1（如 `facechain-finetune`）至 QPS=10、并发=5（如 `aitryon`），超出将排队或拒绝。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)


