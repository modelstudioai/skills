# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该 API 为历史兼容接口，**推荐开发者优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，以获得更统一、持续演进的体验。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，对应下游能力：
- `fine-tune`：用于模型微调（含文本、视频、图像生成类模型），训练数据支持 `.jsonl` 或 `.zip`（单个 zip ≤ 1 GB）；视频/图像微调要求 zip 格式，也可通过 OSS 挂载方式加载未压缩数据集。
- `file-extract`：用于文件内容解析与结构化提取（如 PDF/Word 表格识别、OCR 等）。
- `batch`：用于创建 Batch 异步推理任务，详见 [Batch 接口文档](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：文档 1 中称“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但文档 2 的文件对象定义及列举接口返回示例中明确包含 `purpose: "file-extract"` 和 `purpose: "fine-tune"` 字段，且未限定格式；实际支持情况以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 接口的 `purpose` 参数说明为准，建议以文档 1 的格式要求为当前有效约束。

## 关键参数

| 参数 | 类型 | 传参方式 | 必选 | 说明 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件可上传但无法被下游任务自动识别，[强烈建议显式指定](../../raw/model-api-reference/file-management-api/upload-file-api.md) |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，仅作备注，不影响功能 |
| `file_id` | 字符串 | URL path | 是（GET/DELETE） | 通过上传或列举接口获取，用于查询或删除单个文件 |
| `page_no`, `page_size` | 数字 | Query | 是（GET `/files`） | 分页参数，`page_no ≥ 1`，`1 ≤ page_size ≤ 100` |

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

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（zip 包 ≤ 1 GB）；
  - 总存储空间：≤ 100 GB（有效文件，即未删除状态）；
  - 总文件数量：≤ 10,000 个（有效文件）。
- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；其他 Region 用户需通过控制台操作，或改用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)，后者支持多 Region。
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”，该接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 规范对齐，是长期维护的主推方案。
- **错误处理**：非 200 响应时，返回 `code`（如 `BadRequest.TooLarge`）、`message` 和 `request_id`，可用于问题定位。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


