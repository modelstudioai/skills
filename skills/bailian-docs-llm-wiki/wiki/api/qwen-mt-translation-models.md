# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT）的端到端高保真翻译。它通过统一模态识别、智能路由与原格式重构技术，实现“输入即所见、输出即所用”的翻译体验。该模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景，接口遵循 DashScope 标准协议。详细设计原理与能力边界请参阅 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一公开模型**：当前仅开放 `qwen-mt-uni` 模型，不提供其他子型号或轻量变体。
- **全模态输入支持**：  
  - 文本：`string` 或 `string[]`（批量保持顺序）；  
  - 文档：`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.txt`, `.html`, `.htm`, `.md`, `.markdown`, `.mdown`, `.mkd`；  
  - 图像：`.png`, `.jpg`, `.jpeg`；  
  - 音频：`.mp3`, `.wav`。  
  具体格式限制与兼容性说明详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的“支持的输入格式”章节。
- **双模式执行**：  
  - 同步调用：请求后阻塞等待结果，适合文本、小图（≤100 MB）、短音频（3 秒–60 分钟）；  
  - 异步调用：通过 `X-DashScope-Async: enable` 头触发，返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取最终结果，适用于大文档（≤200 页）或长音频处理。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | 是 | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | 条件必填 | 可访问的 HTTPS URL（不含中文字符），服务端自动识别模态；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| string[]` | 条件必填 | 纯文本输入；与 `fileUrl` 二选一 |
| `input.target_lang` | `string` | 是 | 目标语言代码（如 `en`, `ja`, `ko`），必须显式指定；源语言 `source_lang` 可省略（自动识别） |
| `input.ext.domainHint` | `string` | 否 | **仅限英文**，最多 200 单词，用于引导领域风格（如电商客服、技术文档）；详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | 否 | 术语表（≤100 组），支持原文保留、强制翻译或空目标（`{"src": "API", "tgt": ""}`） |
| `input.ext.sensitives` | `string[]` | 否 | 敏感词列表（区分大小写，≤50 项），完全匹配时跳过翻译并保留原文 |
| `input.ext.config.imageSegment` | `boolean` | 否 | **仅图像生效**；`true` 时跳过人物/Logo等主体区域文字翻译（默认 `false`） |

> **注意**：`domainHint` 字段在原始文档中明确要求“只支持英文”，若传入中文将被忽略且不报错——此行为与部分内部测试文档描述不符，请以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

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
- 成功响应：顶层含 `output` 对象，结果在 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）；
- 失败响应：顶层含 `code` 和 `message` 字段（无 `output`）。

### 异步调用（推荐用于大文档/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   ```
   → 获取 `output.task_id`（24 小时有效）。

2. **轮询结果**（GET `/api/v1/tasks/{task_id}`）：
   - 当 `output.task_status == "SUCCEEDED"` 时，检查 `output.Success`：  
     - `true` → 结果在 `output.Data`；  
     - `false` → 错误原因在 `output.Code` / `output.Message`。  
   - 建议轮询间隔 ≥1s，避免触发限流（默认 RPS=1）。

完整流程与错误码定义请严格参照 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；URL 不得含中文字符。
- **格式兼容性**：不支持旧版 `.doc` / `.ppt`，需先转换为 `.docx` / `.pptx`。
- **[Token](../concepts/token.md) 计费**：按 `usage.input_tokens` 计费，用量明细按模态拆分（`image_tokens`, `document_tokens` 等），详情见响应中的 `usage` 字段。
- **术语表与敏感词**：`glossary` 中 `tgt` 为空字符串表示保留原文；`sensitives` 匹配严格区分大小写且要求完全相等。
- **[异步任务](../concepts/asynchronous-task.md)生命周期**：`task_id` 有效期 24 小时；查询返回的 `TranslatedFileUrl` 也仅 24 小时有效，需及时下载。
- **回调支持**：如需事件驱动而非轮询，可配置[异步任务](../concepts/asynchronous-task.md)回调，具体方法见 `raw/model-api-reference/more-about-models/async-task-api.md`（非本文档覆盖范围）。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


