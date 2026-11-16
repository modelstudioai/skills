# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，适用于 fine-tune、file-extract 和 batch 等场景。该 API 返回结构化文件元数据（如 `file_id`、`url`、`md5`、`purpose`），支持多文件批量上传与分页列举。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，详见 [原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md) 和 [原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

## 支持的模型/功能

- **上传文件**：支持 `multipart/form-data` 方式上传一个或多个文件，按 `purpose` 分类（`fine-tune`、`file-extract`、`batch`），上传后生成唯一 `file_id` 供后续任务复用。
- **查询文件**：通过 `GET /api/v1/files/{file_id}` 获取单个文件的完整元数据及可下载 `url`。
- **列举文件**：通过 `GET /api/v1/files?page_no=1&page_size=20` 分页获取当前用户所有有效文件列表，响应中包含 `purpose` 字段（见 [原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md) 返回示例）。
- **删除文件**：通过 `DELETE /api/v1/files/{file_id}` 永久移除指定文件（不可恢复）。

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及 Region 限制；实际调用时若在非北京 Region 遇到 404 或权限错误，请优先确认 Region 配置，或改用对应 Region 的百炼控制台操作——该不一致需以控制台文档或最新 SDK 为准。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是 | 文件唯一标识，由上传接口返回，用于查询/删除 |
| `page_no` | Number | query | 是 | 当前页码，最小值为 1 |
| `page_size` | Number | query | 是 | 每页数量，取值范围 1–100 |
| `files` | 文件流 | multipart/form-data | 是 | 待上传的文件二进制流（支持多文件） |
| `purpose` | String | multipart/form-data | 否 | 明确用途：`fine-tune`（最大 300MB）、`file-extract`（最大 150MB）、`batch`（最大 500MB）；不传则默认无用途，但影响后续功能可用性 |
| `descriptions` | String | multipart/form-data | 否 | 文件描述文本，非必填，但建议提供 |

## 使用方式

1. **上传文件**（推荐携带 `purpose`）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
     -F 'files=@data.jsonl' \
     -F 'purpose=fine-tune' \
     -F 'descriptions="training data for qwen"'
   ```
   成功响应含 `data.uploaded_files[].file_id`，可用于后续操作。

2. **查询文件详情**：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/files/mbSwIGR9yA6i1EtwIpndFErIoDKFyQ6W5601487ECAB111EDA20422ECF4959B5E" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

3. **列举文件**（支持分页）：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=50" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

4. **删除文件**：
   ```bash
   curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/mbSwIGR9yA6i1EtwIpndFErIoDKFyQ6W5601487ECAB111EDA20422ECF4959B5E" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```

## 限制和注意事项

- **配额限制**：  
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调需 .zip 格式，单包 ≤ 1 GB）；  
  - 总存储空间：≤ 100 GB（有效文件）；  
  - 总文件数量：≤ 10,000 个（有效文件）。

- **Region 限制**：  
  > **注意**：[原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md) 明确指出“当前文件管理 API 仅在北京 Region 开放”，若在其他 Region 调用失败，请切换至北京 Region 的 endpoint 或使用对应 Region 控制台。

- **兼容性提示**：  
  所有原始文档均强调“推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，其路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 API 对齐，长期维护性更高。

- **安全性**：  
  `url` 字段为临时预签名 OSS 下载链接，有效期有限（通常数小时），不可长期缓存；敏感文件请勿公开暴露该 URL。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


