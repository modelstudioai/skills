# qwen mt translation models

Qwen-MT 系列是阿里云百炼平台提供的专业机器翻译模型家族，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制能力。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options` 参数控制源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版与布局。`qwen-mt-image-2.0` 支持 55 种语言间任意互译；`qwen-mt-image` 仅支持源或目标语言至少有一方为中文或英文。两者均支持术语干预（`terminologies`）、敏感词过滤（`sensitives`）和图像主体分割（`imageSegment`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等十余种格式输入，自动识别模态并执行高保真翻译与原格式重构。同步/异步调用统一接口，返回结构化结果（含 `TranslatedFileUrl` 或 `TranslatedTexts`）。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例末尾被截断（`"profe...`），且未说明其值必须为英文；而文档 2 和文档 3 明确要求领域提示（`domainHint`）**只支持英文**。实际使用中应以 `domainHint`（英文字符串）为准，避免使用 `domains` 字段。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 | 是否必填 |
|--------|------|------|----------|----------|
| `source_lang` | `string` | 源语言代码或全称（如 `"zh"`、`"Chinese"`），支持 `"auto"` 自动检测 | 全部 | 文本/图像/文档：条件必填（`qwen-mt-plus` 必填；`qwen-mt-image`/`qwen-mt-uni` 中若传 `fileUrl` 则可选） |
| `target_lang` | `string` | 目标语言代码或全称（如 `"en"`、`"English"`） | 全部 | 必填 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预列表。`qwen-mt-plus` 用 `terms`（字段名 `source`/`target`）；`qwen-mt-image` 用 `terminologies`（字段名 `src`/`tgt`）；`qwen-mt-uni` 用 `glossary`（字段名 `src`/`tgt`） | 各自对应 | 可选 |
| `tm_list` | `array` | 翻译记忆列表（仅 `qwen-mt-plus` 支持） | `qwen-mt-plus` | 可选 |
| `domainHint` | `string` | **英文**领域提示（≤200 单词），用于引导译文风格 | `qwen-mt-image`, `qwen-mt-uni` | 可选 |
| `sensitives` | `array<string>` | 敏感词列表（区分大小写，完全匹配即过滤） | `qwen-mt-image`, `qwen-mt-uni` | 可选 |
| `imageSegment` | `boolean` | 是否跳过图像主体（人物/商品/Logo）上的文字翻译 | `qwen-mt-image`, `qwen-mt-uni`（仅图像输入生效） | 可选，默认 `false` |

## 使用方式

- **调用地址**：全部模型均使用业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 需替换为控制台获取的实际 ID，`{region}` 为 `cn-beijing` / `ap-southeast-1` / `us-east-1`。旧版 `dashscope.aliyuncs.com` 域名仍可用，但[官方推荐迁移](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)以获得更高稳定性。
- **认证方式**：通过 `Authorization: Bearer $DASHSCOPE_API_KEY` 请求头传递 API Key。
- **同步调用**：
  - `qwen-mt-plus`：使用 `/compatible-mode/v1/chat/completions` 接口，将翻译参数置于 `extra_body.translation_options`（OpenAI SDK）或顶层 `translation_options`（curl/Node.js）。
  - `qwen-mt-image` / `qwen-mt-uni`：使用 `/api/v1/services/aigc/.../generation` 接口，参数置于 `input` 和 `ext` 对象中。
- **异步调用**：
  - `qwen-mt-image`：必须在请求头添加 `X-DashScope-Async: enable`。
  - `qwen-mt-uni`：同样需添加 `X-DashScope-Async: enable`，任务查询使用 `GET /api/v1/tasks/{task_id}`。
  - `qwen-mt-plus` **不支持异步调用**。
- **SDK 示例**：Python 和 Node.js 均支持 OpenAI SDK（需配置 `base_url`），`qwen-mt-image` 和 `qwen-mt-uni` 还支持原生 `requests` 调用。具体代码见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 和 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **地域支持**：`qwen-mt-plus` 支持北京、新加坡、美国（弗吉尼亚）三地；`qwen-mt-image` 和 `qwen-mt-uni` 当前仅明确列出华北2（北京）和新加坡地域，调用前请确认控制台业务空间所在地域是否开通对应模型。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB。
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟。
  - URL：必须公网可访问，且**不能包含中文字符**。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 和 `qwen-mt-image` 的 `terminologies` 要求源/目标文本语种严格匹配 `source_lang`/`target_lang`；`sensitives` 在 `qwen-mt-image` 和 `qwen-mt-uni` 中均为**区分大小写**的完全匹配。
- **领域提示**：`domainHint`（`qwen-mt-image`/`qwen-mt-uni`）和 `domains`（`qwen-mt-plus`）功能相似，但前者为强制英文、后者文档不完整且无明确语言要求。**强烈建议统一使用 `domainHint` 并确保为英文描述**。
- **错误处理**：同步调用失败时响应顶层含 `code`/`message`；异步调用需先查 `task_status`，再根据 `output.Success` 判断业务成败（`SUCCEEDED` 状态下 `Success=false` 表示业务失败）。错误码详情见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


