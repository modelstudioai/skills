# 更新 Memory

修改记忆正文、重命名或同时原子修改。

<a id="前提"></a>

<a id="h-update-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-update-endpoint"></a>

## 接口

**POST** `/memory_stores/{memory_store_id}/memories/{memory_id}`

<a id="路径参数"></a>

<a id="h-update-path"></a>

## 路径参数

| 参数 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `memory_store_id` | 是 | string | 记忆库 ID |
| `memory_id` | 是 | string | 记忆 ID |

<a id="请求体"></a>

<a id="h-update-req"></a>

## 请求体

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `path` | 否 | string | 新路径（重命名），规则与创建一致；记忆 ID 保持不变 |
| `content` | 否 | string | 新正文，最大 102400 UTF-8 bytes |
| `precondition` | 否 | object | 可选的乐观锁：携带读取时的 content\_sha256，内容已被修改时返回冲突 |

<a id="请求示例"></a>

<a id="h-update-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/memory_stores/memstore_xxx/memories/mem_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"content": "# 项目约定\n默认开发环境为预发环境。\n变更需要补充回归测试。\n","precondition": {"type": "content_sha256","content_sha256": "e3b0c44b98fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"}}'
```

<a id="响应"></a>

<a id="h-update-resp"></a>

## 响应

<a id="code-block"></a>

```json
{
  "id": "mem_xxx",
  "type": "memory",
  "memory_store_id": "memstore_xxx",
  "path": "/notes/project.md",
  "content_sha256": "e3b0c44b98fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "content_size_bytes": 47,
  "memory_version_id": "memver_yyy",
  "created_at": "2026-09-17T08:00:00Z",
  "updated_at": "2026-09-17T08:30:00Z"
}
```

<a id="响应字段"></a>

<a id="h-update-dto"></a>

### 响应字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 记忆 ID，格式 mem\_xxx |
| `type` | string | 固定为 memory |
| `memory_store_id` | string | 所属记忆库 ID |
| `path` | string | 记忆库内路径，以 / 开头 |
| `content_sha256` | string | 正文的 SHA256 哈希，可用作条件更新的乐观锁 |
| `content_size_bytes` | integer | 正文的 UTF-8 字节数 |
| `memory_version_id` | string | 当前版本 ID，格式 memver\_xxx |
| `created_at` | string | 创建时间，ISO 8601 UTC |
| `updated_at` | string | 最近更新时间，ISO 8601 UTC |

<a id="错误码"></a>

<a id="h-update-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `invalid_request_error` | 参数、路径、limit 或分页游标非法 |
| 401 | `InvalidApiKey` | API Key 缺失、错误或失效 |
| 403 | `permission_error` | 身份或资源访问权限不足 |
| 404 | `not_found_error` | 资源不存在或不属于当前工作空间 |
| 409 | `memory_path_conflict_error` 等 | 路径冲突、条件更新冲突或对已归档记忆库写入 |
