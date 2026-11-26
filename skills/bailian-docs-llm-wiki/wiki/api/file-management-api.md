# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途（如微调、内容提取、批量任务）的文件生命周期管理。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，指定 `purpose` 后可被下游任务复用（如 `fine-tune`、`file-extract`、`batch`）。  
- **查询文件详情**：通过 `file_id` 获取单个文件元信息（含 `url`、`size`、`md5`、`purpose` 等）。  
- **列举文件列表**：分页获取当前账户下所有有效文件，返回中包含 `purpose` 字段，便于按用途筛选。  
- **删除文件**：释放存储配额，删除后不可恢复。  

> **注意**：文档 2 明确指出“当前文件管理 API 仅在北京 Region 开放”，而文档 1 未提及地域限制。若您的 API 调用地域非北京，请优先使用控制台或 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)，否则可能返回 404 或权限错误。该矛盾已在 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中明确标注。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持多个 `files=@...` 字段，用于多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但影响后续功能可用性（详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述文本，非文件内容本身（注意：文档 1 表格中误标为“文件流”，实际为字符串，以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 的请求示例为准） |
| `file_id` | 字符串 | path | 是 | 所有 GET/DELETE 单文件操作必需，由上传成功响应返回 |
| `page_no`, `page_size` | 数字 | query | 是 | 列举文件时必填，`page_size` 最大为 100（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)） |

## 使用方式

### 1. 上传文件（支持多文件）
```http
POST https://dashscope.aliyuncs.com/api/v1/files
Content-Type: multipart/form-data
```
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -F 'files=@file1.jsonl' \
  -F 'purpose=fine-tune' \
  -F 'descriptions="training data"' \
  -F 'files=@file2.pdf' \
  -F 'purpose=file-extract'
```

### 2. 查询单个文件
```http
GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}
```

### 3. 列举所有文件（分页）
```http
GET https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=50
```

### 4. 删除文件
```http
DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}
```

## 限制和注意事项

- **配额限制**：  
  - 有效文件总数量 ≤ 10,000 个  
  - 有效文件总存储空间 ≤ 100 GB  
  - 单文件大小依 `purpose` 不同：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调训练数据需 `.zip` 格式且 ≤ 1 GB，或通过 OSS 挂载）——详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。  

- **行为约束**：  
  - 上传失败时，响应中 `data.failed_uploads` 包含具体错误码（如 `BadRequest.TooLarge`），需主动检查。  
  - 删除文件后，关联的 `file_id` 将失效，且无法用于任何下游任务（如微调、提取）。  
  - `purpose` 一旦设定不可修改，如需变更用途，须重新上传。  

> **注意**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)”。该建议具有一致性，开发者新建集成时应直接采用兼容接口（路径 `/compatible-mode/v1/files`），以获得长期维护保障与功能同步。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


