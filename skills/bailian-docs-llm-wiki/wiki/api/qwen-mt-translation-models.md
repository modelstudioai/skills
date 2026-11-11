# qwen mt translation models

Qwen MT 系列是百炼平台提供的多模态翻译模型家族，专为高精度、低延迟的跨语言内容转换设计，覆盖纯文本、图像及混合模态输入场景。模型基于 Qwen 大语言模型底座优化，支持端到端语义对齐与格式保真。所有模型均通过统一 API 网关接入，兼容 OpenAI 格式与 DashScope 原生协议。

## 支持的模型与功能

- **`qwen-mt`**：纯文本翻译模型，支持 100+ 语言对，适用于 API 调用、批量文本处理等场景。详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。
- **`qwen-mt-image`**：图片翻译模型，可识别图中文字并保持原始排版结构（如表格、多栏、图文混排），输出带坐标信息的翻译结果。
- **`qwen-mt-uni`**：全模态翻译模型，支持文本、PDF/DOCX 文档、PNG/JPEG 图片、WAV/MP3 音频输入，自动执行 OCR/ASR + 翻译 + 格式重建流程。

> **注意**：`qwen-mt-uni` 当前对 PDF 的页数限制为 ≤50 页，而 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中未明确说明该限制，实际调用需以最新 API 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_language` | string | 是 | 源语言代码（如 `zh`, `en`, `ja`），支持 ISO 639-1 标准；`auto` 表示自动检测（仅 `qwen-mt` 和 `qwen-mt-uni` 支持） |
| `target_language` | string | 是 | 目标语言代码（同上） |
| `input_type` | string | 否 | 仅 `qwen-mt-uni` 需指定，取值 `text`/`image`/`document`/`audio`；默认 `text` |
| `preserve_format` | boolean | 否 | 默认 `false`；设为 `true` 时启用排版保真（对 `qwen-mt-image` 和 `qwen-mt-uni` 生效） |

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 或 DashScope SDK 初始化；
2. **请求体**（以 `qwen-mt` 为例）：
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
3. **调用入口**：
   - OpenAI 兼容路径：`POST /v1/chat/completions`（需在 `model` 字段指定模型名）；
   - DashScope 原生路径：`POST /api/v1/services/aigc/mt/text`（对应 `qwen-mt`）；
   - 更多接口细节请参考 [Qwen-MT API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。

## 限制和注意事项

- 单次请求 `input.text` 长度上限为 8192 Unicode 字符（`qwen-mt`）；图片尺寸建议 ≤4096×4096 像素（`qwen-mt-image`）；
- `qwen-mt-uni` 对音频时长限制为 ≤120 秒，超时将截断处理；
- 所有模型均不支持实时流式响应（`stream: true` 无效），响应为完整 JSON 结构；
- 输入含敏感词或违法内容时，请求将被拒绝并返回 `400 Bad Request`，错误码 `InvalidInput` —— 此行为与 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 描述一致，但具体过滤规则以服务端最新策略为准。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


