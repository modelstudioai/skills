# 删除文件

永久删除指定的文件。删除后文件数据将无法恢复。

<a id="前提"></a>

<a id="h-ragapi-delete-file-prereq"></a>

## 前提

已获取阿里云百炼 API Key（[控制台 API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key)）并完成鉴权配置，详见 [Knowledge（原RAG） API 概览](../rag-api-overview.md)与[鉴权](../rag-api-authentication.md)。数据导入接口与其他 Knowledge API（原RAG API） 使用相同的 Base URL 与鉴权方式，路径前缀为 `/api/v1/connector/dash/`。

<a id="接口"></a>

<a id="h-ragapi-delete-file-endpoint"></a>

## 接口

**POST** `/api/v1/connector/dash/deleteFile`

永久删除指定的文件。删除后文件数据将无法恢复。

> **警告**
>
> 此操作不可逆，删除后文件数据将被永久移除，无法恢复。本接口仅删除数据管理（数据集）中的文件，不会删除已导入知识库的文档及其切片索引；如需从知识库移除该文档，请另行调用[删除文档](../rag-api-documents/rag-api-delete-document.md)。

<a id="请求体"></a>

<a id="h-ragapi-delete-file-req"></a>

## 请求体

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `fileId` | 是 | string | 文件 ID，通过 `listFile` 获取。 |

<a id="请求示例"></a>

<a id="h-ragapi-delete-file-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X POST "$BASE_URL/api/v1/connector/dash/deleteFile" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileId": "file_abc123"
  }'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-ragapi-delete-file-resp"></a>

## 响应示例

成功返回 200。

<a id="code-block-2"></a>

```json
{
  "code": "Success",
  "status_code": 200,
  "data": {},
  "requestId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

<a id="响应字段"></a>

<a id="h-ragapi-delete-file-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 响应码，成功时为 `Success`。 |
| `message` | string | 错误或提示信息，成功时为空字符串。 |
| `requestId` | string | 请求唯一标识，排查问题时请提供此 ID。 |
| `data` | object | 删除结果。子字段 `fileId`（string，已删除的文件 ID）、`status`（string，删除后状态，为 `DELETED`）。 |
| `status` | integer | 业务状态码。成功为 `200`，参数错误等失败场景为 `400`。注意失败时 HTTP 状态码仍为 200，需根据本字段与 `code` 判断结果。 |

<a id="错误码"></a>

<a id="h-ragapi-delete-file-err"></a>

## 错误码

| HTTP 状态码 | 错误码 `code` | 说明 |
| --- | --- | --- |
| 400 | `InvalidParameter` | 请求参数无效。`message` 示例：`Required parameter missing or invalid.` |
| 401 | `InvalidApiKey` | 鉴权失败，API Key 无效或缺失。`message` 示例：`Invalid API-key provided.` |

业务失败时 HTTP 状态码仍为 200，需根据响应体中的 `status` 与 `code` 判断结果。
