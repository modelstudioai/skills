# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，适用于本地化、技术文档翻译、电商内容出海等高要求场景。模型能力与部署地域、调用模式（同步/异步）强相关，需按实际需求选择对应模型和接口。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，提供 `translation_options` 参数控制源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）及领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版。`qwen-mt-image-2.0` 支持 55 种语言间任意互译；`qwen-mt-image` 仅支持源或目标语言至少有一项为中文或英文。两者均支持 `imageSegment` 主体分割、`terminologies` 术语干预、`sensitives` 敏感词过滤及英文 `domainHint` 领域提示。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频共 13+ 种格式输入，并原格式输出译文。其设计目标是“一次接入、多模态通译”，通过智能路由自动识别输入类型并调用最优子链路。该模型同时支持同步与异步调用，是处理混合格式或多页文档的首选方案。

> **注意**：文档 2 中 `qwen-mt-image` 的语种限制（“不支持在非中/英语种之间直接翻译”）与文档 3 中 `qwen-mt-uni` 对图像输入的描述存在隐含冲突——`qwen-mt-uni` 在图像模式下实际复用 `qwen-mt-image-2.0` 引擎，因此也支持全部 55 种语言互译。建议以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的能力说明为准。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 | 备注 |
|--------|------|------|----------|------|
| `source_lang` / `target_lang` | `string` | 源/目标语言标识，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（仅 `source_lang`） | 全部 | `qwen-mt-plus` 使用 `source_lang`/`target_lang`；`qwen-mt-image` 和 `qwen-mt-uni` 使用 `source_lang`/`target_lang`（文档 2 和 3 均明确要求必填 `target_lang`） |
| `translation_options` | `object` | `qwen-mt-plus` 专属顶层参数，包裹 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` | `qwen-mt-plus` | OpenAI 兼容模式下必须置于 `extra_body`（Python）或顶层（Node.js/curl） |
| `terms` / `tm_list` | `array` | 术语干预列表（`terms`）与翻译记忆列表（`tm_list`） | `qwen-mt-plus` | `terms` 为 `{source: "...", target: "..."}` 结构；`tm_list` 为 `{source: "...", target: "..."}` 的历史句对集合 |
| `ext.terminologies` / `ext.sensitives` / `ext.domainHint` | `array` / `string` | 图像与全模态模型的扩展配置：术语表、敏感词、英文领域提示 | `qwen-mt-image-*`, `qwen-mt-uni` | `domainHint` 严格限定为英文，且建议 ≤200 单词；`sensitives` 区分大小写；`terminologies`/`glossary` 字段名不同但语义一致（见下文） |
| `glossary` | `array` | `qwen-mt-uni` 中的术语表字段，等效于 `qwen-mt-image` 的 `terminologies` | `qwen-mt-uni` | > **注意**：文档 2 使用 `terminologies`，文档 3 使用 `glossary`，二者结构相同（`{"src": "...", "tgt": "..."}`），属同一能力的不同字段名，调用时请按对应模型文档使用正确字段 |
| `input.fileUrl` / `input.source_texts` | `string` / `array` | `qwen-mt-uni` 的二选一输入方式：文件 URL 或纯文本 | `qwen-mt-uni` | 必须且只能提供其一；`fileUrl` 需公网可访问、无中文字符、符合格式与尺寸限制 |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，`base_url` 按地域配置（北京/新加坡/美国），`model="qwen-mt-plus"`，将翻译配置放入 `translation_options`。示例见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **图像翻译（`qwen-mt-image-*`）**：调用 `POST /api/v1/services/aigc/image2image/image-synthesis`，`model` 设为 `qwen-mt-image-2.0` 或 `qwen-mt-image`，`input` 包含 `image_url`, `source_lang`, `target_lang`，扩展配置放 `ext`。支持同步（默认）与异步（需加 `X-DashScope-Async: enable` 请求头）。
- **全模态翻译（`qwen-mt-uni`）**：调用 `POST /api/v1/services/aigc/multimodal-generation/generation`，`model="qwen-mt-uni"`，`input` 根据输入类型选择 `fileUrl`（文档/图/音）或 `source_texts`（文本）。同步/异步切换仅依赖 `X-DashScope-Async` 请求头，其余参数完全一致。
- **通用前提**：所有模型均需已 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并确保 `{WorkspaceId}` 已从控制台获取且代入 URL。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），旧 DashScope 公共域名（`dashscope.aliyuncs.com`）虽仍可用，但性能与稳定性较低。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 中的迁移建议。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟；
  - URL：禁止包含中文字符。
- **术语与敏感词**：`qwen-mt-image` 和 `qwen-mt-uni` 的术语表（`terminologies`/`glossary`）最多 100 组；敏感词（`sensitives`）最多 50 个，且**完全匹配、区分大小写**。
- **领域提示**：`domainHint`（图像/全模态）与 `domains`（文本）均为英文描述，前者建议 ≤200 单词，后者在文档 1 示例中被截断（原文末尾为 `profe...`），实际应提供完整英文句子。
- **异步任务管理**：`task_id` 有效期 24 小时，查询接口 RPS 默认为 1；译后文件 URL（`TranslatedFileUrl`）同样有效期 24 小时，需及时下载。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


