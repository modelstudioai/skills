# 下载版本 ZIP

获取 Skill 版本 ZIP 包的临时下载地址，有效期 2 小时。

## 接口

**GET** `/api/v1/skills/{skill_id}/versions/{version}/content`

返回版本 ZIP 包的临时下载地址，不直接返回 ZIP 二进制流。版本号精确匹配，不回退到最新版本。

自定义 Skill 可以下载未删除的全部版本，包含 `checking` 和 `rejected` 状态；官方 Skill 仅可下载 `active` 版本。

## 请求参数

参数

类型

必填

说明

skill\_id

`string`

是

Skill ID

version

`string`

是

版本号，例如 `1.0`

## 响应

返回 `VersionDownloadResponse`。

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

**说明**下载地址每次请求实时生成，过期后重新调用本接口获取。

## 示例

```
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills/skill_abc123/versions/1.0/content" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```
```
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "skill_id": "skill_abc123",
    "version": "1.0",
    "file_url": "https://example-bucket.oss-cn-beijing.aliyuncs.com/skills/pdf-skill-1.0.zip?Expires=...&Signature=..."
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

SKILL\_VERSION\_IS\_NULL

`version` 为空白

500

SKILL\_NOT\_EXIST

Skill 不存在、已删除或无权访问

500

SKILL\_VERSION\_NOT\_EXIST

版本不存在、已删除或官方 Skill 的非 `active` 版本

500

SYSTEM\_ERROR

下载地址生成失败
