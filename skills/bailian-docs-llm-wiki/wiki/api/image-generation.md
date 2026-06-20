# image generation

百炼平台提供丰富的图像生成与编辑 API，涵盖文生图、图像编辑、图像翻译、涂鸦作画、背景生成等多种能力。这些 API 主要来自千问（Qwen-Image）、万相（Wan/WanX）、可灵（Kling）、Z-Image 等模型系列，支持通过 HTTP 和 [DashScope SDK](../concepts/dashscope-sdk.md) 调用。开发者可根据场景需求选择不同模型，实现从通用图像生成到电商创意工具的完整图像处理流水线。

## 模型系列总览

### 千问图像系列（Qwen-Image）

千问图像系列包含文生图、图像编辑和图像翻译三大能力，详见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。

**文生图模型：**

| 模型名称 | 特点 | 输出规格 |
|---------|------|---------|
| `qwen-image-2.0-pro` | Pro 系列，文字渲染、真实质感、语义遵循能力最强 | 512\*512 至 2048\*2048，1-6 张，PNG |
| `qwen-image-2.0` | 加速版，兼顾效果与速度 | 同上 |
| `qwen-image-max` | Max 系列，真实感更强，AI 合成痕迹更低 | 固定 1 张，PNG |
| `qwen-image-plus` / `qwen-image` | Plus 系列，擅长多样化艺术风格与文字渲染 | 固定 1 张，PNG |

**图像编辑**（`qwen-image-2.0-pro` / `qwen-image-2.0`）：支持多图输入和多图输出，可修改图内文字、增删或移动物体、改变主体动作、迁移图片风格及增强画面细节。详见 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。

**图像翻译**（`qwen-mt-image`）：可翻译图像中的文字并保留原始排版，支持领域提示、敏感词过滤、术语干预等自定义功能。仅华北2（北京）地域可用。详见 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

### 万相系列（Wan/WanX）

万相系列是百炼平台最全面的图像生成模型家族，从基础文生图到专业图像编辑均有覆盖。

**文生图与图像编辑：**

| 模型名称 | 版本 | 核心能力 | 接口方式 |
|---------|------|---------|---------|
| `wan2.7-image-pro` / `wan2.7-image` | 2.7 | 文生图、文生组图、图生组图、图像编辑、多图参考，Pro 版文生图支持 4K | 同步（推荐） |
| `wan2.6-image` | 2.6 | 图像编辑、图文混排输出 | 同步 |
| `wan2.6-t2i` | 2.6 | 文生图，支持多种艺术风格与写实摄影 | 异步 |
| `wan2.5-image-edit` | 2.5 | 单图编辑、多图融合、主体一致性编辑 | 同步 |
| `wanx2.1-imageedit` | 2.1 | 全局/局部风格化、指令编辑、局部重绘、去水印、扩图、超分、上色、线稿生图 | 异步 |
| `wanx-v1` | V1 | 基础文生图，支持中英文双语和参考图 | 异步 |

**专项能力模型：**

- `wanx-sketch-to-image-lite`：涂鸦作画，通过手绘图案和文字描述生成精美图像。详见 [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)。
- `wanx-x-painting`：图像局部重绘，根据原始图片、涂抹区域和提示词在指定区域生成新内容。详见 [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)。

> **注意**：`wanx-x-painting` 模型当前仅提供免费体验，免费额度用完后不可调用且不支持付费，推荐使用千问图像编辑或万相 2.1 图像编辑替代。

### 可灵系列（Kling）

可灵图像生成模型支持文生图和参考图生图，仅华北2（北京）地域可用。详见 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

| 模型名称 | 能力 | 输出规格 |
|---------|------|---------|
| `kling/kling-v3-image-generation` | 文生图、单图参考图生图 | 1k/2k，1-9 张，PNG |
| `kling/kling-v3-omni-image-generation` | 文生图、多图输入、分镜组图 | 1k/2k/4k，单图 1-9 张或组图 2-9 张，PNG |

### Z-Image

Z-Image 是一款轻量级文生图模型，生成速度快，支持中英文字渲染，灵活适配多种分辨率与宽高比。详见 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。

| 模型名称 | 输出规格 |
|---------|---------|
| `z-image-turbo` | 总像素 512\*512 至 2048\*2048，固定 1 张，PNG |

## 创意工具类模型

百炼还提供一系列面向电商和创意设计场景的专项模型，详见 [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)、[图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md) 等。

