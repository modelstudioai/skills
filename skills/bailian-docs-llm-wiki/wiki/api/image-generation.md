# image generation

百炼平台提供多种图像生成能力，涵盖文生图（T2I）、图生图（I2I）、图像编辑、风格迁移、局部重绘及专业场景工具（如虚拟模特、海报生成、FaceChain写真等）。核心模型包括千问（Qwen-Image）、万相（WanX）、可灵（Kling）、Vidu、Z-Image 及一系列创意工具，支持同步与[异步调用](../concepts/asynchronous-invocation.md)，适配不同性能、精度与成本需求。所有服务均需严格遵循地域隔离原则，API Key、Endpoint 与 Workspace ID 必须同地域匹配。

## 支持的模型/功能

- **通用文生图与编辑**：  
  - `qwen-image-3.0-pro` 和 `qwen-image-3.0` 同时支持 T2I 与 I2I，推荐用于高保真图文混合生成与精确编辑 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - `wan2.7-image-pro` 支持文生图 4K 输出、组图生成与多图参考编辑；`wan2.6-t2i` 专精纯文本生成，支持自由宽高比（1:4 至 4:1）与大尺寸（最高 1440×1440）[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)；  
  - `z-image-turbo` 是轻量级模型，适合快速迭代与中英文字渲染，分辨率支持 512×512 至 2048×2048。

- **专业场景工具**：  
  - `wanx-style-repaint-v1` 专注人像艺术风格转换；`wanx-virtualmodel` / `virtualmodel-v2` 支持商品图模特替换；`shoemodel-v1` 实现鞋靴AI试穿；`creative-poster-generation-v1` 自动排版生成营销海报；`facechain-finetune` 支持基于2张照片训练专属人物LoRA模型并批量生成写真。  
  > **注意**：`wanx-x-painting`（局部重绘）、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等模型当前仅限免费体验，额度用尽后不可调用且不支持付费，官方明确建议迁移到 [千问-图像编辑](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md) 或 [万相2.1图像编辑](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 等正式商用模型。

- **多模态增强生成**：  
  `kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/viduq2-pro_reference2image` 强调上下文一致性与工业级稳定性，适用于漫剧制作与UI设计还原。

## 关键参数

- **`size`**：控制输出分辨率。格式因模型而异：  
  - 千问系列支持 `512x512`～`2048x2048` 总像素范围，可显式指定或留空由模型自动推荐；  
  - 万相 V2 (`wan2.6-t2i`) 要求总像素在 `[1280×1280, 1440×1440]` 区间；  
  - 可灵与 Vidu 使用语义化值（如 `"1K"`、`"2K"`、`"4K"`）；  
  - Z-Image 接受 `width×height` 字符串（如 `"1024x768"`）。

- **`n` / `series_amount`**：控制生成张数。`n` 适用于单图模式（如 `kling/kling-v3-image-generation`，取值 1–9）；`series_amount` 用于可灵组图模式（2–9）。

- **`watermark`**（布尔值）：部分模型（如 `wan2.7-image-pro`）支持关闭水印，默认为 `true`。

- **`thinking_mode`**（布尔值）：启用后返回推理过程描述（如 `wan2.7-image-pro`），便于调试提示词有效性。

- **`element_list`**（可灵特有）：指定需保持一致性的主体列表，提升多图生成中对象跨帧一致性。

## 使用方式

- **调用协议**：  
  - **同步调用**：适用于低延迟场景（如实时预览），支持 DashScope SDK（Python/Java）及 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（仅千问系列）。示例：`qwen-image-3.0-pro` 的 `/images/generations` 接口，传 `image` 字段即触发图生图 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)；  
  - **[异步调用](../concepts/asynchronous-invocation.md)**：适用于耗时任务（通常 1–2 分钟），所有创意工具类模型（如 `wanx-style-repaint-v1`、`image-erase-completion`）及部分万相/可灵模型强制要求。流程为：① `POST /generation` 创建任务获取 `task_id`；② 定期 `GET /task/{task_id}` 查询状态，成功后返回带 24 小时有效期的图像 URL。

- **地域与域名**：  
  所有请求必须使用**同地域**的 API Key、Workspace ID 与 Endpoint。华北2（北京）和新加坡地域已全面启用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但官方强烈建议迁移以获得更高性能与稳定性。

- **输入格式**：  
  - 文本提示词：长度限制因模型而异（如可灵 ≤2500 字符，Vidu ≤5000 字符），需避免空格/特殊符号截断；  
  - 图像输入：支持公网 URL（HTTP/HTTPS）或 Base64 编码；URL 不得含中文字符，需做 percent-encoding；格式通常限 JPEG/PNG/JPG（万相局部重绘、可灵不支持透明通道）；分辨率与文件大小均有明确上限（如可灵单图宽高 300–8000 像素，≤10MB）。

## 限制和注意事项

- **地域强绑定**：跨地域调用（如用北京 API Key 请求新加坡 Endpoint）必然失败。文档多次强调“华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立的 API Key 与请求地址，不可混用” [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)，此为最常见错误根源。

- **模型弃用与兼容性**：  
  - 万相 V1（`wanx-v1`）已明确标注为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”；  
  - 千问早期模型（如 `qwen-image-2.0` 系列）虽仍列于文档，但新版 API 参考中已统一引导至 `qwen-image-3.0-pro`，实际生产环境应优先选用 3.0 系列。

- **免费模型策略风险**：  
  多个创意工具模型（`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion`、`creative-poster-generation-v1`）均注明“目前仅供免费体验，免费额度用完后不可调用且不支持付费”。开发者需评估业务连续性风险，提前规划向千问或万相 2.1+ 正式商用模型的迁移路径。

- **异步任务管理**：  
  异步任务 `task_id` 有效期为 24 小时，超时未查询将丢失结果；创建任务时若重复提交相同请求，可能造成资源浪费，文档明确提示“请勿重复创建任务，轮询获取即可” [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

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
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


