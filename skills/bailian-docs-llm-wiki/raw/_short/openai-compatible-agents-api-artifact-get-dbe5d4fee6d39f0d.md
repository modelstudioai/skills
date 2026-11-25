# 获取 Artifact

查询单个不可变产物版本的元数据。

<a id="接口"></a>

<a id="h-oa-artifact-get-api"></a>

## 接口

**GET** `/agents/sessions/{session_id}/artifacts/{artifact_id}`

返回指定 Artifact 的元数据。成功返回 `200`，不返回文件正文。

<table><tbody><tr><td><a id="h-oa-artifact-get-params"></a><h2>路径参数</h2><p><strong>session_id</strong> <code>string</code> <strong>（必选）</strong></p><p>Artifact 所属 Session</p><p><strong>artifact_id</strong> <code>string</code> <strong>（必选）</strong></p><p>列表返回的 Artifact 版本 ID，不是 <code>file_id</code> 或快照 ID</p><p>无请求体。</p></td><td><a id="h-oa-artifact-get-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS &quot;$BASE_URL/agents/sessions/sess_xxx/artifacts/artifact_xxx&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

artifact = client.beta.agents.sessions.artifacts.retrieve(
    &quot;artifact_xxx&quot;,
    session_id=&quot;sess_xxx&quot;,
)
print(artifact.id, artifact.path, artifact.size_bytes)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-artifact-get-response"></a><h3>响应字段</h3><p><strong>id</strong> <code>string</code></p><p>Artifact 版本 ID，不是 <code>file_id</code></p><p><strong>object</strong> <code>string</code></p><p>Artifact 对象类型，固定为 <code>agent.session.artifact</code></p><p><strong>session_id</strong> <code>string</code></p><p>所属 Session</p><p><strong>environment_id</strong> <code>string</code></p><p>发布来源环境</p><p><strong>turn_id</strong> <code>string</code></p><p>发布来源 Turn</p><p><strong>path</strong> <code>string</code></p><p>产物生成时的沙箱完整路径</p><p><strong>size_bytes</strong> <code>integer</code></p><p>文件大小，单位字节</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p><p>详情不返回底层存储标识、签名下载地址或凭据。</p></td><td><a id="h-oa-artifact-get-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;artifact_xxx&quot;,
  &quot;object&quot;: &quot;agent.session.artifact&quot;,
  &quot;session_id&quot;: &quot;sess_xxx&quot;,
  &quot;environment_id&quot;: &quot;ccarenv_xxx&quot;,
  &quot;turn_id&quot;: &quot;turn_xxx&quot;,
  &quot;path&quot;: &quot;/workspace/outputs/report.txt&quot;,
  &quot;size_bytes&quot;: 19,
  &quot;created_at&quot;: 1793941200
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-artifact-get-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且未删除的 Artifact ID |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
