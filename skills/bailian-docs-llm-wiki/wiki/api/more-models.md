# more models

百炼平台持续扩展模型能力，除基础大语言模型外，还提供面向垂直场景的专用模型服务，覆盖法律、多语言翻译、意图识别、OCR、深度研究及GUI交互等方向。所有模型均通过统一 API 接口调用，支持按需选用。开发者需关注各模型的输入格式、计费粒度及能力边界。

## 支持的模型与功能

当前平台支持以下专用模型（按功能分类）：

- **法律领域**：通义法睿，专为法律文书理解、条款分析与合规推理优化；详情见 [更多模型](../../raw/model-api-reference/more-models.md)  
- **意图识别**：意图理解模型，适用于对话系统中的用户意图分类与槽位提取；参考 [更多模型](../../raw/model-api-reference/more-models.md)  
- **多语言翻译**：Qwen-MT API，支持高质量中英及其他语种互译，输出可控制术语一致性；详见 [更多模型](../../raw/model-api-reference/more-models.md)  
- **视觉文档处理**：Qwen-OCR，专注高精度文本提取（含表格、手写体、低清图像），不支持通用图像理解；  
- **深度研究辅助**：Qwen-Deep-Research，面向长文档摘要、跨文献推理与假设生成，输入长度上限为 128K tokens；  
- **GUI交互理解**：GUI-Plus，专用于截图/录屏中的界面元素识别、操作意图推断与自动化脚本生成。

> **注意**：原始文档中将 Qwen-OCR 归类为 “Qwen-VL OCR”，但最新 SDK 和 OpenAPI 文档已统一使用 `qwen-ocr` 作为 model name，旧名 `qwen-vl-ocr` 已废弃，调用时请以 [Qwen-OCR 文字提取模型](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference) 页面的最新参数说明为准。

## 关键参数

所有模型共用以下核心参数（部分模型有额外字段）：

- `model`: 必填，模型标识符，如 `"qwen-farui"`, `"qwen-intent"`, `"qwen-mt"` 等；  
- `input`: 结构化输入，类型因模型而异（如 `intent` 模型要求 `{"text": "..."}`，`qwen-ocr` 要求 `{"image_url": "..."}`）；  
- `parameters`: 可选，常见字段包括 `temperature`（仅部分模型支持）、`top_k`、`max_output_tokens`；  
- `stream`: 布尔值，仅 `qwen-farui` 和 `qwen-deep-research` 支持流式响应。

## 使用方式

1. 确认模型是否已开通权限（部分模型需单独申请，如 `qwen-deep-research`）；  
2. 构造请求体，严格遵循对应模型的 `input` schema（例如 GUI-Plus 输入必须包含 base64 编码截图或公网可访问 URL）；  
3. 发送 POST 请求至 `/v1/services/aigc/text-generation/generation`（通用入口），平台自动路由至后端专用服务；  
4. 解析响应：成功时返回 `output.text` 或 `output.items`（如 OCR 返回结构化文本块列表）。

## 限制和注意事项

- 所有模型均受百炼平台通用配额限制（QPS、日调用量、单次 token 上限），具体数值需在控制台查看；  
- `qwen-ocr` 不支持 PDF 直接上传，需先转为图像；`qwen-mt` 不支持段落级上下文记忆，每次请求独立翻译；  
- GUI-Plus 当前仅接受 PNG/JPEG 格式，且图像分辨率建议 ≤ 1920×1080，超限将被自动缩放并可能影响识别精度；  
- 意图理解模型返回的 `confidence` 分数为相对置信度，未校准为概率值，不可直接用于阈值过滤。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


