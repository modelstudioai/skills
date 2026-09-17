# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但不同模型对参数、输入格式和输出规格有差异化要求。开发者需根据任务类型选择适配模型，并严格遵循各模型的约束条件。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：
- **千问（Qwen-VL / Qwen2-VL）**：支持多模态理解+生成，适用于图文混合提示的可控生成，详见 [图像生成](../../raw/model-api-reference/image-generation.md)；
- **万相（WanX）**：专注高保真中文语义理解，支持精细 [prompt](../guides/prompt.md) 解析与艺术风格控制；
- **Z-Image**：轻量级实时生成模型，适合低延迟场景，但不支持 negative_[prompt](../guides/prompt.md)，参见 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)；
- **可灵（Kling）**：支持长文本描述与复杂构图，具备强一致性控制能力；
- **Vidu**：虽以视频生成为主，但其图像生成子模块支持高质量静态帧输出，文档见 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)；
- **创意工具（Creative Tools）**：提供图像增强、扩图、线稿上色等后处理能力，非端到端生成模型。

> **注意**：[图像生成](../../raw/model-api-reference/image-generation.md) 中列出的“千问”链接实际指向旧版 Qwen-VL 文档，而新版本 Qwen2-VL 的尺寸限制与 seed 行为已变更，请以 [千问](../../raw/model-api-reference/image-generation/qwen-image-api-reference.md) 最新版为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"wanx-v1"`、`"kling-v1"`；必须与所选模型完全匹配 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；万相与可灵支持分段结构化提示（如 `"主体: 猫; 风格: 水彩"`） |
| `size` | string | 否 | 输出尺寸，支持 `"1024x1024"`、`"768x1024"`、`"1024x768"`；Z-Image 仅支持 `"1024x1024"`（见 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)） |
| `n` | integer | 否 | 生成图片数量，取值 1–4；Vidu 模型固定为 `n=1` |
| `seed` | integer | 否 | 随机种子，用于结果复现；部分模型（如 Z-Image）不支持该参数 |

## 使用方式

1. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/images/generations`  
2. 设置请求头：`Authorization: Bearer YOUR_API_KEY`，`Content-Type: application/json`  
3. 请求体示例（万相模型）：
```json
{
  "model": "wanx-v1",
  "prompt": "一只戴草帽的橘猫坐在窗台，阳光斜射，写实风格",
  "size": "1024x1024",
  "n": 2
}
```
4. 成功响应返回 `data` 数组，每项含 `url`（直链，有效期 1 小时）和 `created` 时间戳。

## 限制和注意事项

- 单次请求最大 `prompt` 长度为 512 字符，超长将被截断且不报错；
- 所有模型禁止生成含暴力、政治、成人内容的图像，违规请求将返回 `400 Bad Request` 并计入风控日志；
- 可灵（Kling）模型暂不支持 `image_url` 输入（即图生图），该能力仅在 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md) 中提供；
- 免费试用额度仅覆盖基础尺寸（1024×1024）生成，超分辨率或批量生成需开通付费套餐；
- 图像 URL 为临时直链，**不可长期缓存**，需在 1 小时内下载或转存。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


