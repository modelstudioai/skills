# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，适用于 fine-tune、file-extract 和 batch 等场景。该 API 返回结构化文件元数据（如 `file_id`、`url`、`md5`、`purpose`），支持多文件批量上传与分页列举。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。

## 支持的模型/功能

- **上传文件**：支持 `multipart/form-data` 方式上传单个或多个文件，按 `purpose` 分类（`fine-tune`、`file-extract`、`batch`）；视频/图像微调需以 `.zip` 格式上传（单包 ≤1 GB），也可通过 OSS 挂载方式加载未压缩数据集。
- **查询文件**：通过 `GET /api/v1/files/{file_id}` 获取指定文件的完整元信息（含下载 `url`、`md5`、`gmt_create` 等）。
- **列举文件**：支持分页获取用户全部有效文件列表（`page_no`/`page_size`），返回中包含 `purpose` 字段，可用于按用途筛选。
- **删除文件**：通过 `DELETE /api/v1/files/{file_id}` 异步删除文件，成功后不可恢复。

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及 Region 限制，且实际调用中其他 Region（如杭州）已普遍可用。请以控制台实际可用 Region 为准，该限制已过时。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是 | 文件唯一标识，由上传接口返回，用于查询/删除 |
| `purpose` | String | form-data | 否（建议必填） | 取值为 `fine-tune`/`file-extract`/`batch`；影响配额策略与下游任务可用性，详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `page_no`, `page_size` | Number | query | 是 | 列举接口分页参数；`page_size` 范围 1–100（默认 10） |
| `files` | 文件流 | form-data | 是 | 上传接口中以 `@path` 形式提交，支持多字段同名上传多个文件 |
| `descriptions` | String | form-data | 否 | 文件描述文本，非 `description` 字段（后者为响应中字段，值来自上传时 `descriptions` 或空字符串） |

## 使用方式

1. **上传**：  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
     -F 'files=@data.jsonl' \
     -F 'purpose=fine-tune' \
     -F 'descriptions="training data for qwen"'
   ```
   成功响应中 `data.uploaded_files[0].file_id` 即为后续操作所需 ID。

2. **查询**：  
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

3. **列举**：  
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

4. **删除**：  
   ```bash
   curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

所有接口均需在请求头携带 `Authorization: Bearer ${DASHSCOPE_API_KEY}`。

## 限制和注意事项

- **配额限制**：  
  - 单文件大小：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB（ZIP 包 ≤1 GB）；  
  - 总空间配额：100 GB；  
  - 总文件数配额：10,000 个（仅统计未删除的有效文件）——详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

- **地域限制已更新**：文档 1 声明“仅在北京 Region 开放”与当前实际不符，杭州等主流 Region 均已支持，该描述应视为过时。

- **兼容性提示**：  
  所有原始文档均强调“推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，其路径为 `/compatible-mode/v1/files`，提供更一致的语义与错误码体系，新项目应优先采用。

- **文件生命周期**：  
  `url` 字段为临时下载链接（含签名与过期时间），不可长期缓存；`file_id` 为长期有效标识。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


