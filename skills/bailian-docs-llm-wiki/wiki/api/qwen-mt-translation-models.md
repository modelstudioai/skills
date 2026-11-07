# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，适用于本地化、技术文档、电商客服、内容出海等高要求翻译任务。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 是文本翻译的核心接口文档。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英日韩法西等主流语种互译，提供 `translation_options`（含 `source_lang`/`target_lang`/`terms`/`tm_list`/`domains`）扩展参数，适用于 API 集成与批量文本处理。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片中的文字，保留原始排版与视觉结构；`qwen-mt-image-2.0` 支持全部 55 种语言互译，而 `qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文（详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)）。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等十余种格式输入，自动识别模态并执行端到端高保真翻译与格式重构，是多格式本地化流水线的首选方案。

> **注意**：文档 2 中 `qwen-mt-image` 的语种限制（“不支持在非中/英语种之间直接翻译”）与文档 3 中 `qwen-mt-uni` 对图像输入的无限制描述存在功能覆盖差异——`qwen-mt-uni` 在图像模式下实际复用 `qwen-mt-image-2.0` 引擎，因此其图像翻译能力等同于 `qwen-mt-image-2.0`，即支持任意 55 种语言互译。该矛盾源于文档粒度不同，应以 `qwen-mt-uni` 的实际能力为准。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 |
|--------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语种，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（仅 `source_lang`）；`qwen-mt-plus` 和 `qwen-mt-uni` 支持全部语种，`qwen-mt-image` 有语种约束 | 全部 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预：`qwen-mt-plus` 使用 `terms`（对象数组，含 `source`/`target` 字段）；`qwen-mt-image` 使用 `terminologies`（含 `src`/`tgt`）；`qwen-mt-uni` 使用 `glossary`（含 `src`/`tgt`），最多 100 组 | 全部 |
| `tm_list` | `array` | 翻译记忆（仅 `qwen-mt-plus`），提供历史句对提升一致性 | `qwen-mt-plus` |
| `domainHint` | `string` | 领域提示，**必须为英文**，建议 ≤200 单词，用于引导译文风格（如技术文档、电商客服） | 全部 |
| `sensitives` | `array` | 敏感词列表，**大小写敏感**，完全匹配时跳过翻译并保留原文；单次请求 ≤50 项 | `qwen-mt-image`, `qwen-mt-uni` |
| `imageSegment` | `bool` | 图像主体分割开关（默认 `false`），开启后跳过人物、商品、Logo 等主体区域文字翻译；旧参数 `skipImgSegment` 已废弃但兼容 | `qwen-mt-image`, `qwen-mt-uni` |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，`POST /compatible-mode/v1/chat/completions`，通过 `extra_body.translation_options` 传参（Python）或顶层字段 `translation_options`（Node.js/curl）。需配置地域专属 `base_url`（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供完整示例。
- **图像翻译（`qwen-mt-image-*`）**：调用 `/api/v1/services/aigc/image2image/image-synthesis`，同步模式直接返回 `output.image_url`；异步模式需添加请求头 `X-DashScope-Async: enable` 并轮询 `GET /api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `/api/v1/services/aigc/multimodal-generation/generation`，支持同步/异步双模式。输入可为 `fileUrl`（文档/图像/音频 URL）或 `source_texts`（字符串或数组），输出结构化返回 `TranslatedFileUrl` 或 `TranslatedTexts`。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 定义了完整的响应 schema。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧 DashScope 域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。
- **文件与内容限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟；
  - URL 中禁止含中文字符。
- **领域提示与术语**：`domainHint` 严格限定为英文；`glossary` 和 `terminologies` 中的 `src`/`tgt` 必须与 `source_lang`/`target_lang` 语种一致，否则被忽略。
- **异步任务生命周期**：`task_id` 有效期 24 小时；异步返回的 `TranslatedFileUrl` 有效期也为 24 小时，需及时下载。
- **错误处理**：同步调用失败时顶层返回 `code`/`message`；`qwen-mt-uni` 同步成功时 `output.Success` 为 `true`，失败时 `output.Success` 为 `false`（即使 `task_status` 为 `SUCCEEDED`）；务必检查 `output.Success` 而非仅 `task_status`。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


