# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、专业创意工具（如虚拟模特、海报生成）等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等系列，均支持通过 DashScope SDK 或 HTTP API 调用。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与 Workspace ID 必须同地域匹配。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/图像编辑双模态任务，[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 明确其输出规格与多图输入能力（最多10张参考图）。
- **万相系列**：涵盖 `wan2.6-t2i`（文生图V2）、`wan2.7-image-pro`（4K文生图）、`wan2.5-i2i-preview`（多图融合编辑）、`wanx2.1-imageedit`（通用图像编辑）等，支持扩图、去水印、风格化、图文混排等丰富功能；[万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 详细列出了全局/局部风格化、指令编辑、局部重绘等能力。
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`vidu/vidu-image-pro_reference2image` 等强调中英文字精准渲染与UI/图表像素级还原，适用于专业设计场景。
- **轻量与垂直模型**：`z-image-turbo` 提供快速轻量文生图；`qwen-mt-image-2.0` 专注图像翻译；FaceChain 支持基于2张照片的人物形象训练与写真生成；创意工具类如 `shoemodel-v1`（鞋靴试穿）、`wanx-style-repaint-v1`（人像风格重绘）、`image-erase-completion`（擦除补全）等面向特定业务需求。

> **注意**：部分模型（如 `wanx-x-painting`、`wanx-poster-generation-v1`、`shoemodel-v1`、`image-instance-segmentation`）当前仅提供免费体验，额度用完后不可调用且不支持付费，官方明确建议参考 [图像编辑-千问](../../raw/model-user-guide/model-experience/image-model/image-edit-guide/qwen-image-edit-guide.md) 或 [图像编辑-万相2.1](../../raw/model-user-guide/model-experience/image-model/image-edit-guide/wanx-image-edit.md) 获取替代方案。

## 关键参数

- **`model`**：必填，指定具体模型名称（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`），不同模型能力差异显著，需按需选择。
- **`size`**：控制输出分辨率。格式因模型而异：
  - 千问系列：支持 `宽*高`（如 `"1024*1024"`）或语义值（如 `"2K"`），总像素需在 `512*512` 至 `2048*2048` 之间；
  - 万相V2（`wan2.6-t2i`）：总像素约束为 `[1280*1280, 1440*1440]`；
  - 可灵/Vidu：支持 `"1K"`/`"2K"`/`"4K"` 等语义值，对应固定分辨率范围。
- **`n` / `series_amount`**：控制生成张数。`n` 用于单图模式（如 `kling` 支持 1–9 张），`series_amount` 用于分镜组图（`kling-v3-omni` 支持 2–9 张）。
- **`input.messages.content`**：统一采用数组结构，包含 `text`（提示词）和可选 `image`（参考图URL或Base64），`text` 长度限制因模型而异（如 `kling` ≤2500字符，`vidu` ≤5000字符）。
- **`parameters.watermark`、`parameters.thinking_mode`**：部分模型（如 `wan2.7-image-pro`）支持关闭水印或启用推理模式。

## 使用方式

- **接入协议**：推荐使用 **DashScope 同步调用**（功能最完整，支持 URL/Base64 输入）；已适配 OpenAI Images 协议的应用可切换 `base_url` 和 `model` 快速迁移（仅限千问系列）；批量或长耗时任务应选用 **DashScope 异步调用**（提交任务后轮询 `task_id`）。
- **请求地址**：必须使用业务空间专属域名（非旧版 `dashscope.aliyuncs.com`）。华北2（北京）格式为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，`{WorkspaceId}` 需从控制台获取。
- **认证与依赖**：所有调用需配置有效的同地域 API Key（通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer sk-xxx` 传入），并安装 [DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)（Python/Java）。
- **调用流程差异**：
  - 同步模型（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`）：单次 POST 请求直接返回结果。
  - 异步模型（如 `kling`、`vidu`、`wan2.5-i2i-preview`、`wanx-style-repaint-v1`）：需两步——先 `POST /generation` 获取 `task_id`，再 `GET /tasks/{task_id}` 轮询状态。

## 限制和注意事项

- **地域强绑定**：API Key、Endpoint、Workspace ID 必须属于同一地域（华北2、新加坡、美国弗吉尼亚等），跨地域调用必然失败。[千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 和 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 均反复强调此前提。
- **输入限制**：图像 URL 需公网可访问、无中文路径（需 URL 编码）；格式通常限 JPG/PNG/WEBP；分辨率与文件大小有严格上限（如 `kling` 图像宽高 300–8000px，文件 ≤10MB；`vidu` 最多支持 14 张参考图）。
- **免费额度与限流**：多数创意工具类模型（如 `wanx-x-painting`、`shoemodel-v1`、`image-erase-completion`）仅限免费体验，额度用尽即停用；所有模型均对 QPS 和并发任务数设限（如 `facechain-finetune` QPS=2，并发=1），详情见各模型文档。
- **模型兼容性**：`wanx-v1`（V1版）已不推荐使用，官方明确指引迁移至 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)；`qwen-mt-image` 不支持非中/英语种间直译（如日→韩），需经中/英中转。

## 来源文档

- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)


