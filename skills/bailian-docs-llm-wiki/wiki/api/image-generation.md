# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型：  
- **Qwen-VL / Qwen2-VL 系列**（统称“千问”）：支持多轮图文理解+生成，适用于图文混合提示场景；详见 [图像生成](../../raw/model-api-reference/image-generation.md)。  
- **万相**：专注高保真艺术风格生成，支持 10+ 预设画风及自定义风格描述；其参数体系与千问不兼容，需单独配置；参见 [图像生成](../../raw/model-api-reference/image-generation.md)。  
- **Z-Image**：轻量级实时生成模型，适合低延迟需求，但仅支持固定分辨率（1024×1024）；详细能力边界见 [图像生成](../../raw/model-api-reference/image-generation.md)。  
- **可灵（Kling）**：支持长视频帧级一致性生成，亦可用于单图生成，但 [prompt](../guides/prompt.md) 中若含时间/动作描述将触发视频模式，需显式指定 `type=image`。  
- **Vidu**：本质为视频生成模型，其单帧输出能力受限，不推荐用于纯图像任务（> **注意**：[图像生成](../../raw/model-api-reference/image-generation.md) 中曾将 Vidu 列为“通用图像模型”，该描述已过时，实际应仅用于视频生成场景）。  
- **创意工具**：提供图像增强、扩图、主体提取等后处理能力，需配合主生成模型使用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-vl-plus`、`wanxiang-v1`、`z-image-1.0` 等，必须与所选模型严格匹配 |
| `prompt` | string | 是 | 中文或英文提示词，建议 ≤ 500 字符；万相对中文 [prompt](../guides/prompt.md) 效果更优，千问支持中英混写 |
| `size` | string | 否 | 格式为 `WxH`，如 `1024x1024`；各模型支持范围不同（Z-Image 仅支持 `1024x1024`，万相支持 `768x1152` 等竖版） |
| `n` | integer | 否 | 生成图片数量，默认 1，最大 4（部分模型如 Z-Image 限 1） |
| `seed` | integer | 否 | 控制随机性，相同 seed + [prompt](../guides/prompt.md) + model 下结果可复现 |

> **注意**：`style` 参数在万相中为字符串枚举（如 `"anime"`），而在千问中已被弃用，改由 prompt 描述风格——此差异已在 [图像生成](../../raw/model-api-reference/image-generation.md) 的最新版本中明确标注。

## 使用方式

1. 发送 POST 请求至 `/v1/images/generations`  
2. Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. Body 示例：
```json
{
  "model": "wanxiang-v1",
  "prompt": "水墨风格的黄山云海，远景，留白",
  "size": "1024x1024",
  "n": 1
}
```
4. 响应包含 `data` 数组，每项含 `url`（有效期 1 小时）和/或 `b64_json`

## 限制和注意事项

- 单次请求最大 `prompt` 长度：千问 500 字符，万相 300 字符，Z-Image 200 字符  
- 禁止生成含暴力、政治敏感、成人内容的图像；违规请求将被拦截并计入风控日志  
- 图像版权归属用户，但平台保留模型生成内容的必要使用权（详见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)）  
- 万相与 Z-Image 不支持 `image_url` 输入（即不支持图生图），如需该能力请选用千问或可灵  
- 所有模型均不支持负向提示词（`negative_prompt`），该字段会被忽略

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


