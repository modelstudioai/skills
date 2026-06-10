# image generation

百炼平台提供丰富的图像生成与编辑 API，涵盖文生图、图像编辑、图像翻译、涂鸦作画、背景生成、虚拟试衣等多种能力。开发者可通过 HTTP 或 DashScope SDK 调用这些模型，主要分为千问图像系列、万相系列、Z-Image、可灵以及多个垂直场景专用模型。

## 模型系列总览

### 千问图像系列（Qwen-Image）

千问图像系列包含文生图、图像编辑和图像翻译三大能力，详见[千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api.md)和[千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-edit-api.md)。

**文生图模型：**

| 模型名称 | 特点 | 输出规格 |
|---------|------|---------|
| qwen-image-2.0-pro | Pro 系列，文字渲染和真实质感更强 | 总像素 512x512 ~ 2048x2048，png，1-6 张 |
| qwen-image-2.0 | 加速版，兼顾效果与速度 | 同上 |
| qwen-image-max | Max 系列，真实感更强，AI 痕迹更低 | 固定 1 张 |
| qwen-image-plus / qwen-image | Plus 系列，擅长多样化艺术风格 | 固定 1 张 |

**图像编辑模型：**

| 模型名称 | 特点 |
|---------|------|
| qwen-image-2.0-pro / qwen-image-2.0 | 与文生图共用模型名，通过输入图像触发编辑模式 |
| qwen-image-edit-max | 工业设计、几何推理、角色一致性更强 |
| qwen-image-edit-plus | 支持多图输出与自定义分辨率 |
| qwen-image-edit | 支持单图编辑和多图融合，不可指定分辨率 |

