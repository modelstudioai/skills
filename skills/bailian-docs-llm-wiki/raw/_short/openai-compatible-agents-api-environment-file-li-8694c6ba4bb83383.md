# 列出 Environment file

查询指定环境中已落盘的文件和目录分页。

<a id="接口"></a>

<a id="h-oa-env-file-list-api"></a>

## 接口

**GET** `/agents/environments/{environment_id}/files`

查询指定环境中的实时文件。成功返回 `200` 和目录分页。该接口用于核对文件是否已经落盘，不返回文件正文。

<table><tbody><tr><td><a id="h-oa-env-file-list-query"></a><h2>查询参数</h2><p><strong>path</strong> <code>string</code> <strong>（可选）</strong></p><p>目录路径，可选，限定 <code>/workspace/</code> 内已存在的绝对目录</p><p><strong>limit</strong> <code>integer</code> <strong>（可选）</strong></p><p>每页数量</p><p><strong>page</strong> <code>string</code> <strong>（可选）</strong></p><p>分页游标；首次不传，后续传上一页返回的 <code>next</code></p><p>分页请求参数名是 <code>page</code>，响应游标字段是 <code>next</code>；不是源文件或 Artifact 的 <code>after</code>。</p></td><td><a id="h-oa-environment-file-list-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS --get &quot;$BASE_URL/agents/environments/ccarenv_xxx/files&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  --data-urlencode &quot;path=/workspace/input/&quot; \
  --data-urlencode &quot;limit=20&quot;
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

page = client.beta.agents.environments.files.list(
    &quot;ccarenv_xxx&quot;,
    path=&quot;/workspace/input/&quot;,
    limit=20,
)
for environment_file in page.data:
    print(environment_file.path, environment_file.size_bytes)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-file-list-response"></a><h3>响应字段</h3><p><strong>object</strong> <code>string</code></p><p>分页对象类型，固定为 <code>page</code></p><p><strong>data</strong> <code>array</code></p><p>当前页的环境文件</p><p><strong>next</strong> <code>string / null</code></p><p>下一页游标；没有下一页时为 <code>null</code></p><p><strong>has_more</strong> <code>boolean</code></p><p>是否还有下一页</p><p><code>data[]</code> 中每一项包含：</p><p>响应包含当前页的 <code>data</code> 数组和下一页游标。目录为空时 <code>data</code> 为空数组。</p><a id="accordion-data-项"></a><section><p>data 项</p><div><p><strong>environment_id</strong> <code>string</code></p><p>环境 ID</p><p><strong>object</strong> <code>string</code></p><p>环境文件对象类型，固定为 <code>agent.environment.file</code></p><p><strong>path</strong> <code>string</code></p><p>环境内文件路径</p><p><strong>size_bytes</strong> <code>integer</code></p><p>文件大小，单位字节</p></div></section></td><td><a id="h-oa-environment-file-list-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;object&quot;: &quot;page&quot;,
  &quot;data&quot;: [
    {
      &quot;environment_id&quot;: &quot;ccarenv_xxx&quot;,
      &quot;object&quot;: &quot;agent.environment.file&quot;,
      &quot;path&quot;: &quot;/workspace/input/input.txt&quot;,
      &quot;size_bytes&quot;: 18
    }
  ],
  &quot;next&quot;: null,
  &quot;has_more&quot;: false
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-file-list-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 传入 `/workspace/` 内已存在的绝对目录 |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且可见的环境 ID |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
