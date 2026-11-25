# 列出 Agent 版本

分页列出某智能体的全部历史版本，按版本号倒序返回。会话创建时锁定当时 version，会话详情中也会嵌入该版本的完整智能体快照。

<a id="前提"></a>

<a id="h-ver-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-ver-endpoint"></a>

## 接口

**GET** `/agents/{agent_id}/versions`

<table><tbody><tr><td><a id="h-ver-query"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>int</code> <strong>（可选）</strong></p><p>单页条数，默认 20，最大 100</p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标。首次不传，后续传上一次响应的 <code>next_page</code> 翻下一页</p></td><td><a id="h-ver-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/agents/agent_xxx/versions&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for version in client.agents.list_versions(&quot;agent_xxx&quot;, limit=10):
    print(version.version, version.created_at)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;AgentVersion&gt; versions = client.agents().listVersions(
    &quot;agent_xxx&quot;, AgentListParam.builder().limit(10).build());
</code></pre></div></div></td></tr></tbody></table>

|  |  |
| --- | --- |
| <a id="h-ver-dto"></a><br><br>### Agent 对象字段<br><br>**id** `string`<br><br>智能体 ID（所有版本相同）<br><br>**type** `string`<br><br>固定为 `agent`<br><br>**version** `int`<br><br>该版本号；按版本号倒序返回<br><br>**name / description / system** `string`<br><br>该版本快照中的名称、用途说明、系统提示词<br><br>**model / tools / mcp\_servers / skills / multiagent / metadata** `object / array`<br><br>该版本快照中的模型、工具包、MCP 引用、技能、多智能体协作配置、业务元数据<br><br>**archived\_at** `string / null`<br><br>归档时间，未归档时为 `null`<br><br>**created\_at / updated\_at** `string`<br><br>该版本的创建 / 更新时间<br><br>**workspace\_id** `string`<br><br>所属工作空间 ID | <a id="h-ver-resp"></a><br><br>## 响应说明<br><br>响应包含 `data`（Agent 对象数组，每项为一个历史版本快照，按版本号倒序排列）、`next_page`（下一页游标，无更多数据时为 `null`）与 `request_id`。每个 Agent 对象的字段同[创建 Agent](agent-create.md)响应，字段说明如下： |
