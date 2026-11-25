# 归档 Session

归档会话：status 置为 terminated 终态，archived\_at 填入归档时间，事件历史仍可查询。

<a id="前提"></a>

<a id="h-sa-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-sa-endpoint"></a>

## 接口

**POST** `/sessions/{session_id}/archive`

<a id="请求示例"></a>

<a id="h-sa-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/sessions/sesn_xxx/archive" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
client.sessions.archive("sesn_xxx")
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
client.sessions().archive("sesn_xxx");
```

<table><tbody><tr><td><a id="h-sa-dto"></a><h3>响应字段</h3><p>响应为 Session 对象。字段如下：</p><strong>id</strong><code>string</code><p>会话 ID</p><strong>type</strong><code>string</code><p>固定为 <code>session</code></p><strong>status</strong><code>string</code><p>归档后置为 <code>terminated</code>（终态）</p><strong>agent</strong><code>object</code><p>智能体配置快照</p><strong>environment_id</strong><code>string</code><p>绑定的运行环境 ID</p><strong>title / metadata</strong><code>string / object</code><p>会话标题、业务元数据</p><strong>archived_at</strong><code>string</code><p>归档时间，ISO 8601；归档接口返回的对象中该字段一定非空</p><strong>created_at / updated_at</strong><code>string</code><p>创建 / 最近更新时间</p><strong>request_id</strong><code>string</code><p>本次请求的唯一标识</p></td><td><a id="h-sa-resp"></a><h2>响应示例</h2><p>返回完整 session 对象，<code>status</code> 置为 <code>terminated</code>，<code>archived_at</code> 被填入归档时间。</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;sesn_xxx&quot;,
  &quot;type&quot;: &quot;session&quot;,
  &quot;status&quot;: &quot;terminated&quot;,
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
  &quot;archived_at&quot;: &quot;2026-05-28T11:00:00Z&quot;,
  &quot;created_at&quot;: &quot;2026-05-28T08:23:11Z&quot;,
  &quot;updated_at&quot;: &quot;2026-05-28T11:00:00Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
