# 上传 Skill 新版本

为已有技能上传新版本的 zip 包。请求体仅含 file\_id，版本号由服务端生成；新版本同样需经过安全扫描，仅 active 可挂载；已挂载旧版本的智能体不受影响。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。上传新版本前需先用[File](raw/application-api-reference/managed-agents-api/files-api.md)上传 zip 包获得 `file_id`。

## 接口

**POST** `/skills/{skill_id}/versions`

请求体仅含 `file_id`。版本号由服务端生成；新版本同样需经过安全扫描；已挂载旧版本的智能体不受影响。

## 请求示例

bash

```
curl -X POST "$AGENTSTUDIO_URL/skills/skill_xxx/versions" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "file_xxx"}'
```

python

```
sv = client.skills.versions.create("skill_xxx", file_id="file_xxx")
print(sv.version)
```

java

```
SkillVersion sv = client.skills().createVersion("skill_xxx",
    SkillCreateParam.builder().fileId("file_xxx").build());
System.out.println(sv.getVersion());
```

## 响应示例

```
{
  "id": "skillver_xxx",
  "skill_id": "skill_xxx",
  "type": "skill_version",
  "name": "pdf3.0",
  "description": "从 SKILL.md 解析的描述",
  "version": "1.1",
  "status": "checking",
  "created_at": "2026-06-15T08:23:11.456+00:00",
  "updated_at": "2026-06-15T08:23:11.456+00:00"
}
```

### 响应字段

字段

类型

说明

`id`

string

版本 ID，格式 `skillver_xxx`

`skill_id`

string

所属技能 ID

`type`

string

固定为 `skill_version`

`name` / `description`

string

从该版本 zip 包内 `SKILL.md` 解析得到

`version`

string

版本号，由服务端生成

`status`

string

扫描状态：`checking` / `active` / `rejected`，仅 `active` 可挂载

`created_at` / `updated_at`

string

创建 / 最近更新时间，ISO 8601

`additional_properties`

object

仅 `status=rejected` 时返回，含 `error_info`：按 zip 包内文件路径列出的安全审查问题
