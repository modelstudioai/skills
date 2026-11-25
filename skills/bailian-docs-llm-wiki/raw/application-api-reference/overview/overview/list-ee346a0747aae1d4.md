# 列出版本

分页查询 Skill 的版本，新版本在前。

<a id="接口"></a>

<a id="h-skill-version-list-endpoint"></a>

## 接口

**GET** `/api/v1/skills/{skill_id}/versions`

分页查询 Skill 的版本，新版本在前。自定义 Skill 返回未删除的全部版本，包含 `checking` 和 `rejected` 状态；官方 Skill 仅返回 `active` 版本。

<a id="请求参数"></a>

<a id="h-skill-version-list-params"></a>

## 请求参数

| 参数 | 位置 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- | --- |
| skill\_id | Path | `string` | 是 | Skill ID |
| pageNo | Query | `integer` | 否 | 页码，默认 1，最小 1 |
| pageSize | Query | `integer` | 否 | 单页条数，默认 20，取值范围 1 到 100 |

`pageNo × pageSize` 不能超过 10000。

<a id="响应"></a>

<a id="h-skill-version-list-response"></a>

## 响应

`data` 为分页对象，`items` 每项为 `SkillVersionDTO`。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| items | `array<SkillVersionDTO>` | 当前页版本列表 |
| total | `long` | 版本总数 |
| page\_no | `integer` | 当前页码 |
| page\_size | `integer` | 单页条数 |

<a id="示例"></a>

<a id="h-skill-version-list-example"></a>

## 示例

<a id="code-block"></a>

```bash
curl "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/skills/skill_abc123/versions?pageNo=1&pageSize=10" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="code-block-2"></a>

```json
{
  "success": true,
  "error_code": null,
  "error_msg": null,
  "data": {
    "items": [
      {
        "id": "skillver_NWQ3YmQ1OTRjNGFmxxxxxx",
        "type": "skill_version",
        "skill_id": "skill_abc123",
        "display_name": "workflow-automation",
        "display_description": "将多个技能串联成自动化工作流",
        "version": "1.0",
        "status": "rejected",
        "created_at": "2026-05-11T09:25:43Z",
        "updated_at": "2026-05-11T09:31:01Z",
        "additional_properties": {
          "error_info": {
            "/index.js": "[Dangerous Tools Without Confirmation] Line 179: ...",
            "/SKILL.md": "[Dangerous Tools Without Confirmation] Line 10: ..."
          }
        }
      }
    ],
    "total": 1,
    "page_no": 1,
    "page_size": 10
  },
  "request_id": "28e054b1-2cc4-4e0f-bac5-0c1395b1d7ae"
}
```

<a id="错误"></a>

<a id="h-skill-version-list-errors"></a>

## 错误

| HTTP 状态码 | error\_code | 说明 |
| --- | --- | --- |
| 401 | WORKSPACE\_ID\_ILLEGAL | 身份信息缺失或无效 |
| 400 | SKILL\_ID\_IS\_NULL | `skill_id` 为空白 |
| 400 | INVALID\_PARAMETER | `pageNo` 或 `pageSize` 非整数、越界或超出分页范围 |
| 500 | SKILL\_NOT\_EXIST | Skill 不存在、已删除或无权访问 |
