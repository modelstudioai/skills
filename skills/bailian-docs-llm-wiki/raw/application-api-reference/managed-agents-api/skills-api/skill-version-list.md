# 列出 Skill 版本

按版本号倒序返回技能的全部版本。status=rejected 的版本会附带 additional\_properties.error\_info，按文件路径列出安全审查问题。仅 active 可挂载。

<a id="前提"></a>

<a id="h-sklv-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-sklv-endpoint"></a>

## 接口

**GET** `/skills/{skill_id}/versions`

按版本号倒序返回。每项含 `version`、`status`、`created_at`。

<table><tbody><tr><td><a id="h-sklv-q"></a><h2>Query 参数</h2><p><strong>limit</strong> <code>int</code> 默认 20</p><p>每页数量，最大 100</p><p><strong>page</strong> <code>string</code> 默认 —</p><p>首次不传，后续传上一次响应的 <code>next_page</code></p></td><td><a id="h-sklv-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl &quot;$AGENTSTUDIO_URL/skills/skill_xxx/versions?limit=20&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>for sv in client.skills.versions.list(&quot;skill_xxx&quot;, limit=20):
    print(sv.version, sv.created_at)
</code></pre></div><a id="fig-code-group-java-tab"></a>Java<div><a id="code-code-group-java"></a><pre class="language-java"><code>CursorPage&lt;SkillVersion&gt; versions = client.skills().listVersions(
    &quot;skill_xxx&quot;, SkillListParam.builder().limit(20).build());
for (SkillVersion sv : versions.getData()) System.out.println(sv.getVersion() + &quot; &quot; + sv.getCreatedAt());
</code></pre></div></div></td></tr></tbody></table>

<a id="响应示例"></a>

<a id="h-sklv-resp"></a>

## 响应示例

<a id="code-block"></a>

```json
{
  "data": [
    {
      "id": "skillver_xxx",
      "skill_id": "skill_xxx",
      "type": "skill_version",
      "name": "pdf3.0",
      "description": "从 SKILL.md 解析的描述",
      "version": "1.1",
      "status": "active",
      "created_at": "2026-06-16T08:12:47+00:00",
      "updated_at": "2026-06-16T08:14:30+00:00"
    },
    {
      "id": "skillver_xxx",
      "skill_id": "skill_xxx",
      "type": "skill_version",
      "name": "pdf3.0",
      "description": "从 SKILL.md 解析的描述",
      "version": "1.0",
      "status": "rejected",
      "created_at": "2026-06-16T07:56:03+00:00",
      "updated_at": "2026-06-16T07:57:42+00:00",
      "additional_properties": {
        "error_info": {
          "/index.js": "[Dangerous Tools Without Confirmation] Line 179: ...",
          "/SKILL.md": "[Dangerous Tools Without Confirmation] Line 10: ..."
        }
      }
    }
  ],
  "next_page": "xxx",
  "request_id": "xxx"
}
```

响应包含 `data`（Skill Version 对象数组）与 `next_page`。Skill Version 对象字段如下：

<a id="skill-version-对象字段"></a>

<a id="h-sklv-dto"></a>

### Skill Version 对象字段

**id** `string`

版本 ID，格式 `skillver_xxx`

**skill\_id** `string`

所属技能 ID

**type** `string`

固定为 `skill_version`

**name / description** `string`

从该版本 zip 包内 `SKILL.md` 解析得到

**version** `string`

版本号，由服务端生成

**status** `string`

扫描状态：`checking` / `active` / `rejected`，仅 `active` 可挂载

**created\_at / updated\_at** `string`

创建 / 最近更新时间，ISO 8601

**additional\_properties** `object`

仅 `status=rejected` 时返回，含 `error_info`：按 zip 包内文件路径列出的安全审查问题
