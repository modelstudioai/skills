# qwen mt translation models

Qwen-MT 系列是阿里云百炼平台提供的专业机器翻译模型家族，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制能力。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并已在华北2（北京）、新加坡、美国（弗吉尼亚）等多地部署。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options` 参数控制源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版与布局；支持图像主体分割（`imageSegment`）、敏感词过滤（`sensitives`）和术语干预（`terminologies`）。`qwen-mt-image-2.0` 支持 55 种语言间任意互译，而 `qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等多种输入格式，自动识别模态并执行高保真翻译与格式重构。同步/[异步调用](../concepts/asynchronous-invocation.md)均支持，且统一使用 `fileUrl` 或 `source_texts` 作为输入入口。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例末尾被截断（`"profe...`），实际应为完整英文描述；正确用法请以 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 中的字段定义为准。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 |
|--------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语言，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（仅部分模型支持） | 全部 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预：`qwen-mt-plus` 用 `terms`，`qwen-mt-image` 用 `terminologies`，`qwen-mt-uni` 用 `glossary`；三者结构一致（`{"source"/"src": "...", "target"/"tgt": "..."}`） | 各自专属 |
| `tm_list` | `array` | 翻译记忆，仅 `qwen-mt-plus` 支持，用于提供历史句对提升一致性 | `qwen-mt-plus` |
| `domainHint` | `string` | 英文领域提示（≤200 单词），影响译文风格；**所有模型均要求英文输入** | `qwen-mt-image`, `qwen-mt-uni` |
| `domains` | `string` | 文本模型专用领域提示字段（文档 1 示例中未闭合），功能同 `domainHint`，但字段名不同 | `qwen-mt-plus` |
| `sensitives` | `array<string>` | 敏感词列表（区分大小写），匹配即过滤原文本；`qwen-mt-image` 和 `qwen-mt-uni` 均支持 | `qwen-mt-image`, `qwen-mt-uni` |
| `imageSegment` | `boolean` | 是否跳过图像主体（人物/Logo/商品）上的文字翻译；默认 `false`；`qwen-mt-image` 和 `qwen-mt-uni` 均支持 | `qwen-mt-image`, `qwen-mt-uni` |

> **注意**：`qwen-mt-plus` 不支持 `sensitives` 和 `imageSegment`；`qwen-mt-image` 的旧参数 `skipImgSegment` 已废弃，应改用 `imageSegment` —— 此差异在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中已明确标注。

## 使用方式

- **地域与 endpoint**：所有模型均支持华北2（北京）、新加坡、美国（弗吉尼亚）地域，需使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**不推荐继续使用旧版 `dashscope.aliyuncs.com` 域名**（[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 已强调迁移必要性）。
- **认证**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 头传递 API Key，需提前[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **调用模式**：
  - `qwen-mt-plus`：仅支持 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/chat/completions`），必须传 `messages` + `extra_body.translation_options`（Python）或顶层 `translation_options`（Node.js/curl）。
  - `qwen-mt-image`：使用 `/api/v1/services/aigc/image2image/image-synthesis`，同步调用无需额外 header；[异步调用](../concepts/asynchronous-invocation.md)需添加 `X-DashScope-Async: enable`。
  - `qwen-mt-uni`：使用 `/api/v1/services/aigc/multimodal-generation/generation`，同步/异步行为由 `X-DashScope-Async` header 控制，请求体结构统一。
- **输入格式选择**：
  - 纯文本 → 优先用 `qwen-mt-plus`（低延迟、高可控性）；
  - 图像 → 用 `qwen-mt-image-2.0`（更广语种支持）或 `qwen-mt-image`（仅中英相关场景）；
  - 文档/音频/混合输入 → 必须用 `qwen-mt-uni`。

## 限制和注意事项

- **语言限制**：`qwen-mt-image` 要求源/目标语种至少一方为中文或英文；`qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制；`qwen-mt-plus` 未明确列出支持语种，建议以控制台实际可用模型为准。
- **文件限制**：`qwen-mt-image` 仅支持 JPG 格式输入；`qwen-mt-uni` 支持 JPG/PNG/MP3/WAV 等十余种格式，但单文件 ≤100 MB、文档 ≤200 页、音频时长 3 秒–60 分钟。
- **URL 要求**：所有模型均要求 `image_url` / `fileUrl` 为公网可访问 HTTPS URL，且 **URL 中不能含中文字符**。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 和 `qwen-mt-uni` 的 `glossary` 最多支持 100 组；`qwen-mt-image` 和 `qwen-mt-uni` 的 `sensitives` 最多 50 个；所有术语/敏感词均**区分大小写**。
- **领域提示**：`domainHint`（`qwen-mt-image`/`qwen-mt-uni`）和 `domains`（`qwen-mt-plus`）**仅接受英文描述**，中文输入将导致效果下降或报错。
- **异步任务管理**：`qwen-mt-image` 和 `qwen-mt-uni` 的异步 `task_id` 有效期均为 24 小时，查询接口默认限频 1 RPS；任务成功后返回的 `TranslatedFileUrl` 或 `image_url` 同样仅 24 小时有效，需及时下载。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


