# file management api

[文件管理](../concepts/file-management.md) API 用于在百炼平台中上传、查询、删除和管理用户上传的文件资源，是调用多模态模型（如 Qwen-VL、Qwen2-Audio）前必需的预处理步骤。所有文件需先通过该 API 上传并获取 `file_id`，后续请求方可通过 `file_id` 引用。API 设计为 RESTful 风格，支持同步上传与异步状态轮询。

## 支持的模型/功能

- **支持模型**：Qwen-VL、Qwen2-Audio、Qwen2-VL、Qwen3-VL（仅限图像/音频类输入场景）  
- **核心功能**：  
  - `POST /v1/files`：上传文件（支持 multipart/form-data 或 base64）  
  - `GET /v1/files/{file_id}`：查询单个文件元信息及处理状态  
  - `DELETE /v1/files/{file_id}`：删除已上传文件（仅限未被引用的文件）  
  - `GET /v1/files`：分页列出当前空间下所有文件（默认按创建时间倒序）  
该能力覆盖文本、图像、音频三类文件格式，但暂不支持视频直接上传（需先抽帧或转为图像序列）。详情见 [文件管理](../../raw/model-api-reference/file-management-api.md)。

## 关键参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
|------|------|------|------|------|
| `file` | form-data | binary | 是 | 原始文件二进制流；最大 100 MB（图像/音频）或 50 MB（文本） |
| `purpose` | form-data | string | 否 | 取值 `vision`（图像）、`audio`（音频）、`assistants`（通用），影响后端解析策略；默认 `assistants` |
| `file_id` | path | string | 是（GET/DELETE） | 由上传响应返回的唯一标识，格式为 `file-xxxxxxxx` |
| `limit` / `offset` | query | integer | 否 | 列表接口分页参数，默认 `limit=20`, `offset=0` |

> **注意**：`purpose=vision` 时，系统将强制启用 OCR 和图像结构化解析；而 [文件管理](../../raw/model-api-reference/file-management-api.md) 中旧版文档曾建议使用 `type=image`，该字段已废弃，请以 `purpose` 为准。

## 使用方式

1. **上传文件**（推荐 multipart）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@/path/to/image.jpg" \
     -F "purpose=vision"
   ```
   成功响应含 `"id": "file-abc123"` 和 `"status": "uploaded"`（若需 OCR 则可能为 `"processing"`）。

2. **轮询状态**（当 `status` 为 `processing` 时）：
   ```bash
   curl "https://dashscope.aliyuncs.com/api/v1/files/file-abc123" \
     -H "Authorization: Bearer $API_KEY"
   ```
   直至返回 `"status": "processed"` 方可安全用于模型调用。

3. **在模型请求中引用**：  
   在 `messages` 中以 `{"type": "image_url", "image_url": {"url": "file-abc123"}}` 形式传入（Qwen-VL 等），详见 [文件管理](../../raw/model-api-reference/file-management-api.md)。

## 限制和注意事项

- 单文件大小上限：图像/音频 ≤ 100 MB，文本 ≤ 50 MB；总空间配额按项目级限制（默认 10 GB）  
- `file_id` 有效期永久，但若文件超过 90 天未被任何模型请求引用，系统可能自动清理（非强制，仅回收冷数据）  
- 删除操作不可逆，且仅当 `file_id` 未出现在任何活跃会话或历史 trace 中时才允许删除  
- 上传时若 `purpose` 与目标模型不匹配（如用 `purpose=audio` 调用 Qwen-VL），将返回 400 错误  
- 注意：部分 SDK 示例中仍沿用旧版 `file_type` 参数，实际应以 [文件管理](../../raw/model-api-reference/file-management-api.md) 中最新定义的 `purpose` 字段为准。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


