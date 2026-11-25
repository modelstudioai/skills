# 更新 Agent

采用全量替换语义：请求体须包含 version（当前版本号，用于乐观锁）以及完整的智能体配置，缺省的字段视为清空。若 version 与服务端不一致返回 409 冲突；成功后 version 自动递增，已绑定旧版本的会话不受影响。

<a id="前提"></a>

<a id="h-update-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-update-endpoint"></a>

## 接口

**POST** `/agents/{agent_id}`

<a id="语义"></a>

<a id="h-update-semantic"></a>

## 语义

采用**全量替换**：请求体须包含 `version`（当前版本号，用于乐观锁）以及完整的 `name`、`model`、`system`、`tools` 等字段，缺省的字段视为清空。成功后响应中 `version` 自动递增；已绑定旧版本的会话不受影响。

<table><tbody><tr><td><a id="h-update-req"></a><h2>请求体</h2><p><strong>version</strong> <code>int</code> <strong>（必选）</strong></p><p>当前版本号，用于乐观锁。若与服务端不一致返回 409 冲突</p><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>智能体名称，缺省视为清空</p><p><strong>model</strong> <code>object</code> <strong>（必选）</strong></p><p>模型配置，结构 <code>{&quot;id&quot;: &quot;qwen3.7-max&quot;}</code>，必填子字段 <code>id</code></p><p><strong>description</strong> <code>string</code> <strong>（可选）</strong></p><p>智能体用途说明，缺省视为清空</p><p><strong>system</strong> <code>string</code> <strong>（可选）</strong></p><p>系统提示词，缺省视为清空</p><p><strong>tools</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>工具包列表，含义同创建，缺省视为清空。<code>builtin_toolkit</code> 至多一项，<code>mcp_toolkit</code> 可多项</p><p><strong>mcp_servers</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>MCP Server 引用列表，含义同创建，缺省视为清空</p><p><strong>skills</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>挂载的技能列表，含义同创建，缺省视为清空</p><p><strong>multiagent</strong> <code>object</code> <strong>（可选）</strong></p><p>多智能体协作配置，含义同创建，缺省视为清空</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值，缺省视为清空</p><p>各字段结构详见<a href="agent-create.md">创建 Agent</a>的<strong>请求体</strong>一节。</p></td><td><a id="h-update-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/agents/agent_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;version&quot;: 1,
    &quot;name&quot;: &quot;data-analyst&quot;,
    &quot;description&quot;: &quot;数据分析助手&quot;,
    &quot;model&quot;: {&quot;id&quot;: &quot;qwen3.7-max&quot;},
    &quot;system&quot;: &quot;你是资深数据分析师，输出结论时附带置信度。&quot;,
    &quot;tools&quot;: [],
    &quot;mcp_servers&quot;: [],
    &quot;skills&quot;: [],
    &quot;multiagent&quot;: {
      &quot;type&quot;: &quot;coordinator&quot;,
      &quot;agents&quot;: [
        {&quot;type&quot;: &quot;self&quot;},
        {&quot;type&quot;: &quot;agent&quot;, &quot;id&quot;: &quot;agent_researcher&quot;, &quot;version&quot;: 3}
      ]
    },
    &quot;metadata&quot;: {&quot;team&quot;: &quot;data&quot;}
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>current = client.agents.retrieve(&quot;agent_xxx&quot;)
agent = client.agents.update(
    &quot;agent_xxx&quot;,
    version=current.version,
    name=&quot;data-analyst&quot;,
    model=&quot;qwen3.8-max&quot;,
    description=&quot;数据分析助手&quot;,
    system_prompt=&quot;你是资深数据分析师，输出结论时附带置信度。&quot;,
    tools=[],
    mcp_servers=[],
    skills=[],
    metadata={&quot;team&quot;: &quot;data&quot;},
)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>Agent current = client.agents().retrieve(&quot;agent_xxx&quot;);
Agent updated = client.agents().update(&quot;agent_xxx&quot;, AgentUpdateParam.builder()
    .version(current.getVersion())
    .name(&quot;data-analyst&quot;)
    .model(&quot;qwen3.7-max&quot;)
    .description(&quot;数据分析助手&quot;)
    .instructions(&quot;你是资深数据分析师，输出结论时附带置信度。&quot;)
    .metadata(Map.of(&quot;team&quot;, &quot;data&quot;))
    .build());
</code></pre></div></div></td></tr></tbody></table>

|  |  |
| --- | --- |
| <a id="h-update-dto"></a><br><br>### 响应字段<br><br>响应为更新后的 Agent 对象，结构同[创建 Agent](agent-create.md)响应，`version` 自动递增。字段如下：<br><br>**id** `string`<br><br>智能体 ID<br><br>**type** `string`<br><br>固定为 `agent`<br><br>**version** `int`<br><br>新版本号（自动递增）；已绑定旧版本的会话不受影响<br><br>**name / description / system** `string`<br><br>请求体覆盖后的新值<br><br>**model / tools / mcp\_servers / skills / multiagent / metadata** `object / array`<br><br>请求体覆盖后的新值，缺省字段为空<br><br>**archived\_at** `string / null`<br><br>归档时间，未归档时为 `null`<br><br>**created\_at / updated\_at** `string`<br><br>创建 / 最近更新时间<br><br>**workspace\_id** `string`<br><br>所属工作空间 ID<br><br>**request\_id** `string`<br><br>本次请求的唯一标识 | <a id="h-update-resp"></a><br><br>## 响应说明 |
