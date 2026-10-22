# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该 API 为历史兼容接口，**推荐开发者优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证，且当前仅在北京 Region 可用。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理，适用于 `fine-tune`、`file-extract` 和 `batch` 场景；其中 `fine-tune` 用途支持 `.zip` 格式训练数据（≤1 GB），也支持 OSS 挂载方式加载未压缩数据集（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）。
- **文件查询与管理**：支持按 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。
- **跨任务复用**：上传后的 `file_id` 可在模型微调、内容提取、Batch 推理等下游任务中直接引用。

> **注意**：文档 1 中提到 fine-tune 的单文件大小上限为 300MB，但文档 2 的“文件对象”小节及文档 1 的“说明”中均明确指出视频/图像生成模型微调的 `.zip` 包可支持 **≤1 GB** —— 此处以实际支持能力为准，300MB 限制不适用于 `.zip` 类型 fine-tune 文件。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件；每个文件需配对 `purpose` 和 `descriptions`（若提供） |
| `purpose` | 字符串 | `multipart/form-data` | 否（但强烈建议指定） | 取值：`fine-tune` / `file-extract` / `batch`；影响后续可用场景及配额统计；未指定时仍可上传，但无法按用途归类管理 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，最大长度未明确定义，建议 ≤512 字符 |
| `file_id` | 字符串 | URL path | 是（查询/删除接口） | 由上传成功响应返回，全局唯一，用于后续操作 |
| `page_no`, `page_size` | 数字 | Query | 是（列举接口） | `page_no ≥ 1`，`page_size ∈ [1, 100]`，默认 `page_no=1`, `page_size=10` |

## 使用方式

- **上传文件**（POST `/api/v1/files`）  
  使用 `multipart/form-data` 提交，示例：
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    -F 'files=@/path/to/data.jsonl' \
    -F 'purpose=fine-tune' \
    -F 'descriptions="qwen fine-tune dataset"'
  ```

- **查询单个文件**（GET `/api/v1/files/{file_id}`）  
  返回含 `url`（临时下载链接）、`size`、`md5`、`purpose` 等完整元信息（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。

- **列举文件**（GET `/api/v1/files`）  
  支持分页，响应中 `data.files[].purpose` 字段明确标识各文件用途，便于按场景筛选。

- **删除文件**（DELETE `/api/v1/files/{file_id}`）  
  成功响应仅含 `request_id`；失败时返回 `code` 和 `message`（如 `ResourceNotFound`）。

## 限制和注意事项

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；其他 Region 用户需通过控制台操作或切换至对应 Region 的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（见 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)）。
- **配额限制**：
  - 单文件大小：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB（纯文本/JSONL）或 ≤1 GB（`.zip` 包）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该兼容接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 规范一致，长期维护性更优。
- **错误处理**：上传失败时响应中 `data.failed_uploads` 明确列出每个失败文件的 `code`（如 `BadRequest.TooLarge`）和 `message`；非 200 响应体结构统一含 `code`、`message`、`request_id`（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）。

> **注意**：文档 2 的“文件对象”小节称 `purpose` 是文件对象的正式字段，且列举接口响应中确实返回 `purpose`；但文档 1 的请求参数表格中将 `purpose` 归类为“multipart/form-data”字段，而未在返回参数中显式声明其属于 `uploaded_files[$]`。实践中，`purpose` 在上传时指定后，将持久化并可在查询/列举响应中稳定获取，开发者可依赖该字段做用途路由。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


