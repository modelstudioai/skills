# 创建 Memory Store

创建一个记忆库，用于保存智能体的长期工作笔记。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/memory_stores`

## 请求体

**name** `string` **（必选）**

记忆库名称，1-255 字符

**description** `string` **（可选）**

用途说明，缺省返回空字符串

**metadata** `object` **（可选）**

业务自定义键值对元数据，缺省为空对象

## 请求示例

curl

```
curl -X POST "$AGENTSTUDIO_URL/memory_stores" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"name": "项目知识库","description": "项目约定、决策记录与排查笔记"}'
```

### 响应字段

**id** `string`

记忆库 ID，格式 memstore\_xxx

**type** `string`

固定为 memory\_store

**name** `string`

记忆库名称，1-255 字符

**description** `string`

用途说明；未填写时为空字符串

**metadata** `object`

业务自定义键值对元数据

**archived\_at** `string | null`

归档时间，未归档时省略或为 null

**created\_at** `string`

创建时间，ISO 8601 UTC

**updated\_at** `string`

最近更新时间，ISO 8601 UTC

## 响应

```
{
  "id": "memstore_xxx",
  "type": "memory_store",
  "name": "项目知识库",
  "description": "项目约定、决策记录与排查笔记",
  "metadata": {
    "team": "data"
  },
  "created_at": "2026-09-17T08:00:00Z",
  "updated_at": "2026-09-17T08:00:00Z"
}
```

## 错误码

**状态码**

**错误码**

**说明**

400

`invalid_request_error`

参数、路径、limit 或分页游标非法

401

`InvalidApiKey`

API Key 缺失、错误或失效

403

`permission_error`

身份或资源访问权限不足
