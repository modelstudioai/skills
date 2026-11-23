# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 决定后续可接入的服务类型：

- `fine-tune`：用于模型微调（包括文本、视频、图像生成类模型），训练数据支持 `.jsonl` 或 `.zip`（单个 zip ≤ 1 GB）；视频/图像微调要求数据集以 zip 形式上传，或通过 OSS 挂载方式加载未压缩目录（[原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md)）。
- `file-extract`：用于内容解析与结构化提取（如 PDF/Word 文本抽取）。
- `batch`：用于创建 Batch 异步任务（[原文标题](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。

> **注意**：文档 1 中说明 `fine-tune` purpose 下“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但文档 2 的“文件对象”小节及列举接口返回示例中均包含 `purpose` 字段且明确其值为字符串（如 `"fine-tune"`），二者一致；而文档 1 同时提到“也可通过 OSS 挂载方式加载……不支持 zip 文件”，此句与前文矛盾。**实际行为以接口返回字段 `purpose` 的取值为准，OSS 挂载属独立机制，不通过本 API 上传，故该矛盾处应以 [原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中关于 zip 上传的要求为准，OSS 挂载不在本 API 范围内。**

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应服务识别（[原文标题](../../raw/model-api-reference/file-management-api/upload-file-api.md)） |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，非文件名，不影响功能 |
| `file_id` | 字符串 | path | 是（GET/DELETE） | 通过上传或列举接口获取，用于查询或删除单个文件 |
| `page_no`, `page_size` | 数字 | query | 是（列举接口） | 分页参数，`page_size` 最大为 100 |

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
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件（DELETE `/api/v1/files/{file_id}`）
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

## 限制和注意事项

- **地域限制**：当前文件管理 API **仅在北京 Region 开放**；如您使用其他 Region，请通过该 Region 的百炼控制台完成文件管理（[原文标题](../../raw/model-api-reference/file-management-api/get-file-api.md)）。
- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB；
  - 总存储空间：100 GB（有效文件，即未删除状态）；
  - 总文件数量：10,000 个（有效文件）。
- **错误处理**：HTTP 非 200 响应表示失败，返回体含 `code` 和 `message` 字段（如 `BadRequest.TooLarge`）；上传接口返回中 `data.failed_uploads` 明确列出失败项及原因。
- **兼容性提示**：两个原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 OpenAI 兼容的 File 接口”，开发者新建集成应优先选用 `/compatible-mode/v1/files` 路径。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


