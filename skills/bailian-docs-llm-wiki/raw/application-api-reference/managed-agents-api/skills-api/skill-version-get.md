# 查询 Skill 版本

返回指定版本的元数据与扫描状态。仅 active 可挂载。

<a id="前提"></a>

<a id="h-skgv-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-skgv-endpoint"></a>

## 接口

**GET** `/skills/{skill_id}/versions/{version}`

<a id="请求示例"></a>

<a id="h-skgv-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/skills/skill_xxx/versions/1.0" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
sv = client.skills.versions.retrieve("skill_xxx", "1.0")
print(sv.version, sv.status)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
SkillVersion v = client.skills().retrieveVersion("skill_xxx", "1.0");
System.out.println(v.getVersion() + " " + v.getStatus());
```

<table><tbody><tr><td><a id="h-skgv-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>版本 ID，格式 <code>skillver_xxx</code></p><p><strong>skill_id</strong> <code>string</code></p><p>所属技能 ID</p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>skill_version</code></p><p><strong>name / description</strong> <code>string</code></p><p>从该版本 zip 包内 <code>SKILL.md</code> 解析得到</p><p><strong>version</strong> <code>string</code></p><p>版本号，由服务端生成</p><p><strong>status</strong> <code>string</code></p><p>扫描状态：<code>checking</code> / <code>active</code> / <code>rejected</code>，仅 <code>active</code> 可挂载</p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>additional_properties</strong> <code>object</code></p><p>仅 <code>status=rejected</code> 时返回，含 <code>error_info</code>：按 zip 包内文件路径列出的安全审查问题</p></td><td><a id="h-skgv-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;skillver_xxx&quot;,
  &quot;skill_id&quot;: &quot;skill_xxx&quot;,
  &quot;type&quot;: &quot;skill_version&quot;,
  &quot;name&quot;: &quot;pdf3.0&quot;,
  &quot;description&quot;: &quot;从 SKILL.md 解析的描述&quot;,
  &quot;version&quot;: &quot;1.0&quot;,
  &quot;status&quot;: &quot;active&quot;,
  &quot;created_at&quot;: &quot;2026-06-16T07:56:03+00:00&quot;,
  &quot;updated_at&quot;: &quot;2026-06-16T07:57:42+00:00&quot;
}
</code></pre></td></tr></tbody></table>
