# 删除 Skill

删除技能及全部版本，不可再挂载到新智能体。已挂载旧版本的智能体仍可正常使用，会话历史不受影响。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/skills/{skill_id}`

## 请求示例

bash

```
curl -X DELETE "$AGENTSTUDIO_URL/skills/skill_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
client.skills.delete("skill_xxx")
```

java

```
client.skills().delete("skill_xxx");
```

## 响应示例

```
{
  "id": "skill_xxx",
  "type": "skill_deleted",
  "request_id": "xxx"
}
```

### 响应字段

字段

类型

说明

`id`

string

被删除的技能 ID

`type`

string

固定为 `skill_deleted`

`request_id`

string

本次请求的唯一标识
