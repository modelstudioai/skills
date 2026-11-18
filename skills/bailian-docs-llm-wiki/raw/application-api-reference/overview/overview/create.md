# 创建版本

为自定义 Skill 上传新版本 ZIP 包，版本号由服务端递增。

## 接口

**POST** `/api/v1/skills/{skill_id}/versions`

使用 `multipart/form-data` 为自定义 Skill 上传新版本。版本号由服务端在 `latest_version` 基础上递增，例如 `1.0` 递增为 `1.1`，不能指定。

## 请求参数

参数

位置

类型

必填

说明

skill\_id

Path

`string`

是

主账号和工作空间下的自定义 Skill ID

file

Form

`file`

是

新版本 ZIP 包，要求同[创建 Skill](raw/application-api-reference/overview/overview/create.md)

display\_name

Form

`string`

否

更新 Skill 展示名称；不传或为空白时取新包 SKILL.md 的 `name`

display\_description

Form

`string`

否

更新 Skill 展示描述；不传或为空白时取新包 SKILL.md 的 `description`

## 业务规则

-   仅自定义 Skill 可以创建版本。
-   Skill 正在安全扫描（`checking`）时不能创建新版本，需等待扫描结束；`rejected` 状态可以重新上传。
-   新包 SKILL.md 的 `name` 不能与官方 Skill 或当前空间的其他自定义 Skill 重名。
-   创建成功后，Skill 的 `latest_version` 指向新版本，旧版本保留。
-   请求中的 `display_name` 和 `display_description` 用于更新 Skill 展示信息。

## 响应

返回新版本的 `SkillVersionDTO`。

字段

类型

说明

id

`string`

版本记录唯一标识

type

`string`

固定为 `skill_version`

skill\_id

`string`

所属 Skill ID

display\_name

`string`

该版本的展示名称

display\_description

`string`

该版本的展示描述

version

`string`

版本号

status

`string`

版本状态

created\_at

`string`

创建时间

updated\_at

`string`

更新时间

additional\_properties

`object / null`

扩展属性

## 示例

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills/skill_abc123/versions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -F "file=@./pdf-skill-v2.zip"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "id": "skillver_xxxxxxxxxxxxxxxxxxxxxx",
    "type": "skill_version",
    "skill_id": "skill_abc123",
    "display_name": "My Custom Skill",
    "display_description": "从 SKILL.md 解析的描述",
    "version": "1.1",
    "status": "checking",
    "created_at": "2026-06-15T08:23:11Z",
    "updated_at": "2026-06-15T08:23:11Z",
    "additional_properties": null
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

400

SKILL\_FILE\_IS\_NULL

未上传 `file` 或文件为空

400

SKILL\_FILE\_FORMATER\_ERROR

文件扩展名不是 `.zip`，或文件头不是 ZIP 格式

400

SKILL\_PACKAGE\_TOO\_LARGE

ZIP 包超过 50MB

400

INVALID\_PARAMETER

multipart 请求格式错误

500

SKILL\_NOT\_EXIST

Skill 不存在、已删除或无权访问

500

SKILL\_VERSION\_NOT\_EXIST

保存成功但读取新版本记录失败

500

SKILL\_UPDATE\_SECURITY\_ERROR

Skill 正在安全扫描中

500

SKILL\_NAME\_OFFICIAL\_DUPLICATE

新包 `name` 与官方 Skill 重名

500

SKILL\_NAME\_CUSTOMER\_DUPLICATE

新包 `name` 与当前空间的其他自定义 Skill 重名

500

SKILL\_UPDATE\_LOCK\_ERROR

同一 Skill 的并发创建版本冲突

完整错误码见[Skill API 错误码](raw/application-api-reference/overview/errors.md)。
