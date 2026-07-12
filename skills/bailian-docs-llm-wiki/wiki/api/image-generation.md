# image generation

百炼平台提供丰富的图像生成与编辑API，涵盖文生图、图像编辑、图像翻译、风格迁移、创意工具等多种能力。平台上的图像模型主要分为千问(Qwen-Image)系列、万相(Wan/Wanx)系列、Z-Image、可灵(Kling)系列以及多种垂直场景创意工具，均通过HTTP或[DashScope SDK](../concepts/dashscope-sdk.md)调用。

## 核心模型系列

### 千问-图像（Qwen-Image）

千问系列覆盖文生图、图像编辑和图像翻译三大能力，擅长复杂文本渲染和图文混合布局。详见[千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。

**文生图模型**：

| 模型名称 | 简介 | 输出规格 |
|---------|------|---------|
| qwen-image-2.0-pro（推荐） | Pro系列，文字渲染、真实质感更强 | 512x512至2048x2048，png，1-6张 |
| qwen-image-2.0（推荐） | 加速版，兼顾效果与速度 | 同上 |
| qwen-image-max | Max系列，真实感更强，AI痕迹更低 | 固定1张 |
| qwen-image-plus / qwen-image | 擅长多样化艺术风格与文字渲染 | 同上 |

**图像编辑**（qwen-image-edit系列）：支持多图输入和多图输出，可精确修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节。详见[千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。

**图像翻译**（qwen-mt-image系列）：精准翻译图像中的文字并保留原始排版，支持领域提示、敏感词过滤、术语干预等功能。详见[千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

### 万相（Wan/Wanx）系列

万相系列是百炼平台图像生成的核心模型族，按功能分为文生图和图像生成与编辑两条产品线。

**文生图V2版**（纯文本到图片）：

| 模型名称 | 简介 |
|---------|------|
| wan2.6-t2i（推荐） | 万相2.6，支持自由尺寸，总像素1280x1280至1440x1440 |
| wan2.5-t2i-preview（推荐） | 万相2.5 preview，支持自由尺寸，单边可达2700 |
| wan2.2-t2i-flash | 极速版，速度提升50% |
| wan2.2-t2i-plus | 专业版，稳定性与成功率提升 |
| wanx2.1-t2i-turbo / wanx2.1-t2i-plus | 万相2.1 |
| wanx2.0-t2i-turbo | 万相2.0 |

详见[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)。

> **注意**：V1版文生图（wanx-v1/wanx-style-repaint-v1等）已不推荐使用，建议迁移至V2版模型。

**图像生成与编辑2.7**（最新）：

| 模型名称 | 简介 |
|---------|------|
| wan2.7-image-pro | 专业版，文生图支持4K输出 |
| wan2.7-image | 生成速度更快 |

支持文生图、文生组图、图生组图、图像编辑和多图参考生成。详见[万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。

**图像生成与编辑2.6**（wan2.6-image）：支持图像编辑和图文混排输出。如需纯文生图，建议使用wan2.6-t2i。详见[万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)。

**通用图像编辑2.5**（wan2.5-image-edit）：仅需文本指令即可基于单张或多张参考图像实现主体一致的图像编辑和多图融合。详见[万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

**其他万相工具模型**（仅限北京地域）：
- **涂鸦作画**（wanx-sketch-to-image）：将涂鸦草图转为精细图像，详见[万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- **图像局部重绘**（wanx-x-painting）：对指定区域进行内容重绘，详见[万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- **通用图像编辑**（wanx-image-edit）：支持风格化、内容编辑、扩图、超分等功能，详见[万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)

> **注意**：wanx-x-painting（局部重绘）当前仅提供免费体验，免费额度用完后不可调用且不支持付费，推荐迁移至千问图像编辑或万相2.1+版本。

### Z-Image

Z-Image（z-image-turbo）是一款轻量级文生图模型，生成速度快，支持中英文字渲染，灵活适配多种分辨率与宽高比。输出像素范围512x512至2048x2048，固定生成1张。详见[Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。

### 可灵（Kling）

| 模型名称 | 能力 | 输出规格 |
|---------|------|---------|
| kling/kling-v3-image-generation | 文生图、单图参考生图 | 1k/2k分辨率，1-9张 |
| kling/kling-v3-omni-image-generation | 文生图、多图参考生图、分镜组图 | 1k/2k/4k分辨率，支持组图2-9张 |

仅限华北2（北京）地域。详见[可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

## 创意工具模型

以下模型均仅限华北2（北京）地域使用，面向特定垂直场景：

| 模型 | 功能 | 计费状态 |
|------|------|---------|
| 人像风格重绘 | 将人物照片转换为多种艺术风格 | 已商业化 |
| image-out-painting | 按宽高比/比例/方向扩展图像画面 | 已商业化（0.18元/张） |
| wanx-background-generation-v2 | 为主体商品生成背景图 | 已商业化 |
| AI试衣（aitryon / aitryon-plus） | 虚拟试衣，支持快速出图和精修 | 已商业化 |
| wanx-virtualmodel / virtualmodel-v2 | 虚拟模特，替换模特和背景 | 仅免费体验 |
| shoemodel-v1 | 鞋靴AI试穿 | 仅免费体验 |
| wanx-poster-generation-v1 | 自动生成海报背景和文字排版 | 仅免费体验 |
| image-instance-segmentation | 人物实例像素级分割 | 仅免费体验 |
| image-erase-completion | 擦除图像中的人物/物体/文字 | 仅免费体验 |
| FaceChain人物写真 | 2张照片训练人物形象，批量生成写真 | 仅免费体验 |
| WordArt锦书 | 创意艺术字生成 | 仅免费体验 |

> **注意**：标注"仅免费体验"的模型免费额度用完后不可调用且不支持付费。建议在正式业务中使用已商业化的模型（如千问图像编辑、万相2.6+版本）作为替代。

详见各模型的API参考文档：[人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)、[AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)、[图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)等。

## 调用方式

图像API支持两种调用模式：

**同步调用**（wan2.6+、qwen-image-2.0+等新版模型）：一次请求直接返回结果，流程简单，推荐大多数场景使用。

```
POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

**[异步调用](../concepts/async-invocation.md)**（所有模型均支持）：先创建任务获取`task_id`，再轮询查询结果。需要在请求头中添加`X-DashScope-Async: enable`。

```
# 1. 创建任务
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis
Header: X-DashScope-Async: enable

# 2. 查询结果
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

此外，还支持通过DashScope Python SDK和Java SDK调用。

## 关键参数

各模型的公共参数包括：

| 参数 | 说明 |
|------|------|
| `model` | 模型名称，如`wan2.7-image-pro`、`qwen-image-2.0-pro` |
| `prompt` | 文本提示词，描述期望生成的图像内容 |
| `size` | 输出图像尺寸，格式因模型而异（如`1024*1024`、`2K`、`4K`） |
| `n` | 生成图像数量 |
| `negative_prompt` | 反向提示词，排除不需要的元素（部分模型支持） |
| `ref_img` / `image`（content） | 参考图像URL，用于图生图和编辑场景 |
| `watermark` | 是否添加水印，默认为true |

> **注意**：`size`参数的取值范围因模型版本不同差异较大。例如wan2.6-t2i支持总像素1280x1280至1440x1440范围内自由设定，而qwen-image-2.0-pro支持512x512至2048x2048。调用前请查阅对应模型文档中的size参数说明。

## 地域与接入域名

- **华北2（北京）**：支持所有图像模型。推荐使用[业务空间](../concepts/workspace.md)专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
- **新加坡**：支持部分模型（千问、万相文生图V2、Z-Image等）。域名：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- **美国（弗吉尼亚）**：支持部分模型。域名：`https://dashscope-us.aliyuncs.com`

> **注意**：不同地域拥有独立的[API Key](../concepts/api-key.md)与请求地址，不可混用，跨地域调用将导致鉴权失败。创意工具类模型（人像风格重绘、虚拟模特、AI试衣等）大多仅在华北2（北京）地域可用。

## 计费与限流

- **免费额度**：开通百炼服务后自动发放，通常为500张/模型，有效期90天。主账号与RAM子账号共享。
- **计费方式**：按成功生成的输出图片数量计费，输入图片和失败请求不收费。
- **限流**：多数模型的默认限制为任务下发QPS 2、同时处理中任务数1-5。主账号与RAM子账号共享限流额度。

详见[常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 常见错误与排查

- **图片下载失败**（`BadRequest.InputDownloadFailed`）：输入图片URL无法访问，需确保URL完整且支持公网访问，建议上传至OSS等云存储。
- **任务创建curl执行失败**：Windows环境下`curl`转义规则与Linux/macOS不同，建议使用Postman等工具或按Windows语法调整命令。
- **鉴权失败**：检查是否使用了正确地域的[API Key](../concepts/api-key.md)，不同地域的Key不可混用。
- **余额不足**：免费额度用尽后需在阿里云控制台充值，或检查模型是否为"仅免费体验"状态。

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







