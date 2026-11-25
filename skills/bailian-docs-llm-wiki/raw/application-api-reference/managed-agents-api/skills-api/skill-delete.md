# 删除 Skill

删除技能及全部版本，不可再挂载到新智能体。已挂载旧版本的智能体仍可正常使用，会话历史不受影响。

<a id="前提"></a>

<a id="h-skd-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-skd-endpoint"></a>

## 接口

**DELETE** `/skills/{skill_id}`

<a id="请求示例"></a>

<a id="h-skd-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X DELETE "$AGENTSTUDIO_URL/skills/skill_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
client.skills.delete("skill_xxx")
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
client.skills().delete("skill_xxx");
```

<table><tbody><tr><td><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>被删除的技能 ID</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>skill_deleted</code></p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-skd-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;skill_xxx&quot;,
  &quot;type&quot;: &quot;skill_deleted&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
