# image generation

百炼平台提供丰富的图像生成与编辑 API，涵盖文生图、图像编辑、图像翻译、涂鸦作画、局部重绘、虚拟模特、试衣、海报生成、背景生成、擦除补全、画面扩展、人物分割、写真生成、创意文字等多种能力。底层模型包括千问图像（Qwen-Image）、万相（Wan）、Z-Image、可灵（Kling）、Vidu 等多个系列，支持同步与异步两种调用模式。

## 模型概览

### 文生图模型

| 模型系列 | 推荐模型名称 | 输出图像规格 | 调用方式 |
| --- | --- | --- | --- |
| 千问图像 | qwen-image-2.0-pro、qwen-image-2.0、qwen-image-max、qwen-image-plus | 分辨率 512×512~2048×2048，PNG，1-6张 | 同步 |
| 万相文生图 | wan2.7-image-pro、wan2.7-image、wan2.6-t2i、wan2.5-t2i-preview、wan2.2-t2i-flash/plus、wanx2.1-t2i-turbo/plus | PNG，尺寸依模型不同 | 同步（wan2.6+）/异步（2.5及以下） |
| Z-Image | z-image-turbo | 512×512~2048×2048，PNG，1张 | 同步 |
| 可灵图像 | kling/kling-v3-image-generation、kling/kling-v3-omni-image-generation | 1K/2K/4K，1-9张，PNG | 异步 |
| Vidu图像 | vidu/vidu-image_reference2image 等 | 1K/2K/4K，1张，PNG | 异步 |

