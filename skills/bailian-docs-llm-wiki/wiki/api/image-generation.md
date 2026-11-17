# image generation

百炼平台提供多种图像生成与编辑模型，覆盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、创意工具等全场景能力。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等，支持同步/异步调用、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到工业级生产的不同需求。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/编辑，部分型号支持最多 10 张参考图输入，并可自动输出带透明通道图像 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **万相系列**：涵盖 `wan2.7-image-pro`（支持 4K 文生图）、`wan2.6-image`、`wan2.5-i2i-preview`（多图融合）、`wanx-sketch-to-image-lite`（涂鸦作画）及 `wanx-x-painting`（局部重绘）等，功能分层清晰，部分模型仅限华北2（北京）地域使用 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。  
- **可灵与 Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图；`vidu/viduq2-pro_reference2image` 强调上下文一致性与工业级稳定性，适用于专业设计场景 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。  
- **轻量与垂直模型**：`z-image-turbo` 为轻量级文生图模型，适合低延迟场景；`qwen-mt-image-2.0` 专注图像翻译，支持 55 种语言互译；FaceChain 支持基于 2 张照片训练专属人像并批量生成写真。  
- **创意工具套件**：含虚拟模特、鞋靴模特、人像风格重绘、创意海报生成、图像擦除补全、人物实例分割等，多数为免费体验模型，额度用尽后不可续用（如 `wanx-x-painting`、`image-instance-segmentation`）[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

> **注意**：`wanx-x-painting`、`image-instance-segmentation`、`shoemodel-v1` 等模型明确标注“仅提供免费体验，额度用完后不可调用且不支持付费”，而千问与万相主干模型（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`）为正式商用模型，计费与限流策略独立。

## 关键参数

- **`model`**：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"`、`"wan2.7-image-pro"`），需与所选地域支持的模型列表一致。  
- **`size`**：控制输出分辨率，格式因模型而异：
  - 千问：支持自由宽高（总像素 512×512 至 2048×2048），默认由提示词推荐；  
  - 万相 V2.7：支持 `"1K"`、`"2K"`、`"4K"` 字符串值；  
  - 可灵/VidU：支持 `"1k"`/`"2k"`/`"4k"` 或具体尺寸（如 `"1024*1024"`）；  
  - Z-Image：需在 `[512×512, 2048×2048]` 总像素范围内指定。  
- **`n` / `series_amount`**：控制生成张数。`n` 用于单图模式（如 `kling/kling-v3-image-generation`，取值 1–9）；`series_amount` 用于分镜组图（如 `kling/kling-v3-omni-image-generation`，取值 2–9）。  
- **`input.messages.content`**：统一采用数组结构，包含 `text`（必填提示词）和可选 `image`（参考图 URL 或 Base64），其中 `image` 在万相 2.7+、可灵、Vidu 中均支持多张（Vidu 最多 14 张）。  
- **`parameters.watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）示例中显式设为 `false`。  
- **`parameters.enable_interleave` + `X-DashScope-Sse`**：仅万相 `wan2.6-image` 等支持图文混排输出时需启用流式响应。

## 使用方式

- **接入协议**：千问支持 OpenAI Images 兼容模式（切换 `base_url` 和 `model` 即可复用现有 OpenAI SDK 代码），其余模型主要通过 DashScope HTTP API 或 SDK 调用。  
- **调用模式**：
  - **同步调用**：适用于 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo` 等，一次请求直接返回图像 URL（PNG 格式），推荐大多数实时场景。  
  - **异步调用**：适用于耗时较长任务（如万相 2.5 编辑、可灵、Vidu、创意工具类），需两步：① `POST /generation` 提交任务获取 `task_id`；② 轮询 `GET /tasks/{task_id}` 获取结果，URL 有效期 24 小时。所有异步 HTTP 请求必须携带 `X-DashScope-Async: enable` 头。  
- **地域与域名**：必须确保 API Key、Endpoint URL、模型部署地域三者一致。强烈建议迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性。  
- **图像输入**：支持公网 URL（HTTP/HTTPS）和 Base64 编码；URL 需 UTF-8 编码（避免中文路径），文件大小通常 ≤10 MB，格式支持 JPG/PNG/WEBP/BMP 等；参考图数量限制依模型而定（如 `qwen-image-2.1-pro` 支持最多 10 张，Vidu 支持最多 14 张）。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key、Endpoint、模型列表完全独立，跨地域调用必然失败。万相 V2.7、可灵、Vidu 等文档多次强调此限制。  
- **分辨率与格式约束**：
  - 所有模型输出均为 PNG（除 `qwen-mt-image-2.0` 固定输出 JPG）；  
  - 千问与 Z-Image 支持总像素 512×512 至 2048×2048；万相 V2.6/V2.7 文生图支持最高 4K（3840×2160），但图像编辑与组图生成限 2K；  
  - 可灵与 Vidu 明确限定宽高比（如 16:9、9:16、1:1），超出将报错。  
- **免费模型风险**：`wanx-x-painting`、`image-instance-segmentation`、`shoemodel-v1`、`wanx-poster-generation-v1` 等明确标注“免费体验，额度用尽后不可调用”，无付费开通路径，生产环境应规避依赖。  
- **输入校验**：FaceChain 要求训练图片为单人脸、正面、≥128×128 像素、无遮挡；人物实例分割要求图像分辨率 ≥512×512 且 ≤4096×4096；所有图像 URL 不得含未编码中文字符，否则触发 `InternalError.Algo` 错误。  
- **异步超时**：[异步任务](../concepts/asynchronous-task.md)轮询需自行实现重试逻辑，典型耗时 1–2 分钟，排队时间受服务负载影响，文档未提供 SLA 承诺。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)


