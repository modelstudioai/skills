# 删除 Webhook

删除 Webhook。删除后不再投递新的事件，已产生但尚未投递的事件会被取消。已有投递事件在 7 天保留期内仍可查询。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/webhook_endpoints/{id}`

## 路径参数

**id** `string` **（必选）**

Webhook ID，格式 wep\_<ULID>

## 请求示例

curl

```
curl -X DELETE "$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 响应字段

**request\_id** `string`

请求唯一标识

## 响应

```
{
  "request_id": "8e1d16e4"
}
```

## 错误码

**状态码**

**错误码**

**说明**

404

`11800001`

webhook not found
