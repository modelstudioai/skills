# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及垂直场景工具（如虚拟模特、海报生成等）。核心模型包括千问（Qwen-Image）、万相（WanX）、Z-Image、Vidu、可灵（Kling）及FaceChain等，支持同步与[异步调用](../concepts/asynchronous-invocation.md)，适配不同性能、精度与成本需求。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro` 和 `qwen-image-3.0` 同时支持T2I与I2I，具备强文本渲染与语义遵循能力；`wan2.7-image-pro` 在文生图场景下支持4K输出，而组图/编辑限2K [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **轻量与极速模型**：`z-image-turbo` 为轻量级模型，兼顾速度与中英文字渲染；`wan2.2-t2i-flash` 较2.1提速50%；`wan2.6-t2i` 支持自由选尺寸（如768×2700），突破单边1400像素限制 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。  
- **垂直场景工具**：创意工具类模型包括人像风格重绘（`wanx-style-repaint-v1`）、虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）、图像擦除补全（`image-erase-completion`）及FaceChain人物写真（需先训练`facechain-finetune`）等。  
- **专业编辑能力**：`wan2.5-i2i-preview` 支持单图编辑与多图融合；`qwen-image-2.1-pro` 和 `qwen-image-2.1-turbo` 均支持最多10张参考图输入；`vidu/viduq2-pro_reference2image` 擅长复杂逻辑与工业级稳定性 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。  

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-erase-completion`）当前仅提供免费体验，额度用完后不可调用且不支持付费，官方明确建议迁移到千问或万相2.1等替代方案。

## 关键参数

- **`size`**：控制输出分辨率。格式因模型而异：`qwen-image-*` 接受总像素范围（512×512 至 2048×2048）；`wan2.7-image-pro` 支持 `"2K"`、`"4K"` 字符串；`wan2.5-i2i-preview` 接受 `"宽*高"`（如 `"1280*1280"`）；`kling/kling-v3-*` 和 `vidu/*` 支持 `"1k"`/`"2k"`/`"4k"` 及宽高比（`16:9`/`9:16`/`1:1`）。未指定时，多数模型按输入图宽高比默认生成（如 `qwen-image-2.0-pro` 默认2048×2048，`wan2.5-i2i-preview` 默认1280×1280）。  
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，取值1–9）；`series_amount` 专用于 `kling/kling-v3-omni-image-generation` 的分镜组图（2–9）。  
- **`watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认开启，可通过 `parameters.watermark=false` 关闭）。  
- **`thinking_mode`**：`wan2.7-image-pro` 特有参数，启用后返回推理过程描述（非必需）。  
- **`element_list`**：`kling/kling-v3-omni-image-generation` 中用于指定需保持一致的主体列表，与参考图数量之和 ≤10。  

## 使用方式

- **接入协议**：主流模型均支持 DashScope SDK（Python/Java）与 HTTP 调用；千问系列额外提供 OpenAI 兼容模式（仅同步，通过 `/images/generations` 接口，传 `image` 字段即为图生图）[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **调用模式**：  
  - **同步调用**：适用于 `qwen-image-*`、`wan2.7-image-*`、`wan2.6-image`、`z-image-turbo` 等，一次请求返回结果，推荐大多数场景。Endpoint 示例：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。  
  - **[异步调用](../concepts/asynchronous-invocation.md)**：适用于耗时较长的模型（如 `wan2.5-i2i-preview`、`kling/*`、`vidu/*`、所有创意工具类模型），需两步：① `POST .../generation` 创建任务获 `task_id`；② 轮询 `GET .../tasks/{task_id}` 获取结果（URL有效期24小时）。  
- **地域与域名**：必须确保模型、API Key、Endpoint URL 属于同一地域（北京/新加坡/弗吉尼亚等）。强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧域名（`dashscope.aliyuncs.com`），以获得更高性能与稳定性。  

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key 与 Endpoint **不可混用**，跨地域调用将导致鉴权失败或服务报错。  
- **输入限制**：  
  - 图像格式：PNG（主流）、JPEG/JPG（部分模型）；不支持透明通道（如 `kling/kling-v3-image-generation` 明确禁止）。  
  - 图像尺寸：`kling` 要求参考图宽高在 `[300, 8000]` 像素；`vidu` 最多支持14张参考图；`wan2.5-i2i-preview` 多图输入时默认按最后一张图宽高比生成。  
  - 文本长度：`kling` 提示词上限2500字符，`vidu` 为5000字符。  
- **免费额度与计费**：多数创意工具模型（如 `wanx-style-repaint-v1`、`image-instance-segmentation`）提供500张免费额度；FaceChain训练为2.5元/次，检测限时免费；具体计费单价与限流（QPS/并发数）详见各模型文档。  
- **模型弃用**：万相V1（`wanx-v1`）已不推荐使用，应升级至V2（`wan2.6-t2i`）；千问早期模型（如 `qwen-image-2.0` 系列）虽仍可用，但新功能与优化集中于3.0系列。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
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
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)


