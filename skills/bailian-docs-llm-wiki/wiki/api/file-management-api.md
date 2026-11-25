# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途（如微调、内容提取、批量任务）的文件生命周期管理。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 参数区分使用场景，对应不同下游能力：

- `fine-tune`：用于模型微调训练数据（支持 `.jsonl`、`.zip` 等格式；视频/图像微调需 ZIP，单包 ≤1 GB；OSS 挂载方式也支持未压缩文件夹）  
- `file-extract`：用于文档内容解析与结构化提取（如 PDF、Word、Excel 等）  
- `batch`：用于创建 Batch 异步任务（如批量推理）  

> **注意**：文档 1 中说明 `fine-tune` 用途下 ZIP 文件单个不超过 1 GB，但文档 1 同时又在“使用限制”中指出 `fine-tune` 单文件大小上限为 300MB —— 此处存在矛盾。实际以 [上传文件 (raw/model-api-reference/file-management-api/upload-file-api.md)](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中“使用限制”为准：`fine-tune` 用途单文件严格限制为 **300MB**；超限 ZIP 需拆分或改用 OSS 挂载方式。

## 关键参数

### 上传接口（`POST /api/v1/files`）关键参数
| 字段 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `files` | 文件流 | 是 | 支持多文件，`multipart/form-data` 方式提交 |
| `purpose` | 字符串 | 否 | 取值：`fine-tune` / `file-extract` / `batch`；[推荐明确指定](../../raw/model-api-reference/file-management-api/upload-file-api.md)，便于后续按用途筛选与管理 |
| `descriptions` | 字符串 | 否 | 文件描述信息，非文件流（文档 1 表格中误标为“文件流”，应为字符串类型） |

### 查询/列举/删除接口通用参数
- `file_id`（path）：所有单文件操作（GET `/files/{file_id}`、DELETE `/files/{file_id}`）必需，由上传响应返回  
- `page_no` & `page_size`（query）：仅 `GET /api/v1/files` 列举接口需要；`page_size` 最大为 100，最小为 1  

## 使用方式

### 1. 上传文件（支持多文件）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/data.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tune dataset"'
```

### 2. 查询单个文件详情
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 3. 列举所有文件（分页）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=50" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 4. 删除文件
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

完整请求/响应结构与示例详见 [上传文件 (raw/model-api-reference/file-management-api/upload-file-api.md)](../../raw/model-api-reference/file-management-api/upload-file-api.md) 和 [查询和管理文件 (raw/model-api-reference/file-management-api/get-file-api.md)](../../raw/model-api-reference/file-management-api/get-file-api.md)。

## 限制和注意事项

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；其他 Region 用户需通过控制台操作，或使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（其跨 Region 可用）  
- **配额限制**：
  - 单文件大小：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB（[原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md)）  
  - 总存储空间：100 GB（有效文件，即未删除状态）  
  - 总文件数量：10,000 个（有效文件）  
- **行为约束**：
  - 上传失败时，响应中 `data.failed_uploads` 包含具体错误码（如 `BadRequest.TooLarge`）和原因  
  - 删除操作不可逆，且无确认机制；删除后 `file_id` 不可复用  
  - `purpose` 一旦设定不可修改，如需变更用途，请重新上传  
- **兼容性提示**：两个原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)”——该建议具有一致性，新集成应遵循此指引。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


