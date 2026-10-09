# qwen mt translation models

Qwen MT 翻译模型系列是百炼平台提供的多模态、高保真机器翻译能力，覆盖文本、图像、文档、音频等多种输入形式。该系列包含面向纯文本的 `qwen-mt-plus`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）、面向全模态统一处理的 `qwen-mt-uni`，以及专注图像翻译优化的 `qwen-mt-image` 和 `qwen-mt-image-2.0`。所有模型均支持术语干预、敏感词过滤、领域提示等企业级定制功能，并提供同步与异步两种调用模式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持翻译记忆（TM）、术语表（`terms`）、领域提示（`domains`）和自动语言检测（`source_lang: "auto"`）。适用于 API 集成度高、已有 OpenAI SDK 生态的场景。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（`source_texts`）、图片、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、MP3/WAV 音频等输入格式，自动识别模态并执行端到端翻译与格式重构。输出保持原始格式（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`）。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：专为图像翻译优化的模型，精准识别图文混排内容并还原排版。`qwen-mt-image-2.0` 支持全部 55 种语种间的任意互译；`qwen-mt-image` 仅支持源或目标语种至少有一项为中文或英文的组合。二者均支持图像主体分割（`imageSegment`）以跳过 Logo/商品/人脸等区域文字。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。

> **注意**：文档 1 中称 `qwen-mt-image` “不支持在非中/英语种之间直接翻译（例如，从日语翻译为韩语）”，而文档 2 对 `qwen-mt-uni` 的图像能力未作语种限制说明；但文档 2 明确其图像处理逻辑复用 `qwen-mt-image-2.0` 能力。因此，若需跨小语种图像翻译，请务必使用 `qwen-mt-image-2.0` 或 `qwen-mt-uni`（后者底层调用 `qwen-mt-image-2.0` 处理图像），避免误用旧版 `qwen-mt-image`。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 |
|--------|------|----------|------|
| `model` | `string` | 是 | 模型名称：`qwen-mt-plus`、`qwen-mt-uni`、`qwen-mt-image` 或 `qwen-mt-image-2.0` |
| `source_lang` | `string` | 条件必选 | 源语言代码（如 `zh`）或全称（如 `Chinese`）；可设为 `"auto"`（仅 `qwen-mt-plus` 和 `qwen-mt-uni` 支持）；`qwen-mt-image` 要求与 `target_lang` 不同且至少一方为 `zh`/`en` |
| `target_lang` | `string` | 是 | 目标语言代码或全称（如 `en`, `Japanese`） |
| `ext.domainHint` | `string` | 否 | 英文领域提示（≤200 单词），用于引导译文风格。**所有模型均仅支持英文**。 |
| `ext.sensitives` | `string[]` | 否 | 敏感词数组，完全匹配且**大小写敏感**，最多 50 个。 |
| `ext.terminologies`（`qwen-mt-image*`）<br>`ext.glossary`（`qwen-mt-uni`）<br>`translation_options.terms`（`qwen-mt-plus`） | `object[]` | 否 | 术语干预：`{"src"/"source": "...", "tgt"/"target": "..."}`。`qwen-mt-uni` 最多支持 100 组；其余模型建议 ≤50 组。 |
| `ext.config.imageSegment` | `boolean` | 否 | **仅对图像输入生效**：`true` 跳过人物/商品/Logo 等主体区域文字翻译（默认 `false`）。旧参数 `skipImgSegment` 已废弃，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。 |

## 使用方式

- **同步调用**（适合文本、小图、短音频）：
  - `qwen-mt-plus`：调用 `/compatible-mode/v1/chat/completions`，在 `extra_body.translation_options` 或顶层 `translation_options` 中传参。
  - `qwen-mt-uni` / `qwen-mt-image*`：调用 `/api/v1/services/aigc/multimodal-generation/generation` 或 `/api/v1/services/aigc/image2image/image-synthesis`，`input` 对象内传参。
  - 响应直接返回结果（`output.Data.TranslatedTexts` 或 `output.image_url`），无需轮询。

- **异步调用**（适合大文档、长音频、高并发）：
  - 所有模型均需在请求头添加 `X-DashScope-Async: enable`。
  - 第一步：发送请求获取 `task_id`（有效期 24 小时）。
  - 第二步：轮询 `GET /api/v1/tasks/{task_id}` 获取最终结果（`TranslatedFileUrl` 或 `TranslatedTexts`）。
  - 注意：`qwen-mt-image` **必须**使用异步模式；`qwen-mt-image-2.0` 和 `qwen-mt-uni` 同步/异步均可。

- **输入格式约束**：
  - 图像：JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，宽高 15–8192 px，宽高比 1:10 至 10:1，≤100 MB。
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频 3 秒–60 分钟。
  - URL 中**禁止含中文字符**；本地文件需先上传获取公网临时 URL（见 [上传文件获取临时URL](../../raw/model-api-reference/more-about-models/get-temporary-file-url.md)）。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），性能与稳定性优于旧版 `dashscope.aliyuncs.com`。华北2（北京）、新加坡、中国香港已全面支持。
- **认证**：所有请求均需 `Authorization: Bearer <DASHSCOPE_API_KEY>`，API Key 需提前[获取与配置](../../raw/model-api-reference/preparations/get-api-key.md)。
- **计费**：`qwen-mt-uni` 按 `input_tokens` 计费（含 `image_tokens`/`document_tokens` 等明细）；`qwen-mt-plus` 和 `qwen-mt-image*` 按请求次数或图像数计费，具体见控制台定价页。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 字段与 `qwen-mt-uni` 的 `glossary` 功能等效，但字段名和嵌套层级不同；`qwen-mt-image*` 使用 `terminologies`。三者均要求 `src`/`source` 与 `source_lang` 一致，`tgt`/`target` 与 `target_lang` 一致。
- **错误处理**：同步调用失败时顶层返回 `code`/`message`；异步调用需检查 `output.task_status === "SUCCEEDED"` 后再读取 `output.Success` 判断业务成败（见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)）。

## 来源文档

- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)


