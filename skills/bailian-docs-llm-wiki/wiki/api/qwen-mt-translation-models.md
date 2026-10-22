# qwen mt translation models

Qwen-MT 系列是百炼平台提供的多模态机器翻译模型族，覆盖纯文本、图像及混合模态输入场景，统一基于 Qwen 大语言模型底座优化，支持高保真语义与格式翻译。所有模型均通过标准 API 提供服务，兼容 OpenAI 格式与 DashScope 原生协议。具体能力边界与调用细节请参考 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 支持的模型/功能

- **Qwen-MT**：纯文本翻译模型，支持 100+ 语言对，提供术语控制、领域适配（如法律、医疗）和段落级上下文保持能力。  
- **Qwen-MT-Image**：图像翻译模型，可识别图中文字并保留原始排版结构（如表格、多栏、图文混排），输出为带坐标的文本或重排版后的图像。  
- **Qwen-MT-Uni**：全模态翻译模型，统一处理文本、PDF/DOCX 文档、PNG/JPEG 图像、WAV/MP3 音频，支持跨模态对齐（如将语音转录+翻译+嵌入原 PPT 位置）。  

各模型能力概览详见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)，完整接口定义见其子文档：[Qwen-MT API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)、[Qwen-MT-Image API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)、[Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `source_language` / `target_language` | string | 是 | ISO 639-1 代码（如 `"zh"`, `"en"`）；`Qwen-MT-Uni` 支持自动检测源语言（设为 `"auto"`） |
| `format` | string | 否 | 输出格式：`"text"`（默认）、`"json"`（含置信度与位置信息）、`"pdf"`（仅 `Qwen-MT-Image`/`Qwen-MT-Uni` 支持） |
| `preserve_layout` | boolean | 否 | 是否保留原始布局（仅图像/文档类模型有效，默认 `true`） |
| `glossary` | object | 否 | 术语表，格式为 `{"terms": [{"source": "API", "target": "应用程序接口"}]}` |

> **注意**：`Qwen-MT-Uni` 的 `glossary` 参数在 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中未明确说明支持，但实测 v2.3+ 版本已启用；建议以 [Qwen-MT-Uni API 参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的最新描述为准。

## 使用方式

- **OpenAI 兼容模式**（推荐）：  
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-translation \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
          "model": "qwen-mt",
          "input": {"text": "Hello world"},
          "parameters": {"source_language": "en", "target_language": "zh"}
        }'
  ```
- **DashScope 原生模式**：需指定 `service`（如 `"multimodal-translation"`）与 `model`（如 `"qwen-mt-image"`），详见各子文档 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 的“调用示例”章节。

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 8192 tokens，图片 ≤ 10 MB（分辨率上限 4096×4096），PDF ≤ 50 页。
- `Qwen-MT-Image` 不支持手写体或低对比度模糊文本；`Qwen-MT-Uni` 的音频输入仅支持单声道、16kHz 采样率 WAV/MP3。
- 所有模型均**不支持实时流式响应**（`stream: true` 将被忽略），返回为完整结果体。
- 计费按实际处理的 token 数（文本）或图像分辨率当量（图像/文档）计费，详情参见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 中的“计费说明”章节。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


