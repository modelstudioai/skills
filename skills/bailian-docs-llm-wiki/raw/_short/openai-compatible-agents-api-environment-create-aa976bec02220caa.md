# 创建 Environment

创建托管运行环境，配置容器、依赖、网络、初始文件和 Skill。

<a id="接口"></a>

<a id="h-oa-env-create-api"></a>

## 接口

**POST** `/agents/environments`

创建一个托管运行环境。成功返回 `201`，表示环境已登记并开始异步准备；准备完成前创建引用该环境的 Session 可能失败。

<table><tbody><tr><td><a id="h-oa-env-create-params"></a><h2>请求体</h2><p><strong>environment</strong> <code>object</code> <strong>（必选）</strong></p><p>环境配置，见下表</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>环境类型，固定为 <code>openai_hosted</code></p><p><strong>environment_template_id</strong> <code>string</code> <strong>（可选）</strong></p><p>环境模板 ID；模板必须属于当前工作空间。模板通过<a href="openai-compatible-agents-api-environment-templat-e9481447eb2967a1.md">环境模板</a>管理。</p><p><strong>env</strong> <code>object</code> <strong>（可选）</strong></p><p>环境变量；变量名需匹配 <code>[A-Za-z_][A-Za-z0-9_]*</code>，不能是 <code>PATH</code>，也不能以保留前缀开头；值不能包含 NUL</p><p><strong>packages</strong> <code>object</code> <strong>（可选）</strong></p><p>预装包，按 <code>npm</code>、<code>python</code>、<code>system</code> 分组</p><p><strong>network</strong> <code>object</code> <strong>（可选）</strong></p><p>网络策略，见下表</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>access</strong> <code>string</code> <strong>（可选）</strong></p><p>网络访问模式，<code>enabled</code>、<code>disabled</code> 或 <code>restricted</code></p><p><strong>allowed_domains</strong> <code>array&lt;string&gt;</code> <strong>（可选）</strong></p><p>允许的域名，<code>access=restricted</code> 时必须非空，只接受主机名，不能包含协议、端口或通配符</p></div></section><p><strong>files</strong> <code>array</code> <strong>（可选）</strong></p><p>初始文件，当前使用 <code>file_id</code> 引用源文件</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>文件引用类型，固定为 <code>file_id</code></p><p><strong>path</strong> <code>string</code> <strong>（必选）</strong></p><p>环境内绝对路径，必须在 <code>/workspace/</code> 内</p><p><strong>file_id</strong> <code>string</code> <strong>（必选）</strong></p><p>通过 <code>POST /agents/file</code> 上传后得到的源文件 ID</p></div></section><p><strong>desktop</strong> <code>object</code> <strong>（可选）</strong></p><p>桌面配置，当前只接受 <code>enabled=false</code>，<code>enabled=true</code> 返回 <code>400</code></p><p><strong>setup_commands</strong> <code>array</code> <strong>（可选）</strong></p><p>初始化命令，按顺序执行。每项包含必填的 <code>command</code> 和可选的 <code>cwd</code>，<code>cwd</code> 默认为 <code>/workspace</code></p><p><strong>skills</strong> <code>array</code> <strong>（可选）</strong></p><p>Skill，当前使用 <code>skill_reference</code>，最多 32 项</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>Skill 引用类型，固定为 <code>skill_reference</code></p><p><strong>skill_id</strong> <code>string</code> <strong>（必选）</strong></p><p>技能资源 ID</p><p><strong>version</strong> <code>string</code> <strong>（可选）</strong></p><p>Skill 版本；省略时解析 <code>latest</code> 并冻结具体版本</p></div></section><p><strong>capability_directories</strong> <code>array</code> <strong>（可选）</strong></p><p>能力发现目录，必须在 <code>/workspace/</code> 内</p></div></section><p><strong>vault_ids</strong> <code>array&lt;string&gt; / null</code> <strong>（可选）</strong></p><p>挂载的 Vault，最多 10 个</p><p><code>plugins</code> 非空时当前拒绝；<code>desktop.enabled=true</code> 当前拒绝。 <code>skill_id</code> 来自 Skill API。先通过<a href="../application-api-reference/managed-agents-api/skills-api/skill-create.md">创建 Skill</a>或<a href="../application-api-reference/managed-agents-api/skills-api/skill-list.md">列出 Skill</a>获取可用的 <code>skill_id</code> 和版本。</p><p>创建支持可选的 <code>Idempotency-Key</code> Header。同一工作空间内使用相同的键和请求正文时返回已有资源；键相同但正文不同返回 <code>409</code>。</p><p>挂载 <code>unrestricted</code> Credential 时，<code>network.access</code> 必须为 <code>restricted</code>，<code>allowed_domains</code> 必须非空且合法。</p><p>示例：<code>&quot;skills&quot;: [{&quot;type&quot;: &quot;skill_reference&quot;, &quot;skill_id&quot;: &quot;skill_xxx&quot;, &quot;version&quot;: &quot;1.0&quot;}]</code></p></td><td><a id="h-oa-environment-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents/environments&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;environment&quot;: {
      &quot;type&quot;: &quot;openai_hosted&quot;,
      &quot;packages&quot;: {&quot;python&quot;: [&quot;pandas&quot;]}
    }
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

