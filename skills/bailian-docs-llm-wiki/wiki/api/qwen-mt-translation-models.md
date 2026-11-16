# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖纯文本、多模态文档（PDF/DOCX/PPTX等）及图像三大输入场景，支持领域适配、术语干预、翻译记忆等企业级定制功能。所有模型均通过统一的 MaaS 域名体系提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)或 DashScope 原生协议调用，适用于高精度、高保真、多格式本地化需求。

## 支持的模型与功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，提供术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）能力。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-uni`**：全模态翻译模型，支持文本、PDF、DOCX、PPTX、XLSX、HTML、Markdown、PNG/JPG、MP3/WAV 等输入，输出保持原始格式；提供同步/异步双模式，支持 `glossary`（术语表）、`sensitives`（敏感词过滤）、`domainHint`（英文领域提示）等扩展能力。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。
- **`qwen-mt-image-2.0` / `qwen-mt-image`**：专用图像翻译模型，精准识别并翻译图中文字，保留排版与视觉结构；支持主体分割（`imageSegment`）、敏感词过滤（`sensitives`）和术语干预（`terminologies`）。其中 `qwen-mt-image-2.0` 支持任意语种互译，而 `qwen-mt-image` 仅支持源/目标语言至少一方为中文或英文。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。

> **注意**：`qwen-mt-image` 模型**必须使用异步调用**（即请求头需含 `X-DashScope-Async: enable`），而 `qwen-mt-image-2.0` 同时支持同步与异步；该差异在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中明确说明，但未在 `qwen-mt-uni` 文档中体现，开发者需按模型严格区分调用方式。

## 关键参数

| 参数 | 类型 | 说明 | 所属模型 |
|------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语言代码（如 `zh`, `en`）或全称（如 `Chinese`, `English`），部分模型支持 `auto` 自动检测 | 全部 |
| `translation_options` | `object` | [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)专用封装对象，包含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` 等字段 | `qwen-mt-plus` |
| `ext.domainHint` | `string` | 英文领域提示（≤200 单词），用于引导译文风格；**所有模型均仅支持英文输入** | `qwen-mt-uni`, `qwen-mt-image-*` |
| `ext.glossary` / `ext.terminologies` | `array` | 术语干预：`qwen-mt-uni` 使用 `glossary: [{"src":"...", "tgt":"..."}]`；`qwen-mt-image-*` 使用 `terminologies` 同名结构 | `qwen-mt-uni`, `qwen-mt-image-*` |
| `ext.sensitives` | `array<string>` | 敏感词列表（大小写敏感），完全匹配时保留原文不翻译 | `qwen-mt-uni`, `qwen-mt-image-*` |
| `ext.config.imageSegment` | `boolean` | 图像主体分割开关：`true` 时跳过人物/商品/Logo 上的文字翻译；旧参数 `skipImgSegment` 已弃用但兼容 | `qwen-mt-image-*` |

## 使用方式

- **OpenAI 兼容调用（仅 `qwen-mt-plus`）**：  
  设置 `base_url` 为地域专属域名（如北京：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），通过 `chat.completions.create` 提交 `messages` 和 `extra_body={"translation_options": {...}}`。需确保已配置 `DASHSCOPE_API_KEY` 环境变量。

- **DashScope 原生调用（`qwen-mt-uni`, `qwen-mt-image-*`）**：  
  - **同步调用**：`POST /api/v1/services/aigc/...`，直接返回结果（文本或文件 URL）；  
  - **异步调用**：添加请求头 `X-DashScope-Async: enable` 获取 `task_id`，再 `GET /api/v1/tasks/{task_id}` 轮询状态。  
  > **注意**：`qwen-mt-image` 模型**不支持同步调用**，强制要求异步流程；此限制在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中明确强调，与 `qwen-mt-uni` 的灵活模式存在关键差异。

- **地域与域名**：  
  推荐使用业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），替代旧版 `dashscope.aliyuncs.com`；各模型对地域支持略有不同（如 `qwen-mt-image` 仅支持华北2（北京）和新加坡），具体请以各模型文档为准。

## 限制和注意事项

- **输入限制**：  
  - `qwen-mt-uni`：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟；  
  - `qwen-mt-image-*`：图像尺寸 15–8192 px，宽高比 1:10 至 10:1，大小 ≤100 MB；  
  - 所有模型的 URL 地址中**禁止包含中文字符**。

- **语言与功能约束**：  
  - `qwen-mt-image` 不支持非中/英语种间直译（如日→韩），而 `qwen-mt-image-2.0` 无此限制；  
  - `domainHint` 在全部模型中**仅接受英文输入**，中文提示将导致行为未定义；  
  - `qwen-mt-plus` 的 `domains` 字段在文档 1 示例中被截断（末尾为 `profe...`），实际应为完整英文描述，建议参考 [翻译能力（Qwen-MT）](../../raw/model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md) 获取规范用法。

- **Token 计费与用量**：  
  `qwen-mt-uni` 返回详细 `usage` 统计（含 `input_tokens_details` 按模态拆分）；`qwen-mt-image-*` 仅返回 `image_count`；`qwen-mt-plus`（OpenAI 兼容）暂不返回用量字段，计费依据为请求次数与模型规格。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)


