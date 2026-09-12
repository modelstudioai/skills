# file management api

百炼平台的文件管理 API 提供上传、查询、列举和删除文件的能力，适用于 fine-tune、file-extract、batch 等多种用途场景。该 API 采用 RESTful 设计，支持 multipart/form-data 和标准 JSON 请求；但需注意，**当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)**（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 和 [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 中的明确提示）。所有操作均需通过 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 认证。

## 支持的模型/功能

文件管理 API 本身不绑定具体大模型，而是为下游任务提供统一的文件托管能力，主要支持以下用途（由 `purpose` 参数指定）：

- `fine-tune`：用于模型微调训练数据（支持 `.jsonl`、`.zip` 等格式；视频/图像微调需以 zip 包上传，单包 ≤ 1 GB）；
- `file-extract`：用于文档内容解析与结构化提取；
- `batch`：用于创建批量推理任务（参见 [OpenAI 兼容的 Batch 接口](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai)）。

> **注意**：[上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md) 文档中说明 `fine-tune` 用途支持 OSS 挂载方式加载未压缩数据集，但 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 的“文件对象”小节未提及该能力，且其返回字段中无 `oss_path` 或挂载标识。该差异表明 OSS 挂载属于高级用法，不在基础文件管理 API 的标准响应中体现，开发者应以控制台或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)为准。

## 关键参数

| 字段 | 类型 | 传参方式 | 必选 | 描述 |
|------|------|----------|------|------|
| `file_id` | String | path | 是（GET/DELETE） | 文件唯一标识，由上传接口返回，用于查询或删除单个文件 |
| `page_no` / `page_size` | Number | query | 是（GET `/files`） | 分页参数；`page_size` 最大为 100（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)） |
| `files` | 文件流 | multipart/form-data | 是（POST `/files`） | 支持多文件同时上传 |
| `purpose` | String | multipart/form-data | 否（但强烈建议指定） | 明确文件用途，影响后续可用性及配额统计（如 `fine-tune`、`file-extract`、`batch`） |
| `descriptions` | String | multipart/form-data | 否 | 文件描述信息，非必填，但有助于人工识别 |

## 使用方式

- **上传文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，使用 `multipart/form-data`，携带 `files`、`purpose` 和可选 `descriptions`；
- **查询单个文件**：`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}`，返回含 `url`、`name`、`size`、`md5` 等元信息的完整文件对象；
- **列举文件列表**：`GET https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20`，响应中 `data.files` 为文件对象数组，每个对象包含 `purpose` 字段（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 返回示例）；
- **删除文件**：`DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}`，成功仅返回 `request_id`，无响应体。

## 限制和注意事项

- **地域限制**：当前文件管理 API 仅在北京 Region 开放；其他 Region 用户须通过对应 Region 的百炼控制台管理文件（见 [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md) 底部说明）；
- **配额限制**：
  - 单文件大小：`file-extract` ≤ 150 MB，`batch` ≤ 500 MB，`fine-tune` ≤ 300 MB（zip 包 ≤ 1 GB）；
  - 总存储空间：100 GB；
  - 总文件数量：10,000 个（均指有效/未删除文件）；
- **兼容性提示**：两篇原始文档均强调“当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)”，该建议具有一致性，应作为开发首选；
- **安全性**：`url` 字段为临时预签名下载链接，有效期有限，不可长期缓存或公开分发。

## 来源文档

- [查询和管理文件](../../raw/model-api-reference/file-management-api/get-file-api.md)
- [上传文件](../../raw/model-api-reference/file-management-api/upload-file-api.md)


