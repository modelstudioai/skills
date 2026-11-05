# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。它通过统一的模态识别、智能路由、内容抽取与格式重构链路实现跨模态保形翻译，并提供同步与异步两种调用模式以适配不同耗时场景。该模型严格遵循 DashScope 标准协议，所有接口行为与计费逻辑均以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或历史版本（如 `qwen-mt` 或 `qwen-mt-v1`）。
- **全模态输入支持**：  
  - 文本：`string` 或 `string[]`（批量保持顺序与形状）；  
  - 文档：`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.txt`, `.html`, `.md` 等；  
  - 图像：`.jpg`, `.jpeg`, `.png`；  
  - 音频：`.mp3`, `.wav`。  
  输出格式与输入严格对应（如 PDF → PDF，JPG → JPG），详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的“支持的输入格式”章节。
- **双模式调度**：  
  - **同步调用**：适用于文本、小图、短音频（≤30 秒），请求后直接返回结果；  
  - **[异步调用](../concepts/asynchronous-invocation.md)**：需在请求头添加 `X-DashScope-Async: enable`，适用于大文档（≤200 页）、长音频（3 秒–60 分钟）等长耗时任务，通过 `task_id` 轮询获取结果。

> **注意**：原始文档中未提及 `qwen-mt-base` 或 `qwen-mt-pro` 等子型号，所有能力均由 `qwen-mt-uni` 单一模型承载。若其他内部文档列出此类名称，应视为过时信息，以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️（条件必填） | 可公开访问的 HTTPS URL，服务端自动识别模态类型；URL 中**禁止含中文字符**；单文件 ≤100 MB，文档 ≤200 页，音频 3s–60min |
| `input.source_texts` | `string \| string[]` | ⚠️（条件必填） | 与 `fileUrl` **二选一且必须选一**；数组形式支持批量翻译，响应保持相同结构 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），不可为空；源语言 `source_lang` 为可选，不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | 英文领域提示（≤200 单词），**仅支持英文**，用于引导译文风格；中文提示将被忽略 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 术语表（≤100 组），支持原文保留（`tgt` 为空）、强制翻译（`tgt` 非空）等策略 |
| `input.ext.sensitives` | `string[]` | ❌ | 敏感词列表（≤50 项，区分大小写），匹配即原样保留，不送入模型 |

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
- 成功响应顶层含 `output` 对象，结果在 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）；
- 失败响应顶层含 `code` 和 `message` 字段（无 `output`）。

### [异步调用](../concepts/asynchronous-invocation.md)（推荐用于大文档/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable` 头）：
   ```bash
   curl --location '...' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   # → 返回 output.task_id（有效期 24 小时）
   ```
2. **轮询结果**（GET `/api/v1/tasks/{task_id}`）：
   - 当 `output.task_status == "SUCCEEDED"` 时，检查 `output.Success`：  
     - `true` → 结果在 `output.Data`；  
     - `false` → 错误详情在 `output.Code` / `output.Message`。  
   - `TranslatedFileUrl` 有效期也为 24 小时，需及时下载。

详细请求/响应结构、错误码定义及用量字段（`usage.input_tokens_details` 等）请严格参照 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **格式限制**：旧版 `.doc` / `.ppt` 文件必须先转换为 `.docx` / `.pptx`；URL 不得含中文字符；图像主体分割（`ext.imageSegment`）仅对 `.jpg`/`.png` 生效。
- **容量限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频 3 秒–60 分钟；`glossary` ≤100 组，`sensitives` ≤50 项。
- **[Token](../concepts/token.md) 计费**：按 `usage.input_tokens` 计费，`input_tokens_details` 按模态拆分（`image_tokens`, `document_tokens`, `audio_tokens`, `character_tokens`），无额外调用费用。
- **安全要求**：API Key 必须通过环境变量 `DASHSCOPE_API_KEY` 配置，或显式传入 `Authorization: Bearer sk-xxx`；严禁硬编码或泄露。
- **异步轮询**：默认 RPS = 1，高频轮询需配置回调（见 `raw/model-api-reference/more-about-models/async-task-api.md`）。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


