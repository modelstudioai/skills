# 更新 Agent

采用全量替换语义：请求体须包含 version（当前版本号，用于乐观锁）以及完整的智能体配置，缺省的字段视为清空。若 version 与服务端不一致返回 409 冲突；成功后 version 自动递增，已绑定旧版本的会话不受影响。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**POST** `/agents/{agent_id}`

## 语义

采用**全量替换**：请求体须包含 `version`（当前版本号，用于乐观锁）以及完整的 `name`、`model`、`system`、`tools` 等字段，缺省的字段视为清空。成功后响应中 `version` 自动递增；已绑定旧版本的会话不受影响。

## 请求体

字段

必填

类型

说明

`version`

是

int

当前版本号，用于乐观锁。若与服务端不一致返回 409 冲突

`name`

是

string

智能体名称，缺省视为清空

`model`

是

object

模型配置，结构 `{"id": "qwen3-max"}`，必填子字段 `id`

`description`

否

string

智能体用途说明，缺省视为清空

`system`

否

string

系统提示词，缺省视为清空

`tools`

否

array<object>

工具包列表，含义同创建，缺省视为清空。`builtin_toolkit` 至多一项，`mcp_toolkit` 可多项

`mcp_servers`

否

array<object>

MCP Server 引用列表，含义同创建，缺省视为清空

`skills`

否

array<object>

挂载的技能列表，含义同创建，缺省视为清空

`multiagent`

否

object

多智能体协作配置，含义同创建，缺省视为清空

`metadata`

否

object

业务自定义键值，缺省视为清空

各字段结构详见[创建 Agent](raw/application-api-reference/managed-agents-api/agent-api/agent-create.md)的**请求体**一节。

## 请求示例

bash

```
curl -X POST "$AGENTSTUDIO_URL/agents/agent_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "version": 1,
    "name": "data-analyst",
    "description": "数据分析助手",
    "model": {"id": "qwen3-max"},
    "system": "你是资深数据分析师，输出结论时附带置信度。",
    "tools": [],
    "mcp_servers": [],
    "skills": [],
    "multiagent": {
      "type": "coordinator",
      "agents": [
        {"type": "self"},
        {"type": "agent", "id": "agent_researcher", "version": 3}
      ]
    },
    "metadata": {"team": "data"}
  }'
```

python

```
current = client.agents.retrieve("agent_xxx")
agent = client.agents.update(
    "agent_xxx",
    version=current.version,
    name="data-analyst",
    model="qwen3.8-max",
    description="数据分析助手",
    system_prompt="你是资深数据分析师，输出结论时附带置信度。",
    tools=[],
    mcp_servers=[],
    skills=[],
    metadata={"team": "data"},
)
```

java

```
Agent current = client.agents().retrieve("agent_xxx");
Agent updated = client.agents().update("agent_xxx", AgentUpdateParam.builder()
    .version(current.getVersion())
    .name("data-analyst")
    .model("qwen3-max")
    .description("数据分析助手")
    .instructions("你是资深数据分析师，输出结论时附带置信度。")
    .metadata(Map.of("team", "data"))
    .build());
```

## 响应说明

响应为更新后的 Agent 对象，结构同[创建 Agent](raw/application-api-reference/managed-agents-api/agent-api/agent-create.md)响应，`version` 自动递增。字段如下：

### 响应字段

字段

类型

说明

`id`

string

智能体 ID

`type`

string

固定为 `agent`

`version`

int

新版本号（自动递增）；已绑定旧版本的会话不受影响

`name` / `description` / `system`

string

请求体覆盖后的新值

`model` / `tools` / `mcp_servers` / `skills` / `multiagent` / `metadata`

object / array

请求体覆盖后的新值，缺省字段为空

`archived_at`

string / null

归档时间，未归档时为 `null`

`created_at` / `updated_at`

string

创建 / 最近更新时间

`workspace_id`

string

所属工作空间 ID

`request_id`

string

本次请求的唯一标识
