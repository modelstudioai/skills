# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但不同模型对参数、输入格式和输出规格有差异化要求。开发者需根据任务类型选择适配模型，并严格遵循各模型的约束条件。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：
- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：支持多轮图文对话驱动的图像生成与编辑，适用于复杂语义理解场景；[原文标题](../../raw/model-api-reference/image-generation.md) 中明确将其列为首选多模态基础模型。
- **万相（WanX）**：专注高保真文生图，支持 1024×1024 及 1024×1792 分辨率输出，具备丰富艺术风格控制；其 API 行为与 [原文标题](../../raw/model-api-reference/image-generation.md) 所列一致。
- **Z-Image**：轻量级实时生成模型，响应延迟 <800ms（P95），适用于低延迟交互场景；文档 [原文标题](../../raw/model-api-reference/image-generation.md) 特别标注其不支持 `image_url` 输入。
- **可灵（Kling）**：支持长宽比自定义（如 4:3、16:9）、主体一致性保持及多步迭代优化，但仅接受 UTF-8 编码的纯文本 [prompt](../guides/prompt.md)。
- **Vidu**：虽以视频生成为主，但其图像生成接口可用于高质量单帧预览图生成，注意其 `size` 参数仅接受 `"1024x1024"` 字符串值（不可传数字数组）。
- **创意工具（Creative Tools）**：提供图生图、涂鸦转图、局部重绘等编辑能力，需配合 `image_url` 和 `mask_url` 使用；该模块能力在 [原文标题](../../raw/model-api-reference/image-generation.md) 的子页面中有详细说明。

> **注意**：`Vidu` 模型的 `size` 参数行为与 `万相` 不同——后者支持 `"1024x1024"` 和 `"1024x1792"`，而 `Vidu` 仅接受前者，且必须为字符串字面量。此差异已在 [原文标题](../../raw/model-api-reference/image-generation.md) 的 `vidu-image-models.md` 子页中确认，非文档笔误。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"wanx-v1"`, `"qwen2-vl-image"`, `"z-image-v1"`；必须与所选模型完全匹配 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；部分模型（如 Kling）不支持换行符 |
| `size` | string | 否 | 输出尺寸，格式为 `"WxH"`，如 `"1024x1024"`；Z-Image 仅支持 `"1024x1024"`，万相支持 `"1024x1024"` 和 `"1024x1792"` |
| `n` | integer | 否 | 生成图片数量，默认 1，最大 4（万相/千问）或 1（Z-Image） |
| `image_url` | string | 否（图生图必需） | Base64 或公网可访问 URL；Z-Image 明确不支持该字段 |
| `mask_url` | string | 否（局部重绘必需） | 仅创意工具支持，需为灰度掩码图（白色区域为重绘区） |

## 使用方式

1. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/images/generations`
2. Header 中设置 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`
3. Body 示例（万相文生图）：
```json
{
  "model": "wanx-v1",
  "prompt": "中国水墨风格的山水画，远山含黛，近水泛舟",
  "size": "1024x1024",
  "n": 2
}
```
4. 成功响应返回 `data` 数组，每项含 `url`（临时直链，有效期 1 小时）和 `revised_prompt`（模型优化后的提示词）

## 限制和注意事项

- 所有模型均禁止生成含暴力、色情、政治敏感或侵犯版权的内容，违规请求将被拦截并记录；
- 单次请求最大超时时间为 60 秒（Z-Image 为 15 秒），超时后服务端可能返回 `504 Gateway Timeout`；
- `image_url` 必须为公网可访问地址或合法 Base64（`data:image/png;base64,...`），内网地址或本地路径无效；
- `prompt` 中若含中文标点（如“，”、“。”），部分旧版 SDK 可能因编码问题截断，建议统一使用英文标点或显式指定 `charset=utf-8`；
- 创意工具模块的 `mask_url` 掩码图必须为单通道 8-bit PNG，黑色（0）表示保留区，白色（255）表示重绘区；其他灰度值将被二值化处理。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


