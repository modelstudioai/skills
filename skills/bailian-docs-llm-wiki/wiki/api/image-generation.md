# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但不同模型在参数支持、输出质量与适用场景上存在差异。开发者需根据任务需求选择合适模型，并严格遵循各模型的输入约束与计费规则。

## 支持的模型与功能

当前支持以下图像生成模型（按发布顺序排列）：
- **Qwen-VL / Qwen2-VL 图像生成能力**：基于千问多模态系列，支持中英文提示词理解与基础文生图；详见 [图像生成](../../raw/model-api-reference/image-generation.md)。
- **万相（WanX）**：专注高保真中文语义理解与艺术风格生成，支持 `style` 参数控制画风（如“水墨”“赛博朋克”），但不支持图生图；参考 [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)。
- **Z-Image**：轻量级实时生成模型，适用于低延迟场景（如 UI 预览），仅支持 1024×1024 单尺寸输出；其参数集与万相不兼容，详见 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)。
- **可灵（Kling）**：支持文生图与图生图双模式，且提供 `strength` 参数控制原图保留程度；注意其 `size` 参数必须为 `"1024x1024"` 或 `"768x768"`，其他值将被拒绝；该限制在 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md) 中明确说明。
- **Vidu**：虽以视频生成为主，但其图像生成接口（`/v1/images/generations` with `model=vidu-image`）可用于高质量单帧输出，支持 `negative_prompt`；参见 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)。
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、扩展画布（outpainting）等高级编辑能力，需配合 `mask` 和 `image` 字段使用；详细字段定义见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：原始文档中 [图像生成](../../raw/model-api-reference/image-generation.md) 的导航列表未包含已下线的 `Tongyi-Illustration` 模型，该模型自 2024-06 起停止维护，请勿在新项目中引用。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"wanx"`, `"kling"`, `"zimage"`；必须与所选模型完全匹配，大小写敏感 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；万相对中文提示优化更好，Z-Image 对英文更稳定 |
| `size` | string | 否 | 输出尺寸，格式为 `"WxH"`；支持值因模型而异（如 `kling` 仅支持 `"1024x1024"`，`wanx` 支持 `"1024x1024"`/`"768x768"`/`"512x512"`） |
| `n` | integer | 否 | 生成图片数量，默认 1，最大 4（`zimage` 最大为 1） |
| `seed` | integer | 否 | 随机种子，用于结果复现；部分模型（如 `kling`）要求 seed ∈ [0, 2¹⁶) |
| `image` / `mask` | string (base64) | 条件必填 | 图生图或局部重绘时必需；`image` 为 base64 编码的 PNG/JPEG，`mask` 为同尺寸二值掩码图 |

## 使用方式

1. **构造请求体**：确保 `model` 与目标模型一致，`prompt` 无非法字符（如控制字符、超长 emoji）；
2. **设置 HTTP 头**：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；
3. **发送 POST 请求**至 `https://dashscope.aliyuncs.com/api/v1/images/generations`；
4. **解析响应**：成功时返回 `data` 数组，每项含 `url`（临时直链，有效期 1 小时）和 `revised_prompt`（模型修正后的提示词）。

示例（万相文生图）：
```json
{
  "model": "wanx",
  "prompt": "一只青花瓷风格的猫，背景为江南园林",
  "size": "1024x1024",
  "n": 1
}
```

## 限制和注意事项

- 所有模型均**不支持**直接上传文件 URL，`image` 和 `mask` 字段必须为 base64 编码字符串（PNG/JPEG 格式，≤ 10 MB）；
- `prompt` 中禁止包含违法、暴力、成人内容，违者触发实时拦截并计入违规调用次数；
- `kling` 模型的 `strength` 参数范围为 `[0.1, 1.0]`，但 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md) 文档中示例误标为 `[0, 1]`，实际小于 0.1 将被截断为 0.1；
- `zimage` 不支持 `negative_prompt` 和 `style` 参数，若传入将被静默忽略——此行为与 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md) 文档描述一致；
- 计费按**成功生成的图片张数**计算（`n` 值），失败请求（如参数错误、鉴权失败）不计费；
- 临时图片 URL 由 OSS 提供，不可长期缓存；如需持久化，请自行下载并存储。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


