# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘等核心能力。所有模型均通过 `POST /v1/images/generations` 调用，采用标准 OpenAI 兼容格式，便于快速集成。模型能力与参数细节以各模型官方文档为准，[原文标题](../../raw/model-api-reference/image-generation.md) 列出了全部可用模型及其参考链接。

## 支持的模型/功能

当前支持以下图像生成模型（按发布顺序）：
- **千问（Qwen-VL/Qwen2-VL）**：侧重多模态理解与图文协同生成，支持中文提示词优化  
- **万相（WanX）**：面向设计场景，强于风格一致性与构图控制  
- **Z-Image**：轻量级实时生成模型，适合低延迟需求（如 UI 预览）  
- **可灵（Kling）**：支持高分辨率（最高 2048×2048）、长宽比灵活配置及多步编辑链  
- **Vidu**：虽以视频生成为主，但其图像生成模块支持帧级精细控制，适用于动画关键帧生成  
- **创意工具（Creative Tools）**：提供背景替换、主体增强、色彩迁移等后处理能力，需配合主生成模型使用  

> **注意**：Vidu 的图像生成能力在 [原文标题](../../raw/model-api-reference/image-generation.md) 中被列为独立条目，但实际调用需指定 `model=vidu-image` 且仅支持部分参数（如不支持 `image` 输入字段），详见 [原文标题](../../raw/model-api-reference/image-generation.md) 的“Vidu”子章节。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-vl-plus`, `wanx`, `z-image`, `kling`, `vidu-image`, `creative-tools` |
| `prompt` | string | 是 | 中文或英文提示词，建议≤500字符；千问系模型对中文提示更鲁棒 |
| `size` | string | 否 | 格式为 `WxH`，如 `1024x1024`；各模型支持范围不同（可灵支持 `768x768` 至 `2048x2048`，Z-Image 仅支持 `512x512`） |
| `n` | integer | 否 | 生成图片数量，默认 1，最大 4（可灵限 1，创意工具限 1） |
| `image` / `mask` | string (base64) | 否 | 图生图或局部重绘时必填；仅万相、可灵、创意工具支持，[原文标题](../../raw/model-api-reference/image-generation.md) 明确标注了兼容性 |

## 使用方式

1. 构造请求体（JSON）：
```json
{
  "model": "kling",
  "prompt": "中国水墨风格山水画，远山薄雾，留白处题诗",
  "size": "1024x1024",
  "n": 1
}
```
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/images/generations`，携带 `Authorization: Bearer <api_key>`  
3. 解析响应中 `data[0].url` 获取图片直链（有效期 1 小时）或 `data[0].b64_json` 获取 base64 编码  

## 限制和注意事项

- 所有模型单次请求最大 token 数为 4096（含 [prompt](../guides/prompt.md) + system [prompt](../guides/prompt.md)），超长提示将被截断  
- 可灵与 Vidu 模型不支持 `response_format=url` 以外的返回格式（即不支持 `b64_json`）  
- 创意工具必须与主生成模型分两步调用：先调用 `kling` 生成基础图，再以该图 URL 或 base64 作为 `image` 字段传入 `creative-tools`  
- 禁止生成含暴力、政治敏感、成人内容的图像，违规请求将被拦截并计入配额  
- Z-Image 模型无异步队列，超时阈值为 8 秒；其他模型默认超时 60 秒，可通过 `timeout` 参数覆盖（最大 120 秒）

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


