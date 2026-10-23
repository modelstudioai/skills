# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、深度研究、OCR 文字提取及 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持按需选用，无需额外部署。详细能力说明与接口规范请参考各子模型文档。

## 支持的模型/功能

当前 `more models` 类别下包含以下专用模型：
- **意图理解模型**：用于识别用户输入背后的业务意图（如“查订单”“退订服务”），适用于对话系统前置路由；详见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research**：专为长文档分析、多跳推理与事实核查设计，支持 128K 上下文；其能力边界和典型用例见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR**：基于 Qwen-VL 架构优化的端到端 OCR 模型，可直接从图像中提取结构化文本（含表格、公式）；接口参数与返回格式详见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus**：针对截图/录屏等 GUI 界面图像进行操作意图识别与控件定位，输出可执行指令序列；具体输入约束与坐标系约定参见 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

## 关键参数

所有模型均遵循统一请求体结构，必填字段包括：
- `model`: 模型标识符（如 `qwen-deep-research`, `qwen-ocr`, `gui-plus`）
- `input`: 输入数据，类型依模型而异（纯文本、base64 图像、或含 image + text 的 multipart 结构）
- `parameters.temperature`: 浮点数，范围 `[0.0, 2.0]`，仅对生成类模型（如 `qwen-deep-research`）生效；OCR 和意图理解模型忽略该参数。

> **注意**：原始文档中 `gui-plus` 的 `input` 字段示例使用了过时的 `screenshot_url` 字段，实际 API 已强制要求 `image` 字段以 base64 编码传入，最新定义以 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中的「请求体示例」为准。

## 使用方式

通过 `/v1/models/{model}/invoke` 接口调用（POST），需在 Header 中携带 `Authorization: Bearer <api_key>`。  
示例（调用 Qwen-OCR）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/qwen-ocr/invoke" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "input": {"image": "data:image/png;base64,iVBORw..."},
        "parameters": {}
      }'
```

## 限制和注意事项

- 所有模型均不支持流式响应（`stream: true` 将被忽略）；
- Qwen-OCR 单次请求图像分辨率上限为 4096×4096 像素，超限将返回 `400 Bad Request`；
- 意图理解模型仅接受纯文本输入，传入图像或 base64 将触发 `422 Unprocessable Entity`；
- 同一 API Key 下，`qwen-deep-research` 与 `gui-plus` 共享每分钟 5 次调用配额，详情见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 的「配额说明」章节。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


