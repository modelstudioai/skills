# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 决定文件后续可接入的服务类型：

- `fine-tune`：用于模型微调（含文本、视频、图像生成类模型），训练数据支持 `.jsonl` 或 `.zip`（单个 zip ≤ 1 GB）；视频/图像微调推荐使用 OSS 挂载方式加载未压缩数据集，**不支持 zip 文件**（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）。
- `file-extract`：用于内容解析与结构化提取（如 PDF/Word 文本抽取）。
- `batch`：用于创建 Batch 异步任务（兼容 OpenAI Batch 格式）。

> **注意**：文档 1 中称“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但同一文档后文又明确说明“不支持 zip 文件”——此处存在自相矛盾。实际行为以控制台和最新 SDK 为准，建议优先使用 OSS 挂载方式，避免依赖 zip 上传。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应服务识别和调用 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述，仅作备注，不影响功能 |

在查询与管理接口中，关键路径/查询参数包括：
- `GET /api/v1/files/{file_id}`：`file_id` 为必填 path 参数，可通过 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 返回获取；
- `GET /api/v1/files`：需指定 `page_no`（≥1）和 `page_size`（1–100）进行分页；
- `DELETE /api/v1/files/{file_id}`：同样依赖 `file_id` 路径参数。

## 使用方式

### 上传文件（POST）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file1.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tune sample"' \
  --form 'files=@"/path/to/file2.pdf"' \
  --form 'purpose="file-extract"'
```

### 查询单个文件（GET）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举文件（GET）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件（DELETE）
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

所有响应均含 `request_id`，用于问题排查；失败时返回非 200 状态码及 JSON 错误体（含 `code` 和 `message` 字段），详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 和 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 的异常说明。

## 限制和注意事项

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过该 Region 的百炼控制台完成文件管理（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。
- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。
- **兼容性提示**：两个原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。该兼容接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 Files API 一致，建议新集成项目直接采用。
- **文件生命周期**：`file_id` 一经生成即全局唯一且永久有效（除非显式删除）；删除后不可恢复，`url` 失效。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


