# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、深度研究、OCR 文字提取和 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持按需选用，无需额外部署。所有模型均基于 Qwen 系列底座优化，具备明确的输入输出契约与性能边界。

## 支持的模型与功能

- **意图理解模型**：用于识别用户输入中的操作意图（如“查订单”“改地址”），适用于对话系统前置路由；详见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **Qwen-Deep-Research**：支持长上下文（最高 128K tokens）、多跳推理与文献溯源，专为科研分析与复杂报告生成设计；详见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **Qwen-OCR**：基于 Qwen-VL 架构，可从截图、PDF 页面或扫描件中高精度提取结构化文本及位置信息；详见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  
- **GUI-Plus**：接受屏幕截图 + 自然语言指令，输出 UI 元素定位坐标、操作动作（如 click/tap）或界面改写建议；详见 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `qwen-deep-research`, `qwen-ocr`, `gui-plus` |
| `input` | object | 是 | 模型特定输入结构（如 OCR 要求 `image_url` 或 `base64_image`，GUI-Plus 需 `screenshot` + `instruction`） |
| `max_output_tokens` | integer | 否 | 输出长度上限，默认值因模型而异（Qwen-Deep-Research 默认 4096，GUI-Plus 默认 512） |
| `temperature` | float | 否 | 仅对 Qwen-Deep-Research 和意图理解模型生效；GUI-Plus 与 Qwen-OCR 不支持采样控制 |

> **注意**：原始文档 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中标注 `top_p` 为支持参数，但当前 v2.3.1 API 实际返回 `400 Bad Request`；请暂勿设置该字段。

## 使用方式

1. 通过 `/v1/models/{model}/invoke` 发起 POST 请求（推荐）  
2. 或使用 SDK 封装方法（Python SDK v3.2+ 已内置 `QwenDeepResearchClient`, `QwenOcrClient` 等）  
3. 请求体需严格遵循各模型定义的 `input` schema —— 例如 Qwen-OCR 要求 `{"image_url": "https://..."}`，而 GUI-Plus 要求 `{"screenshot": "...", "instruction": "点击右上角设置图标"}`  
4. 响应格式统一为 `{ "output": { ... }, "usage": { "prompt_tokens", "completion_tokens" } }`

## 限制和注意事项

- 所有模型均不支持流式响应（`stream: true` 将被忽略）  
- Qwen-OCR 单次请求最大图像尺寸为 4096×4096 像素，超限将返回 `413 Payload Too Large`  
- GUI-Plus 仅接受 PNG/JPEG 格式截图，不支持 GIF 或 WebP；且 `instruction` 字段长度不得超过 200 字符  
- 意图理解模型的类别集合固定为预定义的 37 种 action type，不可自定义扩展；完整列表见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- 多模型并发调用时，配额按模型独立计费，但共享同一账户的总 RPS 限制（默认 10 QPS）；详细配额策略参见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 的“计费说明”章节

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


