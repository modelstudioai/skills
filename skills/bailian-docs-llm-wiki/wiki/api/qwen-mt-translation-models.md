# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。它通过统一的模态识别、智能路由、内容抽取与格式重构链路实现跨模态语义对齐，同时提供同步与异步两种调用模式以适配不同耗时场景。该模型严格遵循 DashScope 标准协议，所有接口行为与错误处理机制均在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或变体。
- **输入模态**：支持字符串（单条或数组）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV 共 10 类格式；旧版 `.doc`/`.ppt` 需先转换为 OOXML 格式。
- **输出保持**：输出格式与输入严格对应（如 `.pdf` → `.pdf`，`list[str]` → `list[str]`），图像输出统一为 `.jpg`，音频为 `.mp3`。
- **双模式支持**：
  - **同步调用**：适用于文本、小图、短音频（≤3 秒），请求后直接返回结果；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，适用于大文档（≤200 页）、长音频（3 秒–60 分钟）等长耗时任务，通过 `task_id` 轮询获取结果。

> **注意**：文档中未提及任何 `qwen-mt-base` 或 `qwen-mt-pro` 等衍生模型，所有功能均基于 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 所述能力，切勿假设存在其他模型变体。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️（条件必填） | 可访问的 HTTPS URL，服务端自动识别模态；URL 不得含中文字符；单文件 ≤100 MB |
| `input.source_texts` | `string \| array<string>` | ⚠️（条件必填） | 与 `fileUrl` 二选一；批量翻译保持顺序与形状 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[支持语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | `string` | ❌（可选） | 源语言代码；不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | 英文领域提示（≤200 单词），**仅支持英文**，影响译文风格 |
| `input.ext.format_hint` | `string` | ❌ | 当 `fileUrl` 无后缀时显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | `array<string>` | ❌ | 敏感词列表（区分大小写，≤50 项），匹配则保留原文不翻译 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 术语表（≤100 组），支持原文保留、强制翻译或空目标词 |
| `input.ext.config.imageSegment` | `boolean` | ❌ | **仅图像生效**；`true` 时跳过人物/商品/Logo 上文字翻译 |

所有参数定义与约束均以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准，无扩展字段或隐藏参数。

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
- 成功响应：顶层含 `output` 对象，`output.Data.TranslatedTexts` 返回翻译结果；`usage` 字段含 token 统计。
- 失败响应：顶层含 `code` 和 `message` 字段（如 `InvalidParameter`），无 `output`。

### 异步调用（必须用于大文件/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   ```
   → 响应含 `output.task_id`（有效期 24 小时）。

2. **轮询结果**（每秒最多 1 次）：
   ```bash
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   - 当 `output.task_status == "SUCCEEDED"` 且 `output.Success == true` 时，从 `output.Data.TranslatedFileUrl` 或 `TranslatedTexts` 获取结果；
   - `TranslatedFileUrl` 有效期亦为 24 小时，需及时下载。

详细流程与状态机逻辑请严格参照 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中“异步调用”章节。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX/XLSX ≤200 页；音频时长 3 秒–60 分钟。
- **语言识别**：`source_lang` 为空时自动识别，但对混合语言或低质量 OCR 文本识别准确率下降，建议显式指定。
- **敏感词与术语表**：`sensitives` 区分大小写且要求**完全匹配**；`glossary` 当前为 Prompt 注入方式，不保证 100% 强制应用。
- **图像分割**：`imageSegment=true` 仅跳过主体区域文字，边框、水印、背景文字仍会被翻译。
- **Token 计费**：按 `usage.input_tokens` 计费，`input_tokens_details` 中 `image_tokens`/`document_tokens` 等字段反映各模态实际消耗，非简单字符计数。
- **错误处理**：同步失败直接返回 `code`/`message`；异步任务即使 `task_status == "SUCCEEDED"`，也**必须检查 `output.Success`** 才能确认业务成功——这是易错点，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的“异步调用”说明。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


