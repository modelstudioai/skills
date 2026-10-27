# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，指定 `purpose` 后可被对应下游任务（如 fine-tune、file-extract、batch）直接引用；
- **查询文件详情**：通过 `file_id` 获取元信息（含 `url` 下载链接、`md5`、`size` 等）；
- **列举文件**：分页获取当前用户全部有效文件列表，返回中包含 `purpose` 字段，便于按用途筛选；
- **删除文件**：释放存储配额与文件引用，删除后不可恢复。

> **注意**：文档 2 明确指出“当前文件管理 API 仅在北京 Region 开放”，但文档 1 未提及地域限制。实际调用时若在非北京 Region 遇到 404 或权限错误，请切换至北京 Region 或改用控制台操作 —— 此不一致已在 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中明确标注。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | 文件流 | multipart/form-data | 是 | 支持多次提交，即一次请求上传多个文件 |
| `purpose` | 字符串 | multipart/form-data | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)建议显式指定以便后续管理 |
| `descriptions` | 字符串 | multipart/form-data | 否 | 文件描述，非文件名，用于业务标识 |
| `file_id` | 字符串 | path | 是（GET/DELETE） | 由上传响应返回，全局唯一，用于查/删操作 |
| `page_no`, `page_size` | 数字 | query | 是（列举接口） | `page_no ≥ 1`，`page_size ∈ [1, 100]` |

## 使用方式

### 上传（POST `/api/v1/files`）
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  -F 'files=@/path/to/data.jsonl' \
  -F 'purpose=fine-tune' \
  -F 'descriptions="qwen fine-tuning dataset"'
```

### 查询单个文件（GET `/api/v1/files/{file_id}`）
```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举文件（GET `/api/v1/files`）
```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件（DELETE `/api/v1/files/{file_id}`）
```bash
curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调训练数据需 ZIP 格式且 ≤ 1 GB）；
  - 总存储空间：≤ 100 GB（有效文件，即未删除状态）；
  - 总文件数量：≤ 10,000 个（有效文件）。
- **地域限制**：仅北京 Region 可用，其他 Region 用户请参考 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 的说明。
- **兼容性提示**：两篇原始文档均强调“推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 保持一致，是长期维护的首选方案。
- **失败处理**：上传接口返回 `data.failed_uploads` 数组，含每个失败文件的 `code` 与 `message`（如 `BadRequest.TooLarge`），需主动解析并重试或告警。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


