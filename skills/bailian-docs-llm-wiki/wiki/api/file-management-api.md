# file management api

文件管理 API 用于在百炼平台中上传、查询、删除和管理用户上传的文件资源，是调用多模态模型（如 Qwen-VL、Qwen2-Audio）前必需的预处理步骤。所有文件需先通过该 API 上传并获取 `file_id`，后续请求方可通过 `file_id` 引用。API 设计为 RESTful 风格，支持 `multipart/form-data` 和 `application/json` 两种上传方式。

## 支持的模型/功能

当前仅支持与多模态模型协同使用，包括 `qwen-vl-plus`、`qwen2-audio`、`qwen2-vl-7b-instruct` 等（详见 [文件管理](../../raw/model-api-reference/file-management-api.md)）。纯文本模型（如 `qwen-max`、`qwen-plus`）**不接受** `file_id` 输入，尝试传入将返回 `400 Bad Request`。文件本身不参与模型训练或微调，仅作为单次推理的上下文输入。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | binary | 是（表单上传） | 原始文件二进制流，支持 PNG/JPEG/MP3/WAV/PDF/TXT/DOCX 等格式（[文件管理](../../raw/model-api-reference/file-management-api.md) 列出完整清单） |
| `filename` | string | 否（推荐） | 显式指定文件名，影响 MIME 类型推断；若未提供且 `Content-Type` 不明确，可能导致解析失败 |
| `purpose` | string | 否 | 固定值 `"batch"` 或 `"vision"`；`"vision"` 用于图像理解类任务（默认），`"batch"` 用于异步批量处理（见 [文件管理](../../raw/model-api-reference/file-management-api.md)） |

> **注意**：文档中曾提及 `purpose=embedding`，但该值已废弃，服务端将拒绝该取值——请勿使用。

## 使用方式

1. **上传文件**：`POST https://dashscope.aliyuncs.com/api/v1/files`，使用 `multipart/form-data` 提交 `file` 字段；  
2. **获取响应**：成功时返回 `{"id": "file-xxx", "filename": "...", "status": "uploaded"}`；  
3. **在模型请求中引用**：在 `messages` 中以 `{"file_id": "file-xxx"}` 形式传入（非 URL）；  
4. **查询状态**：`GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}` 可检查上传是否完成（部分大文件需数秒处理）。

## 限制和注意事项

- 单文件最大 100 MB（PDF/DOCX 类文档建议 ≤50 MB 以保障 OCR 解析质量）；  
- 每个 `file_id` 有效期为 **30 天**，过期后自动清理，不可恢复；  
- 同一账号下最多保留 10,000 个有效 `file_id`，超出后上传将失败（需主动调用删除接口清理）；  
- 删除操作（`DELETE /api/v1/files/{file_id}`）仅释放引用，**不保证立即物理删除**，实际清理延迟可能达 24 小时。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


