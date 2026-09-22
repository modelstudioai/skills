# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、背景生成、创意文字等场景。核心模型包括千问图像系列、万相、Z-Image、可灵、Vidu及一系列垂直创意工具（如AI试衣、FaceChain、WordArt等），支持同步/异步调用、OpenAI兼容协议及DashScope SDK，适用于从快速原型到专业设计的全栈需求。

## 支持的模型/功能

平台图像能力分为通用生成模型与垂直创意工具两大类：

- **通用生成模型**  
  - **千问图像系列**：`qwen-image-3.0-pro` 和 `qwen-image-3.0` 同时支持文生图与图生图/编辑，推荐用于高精度图文混合任务；早期模型如 `qwen-image-2.0-pro` 仍可调用，但能力已被3.0系列覆盖 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
  - **万相系列**：`wan2.7-image-pro` 支持4K文生图输出；`wan2.6-t2i` 专注文生图，支持自由宽高比（1:4 至 4:1）；`wan2.5-i2i-preview` 支持单图编辑与多图融合 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。  
  - **Z-Image**：轻量级 `z-image-turbo` 模型，主打快速响应，支持512×512至2048×2048分辨率 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。  
  - **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/vidu-image-pro_reference2image` 强调UI/图表像素级还原与工业级稳定性 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

- **垂直创意工具**  
  包括AI试衣（`aitryon`/`aitryon-plus`）、人物写真FaceChain（`facechain-generation`）、创意文字WordArt（`wordart-semantic`/`wordart-texture`）、虚拟模特、图像擦除补全、背景生成等，均面向特定业务场景深度优化。其中部分工具（如 `wanx-x-painting`、`image-erase-completion`）当前仅限免费体验，额度用尽后不可调用 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

> **注意**：文档中 `wanx-v1`（万相V1）明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，且其计费单价（0.16元/张）与V2版模型无直接对标，实际生产环境应优先选用V2及以上版本。

## 关键参数

| 参数 | 类型 | 必选 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model` | string | 是 | 模型名称，需与地域匹配 | `"qwen-image-3.0-pro"`, `"wan2.7-image-pro"` |
| `size` | string | 否 | 输出分辨率，格式为`宽*高`（像素）；未指定时按模型默认策略（如 `qwen-image-3.0-pro` 自动推荐，`wan2.5-i2i-preview` 默认1280×1280） | `"1024*1024"`, `"2048*1152"` |
| `n` | integer | 否 | 生成图片张数（部分模型支持） | `1`（默认）至 `9`（如 `kling/kling-v3-image-generation`） |
| `input.messages` | array | 是（多数模型） | 提示词与参考图数组，首条非空`text`为正向提示，所有`image`为参考图 | `[{"role":"user","content":[{"text":"一只猫","image":"https://..."}]}]` |
| `X-DashScope-Async` | string | 是（HTTP异步调用） | 必须设为 `"enable"`，否则报错 `"current user api does not support synchronous calls"` | `"enable"` |

- **分辨率约束**：  
  - 千问/万相/Z-Image：总像素需在 `512×512` 至 `2048×2048` 之间；  
  - 可灵：仅支持 `1k`（1024×1024）、`2k`（2048×2048）固定尺寸；  
  - Vidu：支持 `1k`/`2k`/`4k`，`4k` 仅限 `vidu-image-pro` 等Pro系列。

- **图像输入**：  
  支持公网URL（HTTP/HTTPS）或Base64编码；URL需可公开访问，含中文字符需URL编码 [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)。

## 使用方式

- **调用协议**：  
  - **同步调用**：适用于千问3.0、万相2.7、Z-Image等模型，一次请求返回结果，推荐大多数场景；  
  - **异步调用**：适用于耗时较长的任务（如万相2.5编辑、可灵、Vidu、AI试衣等），需两步操作：① 创建任务获取 `task_id`；② 轮询 `task_id` 查询结果；  
  - **OpenAI兼容**：千问3.0支持切换 `base_url` 和 `model` 直接接入现有OpenAI应用。

- **Endpoint与认证**：  
  - 必须确保 **模型、Endpoint URL、API Key 属于同一地域**（如华北2北京、新加坡、弗吉尼亚），跨地域调用将失败；  
  - 推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`；  
  - API Key 需配置至环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer sk-xxx`。

- **SDK支持**：  
  DashScope Python/Java SDK 已覆盖全部主流模型；部分工具（如 `wanx-x-painting`）仅提供HTTP API，需自行实现轮询逻辑 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立API Key与Endpoint，不可混用；万相2.6支持三地调用，而千问3.0仅明确列出北京与新加坡 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **免费额度**：多数模型（如 `wanx-style-repaint-v1`、`facechain-generation`、`wordart-semantic`）提供90天内500张免费额度，额度按账号（主账号+RAM子账号）共享，用尽后需付费或切换模型 [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)。
- **异步任务限制**：  
  - 并发任务数上限为1–5个（如 `aitryon` 为5，`facechain-finetune` 为1）；  
  - `X-DashScope-Async: enable` 为HTTP异步调用强制头，缺失即报错；  
  - 任务结果URL有效期24小时。
- **输入规范**：  
  - 图像文件大小≤10MB（实例分割）、≤5MB（FaceChain）；  
  - 格式支持PNG/JPEG/WEBP/BMP等，但 `qwen-mt-image-2.0` 仅输出JPG [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)；  
  - 文字渲染类模型（如千问、Vidu）对中英文提示词兼容性最佳，非中英语言可能效果下降。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
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
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣-图片精修API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/ai-fitting-picture-finishing-api-details.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [快速开始](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-quick-start.md)
- [人物形象训练API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)
- [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)
- [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [人物写真生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [文字纹理生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/fill-texture-effect-api.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)


