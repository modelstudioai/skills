# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。其核心能力基于统一模态识别、智能路由与原格式重构，兼顾语义准确性与排版/结构一致性。模型提供同步与异步两种调用模式，分别适用于低延迟短任务与长耗时大文件场景。详细协议规范与行为定义请参阅 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或历史版本（如 `qwen-mt` 旧版已下线）。
- **输入模态**：支持字符串（单条或数组）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV 共 10 类格式；输出格式严格对应输入类型（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`）。
- **调用模式**：
  - **同步调用**：请求后阻塞等待结果，适合文本、小图、短音频（≤30 秒）等低延迟场景；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取结果，适用于大文档（>200 页）、长音频（3 秒–60 分钟）等长耗时任务。
- **关键能力**：
  - 自动语言识别（可显式指定 `source_lang`）；
  - 领域提示（`ext.domainHint`，**仅支持英文**）；
  - 敏感词保护（`ext.sensitives`，完全匹配则保留原文）；
  - 术语表控制（`ext.glossary`，支持源→目标映射）；
  - 图像主体分割（`ext.config.imageSegment=true` 时跳过人物/Logo 等主体文字翻译）。

> **注意**：原始文档中“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转换为 OOXML 格式”这一说明与当前平台实际兼容性存在偏差——实测 `.doc` 文件上传会直接返回 `InvalidFormat` 错误，而 `.ppt` 文件虽能接收但译文质量显著下降。建议严格遵循 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确列出的格式清单，避免使用非标格式。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `input` 外层 | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `fileUrl` | `input` 内 | `string` | ⚠️（条件必填） | 可公开访问的 HTTPS URL；与 `source_texts` **二选一**；URL 不得含中文字符 |
| `source_texts` | `input` 内 | `string \| array<string>` | ⚠️（条件必填） | 文本输入；与 `fileUrl` **二选一**；批量时保持顺序与形状 |
| `target_lang` | `input` 内 | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[支持语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `source_lang` | `input` 内 | `string` | ❌（可选） | 源语言代码；不填则自动识别 |
| `ext.domainHint` | `input.ext` 内 | `string` | ❌ | 英文领域描述（≤200 单词），影响译文风格；**不支持中文** |
| `ext.format_hint` | `input.ext` 内 | `string` | ❌ | 当 `fileUrl` 无后缀时显式指定格式（如 `"pdf"`, `"image"`） |
| `ext.sensitives` | `input.ext` 内 | `array<string>` | ❌ | 敏感词列表（区分大小写，≤50 项），完全匹配则保留原文 |
| `ext.glossary` | `input.ext` 内 | `array<{src: string, tgt: string}>` | ❌ | 术语表（≤100 组），支持空 `tgt` 表示保留源词 |
| `ext.config.imageSegment` | `input.ext.config` 内 | `boolean` | ❌ | **仅图像生效**；`true` 时跳过主体文字翻译（默认 `false`） |

## 使用方式

1. **前置准备**：确保已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，且环境变量 `DASHSCOPE_API_KEY` 已设置。
2. **选择端点**：  
   - 同步：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`  
   - 异步：同上，但请求头必须包含 `X-DashScope-Async: enable`
3. **构造请求**：  
   - 设置 `Content-Type: application/json` 和 `Authorization: Bearer <API_KEY>`；  
   - `input` 中**仅提供 `fileUrl` 或 `source_texts` 之一**；  
   - `target_lang` 必须显式指定。
4. **处理响应**：  
   - **同步成功**：检查顶层 `output.Success === true`，结果在 `output.Data`（`TranslatedTexts` 或 `TranslatedFileUrl`）；  
   - **异步成功**：轮询 `GET /api/v1/tasks/{task_id}`，当 `output.task_status === "SUCCEEDED"` 且 `output.Success === true` 时读取 `output.Data`；  
   - **失败判断**：同步看顶层 `code` 字段；异步需同时检查 `output.task_status === "SUCCEEDED"` 和 `output.Success === false`（此时错误信息在 `output.Code`/`output.Message`）。  
   完整交互逻辑与字段定义详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；URL 不得含中文字符。
- **[Token](../concepts/token.md) 计费**：按 `usage.input_tokens` 计费；用量明细（`input_tokens_details`）按模态拆分（`document_tokens`/`image_tokens`/`audio_tokens`/`character_tokens`），便于成本归因。
- **时效性**：  
  - 异步 `task_id` 有效期 24 小时；  
  - 异步返回的 `TranslatedFileUrl` 有效期 24 小时；  
  - 建议及时下载并持久化存储译后文件。
- **安全与合规**：  
  - `ext.sensitives` 匹配严格区分大小写且要求完全相等；  
  - `ext.glossary` 中 `src` 字段若含空格或标点，需确保与原文完全一致；  
  - 所有输入内容经服务端解析，敏感数据请勿传入未脱敏原文。
- **调试建议**：失败时优先检查 `request_id` 并结合 [错误码文档](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-errors) 排查；异步任务轮询频率建议 ≤1 QPS，高频需求请配置回调（见 [async-task-api.md](../../raw/model-api-reference/more-about-models/async-task-api.md)）。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


