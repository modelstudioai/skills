# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 决定后续可接入的服务类型：

- `fine-tune`：用于模型微调训练数据（支持 `.jsonl`、`.zip` 等格式；视频/图像微调需传 `.zip`，单包 ≤1 GB）；文件在控制台「模型调优」页与 API 中均可见。
- `file-extract`：用于文档内容解析与结构化提取（如 PDF、Word、Excel 等文本类文件）。
- `batch`：用于创建 [Batch 任务](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，支持异步批量推理。

> **注意**：文档 1 中说明 `fine-tune` 用途下“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，而文档 2 的文件对象定义及列举返回示例中均包含 `purpose` 字段且明确可用于 `fine-tune` 和 `file-extract`，二者一致；但文档 1 中 `purpose` 参数描述表格内将 `descriptions` 类型误标为“文件流”，实际应为字符串（见请求示例与文档 2 的 `data.description` 字段），此为笔误。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但**强烈建议显式指定**以便归类管理（详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非文件流（文档 1 表格中类型标注错误，以实际示例和 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 返回字段 `data.description` 为准） |
| `file_id` | 字符串 | path（URL 路径） | 是（单文件操作） | 通过上传或列举接口获取，用于 `GET /files/{file_id}` 或 `DELETE /files/{file_id}` |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数，`page_size` 最大为 100（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)） |

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
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举所有文件（GET `/api/v1/files`）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=50" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件（DELETE `/api/v1/files/{file_id}`）
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

## 限制和注意事项

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过对应 Region 的百炼控制台完成文件管理（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 末尾说明）。
- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调 zip 包 ≤ 1 GB，属特例）；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该建议具有一致性，新集成应直接选用 `/compatible-mode/v1/files` 路径。
- **错误处理**：HTTP 非 200 响应体含 `code`、`message`、`request_id`；成功响应中 `data.failed_uploads` 可定位具体失败文件及原因（如 `BadRequest.TooLarge`、`BadRequest.TooMany`）。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


