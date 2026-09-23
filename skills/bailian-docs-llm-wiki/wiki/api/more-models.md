# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律推理、意图识别、深度研究、OCR 文字提取及 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持与基础大模型（如 Qwen-Max）协同编排。所有模型均需通过 `model` 参数显式指定，不支持默认 fallback。

## 支持的模型与功能

当前开放以下专用模型（按功能分类）：

- **法律领域**：通义法睿，专为法律条文理解、类案检索与文书生成优化，详见 [通义法睿](../../raw/model-api-reference/more-models/tongyi-farui-api.md)  
- **语义理解**：意图理解模型，适用于对话系统中的用户意图分类与槽位抽取，详见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)  
- **长程推理**：Qwen-Deep-Research，支持多步假设验证与跨文档证据聚合，适用于科研分析场景，详见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)  
- **多模态 OCR**：Qwen-OCR，可从截图、扫描件中高精度提取结构化文本（含表格、公式），详见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)  
- **GUI 交互**：GUI-Plus，接受屏幕截图 + 自然语言指令，输出操作路径或 UI 元素坐标，详见 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)

> **注意**：GUI-Plus 当前仅支持 PNG 格式输入，且最大分辨率限制为 1920×1080；而 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 明确支持 JPG/PNG/PDF（单页），二者在输入格式兼容性上存在差异，调用前请严格校验输入类型。

## 关键参数

所有模型共用以下必需参数：

- `model`: 字符串，必须为模型 ID（如 `"qwen-farui"`、`"qwen-ocr"`），不可省略  
- `input`: 对象，结构依模型而异（如 GUI-Plus 要求 `{"image": "base64...", "instruction": "..."}`，而意图理解仅需 `{"text": "..."}`）  
- `parameters`: 可选对象，支持 `temperature`（仅部分模型生效）、`max_output_tokens`（全局生效）

> **注意**：`temperature` 在 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中明确标注为“无效参数”，但在 [通义法睿](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 文档中未声明是否支持——实际调用时设为非默认值将被静默忽略。

## 使用方式

1. 构造请求体，确保 `model` 与对应模型文档要求的 `input` 结构一致  
2. 发送 POST 请求至 `/v1/chat/completions`（所有模型统一入口）  
3. 解析响应中的 `output.text` 或 `output.choices[0].message.content`（具体字段见各模型文档）

示例（调用 Qwen-OCR）：
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-ocr",
    "input": {"image": "data:image/png;base64,..."},
    "parameters": {"max_output_tokens": 2048}
  }'
```

## 限制和注意事项

- 所有模型均不支持流式响应（`stream: true` 将返回 400 错误）  
- 输入长度限制因模型而异：Qwen-Deep-Research 最高支持 32K tokens 上下文，GUI-Plus 图像 base64 编码后不得超过 10MB  
- 模型 ID 区分大小写，`"qwen-ocr"` 有效，`"Qwen-OCR"` 无效  
- 调用失败时，错误码 `ModelNotSupported` 表示该 `model` 值未注册或已下线，需查阅最新 [更多模型](../../raw/model-api-reference/more-models.md) 文档确认可用列表

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


