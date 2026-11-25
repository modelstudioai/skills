# 删除 Memory

删除当前记忆文件，并产生 deleted 版本；历史版本仍可通过版本接口查询。

<a id="前提"></a>

<a id="h-delete-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-delete-endpoint"></a>

## 接口

**DELETE** `/memory_stores/{memory_store_id}/memories/{memory_id}`

<a id="路径参数"></a>

<a id="h-delete-path"></a>

## 路径参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `memory_store_id` | 是 | string | 记忆库 ID |
| `memory_id` | 是 | string | 记忆 ID |

<a id="请求示例"></a>

<a id="h-delete-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X DELETE "$AGENTSTUDIO_URL/memory_stores/memstore_xxx/memories/mem_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="响应"></a>

<a id="h-delete-resp"></a>

## 响应

<a id="code-block"></a>

```json
{
  "id": "mem_xxx",
  "type": "memory_deleted"
}
```

<a id="响应字段"></a>

<a id="h-delete-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | — |
| `type` | string | — |

<a id="错误码"></a>

<a id="h-delete-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 401 | `InvalidApiKey` | API Key 缺失、错误或失效 |
| 403 | `permission_error` | 身份或资源访问权限不足 |
| 404 | `not_found_error` | 资源不存在或不属于当前工作空间 |
