# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及专业创意工具等全场景需求。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu 和 Z-Image 等系列，均支持通过 DashScope SDK 或 HTTP API 调用。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与业务空间必须同地域配对使用。

## 支持的模型/功能

- **千问系列**：`qwen-image-3.0-pro` 和 `qwen-image-3.0` 同时支持文生图与图生图/图像编辑；`qwen-image-2.1-pro` 和 `qwen-image-2.1-turbo` 支持最多 10 张参考图输入，并可自动输出带透明通道图像 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **万相系列**：`wan2.7-image-pro` 支持文生图 4K 输出及组图生成；`wan2.5-i2i-preview` 支持单图编辑与多图融合；`wanx-style-repaint-v1` 专注人像艺术风格重绘；`wanx-x-painting` 提供图像局部重绘能力（当前仅限免费体验）[万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。  
- **可灵与 Vidu**：`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图；`vidu/vidu-image-pro_reference2image` 强调中英文字精准渲染与 UI/图表像素级还原 [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)。  
- **轻量与创意工具**：`z-image-turbo` 为轻量级文生图模型，适合快速响应；`facechain-finetune` 支持基于 2 张照片训练专属人像模型，用于批量写真生成。

> **注意**：文档中 `wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`wanx-poster-generation-v1`、`image-instance-segmentation`、`image-erase-completion` 等模型均明确标注“仅提供免费体验，额度用完后不可调用且不支持付费”，而同期发布的 `qwen-image-3.0-pro` 和 `wan2.7-image-pro` 均无此限制，表明其已进入正式商用阶段，开发者应优先选用后者以保障服务连续性。

## 关键参数

- **`size`**：控制输出分辨率。不同模型取值范围不同：`qwen-image-*` 支持 `512*512` 至 `2048*2048` 总像素；`wan2.6-t2i` 限定在 `[1280*1280, 1440*1440]`；`kling` 和 `vidu` 支持 `1K/2K/4K` 字符串标识或具体宽高比（如 `16:9`）；`z-image-turbo` 同样接受总像素约束内的自由尺寸。未指定时，多数模型按提示词或输入图宽高比自动推荐默认尺寸。  
- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，取值 1–9）；`series_amount` 专用于 `kling/kling-v3-omni-image-generation` 的组图模式（2–9）。  
- **`watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认 `false`）。  
- **`thinking_mode`**：启用推理过程可视化（如 `wan2.7-image-pro` 示例中所示），便于调试但非必需。  
- **`element_list`**（可灵）与 **`mask_url`**（擦除补全）：分别用于主体一致性保持和区域掩码输入，属高级编辑类参数。

## 使用方式

- **同步调用**：适用于 `qwen-image-*`（DashScope 同步或 OpenAI 兼容模式）、`wan2.6-image`、`wan2.7-image-*`、`z-image-turbo` 等模型。请求体为 JSON，含 `model`、`input.messages`（含 `text` 和可选 `image` URL/Base64）及 `parameters`。HTTP 方法为 `POST`，Endpoint 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。  
- **异步调用**：适用于耗时较长任务（如万相 V2 编辑、可灵、Vidu、虚拟模特、海报生成等）。流程为两步：① `POST /api/v1/services/.../generation` 提交任务并获取 `task_id`；② 定期 `GET /api/v1/tasks/{task_id}` 查询状态，成功后返回 PNG 图像 URL（有效期 24 小时）。所有异步请求头必须包含 `X-DashScope-Async: enable`。  
- **SDK 集成**：推荐使用 DashScope Python/Java SDK，已全面支持同步与异步模式。安装见 [安装DashScope SDK](../../raw/model-api-reference/preparations/install-sdk.md)，配置需设置环境变量 `DASHSCOPE_API_KEY` 并确保与 Workspace ID 地域一致。

## 限制和注意事项

- **地域强绑定**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立 API Key 与 Endpoint，跨地域调用必然失败。务必通过控制台确认模型可用地域，并使用对应 Workspace ID 构造专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **输入限制**：文本提示词长度上限因模型而异——`kling` 为 2500 字符，`vidu` 为 5000 字符；图像格式普遍支持 JPG/PNG（部分禁用透明通道），单图大小通常 ≤10 MB，分辨率宽高均在 `[300, 8000]` 像素内；多图输入时，`kling` 要求参考图数量 + 主体数量 ≤10，`vidu` 最多支持 14 张参考图。  
- **免费模型风险**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1` 等模型明确声明“免费额度用完后不可调用且不支持付费”，且文档多次建议迁移到 `qwen-image-edit-guide` 或 `wanx-image-edit` 等替代方案，生产环境应规避此类模型。  
- **认证与权限**：RAM 子账号调用必须显式传入 `X-DashScope-WorkSpace` 头；主账号可省略，但 Workspace ID 仍需存在于请求 URL 中。所有调用均需 `Authorization: Bearer <API_KEY>`，且 API Key 必须已在对应地域开通模型权限。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)


