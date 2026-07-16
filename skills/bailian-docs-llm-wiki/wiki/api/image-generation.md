# image generation

阿里云百炼平台提供了一整套图像生成与编辑 API，覆盖文生图、图像编辑、图像翻译以及大量垂直创意工具（虚拟模特、鞋靴模特、扩图、擦除补全、海报生成等）。这些接口以 DashScope 网关为基础，模型来自千问（Qwen-Image）、通义万相（Wan/WanX）、Z-Image、可灵（Kling）、Vidu 等多个系列。本文面向开发者，梳理各类模型能力、调用方式、关键参数及常见限制。

## 支持的模型与功能

按能力可将图像模型大致分为四类：

- **通用文生图**：千问文生图（qwen-image 系列，擅长复杂文本渲染）、万相文生图 V2（wan2.6-t2i / wan2.5-t2i-preview / wan2.2-t2i-* / wanx2.1-t2i-*）、万相文生图 V1（wanx-v1，仅存量）、轻量快速的 z-image-turbo，以及可灵、Vidu 系列。详见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md) 与 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。
- **图像编辑 / 多图融合**：千问图像编辑（qwen-image-edit 系列，支持多图输入输出、改文字/增删物体/风格迁移）、万相通用图像编辑 2.5/2.6/2.7、万相通用图像编辑（wanx2.1-imageedit，支持风格化、指令编辑、局部重绘、去水印、扩图、超分、上色、线稿生图）、图像局部重绘（wanx-x-painting）。参见 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md) 与 [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)。
- **图像翻译**：千问图像翻译（qwen-mt-image），精准翻译图中文字并保留排版。见 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。
- **垂直创意工具**：人像风格重绘（wanx-style-repaint-v1）、虚拟模特（wanx-virtualmodel / virtualmodel-v2）、鞋靴模特（shoemodel-v1）、图像画面扩展（image-out-painting）、创意海报生成（wanx-poster-generation-v1）、人物实例分割（image-instance-segmentation）、AI 试衣 OutfitAnyone（aitryon 系列）、图像背景生成（wanx-background-generation-v2）、图像擦除补全（image-erase-completion）、人物写真 FaceChain、创意文字 WordArt 锦书。

## 调用方式

图像 API 主要有两种调用协议，选择取决于模型版本：

- **异步调用（传统主流）**：由于生成耗时较长（通常 1-2 分钟），多数模型仅支持异步。流程为「创建任务 → 轮询获取结果」两步：先 POST 创建任务拿到 `task_id`，再用 `task_id` 查询状态直至 `SUCCEEDED` 并取回图像 URL。任务创建请求必须携带请求头 `X-DashScope-Async: enable`，否则会报错 `current user api does not support synchronous calls`。返回的图像 URL 有效期为 24 小时，`task_id` 有效期也为 24 小时，请勿重复创建任务。
- **HTTP 同步调用（新版协议）**：仅新版模型支持，一次请求即可拿到结果，流程更简单，推荐大多数场景使用。目前支持同步的有 **wan2.6 / wan2.7 图像模型**、**z-image-turbo** 等，走 `multimodal-generation/generation` 端点。

> **注意**：同步调用仅限新版模型。以万相文生图为例，wan2.6 支持 HTTP 同步/异步与 SDK 调用，而 **wan2.5 及以下版本不支持 HTTP 同步调用**，只能异步 + SDK。请勿把同步协议用在旧模型上。

任务状态取值：`PENDING`（排队）、`RUNNING`（处理中）、`SUSPENDED`（挂起）、`SUCCEEDED`（成功）、`FAILED`（失败）。

不同模型使用的服务端点也不同，常见的有：

- `.../aigc/text2image/image-synthesis`（万相 V1、创意海报等文生图）
- `.../aigc/image2image/image-synthesis`（图像编辑、涂鸦、局部重绘、图像翻译、擦除补全等）
- `.../aigc/multimodal-generation/generation`（wan2.6/2.7、z-image 等新版）
- `.../aigc/image-generation/generation`（可灵、Vidu、人像风格重绘）
- `.../aigc/virtualmodel/generation`（虚拟模特、鞋靴模特）
- `.../aigc/image2image/out-painting`（图像画面扩展）
- `.../aigc/background-generation/generation`（图像背景生成）

## 关键参数

- **鉴权与请求头**：`Authorization: Bearer $DASHSCOPE_API_KEY`（必选）、`Content-Type: application/json`（必选）、异步接口需 `X-DashScope-Async: enable`。子账号调用可通过 `X-DashScope-WorkSpace` 指定业务空间 ID。
- **input**：文生图通常传 `prompt`（可选 `negative_prompt` 反向提示词）；图像编辑/参考图任务传 `image_url` / `images` / `base_image_url` / `mask_image_url` 等；新版多模态模型使用 `messages`（含 `text` 与 `image` 的 content 数组）结构。
- **parameters**：`size`（分辨率，格式 `宽*高` 或档位如 `1K`/`2K`/`4K`）、`n`（生成张数）、`style`、`watermark`、`prompt_extend`（智能改写/思考，如 z-image、wan2.6）、`thinking_mode`、`aspect_ratio`/`resolution`（可灵）等，随模型而异。

输出图像规格差异较大：例如千问 Pro/Plus 系列总像素需在 512\*512 至 2048\*2048 之间、可 1-6 张；万相 2.6 总像素在 [1280\*1280, 1440\*1440]、宽高比 [1:4, 4:1]；可灵支持 1k/2k/4k 及组图；z-image 固定 1 张。具体以各模型文档为准。

## 限制与注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有**独立的 API Key 与请求地址，不可混用**，跨地域调用会导致鉴权失败或报错。相当一部分创意工具（如虚拟模特、鞋靴模特、人像风格重绘、图像翻译、可灵、Vidu 等）**仅在华北2（北京）地域可用**。
- **专属域名迁移**：百炼为北京/新加坡地域推出业务空间专属域名（`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com` / `...ap-southeast-1.maas.aliyuncs.com`），性能与稳定性更佳，建议从 `https://dashscope.aliyuncs.com` 迁移。旧域名仍可用。
- **图片 URL 必须公网可访问**：使用自有图片时若报 `BadRequest.InputDownloadFailed`（下载图片失败），需确认 URL 完整、支持公网访问，可上传至 OSS 等云存储；URL 中不能包含中文字符。相关排查见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- **计费与限流**：只对成功生成的输出图片计费，输入图片和失败任务不计费；免费额度（通常 500 张）有效期 90 天，主账号与 RAM 子账号共享额度与限流。部分模型标注「限时免费」（公测阶段，额度用尽即不可用）。

> **注意**：多个模型（如 wanx-x-painting 局部重绘、wanx-virtualmodel/virtualmodel-v2 虚拟模特、wanx-poster-generation-v1 海报生成、image-erase-completion 擦除补全等）当前**仅供免费体验，额度用完后不可调用且不支持付费**，官方推荐迁移到千问图像编辑或万相 2.1 等替代方案。新项目集成前请确认目标模型的商业化状态。

> **注意**：万相文生图 V1（wanx-v1）已被 V2 版全面替代，官方推荐使用 V2；旧版仅适用于北京地域。选择模型时优先考虑最新版本。

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


