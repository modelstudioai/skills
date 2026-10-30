# image generation

百炼平台提供多种图像生成能力，覆盖文生图（T2I）、图生图（I2I）、图像编辑、局部重绘、风格迁移及垂直场景工具（如虚拟模特、海报生成、FaceChain写真等）。核心模型包括千问图像系列（qwen-image-*）、万相系列（wanx-*, wan2.*）、可灵（kling）、Vidu、Z-Image及创意工具套件。所有服务均需地域对齐的API Key与Endpoint，并强烈建议迁移到业务空间专属域名以获得更优性能。

## 支持的模型/功能

- **通用文生图与编辑**：`qwen-image-3.0-pro`、`qwen-image-3.0` 支持T2I与I2I一体化调用；`wan2.7-image-pro` 支持4K文生图输出；`z-image-turbo` 为轻量级快速生图模型 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **多模态编辑与融合**：`wan2.5-i2i-preview` 支持单图编辑与多图融合；`kling/kling-v3-omni-image-generation` 支持多图输入与分镜组图生成；`vidu/viduq2-pro_reference2image` 擅长UI/图表像素级还原 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。
- **垂直创意工具**：包括人像风格重绘（`wanx-style-repaint-v1`）、虚拟模特（`wanx-virtualmodel`）、鞋靴AI试穿（`shoemodel-v1`）、创意海报生成（`wanx-poster-generation-v1`）及FaceChain人物写真（需先训练`facechain-finetune`模型）[创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。
- **免费体验模型**：`wanx-x-painting`（局部重绘）、`image-erase-completion`（擦除补全）、`image-instance-segmentation`（实例分割）等当前仅限免费额度使用，用尽后不可调用且不支持付费 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

> **注意**：`wanx-v1`（万相V1）和`qwen-image-2.0`早期模型已被明确标记为“推荐使用全面升级的[文生图V2版模型](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)”或“早期图像模型”，实际生产环境应优先选用`wan2.6-t2i`、`qwen-image-3.0`等新版模型。

## 关键参数

- **`size`**：控制输出分辨率。格式因模型而异：`qwen-image-*` 接受 `宽*高`（如`1024*1024`）或预设值（如`2K`）；`kling` 和 `vidu` 仅支持枚举值（`1K`/`2K`/`4K`）；`z-image-turbo` 要求总像素在`512*512`至`2048*2048`之间。
- **`n` / `series_amount`**：控制生成张数。`n` 适用于多数模型（如`kling`文生图，范围1–9）；`series_amount` 专用于`kling-v3-omni`的组图模式（2–9）。
- **`watermark`**：布尔值，控制是否添加水印（如`wan2.7-image-pro`默认`true`，可设为`false`关闭）。
- **`thinking_mode`**：部分万相模型（如`wan2.7-image-pro`）支持开启思考模式以提升语义一致性。
- **`element_list`**：`kling`模型特有，用于指定需保持一致性的主体列表，与参考图数量之和≤10。

## 使用方式

- **同步调用**：适用于响应快、低延迟场景。`qwen-image-*`（DashScope同步）、`wan2.7-image-pro`、`z-image-turbo` 均支持HTTP同步请求，Endpoint为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`。
- **异步调用**：适用于耗时较长任务（通常1–2分钟）。`kling`、`vidu`、`wan2.5-i2i-preview`、`wanx-sketch-to-image-lite` 等必须使用异步流程：先`POST /generation`获取`task_id`，再轮询`GET /tasks/{task_id}`查询结果。所有异步请求**必须携带 `X-DashScope-Async: enable` 请求头**，否则报错 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。
- **OpenAI 兼容模式**：`qwen-image-*` 支持通过`/images/generations`接口调用，不传`image`为T2I，传`image`为I2I，仅同步非流式。
- **专用流程**：FaceChain需三步——先调用`facechain-facedetect`校验人脸质量，再上传图片并调用`facechain-finetune`训练专属模型，最后基于训练所得`resource_id`生成写真。

## 限制和注意事项

- **地域强绑定**：API Key、Endpoint URL、业务空间ID（`{WorkspaceId}`）**必须属于同一地域**（如华北2北京、新加坡、美国弗吉尼亚）。跨地域调用将导致鉴权失败或服务报错，此限制适用于所有模型 [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。
- **输入图像限制**：`kling`要求参考图宽高比在`1:2.5 ~ 2.5:1`，且不支持透明通道；`vidu`最多支持14张参考图；`shoemodel-v1`要求模板图与鞋图比例在`[2:3, 3:2]`内且多视角图≤3张。
- **免费额度与限流**：多数创意工具模型（如`wanx-x-painting`、`shoemodel-v1`）仅限免费额度（500张），用尽即停；`facechain-finetune`计费2.5元/次，QPS限制为2，同时处理任务数上限为1 [FaceChain人物写真生成模型计量计费](../../raw/_short/facechain-billing-eb89b38a921f33a8.md)。
- **域名迁移强制建议**：华北2（北京）与新加坡地域已启用业务空间专属域名（如`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧域名（`dashscope.aliyuncs.com`）虽仍可用，但新域名提供“卓越的性能和更高的稳定性”，文档中多次强调“建议迁移” [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

## 来源文档

- [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md)
- [千问-图像生成与编辑 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)
- [千问-早期图像模型](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-api.md)
- [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/legacy-qwen-image-models/qwen-image-edit-api.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)
- [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)
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


