# 归档 Agent

软归档：智能体保留但默认不出现在列表中（除非 include\_archived=true），且不可用于新建会话；已有会话不受影响。响应返回完整 Agent 对象，archived\_at 字段被填入归档时间。

<a id="前提"></a>

<a id="h-arc-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-arc-endpoint"></a>

## 接口

**POST** `/agents/{agent_id}/archive`

<a id="语义"></a>

<a id="h-arc-semantic"></a>

## 语义

软归档：响应返回完整 agent 对象，`archived_at` 字段被填入归档时间。归档后默认不出现在列表中（除非 `include_archived=true`），不可用于新建会话，已有会话不受影响。

<a id="请求示例"></a>

<a id="h-arc-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/agents/agent_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
client.agents.archive("agent_xxx")
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
client.agents().archive("agent_xxx");
```

|  |  |
| --- | --- |
| <a id="h-arc-dto"></a><br><br>### 响应字段<br><br>响应为 Agent 对象，结构同[创建 Agent](agent-create.md)响应，唯一差异是 `archived_at` 字段被填入归档时间（不再为 `null`）。字段如下：<br><br>**id** `string`<br><br>智能体 ID<br><br>**type** `string`<br><br>固定为 `agent`<br><br>**version** `int`<br><br>当前版本号（归档不改变版本）<br><br>**name / description / system** `string`<br><br>智能体名称、用途说明、系统提示词<br><br>**model / tools / mcp\_servers / skills / multiagent / metadata** `object / array`<br><br>模型、工具包、MCP 引用、技能、多智能体协作配置、业务元数据<br><br>**archived\_at** `string`<br><br>归档时间，ISO 8601；归档接口返回的对象中该字段一定非空<br><br>**created\_at / updated\_at** `string`<br><br>创建 / 最近更新时间<br><br>**workspace\_id** `string`<br><br>所属工作空间 ID<br><br>**request\_id** `string`<br><br>本次请求的唯一标识 | <a id="h-arc-resp"></a><br><br>## 响应说明 |
