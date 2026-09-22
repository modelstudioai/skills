# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown 等）的端到端高保真翻译。它通过统一模态识别、智能路由与原格式重构技术，在保持原始排版与结构的前提下完成跨语言转换。该模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景。详细协议与字段定义请参见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **模型名称**：`qwen-mt-uni`（当前唯一公开发布的 Qwen MT 翻译模型）  
- **输入模态**：纯文本（`string` 或 `string[]`）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV  
- **输出模态**：与输入严格对应（如输入 `.pdf` → 输出 `.pdf`；输入 `string[]` → 输出 `string[]`）  
- **核心能力**：
  - 自动源语言识别（可显式指定 `source_lang`）
  - 多粒度术语控制（`glossary` 字段支持 `{"src": "...", "tgt": "..."}` 映射）
  - 敏感词保护（`sensitives` 列表中完全匹配项保留原文，不送入模型）
  - 领域风格引导（`ext.domainHint`，**仅支持英文描述**，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)）
  - 图像主体分割（`ext.config.imageSegment = true` 时跳过人物/Logo等主体区域文字翻译）

> **注意**：文档中提及“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转为 OOXML 格式”，但该限制在部分内部测试环境中已放宽；实际使用前请以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的最新运行时行为为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️ 条件必填 | 可访问的 HTTPS URL（无中文字符），服务端自动识别模态类型；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| string[]` | ⚠️ 条件必填 | 文本或文本数组；与 `fileUrl` 二选一 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），不可为空 |
| `input.source_lang` | `string` | ❌ | 源语言代码（如 `zh`, `fr`）；不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | 英文领域提示（≤200 单词），影响译文风格 |
| `input.ext.format_hint` | `string` | ❌ | 当 `fileUrl` 无后缀时，显式声明格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | `string[]` | ❌ | 敏感词列表（区分大小写，≤50 项），完全匹配则保留原文 |
| `input.ext.glossary` | `{src: string, tgt: string}[]` | ❌ | 术语表（≤100 组），支持空 `tgt` 表示保留原文 |

## 使用方式

### 同步调用（推荐用于文本、小图、短音频）
- **Endpoint**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`  
- **Header**：`Authorization: Bearer <API_KEY>`，`Content-Type: application/json`  
- **响应**：直接返回 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）  
- 示例请求体：
  ```json
  {
    "model": "qwen-mt-uni",
    "input": {
      "source_texts": ["Hello world", "Thank you very much"],
      "target_lang": "zh"
    }
  }
  ```

### 异步调用（必须用于大文档、长音频、高并发场景）
- **步骤 1（创建任务）**：在同步请求头中添加 `X-DashScope-Async: enable`，获取 `task_id`  
- **步骤 2（轮询结果）**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`  
- **关键约束**：
  - `task_id` 有效期 24 小时  
  - 查询接口默认限频 1 RPS；高频轮询需配置回调，详见 [async-task-api.md](../../raw/model-api-reference/more-about-models/async-task-api.md)  
- **状态判断逻辑**：`task_status == "SUCCEEDED"` 仅表示任务执行完毕，**必须检查 `output.Success == true` 才代表业务成功**（失败时 `Code`/`Message` 在 `output` 内）

## 限制和注意事项

- **文件限制**：单文件 ≤ 100 MB；PDF/DOCX/PPTX ≤ 200 页；音频时长 3 秒～60 分钟  
- **URL 要求**：`fileUrl` 必须为有效 HTTPS 地址，且路径中**不能含中文字符或空格**  
- **[Token](../concepts/token.md) 计费**：按 `usage.input_tokens` 计费，用量明细按模态拆分（`image_tokens`, `document_tokens`, `audio_tokens`, `character_tokens`）  
- **术语表行为**：`glossary` 当前作为 Prompt 注入，不保证 100% 强制替换；若需强一致性，建议结合 `sensitives` + 后处理校验  
- **错误处理**：同步失败返回顶层 `code`/`message`；异步失败仍返回 `task_status: "SUCCEEDED"`，需依赖 `output.Success` 和 `output.Code` 判断——此设计易引发误判，务必在代码中显式校验，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的响应结构说明

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


