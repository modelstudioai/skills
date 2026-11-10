# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。它通过统一的模态识别、智能路由、内容抽取与原格式重构链路实现跨模态保形翻译，并提供同步与异步两种调用模式以适配不同耗时场景。该模型严格遵循 DashScope 标准协议，所有接口行为与错误处理机制均在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或变体。
- **输入模态**：支持字符串（标量或数组）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV 共 10 类输入格式；输出格式严格对应输入类型（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`）。
- **调用模式**：
  - **同步调用**：适用于文本、小图、短音频等低延迟场景，请求后直接返回结果（含 `output.Data` 或错误 `code`）；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，先获 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 获取最终结果；适用于大文档（≤200页）、长音频（3秒–60分钟）等高耗时任务。
- **关键能力**：自动语言识别（可覆盖 `source_lang`）、领域提示（`domainHint`，**仅支持英文**）、敏感词保留（`sensitives`）、术语表强制对齐（`glossary`）、图像主体分割控制（`config.imageSegment`）。

> **注意**：原始文档中“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转换为 OOXML 格式”这一限制，在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确列为前提条件，但未说明是否已支持在线转换。开发者应主动完成格式预处理，避免因格式不兼容导致 `InvalidParameter` 错误。

## 关键参数

| 参数 | 位置 | 必选性 | 说明 |
|------|------|--------|------|
| `model` | request body | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` 或 `input.source_texts` | request body > `input` | ⚠️ 二选一 | `fileUrl`：公网可访问 HTTPS URL（无中文字符，≤100 MB）；`source_texts`：`string` 或 `string[]`，批量保持顺序与形状 |
| `input.target_lang` | request body > `input` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[支持语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | request body > `input` | ❌ | 源语言代码（如 `zh`），不填则自动识别 |
| `input.ext.domainHint` | request body > `input.ext` | ❌ | 英文领域描述（≤200 单词），影响译文风格；**非英文内容将被忽略** |
| `input.ext.glossary` | request body > `input.ext` | ❌ | 最多 100 组 `{"src": "...", "tgt": "..."}`，用于术语强制对齐 |
| `input.ext.sensitives` | request body > `input.ext` | ❌ | 最多 50 个区分大小写的敏感词，匹配即原文保留 |
| `input.ext.config.imageSegment` | request body > `input.ext.config` | ❌ | 仅对图像生效：`true` 跳过人物/Logo等主体文字翻译；默认 `false` |

## 使用方式

1. **前置准备**：确保已[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，并设置环境变量 `DASHSCOPE_API_KEY`。
2. **构造请求**：
   - 同步调用：`POST /api/v1/services/aigc/multimodal-generation/generation`，Header 含 `Authorization: Bearer <key>` 和 `Content-Type: application/json`；
   - 异步调用：同上，**额外添加 Header** `X-DashScope-Async: enable`。
3. **解析响应**：
   - 同步成功：检查顶层是否存在 `output`，若存在且 `output.Success === true`，则结果在 `output.Data`（`TranslatedTexts` 或 `TranslatedFileUrl`）；
   - 同步失败：检查顶层是否存在 `code` 字段（如 `InvalidParameter`）；
   - 异步成功：轮询 `/api/v1/tasks/{task_id}`，当 `output.task_status === "SUCCEEDED"` 且 `output.Success === true` 时，结果在 `output.Data`；
   - 异步失败：`output.task_status === "SUCCEEDED"` 但 `output.Success === false`，错误原因见 `output.Code` / `output.Message`。
4. **用量统计**：`usage` 对象始终位于响应顶层（同步/异步均返回），含 `input_tokens`、`output_tokens` 及按模态细分的 `*_tokens_details` 字段，用于计费与调试。

完整请求示例与响应结构详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX/XLSX ≤200 页；音频时长 3 秒–60 分钟；URL 不得含中文字符。
- **格式限制**：不支持 `.doc` / `.ppt` 等旧版二进制格式，必须转为 `.docx` / `.pptx`。
- **领域提示**：`domainHint` **仅接受英文输入**，中文或其他语言将导致提示失效；该约束在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确强调。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：`task_id` 有效期 24 小时；查询接口默认 RPS=1；译后文件 URL 有效期亦为 24 小时，需及时下载。
- **错误处理差异**：同步失败返回顶层 `code`/`message`；异步失败仍返回 `task_status: "SUCCEEDED"`，**必须依赖 `output.Success` 判断业务成败**——此关键逻辑差异已在原始文档中反复强调，开发者不可忽略。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


