# 删除 Session

硬删除：会话元数据、事件历史、内部拷贝的资源一并清除，不可恢复。若需保留事件历史请改用归档接口。

<a id="前提"></a>

<a id="h-sd-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-sd-endpoint"></a>

## 接口

**DELETE** `/sessions/{session_id}`

<a id="请求示例"></a>

<a id="h-sd-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X DELETE "$AGENTSTUDIO_URL/sessions/sesn_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
client.sessions.delete("sesn_xxx")
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
client.sessions().delete("sesn_xxx");
```

<table><tbody><tr><td><a id="h-sd-dto"></a><h3>响应字段</h3><strong>id</strong><code>string</code><p>被删除的会话 ID</p><strong>type</strong><code>string</code><p>固定为 <code>session_deleted</code>，标识删除成功</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p></td><td><a id="h-sd-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesn_xxx&quot;,
  &quot;type&quot;: &quot;session_deleted&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
