# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除能力，支持多用途文件复用（如微调、内容提取、批量推理等）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理本身不绑定具体模型，但通过 `purpose` 参数明确文件用途，从而关联下游能力：
- `fine-tune`：用于模型微调（支持 `.jsonl`、`.zip` 等格式；视频/图像微调训练数据需以 `.zip` 上传，单个 zip 不超过 1 GB）；
- `file-extract`：用于内容解析与结构化提取；
- `batch`：用于创建 Batch 任务（[创建Batch任务](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai)）。

> **注意**：文档 1 中说明“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，而文档 2 的文件对象定义及列举接口返回示例中均包含 `purpose` 字段（如 `"purpose": "fine-tune"`），但未重复强调 zip 限制。该约束仅在 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中明确定义，开发者应以该文档为准。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则上传成功但无法按用途归类管理 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非文件名，不影响功能 |
| `file_id` | 字符串 | path（URL 路径） | 是（获取/删除时） | 由上传接口返回，全局唯一，用于后续操作 |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数，`page_size` 最大为 100 |

## 使用方式

### 上传文件
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file1.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tune sample"' \
  --form 'files=@"/path/to/file2.zip"' \
  --form 'purpose="fine-tune"'
```
> 返回包含 `uploaded_files[].file_id` 和 `failed_uploads[]`，详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

### 查询单个文件
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```
返回含 `url`（临时下载链接）、`size`、`md5`、`purpose` 等字段，详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)。

### 列举所有文件
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```
响应中 `data.files[].purpose` 字段可用于过滤用途，`data.total` 表示总数。

### 删除文件
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```
成功返回仅含 `request_id`，失败时返回 `code` 和 `message`。

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（zip 包上限为 1 GB，见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。
- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；其他 Region 用户需通过控制台操作（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 OpenAI 兼容的 File 接口”。若新项目无历史依赖，应直接采用 `/compatible-mode/v1/files` 路径。
- **purpose 字段一致性**：`purpose` 在上传时指定，在列举和详情接口中均会返回，是区分文件用途的核心字段；但上传时不传 `purpose` 仍可成功（仅影响后续管理），建议始终显式声明。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


