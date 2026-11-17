# 删除 Vault

删除 Vault 及其下全部 Credential。删除后无法恢复。

## 接口

**DELETE** `/vaults/{vault_id}`

路径相对 Base URL。每个请求携带 `Authorization: Bearer $DASHSCOPE_API_KEY`，认证方式见[认证](raw/application-api-reference/openai-compatible-agents-api/openai-compatible-agents-api-authentication.md)。

## 路径参数

**vault\_id** `string` **（必选）**

Vault ID，按不透明 ID 使用

## 请求示例

curl

```
curl -sS -X DELETE "$BASE_URL/vaults/vlt_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

Python

```
import os
import requests

resp = requests.delete(
    f"{os.environ['BASE_URL']}/vaults/vlt_xxx",
    headers={"Authorization": f"Bearer {os.environ['DASHSCOPE_API_KEY']}"},
)
print(resp.json())
```

### 响应字段

`200`，返回删除信封：

**id** `string`

被删除的 Vault ID

**object** `string`

Vault 删除结果对象类型，固定为 `vault.deleted`

**deleted** `boolean`

是否删除成功，成功时为 `true`

删除 Vault 会删除其下全部 Credential。删除后再次获取或删除返回 `404`。

## 响应示例

```
{
  "id": "vlt_xxx",
  "object": "vault.deleted",
  "deleted": true
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
