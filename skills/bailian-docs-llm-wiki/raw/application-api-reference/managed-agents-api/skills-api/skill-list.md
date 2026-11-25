# 列出 Skill

cursor 分页列出技能，按 created\_at 倒序。支持按来源过滤（自建或阿里云百炼官方）。仅 active 状态可挂载到智能体。

<a id="前提"></a>

<a id="h-skl-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-skl-endpoint"></a>

## 接口

**GET** `/skills`

<table><tbody><tr><td><a id="h-skl-q"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>int</code> 默认 20</p><p>每页数量，最大 100</p><p><strong>page</strong> <code>string</code> 默认 —</p><p>首次不传，后续传上一次响应的 <code>next_page</code></p><p><strong>source</strong> <code>string</code> 默认 <code>customer</code></p><p>来源筛选：<code>customer</code>（自建）或 <code>official</code>（阿里云百炼官方）</p></td><td><a id="h-skl-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/skills?source=customer&amp;limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for skill in client.skills.list(source=&quot;customer&quot;, limit=20):
    print(skill.id, skill.name)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;Skill&gt; page = client.skills().list(SkillListParam.builder()
    .source(&quot;customer&quot;).limit(20).build());
for (Skill s : page.getData()) System.out.println(s.getId() + &quot; &quot; + s.getName());
</code></pre></div></div></td></tr></tbody></table>

<a id="响应示例"></a>

<a id="h-skl-resp"></a>

## 响应示例

<a id="code-block"></a>

```json
{
  "data": [
    {
      "id": "skill_xxx",
      "type": "skill",
      "name": "pdf3.0",
      "description": "Use this skill whenever the user wants to do anything with PDF files...",
      "source": "customer",
      "status": "active",
      "latest_version": "1.1",
      "created_at": "2026-06-16T07:56:03+00:00",
      "updated_at": "2026-06-16T08:12:47+00:00"
    }
  ],
  "next_page": "skill_xxx",
  "request_id": "xxx"
}
```

响应包含 `data`（Skill 对象数组）与 `next_page`。Skill 对象字段如下：

<a id="skill-对象字段"></a>

<a id="h-skl-dto"></a>

### Skill 对象字段

**id** `string`

技能 ID，格式 `skill_xxx`

**type** `string`

固定为 `skill`

**name / description** `string`

从 zip 包内 `SKILL.md` 解析得到

**source** `string`

来源：`customer`（自建） / `official`（阿里云百炼官方）

**status** `string`

扫描状态：`checking` / `active` / `rejected` / `deleted`，仅 `active` 可挂载

**latest\_version** `string`

最新版本号，挂载到智能体时不能锁定到 `latest`，必须指定具体版本号

**created\_at / updated\_at** `string`

创建 / 最近更新时间，ISO 8601
