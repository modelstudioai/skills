# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT 等）的一体化高保真翻译。它通过统一的模态识别、智能路由与原格式重构能力，在保持原始排版与结构的同时完成跨语言转换。模型提供同步与异步两种调用模式，分别适用于低延迟短任务和长耗时大文件场景，接口遵循 DashScope 标准协议。详细设计原理与链路说明见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一可用模型**：当前仅开放 `qwen-mt-uni` 模型，不支持其他别名或历史版本（如 `qwen-mt` 旧版已下线）。
- **全模态输入**：支持字符串、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、PNG/JPG、MP3/WAV 共 10 类输入格式，输出格式严格对应（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`）。
- **双模式调度**：
  - **同步调用**：适用于文本、小图、短音频（≤30 秒），请求后阻塞等待结果返回；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，返回 `task_id` 后轮询 `/api/v1/tasks/{task_id}` 获取最终结果，适用于大文档（≤200 页）、长音频（3 秒–60 分钟）等场景。
- **自动语言识别**：`source_lang` 为可选参数；未提供时模型自动检测源语言，但对混合语种或极短文本（如单词）识别可能不稳定 —— 建议明确指定以保障一致性。该行为已在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️ 条件必填 | 可公开访问的 HTTPS URL（不含中文字符），服务端自动识别模态类型；与 `source_texts` 二选一 |
| `input.source_texts` | `string \| array<string>` | ⚠️ 条件必填 | 文本内容，支持单条或批量（保持顺序）；与 `fileUrl` 二选一 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[官方语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | `string` | ❌ | 源语言代码（如 `zh`, `fr`），不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | **仅英文有效**，最多 200 词，用于引导领域风格（如电商客服、技术文档）；该限制在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中强调为硬性要求 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 术语表，最多 100 组，支持原文保留（`tgt` 为空）或强制替换 |
| `input.ext.sensitives` | `array<string>` | ❌ | 敏感词列表（区分大小写），匹配即原样保留，不送入模型 |

> **注意**：`input.ext.format_hint` 仅在 `fileUrl` 无后缀或后缀不可识别时使用（如 `https://example.com/file?x=1`），否则会被忽略；此逻辑与部分旧版文档描述存在偏差，应以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

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
- 成功响应含 `output.Data.TranslatedTexts`（数组）与 `usage` 用量统计；
- 失败响应含顶层 `code` 和 `message` 字段。

### 异步调用（推荐用于大文档/长音频）
1. **提交任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   ```
   → 获取 `output.task_id`（24 小时有效）。

2. **轮询结果**（建议间隔 ≥1s，RPS ≤1）：
   ```bash
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   - 当 `output.task_status == "SUCCEEDED"` 且 `output.Success == true` 时，结果在 `output.Data.TranslatedFileUrl` 或 `TranslatedTexts` 中；
   - `output.Success == false` 表示业务失败（如译文质量不达标），此时 `output.Code`/`output.Message` 提供具体原因。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX ≤200 页；音频时长 3 秒–60 分钟；URL 中禁止中文字符。
- **格式兼容性**：仅支持 OOXML 格式（`.docx`/`.pptx`），旧版 `.doc`/`.ppt` 需预先转换。
- **[Token](../concepts/token.md) 计费**：按 `usage.input_tokens` 计费，`input_tokens_details` 拆分统计 `document_tokens`/`image_tokens`/`audio_tokens`/`character_tokens`，便于成本归因。
- **图像翻译控制**：通过 `input.ext.config.imageSegment: true` 可跳过人物/Logo 等主体区域文字，避免误译 —— 此参数仅对图像输入生效。
- **术语与敏感词**：`glossary` 与 `sensitives` 均区分大小写，且 `sensitives` 为**完全匹配**（非子串匹配）。
- **回调支持**：高频轮询不推荐，如需事件驱动，请配置异步任务回调，详见 `raw/model-api-reference/more-about-models/async-task-api.md`。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


