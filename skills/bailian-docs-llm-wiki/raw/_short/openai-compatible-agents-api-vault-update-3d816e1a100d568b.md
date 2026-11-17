# 更新 Vault

更新 Vault 的名称或元数据。更新使用 POST，元数据整体替换。

## 接口

**POST** `/vaults/{vault_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，按不透明 ID 使用

## 请求体

**name** `string / null` **（可选）**

Vault 名称，省略时保持原值；`null` 清除名称；提供时去除首尾空白后 1–256 字节

**metadata** `object` **（可选）**

元数据，省略时保持原值；`null` 返回 `400`；`{}` 清空。最多 16 项；key 1–64 字符，value 最多 512 字符

`metadata` 整体替换，不合并；未出现在新对象中的旧 key 会被删除。更新空对象 `{}` 不会修改可空字段。未知字段返回 `400 unknown_parameter`。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/vaults/vlt_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "production-secrets-v2",
    "metadata": {"team": "support", "stage": "prod"}
  }'
```

Python

```
import os
import requests

resp = requests.post(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
    json={
        "name": "production-secrets-v2",
        "metadata": {"team": "support", "stage": "prod"},
    },
)
print(resp.status_code, resp.json())
```

### 响应字段

`200`，返回更新后的 Vault：

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
  "name": "production-secrets-v2",
  "metadata": {"team": "support", "stage": "prod"}
}
```

## 错误码

错误响应结构见[错误码](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-errors.md)。

HTTP 状态码

错误类型 / 错误码

解决方案

`400`

`invalid_request_error` / `unknown_parameter`

移除 `status` 等未知字段

`400`

`invalid_request_error` / `invalid_type`

按字段说明修正类型

`400`

`invalid_request_error` / `invalid_request_error`

按字段说明修正 `name`，并避免传 `null` 的 `metadata`

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在且未删除的 Vault ID

`409`

`conflict_error` / `conflict_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
