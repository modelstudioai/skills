# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态机器翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT）的端到端高保真翻译。它通过统一模态识别、智能路由与原格式重构技术，实现“输入即所见、输出即所用”的翻译体验。该模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景。详细协议规范请参阅 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或变体。
- **全模态输入**：支持字符串（单条或数组）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV 等格式；输出保持同类型（如输入 `.pdf` → 输出 `.pdf`）。
- **双模式调度**：
  - **同步调用**：适用于文本、小图（≤100 MB）、短音频（3 秒–60 分钟），请求后直接返回结果（`output.Data` 或错误 `code`）；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取最终结果；适用于大文档（≤200 页）或长音频等耗时场景。  
  具体行为差异详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中“同步调用”与“异步调用”章节。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️ 条件必填 | 可公开访问的 HTTPS URL（不含中文字符），服务端自动识别模态；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| array<string>` | ⚠️ 条件必填 | 文本输入，支持单条或批量（保持顺序与形状）；与 `fileUrl` 二选一 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），[完整列表见官方文档](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | `string` | ❌ | 源语言代码（如 `zh`），不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | **仅英文**领域提示（≤200 单词），用于引导译文风格（例：`"These sentences are from medical reports..."`） |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 术语表（≤100 组），支持原文保留、强制翻译或空目标（`{"src": "API", "tgt": ""}`） |
| `input.ext.sensitives` | `array<string>` | ❌ | 敏感词列表（≤50 个，区分大小写），匹配则原样保留不翻译 |
| `input.ext.config.imageSegment` | `boolean` | ❌ | **仅图像生效**；`true` 时跳过人物/Logo等主体区域文字翻译（默认 `false`） |

> **注意**：`domainHint` 字段在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确要求“只支持英文”，若传入中文将被忽略且无报错，开发者需自行校验。

## 使用方式

1. **前置准备**：确保已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐通过环境变量 `DASHSCOPE_API_KEY` 设置。
2. **构造请求**：
   - **Endpoint**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
     - `{WorkspaceId}` 需替换为实际工作区 ID（见 [Regions 文档](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）
   - **Headers**：`Authorization: Bearer <your_api_key>` + `Content-Type: application/json`；异步调用额外加 `X-DashScope-Async: enable`
3. **选择模式**：
   - 同步：等待响应，检查顶层是否存在 `output`（成功）或 `code`（失败）；
   - 异步：第一步获 `task_id`，第二步用 `GET /api/v1/tasks/{task_id}` 轮询，直到 `output.task_status = "SUCCEEDED"` 且 `output.Success = true`。
4. **解析结果**：
   - 文本输入 → 查 `output.Data.TranslatedTexts`
   - 文件输入 → 查 `output.Data.TranslatedFileUrl`（带签名，24 小时有效）
   - Token 用量始终在响应顶层 `usage` 字段中，按 `input_tokens` 计费

完整示例与响应结构可参考 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的“同步调用”与“异步调用”章节。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；URL 不得含中文字符。
- **格式兼容性**：仅支持 OOXML 格式（`.docx`/`.pptx`），旧版 `.doc`/`.ppt` 需先转换。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：`task_id` 有效期 24 小时；查询接口默认限流 1 QPS；译后文件 URL 同样 24 小时有效。
- **敏感词与术语**：`sensitives` 区分大小写且要求**完全匹配**；`glossary` 中空 `tgt` 值表示保留原文（非跳过）。
- **错误处理**：同步失败返回 `code`/`message`；异步失败时 `task_status` 仍为 `"SUCCEEDED"`，必须检查 `output.Success === false` 及 `output.Code`/`output.Message`。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


