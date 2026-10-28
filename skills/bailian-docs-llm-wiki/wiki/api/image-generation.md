# image generation

百炼平台提供丰富的图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘、创意工具等全栈场景。核心模型包括千问（Qwen-Image）、万相（WanX）、Z-Image、可灵（Kling）、Vidu 及 FaceChain 等，支持同步/异步调用、OpenAI 兼容协议及 DashScope 原生 SDK。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与 Workspace ID 必须同属一个地域。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`qwen-image-3.0`、`wan2.7-image-pro`、`wan2.6-t2i`、`z-image-turbo` 支持自由分辨率设定（512×512 至 2048×2048），默认输出 PNG 格式；其中 `qwen-image-3.0-pro` 和 `wan2.7-image-pro` 明确支持文生图与图生图双模态 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **专业图像翻译**：`qwen-mt-image-2.0` 专用于多语种图文翻译，保留原始排版，支持中/英/日/韩/西/法等 55 种语言互译，输出 JPG 格式 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。
- **创意增强工具**：包含虚拟模特（`wanx-virtualmodel`）、鞋靴模特（`shoemodel-v1`）、人像风格重绘（`wanx-style-repaint-v1`）、图像擦除补全（`image-erase-completion`）等垂直能力，多数当前仅限免费体验 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。
- **高阶定制化**：FaceChain 支持基于 2 张人脸照片训练专属 LoRA 模型，实现高保真写真生成，需先完成人物图像检测（`facechain-facedetect`）与形象训练（`facechain-finetune`）两步前置流程 [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)。
- **视频关联图像模型**：可灵（Kling）与 Vidu 均提供 `reference2image` 类模型，支持多图参考生成分镜组图或 UI/图表像素级还原，其中 `kling/kling-v3-omni-image-generation` 最多支持 14 张参考图输入 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

> **注意**：万相 V1 版（`wanx-v1`）已明确标注“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”；而 `wan2.5-i2i-preview` 在文档中未说明是否已被 `wan2.7-image-pro` 取代，但其能力描述（如“preview”标签、分辨率限制）表明其为过渡版本，生产环境应优先选用 `wan2.7-image-pro` 或 `wan2.6-image`。

## 关键参数

- **`size`**：控制输出分辨率，格式因模型而异：
  - 千问系列支持数值型（如 `"1024*1024"`）或语义型（如 `"2K"`）；
  - 万相 V2（`wan2.6-t2i`）要求总像素在 `[1280×1280, 1440×1440]` 区间；
  - 可灵与 Vidu 仅接受预设值（`"1K"`/`"2K"`/`"4K"`）；
  - Z-Image 要求总像素在 `[512×512, 2048×2048]` 区间。
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，取值 1–9）；`series_amount` 专用于分镜组图（如 `kling/kling-v3-omni-image-generation`，取值 2–9）。
- **`image_url` / `mask_url`**：图像输入参数，需公网可访问 URL 或 Base64 编码。所有图像类模型均对格式（JPG/PNG/WEBP 等）、尺寸（宽高比 1:10 至 10:1，单边 300–8192 px）、大小（≤10 MB）有严格限制。
- **`watermark`**：布尔值，控制是否添加百炼水印（默认 `true`），部分模型（如 `wan2.7-image-pro`）支持通过 `parameters.watermark=false` 关闭。
- **`thinking_mode`**：万相 2.7 系列特有参数，启用后返回更详细的推理过程（JSON 结构），便于调试提示词效果。

## 使用方式

- **同步调用**：适用于低延迟场景（如实时预览），支持 `qwen-image-*`、`wan2.7-image-pro`、`z-image-turbo`、`wan2.6-image` 等模型，请求路径统一为 `/api/v1/services/aigc/multimodal-generation/generation`（万相/千问/Z-Image）或 `/api/v1/services/aigc/image-generation/generation`（可灵/Vidu），需设置 `Content-Type: application/json` 与 `Authorization: Bearer <API_KEY>`。
- **异步调用**：适用于耗时较长任务（通常 >30s），如万相 V1、局部重绘（`wanx-x-painting`）、创意海报（`wanx-poster-generation-v1`）、FaceChain 训练等，流程为：① `POST /api/v1/services/.../image-synthesis` 提交任务获取 `task_id`；② 定期 `GET /api/v1/tasks/{task_id}` 轮询状态，成功后返回图像 URL（有效期 24 小时）。
- **OpenAI 兼容模式**：千问图像模型支持 OpenAI Images 协议，只需将 `base_url` 切换为百炼专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/v1`），并指定 `model="qwen-image-3.0-pro"` 即可复用现有 OpenAI SDK 代码 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **SDK 集成**：推荐使用 DashScope Python/Java SDK，自动处理认证、重试与异步轮询逻辑；部分模型（如 `wanx-style-repaint-v1`）明确声明“仅提供 HTTP API，暂无 SDK”。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）地域完全独立，API Key、Endpoint、Workspace ID 必须三者同地域，跨地域调用必然失败。万相 V2 文档明确指出“华北2（北京）、新加坡和美国（弗吉尼亚）地域拥有独立的 API Key 与请求地址” [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **域名迁移强制要求**：所有新项目必须使用业务空间专属域名（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性显著下降，且部分新功能（如高并发[流式输出](../concepts/streaming-output.md)）仅在新域名下支持。
- **免费额度与限流**：多数创意工具类模型（如 `wanx-x-painting`、`image-erase-completion`、`wanx-poster-generation-v1`）当前仅限免费体验，额度用尽即不可调用；所有模型均对 QPS（如主账号+RAM 子账号共用 2 QPS）与并发任务数（如 FaceChain 训练限 1 个）设硬性上限。
- **输入安全约束**：所有图像 URL 不得含中文字符，否则触发 `InternalError.Algo` 错误；文本提示词长度受限（千问/万相 ≤2500 字符，Vidu ≤5000 字符），超长将直接报错；参考图数量上限因模型而异（`qwen-image-2.1-pro` 支持最多 10 张，`vidu/*` 支持最多 14 张）。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)


