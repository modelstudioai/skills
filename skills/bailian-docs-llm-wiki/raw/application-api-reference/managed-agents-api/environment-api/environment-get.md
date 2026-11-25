# 获取 Environment

根据环境 ID 返回完整配置，包括沙箱类型、预装依赖与网络策略。

<a id="前提"></a>

<a id="h-eg-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-eg-endpoint"></a>

## 接口

**GET** `/environments/{environment_id}`

<a id="请求示例"></a>

<a id="h-eg-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/environments/env_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
env = client.environments.retrieve("env_xxx")
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
Environment env = client.environments().retrieve("env_xxx");
```

<table><tbody><tr><td><a id="h-eg-dto"></a><h3>响应字段</h3><p>响应为 Environment 对象。字段如下：</p><p><strong>id</strong> <code>string</code></p><p>环境 ID，格式 <code>env_&amp;lt;ULID&amp;gt;</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>environment</code></p><p><strong>name / description / scope / config / metadata</strong> <code>string / object</code></p><p>环境基础属性与完整运行时配置（沙箱类型、预装依赖、网络策略）</p><p><strong>archived_at</strong> <code>string / null</code></p><p>归档时间，未归档时为 <code>null</code></p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-eg-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
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
  &quot;updated_at&quot;: &quot;2026-06-16T12:45:34+08:00&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
