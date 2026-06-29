# image generation

百炼平台提供一系列图像生成与编辑模型 API，覆盖文生图、图生图、图像编辑、图像翻译、风格重绘、虚拟模特、试衣、海报、背景生成、擦除补全、画面扩展、实例分割、人物写真、创意文字等场景。所有 API 通过 DashScope HTTP 接口调用，部分模型同时支持 DashScope SDK（Python/Java），统一使用百炼 [API Key](../concepts/api-key.md) 鉴权。

## 调用模式与端点

图像 API 分为同步调用与[异步调用](../concepts/async-invocation.md)两种模式：

- **同步调用（推荐）**：一次请求即返回结果，流程简单。千问图像系列（qwen-image-2.0-pro/max/plus）、万相 2.6/2.7 文生图与编辑、Z-Image 等新版模型支持同步调用，走 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`（新加坡地域使用[业务空间](../concepts/workspace.md)专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/...`）。详见 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md) 与 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。
- **[异步调用](../concepts/async-invocation.md)**：图像处理耗时较长（通常 1-2 分钟），V1 版模型及部分编辑/创意类模型仅支持异步，分两步：① 创建任务获取 `task_id`；② 用 `task_id` 轮询 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 直到 `SUCCEEDED`。异步请求必须带请求头 `X-DashScope-Async: enable`，缺少该头会报错 "current user api does not [support](../guides/support.md) synchronous calls"。`task_id` 有效期 24 小时，请勿重复创建任务，轮询即可。详见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

> **注意**：华北2（北京）、新加坡、美国（弗吉尼亚）等地域拥有独立的 [API Key](../concepts/api-key.md) 与请求地址，不可混用，跨地域调用将导致鉴权失败。千问-图像翻译（qwen-mt-image）仅在华北2（北京）地域可用。百炼为北京/新加坡/弗吉尼亚推出[业务空间](../concepts/workspace.md)专属域名，建议迁移以获得更好性能与稳定性。

## 前提条件

