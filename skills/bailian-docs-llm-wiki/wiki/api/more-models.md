# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、深度研究、OCR 文字提取及 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持与基础大模型协同编排。所有模型均需通过 `model` 参数显式指定，不参与默认模型路由。

## 支持的模型与功能

当前可用的专用模型包括：
- **意图理解模型**：用于高精度识别用户输入的结构化意图（如“查订单”“比价”“预约维修”），适用于对话系统前置解析；详情见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research**：专为长文档分析、多跳推理与证据溯源设计，支持 128K 上下文和结构化输出；其能力边界与调用规范详见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR**：基于 Qwen-VL 架构优化的端到端文字识别模型，支持图像中印刷体、手写体及复杂版式文本提取；接口定义与示例请参考 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus**：针对截图/录屏等 GUI 元素理解任务优化，可定位控件、识别状态并生成可执行操作指令（如 `click("提交按钮")`）；具体输入格式与响应 schema 见 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

## 关键参数

- `model`: 必填，取值为模型标识符（如 `"qwen-deep-research"`、`"qwen-ocr"`），**不可使用别名或版本后缀**（例如 `"qwen-deep-research-v1"` 将报错）。
- `input`: 结构依赖模型类型：
  - 意图理解与 GUI-Plus 要求 `{"text": "...", "image_url": "..."}` 或仅 `{"text": "..."}`；
  - Qwen-OCR 仅接受 `{"image_url": "..."}`；
  - Qwen-Deep-Research 支持 `{"text": "...", "documents": [...]}`。
- `parameters.temperature`: 仅对意图理解和 Qwen-Deep-Research 生效；GUI-Plus 与 Qwen-OCR 固定为 0（确定性输出）。

> **注意**：原始文档 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中提及支持 `max_output_tokens` 参数，但实测 v2.3.0+ 版本已弃用该参数，应改用 `parameters.max_new_tokens` —— 请以实际 API 响应错误提示为准。

## 使用方式

1. 发送 POST 请求至 `/v1/models/{model}/invoke`（如 `/v1/models/qwen-ocr/invoke`）；
2. Header 中携带 `Authorization: Bearer <api_key>`；
3. Body 为 JSON，按模型要求组织 `input` 和 `parameters`；
4. 同步返回 `output` 字段，结构因模型而异（例如 Qwen-OCR 返回 `{"text": "识别结果", "boxes": [...]}`）。

## 限制和注意事项

- 所有专用模型均不支持流式响应（`stream: true` 将被忽略）；
- Qwen-OCR 单次请求图像尺寸上限为 4096×4096 像素，超限将返回 `400 Bad Request`；
- GUI-Plus 模型暂不支持批量处理（`input` 中不可传入多个 image_url）；
- 意图理解模型的类别体系由平台预置且定期更新，**不可通过 `parameters.custom_labels` 扩展**——该字段在 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md) 文档中已被标记为废弃（v2.1.0 起）。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


