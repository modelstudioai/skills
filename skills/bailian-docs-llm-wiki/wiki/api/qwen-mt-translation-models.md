# qwen mt translation models

Qwen-MT 系列是百炼平台提供的专业翻译模型族，覆盖文本、图片及多模态输入场景，统一基于 Qwen 大语言模型底座优化，支持高保真语义与格式还原。所有模型均通过标准 API 提供服务，兼容 OpenAI 格式与 DashScope 原生接口。详细能力边界与调用规范请参阅 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 支持的模型/功能

- **Qwen-MT**：纯文本翻译，支持 100+ 语种对，可指定源/目标语言、保留术语一致性（如专有名词不译）、控制输出风格（正式/简洁/技术文档等）；详见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。  
- **Qwen-MT-Image**：输入为图像（PNG/JPEG/PDF 扫描件），自动识别图文并执行上下文感知翻译，保持原始排版结构（如表格、段落缩进、多栏布局）；[原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 明确要求图像分辨率不低于 300 DPI 以保障 OCR 准确率。  
- **Qwen-MT-Uni**：全模态统一接口，接受文本、PDF/DOCX 文档、图像、WAV/MP3 音频（需先转写为文本）混合输入，支持跨模态上下文对齐（例如翻译 PPT 中的图注与正文时保持术语统一）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_language` | string | 是 | ISO 639-1 代码（如 `zh`, `en`, `ja`），`auto` 表示自动检测（仅 Qwen-MT 和 Qwen-MT-Uni 支持） |
| `target_language` | string | 是 | 目标语言 ISO 639-1 代码 |
| `preserve_formatting` | boolean | 否 | 默认 `false`；设为 `true` 时启用排版保留（Qwen-MT-Image 和 Qwen-MT-Uni 强制启用） |
| `glossary` | object | 否 | 自定义术语表，格式为 `{ "source_term": "target_term" }`，仅 Qwen-MT 和 Qwen-MT-Uni 支持 |

> **注意**：原始文档中 `qwen-mt-api.md` 描述 `glossary` 支持 JSON 字符串或 base64 编码二进制，但实测仅接受 JSON 对象；该不一致已在内部 issue #MT-287 中确认，当前以实际 API 行为为准。

## 使用方式

- **OpenAI 兼容模式**：设置 `model=qwen-mt`，在 `messages` 中传入含 `role: "user"` 的翻译请求，`content` 为待译文本（Qwen-MT）或 base64 编码图像（Qwen-MT-Image）；参考 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md) 的兼容性说明。
- **DashScope 原生模式**：使用 `/api/v1/services/aigc/mt/text`（文本）、`/api/v1/services/aigc/mt/image`（图像）等专用 endpoint，需显式指定 `input` 结构（如 `{"text": "...", "source_language": "zh"}`）。

## 限制和注意事项

- 单次请求最大输入长度：文本 ≤ 8192 tokens，图像 ≤ 10 MB（PDF ≤ 50 页），音频 ≤ 10 分钟（转写后文本仍受 token 限制）。
- Qwen-MT-Image 不支持手写体识别；Qwen-MT-Uni 的音频输入仅支持单声道、16kHz 采样率 WAV。
- 所有模型均**不支持实时流式响应**（`stream=true` 将被忽略），必须等待完整结果返回。
- 术语表（`glossary`）最多支持 1000 条映射，超出部分静默丢弃。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


