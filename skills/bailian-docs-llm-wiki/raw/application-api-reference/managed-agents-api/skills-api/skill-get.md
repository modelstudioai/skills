# 查询 Skill

返回技能元数据与最新版本号。响应结构与创建技能一致。仅 active 状态可挂载到智能体，挂载时不能锁定到 latest，必须指定具体版本号。

<a id="前提"></a>

<a id="h-skg-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-skg-endpoint"></a>

## 接口

**GET** `/skills/{skill_id}`

<a id="请求示例"></a>

<a id="h-skg-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl "$AGENTSTUDIO_URL/skills/skill_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
skill = client.skills.retrieve("skill_xxx")
print(skill.name, skill.latest_version)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
Skill s = client.skills().retrieve("skill_xxx");
System.out.println(s.getName() + " " + s.getLatestVersion());
```

<table><tbody><tr><td><a id="h-skg-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>技能 ID，格式 <code>skill_xxx</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>skill</code></p><p><strong>name / description</strong> <code>string</code></p><p>从 zip 包内 <code>SKILL.md</code> 解析得到</p><p><strong>source</strong> <code>string</code></p><p>来源：<code>customer</code>（自建） / <code>official</code>（阿里云百炼官方）</p><p><strong>status</strong> <code>string</code></p><p>扫描状态：<code>checking</code> / <code>active</code> / <code>rejected</code> / <code>deleted</code>，仅 <code>active</code> 可挂载</p><p><strong>latest_version</strong> <code>string</code></p><p>最新版本号，挂载到智能体时不能锁定到 <code>latest</code>，必须指定具体版本号</p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-skg-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;skill_xxx&quot;,
  &quot;type&quot;: &quot;skill&quot;,
  &quot;name&quot;: &quot;pdf3.0&quot;,
  &quot;description&quot;: &quot;Use this skill whenever the user wants to do anything with PDF files...&quot;,
  &quot;source&quot;: &quot;customer&quot;,
  &quot;status&quot;: &quot;active&quot;,
  &quot;latest_version&quot;: &quot;1.1&quot;,
  &quot;created_at&quot;: &quot;2026-06-16T07:56:03Z&quot;,
  &quot;updated_at&quot;: &quot;2026-06-16T08:12:47Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>
