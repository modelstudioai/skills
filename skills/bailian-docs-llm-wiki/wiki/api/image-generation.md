# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、图像翻译、局部重绘、背景生成、创意文字生成等核心场景。所有模型均通过统一的 API 接口调用，支持同步与异步两种模式，适配不同业务对延迟、吞吐和结果确定性的要求。开发者需注意地域隔离、API Key 与 Endpoint 的严格匹配，以及免费额度与计费规则。

## 支持的模型/功能

百炼平台当前提供三大类图像生成模型：

- **通用文生图与编辑模型**：包括千问系列（`qwen-image-3.0-pro`、`qwen-image-2.0-pro` 等）、万相系列（`wan2.6-t2i`、`wan2.7-image-pro`、`wan2.5-i2i-preview` 等）及轻量级模型 `z-image-turbo`。其中千问-图像生成与编辑3.0同时支持文生图与图生图，且明确支持1–3张参考图输入 [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；万相-图像生成与编辑2.7则支持文生图、文生组图、图生组图及多图参考生成 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。

- **垂直领域专用模型**：如 `qwen-mt-image-2.0`（图像翻译）、`kling/kling-v3-omni-image-generation`（支持多图输入与分镜组图）、`vidu/vidu-image-pro_reference2image`（UI/图表像素级还原）等，聚焦特定任务精度与效果。

- **创意工具与辅助模型**：涵盖人像风格重绘、虚拟模特、鞋靴模特、AI试衣（`aitryon-plus`）、人物写真（`facechain-generation`）、创意海报、图像擦除补全、背景生成、WordArt锦书（文字纹理/变形）等。这些模型多为任务链式组合，例如 AI试衣需配合图片分割（`aitryon-parsing-v1`）与精修（`aitryon-refiner`）使用 [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)。

> **注意**：部分早期文档存在模型命名与能力描述不一致问题。例如文档4中 `qwen-image-2.0-pro` 被标注为“当前与 `qwen-image-2.0-pro-2026-04-22` 能力相同”，但文档5中同名模型又指向 `qwen-image-2.0-pro-2026-06-22`，且未说明版本演进逻辑。实际调用应以最新发布的 `qwen-image-3.0-pro` 为准，其能力已覆盖旧版全部功能并增强语义遵循性。

## 关键参数

所有图像生成 API 均通过 `model`、`input` 和 `parameters` 三类核心参数控制行为：

- **`model`**：必填字符串，指定具体模型名称（如 `qwen-image-3.0-pro`、`wan2.6-t2i`、`kling/kling-v3-image-generation`）。不同地域支持的模型列表不同，必须与 API Key 所属地域一致。

- **`input`**：必填对象，结构因任务类型而异：
  - 文生图：通常含 `prompt` 字段（文本提示词），部分模型（如 `qwen-image-3.0-pro`）支持 `messages` 数组格式。
  - 图生图/编辑：含 `image_url` 或 `image`（Base64）字段，部分模型（如 `wan2.5-i2i-preview`）支持多图输入。
  - 图像翻译：`input` 中需指定 `source_lang` 和 `target_lang`（见 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)）。

- **`parameters`**：可选对象，常用字段包括：
  - `size`：指定输出分辨率，格式为 `"宽*高"`（如 `"1024*1024"`）。各模型有硬性约束：`qwen-image-3.0-pro` 要求总像素在 `512*512` 至 `2048*2048` 之间；`wan2.6-t2i` 限定在 `[1280*1280, 1440*1440]`；`kling` 系列仅支持 `1k/2k/4k` 预设尺寸。
  - `n`：生成图像张数，范围因模型而异（如 `kling` 支持 `1–9`，`qwen-image-2.0-pro` 支持 `1–6`）。
  - `style` / `template`：用于风格迁移或预设模板（如 `facechain-generation` 的 `trainfree` 模式需传入自定义风格模板图）。

## 使用方式

调用方式分为同步与异步两类，选择依据是任务耗时与业务容忍度：

- **同步调用**：适用于响应时间敏感、单次请求量小的场景（如实时预览）。支持模型包括 `qwen-image-3.0-pro`（DashScope 同步）、`wan2.6-t2i`、`z-image-turbo` 等。请求直接返回图像 URL 或 Base64 数据，无需轮询。示例 endpoint：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。

- **异步调用**：适用于批量生成、高分辨率输出或复杂编辑任务（如 `wan2.5-i2i-preview`、`aitryon-plus`、`facechain-finetune`）。流程为两步：
  1. 提交任务获取 `task_id`（如 `POST .../generation`）；
  2. 轮询 `GET .../tasks/{task_id}` 获取状态与结果。所有异步接口均需在请求头中显式设置 `X-DashScope-Async: enable`，否则报错 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

> **注意**：`X-DashScope-Async` 头部为强制要求，缺失将导致 `current user api does not support synchronous calls` 错误。此外，华北2（北京）与新加坡地域已启用业务空间专属域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 虽仍可用，但官方强烈建议迁移以获得更高稳定性。

## 限制和注意事项

- **地域与凭证强绑定**：API Key、Endpoint URL、模型部署地域必须完全一致。跨地域调用（如北京 Key 调用新加坡 Endpoint）必然失败。万相、可灵、Vidu 等模型在弗吉尼亚、法兰克福等地域的支持情况需查阅对应文档，部分仅限北京/新加坡 [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。

- **输入与输出约束**：
  - 图像 URL 必须公网可访问，且不含中文路径（需 URL 编码）；
  - 输入图像分辨率普遍要求不低于 `512*512`，部分模型（如 `facechain-facedetect`）上限为 `4096*4096`；
  - 输出格式以 PNG 为主，`qwen-mt-image-2.0` 例外，固定输出 JPG。

- **免费额度与计费**：所有模型均提供 500 张/90 天的新人免费额度（部分如 `wanx-x-painting`、`shoemodel-v1` 为限时免费体验），额度用尽后按量计费。计费单元统一为“成功生成的图片张数”，失败请求不扣费。AI试衣-图片精修（`aitryon-refiner`）采用阶梯定价，用量越大单价越低 [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)。

- **并发与速率限制**：以主账号（含 RAM 子账号）为单位，QPS 与并发数独立限制。例如 `aitryon-plus` 任务下发 QPS 限 10，同时处理中任务数限 5；`facechain-finetune` 并发任务数限 1。超出限制的请求将被拒绝或排队。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [AI试衣-图片精修API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/ai-fitting-picture-finishing-api-details.md)
- [AI试衣-图片分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-parsing-api.md)
- [AI试衣-Plus版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/aitryon-plus-api.md)
- [AI试衣-基础版API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/outfitanyone-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [快速开始](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-quick-start.md)
- [人物图像检测API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-face-detection-api.md)
- [人物形象训练API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-finetune-api.md)
- [人物写真生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-generation.md)
- [FaceChain人物写真生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation/facechain-billing.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [文字纹理生成API详情](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/fill-texture-effect-api.md)
- [WordArt锦书-创意文字生成模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start/wordart-billing.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [AI试衣OutfitAnyone模型计量计费](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone/billing-for-outfitanyone.md)


