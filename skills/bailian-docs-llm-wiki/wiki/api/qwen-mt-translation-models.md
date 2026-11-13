# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、音频及多格式文档等全模态输入场景。其核心模型包括面向纯文本的 `qwen-mt-plus`、专注图像翻译的 `qwen-mt-image-*` 系列，以及统一处理多模态输入的 `qwen-mt-uni`。所有模型均支持术语干预、领域提示、翻译记忆等高级功能，并提供 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)与 DashScope 原生协议两种调用方式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，通过 OpenAI 兼容 `/chat/completions` 接口调用，支持 `source_lang`/`target_lang` 指定、术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，同时保留原始排版。`qwen-mt-image-2.0` 支持全部 55 种语言互译；`qwen-mt-image` 仅支持中/英文作为源或目标语种之一。二者均支持敏感词过滤（`sensitives`）、术语干预（`terminologies`）和图像主体分割（`imageSegment`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串或数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等多种输入格式，并自动重构为对应格式的译后结果。同步/异步双模式，统一使用 `/api/v1/services/aigc/multimodal-generation/generation` 接口。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 参数在示例代码末尾被截断（“profe…”），且未说明其值是否必须为英文；而文档 2 和文档 3 明确要求领域提示（`domainHint`）**只支持英文**。实践中应统一使用完整、合规的英文描述，避免依赖截断参数。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 | 备注 |
|--------|------|------|----------|------|
| `source_lang` / `target_lang` | `string` | 源/目标语种，支持全称（如 `"Chinese"`）、编码（如 `"zh"`）或 `"auto"` | 全部 | `qwen-mt-image` 要求至少一端为中/英文；`qwen-mt-uni` 和 `qwen-mt-plus` 无此限制 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预列表 | `qwen-mt-plus` / `qwen-mt-image-*` / `qwen-mt-uni` | 字段名不同但语义一致；`qwen-mt-plus` 使用 `terms`，`qwen-mt-image` 使用 `terminologies`，`qwen-mt-uni` 使用 `glossary` |
| `tm_list` | `array` | 翻译记忆（历史句对） | `qwen-mt-plus` | 仅该模型支持 |
| `domainHint` | `string` | 英文领域提示（≤200 单词） | `qwen-mt-image-*`, `qwen-mt-uni` | **必须为英文**；`qwen-mt-plus` 的 `domains` 字段行为不明确，建议避免使用 |
| `sensitives` | `array<string>` | 敏感词列表（完全匹配、大小写敏感） | `qwen-mt-image-*`, `qwen-mt-uni` | `qwen-mt-plus` 不支持 |
| `imageSegment` | `boolean` | 是否跳过图像主体（人物/Logo/商品）上的文字翻译 | `qwen-mt-image-*`, `qwen-mt-uni` | 默认 `false`；旧版 `skipImgSegment` 已弃用，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 OpenAI SDK，`base_url` 指向业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），通过 `extra_body={"translation_options": {...}}` 传参。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供了 Python/Node.js/curl 完整示例。
- **图像翻译（`qwen-mt-image-*`）**：调用 DashScope 原生接口 `POST /api/v1/services/aigc/image2image/image-synthesis`，需在 `input` 对象中指定 `image_url`、`source_lang`、`target_lang`，并在 `ext` 中配置扩展功能。
- **全模态翻译（`qwen-mt-uni`）**：调用 DashScope 原生接口 `POST /api/v1/services/aigc/multimodal-generation/generation`，通过 `input.fileUrl`（文件 URL）或 `input.source_texts`（文本）指定输入，`target_lang` 必填。
- **同步 vs 异步**：
  - 同步：直接返回结果（文本内容或文件 URL），适用于文本、小图、短音频等低延迟场景。
  - 异步：请求头添加 `X-DashScope-Async: enable`，先获 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果。`qwen-mt-image` **必须异步**；`qwen-mt-uni` 和 `qwen-mt-image-2.0` 支持两者。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。旧域名仍可用，但性能与稳定性较低（见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)）。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB。
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟。
  - URL：不得含中文字符。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms`、`qwen-mt-image` 的 `terminologies`、`qwen-mt-uni` 的 `glossary` 均最多支持 100 组；`sensitives` 最多 50 个。
- **领域提示**：`domainHint`（`qwen-mt-image-*`, `qwen-mt-uni`）和 `domains`（`qwen-mt-plus`）均要求英文，且长度不宜过长；实测显示非英文提示可能导致解析失败或忽略。
- **错误处理**：`qwen-mt-plus`（OpenAI 兼容）返回标准 OpenAI 错误结构；`qwen-mt-image-*` 和 `qwen-mt-uni`（DashScope 原生）采用 `code`/`message` 或 `output.Code`/`output.Message` 结构，需按协议分别解析。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


