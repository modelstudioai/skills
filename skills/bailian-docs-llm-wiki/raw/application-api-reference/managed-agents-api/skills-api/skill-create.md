# 创建 Skill

从已上传的 zip 包创建技能。请求体仅含 file\_id，name 与 description 由服务端从 zip 包内的 SKILL.md 解析得到。新建技能进入 checking，扫描通过后变为 active，仅 active 可挂载到智能体；命中安全风险变为 rejected。

<a id="前提"></a>

<a id="h-skc-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。创建技能前需先用[File](../files-api.md)上传 zip 包获得 `file_id`。zip 包根目录须包含 `SKILL.md`，声明技能名称与描述。

<a id="接口"></a>

<a id="h-skc-endpoint"></a>

## 接口

**POST** `/skills`

请求体仅含 `file_id`，对应文件须为 `.zip` 且通过审核。`name` 与 `description` 由服务端从 zip 包内的 `SKILL.md` 解析得到。

<a id="请求示例"></a>

<a id="h-skc-eg"></a>

## 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-curl-tab"></a>

curl

<a id="code-code-group-curl"></a>

```bash
curl -X POST "$AGENTSTUDIO_URL/skills" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "file_xxx"}'
```

<a id="fig-code-group-python-tab"></a>

Python

<a id="code-code-group-python"></a>

```python
skill = client.skills.create(file_id="file_xxx")
print(skill.id)
```

<a id="fig-code-group-java-tab"></a>

Java

<a id="code-code-group-java"></a>

```java
Skill skill = client.skills().create(SkillCreateParam.builder()
    .fileId("file_xxx").build());
System.out.println(skill.getId());
```

<table><tbody><tr><td><a id="h-skc-dto"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>技能 ID，格式 <code>skill_xxx</code></p><p><strong>type</strong> <code>string</code></p><p>固定为 <code>skill</code></p><p><strong>name / description</strong> <code>string</code></p><p>从 zip 包内 <code>SKILL.md</code> 解析得到</p><p><strong>source</strong> <code>string</code></p><p>来源：<code>customer</code>（自建） / <code>official</code>（阿里云百炼官方）</p><p><strong>status</strong> <code>string</code></p><p>扫描状态：<code>checking</code> / <code>active</code> / <code>rejected</code> / <code>deleted</code>，仅 <code>active</code> 可挂载</p><p><strong>latest_version</strong> <code>string</code></p><p>最新版本号，挂载到智能体时不能锁定到 <code>latest</code>，必须指定具体版本号</p><p><strong>created_at / updated_at</strong> <code>string</code></p><p>创建 / 最近更新时间，ISO 8601</p><p><strong>request_id</strong> <code>string</code></p><p>本次请求的唯一标识</p></td><td><a id="h-skc-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;skill_xxx&quot;,
  &quot;type&quot;: &quot;skill&quot;,
  &quot;name&quot;: &quot;pdf3.0&quot;,
  &quot;description&quot;: &quot;Use this skill whenever the user wants to do anything with PDF files...&quot;,
  &quot;source&quot;: &quot;customer&quot;,
  &quot;status&quot;: &quot;checking&quot;,
  &quot;latest_version&quot;: &quot;1.0&quot;,
  &quot;created_at&quot;: &quot;2026-06-16T07:56:03Z&quot;,
  &quot;updated_at&quot;: &quot;2026-06-16T07:56:03Z&quot;,
  &quot;request_id&quot;: &quot;xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="扫描状态"></a>

<a id="h-skc-status"></a>

## 扫描状态

新建技能或上传新版本进入 `checking` 状态，扫描通过后变为 `active` 才可挂载到智能体；命中安全风险变为 `rejected`，不能挂载，可根据版本信息获取具体错误原因。删除后状态为 `deleted`。
