# image generation

百炼平台提供丰富的图像生成与编辑 API，涵盖文生图、图像编辑、风格迁移、涂鸦作画、虚拟试衣等多种能力。这些 API 分布在千问（Qwen-Image）、万相（Wanx/Wan）、Z-Image、可灵（Kling）等多个模型系列中，均通过异步任务方式调用，支持 HTTP 和 SDK（Python/Java）两种接入方式。

## 主要模型系列

### 千问图像（Qwen-Image）

千问图像系列包含三类能力：

- **文生图**：`qwen-image-2.0-pro`（推荐）、`qwen-image-2.0`、`qwen-image-max` 等，擅长复杂文本渲染、多行布局和细粒度细节刻画。详见 [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)。
- **图像编辑**：`qwen-image-2.0-pro`、`qwen-image-edit-max`、`qwen-image-edit-plus` 等，支持多图输入/输出，可修改图内文字、增删物体、风格迁移、增强细节。详见 [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)。
- **图像翻译**：`qwen-mt-image` 模型可翻译图中文字并保留原排版，支持中/英文与其他语种互译（不支持非中英语种之间直译）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)。

### 万相（Wan/Wanx）

万相系列是百炼图像生成的核心模型族，版本跨度从 V1 到 2.7：

| 模型 | 能力 | 说明 |
|------|------|------|
| `wan2.7-image-pro` / `wan2.7-image` | 文生图、文生组图、图生组图、图像编辑、多图参考 | 最新版本，Pro 支持 4K 输出 |
| `wan2.6-image` | 图像编辑、图文混排输出 | — |
| `wan2.6-t2i`（推荐）/ `wan2.5-t2i` 等 | 文生图 | V2 版文生图，支持多种艺术风格与写实摄影 |
| `wan2.5-image-edit` | 单图编辑、多图融合 | 仅需文本指令即可完成主体一致编辑 |
| `wanx2.1-image-edit` | 风格化、内容编辑、扩图、超分、上色、线稿生图 | 通用图像编辑 |
| `wanx-v1` | 文生图（V1 版） | 建议迁移到 V2 |
| `wanx-sketch-to-image-lite` | 涂鸦作画 | 手绘图案 + 文字描述生成图像 |
| `wanx-x-painting` | 图像局部重绘 | 仅免费体验，推荐迁移到千问或万相 2.1 编辑 |

> **注意**：万相文生图 V1（`wanx-v1`）已被 V2 版全面升级，官方推荐使用 `wan2.6-t2i` 等新模型。多个早期模型（如 `wanx-x-painting`、虚拟模特、鞋靴模特等）仅提供免费体验额度，用完后不可调用且不支持付费。

### Z-Image

`z-image-turbo` 是一款轻量级文生图模型，生图速度快，支持中英文字渲染，总像素范围 512×512 到 2048×2048。适合对速度要求高的场景。详见 [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)。

### 可灵（Kling）

`kling/kling-v3-image-generation` 支持文生图和参考图生图（单图输入），仅在北京地域可用。详见 [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)。

## 创意工具类模型

百炼还提供一系列面向特定场景的图像创意工具 API：

| 模型 | 功能 | 状态 |
|------|------|------|
| 人像风格重绘 | 将人物照片转换为多种预设/自定义艺术风格 | 可用 |
| 图像画面扩展 | 按宽高比/比例/方向扩图，支持结合旋转角度 | 可用 |
| AI 试衣 OutfitAnyone | 虚拟试衣，包含基础版、Plus 版、图片精修、图片分割 | 可用（北京地域） |
| 创意海报生成 | 自动生成海报背景和文字排版 | 仅免费体验 |
| 图像背景生成 | 替换/生成图像背景 | 可用（北京地域） |
| 人物实例分割 | 像素级人物检测与分割 | 仅免费体验 |
| 图像擦除补全 | 移除图像中的人物/物体/文字/水印 | 仅免费体验，推荐迁移 |
| 虚拟模特 | 替换商品图中的模特和背景 | 仅免费体验，推荐迁移 |
| 鞋靴模特 | 鞋靴 AI 试穿 | 仅免费体验 |
| 人物写真 FaceChain | 2 张照片训练人物形象，批量生成风格写真 | 可用（北京地域） |
| 创意文字 WordArt 锦书 | 文字变形、文字纹理生成 | 可用（北京地域） |

## 通用调用方式

所有图像生成 API 均采用**异步调用**模式，流程分两步：

