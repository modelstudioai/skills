# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业化机器翻译能力，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。

## 支持的模型与功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中/英/日/韩/法/西等主流语种互译，提供 `translation_options` 扩展参数（含 `source_lang`/`target_lang`/`terms`/`tm_list`/`domains`），适用于高精度、强可控的文本翻译场景。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版与视觉结构；`qwen-mt-image-2.0` 支持全部 55 种语言互译，而 `qwen-mt-image` 仅支持源或目标语言至少一方为中文或英文。两者均支持 `imageSegment` 主体分割控制。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等输入格式，自动识别模态并执行端到端翻译与格式重构。同步调用返回 `TranslatedTexts` 或 `TranslatedFileUrl`，[异步调用](../concepts/asynchronous-invocation.md)需轮询任务状态。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 2 中 `qwen-mt-image` 的语种限制（“不支持非中/英语种间直译”）与文档 3 中 `qwen-mt-uni` 对图像输入的语种支持描述存在隐含冲突——`qwen-mt-uni` 在图像模式下实际复用 `qwen-mt-image-2.0` 引擎，因此其图像翻译能力应等同于 `qwen-mt-image-2.0`，即无语种互译限制。建议以 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 的能力为准。

## 关键参数

| 参数名 | 类型 | 说明 | 是否必选 | 备注 |
|--------|------|------|----------|------|
| `model` | `string` | 模型名称，如 `"qwen-mt-plus"`、`"qwen-mt-image-2.0"`、`"qwen-mt-uni"` | 是 | — |
| `source_lang` | `string` | 源语言（全称或 ISO 639-1 编码），如 `"Chinese"`、`"zh"`、`"auto"` | 文本/图像/文档调用中为**条件必选**（`qwen-mt-plus` 必填；`qwen-mt-uni` 可选，不填则自动识别） | `qwen-mt-plus` 不支持 `"auto"`；`qwen-mt-image` 和 `qwen-mt-uni` 支持 `"auto"` |
| `target_lang` | `string` | 目标语言（全称或编码），如 `"English"`、`"en"` | 是 | — |
| `translation_options`（仅 `qwen-mt-plus`） | `object` | 包含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` | 否（但 `source_lang`/`target_lang` 必须在其中） | `domains` 字段在文档 1 示例末尾被截断，完整值应为英文描述，且长度建议 ≤200 单词 |
| `input.fileUrl` / `input.source_texts`（仅 `qwen-mt-uni`） | `string` / `array<string>` | 文件公网 URL 或待翻译文本（二者**必须且只能提供一个**） | 条件必选 | `fileUrl` 需为 HTTP(S) 地址，不含中文字符；单文件 ≤100 MB，文档 ≤200 页，音频 3s–60min |
| `ext.terminologies` / `ext.glossary` | `array` | 术语干预：`qwen-mt-image` 使用 `terminologies`（字段 `src`/`tgt`），`qwen-mt-uni` 使用 `glossary`（字段 `src`/`tgt`），`qwen-mt-plus` 使用 `terms`（字段 `source`/`target`） | 否 | 三者语义一致，仅字段名不同；`qwen-mt-uni` 最多支持 100 组，其余模型建议 ≤50 组 |
| `ext.domainHint` | `string` | 领域提示，**仅支持英文**，建议 ≤200 单词 | 否 | 三者均支持，用于引导译文风格（如 `"IT documentation"`、`"e-commerce customer service"`） |
| `ext.sensitives` | `array<string>` | 敏感词列表，**完全匹配、大小写敏感**，最多 50 个 | 否 | 三者均支持，匹配后原文保留，不送入模型 |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，`POST /compatible-mode/v1/chat/completions`，通过 `extra_body.translation_options` 传参（Python SDK）或顶层 `translation_options` 字段（Node.js/curl）。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供了完整的 Python/Node.js/curl 示例。
- **图像翻译（`qwen-mt-image-*`）**：调用 `POST /api/v1/services/aigc/image2image/image-synthesis`，请求头需设 `Content-Type: application/json` 和 `Authorization: Bearer <API_KEY>`；同步模式直接返回 `output.image_url`，异步模式需加 `X-DashScope-Async: enable` 并轮询 `/api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `POST /api/v1/services/aigc/multimodal-generation/generation`，同步模式返回 `output.Data.TranslatedFileUrl` 或 `output.Data.TranslatedTexts`；异步模式同样需加 `X-DashScope-Async: enable`，再通过 `GET /api/v1/tasks/{task_id}` 查询结果。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确区分了同步/异步响应结构与错误处理逻辑。
- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。`{WorkspaceId}` 可在百炼控制台「业务空间详情」中获取。

## 限制和注意事项

- **API Key 隔离**：北京、新加坡、美国（弗吉尼亚）地域的 API Key **不通用**，需分别申请与配置（见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)）。
- **图像格式限制**：`qwen-mt-image` 和 `qwen-mt-uni`（图像输入）均要求图像宽高在 15–8192 像素、宽高比 1:10 至 10:1、大小 ≤100 MB；URL 不得含中文字符；支持 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP。
- **领域提示语言限制**：`domainHint` 在所有模型中**仅支持英文输入**，非英文提示将导致效果下降或报错。
- **参数命名差异**：图像主体分割开关在 `qwen-mt-image` 中为 `imageSegment`（新）或 `skipImgSegment`（旧兼容），而在 `qwen-mt-uni` 中为 `config.imageSegment`；术语表字段名分别为 `terminologies`（图像）、`glossary`（全模态）、`terms`（文本），开发者需按模型严格匹配。
- **异步任务生命周期**：`task_id` 有效期为 24 小时；异步返回的 `TranslatedFileUrl` 同样有效期为 24 小时，需及时下载保存。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


