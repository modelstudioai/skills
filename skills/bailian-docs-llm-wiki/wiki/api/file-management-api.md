# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，适用于 fine-tune、file-extract 和 batch 等场景。该 API 返回结构化文件元数据（如 `file_id`、`url`、`purpose`），支持多文件上传与分页列举。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)**，详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 和 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

## 支持的模型/功能

- **上传文件**：支持 `multipart/form-data` 多文件上传，按 `purpose` 分类（`fine-tune`、`file-extract`、`batch`）；视频/图像微调需以 `.zip` 格式上传（单个 zip ≤ 1 GB），也可通过 OSS 挂载方式加载未压缩数据集。
- **查询与列举**：支持通过 `GET /api/v1/files/{file_id}` 获取单个文件详情，或 `GET /api/v1/files` 分页列举全部文件。
- **删除文件**：支持 `DELETE /api/v1/files/{file_id}` 删除指定文件。

> **注意**：[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中声明“当前文件管理 API 仅在北京 Region 开放”，但 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 未提及 Region 限制；实际调用时若遇 404 或权限错误，请确认所用 API Endpoint 对应的 Region 是否为 `cn-beijing`，或改用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（`/compatible-mode/v1/files`）。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是 | 文件唯一标识，由上传接口返回，用于查询/删除 |
| `page_no` / `page_size` | Number | query | 是 | 列举文件时分页参数；`page_size` 范围 1–100（默认 10） |
| `files` | 文件流 | multipart/form-data | 是 | 上传时的二进制文件字段，支持多次出现上传多个文件 |
| `purpose` | String | multipart/form-data | 否 | 文件用途，取值 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但**强烈建议显式指定**以便后续管理 |
| `descriptions` | String | multipart/form-data | 否 | 文件描述（注意文档中误标为“文件流”类型，实为字符串，见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |

## 使用方式

1. **上传文件**（示例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
     -F 'files=@data.jsonl' \
     -F 'purpose=fine-tune' \
     -F 'descriptions="training data for qwen"'
   ```
   成功响应中 `data.uploaded_files[].file_id` 即为后续操作凭证。

2. **查询文件**：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

3. **列举文件**（带分页）：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=50" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

4. **删除文件**：
   ```bash
   curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调 zip 包 ≤ 1 GB）；
  - 总存储空间：100 GB；
  - 总文件数：10,000 个（均指有效/未删除文件）。

- **地域限制**：当前原生 `/api/v1/files` 接口仅在北京 Region（`cn-beijing`）可用；其他 Region 用户请使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface) 或百炼控制台操作。

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)”，该建议具有一致性，开发者新项目应直接集成 `/compatible-mode/v1/files` 路径。

- **字段差异**：列举接口返回的文件对象含 `purpose` 字段（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 示例），但查询单个文件的返回示例中未展示 `purpose`；实践中该字段在两种响应中均存在，属文档示例遗漏，非功能缺失。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


