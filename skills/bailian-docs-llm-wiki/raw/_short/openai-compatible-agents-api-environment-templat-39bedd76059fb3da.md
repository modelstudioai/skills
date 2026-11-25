# 创建 Environment template

创建可复用的环境模板，保存容器、依赖、网络、初始文件和 Skill 配置。

<a id="接口"></a>

<a id="h-oa-env-template-create-endpoint"></a>

## 接口

**POST** `/agents/environments/templates`

成功返回 `201` 和完整环境模板。请求体可以为空，此时创建使用默认配置的模板。

<table><tbody><tr><td><a id="h-oa-env-template-create-body"></a><h2>请求体</h2><p><strong>name</strong> <code>string / null</code> <strong>（可选）</strong></p><p>模板名称</p><p><strong>packages</strong> <code>object</code> <strong>（可选）</strong></p><p>预装包，按 <code>npm</code>、<code>python</code>、<code>system</code> 分组，默认三组均为空数组</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>python</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>Python 包</p><p><strong>system</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>系统包</p><p><strong>npm</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>npm 包</p></div></section><p><strong>env</strong> <code>object&lt;string,string&gt;</code> <strong>（可选）</strong></p><p>环境变量；变量名需匹配 <code>[A-Za-z_][A-Za-z0-9_]*</code>，不能是 <code>PATH</code>，也不能以服务端保留前缀开头；值不能包含 NUL</p><p><strong>setup_commands</strong> <code>array</code> <strong>（可选）</strong></p><p>初始化命令，按顺序执行。每项包含必填的 <code>command</code> 和可选的 <code>cwd</code>，<code>cwd</code> 默认为 <code>/workspace</code></p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>command</strong> <code>string</code> <strong>（可选）</strong></p><p>初始化命令</p><p><strong>cwd</strong> <code>string</code> <strong>（可选）</strong></p><p>工作目录，默认 <code>/workspace</code></p></div></section><p><strong>network</strong> <code>object</code> <strong>（可选）</strong></p><p>网络策略，默认 <code>enabled</code>；不接受 <code>blocked_domains</code></p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>access</strong> <code>string</code> <strong>（可选）</strong></p><p>网络访问模式，<code>enabled</code>、<code>disabled</code> 或 <code>restricted</code></p><p><strong>allowed_domains</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>允许的域名，仅 <code>access=restricted</code> 时生效</p></div></section><p><strong>desktop</strong> <code>object</code> <strong>（可选）</strong></p><p>桌面配置，只接受 <code>enabled=false</code>，<code>enabled=true</code> 返回 <code>400</code></p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>enabled</strong> <code>boolean</code> <strong>（可选）</strong></p><p>是否启用桌面</p></div></section><p><strong>capability_directories</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>能力发现目录，默认 <code>[]</code></p><p><strong>skills</strong> <code>array</code> <strong>（可选）</strong></p><p>Skill 配置，固定为 <code>skill_reference</code></p><p><strong>plugins</strong> <code>array</code> <strong>（可选）</strong></p><p>插件配置，当前只支持空数组，非空返回 <code>400</code></p><p><strong>files</strong> <code>array</code> <strong>（可选）</strong></p><p>初始文件配置，固定为 <code>file_id</code></p><p>模板响应不返回 <code>env</code> 和 <code>setup_commands</code>。<code>files</code> 固定为 <code>file_id</code>，<code>skills</code> 固定为 <code>skill_reference</code>。</p></td><td><a id="h-oa-environment-template-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents/environments/templates&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;name&quot;: &quot;example-template&quot;,
    &quot;network&quot;: {&quot;access&quot;: &quot;disabled&quot;},
    &quot;capability_directories&quot;: [&quot;/workspace/skills&quot;]
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>template = client.beta.agents.environments.templates.create(
    name=&quot;example-template&quot;,
    network={&quot;access&quot;: &quot;disabled&quot;},
    capability_directories=[&quot;/workspace/skills&quot;],
)
print(template.id, template.name)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-template-create-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>环境模板 ID</p><p><strong>object</strong> <code>string</code></p><p>环境模板对象类型，固定为 <code>agent.environment.template</code></p><p><strong>name</strong> <code>string / null</code></p><p>模板名称</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p><strong>updated_at</strong> <code>integer</code></p><p>最近更新时间，Unix 秒</p><p><strong>packages</strong> <code>object</code></p><p>预装包，包含 <code>python</code>、<code>system</code>、<code>npm</code></p><p><strong>network</strong> <code>object</code></p><p>网络策略，包含 <code>access</code>、<code>allowed_domains</code></p><p><strong>desktop</strong> <code>object</code></p><p>桌面配置，包含 <code>enabled</code></p><p><strong>capability_directories</strong> <code>array&lt;string&gt;</code></p><p>能力发现目录</p><p><strong>skills</strong> <code>array</code></p><p>Skill 配置，包含 <code>type</code>、<code>skill_id</code>、<code>version</code></p><p><strong>plugins</strong> <code>array</code></p><p>插件安全元数据。包含 <code>type</code>、<code>name</code>、<code>description</code>，当前为空数组</p><p><strong>files</strong> <code>array</code></p><p>初始文件配置，每项包含 <code>type</code>、<code>path</code>、<code>file_id</code></p></td><td><a id="h-oa-environment-template-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
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

<a id="h-oa-env-template-create-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按字段说明修正请求体 |
| `400` | `invalid_request_error` / `invalid_request_error` | `desktop.enabled=true`、非空 `plugins` 和 `network.blocked_domains` 都会被拒绝，按字段说明调整 |
| `401` | `authentication_error` / `invalid_api_key` | 在请求头携带有效的 `Authorization: Bearer $DASHSCOPE_API_KEY` |
| `500` | `server_error` / `server_error` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |
