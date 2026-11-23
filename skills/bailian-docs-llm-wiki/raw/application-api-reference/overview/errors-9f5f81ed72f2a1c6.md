# Skill API 错误码

Skill API 的错误响应结构、常见错误码和排查建议。

Skill API 的成功响应和业务错误使用统一响应结构。

## 响应结构

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

`object / null`

业务数据，失败时为 `null`

request\_id

`string`

请求 ID，同时通过响应头 `X-Request-Id` 返回

```
{
  "success": false,
  "error_code": "SKILL_NOT_EXIST",
  "error_msg": "skill不存在",
  "data": null,
  "request_id": "15a89d4c-f142-4e00-a9f7-b088442417c9"
}
```

## HTTP 状态码

HTTP 状态码

说明

400

请求参数缺失、格式错误或超出取值范围

401

身份信息缺失或无效

500

业务处理失败或服务内部错误，`error_code` 给出具体原因

## 常见错误码

HTTP 状态码

error\_code

说明

401

WORKSPACE\_ID\_ILLEGAL

身份信息缺失或无效

400

INVALID\_PARAMETER

参数格式错误、取值不合法或分页超出范围

400

SKILL\_ID\_IS\_NULL

`skill_id` 为空白

400

SKILL\_VERSION\_IS\_NULL

`version` 为空白

400

SKILL\_FILE\_IS\_NULL

未上传 `file` 或文件为空

400

SKILL\_FILE\_FORMATER\_ERROR

文件扩展名不是 `.zip`，或文件头不是 ZIP 格式

400

SKILL\_PACKAGE\_TOO\_LARGE

ZIP 包超过 50MB

500

SKILL\_FILE\_FORMATER\_ERROR

缺少 `SKILL.md`，或 Front Matter 缺少 `name` 或 `description`

500

SKILL\_PACKAGE\_TOO\_LARGE

ZIP 解压后累计大小超过 100MB

500

SKILL\_FILE\_READ\_ERROR

读取上传文件或写入存储失败

500

SKILL\_EXTRA\_ZIP\_ERROR

ZIP 解压失败，仅支持 UTF-8 或 GBK 文件名编码

500

SKILL\_NOT\_EXIST

Skill 不存在、已删除或无权访问

500

SKILL\_VERSION\_NOT\_EXIST

版本不存在、已删除或不可见

500

SKILL\_DELETE\_OFFICIAL\_NOT\_ALLOWED

尝试删除官方 Skill

500

SKILL\_DELETE\_ERROR

删除 Skill 失败

500

SKILL\_UPDATE\_SECURITY\_ERROR

Skill 正在安全扫描中，暂不能创建新版本

500

SKILL\_NAME\_OFFICIAL\_DUPLICATE

SKILL.md 的 `name` 与官方 Skill 重名

500

SKILL\_NAME\_CUSTOMER\_DUPLICATE

SKILL.md 的 `name` 与当前空间的自定义 Skill 重名

500

SKILL\_SUBMIT\_SECURITY\_ERROR

提交安全扫描失败

500

SKILL\_INSERT\_ERROR

保存 Skill 或版本记录失败

500

SKILL\_UPDATE\_LOCK\_ERROR

同一 Skill 的保存操作并发冲突

500

SYSTEM\_ERROR

服务内部错误

## 排查建议

1.  使用 `request_id` 定位具体请求。
2.  检查 API Key、工作空间 ID 和 Endpoint 是否正确，详见[认证](raw/application-api-reference/overview/authentication-26822a11844efd00.md)。
3.  上传 ZIP 包前确认文件不超过 50MB，且包内包含 `SKILL.md`。
4.  按 `skill_id` 查询 Skill 状态，确认无正在进行的扫描或并发操作。
