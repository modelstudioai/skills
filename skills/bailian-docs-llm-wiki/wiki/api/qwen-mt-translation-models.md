# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态机器翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT）的端到端高保真翻译，并自动完成格式重构。它提供同步与异步两种调用模式，分别适用于低延迟小规模输入和长耗时大文件处理场景。该模型基于 DashScope 统一协议实现，所有接口均需通过 API Key 认证，详细行为请严格参照 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或历史版本（如 `qwen-mt` 旧版已下线）。
- **多模态输入支持**：  
  - 文本：`string` 或 `string[]`（批量保持顺序与形状）；  
  - 文档：`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.txt`, `.html`, `.htm`, `.md`, `.markdown`, `.mdown`, `.mkd`；  
  - 图像：`.png`, `.jpg`, `.jpeg`；  
  - 音频：`.mp3`, `.wav`。  
- **输出保形保格式**：输入为字符串则返回字符串（或数组），输入为某类文件则返回同格式译后文件（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`）。  
- **双模式调度**：同步调用（默认）适合文本/小图/短音频；异步调用（需加 `X-DashScope-Async: enable` 请求头）适合大文档（≤200页）、长音频（3秒–60分钟）等场景。具体流程与状态机定义详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️ 条件必填 | 可公开访问的 HTTPS URL（不含中文字符），服务端自动识别模态类型；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| string[]` | ⚠️ 条件必填 | 非空字符串或字符串数组；与 `fileUrl` 二选一 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），必须填写；源语言 `source_lang` 可省略（自动识别） |
| `input.ext.domainHint` | `string` | ❌ | 英文领域提示（≤200词），**仅支持英文**，影响译文风格；详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中示例 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 术语表（≤100组），支持原文保留、指定翻译、空目标词等策略 |
| `input.ext.sensitives` | `string[]` | ❌ | 敏感词列表（区分大小写，≤50项），匹配即原样保留不翻译 |
| `input.ext.config.imageSegment` | `boolean` | ❌ | **仅图像生效**：`true` 时跳过人物/商品/Logo等主体区域文字翻译 |

> **注意**：`domainHint` 字段在部分旧版 SDK 示例中被误标为支持中文，实际仅接受英文描述——该不一致已在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确修正。

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
- 成功响应含 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）；
- 失败响应顶层含 `code` 和 `message` 字段（非 `output` 下）。

### 异步调用（推荐用于大文档/长音频）
1. **提交任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   ```
   → 获取 `output.task_id`（24小时有效）。

2. **轮询结果**（`GET /api/v1/tasks/{task_id}`）：
   - 轮询间隔建议 ≥1s（默认 RPS=1）；
   - `task_status = "SUCCEEDED"` 仅表示任务执行完毕，**必须检查 `output.Success === true` 才代表业务成功**；
   - 业务失败时 `output.Success = false`，错误原因在 `output.Code` / `output.Message`。

完整协议细节、请求/响应结构及 [Token](../concepts/token.md) 用量字段（`usage.input_tokens_details` 等）请严格以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200页；音频时长 3秒–60分钟；URL 中禁止含中文字符。
- **格式兼容性**：仅支持 OOXML 格式（`.docx`/`.pptx`），旧版 `.doc`/`.ppt` 需先转换。
- **[Token](../concepts/token.md) 计费**：按 `input_tokens` 计费，`usage.input_tokens_details` 按模态（`document_tokens`, `image_tokens`, `audio_tokens`, `character_tokens`）细分统计。
- **安全约束**：`sensitives` 匹配严格区分大小写；`glossary` 中 `src` 字段不支持正则或模糊匹配。
- **异步可靠性**：`task_id` 和 `TranslatedFileUrl` 均为 24 小时有效期，超时需重提任务；高频轮询请配置[异步任务回调](raw/model-api-reference/more-about-models/async-task-api.md)替代。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


