# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移、创意工具等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及 FaceChain 等，支持同步/[异步调用](../concepts/asynchronous-invocation.md)、OpenAI 兼容协议及 DashScope SDK，适用于从快速原型到工业级生产的各类开发者场景。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro`（T2I+I2I二合一）、`qwen-image-2.1-turbo`（高性价比）、`qwen-image-2.0-pro`（强文字渲染与语义遵循）；支持多图输入（最多10张）、透明通道自动识别及水墨/书法等复杂文本生成 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **万相系列**：`wan2.7-image-pro`（4K文生图）、`wan2.6-image`（图文混排）、`wan2.5-i2i-preview`（单/多图融合编辑）、`wanx-sketch-to-image-lite`（涂鸦作画）、`wanx-style-repaint-v1`（人像风格重绘）；部分模型如 `wanx-x-painting` 和 `wanx-virtualmodel` 当前仅限免费体验 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
- **可灵与Vidu**：`kling/kling-v3-omni-image-generation`（支持多图参考与分镜组图）、`vidu/vidu-image-pro_reference2image`（UI/图表像素级还原、中英文字精准渲染）；二者均强调设计级输出质量与上下文一致性 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。
- **轻量与垂直模型**：`z-image-turbo`（快速生图，512×512–2048×2048自由分辨率）、`facechain-finetune`（基于2张图训练专属人物LoRA）、`image-erase-completion`（擦除补全）、`virtualmodel-v2`（虚拟模特，支持2048短边与多比例背景）。

> **注意**：`wanx-image-edit-api`（文档3）与 `wan2-5-image-edit-api-reference`（文档11）对“多图融合”能力描述一致，但前者未明确支持多图输入数量上限，后者明确支持；建议以 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md) 为准，其明确支持多图输入且兼容性更清晰。

## 关键参数

- **`size`**：控制输出分辨率。格式因模型而异：
  - 千问：接受 `宽*高`（如 `"1024*1024"`）或预设值（如 `"2K"`），总像素需在 `512×512` 至 `2048×2048` 之间；
  - 万相V2/V2.7：支持 `"1K"`/`"2K"`/`"4K"` 或具体尺寸（如 `"1280*1280"`），宽高比约束为 `[1:4, 4:1]`；
  - Vidu/可灵：仅支持预设档位（`"1K"`/`"2K"`/`"4K"`）及固定宽高比（`16:9`/`9:16`/`1:1`）。
- **`n`**：生成图像张数。千问、万相V2.7、可灵支持 `1–9` 张；Z-Image 固定为 `1` 张；Vidu 固定为 `1` 张。
- **`watermark`**：布尔值，控制是否添加平台水印（默认 `true`，部分模型如 `wan2.7-image-pro` 可设为 `false`）。
- **`image`（输入）**：支持公网URL或Base64；万相2.5支持最多14张参考图，可灵限制参考图+主体数≤10；所有图像须为JPEG/PNG/JPG，无透明通道（可灵明确不支持）。
- **`thinking_mode`**：万相2.7特有参数，启用后返回推理过程日志，便于调试。

## 使用方式

- **调用协议**：推荐使用 **DashScope SDK**（Python/Java），或 **DashScope HTTP 同步/异步接口**；千问同时支持 **OpenAI 兼容模式**（仅同步，`/images/generations` 接口，不传 `image` 为T2I，传入则为I2I）。
- **地域与域名**：必须保证 **API Key、Endpoint URL、模型部署地域三者一致**。华北2（北京）和新加坡地域已启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧域名 `dashscope.aliyuncs.com`，强烈建议迁移。
- **异步流程（通用）**：适用于耗时较长任务（如编辑、海报生成、FaceChain训练）：
  1. `POST /api/v1/services/.../generation` 提交任务，获取 `task_id`；
  2. 轮询 `GET /api/v1/tasks/{task_id}` 获取状态与结果（URL有效期24小时）。
- **同步流程（推荐多数场景）**：千问、万相2.6/2.7、Z-Image、Vidu（部分）支持，一次请求直接返回图像数据（PNG Base64或URL）。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域的 API Key 与 Endpoint **完全独立，不可混用**；跨地域调用将导致鉴权失败或 `401/403` 错误。
- **免费额度与停用模型**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`wanx-poster-generation-v1` 等模型当前**仅限免费体验，额度用尽即不可调用，且不支持付费开通**；官方推荐迁移到千问或万相2.1+替代方案 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。
- **输入限制**：
  - 文本长度：千问/万相V2提示词 ≤2500字符；Vidu ≤5000字符；FaceChain检测图片需 ≥256×256 且 ≤4096×4096 像素。
  - 图像格式：禁止透明通道（可灵明确要求）；万相涂鸦/局部重绘要求输入图为 JPG/PNG；FaceChain训练需2–10张正面、无遮挡人脸图。
- **计费与限流**：主账号与RAM子账号共享QPS及并发限制（如 `wanx-style-repaint-v1` QPS=2，并发=1）；FaceChain训练按次计费（2.5元/次），检测限时免费。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
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
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


