# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。它通过统一的模态识别、智能路由、内容抽取与格式重构链路实现跨模态语义对齐，同时提供同步与异步两种调用模式以适配不同耗时场景。该模型严格遵循 DashScope 标准协议，所有接口行为与错误处理机制均在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 支持的模型与功能

- **模型名称**：`qwen-mt-uni`（当前唯一公开发布的 Qwen MT 翻译模型）  
- **模态支持**：文本（字符串或数组）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV  
- **核心能力**：
  - 自动源语言识别（可显式指定 `source_lang`）
  - 多目标语言翻译（`target_lang` 必填，详见[支持的语种](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages)）
  - 领域自适应（通过英文 `domainHint` 引导译文风格）
  - 格式保真（输入 DOCX → 输出 DOCX；输入 JPG → 输出 JPG）
  - 敏感词保留（`sensitives` 列表中完全匹配的字符串不翻译）
  - 术语强约束（`glossary` 支持源-目标映射，当前以 Prompt 注入方式生效）

> **注意**：文档中提及“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转换为 OOXML 格式”，但 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确未将 `.doc`/`.ppt` 列入**支持的输入格式**，因此该类文件实际不可用，无需转换——直接拒绝即可。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️（条件必填） | 可访问的 HTTPS URL；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| array<string>` | ⚠️（条件必填） | 文本输入；与 `fileUrl` 二选一 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），不可为空 |
| `input.source_lang` | `string` | ❌（可选） | 源语言代码；不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | **仅支持英文**，最多 200 单词，用于领域风格引导 |
| `input.ext.format_hint` | `string` | ❌ | 当 `fileUrl` 无后缀时显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | `array<string>` | ❌ | 区分大小写，最多 50 项，完全匹配则保留原文 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 最多 100 组，支持空 `tgt`（即保留原文） |
| `input.ext.config.imageSegment` | `boolean` | ❌ | 仅图像生效；`true` 时跳过主体（人物/Logo/商品）上的文字翻译 |

## 使用方式

### 同步调用（推荐用于 ≤100 MB 小文件或文本）
- **Endpoint**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`  
- **Header**：`Authorization: Bearer <API_KEY>`，`Content-Type: application/json`  
- **成功响应结构**：顶层含 `output` 对象（含 `Data.TranslatedTexts` 或 `Data.TranslatedFileUrl`）和 `usage` 用量统计；失败时顶层返回 `code`/`message`  
- 示例见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的 `curl` 调用片段

### 异步调用（必需用于大文档/长音频）
- **步骤 1（创建任务）**：同上 Endpoint，**额外添加 Header** `X-DashScope-Async: enable`，响应返回 `output.task_id`  
- **步骤 2（轮询结果）**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`，轮询至 `output.task_status = "SUCCEEDED"` 后检查 `output.Success` 字段  
- **关键约束**：`task_id` 有效期 24 小时；`TranslatedFileUrl` 下载链接有效期亦为 24 小时；默认查询 RPS 为 1  

## 限制和注意事项

- **文件限制**：单文件 ≤ 100 MB；PDF/DOCX/PPTX ≤ 200 页；音频时长 3 秒～60 分钟  
- **URL 要求**：`fileUrl` 必须为合法 HTTPS 地址，**禁止包含中文字符或空格**  
- **语言代码**：`target_lang` 为必填项且必须有效；`source_lang` 可省略（自动识别），但若显式指定，需确保与实际内容一致，否则可能降低质量  
- **[Token](../concepts/token.md) 计费**：按 `input_tokens` 计费，用量明细区分 `document_tokens`/`image_tokens`/`audio_tokens`/`character_tokens`，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的 `usage` 字段说明  
- **错误处理**：同步失败直接返回 `code`/`message`；[异步任务](../concepts/asynchronous-task.md)即使 `task_status = "SUCCEEDED"`，仍需校验 `output.Success === true` 才代表业务成功，否则 `output.Code`/`output.Message` 提供具体失败原因

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


