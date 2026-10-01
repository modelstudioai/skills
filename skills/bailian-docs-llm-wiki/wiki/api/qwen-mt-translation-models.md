# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT）的端到端高保真翻译。它通过统一模态识别、智能路由与格式重构链路，实现输入即译、输出即用。该模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景。详细协议规范与行为定义请参见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或历史版本（如 `qwen-mt-zh2en` 等已下线）。
- **全模态输入支持**：文本（`str` / `list[str]`）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV。
- **双模式执行**：
  - **同步调用**：直接返回结果（文本或带签名的译后文件 URL），适合 ≤100 MB 文件或 ≤60 分钟音频；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，先获 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 获取最终结果；任务有效期 24 小时，结果 URL 同样有效期 24 小时。
- **自动语言识别**：`source_lang` 为可选字段，未提供时由模型自动检测；`target_lang` 为必填项，须为 ISO 639-1 代码（如 `zh`, `en`, `ko`, `ja`）。
- **领域与格式增强**：支持 `ext.domainHint`（英文领域提示）、`ext.format_hint`（显式指定无后缀 URL 格式）、`ext.sensitives`（敏感词原文保留）、`ext.glossary`（术语表映射）等扩展能力。

> **注意**：原始文档中提及“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转换为 OOXML 格式”，但 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确未将 `.doc`/`.ppt` 列入支持格式列表，因此该说明仅为兼容性提醒，非功能支持项。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | request body | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | request body → `input` | `string` | ⚠️ 条件必填 | 可公开访问的 HTTPS URL；与 `source_texts` 二选一 |
| `input.source_texts` | request body → `input` | `string \| array<string>` | ⚠️ 条件必填 | 文本输入；与 `fileUrl` 二选一；保持形状一致性 |
| `input.target_lang` | request body → `input` | `string` | ✅ | 目标语言代码（如 `fr`, `es`）；详见[支持语种](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | request body → `input` | `string` | ❌ | 源语言代码；不填则自动识别 |
| `input.ext.domainHint` | request body → `input.ext` | `string` | ❌ | **仅支持英文**；最多 200 单词；用于引导领域风格 |
| `input.ext.format_hint` | request body → `input.ext` | `string` | ❌ | 当 `fileUrl` 无后缀时显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | request body → `input.ext` | `array<string>` | ❌ | 敏感词列表（区分大小写，最多 50 个）；完全匹配则保留原文 |
| `input.ext.glossary` | request body → `input.ext` | `array<{src: string, tgt: string}>` | ❌ | 术语表（最多 100 组）；支持空 `tgt` 表示跳过翻译 |
| `input.ext.config.imageSegment` | request body → `input.ext.config` | `boolean` | ❌ | **仅图像生效**；`true` 时跳过人物/Logo 等主体区域文字翻译 |

## 使用方式

1. **前置准备**：确保已[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`。
2. **选择调用模式**：
   - 同步：发送 `POST /api/v1/services/aigc/multimodal-generation/generation`，**不加** `X-DashScope-Async` 头；
   - 异步：同上接口，**必须添加** `X-DashScope-Async: enable` 请求头。
3. **构造请求体**：按需提供 `fileUrl` 或 `source_texts`，必填 `target_lang`，其余扩展字段按需补充。
4. **处理响应**：
   - 同步成功：检查顶层 `output.Success === true`，结果在 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）；
   - 同步失败：检查顶层 `code` 字段（如 `"InvalidParameter"`）；
   - 异步创建成功：提取 `output.task_id`；
   - 异步查询结果：轮询 `GET /api/v1/tasks/{task_id}`，待 `output.task_status === "SUCCEEDED"` 后，**必须验证 `output.Success === true`** 才视为业务成功（`output.Success === false` 表示任务执行完毕但翻译失败）。

完整请求示例（同步图片翻译）见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤ 100 MB；PDF/DOCX/PPTX ≤ 200 页；音频时长 3 秒～60 分钟。
- **URL 要求**：`fileUrl` 必须为 HTTPS 协议，且路径中**不能含中文字符**（否则返回 `InvalidParameter`）。
- **Token 计费**：按 `usage.input_tokens` 计费；用量明细按模态拆分（`image_tokens`, `document_tokens`, `audio_tokens`, `character_tokens`）。
- **术语表与敏感词**：`glossary` 和 `sensitives` 均区分大小写，且仅做精确字符串匹配（非子串/模糊匹配）。
- **异步轮询建议**：默认 RPS 限流为 1，请避免高频轮询；如需实时通知，应配置[异步任务回调](../../raw/model-api-reference/more-about-models/async-task-api.md)。
- **错误排查**：所有失败响应均含 `request_id`，可用于工单提报；常见错误码详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的错误码章节。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


