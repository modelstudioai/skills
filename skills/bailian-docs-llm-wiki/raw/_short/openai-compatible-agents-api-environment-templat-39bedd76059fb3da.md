# 创建 Environment template

创建可复用的环境模板，保存容器、依赖、网络、初始文件和 Skill 配置。

## 接口

**POST** `/agents/environments/templates`

成功返回 `201` 和完整环境模板。请求体可以为空，此时创建使用默认配置的模板。

## 请求体

**name** `string / null` **（可选）**

模板名称

**packages** `object` **（可选）**

预装包，按 `npm`、`python`、`system` 分组，默认三组均为空数组

属性

**python** `array<string>` **（可选）**

Python 包

**system** `array<string>` **（可选）**

系统包

**npm** `array<string>` **（可选）**

npm 包

**env** `object<string,string>` **（可选）**

环境变量；变量名需匹配 `[A-Za-z_][A-Za-z0-9_]*`，不能是 `PATH`，也不能以服务端保留前缀开头；值不能包含 NUL

**setup\_commands** `array` **（可选）**

初始化命令，按顺序执行。每项包含必填的 `command` 和可选的 `cwd`，`cwd` 默认为 `/workspace`

属性

**command** `string` **（可选）**

初始化命令

**cwd** `string` **（可选）**

工作目录，默认 `/workspace`

**network** `object` **（可选）**

网络策略，默认 `enabled`；不接受 `blocked_domains`

属性

**access** `string` **（可选）**

网络访问模式，`enabled`、`disabled` 或 `restricted`

**allowed\_domains** `array<string>` **（可选）**

允许的域名，仅 `access=restricted` 时生效

**desktop** `object` **（可选）**

桌面配置，只接受 `enabled=false`，`enabled=true` 返回 `400`

属性

**enabled** `boolean` **（可选）**

是否启用桌面

**capability\_directories** `array<string>` **（可选）**

能力发现目录，默认 `[]`

**skills** `array` **（可选）**

Skill 配置，固定为 `skill_reference`

**plugins** `array` **（可选）**

插件配置，当前只支持空数组，非空返回 `400`

**files** `array` **（可选）**

初始文件配置，固定为 `file_id`

模板响应不返回 `env` 和 `setup_commands`。`files` 固定为 `file_id`，`skills` 固定为 `skill_reference`。

## 请求示例

curl

```
curl -sS -X POST "$BASE_URL/agents/environments/templates" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "OpenAI-Beta: agents=v1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example-template",
    "network": {"access": "disabled"},
    "capability_directories": ["/workspace/skills"]
  }'
```

Python

```
template = client.beta.agents.environments.templates.create(
    name="example-template",
    network={"access": "disabled"},
    capability_directories=["/workspace/skills"],
)
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

`400`

`invalid_request_error` / `invalid_request_error`

按字段说明修正请求体

`400`

`invalid_request_error` / `invalid_request_error`

`desktop.enabled=true`、非空 `plugins` 和 `network.blocked_domains` 都会被拒绝，按字段说明调整

`401`

`authentication_error` / `invalid_api_key`

在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY`

`500`

`server_error` / `server_error`

稍后重试；持续失败时提交工单并提供 `x-request-id`
