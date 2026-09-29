# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，适用于本地化、技术文档翻译、电商内容出海等高精度需求场景。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 是文本翻译的核心接口文档。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options`（含 `source_lang`/`target_lang`/`terms`/`tm_list`/`domains`）扩展参数，适用于 API 集成与批量文本处理。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版；`qwen-mt-image-2.0` 支持全部 55 种语言互译，而 `qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文的组合（如日→中、英→法），详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等十余种格式输入，自动识别模态并执行端到端翻译与格式重构，是多格式混合场景的首选方案。

> **注意**：文档 1 中示例代码的 `domains` 字段在 Python 示例末尾被截断（`"profe...`），且未说明其值必须为英文；而文档 2 和文档 3 明确要求 `domainHint` **只支持英文**（最多 200 个英文单词）。实际使用时请严格传入完整英文描述，否则可能导致字段被忽略或报错。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 |
|--------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语种，支持全称（`Chinese`）、编码（`zh`）或 `auto`（仅部分模型支持）；二者不可相同 | 全部 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预：`qwen-mt-plus` 用 `terms`（对象数组，`source`/`target` 键）；`qwen-mt-image` 用 `terminologies`（`src`/`tgt`）；`qwen-mt-uni` 用 `glossary`（`src`/`tgt`） | 各模型独立命名，语义一致 |
| `tm_list` | `array` | 翻译记忆（仅 `qwen-mt-plus`），提供历史句对提升一致性 | `qwen-mt-plus` |
| `domainHint` / `domains` | `string` | 领域提示：`qwen-mt-image` 和 `qwen-mt-uni` 使用 `domainHint`；`qwen-mt-plus` 使用 `domains`；三者均**强制要求英文输入** | 全部 |
| `sensitives` | `array` | 敏感词过滤列表，**大小写敏感**，完全匹配即跳过翻译 | `qwen-mt-image`, `qwen-mt-uni` |
| `imageSegment` | `bool` | 图像主体分割开关（跳过人物/Logo等主体上的文字），默认 `false`；旧参数 `skipImgSegment` 已弃用但兼容 | `qwen-mt-image`, `qwen-mt-uni` |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，`POST /chat/completions`，通过 `extra_body.translation_options`（Python）或顶层 `translation_options`（Node.js/curl）传参。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供了完整的 SDK 示例。
- **图像翻译（`qwen-mt-image-*`）**：调用 `/api/v1/services/aigc/image2image/image-synthesis`，同步模式直接返回 `image_url`；异步模式需添加 `X-DashScope-Async: enable` 请求头并轮询 `/api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `/api/v1/services/aigc/multimodal-generation/generation`，通过 `input.fileUrl`（文件 URL）或 `input.source_texts`（文本）指定输入，同步/异步行为与 `qwen-mt-image` 一致，但支持更广格式和用量明细统计（`usage.input_tokens_details`）。

所有模型均需配置业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）及有效的 `DASHSCOPE_API_KEY`，不推荐继续使用旧版 `dashscope.aliyuncs.com` 域名。

## 限制和注意事项

- **地域与域名**：北京、新加坡、美国（弗吉尼亚）地域均提供专属业务空间域名，强烈建议迁移以获得更高稳定性与性能；旧域名虽仍可用，但已不推荐用于生产环境。
- **输入限制**：
  - 图像类模型：尺寸 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - `qwen-mt-uni`：单文件 ≤100 MB，文档 ≤200 页，音频 3 秒–60 分钟；
  - URL 地址中**禁止包含中文字符**。
- **术语与领域**：所有 `domainHint`/`domains` 字段**仅接受英文描述**；术语表（`glossary`/`terminologies`/`terms`）中 `src` 与 `source_lang`、`tgt` 与 `target_lang` 的语种必须严格一致。
- **异步任务**：`task_id` 有效期 24 小时；异步返回的 `TranslatedFileUrl` 同样有效期 24 小时，需及时下载保存。
- **错误处理**：同步调用失败时响应顶层含 `code`/`message`；`qwen-mt-uni` 同步成功响应中 `output.Success` 为 `true`，失败则无 `output`；异步调用中 `task_status == "SUCCEEDED"` 仅表示任务完成，**必须检查 `output.Success` 才能确认业务是否成功**。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


