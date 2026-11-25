# 更新 Environment

采用部分更新语义：传入的字段会被更新，未传字段保留原值。运行中会话使用绑定时的快照，不受影响；新会话使用更新后的环境。config.type 不可变，传入异于原值将报错；config.packages 与 metadata 传入即整体替换原值。

<a id="前提"></a>

<a id="h-eu-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-eu-endpoint"></a>

## 接口

**POST** `/environments/{environment_id}`

<a id="语义"></a>

<a id="h-eu-semantic"></a>

## 语义

采用**部分更新**语义：请求体中传入的字段会被更新，未传字段保留原值。已绑定该环境的运行中会话使用绑定时的快照，不受更新影响；新会话使用更新后的环境。

-   `config.type` 不可变，传入异于原值将报错。
-   `config.packages` 传入即整体替换原值（含子键 `apt`、`pip` 等），未列出的包将被移除。
-   `metadata` 传入即整体替换原值，不做键级合并。

<table><tbody><tr><td><a id="h-eu-req"></a><h2>请求体</h2><p>字段同<a href="environment-create.md">创建 Environment</a>的<strong>请求体</strong>一节，仅传入需更新的字段。</p></td><td><a id="h-eu-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST &quot;$AGENTSTUDIO_URL/environments/env_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;data-sandbox&quot;,
    &quot;description&quot;: &quot;数据分析沙箱（更新）&quot;,
    &quot;scope&quot;: &quot;organization&quot;,
    &quot;metadata&quot;: {&quot;team&quot;: &quot;infra&quot;},
    &quot;config&quot;: {
      &quot;type&quot;: &quot;cloud&quot;,
      &quot;packages&quot;: {&quot;apt&quot;: [&quot;ffmpeg&quot;], &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;scikit-learn&quot;]},
      &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;}
    }
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>env = client.environments.update(
    &quot;env_xxx&quot;,
    name=&quot;data-sandbox&quot;,
    description=&quot;数据分析沙箱（更新）&quot;,
    config={
        &quot;type&quot;: &quot;cloud&quot;,
        &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;},
        &quot;packages&quot;: {&quot;apt&quot;: [&quot;ffmpeg&quot;], &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;scikit-learn&quot;]},
    },
    metadata={&quot;team&quot;: &quot;infra&quot;},
)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>Environment u = client.environments().update(&quot;env_xxx&quot;,
    EnvironmentUpdateParam.builder()
        .name(&quot;data-sandbox&quot;)
        .description(&quot;数据分析沙箱（更新）&quot;)
        .build());
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-eu-dto"></a><h3>响应字段</h3><p>响应为更新后的 Environment 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>环境 ID</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>environment</code></p><p><strong>name / description / scope / config / metadata</strong> <code>string / object</code></p><p>更新后的环境配置；未传入字段保留原值</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-eu-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;env_xxx&quot;,
  &quot;type&quot;: &quot;environment&quot;,
  &quot;name&quot;: &quot;data-sandbox&quot;,
  &quot;description&quot;: &quot;数据分析沙箱（更新）&quot;,
  &quot;config&quot;: {
    &quot;type&quot;: &quot;cloud&quot;,
    &quot;packages&quot;: {&quot;apt&quot;: [&quot;ffmpeg&quot;], &quot;pip&quot;: [&quot;pandas&quot;, &quot;numpy&quot;, &quot;scikit-learn&quot;]},
    &quot;networking&quot;: {&quot;type&quot;: &quot;unrestricted&quot;}
  },
  &quot;metadata&quot;: {&quot;team&quot;: &quot;infra&quot;},
  &quot;scope&quot;: &quot;organization&quot;,
  &quot;archived_at&quot;: null,
  &quot;created_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;,
  &quot;updated_at&quot;: &quot;2026-06-16T12:52:31+08:00&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
