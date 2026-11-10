# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：
- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：支持多轮图文理解+生成，适用于图文混合提示场景；[原文标题](../../raw/model-api-reference/image-generation.md)
- **万相（WanX）**：专注高保真中文语义理解，支持精细控制（如服饰、光照、构图关键词），但不支持图生图；[原文标题](../../raw/model-api-reference/image-generation.md)
- **Z-Image**：轻量级实时生成模型，适合低延迟需求，仅支持 1024×1024 单一分辨率；[原文标题](../../raw/model-api-reference/image-generation.md)
- **可灵（Kling）**：支持 1080p 高清输出及动态构图提示（如“镜头缓慢推进”），但需显式指定 `aspect_ratio: "16:9"`；
- **Vidu**：虽以视频生成为主，其图像生成接口可作为高质量静态帧生成备选（`type: "image"`），但响应时间显著高于专用图像模型；
- **创意工具（Creative Tools）**：提供图像增强、背景移除、主体抠图等后处理能力，需配合主生成模型链式调用。

> **注意**：原始文档中将 Vidu 归类为图像生成模型，但 [原文标题](../../raw/model-api-reference/image-generation.md) 明确说明其图像模式为“实验性功能，不承诺 SLA”，生产环境应优先选用万相或千问。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"wanx-v1"`, `"qwen2-vl-image"`, `"z-image-v1"` |
| `prompt` | string | 是 | 中文提示词，建议 ≤ 500 字符；避免模糊表述（如“好看”“高级感”） |
| `size` | string | 否 | 输出尺寸，格式为 `"WxH"`，如 `"1024x1024"`；不同模型支持范围不同（见各子文档） |
| `n` | integer | 否 | 生成数量，默认 1，最大 4（万相/千问）或 1（Z-Image） |
| `seed` | integer | 否 | 随机种子，用于结果复现；设为 `-1` 表示随机 |

## 使用方式

1. 构造 POST 请求至 `/v1/images/generations`  
2. 在 `Authorization` Header 中携带 Bearer [Token](../concepts/token.md)  
3. Body 示例（JSON）：
```json
{
  "model": "wanx-v1",
  "prompt": "一只戴墨镜的橘猫坐在太空舱内，赛博朋克风格",
  "size": "1024x1024",
  "n": 1
}
```
4. 响应包含 `data` 数组，每项含 `url`（有效期 1 小时）和 `b64_json`（Base64 图像数据）

## 限制和注意事项

- 所有模型均禁止生成含暴力、政治敏感、成人内容的图像，违规请求将被拦截并记录日志；
- 千问模型对多模态 prompt（如“参考图中红墙颜色”）支持有限，实际效果弱于万相；建议复杂视觉控制优先使用万相；
- Z-Image 不支持 `size` 参数自定义，强制固定为 `1024x1024`，传入其他值将被忽略；
- 可灵模型要求 `prompt` 中必须包含明确的空间/动作描述（如“站立”“侧身”“仰视”），否则生成质量下降明显；
- 创意工具类接口（如背景移除）需先调用主生成接口获取图像 URL，再作为 `input_url` 提交至 `/v1/images/creative-tools/remove-background`。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


