# 获取 Environment template

根据模板 ID 返回完整的环境模板配置。

## 接口

**GET** `/agents/environments/templates/{template_id}`

成功返回 `200` 和完整环境模板。

## 路径参数

**template\_id** `string` **（必选）**

环境模板 ID

## 请求示例

curl

```
curl -sS "$BASE_URL/agents/environments/templates/envtmpl_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1"
```

Python

```
template = client.beta.agents.environments.templates.retrieve("envtmpl_xxx")
print(template.id, template.name)
```

### 响应字段

**id** `string`

环境模板 ID

**object** `string`

环境模板对象类型，固定为 `agent.environment.template`

**name** `string / null`

模板名称

**created\_at** `integer`

创建时间，Unix 秒

**updated\_at** `integer`

最近更新时间，Unix 秒

**packages** `object`

预装包，包含 `python`、`system`、`npm`

**network** `object`

网络策略，包含 `access`、`allowed_domains`

**desktop** `object`

桌面配置，包含 `enabled`

**capability\_directories** `array<string>`

能力发现目录

**skills** `array`

Skill 配置，包含 `type`、`skill_id`、`version`

**plugins** `array`

插件安全元数据。包含 `type`、`name`、`description`，当前为空数组

**files** `array`

初始文件配置，每项包含 `type`、`path`、`file_id`

响应不返回 `env` 和 `setup_commands`。

## 响应示例

```
{
  "id": "envtmpl_xxx",
  "name": "example-template",
  "object": "agent.environment.template",
  "created_at": 1794319007,
  "updated_at": 1794319007,
  "packages": {"python": [], "system": [], "npm": []},
  "network": {"access": "disabled", "allowed_domains": []},
  "desktop": {"enabled": false},
  "capability_directories": ["/workspace/skills"],
  "skills": [],
  "plugins": [],
  "files": []
}
```

## 错误码

HTTP 状态码

错误类型 / 错误码

解决方案

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在的环境模板 ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
