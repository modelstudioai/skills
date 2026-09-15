# 下载 Skill 包

返回 OSS 预签名 URL（file\_url），有效期 2 小时，可直接 GET 该 URL 拿到 zip 包内容。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/skills/{skill_id}/versions/{version}/content`

## 请求示例

bash

```
curl "$AGENTSTUDIO_URL/skills/skill_xxx/versions/1.0/content" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
content = client.skills.versions.download("skill_xxx", "1.0")
print(content["file_url"])
```

java

```
JsonObject content = client.skills().downloadVersion("skill_xxx", "1.0");
System.out.println(content.get("file_url").getAsString());
```

## 响应示例

```
{
  "skill_id": "skill_xxx",
  "version": "1.0",
  "file_url": "https://<oss-bucket>.oss-cn-xxx.aliyuncs.com/...?Expires=...&Signature=YOUR_SIGNATURE",
  "request_id": "xxx"
}
```

### 响应字段

字段

类型

说明

`skill_id`

string

所属技能 ID

`version`

string

版本号

`file_url`

string

OSS 预签名下载 URL，有效期 2 小时

`request_id`

string

本次请求的唯一标识
