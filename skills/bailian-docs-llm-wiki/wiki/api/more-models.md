# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、深度研究、OCR 文字提取及 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持与基础大模型协同编排。所有模型均需通过 `model` 参数显式指定，不参与默认模型路由。

## 支持的模型与功能

当前可用的专用模型包括：

- **意图理解模型**：用于高精度识别用户输入背后的业务意图（如“查订单”“退订服务”），适用于对话系统前置路由；详见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **Qwen-Deep-Research**：专为长文档分析、多跳推理与证据溯源设计，支持 128K 上下文与结构化输出；参考 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **Qwen-OCR**：基于 Qwen-VL 架构优化的端到端 OCR 模型，可直接从截图/扫描件中提取文字并保留表格、段落结构；说明见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  
- **GUI-Plus**：针对桌面/移动端界面截图的理解与操作生成模型，支持控件定位、操作指令生成（如“点击右上角设置图标”）；详情参阅 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)

> **注意**：GUI-Plus 当前仅支持 PNG/JPEG 格式截图输入，且不兼容含透明通道的图像——该限制未在 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中明确说明，以本 Wiki 实际行为为准。

## 关键参数

调用时必须指定以下参数：

- `model`: 字符串，取值为 `intent-detect` / `qwen-deep-research` / `qwen-ocr` / `gui-plus`（大小写敏感）  
- `input`: 结构依模型而异：  
  - `intent-detect` 和 `qwen-deep-research` 接受 `{"text": "..."}`；  
  - `qwen-ocr` 和 `gui-plus` 必须传 `{"image_url": "https://..."}` 或 `{"image_base64": "..."}`  
- `parameters`（可选）：各模型支持子集参数，例如 `qwen-deep-research` 支持 `max_output_tokens`，但 `intent-detect` 不支持 `temperature`

## 使用方式

通过 `/v1/models/{model}/invoke` 端点发起 POST 请求（推荐），或使用 SDK 的 `client.models.invoke()` 方法：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/models/qwen-ocr/invoke \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"image_url": "https://example.com/receipt.jpg"}}'
```

> **注意**：`/v1/chat/completions` 端点**不支持**调用上述专用模型，必须使用 `/v1/models/{model}/invoke` —— 此要求与部分旧版示例代码冲突，以 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 中的接口定义为准。

## 限制和注意事项

- 所有模型均按请求计费，无免费额度；  
- `qwen-ocr` 单次请求最大图像尺寸为 4096×4096 像素，超限将返回 `400 Bad Request`；  
- `gui-plus` 输出不含置信度分数，不可用于阈值过滤；  
- 意图理解模型仅支持中文输入，英文输入将返回空结果（该行为未在 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中声明，属隐式约束）。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


