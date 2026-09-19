# qwen mt translation models

Qwen-MT-Uni 是百炼平台提供的全模态翻译模型，支持文本、图片、音频及多种文档格式（PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT/图像/音频）的一体化高保真翻译。它通过统一的模态识别、智能路由、内容抽取与跨模态翻译链路实现端到端处理，并提供同步与异步两种调用模式以适配不同耗时场景。该模型严格遵循 DashScope 标准协议，所有接口行为与错误处理逻辑均在 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 中明确定义。

## 支持的模型与功能

- **模型名称**：`qwen-mt-uni`（当前唯一公开发布的 Qwen MT 翻译模型）  
- **输入模态**：纯文本（`string` 或 `string[]`）、PDF、DOCX、PPTX、XLSX、TXT、HTML、Markdown、JPG/PNG、MP3/WAV  
- **输出模态**：保持输入格式一致（如输入 PDF 输出 PDF；输入 JPG 输出 JPG；输入字符串数组则输出同形状字符串数组）  
- **核心能力**：自动语言识别（可选覆盖）、领域提示（`domainHint`，仅英文）、格式提示（`format_hint`）、敏感词保留（`sensitives`）、术语表控制（`glossary`）、图像主体文字跳过（`config.imageSegment`）  
- **调用模式**：  
  - **同步调用**：适用于文本、小图、短音频等低延迟场景，直接返回结果或文件 URL  
  - **异步调用**：需在请求头添加 `X-DashScope-Async: enable`，适用于大文档（≤200页）、长音频（3秒–60分钟）等高耗时任务，通过 `task_id` 轮询获取结果  

> **注意**：原始文档中未提及除 `qwen-mt-uni` 外的其他 Qwen MT 模型（如 `qwen-mt-base` 或 `qwen-mt-pro`），因此当前生产环境仅支持该单一模型。如有旧文档声称存在多版本模型，请以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | `string` | ✅ | 固定为 `"qwen-mt-uni"` |
| `input.fileUrl` | `string` | ⚠️（条件必填） | 可公开访问的 HTTPS URL，服务端自动识别模态类型；URL 不得含中文字符；单文件 ≤100 MB；文档 ≤200 页；音频时长 3s–60min |
| `input.source_texts` | `string \| string[]` | ⚠️（条件必填） | 与 `fileUrl` **二选一**；批量翻译保持顺序与形状一致性 |
| `input.target_lang` | `string` | ✅ | 目标语言代码（如 `en`, `ja`, `ko`），详见[支持语种列表](https://help.aliyun.com/zh/model-studio/qwen-mt-uni-api#uni-languages) |
| `input.source_lang` | `string` | ❌（可选） | 源语言代码；不填则启用自动识别 |
| `input.ext.domainHint` | `string` | ❌ | 英文领域描述（≤200 单词），用于引导译文风格；**仅支持英文**，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) |
| `input.ext.sensitives` | `string[]` | ❌ | 敏感词列表（区分大小写，≤50项），匹配即原样保留不翻译 |
| `input.ext.glossary` | `{src: string, tgt: string}[]` | ❌ | 术语表（≤100组），支持原文保留（`tgt` 为空）、强制翻译、空目标词等策略 |
| `input.ext.config.imageSegment` | `boolean` | ❌ | **仅对图像生效**；`true` 表示跳过人物/商品/Logo 等主体区域文字翻译（默认 `false`） |

## 使用方式

### 前提条件
- 已获取并配置有效的百炼 API Key（参见 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)）  
- 请求域名中的 `{WorkspaceId}` 需替换为实际工作空间 ID（参见 [获取 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)）

### 同步调用示例（文本）
```bash
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-mt-uni",
    "input": {
        "source_texts": ["Hello, world!", "Thank you very much."],
        "target_lang": "zh"
    }
}'
```

### 异步调用示例（PDF 文件）
```bash
# 步骤1：创建任务
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-mt-uni",
    "input": {
        "fileUrl": "https://example.com/report.pdf",
        "target_lang": "ja"
    }
}'

# 步骤2：轮询结果（使用返回的 task_id）
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

> **注意**：[异步任务](../concepts/asynchronous-task.md) `task_id` 有效期为 24 小时；查询接口默认限流 1 RPS；若需更高频轮询或事件通知，请参考 [async-task-api.md](../../raw/model-api-reference/more-about-models/async-task-api.md) 配置回调。

## 限制和注意事项

- **文件限制**：单文件 ≤100 MB；PDF/DOCX/PPTX/XLSX 文档 ≤200 页；音频时长 3 秒–60 分钟  
- **格式兼容性**：不支持旧版 `.doc` / `.ppt`；必须先转换为 `.docx` / `.pptx`  
- **URL 规范**：`fileUrl` 必须为合法 HTTPS 地址，且路径中**禁止出现中文字符**  
- **领域提示**：`domainHint` 字段**仅接受纯英文描述**，非英文内容将被忽略或导致不可预期行为  
- **响应结构差异**：  
  - 同步成功响应顶层含 `output` 和 `usage`；失败时顶层为 `code`/`message`  
  - 异步成功响应中，`task_status == "SUCCEEDED"` 仅表示任务执行完成，**业务是否成功需检查 `output.Success` 字段**（`false` 表示业务失败，原因见 `output.Code`/`output.Message`）  
- **[Token](../concepts/token.md) 计费**：按 `input_tokens` 计费，用量明细按模态拆分（`document_tokens`/`image_tokens`/`audio_tokens`/`character_tokens`），详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 的 `usage` 字段说明

## 来源文档

- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


