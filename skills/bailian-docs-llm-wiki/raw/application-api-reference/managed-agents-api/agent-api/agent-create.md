# 创建 Agent

创建一个智能体。请求体包含模型、系统提示词、工具包与技能配置；响应返回完整的 Agent 对象，初始 version 为 1。

<a id="前提"></a>

<a id="h-create-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-create-endpoint"></a>

## 接口

**POST** `/agents`

<table><tbody><tr><td><a id="h-create-req"></a><h2>请求体</h2><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>智能体名称，用于在控制台与列表中辨识</p><p><strong>description</strong> <code>string</code> <strong>（可选）</strong></p><p>智能体用途说明</p><p><strong>model</strong> <code>object</code> <strong>（必选）</strong></p><p>模型配置。必填子字段 <code>id</code>（模型 ID，如 qwen3.7-max）；可选子字段 <code>enable_thinking</code>（bool，是否启用思考模式）、<code>max_tokens</code>（int32，最大生成长度）、<code>temperature</code>（double，温度参数，控制随机性）、<code>thinking_budget</code>（int32，思考预算长度）</p><p><strong>system</strong> <code>string</code> <strong>（可选）</strong></p><p>系统提示词，定义角色与行为约束</p><p><strong>tools</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>工具包列表，按类型分组。每项含 <code>type</code>（<code>builtin_toolkit</code> / <code>mcp_toolkit</code>）、<code>default_config</code>（含 <code>enabled</code> 与 <code>permission_policy</code>）、<code>configs</code>（逐工具配置，覆盖 <code>default_config</code>；单个工具配置支持 <code>params</code> 传工具专属参数），MCP 类还需 <code>mcp_server_name</code>。<code>builtin_toolkit</code> 至多一项，<code>mcp_toolkit</code> 可多项</p><p><strong>mcp_servers</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>MCP Server 引用列表，每项含 <code>type</code>（<code>official</code> / <code>customer</code>）与 <code>name</code>。<code>name</code> 可在百炼控制台 <strong>MCP 管理</strong>菜单的服务卡片上查看（自定义服务在创建时指定）</p><p><strong>skills</strong> <code>array&lt;object&gt;</code> <strong>（可选）</strong></p><p>挂载的技能列表，每项含 <code>type</code>（<code>official</code> / <code>customer</code>）、<code>skill_id</code> 与 <code>version</code>（必须锁定到具体版本号）。<code>skill_id</code> 在百炼控制台 <strong>技能管理</strong>菜单的技能详情页查看</p><p><strong>multiagent</strong> <code>object</code> <strong>（可选）</strong></p><p>多智能体协作配置。不传或为空表示单智能体；配置后该智能体作为 coordinator 编排编队成员。含 <code>type</code>（当前仅 <code>coordinator</code>）与 <code>agents</code>（编队条目列表，1-20 个，传空数组表示清空编队），每项含 <code>type</code>（<code>agent</code> 引用另一个 Agent / <code>self</code> coordinator 自身，编队中最多一个）、<code>id</code>（<code>type=agent</code> 时必填，最长 64 字符；<code>type=self</code> 时不可传）、<code>version</code>（<code>type=agent</code> 时可选，&gt;=1 不传取最新；<code>type=self</code> 时不可传）</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值，不影响模型行为</p><p><code>permission_policy.type</code> 取值 <code>always_allow</code>（直接执行） / <code>always_ask</code>（每次调用前暂停等待人工确认）。工具审批仅支持主智能体，不支持在子智能体中使用。MCP 工具的审批策略配置在 <code>tools[].type=mcp_toolkit</code> 项的 <code>default_config</code> / <code>configs</code> 中，不在 <code>mcp_servers[]</code> 中设置。</p><p><code>configs[].params</code> 与 <code>name</code>、<code>enabled</code>、<code>permission_policy</code> 同级，用于传入工具专属参数。启用 <code>search_knowledgebases</code> 时，必须提供非空的 <code>params.knowledge_application_id</code>，值为知识检索服务 ID，不是单个知识库 ID；缺少或为空时创建 Agent 返回 400。一个智能体最多配置一个该工具。</p></td><td><a id="h-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/agents&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;data-analyst&quot;,
    &quot;description&quot;: &quot;数据分析助手&quot;,
    &quot;model&quot;: {&quot;id&quot;: &quot;qwen3.7-max&quot;},
    &quot;system&quot;: &quot;你是数据分析专家，使用 pandas 处理 CSV 文件。&quot;,
    &quot;tools&quot;: [
      {
        &quot;type&quot;: &quot;builtin_toolkit&quot;,
        &quot;default_config&quot;: {&quot;enabled&quot;: true, &quot;permission_policy&quot;: {&quot;type&quot;: &quot;always_allow&quot;}},
        &quot;configs&quot;: [
          {&quot;name&quot;: &quot;bash&quot;, &quot;enabled&quot;: true, &quot;permission_policy&quot;: {&quot;type&quot;: &quot;always_ask&quot;}},
          {&quot;name&quot;: &quot;read&quot;, &quot;enabled&quot;: true},
          {&quot;name&quot;: &quot;write&quot;, &quot;enabled&quot;: true}
        ]
      }
    ],
    &quot;mcp_servers&quot;: [],
    &quot;skills&quot;: [
      {&quot;type&quot;: &quot;customer&quot;, &quot;skill_id&quot;: &quot;skill_xxx&quot;, &quot;version&quot;: &quot;1.0&quot;}
    ],
    &quot;multiagent&quot;: {
      &quot;type&quot;: &quot;coordinator&quot;,
      &quot;agents&quot;: [
        {&quot;type&quot;: &quot;self&quot;},
        {&quot;type&quot;: &quot;agent&quot;, &quot;id&quot;: &quot;agent_researcher&quot;, &quot;version&quot;: 3}
      ]
    },
    &quot;metadata&quot;: {&quot;team&quot;: &quot;data&quot;}
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>agent = client.agents.create(
    name=&quot;data-analyst&quot;,
    model=&quot;qwen3.8-max&quot;,
    description=&quot;数据分析助手&quot;,
    system_prompt=&quot;你是数据分析专家，使用 pandas 处理 CSV 文件。&quot;,
    tools=[
        {&quot;type&quot;: &quot;builtin_toolkit&quot;,
         &quot;default_config&quot;: {&quot;enabled&quot;: True},
         &quot;configs&quot;: [
             {&quot;name&quot;: &quot;bash&quot;, &quot;enabled&quot;: True},
             {&quot;name&quot;: &quot;read&quot;, &quot;enabled&quot;: True},
             {&quot;name&quot;: &quot;write&quot;, &quot;enabled&quot;: True},
         ]}
    ],
    mcp_servers=[],
    skills=[{&quot;type&quot;: &quot;customer&quot;, &quot;skill_id&quot;: &quot;skill_xxx&quot;, &quot;version&quot;: &quot;1.0&quot;}],
    metadata={&quot;team&quot;: &quot;data&quot;},
)
print(agent.id)       # &quot;agent_xxx&quot;
print(agent.version)  # 1
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>Agent agent = client.agents().create(AgentCreateParam.builder()
    .name(&quot;data-analyst&quot;)
    .model(&quot;qwen3.7-max&quot;)
    .description(&quot;数据分析助手&quot;)
    .instructions(&quot;你是数据分析专家，使用 pandas 处理 CSV 文件。&quot;)
    .metadata(Map.of(&quot;team&quot;, &quot;data&quot;))
    .build());
