# image generation

百炼平台提供多种图像生成模型的 API 接口，支持文生图、图生图、局部重绘、风格迁移等核心能力。所有模型均通过统一的 `/v1/images/generations` 端点调用，但不同模型在参数支持、输出质量与适用场景上存在差异。开发者需根据任务需求选择合适模型，并严格遵守各模型的输入约束与计费规则。

## 支持的模型/功能

当前支持以下图像生成模型（按发布顺序排列）：  
- **千问（Qwen-VL / Qwen2-VL 图像生成版）**：支持中英文多模态提示词理解，适用于通用文生图与图文理解增强生成；  
- **万相（WanXiang）**：专注高保真艺术风格生成，支持 `style_preset` 参数指定 12 种预设风格；  
- **Z-Image**：轻量级实时生成模型，响应延迟低于 800ms，适合低延迟交互场景；  
- **可灵（Kling）**：支持长文本描述解析与复杂构图控制，对人物姿态、光影逻辑建模更强；  
- **Vidu**：虽以视频生成为主，但其图像生成子模块支持帧级静态图输出，适用于视频前导图生成；  
- **创意工具（Creative Tools）**：提供 `inpainting`、`outpainting`、`sketch_to_image` 等结构化编辑能力，需配合 mask 或草图输入。  

详细能力对比请参阅 [图像生成](../../raw/model-api-reference/image-generation.md) 文档中的模型列表说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-vl-plus"`、`"wanx-2.1"`、`"kling-1.0"`；必须与 [图像生成](../../raw/model-api-reference/image-generation.md) 中列出的模型名完全一致 |
| `prompt` | string | 是 | 中文或英文提示词，长度 ≤ 1000 字符；部分模型（如 Z-Image）对 emoji 和标点敏感，建议精简 |
| `size` | string | 否 | 输出尺寸，支持 `"1024x1024"`、`"768x1344"`（竖版）、`"1344x768"`（横版）；万相不支持 `"768x1344"`，详见 [万相](../../raw/model-api-reference/image-generation/wan-image-api-reference.md) 文档 |
| `n` | integer | 否 | 生成图片数量，默认为 1，最大为 4（Z-Image 仅支持 `n=1`） |
| `seed` | integer | 否 | 随机种子，用于结果复现；若未指定，服务端自动生成 |

> **注意**：`size` 参数在 [Vidu](../../raw/model-api-reference/image-generation/vidu-image-models.md) 文档中标注支持 `"512x512"`，但实测该尺寸已下线，当前仅支持 `"1024x1024"` 和 `"1344x768"`，请以最新 API 响应为准。

## 使用方式

调用标准 REST API：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/images/generations" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "wanx-2.1",
        "prompt": "中国水墨风格的松鹤图，留白丰富",
        "size": "1024x1024",
        "n": 1
      }'
```

响应体返回 `data[0].url`（直链地址，有效期 1 小时）及 `data[0].extra_info`（含 seed、cost_tokens 等元信息）。  
对于创意工具类操作（如局部重绘），需额外传入 `image_url` 和 `mask_url`，具体格式见 [创意工具](../../raw/model-api-reference/image-generation/image-creative-tools-api-reference.md) 文档。

## 限制和注意事项

- 单次请求 `prompt` 中禁止包含违法、暴力、成人内容，违者触发实时拦截并计入调用失败；
- 所有模型均不支持负向提示词（`negative_prompt`），该字段将被忽略（与 [常见问题](../../raw/model-api-reference/image-generation/image-faq.md) 中旧版说明矛盾，请以本条为准）；
- 输入图片（如用于 `inpainting`）须为 PNG/JPEG 格式，分辨率 ≤ 2048×2048，文件大小 ≤ 5MB；
- 免费额度仅覆盖 `qwen-vl-plus` 和 `wanx-2.1` 的基础调用，其余模型按实际 token 消耗计费；
- 生成结果版权归属调用方，但平台保留对违规内容的删除权。

## 来源文档

- [图像生成](../../raw/model-api-reference/image-generation.md)


