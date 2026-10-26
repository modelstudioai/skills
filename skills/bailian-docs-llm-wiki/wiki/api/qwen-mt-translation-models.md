# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。开发者可根据输入类型、延迟要求和文件规模选择最适配的模型。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，适用于 API 风格的轻量级文本翻译请求。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 详细说明了其 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)用法。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片中的文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持 55 种语言间任意互译；`qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文。[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 提供了图像格式、尺寸及语种限制等关键约束。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等十余种输入格式，自动识别模态并执行端到端高保真翻译与格式重构。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确了各格式的大小、页数与时长上限。

> **注意**：`qwen-mt-image` 和 `qwen-mt-uni` 均支持图像输入，但前者专精于 OCR+翻译流水线，后者作为通用模态路由器，对图像处理逻辑不同（如 `qwen-mt-uni` 的 `config.imageSegment` 仅在图像格式下生效）。实际选型应以具体业务需求为准，避免混用模型能力边界。

## 关键参数

| 参数 | 适用模型 | 说明 | 示例值 |
|--------|-----------|------|---------|
| `source_lang` / `target_lang` | 全部 | 源/目标语种，支持全称（`Chinese`）、编码（`zh`）或 `auto`（自动检测）；`qwen-mt-image` 要求至少一端为 `Chinese` 或 `English` | `"zh"`, `"en"`, `"auto"` |
| `translation_options`（文本） | `qwen-mt-plus` | 包含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` 等子字段 | `{ "source_lang": "Chinese", "target_lang": "English", "terms": [...] }` |
| `ext.terminologies` / `ext.sensitives` / `ext.domainHint` | `qwen-mt-image`, `qwen-mt-uni` | 统一扩展字段：术语表（`src`/`tgt` 键）、敏感词数组、英文领域提示（≤200 单词） | `[{"src":"API","tgt":"应用程序接口"}]`, `["全场9折"]`, `"E-commerce product description..."` |
| `input.fileUrl` / `input.source_texts` | `qwen-mt-uni` | 二选一必填：公网可访问的文件 URL 或纯文本内容（字符串或数组） | `"https://example.com/doc.pdf"`, `["Hello", "World"]` |
| `config.imageSegment` | `qwen-mt-image`, `qwen-mt-uni` | 图像专用：是否跳过人物/商品/Logo 等主体区域的文字翻译（`true` = 不翻译主体） | `true`, `false` |

> **注意**：`qwen-mt-plus` 使用 `extra_body.translation_options`（Python SDK）或顶层 `translation_options`（Node.js/curl），而 `qwen-mt-image` 和 `qwen-mt-uni` 均使用嵌套在 `ext` 中的 `terminologies`/`sensitives`/`domainHint`。参数命名与层级不一致，需严格按模型文档区分。

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 OpenAI SDK，配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），调用 `chat.completions.create`，将翻译参数置于 `extra_body`（Python）或顶层对象（Node.js/curl）。
- **图像翻译（`qwen-mt-image`/`qwen-mt-image-2.0`）**：调用 `POST /api/v1/services/aigc/image2image/image-synthesis`，设置 `X-DashScope-Async: enable` 启用异步（`qwen-mt-image` 必须），否则默认同步；同步响应直接返回 `output.image_url`，异步需轮询 `/api/v1/tasks/{task_id}`。
- **全模态翻译（`qwen-mt-uni`）**：调用 `POST /api/v1/services/aigc/multimodal-generation/generation`，行为与 `qwen-mt-image` 类似，但支持更多输入格式；同步响应在 `output.Data.TranslatedFileUrl` 或 `output.Data.TranslatedTexts` 中返回结果，异步同样需轮询任务接口。

所有模型均需配置 `DASHSCOPE_API_KEY` 环境变量，并替换 `{WorkspaceId}` 为控制台获取的真实业务空间 ID。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供了各语言 SDK 的完整示例代码。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧版 `dashscope.aliyuncs.com` 域名虽仍可用，但性能与稳定性较低。
- **图像限制**：`qwen-mt-image` 和 `qwen-mt-uni` 对图像输入均有相同约束——格式支持 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP；宽高范围 15–8192 像素；宽高比 1:10 至 10:1；文件大小 ≤100 MB；URL 中不得含中文字符。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 字段为对象数组（`{source: "...", target: "..."}`），而 `qwen-mt-image` 和 `qwen-mt-uni` 的 `terminologies` 要求 `src`/`tgt` 键；所有敏感词均**区分大小写**且要求**完全匹配**。
- **领域提示**：`qwen-mt-plus` 的 `domains` 字段在文档 1 中示例被截断（见“profe…”），实际应为完整英文描述；`qwen-mt-image` 和 `qwen-mt-uni` 的 `domainHint` 明确要求仅支持英文且 ≤200 单词，此为强约束。
- **[异步任务](../concepts/asynchronous-task.md)管理**：`task_id` 有效期 24 小时，查询接口默认 RPS 为 1；任务成功后 `TranslatedFileUrl` 同样仅 24 小时有效，需及时下载。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


