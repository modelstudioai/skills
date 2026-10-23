# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，`purpose` 字段决定后续可用场景：
  - `fine-tune`：用于模型微调（视频/图像生成模型需以 `.zip` 格式上传，单包 ≤1 GB；也可通过 OSS 挂载方式加载未压缩数据集）；
  - `file-extract`：用于内容分析（如 PDF/Word 文本抽取）；
  - `batch`：用于创建 [Batch 任务](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。
- **查询与管理**：支持按 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件。

> **注意**：文档 1 中称 fine-tune 场景下“不支持 zip 文件”，但文档 2 的“文件对象”小节及文档 1 自身的 purpose 说明中均明确指出“视频/图像生成模型微调的训练数据需以 .zip 格式上传”。此处以文档 1 的详细说明为准，即 **zip 支持仅限于视频/图像生成类模型微调场景**；通用 fine-tune（如文本模型）仍建议使用未压缩 JSONL 等格式。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 上传的文件二进制流，支持多次 `--form 'files=@...'` 实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否（但强烈建议指定） | 取值为 `fine-tune` / `file-extract` / `batch`；影响配额计算与下游任务可用性；详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非文件名，用于业务标识 |
| `file_id` | 字符串 | path（URL 路径） | 是（查询/删除时） | 由上传成功响应返回，全局唯一；可通过 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 或列举接口获取 |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数：`page_no ≥ 1`，`page_size ∈ [1, 100]` |

## 使用方式

- **上传文件**（POST `/api/v1/files`）  
  使用 `multipart/form-data`，示例见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。注意：同一请求中多个文件可指定不同 `purpose` 和 `descriptions`。

- **查询单个文件**（GET `/api/v1/files/{file_id}`）  
  返回含 `url`（临时下载链接）、`size`、`md5`、`purpose` 等完整元数据，详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)。

- **列举文件**（GET `/api/v1/files`）  
  支持分页，响应中 `data.files[].purpose` 字段明确标识各文件用途，便于按场景筛选。

- **删除文件**（DELETE `/api/v1/files/{file_id}`）  
  成功响应无 body，仅返回 `request_id`；失败时返回 `code` 和 `message`。

## 限制和注意事项

- **配额限制**：
  - 单文件大小上限依 `purpose` 而定：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调 zip 包 ≤ 1 GB）；
  - 有效文件总空间 ≤ 100 GB；
  - 有效文件总数 ≤ 10,000 个。

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；其他 Region 用户需通过对应 Region 的百炼控制台管理文件（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。新项目应优先采用 OpenAI 兼容路径（`/compatible-mode/v1/files`），其行为、配额和地域支持更一致。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


