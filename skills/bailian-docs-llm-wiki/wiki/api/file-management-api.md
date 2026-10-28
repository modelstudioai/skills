# file management api

百炼平台的文件管理 API 提供[文件上传](../concepts/file-upload.md)、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该 API 为历史兼容接口，**推荐开发者优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，以获得更统一、持续演进的体验。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，对应下游能力：
- `fine-tune`：用于模型微调（含文本、视频、图像生成类模型），训练数据支持 `.jsonl` 或 `.zip`（单个 zip ≤ 1 GB）；视频/图像微调要求 zip 格式，也可通过 OSS 挂载方式加载未压缩数据集。
- `file-extract`：用于文件内容解析与结构化提取（如 PDF/Word 表格识别、OCR 等）。
- `batch`：用于创建 Batch 异步推理任务，详见 [Batch 接口文档](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：文档 1 中称“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但文档 2 的文件对象定义及列举接口返回示例中明确包含 `purpose: "file-extract"` 和 `purpose: "fine-tune"` 字段，且未限定格式；实际支持情况以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 接口的 `purpose` 参数说明为准，建议以文档 1 的格式要求为当前有效约束。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否（但强烈建议指定） | 取值为 `fine-tune` / `file-extract` / `batch`；未指定时文件可上传成功，但无法被下游任务自动识别和调用 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，最大长度未明确定义，建议控制在 500 字符内 |

查询与删除操作的关键路径参数：
- `file_id`：通过上传响应中的 `data.uploaded_files[0].file_id` 或列举接口 `data.files[].file_id` 获取，是所有单文件操作（GET / DELETE）的必需 path 参数。
- `page_no` / `page_size`：仅用于 `GET /api/v1/files` 列举接口，`page_no` ≥ 1，`page_size` ∈ [1, 100]。

## 使用方式

### 上传文件（POST `/api/v1/files`）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file1.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tune sample"' \
  --form 'files=@"/path/to/file2.pdf"' \
  --form 'purpose="file-extract"'
```

### 查询单个文件（GET `/api/v1/files/{file_id}`）
返回文件元信息及预签名下载 URL（有效期有限），详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)。

### 列举所有文件（GET `/api/v1/files`）
支持分页，例如 `?page_no=1&page_size=50`。响应中 `data.files[].purpose` 字段可用于按用途筛选资源。

### 删除文件（DELETE `/api/v1/files/{file_id}`）
成功响应仅含 `request_id`，无 body；失败时返回 `code` 和 `message`。

## 限制和注意事项

- **地域限制**：当前文件管理 API 仅在北京 Region（`cn-beijing`）开放。如您使用其他 Region，请通过该 Region 的百炼控制台完成文件管理操作 —— 此限制在 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文档末尾明确声明。
- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（zip 包 ≤ 1 GB）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。该 OpenAI 兼容路径为 `/compatible-mode/v1/files`，提供与 OpenAI Files API 高度一致的语义和行为，是新项目首选。
- **错误处理**：上传失败时，响应 `data.failed_uploads[]` 包含具体错误码（如 `BadRequest.TooLarge`）和消息；通用错误（如 `InvalidParameter`）在 HTTP 非 200 响应体中返回。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


