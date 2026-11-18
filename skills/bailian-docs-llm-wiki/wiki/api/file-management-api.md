# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途（如 fine-tune、file-extract、batch）的文件生命周期管理。该接口为 DashScope 原生协议，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传，按 `purpose` 分类存储，后续可用于模型微调（`fine-tune`）、内容提取（`file-extract`）或批量推理（`batch`）任务。
- **查询与管理**：支持按 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件。
- **文件复用**：上传后的文件可在多个任务中重复引用（如多个 fine-tune 任务共用同一训练集），无需重复上传。

> **注意**：文档 1 中称“视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）”，但文档 2 的列举返回示例中明确包含 `purpose: "fine-tune"` 的 `.mp4` 文件（`sdsdsd.mp4`），且未要求 zip 封装。实际行为以 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中的字段定义为准，`purpose` 字段在响应中稳定存在并可被消费，说明非 zip 文件亦支持 fine-tune 场景。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则默认无用途，但**强烈建议显式指定**以便后续按用途筛选和管理（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，最大长度未明确定义，建议控制在 512 字符内 |
| `file_id` | 字符串 | path（URL 路径） | 是（查询/删除时） | 由上传成功响应中的 `data.uploaded_files[0].file_id` 返回，是全局唯一标识符（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)） |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数，`page_size` 最大为 100，最小为 1 |

## 使用方式

- **上传文件**  
  ```bash
  curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
    -F 'files=@/path/to/data.jsonl' \
    -F 'purpose=fine-tune' \
    -F 'descriptions=training set for qwen'
  ```

- **查询单个文件**  
  ```bash
  curl -X GET "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

- **列举所有文件（分页）**  
  ```bash
  curl -X GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

- **删除文件**  
  ```bash
  curl -X DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
    -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
  ```

## 限制和注意事项

- **配额限制**：
  - 单文件大小上限依 `purpose` 不同而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)）；
  - 总有效文件数 ≤ 10,000 个；
  - 总有效文件存储空间 ≤ 100 GB。

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过该 Region 对应的百炼控制台操作，或迁移到 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（其跨 Region 支持更完善）。

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。该兼容接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 Files API 一致，且已验证支持多 Region 和更完善的错误码体系。

- **失败处理**：上传接口返回中 `data.failed_uploads` 字段会明确列出失败文件及原因（如 `BadRequest.TooLarge`、`BadRequest.TooMany`），建议解析该字段而非仅依赖 HTTP 状态码判断整体成败。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


