# 列出 Environment

分页列出当前工作空间的托管环境，按指定顺序返回。

<a id="接口"></a>

<a id="h-oa-env-list-api"></a>

## 接口

**GET** `/agents/environments`

分页列出当前工作空间的托管环境。成功返回 `200` 和列表信封。

<table><tbody><tr><td><a id="h-oa-env-list-query"></a><h2>查询参数</h2><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量，默认 20，范围 1–100</p><p><strong>order</strong> <code>string</code> <strong>（可选）</strong></p><p>排序方向，<code>asc</code> 或 <code>desc</code>，默认 <code>desc</code></p><p><strong>after</strong> <code>string</code> <strong>（可选）</strong></p><p>上一页的 <code>last_id</code>；结果不包含游标项</p><p><strong>type</strong> <code>string</code> <strong>（可选）</strong></p><p>环境类型；<code>openai_hosted</code> 或 <code>bailian_hosted</code>，当前只校验取值，不按类型过滤，不要依赖它区分托管环境</p><p><code>before</code> 当前返回 <code>400</code>。</p></td><td><a id="h-oa-environment-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS --get &quot;$BASE_URL/agents/environments&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  --data-urlencode &quot;limit=20&quot; \
  --data-urlencode &quot;order=desc&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

page = client.beta.agents.environments.list(limit=20, order=&quot;desc&quot;)
while True:
    for environment in page.data:
        print(environment.id, environment.status)
    if not page.has_more:
        break
    page = page.get_next_page()
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>列表对象类型，固定为 <code>list</code></p><p><strong>data</strong> <code>array</code></p><p>当前页的环境列表，可为空</p><p><strong>first_id</strong> <code>string / null</code></p><p>当前页首项 ID。空页为 <code>null</code></p><p><strong>last_id</strong> <code>string / null</code></p><p>当前页末项 ID。空页为 <code>null</code></p><p><strong>has_more</strong> <code>boolean</code></p><p>当前方向是否还有下一页</p><p>空列表返回：</p></td><td><a id="h-oa-environment-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;list&quot;,
  &quot;data&quot;: [{
    &quot;id&quot;: &quot;ccarenv_xxx&quot;,
    &quot;object&quot;: &quot;agent.environment&quot;,
    &quot;type&quot;: &quot;openai_hosted&quot;,
    &quot;status&quot;: &quot;ready&quot;,
    &quot;files&quot;: [],
    &quot;skills&quot;: [],
    &quot;plugins&quot;: []
  }],
  &quot;first_id&quot;: &quot;ccarenv_xxx&quot;,
  &quot;last_id&quot;: &quot;ccarenv_xxx&quot;,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按查询参数说明修正 `limit`、`order`，并移除 `before` |
| `401` | `invalid_request_error` / `workspace_required` 或 `user_required` | 使用当前工作空间的 API Key |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
