# 获取 Environment template

根据模板 ID 返回完整的环境模板配置。

<a id="接口"></a>

<a id="h-oa-env-template-get-endpoint"></a>

## 接口

**GET** `/agents/environments/templates/{template_id}`

成功返回 `200` 和完整环境模板。

<table><tbody><tr><td><a id="h-oa-env-template-get-path"></a><h2>路径参数</h2><p><strong>template_id</strong> <code>string</code> <strong>（必选）</strong></p><p>环境模板 ID</p></td><td><a id="h-oa-environment-template-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/environments/templates/envtmpl_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>template = client.beta.agents.environments.templates.retrieve(&quot;envtmpl_xxx&quot;)
print(template.id, template.name)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-template-get-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>环境模板 ID</p><p><strong>object</strong> <code>string</code></p><p>环境模板对象类型，固定为 <code>agent.environment.template</code></p><p><strong>name</strong> <code>string / null</code></p><p>模板名称</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近更新时间，Unix 秒</p><p><strong>packages</strong> <code>object</code></p><p>预装包，包含 <code>python</code>、<code>system</code>、<code>npm</code></p><p><strong>network</strong> <code>object</code></p><p>网络策略，包含 <code>access</code>、<code>allowed_domains</code></p><p><strong>desktop</strong> <code>object</code></p><p>桌面配置，包含 <code>enabled</code></p><p><strong>capability_directories</strong> <code>array&lt;string&gt;</code></p><p>能力发现目录</p><p><strong>skills</strong> <code>array</code></p><p>Skill 配置，包含 <code>type</code>、<code>skill_id</code>、<code>version</code></p><p><strong>plugins</strong> <code>array</code></p><p>插件安全元数据。包含 <code>type</code>、<code>name</code>、<code>description</code>，当前为空数组</p><p><strong>files</strong> <code>array</code></p><p>初始文件配置，每项包含 <code>type</code>、<code>path</code>、<code>file_id</code></p><p>响应不返回 <code>env</code> 和 <code>setup_commands</code>。</p></td><td><a id="h-oa-environment-template-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;envtmpl_xxx&quot;,
  &quot;name&quot;: &quot;example-template&quot;,
  &quot;object&quot;: &quot;agent.environment.template&quot;,
  &quot;created_at&quot;: 1794319007,
  &quot;updated_at&quot;: 1794319007,
  &quot;packages&quot;: {&quot;python&quot;: [], &quot;system&quot;: [], &quot;npm&quot;: []},
  &quot;network&quot;: {&quot;access&quot;: &quot;disabled&quot;, &quot;allowed_domains&quot;: []},
  &quot;desktop&quot;: {&quot;enabled&quot;: false},
  &quot;capability_directories&quot;: [&quot;/workspace/skills&quot;],
  &quot;skills&quot;: [],
  &quot;plugins&quot;: [],
  &quot;files&quot;: []
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-template-get-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在的环境模板 ID |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