千问图像模型擅长复杂文字渲染和真实质感，万相文生图支持多种艺术风格与写实摄影，Z-Image 为轻量快速生图模型，可灵支持文生图和参考图生图（含组图分镜模式），Vidu 擅长中英文字精准渲染和 UI/图表像素级还原。详见[千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)和[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

### 图像编辑模型

| 模型系列 | 推荐模型名称 | 核心能力 |
| --- | --- | --- |
| 千问图像编辑 | qwen-image-2.0-pro、qwen-image-2.0、qwen-image-edit-max、qwen-image-edit-plus | 多图输入/输出、精确修改文字、增删移动物体、风格迁移、细节增强 |
| 万相图像编辑 | wan2.7-image-pro、wan2.6-image、wan2.5-i2i-preview、wanx2.1-imageedit | 单图编辑、多图融合、风格化、去水印、扩图、超分、上色、线稿生图 |
| 万相局部重绘 | wanx-x-painting | 基于涂抹区域和提示词的局部重绘 |
| 万相涂鸦作画 | wanx-sketch-to-image-lite | 手绘图案+文字描述生成涂鸦绘画 |

千问图像编辑模型支持多图融合和精确文字修改，万相通用编辑覆盖风格化、局部重绘、去水印、扩图、超分等场景。详见[千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。

### 图像翻译

千问-图像翻译模型（qwen-mt-image）可精准翻译图像中的文字并保留原始排版，支持中/英文与日/韩/西/法等语种互译（不支持非中英语种间直接翻译），还支持领域提示、敏感词过滤、术语干预。详见[千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

### 创意工具类模型

| 模型名称 | 功能 | 状态 |
| --- | --- | --- |
| wanx-style-repaint-v1 | 人像风格重绘 | 付费 |
| wanx-virtualmodel / virtualmodel-v2 | 虚拟模特生成 | 免费体验 |
| shoemodel-v1 | 鞋靴模特试穿 | 免费体验 |
| image-out-painting | 图像画面扩展 | 付费 |
| wanx-poster-generation-v1 | 创意海报生成 | 免费体验 |
| image-instance-segmentation | 人物实例分割 | 免费体验 |
| aitryon / aitryon-plus / aitryon-refiner / aitryon-parsing-v1 | AI试衣（基础/Plus/精修/分割） | 付费 |
| wanx-background-generation-v2 | 图像背景生成 | 付费 |
| image-erase-completion | 图像擦除补全 | 免费体验 |
| FaceChain | 人物写真生成 | — |
| WordArt锦书 | 创意文字变形/纹理生成 | — |

> **注意**：wanx-x-painting、wanx-virtualmodel、virtualmodel-v2、image-erase-completion、image-instance-segmentation、shoemodel-v1、wanx-poster-generation-v1 等模型当前仅提供免费体验，额度用完后不可调用且不支持付费。官方推荐参考千问图像编辑或万相2.1图像编辑获取替代方案。

## 调用方式

### 同步调用（推荐）

适用于千问图像、万相2.6+、Z-Image、千问3.0等新版模型。一次请求即可获得结果：

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

请求体采用 `model` + `input.messages`（含 `text`/`image` 内容块）+ `parameters` 结构，类似[多模态](../concepts/multimodal.md)对话格式。

### [异步调用](../concepts/async-invocation.md)

适用于万相2.5及以下版本、可灵、Vidu、以及大部分创意工具类模型。分两步：

1. **创建任务**：发送请求，获取 `task_id`（有效期24小时）。
2. **轮询结果**：使用 `task_id` 查询任务状态，成功后获取图像URL（有效期24小时）。

创建任务时必须携带 `X-DashScope-Async: enable` 请求头，否则会报错。接口路径因功能不同而异：
- 文生图：`/api/v1/services/aigc/text2image/image-synthesis`
- 图生图/编辑：`/api/v1/services/aigc/image2image/image-synthesis`
- 可灵/Vidu图像生成：`/api/v1/services/aigc/image-generation/generation`
- 虚拟模特：`/api/v1/services/aigc/virtualmodel/generation`
- 背景生成：`/api/v1/services/aigc/background-generation/generation`
- 画面扩展：`/api/v1/services/aigc/image2image/out-painting`

## 关键参数

| 参数 | 适用场景 | 说明 |
| --- | --- | --- |
| `prompt` | 文生图/编辑 | 正向提示词，描述期望生成的图像内容 |
| `negative_prompt` | 文生图 | 反向提示词，描述不希望出现的元素（V1版本支持） |
| `size` | 通用 | 输出图像分辨率，如 `1024*1024`、`1K`、`2K`、`4K` |
| `n` | 通用 | 输出图像张数，范围1-9（因模型而异） |
| `style` | 文生图 | 风格预设，如 `<auto>`、`<watercolor>` |
| `watermark` | 通用 | 是否添加水印，默认 true |
| `prompt_extend` | 万相/Z-Image/千问3.0 | 开启智能提示词扩展，优化生成效果 |
| `thinking_mode` | 万相2.7 | 开启智能思考模式 |
| `enable_interleave` | 万相2.6 | 开启图文混排输出（仅流式） |
| `aspect_ratio` / `resolution` | 可灵 | 宽高比（16:9/9:16/1:1）和分辨率（1k/2k/4k） |

## [计费](../concepts/billing.md)与[限流](../concepts/rate-limit.md)

- **免费额度**：开通百炼服务后自动发放，有效期90天，主账号与RAM子账号共享。仅成功生成的输出图片占用免费额度。
- **限时免费**：公测阶段模型，免费额度用尽后不可使用。
- **商业化模型**：如 wanx-v1（0.16元/张）、wanx2.1-imageedit（0.14元/张）、image-out-painting（0.18元/张）等，按成功输出图片[计费](../concepts/billing.md)。
- **[限流](../concepts/rate-limit.md)**：任务下发接口QPS限制通常为2，同时处理中任务数量1-5（因模型而异），主账号与RAM子账号共享。详见[常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 限制与注意事项

- **地域隔离**：华北2（北京）、新加坡、美国（弗吉尼亚）地域拥有独立的 [API Key](../concepts/api-key.md) 与请求地址，不可混用，跨地域调用将导致鉴权失败。建议使用[业务空间](../concepts/workspace.md)专属域名 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
- **图片URL要求**：输入图片URL需支持公网访问。若报错"下载图片失败"，请确保URL完整且可公网访问，可将图片上传至OSS等云存储。
- **图片格式与大小**：支持 JPEG、PNG、BMP、WEBP 等格式，图片大小建议小于5-10MB，分辨率不低于512×512。
- **task_id与结果有效期**：task_id 有效期24小时，生成结果图像URL有效期24小时，请及时下载。
- **SDK支持**：千问、万相等模型支持 [DashScope SDK](../concepts/dashscope-sdk.md)（Python/Java），部分创意工具类模型（如人像风格重绘）仅提供HTTP API。

> **注意**：万相文生图V1版（wanx-v1）为早期模型，官方推荐使用升级后的V2版模型。万相2.5及以下版本不支持HTTP同步调用，仅支持[异步调用](../concepts/async-invocation.md)。

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
- [千问-图像生成与编辑3.0 API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)








