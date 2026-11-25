# 获取版本详情

查询指定版本的元数据和扫描状态。

<a id="接口"></a>

<a id="h-skill-version-get-endpoint"></a>

## 接口

**GET** `/api/v1/skills/{skill_id}/versions/{version}`

查询指定版本。版本号精确匹配，不回退到最新版本。

官方 Skill 仅可查询 `active` 版本，其他状态按版本不存在处理。已删除版本按不存在处理。

<a id="请求参数"></a>

<a id="h-skill-version-get-params"></a>

## 请求参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| skill\_id | `string` | 是 | Skill ID |
| version | `string` | 是 | 版本号，例如 `1.0` |

<a id="响应"></a>

<a id="h-skill-version-get-response"></a>

## 响应

返回 `SkillVersionDTO`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | `string` | 版本记录唯一标识 |
| type | `string` | 固定为 `skill_version` |
| skill\_id | `string` | 所属 Skill ID |
| display\_name | `string` | 该版本的展示名称 |
| display\_description | `string` | 该版本的展示描述 |
| version | `string` | 版本号 |
| status | `string` | 版本状态 |
| created\_at | `string` | 创建时间 |
| updated\_at | `string` | 更新时间 |
| additional\_properties | `object / null` | 扩展属性；安全扫描未通过时包含 `error_info` |

<a id="示例"></a>

<a id="h-skill-version-get-example"></a>

## 示例

<a id="code-block"></a>

```bash
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills/skill_abc123/versions/1.0" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="code-block-2"></a>

```json
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
    "version": "1.0",
    "status": "checking",
    "created_at": "2026-06-15T08:23:11Z",
    "updated_at": "2026-06-15T08:23:11Z",
    "additional_properties": null
  },
  "request_id": "15a89d4c-f142-4e00-a9f7-b088442417c9"
}
```

<a id="错误"></a>

<a id="h-skill-version-get-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 401 | WORKSPACE\_ID\_ILLEGAL | 身份信息缺失或无效 |
| 400 | SKILL\_ID\_IS\_NULL | `skill_id` 为空白 |
| 400 | SKILL\_VERSION\_IS\_NULL | `version` 为空白 |
| 500 | SKILL\_NOT\_EXIST | Skill 不存在、已删除或无权访问 |
| 500 | SKILL\_VERSION\_NOT\_EXIST | 版本不存在、已删除或官方 Skill 的非 `active` 版本 |
