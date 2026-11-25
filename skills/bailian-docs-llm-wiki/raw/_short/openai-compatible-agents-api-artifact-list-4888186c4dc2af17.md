# 列出 Artifact

分页列出 Session 已发布的不可变产物版本。

<a id="接口"></a>

<a id="h-oa-artifact-list-api"></a>

## 接口

**GET** `/agents/sessions/{session_id}/artifacts`

分页列出指定 Session 已发布的 Artifact。成功返回 `200` 和列表信封。

> **说明**
>
> Artifact 需要目标工作空间已开通产物能力，并在 Turn 成功完成后才会产生。托管环境完成 Turn 后，如果工作空间未开通产物能力，列表返回空数组。本轮没有新增产物时，列表仍可能包含此前 Turn 的产物；可读取返回项的 `turn_id` 筛选本轮结果。

> **说明**
>
> 使用 `environment.type=none` 的 Session 没有关联环境，产物列表可能返回 `404`。需要托管环境完成 Turn 后再查询。

<table><tbody><tr><td><a id="h-oa-artifact-list-query"></a><h2>查询参数</h2><p><strong>environment_id</strong> <code>string</code> <strong>（可选）</strong></p><p>环境 ID，可选，按环境过滤</p><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20，范围 1–100</p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code></p><p><strong>before</strong> <code>string</code> <strong>（可选）</strong></p><p>反向分页游标，可选；与 <code>after</code> 不能同时使用</p><p>当前不提供按 <code>turn_id</code> 或 <code>path</code> 的服务端过滤。分页后由调用方自行筛选。</p></td><td><a id="h-oa-artifact-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS --get &quot;$BASE_URL/agents/sessions/sess_xxx/artifacts&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  --data-urlencode &quot;environment_id=ccarenv_xxx&quot; \
  --data-urlencode &quot;limit=100&quot; \
  --data-urlencode &quot;order=desc&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

page = client.beta.agents.sessions.artifacts.list(
    &quot;sess_xxx&quot;,
    environment_id=&quot;ccarenv_xxx&quot;,
    limit=100,
    order=&quot;desc&quot;,
)
for artifact in page.data:
    print(artifact.id, artifact.turn_id, artifact.path)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-artifact-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当前页的 Artifact 列表，可为空</p><p><strong>first_id</strong> <code>string / null</code></p><p>当前页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当前页末项 ID。空页为 <code>null</code></p><p><strong>has_more</strong> <code>boolean</code></p><p>当前方向是否还有下一页</p><p><code>data</code> 项字段：</p><p>列表不返回底层存储标识、签名下载地址或凭据。</p><a id="accordion-data-项"></a><section><p>data 项</p><div><p><strong>id</strong> <code>string</code></p><p>Artifact 版本 ID，不是 <code>file_id</code></p><p><strong>object</strong> <code>string</code></p><p>Artifact 对象类型，固定为 <code>agent.session.artifact</code></p><p><strong>session_id</strong> <code>string</code></p><p>所属 Session</p><p><strong>environment_id</strong> <code>string</code></p><p>发布来源环境</p><p><strong>turn_id</strong> <code>string</code></p><p>发布来源 Turn</p><p><strong>path</strong> <code>string</code></p><p>产物生成时的沙箱完整路径</p><p><strong>size_bytes</strong> <code>integer</code></p><p>文件大小，单位字节</p><p><strong>created_at</strong> <code>integer</code></p><p>创建时间，Unix 秒</p></div></section></td><td><a id="h-oa-artifact-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [{
    &quot;id&quot;: &quot;artifact_xxx&quot;,
    &quot;object&quot;: &quot;agent.session.artifact&quot;,
    &quot;session_id&quot;: &quot;sess_xxx&quot;,
    &quot;environment_id&quot;: &quot;ccarenv_xxx&quot;,
    &quot;turn_id&quot;: &quot;turn_xxx&quot;,
    &quot;path&quot;: &quot;/workspace/outputs/report.txt&quot;,
    &quot;size_bytes&quot;: 19,
    &quot;created_at&quot;: 1793941200
  }],
  &quot;first_id&quot;: &quot;artifact_xxx&quot;,
  &quot;last_id&quot;: &quot;artifact_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-artifact-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`，并避免同时传冲突参数 |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且可见的 Session ID |
| `404` | `not_found_error` / `not_found_error` | 使用当前集合上一页返回的 `last_id` 作为游标 |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。排查时保留 Session ID、Turn ID、环境 ID 和 `x-request-id`。
