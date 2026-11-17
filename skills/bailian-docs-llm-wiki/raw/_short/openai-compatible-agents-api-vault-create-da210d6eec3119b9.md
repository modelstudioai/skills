# 创建 Vault

创建一个 Vault，作为 Credential 的容器。创建空对象可生成匿名 Vault。

## 接口

**POST** `/vaults`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 请求体

**name** `string` **（可选）**

显示名称。去除首尾空白后 1–256 字节。省略时响应返回 `null`，显式传入 `null` 返回 `400`

**metadata** `object / null` **（可选）**

元数据，字符串键值对，最多 16 项；key 1–64 字符，value 最多 512 字符。省略或传 `null` 时响应为 `{}`

创建空对象 `{}` 会生成匿名 Vault，响应中的 `name` 为 `null`，不会自动生成名称。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/vaults" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "production-secrets",
    "metadata": {"team": "support"}
  }'
```

Python

```
import os
import requests

resp = requests.post(
    f"{os.environ['BASE_URL']}/vaults",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    json={"name": "production-secrets", "metadata": {"team": "support"}},
)
print(resp.status_code, resp.json())
```

### 响应字段

`201`，返回 Vault：

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

`400`

`invalid_request_error` / `unknown_parameter`

移除未知字段

`400`

`invalid_request_error` / `invalid_type`

按字段说明修正类型

`400`

`invalid_request_error` / `invalid_request_error`

按字段说明修正 `name` 或 `metadata`

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`409`

`conflict_error` / `conflict_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
