# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途（如 fine-tune、file-extract、batch）的文件生命周期管理。该接口为 DashScope 原生协议，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 对应不同下游能力：

- `fine-tune`：用于模型微调训练数据（支持 `.jsonl`、`.zip` 等格式；视频/图像生成模型微调要求训练数据以 `.zip` 格式上传，单个 zip 不超过 1 GB）；上传后可在控制台「模型调优」页面及 API 中直接引用。
- `file-extract`：用于内容提取与分析任务（如 PDF/Word 文本解析、表格识别等）。
- `batch`：用于创建 Batch 异步推理任务（详见 [batch-interfaces-compatible-with-openai](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai)）。

> **注意**：文档 1 中说明“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但未明确是否支持其他格式（如纯文件夹 OSS 挂载）。而文档 2 的「文件对象」小节及列举接口返回中均包含 `purpose` 字段，且示例中 `fine-tune` 文件为 `.txt`，表明非 zip 文件亦可上传成功。实际行为以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 接口为准，建议优先按目的选择格式并验证。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件；每个 `files` 字段对应一个文件二进制流 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被下游任务自动识别，**强烈建议显式指定** |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，最大长度未明确定义，建议 ≤ 500 字符 |
| `file_id` | 字符串 | path（URL 路径） | 是（GET/DELETE 单文件时） | 通过 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 返回的 `data.uploaded_files[0].file_id` 获取 |
| `page_no`, `page_size` | 数字 | query | 是（列举接口） | `page_no ≥ 1`，`page_size ∈ [1, 100]`；默认 `page_no=1`, `page_size=10` |

## 使用方式

### 1. 上传文件（POST `/api/v1/files`）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/data.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tuning dataset"'
```
支持多文件同请求上传（重复 `--form 'files=@...'` 即可），响应中 `data.uploaded_files` 包含成功文件的 `file_id`，`data.failed_uploads` 包含失败原因。

### 2. 查询单个文件（GET `/api/v1/files/{file_id}`）
通过 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 获取文件元信息（含 `url` 下载链接、`size`、`md5`、`purpose` 等）。

### 3. 列举文件（GET `/api/v1/files`）
分页获取全部文件列表，响应中 `data.files[].purpose` 显示各文件用途，便于按场景筛选。

### 4. 删除文件（DELETE `/api/v1/files/{file_id}`）
根据 `file_id` 删除指定文件；删除成功仅返回 `request_id`，无 body。

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（zip 包上限为 1 GB，见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过该 Region 的百炼控制台完成文件管理（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)”。新项目应优先接入 `/compatible-mode/v1/files` 路径，以获得长期维护保障与 OpenAI 生态一致性。

- **错误处理**：HTTP 非 200 响应体中包含 `code` 和 `message` 字段（如 `BadRequest.TooLarge`），需在客户端做针对性重试或降级处理。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


