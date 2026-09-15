# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但不同模型对参数、输入格式和输出规格有差异化要求。开发者需根据任务类型选择适配模型，并严格遵循各模型的约束条件。

## 支持的模型与功能

当前支持以下图像生成模型（按能力演进顺序排列）：
- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：支持中英文多模态提示词理解，适用于通用文生图与图文问答增强生成；[原文标题](../../raw/model-api-reference/image-generation.md) 中明确列出其为首批上线模型。
- **万相（WanX）**：专注高保真艺术风格生成，支持 `style_preset` 参数指定水墨、赛博朋克等 12 种预设风格；其能力细节见 [原文标题](../../raw/model-api-reference/image-generation/wan-image-api-reference.md)。
- **Z-Image**：面向电商与设计场景，支持精确尺寸控制（如 `1024x1536`）、透明背景（`alpha=true`）及批量生成；[原文标题](../../raw/model-api-reference/image-generation/z-image-generation-api-reference.md) 强调其对 PNG 输出与 alpha 通道的原生支持。
- **可灵（Kling）**：主打高动态范围与复杂构图，支持 `negative_prompt` 和 `controlnet` 类型参数（需额外开通权限）；注意其 `size` 参数仅接受 `1024x1024` 或 `768x1344` 两种固定值，与 Z-Image 的灵活尺寸形成差异。
- **Vidu**：虽以视频生成为主，但其图像生成接口（`/v1/images/generations?model=vidu-image`）可用于高质量单帧初始化，详见 [原文标题](../../raw/model-api-reference/image-generation/vidu-image-models.md)。

> **注意**：原始文档中“创意工具”模块描述其支持“一键抠图+换背景”，但该功能实际已整合至万相模型的 `tool=remove_bg` 子能力中；独立调用 `/v1/images/tools` 接口将返回 `404`，请以 [原文标题](../../raw/model-api-reference/image-generation.md) 的最新目录结构为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-vl-plus`, `wanx`, `zimage`, `kling`, `vidu-image` |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 512 字符；万相与可灵支持分段提示（用 `::` 分隔主体/风格/质量） |
| `size` | string | 否 | 格式为 `WxH`，默认 `1024x1024`；Z-Image 支持任意比例（如 `1280x720`），而可灵仅支持 `1024x1024` 或 `768x1344` |
| `n` | integer | 否 | 生成图片数量，取值 1–4；超过 4 将被截断并返回警告 |
| `quality` | string | 否 | 取值 `standard`（默认）或 `hd`；`hd` 模式在万相与 Z-Image 上生效，千问不支持该参数 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头；
2. **请求体**（JSON）：
   ```json
   {
     "model": "wanx",
     "prompt": "一只青花瓷猫，工笔画风格，高清细节",
     "size": "1024x1024",
     "quality": "hd"
   }
   ```
3. **响应**：返回 `data` 数组，每项含 `url`（直链，有效期 1 小时）和 `b64_json`（Base64 编码图像，可选）；
4. **错误处理**：`400` 表示参数校验失败（如 `size` 格式错误），`403` 表示模型未开通权限，`429` 表示超出速率限制（默认 10 QPS/项目）。

## 限制和注意事项

- 所有模型均禁止生成含暴力、色情、政治敏感或可识别真人肖像的内容，违规请求将触发实时拦截并记录审计日志；
- 单次请求最大 `prompt` 长度为 512 字符，超长部分会被静默截断（非报错）；
- Z-Image 的 `alpha=true` 参数仅在 `format=png` 时生效，JPEG 格式下自动忽略；
- 可灵模型暂不支持 `response_format=b64_json`，强制设置将返回 `400` 错误；
- 生成结果的版权归属用户，但平台保留基于安全合规目的的审核权；详细条款参见 [原文标题](../../raw/model-api-reference/image-generation/image-faq.md)。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


