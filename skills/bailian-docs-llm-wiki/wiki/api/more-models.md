# more models

百炼平台提供一系列面向垂直场景的专用模型，覆盖意图理解、深度研究、OCR 文字提取及 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持按需选用，无需额外部署。详细能力说明与接口规范请参考各子模型文档。

## 支持的模型/功能

当前 `more models` 类别下包含以下专用模型：
- **意图理解模型**：用于识别用户输入背后的业务意图（如“查订单”“退订服务”），适用于对话系统前置路由；详情见 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md)。
- **Qwen-Deep-Research**：专为长文档分析、多跳推理与事实核查设计，支持 128K 上下文；其输入格式与参数约束详见 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md)。
- **Qwen-OCR**：基于 Qwen-VL 架构的端到端 OCR 模型，可直接从图像中提取结构化文本（含表格、公式）；使用方式和输出 schema 见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md)。
- **GUI-Plus**：针对截图/录屏理解优化的模型，支持按钮定位、操作意图识别与跨平台界面生成；能力边界与典型用例参见 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md)。

## 关键参数

所有模型均遵循标准 `/v1/chat/completions` 接口，但需指定 `model` 字段为对应模型标识符（如 `qwen-deep-research`、`qwen-ocr`）。  
- `input` 字段类型依模型而异：意图理解与 GUI-Plus 接受文本+base64 图像混合输入；Qwen-OCR 仅接受图像（`image_url` 或 `image_base64`）；Qwen-Deep-Research 支持纯文本或文本+图像组合。  
- `max_tokens` 对 Qwen-Deep-Research 默认上限为 8192，超出需显式设置；其他模型默认限制为 2048，不可超限。  
> **注意**：原始文档中 GUI-Plus 的 `temperature` 参数说明与 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 中的最新版本存在不一致——后者已明确该参数被忽略，实际行为恒为 0.0。

## 使用方式

1. 在请求 Header 中携带有效的 `Authorization: Bearer <api_key>`；  
2. POST 到 `https://dashscope.aliyuncs.com/api/v1/chat/completions`；  
3. Body 中指定 `model`（如 `"qwen-ocr"`）、`input`（结构符合各模型要求）及必要参数；  
4. 解析响应中的 `output.text`（文本类模型）或 `output.choices[0].message.content`（兼容 OpenAI 格式）字段。  
示例代码与 cURL 调用片段见 [Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 的 “快速开始” 章节。

## 限制和注意事项

- 所有 `more models` 均不支持流式响应（`stream: true` 将被拒绝）；  
- Qwen-Deep-Research 和 GUI-Plus 暂不支持 `system` 消息角色，传入将被静默丢弃；  
- 图像输入尺寸上限为 4096×4096 像素，超限图像将被自动缩放并可能影响 OCR 或 GUI 定位精度；  
> **注意**：[意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md) 文档中提及的“支持 50+ 预置意图标签”为旧版描述，当前实际支持标签集已扩展至 127 个，以控制台最新发布的 Intent Schema 为准。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


