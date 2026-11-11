# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除能力，支持多用途文件复用（如微调、内容提取、批量任务）。该 API 采用 RESTful 设计，基于 `multipart/form-data` 和标准 HTTP 方法实现。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理，适用于 `fine-tune`、`file-extract` 和 `batch` 场景；其中 `fine-tune` 用途支持 `.zip` 格式（≤1 GB）或 OSS 挂载方式加载未压缩数据集。
- **文件查询与管理**：支持通过 `file_id` 获取单个文件详情（含下载链接 `url`、`md5`、`size` 等元信息），分页列举全部文件，并支持按需删除。
- **跨任务复用**：上传后的 `file_id` 可在模型微调、内容提取、Batch 任务等下游接口中直接引用。

> **注意**：文档 2 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 1 未提及地域限制；实际调用时若遇 404 或权限错误，请确认所用 API Endpoint 所属 Region 并参考 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 的 endpoint 示例验证可用性。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持多次提交，实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认可上传但无法被下游任务识别，[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 明确建议显式指定 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述，非必填，但有助于后续管理 |
| `file_id` | 字符串 | path（URL 路径） | 是（查询/删除时） | 由上传成功响应返回，用于精确操作单个文件 |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | `page_no ≥ 1`，`page_size ∈ [1, 100]`，默认 `page_no=1`, `page_size=10` |

## 使用方式

- **上传文件**（POST `/api/v1/files`）  
  使用 `curl --form` 或 SDK 构造 multipart 请求，示例见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。注意：同一请求中多个 `files` 字段可对应不同 `purpose` 和 `descriptions`。

- **查询单个文件**（GET `/api/v1/files/{file_id}`）  
  传入 `file_id` 获取完整元数据，包括可直连下载的 `url`（带临时签名，有效期有限）。

- **列举文件**（GET `/api/v1/files`）  
  支持分页，响应中 `data.files[].purpose` 字段明确标识各文件用途，便于按场景筛选。

- **删除文件**（DELETE `/api/v1/files/{file_id}`）  
  成功响应无 body，仅返回 `request_id`；失败时返回 `code` 和 `message`（如 `NotFound.File`）。

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调训练数据 ZIP 包上限为 1 GB，此为特例，见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。

- **行为约束**：
  - 上传失败时，响应中 `failed_uploads` 包含具体错误码（如 `BadRequest.TooLarge`）和原因，需主动解析；
  - 删除操作不可逆，且删除后 `file_id` 不再可用于任何下游任务；
  - `purpose` 在上传时指定后不可修改，如需变更用途，须重新上传。

- **兼容性提示**：  
  > **注意**：两篇原始文档均强调“推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，其路径为 `/compatible-mode/v1/files`，提供与 OpenAI v1 Files API 高度一致的语义和字段（如 `filename` 替代 `name`，`status` 字段等）。新项目应优先集成该兼容接口，原生接口仅建议用于存量系统迁移过渡。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


