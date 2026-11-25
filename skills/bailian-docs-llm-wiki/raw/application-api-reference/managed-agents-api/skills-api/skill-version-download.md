# 下载 Skill 包

返回 OSS 预签名 URL（file\_url），有效期 2 小时，可直接 GET 该 URL 拿到 zip 包内容。

<a id="前提"></a>

<a id="h-skdl-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-skdl-endpoint"></a>

## 接口

**GET** `/skills/{skill_id}/versions/{version}/content`

<a id="请求示例"></a>

<a id="h-skdl-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/skills/skill_xxx/versions/1.0/content" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
content = client.skills.versions.download("skill_xxx", "1.0")
print(content["file_url"])
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
JsonObject content = client.skills().downloadVersion("skill_xxx", "1.0");
System.out.println(content.get("file_url").getAsString());
```

<table><tbody><tr><td><h3>响应字段</h3><p><strong>skill_id</strong> <code>string</code></p><p>所属技能 ID</p><p><strong>version</strong> <code>string</code></p><p>版本号</p><p><strong>file_url</strong> <code>string</code></p><p>OSS 预签名下载 URL，有效期 2 小时</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-skdl-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;skill_id&quot;: &quot;skill_xxx&quot;,
  &quot;version&quot;: &quot;1.0&quot;,
  &quot;file_url&quot;: &quot;https://&lt;oss-bucket&gt;.oss-cn-xxx.aliyuncs.com/...?Expires=...&amp;Signature=YOUR_SIGNATURE&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