**图像翻译模型（qwen-mt-image）：** 精准翻译图像中文字并保留排版，支持中/英文与其他语种互译，但不支持非中英语种之间的直接翻译。仅限中国内地地域使用，详见[千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

### 万相系列（Wan/Wanx）

万相系列按版本演进提供文生图和图像编辑能力，详见[万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/text-to-image-v2-api-reference.md)和[万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)。

**文生图模型：**

| 模型名称 | 版本 | 特点 |
|---------|------|------|
| wan2.7-image-pro | 2.7 | 文生图支持 4K 输出，同时支持图像编辑和组图生成 |
| wan2.7-image | 2.7 | 生成速度更快 |
| wan2.6-t2i | 2.6 | 支持自由尺寸，总像素 1280x1280 ~ 1440x1440 |
| wan2.5-t2i-preview | 2.5 | 支持灵活尺寸，单边可达 2700 |
| wan2.2-t2i-flash / plus | 2.2 | 极速版速度提升 50% |
| wanx2.1-t2i-turbo / plus | 2.1 | 极速版和专业版 |
| wanx2.0-t2i-turbo | 2.0 | 极速版 |
| wanx-v1 | 1.0 | 旧版文生图，仅限北京地域 |

**图像编辑模型：**

| 模型名称 | 能力 |
|---------|------|
| wan2.6-image | 图像编辑 + 图文混排输出 |
| wan2.5-i2i-preview | 单图编辑、多图融合 |
| wanx2.1-imageedit | 风格化、指令编辑、局部重绘、去水印、扩图、超分、上色、线稿生图等 |

> **注意**：万相 2.6 及以上版本支持 HTTP 同步调用；2.5 及以下版本仅支持异步调用，需两步操作（创建任务 + 轮询结果）。

### Z-Image

Z-Image（z-image-turbo）是轻量级文生图模型，生成速度快，支持中英文字渲染，总像素范围 512x512 ~ 2048x2048。支持"智能思考"能力（设置 `prompt_extend=true`），可返回优化后的提示词及推理过程，详见[Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-api-reference.md)。

### 可灵图像生成（Kling）

可灵模型支持文生图和参考图生图，需先在百炼控制台开通可灵 AI 服务。仅限北京地域，详见[可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-generation-api-reference.md)。

| 模型名称 | 能力 | 分辨率 |
|---------|------|--------|
| kling/kling-v3-image-generation | 文生图、单图参考生图 | 1k/2k |
| kling/kling-v3-omni-image-generation | 文生图、多图参考、分镜组图 | 1k/2k/4k |

## 垂直场景模型

以下模型面向特定场景，大部分仅限北京地域，且多数处于免费体验阶段（500 张额度），额度用尽后不可调用。

| 模型 | 用途 | 计费状态 |
|------|------|---------|
| wanx-style-repaint-v1 | 人像风格重绘，多种预设/自定义艺术风格 | 0.12 元/张 |
| wanx-x-painting | 图像局部重绘 | 仅免费体验 |
| image-out-painting | 图像画面扩展（扩图），支持按比例/方向/宽高比扩展 | 0.18 元/张 |
| wanx-background-generation-v2 | 商品背景生成，支持文本/图像/边缘引导 | 0.08 元/张 |
| wanx-virtualmodel / virtualmodel-v2 | 虚拟模特，替换模特和背景 | 仅免费体验 |
| shoemodel-v1 | 鞋靴模特，AI 试穿 | 仅免费体验 |
| wanx-poster-generation-v1 | 创意海报生成 | 仅免费体验 |
| image-instance-segmentation | 人物实例分割 | 仅免费体验 |
| image-erase-completion | 图像擦除补全 | 仅免费体验 |
| aitryon / aitryon-plus | AI 试衣，基础版/Plus 版 | 收费 |
| FaceChain | 人物写真生成（训练 + 推理） | 收费 |
| WordArt 锦书 | 创意文字变形与纹理生成 | 收费 |

> **注意**：部分仅免费体验的模型（如虚拟模特、图像局部重绘、图像擦除补全）官方推荐迁移到千问图像编辑或万相 2.1 通用图像编辑作为替代方案。

## 调用方式

### 同步调用

较新模型（千问图像 2.0 系列、万相 2.6/2.7、Z-Image）支持同步调用，一次请求直接返回结果：

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

请求头需包含 `Authorization: Bearer $DASHSCOPE_API_KEY` 和 `Content-Type: application/json`。

### 异步调用

大多数图像模型采用异步模式，分两步完成：

1. **创建任务**：发送请求获取 `task_id`，需设置请求头 `X-DashScope-Async: enable`
2. **轮询结果**：使用 `GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}` 查询状态，`task_id` 有效期 24 小时

不同模型的创建任务 endpoint 不同，例如：
- 文生图 V1：`/api/v1/services/aigc/text2image/image-synthesis`
- 图像编辑类：`/api/v1/services/aigc/image2image/image-synthesis`
- 背景生成：`/api/v1/services/aigc/background-generation/generation/`

### SDK 调用

DashScope SDK 支持 Python 和 Java，使用前需安装 SDK 并配置 API Key 环境变量。

## 关键参数

| 参数 | 说明 | 适用模型 |
|------|------|---------|
| `size` / `aspect_ratio` | 输出图像尺寸或宽高比 | 大部分模型 |
| `n` | 生成图像数量 | 大部分模型 |
| `prompt_extend` | 智能扩展提示词 | 万相 2.6+、Z-Image |
| `watermark` | 是否添加水印 | 万相 2.7、2.6 |
| `thinking_mode` | 启用思考模式 | 万相 2.7 |
| `negative_prompt` | 反向提示词 | 文生图 V1 |
| `style` | 图像风格 | 文生图 V1、涂鸦作画 |
| `ref_image` / `ref_strength` / `ref_mode` | 参考图相关参数 | 文生图 V1 |
| `enable_interleave` | 图文混排输出（需流式） | 万相 2.6 |

## 地域与鉴权

- **北京地域**：`https://dashscope.aliyuncs.com`
- **新加坡地域**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
- **弗吉尼亚地域**：`https://dashscope-us.aliyuncs.com`（仅部分万相模型支持）

> **注意**：各地域拥有独立的 API Key 与请求地址，不可混用，跨地域调用将导致鉴权失败。新加坡地域的旧版域名 `https://dashscope-intl.aliyuncs.com` 即将下线，请迁移到新版域名。

## 限流与计费

- 各模型的任务下发接口 QPS 限制通常为 2，同时处理中任务数量为 1-5 个，主账号与 RAM 子账号共享限流
- 新用户通常有 500 张免费额度（90 天有效），部分模型免费体验额度用尽后不可调用
- 仅对成功生成的输出图片计费，生成失败不收费
- 详细计费信息参见[常见问题](../../raw/model-api-reference/image-generation/image-faq.md)

## 常见问题

- **图像无法下载**（`BadRequest.InputDownloadFailed`）：确保输入图片 URL 为公网可访问地址，不包含中文字符
- **不支持同步调用**（`current user api does not support synchronous calls`）：异步接口必须设置 `X-DashScope-Async: enable` 请求头
- **鉴权失败**：检查 API Key 是否与请求地域匹配，北京和新加坡的 API Key 不可混用
- **本地文件如何使用**：可通过上传文件获取临时 URL 的方式将本地图片转为公网可访问链接

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


