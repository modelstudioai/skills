# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业化机器翻译能力，覆盖文本、图像、多格式文档及音频等多模态输入场景。模型通过统一架构实现高保真翻译与原格式重构，支持术语干预、领域提示、翻译记忆等企业级定制功能。开发者可根据输入类型（纯文本/图片/文件）和延迟要求（同步/异步）选择对应模型与调用方式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，基于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，支持 `source_lang`/`target_lang` 指定、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-uni`**：全模态翻译模型，支持文本（`source_texts`）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown/图像/音频（`fileUrl`）等多种输入格式，输出保持原始格式（如译后 PDF、带文字替换的 JPG）。提供同步与异步两种调用模式。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。
- **`qwen-mt-image-2.0` 与 `qwen-mt-image`**：专用图像翻译模型，精准识别并翻译图中文字，保留排版与图像尺寸。`qwen-mt-image-2.0` 支持任意语种互译；`qwen-mt-image` 仅支持源或目标语言至少有一方为中文或英文。二者均支持 `imageSegment` 主体分割、敏感词过滤（`sensitives`）和术语干预（`terminologies`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。

> **注意**：`qwen-mt-image` 模型**必须使用异步调用**（即请求头需含 `X-DashScope-Async: enable`），而 `qwen-mt-image-2.0` 同时支持同步与异步。该限制在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中明确说明，但未在 `qwen-mt-uni` 文档中体现，属模型级行为差异，非文档矛盾。

## 关键参数

| 参数名 | 类型 | 说明 | 所属模型 |
|--------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语言代码或全称（如 `"zh"`、`"Chinese"`、`"auto"`）；`qwen-mt-plus` 和 `qwen-mt-uni` 支持 `auto` 自动检测；`qwen-mt-image` 对语种组合有限制 | 全部 |
| `translation_options` | `object` | `qwen-mt-plus` 专用顶层字段，包裹 `source_lang`、`target_lang`、`terms`、`tm_list`、`domains` | `qwen-mt-plus` |
| `terms` / `terminologies` | `array` | 术语干预：`qwen-mt-plus` 使用 `terms`（结构为 `{"source": "...", "target": "..."}`）；`qwen-mt-image` 和 `qwen-mt-uni` 使用 `terminologies`（结构为 `{"src": "...", "tgt": "..."}`） | `qwen-mt-plus`, `qwen-mt-image`, `qwen-mt-uni` |
| `tm_list` | `array` | 翻译记忆列表，仅 `qwen-mt-plus` 支持，用于上下文一致性控制 | `qwen-mt-plus` |
| `domains` | `string` | 领域提示（英文），仅 `qwen-mt-plus` 支持；`qwen-mt-uni` 和 `qwen-mt-image` 使用 `ext.domainHint`（同样限英文） | `qwen-mt-plus` |
| `ext.domainHint` | `string` | 领域提示（英文），`qwen-mt-uni` 和 `qwen-mt-image` 的标准字段，建议 ≤200 英文单词 | `qwen-mt-uni`, `qwen-mt-image` |
| `ext.sensitives` | `array<string>` | 敏感词过滤（大小写敏感），匹配原文本后直接保留不翻译 | `qwen-mt-uni`, `qwen-mt-image` |
| `ext.config.imageSegment` | `boolean` | 图像主体分割开关（默认 `false`）：`true` 时不翻译人物/商品/Logo 上的文字；旧参数 `skipImgSegment` 已废弃但兼容 | `qwen-mt-image` |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 OpenAI SDK，设置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），通过 `extra_body={"translation_options": {...}}` 传参。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供完整 Python/Node.js/curl 示例。
- **多模态翻译（`qwen-mt-uni`）**：使用 DashScope 标准协议，`POST /api/v1/services/aigc/multimodal-generation/generation`。同步调用直接返回结果；异步调用需添加请求头 `X-DashScope-Async: enable` 获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}`。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确区分同步/异步流程与响应结构。
- **图像翻译（`qwen-mt-image-2.0` / `qwen-mt-image`）**：使用 DashScope 图像接口，`POST /api/v1/services/aigc/image2image/image-synthesis`。同步调用适用于小图；大图或高并发场景推荐异步。注意 `qwen-mt-image` 必须异步。[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 给出各参数的精确约束（如图像尺寸 15–8192px、宽高比 1:10–10:1）。

## 限制和注意事项

- **地域与域名**：所有模型均推荐使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。旧域名虽仍可用，但性能与稳定性较低（见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)）。
- **输入限制**：
  - `qwen-mt-uni`：单文件 ≤100 MB，文档 ≤200 页，音频 3 秒–60 分钟；URL 不得含中文。
  - `qwen-mt-image`：图像 ≤100 MB，宽高 15–8192 px，宽高比 1:10–10:1；URL 不得含中文。
- **语言与格式**：`domainHint` 和 `domains` 字段**仅支持英文输入**，中文提示将导致效果下降或报错。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 和 `qwen-mt-image` 的 `terminologies` 均要求 `src`/`source` 与 `source_lang` 一致、`tgt`/`target` 与 `target_lang` 一致；`sensitives` 区分大小写且需完全匹配。
- **异步任务生命周期**：`task_id` 及其返回的 `TranslatedFileUrl` / `image_url` 有效期均为 **24 小时**，需及时下载保存。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)


