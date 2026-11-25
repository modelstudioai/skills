# 删除 Artifact

删除单个不可变产物版本，不影响其他版本和环境原文件。

<a id="接口"></a>

<a id="h-oa-artifact-delete-api"></a>

## 接口

**DELETE** `/agents/sessions/{session_id}/artifacts/{artifact_id}`

删除指定的 Artifact 版本。成功返回 `200` 和删除信封。

<table><tbody><tr><td><a id="h-oa-artifact-delete-params"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Artifact 所属 Session</p><p><strong>artifact_id</strong> <code>string</code> <strong>（必选）</strong></p><p>要删除的 Artifact 版本 ID</p><p>无请求体。</p></td><td><a id="h-oa-artifact-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X DELETE \
  &quot;$BASE_URL/agents/sessions/sess_xxx/artifacts/artifact_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

deleted = client.beta.agents.sessions.artifacts.delete(
    &quot;artifact_xxx&quot;,
    session_id=&quot;sess_xxx&quot;,
)
print(deleted.deleted)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-artifact-delete-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>被删除的 Artifact 版本 ID</p><p><strong>object</strong> <code>string</code></p><p>Artifact 删除结果对象类型，固定为 <code>agent.session.artifact.deleted</code></p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，成功为 <code>true</code></p><p>删除只移除指定的 Artifact 版本。删除后详情、下载和重复删除返回 <code>404</code>，列表不再出现该版本。删除 Artifact 不等于删除沙箱中的原文件，也不等于删除上传的源文件。</p></td><td><a id="h-oa-artifact-delete-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;artifact_xxx&quot;,
  &quot;object&quot;: &quot;agent.session.artifact.deleted&quot;,
  &quot;deleted&quot;: true
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-artifact-delete-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Artifact ID |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
