# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但不同模型对参数、输入格式和输出规格有差异化要求。开发者需根据任务类型选择适配模型，并严格遵循各模型的约束条件。

## 支持的模型与功能

当前支持以下图像生成模型（按发布顺序及能力定位）：

- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：侧重多模态理解引导的文生图，支持中文提示词优化；详见 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)  
- **万相（WanXiang）**：面向高精度可控生成，支持 ControlNet 类型控制（如边缘、深度、姿态），但需显式启用 `control_type` 参数；详见 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)  
- **Z-Image**：轻量级快速生成模型，响应延迟低于 3s（P95），适用于低敏感度批量任务；不支持图生图或尺寸大于 1024×1024 的输出。  
- **可灵（Kling）**：支持长宽比自适应（如 `16:9`, `4:3`, `1:1`）及高分辨率输出（最高 2048×2048），但仅接受英文 [prompt](../guides/prompt.md)；详见 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md)  
- **Vidu**：虽以视频生成为主，但其 `image_mode` 模式可作为静态图生成器使用，支持文本+参考图联合输入；注意该模式未在官方文档中明确标注为“图像生成”，需参考 Vidu 专项说明。  
- **创意工具（Creative Tools）**：提供局部重绘（inpainting）、扩图（outpainting）、风格迁移三类原子能力，需通过 `tool_type` 指定，不接受自由文本 [prompt](../guides/prompt.md)。

> **注意**：原始文档中将 Vidu 列为“图像生成”模型，但其实际主能力为视频生成，且 `image_mode` 的稳定性与图像专用模型存在差距；生产环境建议优先选用万相或可灵。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `wanx-v1`, `kling-v1`, `zimage-v1`；必须与所选模型严格匹配 |
| `prompt` | string | 是（除创意工具外） | 中文或英文提示词；千问支持中文，可灵仅支持英文，万相推荐中英混合（主体用中文，风格/质量词用英文） |
| `size` | string | 否 | 输出尺寸，格式为 `WxH`（如 `1024x1024`）；部分模型（如 Z-Image）仅支持固定尺寸列表 |
| `n` | integer | 否 | 生成图片数量，默认 1，最大值因模型而异（万相≤4，可灵≤2） |
| `seed` | integer | 否 | 随机种子，用于结果复现；设为 `-1` 表示随机，其他值需为 ≥0 的整数 |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头；
2. **端点**：`POST https://dashscope.aliyuncs.com/api/v1/images/generations`；
3. **请求体**（JSON）：
   ```json
   {
     "model": "wanx-v1",
     "prompt": "一只青花瓷风格的猫，水墨背景，高清细节",
     "size": "1024x1024",
     "n": 1,
     "seed": 42
   }
   ```
4. **响应解析**：成功时返回 `data[0].url`（直链 URL，有效期 1 小时），或 `data[0].b64_json`（Base64 编码图像）。

## 限制和注意事项

- 所有模型均禁止生成含暴力、色情、政治敏感、人脸可识别身份的内容；违反将触发实时拦截并记录审计日志。
- 单次请求最大 `prompt` 长度为 512 字符（可灵为 256 字符）；超长 [prompt](../guides/prompt.md) 将被截断，不报错。
- 万相模型若未指定 `control_type` 但传入 `image` 字段，将静默忽略参考图——此行为与 [图像生成 (raw/model-api-reference/image-generation.md)](../../raw/model-api-reference/image-generation.md) 中“图生图默认启用”的描述矛盾，实际以 API 运行时行为为准。
- 免费试用额度仅覆盖千问与 Z-Image；万相、可灵、Vidu 均需开通对应模型的付费包。
- 输出图像 URL 为临时直链，**不可长期缓存**；需在 1 小时内下载或转存至自有存储。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


