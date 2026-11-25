# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途（如微调、内容提取、批量任务）的文件生命周期管理。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，指定 `purpose` 后可被下游任务复用（如 `fine-tune`、`file-extract`、`batch`）。  
- **查询文件**：通过 `file_id` 获取单个文件的元信息（含 `url`、`size`、`md5`、`purpose` 等），详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)。  
- **列举文件**：分页获取当前用户全部有效文件列表，返回中包含 `purpose` 字段，便于按用途筛选。  
- **删除文件**：释放存储配额并移除文件引用，已删除文件不可恢复。  

> **注意**：文档 1 中提到“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，但文档 2 的 [文件对象](../../raw/model-api-reference/file-management-api/get-file-api.md) 表格明确列出 `purpose` 字段存在于列举接口返回中，而文档 1 的请求参数表格未说明 `purpose` 可在上传时重复指定（如多文件不同 purpose），实际行为以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中的 curl 示例为准——即**每个 `files` 字段可独立绑定 `purpose` 和 `descriptions`**。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持多次出现，用于上传多个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，**强烈建议显式指定**（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 每个文件对应一条描述，与 `files` 顺序一一对应 |
| `file_id` | 字符串 | path | 是（查询/删除） | 由上传成功响应中的 `data.uploaded_files[].file_id` 返回 |
| `page_no`, `page_size` | 数字 | query | 是（列举） | `page_no ≥ 1`，`page_size ∈ [1, 100]` |

## 使用方式

- **上传**：`POST /api/v1/files`，使用 `multipart/form-data`，示例见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。  
- **查询单个文件**：`GET /api/v1/files/{file_id}`，返回含 `url` 的完整元数据。  
- **列举文件**：`GET /api/v1/files?page_no=1&page_size=20`，响应中 `data.files[].purpose` 可用于过滤用途。  
- **删除文件**：`DELETE /api/v1/files/{file_id}`，成功响应仅含 `request_id`（无 body）。  

所有接口均要求 `Accept: application/json`（查询/删除）或正确设置 `Content-Type: multipart/form-data`（上传）。

## 限制和注意事项

- **配额限制**：  
  - 单文件大小上限依 `purpose` 而定：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；  
  - 总有效文件数 ≤ 10,000 个，总有效存储空间 ≤ 100 GB。  
- **地域限制**：当前仅在北京 Region 开放 API 访问；其他 Region 用户需通过控制台管理（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。  
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)”，开发者应评估迁移可行性。  
- **错误处理**：非 200 响应体结构统一（含 `code`、`message`、`request_id`），需解析 `code` 字段判断具体失败原因（如 `BadRequest.TooLarge`、`InvalidParameter`）。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


