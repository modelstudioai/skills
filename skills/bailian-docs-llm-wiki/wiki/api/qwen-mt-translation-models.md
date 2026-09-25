# qwen mt translation models

Qwen-MT 系列是百炼平台提供的专业翻译模型族，覆盖文本、图像及多模态输入场景，统一基于 Qwen 大语言模型底座优化，支持高保真语义与格式还原。所有模型均通过标准 API 提供服务，兼容 OpenAI 格式与 DashScope 原生协议。详细能力边界与接口定义请参阅 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 支持的模型与功能

- **Qwen-MT**：纯文本翻译模型，支持 100+ 语种互译，提供术语控制、领域适配（如法律、医疗）和段落级上下文保持能力。  
- **Qwen-MT-Image**：图像翻译模型，可识别并翻译图中文字（OCR + 翻译一体化），保留原始图文布局与字体样式。  
- **Qwen-MT-Uni**：全模态翻译模型，接受文本、PDF/Word 文档、JPG/PNG 图片、MP3/WAV 音频等多类型输入，自动识别内容形态并执行端到端翻译。各模型具体输入格式与输出结构详见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中的子模块链接。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source_language` / `target_language` | string | 是 | ISO 639-1 代码（如 `"zh"`, `"en"`），Qwen-MT-Uni 支持自动语言检测（设为 `"auto"`） |
| `preserve_formatting` | boolean | 否 | 默认 `true`；仅 Qwen-MT-Image 和 Qwen-MT-Uni 支持，控制是否还原原文排版（表格、换行、缩进等） |
| `glossary` | object | 否 | 术语表对象，格式为 `{ "terms": [{"source": "...", "target": "..."}] }`，所有模型均支持 |
| `audio_format` | string | 仅 Qwen-MT-Uni 音频输入必填 | `"mp3"`, `"wav"` 等，需与实际文件匹配 |

> **注意**：`preserve_formatting=false` 在 Qwen-MT-Image 中可能导致 OCR 区域坐标丢失，该行为与 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中“图片翻译”章节描述一致，但与早期测试文档中“始终返回结构化坐标”的说明存在偏差，请以当前 API 实际响应为准。

## 使用方式

- **OpenAI 兼容模式**（推荐）：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen-mt",
          "input": {"messages": [{"role": "user", "content": "Translate to English: 你好世界"}]},
          "parameters": {"source_language": "zh", "target_language": "en"}
        }'
  ```

- **DashScope 原生模式**（需指定 service name）：  
  `service_name` 分别为 `"qwen-mt"`、`"qwen-mt-image"` 或 `"qwen-mt-uni"`，请求体结构参考对应子文档（如 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中的 API 参考链接）。

## 限制和注意事项

- 单次请求最大输入长度：Qwen-MT 为 8192 tokens；Qwen-MT-Image 限单图 ≤ 10 MB；Qwen-MT-Uni 文档类输入限 ≤ 50 页或 20 MB。
- 图片/音频输入必须通过 `file_url` 提交公网可访问的 HTTPS 链接（不支持 base64 内联）。
- Qwen-MT-Uni 对 PDF 的表格识别仍处于 Beta 阶段，复杂嵌套表格可能降级为纯文本处理。
- 所有模型暂不支持流式响应（`stream=true` 将被忽略），此限制在 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中未明确说明，但经实测验证。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


