# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、Batch 任务）。该 API 为历史兼容接口，**推荐开发者优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**，以获得更统一的体验和持续的功能演进。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体模型，而是按 `purpose` 字段区分使用场景，不同 purpose 决定文件后续可接入的服务类型：
- `fine-tune`：用于模型微调（含文本、视频、图像生成类模型），训练数据支持 `.jsonl` 或 `.zip`（单个 zip ≤ 1 GB）；视频/图像微调要求 zip 格式，也可通过 OSS 挂载方式加载未压缩数据集。
- `file-extract`：用于文档内容解析与结构化提取（如 PDF、Word、Excel 等格式）。
- `batch`：用于创建 Batch 异步推理任务，详见 [Batch 接口（OpenAI 兼容）](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

> **注意**：文档 1 中提到“视频/图像生成模型微调的训练数据需以 .zip 格式上传”，但文档 2 的文件对象定义及列举接口返回示例中明确包含 `purpose: "file-extract"` 和 `purpose: "fine-tune"` 字段，且未限制 fine-tune 仅限 zip。实际支持范围以 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 文档为准，但建议对非 zip 格式 fine-tune 数据（如纯文本 jsonl）进行充分测试。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 支持一次上传多个文件，每个 `files` 字段对应一个文件 |
| `purpose` | 字符串 | `multipart/form-data` | 否 | 取值为 `fine-tune` / `file-extract` / `batch`；不传则文件仍可上传，但无法被对应服务自动识别和调用 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述信息，最大长度未明确定义，建议 ≤ 500 字符 |

在查询与管理接口中，关键路径/查询参数包括：
- `file_id`（path）：用于获取或删除指定文件，必须通过上传成功响应中的 `data.uploaded_files.$.file_id` 获取；
- `page_no` & `page_size`（query）：用于列举文件，`page_size` 最大为 100，最小为 1。

## 使用方式

### 上传文件
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/file1.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tune sample"' \
  --form 'files=@"/path/to/file2.pdf"' \
  --form 'purpose="file-extract"'
```

### 查询单个文件
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举所有文件（分页）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 删除文件
```bash
curl --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/{file_id}" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

所有接口均返回标准 `request_id`，可用于问题排查；失败时 HTTP 状态码非 200，响应体含 `code` 和 `message` 字段，例如 `{"code": "InvalidParameter", "message": "File not found."}` —— 详情见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中的“请求异常”章节。

## 限制和注意事项

- **配额限制**：
  - 单文件大小上限依 `purpose` 而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB；
  - 总有效文件数 ≤ 10,000 个；
  - 总有效文件存储空间 ≤ 100 GB。

- **地域限制**：当前原生文件管理 API **仅在北京 Region 开放**；若使用其他 Region，请通过该 Region 对应的百炼控制台完成文件管理，或迁移至 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)，后者支持多 Region。

- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。该兼容接口路径为 `/compatible-mode/v1/files`，语义与 OpenAI v1 Files API 一致，是未来主推路径。

- **文件生命周期**：已删除文件不可恢复；`url` 字段返回的下载链接为临时签名 URL，有效期有限，不可长期缓存。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


