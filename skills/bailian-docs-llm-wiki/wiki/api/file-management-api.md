# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，按 `purpose` 分类管理（`fine-tune`、`file-extract`、`batch`），上传后生成全局唯一 `file_id` 供下游任务引用。
- **查询文件**：通过 `GET /api/v1/files/{file_id}` 获取单个文件元信息（含下载 URL、MD5、大小等）。
- **列举文件**：分页获取当前用户全部有效文件列表，返回中包含 `purpose` 字段，便于按用途筛选。
- **删除文件**：通过 `DELETE /api/v1/files/{file_id}` 异步清理文件（删除后不可恢复）。

> **注意**：文档 2 明确指出“当前文件管理 API 仅在北京 Region 开放”，但文档 1 未提及地域限制。若在非北京 Region 调用失败，请改用对应 Region 的百炼控制台操作，或切换至 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)，后者已支持多 Region。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持多次出现，上传多个文件；详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但影响后续任务调用与配额统计 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述，最大长度 256 字符 |
| `page_no` / `page_size` | 数字 | Query | 是（列举时） | 分页参数，`page_size` 范围 1–100，默认 10；详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) |
| `file_id` | 字符串 | Path | 是（查/删时） | 由上传接口返回，全局唯一，用于定位文件 |

## 使用方式

- **上传**：`POST https://dashscope.aliyuncs.com/api/v1/files`，使用 `multipart/form-data` 格式提交 `files`、`purpose` 等字段。示例见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。
- **查询单个文件**：`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}`，响应含可直链下载的 `url` 字段。
- **列举文件**：`GET https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20`，返回 `data.files[]` 中每个对象均含 `purpose` 字段，可用于过滤用途。
- **删除文件**：`DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}`，成功响应仅含 `request_id`，无 body。

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调训练数据需 `.zip` 格式，单包 ≤ 1 GB）；
  - 总存储空间：≤ 100 GB（有效文件）；
  - 总文件数量：≤ 10,000 个（有效文件）。
- **地域限制**：原生接口仅在北京 Region 可用；其他 Region 用户请使用控制台或 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **用途一致性**：`purpose` 在上传时指定后不可修改；`fine-tune` 文件仅可在模型调优任务中使用，`file-extract` 文件仅可用于内容解析类 API。
- **错误处理**：HTTP 非 200 响应体含 `code` 和 `message` 字段，常见错误如 `BadRequest.TooLarge`（超空间）、`BadRequest.TooMany`（超数量），详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 的异常说明。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


