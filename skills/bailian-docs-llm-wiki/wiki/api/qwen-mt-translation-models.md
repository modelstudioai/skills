# qwen mt translation models

Qwen MT 翻译模型系列是百炼平台提供的多模态机器翻译能力集合，覆盖纯文本、图像、文档（PDF/DOCX/PPTX等）及音频等多种输入格式。模型通过统一架构实现高保真内容抽取与格式重构，支持术语干预、敏感词过滤、领域提示等专业功能，适用于本地化、技术文档翻译、电商图片翻译等场景。所有模型均基于 DashScope API 协议，兼容 OpenAI SDK 调用方式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持 55+ 语种互译，提供术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domainHint`）能力，可通过 [OpenAI 兼容接口](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 调用。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：专用图像翻译模型，精准识别并重排版图像中的文字；`qwen-mt-image-2.0` 支持全部 55 个语种间任意互译，而 `qwen-mt-image` 仅支持源或目标语种至少有一方为中/英文（详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)）。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本、图像、PDF、DOCX、PPTX、XLSX、HTML、Markdown、MP3、WAV 等十余种格式输入与原格式输出，是当前推荐的通用入口模型（参见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)）。

> **注意**：文档 1 中 `qwen-mt-image` 的语种限制描述（“不支持在非中/英语种之间直接翻译”）与文档 3 中 `qwen-mt-uni` 的全语种路由能力存在定位差异——前者为专用图像模型的历史约束，后者为新统一架构下的能力升级。生产环境建议优先使用 `qwen-mt-uni` 处理图像，其已继承并扩展了 `qwen-mt-image-2.0` 的全部语种与功能特性。

## 关键参数

| 参数 | 类型 | 必选性 | 说明 |
|------|------|--------|------|
| `model` | `string` | 必选 | 固定为 `qwen-mt-plus`、`qwen-mt-image-2.0`、`qwen-mt-image` 或 `qwen-mt-uni` |
| `source_lang` | `string` | 条件必选 | 源语言代码（如 `zh`、`en`）或 `auto`；`qwen-mt-plus` 和 `qwen-mt-uni` 支持自动检测，`qwen-mt-image` 在 `auto` 下效果受限 |
| `target_lang` | `string` | 必选 | 目标语言代码或全称（如 `ko`、`Korean`），大小写不敏感 |
| `input.fileUrl` / `input.source_texts` | `string` / `array<string>` | 二选一 | `qwen-mt-uni` 同步调用中二者必须且只能提供一个；`qwen-mt-plus` 仅支持 `source_texts`（即 `messages` 中的 `content`） |
| `ext.domainHint` | `string` | 可选 | **仅支持英文**，最多 200 单词，用于引导领域风格（[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 与 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 均明确要求） |
| `ext.sensitives` | `array<string>` | 可选 | 敏感词列表，**区分大小写**，完全匹配时保留原文；单次请求 ≤50 项 |
| `ext.glossary`（`qwen-mt-uni`） / `ext.terminologies`（`qwen-mt-image`） / `translation_options.terms`（`qwen-mt-plus`） | `array<object>` | 可选 | 术语干预，结构均为 `{ "src": "...", "tgt": "..." }`；`qwen-mt-uni` 最多支持 100 组，其余模型建议 ≤50 组 |

## 使用方式

- **同步调用**（适合文本、小图、短音频）：
  - `qwen-mt-plus`：使用 OpenAI 兼容 `/chat/completions` 接口，将 `translation_options` 作为 `extra_body` 传入（[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)）。
  - `qwen-mt-image-*`：调用 `image2image/image-synthesis` 接口，`input` 中指定 `image_url`、`source_lang`、`target_lang`。
  - `qwen-mt-uni`：调用 `multimodal-generation/generation` 接口，根据输入类型选择 `fileUrl` 或 `source_texts`。

- **异步调用**（适合大文档、长音频、高分辨率图像）：
  - 所有模型均需在请求头添加 `X-DashScope-Async: enable`。
  - `qwen-mt-image` **必须**使用异步模式（文档 1 明确指出：“`qwen-mt-image`模型必须设置此请求头”）；`qwen-mt-image-2.0` 和 `qwen-mt-uni` 同步/异步均可。
  - 异步任务创建后，需轮询 `GET /api/v1/tasks/{task_id}`（具体路径见各文档）获取结果。

- **地域与域名**：  
  推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`（参见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 中的迁移说明）。

## 限制和注意事项

- **文件限制**：图像/文档/音频单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；图像尺寸 15–8192 像素，宽高比 1:10 至 10:1。
- **URL 要求**：所有 `image_url` / `fileUrl` 必须为公网可访问的 HTTP/HTTPS 链接，**URL 中不能含中文字符**。
- **术语与敏感词**：`qwen-mt-image` 的 `terminologies` 和 `qwen-mt-uni` 的 `glossary` 均要求 `src` 与 `source_lang`、`tgt` 与 `target_lang` 严格对应；`sensitives` 在所有模型中均为**大小写敏感**的完全匹配。
- **图像主体分割**：`imageSegment`（启用后跳过人物/商品/Logo 上的文字）是 `qwen-mt-image-*` 和 `qwen-mt-uni` 共享的参数；旧参数 `skipImgSegment` 已废弃，仅作兼容（[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中已标注）。
- **计费依据**：`qwen-mt-uni` 按 `input_tokens` 计费，并细分为 `document_tokens`、`image_tokens` 等；`qwen-mt-image-*` 按 `image_count` 计费（固定为 1）；`qwen-mt-plus` 按 token 总量计费（未在原始文档中显式说明，但遵循 DashScope 通用规则）。

## 来源文档

- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


