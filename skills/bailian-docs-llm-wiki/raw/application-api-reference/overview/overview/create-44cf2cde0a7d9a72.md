# 创建 Skill

上传 ZIP 包创建自定义 Skill，初始版本为 1.0。

## 接口

**POST** `/api/v1/skills`

使用 `multipart/form-data` 上传 ZIP 包，创建自定义 Skill。创建成功后初始版本为 `1.0`。

此接口只新增 Skill，不更新已有 Skill。为已有 Skill 上传新版本，使用[创建版本](raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)。

## 请求参数

表单字段

类型

必填

说明

file

`file`

是

Skill 包，必须为 `.zip`，大小不超过 50MB

display\_name

`string`

否

展示名称；不传或为空白时取 SKILL.md 的 `name`

display\_description

`string`

否

展示描述；不传或为空白时取 SKILL.md 的 `description`

ZIP 包根目录须包含 `SKILL.md`，Front Matter 中须包含 `name` 和 `description`。

## 响应

返回 `SkillDTO`。新建后 `latest_version` 为 `1.0`。提交安全扫描后 `status` 为 `checking`；未产生扫描任务时为 `active`。

字段

类型

说明

id

`string`

Skill 唯一标识

display\_name

`string`

展示名称

display\_description

`string`

展示描述

source

`string`

固定为 `customer`

status

`string`

`checking` 或 `active`

latest\_version

`string`

最新版本号

classification

`string / null`

固定为 `null`，自定义 Skill 无分类

meta\_info

`object / null`

固定为 `null`，自定义 Skill 无元信息

created\_at

`string`

创建时间

updated\_at

`string`

更新时间

## 示例

```
curl -X POST "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -F "file=@./pdf-skill.zip" \
  -F "display_name=pdf3.0" \
  -F "display_description=PDF 处理技能"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "id": "skill_NWVhN2MyM2MyZjA3xxxxxxxxxxxx",
    "display_name": "pdf3.0",
    "display_description": "PDF 处理技能",
    "source": "customer",
    "status": "checking",
    "latest_version": "1.0",
    "classification": null,
    "meta_info": null,
    "created_at": "2026-06-16T07:56:03Z",
    "updated_at": "2026-06-16T07:56:03Z"
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

SKILL\_FILE\_FORMATER\_ERROR

缺少 `SKILL.md`，或 Front Matter 缺少 `name` 或 `description`

500

SKILL\_NAME\_OFFICIAL\_DUPLICATE

SKILL.md 的 `name` 与官方 Skill 重名

500

SKILL\_NAME\_CUSTOMER\_DUPLICATE

SKILL.md 的 `name` 与当前空间的自定义 Skill 重名

500

SKILL\_PACKAGE\_TOO\_LARGE

ZIP 解压后累计大小超过 100MB

完整错误码见[Skill API 错误码](raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)。
