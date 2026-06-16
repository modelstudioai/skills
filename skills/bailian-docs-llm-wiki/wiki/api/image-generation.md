# image generation

百炼平台提供了丰富的图像生成与编辑 API，覆盖文生图、图像编辑、风格迁移、电商场景等多种能力。主要模型系列包括千问 Qwen-Image、万相 Wanx/Wan、Z-Image 以及可灵 Kling，开发者可根据质量、速度和功能需求选择合适的模型。所有图像 API 均通过 HTTP 调用，大部分模型同时支持同步和异步两种调用模式。

## 核心模型系列

### 千问-文生图 / 图像编辑（Qwen-Image）

千问图像模型同时支持生成和编辑，擅长**复杂文本渲染**和图文混合布局。推荐使用 `qwen-image-2.0-pro` 或 `qwen-image-2.0`，前者文字渲染和真实质感更强，后者兼顾效果与速度。详细参数和调用方式参见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md) 和 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)。

- 输出分辨率：总像素在 512x512 至 2048x2048 之间，默认 2048x2048（生成）或 1024x1024（编辑）
- 输出格式：PNG
- 生成张数：1-6 张（Pro/2.0 系列），Max 系列固定 1 张
- 编辑能力：支持多图输入/输出，可修改文字、增删物体、迁移风格、增强细节

千问还提供 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)（`qwen-mt-image`），可翻译图像中的文字并保留原始排版，支持中英日韩等多语种，以及领域提示和术语干预。

### 万相文生图（Wan T2I）

万相文生图有多个版本迭代，推荐使用最新版本：

| 模型 | 特点 |
|------|------|
| `wan2.7-image-pro` | 万相 2.7 专业版，文生图支持 4K 输出，同时支持文生组图、图生组图、图像编辑 |
| `wan2.7-image` | 万相 2.7 标准版，生成速度更快 |
| `wan2.6-image` | 支持图像编辑和图文混排输出 |
| `wan2.6-t2i` | 文生图专用，支持自由尺寸 |
| `wan2.5-t2i-preview` | 支持更灵活的宽高比（单边可达 2700） |

详细参数参见 [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md) 和 [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)。

> **注意**：万相文生图 V1 版（`wanx-v1`）已不再推荐，建议迁移到 V2 或更新版本。V1 仅支持异步调用且仅限北京地域。

### Z-Image

Z-Image（`z-image-turbo`）是轻量级文生图模型，生成速度快，支持中英文字渲染。输出分辨率在 512x512 至 2048x2048 之间，固定输出 1 张 PNG 图像。支持 `prompt_extend=true` 参数开启智能思考，系统会优化提示词但会增加响应时间。

### 可灵图像生成（Kling）

可灵提供 `kling/kling-v3-image-generation` 和 `kling/kling-v3-omni-image-generation` 两个模型，支持文生图和参考图生图。Omni 版支持多图输入和分镜组图生成，最高支持 4K 分辨率。使用前需在百炼控制台单独开通可灵 AI 服务。详见 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md)。

> **注意**：可灵模型仅适用于北京地域。

## 图像编辑类模型

除千问和万相 2.6/2.7 内置的编辑能力外，平台还提供多个专用编辑模型：

| 模型 | 功能 | 模型名称 |
|------|------|----------|
| 通用图像编辑 2.5 | 单图编辑、多图融合、主体一致性编辑 | `wan2.5-i2i-preview` |
| 通用图像编辑 2.1 | 风格化、指令编辑、局部重绘、去水印、扩图、超分、上色、线稿生图 | `wanx2.1-imageedit` |
| 图像局部重绘 | 根据涂抹区域和提示词局部重绘 | `wanx-x-painting` |
| 图像画面扩展 | 按宽高比/比例/方向扩展画面，支持旋转 | `image-out-painting` |
| 图像擦除补全 | 移除人物、物体、文字、水印等并补全背景 | `image-erase-completion` |

> **注意**：`wanx-x-painting`、`image-erase-completion` 等部分模型仅提供免费体验，额度用完后不可付费续用，推荐使用千问图像编辑或万相 2.1 作为替代方案。

详见 [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md) 和 [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)。

## 电商与行业场景模型

| 模型 | 功能 | 模型名称 |
|------|------|----------|
| 虚拟模特 | 替换商品图中的模特和背景 | `wanx-virtualmodel` / `virtualmodel-v2` |
| 鞋靴模特 | 鞋靴 AI 试穿 | `shoemodel-v1` |
| AI 试衣 OutfitAnyone | 虚拟试衣（基础版/Plus版/精修/分割） | `aitryon` 等 |
| 图像背景生成 | 为商品主体生成背景，支持文本/图像引导 | `wanx-background-generation-v2` |
| 人物实例分割 | 像素级人物分割掩码 | `image-instance-segmentation` |
| 创意海报生成 | 自动生成海报背景和文字排版 | `wanx-poster-generation-v1` |
| 人像风格重绘 | 将人物照片转换为多种艺术风格 | `wanx-style-repaint-v1` |
| 人物写真 FaceChain | 2 张照片训练专属形象并批量生成写真 | FaceChain 系列 |

> **注意**：虚拟模特、鞋靴模特、创意海报生成等部分模型仅提供免费体验额度，不支持付费。

## 创意文字

WordArt 锦书支持文字变形和文字纹理生成，可通过提示词对汉字轮廓进行创意变形或添加艺术纹理，适用于海报、配图等场景。详见 [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/wordart-quick-start.md)。

## 调用方式

所有图像 API 的调用流程大致相同：

1. **获取 API Key** 并配置到环境变量 `DASHSCOPE_API_KEY`
2. **选择调用模式**：
   - **同步调用**（推荐，新版模型如 Qwen-Image 2.0、Wan 2.6/2.7、Z-Image）：单次请求直接返回结果
   - **异步调用**（旧版模型如 V1 文生图、涂鸦作画等）：先提交任务获取 `task_id`，再轮询查询结果
3. **请求地址**：
   - 北京：`https://dashscope.aliyuncs.com/api/v1/services/aigc/...`
   - 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/...`

> **注意**：北京和新加坡地域的 API Key 与请求地址相互独立，不可混用。新加坡旧版域名 `dashscope-intl.aliyuncs.com` 即将下线，请迁移到新版域名。

## 通用参数说明

- `model`：模型名称
- `size`：输出图像尺寸，不同模型支持的尺寸范围不同
- `n`：生成图片数量
- `prompt`（或 `messages[].content[].text`）：文本提示词
- `image`（或 `messages[].content[].image`）：输入参考图像 URL
- `watermark`：是否添加水印，默认部分模型为 true
- `seed`：随机种子，用于结果复现

## 常见问题

- 图像 URL 有效期通常为 24 小时，需及时下载
- 免费额度用完后需付费才能继续调用（部分仅免费体验的模型除外）
- 限流按主账号维度计算，RAM 子账号共享限流配额
- 调试时可直接使用 curl 命令（macOS/Linux）或 Postman 等工具（Windows）

更多调试和计费细节参见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 来源文档

- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-api-reference.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wanx-sketch-to-image-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/portrait-style-redraw-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/vary-region-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-instance-segmentation-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/wanx-background-generation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-erase-completion-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/wordart-quick-start.md)
- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md)






