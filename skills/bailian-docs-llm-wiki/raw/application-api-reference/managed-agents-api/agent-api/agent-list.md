# 列出 Agent

分页列出当前工作空间下的智能体，按 created\_at 倒序返回。默认不包含已归档项，传 include\_archived=true 可包含。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**GET** `/agents`

## Query 参数

参数

必填

类型

说明

`limit`

否

int

单页条数，默认 20，最大 100

`page`

否

string

分页游标。首次不传，后续传上一次响应的 `next_page` 翻下一页

`include_archived`

否

bool

是否包含已归档智能体，默认 `false`

## 请求示例

bash

```
curl "$AGENTSTUDIO_URL/agents?limit=20&include_archived=true" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
for agent in client.agents.list(limit=20, include_archived=True):
    print(agent.id, agent.name, agent.model['id'])
```

java

```
CursorPage<Agent> page = client.agents().list(AgentListParam.builder()
    .limit(20).includeArchived(true).build());
for (Agent a : page.getData()) System.out.println(a.getId() + " " + a.getName());
```

## 响应说明

响应包含 `data`（Agent 对象数组）与 `next_page`（下一页游标，无更多数据时为 `null`）。每个 Agent 对象的字段同[创建 Agent](raw/application-api-reference/managed-agents-api/agent-api/agent-create.md)响应，字段说明如下：

### Agent 对象字段

字段

类型

说明

`id`

string

智能体 ID，格式 `agent_&lt;ULID&gt;`

`type`

string

固定为 `agent`

`version`

int

当前版本号，每次更新自动递增

`name` / `description` / `system`

string

智能体名称、用途说明、系统提示词

`model` / `tools` / `mcp_servers` / `skills` / `multiagent` / `metadata`

object / array

模型、工具包、MCP 引用、技能、多智能体协作配置、业务元数据

`archived_at`

string / null

归档时间，未归档时为 `null`

`created_at` / `updated_at`

string

创建 / 最近更新时间，ISO 8601

`workspace_id`

string

所属工作空间 ID
