# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种办公文档（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT）的端到端高保真翻译。它通过统一模态识别、智能路由与原格式重构，实现“输入即所见、输出即所用”的翻译体验。该模型提供同步与异步两种调用模式，分别适用于短耗时与长耗时任务场景，接口遵循 DashScope 标准协议。详细设计原理与能力边界请参阅 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 支持的模型与功能

- **唯一公开模型**：当前仅开放 `qwen-mt-uni` 模型，无 `qwen-mt-base`、`qwen-mt-pro` 等变体；其他命名模型（如 `qwen-mt-zh2en`）未在官方文档中定义，属过时或内部测试名称。
- **全模态输入支持**：文本（`str` / `list[str]`）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、PNG/JPG、MP3/WAV。
- **双模式执行**：
  - **同步调用**：适用于文本、小图、短音频（≤30s），请求后阻塞等待结果返回；
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，适用于大文档（≤200页）、长音频（3s–60min）等长耗时任务，需轮询 `GET /api/v1/tasks/{task_id}` 获取最终结果。
- **格式保持能力**：输出文件类型与输入严格对应（如 `.pdf` → `.pdf`，`.jpg` → `.jpg`），文本翻译结果形状与 `source_texts` 输入一致（标量/数组）。

> **注意**：原始文档中多次提及“旧版二进制 Word（`.doc`）和 PowerPoint（`.ppt`）需先转换为 OOXML 格式”，但 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确将 `.doc` 和 `.ppt` 列为**不支持格式**，而非“需转换后支持”。因此应以“不支持”为准，避免兼容性误判。

## 关键参数

| 字段 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️（条件必填） | 可访问的 HTTPS URL；与 `source_texts` **互斥且必须选其一**；URL 中禁止含中文字符 |
| `input.source_texts` | `string \| array<string>` | ⚠️（条件必填） | 非空字符串或字符串数组；批量翻译保持顺序与形状 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[支持语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | `string` | ❌（可选） | 源语言代码；不填则自动识别 |
| `input.ext.domainHint` | `string` | ❌ | 英文领域提示（≤200词），影响译文风格；**仅支持英文**，中文提示无效 |
| `input.ext.format_hint` | `string` | ❌ | 当 `fileUrl` 无后缀时，显式指定格式（如 `"pdf"`, `"image"`） |
| `input.ext.sensitives` | `array<string>` | ❌ | 敏感词列表（区分大小写，≤50项），匹配则原文保留、不送入模型 |
| `input.ext.glossary` | `array<{src: string, tgt: string}>` | ❌ | 术语表（≤100组），支持原文保留（`tgt=""`）、强制翻译、空目标词等策略 |
| `input.ext.config.imageSegment` | `boolean` | ❌ | **仅图像生效**；`true` 时跳过人物/商品/Logo等主体区域文字翻译 |

Token 用量统计字段（`usage`）位于响应顶层，按 `input_tokens` 计费；明细字段（如 `image_tokens`, `document_tokens`）可用于成本归因分析，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

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
- 成功响应：`output.Success === true`，结果在 `output.Data.TranslatedTexts`（文本）或 `output.Data.TranslatedFileUrl`（文件）。
- 失败响应：顶层含 `code` 和 `message` 字段（如 `InvalidParameter`）。

### 异步调用（必需用于大文档/长音频）
1. **创建任务**（加 `X-DashScope-Async: enable`）：
   ```bash
   curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
   --header 'X-DashScope-Async: enable' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
   --header 'Content-Type: application/json' \
   --data '{...}'
   ```
   → 提取 `output.task_id`（有效期 24 小时）。

2. **轮询结果**（建议间隔 ≥1s，RPS ≤1）：
   ```bash
   curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
   --header "Authorization: Bearer $DASHSCOPE_API_KEY"
   ```
   - 当 `output.task_status === "SUCCEEDED"` 时，检查 `output.Success`：
     - `true`：结果在 `output.Data`；
     - `false`：失败原因在 `output.Code` / `output.Message`。

完整流程与错误处理逻辑详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX/XLSX ≤200 页；音频时长 3 秒 – 60 分钟。
- **URL 要求**：`fileUrl` 必须为公网可访问 HTTPS 地址，且路径中**不能含中文字符或空格**。
- **语言识别**：`source_lang` 为空时自动识别，但对混合语言或低质量 OCR 文本识别准确率下降；建议明确指定。
- **术语表与敏感词**：`glossary` 和 `sensitives` 均区分大小写，且仅做**完全匹配**（非子串匹配）。
- **异步任务生命周期**：
  - `task_id` 有效期：24 小时；
  - 查询接口 RPS 限制为 1，高频轮询需自行限速或配置[回调通知](raw/model-api-reference/more-about-models/async-task-api.md)；
  - `TranslatedFileUrl` 有效期：24 小时，需及时下载。
- **计费说明**：按 `usage.input_tokens` 计费，`input_tokens_details` 可区分模态用量（如 `image_tokens` 对应 OCR + 翻译开销）。

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


