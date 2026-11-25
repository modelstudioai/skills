# 列出 Session

分页列出会话，按 created\_at 倒序返回。支持按智能体、状态、创建时间范围过滤。

<a id="前提"></a>

<a id="h-sl-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-sl-endpoint"></a>

## 接口

**GET** `/sessions`

<table><tbody><tr><td><a id="h-sl-q"></a><h2>Query 参数</h2><strong>agent_id</strong><code>string</code>默认 —<p>按智能体过滤</p><strong>statuses[]</strong><code>string</code>默认 —<p>多状态过滤，可重复传入。如 <code>?statuses[]=idle&amp;statuses[]=running</code></p><strong>created_at[gte] / created_at[lte]</strong><code>string</code>默认 —<p>创建时间范围，ISO 8601</p><strong>limit</strong><code>int</code>默认 20<p>每页数量，最大 100</p><strong>page</strong><code>string</code>默认 —<p>首次不传，后续传上一次响应的 <code>next_page</code></p></td><td><a id="h-sl-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/sessions?agent_id=agent_xxx&amp;statuses[]=idle&amp;limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for session in client.sessions.list(
    limit=20,
    agent_id=&quot;agent_xxx&quot;,
    statuses=[&quot;idle&quot;],
):
    print(session.id, session.status, session.title)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;Session&gt; page = client.sessions().list(SessionListParam.builder()
    .limit(20)
    .agentId(&quot;agent_xxx&quot;)
    .statuses(Arrays.asList(&quot;idle&quot;))
    .build());
for (Session s : page.getData()) {
    System.out.println(s.getId() + &quot; &quot; + s.getStatus() + &quot; &quot; + s.getTitle());
}
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-sl-dto"></a><h3>Session 对象字段</h3><p>响应包含 <code>data</code>（Session 对象数组）与 <code>next_page</code>（下一页游标）。Session 对象字段如下：</p><strong>id</strong><code>string</code><p>会话 ID，格式 <code>sesn_&amp;lt;ULID&amp;gt;</code></p><strong>type</strong><code>string</code><p>固定为 <code>session</code></p><strong>status</strong><code>string</code><p>会话状态：<code>idle</code> / <code>running</code> / <code>terminated</code></p><strong>stop_reason</strong><code>object / null</code><p>会话回到 <code>idle</code> 的原因，判别联合。<code>null</code> / <code>{&quot;type&quot;:&quot;end_turn&quot;}</code> / <code>{&quot;type&quot;:&quot;retries_exhausted&quot;}</code> / <code>{&quot;type&quot;:&quot;requires_action&quot;,&quot;pending_batch_id&quot;:&quot;...&quot;,&quot;pending_call_ids&quot;:[...]}</code>。仅在 <code>status=idle</code> 时用于判断交互状态</p><strong>agent</strong><code>object</code><p>智能体配置快照，含 <code>id</code> / <code>version</code> / <code>name</code> / <code>model</code> / <code>system</code> / <code>tools</code> 等</p><strong>environment_id</strong><code>string</code><p>绑定的运行环境 ID</p><strong>title / metadata</strong><code>string / object</code><p>会话标题与业务自定义元数据</p><strong>archived_at</strong><code>string / null</code><p>归档时间，未归档时为 <code>null</code></p><strong>created_at / updated_at</strong><code>string</code><p>创建 / 最近更新时间，ISO 8601</p><strong>environment_variables</strong><code>object</code><p>会话运行时注入的环境变量，字符串键值对，沙箱代码中可直接按名读取</p></td><td><a id="h-sl-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;sesn_xxx&quot;,
      &quot;type&quot;: &quot;session&quot;,
      &quot;status&quot;: &quot;idle&quot;,
      &quot;stop_reason&quot;: null,
      &quot;agent&quot;: {
        &quot;id&quot;: &quot;agent_xxx&quot;,
        &quot;type&quot;: &quot;agent&quot;,
        &quot;version&quot;: 1,
        &quot;name&quot;: &quot;data-analyst&quot;,
        &quot;model&quot;: {&quot;id&quot;: &quot;qwen3.7-max&quot;},
        &quot;system&quot;: &quot;你是数据分析专家，使用 pandas 处理 CSV 文件。&quot;,
        &quot;tools&quot;: []
      },
      &quot;environment_id&quot;: &quot;env_xxx&quot;,
      &quot;title&quot;: &quot;Q3 销售数据分析&quot;,
      &quot;metadata&quot;: {&quot;biz_ticket_id&quot;: &quot;1234&quot;},
      &quot;archived_at&quot;: null,
      &quot;created_at&quot;: &quot;2026-05-28T08:23:11.456000Z&quot;,
      &quot;updated_at&quot;: &quot;2026-05-28T08:23:25.789000Z&quot;,
      &quot;environment_variables&quot;: {&quot;API_BASE_URL&quot;: &quot;https://api.example.com&quot;, &quot;LOG_LEVEL&quot;: &quot;info&quot;}
    }
  ],
  &quot;next_page&quot;: &quot;xxx&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
