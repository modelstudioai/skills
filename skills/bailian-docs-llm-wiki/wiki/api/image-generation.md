# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、创意工具等全栈场景。所有模型均通过统一的 DashScope 协议或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)接入，支持同步/异步调用，并需严格遵循地域隔离原则（API Key、Endpoint、Workspace ID 必须同地域）。开发者应优先选用 `qwen-image-3.0-pro`、`wan2.7-image-pro` 或 `kling/kling-v3-omni-image-generation` 等新一代模型，旧版模型（如 `wanx-v1`）已明确标注为“推荐使用全面升级的[文生图V2版模型](raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)” [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

## 支持的模型/功能

平台当前提供三大类图像模型能力：

- **通用生成与编辑**：  
  - 千问系列：`qwen-image-3.0-pro`（T2I + I2I 全能力）、`qwen-image-3.0`（平衡版），支持多图参考编辑与复杂文本渲染 [原文标题](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - 万相系列：`wan2.7-image-pro`（4K 文生图）、`wan2.6-t2i`（V2 文生图）、`wan2.5-i2i-preview`（多图融合编辑）；  
  - 可灵（Kling）：`kling/kling-v3-omni-image-generation`（支持分镜组图生成）；  
  - Vidu：`vidu/viduq2-pro_reference2image`（工业级稳定性，UI/图表像素级还原）。

- **轻量与专项模型**：  
  - `z-image-turbo`：轻量文生图，快速响应，支持中英文字渲染；  
  - `wanx-sketch-to-image-lite`：涂鸦转精细绘画；  
  - `wanx-x-painting`：图像局部重绘（当前仅限免费体验）[原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

- **创意工具套件**：  
  包含人像风格重绘、虚拟模特、鞋靴试穿、AI试衣（`aitryon`/`aitryon-plus`）、人物写真（`facechain-generation`）、创意海报、文字艺术（`wordart-semantic`/`wordart-texture`）等垂直场景模型，详见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md) 目录。

> **注意**：多个文档对 `wanx-v1`（文档8）和 `wanx2.1-t2i-turbo`（文档7）等早期万相模型标注了“推荐使用全面升级的[文生图V2版模型](raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，且其调用方式（仅支持异步）、分辨率限制（单边≤1440）及地域支持范围（仅北京）均显著落后于 V2/V2.7 模型，实际开发中应避免选用。

## 关键参数

核心参数在不同模型间保持高度一致，但存在关键差异：

- **`size`**：指定输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。  
  - 千问系列：总像素需在 `512×512` 至 `2048×2048` 之间，不指定时自动推荐；  
  - 万相 V2.7：`wan2.7-image-pro` 文生图支持 4K（如 `"3840*2160"`），编辑/组图限 2K；  
  - 可灵：仅支持预设宽高比（`16:9`/`9:16`/`1:1`）与分辨率等级（`1k`/`2k`/`4k`）组合；  
  - Z-Image：同千问，总像素区间 `512×512`–`2048×2048`。

- **`n`**：控制生成张数。  
  - 千问/万相标准模型：`1–6` 张；  
  - 可灵：`1–9` 张（单图模式）或 `2–9` 张（分镜组图模式，通过 `series_amount` 指定）；  
  - Z-Image：固定 `1` 张。

- **`input.messages`**：统一输入结构，为 `[{ "role": "user", "content": [...] }]` 数组。  
  - `content` 内可混合 `text`（提示词）与 `image`（Base64 或公网 URL），万相 `wan2.5-i2i-preview` 明确支持多图输入并按“最后一张图宽高比”默认裁剪 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

- **异步必需头**：所有 HTTP 异步调用必须携带 `X-DashScope-Async: enable`，缺失将报错 `"current user api does not support synchronous calls"`（见文档19、20、22等）。

## 使用方式

### 接入协议
- **推荐 DashScope 同步调用**：功能最完整，支持 Base64 与 URL 图像输入，适用于 `qwen-image-3.0-pro`、`wan2.7-image-pro` 等主流模型；  
- **OpenAI 兼容协议**：仅支持同步调用，适用于已集成 OpenAI Images SDK 的应用，切换 `base_url` 和 `model` 即可；  
- **HTTP 异步调用**：适用于耗时较长任务（如局部重绘、虚拟模特），流程为“创建任务 → 轮询结果”，所有异步接口均需 `X-DashScope-Async: enable` 头。

### 地域与域名
- **强制同地域**：API Key、Endpoint、Workspace ID 必须属于同一地域（北京/新加坡/弗吉尼亚），跨地域调用必然失败；  
- **推荐专属域名**：华北2（北京）和新加坡地域已启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性更优，旧域名（`dashscope.aliyuncs.com`）仍可用但不推荐。

### SDK 与环境配置
- 安装 `dashscope` SDK（Python/Java）并配置 `DASHSCOPE_API_KEY` 环境变量；  
- 示例代码中的 `DASHSCOPE_API_HOST` 需替换为实际 Workspace ID 对应的专属域名；  
- 所有模型均需提前在百炼控制台开通服务（如可灵、Vidu 需手动开通）。

## 限制和注意事项

- **地域隔离刚性约束**：文档2、9、10、11、19、20 等反复强调“API Key 与请求地址不可混用，跨地域调用将导致鉴权失败或服务报错”。例如，新加坡地域的 Key 无法调用北京 Endpoint，反之亦然。

- **免费额度与限流**：  
  - 多数模型（如 `wanx-style-repaint-v1`、`aitryon`、`facechain-generation`）提供 500 张/90 天免费额度，额度用尽后转为按量付费；  
  - 限流以主账号+RAM子账号为单位共享，例如 `aitryon` 的 RPS 限 10，`facechain-finetune` 的并发任务数限 1；  
  - `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1` 等模型明确标注“免费额度用完后不可调用且不支持付费”，属临时体验能力。

- **输入规范**：  
  - 图像 URL 必须公网可访问、支持 HTTPS、无中文路径（需 URL 编码）；  
  - 人物写真（FaceChain）要求正脸单人照、≥256×256 像素、无遮挡；  
  - 文字渲染类模型（千问、Vidu）对中英文提示词兼容性好，但复杂排版需明确指定位置与字体。

- **异步任务时效性**：  
  - 任务 ID 有效期 24 小时，生成图像 URL 有效期 24 小时；  
  - 队列排队时间不可控，高并发时建议增加轮询间隔或使用 Webhook（若支持）。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
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
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)