environment = client.beta.agents.environments.create(
    environment={
        &quot;type&quot;: &quot;openai_hosted&quot;,
          &quot;packages&quot;: {&quot;python&quot;: [&quot;pandas&quot;]},
    },
)
print(environment.id, environment.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-create-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>环境 ID</p><p><strong>object</strong> <code>string</code></p><p>Environment 对象类型，固定为 <code>agent.environment</code></p><p><strong>type</strong> <code>string</code></p><p>环境类型，固定为 <code>openai_hosted</code></p><p><strong>status</strong> <code>string</code></p><p>环境状态：<code>pending</code>、<code>ready</code>、<code>connected</code>、<code>disconnected</code>、<code>suspended</code>、<code>expired</code>、<code>failed</code></p><p><strong>files</strong> <code>array</code></p><p>已安装文件的安全元数据，不返回文件内容。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>环境文件 ID</p><p><strong>type</strong> <code>string</code></p><p>文件引用类型，固定为 <code>file_id</code></p><p><strong>path</strong> <code>string</code></p><p>环境内文件路径</p><p><strong>size_bytes</strong> <code>integer</code></p><p>文件字节数</p><p><strong>file_id</strong> <code>string</code></p><p>原始源文件 ID</p></div></section><p><strong>skills</strong> <code>array</code></p><p>已安装 Skill 的安全元数据，不返回 Skill 包内容。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>Skill 引用类型，固定为 <code>skill_reference</code></p><p><strong>name</strong> <code>string</code></p><p>技能名称</p><p><strong>description</strong> <code>string</code></p><p>技能说明</p><p><strong>skill_id</strong> <code>string</code></p><p>技能资源 ID</p><p><strong>version</strong> <code>string</code></p><p>已冻结的具体版本</p></div></section><p><strong>plugins</strong> <code>array</code></p><p>插件列表，当前托管环境返回 <code>[]</code>；历史记录中的插件字段不代表可以创建</p><p>创建返回 <code>201</code> 不表示环境已经 <code>ready</code>。使用环境前先获取状态并确认 <code>ready</code>。</p></td><td><a id="h-oa-environment-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;ccarenv_xxx&quot;,
  &quot;object&quot;: &quot;agent.environment&quot;,
  &quot;type&quot;: &quot;openai_hosted&quot;,
  &quot;status&quot;: &quot;pending&quot;,
  &quot;files&quot;: [],
  &quot;skills&quot;: [],
  &quot;plugins&quot;: []
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-create-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `missing_required_parameter`，`param=environment` | 在请求体提供 `environment` |
| `400` | `invalid_request_error` / `invalid_request_error` | 按 `environment` 字段说明修正 `type` 和配置 |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间内存在且可访问的模板或环境 |
| `409` | `conflict_error` / `conflict_error` | 同一幂等键使用相同请求正文 |
| `503` | `server_error` / `environment_unavailable` 或 `template_storage_unavailable` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。排查时保留 HTTP 状态、`x-request-id` 和脱敏后的请求正文。
