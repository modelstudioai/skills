# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。其核心能力基于统一模态识别、智能路由与原格式重构，兼顾语义准确性与排版/结构一致性。该模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景，接口遵循 DashScope 标准协议。详细设计原理与链路说明见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或历史版本（如 `qwen-mt` 旧版已下线）。
- **全模态输入支持**：
  - 文本：`string` 或 `string[]`，输出保持形状一致；
  - 文档：`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.txt`, `.html`, `.md` 等，输出同格式译后文件；
  - 图像：`.jpg`, `.jpeg`, `.png`，输出 `.jpg` 格式译后图；
  - 音频：`.mp3`, `.wav`，输出 `.mp3` 格式译后音频（含语音转文字+翻译）。
- **双模式调度**：
  - 同步调用：直接返回结果（文本或带签名的 `TranslatedFileUrl`），适合 ≤100 MB 文件或 ≤60 分钟音频；
  - 异步调用：通过 `X-DashScope-Async: enable` 头触发，先返回 `task_id`，再轮询 `/api/v1/tasks/{task_id}` 获取结果，适用于大文档或长音频场景。完整流程详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：原始文档中“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转换为 OOXML 格式”这一要求仍有效，但部分内部测试文档曾误标为“已支持”，请以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中的明确限制为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✓ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | △（与 `source_texts` 二选一） | 可公开访问的 HTTPS URL，服务端自动识别模态；URL 不得含中文字符；单文件 ≤100 MB，文档 ≤200 页，音频时长 3s–60min |
| `input.source_texts` | `string \| string[]` | △（与 `fileUrl` 二选一） | 纯文本输入；批量翻译保持顺序与形状 |
| `input.target_lang` | `string` | ✓ | 目标语言代码（如 `en`, `ja`, `ko`），必填；源语言 `source_lang` 可选（自动识别） |
| `input.ext.domainHint` | `string` | ✗ | 英文领域提示（≤200 单词），影响译文风格；**仅支持英文**，中文提示将被忽略 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ✗ | 术语表（≤100 组），用于强制术语对齐；空 `tgt` 表示保留原文 |
| `input.ext.sensitives` | `string[]` | ✗ | 敏感词列表（≤50 项，区分大小写），匹配则原文透传不翻译 |
| `input.ext.config.imageSegment` | `boolean` | ✗ | **仅图像生效**；`true` 时跳过人物/Logo等主体区域文字翻译 |

## 使用方式

1. **前置准备**：确保已[获取并配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，且环境变量 `DASHSCOPE_API_KEY` 已设置。
2. **构造请求**：
   - Endpoint：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
   - 替换 `{WorkspaceId}` 为实际工作区 ID（参见[地域与域名迁移说明](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)）
   - Headers：`Content-Type: application/json` + `Authorization: Bearer <your_api_key>`
   - 异步调用需额外添加 `X-DashScope-Async: enable`
3. **处理响应**：
   - 同步成功：检查顶层 `output.Success === true`，结果在 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）；
   - 同步失败：检查顶层 `code` 字段（如 `InvalidParameter`）；
   - 异步成功：轮询 `GET /api/v1/tasks/{task_id}`，待 `output.task_status === "SUCCEEDED"` 后，**必须验证 `output.Success === true`**（`task_status=SUCCEEDED` 不代表业务成功）；
   - Token 用量始终位于顶层 `usage` 对象中，按 `input_tokens` 计费，明细字段见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；URL 不得含中文字符。
- **格式限制**：不支持 `.doc`/`.ppt` 等旧版二进制格式，必须转为 `.docx`/`.pptx`；图像输入仅支持 JPG/PNG，输出强制为 JPG。
- **领域提示**：`domainHint` 严格限定为英文，中文输入无效，此限制未在所有内部文档中明确强调，但已在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。
- **异步任务生命周期**：`task_id` 有效期 24 小时；查询接口默认 RPS=1；译后文件 URL 有效期亦为 24 小时，需及时下载。
- **错误处理**：同步失败响应含 `code`/`message`；异步任务即使 `task_status=SUCCEEDED`，也需检查 `output.Success` 和 `output.Code` 判断业务成败。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


