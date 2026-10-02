# qwen mt translation models

Qwen-MT 系列是百炼平台提供的专业翻译模型族，覆盖纯文本、图片及多模态输入场景，统一基于 Qwen 大模型底座优化，支持高保真语义与格式还原。所有模型均通过标准 API 提供服务，兼容 OpenAI 格式与 DashScope 原生协议。开发者需根据输入类型选择对应模型，避免混用接口。

## 支持的模型与功能

- **Qwen-MT**：纯文本翻译，支持 100+ 语言对，提供术语控制、风格适配（如正式/口语）等高级能力。详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。
- **Qwen-MT-Image**：图片翻译，自动识别图文结构（如表格、分栏、标题），保持原文排版输出译文图像。其能力边界与图像预处理逻辑在 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中有明确说明。
- **Qwen-MT-Uni**：全模态翻译，支持文本、PDF/DOCX 文档、JPG/PNG 图片、MP3/WAV 音频输入，输出对应格式译文。该模型的输入格式约束和 MIME 类型要求详见 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 关键参数

- `source_language` / `target_language`：必填，ISO 639-1 代码（如 `"zh"`, `"en"`），不支持自动检测；Qwen-MT-Uni 的音频转译需额外指定 `source_language`（语音识别阶段使用）。
- `preserve_formatting`：布尔值，默认 `true`，仅 Qwen-MT-Image 和 Qwen-MT-Uni 支持；设为 `false` 时返回纯文本译文（丢失布局信息）。
- `glossary`：JSON 数组，用于术语强制替换，格式为 `[{"source": "API", "target": "应用程序接口"}]`；Qwen-MT 与 Qwen-MT-Uni 支持，Qwen-MT-Image **不支持**术语表。

## 使用方式

- 所有模型均通过 `/v1/services/translation` 路径调用，具体 endpoint 因模型而异：
  - Qwen-MT：`POST https://dashscope.aliyuncs.com/api/v1/services/translation/qwen-mt`
  - Qwen-MT-Image：`POST https://dashscope.aliyuncs.com/api/v1/services/translation/qwen-mt-image`
  - Qwen-MT-Uni：`POST https://dashscope.aliyuncs.com/api/v1/services/translation/qwen-mt-uni`
- 请求体为 JSON，需包含 `input` 字段（字符串、base64 编码图像或文件 URL），并显式声明 `model`（如 `"qwen-mt"`）以兼容 OpenAI 兼容模式。
- 认证方式统一使用 `Authorization: Bearer <api_key>`，无需额外签名。

## 限制和注意事项

- 单次请求最大输入长度：Qwen-MT 为 8192 tokens；Qwen-MT-Image 为单图 ≤ 10 MB；Qwen-MT-Uni 的 PDF 文档 ≤ 50 页且总大小 ≤ 20 MB。
- Qwen-MT-Uni 对音频输入仅支持采样率 16kHz、单声道、PCM/WAV/MP3 格式；若传入双声道 MP3，将静默降为单声道处理，**不报错也不警告**。
- > **注意**：原始文档中提及 Qwen-MT-Uni “支持视频输入”，但当前 API 实际拒绝 `.mp4` 或 `.avi` 文件并返回 `400 Unsupported media type`。该描述已过时，应以 [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md) 中最新接口规范为准。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


