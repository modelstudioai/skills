# 获取 Memory

读取单个记忆，包含正文。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/memory_stores/{memory_store_id}/memories/{memory_id}`

<a id="路径参数"></a>

<a id="h-get-path"></a>

## 路径参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `memory_store_id` | 是 | string | 记忆库 ID |
| `memory_id` | 是 | string | 记忆 ID |

<a id="请求示例"></a>

<a id="h-get-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/memory_stores/memstore_xxx/memories/mem_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="响应"></a>

<a id="h-get-resp"></a>

## 响应

<a id="code-block"></a>

```json
{
  "id": "mem_xxx",
  "type": "memory",
  "memory_store_id": "memstore_xxx",
  "path": "/notes/project.md",
  "content": "# 项目约定\n默认开发环境为预发环境。\n",
  "content_sha256": "e3b0c44b98fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "content_size_bytes": 47,
  "memory_version_id": "memver_xxx",
  "created_at": "2026-09-17T08:00:00Z",
  "updated_at": "2026-09-17T08:00:00Z"
}
```

<a id="响应字段"></a>

<a id="h-get-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 记忆 ID，格式 mem\_xxx |
| `type` | string | 固定为 memory |
| `memory_store_id` | string | 所属记忆库 ID |
| `path` | string | 记忆库内路径，以 / 开头 |
| `content` | string | 正文，UTF-8 文本；view=full 或单条读取时返回 |
| `content_sha256` | string | 正文的 SHA256 哈希，可用作条件更新的乐观锁 |
| `content_size_bytes` | integer | 正文的 UTF-8 字节数 |
| `memory_version_id` | string | 当前版本 ID，格式 memver\_xxx |
| `created_at` | string | 创建时间，ISO 8601 UTC |
| `updated_at` | string | 最近更新时间，ISO 8601 UTC |

<a id="错误码"></a>

<a id="h-get-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 401 | `InvalidApiKey` | API Key 缺失、错误或失效 |
| 403 | `permission_error` | 身份或资源访问权限不足 |
| 404 | `not_found_error` | 资源不存在或不属于当前工作空间 |
