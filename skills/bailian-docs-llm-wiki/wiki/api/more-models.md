# more models

百炼平台持续扩展模型能力，除基础大语言模型外，还提供面向垂直场景的专用模型服务，覆盖法律、多语言翻译、深度研究、OCR识别、GUI交互等方向。所有模型均通过统一 API 接口调用，支持按需选用与灵活集成。开发者需注意各模型的输入格式、计费粒度及能力边界。

## 支持的模型/功能

当前支持以下专用模型（按功能分类）：

- **法律领域**：通义法睿，专为法律文书理解、条款分析与合规推理优化；详情见 [更多模型](../../raw/model-api-reference/more-models.md)  
- **意图识别**：意图理解模型，适用于对话系统中的用户意图分类与槽位抽取；参考 [更多模型](../../raw/model-api-reference/more-models.md)  
- **多语言机器翻译**：Qwen-MT，支持中英等 100+ 语种互译，提供流式响应与术语控制能力  
- **深度研究辅助**：Qwen-Deep-Research，支持长文档解析、跨文档推理与结构化结论生成  
- **视觉文本识别**：Qwen-OCR，专注高精度文字提取（含表格、手写体、低清图像），输出带坐标信息的结构化文本  
- **GUI交互理解**：GUI-Plus，可解析截图/录屏中的界面元素、操作路径与交互逻辑，适用于自动化测试与无障碍辅助  

> **注意**：Qwen-OCR 的实际识别精度受图像分辨率与背景复杂度显著影响，其能力描述与 [更多模型](../../raw/model-api-reference/more-models.md) 中链接指向的官方文档一致，但部分旧版 SDK 示例未启用坐标回归开关，建议以最新 API 文档为准。

## 关键参数

各模型共用以下核心参数（部分模型支持扩展字段）：

- `model`: 必填，模型标识符（如 `qwen-farui`, `qwen-intent`, `qwen-mt-zh2en`）  
- `input`: 必填，结构化输入对象，格式因模型而异（例如 Qwen-OCR 要求 `{"image_url": "..."}`，Qwen-MT 要求 `{"source_text": "...", "target_language": "en"}`）  
- `parameters`: 可选，控制生成行为（如 `temperature`, `top_p` 仅对生成类模型生效；OCR 类模型不支持）  

具体参数定义请严格参照对应模型的 API 文档，例如 Qwen-Deep-Research 的 `max_research_depth` 参数在 [更多模型](../../raw/model-api-reference/more-models.md) 中未展开说明，需查阅其独立接口文档。

## 使用方式

1. 确认模型开通权限（部分模型需单独申请配额）  
2. 构造 HTTP POST 请求，Endpoint 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/<service>/call`（`<service>` 由模型类型决定，如 `farui`, `intent-detect`）  
3. 设置 `Authorization: Bearer <api_key>` 与 `Content-Type: application/json`  
4. 按模型要求组织 `input` 字段（严禁混用不同模型的 input schema）  

示例（Qwen-MT）：
```json
{
  "model": "qwen-mt-zh2en",
  "input": {
    "source_text": "你好，今天天气不错。",
    "target_language": "en"
  }
}
```

## 限制和注意事项

- 所有模型均按 token 或请求次数计费，Qwen-OCR 按图片张数计费，Qwen-Deep-Research 按“研究步骤”计费，计费规则详见各模型文档  
- 单次请求最大输入长度因模型而异：Qwen-Deep-Research 支持最长 128K tokens 上下文，而意图理解模型限制为 512 字符  
- GUI-Plus 当前仅支持 PNG/JPEG 格式截图，不支持视频帧序列批量处理  
- 部分模型（如通义法睿）返回结果含法律依据引用，但该引用不构成正式法律意见，不可直接用于司法程序  

> **注意**：原始文档中列出的“意图理解”链接已更新至新版路径，旧版文档存在参数名不一致问题（如 `query` vs `text`），实际调用必须以 [更多模型](../../raw/model-api-reference/more-models.md) 中提供的最新链接为准。

## 来源文档

- [更多模型](../../raw/model-api-reference/more-models.md)


