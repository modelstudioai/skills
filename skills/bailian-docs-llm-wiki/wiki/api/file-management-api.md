# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，适用于 fine-tune、file-extract、batch 等场景。该接口为 DashScope 原生协议，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **上传（POST `/api/v1/files`）**：支持多文件并发上传，按 `purpose` 分类（`fine-tune` / `file-extract` / `batch`），上传后生成唯一 `file_id` 供后续任务复用。  
- **查询（GET `/api/v1/files/{file_id}`）**：获取单个文件的元信息与临时下载 URL。  
- **列举（GET `/api/v1/files`）**：分页获取当前账户下所有有效文件列表，支持 `page_no` 和 `page_size` 控制返回范围。  
- **删除（DELETE `/api/v1/files/{file_id}`）**：异步删除指定文件（不可恢复），成功响应仅含 `request_id`。  

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及 Region 限制；实际调用时若遇 404 或权限错误，请确认所用 API Endpoint 是否匹配账号所属 Region，并优先参考 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md) 的跨 Region 支持能力。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是（查询/删除） | 由上传接口返回，全局唯一，非用户自定义 ID |
| `page_no` | Number | query | 是（列举） | 当前页码，最小值为 1，默认为 1 |
| `page_size` | Number | query | 是（列举） | 每页数量，取值范围 1–100，默认为 10 |
| `purpose` | String | multipart/form-data | 否（上传） | 明确用途可提升管理效率；取值见下表；不传则默认无用途标记 |
| `files` | 文件流 | multipart/form-data | 是（上传） | 支持多次 `--form 'files=@...'` 上传多个文件 |
| `descriptions` | String | multipart/form-data | 否（上传） | 对应每个 `files` 的描述文本，建议简明标识用途 |

`purpose` 取值说明：
- `fine-tune`：用于模型微调，.zip 包 ≤ 1 GB（视频/图像微调需 zip）；OSS 挂载方式支持未压缩目录。
- `file-extract`：用于内容解析（如 PDF 文本提取），单文件 ≤ 150 MB。
- `batch`：用于 Batch 任务，单文件 ≤ 500 MB。

## 使用方式

1. **上传文件**（示例）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
     -F 'files=@data.jsonl' \
     -F 'purpose=fine-tune' \
     -F 'descriptions="qwen fine-tuning dataset"'
   ```
   成功响应中 `data.uploaded_files[0].file_id` 即为后续调用凭证。

2. **查询文件详情**（示例）：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
     -H "Authorization: Bearer ${DASHSCOPE_API_KEY}"
   ```
   返回 `data.url` 为带签名的临时 OSS 下载链接（有效期约 1 小时），详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)。

3. **列举与删除**：按需组合 `page_no`/`page_size` 调用列举接口，再对目标 `file_id` 发起 DELETE 请求。

## 限制和注意事项

- **配额限制**：  
  - 单文件大小依 `purpose` 不同而异（`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB 或 zip ≤ 1 GB）；  
  - 总有效文件数上限 10,000 个；  
  - 总有效文件存储空间上限 100 GB。  
  超限时返回 `BadRequest.TooLarge` 或 `BadRequest.TooMany` 错误码，详见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

- **地域限制**：原生接口仅在北京 Region 可用；其他 Region 用户请使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)或控制台操作。

- **兼容性提示**：两篇原始文档均强调“**当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**”，新项目应直接集成 `/compatible-mode/v1/files` 路径，以获得更一致的语义、跨 Region 支持及长期维护保障。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


