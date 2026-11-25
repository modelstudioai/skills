# Skill 管理

创建、查询和删除 Skill。

Skill 管理接口用于创建自定义 Skill、查询 Skill 详情和列表，以及删除自定义 Skill。

| 接口 | 方法 | 说明 |
| --- | --- | --- |
| [创建 Skill](overview/create-44cf2cde0a7d9a72.md) | POST `/api/v1/skills` | 上传 ZIP 包创建自定义 Skill |
| [获取 Skill](overview/get-9c06b4218676761a.md) | GET `/api/v1/skills/{skill_id}` | 查询单个 Skill |
| [列出 Skill](overview/list-b23c792b7a3bf72b.md) | GET `/api/v1/skills` | 分页查询自定义和官方 Skill |
| [删除 Skill](overview/delete-75ffff308650522a.md) | DELETE `/api/v1/skills/{skill_id}` | 删除自定义 Skill 及其全部版本 |

> **说明**
>
> 状态为 `active` 时才能挂载到智能体；安全扫描未完成时状态为 `checking`。挂载方式见 Agent 的 [`skills` 字段](../managed-agents-api/agent-api/agent-create.md)。
