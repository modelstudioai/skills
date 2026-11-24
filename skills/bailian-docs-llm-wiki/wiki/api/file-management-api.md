# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该 API 为历史兼容接口，**推荐开发者优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，以获得更统一、持续演进的体验。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 参数划分使用场景，不同用途对应不同下游能力：

- `fine-tune`：用于模型微调训练数据（支持 `.jsonl`、`.zip` 等格式；视频/图像微调需 `.zip`，单包 ≤1 GB）；文件在控制台「模型调优」页与 API 中均可见。
- `file-extract`：用于文档内容解析与结构化提取（如 PDF、Word、Excel 等）。
- `batch`：用于创建 [Batch 任务](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，批量处理提示词请求。

> **注意**：文档 1 中说明 fine-tune 的 zip 文件“单个 zip 包不超过 1 GB”，但文档 2 的文件对象定义及实际上传限制未提及此值；该约束仅在文档 1 的 purpose 说明中明确，应以文档 1 为准。另需注意，[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 接口支持多文件同请求上传，而 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中的列举接口返回字段含 `purpose`（见返回示例），但文档 1 的上传参数表未将 `purpose` 标为“必选”，实际建议始终显式指定。

## 关键参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 待上传文件，支持一次请求多个 `files` 字段 |
| `purpose` | 字符串 | `multipart/form-data` | 否（**强烈建议指定**） | 取值为 `fine-tune` / `file-extract` / `batch`；影响后续可用性与配额统计 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非文件名，用于业务标识 |

此外，管理类接口共用以下路径/查询参数：
- `GET /api/v1/files/{file_id}`：`file_id` 从上传响应或列举结果中获取；
- `GET /api/v1/files`：需传 `page_no`（≥1）和 `page_size`（1–100）；
- `DELETE /api/v1/files/{file_id}`：仅需 `file_id`。

## 使用方式

### 上传文件（POST）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/data.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tuning dataset"'
```

### 查询单个文件（GET）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举文件（GET）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件（DELETE）
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤150 MB，`batch` ≤500 MB，`fine-tune` ≤300 MB（zip 包额外允许 ≤1 GB，见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；
  - 总有效文件数 ≤10,000 个；
  - 总有效文件存储空间 ≤100 GB。

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；其他 Region 用户须通过对应 Region 的百炼控制台管理文件（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。该兼容接口路径为 `/compatible-mode/v1/files`，行为与 OpenAI v1 Files API 高度一致，是新项目的首选。

- **错误处理**：非 200 响应体含 `code` 和 `message` 字段（如 `"code": "BadRequest.TooLarge"`），需结合 `request_id` 追踪问题。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