| 模型 | 功能 | 计费状态 |
|------|------|---------|
| `wanx-style-repaint-v1` | 人像风格重绘，将人物照片转换为多种艺术风格 | 0.04 元/张 |
| `image-out-painting` | 图像画面扩展（扩图），支持按比例/宽高比/方向扩展 | 0.18 元/张 |
| `wanx-background-generation-v2` | 图像背景生成，为商品主体生成背景图 | 已商业化 |
| `image-erase-completion` | 图像擦除补全，移除图像中的人物/物体/文字等 | 仅免费体验 |
| `image-instance-segmentation` | 人物实例分割，像素级掩码输出 | 仅免费体验 |
| `wanx-poster-generation-v1` | 创意海报生成，自动生成海报背景和文字排版 | 仅免费体验 |
| `shoemodel-v1` | 鞋靴模特，AI 试穿生成 | 仅免费体验 |
| `wanx-virtualmodel` / `virtualmodel-v2` | 虚拟模特，替换商品图中的模特和背景 | 仅免费体验 |
| AI 试衣 OutfitAnyone | 试衣模型+辅助模型组合 | 部分付费 |
| FaceChain 人物写真 | 仅需 2 张照片训练人物形象，批量生成写真 | 已商业化 |
| WordArt 锦书 | 创意文字变形与文字纹理生成 | 已商业化 |

> **注意**：多个创意工具模型（鞋靴模特、虚拟模特、创意海报生成、人物实例分割、图像擦除补全）当前仅提供免费体验，免费额度用完后不可调用且不支持付费。推荐使用千问图像编辑或万相 2.1 图像编辑模型作为替代方案。

## 调用方式

图像 API 支持两种调用模式：

### 同步调用

千问系列（qwen-image-*）、万相 2.5/2.6/2.7 系列支持同步接口，一次请求即可获得结果，推荐大多数场景使用。

**请求地址（以千问/万相2.7为例）：**

- 北京：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- 新加坡：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**示例（万相2.7文生图）：**

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
    "model": "wan2.7-image-pro",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"text": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"}
                ]
            }
        ]
    },
    "parameters": {
        "size": "2K",
        "n": 1
    }
}'
```

### 异步调用

万相 V1/V2、可灵、以及创意工具类模型采用异步调用模式（需在 Header 中加 `X-DashScope-Async: enable`），流程为"创建任务 -> 轮询获取结果"。

**步骤一：提交任务**

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-t2i-turbo",
    "input": {
        "prompt": "一间有着精致窗户的花店"
    },
    "parameters": {
        "size": "1024*1024",
        "n": 1
    }
}'
```

**步骤二：查询结果**

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

响应中 `task_status` 为 `SUCCEEDED` 时，`results` 数组中包含生成图像的 URL。

## 关键参数

各模型的通用参数包括：

| 参数 | 说明 |
|------|------|
| `model` | 模型名称 |
| `prompt` / `messages` | 文本描述（同步接口使用 messages 格式，异步接口部分使用 [prompt](../guides/prompt.md) 字段） |
| `size` | 输出图像尺寸，不同模型支持的分辨率范围不同 |
| `n` | 生成图像数量 |
| `negative_prompt` | 反向提示词，指定不希望出现的内容（部分模型支持） |
| `ref_img` / `input.image` | 参考图像 URL（图像编辑和图生图场景） |

> **注意**：不同模型系列的请求地址和参数结构有差异。千问和万相 2.5+ 使用 `messages` 格式，万相 V1/V2 使用 `prompt` + `parameters` 格式，可灵使用 `messages` 格式但请求地址不同。请务必参考各模型的 API 文档。

## 计费与限流

- **免费额度**：开通百炼服务后自动发放，通常为 500 张，有效期 90 天。主账号与 RAM 子账号共享额度。免费额度仅计算成功生成的输出图片数量。
- **计费单价**：已商业化的模型按张计费（如 wanx-v1 为 0.16 元/张，wanx2.1-imageedit 为 0.14 元/张）。"限时免费"表示公测中，额度用尽后不可使用。
- **限流**：主账号与 RAM 子账号共享限流。典型限流为任务下发 QPS 2、同时处理任务数 1-5。

## 前提条件

1. [开通模型服务并获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
2. [配置 API Key 到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
3. 如需 SDK 调用，需 [安装 DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)

> **注意**：华北2（北京）和新加坡地域拥有独立的 API Key 与请求地址，不可混用，跨地域调用将导致鉴权失败或服务报错。

## 常见问题

- **图像无法下载**：输入图片 URL 必须支持公网访问，可上传至 OSS 等云存储服务。报错码为 `BadRequest.InputDownloadFailed`。
- **curl 命令执行失败**：Windows 环境下需将 `$DASHSCOPE_API_KEY` 替换为实际 API Key 值，或使用 Postman 等工具发送请求。
- **地域限制**：部分模型（如千问图像翻译、可灵、多数创意工具模型）仅在华北2（北京）地域可用。

更多常见问题请参考 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)


