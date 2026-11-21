# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、虚拟模特、创意海报等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列垂直创意工具。所有服务均通过统一的 DashScope API 协议接入，支持同步与[异步调用](../concepts/asynchronous-invocation.md)模式，并需严格遵循地域隔离原则。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0` 等支持文生图与图生图二合一，其中 `qwen-image-2.1-pro` 和 `qwen-image-2.1-turbo` 支持最多 10 张参考图输入，并可自动输出带透明通道图像 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **万相系列**：涵盖多代能力，`wan2.7-image-pro` 支持文生图 4K 输出；`wan2.6-t2i` 专注高质量文生图；`wan2.5-i2i-preview` 支持单/多图融合编辑；`wanx-style-repaint-v1` 提供人像风格重绘；`wanx-sketch-to-image-lite` 实现涂鸦作画 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。  
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`vidu/viduq3.1-fast_reference2image` 支持按分辨率与画幅比例精确指定输出尺寸 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。  
- **轻量与垂直模型**：`z-image-turbo` 为快速响应型文生图模型；`facechain-finetune` 支持基于 2 张照片训练专属人物形象；`image-erase-completion`、`image-instance-segmentation` 等创意工具类模型当前仅限免费体验，额度用尽后不可调用 [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)。

> **注意**：文档中 `wanx-poster-generation-v1`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`image-instance-segmentation`、`wanx-x-painting` 等模型均明确标注“仅提供免费体验，免费额度用完后不可调用且不支持付费”，与通用付费模型（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`）存在本质服务策略差异，开发者需在选型时严格区分。

## 关键参数

- **`size`**：控制输出分辨率，格式因模型而异：`qwen-image-*` 接受 `宽*高`（如 `"1024*1024"`）或语义值（如 `"2K"`）；`wan2.7-image-pro` 明确支持 `"2K"`/`"4K"`；`kling` 和 `vidu` 仅接受预设枚举值（`"1K"`/`"2K"`/`"4K"`）及宽高比（`"16:9"`/`"1:1"` 等）。  
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图生成（如 `qwen-image-3.0-pro`、`kling/kling-v3-image-generation`），取值范围通常为 `1–9`；`series_amount` 专用于 `kling/kling-v3-omni-image-generation` 的分镜组图，取值 `2–9`。  
- **`watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）支持显式关闭。  
- **`thinking_mode`**：仅 `wan2.7-image-pro` 支持，启用后返回推理过程描述，便于调试。  
- **`element_list`**（可灵）与 **`auxiliary_parameters`**（创意海报）：分别为主体一致性控制和二次高清增强的关键结构化参数，需按模型文档严格构造。

## 使用方式

- **接入协议**：推荐使用 DashScope SDK（Python/Java），亦支持 OpenAI 兼容模式（仅限 `qwen-image-*` 系列）或原生 HTTP 调用。OpenAI 兼容模式下，`/images/generations` 接口通过是否传入 `image` 字段区分 T2I/I2I [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **调用模式**：  
  - **同步调用**：适用于 `qwen-image-*`、`wan2.7-image-*`、`z-image-turbo` 等低延迟模型，单次请求直接返回图像 Base64 或 URL。  
  - **[异步调用](../concepts/asynchronous-invocation.md)**：适用于耗时较长任务（如 `wan2.5-i2i-preview`、`kling`、`vidu`、所有创意工具类模型），需先 `POST /generation` 获取 `task_id`，再轮询 `GET /tasks/{task_id}` 查询状态。  
- **地域与域名**：必须确保 API Key、Endpoint、Workspace ID 同属一地域（北京/新加坡/弗吉尼亚等）。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

## 限制和注意事项

- **地域隔离强制要求**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key、Endpoint、Workspace ID 严格隔离，混用将导致鉴权失败或 403 错误。此规则适用于所有图像模型，无例外。  
- **输入图像约束**：  
  - 格式：普遍支持 JPEG/PNG/JPG，但 `kling` 明确**不支持透明通道**；`wan2.5-i2i-preview` 要求 PNG；`image-erase-completion` 支持 BMP/WEBP/HEIF。  
  - 分辨率：多数模型要求总像素在 `512×512` 至 `2048×2048` 之间；`wan2.7-image-pro` 文生图支持 4K（`3840×2160`）；`kling` 和 `vidu` 限定 `1K`/`2K`/`4K` 预设尺寸。  
- **文本提示词限制**：`kling` 提示词长度上限为 2500 字符；`vidu` 为 5000 字符；`qwen-image-*` 未明确说明，但实践中建议 ≤2000 字符以保障效果。  
- **免费模型风险**：`wanx-poster-generation-v1`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`wanx-x-painting` 等模型在免费额度耗尽后**完全不可用且无付费通道**，生产环境应避免依赖 [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)


