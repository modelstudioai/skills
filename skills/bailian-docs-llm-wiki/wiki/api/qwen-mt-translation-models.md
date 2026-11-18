# qwen mt translation models

Qwen-MT 系列是百炼平台提供的专业翻译模型族，覆盖文本、图片及多模态输入场景，统一基于 Qwen 大语言模型底座优化，支持高保真语义与格式还原。所有模型均通过标准 API 提供服务，兼容 OpenAI 格式与 DashScope 原生接口。详细能力边界与调用规范请参阅 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 支持的模型/功能

- **Qwen-MT**：纯文本翻译，支持 100+ 语种对，可指定源/目标语言、保留术语一致性（如专有名词不译）、控制输出风格（正式/简洁/技术文档等）；详见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。  
- **Qwen-MT-Image**：输入为图像（PNG/JPEG/PDF 扫描件），自动识别图文并执行上下文感知翻译，保持原始排版结构（如表格、段落缩进、多栏布局）；[原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 明确要求图像分辨率不低于 300 DPI 以保障 OCR 准确率。  
- **Qwen-MT-Uni**：全模态统一接口，接受文本、PDF/DOCX 文档、图像、WAV/MP3 音频（需先转写为文本）混合输入，支持跨模态上下文对齐（例如翻译 PPT 中的图注与正文时保持术语统一）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_language` | string | 是 | ISO 639-1 代码（如 `"zh"`、`"en"`），`auto` 表示自动检测（仅 Qwen-MT 和 Qwen-MT-Uni 支持） |
| `target_language` | string | 是 | 目标语言代码（如 `"ja"`、`"fr"`） |
| `preserve_formatting` | boolean | 否 | 默认 `false`；设为 `true` 时启用排版保留（Qwen-MT-Image 和 Qwen-MT-Uni 强制启用） |
| `glossary` | object | 否 | 自定义术语表，格式为 `{ "source_term": "target_term" }`，仅 Qwen-MT 和 Qwen-MT-Uni 支持 |

> **注意**：原始文档中 `qwen-mt-api.md` 将 `glossary` 描述为“仅支持 JSON 字符串形式”，但 `qwen-mt-uni-api.md` 明确要求传入结构化对象。实际调用应以 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的对象格式为准，避免字符串解析失败。

## 使用方式

- **OpenAI 兼容模式**：设置 `model="qwen-mt"`，在 `messages` 中以 `{"role": "user", "content": "原文"}` 形式提交；图片和文档需先 base64 编码后作为 `content` 字段值，并显式声明 `type="image_url"` 或 `type="file"`。  
- **DashScope 原生模式**：使用 `/api/v1/services/aigc/text-generation/generation`（文本）、`/api/v1/services/aigc/image-generation/generation`（图片）等专用路径，请求体需包含 `input` 和 `parameters` 字段。完整字段映射见 [原文标题](../../raw/model-api-reference/qwen-mt-translation-models.md)。

## 限制和注意事项

- 单次请求最大 token 数：Qwen-MT 为 8192，Qwen-MT-Image 为 2048（OCR 后文本长度），Qwen-MT-Uni 为 4096（含所有模态内容总和）。  
- 图片翻译不支持手写体、低对比度或严重畸变图像；PDF 输入仅解析第一页（Qwen-MT-Image）或前 50 页（Qwen-MT-Uni）。  
- 音频输入在 Qwen-MT-Uni 中需预先完成语音转写（ASR），平台不内置 ASR 能力；若直接上传音频，将返回 `400 Unsupported media type`。

## 来源文档

- [翻译模型](../../raw/model-api-reference/qwen-mt-translation-models.md)


