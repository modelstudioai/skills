# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、背景生成、文字特效等场景。核心能力由千问（Qwen）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 等模型及一系列创意工具共同支撑，支持同步/异步调用、多地域部署与业务空间专属域名接入。所有服务均需配置对应地域的 API Key 并遵守地域隔离原则。

## 支持的模型/功能

平台图像生成能力分为三类：

- **通用生成模型**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0`（支持文生图与图生图一体化）[千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - `wan2.7-image-pro`（支持4K文生图）与 `wan2.6-t2i`（V2版文生图主力模型）；  
  - `kling/kling-v3-omni-image-generation`（支持多图参考与分镜组图）；  
  - `vidu/vidu-image-pro_reference2image`（强上下文一致性与工业级稳定性）；  
  - `z-image-turbo`（轻量快速生图，适合低延迟场景）。

- **专业编辑与增强模型**：  
  - `qwen-mt-image-2.0`（图像翻译，保留排版并支持术语干预）；  
  - `wan2.5-i2i-preview`（通用图像编辑，支持单图编辑与多图融合）；  
  - `wanx-background-generation-v2`（电商/海报专用背景生成）；  
  - `image-out-painting`（画面扩展/扩图）；  
  - `image-erase-completion`（擦除补全，免费体验）。

- **垂直创意工具**：  
  - `facechain-generation`（人物写真生成，支持免训练模式）；  
  - `wordart-semantic`（文字变形）与 `wordart-texture`（文字纹理生成）；  
  - `aitryon-plus`（AI试衣Plus版，提升布料纹理与Logo还原）；  
  - `wanx-style-repaint-v1`（人像风格重绘）。

> **注意**：部分早期模型（如 `wanx-v1`、`qwen-image-2.0`）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”或“当前与新版能力相同”，实际生产环境应优先选用带 `-pro`、`-v2`、`-v3` 或 `2.7` 等后缀的最新版本，避免使用无明确维护状态的 legacy 模型。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 示例值 |
|--------|------|------|------|--------|
| `model` | string | 是 | 模型名称，严格区分大小写与斜杠（如 `kling/kling-v3-image-generation`） | `"wan2.7-image-pro"` |
| `input.prompt` | string | 文生图必选 | 中英文提示词，建议1–200字，避免模糊指令 | `"水墨风格山水画，题诗'青石桥畔柳风轻'"` |
| `input.messages` | array | 可灵/Vidu必选 | 单元素数组，含 `role: "user"` 与 `content`（含 `text` 和/或 `image`） | `[{"role":"user","content":[{"text":"..."}]}]` |
| `parameters.size` | string | 部分模型必选 | 输出分辨率，格式为 `宽*高`（像素），需符合模型约束 | `"1024*1024"`、`"1280*720"` |
| `parameters.n` | integer | 部分模型必选 | 生成张数，范围依模型而异（如 `wan2.7-image-pro` 支持1–9张） | `2` |
| `input.image_url` | string | 图像输入类必选 | 公网可访问的图片URL（HTTP/HTTPS），需支持临时URL生成 | `"https://example.com/input.jpg"` |

- **分辨率约束**：  
  - 千问系列：总像素须在 `512×512` 至 `2048×2048` 之间；  
  - 万相V2：宽高比限 `1:4` 至 `4:1`，总像素限 `[1280×1280, 1440×1440]`；  
  - 可灵/Vidu：支持 `1K`/`2K`/`4K`，具体以模型文档为准；  
  - Z-Image：同千问，`512×512` 至 `2048×2048`。

- **图像输入限制**：  
  - URL 必须公网可访问，禁止含中文路径（需 URL 编码）；  
  - Base64 输入仅限 DashScope 同步调用（如千问3.0）；  
  - 文件大小通常 ≤10 MB，格式支持 PNG/JPEG/WEBP/BMP。

## 使用方式

### 接入协议与调用模式
- **同步调用**：适用于响应时间敏感场景（≤30秒），支持 OpenAI 兼容协议（仅千问3.0）及 DashScope SDK/HTTP。示例 endpoint：  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（万相2.7）  
  `POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`（万相V2文生图）  
  > 注意：万相V2.5及以下、可灵、Vidu、所有创意工具均**不支持同步调用**，必须使用异步流程 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

- **异步调用**：适用于耗时任务（1–2分钟），需两步操作：  
  1. `POST /generation` 创建任务，获取 `task_id`；  
  2. `GET /tasks/{task_id}` 轮询结果（有效期24小时）。  
  所有异步请求**必须携带 `X-DashScope-Async: enable` 请求头**，缺失将报错。

### 地域与域名配置
- **强制地域对齐**：模型、API Key、Endpoint URL 必须属于同一地域（华北2/北京、新加坡、美东等），跨地域调用必然失败。  
- **推荐域名**：使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代 `dashscope.aliyuncs.com`，可获得更高性能与稳定性 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

### SDK 与环境准备
- 安装 DashScope SDK（Python/Java）并配置 `DASHSCOPE_API_KEY` 环境变量；  
- 若使用 HTTP，需手动设置 `Authorization: Bearer <API_KEY>` 与 `Content-Type: application/json`；  
- Workspace ID 从控制台「业务空间详情」获取，不可硬编码。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美东（弗吉尼亚）等地域拥有独立 API Key 与 Endpoint，不可混用。例如万相2.6支持三地，但万相2.5仅支持北京与新加坡 [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。

- **免费额度与计费**：  
  - 多数模型提供 90 天内 400–500 张免费额度（主账号与 RAM 子账号共享）；  
  - `wanx-x-painting`、`image-instance-segmentation`、`wanx-poster-generation-v1` 等模型为**限时免费体验**，额度用尽即不可用且不支持付费；  
  - FaceChain、WordArt 等需单独申请体验权限，审批通过后额度才生效。

- **输入合规性**：  
  - 提示词禁止包含违法、色情、暴力内容，否则返回空结果或错误码；  
  - 图像 URL 中若含非 ASCII 字符（如中文文件名），必须进行 URL 编码，否则触发 `InternalError.Algo` 错误 [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)；  
  - 涂鸦作画、局部重绘等模型要求输入图像满足特定比例（如 `4:3`）或分辨率下限（如 `512×512`）。

- **并发与速率限制**：  
  - QPS/RPS 限制以主账号为单位（含所有子账号），典型值为 `2–10`；  
  - 同时处理中任务数通常为 `1–5`，超限任务自动排队；  
  - `aitryon-parsing-v1`（图片分割）为同步接口，无并发数限制但 QPS 限 `10`。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [AI试衣-图片精修API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/ai-fitting-picture-finishing-api-details.md)
- [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-quick-start.md)
- [人物形象训练API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)
- [人物写真生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)
- [文字纹理生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/fill-texture-effect-api.md)


