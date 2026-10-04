# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、创意工具等多类模型。所有服务均通过统一的 API 接口调用，支持同步与异步两种模式，适用于从快速原型到高精度生产级的各种开发场景。

## 支持的模型/功能

平台当前提供三大类图像生成模型：

- **通用文生图与编辑模型**：包括千问系列（`qwen-image-3.0-pro`、`qwen-image-2.1-pro`）和万相系列（`wan2.7-image-pro`、`wan2.6-t2i`、`wan2.5-i2i-preview`），支持高质量 T2I、I2I、多图融合及图文混排输出。其中千问-图像生成与编辑3.0模型同时支持文生图与图生图，且具备强文本渲染能力 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；万相2.7 image专业版在文生图场景下支持4K高清输出 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。

- **轻量与专用模型**：Z-Image（`z-image-turbo`）为轻量级文生图模型，兼顾速度与中英文字渲染；可灵（`kling/kling-v3-omni-image-generation`）和Vidu（`vidu/viduq2-pro_reference2image`）专注高分辨率与复杂语义理解，支持分镜组图、UI/图表像素级还原等专业场景。

- **创意工具与垂直应用**：覆盖人像风格重绘、虚拟模特、AI试衣（`aitryon-plus`）、人物写真（`facechain-generation`）、图像背景生成、文字变形（`wordart-semantic`）等20+细分能力。例如，FaceChain支持免训练（trainfree）模式一键生成个性化写真，大幅降低使用门槛 [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)。

> **注意**：部分早期模型（如 `wanx-v1`、`wanx2.1-t2i-turbo`）已明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，其功能、性能与计费策略已被新版本替代，不建议新项目接入。

## 关键参数

所有图像生成 API 的核心参数结构高度一致，关键字段如下：

- `model`：必填字符串，指定模型名称（如 `"qwen-image-3.0-pro"` 或 `"wan2.7-image-pro"`）。
- `input.messages`：必填数组，含单条 `user` 角色消息，其 `content` 为文本提示词（`text`）与可选图像（`image`，支持 Base64 或公网 URL）的混合列表。
- `parameters.size`：可选字符串，格式为 `"宽*高"`（如 `"1024*1024"`）。各模型约束不同：
  - 千问系列：总像素需在 `512*512` 至 `2048*2048` 之间；
  - 万相V2（`wan2.6-t2i`）：宽高比限制 `[1:4, 4:1]`，总像素在 `[1280*1280, 1440*1440]`；
  - 可灵与Vidu：仅支持预设分辨率（1K/2K/4K）及固定宽高比（16:9、9:16、1:1）。
- `parameters.n`：可选整数，控制生成图像张数（通常为 `1–9`，部分工具类模型如 `wordart-semantic` 限定为 `1–4`）。
- `X-DashScope-Async`：HTTP 调用时必填请求头，值必须为 `"enable"`（异步）或 `"disable"`（同步，仅部分模型支持）。

## 使用方式

### 接入协议与调用模式
- **同步调用**：适用于响应时间敏感、图像尺寸可控的场景（如 `qwen-image-3.0-pro`、`wan2.7-image-pro` 文生图）。直接发送 POST 请求至 `/api/v1/services/aigc/multimodal-generation/generation`，一次返回结果。
- **异步调用**：适用于耗时较长（通常 1–2 分钟）的任务（如图像编辑、扩图、AI试衣）。流程为两步：
  1. `POST /api/v1/services/.../generation` 创建任务，获取 `task_id`；
  2. 定期 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回带有效期（24 小时）的图像 URL。
- **OpenAI 兼容协议**：千问系列支持 OpenAI Images 接口规范，仅需切换 `base_url` 和 `model` 即可迁移现有代码。

### 地域与域名
- **严格地域隔离**：API Key、Endpoint URL、模型必须属于同一地域（如华北2北京、新加坡、美国弗吉尼亚），跨地域调用将失败。
- **推荐使用业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，性能与稳定性更优。`{WorkspaceId}` 可在控制台“业务空间详情”页获取。

## 限制和注意事项

- **免费额度与计费**：所有模型均提供独立免费额度（通常 500 张/90 天），额度用尽后按量付费。单价差异显著，例如 `aitryon-plus` 为 0.50 元/张，而 `wordart-texture` 仅 0.08 元/张；部分模型（如 `wanx-x-painting`、`shoemodel-v1`）为限时免费，额度用尽即不可用 [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)。
- **输入限制**：图像 URL 必须为公网可访问的 HTTP/HTTPS 链接，且不含中文字符（需 URL 编码）；Base64 数据需符合标准格式；文件大小通常限制在 5–10 MB 内。
- **并发与速率**：所有模型均对 QPS（每秒请求数）与并发任务数进行限制，以账号（主账号 + RAM 子账号）为单位。例如 `facechain-finetune` 并发上限为 1，`aitryon-parsing-v1` 为无限制（同步接口），需根据业务负载合理设计重试与排队逻辑。
- **模型可用性**：部分模型（如 `wanx-v1`、`wanx2.1-imageedit`）仅限华北2（北京）地域；万相V2（`wan2.6-t2i`）在弗吉尼亚地域支持同步调用，但其他地域仅支持异步。务必查阅各地域模型列表确认支持情况。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-图片精修API参考](../../raw/_short/ai-fitting-picture-finishing-api-details-8c8f980f48b3085f.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物写真生成API详情](../../raw/_short/facechain-generation-e11b15fa1f0ad97a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [文字变形API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/word-transformer.md)
- [文字纹理生成API详情](../../raw/_short/fill-texture-effect-api-702f76f58b3dd251.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)


