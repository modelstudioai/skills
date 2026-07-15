# image generation

阿里云百炼平台提供覆盖文生图、图像编辑、图像翻译及一系列创意工具的图像生成 API，涵盖千问（Qwen-Image）、万相（Wan/Wanx）、Z-Image、可灵（Kling）、Vidu 等模型家族。这些接口统一通过 DashScope 网关调用，既支持 HTTP，也支持 DashScope Python/Java SDK，可满足文生图、图生图、局部重绘、扩图、背景生成、虚拟模特、AI 试衣、创意海报等多样化场景。

## 支持的模型与功能

按能力大致可分为四类：

- **通用文生图**：千问 `qwen-image-*` 系列擅长复杂文本渲染与图文混排；万相 `wan2.6-t2i` / `wan2.5-t2i-preview` / `wan2.2-t2i-*` / `wanx2.1-t2i-*` 系列支持写实与多种艺术风格；`z-image-turbo` 为轻量快速生图模型，支持中英文字渲染。详见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 与 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。
- **图像编辑 / 生成一体**：`qwen-image-edit-*`、`wan2.7-image*`、`wan2.6-image`、`wan2.5-i2i-preview`、`wanx2.1-imageedit` 支持单图编辑、多图融合、图文混排、局部重绘、去水印、扩图、超分、上色、线稿生图等。参见 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md) 与 [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)。
- **第三方模型**：可灵 `kling/kling-v3-*`（文生图、参考图生图、分镜组图）、Vidu `vidu/*`（参考生图、文生图、图片编辑，最多 14 张参考图）。
- **创意与电商工具**：人像风格重绘、虚拟模特、鞋靴模特、图像画面扩展（扩图）、创意海报生成、人物实例分割、AI 试衣 OutfitAnyone、图像背景生成、图像擦除补全、人物写真 FaceChain、创意文字 WordArt 锦书、千问图像翻译（Qwen-MT-Image）。

## 调用方式

绝大多数图像模型处理耗时较长（通常 1-2 分钟），因此接口以**异步**为主，流程分两步：

1. **创建任务获取任务 ID**：提交请求，必须设置请求头 `X-DashScope-Async: enable`（缺失会报错 `current user api does not support synchronous calls`），返回 `task_id`。
2. **根据任务 ID 轮询结果**：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`，任务成功后返回图像 URL，**有效期 24 小时**，`task_id` 有效期同样为 24 小时。**请勿重复创建任务**，轮询即可。

新一代模型（如 `wan2.6-image`、`wan2.7-image`、`z-image-turbo`）新增 **HTTP 同步调用**，一次请求即可返回结果，接口路径为 `.../aigc/multimodal-generation/generation`，请求体采用 `messages` 结构（`content` 内含 `text` / `image`）。

> **注意**：不同模型的接口路径并不统一。文生图 V1/涂鸦/局部重绘等旧模型走 `.../text2image/image-synthesis` 或 `.../image2image/image-synthesis`；可灵、Vidu 走 `.../image-generation/generation`；虚拟模特、鞋靴模特走 `.../virtualmodel/generation`；扩图走 `.../image2image/out-painting`。调用前请以对应模型文档为准。

## 关键参数

- `model`（必选）：模型名，如 `wanx2.1-t2i-turbo`、`qwen-mt-image`、`wan2.6-image` 等。
- `input`：输入内容。文生图用 `prompt`，可附 `negative_prompt`；新协议模型用 `messages`；图像编辑/参考类用 `images`、`image_url`、`base_image_url`、`mask_image_url` 等。
- `parameters`：`size`（如 `1024*1024`、`1K`/`2K`/`4K`）、`n`（生成张数）、`aspect_ratio`、`resolution`、`watermark`、`prompt_extend`（智能扩写/思考）、`thinking_mode` 等，按模型不同而异。

分辨率与张数因模型而异：千问 Pro 系列总像素 512\*512～2048\*2048、可生成 1-6 张；`qwen-image-max` 固定 1 张；万相 2.6 总像素在 1280\*1280～1440\*1440；可灵支持 1k/2k/4k、1-9 张。

## 计费、限流与注意事项

- **计费**：仅对模型**成功生成的输出图片**计费，输入图片及处理失败不计费、不占免费额度。免费额度开通后自动发放，有效期 90 天，主账号与 RAM 子账号共享。计费与限流详情见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **限流**：主账号与 RAM 子账号共用任务下发 QPS 与同时处理中任务数量限制。
- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有**独立的 API Key 与请求地址，不可混用**，跨地域调用会导致鉴权失败或报错。百炼推荐迁移到业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），现有域名仍可用。
- **输入图片要求**：图片 URL 必须公网可访问，否则报 `BadRequest.InputDownloadFailed`；URL 不能包含中文字符；常见格式限制为 JPG/PNG/JPEG/BMP/WEBP，分辨率多要求 [512, 4096] 像素、大小不超过 10MB。

> **注意**：部分创意工具模型（如 `wanx-x-painting` 图像局部重绘、`wanx-virtualmodel`/`virtualmodel-v2` 虚拟模特、`shoemodel-v1` 鞋靴模特、`wanx-poster-generation-v1` 创意海报、`image-erase-completion` 图像擦除补全、`image-instance-segmentation` 人物实例分割）当前**仅提供免费体验，免费额度用完后不可调用且不支持付费**。官方建议迁移到 [千问-图像编辑](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)或万相 2.1 等替代方案。

> **注意**：文生图 V1 版（`wanx-v1`）已被 V2 版全面替代，且仅适用于华北2（北京）地域；千问图像翻译（`qwen-mt-image`）同样仅在华北2（北京）可用，且不支持非中/英语种之间的直接互译（如日译韩）。新项目应优先选择推荐的新版模型。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)
- [Vidu-图像生成API参考](../../raw/model-api-reference/image-generation/vidu-image-models/vidu-image-generation-api-reference.md)


