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

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | 是 | multipart 表单字段，原始文件二进制流；若使用 base64 方式，则传 `file_base64` 字段 |
| `purpose` | string | 否 | 取值为 `"vision"`（图像）、`"audio"`（音频）、`"assistants"`（通用），影响后端解析策略；默认为 `"assistants"` |
| `file_id` | string | 是（路径参数） | 由上传响应返回的唯一标识，格式为 `file-xxxxxxxx` |
| `limit` / `offset` | integer | 否 | 列表接口分页参数，默认 `limit=20`, `offset=0` |

> **注意**：`purpose=vision` 是调用 Qwen-VL 等视觉模型的**强制要求**，否则模型将拒绝处理图像文件。此约束在 [文件管理](../../raw/model-api-reference/file-management-api.md) 中明确说明，但部分旧版 SDK 示例误设为默认 `"assistants"`，请以该文档为准。

## 使用方式

1. **上传文件**（推荐 multipart）：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/files" \
     -H "Authorization: Bearer $API_KEY" \
     -F "file=@/path/to/image.jpg" \
     -F "purpose=vision"
   ```
   成功响应含 `"id": "file-abc123"` 和 `"status": "uploaded"`。

2. **等待就绪**（异步场景）：  
   若响应中 `"status"` 为 `"processing"`，需轮询 `GET /v1/files/{file_id}` 直至变为 `"processed"`（通常 <5s）。  
   详见 [文件管理](../../raw/model-api-reference/file-management-api.md) 中“状态流转”章节。

3. **在模型请求中引用**：  
   将 `file_id` 填入消息内容，例如：  
   ```json
   { "role": "user", "content": [{"file_id": "file-abc123"}] }
   ```

## 限制和注意事项

- 单文件大小上限：图像 ≤ 20 MB，音频 ≤ 100 MB，文本 ≤ 50 MB  
- 每日上传配额：免费版 100 次/天，企业版按合同约定（参见控制台配额页）  
- 已删除文件不可恢复；被模型请求引用中的文件无法删除（API 返回 409）  
- 文件元数据（如 `filename`、`mime_type`）由服务端自动识别，客户端不可覆盖  
- 超过 30 天未被任何模型请求引用的文件将被系统自动清理  

> **注意**：文档中提及“支持 PDF 文本提取”，但当前版本（v2024.07+）实际仅支持 PDF 的**页面图像化后作为 vision 输入**，不提供 OCR 文本结构化解析。该功能差异已在 [文件管理](../../raw/model-api-reference/file-management-api.md) 的“已知限制”小节更新说明。

## 来源文档

- [文件管理](../../raw/model-api-reference/file-management-api.md)


