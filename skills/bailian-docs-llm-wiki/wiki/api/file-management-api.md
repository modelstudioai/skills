# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同用途对应不同下游能力：

- `fine-tune`：用于模型微调（含文本、视频、图像生成类模型），训练数据支持 `.jsonl` 或 `.zip`（单个 zip ≤ 1 GB）；视频/图像微调要求 zip 格式，也可通过 OSS 挂载方式加载未压缩数据集。
- `file-extract`：用于文件内容结构化提取（如 PDF/Word 表格识别、OCR 文本抽取等）。
- `batch`：用于创建 [Batch 任务](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，支持异步批量推理。

> **注意**：文档 1 中提到“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但文档 2 的列举接口返回示例中明确包含 `purpose: "file-extract"` 和 `purpose: "fine-tune"` 字段，且 `fine-tune` 文件可为任意类型（如 `test.txt`）。实际支持格式应以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 文档为准，但需注意 zip 限制仅针对视频/图像类微调，文本微调（如 Qwen）支持 `.jsonl` 等纯文本格式。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 描述 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应用途的下游服务识别 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非必填，最大长度未明确定义，建议 ≤ 500 字符 |

> **注意**：`purpose` 在上传时指定后不可修改，后续需通过 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 接口确认其值；若用途误设，需重新上传。

## 使用方式

### 1. 上传文件（POST `/api/v1/files`）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file1.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="Qwen 微调样本"' \
  --form 'files=@"/path/to/file2.pdf"' \
  --form 'purpose="file-extract"'
```

### 2. 查询单个文件（GET `/api/v1/files/{file_id}`）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 3. 列举文件（GET `/api/v1/files`）
支持分页，`page_no` ≥ 1，`page_size` ∈ [1, 100]：
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 4. 删除文件（DELETE `/api/v1/files/{file_id}`）
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调 zip 包 ≤ 1 GB）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；如您使用其他 Region，请通过该 Region 的百炼控制台完成文件管理操作（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文档说明）。

- **兼容性提示**：两个原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。新项目应优先集成 OpenAI 兼容路径（`/compatible-mode/v1/files`），因其提供更一致的错误码、字段命名及长期维护保障。

- **失败处理**：上传接口返回中 `data.failed_uploads` 明确列出失败文件及原因（如 `BadRequest.TooLarge`、`BadRequest.TooMany`），需主动解析并重试或告警。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


