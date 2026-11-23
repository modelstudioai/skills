# Skill API 概览

Skill API 用于管理百炼上的 Skill，支持创建、查询、删除 Skill 及管理版本。

Skill API 用于管理阿里云百炼上的 Skill，覆盖自定义 Skill 与官方 Skill 的创建、查询、删除，以及版本上传、查询和下载。

**说明**调用前请先配置[认证](raw/application-api-reference/overview/authentication-26822a11844efd00.md)；错误处理见[Skill API 错误码](raw/application-api-reference/overview/errors-9f5f81ed72f2a1c6.md)。

## 前提条件

1.  已开通阿里云百炼，并[创建 API Key](raw/model-api-reference/preparations/get-api-key.md)。
2.  已获取工作空间 ID。登录[百炼控制台](https://bailian.console.aliyun.com/)，在右上角工作空间菜单中复制工作空间 ID。

## Endpoint

```
https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills
```

-   `workspace_id`：工作空间 ID。

## 接口列表

接口

方法

说明

[创建 Skill](raw/application-api-reference/overview/overview/create-44cf2cde0a7d9a72.md)

POST `/api/v1/skills`

上传 ZIP 包创建自定义 Skill

[获取 Skill](raw/application-api-reference/overview/overview/get-9c06b4218676761a.md)

GET `/api/v1/skills/{skill_id}`

查询单个 Skill

[列出 Skill](raw/application-api-reference/overview/overview/list-b23c792b7a3bf72b.md)

GET `/api/v1/skills`

分页查询自定义和官方 Skill

[删除 Skill](raw/application-api-reference/overview/overview/delete-75ffff308650522a.md)

DELETE `/api/v1/skills/{skill_id}`

删除自定义 Skill 及其全部版本

[创建版本](raw/application-api-reference/overview/overview/create-66b335d7c24c1f0f.md)

POST `/api/v1/skills/{skill_id}/versions`

为自定义 Skill 上传新版本

[列出版本](raw/application-api-reference/overview/overview/list-ee346a0747aae1d4.md)

GET `/api/v1/skills/{skill_id}/versions`

分页查询版本

[获取版本详情](raw/application-api-reference/overview/overview/get-2856ed31dd1c9b3d.md)

GET `/api/v1/skills/{skill_id}/versions/{version}`

查询指定版本

[下载版本 ZIP](raw/application-api-reference/overview/overview/download.md)

GET `/api/v1/skills/{skill_id}/versions/{version}/content`

获取 ZIP 包的临时下载地址

## 响应结构

成功和业务错误统一返回以下结构：

字段

类型

说明

success

`boolean`

请求是否成功

error\_code

`string / null`

错误码，成功时为 `null`

error\_msg

`string / null`

错误信息，成功时为 `null`

data

`object / array / null`

业务数据，失败时为 `null`

request\_id

`string`

请求 ID，同时通过响应头 `X-Request-Id` 返回

```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {},
  "request_id": "15a89d4c-f142-4e00-a9f7-b088442417c9"
}
```

## 分页

Skill 列表和版本列表使用页码分页。

参数

类型

默认

说明

pageNo

`integer`

1

页码，最小 1

pageSize

`integer`

20

单页条数，取值范围 1 到 100

`pageNo × pageSize` 不能超过 10000。响应返回 `total`、`page_no`、`page_size`，调用方据此计算总页数。

## 枚举

**status**

值

说明

checking

安全扫描中，暂不可用

active

可用

rejected

未通过安全扫描，不可用

deleted

已删除，正常查询不返回

**source**

值

说明

customer

主账号和工作空间下的自定义 Skill

official

官方 Skill

## 数据结构

### SkillDTO

创建 Skill、获取 Skill 和 Skill 列表返回此对象。

字段

类型

说明

id

`string`

Skill 唯一标识，用作路径参数 `skill_id`

display\_name

`string`

展示名称；为空时取 SKILL.md 的 `name`

display\_description

`string`

展示描述；为空时取 SKILL.md 的 `description`

source

`string`

`customer` 或 `official`

status

`string`

Skill 主记录状态，见上表

latest\_version

`string`

最新版本号，例如 `1.0`

classification

`string / null`

分类；官方 Skill 有值，自定义 Skill 为 `null`

meta\_info

`object / null`

官方 Skill 的元信息；自定义 Skill 为 `null`

created\_at

`string`

创建时间，ISO 8601 UTC

updated\_at

`string`

更新时间，ISO 8601 UTC

### SkillVersionDTO

创建版本、列出版本和获取版本详情返回此对象。

字段

类型

说明

id

`string`

版本记录唯一标识，`skillver_` 前缀

type

`string`

固定为 `skill_version`

skill\_id

`string`

所属 Skill ID

display\_name

`string`

该版本的展示名称；为空时取该版本 SKILL.md 的 `name`

display\_description

`string`

该版本的展示描述；为空时取该版本 SKILL.md 的 `description`

version

`string`

版本号，格式为 `major.minor`，例如 `1.0`、`1.1`

status

`string`

该版本状态，见上表

created\_at

`string`

创建时间，ISO 8601 UTC

updated\_at

`string`

更新时间，ISO 8601 UTC

additional\_properties

`object / null`

扩展属性；无内容时为 `null`

`additional_properties` 字段：

字段

类型

说明

error\_info

`map<string,string> / null`

安全扫描未通过时的明细，键为文件路径，值为问题描述

### SkillDeletedResponse

字段

类型

说明

id

`string`

被删除的 Skill ID

type

`string`

固定为 `skill_deleted`

### VersionDownloadResponse

字段

类型

说明

skill\_id

`string`

Skill ID

version

`string`

版本号

file\_url

`string`

ZIP 包的预签名下载地址，有效期 2 小时

### Page

Skill 列表和版本列表的 `data` 结构。

字段

类型

说明

items

`array`

当前页记录

total

`long`

命中总数

page\_no

`integer`

当前页码

page\_size

`integer`

单页条数

## 可见性

按 `skill_id` 访问的接口先校验可见性，不可见时按不存在处理。

对象

自定义 Skill

官方 Skill

Skill

主账号和工作空间下未删除的记录

未删除且状态为 `active`

版本

未删除的全部状态，包含 `checking` 和 `rejected`

仅 `active`
