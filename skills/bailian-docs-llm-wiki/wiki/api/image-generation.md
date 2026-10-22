# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按发布顺序排列）：
- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：支持多轮图文对话驱动的图像生成，适用于语义理解强的复杂提示词场景；详见 [图像生成](../../raw/model-api-reference/image-generation.md)。
- **万相（WanX）**：专注高保真中文提示词解析，支持 1024×1024 及 1024×1536 分辨率输出；其能力说明见 [图像生成](../../raw/model-api-reference/image-generation.md)。
- **Z-Image**：轻量级实时生成模型，适合低延迟需求，但仅支持 `1:1` 和 `4:3` 长宽比；参考 [图像生成](../../raw/model-api-reference/image-generation.md) 中的模型列表。
- **可灵（Kling）**：支持动态构图与精细结构控制，提供 `controlnet` 类型参数扩展；文档细节位于 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)。
- **Vidu**：虽以视频生成为主，但其静态帧生成能力可用于高质量单图输出，注意其 `image_generation` 模式需显式指定；参见 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)。
- **创意工具（Creative Tools）**：提供图像增强、扩图、去背景等后处理能力，不直接生成新图像，需配合主模型使用；接口定义见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：原始文档中将 Vidu 归类为“图像生成模型”，但其实际设计目标为视频生成，`image_generation` 模式属于降级兼容用法，生成质量与稳定性低于专用图像模型（如万相或 Z-Image），建议仅用于原型验证。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx-v1`, `kling-v2`, `zimage-pro`；必须与 [图像生成](../../raw/model-api-reference/image-generation.md) 中列出的模型名严格一致 |
| `prompt` | string | 是 | 中文提示词，长度 ≤ 500 字符；部分模型（如万相）支持负向提示词，通过 `negative_prompt` 字段传入 |
| `size` | string | 否 | 输出尺寸，格式为 `WxH`，如 `1024x1024`；各模型支持范围不同，请查阅对应子文档（如 [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)） |
| `n` | integer | 否 | 生成数量，默认为 1，最大值依模型而定（万相≤4，Z-Image≤1） |

## 使用方式

1. 发送 `POST /v1/images/generations` 请求；
2. 在请求体中指定 `model`、`prompt` 等必需参数；
3. 成功响应返回 `data: [{ "url": "...", "b64_json": "..." }]`，其中 `url` 有效期为 1 小时；
4. 如需图生图或局部重绘，须额外提供 `image`（Base64 或 URL）及 `mask`（可选），具体字段见各模型子文档，例如 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md) 明确要求 `image_url` 和 `mask_url`。

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 500 字符，超长将被截断且不报错；
- 所有模型均禁止生成含暴力、政治敏感、成人内容的图像，违规请求将返回 HTTP 400 并记录审计日志；
- `size` 参数必须为模型明确支持的组合（如万相不支持 `768x768`），否则返回 422 错误；
- Z-Image 模型暂不支持 `negative_prompt`，若传入该字段将被静默忽略；
- 创意工具类接口（如去背景）必须单独调用 `/v1/images/editing` 路径，不可与生成接口混用。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


