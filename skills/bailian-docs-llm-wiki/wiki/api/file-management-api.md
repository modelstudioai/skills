# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理，适用于 `fine-tune`、`file-extract` 和 `batch` 三类核心场景。  
- **文件查询与管理**：支持按 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件。  
- **文件复用**：上传后的 `file_id` 可在微调任务、内容提取任务或 Batch 任务中直接引用。  
- **OpenAI 兼容路径**：除原生 `/api/v1/files` 外，亦可通过 `/compatible-mode/v1/files` 调用 OpenAI 风格接口，详见 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。

> **注意**：文档 1 中提到“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，但文档 2 的 `purpose` 字段说明及列举返回示例中均未体现对 `.zip` 的特殊要求；且文档 1 同时指出 fine-tune 文件“也可通过 OSS 挂载方式加载”，而文档 2 未提及该能力。建议以控制台或最新 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)为准，原生接口行为可能存在收敛差异。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 描述 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 待上传文件，支持多字段同名上传（即一次请求传多个文件） |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但**强烈建议显式指定**以便后续管理；[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 文档明确说明 purpose 影响配额与可用性 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非文件名，用于语义标识 |
| `file_id` | 字符串 | URL path | 是（查询/删除） | 由上传接口返回，全局唯一，用于定位文件；[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文档强调其为必要路径参数 |
| `page_no`, `page_size` | 数字 | Query | 是（列举） | 分页参数，`page_size` 最大为 100；[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文档明确约束范围 |

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

### 列举文件（GET `/api/v1/files`）
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

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过对应 Region 的百炼控制台完成操作（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文末说明）。
- **配额限制**：
  - 单文件大小上限依 `purpose` 不同而异：`file-extract` ≤ 150MB，`batch` ≤ 500MB，`fine-tune` ≤ 300MB；
  - 有效文件总空间配额为 100GB，总数量配额为 10000 个；
  - 配额统计基于“未删除”状态文件。
- **错误处理**：非 200 响应体结构统一包含 `request_id`、`code` 和 `message` 字段，可用于问题定位与重试。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该路径提供更一致的语义、更广的 Region 支持及长期维护保障。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


