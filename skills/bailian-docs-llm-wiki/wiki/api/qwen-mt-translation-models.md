# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态机器翻译模型，支持文本、图片、音频及各类办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown 等）的端到端高保真翻译。它通过统一的模态识别、[智能路由](../concepts/model-routing.md)与格式重构链路，实现“输入即所见、输出即所用”的一体化翻译体验。模型提供同步与异步两种调用模式，分别适用于短耗时与长耗时任务场景，接口遵循 DashScope 标准协议。详细设计与行为规范请参阅 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一公开模型**：当前仅开放 `qwen-mt-uni` 模型，无 `qwen-mt-base` 或 `qwen-mt-pro` 等变体；所有文档中提及的 Qwen-MT 系列能力均指向该模型。
- **全模态输入支持**：包括纯文本（`str` / `list[str]`）、图像（`.jpg`, `.png`）、音频（`.mp3`, `.wav`）及 7 类文档格式（`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.txt`, `.html`, `.md` 等），输出保持原始格式与结构。
- **双模式执行**：
  - **同步调用**：适用于文本、小图、短音频等低延迟场景，请求后直接返回结果（含 `output.Data.TranslatedTexts` 或 `TranslatedFileUrl`）；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，返回 `task_id` 后轮询查询，适用于大文档（≤200页）、长音频（3秒–60分钟）等高耗时任务。
- **智能辅助能力**：支持自动语言检测（`source_lang` 可选）、领域提示（`ext.domainHint`，**仅限英文**）、敏感词保护（`ext.sensitives`）、术语表控制（`ext.glossary`）及图像主体分割开关（`ext.config.imageSegment`）。

> **注意**：原始文档中未提及其他 Qwen-MT 子型号（如 `qwen-mt-text-only`），且所有功能描述均集中于 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)，因此不应假设存在独立文本专用模型或非 Uni 架构变体。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️ 条件必填 | 可访问的 HTTPS URL（不含中文字符），单文件 ≤100 MB；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| string[]` | ⚠️ 条件必填 | 非空字符串或数组；与 `fileUrl` 二选一；批量翻译保持顺序与形状 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `"en"`, `"ja"`），详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中语种列表 |
| `input.source_lang` | `string` | ❌ | 源语言代码（如 `"zh"`），不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | **仅支持英文**，最多 200 单词，用于引导领域风格（例：`"These sentences are from seller-buyer conversations..."`） |
| `input.ext.format_hint` | `string` | ❌ | 当 `fileUrl` 无后缀时显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | `string[]` | ❌ | 敏感词列表（区分大小写，≤50项），完全匹配时保留原文不翻译 |
| `input.ext.glossary` | `{src: string, tgt: string}[]` | ❌ | 术语表（≤100组），支持原文保留（`tgt=""`）、强制翻译、空目标词等策略 |
| `input.ext.config.imageSegment` | `boolean` | ❌ | **仅图像生效**；`true` 时跳过人物/Logo等主体区域文字翻译（默认 `false`） |

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
- 成功响应顶层含 `output` 对象，结果位于 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）；
- 失败响应顶层含 `code` 和 `message` 字段（如 `InvalidParameter: missing required field: input.target_lang`）。

### 异步调用（必需用于大文档/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{"model":"qwen-mt-uni","input":{"fileUrl":"...","target_lang":"zh"}}'
   ```
   - 响应含 `output.task_id`（24 小时有效）和 `output.task_status`（初始为 `"QUEUED"` 或 `"RUNNING"`）。

2. **轮询查询结果**（使用 `task_id` 调用查询接口）：
   - 直至 `output.task_status == "SUCCEEDED"`；
   - 若 `output.Success == true`，结果在 `output.Data`；若 `false`，失败原因在 `output.Code` / `output.Message`。

完整流程与错误处理逻辑详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX/XLSX 文档 ≤200 页；音频时长 3 秒–60 分钟；URL 中禁止含中文字符。
- **格式兼容性**：仅支持 OOXML 格式（`.docx`, `.pptx`），旧版 `.doc` / `.ppt` 需预先转换。
- **领域提示约束**：`ext.domainHint` **严格限定为英文**，输入中文将导致提示失效（非报错）。
- **术语表行为**：`ext.glossary` 当前以 Prompt 注入方式实现，不保证 100% 强制替换，尤其在上下文强约束场景下可能被模型忽略。
- **计费依据**：按 `usage.input_tokens` 计费，`input_tokens_details` 细分 `document_tokens` / `image_tokens` / `audio_tokens` 等，开发者需关注多模态输入的实际 token 消耗。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


