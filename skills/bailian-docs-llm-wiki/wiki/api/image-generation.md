# image generation

百炼平台提供多种图像生成模型的统一 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过标准 RESTful 接口调用，返回 Base64 编码图像或可下载 URL。开发者需根据任务类型选择适配模型，并注意各模型在分辨率、长宽比和输入约束上的差异。

## 支持的模型与功能

当前支持以下图像生成模型（按发布顺序排列）：
- **Qwen-VL / Qwen2-VL 图像生成能力**：基于千问多模态系列，支持中英文提示词理解与高保真生成，详见 [图像生成](../../raw/model-api-reference/image-generation.md)；
- **万相（WanX）**：专注中国风与艺术化表达，支持水墨、工笔、赛博朋克等 20+ 预设风格，其参数体系与千问不兼容，需单独配置；
- **Z-Image**：轻量级实时生成模型，适用于低延迟场景（如 UI 实时预览），输出仅支持 `1024x1024` 固定尺寸，参见 [Z-Image](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md)；
- **可灵（Kling）**：支持 1024×1024 至 2048×2048 分辨率，具备强构图控制能力，但不支持 `image_url` 输入（即不支持图生图），该限制在 [可灵](../../raw/model-api-reference/image-generation/kling-image-api-reference.md) 文档中有明确说明；
- **Vidu 图像模型**：虽以视频生成为主，但其静态帧生成能力已开放，适用于关键帧生成任务，详见 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md)；
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、涂鸦生成（scribble-to-image）、草图增强等高级编辑能力，接口设计与基础生成模型分离，参考 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md)。

> **注意**：原始文档中将 Vidu 列为“图像模型”，但其实际为视频生成模型的静态帧导出能力；生产环境建议优先使用专用图像模型（如万相或 Z-Image）以保障稳定性与性能。

## 关键参数

通用必填参数：
- `model`: 模型标识符（如 `wanx-v1`, `kling-v1`, `zimage-v1`），必须与所选模型严格匹配；
- `input.prompt`: 中文或英文提示词，长度 ≤ 512 字符；部分模型（如万相）支持 `negative_prompt`；
- `parameters.size`: 格式为 `WxH`（如 `1024x1024`），不同模型支持范围不同（Z-Image 仅支持 `1024x1024`，可灵支持 `1024x1024`/`1216x832`/`832x1216`）；
- `parameters.n`: 生成图片数量（1–4），默认为 1。

模型特有参数：
- 万相支持 `style`（枚举值）、`quality`（`standard`/`hd`）；
- 创意工具类接口需额外传入 `input.image_url` 或 `input.mask_url`，且 `size` 必须与原图一致。

## 使用方式

1. 发送 `POST /v1/images/generations` 请求；
2. 请求体为 JSON，结构遵循 [图像生成](../../raw/model-api-reference/image-generation.md) 定义；
3. 响应包含 `output` 数组，每项含 `url`（有效期 1 小时）和/或 `b64_image` 字段；
4. 图生图或编辑类任务请改用 `/v1/images/edits` 路径，并确保请求体符合 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md) 规范。

## 限制和注意事项

- 单次请求最大 token 数（prompt + parameters）为 1024，超限将返回 `400 Bad Request`；
- 所有模型均禁止生成违法、暴力、成人内容，违规提示词将被拦截并返回 `403 Forbidden`；
- 可灵模型不支持 `image_url` 输入，若误传将返回 `422 Unprocessable Entity`（该行为与万相、创意工具形成明显差异）；
- Z-Image 模型响应时间通常 < 800ms，但并发数超过 50 时可能出现排队，建议业务层实现降级逻辑；
- 生成图像的版权归属用户，但平台保留反滥用审计权——相关条款详见 [图像生成](../../raw/model-api-reference/image-generation.md)。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


