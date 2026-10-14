# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，适用于 fine-tune、file-extract 和 batch 等场景。该 API 返回结构化文件元数据（如 `file_id`、`url`、`md5`、`purpose`），支持多文件批量上传与分页列举。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，详见 [原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md) 和 [原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

## 支持的模型/功能

- **上传文件**：支持 `multipart/form-data` 方式一次上传多个文件，按 `purpose` 分类（`fine-tune`、`file-extract`、`batch`）；视频/图像微调需以 `.zip` 格式上传（单个 ≤1 GB），也可通过 OSS 挂载方式加载未压缩数据集。
- **查询文件**：通过 `GET /api/v1/files/{file_id}` 获取单个文件详情，含下载链接、MD5、大小、上传时间等元信息。
- **列举文件**：支持分页查询全部文件（`page_no`/`page_size`），返回含 `purpose` 字段的文件列表，便于按用途筛选。
- **删除文件**：通过 `DELETE /api/v1/files/{file_id}` 异步删除指定文件。

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及 Region 限制，且实际 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/files`）已支持多 Region。建议优先使用 OpenAI 兼容路径以规避地域限制，详见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是 | 文件唯一标识，由上传接口返回，用于查询/删除 |
| `page_no` | Number | query | 是 | 当前页码，最小值为 1 |
| `page_size` | Number | query | 是 | 每页数量，范围 1–100 |
| `purpose` | String | form-data | 否 | 文件用途，取值 `fine-tune`/`file-extract`/`batch`；不传则默认无用途，但影响后续功能可用性 |
| `files` | 文件流 | form-data | 是 | 多文件上传时可重复传递，支持同请求上传多个文件 |
| `descriptions` | String | form-data | 否 | 文件描述文本，非必填，但建议填写以便管理 |

## 使用方式

1. **上传文件**（POST `/api/v1/files`）  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
     -F 'files=@data.jsonl' \
     -F 'purpose=fine-tune' \
     -F 'descriptions="training data for qwen"'
   ```
   成功响应中 `data.uploaded_files[].file_id` 即为后续操作所需 ID。

2. **查询文件详情**（GET `/api/v1/files/{file_id}`）  
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/files/mbSwIGR9yA6i1EtwIpndFErIoDKFyQ6W5601487ECAB111EDA20422ECF4959B5E" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

3. **列举文件**（GET `/api/v1/files?page_no=1&page_size=20`）  
   响应中 `data.files[].purpose` 可用于过滤特定用途文件。

4. **删除文件**（DELETE `/api/v1/files/{file_id}`）  
   删除后不可恢复，`file_id` 将失效。

## 限制和注意事项

- **配额限制**：有效文件总数上限 10,000 个，总存储空间上限 100 GB。
- **单文件大小限制**：依 `purpose` 不同而异 — `file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB（ZIP 包 ≤1 GB）。
- **Region 限制**：原生 `/api/v1/files` 接口仅在北京 Region 可用；其他 Region 用户必须使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)（`/compatible-mode/v1/files`）或控制台操作。
- **兼容性提示**：两篇原始文档均强调“推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该接口语义一致、多 Region 支持更完善，且与主流 SDK 兼容性更好 — 建议新项目直接采用，详见 [原文标题](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


