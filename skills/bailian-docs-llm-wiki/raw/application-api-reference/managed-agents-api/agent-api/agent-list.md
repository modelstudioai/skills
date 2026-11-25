# 列出 Agent

分页列出当前工作空间下的智能体，按 created\_at 倒序返回。默认不包含已归档项，传 include\_archived=true 可包含。

<a id="前提"></a>

<a id="h-list-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-list-endpoint"></a>

## 接口

**GET** `/agents`

<table><tbody><tr><td><a id="h-list-query"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>int</code> <strong>（可选）</strong></p><p>单页条数，默认 20，最大 100</p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标。首次不传，后续传上一次响应的 <code>next_page</code> 翻下一页</p><p><strong>include_archived</strong> <code>bool</code> <strong>（可选）</strong></p><p>是否包含已归档智能体，默认 <code>false</code></p></td><td><a id="h-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/agents?limit=20&amp;include_archived=true&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for agent in client.agents.list(limit=20, include_archived=True):
    print(agent.id, agent.name, agent.model['id'])
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;Agent&gt; page = client.agents().list(AgentListParam.builder()
    .limit(20).includeArchived(true).build());
for (Agent a : page.getData()) System.out.println(a.getId() + &quot; &quot; + a.getName());
</code></pre></div></div></td></tr></tbody></table>

|  |  |
| --- | --- |
| <a id="h-list-dto"></a><br><br>### Agent 对象字段<br><br>**id** `string`<br><br>智能体 ID，格式 `agent_&lt;ULID&gt;`<br><br>**type** `string`<br><br>固定为 `agent`<br><br>**version** `int`<br><br>当前版本号，每次更新自动递增<br><br>**name / description / system** `string`<br><br>智能体名称、用途说明、系统提示词<br><br>**model / tools / mcp\_servers / skills / multiagent / metadata** `object / array`<br><br>模型、工具包、MCP 引用、技能、多智能体协作配置、业务元数据<br><br>**archived\_at** `string / null`<br><br>归档时间，未归档时为 `null`<br><br>**created\_at / updated\_at** `string`<br><br>创建 / 最近更新时间，ISO 8601<br><br>**workspace\_id** `string`<br><br>所属工作空间 ID | <a id="h-list-resp"></a><br><br>## 响应说明<br><br>响应包含 `data`（Agent 对象数组）与 `next_page`（下一页游标，无更多数据时为 `null`）。每个 Agent 对象的字段同[创建 Agent](agent-create.md)响应，字段说明如下： |
