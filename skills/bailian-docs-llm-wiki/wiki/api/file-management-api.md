# file management api

百炼平台的文件管理 API 提供文件上传、查询、列举和删除等基础能力，支持多用途文件复用（如微调、内容提取、批量任务）。该接口为 DashScope 原生实现，**当前主要用于兼容历史场景**；新项目应优先采用 [OpenAI 兼容的 File 接口](raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

- **文件上传**：支持单次多文件上传，按 `purpose` 分类管理（`fine-tune`、`file-extract`、`batch`），上传后生成全局唯一 `file_id` 供下游任务引用。
- **文件查询与管理**：支持按 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件。
- **跨任务复用**：同一 `file_id` 可在 fine-tune、file-extract、batch 等不同场景中重复使用（需符合对应 purpose 的格式与大小限制）。

> **注意**：文档 2 明确指出“当前文件管理 API 仅在北京 Region 开放”，但文档 1 未提及地域限制。实际调用时若在非北京 Region 遇到 404 或权限错误，请切换至北京 Region 或改用控制台操作。

## 关键参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
|------|------|----------|------|------|
| `files` | 文件流 | `multipart/form-data` | 是 | 待上传的文件二进制流；支持多次 `--form 'files=@...'` 实现多文件上传 |
| `purpose` | 字符串 | `multipart/form-data` | 否（但强烈建议指定） | 取值为 `fine-tune` / `file-extract` / `batch`；影响后续可用性及配额计算；[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中明确说明不传仍可成功，但不利于管理 |
| `descriptions` | 字符串 | `multipart/form-data` | 否 | 文件描述文本，最大长度未明确定义，建议 ≤512 字符 |
| `file_id` | 字符串 | path（URL 路径） | 是（查询/删除时） | 由上传接口返回，用于精确定位文件；详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) |
| `page_no`, `page_size` | 数字 | query | 是（列举时） | 分页参数：`page_no ≥ 1`，`page_size ∈ [1, 100]` |

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

### 列举全部文件（GET `/api/v1/files`）
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
  - 单文件大小上限依 `purpose` 不同而异：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调训练数据允许 `.zip` 格式，单包 ≤ 1 GB）；
  - 总有效文件数 ≤ 10,000 个；
  - 总有效文件存储空间 ≤ 100 GB；
  - 所有配额均按「未删除」状态统计。

- **地域限制**：  
  > **注意**：[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 文档明确声明“当前文件管理 API 仅在北京 Region 开放”，其他 Region 调用将失败。请确认 endpoint 地域一致性或改用控制台。

- **兼容性提示**：  
  两篇原始文档均强调“**当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**”。新集成应直接对接 `/compatible-mode/v1/files` 路径，以获得长期维护保障与统一行为。

- **文件用途不可变**：`purpose` 在上传时指定后不可修改；若需变更用途，须重新上传并指定新 `purpose`。

## 来源文档

- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)
- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)


