# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：

- **千问（Qwen-VL / Qwen2-VL 图像生成分支）**：支持中英文多轮图文理解+生成，适用于图文混合提示场景；[原文标题](../../raw/model-api-reference/image-generation.md)  
- **万相（WanX）**：专注高保真中文语义理解，对古风、国画、广告海报类提示词优化显著；[原文标题](../../raw/model-api-reference/image-generation.md)  
- **Z-Image**：轻量级实时生成模型，适合低延迟需求（如 UI 原型草图），仅支持 512×512 单一分辨率；[原文标题](../../raw/model-api-reference/image-generation.md)  
- **可灵（Kling）**：支持 1024×1024 及以上高分辨率输出，具备强构图控制能力，但不支持图生图；  
- **Vidu**：虽以视频生成为主，其静态帧生成能力可用于高质量单图输出，但需显式指定 `type=image`；  
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、涂鸦转图（scribble-to-image）、风格迁移等编辑类功能，需配合 mask 或 reference image 使用。

> **注意**：原始文档中将 Vidu 归类为“图像生成模型”，但 [原文标题](../../raw/model-api-reference/image-generation/vidu-image-models.md) 明确说明其图像生成能力为视频模型的副产物，稳定性与一致性低于专用图像模型，生产环境建议优先选用万相或可灵。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx-v1`, `kling-v2`, `zimage-v1`；详见各子文档 |
| `prompt` | string | 是 | 中文提示词（推荐），长度 ≤ 512 字符；部分模型（如 Z-Image）仅支持简体中文 |
| `size` | string | 否 | 格式为 `WxH`，如 `1024x1024`；默认值依模型而定（万相默认 `768x768`，可灵默认 `1024x1024`） |
| `n` | integer | 否 | 生成图片数量，取值 1–4；超过 1 时按 `quality=standard` 限制，不支持 `quality=hd` |
| `quality` | string | 否 | 可选 `standard`（默认）或 `hd`；仅万相与可灵支持 `hd`，Z-Image 不支持该参数 |

## 使用方式

1. **基础调用（文生图）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "wanx-v1",
           "prompt": "水墨风格的杭州西湖断桥",
           "size": "768x768"
         }'
   ```

2. **图生图（需 base64 图像）**：
   ```json
   {
     "model": "wanx-v1",
     "prompt": "转换为赛博朋克风格",
     "image_url": "data:image/png;base64,...",
     "task_type": "image-to-image"
   }
   ```

3. **局部重绘（需 mask）**：
   使用 `creative-tools` 模型，传入 `mask_url`（base64 或公网可访问 URL）及 `prompt`；详细字段见 [原文标题](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

## 限制和注意事项

- 单次请求最大 token 数（prompt + system context）不超过 2048；超长 prompt 将被截断，不报错；
- 所有模型禁止生成含人脸、真实人物肖像、暴力、政治敏感内容，违规请求将返回 `400 Bad Request` 并记录审计日志；
- Z-Image 模型不支持 `negative_prompt` 参数，且 `size` 固定为 `512x512`，传入其他值将被忽略；
- 可灵模型对长宽比敏感：仅支持 `1:1`、`4:3`、`3:4`、`16:9`、`9:16`，其余比例将自动裁剪适配；
- 免费试用额度仅覆盖 `standard` 质量生成；`hd` 模式及创意工具类操作按更高计费单元扣除。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


