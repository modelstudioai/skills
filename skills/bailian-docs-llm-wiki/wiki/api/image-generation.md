# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、AI试穿等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列创意工具，均支持通过 DashScope SDK 或 HTTP API 调用。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与业务空间必须同地域。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-2.1-turbo` 等支持统一 T2I/I2I 接口，具备强文本渲染与多图参考编辑能力；`qwen-mt-image-2.0` 专用于高保真图像翻译，支持 55 种语言互译并保留原始排版 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。
- **万相系列**：涵盖 `wan2.7-image-pro`（4K 文生图）、`wan2.5-i2i-preview`（多图融合编辑）、`wanx-sketch-to-image-lite`（涂鸦作画）及 `wanx-style-repaint-v1`（人像风格重绘）等，功能高度细分且持续迭代 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/viduq2-pro_reference2image` 强调工业级稳定性与上下文一致性，适用于专业设计与漫剧制作 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。
- **创意工具**：包含虚拟模特（`virtualmodel-v2`）、鞋靴模特（`shoemodel-v1`）、FaceChain 人物写真（需先训练 `facechain-finetune` 模型）、图像擦除补全（`image-erase-completion`）等垂直场景模型，多数当前仅限免费体验。

> **注意**：`wanx-virtualmodel`、`wanx-poster-generation-v1`、`wanx-x-painting`、`image-erase-completion` 等多个创意工具模型明确标注“目前仅供免费体验，免费额度用完后不可调用且不支持付费”，开发者应提前规划替代方案，例如使用 [千问-图像编辑](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md) 或万相 2.1+ 系列替代。

## 关键参数

- **`model`**：必填，指定具体模型名（如 `qwen-image-3.0-pro`、`wan2.7-image-pro`），不同模型能力差异显著，需按需选择。
- **`size`**：控制输出分辨率，格式因模型而异：
  - 千问系：支持 `宽*高`（如 `"1024*1024"`）或语义值（如 `"2K"`）；
  - 万相 V2+：支持 `"1280*1280"`、`"2K"`、`"4K"` 等；
  - 可灵/Vidu：仅支持 `"1K"`、`"2K"`、`"4K"`。
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，范围 1–9）；`series_amount` 专用于 Vidu/Kling 的分镜组图（2–9 张）。
- **`input.messages.content`**：统一结构，为 `text`（提示词）与 `image`（参考图 URL 数组）的混合列表。Vidu 明确支持最多 14 张参考图，而千问 2.1 系列支持最多 10 张。
- **`parameters.watermark`**：布尔值，控制是否添加水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）支持设为 `false`。

## 使用方式

- **同步调用**：适用于千问 3.0+、万相 2.6/2.7、Z-Image 等低延迟模型，一次 HTTP POST 即返回结果（含图像 URL）。Endpoint 示例：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长任务（如万相 2.5 编辑、可灵、Vidu、FaceChain 训练），需两步操作：
  1. 提交任务获取 `task_id`（如 `POST .../image-generation/generation`）；
  2. 轮询 `GET .../tasks/{task_id}` 获取状态与结果（URL 有效期通常为 24 小时）。
- **SDK 集成**：推荐使用 DashScope Python/Java SDK，自动处理认证、重试与异步轮询逻辑。所有模型均要求配置 `DASHSCOPE_API_KEY` 环境变量，并设置 `DASHSCOPE_API_HOST` 为对应地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）。
- **地域与域名**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域独立部署，API Key、Endpoint、Workspace ID 必须严格匹配。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性。

## 限制和注意事项

- **地域隔离强制**：跨地域调用（如北京 API Key 请求新加坡 Endpoint）必然失败。文档多次强调“API Key 与请求地址必须属于同一地域”，此为硬性约束 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **图像输入限制**：
  - 格式：主流支持 PNG/JPEG/JPG/WEBP，但 `qwen-mt-image-2.0` 仅支持 JPG；`kling` 不支持透明通道。
  - 分辨率：宽高均需在 `[300, 8000]` 像素（Kling）或 `[512, 4096]`（擦除补全）范围内，宽高比通常限制在 `1:4` 至 `4:1`。
  - 大小：单图上限多为 10MB（Kling/Vidu）或 100MB（Qwen-MT），需注意上传前压缩。
- **提示词长度**：Kling 限制 2500 字符，Vidu 放宽至 5000 字符，超长将直接报错。
- **免费额度与限流**：多数创意工具（如 `wanx-x-painting`、`shoemodel-v1`）仅限免费体验，额度用尽即停服；所有模型均对 QPS（如 2 RPS）与并发任务数（如 1）设限，需在业务侧做好排队与降级。
- **模型弃用风险**：`wanx-v1`、`wanx2.1-t2i-turbo` 等旧版模型被明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，应避免新项目接入。

## 来源文档

- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
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
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)


