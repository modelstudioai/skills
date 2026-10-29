# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景需求。核心模型包括千问系列（Qwen-Image）、万相系列（WanX）、Z-Image、可灵（Kling）、Vidu 及 FaceChain 等，支持同步/异步调用、多地域部署与 OpenAI 兼容协议。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与 Workspace ID 必须同属同一地域。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo` 支持自由分辨率设定（总像素 512×512 至 2048×2048），默认输出 PNG；其中 `qwen-image-3.0-pro` 同时支持 T2I 和 I2I [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **专业图像编辑与融合**：`wan2.5-i2i-preview` 支持单图编辑与多图融合；`wanx2.1-imageedit` 提供扩图、去水印、风格迁移、局部重绘等 5 类能力；`qwen-image-2.1-pro` 支持最多 10 张参考图输入 [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)。
- **垂直场景工具**：`facechain-finetune` 支持基于 2~10 张人脸图像训练专属 LoRA 模型；`wanx-virtualmodel` 和 `shoemodel-v1` 分别面向虚拟模特与鞋靴试穿；`image-erase-completion` 实现掩码驱动的智能擦除补全。
- **图像翻译与本地化**：`qwen-mt-image-2.0` 支持中/英/日/韩等 55 种语言互译，精准保留排版 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。
- **特殊能力模型**：`vidu/viduq2-pro_reference2image` 擅长复杂逻辑与工业级稳定性；`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成。

> **注意**：`wanx-v1`（V1版文生图）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”，且其 HTTP 同步调用能力缺失，仅支持异步，而 V2 版 `wan2.6-t2i` 已支持同步调用，应优先选用 V2 系列。

## 关键参数

- **`size`**：控制输出分辨率。格式因模型而异：
  - `qwen-image-*`：接受 `"1024x1024"` 或 `"2K"`（如 `2048x1024`）等字符串；
  - `wan2.5-i2i-preview`：支持 `"宽*高"`（如 `"1280*1280"`），未指定时默认 `1280*1280`；
  - `kling/*` 与 `vidu/*`：仅接受枚举值 `"1K"`/`"2K"`/`"4K"`，对应固定分辨率范围。
- **`n`**：生成图像张数。`qwen-image-*`、`kling/*`（单图模式）、`wan2.6-t2i` 支持 `1–6` 或 `1–9`；`z-image-turbo` 固定为 `1` 张。
- **`watermark`**：布尔值，控制是否添加百炼水印（默认 `true`），部分模型如 `wan2.7-image-pro` 明确支持设为 `false`。
- **`thinking_mode`**：仅 `wan2.7-image-pro` 支持，启用后返回推理过程文本（非必需）。
- **`image`（输入）**：图生图类模型通过 `input.messages[].content[].image` 字段传入参考图 URL（支持多张），`qwen-image-3.0-pro` 与 `vidu/*` 最多支持 14 张；`kling/kling-v3-omni-image-generation` 明确支持多图输入并生成分镜组图。

## 使用方式

- **接入协议**：主流模型均支持 DashScope SDK（Python/Java）与 HTTP 调用；`qwen-image-*` 还提供 OpenAI 兼容模式（切换 `base_url` 与 `model` 即可复用现有 OpenAI 代码）。
- **调用模式**：
  - **同步调用**：适用于 `qwen-image-3.0-pro`、`wan2.7-image-pro`、`z-image-turbo`、`wan2.6-t2i` 等低延迟模型，一次请求即返回图像 URL（或 Base64）。
  - **异步调用**：适用于耗时较长任务（如 `wan2.5-i2i-preview`、`kling/*`、`vidu/*`、`facechain-finetune`），需先 `POST /generation` 获取 `task_id`，再轮询 `/tasks/{task_id}` 查询状态。
- **地域与域名**：必须使用与 API Key 同地域的 Endpoint。**强烈建议迁移至业务空间专属域名**：华北2（北京）为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`，以获得更高性能与稳定性 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 限制和注意事项

- **地域强绑定**：API Key、Endpoint、Workspace ID 必须同属一个地域（北京/新加坡/弗吉尼亚等）。跨地域调用将直接失败，且各模型支持的地域不同（如 `wan2.6-t2i` 支持弗吉尼亚，但 `qwen-mt-image-2.0` 仅支持北京与新加坡）。
- **输入限制**：
  - 图像格式：普遍支持 JPG/JPEG/PNG/BMP/WEBP，但 `qwen-mt-image-2.0` 仅支持 JPG；`kling/*` 不支持透明通道。
  - 图像尺寸：宽高均需在 `[300, 8000]` 像素（`kling`）、`[512, 4096]`（`image-erase-completion`）或 `[15, 8192]`（`qwen-mt-image-2.0`）范围内。
  - 文本长度：`kling/*` 提示词 ≤2500 字符，`vidu/*` ≤5000 字符。
- **免费额度与计费**：多数创意工具类模型（如 `wanx-x-painting`、`image-instance-segmentation`、`wanx-poster-generation-v1`）当前仅限免费体验，额度用尽后不可调用且不支持付费，文档中已明确提示替代方案 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。
- **模型弃用风险**：`wanx-v1`、`wanx2.1-t2i-turbo` 等 V1/V2.1 旧版模型在文档中被标记为“推荐使用升级版”，应避免新项目接入。

## 来源文档

- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)


