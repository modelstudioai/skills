# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，适用于本地化、技术文档、电商客服、内容出海等高要求翻译任务。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options` 参数启用术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版与图文关系；支持图像主体分割（`imageSegment`）、敏感词过滤（`sensitives`）及术语干预（`terminologies`）。`qwen-mt-image-2.0` 支持全部 55 种语言互译，而 `qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等多种格式输入，并自动重构为同格式输出。同步/异步双模式，内置格式感知路由与跨模态翻译链路。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：`qwen-mt-plus` 的领域提示参数名为 `domains`（见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)），而 `qwen-mt-image` 和 `qwen-mt-uni` 均使用 `domainHint` 且**仅支持英文描述**。三者参数命名与语义不一致，开发时需按模型分别适配。

## 关键参数

| 参数名 | 类型 | 说明 | 模型支持 |
|--------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语种（支持全称如 `"Chinese"`、编码如 `"zh"` 或 `"auto"`） | 全部 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预列表；`qwen-mt-plus` 用 `terms`（字段 `source`/`target`），`qwen-mt-image` 用 `terminologies`（字段 `src`/`tgt`），`qwen-mt-uni` 用 `glossary`（字段 `src`/`tgt`） | 各自专属 |
| `tm_list` | `array` | 翻译记忆对列表（仅 `qwen-mt-plus` 支持） | `qwen-mt-plus` |
| `domainHint` / `domains` | `string` | 领域提示（英文，≤200 单词）；`qwen-mt-plus` 使用 `domains`，其余模型使用 `domainHint` | 全部（命名不同） |
| `sensitives` / `sensitives` | `array` | 敏感词列表（完全匹配、大小写敏感）；`qwen-mt-image` 和 `qwen-mt-uni` 均支持，但 `qwen-mt-plus` 不支持 | `qwen-mt-image`, `qwen-mt-uni` |
| `imageSegment` | `bool` | 是否跳过图像主体（人物/商品/Logo）上的文字翻译；`qwen-mt-image` 和 `qwen-mt-uni` 支持，`qwen-mt-plus` 不适用 | `qwen-mt-image`, `qwen-mt-uni` |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，`POST /compatible-mode/v1/chat/completions`，将 `translation_options` 作为 `extra_body`（Python）或顶层字段（Node.js/curl）传入。必须配置地域专属 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。
- **图像翻译（`qwen-mt-image-*`）**：调用 `POST /api/v1/services/aigc/image2image/image-synthesis`，`input` 中指定 `image_url`、`source_lang`、`target_lang`；同步模式直接返回 `output.image_url`，异步模式需加请求头 `X-DashScope-Async: enable` 并轮询 `/api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `POST /api/v1/services/aigc/multimodal-generation/generation`，`input` 中二选一：`fileUrl`（文档/图片/音频 URL）或 `source_texts`（字符串或数组）；同步/异步行为与 `qwen-mt-image` 一致，但响应结构统一为 `output.Data` 包含 `TranslatedFileUrl` 或 `TranslatedTexts`。

> **注意**：`qwen-mt-image` 模型**必须**使用异步模式（即强制设置 `X-DashScope-Async: enable`），而 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 同步/异步均可。该限制在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中明确说明，但未在 `qwen-mt-uni` 文档中强调，开发者需主动规避同步调用 `qwen-mt-image`。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧 DashScope 公共域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低，详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **文件限制**：`qwen-mt-image` 仅支持 JPG 格式；`qwen-mt-uni` 支持 JPG/PNG/MP3/WAV 等 10+ 格式，但单文件 ≤100 MB、文档 ≤200 页、音频 3 秒–60 分钟；所有 URL 不得含中文字符。
- **术语与敏感词**：`qwen-mt-plus` 不支持敏感词过滤；`qwen-mt-image` 和 `qwen-mt-uni` 的 `sensitives` 对大小写敏感，且仅做完全匹配过滤；`glossary`（`qwen-mt-uni`）最多 100 组，`terminologies`（`qwen-mt-image`）无显式上限但建议 ≤50。
- **领域提示**：`domainHint`（`qwen-mt-image`/`qwen-mt-uni`）和 `domains`（`qwen-mt-plus`）均**仅支持英文输入**，中文提示将导致效果下降或报错。
- **认证与 Key**：所有模型均需 `DASHSCOPE_API_KEY`，且北京/新加坡/弗吉尼亚地域的 Key **不通用**，须按地域分别获取与配置。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


