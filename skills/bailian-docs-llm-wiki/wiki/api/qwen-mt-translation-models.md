# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力，覆盖文本、图像、文档、音频等[多模态](../concepts/multi-modal.md)输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中、英、日、韩、法、西等 55+ 语种互译，适用于高精度、低延迟的文本翻译场景。支持术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图像内文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持全部 55+ 语种直译（如日→韩），而 `qwen-mt-image` 仅支持源/目标语种至少一方为中/英文的组合。两者均支持图像主体分割（`imageSegment`）、敏感词过滤（`sensitives`）和术语干预（`terminologies`）。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串或数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等多种输入格式，自动识别模态并执行端到端高保真翻译与格式重构。该模型是 `qwen-mt-plus` 和 `qwen-mt-image` 的超集，推荐新项目优先选用。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 2 中称 `qwen-mt-image` “不支持在非中/英语种之间直接翻译”，而文档 3 中 `qwen-mt-uni` 明确支持全语种直译（含图像输入），且其图像处理能力基于 `qwen-mt-image-2.0`。因此，若需日→韩等非中英直译，请务必使用 `qwen-mt-uni` 或显式指定 `qwen-mt-image-2.0`，避免误用旧版 `qwen-mt-image`。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 |
|--------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语言，支持全称（`Chinese`）、编码（`zh`）或 `auto`（仅 `source_lang`）。`qwen-mt-plus` 和 `qwen-mt-uni` 无语种限制；`qwen-mt-image` 要求至少一方为中/英文。 | 全部 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预：`qwen-mt-plus` 用 `terms`（对象数组，含 `source`/`target` 字段）；`qwen-mt-image` 用 `terminologies`（含 `src`/`tgt`）；`qwen-mt-uni` 用 `glossary`（含 `src`/`tgt`），最多 100 组。 | 各模型独立命名 |
| `tm_list` | `array` | 翻译记忆（仅 `qwen-mt-plus`），提供历史句对提升一致性。 | `qwen-mt-plus` |
| `domains` / `domainHint` | `string` | 领域提示：`qwen-mt-plus` 使用 `domains`（值为中文或英文描述）；`qwen-mt-image` 和 `qwen-mt-uni` 均使用 `domainHint`，**且仅支持英文**，建议 ≤200 单词。 | `qwen-mt-plus`, `qwen-mt-image`, `qwen-mt-uni` |
| `sensitives` | `array` | 敏感词过滤（完全匹配、大小写敏感），最多 50 个。`qwen-mt-image` 和 `qwen-mt-uni` 均支持。 | `qwen-mt-image`, `qwen-mt-uni` |
| `imageSegment` | `bool` | 图像主体分割开关（跳过人物/商品/Logo 上文字），默认 `false`。`qwen-mt-image` 和 `qwen-mt-uni` 均支持；`qwen-mt-plus` 不适用。 | `qwen-mt-image`, `qwen-mt-uni` |

## 使用方式

- **调用地址**：所有模型均使用业务空间专属域名（推荐），格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/...`，其中 `{WorkspaceId}` 在百炼控制台「业务空间详情」中查看。地域支持北京（`cn-beijing`）、新加坡（`ap-southeast-1`）、美国弗吉尼亚（`us-east-1`）。旧 DashScope 域名仍可用，但性能与稳定性较低。
- **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 头传递 API Key，需提前[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md) `/compatible-mode/v1/chat/completions`，将 `translation_options` 作为 `extra_body`（Python）或顶层字段（Node.js/curl）传入。
- **图像/[多模态](../concepts/multi-modal.md)翻译（`qwen-mt-image-*` / `qwen-mt-uni`）**：使用 DashScope 标准接口 `/api/v1/services/aigc/.../generation`，请求体为 JSON，`input` 对象包含 `fileUrl` 或 `source_texts`。
- **同步 vs 异步**：
  - 同步：直接返回结果（文本内容或文件 URL），适合小文本、单图、短音频（≤60 秒）；
  - 异步：请求头加 `X-DashScope-Async: enable`，先获 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询结果。`qwen-mt-image` **必须异步**；`qwen-mt-image-2.0` 和 `qwen-mt-uni` 可选同步或异步。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。

## 限制和注意事项

- **文件限制**：图像/文档/音频单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；图像尺寸 15–8192 像素，宽高比 1:10 至 10:1；URL 中不得含中文字符。
- **语言检测**：`source_lang="auto"` 仅在 `qwen-mt-plus` 和 `qwen-mt-uni` 中可靠；`qwen-mt-image` 的自动检测准确率较低，建议显式指定。
- **领域提示**：`domainHint`（`qwen-mt-image`/`qwen-mt-uni`）和 `domains`（`qwen-mt-plus`）虽语义相近，但实现机制不同，效果不可直接类比；且 `domainHint` **强制要求英文输入**，中文提示将被忽略。
- **术语与敏感词**：`sensitives` 过滤发生在翻译前，匹配原文本；`glossary`/`terminologies`/`terms` 作用于翻译过程，影响译文生成。三者均区分大小写。
- **计费依据**：`qwen-mt-uni` 按 `input_tokens` 计费（含 `image_tokens`/`document_tokens` 等明细）；`qwen-mt-plus` 和 `qwen-mt-image` 按请求次数与字符数计费，具体见控制台定价页。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


