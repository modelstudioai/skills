# 删除 Skill

删除自定义 Skill 及其全部版本，删除后不可恢复。

## 接口

**DELETE** `/api/v1/skills/{skill_id}`

删除自定义 Skill 及其全部版本。删除后不可恢复，已挂载旧版本的智能体不受影响。

## 请求参数

参数

类型

必填

说明

skill\_id

`string`

是

自定义 Skill ID

## 响应

返回 `SkillDeletedResponse`。

字段

类型

说明

id

`string`

被删除的 Skill ID

type

`string`

固定为 `skill_deleted`

## 示例

```
curl -X DELETE "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills/skill_abc123" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "id": "skill_abc123",
    "type": "skill_deleted"
  },
  "request_id": "15a89d4c-f142-4e00-a9f7-b088442417c9"
}
```

## 错误

HTTP 状态码

error\_code

说明

401

WORKSPACE\_ID\_ILLEGAL

身份信息缺失或无效

400

SKILL\_ID\_IS\_NULL

`skill_id` 为空白

500

SKILL\_NOT\_EXIST

Skill 不存在、已删除或无权访问；重复删除返回此错误

500

SKILL\_DELETE\_OFFICIAL\_NOT\_ALLOWED

尝试删除官方 Skill

500

SKILL\_DELETE\_ERROR

删除失败
