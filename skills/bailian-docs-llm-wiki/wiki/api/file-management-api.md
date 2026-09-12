# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生协议，**当前主要用于兼容历史场景；新项目强烈推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理，后续可被 fine-tune、file-extract、batch 等下游任务引用。  
- **文件查询与列举**：支持按 `file_id` 获取单个文件详情（含下载 URL、MD5、大小等元信息），或分页列举全部有效文件。  
- **文件删除**：支持按 `file_id` 删除已上传文件，释放配额。  
- **用途隔离**：不同 `purpose`（如 `fine-tune`、`file-extract`、`batch`）对应不同服务链路，且在控制台与 API 返回中均显式暴露（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中 `data.files[].purpose` 字段）。

> **注意**：文档 1 中称“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，但该限制未在文档 2 或其他公开规范中复现，且与 `fine-tune` 场景下常规 JSONL/CSV 数据格式惯例不符；建议以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 当前描述为准，实际使用时优先验证 zip 解压路径与数据格式兼容性。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 上传的二进制文件流，支持多次出现实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应用途任务识别（[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 明确建议指定） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述文本，用于人工识别 |
| `file_id` | 字符串 | path（URL 路径） | 是 | 用于 `GET /files/{file_id}` 和 `DELETE /files/{file_id}`，由上传成功响应返回 |
| `page_no`, `page_size` | 数字 | query | 是 | 用于 `GET /files` 列举，`page_size` 最大为 100（[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 明确限定） |

## 使用方式

- **上传文件**（POST `/api/v1/files`）：  
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    -F 'files=@/path/to/data.jsonl' \
    -F 'purpose=fine-tune' \
    -F 'descriptions="qwen fine-tuning dataset"'
  ```

- **查询单个文件**（GET `/api/v1/files/{file_id}`）：  
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

- **列举文件**（GET `/api/v1/files`）：  
  ```bash
  curl "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

- **删除文件**（DELETE `/api/v1/files/{file_id}`）：  
  ```bash
  curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

## 限制和注意事项

- **配额限制**：  
  - 单文件大小上限依 `purpose` 而定：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 明确列出）；  
  - 总有效文件数 ≤ 10,000 个；  
  - 总有效文件存储空间 ≤ 100 GB。  

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过该 Region 的百炼控制台操作，或切换至 [OpenAI 兼容接口](../concepts/openai-compatibility.md)（[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 明确声明）。  

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 OpenAI 兼容的 File 接口”——该一致性提示应作为开发者决策首要依据。  

- **错误处理**：非 200 响应体结构统一包含 `request_id`、`code`、`message` 字段（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 和 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 的“请求异常”章节）。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)



