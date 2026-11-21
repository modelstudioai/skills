# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理，后续可被 fine-tune、file-extract 或 batch 任务引用。
- **文件查询与列举**：支持按 `file_id` 获取单个文件详情，或分页列举全部文件（含 `purpose` 字段）。
- **文件删除**：支持按 `file_id` 删除已上传文件（不可恢复）。
- **文件复用**：同一 `file_id` 可在多个任务中重复使用，例如一个 `file-extract` 用途的 PDF 文件可被多次用于文档解析。

> **注意**：文档 2 明确指出“当前文件管理 API 仅在北京 Region 开放”，但文档 1 未提及地域限制。实际调用时若在非北京 Region 遇到 404 或权限错误，请切换至北京 Region 或改用控制台操作 —— 此不一致已在 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中明确标注。

## 关键参数

| 参数名 | 类型 | 传参方式 | 必选 | 说明 |
|--------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 待上传的文件二进制流；支持多次 `--form 'files=@...'` 实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否（但强烈建议指定） | 取值为 `fine-tune` / `file-extract` / `batch`；影响配额计算与下游任务可用性；[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中强调“不传仍可成功，但建议明确指定” |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述文本，最大长度未明确定义，建议 ≤500 字符 |
| `file_id` | 字符串 | URL path | 是（查询/删除） | 由上传响应返回，全局唯一；[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中定义其为“可通过上传或列举接口获取” |
| `page_no`, `page_size` | 数字 | Query | 是（列举时） | `page_no ≥ 1`，`page_size ∈ [1, 100]`；默认 `page_no=1`, `page_size=10` |

## 使用方式

### 上传文件（POST `/api/v1/files`）
```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/data.jsonl"' \
  --form 'purpose="fine-tune"' \
  --form 'descriptions="qwen fine-tuning dataset"'
```

### 查询单个文件（GET `/api/v1/files/{file_id}`）
```bash
curl --request GET "https://dashscope.aliyuncs.com/api/v1/files/9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 列举文件（GET `/api/v1/files`）
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
  - 单文件大小：`file-extract` ≤ 150MB，`batch` ≤ 500MB，`fine-tune` ≤ 300MB（视频/图像微调训练数据需 zip 格式，单包 ≤ 1GB）；
  - 总存储空间：≤ 100GB（有效文件，即未删除）；
  - 总文件数量：≤ 10,000 个（有效文件）。
- **地域限制**：API 仅在北京 Region 可用；其他 Region 用户需通过控制台操作或迁移至北京 Region —— 此关键约束在 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 中明确声明。
- **兼容性提示**：两篇原始文档均以加粗“**重要**”开头，强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。开发者新建集成应直接对接 `/compatible-mode/v1/files` 路径。
- **失败处理**：上传接口返回 `data.failed_uploads` 数组，含每个失败文件的 `code` 和 `message`（如 `BadRequest.TooLarge`），需逐项检查；非 200 响应体结构统一含 `code`/`message`/`request_id`。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


