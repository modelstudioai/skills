# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、图像编辑等核心能力。开发者可通过标准 HTTP 请求调用，所有模型均需指定 `model` 参数并遵循对应参数规范。详细模型能力与行为差异请参考 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)。

## 支持的模型/功能

当前支持以下图像生成模型：
- **Qwen-VL / Qwen2-VL 系列**（文生图、[多模态](../concepts/multi-modal.md)理解+生成）  
- **WanX（万相）**：侧重艺术风格与高精度构图  
- **Z-Image**：强调写实细节与物理一致性  
- **Kling（可灵）**：支持长宽比自定义、高分辨率输出（最高 1024×1024）  
- **Vidu 图像模型**：专为视频帧生成优化，亦支持单图生成（注意：其图像生成能力与 Vidu 视频模型接口分离）  
- **创意工具（Creative Tools）**：提供局部重绘、涂鸦生成、背景替换等编辑类能力  

各模型具体输入格式、支持的 [prompt](../guides/prompt.md) 语法及风格控制方式存在差异，详见 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-vl-plus"`、`"wanx-v1"`、`"zimage-v1"`、`"kling-v1"`、`"vidu-image-v1"` 或 `"creative-tools-v1"` |
| `input.prompt` | string | 是 | 中文或英文提示词；部分模型（如 WanX）支持负向提示词，通过 `input.negative_prompt` 传入 |
| `parameters.size` | string | 否 | 输出尺寸，格式为 `"WxH"`，如 `"1024x1024"`；Kling 和 Z-Image 支持 `"768x1024"` 等非正方形尺寸，WanX 仅支持 `"1024x1024"` |
| `parameters.seed` | integer | 否 | 随机种子，用于结果复现；设为 `-1` 表示随机（默认） |
| `parameters.steps` | integer | 否 | 采样步数（仅部分模型支持，如 Z-Image 默认 30，最大 50） |

> **注意**：`parameters.guidance_scale` 在 WanX 和 Kling 中含义不同——WanX 中该值越高越贴近 [prompt](../guides/prompt.md)，而 Kling 中过高（>15）易导致过饱和失真。实际行为以 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md) 中最新说明为准。

## 使用方式

1. 发送 `POST` 请求至 `/v1/images/generations`  
2. Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. Body 示例（Kling 文生图）：
```json
{
  "model": "kling-v1",
  "input": {
    "prompt": "一只赛博朋克风格的机械猫蹲在东京涩谷十字路口，霓虹雨夜，8k细节",
    "negative_prompt": "文字、水印、模糊、畸变"
  },
  "parameters": {
    "size": "1024x1024",
    "seed": 42
  }
}
```
响应返回 `data[0].url`（直链 URL，有效期 24 小时）及 `data[0].base64`（可选，需在请求中显式设置 `response_format: "b64_json"`）。

## 限制和注意事项

- 单次请求最多生成 4 张图像（`n` 参数最大为 4），超出将报错 `400 Bad Request`  
- 输入 [prompt](../guides/prompt.md) 长度上限为 512 字符（含空格），超长截断不报错但可能影响效果  
- 所有模型均**不支持**直接上传图像作为输入源（图生图、局部重绘等功能需通过 `creative-tools-v1` 模型并传入 `input.image_url` 或 `input.image_base64`）  
- 免费试用额度仅适用于 `qwen-vl-plus` 和 `wanx-v1`；其他模型需开通对应服务并确认配额  
- Vidu 图像模型与 Vidu 视频模型使用独立计费单元，不可混用配额  

如遇生成内容异常（如结构崩坏、提示词忽略），建议优先检查 [prompt](../guides/prompt.md) 格式是否符合目标模型要求，并查阅 [常见问题 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md) 中的排障指南。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)



