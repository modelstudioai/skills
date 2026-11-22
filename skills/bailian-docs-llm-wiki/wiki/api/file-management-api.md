# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，支持多用途文件复用（如 `fine-tune`、`file-extract`、`batch`）。该接口为 DashScope 原生实现，**当前仅在北京 Region 开放**；其他地域用户需通过控制台操作或使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 和 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 是核心操作入口。

## 支持的模型/功能

- **不绑定具体模型**：文件管理 API 本身是基础设施层能力，不直接调用语言模型，但所上传文件可被下游服务复用，例如：
  - `purpose=fine-tune`：用于 Qwen 等模型的微调训练（支持 `.jsonl`、`.zip` 格式）；
  - `purpose=file-extract`：用于文档内容解析与结构化提取；
  - `purpose=batch`：用于创建批量推理任务。
- **兼容性路径**：除原生接口外，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)，其路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 API 对齐。

> **注意**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 OpenAI 兼容的 File 接口”，但未说明原生接口是否计划下线。开发者应以 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 作为新项目首选。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是（GET/DELETE） | 文件唯一标识，由上传接口返回，见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `page_no`, `page_size` | Number | query | 是（LIST） | 分页参数：`page_no ≥ 1`，`page_size ∈ [1, 100]` |
| `files` | 文件流 | multipart/form-data | 是（UPLOAD） | 支持一次上传多个文件，每个文件需单独 `--form 'files=@...'` |
| `purpose` | String | multipart/form-data | 否（UPLOAD） | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应用途服务识别 |
| `descriptions` | String | multipart/form-data | 否（UPLOAD） | 文件描述文本，非文件名，最大长度未明确定义，建议 ≤ 500 字符 |

## 使用方式

1. **上传文件**（POST `/api/v1/files`）  
   使用 `multipart/form-data`，支持多文件、指定 `purpose` 和 `descriptions`。示例见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

2. **查询单个文件**（GET `/api/v1/files/{file_id}`）  
   传入 `file_id` 获取元数据及临时下载链接（`url` 字段有效期有限，不可长期缓存）。

3. **列举文件**（GET `/api/v1/files`）  
   支持分页，返回 `files[]` 数组，含 `purpose` 字段（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 返回示例）。

4. **删除文件**（DELETE `/api/v1/files/{file_id}`）  
   成功响应无 body，仅含 `request_id`；失败时返回 `code` 和 `message`。

## 限制和注意事项

- **地域限制**：原生文件管理 API **仅在北京 Region 开放**；其他地域用户必须使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)或控制台，此限制在 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文档末尾明确声明。
- **配额限制**（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调需 `.zip`，单包 ≤ 1 GB）；
  - 总空间：100 GB；
  - 总文件数：10,000 个。
- **文件生命周期**：`url` 字段为临时 OSS 下载链接，含签名与过期时间（如示例中 `Expires=1679797621`），**不可持久化存储或长期复用**。
- **purpose 字段一致性**：上传时指定的 `purpose` 决定文件可用范围；例如 `purpose=file-extract` 的文件不能用于 `fine-tune` 任务，且该字段在查询/列举响应中均存在，可用于客户端过滤。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


