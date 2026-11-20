# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业化机器翻译能力集合，覆盖纯文本、图像、多格式文档及音频等全模态输入场景。模型采用统一架构设计，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能，并提供同步/异步两种调用模式以适配不同延迟与吞吐需求。所有模型均通过 DashScope 标准 API 协议或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)提供服务。

## 支持的模型与功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options` 参数控制源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持全部 55 种语言间直译；`qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文。二者均支持图像主体分割（`imageSegment`）、敏感词过滤（`sensitives`）和术语干预（`terminologies`）。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本字符串、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等 14+ 种输入格式，自动识别模态并执行高保真翻译与原格式重构。其 `glossary` 字段替代旧版 `terms`，`fileUrl` 与 `source_texts` 二选一，且强制要求 `target_lang`。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例被截断（末尾为 `"profe`），且未说明该字段是否支持非英文描述；而文档 2 和文档 3 明确要求领域提示（`domainHint`）**只支持英文**。因此 `qwen-mt-plus` 的 `domains` 字段实际行为应与 `domainHint` 一致，即仅接受英文提示 —— 此处以 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 和 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的约束为准。

## 关键参数

| 参数名 | 类型 | 适用模型 | 说明 |
|--------|------|----------|------|
| `source_lang` / `target_lang` | `string` | 全部 | 语种标识，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（仅 `source_lang`）。`qwen-mt-image` 对语种组合有限制；`qwen-mt-uni` 和 `qwen-mt-image-2.0` 无限制。 |
| `terms` / `terminologies` / `glossary` | `array` | `qwen-mt-plus` / `qwen-mt-image*` / `qwen-mt-uni` | 术语干预。字段名不同但语义一致：`src`/`source` 与 `tgt`/`target` 需分别匹配源/目标语种。`qwen-mt-uni` 的 `glossary` 最多支持 100 组，其余模型建议 ≤50 组。 |
| `tm_list` | `array` | `qwen-mt-plus` 专属 | 翻译记忆列表，每项为 `{ "source": "...", "target": "..." }`，用于保持历史译文一致性。`qwen-mt-uni` 和 `qwen-mt-image` 不支持此参数。 |
| `domainHint` | `string` | `qwen-mt-image*`, `qwen-mt-uni` | 英文领域提示（≤200 单词），影响译文风格与术语选择。`qwen-mt-plus` 使用 `domains` 字段，但行为与之相同。 |
| `sensitives` | `array<string>` | `qwen-mt-image*`, `qwen-mt-uni` | 敏感词列表，**完全匹配且大小写敏感**，匹配后原文保留不翻译。`qwen-mt-plus` 不支持。 |
| `imageSegment` | `bool` | `qwen-mt-image*`, `qwen-mt-uni`（图像输入时生效） | 是否跳过图像主体（人物、商品、Logo）上的文字翻译。默认 `false`。旧版 `skipImgSegment` 已废弃，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。 |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，通过 `extra_body={"translation_options": {...}}` 传入参数。必须配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），不可使用旧版 `dashscope.aliyuncs.com` 域名（[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 强烈建议迁移）。
- **图像翻译（`qwen-mt-image*`）**：调用 `/api/v1/services/aigc/image2image/image-synthesis`。同步模式直接返回 `output.image_url`；异步模式需添加请求头 `X-DashScope-Async: enable` 并轮询 `/api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `/api/v1/services/aigc/multimodal-generation/generation`。同步模式返回 `output.Data.TranslatedFileUrl` 或 `output.Data.TranslatedTexts`；异步模式同样依赖 `X-DashScope-Async: enable` 及任务轮询。注意：`fileUrl` 与 `source_texts` **必须且只能提供一个**，且 URL 中不能含中文字符。

## 限制和注意事项

- **地域与域名**：所有模型均支持华北2（北京）、新加坡、美国（弗吉尼亚）地域，但 `qwen-mt-image` 和 `qwen-mt-uni` 的 API 路径仅文档明确列出北京地域（`cn-beijing`）示例；其他地域需将域名中的 `cn-beijing` 替换为对应区域标识（如 `ap-southeast-1`），路径保持不变。务必使用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），旧版 DashScope 域名已不推荐。
- **输入限制**：`qwen-mt-uni` 支持单文件 ≤100 MB、文档 ≤200 页、音频 3 秒–60 分钟；`qwen-mt-image*` 要求图像宽高 15–8192 像素、宽高比 1:10 至 10:1、大小 ≤100 MB；`qwen-mt-plus` 无显式长度限制，但受上下文窗口约束。
- **术语与敏感词**：`sensitives` 在 `qwen-mt-image*` 和 `qwen-mt-uni` 中均为**完全匹配、大小写敏感**；`glossary`/`terminologies` 中的 `src` 必须严格匹配原文（含空格、标点），否则不生效。
- **错误处理**：`qwen-mt-plus`（OpenAI 兼容）失败时抛出异常；`qwen-mt-image*` 和 `qwen-mt-uni` 同步调用失败时顶层返回 `code`/`message`；[异步调用](../concepts/asynchronous-invocation.md)需检查 `output.task_status` 和 `output.Success` 双重状态（即使 `task_status == "SUCCEEDED"`，`Success == false` 仍表示业务失败）。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


