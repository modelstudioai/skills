# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。开发者可根据输入类型、延迟要求和文件规模选择最适配的模型。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options` 参数控制源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片中的文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持 55 种语言互译，而 `qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文。两者均支持术语干预（`terminologies`）、敏感词过滤（`sensitives`）和图像主体分割（`imageSegment`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等多种输入格式，自动识别模态并执行高保真翻译与格式重构。其 `ext.glossary` 支持最多 100 组术语映射，`ext.sensitives` 支持最多 50 个敏感词。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例被截断（末尾为 `"profe"`），且未说明该字段是否生效；而文档 2 和文档 3 明确要求领域提示（`domainHint`）**必须为英文且不超过 200 单词**。实际开发中应以 `domainHint`（英文）为准，避免使用 `domains` 字段。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 | 备注 |
|--------|------|------|----------|------|
| `source_lang` / `target_lang` | `string` | 源/目标语言，支持语种全称（如 `"Chinese"`）、ISO 编码（如 `"zh"`）或 `"auto"`（仅部分模型支持） | 全部 | `qwen-mt-image` 要求源/目标至少一方为中/英文；`qwen-mt-uni` 和 `qwen-mt-image-2.0` 无此限制 |
| `translation_options` | `object` | 文本模型专用参数对象，含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` | `qwen-mt-plus` | 必须通过 `extra_body` 传入 OpenAI SDK；`curl` 中直接作为顶层字段 |
| `terminologies` / `glossary` | `array` | 术语干预列表，每项为 `{ "src": "...", "tgt": "..." }` | `qwen-mt-image*` 使用 `terminologies`；`qwen-mt-uni` 使用 `glossary` | `qwen-mt-plus` 使用 `terms`；三者语义一致但字段名不同 |
| `sensitives` | `array<string>` | 敏感词列表，**完全匹配且大小写敏感**，匹配后原文保留不翻译 | `qwen-mt-image*`, `qwen-mt-uni` | `qwen-mt-plus` 未提及该能力 |
| `domainHint` | `string` | **仅支持英文**，用于引导译文风格（如电商客服、技术文档），建议 ≤200 单词 | `qwen-mt-image*`, `qwen-mt-uni` | `qwen-mt-plus` 的 `domains` 字段已弃用或不生效，应统一使用 `domainHint` |
| `imageSegment` | `boolean` | 是否跳过图像中人物/商品/Logo 等主体区域的文字翻译 | `qwen-mt-image*`, `qwen-mt-uni`（仅对图像生效） | 旧版 `skipImgSegment` 仍兼容，但推荐使用 `imageSegment` |

## 使用方式

- **地域与 endpoint**：所有模型均支持华北2（北京）、新加坡、美国（弗吉尼亚）地域，需使用业务空间专属域名：`https://{WorkspaceId}.{region}.maas.aliyuncs.com`（如 `cn-beijing`）。旧域名（`dashscope.aliyuncs.com`）仍可用，但[官方推荐迁移](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)以获得更高稳定性。
- **认证**：需配置 `DASHSCOPE_API_KEY` 环境变量或显式传入，通过 `Authorization: Bearer <key>` 认证。
- **调用模式**：
  - **同步调用**：适用于文本、小图、短音频等低延迟场景，请求后直接返回结果（`qwen-mt-plus` 和 `qwen-mt-uni` 的文本/图像输入默认同步；`qwen-mt-image` 必须显式启用异步）。
  - **异步调用**：适用于大文档、长音频等耗时操作，需在请求头添加 `X-DashScope-Async: enable` 获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询结果。`qwen-mt-uni` 和 `qwen-mt-image` 均支持异步。
- **输入格式适配**：
  - `qwen-mt-plus`：仅支持 `messages` 数组（`role: "user", content: string`），通过 `translation_options` 控制翻译行为。
  - `qwen-mt-image*`：使用 `/api/v1/services/aigc/image2image/image-synthesis` 接口，`input.image_url` 为必填。
  - `qwen-mt-uni`：使用 `/api/v1/services/aigc/multimodal-generation/generation` 接口，`input.fileUrl` 或 `input.source_texts` **二选一**。

## 限制和注意事项

- **语言识别**：`source_lang="auto"` 仅在 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 中稳定支持；`qwen-mt-plus` 和 `qwen-mt-image` 的自动检测能力有限，生产环境建议显式指定。
- **文件限制**：`qwen-mt-image*` 仅支持 JPG 格式（文档 2 明确限定），而 `qwen-mt-uni` 支持 JPG/PNG/MP3/WAV 等十余种格式，且单文件 ≤100 MB、文档 ≤200 页、音频 3 秒–60 分钟（见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)）。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 和 `tm_list` 为 JSON 数组，嵌套在 `translation_options` 内；`qwen-mt-image*` 的 `terminologies` 和 `qwen-mt-uni` 的 `glossary` 则位于 `ext` 对象下，结构相同但路径不同。
- **领域提示一致性**：所有模型的领域提示字段（`domainHint`）均**强制要求英文**，且长度建议 ≤200 单词。文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例为中文且被截断，属于过时或错误信息，应忽略。
- **错误处理**：同步调用失败时，响应顶层含 `code`/`message`；异步调用创建任务失败同理，但任务执行失败需检查 `output.Success === false` 及 `output.Code`/`output.Message`（见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)）。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


