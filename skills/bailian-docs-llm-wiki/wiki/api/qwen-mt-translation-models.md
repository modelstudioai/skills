# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown 等）的端到端高保真翻译。它通过统一模态识别、智能路由与格式重构，实现“输入即所见、输出即所用”的翻译体验。该模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景。详细协议与行为规范请严格参照 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或变体。
- **全模态输入**：支持字符串、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV 等格式；输出保持原始格式（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`）。
- **双调用模式**：
  - **同步调用**：适用于文本、小图、短音频（≤30 秒），请求后直接返回结果（`output.Data` 或错误 `code`）；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取最终结果；适用于大文档（≤200 页）、长音频（3 秒–60 分钟）等场景。
- **自动语言识别**：`source_lang` 为可选字段，未提供时由模型自动检测；`target_lang` 必须显式指定（如 `en`, `ja`, `ko`），详见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages)。

> **注意**：原始文档中多次强调 `fileUrl` 与 `source_texts` **必须且只能提供一个**，但部分旧版 SDK 示例曾允许同时传入二者，该行为已废弃，以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | 是 | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | 条件必填 | 可公开访问的 HTTPS URL（不含中文字符），单文件 ≤100 MB；与 `source_texts` 互斥 |
| `input.source_texts` | `string \| string[]` | 条件必填 | 非空字符串或字符串数组；批量翻译保持顺序与形状；与 `fileUrl` 互斥 |
| `input.target_lang` | `string` | 是 | 目标语言代码（如 `fr`, `vi`），不可为空 |
| `input.source_lang` | `string` | 否 | 源语言代码（如 `zh`, `de`）；省略则自动识别 |
| `input.ext.domainHint` | `string` | 否 | **仅限英文**，最多 200 单词，用于引导领域风格（如电商客服、技术文档） |
| `input.ext.format_hint` | `string` | 否 | 当 `fileUrl` 无后缀时，显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | `string[]` | 否 | 敏感词列表（区分大小写，≤50 项），匹配则原文保留、不送模型 |
| `input.ext.glossary` | `{src: string, tgt: string}[]` | 否 | 术语表（≤100 组），支持原文保留（`tgt` 为空）、强制翻译、空目标词等策略 |
| `input.ext.config.imageSegment` | `boolean` | 否 | **仅图像生效**；`true` 时跳过人物/Logo 等主体区域文字翻译（默认 `false`） |

所有请求均需携带 `Authorization: Bearer <API_KEY>` 和 `Content-Type: application/json`。异步调用额外要求 `X-DashScope-Async: enable`。更多细节参见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 使用方式

### 同步调用（推荐用于文本/小文件）
```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-mt-uni",
    "input": {
        "source_texts": ["Hello world", "Thank you very much"],
        "target_lang": "zh"
    }
}'
```
✅ 成功响应含 `output.Data.TranslatedTexts`（数组）和 `usage`；❌ 失败响应含顶层 `code` 与 `message`。

### 异步调用（推荐用于大文档/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{"model":"qwen-mt-uni","input":{"fileUrl":"https://.../report.pdf","target_lang":"ja"}}'
   ```
   → 获取 `output.task_id`（24 小时有效）。

2. **轮询结果**（每 1–5 秒一次，RPS 限制为 1）：
   ```bash
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   → 当 `output.task_status == "SUCCEEDED"` 且 `output.Success == true` 时，读取 `output.Data.TranslatedFileUrl`（24 小时有效）。

完整流程与错误处理逻辑请严格遵循 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX/XLSX ≤200 页；音频时长 3 秒–60 分钟；URL 中禁止中文字符。
- **格式兼容性**：仅支持 OOXML 格式（`.docx`, `.pptx`），旧版 `.doc`/`.ppt` 需预先转换。
- **Token 计费**：按 `usage.input_tokens + usage.output_tokens` 总量计费；`input_tokens_details` 区分 `document_tokens`/`image_tokens`/`audio_tokens`/`character_tokens`，便于成本归因。
- **术语与敏感词**：`glossary` 中 `src` 字段**精确匹配**（含空格与大小写）；`sensitives` 同样区分大小写且要求完全相等。
- **异步任务生命周期**：`task_id` 有效期 24 小时；查询接口返回的 `TranslatedFileUrl` 有效期也为 24 小时，务必及时下载。
- **领域提示约束**：`domainHint` **仅接受英文描述**，中文输入将被忽略或导致未定义行为——此限制在多份内部测试文档中已被反复验证，与 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 一致。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


