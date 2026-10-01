# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、创意文字生成等多类任务。核心模型包括千问系列（qwen-image）、万相系列（wanx/wan2.x）、可灵（Kling）、Vidu、Z-Image 及一系列垂直场景工具（如 FaceChain、OutfitAnyone、WordArt 等）。所有服务均需通过 API Key 鉴权，并遵循地域隔离原则。

## 支持的模型/功能

平台图像生成能力按技术路径与业务场景分为三类：

- **通用文生图与编辑模型**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0`（支持 T2I/I2I 一体化，[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)）；  
  - `wan2.6-t2i`、`wan2.7-image-pro`（万相 V2/V2.7，支持 4K 文生图及组图生成）；  
  - `z-image-turbo`（轻量级快速生图，适合低延迟场景）；  
  - `kling/kling-v3-omni-image-generation`（支持多图参考与分镜组图）；  
  - `vidu/vidu-image-pro_reference2image`（强语义一致性与 UI/图表像素级还原）。

- **垂直场景工具模型**：  
  - `facechain-generation`（人物写真生成，支持免训练 trainfree 模式）；  
  - `aitryon-plus`（AI 试衣 Plus 版，提升布料纹理与 Logo 还原）；  
  - `wordart-semantic` / `wordart-texture`（创意文字变形与纹理生成）；  
  - `image-out-painting`（图像画面扩展/扩图）；  
  - `wanx-background-generation-v2`（电商商品背景生成）。

- **辅助与检测模型**（非生成主干，但为工作流关键环节）：  
  - `facechain-facedetect`（人脸质量检测）；  
  - `image-instance-segmentation`（人物实例分割）；  
  - `aitryon-parsing-v1`（服饰区域分割）。

> **注意**：部分早期模型（如 `wanx-v1`、`wanx2.1-t2i-turbo`）已明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，其能力、计费与接口稳定性均已被新版本覆盖，不建议新项目接入。

## 关键参数

各模型共性关键参数如下（具体以各模型文档为准）：

- `model`：必填字符串，指定模型名称（如 `"wan2.7-image-pro"`、`"qwen-image-3.0-pro"`），**必须与所选 endpoint 地域匹配**。
- `input`：输入对象，结构因任务类型而异：
  - 文生图：通常含 `prompt` 字段（纯文本提示词）或 `messages` 数组（OpenAI 兼容格式）；
  - 图生图/编辑：含 `image_url` 或 `image`（Base64/URL）及编辑指令 `prompt`；
  - 多模态任务（如 Vidu/Kling）：`messages` 中混合 `text` 与 `image` 元素。
- `parameters.size`：图像分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。不同模型约束不同：
  - 千问系列：总像素需在 `512*512` 至 `2048*2048` 之间；
  - 万相 V2.6+：支持 `1280*1280` 至 `1440*1440`；
  - Vidu/Kling：支持 `1K`/`2K`/`4K`（对应 `1024*1024`/`2048*2048`/`4096*4096`）；
  - Z-Image：同千问，`512*512` 至 `2048*2048`。
- `parameters.n`：生成图像张数（1–9），部分模型（如 `wan2.5-i2i-preview`）默认为 1 张且不可调。
- `X-DashScope-Async`：HTTP 调用时**必填**请求头，值为 `"enable"`（异步）或省略（同步，仅部分模型支持）。

## 使用方式

### 接入协议与调用模式
- **同步调用**：适用于响应快、逻辑简单的任务（如 `qwen-image-3.0` DashScope 同步接口、`z-image-turbo`、`wan2.7-image-pro` HTTP 同步接口）。一次请求即返回图像 URL（PNG 格式）。
- **异步调用**：适用于耗时较长的任务（如多数编辑、扩图、试衣、写真生成）。流程为两步：
  1. `POST /api/v1/services/.../generation` 提交任务，获取 `task_id`；
  2. 定期 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回图像 URL（有效期通常为 24 小时）。
- **OpenAI 兼容协议**：`qwen-image-3.0` 等模型支持，只需将 `base_url` 切换为百炼专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），并设置 `model` 参数。

### 域名与认证
- **必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确建议迁移。
- **API Key 必须与 endpoint 地域严格一致**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 Key 与 URL 不可混用，跨地域调用将直接失败。

## 限制和注意事项

- **地域隔离强制要求**：所有模型调用必须保证模型、API Key、Endpoint URL 属于同一地域。例如，调用 `wan2.7-image-pro` 时若使用新加坡 Key 却请求北京 endpoint，将报鉴权错误。该规则在 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md) 和 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md) 中均有强调。
- **免费额度与限流**：绝大多数模型对主账号与 RAM 子账号共享免费额度（如 500 张）及限流（如 QPS=2，同时处理中任务数=1）。`wanx-x-painting`、`shoemodel-v1`、`wanx-poster-generation-v1` 等模型明确标注“免费额度用完后不可调用且不支持付费”，属限时体验模型，生产环境应规避。
- **输入规范**：
  - 图像 URL 必须公网可访问、无中文路径（需 URL 编码），格式支持 JPG/PNG/WEBP 等；
  - 提示词长度通常限制在 200 字以内（如 `wordart-semantic`）；
  - 人脸类任务（FaceChain）对输入图像有严格要求：单人脸、正面、≥128×128 像素、无遮挡，详见 [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)。
- **输出格式**：主流模型（千问、万相、Kling、Vidu、Z-Image）统一输出 PNG；`qwen-mt-image-2.0`（图像翻译）为 JPG，属特例。

## 来源文档

- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)


