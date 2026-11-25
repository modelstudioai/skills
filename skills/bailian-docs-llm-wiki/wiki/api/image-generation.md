# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回结构化图像 URL 及元数据。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型：
- **千问（Qwen-VL / Qwen2-VL）**：支持多模态理解+生成，适用于图文混合提示场景；  
- **万相（WanXiang）**：专注高保真文生图，支持 1024×1024 及 1024×1536 等多种比例；  
- **Z-Image**：轻量级实时生成模型，适合低延迟需求的草图生成与快速迭代；  
- **可灵（Kling）**：支持长视频帧级一致性生成，亦提供单帧高质量图像输出；  
- **Vidu**：以视频生成为主，但其图像生成能力基于相同底层架构，适用于动态构图提示；  
- **创意工具（Creative Tools）**：提供图像增强、扩图、主体提取等后处理能力，常与前述模型组合使用。  
详细能力对比请参见 [图像生成](../../raw/model-api-reference/image-generation.md) 的模型索引页。

## 关键参数

通用必选参数包括 `model`（如 `"wanx-v1"`）、`input.prompt`（字符串，最大 1000 字符）；  
可选参数因模型而异：
- `size`：格式为 `"WIDTHxHEIGHT"`，常见值有 `"1024x1024"`、`"1024x1536"`；部分模型（如 Z-Image）仅支持固定尺寸，详见 [Z-Image](../../raw/image-generation/z-image-generation-api-reference.md) 文档；  
- `n`：生成图像数量（默认 1，最大 4）；  
- `seed`：整数，用于结果复现；  
- `image_url` 或 `image`：图生图场景下必需，Base64 编码或公网可访问 URL；  
> **注意**：`size` 参数在 [万相](../../raw/image-generation/wan-image-api-reference.md) 中支持 `"768x768"`，但在 [可灵](../../raw/image-generation/kling-image-api-reference.md) 中该尺寸已被弃用，仅保留 `"1024x1024"` 和 `"1280x720"`，调用前请确认目标模型文档。

## 使用方式

1. 发送 `POST /v1/images/generations` 请求；  
2. 请求体为 JSON，结构遵循 OpenAI 兼容格式（`model`, `prompt`, `size` 等字段）；  
3. 成功响应返回 `data[]` 数组，每项含 `url`（临时 CDN 链接，有效期 1 小时）和 `revised_prompt`（模型优化后的提示词）；  
4. 错误码参考标准 HTTP 状态码及 `code` 字段（如 `InvalidParameter`、`ModelNotSupported`）。  
完整请求示例与 SDK 调用方法见 [图像生成](../../raw/model-api-reference/image-generation.md)。

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 1000 字符，超长将被截断且不报错；  
- 所有图像 URL 有效期为 1 小时，需及时下载或转存；  
- 涉及人脸、商标、知名人物等敏感内容可能被自动过滤，返回 `content_filter` 错误；  
- 图生图任务中，若输入图分辨率低于 512×512，部分模型（如 Vidu）会拒绝请求，具体阈值请查阅 [Vidu](../../raw/image-generation/vidu-image-models.md) 文档；  
- 创意工具类接口（如扩图）必须与原始生成任务关联 `request_id`，否则返回 `InvalidOperation`。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


