# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，适用于 fine-tune、file-extract、batch 等场景。该接口为 DashScope 原生协议，**当前主要用于兼容历史场景**，新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持多文件并发上传（`multipart/form-data`），按 `purpose` 分类管理（`fine-tune` / `file-extract` / `batch`）；视频/图像微调需以 `.zip` 格式上传（单包 ≤1 GB），或通过 OSS 挂载方式加载未压缩数据集  
- **查询文件**：根据 `file_id` 获取单个文件元信息与临时下载链接（`url` 字段）  
- **列举文件**：分页获取当前用户全部有效文件列表，返回含 `purpose` 字段的完整文件对象  
- **删除文件**：异步释放存储空间与关联资源  

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及地域限制，且 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（见 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）已全地域可用。建议新接入直接使用兼容接口以规避地域约束。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path（GET/DELETE） | 是 | 文件唯一标识，由上传接口返回，详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `page_no` / `page_size` | Number | query（GET /files） | 是 | 分页参数，`page_size` 范围 1–100，默认 10 |
| `files` | 文件流 | multipart/form-data（POST） | 是 | 待上传的二进制文件，支持多字段同名上传 |
| `purpose` | String | multipart/form-data（POST） | 否 | 明确用途可提升后续任务调度效率；取值见下表 |
| `descriptions` | String | multipart/form-data（POST） | 否 | 文件描述文本，非必填但推荐提供 |

`purpose` 取值说明：
- `fine-tune`：用于模型微调（训练数据需为 `.jsonl` 或 `.zip`）
- `file-extract`：用于内容解析与结构化提取
- `batch`：用于创建 Batch [异步任务](../concepts/asynchronous-task.md)  
未指定时文件仍可上传，但无法被 purpose-aware 功能自动识别。

## 使用方式

1. **上传**：`POST /api/v1/files`，携带 `files` 和可选 `purpose`/`descriptions`  
2. **查询单个文件**：`GET /api/v1/files/{file_id}`，响应中 `data.url` 为带签名的临时 OSS 下载链接（有效期约 1 小时）  
3. **列举文件**：`GET /api/v1/files?page_no=1&page_size=20`，响应 `data.files[]` 包含完整文件对象，含 `purpose` 字段  
4. **删除**：`DELETE /api/v1/files/{file_id}`，成功后无响应体，仅返回 `request_id`  

所有请求均需在 Header 中设置 `Authorization: Bearer ${DASHSCOPE_API_KEY}`。详细请求/响应示例请参考 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)。

## 限制和注意事项

- **配额限制**：  
  - 单文件大小：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB（ZIP 包 ≤1 GB）  
  - 总存储空间：100 GB  
  - 总文件数量：10,000 个（仅统计未删除的有效文件）  
- **URL 时效性**：`data.url` 为临时签名链接，过期后需重新查询接口获取新链接  
- **地域限制**：DashScope 原生文件 API 当前仅在北京 Region 可用（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)），其他地域用户请通过控制台或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)操作  
- **错误处理**：上传失败时返回 `data.failed_uploads[]`，含 `code` 与 `message`；通用错误（如 4xx/5xx）返回顶层 `code`/`message` 字段（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