1. [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 并[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
2. 如需 SDK 调用，[安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)（Python/Java）。
3. 可灵（kling）系列需先在百炼控制台搜索"可灵"并单击"立即开通"完成授权。
4. RAM 子账号 [API Key](../concepts/api-key.md) 调用时需带 `X-DashScope-WorkSpace` 指定[业务空间](../concepts/workspace.md)。

## 核心模型与功能

### 文生图

| 模型 | 系列 | 输出规格 | 调用模式 |
| --- | --- | --- | --- |
| qwen-image-2.0-pro / -2026-06-22 / -2026-04-22 / -2026-03-03 | 千问 Pro（推荐） | 自由宽高，总像素 512*512~2048*2048，默认 2048*2048，1-6 张，png | 同步 |
| qwen-image-2.0 / -2026-03-03 | 千问加速版（推荐） | 同上 | 同步 |
| qwen-image-max / -2025-12-30 | 千问 Max，真实感更强 | 固定 1 张，png | 同步 |
| qwen-image-plus / qwen-image | 千问 Plus，艺术风格 | — | 同步 |
| wan2.7-image-pro / wan2.7-image | 万相 2.7，文生图支持 4K | PNG | 同步 |
| wan2.6-t2i / wan2.6-image | 万相 2.6，图文混排输出 | 总像素 1280*1280~1440*1440，宽高比 1:4~4:1，png | 同步 |
| wan2.5-t2i-preview | 万相 2.5 preview，自由选尺寸 | 同 wan2.6 | 仅异步 |
| wan2.2-t2i-flash/plus、wanx2.1-t2i-turbo/plus、wanx2.0-t2i-turbo | 万相 2.2/2.1/2.0 | 宽高均 512~1440，png | 仅异步 |
| wanx-v1 | 万相 V1，支持参考图内容/风格迁移 | 1024*1024 等 | 仅异步 |
| z-image-turbo | Z-Image 轻量快速 | 总像素 512*512~2048*2048，固定 1 张，png | 同步 |
| kling/kling-v3-image-generation、kling/kling-v3-omni-image-generation | 可灵，文生图+参考图生图 | 1k/2k/4k，1~9 张或组图 2~9 | 异步 |

千问图像系列擅长复杂文字渲染，详见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。万相 2.6 图文混排需开启 `enable_interleave=true` 且同时设置 `X-DashScope-Sse: enable` 与 `parameters.stream=true`，仅支持[流式输出](../concepts/streaming-output.md)。

### 图像编辑

| 模型 | 系列 | 关键能力 |
| --- | --- | --- |
| qwen-image-2.0-pro / qwen-image-2.0 | 千问图像编辑（推荐） | 多图输入/输出，精确修改文字、增删移动物体、改主体动作、迁移风格 |
| qwen-image-edit-max | 千问编辑 Max | 工业设计、几何推理、角色一致性 |
| qwen-image-edit-plus / qwen-image-edit | 千问编辑 Plus/基础 | 多图输出、自定义分辨率；edit 仅固定 1 张 |
| wan2.7-image-pro | 万相 2.7 | 图像编辑、交互式编辑，最高 2K |
| wan2.6-image | 万相 2.6 | 图像编辑、图文混排 |
| wan2.5-i2i-preview | 万相 2.5 通用编辑 | 单图编辑、多图融合 |
| wanx2.1-imageedit | 万相 2.1 通用编辑 | 风格化、指令编辑、局部重绘、去水印、扩图、超分、上色、线稿生图、参考卡通生图 |

千问图像编辑支持可指定分辨率（宽高范围 [512,2048]），默认总像素接近 1024*1024 且宽高比贴近最后一张输入图。详见 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md) 与 [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)。

> **注意**：wanx-x-painting（图像局部重绘）、wanx-virtualmodel、virtualmodel-v2、shoemodel-v1、wanx-poster-generation-v1、image-instance-segmentation、image-erase-completion 等模型当前仅提供**免费体验**，额度用尽后不可调用且不支持付费，官方推荐改用千问图像编辑或万相 2.1 图像编辑。

### 图像翻译

qwen-mt-image 支持中/英文与日、韩、西、法等语种互译（不支持非中/英语种间直接翻译），保留原始排版，支持领域提示、敏感词过滤、术语干预。仅在华北2（北京）可用，[异步调用](../concepts/async-invocation.md)。详见 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

### 垂直场景与创意工具

- **涂鸦作画**：wanx-sketch-to-image-lite，手绘草图+文字生成涂鸦作品，[prompt](../guides/prompt.md)≤75 字符。
- **图像局部重绘**：wanx-x-painting，输入原图+涂抹 mask+[prompt](../guides/prompt.md) 重绘指定区域。
- **人像风格重绘**：wanx-style-repaint-v1，预置风格或自定义风格参考图，仅 HTTP 异步。
- **虚拟模特**：wanx-virtualmodel（V1）、virtualmodel-v2（V2 支持人台、改分辨率、背景参考权重）。
- **鞋靴模特**：shoemodel-v1，多视角鞋靴图对模板模特图试穿。
- **图像画面扩展（扩图）**：image-out-painting，支持按宽高比、按比例、指定方向、结合旋转。
- **创意海报**：wanx-poster-generation-v1，支持 generate/sr/hrf 三种模式，可二次提升分辨率。
- **人物实例分割**：image-instance-segmentation，像素级 mask，可作为擦除掩码输入。
- **AI 试衣**：aitryon（基础版，快速）、aitryon-plus（推荐，细节更好）、aitryon-refiner（精修）、aitryon-parsing-v1（服饰分割），可组合实现基础/精修/局部试衣/获取服饰坐标。
- **图像背景生成**：wanx-background-generation-v2，文本/图像/边缘引导，电商与海报场景。
- **图像擦除补全**：image-erase-completion，按 mask 移除人物/物体/文字/水印，保留背景。
- **人物写真**：FaceChain，2 张照片训练专属形象，批量生成多风格写真，含检测/训练/生成三个 API。
- **创意文字**：WordArt 锦书，文字变形（边缘轮廓创意变形）与文字纹理生成（自定义 3 种+预设 18 种风格）。

## 关键参数

- `model`（必选）：模型名称。
- `input`（必选）：提示词 `prompt`、图像 URL（`image_url`/`base_image_url`/`sketch_image_url`/`template_image_url` 等）、参考图等。万相 2.6/2.7 与千问、Z-Image 同步接口用 `input.messages[].content[]` 的 `text`/`image` 数组结构。
- `parameters`：分辨率 `size`（如 `1024*1024`、`2K`、`1K`）、张数 `n`、风格 `style`、水印 `watermark`、智能思考 `prompt_extend`/`thinking_mode`、负向提示 `negative_prompt`、宽高比 `aspect_ratio`、组图 `series_amount`、`ref_strength`/`ref_mode` 等。各模型支持的字段不同，以对应 API 文档为准。
- 图像 URL 需公网可访问，支持 HTTP/HTTPS；多数模型不支持 Base64（部分如人像风格重绘、擦除补全支持 Base64）。本地文件可上传获取临时 URL。URL 中不能含中文字符。

## [计费](../concepts/billing.md)与限流

- 免费额度：开通百炼服务后自动发放，有效期 90 天，主账号与 RAM 子账号共享。额度按成功输出的图片张数计算，输入图与失败任务不占用。
- 限时免费（公测阶段）：额度用尽后不可使用；明确单价的模型额度用尽或过期后按张付费（如 wanx-v1 0.16 元/张、wanx2.1-imageedit 0.14 元/张、wanx-style-repaint-v1 0.12 元/张、image-out-painting 0.18 元/张、wanx-background-generation-v2 0.08 元/张、wanx-sketch-to-image-lite 0.06 元/张）。
- 限流：主账号与 RAM 子账号共享，常见为任务下发 QPS 限制 2、同时处理中任务数 1（部分模型如 image-out-painting 同时处理 5）。详细单价与限流以 [百炼模型价格](https://help.aliyun.com/zh/model-studio/model-pricing) 与各模型文档为准。

## 常见报错

- `BadRequest.InputDownloadFailed`（下载图片失败）：输入图片 URL 不可访问或权限受限。确保 URL 完整且公网可访问，可上传至 OSS 等云存储。
- `current user api does not support synchronous calls`：异步请求缺少 `X-DashScope-Async: enable` 请求头。
- `InvalidApiKey`：API Key 无效或跨地域混用。
- 任务状态：`PENDING`（排队）→ `RUNNING`（处理）→ `SUCCEEDED`/`FAILED`，`SUSPENDED` 为挂起。结果图片 URL 有效期 24 小时。

> **注意**：使用 Postman/Apifox 等平台调试时，需将 curl 中的 `$DASHSCOPE_API_KEY` 替换为真实 API Key（如 `Bearer sk-xxxx`）。macOS/Linux 可直接执行 curl，Windows 建议用接口平台。

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



