# qwen mt translation models

Qwen-MT 系列是百炼平台提供的多模态机器翻译模型族，覆盖纯文本、图像及混合模态输入的翻译场景。模型基于 Qwen 大语言模型底座优化，支持高保真语义转换与格式还原。所有模型均通过统一 API 接口提供服务，兼容 OpenAI 格式与 DashScope 原生协议。

## 支持的模型/功能

- **Qwen-MT**：纯文本翻译，支持 100+ 语言对，适用于通用、技术、商务等场景；详见 [翻译模型 (raw/model-api-reference/qwen-mt-translation-models.md)](../../raw/model-api-reference/qwen-mt-translation-models.md)。  
- **Qwen-MT-Image**：图像内嵌文本识别与翻译，保留原文排版结构（如表格、段落缩进、图文位置关系）；能力说明见 [翻译模型 (raw/model-api-reference/qwen-mt-translation-models.md)](../../raw/model-api-reference/qwen-mt-translation-models.md)。  
- **Qwen-MT-Uni**：全模态翻译模型，接受文本、PDF/DOCX 文档、JPG/PNG 图像、WAV/MP3 音频作为输入，自动识别内容类型并执行端到端翻译；其接口规范参见 [翻译模型 (raw/model-api-reference/qwen-mt-translation-models.md)](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source_language` | string | 是 | 源语言代码（如 `"zh"`、`"en"`），部分模型支持 `"auto"` 自动检测 |
| `target_language` | string | 是 | 目标语言代码（如 `"ja"`、`"fr"`） |
| `input` | string / object | 是 | 文本模式为字符串；图片/文档/音频需传入 base64 或 OSS URL 对象（详见 [Qwen-MT-Uni API 参考](raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)） |
| `preserve_format` | boolean | 否 | 默认 `false`；设为 `true` 时启用排版保留（仅 Qwen-MT-Image 和 Qwen-MT-Uni 支持） |

> **注意**：`source_language="auto"` 在 Qwen-MT-Uni 中实际支持度低于文档描述——实测对低资源语言（如斯瓦希里语、缅甸语）检测准确率显著下降，建议显式指定源语言。

## 使用方式

- 所有模型均支持两种调用方式：  
  - DashScope 原生 SDK（推荐）：`dashscope.Generation.call(model='qwen-mt', ...)`  
  - [OpenAI 兼容接口](../concepts/openai-compatible-api.md)：`POST https://dashscope.aliyuncs.com/api/v1/chat/completions`，`model` 字段设为 `"qwen-mt"`、`"qwen-mt-image"` 或 `"qwen-mt-uni"`  
- 图片/文档/音频输入必须通过 `input` 字段以结构化对象传递，不可拼接为纯文本；具体 schema 见 [Qwen-MT-Image API 参考](raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 和 [Qwen-MT-Uni API 参考](raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 8192 tokens；图片分辨率 ≤ 4096×4096 px；PDF 页数 ≤ 50 页；音频时长 ≤ 10 分钟。  
- Qwen-MT-Uni 的音频翻译仅支持语音转写+翻译两步合一，**不支持**直接输入已转写的文本再触发翻译（该行为将被静默忽略）。  
- 所有模型均不支持实时流式响应（`stream=true` 参数无效），返回为完整 JSON 结构体。  
- 输出字段 `translated_text` 在图片/文档类模型中可能为 HTML 片段（含 `<span style="...">` 标签），客户端需做安全渲染处理。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