System.out.println(agent.getId());       // &quot;agent_xxx&quot;
System.out.println(agent.getVersion());  // 1
</code></pre></div></div><a id="h-create-knowledge"></a><h3>知识检索配置示例</h3><p>在 <code>builtin_toolkit.configs[]</code> 中启用 <code>search_knowledgebases</code>，并通过 <code>params.knowledge_application_id</code> 指定知识检索服务（ID 形如 <code>aid-...</code>）：</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;tools&quot;: [
    {
      &quot;type&quot;: &quot;builtin_toolkit&quot;,
      &quot;configs&quot;: [
        {
          &quot;name&quot;: &quot;search_knowledgebases&quot;,
          &quot;enabled&quot;: true,
          &quot;params&quot;: {
            &quot;knowledge_application_id&quot;: &quot;aid-xxxxxxxx&quot;
          }
        }
      ]
    }
  ]
}
</code></pre><p><code>search_knowledgebases</code> 未配置时不启用检索。模型按需调用，并结合多轮对话生成检索问题。使用前需先创建知识检索服务，详见<a href="../../../application-user-guide/agent-context/knowledge-base/service/rag-knowledge-retrieval.md">知识检索</a>。更新已有智能体时，保留其他仍在使用的工具配置。使用方式详见 <a href="../../../application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md#h-bt-knowledge">Agent 工具配置</a>。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-create-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>智能体 ID，格式 <code>agent_&amp;lt;ULID&amp;gt;</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>agent</code></p><p><strong>version</strong> <code>int</code></p><p>当前版本号，每次更新自动递增；会话创建时锁定该值</p><p><strong>name / description / system</strong> <code>string</code></p><p>同请求体</p><p><strong>model / tools / mcp_servers / skills / multiagent / metadata</strong> <code>object / array</code></p><p>同请求体</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>workspace_id</strong> <code>string</code></p><p>所属工作空间 ID</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识，排查问题时附带</p></td><td><a id="h-create-resp"></a><h2>响应示例</h2><a id="code-block-2"></a><pre class="language-json"><code>{
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
