# 归档 Environment

软归档：环境保留但默认不出现在列表中（除非 include\_archived=true），仍可被 GET 查询。已绑定的会话继续可用。响应返回完整 Environment 对象，archived\_at 字段被填入归档时间。

<a id="前提"></a>

<a id="h-ea-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-ea-endpoint"></a>

## 接口

**POST** `/environments/{environment_id}/archive`

<a id="语义"></a>

<a id="h-ea-semantic"></a>

## 语义

软归档：响应返回完整 environment 对象，`archived_at` 字段被填入归档时间。归档后默认不出现在列表中（除非 `include_archived=true`），仍可被 `GET` 查询。已绑定的会话继续可用。

<a id="请求示例"></a>

<a id="h-ea-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/environments/env_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
client.environments.archive("env_xxx")
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
client.environments().archive("env_xxx");
```

<table><tbody><tr><td><a id="h-ea-dto"></a><h3>响应字段</h3><p>响应为 Environment 对象，<code>archived_at</code> 已填入归档时间。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>环境 ID</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>environment</code></p><p><strong>name / description / scope / config / metadata</strong> <code>string / object</code></p><p>环境基础属性与完整运行时配置</p><p><strong>archived_at</strong> <code>string</code></p><p>归档时间，ISO 8601；归档接口返回的对象中该字段一定非空</p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间</p><p><strong>requestId</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-ea-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
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
  &quot;archived_at&quot;: &quot;2026-06-16T13:47:18+08:00&quot;,
  &quot;created_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;,
  &quot;updated_at&quot;: &quot;2026-06-16T13:47:18+08:00&quot;,
  &quot;requestId&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
