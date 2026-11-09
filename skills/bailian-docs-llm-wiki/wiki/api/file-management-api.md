# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该 API 为 DashScope 原生接口，**当前主要用于兼容历史场景**；新项目应优先采用 OpenAI 兼容的 File 接口以获得更统一的体验和持续演进的功能支持 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理，适用于 `fine-tune`（模型微调）、`file-extract`（内容解析）和 `batch`（批量推理任务）三类核心场景。
- **文件查询与管理**：支持按 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件。
- **文件复用**：上传后的 `file_id` 可在多个下游 API（如微调任务创建、Batch 任务提交、RAG 知识库构建等）中直接引用。

> **注意**：文档 1 中提到“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，但文档 2 的文件对象定义及列举返回示例中均未体现对 `.zip` 的特殊处理逻辑，且 `purpose=fine-tune` 的通用限制仍为 300MB（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）。实际使用中请以上传接口返回的 `BadRequest.TooLarge` 错误为准，避免依赖文档中未被其他接口验证的容量例外说明。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 描述 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 待上传的文件二进制流，支持多次出现实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 指定文件用途：`fine-tune` / `file-extract` / `batch`；不传则默认无用途，但**强烈建议显式指定**以便后续按用途筛选和管理（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述文本，用于人工识别，非结构化字段 |
| `file_id` | 字符串 | path（URL 路径） | 是（查询/删除时） | 文件唯一标识，由上传成功响应返回，格式为 64 位十六进制字符串 |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数：`page_no ≥ 1`，`page_size ∈ [1, 100]`，默认 `page_no=1`, `page_size=10` |

## 使用方式

### 上传文件（POST `/api/v1/files`）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/data.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tuning dataset"'
```
- 支持一次请求上传多个同 `purpose` 的文件（重复添加 `--form 'files=@...'` 即可）。
- 成功响应中 `data.uploaded_files[].file_id` 为后续调用的关键凭证。

### 查询单个文件（GET `/api/v1/files/{file_id}`）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```
- 返回含 `url` 字段，可用于直链下载（有效期有限，需及时使用）。

### 列举文件（GET `/api/v1/files`）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```
- 响应中 `data.files[].purpose` 显示各文件的实际用途，便于按场景过滤（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。

### 删除文件（DELETE `/api/v1/files/{file_id}`）
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```
- 删除后不可恢复，且关联任务（如未启动的微调任务）将失效。

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150MB，`batch` ≤ 500MB，`fine-tune` ≤ 300MB（[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；
  - 总存储空间：100GB（有效文件，即未删除状态）；
  - 总文件数量：10000 个（有效文件）。
- **地域限制**：当前仅在北京 Region 开放 API 访问；其他 Region 用户需通过控制台操作或切换至对应 Region 的百炼服务实例。
- **兼容性提示**：所有接口均标注“**推荐优先使用 OpenAI 兼容的 File 接口**”，因其提供更标准化的路径（`/compatible-mode/v1/files`）、一致的错误码体系及长期维护保障 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。
- **错误处理**：HTTP 非 200 响应体中必含 `code` 和 `message` 字段（如 `InvalidParameter`, `File not found.`），应据此做针对性重试或用户提示。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


