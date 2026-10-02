# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律、意图识别、深度研究、OCR 与 GUI 交互等任务。这些模型通过统一 API 接口调用，支持按需选用。所有模型均需显式指定 `model` 参数，且部分模型对输入格式、上下文长度或请求频率存在特定约束。

## 支持的模型与功能

当前可用的专用模型包括：
- **通义法睿**：面向法律领域的推理与问答模型，支持法条引用、案例类比和合规性分析；详见 [通义法睿](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。
- **意图理解**：轻量级实时意图分类模型，适用于对话系统前置路由；其能力边界与标签体系定义见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research**：长上下文（最高 1M tokens）研究型模型，专为多文档交叉分析、假设验证与报告生成优化；详细接口规范参见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR**：端到端图文理解模型，支持复杂版式 PDF/扫描件中的文字提取与结构化输出；使用说明见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus**：基于屏幕截图理解用户操作意图并生成可执行指令的模型，仅接受 base64 编码图像输入；具体交互协议参考 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

> **注意**：原始文档中 `Qwen-OCR` 的路径名含 `-vl-`（即 `qwen-vl-ocr-api-reference.md`），但实际模型 ID 为 `qwen-ocr`；调用时请以 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 中声明的 `model` 字段值为准，避免使用路径名推断模型 ID。

## 关键参数

所有模型共用以下必需参数：
- `model`: 字符串，必须与文档中声明的模型 ID 完全一致（如 `"qwen-farui"`、`"qwen-deep-research"`）；
- `input`: 结构体，字段依模型而异（例如 GUI-Plus 要求 `{"image": "base64..."}`，而意图理解仅接受 `{"text": "..."}`）；
- `parameters.temperature`: 可选，范围 `[0.0, 1.0]`，默认 `0.3`；部分模型（如通义法睿）对该参数敏感度较低，建议优先调整 `top_p`。

## 使用方式

通过 `/v1/models/{model}/invoke` 或统一 `/v1/chat/completions`（需在 `model` 字段中指定）发起 POST 请求。推荐使用后者以保持客户端兼容性。示例（意图理解）：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-intent-detection",
    "input": {"text": "我想查一下上个月的报销进度"},
    "parameters": {"top_p": 0.8}
  }'
```

> **注意**：`qwen-intent-detection` 是当前生效的模型 ID，而非原始文档标题中的“意图理解”；该命名差异已在 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md) 中更新说明，请以该文档的 `model` 字段值为唯一依据。

## 限制和注意事项

- 所有模型均受百炼平台通用配额限制（QPS、并发数、月度 token 总量），具体阈值需在控制台查看；
- Qwen-Deep-Research 模型单次请求最大上下文为 1,048,576 tokens，但输入超 500K tokens 时响应延迟显著增加，建议分块预处理；
- GUI-Plus 不支持文本输入，若传入 `input.text` 将返回 `400 Bad Request`；
- 通义法睿暂不支持 `stream: true`，启用流式响应将导致 `501 Not Implemented` 错误；
- 模型 ID 区分大小写，且不可混用别名（如 `tongyi-farui` ≠ `qwen-farui`），请严格对照各模型文档中的 [通义法睿](../../raw/model-api-reference/more-models/tongyi-farui-api.md) 等原文定义。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


