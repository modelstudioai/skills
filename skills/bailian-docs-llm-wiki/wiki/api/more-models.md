# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、深度研究、OCR 文字提取和 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持按需选用，无需额外部署。所有模型均需通过 `model` 参数显式指定，不参与通用模型的自动路由。

## 支持的模型与功能

当前可用的专用模型包括：
- **意图理解模型**：用于识别用户输入背后的业务意图（如“查订单”“改地址”），适用于对话系统前置处理；详见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research**：专为长文档分析、多跳推理与事实核查优化的大模型，支持 128K 上下文；其能力细节与典型用例见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR**：基于多模态架构的端到端文字识别模型，可直接输入图像 URL 或 base64 编码图像，输出结构化文本及坐标信息；接口规范参见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus**：针对截图/录屏图像进行 UI 元素识别、操作意图解析与自然语言指令生成的专用模型，适用于自动化测试与无障碍辅助场景。

> **注意**：原始文档中 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 提到支持“实时屏幕流输入”，但该能力尚未在 v2.3.0 API 中开放，实际仅接受单帧 PNG/JPEG 图像。请以最新 SDK 文档为准。

## 关键参数

调用上述模型时，必须设置以下参数：
- `model`: 字符串，取值为 `qwen-intent`, `qwen-deep-research`, `qwen-ocr`, 或 `gui-plus`（大小写敏感）；
- `input`: 结构体，内容依模型而异：
  - `qwen-intent` 和 `qwen-deep-research`：`{"text": "..."}`；
  - `qwen-ocr`：`{"image_url": "...", "language": "zh"}` 或 `{"image": "base64..."}`；
  - `gui-plus`：`{"image": "base64...", "instruction": "点击登录按钮"}`（`instruction` 为可选字段）；
- `parameters.temperature`：仅对 `qwen-intent` 和 `qwen-deep-research` 有效，`qwen-ocr` 与 `gui-plus` 不支持采样控制。

## 使用方式

1. 发送 POST 请求至 `/v1/models/chat/completions`（与通用模型共用 endpoint）；
2. 在请求体中明确指定 `model` 及对应 `input` 结构；
3. 注意响应格式差异：`qwen-ocr` 返回 `{"text": "...", "boxes": [...]}`，而 `gui-plus` 返回 `{"action": "...", "elements": [...]}`，需按模型文档解析。

## 限制和注意事项

- 所有专用模型均不支持 `stream: true` 流式响应（[Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 明确标注此限制）；
- `qwen-ocr` 单次请求图像尺寸上限为 4096×4096 像素，超限将返回 `400 Bad Request`；
- `gui-plus` 输入图像需为清晰 UI 截图，不支持自然场景图或低分辨率模糊图像；
- 模型计费独立于通用模型，按调用次数与输入 token（或图像）分别计量，详情见配额管理后台。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


