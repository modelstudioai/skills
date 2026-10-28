# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。它通过统一的模态识别、智能路由、内容抽取与格式重构链路实现跨模态语义对齐，同时提供同步与异步两种调用模式以适配不同耗时场景。该模型严格遵循 DashScope 标准协议，所有接口行为与错误处理机制均在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或变体。
- **输入模态**：支持字符串（标量/数组）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV；旧版 `.doc`/`.ppt` 需先转换为 OOXML 格式。
- **输出保持原格式**：输入 PDF 输出 PDF，输入 JPG 输出 JPG，输入字符串数组则返回同形状字符串数组。
- **双模式调度**：
  - **同步调用**：适用于文本、小图、短音频（≤100 MB / ≤200 页 / 3s–60min），直接返回结果；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取结果，适用于大文件或长任务。

> **注意**：文档中未提及 `qwen-mt-base` 或 `qwen-mt-pro` 等子型号，所有能力均由 `qwen-mt-uni` 单一模型承载；若其他文档声称存在多版本模型，请以本 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

## 关键参数

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `model` | string | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | string | ⚠️ 条件必选 | 可访问的 HTTPS URL，服务端自动识别模态；URL 不得含中文字符；单文件 ≤100 MB，文档 ≤200 页，音频 3s–60min |
| `input.source_texts` | string \| string[] | ⚠️ 条件必选 | 与 `fileUrl` **二选一且必须选一**；批量翻译保持顺序与形状 |
| `input.target_lang` | string | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[支持语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | string | ❌ | 源语言代码（如 `zh`），不填则自动识别 |
| `input.ext.domainHint` | string | ❌ | 英文领域提示（≤200 单词），**仅支持英文**，用于引导译文风格 |
| `input.ext.format_hint` | string | ❌ | 当 `fileUrl` 无后缀时显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | string[] | ❌ | 敏感词列表（区分大小写，≤50 项），匹配则保留原文不翻译 |
| `input.ext.glossary` | {src: string, tgt: string}[] | ❌ | 术语表（≤100 组），支持原文保留、强制翻译或空目标词 |
| `input.ext.config.imageSegment` | boolean | ❌ | **仅图像生效**；`true` 表示跳过人物/Logo等主体区域文字翻译 |

所有参数定义与约束均严格依据 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 使用方式

### 同步调用（推荐用于轻量请求）
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
- 失败响应含顶层 `code` 和 `message` 字段。

### 异步调用（推荐用于大文件/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location '...' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   ```
   → 返回 `output.task_id`（24 小时有效）。

2. **轮询结果**（每秒最多 1 次，建议指数退避）：
   ```bash
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   - 当 `output.task_status == "SUCCEEDED"` 时，检查 `output.Success`：
     - `true`：结果在 `output.Data` 中；
     - `false`：失败原因在 `output.Code` / `output.Message`。

详细流程与字段含义请参阅 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；URL 路径禁止含中文字符。
- **[Token](../concepts/token.md) 计费**：按 `usage.input_tokens` 计费，`input_tokens_details` 按模态拆分（`document_tokens`, `image_tokens`, `audio_tokens`, `character_tokens`）。
- **术语表与敏感词**：`glossary` 当前以 Prompt 注入方式实现，不保证 100% 强制替换；`sensitives` 匹配为**全字符串精确匹配、区分大小写**。
- **异步任务生命周期**：`task_id` 有效期 24 小时；查询到的 `TranslatedFileUrl` 也仅 24 小时有效，需及时下载。
- **领域提示限制**：`domainHint` **必须为纯英文**，中文或混合内容将导致提示失效。
- **图像分割**：`imageSegment=true` 仅跳过主体区域文字，背景/边框/水印等非主体区域仍会翻译。

> **注意**：文档明确指出“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需要先转换为 OOXML 格式”，若其他资料建议直传 `.doc`，请忽略——该行为在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中已被明确弃用。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


