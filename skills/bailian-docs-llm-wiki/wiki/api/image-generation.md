# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及垂直场景工具（如虚拟模特、海报生成、FaceChain写真等）。核心模型包括千问（Qwen-Image）、万相（WanX）、Z-Image、可灵（Kling）、Vidu 及创意工具套件，支持同步与异步调用，适配不同性能、精度与成本需求。所有服务均需严格匹配地域（如华北2、新加坡）的 API Key 与 Endpoint。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`qwen-image-3.0` 支持 T2I 和 I2I，支持最多 10 张参考图输入，并可自动输出带透明通道图像；`wan2.7-image-pro` 在文生图场景支持 4K 输出，而组图与编辑限于 2K [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **轻量与极速模型**：`z-image-turbo` 为轻量级模型，适合快速生成；`wan2.2-t2i-flash` 较前代提速 50%；`qwen-image-2.1-turbo` 是 Qwen-Image 系列中“综合表现与性价比最优”的模型 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **多模态与专业能力**：`vidu/viduq2-pro_reference2image` 擅长复杂逻辑与工业级稳定性；`kling/kling-v3-omni-image-generation` 支持多图参考与分镜组图生成；`wan2.5-i2i-preview` 支持单图编辑与多图融合 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。  
- **垂直场景工具**：包括人像风格重绘、虚拟模特、鞋靴试穿、创意海报、人物实例分割、图像擦除补全等；FaceChain 支持基于 2 张照片训练专属人像并批量生成写真，需先完成人脸检测与形象训练两步 [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)。

> **注意**：部分早期模型（如 `wanx-v1`、`wanx-x-painting`、`wanx-poster-generation-v1`、`shoemodel-v1`）当前仅提供免费体验，额度用尽后不可调用且不支持付费，官方明确推荐迁移到千问或万相 2.1+ 等新版模型 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

## 关键参数

- **`size`**：控制输出分辨率。格式因模型而异：`qwen-image-*` 接受 `宽*高`（如 `1024*1024`）或语义值（如 `"2K"`）；`wan2.6-t2i` 要求总像素在 `[1280*1280, 1440*1440]`；`kling` 和 `vidu` 仅支持预设值（`1K`/`2K`/`4K`）。未指定时，多数模型默认接近 `1024*1024` 或按输入图宽高比自适应。  
- **`n`**：生成图像张数。`qwen-image-*`、`kling/*` 支持 `1–9` 张；`z-image-turbo` 固定为 `1` 张；`wan2.7-image-pro` 在组图模式下通过 `series_amount` 指定 `2–9` 张。  
- **`watermark`**：布尔值，控制是否添加水印（如 `wan2.7-image-pro` 默认开启，可设为 `false` 关闭）。  
- **`thinking_mode`**：`wan2.7-image-pro` 特有参数，启用后返回推理过程描述（非必需）。  
- **`element_list`**（Kling）与 `mask_url`（擦除补全）等为特定任务专用参数，详见各模型文档。

## 使用方式

- **接入协议**：主流模型（Qwen-Image、WanX 2.6+、Z-Image、Kling、Vidu）均支持 DashScope 同步/异步 HTTP 调用及 SDK（Python/Java）；Qwen-Image 还提供 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，仅需切换 `base_url` 和 `model` 即可复用现有 OpenAI 集成 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。  
- **调用模式**：  
  - **同步调用**：适用于低延迟场景（如实时预览），支持 `qwen-image-*`、`wan2.7-image-*`、`wan2.6-image`、`z-image-turbo` 等，一次请求即返回结果。  
  - **异步调用**：适用于耗时较长任务（通常 1–2 分钟），如 `wan2.5-i2i-preview`、`kling/*`、`vidu/*`、所有创意工具类模型（虚拟模特、海报、擦除补全等），流程为“创建任务 → 轮询 `task_id` 获取结果”，`task_id` 有效期 24 小时。  
- **地域与域名**：必须确保 API Key、Endpoint URL、业务空间 ID（`{WorkspaceId}`）三者同地域（华北2、新加坡、弗吉尼亚等）。强烈建议使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）替代旧版 `dashscope.aliyuncs.com`，以获得更高性能与稳定性。

## 限制和注意事项

- **地域隔离**：华北2（北京）、新加坡、弗吉尼亚等地域的 API Key 与 Endpoint **完全独立，不可混用**；跨地域调用将导致鉴权失败或服务报错。  
- **图像输入限制**：  
  - 参考图格式普遍支持 JPG/JPEG/PNG（**不支持透明通道**，如 `kling` 明确说明）；  
  - 分辨率范围因模型而异：`kling` 要求单边 `300–8000` 像素；`vidu` 支持最多 14 张参考图；`wan2.5-i2i-preview` 多图输入时宽高比按最后一张图对齐。  
- **文本提示词**：长度上限各异——`kling` 为 2500 字符，`vidu` 为 5000 字符；所有模型均要求 UTF-8 编码，含中文需确保传输无乱码。  
- **免费模型限制**：`wanx-x-painting`、`wanx-virtualmodel`、`shoemodel-v1`、`image-erase-completion` 等明确标注“仅供免费体验”，额度用尽即停服，无付费通道，开发中应避免依赖 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。  
- **FaceChain 流程约束**：人物写真生成是三阶段流程（人脸检测 → 形象训练 → 写真生成），其中训练为[异步任务](../concepts/asynchronous-task.md)，且 `facechain-finetune` 并发任务数严格限制为 `1`，QPS 限 `2`，需合理编排调度 [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [人物图像检测API详情](../../raw/_short/facechain-face-detection-api-3fa0c8f9a08beb3a.md)
- [FaceChain人物形象训练快速开始](../../raw/_short/facechain-quick-start-20c922b5dddad051.md)
- [人物形象训练API详情](../../raw/_short/facechain-finetune-api-98000a80fe5f2fef.md)
- [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)


