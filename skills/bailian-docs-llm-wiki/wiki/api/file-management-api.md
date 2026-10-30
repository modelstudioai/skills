# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，适用于 fine-tune、file-extract 和 batch 等场景。该 API 返回结构化文件元数据（如 `file_id`、`url`、`md5`、`purpose`），支持多文件上传与分页列举。**注意：当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)**。

## 支持的模型/功能

- **上传文件**：支持单次多文件上传（`multipart/form-data`），按 `purpose` 分类管理，包括：
  - `fine-tune`：用于模型微调（训练数据需为 `.jsonl` 或 `.zip` 格式；视频/图像微调要求 zip 包 ≤ 1 GB）；
  - `file-extract`：用于内容解析与分析；
  - `batch`：用于创建 Batch 任务（参见 [batch-interfaces-compatible-with-openai.md](../../raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)）。
- **查询与管理**：支持通过 `file_id` 获取单个文件详情、分页列举全部文件、以及删除指定文件。

> **注意**：文档 1 中声明“当前文件管理 API 仅在北京 Region 开放”，但文档 2 未提及 Region 限制；实际调用时若在非北京 Region 失败，请改用对应 Region 的百炼控制台操作，或确认是否已启用跨 Region 文件访问能力。

## 关键参数

| 参数 | 类型 | 位置 | 必选 | 说明 |
|------|------|------|------|------|
| `file_id` | String | path | 是（GET/DELETE） | 通过上传接口返回或列举接口获取，全局唯一标识符 |
| `page_no` | Number | query | 是（GET /files） | 当前页码，最小值为 1，默认为 1 |
| `page_size` | Number | query | 是（GET /files） | 每页数量，范围 1–100，默认为 10 |
| `files` | 文件流 | multipart/form-data | 是（POST /files） | 待上传的二进制文件流，支持多次 `--form 'files=@...'` |
| `purpose` | String | multipart/form-data | 否（但强烈建议指定） | 取值为 `fine-tune` / `file-extract` / `batch`，影响后续功能可用性及配额计算 |
| `descriptions` | String | multipart/form-data | 否 | 文件描述文本，最大长度未明确定义，建议 ≤ 500 字符 |

## 使用方式

- **上传文件**（POST `/api/v1/files`）  
  使用 `curl --form` 或 SDK 构造 multipart 请求，示例见 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)。

- **查询单个文件**（GET `/api/v1/files/{file_id}`）  
  需提供有效 `file_id`，响应中 `data.url` 为临时可下载链接（含签名与过期时间）。

- **列举文件**（GET `/api/v1/files?page_no=1&page_size=20`）  
  返回 `data.files[]` 数组，每个元素包含完整文件对象字段（详见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)）。

- **删除文件**（DELETE `/api/v1/files/{file_id}`）  
  成功响应仅含 `request_id`，无 `data` 字段；失败时返回 `code` 与 `message`。

## 限制和注意事项

- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（视频/图像微调 zip 包上限为 1 GB）；
  - 总空间配额：100 GB（有效文件，即未删除状态）；
  - 总文件数配额：10,000 个（有效文件）。

- **地域限制**：  
  > **注意**：[查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 明确指出“当前文件管理 API 仅在北京 Region 开放”，而 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 未说明。若在其他 Region 调用失败，请优先检查 Region 配置或切换至 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)（`/compatible-mode/v1/files`）。

- **兼容性提示**：  
  两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../../raw/model-api-reference/toolkits-and-frameworks/openai-file-interface.md)”。新项目应优先采用该兼容路径以获得长期维护保障。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


