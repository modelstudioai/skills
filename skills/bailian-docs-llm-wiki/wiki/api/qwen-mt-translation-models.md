# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，适用于本地化、技术文档翻译、电商内容出海等高要求场景。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 是文本翻译的核心接口文档。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中/英/日/韩/法/西等主流语种互译，提供 `translation_options`（含 `source_lang`/`target_lang`/`terms`/`tm_list`/`domains`）扩展参数，适用于 API 集成与批量文本处理。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版。`qwen-mt-image-2.0` 支持全部 55 种语言间直译；`qwen-mt-image` 仅支持源或目标语种至少有一项为中文或英文的组合。二者均支持术语干预（`terminologies`）、敏感词过滤（`sensitives`）和图像主体分割（`imageSegment`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持字符串、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等输入格式，自动识别模态并执行端到端高保真翻译与格式重构。同步调用返回文本或文件 URL，异步调用支持大文档/长音频处理。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 提供完整协议规范。

> **注意**：`qwen-mt-image` 和 `qwen-mt-uni` 均支持图像输入，但 `qwen-mt-image` 专精于 OCR+翻译流水线，而 `qwen-mt-uni` 将图像作为多模态输入链路的一环，其图像处理能力依赖统一模态理解模块，二者适用场景不同，不可简单互换。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 | 备注 |
|--------|------|------|----------|------|
| `source_lang` / `target_lang` | `string` | 源/目标语种，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（仅 `source_lang`） | 全部 | `qwen-mt-image` 要求至少一项为 `"Chinese"` 或 `"English"`；`qwen-mt-uni` 无此限制 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预列表，格式为 `[{"source": "...", "target": "..."}]`（`qwen-mt-plus`）、`[{"src": "...", "tgt": "..."}]`（`qwen-mt-image`）、`[{"src": "...", "tgt": "..."}]`（`qwen-mt-uni`） | 全部 | `qwen-mt-plus` 使用 `terms` 字段；`qwen-mt-image` 使用 `terminologies`；`qwen-mt-uni` 使用 `glossary`；三者语义一致，但字段名与嵌套结构不同 |
| `tm_list` | `array` | 翻译记忆列表，格式为 `[{"source": "...", "target": "..."}]` | `qwen-mt-plus` 专属 | 仅该模型支持，用于提升术语与句式一致性 |
| `domainHint` | `string` | 英文领域提示，最多 200 个单词，用于引导译文风格 | 全部 | **必须为英文**，中文提示无效；`qwen-mt-plus` 的 `domains` 字段为旧版命名，已废弃，应统一使用 `domainHint` |
| `sensitives` | `array<string>` | 敏感词列表，完全匹配时跳过翻译并保留原文，**区分大小写** | `qwen-mt-image`, `qwen-mt-uni` | `qwen-mt-plus` 不支持此功能 |
| `imageSegment` | `boolean` | 是否跳过图像主体（人物/商品/Logo）上的文字翻译 | `qwen-mt-image`, `qwen-mt-uni` | 默认 `false`；`qwen-mt-image` 旧版参数 `skipImgSegment` 已弃用，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，`POST /compatible-mode/v1/chat/completions`，通过 `extra_body.translation_options` 传入参数。推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），性能与稳定性优于旧版 `dashscope.aliyuncs.com` 域名。
- **图像翻译（`qwen-mt-image-*`）**：调用 `POST /api/v1/services/aigc/image2image/image-synthesis`。同步模式直接返回 `output.image_url`；异步模式需添加请求头 `X-DashScope-Async: enable` 获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `POST /api/v1/services/aigc/multimodal-generation/generation`。输入支持 `fileUrl`（文档/图片/音频 URL）或 `source_texts`（字符串或数组）。同步模式返回 `output.Data.TranslatedFileUrl` 或 `output.Data.TranslatedTexts`；异步模式同样需 `X-DashScope-Async: enable` 并轮询任务状态。

> **注意**：`qwen-mt-plus` 仅支持文本输入，不接受文件 URL；`qwen-mt-image` 和 `qwen-mt-uni` 均支持图像，但接口路径、请求体结构及响应格式完全不同，不可混用。务必根据输入类型选择对应模型与 endpoint。

## 限制和注意事项

- **地域与域名**：北京、新加坡、美国（弗吉尼亚）地域均提供业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），强烈建议迁移使用；旧版 `dashscope.aliyuncs.com` 域名虽仍可用，但性能与稳定性较低。
- **认证与配置**：所有调用均需有效 `DASHSCOPE_API_KEY`，且需在环境变量或 SDK 初始化时正确配置。API Key 因地域隔离，北京与新加坡的 Key 不通用。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟；
  - URL 中禁止包含中文字符。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms`、`qwen-mt-image` 的 `terminologies`、`qwen-mt-uni` 的 `glossary` 功能语义一致，但字段名与结构不同，集成时需按模型适配；`sensitives` 仅 `qwen-mt-image` 和 `qwen-mt-uni` 支持，且对大小写敏感。
- **领域提示**：`domainHint`（或已废弃的 `domains`）**必须为英文**，中文输入将被忽略，此限制在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 和 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中均有明确说明。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


