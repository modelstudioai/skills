# 获取 Environment

根据环境 ID 查询准备状态和已安装资产的安全元数据。

<a id="接口"></a>

<a id="h-oa-env-get-api"></a>

## 接口

**GET** `/agents/environments/{environment_id}`

返回指定环境的当前状态和安全元数据。成功返回 `200`。

<table><tbody><tr><td><a id="h-oa-env-get-params"></a><h2>路径参数</h2><p><strong>environment_id</strong> <code>string</code> <strong>（必选）</strong></p><p>创建回执中的环境 ID，不是 Session ID、模板 ID 或 sandbox ID</p><p>无请求体。</p></td><td><a id="h-oa-environment-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/environments/ccarenv_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

environment = client.beta.agents.environments.retrieve(&quot;ccarenv_xxx&quot;)
print(environment.status)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-get-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>环境 ID</p><p><strong>object</strong> <code>string</code></p><p>Environment 对象类型，固定为 <code>agent.environment</code></p><p><strong>type</strong> <code>string</code></p><p>环境类型，固定为 <code>openai_hosted</code></p><p><strong>status</strong> <code>string</code></p><p>环境状态：<code>pending</code>、<code>ready</code>、<code>connected</code>、<code>disconnected</code>、<code>suspended</code>、<code>expired</code>、<code>failed</code></p><p><strong>files</strong> <code>array</code></p><p>已安装文件的安全元数据，不返回文件内容。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>id</strong> <code>string</code></p><p>环境文件 ID</p><p><strong>type</strong> <code>string</code></p><p>文件引用类型，固定为 <code>file_id</code></p><p><strong>path</strong> <code>string</code></p><p>环境内文件路径</p><p><strong>size_bytes</strong> <code>integer</code></p><p>文件字节数</p><p><strong>file_id</strong> <code>string</code></p><p>原始源文件 ID</p></div></section><p><strong>skills</strong> <code>array</code></p><p>已安装 Skill 的安全元数据，不返回 Skill 包内容。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>Skill 引用类型，固定为 <code>skill_reference</code></p><p><strong>name</strong> <code>string</code></p><p>技能名称</p><p><strong>description</strong> <code>string</code></p><p>技能说明</p><p><strong>skill_id</strong> <code>string</code></p><p>技能资源 ID</p><p><strong>version</strong> <code>string</code></p><p>已冻结的具体版本</p></div></section><p><strong>plugins</strong> <code>array</code></p><p>插件列表，当前托管环境返回 <code>[]</code>；历史记录中的插件字段不代表可以创建</p><p><code>ready</code> 表示环境准备完成，可以创建引用该环境的 Session。<code>connected</code> 表示实例已经连接，不保证后续每条命令都成功。</p></td><td><a id="h-oa-environment-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;ccarenv_xxx&quot;,
  &quot;object&quot;: &quot;agent.environment&quot;,
  &quot;type&quot;: &quot;openai_hosted&quot;,
  &quot;status&quot;: &quot;ready&quot;,
  &quot;files&quot;: [],
  &quot;skills&quot;: [],
  &quot;plugins&quot;: []
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-get-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且可见的环境 ID |
| `503` | `server_error` / `environment_unavailable` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。排查时保留 HTTP 状态、`x-request-id` 和环境 ID。
