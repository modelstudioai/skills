# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入长度上的差异。

## 支持的模型与功能

当前支持以下图像生成模型：
- **千问（Qwen-VL / Qwen2-VL）**：侧重[多模态](../concepts/multi-modal.md)理解与图文协同生成，支持中文提示词优化；详见 [图像生成](../../raw/model-api-reference/image-generation.md)。
- **万相（WanX）**：专注高质量文生图，支持 1024×1024、1280×720 等多种分辨率及 `--style` 参数控制艺术风格；其详细参数说明见 [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)。
- **Z-Image**：轻量级实时生成模型，适用于低延迟场景，但仅支持固定尺寸（512×512）输出；参考 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)。
- **可灵（Kling）**：支持高保真图生图与主体一致性控制，需传入 `image_url` 或 `image_base64`；具体约束见 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md)。
- **Vidu**：虽以视频生成为主，但提供静态帧生成能力（`type=image`），不支持负向提示词；参见 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)。
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、扩展画布（outpainting）、色彩化等编辑能力，需配合 mask 图像使用；完整接口定义见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：Vidu 文档中声明“支持负向提示词”，但实测 v1.2.3 版本 API 忽略 `negative_prompt` 字段——该行为与 [图像生成](../../raw/model-api-reference/image-generation.md) 中的通用参数说明矛盾，建议以实际请求响应为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx-v1`, `kling-v2`, `zimage-v1` |
| `prompt` | string | 是 | 中文或英文提示词，最大长度 512 字符（万相为 1024） |
| `size` | string | 否 | 输出尺寸，格式 `WxH`，如 `1024x1024`；各模型支持范围不同，详见对应文档 |
| `n` | integer | 否 | 生成数量（1–4），默认为 1；Z-Image 固定为 1 |
| `seed` | integer | 否 | 随机种子，用于结果复现（部分模型如万相支持，Z-Image 不支持） |

## 使用方式

1. 发送 `POST /v1/images/generations` 请求；
2. 在 `Authorization` Header 中携带 `Bearer <api_key>`；
3. Body 为 JSON，结构示例：
```json
{
  "model": "wanx-v1",
  "prompt": "一只青花瓷风格的猫，水墨背景",
  "size": "1024x1024",
  "n": 1
}
```
4. 成功响应包含 `data: [{ "url": "...", "b64_json": "..." }]`；若启用 `response_format=base64`，则仅返回 `b64_json` 字段。

## 限制和注意事项

- 单次请求最大 `prompt` 长度依模型而异：万相支持 1024 字符，其余模型普遍为 512；超长将被截断且无警告。
- 所有模型均**不支持**直接上传本地图片文件，图生图类请求必须提供可公开访问的 `image_url` 或 Base64 编码字符串。
- 生成内容受平台内容安全策略约束，含暴力、成人、政治敏感等关键词将触发拦截并返回 `400 Bad Request`；具体规则见 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md)。
- 免费试用额度仅适用于 `wanx-v1` 和 `zimage-v1`；调用 `kling-v2` 或 `vidu-image` 需开通对应模型权限。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


