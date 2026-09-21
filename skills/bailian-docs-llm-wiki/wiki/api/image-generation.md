# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但参数兼容性与功能边界因模型而异。开发者需根据任务类型选择适配模型，并严格遵循各模型的输入约束。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：
- **千问（Qwen-VL / Qwen2-VL 图像生成分支）**：支持中英文多模态提示词理解，适用于通用文生图与图文混合推理任务；[原文标题](../../raw/model-api-reference/image-generation.md) 中明确将其列为首选基础模型。
- **万相（WanX）**：专注高保真艺术风格生成，支持 `style_preset` 参数控制油画、水墨、赛博朋克等 12 种预设风格；其能力细节见 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)。
- **Z-Image**：面向电商与设计场景，支持精确尺寸控制（如 `1024x1536`）、透明背景（`alpha_channel: true`）及批量生成；[原文标题](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md) 强调其对 `size` 和 `quality` 参数的强约束。
- **可灵（Kling）**：支持图生图与局部重绘（inpainting），需传入 `image` 和 `mask` 字段；注意其不支持 `n > 1` 的多图生成（详见 [原文标题](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)）。
- **Vidu**：虽以视频生成为主，但其 `image_mode` 模式可输出单帧高质量图像，适用于需要与视频工作流对齐的场景。

> **注意**：原始文档中将 Vidu 列为图像生成模型之一，但 [原文标题](../../raw/model-api-reference/image-generation/vidu-image-models.md) 明确说明其图像模式为实验性功能，输出稳定性低于专用图像模型，生产环境建议优先选用万相或 Z-Image。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"wanx-v1"`、`"zimage-v2"`；必须与所选模型完全匹配 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；万相模型对中文提示词优化更佳 |
| `size` | string | 否 | 格式为 `"WxH"`，如 `"1024x1024"`；Z-Image 仅支持 `["1024x1024", "1024x1536", "1536x1024"]`，其他模型默认 `"1024x1024"` |
| `n` | integer | 否 | 生成图片数量，默认 `1`；可灵（Kling）强制限制为 `1` |
| `style_preset` | string | 否 | 仅万相支持，取值见其文档；其他模型传入将被忽略 |

## 使用方式

1. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/images/generations`  
2. Header 中设置 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`  
3. Body 示例（万相生成中国山水画）：
```json
{
  "model": "wanx-v1",
  "prompt": "水墨风格，黄山云海，松石相映，留白意境",
  "size": "1024x1024",
  "style_preset": "ink_wash"
}
```
4. 响应中 `output.images[0].url` 为可直接访问的 CDN 图片地址（有效期 24 小时）

## 限制和注意事项

- 所有模型均禁止生成含暴力、色情、政治敏感或可识别人脸的内容；违规请求将返回 `400` 错误并记录审计日志。
- 单次请求最大 `prompt` 长度为 512 字符，超长截断不报错，可能导致语义失真。
- Z-Image 模型要求 `size` 必须显式指定且仅限预设值，否则返回 `422`；而千问模型允许省略 `size`，自动降级为默认尺寸。
- 图像生成任务不支持流式响应（`stream: true`），响应体为完整 JSON 结构。
- 生成图片分辨率上限为 `2048x2048`（万相与 Z-Image 支持），超出将被裁剪或拒绝；Vidu 图像模式上限为 `1024x1024`。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


