# 删除 Environment template

删除指定的环境模板。

## 接口

**DELETE** `/agents/environments/templates/{template_id}`

成功返回 `200` 和删除信封。删除后再次获取或删除返回 `404`。

## 路径参数

**template\_id** `string` **（必选）**

环境模板 ID

本接口没有请求体和 Query 参数。

## 请求示例

curl

```
curl -sS -X DELETE "$BASE_URL/agents/environments/templates/envtmpl_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
client.beta.agents.environments.templates.delete("envtmpl_xxx")
```

### 响应字段

**id** `string`

被删除的环境模板 ID

**object** `string`

环境模板删除结果对象类型，固定为 `agent.environment.template.deleted`

**deleted** `boolean`

是否删除成功，删除成功时为 `true`

## 响应示例

```
{
  "id": "envtmpl_xxx",
  "object": "agent.environment.template.deleted",
  "deleted": true
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在的环境模板 ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
