# qwen mt translation models

Qwen MT 系列是百炼平台提供的多模态翻译模型家族，专为高精度、低延迟的跨语言内容转换设计，覆盖纯文本、图像及混合模态输入场景。模型基于 Qwen 大语言模型底座优化，支持端到端语义对齐与格式保真。所有模型均通过统一 API 网关接入，兼容 OpenAI 格式与 DashScope 原生协议。

## 支持的模型与功能

- **`qwen-mt`**：纯文本翻译模型，支持 100+ 语言对，适用于 API 调用、批量文本处理等场景。详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。
- **`qwen-mt-image`**：图片翻译模型，可识别图中文字并保留原始排版结构（如表格、多栏、图文混排），输出带坐标信息的翻译结果。该能力在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中有明确说明。
- **`qwen-mt-uni`**：全模态翻译模型，支持文本、PDF/DOCX 文档、JPG/PNG 图片、MP3/WAV 音频等多种输入格式，自动执行 OCR/ASR + 翻译 + 格式重建。其接口定义见 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_language` | string | 是 | 源语言代码（如 `zh`, `en`, `ja`），部分模型支持 `auto` 自动检测 |
| `target_language` | string | 是 | 目标语言代码（如 `en`, `fr`, `ko`） |
| `input_type` | string | 否（仅 `qwen-mt-uni` 需显式指定） | 取值：`text` / `image` / `document` / `audio` |
| `preserve_format` | boolean | 否 | 默认 `false`；设为 `true` 时启用排版保真（仅 `qwen-mt-image` 和 `qwen-mt-uni` 支持） |
| `response_format` | string | 否 | 可选 `json`（含结构化字段）或 `text`（纯翻译结果） |

> **注意**：`qwen-mt` 模型不支持 `input_type` 和 `preserve_format` 参数；若在调用 `qwen-mt` 时传入这些参数，将被静默忽略——此行为与 [Qwen-MT API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 中的参数说明一致，但需开发者自行校验输入模型类型。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 或 DashScope `X-DashScope-Access-Token` 头；
2. **Endpoint**（以 `qwen-mt` 为例）：
   - OpenAI 兼容：`POST https://dashscope.aliyuncs.com/v1/chat/completions`
   - DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multilingual-translation/text`
3. **请求体示例（文本翻译）**：
   ```json
   {
     "model": "qwen-mt",
     "input": {"text": "你好，世界！"},
     "parameters": {
       "source_language": "zh",
       "target_language": "en"
     }
   }
   ```
   图片与文档类请求需按 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 规范上传 base64 或 OSS URL。

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 8192 字符，图片 ≤ 10 MB（PNG/JPG），音频 ≤ 60 秒；
- `qwen-mt-image` 和 `qwen-mt-uni` 对复杂 PDF 表格或手写体识别准确率受限，建议预处理为清晰扫描件；
- 所有模型暂不支持实时流式响应（`stream: true` 不生效），响应为完整 JSON；
- `qwen-mt-uni` 的 `audio` 输入仅支持普通话 ASR，其他语种音频将触发失败（错误码 `InvalidInput`），该限制未在 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确标注，实际行为以运行时为准。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


