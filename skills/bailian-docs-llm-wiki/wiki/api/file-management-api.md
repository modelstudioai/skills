# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途（如 fine-tune、file-extract、batch）的文件生命周期管理。该接口为 DashScope 原生协议，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类存储，后续可被 fine-tune、file-extract 或 batch 任务复用；
- **文件查询与列举**：支持按 `file_id` 获取单个文件详情，或分页列举全部文件（含 `purpose` 字段）；
- **文件删除**：支持按 `file_id` 删除已上传文件；
- **文件元数据**：返回 `url`（临时下载链接）、`md5`、`size`、`gmt_create`、`purpose` 等关键属性，详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中的“文件对象”定义。

> **注意**：文档 1 中称“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，但文档 2 及当前控制台实践表明，`purpose=fine-tune` 下 `.jsonl`、`.csv`、`.zip` 均被支持；.zip 限制实为 **500MB**（与 `batch` 用途一致），而非文档 1 所述的 1GB。请以实际接口响应和 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 的最新行为为准。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持多次传参实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值：`fine-tune`、`file-extract`、`batch`；不传则默认无用途，但**强烈建议显式指定**以便归类管理（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述，非文件名，用于辅助识别 |
| `file_id` | 字符串 | path（URL 路径） | 是 | 用于 `GET /files/{file_id}` 和 `DELETE /files/{file_id}` |
| `page_no`, `page_size` | 数字 | query | 是 | 仅用于 `GET /files` 列举接口；`page_size` 最大为 100 |

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
  curl "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=50" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

- **删除文件**（DELETE `/api/v1/files/{file_id}`）：
  ```bash
  curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150MB，`batch` ≤ 500MB，`fine-tune` ≤ 500MB（非 1GB）；
  - 总有效文件数 ≤ 10,000 个；
  - 总有效文件空间 ≤ 100GB。
- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过对应 Region 的百炼控制台操作，或切换至 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)（该接口支持多 Region）。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景”，且明确推荐迁移至 OpenAI 兼容路径（`/compatible-mode/v1/files`）。新项目应优先采用该兼容接口，以获得更稳定的版本演进与跨平台一致性。
- **失败处理**：上传接口返回中 `data.failed_uploads` 明确列出失败文件及错误码（如 `BadRequest.TooLarge`），需主动解析并重试或降级处理。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


