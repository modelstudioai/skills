# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，支持多用途文件复用（如 fine-tune、file-extract、batch）。该接口采用 RESTful 设计，基于 `https://dashscope.aliyuncs.com/api/v1/files` 路径提供服务。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，详见 [原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md) 和 [原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，按 `purpose` 分类（`fine-tune`、`file-extract`、`batch`），上传后生成唯一 `file_id` 供后续任务引用。
- **查询文件**：通过 `GET /files/{file_id}` 获取指定文件元信息与可下载 URL。
- **列举文件**：分页获取当前账户下所有有效文件列表，支持按 `page_no` 和 `page_size` 控制返回范围。
- **删除文件**：通过 `DELETE /files/{file_id}` 异步删除文件（删除后不可恢复）。

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及 Region 限制；实际调用时若在非北京 Region 遇到 404 或权限错误，请优先确认所用 endpoint 是否匹配所在 Region，或改用对应 Region 的控制台操作 —— 此不一致已在 [原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md) 明确标注。

## 关键参数

| 参数名 | 类型 | 位置 | 必选 | 说明 |
|--------|------|------|------|------|
| `file_id` | String | path | 是（查询/删除） | 文件唯一标识，由上传接口返回，见 [原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `page_no` | Number | query | 是（列举） | 当前页码，最小值为 1，默认为 1 |
| `page_size` | Number | query | 是（列举） | 每页数量，取值范围 1–100，默认为 10 |
| `purpose` | String | multipart/form-data | 否（上传） | 指定文件用途：`fine-tune`（最大 300MB）、`file-extract`（最大 150MB）、`batch`（最大 500MB）；不传则默认无用途标记 |
| `files` | 文件流 | multipart/form-data | 是（上传） | 支持多次 `--form 'files=@...'` 上传多个文件 |
| `descriptions` | String | multipart/form-data | 否（上传） | 文件描述文本，建议简明说明内容用途 |

## 使用方式

- **上传**：`POST /api/v1/files`，`Content-Type: multipart/form-data`，需携带 `files` 和可选 `purpose`、`descriptions` 字段。
- **查询**：`GET /api/v1/files/{file_id}`，需在 Header 中提供 `Authorization: Bearer ${DASHSCOPE_API_KEY}`。
- **列举**：`GET /api/v1/files?page_no=1&page_size=20`，同上鉴权。
- **删除**：`DELETE /api/v1/files/{file_id}`，同上鉴权。

所有请求均需使用有效的 DashScope API Key，并确保其具备文件管理权限。返回体中 `request_id` 用于问题排查与日志追踪。

## 限制和注意事项

- **配额限制**：
  - 单个文件大小上限依 `purpose` 而异（`file-extract`: ≤150MB；`batch`: ≤500MB；`fine-tune`: ≤300MB；视频/图像微调训练数据需以 `.zip` 格式上传，单包 ≤1GB）；
  - 有效文件总数量上限：10,000 个；
  - 有效文件总存储空间上限：100 GB。
- **地域限制**：API 仅在北京 Region 可用，其他 Region 用户应通过控制台操作或切换至对应 Region 的兼容接口。
- **兼容性提示**：两个原始文档均强调“推荐优先使用 OpenAI 兼容的 File 接口”，该接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 Files API 对齐，更适合新项目集成。
- **文件生命周期**：已删除文件无法恢复，且其 `file_id` 不再可用于任何 API 调用（包括查询或作为任务输入）。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


