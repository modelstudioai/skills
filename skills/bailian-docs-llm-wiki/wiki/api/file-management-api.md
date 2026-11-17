# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 决定后续可接入的服务类型：

- `fine-tune`：用于模型微调训练数据（支持 `.jsonl`、`.zip` 等格式；视频/图像微调需 zip 包 ≤ 1 GB）；文件在控制台「模型调优」页与 API 中均可见。
- `file-extract`：用于文档内容解析与结构化提取（如 PDF、Word、Excel 等），最大单文件 150 MB。
- `batch`：用于创建 Batch [异步任务](../concepts/asynchronous-task.md)，最大单文件 500 MB。

> **注意**：文档 1 中说明 fine-tune 场景“也可通过 OSS 挂载方式加载”，但该能力未在 [查询和管理文件](raw/model-api-reference/file-management-api/get-file-api.md) 文档中体现，且当前 API 不提供 OSS 挂载相关字段或接口，实际开发中请以控制台或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)为准。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件；每个文件需配对指定 `purpose` 和 `descriptions`（若提供） |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应服务识别，[上传文件](raw/model-api-reference/file-management-api/upload-file-api.md) 文档明确建议显式指定 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述文本，非必填，不影响功能 |

在查询类接口中：
- `file_id`（path 参数）为所有 GET/DELETE 接口必需；
- 列举文件时需提供 `page_no` 和 `page_size`（均为 query 参数，`page_size` 最大 100）。

## 使用方式

### 上传文件
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tuning dataset"'
```

### 查询单个文件
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举全部文件
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

所有响应均含 `request_id`，可用于问题排查；失败响应 HTTP 状态码非 200，body 含 `code` 和 `message` 字段，详见 [上传文件](raw/model-api-reference/file-management-api/upload-file-api.md) 的「请求异常」章节。

## 限制和注意事项

- **地域限制**：当前原生文件管理 API 仅在北京 Region 开放；其他 Region 用户需通过对应 Region 的百炼控制台操作，或使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)（该接口支持多 Region）。
- **配额限制**：
  - 有效文件总数量 ≤ 10,000 个；
  - 有效文件总存储空间 ≤ 100 GB；
  - 单文件大小依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（注意：文档 1 中 fine-tune 的 zip 包上限为 1 GB，此为特殊格式例外，非通用限制）。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该建议具有一致性，开发者应优先评估迁移可行性。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


