# 获取 Agent

根据智能体 ID 返回完整配置。默认返回最新版本，可通过 version 参数指定历史版本。

<a id="前提"></a>

<a id="h-get-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-get-endpoint"></a>

## 接口

**GET** `/agents/{agent_id}`

<table><tbody><tr><td><a id="h-get-query"></a><h2>Query 参数</h2><p><strong>version</strong> <code>int</code> <strong>（可选）</strong></p><p>指定要查询的版本号；不传则返回最新版本</p></td><td><a id="h-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code># 默认返回最新版本
curl &quot;$AGENTSTUDIO_URL/agents/agent_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;

# 指定版本
curl &quot;$AGENTSTUDIO_URL/agents/agent_xxx?version=3&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code># 默认返回最新版本
agent = client.agents.retrieve(&quot;agent_xxx&quot;)

# 指定版本
agent = client.agents.retrieve(&quot;agent_xxx&quot;, version=3)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>// 默认返回最新版本
Agent agent = client.agents().retrieve(&quot;agent_xxx&quot;);

// 指定版本
Agent agentV2 = client.agents().retrieve(&quot;agent_xxx&quot;, 2);
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-get-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>智能体 ID，格式 <code>agent_&amp;lt;ULID&amp;gt;</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>agent</code></p><p><strong>version</strong> <code>int</code></p><p>当前版本号，每次更新自动递增；会话创建时锁定该值</p><p><strong>name / description / system</strong> <code>string</code></p><p>智能体名称、用途说明、系统提示词</p><p><strong>model / tools / mcp_servers / skills / multiagent / metadata</strong> <code>object / array</code></p><p>模型、工具包、MCP 引用、技能、多智能体协作配置、业务元数据，结构同创建时</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>workspace_id</strong> <code>string</code></p><p>所属工作空间 ID</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;agent_xxx&quot;,
  &quot;type&quot;: &quot;agent&quot;,
  &quot;version&quot;: 1,
  &quot;name&quot;: &quot;data-analyst&quot;,
  &quot;description&quot;: &quot;数据分析助手&quot;,
  &quot;model&quot;: {&quot;id&quot;: &quot;qwen3.7-max&quot;},
  &quot;system&quot;: &quot;你是数据分析专家，使用 pandas 处理 CSV 文件。&quot;,
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
  &quot;metadata&quot;: {&quot;team&quot;: &quot;data&quot;},
  &quot;created_at&quot;: &quot;2026-05-28T16:23:11.456+08:00&quot;,
  &quot;updated_at&quot;: &quot;2026-05-28T16:23:11.456+08:00&quot;,
  &quot;archived_at&quot;: null,
  &quot;workspace_id&quot;: &quot;ws_xxx&quot;,
  &quot;request_id&quot;: &quot;req_xxx&quot;
}
</code></pre></td></tr></tbody></table>
