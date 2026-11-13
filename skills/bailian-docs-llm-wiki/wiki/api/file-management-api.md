# file management api

文件管理 API 提供对上传、查询、删除和元数据操作等文件生命周期能力的支持，适用于模型训练、推理输入、知识库构建等场景。该 API 与百炼平台的模型服务深度集成，支持异步上传与状态轮询，并通过 `file_id` 统一标识资源。所有操作均需通过 `Authorization: Bearer <api_key>` 认证。

## 支持的模型/功能

- **核心功能**：文件上传（`POST /v1/files`）、列表查询（`GET /v1/files`）、单文件详情获取（`GET /v1/files/{file_id}`）、文件删除（`DELETE /v1/files/{file_id}`）  
- **格式支持**：`.txt`, `.pdf`, `.docx`, `.xlsx`, `.csv`, `.json`, `.md`（详见 [文件管理](../../raw/model-api-reference/file-management-api.md)）  
- **适用模型**：当前仅支持 `qwen-max`, `qwen-plus`, `qwen-turbo` 及 `bailian-embedding-v1` 等明确声明支持文件输入的模型；其他模型调用时若传入 `file_id` 将返回 `400 Bad Request` —— 此限制在 [文件管理](../../raw/model-api-reference/file-management-api.md) 中有明确定义，但部分旧版 SDK 示例误将 `qwen-1.5-72b-chat` 列为兼容模型，> **注意**：该模型实际不支持文件引用，请以 [文件管理](../../raw/model-api-reference/file-management-api.md) 的最新说明为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | binary | 是（上传时） | multipart/form-data 格式二进制文件体，最大 100 MB |
| `purpose` | string | 否 | 取值为 `"fine-tune"` 或 `"assistants"`；默认为 `"assistants"`，影响后续使用上下文（如知识库索引） |
| `file_id` | string | 是（除上传外） | 全局唯一文件标识符，由上传响应返回的 `id` 字段提供 |

## 使用方式

1. **上传文件**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/files \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@report.pdf" \
     -F "purpose=assistants"
   ```
   成功响应包含 `id`, `filename`, `status`（通常为 `"uploaded"` 或 `"processing"`）等字段。

2. **轮询处理状态**（如需解析 PDF/DOCX 内容）：  
   调用 `GET /v1/files/{file_id}`，检查 `status` 是否变为 `"processed"`；若为 `"error"`，需查看 `error.message`。

3. **在模型请求中引用**：  
   在 `messages` 或 `input` 中通过 `{"file_id": "xxx"}` 结构传入（具体格式依模型而定），详见各模型的 input schema 文档。

## 限制和注意事项

- 单文件大小上限：100 MB（硬性限制，超限返回 `413 Payload Too Large`）  
- 每个账号默认配额：10,000 个文件（可申请提升）  
- 已删除文件不可恢复，且 `file_id` 不再有效；重复上传相同内容文件会生成新 `file_id`  
- 文件元数据（如 `created_at`, `size_bytes`）仅在 `GET /v1/files/{file_id}` 响应中返回，列表接口 `GET /v1/files` 默认不包含 `size_bytes` 字段 —— 此行为与 [文件管理](../../raw/model-api-reference/file-management-api.md) 描述一致，但部分早期文档草稿曾错误声称列表接口含完整元数据，> **注意**：请以 [文件管理](../../raw/model-api-reference/file-management-api.md) 的正式定义为准。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


