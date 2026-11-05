# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该 API 为历史兼容接口，**推荐开发者优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，以获得更统一的体验和持续的功能演进。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 决定文件后续可接入的服务类型：

- `fine-tune`：用于模型微调，支持 `.jsonl`（文本微调）和 `.zip`（视频/图像生成模型微调，单个 zip ≤ 1 GB）；文件在控制台「模型调优」页与 API 中均可见可用。  
- `file-extract`：用于内容解析与结构化提取（如 PDF/Word 文本抽取）。  
- `batch`：用于创建 [Batch 任务](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)，批量处理提示词请求。  

> **注意**：文档 1 中说明“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但文档 2 的列举接口返回示例中明确包含 `purpose: "file-extract"` 的 `.mp4` 文件（`sdsdsd.mp4`），且未限制非 zip 视频格式。这表明 `purpose` 仅约束下游服务调用权限，**不限制上传文件类型本身**；实际支持的 MIME 类型由对应下游服务（如 file-extract 或 fine-tune）各自校验，API 层不做预过滤。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件流 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 指定用途，取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但仍可上传成功（[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，仅作元数据存储，不影响功能 |
| `file_id` | 字符串 | path（URL 路径） | 是（查询/删除时） | 通过上传或列举接口获取，是文件唯一标识（[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)） |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数，`page_size` 最大为 100（[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)） |

## 使用方式

### 上传文件（POST `/api/v1/files`）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file1.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tune data"' \
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

- **配额限制**：  
  - 单文件大小上限依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；  
  - 总有效文件数 ≤ 10,000 个；  
  - 总有效文件存储空间 ≤ 100 GB。  

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；其他 Region 用户需通过对应 Region 的百炼控制台管理文件（[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。  

- **兼容性声明**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该建议具有一致性，开发者应以此为设计基准。  

- **错误处理**：非 200 响应表示失败，返回体含 `code`（错误码）、`message`（错误详情）和 `request_id`（用于问题排查）；上传失败时，响应中 `data.failed_uploads` 明确列出各失败文件的 `code` 与 `message`（如 `BadRequest.TooLarge`、`BadRequest.TooMany`）。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


