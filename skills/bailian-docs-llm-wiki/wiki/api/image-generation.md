# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：

- **千问（Qwen-VL / Qwen2-VL 图像生成分支）**：支持中英文多轮图文理解+生成，适用于图文混合提示场景；[原文标题](../../raw/model-api-reference/image-generation.md)  
- **万相（WanX）**：专注高保真中文语义理解，对古风、国画、广告海报类提示词优化显著；[原文标题](../../raw/model-api-reference/image-generation.md)  
- **Z-Image**：轻量级实时生成模型，适合低延迟需求（如 UI 原型草图），仅支持 512×512 单一分辨率；[原文标题](../../raw/model-api-reference/image-generation.md)  
- **可灵（Kling）**：支持 1024×1024 及以上高分辨率输出，具备强构图控制能力，但不支持图生图；  
- **Vidu**：虽以视频生成为主，其静态帧生成能力可用于高质量单图输出，但需显式指定 `type=image`；  
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、涂鸦转图（scribble-to-image）、风格迁移等编辑类功能，需配合 mask 或 reference image 使用。

> **注意**：原始文档中将 Vidu 归类为“图像生成模型”，但 [原文标题](../../raw/model-api-reference/image-generation/vidu-image-models.md) 明确说明其图像生成能力为视频模型的副产物，稳定性与一致性低于专用图像模型，生产环境建议优先选用万相或可灵。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx-v1`, `kling-v2`, `zimage-v1`；详见各子文档 |
| `prompt` | string | 是 | 中文提示词（推荐），最长 512 字符；部分模型（如 Z-Image）仅支持简体中文 |
| `size` | string | 否 | 格式为 `WxH`，如 `1024x1024`；默认值因模型而异（万相默认 `768x768`，可灵默认 `1024x1024`） |
| `n` | integer | 否 | 生成图片数量，取值 1–4；超过 1 时按质量降序返回 |
| `seed` | integer | 否 | 随机种子，用于结果复现；设为 `-1` 表示随机 |
| `image_url` / `image` | string / base64 | 否 | 图生图或局部重绘时必需；`image_url` 优先级高于 `image` |

## 使用方式

1. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation`  
2. Header 中携带 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`  
3. Body 示例（万相文生图）：
```json
{
  "model": "wanx-v1",
  "prompt": "水墨风格的杭州西湖断桥，春日垂柳，远处雷峰塔",
  "size": "768x768",
  "n": 1,
  "seed": 42
}
```
4. 成功响应包含 `output.results[]`，每个元素含 `url`（有效期 1 小时）和 `base64` 字段。

## 限制和注意事项

- 单次请求最大 token 数：提示词 + 系统指令 ≤ 1024 tokens（超限将截断，不报错）；  
- 输出图像尺寸上限：万相/千问 ≤ 1024×1024，可灵 ≤ 2048×2048，Z-Image 严格限定为 512×512；  
- 所有模型禁止生成含暴力、政治敏感、成人内容的图像，违规提示词将被静默过滤并返回空结果；  
- 图生图任务中，若 `image_url` 返回 404 或格式不支持（非 JPEG/PNG），API 将返回 `INVALID_IMAGE_URL` 错误；  
- 创意工具类功能（如局部重绘）必须传入 `mask` 参数（Base64 编码的单通道灰度图），否则视为普通文生图请求。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


