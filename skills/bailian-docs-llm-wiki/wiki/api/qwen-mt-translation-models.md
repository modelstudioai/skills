# qwen mt translation models

Qwen MT 翻译模型系列是百炼平台提供的多模态机器翻译能力集合，覆盖纯文本、图像、文档（PDF/DOCX等）及音频等多种输入格式。该系列包含专用模型（如 `qwen-mt-image-2.0`）与统一模型（`qwen-mt-uni`），均支持高保真语义翻译、术语干预、领域提示和敏感词过滤等生产级功能。所有模型均通过 DashScope API 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于本地化、内容出海、多语言客服等场景。

## 支持的模型/功能

- **`qwen-mt-image-2.0`**：专注图像翻译的专用模型，支持中、英、日、韩、西、法等 **55 个语种**互译（无源/目标语种限制），可精准还原排版并支持商品主体检测、术语干预、敏感词过滤；仅限华北2（北京）、新加坡地域。  
- **`qwen-mt-image`**：基础图像翻译模型，**仅支持源或目标语种至少有一项为中文或英文**（例如不可直接日→韩），其余能力与 `qwen-mt-image-2.0` 类似。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。  
- **`qwen-mt-plus`**：面向纯文本的高性能翻译模型，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持术语干预（`terms`）、翻译记忆（`tm_list`）和自动语种识别（`source_lang: "auto"`）。  
- **`qwen-mt-uni`**：全模态统一翻译模型，**单一接口支持文本、图片、PDF、DOCX、PPTX、XLSX、HTML、Markdown、MP3、WAV 等十余种格式**，自动识别模态并执行端到端翻译与格式重构。其设计目标是替代多个专用接口，降低集成复杂度。该能力在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中完整定义。  
> **注意**：文档1中 `qwen-mt-image` 的语种限制（“不支持非中/英语种间直译”）与文档3中 `qwen-mt-uni` 的全语种支持能力存在定位差异，二者并非版本迭代关系，而是**不同模型的适用边界声明**；开发者应根据输入模态选择对应模型，而非假设 `qwen-mt-uni` 可完全替代 `qwen-mt-image-2.0` 的图像排版还原精度。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `qwen-mt-image-2.0`、`qwen-mt-image`、`qwen-mt-plus` 或 `qwen-mt-uni` |
| `input.source_lang` | `string` | ⚠️（`qwen-mt-plus`/`qwen-mt-uni` 可选；`qwen-mt-image-*` 必填） | 源语言代码（如 `zh`, `en`, `ja`）或 `"auto"`（仅 `qwen-mt-plus` 和 `qwen-mt-uni` 支持） |
| `input.target_lang` | `string` | ✅ | 目标语言代码或全称（如 `ko`, `Korean`），大小写不敏感 |
| `input.fileUrl` / `input.source_texts` | `string` / `array<string>` | ✅（二选一） | `qwen-mt-uni` 专用：文件公网 URL 或纯文本数组；`qwen-mt-plus` 仅支持 `messages` 字段传文本 |
| `ext.domainHint` | `string` | ❌ | **仅英文**，最多 200 单词，用于引导领域风格（如电商客服、技术文档） |
| `ext.sensitives` | `array<string>` | ❌ | 敏感词列表，**区分大小写**，完全匹配时保留原文不翻译；单次请求 ≤50 项 |
| `ext.glossary`（`qwen-mt-uni`） / `ext.terminologies`（`qwen-mt-image-*`） / `translation_options.terms`（`qwen-mt-plus`） | `array<object>` | ❌ | 术语干预：`{ "src": "...", "tgt": "..." }`，语种需与 `source_lang`/`target_lang` 一致 |

## 使用方式

- **同步调用**（推荐小负载）：  
  - 文本/图像/小文件 → 直接返回结果（`output.Data.TranslatedTexts` 或 `output.Data.TranslatedFileUrl`）  
  - `qwen-mt-plus`：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md) `/chat/completions`，将 `translation_options` 作为 `extra_body` 传入（见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)）  
  - `qwen-mt-image-*` / `qwen-mt-uni`：使用 DashScope 标准接口 `/generation` 或 `/image-synthesis`，**无需额外请求头**  

- **异步调用**（推荐大文件/长音频）：  
  - 所有模型均支持，**必须添加请求头 `X-DashScope-Async: enable`**  
  - 第一步：POST 创建任务，获取 `task_id`  
  - 第二步：轮询 `GET /api/v1/tasks/{task_id}`（`qwen-mt-uni`）或 `GET /api/v1/tasks/image-synthesis/{task_id}`（`qwen-mt-image-*`）直至 `task_status = SUCCEEDED`  

- **地域与域名**：  
  - 统一使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），**不再推荐旧版 `dashscope.aliyuncs.com` 域名**（见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)）  

## 限制和注意事项

- **输入限制**：  
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/WEBP/TIFF，大小 ≤100 MB  
  - 文档/音频：单文件 ≤100 MB，PDF ≤200 页，音频时长 3 秒–60 分钟  
  - URL 中**禁止含中文字符**，否则请求失败  

- **语种兼容性**：  
  - `qwen-mt-image` 不支持非中/英语种间直译（如日→韩），而 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制  
  - `domainHint` 和 `sensitives` **严格要求英文输入**，中文提示将被忽略  

- **术语与敏感词**：  
  - `sensitives` 为**完全匹配、区分大小写**；`glossary`/`terminologies` 中 `src` 必须与 `source_lang` 语种一致，`tgt` 必须与 `target_lang` 一致  
  - `qwen-mt-uni` 的 `glossary` 最多支持 100 组术语，`qwen-mt-image-*` 的 `terminologies` 建议 ≤50 组  

- **输出时效性**：  
  - 同步返回的 `TranslatedFileUrl`（图像/文档）有效期为 **24 小时**，需及时下载保存  
  - 异步任务 `task_id` 有效期也为 **24 小时**，超时需重新提交  

> **注意**：文档1中 `qwen-mt-image` 的 `skipImgSegment` 参数已被弃用，新代码应统一使用 `ext.config.imageSegment`（见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)）；文档3中 `qwen-mt-uni` 的 `ext.config.imageSegment` 作用相同，但仅对图像输入生效。

## 来源文档

- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


