# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、虚拟模特等全栈场景。核心模型包括千问图像系列、万相（WanX）、可灵（Kling）、Vidu 及一系列创意工具，均支持通过 HTTP API 或 DashScope SDK 调用。所有服务均需严格遵循地域隔离原则，模型、API Key 与 Endpoint 必须同属一个地域。

## 支持的模型/功能

- **千问图像系列**：`qwen-image-3.0-pro`、`qwen-image-3.0` 等支持统一 T2I/I2I 接口，具备强文字渲染与多参考图编辑能力（最多 10 张），详见 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **万相（WanX）**：提供分层能力矩阵，包括 `wan2.7-image-pro`（4K 文生图）、`wan2.6-t2i`（V2 文生图）、`wan2.5-i2i-preview`（多图融合编辑）、`wanx-style-repaint-v1`（人像风格重绘）及 `wanx-sketch-to-image-lite`（涂鸦作画）等，覆盖从轻量生成到专业编辑的完整链路。
- **可灵与 Vidu**：`kling/kling-v3-omni-image-generation` 支持分镜组图生成；`vidu/viduq2-pro_reference2image` 专注高一致性工业级参考生图与 UI/图表像素级还原，二者均强调中英文字精准渲染能力。
- **创意工具套件**：包含虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、人物实例分割（`image-instance-segmentation`）、图像擦除补全（`image-erase-completion`）及 FaceChain 人物写真（需先训练 `facechain-finetune` 模型）等垂直场景专用能力，详见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：`wanx-x-painting`（图像局部重绘）、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等多个创意工具模型当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确建议迁移到 [图像编辑-千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md) 或 [图像编辑-万相2.1](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 作为替代方案。

## 关键参数

- **`model`**：必填字符串，指定调用模型全名（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`kling/kling-v3-omni-image-generation`），不同模型能力差异显著，需严格匹配文档。
- **`size` / `parameters.size`**：控制输出分辨率。规则因模型而异：
  - 千问系列：总像素需在 `512×512` 至 `2048×2048` 之间；未指定时自动推荐；
  - 万相 V2 (`wan2.6-t2i`)：宽高均在 `[512, 1440]` 像素间，或总像素在 `[1280×1280, 1440×1440]` 区间；
  - 可灵/Vidu：明确支持 `1K`/`2K`/`4K` 分辨率及 `16:9`/`9:16`/`1:1` 等固定宽高比；
  - Z-Image：总像素范围同千问，为 `[512×512, 2048×2048]`。
- **`n` / `series_amount`**：控制生成张数。`n` 用于单图模式（如 `kling` 的 1–9 张），`series_amount` 用于分镜组图（如 `kling-v3-omni` 的 2–9 张）。
- **`input`**：结构体，包含 `image_url`（公网可访问 URL）或 `image`（Base64 编码），部分模型（如 `qwen-image-3.0-pro`）同时支持 OpenAI 兼容格式的 `image_url` 和 `b64_json`。
- **`X-DashScope-Async`**：HTTP 请求头，**必须显式设置为 `enable`** 才能成功调用异步模型（如万相编辑、可灵、Vidu、所有创意工具），缺失将报错 `"current user api does not support synchronous calls"`。

## 使用方式

- **同步调用**：适用于响应快的模型，如 `qwen-image-3.0-pro`、`wan2.7-image`、`z-image-turbo`。单次 POST 请求即可返回图像数据（PNG Base64）或直接返回 URL。Endpoint 示例：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长（通常 1–2 分钟）的任务，如万相编辑、可灵、Vidu、所有创意工具及 FaceChain 训练。流程为两步：
  1. **创建任务**：发送 POST 请求至 `/generation` 或 `/image-synthesis` 等端点，获取 `task_id`；
  2. **轮询结果**：使用 `task_id` 定期 GET 查询 `/tasks/{task_id}`，直至状态为 `SUCCESS`，返回图像 URL（有效期 24 小时）。
- **地域与认证**：所有调用必须确保模型、API Key、Endpoint 同属一地域（北京、新加坡、弗吉尼亚等）。强烈推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧域名，以获得更高性能与稳定性，该要求在 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md) 和 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md) 中被多次强调。

## 限制和注意事项

- **地域强绑定**：跨地域调用（如北京 Key 调用新加坡 Endpoint）必然失败，此限制在千问、万相、可灵、Vidu 及所有创意工具文档中均被明确标注为“重要”或“适用范围”前提。
- **免费模型额度限制**：`wanx-x-painting`、`virtualmodel-v2`、`shoemodel-v1`、`image-erase-completion`、`wanx-poster-generation-v1` 等十余个创意工具模型均设 500 张免费额度，用尽即停用，且无付费通道。FaceChain 训练（`facechain-finetune`）虽可付费（2.5 元/次），但检测（`facechain-facedetect`）为限时免费。
- **输入质量要求**：FaceChain 系列对训练图像有严格规范（单人脸、>128×128 像素、无遮挡、分辨率 256×256–4096×4096），不符合将导致训练失败，详情见 [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)。
- **异步请求头强制性**：所有异步模型（含万相编辑、可灵、Vidu、创意工具）的 HTTP 请求**必须包含 `X-DashScope-Async: enable` 头**，否则服务拒绝处理，该关键约束在 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md) 和 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md) 的 HTTP 调用章节中被突出标为“重要”。

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
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)