1. **创建任务**：发送 POST 请求，请求头必须包含 `X-DashScope-Async: enable`，返回 `task_id`。
2. **轮询结果**：使用 `task_id` 调用查询接口获取任务状态和结果图像 URL。`task_id` 有效期 24 小时，请勿重复创建任务。

**请求地址**（以千问图像编辑为例）：
- 北京地域：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- 新加坡地域：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

> **注意**：不同模型的请求路径可能不同。例如万相文生图 V1/V2 使用 `/services/aigc/text2image/image-synthesis`，图像翻译使用 `/services/aigc/image2image/image-synthesis`。请以各模型的 API 文档为准。

**认证方式**：请求头 `Authorization: Bearer $DASHSCOPE_API_KEY`。

**示例（文生图 curl）**：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wanx2.1-t2i-turbo",
    "input": {
        "prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵"
    },
    "parameters": {
        "size": "1024*1024",
        "n": 1
    }
}'
```

## 关键参数

各模型的参数细节不同，但以下参数在多个模型中通用：

- **model**（必选）：模型名称，如 `qwen-image-2.0-pro`、`wan2.6-t2i`。
- **[prompt](../guides/prompt.md)**（必选）：文本描述，支持中英文，通常限制在 800 字符以内（千问系列支持更长）。
- **size**：输出图像尺寸，格式为 `宽*高`，如 `1024*1024`。不同模型对分辨率范围和宽高比有不同限制。
- **n**：生成图片数量，通常 1-4 张。
- **negative_[prompt](../guides/prompt.md)**：反向提示词，描述不希望出现的元素。
- **seed**：随机种子，固定后可复现结果。

## 地域与限制

- 大多数模型在**华北2（北京）**地域可用，部分模型（如千问文生图、万相文生图 V2、Z-Image）同时支持**新加坡**和**弗吉尼亚**地域。
- 北京和新加坡地域拥有独立的 API Key 与请求地址，**不可混用**，跨地域调用将导致鉴权失败。
- 各模型均有独立的 QPS 限制（通常 2 QPS）和并发任务数限制（通常 1-2 个），主账号与 RAM 子账号共享限流配额。
- 新用户可获得免费额度（通常 500 张），有效期 90 天，详见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 前提条件

调用任意图像 API 前需要完成：

1. 开通阿里云百炼大模型服务。
2. 获取 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`。
3. 如使用 SDK，需安装 [DashScope SDK](../concepts/dashscope-sdk.md)（支持 Python 和 Java）。

## 来源文档

- [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)
- [千问-图像编辑API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-edit-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-mt-image-api.md)
- [千问-文生图API参考](../../raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-api.md)
- [万相-文生图V1版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-api-reference.md)
- [万相-文生图V2版API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/text-to-image-v2-api-reference.md)
- [万相-图像生成与编辑2.6 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-api-reference.md)
- [万相-图像生成与编辑2.7 API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan-image-generation-and-editing-api-reference.md)
- [万相-通用图像编辑2.5](../../raw/model-api-reference/image-generation/wan-image-api-reference/wan2-5-image-edit-api-reference.md)
- [万相-通用图像编辑API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-image-edit-api-reference.md)
- [万相-涂鸦作画API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/wanx-sketch-to-image-api-reference.md)
- [Z-Image API参考](../../raw/model-api-reference/image-generation/z-image-generation-api-reference/z-image-api-reference.md)
- [万相-图像局部重绘API参考](../../raw/model-api-reference/image-generation/wan-image-api-reference/vary-region-api-reference.md)
- [可灵-图像生成API参考](../../raw/model-api-reference/image-generation/kling-image-api-reference/kling-image-generation-api-reference.md)
- [人像风格重绘API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/portrait-style-redraw-api-reference.md)
- [图像画面扩展API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-scaling-api.md)
- [虚拟模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/virtual-model-api-details.md)
- [鞋靴模特API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/shoe-model-api.md)
- [创意海报生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/creative-poster-generation-api.md)
- [人物实例分割API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-instance-segmentation-api-reference.md)
- [图像擦除补全API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/image-erase-completion-api-reference.md)
- [AI试衣OutfitAnyone](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/outfitanyone.md)
- [图像背景生成API参考](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wanx-background-generation-api-reference.md)
- [人物写真生成FaceChain](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/facechain-portrait-generation.md)
- [创意文字WordArt锦书](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference/wordart-quick-start.md)




