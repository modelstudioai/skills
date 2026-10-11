# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按发布成熟度排序）：
- **Qwen-VL / Qwen2-VL 图像生成能力**：基于千问多模态系列，支持中英文提示词理解与高保真细节生成，适用于通用文生图场景；详见 [图像生成](../../raw/model-api-reference/image-generation.md)。
- **万相（WanX）**：专注中国风与艺术化表达，支持水墨、工笔、赛博国风等 10+ 预设风格，但不支持图生图；参考 [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)。
- **Z-Image**：轻量级实时生成模型，响应快（平均 <1.5s），仅支持 1024×1024 单一分辨率，适合 UI 原型草图生成；见 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)。
- **可灵（Kling）与 Vidu**：二者均支持视频生成，但其图像生成接口为视频首帧抽帧服务，**不推荐用于纯静态图任务**；该限制在 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md) 和 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md) 文档中均有明确说明。
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、涂鸦生成（scribble-to-image）、尺寸扩展（outpainting）等高级编辑能力，需配合 mask 或 control image 使用；参见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：原始文档中将 Vidu 列为“图像生成模型”，但实际其 `/v1/images/generations` 接口返回的是视频首帧，且无独立图像优化逻辑。该归类易引发误用，建议仅在需与视频流程对齐时调用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-vl-plus`, `wanx`, `z-image` 等，必须与所选模型严格匹配 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；万相对中文提示词效果更优 |
| `size` | string | 否 | 格式为 `WxH`，如 `1024x1024`；Z-Image 仅支持 `1024x1024`，万相支持 `1024x1024`/`1792x1024`/`1024x1792` |
| `n` | integer | 否 | 生成图像数量，默认 1，最大 4（Z-Image 限 1） |
| `seed` | integer | 否 | 控制生成确定性，范围 0–4294967295；部分模型（如万相）对 seed 敏感度较低 |

## 使用方式

1. 发送 `POST /v1/images/generations` 请求；
2. 在 `Authorization` header 中携带 `Bearer <api_key>`；
3. Body 为 JSON，结构示例如下：
```json
{
  "model": "wanx",
  "prompt": "敦煌飞天，飘带飞扬，金色背景，高清写实",
  "size": "1024x1024",
  "n": 1
}
```
4. 成功响应返回 `data: [{ "url": "https://...", "b64_json": "..." }]`；若需直接处理图像，优先使用 `b64_json` 字段解码。

## 限制和注意事项

- 所有模型单次请求 `prompt` 长度上限为 512 Unicode 字符，超长将被截断且**不报错**；
- 万相与 Z-Image 不支持 negative [prompt](../guides/prompt.md)；Qwen-VL 系列支持 `negative_prompt` 字段（需显式传入）；
- 图生图、inpainting 等编辑类任务**必须使用创意工具模型**（`creative-tools`），其他模型不支持 `image` 或 `mask` 参数；
- 调用 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md) 时，`image` 必须为 Base64 编码 PNG/JPEG，且尺寸需与 `size` 匹配，否则返回 `400 Bad Request`；
- 免费试用额度仅覆盖 Qwen-VL 和万相；Z-Image、可灵、Vidu 及创意工具需单独开通配额。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


