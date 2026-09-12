# more models

百炼平台持续扩展模型能力，除基础大语言模型外，还提供面向垂直场景的专用模型，覆盖法律、多语言翻译、深度研究、OCR识别、GUI交互等方向。所有模型均通过统一 API 接口调用，支持按需选用。开发者需注意各模型的输入格式、计费粒度及能力边界。

## 支持的模型/功能

当前支持以下专用模型：
- **通义法睿**：面向法律领域的推理与问答模型，适用于合同审查、法规检索等场景；详见 [更多模型](../../raw/model-api-reference/more-models.md)。
- **意图理解**：轻量级模型，专用于用户输入的意图分类与槽位提取，适合对话系统前置处理。
- **Qwen-MT**：高质量多语言机器翻译模型，支持 100+ 语言对，输出为纯文本，不包含结构化元信息。
- **Qwen-Deep-Research**：支持长上下文（最高 1M tokens）与多跳推理，适用于技术文档分析、论文精读等复杂任务；其能力说明见 [更多模型](../../raw/model-api-reference/more-models.md)。
- **Qwen-OCR**：端到端文字识别模型，可直接从图像中提取结构化文本（含位置、行段、置信度），不依赖预处理；详细接口定义参见 [更多模型](../../raw/model-api-reference/more-models.md)。
- **GUI-Plus**：针对截图/录屏图像的界面元素识别与操作意图理解模型，输出控件树及可执行动作建议。

> **注意**：原始文档中 GUI-Plus 的描述未明确是否支持视频帧序列输入，而 [Qwen-Deep-Research 深入研究模型](https://help.aliyun.com/zh/model-studio/qwen-deep-research-api) 官方页面注明其支持“连续帧分析”，该能力在 [更多模型](../../raw/model-api-reference/more-models.md) 中未体现，建议以最新 API 文档为准。

## 关键参数

- `model`: 必填，取值如 `qwen-farui`, `qwen-intent`, `qwen-mt`, `qwen-deep-research`, `qwen-ocr`, `gui-plus`。
- `input`: 结构依模型而异：
  - 法睿/意图/Qwen-MT：`{"text": "..."}`；
  - Qwen-Deep-Research：支持 `{"text": "...", "files": [...]}`（文件为 PDF/DOCX 等）；
  - Qwen-OCR/GUI-Plus：`{"image_url": "..."}` 或 `{"image_base64": "..."}`。
- `parameters.top_k` 等通用参数对部分模型无效（如 OCR 不支持 temperature），具体以各模型文档为准。

## 使用方式

所有模型均通过 `/v1/services/aigc/text-generation/generation` 统一入口调用（POST），鉴权方式与基础模型一致（Bearer [Token](../concepts/token.md)）。示例请求体：
```json
{
  "model": "qwen-ocr",
  "input": {
    "image_url": "https://example.com/receipt.jpg"
  }
}
```
响应结构统一为 `{ "output": { "text": "...", "extra": {...} } }`，其中 `extra` 字段内容因模型而异（如 OCR 返回 `{"boxes": [...], "confidence": 0.98}`）。

## 限制和注意事项

- Qwen-Deep-Research 单次请求最大上下文长度为 1,048,576 tokens，但实际可用长度受文件解析开销影响，PDF 解析后文本可能膨胀 2–3 倍。
- Qwen-OCR 对低分辨率（< 300dpi）或严重畸变图像识别准确率显著下降，建议预处理增强。
- GUI-Plus 当前仅支持单张静态图像，不支持批量图像或视频流（与 [更多模型](../../raw/model-api-reference/more-models.md) 描述一致，但与部分内部测试文档存在出入，以正式发布版本为准）。
- 所有模型均不支持 `stream: true` 流式响应，必须等待完整结果返回。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)



