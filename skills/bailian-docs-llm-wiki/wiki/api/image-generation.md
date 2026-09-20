# image generation

百炼平台提供丰富的图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全链路场景。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列垂直创意工具（如 FaceChain、WordArt、AI试衣等），均通过统一的 DashScope API 协议或 OpenAI 兼容协议接入，支持同步/[异步调用](../concepts/asynchronous-invocation.md)。

## 支持的模型与功能

平台图像能力按技术路径和业务场景分为三类：

- **通用生成模型**：面向基础创作需求。
  - `qwen-image-3.0-pro` / `qwen-image-3.0`：支持文生图与图生图一体化，推荐用于高精度图文混合任务 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
  - `wan2.7-image-pro`：万相2.7专业版，文生图支持4K输出；`wan2.6-t2i` 等V2系列模型支持自由宽高比与大尺寸（如768×2700）[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
  - `kling/kling-v3-omni-image-generation`：支持多图输入与分镜组图生成；`vidu/viduq2-pro_reference2image`：擅长复杂逻辑与工业级稳定性 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

- **轻量与专项模型**：兼顾速度、成本或特定任务。
  - `z-image-turbo`：轻量级文生图模型，响应快，支持中英文字渲染 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。
  - `wanx-sketch-to-image-lite`：涂鸦作画专用；`wanx-x-painting`：图像局部重绘（免费体验）；`image-out-painting`：画面扩展（扩图）。

- **垂直创意工具**：面向行业场景深度优化。
  - `facechain-generation`：基于2张照片生成人物写真，支持免训练（trainfree）模式 [人物写真生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)。
  - `aitryon-plus`：AI试衣Plus版，提升布料纹理与Logo还原效果；`wordart-semantic`：文字变形生成黑底白字蒙版图 [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)。
  - `wanx-background-generation-v2`：电商商品背景生成；`image-erase-completion`：擦除补全（免费体验）。

> **注意**：部分早期模型（如 `wanx-v1`、`qwen-image-2.0` 系列）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”或“当前与qwen-image-2.0-pro-2026-04-22能力相同”，表明其功能已被新版本覆盖，文档中列出的旧型号（如 `qwen-image-2.0`）不应作为首选。

## 关键参数

所有图像API共用核心参数结构，关键字段如下：

- `model`（必选）：模型名称，如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`。必须与所选地域的可用模型列表一致。
- `input`（必选）：包含提示词与可选图像输入。
  - `input.prompt`（文生图）：文本描述，支持中英文及复杂细节指令（如“冬日北京的都市街景…左侧为书法店…”）。
  - `input.messages[].content`（多模态模型）：数组形式，含 `text` 字段（提示词）和 `image` 字段（Base64 或公网URL，支持1–3张）。
- `parameters.size`（可选）：指定输出分辨率，格式为 `"宽*高"`（像素）。不同模型约束不同：
  - Qwen-3.0：总像素需在 `512*512` 至 `2048*2048` 之间；
  - Wan2.7 Pro：文生图支持4K（如 `3840*2160`），编辑/组图限2K；
  - Wan2.5 I2I：默认 `1280*1280`，宽高比按输入图自动适配。
- `parameters.n`（可选）：生成张数，范围因模型而异（如 `qwen-image-3.0-pro` 默认1张，`kling` 支持1–9张，`wordart-semantic` 限1–4张）。
- `X-DashScope-Async`（HTTP调用必选）：值必须为 `"enable"`，否则报错 `"current user api does not support synchronous calls"`。

## 使用方式

### 接入协议与方式
- **同步调用**：适用于 `qwen-image-3.0`、`wan2.7-image-pro`、`z-image-turbo` 等低延迟模型，单次请求返回结果。Endpoint 示例：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
- **[异步调用](../concepts/asynchronous-invocation.md)**：适用于耗时较长的任务（如编辑、扩图、试衣），需两步操作：
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. `GET /api/v1/tasks/{task_id}` 轮询状态，成功后返回图像URL（有效期24小时）。
- **OpenAI 兼容**：仅支持 `qwen-image-3.0` 系列，切换 `base_url` 和 `model` 即可迁移，图像输入支持公网URL与Base64。

### 地域与认证要求
- **严格地域绑定**：模型、API Key、Endpoint URL 必须属于同一地域（如华北2北京、新加坡、美国弗吉尼亚）。跨地域调用将鉴权失败 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **推荐使用业务空间专属域名**：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`（北京）或 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`（新加坡），性能与稳定性优于公共域名 `dashscope.aliyuncs.com`。
- **API Key 配置**：必须通过环境变量（如 `DASHSCOPE_API_KEY`）或请求头 `Authorization: Bearer <key>` 传递，且需与所选地域匹配。

## 限制和注意事项

- **免费额度与计费**：多数模型提供90天内500张免费额度（主账号与RAM子账号共享），用尽后按量付费。单价差异显著：`aitryon-plus` 为0.50元/张，`aitryon-parsing-v1` 仅0.004元/张，`wordart-semantic` 为0.24元/张 [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)。
- **并发与速率限制**：以账号为单位限制，例如 `facechain-finetune` 并发任务数为1，`aitryon` RPS限制为10 [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)。
- **输入规范**：
  - 图像URL需公网可访问、无中文路径（需URL编码），格式支持 JPG/PNG/WEBP/BMP/AVIF；
  - 提示词长度通常限200字符内（如 `wordart-semantic`）；
  - FaceChain 训练图要求单人脸、正面、≥128×128像素、无遮挡 [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)。
- **功能可用性**：部分模型（如 `wanx-virtualmodel`、`shoemodel-v1`、`wanx-x-painting`）明确标注“仅提供免费体验，额度用完后不可调用且不支持付费”，生产环境应提前规划替代方案。

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
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
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
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片精修API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/ai-fitting-picture-finishing-api-details.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)
- [快速开始](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-quick-start.md)
- [人物形象训练API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)
- [人物写真生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [文字纹理生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/fill-texture-effect-api.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)


