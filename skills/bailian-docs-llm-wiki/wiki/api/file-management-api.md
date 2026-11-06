# file management api

[文件管理](../concepts/file-management.md) API 用于在百炼平台中上传、查询、删除和管理用户上传的文件资源，是调用多模态模型（如 Qwen-VL、Qwen2-Audio）前必需的预处理步骤。所有文件需先通过该 API 上传并获取 `file_id`，后续请求方可通过 `file_id` 引用。API 设计为 RESTful 风格，支持 `multipart/form-data` 和 `application/json` 两种上传方式。

## 支持的模型/功能

当前仅支持与多模态模型协同使用，包括 `qwen-vl-plus`、`qwen2-audio`、`qwen2-vl-7b-instruct` 等（详见 [文件管理](../../raw/model-api-reference/file-management-api.md)）。纯文本模型（如 `qwen-max`、`qwen-plus`）**不接受** `file_id` 输入，尝试传入将返回 `400 Bad Request`。文件本身不参与模型训练或微调，仅作为单次推理的上下文输入。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | binary | 是（表单上传） | 原始文件二进制流，支持 PNG/JPEG/MP3/WAV/PDF/TXT/DOCX 等格式（[文件管理](../../raw/model-api-reference/file-management-api.md) 列出完整清单） |
| `filename` | string | 否（推荐） | 显式指定文件名，影响 MIME 类型推断；若未提供且服务端无法识别扩展名，将拒绝上传 |
| `purpose` | string | 否 | 固定值 `"batch"` 或 `"vision"`；`"vision"` 用于图像理解类模型（如 Qwen-VL），`"batch"` 用于异步批量处理任务；默认为 `"vision"` |

> **注意**：原始文档 [文件管理](../../raw/model-api-reference/file-management-api.md) 中曾提及支持 `"audio"` purpose，但该值已于 v2.3.0 版本废弃，实际请求将被静默转为 `"vision"`，请勿依赖。

## 使用方式

1. **上传文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，使用 `multipart/form-data` 提交 `file` 字段（推荐）；或 `POST` + `application/json` 提交 base64 编码的 `file_content`（仅限 ≤1MB 文本类文件）  
2. **获取文件列表**：`GET https://dashscope.aliyuncs.com/api/v1/files`（支持分页参数 `limit`/`offset`）  
3. **查询单个文件**：`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}`  
4. **删除文件**：`DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}`（成功后 `file_id` 不可复用）

## 限制和注意事项

- 单文件大小上限：**100 MB**（PDF/DOCX 等文档类）或 **50 MB**（音视频类）；超出将返回 `413 Payload Too Large`  
- 文件保留期：上传后默认保留 **30 天**，无调用记录的文件可能被提前清理（[文件管理](../../raw/model-api-reference/file-management-api.md) 明确说明此策略）  
- 并发限制：同一 `file_id` 在 10 秒内不可重复用于不同请求，否则可能触发幂等性校验失败  
- 安全要求：所有请求必须携带有效的 `Authorization: Bearer <api_key>`，且 `api_key` 需具备 `files:write` 权限

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


