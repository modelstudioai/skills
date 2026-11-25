# 创建 Environment

创建一个运行环境。请求体定义沙箱类型、预装依赖与网络策略；响应返回完整的 Environment 对象。

<a id="前提"></a>

<a id="h-ec-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-ec-endpoint"></a>

## 接口

**POST** `/environments`

<table><tbody><tr><td><a id="h-ec-req"></a><h2>请求体</h2><p><strong>name</strong> <code>string</code> <strong>（必选）</strong></p><p>工作空间内唯一标识</p><p><strong>description</strong> <code>string</code> <strong>（可选）</strong></p><p>环境用途说明</p><p><strong>scope</strong> <code>string</code> <strong>（可选）</strong></p><p>作用域。<code>organization</code>：工作空间全部成员可见与复用。默认 <code>organization</code></p><p><strong>config.type</strong> <code>string</code> <strong>（可选）</strong></p><p><code>cloud</code> 云端容器。创建后不可修改。未传入 <code>config</code> 时服务端默认补全为 <code>cloud</code></p><p><strong>config.packages</strong> <code>object</code> <strong>（可选）</strong></p><p>预装依赖，按包管理器分组。键为 <code>apt</code> / <code>pip</code> / <code>npm</code>，值为包名数组。安装可能需要预热时间，完成前环境不可被会话绑定</p><p><strong>config.networking</strong> <code>object</code> <strong>（可选）</strong></p><p>网络策略对象，结构 <code>{&quot;type&quot;: &quot;unrestricted&quot;}</code>，目前仅支持放行全部出站访问</p><p><strong>metadata</strong> <code>object</code> <strong>（可选）</strong></p><p>业务自定义键值，不影响运行行为</p></td><td><a id="h-ec-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/environments&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;data-sandbox&quot;,
    &quot;description&quot;: &quot;数据分析沙箱&quot;,
    &quot;scope&quot;: &quot;organization&quot;,
    &quot;metadata&quot;: {&quot;team&quot;: &quot;infra&quot;},
    &quot;config&quot;: {
      &quot;type&quot;: &quot;cloud&quot;,
      &quot;packages&quot;: {
        &quot;apt&quot;: [&quot;ffmpeg&quot;],
        &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;matplotlib&quot;]
      },
      &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;}
    }
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>env = client.environments.create(
    name=&quot;data-sandbox&quot;,
    config={
        &quot;type&quot;: &quot;cloud&quot;,
        &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;},
        &quot;packages&quot;: {
            &quot;apt&quot;: [&quot;ffmpeg&quot;],
            &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;matplotlib&quot;],
        },
    },
    description=&quot;数据分析沙箱&quot;,
    scope=&quot;organization&quot;,
    metadata={&quot;team&quot;: &quot;infra&quot;},
)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>Environment env = client.environments().create(EnvironmentCreateParam.builder()
    .name(&quot;data-sandbox&quot;)
    .description(&quot;数据分析沙箱&quot;)
    .build());
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-ec-dto"></a><h3>响应字段</h3><p>响应为 Environment 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>环境 ID，格式 <code>env_&lt;base64 编码字符串&gt;</code>，示例值 <code>env_N2M2OTc4NTY4ZjRkNDEwZT</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>environment</code></p><p><strong>name / description / scope / config / metadata</strong> <code>string / object</code></p><p>同请求体；<code>config</code> 为完整运行时配置（沙箱类型、预装依赖、网络策略）</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>requestId</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-ec-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;env_xxx&quot;,
  &quot;type&quot;: &quot;environment&quot;,
  &quot;name&quot;: &quot;data-sandbox&quot;,
  &quot;description&quot;: &quot;数据分析沙箱&quot;,
  &quot;scope&quot;: &quot;organization&quot;,
  &quot;config&quot;: {
    &quot;type&quot;: &quot;cloud&quot;,
    &quot;packages&quot;: {&quot;apt&quot;: [&quot;ffmpeg&quot;], &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;matplotlib&quot;]},
    &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;}
  },
  &quot;metadata&quot;: {&quot;team&quot;: &quot;infra&quot;},
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;,
  &quot;updated_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;,
  &quot;requestId&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
