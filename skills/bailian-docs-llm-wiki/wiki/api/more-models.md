# more models

百炼平台持续扩展模型能力，除基础大语言模型外，还提供面向垂直场景的专用模型服务，覆盖法律、多语言翻译、深度研究、OCR识别、GUI交互等方向。所有模型均通过统一 API 接口调用，支持按需选用与灵活集成。开发者需注意各模型的输入格式、计费粒度及能力边界。

## 支持的模型/功能

当前支持以下专用模型（按功能分类）：

- **法律领域**：通义法睿，专为法律文书理解、条款分析与合规推理优化；详情见 [更多模型](../../raw/model-api-reference/more-models.md)  
- **意图识别**：意图理解模型，适用于对话系统中的用户意图分类与槽位抽取；参考 [更多模型](../../raw/model-api-reference/more-models.md)  
- **多语言机器翻译**：Qwen-MT，支持中英等 100+ 语种互译，提供流式与非流式两种响应模式  
- **深度研究辅助**：Qwen-Deep-Research，面向长文档阅读、跨文档推理与复杂问题拆解；其能力说明见 [更多模型](../../raw/model-api-reference/more-models.md)  
- **视觉文字提取**：Qwen-OCR，专精于扫描件、截图、表格图像中的文本定位与结构化识别  
- **GUI界面理解与操作**：GUI-Plus，可解析界面截图并生成可执行操作指令（如“点击右上角设置按钮”）

> **注意**：Qwen-OCR 当前仅支持 PNG/JPEG 格式输入，不支持 PDF 直接上传；而部分旧版文档误述其支持 PDF —— 请以 [更多模型](../../raw/model-api-reference/more-models.md) 中链接的最新 API 文档为准。

## 关键参数

各模型共用以下核心参数（部分模型有额外字段）：

- `model`: 必填，模型标识符（如 `qwen-farui`、`qwen-ocr`、`gui-plus`）  
- `input`: 必填，结构体，内容依模型而异（例如 Qwen-OCR 要求 `image_url` 或 `image_base64`；GUI-Plus 需 `screenshot` + `instruction`）  
- `parameters.temperature`: 可选，仅对生成类模型（如法睿、Deep-Research）生效，范围 0.0–1.0  
- `stream`: 布尔值，仅 Qwen-MT 和 Qwen-Deep-Research 支持流式响应  

## 使用方式

1. 确认模型是否已开通权限（部分模型需单独申请配额）  
2. 构造请求体，严格遵循对应模型的 `input` schema（参见各模型官方文档页）  
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/<model-name>/completion`  
4. 解析响应中的 `output.text`（文本类）或 `output.data`（结构化结果，如 OCR 的 `text_lines` 字段）  

## 限制和注意事项

- 所有模型均受百炼平台通用速率限制（RPS）与单次请求长度限制约束；具体阈值以控制台配额页为准  
- Qwen-Deep-Research 单次输入最大支持 500 页 PDF 文本（经预处理后），超长内容将被截断且不报错  
- GUI-Plus 模型要求截图分辨率为 1920×1080 或更低，过高分辨率可能导致识别失败或延迟增加  
- 意图理解模型输出为 JSON 数组，每个元素含 `intent` 和 `slots` 字段，**不返回自然语言回复** —— 此行为与早期文档描述不符，请以 [更多模型](../../raw/model-api-reference/more-models.md) 中链接的最新接口规范为准

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


