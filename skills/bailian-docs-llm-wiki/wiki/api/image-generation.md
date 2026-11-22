# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及垂直场景工具（如虚拟模特、海报生成等）。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 等，支持同步/异步调用、多地域部署及 OpenAI 兼容协议。所有服务均需严格匹配 API Key 所属地域与请求 endpoint。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`qwen-image-2.1-pro` 等，统一支持文生图与图生图/编辑，其中 `qwen-image-3.0-pro` 为当前主力推荐模型 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；早期 `qwen-image-2.0-pro` 系列仍被部分文档引用，但已明确标注“当前与 qwen-image-2.0-pro-2026-04-22 能力相同”，属历史兼容型号。
- **万相系列**：覆盖全栈能力，包括 `wan2.7-image-pro`（支持 4K 文生图）、`wan2.6-t2i`（V2 文生图主力）、`wan2.5-i2i-preview`（通用图像编辑）、`wanx-sketch-to-image-lite`（涂鸦作画）等；注意 `wan2.6-image` 模型**不推荐用于纯文生图**，应优先选用 `wan2.6-t2i` [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **可灵与 Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图；`vidu/vidu-image-pro_reference2image` 强调中英文字精准渲染与 UI/图表像素级还原 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。
- **轻量与垂直模型**：`z-image-turbo` 适用于快速轻量生成；`facechain-finetune` 支持基于 2 张图的人物形象定制训练；`wanx-style-repaint-v1`、`shoemodel-v1`、`wanx-poster-generation-v1` 等均为华北2（北京）地域专属的创意工具类模型，多数处于免费体验阶段且**不支持付费开通**。

> **注意**：多份文档（如[万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)、[虚拟模特](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)、[图像擦除补全](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)）均明确声明“免费额度用完后不可调用且不支持付费”，开发者需评估长期可用性，建议关键业务链路优先选用千问或万相 Pro 系列。

## 关键参数

- **`size`**：控制输出分辨率，格式因模型而异：
  - 千问系：接受 `"2K"`、`"4K"` 或具体宽高（如 `"1024*1024"`），总像素须在 `512×512` 至 `2048×2048` 之间；
  - 万相 V2（`wan2.6-t2i`）：仅支持固定区间 `[1280×1280, 1440×1440]`；
  - 可灵/VidU：支持 `"1K"`/`"2K"`/`"4K"` 及宽高比（`16:9`/`9:16`/`1:1`）；
  - Z-Image：接受任意宽高组合，总像素约束同千问系。
- **`n`**：生成图像张数，千问/万相/可灵均支持 `1–6` 或 `1–9`（依模型而定），Z-Image 固定为 `1` 张。
- **`watermark`**：布尔值，控制是否添加水印（默认 `true`），千问 `qwen-image-3.0-pro` 等模型支持显式关闭。
- **`thinking_mode`**：千问 `qwen-image-3.0-pro` 特有参数，启用后返回推理过程描述（非必需）。
- **`element_list`**：可灵模型用于指定需保持一致性的主体列表，数量与参考图总数之和 ≤ 10。

## 使用方式

- **接入协议**：千问支持 OpenAI 兼容模式（仅需切换 `base_url` 和 `model`），其余模型主要通过 DashScope HTTP API 或 SDK 调用。
- **调用模式**：
  - **同步调用**：适用于千问（DashScope 同步）、万相 `wan2.7-image-pro`、Z-Image 等低延迟模型，单次请求直接返回图像 Base64 或 URL；
  - **异步调用**：适用于耗时较长任务（如万相 `wan2.5-i2i-preview`、可灵、Vidu、所有创意工具类模型），流程为 `POST 创建任务 → 轮询 task_id 获取结果`，task_id 有效期 24 小时。
- **地域与域名**：**必须确保 API Key、endpoint、模型三者地域一致**（华北2/新加坡/弗吉尼亚等）。强烈建议迁移至业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **输入格式**：文本提示词（`text`）为必填项；图像输入支持公网 URL 或 Base64 编码；多图输入时，各模型对最大张数有明确限制（如千问 `qwen-image-2.1-pro` 支持最多 10 张参考图）。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域的 API Key、Endpoint、模型列表完全独立，跨地域调用必然失败。例如，万相 `wan2.6-t2i` 在弗吉尼亚地域可用，但 `wan2.7-image-pro` 仅限北京/新加坡。
- **图像输入限制**：
  - 格式：普遍支持 PNG/JPEG，但可灵明确**不支持透明通道**；
  - 分辨率：单边长度通常要求 `≥512` 且 `≤4096` 像素，万相 V2 要求宽高比在 `[1:4, 4:1]` 内；
  - 大小：多数模型限制单图 ≤ 10MB。
- **文本提示词限制**：千问/万相无明确字符数上限；可灵限制 `≤2500` 字符；Vidu 支持 `≤5000` 字符；所有模型均要求 UTF-8 编码，避免特殊控制字符。
- **免费模型风险**：`wanx-style-repaint-v1`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-instance-segmentation` 等十余个创意工具类模型均标注“免费额度用完后不可调用且不支持付费”，其稳定性与长期维护性低于主力生成模型，生产环境慎用。
- **SDK 支持差异**：人像风格重绘等部分模型**仅提供 HTTP API，暂无官方 SDK**，需自行封装调用逻辑。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


