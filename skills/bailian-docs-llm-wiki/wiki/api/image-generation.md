# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在输入约束、输出分辨率和计费粒度上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按发布顺序排列）：
- **Qwen-VL / Qwen2-VL 系列**：支持多模态理解+生成，适用于图文混合提示词场景，详见 [图像生成](../../raw/model-api-reference/image-generation.md)；
- **WanX（万相）**：专注高保真中文语义理解与艺术化渲染，支持负向提示词和多步采样控制；
- **Z-Image**：轻量级实时生成模型，适用于低延迟需求场景，但不支持图生图，详见 [图像生成](../../raw/model-api-reference/image-generation.md)；
- **Kling（可灵）**：支持长文本描述解析与复杂构图生成，对人物姿态、光影逻辑建模更强；
- **Vidu**：虽以视频生成为主，但其图像生成模式（`/v1/images/generations`）可作为静态帧高质量备选，参见 [图像生成](../../raw/model-api-reference/image-generation.md)；
- **创意工具（Creative Tools）**：提供图像增强、扩图、线稿上色等后处理能力，非端到端生成模型。

> **注意**：Vidu 文档中声明“图像生成模式仅限白名单用户开通”，而 [图像生成](../../raw/model-api-reference/image-generation.md) 主文档未提及该限制，实际调用前请确认账户权限。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx-v1`, `kling-v1`, `zimage-v1`；必须与所选模型严格匹配 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；万相与可灵支持分句加权（如 `(cat:1.3)`） |
| `size` | string | 否 | 输出尺寸，格式为 `WxH`，如 `1024x1024`；各模型支持范围不同（Z-Image 仅支持 `512x512` 和 `768x768`） |
| `n` | integer | 否 | 生成数量，默认 1，最大值因模型而异（万相上限为 4，可灵为 1） |
| `seed` | integer | 否 | 随机种子，用于结果复现；设为 `-1` 表示随机，部分模型（如 Z-Image）不支持该参数 |

## 使用方式

1. 发送 `POST` 请求至 `https://dashscope.aliyuncs.com/api/v1/images/generations`  
2. Header 中携带 `Authorization: Bearer YOUR_API_KEY` 和 `Content-Type: application/json`  
3. Body 示例（以万相为例）：
```json
{
  "model": "wanx-v1",
  "prompt": "水墨风格山水画，远山含黛，小舟泛波",
  "size": "1024x1024",
  "n": 1
}
```
4. 成功响应返回 `output.results[]`，每项含 `url`（有效期 1 小时）和 `base64` 字段（若请求头指定 `Accept: application/json+base64`）

## 限制和注意事项

- 所有模型均禁止生成含暴力、色情、政治敏感或可识别真实人脸的内容，违规请求将被拦截并计入失败配额；
- 单次请求 `prompt` 中不得包含 URL、文件路径或执行指令（如 “运行 Python”），否则触发安全过滤；
- Z-Image 模型不支持 `negative_prompt` 参数，而万相与可灵支持；若在 Z-Image 请求中传入该字段，将被静默忽略；
- 图像生成配额按「模型 × 分辨率 × 数量」独立计量，例如 `kling-v1` 生成 `1024x1024×2` 占用 2 个单位，而 `zimage-v1` 同尺寸仅占 1 单位；
- 对于需高精度控制的场景（如 UI 元素生成），建议优先使用 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md) 的 `inpainting` 或 `outpainting` 接口，而非通用文生图。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


