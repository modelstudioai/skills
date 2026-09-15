# [more](more.md) models

百炼平台提供一系列面向垂直场景的专用模型，覆盖法律推理、意图识别、多语言翻译、深度研究、OCR 文字提取及 GUI 界面交互等任务。这些模型通过统一 API 接口调用，支持按需选用，无需额外部署。详细能力与接口规范请参考各子模型文档，例如 [通义法睿](../../raw/model-api-reference/more-models/tongyi-farui-api.md)。

## 支持的模型与功能

当前支持以下专用模型：

- **通义法睿**：面向法律领域的推理与问答模型，支持法条检索、案例类比和判决预测；  
- **意图理解**：轻量级实时意图识别模型，适用于对话系统前端过滤与路由；  
- **Qwen-MT**：多语言机器翻译模型，支持 100+ 语种互译，提供流式响应与术语控制能力；  
- **Qwen-Deep-Research**：长上下文（最高 1M tokens）研究型模型，专为文献综述、技术报告生成优化；  
- **Qwen-OCR**：端到端图文理解模型，可直接输入截图或扫描件，输出结构化文本及坐标信息；  
- **GUI-Plus**：基于屏幕截图理解用户界面操作意图的模型，支持按钮定位、控件描述与操作建议生成。

> **注意**：[Qwen-OCR 文字提取模型](../../raw/model-api-reference/more-models/qwen-vl-ocr-api-reference.md) 当前仅支持 PNG/JPEG 格式输入，PDF 需先转图；而 [GUI-Plus 界面交互专用模型](../../raw/model-api-reference/more-models/gui-plus-interface-interaction-model.md) 的输入分辨率上限为 1920×1080，超出部分将被自动缩放裁剪——该限制未在 [意图理解](../../raw/model-api-reference/more-models/intent-detect-capability.md) 文档中声明，但实测一致生效。

## 关键参数

所有模型共用以下基础参数（部分模型支持扩展参数）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型标识符，如 `"qwen-farui"`、`"qwen-mt"`、`"gui-plus"` 等，详见各模型文档 |
| `input` | object | 是 | 输入数据结构，格式因模型而异（如 OCR 要求 `{"image": "base64..."}`，MT 要求 `{"source_text": "...", "source_lang": "zh", "target_lang": "en"}`） |
| `parameters` | object | 否 | 模型特定配置，如 `temperature`（仅 Qwen-Deep-Research 支持）、`term_dict`（Qwen-MT 支持术语表注入） |

## 使用方式

1. 通过 `/v1/models/{model}/invoke` 发起 POST 请求（推荐）；  
2. 或使用 SDK 封装方法：`client.invoke_model(model='qwen-deep-research', input=..., parameters={...})`；  
3. 输入结构严格遵循对应模型文档定义，例如 [Qwen-Deep-Research 深入研究模型](../../raw/model-api-reference/more-models/qwen-deep-research-api.md) 要求 `input` 中必须包含 `query` 和 `documents` 字段。

## 限制和注意事项

- 所有模型均不支持跨模型混合输入（如向 `qwen-mt` 发送图像 base64）；  
- 单次请求最大输入长度依模型而定：Qwen-Deep-Research 支持 1M tokens，而意图理解模型上限为 512 tokens；  
- GUI-Plus 和 Qwen-OCR 均要求输入图像为 RGB 模式，CMYK 或带 alpha 通道的 PNG 将导致 400 错误；  
- 模型计费按 token + 调用次数双维度计量，具体计费规则见各模型文档说明。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


