# more models

百炼平台持续扩展模型能力，除基础大语言模型外，还提供面向垂直场景的专用模型，覆盖法律、多语言翻译、深度研究、OCR识别、GUI交互等方向。这些模型通过统一 API 接口调用，支持按需选用。开发者需注意各模型的输入格式、计费粒度及服务可用区域差异。

## 支持的模型/功能

当前支持以下专用模型：
- **通义法睿**：面向法律领域的推理与问答模型，适用于合同审查、法规检索等场景 [更多模型](../../raw/model-api-reference/more-models.md)  
- **意图理解**：轻量级 NLU 模型，用于用户输入的意图分类与槽位抽取 [更多模型](../../raw/model-api-reference/more-models.md)  
- **Qwen-MT**：高质量多语言机器翻译模型，支持 100+ 语种互译  
- **Qwen-Deep-Research**：支持长上下文（最高 1M tokens）、多跳推理与文献溯源的深度研究模型  
- **Qwen-OCR**：基于视觉-语言融合架构的文字提取模型，可处理扫描件、截图等复杂版式图像  
- **GUI-Plus**：专为界面理解与操作生成设计的多模态模型，支持截图输入与交互指令生成 [更多模型](../../raw/model-api-reference/more-models.md)  

> **注意**：Qwen-OCR 文档中声明支持“表格结构识别”，但 [Qwen-VL OCR API 参考](https://help.aliyun.com/zh/model-studio/qwen-vl-ocr-api-reference) 当前版本未开放 `return_table` 参数；实际使用请以最新 OpenAPI Schema 为准。

## 关键参数

所有模型均遵循百炼通用请求体结构，但部分字段为必需或有特殊约束：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `model` | 必填，模型标识符 | `"qwen-farui"`、`"qwen-mt"`、`"gui-plus"` |
| `input` | 必填，结构依模型而异（如 `text`、`image_url`、`source_lang/target_lang`） | `{ "text": "合同第5条是否构成违约？" }` |
| `parameters.top_k` | 仅法睿、意图理解等分类类模型支持 | `3` |
| `parameters.source_lang` / `target_lang` | Qwen-MT 必填 | `"zh"`, `"en"` |

## 使用方式

1. 确认模型是否已在控制台「模型服务」中开通（部分模型需单独申请配额）  
2. 构造 POST 请求至 `/v1/services/aigc/text-generation/generation`（通用入口）或 `/v1/services/aigc/translation/generation`（Qwen-MT 专用入口）  
3. 在请求头中携带 `Authorization: Bearer <api_key>`  
4. 注意响应中的 `usage.input_tokens` 和 `usage.output_tokens`，用于成本核算与限流判断  

## 限制和注意事项

- 所有模型均受百炼平台全局速率限制（RPS）与账户级并发数限制，GUI-Plus 和 Qwen-Deep-Research 默认并发上限为 2  
- Qwen-Deep-Research 输入长度上限为 1,048,576 tokens，但实际可用长度受内存与超时（默认 120s）制约  
- Qwen-OCR 不支持 PDF 直传，须先转为 JPG/PNG；若图像尺寸 > 4096×4096，将自动缩放并可能影响精度  
- 意图理解模型仅返回 `intent` 和 `slots` 字段，不支持 `stream=true` 流式响应 —— 此行为与 [更多模型](../../raw/model-api-reference/more-models.md) 中描述一致，但与通用文本生成接口文档存在隐式不兼容，建议显式设置 `stream=false`

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


