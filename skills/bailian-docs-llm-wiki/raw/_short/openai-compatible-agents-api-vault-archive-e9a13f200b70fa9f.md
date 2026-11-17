# 归档 Vault

归档 Vault 并级联归档其下 Credential。该接口是百炼扩展。

## 接口

**POST** `/vaults/{vault_id}/archive`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，按不透明 ID 使用

本接口没有请求体。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/vaults/vlt_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
import os
import requests

resp = requests.post(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx/archive",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.json())
```

### 响应字段

`200`，返回归档后的 Vault：

**id** `string`

Vault ID

**object** `string`

Vault 对象类型，固定为 `vault`

**created\_at** `integer`

创建时间，Unix 秒

**name** `string / null`

显示名称

**metadata** `object`

元数据，字符串键值对；未设置时为 `{}`

响应仍是 Vault 结构，不返回 `archived_at` 或 `status`。归档 Vault 会级联归档其下 Credential。归档后资源仍可获取，默认列表同时包含 `active` 和 `archived`。没有恢复接口。

## 响应示例

```
{
  "id": "vlt_xxx",
  "object": "vault",
  "created_at": 1793941200,
  "name": "production-secrets",
  "metadata": {"team": "support"}
}
```

## 错误码

错误响应结构见[错误码](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

HTTP 状态码

错误类型 / 错误码

解决方案

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Vault ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
