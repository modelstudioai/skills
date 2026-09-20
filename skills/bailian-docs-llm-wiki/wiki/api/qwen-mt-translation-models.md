# qwen mt translation models

Qwen MT 翻译模型系列是阿里云百炼平台提供的多模态、多场景机器翻译能力集合，涵盖全模态文档翻译（`qwen-mt-uni`）、通用文本翻译（`qwen-mt-plus`）和专业图像翻译（`qwen-mt-image-2.0`/`qwen-mt-image`）三类核心模型。各模型统一采用 DashScope API 协议，支持同步与[异步调用](../concepts/asynchronous-invocation.md)模式，并提供术语干预、领域提示、敏感词过滤等企业级定制能力。开发者可根据输入类型（纯文本、文件、图像）和精度/性能需求选择对应模型。

## 支持的模型与功能

- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等 12+ 种格式输入，自动识别模态并执行端到端翻译与原格式重构。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。
- **`qwen-mt-plus`**：通用文本翻译模型，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适用于 API 集成度高、已有 OpenAI SDK 生态的场景，支持 `translation_options` 中的 `source_lang`/`target_lang`、`terms`（术语表）、`tm_list`（翻译记忆）、`domains`（领域提示）等参数。
- **`qwen-mt-image-2.0` 与 `qwen-mt-image`**：专用图像翻译模型，精准识别并翻译图像内文字，保留原始排版与视觉结构；其中 `qwen-mt-image-2.0` 支持全部 55 种语言互译，而 `qwen-mt-image` 仅支持源或目标语言至少一方为中/英文的组合。该模型使用独立的 `/image2image/image-synthesis` 接口路径，与 `qwen-mt-uni` 的 `/multimodal-generation/generation` 路径不兼容。> **注意**：文档 3 明确指出 `qwen-mt-image` 模型**必须**使用 `X-DashScope-Async: enable` 请求头（即仅支持异步），而文档 1 中 `qwen-mt-uni` 对图像输入支持同步调用——二者调用路径、参数结构及同步性约束存在本质差异，不可混用。

## 关键参数

| 参数 | 说明 | 所属模型 | 备注 |
|------|------|----------|------|
| `model` | 必填，模型标识符 | 全部 | 值为 `qwen-mt-uni` / `qwen-mt-plus` / `qwen-mt-image-2.0` / `qwen-mt-image` |
| `source_lang`, `target_lang` | 源/目标语言代码或全称（如 `zh` / `Chinese` / `auto`） | 全部 | `qwen-mt-image` 要求至少一者为中/英文；`qwen-mt-uni` 和 `qwen-mt-plus` 支持更广语种范围 |
| `fileUrl`（`qwen-mt-uni`） / `image_url`（`qwen-mt-image-*`） / `messages.content`（`qwen-mt-plus`） | 输入数据载体 | 各自专属 | 三者互斥，不可跨模型复用字段名 |
| `ext.glossary`（`qwen-mt-uni`） / `translation_options.terms`（`qwen-mt-plus`） / `ext.terminologies`（`qwen-mt-image-*`） | 术语干预列表 | 全部 | 均为 `{"src": "...", "tgt": "..."}` 数组，但字段路径不同 |
| `ext.domainHint` / `translation_options.domains` / `ext.domainHint` | 领域提示（英文，≤200 单词） | 全部 | 文档 1 和文档 3 均强调“**只支持英文**”，文档 2 示例中 `domains` 字段值被截断，实际应为完整英文句子 |
| `ext.sensitives` / `translation_options.sensitives` / `ext.sensitives` | 敏感词列表（大小写敏感，最多 50 项） | 全部 | `qwen-mt-uni` 和 `qwen-mt-image-*` 字段名一致；`qwen-mt-plus` 在文档 2 中未显式定义该字段，但其 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)实际支持（需通过 `extra_body` 透传） |

> **注意**：`qwen-mt-image-*` 模型的 `config.imageSegment` 参数在文档 3 中明确标注旧版别名 `skipImgSegment` 已兼容但**不推荐使用**；而文档 1 中同名参数 `config.imageSegment` 仅作用于图像输入场景，逻辑一致，无冲突。

## 使用方式

- **同步调用**：适用于文本、小图、短音频等低延迟场景。  
  - `qwen-mt-uni`：POST `/api/v1/services/aigc/multimodal-generation/generation`，不带 `X-DashScope-Async` 头。  
  - `qwen-mt-image-2.0`：POST `/api/v1/services/aigc/image2image/image-synthesis`，不带 `X-DashScope-Async` 头（`qwen-mt-image` 不支持同步）。  
  - `qwen-mt-plus`：POST `/compatible-mode/v1/chat/completions`（OpenAI 兼容路径），无需额外头。  
- **[异步调用](../concepts/asynchronous-invocation.md)**：适用于大文件、长文档、长音频或高并发轮询场景。  
  - 所有模型均支持：在请求头添加 `X-DashScope-Async: enable`，获取 `task_id` 后轮询 `GET /api/v1/tasks/{task_id}`。  
  - 任务 ID 有效期 24 小时；结果 URL（如 `TranslatedFileUrl` 或 `image_url`）有效期也为 24 小时。  
- **认证与环境**：所有调用均需 `Authorization: Bearer <API_KEY>`，且 API Key 需按地域（北京/新加坡/美东）配置对应 `base_url`。强烈建议迁移至业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。详情见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。

## 限制和注意事项

- **输入限制**：  
  - 单文件 ≤ 100 MB；PDF/DOCX/PPTX/XLSX ≤ 200 页；音频时长 3 秒–60 分钟；图像宽高 15–8192 px，宽高比 1:10 至 10:1。  
  - 所有 URL（`fileUrl`/`image_url`）**禁止含中文字符**；旧格式 `.doc`/`.ppt` 需先转 `.docx`/`.pptx`。  
- **语言与模型约束**：  
  - `qwen-mt-image` 严格限制语种组合（必须含中或英），而 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制。  
  - `qwen-mt-plus` 的 `source_lang` 支持 `"auto"`，但 `qwen-mt-image-*` 的 `source_lang` 也支持 `"auto"`（文档 3 明确列出）。  
- **术语与敏感词**：  
  - `glossary`（`qwen-mt-uni`）、`terms`（`qwen-mt-plus`）、`terminologies`（`qwen-mt-image-*`）三者语义相同，但字段路径不同，集成时需按模型适配。  
  - 所有敏感词匹配均为**全字符串、大小写敏感**，且仅过滤完全一致的原文片段。  
- **错误处理**：  
  - 同步失败返回顶层 `code`/`message`；异步创建失败同理；异步执行失败则 `task_status = SUCCEEDED` 但 `output.Success = false`，需双重判断。错误码详见各文档引用链接，例如 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的错误码章节。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)


