# 更新 Environment template

更新环境模板配置；省略的字段保持原值。

## 接口

**POST** `/agents/environments/templates/{template_id}`

成功返回 `200` 和更新后的完整环境模板。省略的字段保持原值。

## 路径参数

**template\_id** `string` **（必选）**

环境模板 ID

## 请求体

**name** `string / null` **（可选）**

模板名称

**packages** `object` **（可选）**

预装包，按 `npm`、`python`、`system` 分组

**env** `object<string,string>` **（可选）**

环境变量；变量名和值限制与创建环境模板一致

**setup\_commands** `array` **（可选）**

初始化命令，按顺序执行

**network** `object` **（可选）**

网络策略，包含 `access`、`allowed_domains`；不接受 `blocked_domains`

**desktop** `object` **（可选）**

桌面配置，只接受 `enabled=false`，`enabled=true` 返回 `400`

**capability\_directories** `array<string>` **（可选）**

能力发现目录

**skills** `array` **（可选）**

Skill 配置，固定为 `skill_reference`

**plugins** `array` **（可选）**

插件配置，当前只支持空数组，非空返回 `400`

**files** `array` **（可选）**

初始文件配置，固定为 `file_id`

只传 `name` 时，原有 `network`、`capability_directories` 等配置保持不变。

显式 `null` 会重置对应字段：`name` 清空，`network` 恢复默认策略，`desktop` 恢复 `enabled=false`，数组字段清空。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/environments/templates/envtmpl_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{"name": "example-template-v2"}'
```

Python

```
template = client.beta.agents.environments.templates.update(
    "envtmpl_xxx",
    name="example-template-v2",
)
print(template.updated_at)
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
  "name": "example-template-v2",
  "object": "agent.environment.template",
  "created_at": 1794319007,
  "updated_at": 1794319102,
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

`400`

`invalid_request_error` / `invalid_request_error`

按字段说明修正请求体

`400`

`invalid_request_error` / `invalid_request_error`

`desktop.enabled=true`、非空 `plugins` 和 `network.blocked_domains` 都会被拒绝，按字段说明调整

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`404`

`not_found_error` / `not_found_error`

使用当前工作空间中存在的环境模板 ID

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
