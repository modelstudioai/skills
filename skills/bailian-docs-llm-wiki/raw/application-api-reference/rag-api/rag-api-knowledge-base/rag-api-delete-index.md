# 删除知识库

永久删除指定的知识库及其所有文档和切片。删除后无法恢复，请在调用前确认目标知识库已无业务依赖。

<a id="前提"></a>

<a id="h-ragapi-delete-index-prereq"></a>

## 前提

已获取 API Key 和业务空间 ID，并完成鉴权配置，详见[API 总览](../rag-api-overview.md)与[鉴权说明](../rag-api-authentication.md)。

<a id="接口"></a>

<a id="h-ragapi-delete-index-endpoint"></a>

## 接口

**POST** `/api/v1/indices/rag/index/delete`

永久删除指定的知识库。删除后，该知识库下的所有文档、切片和索引数据将被一并移除，且无法恢复。请在调用前确认操作。

> **警告**
>
> 此操作不可逆。删除后，该知识库下的所有文档、切片和索引数据将被一并移除，且无法恢复。请在调用前确认目标知识库已无业务依赖。

<a id="请求体"></a>

<a id="h-ragapi-delete-index-req"></a>

## 请求体

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `index_id` | 是 | string | 要删除的知识库 ID，即[创建知识库并导入](rag-api-create-index.md)接口返回的 `data.pipelineId` |

<a id="请求示例"></a>

<a id="h-ragapi-delete-index-eg"></a>

## 请求示例

<a id="code-block"></a>

```bash
curl -X POST "$BASE_URL/api/v1/indices/rag/index/delete" \
  -H "Authorization: Bearer $BAILIAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"index_id": "your-kb-id"}'
```

其中 `BASE_URL` 为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`（`{workspace_id}` 为业务空间 ID），`BAILIAN_API_KEY` 为阿里云百炼 API Key。

<a id="响应示例"></a>

<a id="h-ragapi-delete-index-resp"></a>

## 响应示例

删除成功返回 200。

<a id="code-block-2"></a>

```json
{
  "code": "Success",
  "status_code": 200,
  "success": true,
  "message": "success",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "status": "SUCCESS"
}
```

<a id="响应字段"></a>

<a id="h-ragapi-delete-index-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | string | 响应码，成功时为 `Success` |
| `status_code` | integer | HTTP 状态码 |
| `success` | boolean | 操作是否成功 |
| `message` | string | 响应消息，成功时为 `success` |
| `request_id` | string | 请求唯一标识，排查问题时请提供此 ID |
| `status` | string | 请求状态，成功时为 `SUCCESS` |
