# 列出 Environment

分页列出当前工作空间下的运行环境，按 created\_at 倒序返回。默认不包含已归档项。

<a id="前提"></a>

<a id="h-el-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-el-endpoint"></a>

## 接口

**GET** `/environments`

<table><tbody><tr><td><a id="h-el-q"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>int</code> 默认 20</p><p>每页数量，最大 100</p><p><strong>page</strong> <code>string</code> 默认 —</p><p>首次不传，后续传上一次响应的 <code>next_page</code></p><p><strong>include_archived</strong> <code>bool</code> 默认 false</p><p>是否包含已归档环境</p></td><td><a id="h-el-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/environments?limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for env in client.environments.list(include_archived=False, limit=20):
    print(env.id, env.name)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;Environment&gt; page = client.environments().list(EnvironmentListParam.builder()
    .includeArchived(false)
    .limit(20)
    .build());
for (Environment e : page.getData()) System.out.println(e.getId() + &quot; &quot; + e.getName());
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-el-dto"></a><h3>Environment 对象字段</h3><p>响应顶层包含 <code>data</code>（Environment 对象数组）、<code>next_page</code>（下一页游标）与 <code>request_id</code>（本次请求的唯一标识）。Environment 对象字段如下：</p><p><strong>id</strong> <code>string</code></p><p>环境 ID，格式 <code>env_&amp;lt;ULID&amp;gt;</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>environment</code></p><p><strong>name / description / scope / config / metadata</strong> <code>string / object</code></p><p>环境基础属性与完整运行时配置（沙箱类型、预装依赖、网络策略）</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p></td><td><a id="h-el-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;data&quot;: [
    {
      &quot;id&quot;: &quot;env_xxx&quot;,
      &quot;type&quot;: &quot;environment&quot;,
      &quot;name&quot;: &quot;data-sandbox&quot;,
      &quot;description&quot;: &quot;数据分析沙箱&quot;,
      &quot;config&quot;: {
        &quot;type&quot;: &quot;cloud&quot;,
        &quot;packages&quot;: {&quot;apt&quot;: [&quot;ffmpeg&quot;], &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;matplotlib&quot;]},
        &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;}
      },
      &quot;metadata&quot;: {&quot;team&quot;: &quot;infra&quot;},
      &quot;scope&quot;: &quot;organization&quot;,
      &quot;archived_at&quot;: null,
      &quot;created_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;,
      &quot;updated_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;
    }
  ],
  &quot;next_page&quot;: &quot;xxx&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
