# 写入 Environment file

将当前工作空间的源文件写入指定环境路径。

<a id="接口"></a>

<a id="h-oa-env-file-create-api"></a>

## 接口

**POST** `/agents/environments/{environment_id}/files`

将源文件写入指定环境的 `/workspace/` 路径。成功返回 `201` 和环境文件信息。写入成功只表示文件已经落盘，不表示模型已经读取。

<table><tbody><tr><td><a id="h-oa-env-file-create-path"></a><h2>路径参数</h2><p><strong>environment_id</strong> <code>string</code> <strong>（必选）</strong></p><p>环境 ID，当前工作空间中的环境</p><a id="h-oa-env-file-create-params"></a><h2>请求体</h2><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>文件引用类型，固定为 <code>file_id</code></p><p><strong>file_id</strong> <code>string</code> <strong>（必选）</strong></p><p>源文件 ID，来自当前工作空间的 Agent API 上传</p><p><strong>path</strong> <code>string</code> <strong>（必选）</strong></p><p>文件路径；<code>/workspace/</code> 内的规范绝对文件路径，不能包含目录穿越</p><p>请求体不接受额外字段。源文件必须来自当前工作空间的 Agent API 上传。</p></td><td><a id="h-oa-environment-file-create-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -sS -X POST &quot;$BASE_URL/agents/environments/ccarenv_xxx/files&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;OpenAI-Beta: agents=v1&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;type&quot;: &quot;file_id&quot;,
    &quot;file_id&quot;: &quot;file_xxx&quot;,
    &quot;path&quot;: &quot;/workspace/input/input.txt&quot;
  }'
</code></pre></div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ[&quot;DASHSCOPE_API_KEY&quot;],
    base_url=os.environ[&quot;BASE_URL&quot;],
)

environment_file = client.beta.agents.environments.files.create(
    &quot;ccarenv_xxx&quot;,
    type=&quot;file_id&quot;,
    file_id=&quot;file_xxx&quot;,
    path=&quot;/workspace/input/input.txt&quot;,
)
print(environment_file.path, environment_file.size_bytes)
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-oa-env-file-create-response"></a><h3>响应字段</h3><p><strong>environment_id</strong> <code>string</code></p><p>环境 ID</p><p><strong>object</strong> <code>string</code></p><p>环境文件对象类型，固定为 <code>agent.environment.file</code></p><p><strong>path</strong> <code>string</code></p><p>环境内文件路径</p><p><strong>size_bytes</strong> <code>integer</code></p><p>本次写入的字节数</p><p>响应没有新的源文件 ID，也不是 Artifact 发布回执。</p></td><td><a id="h-oa-environment-file-create-resp"></a><h2>响应示例</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;environment_id&quot;: &quot;ccarenv_xxx&quot;,
  &quot;object&quot;: &quot;agent.environment.file&quot;,
  &quot;path&quot;: &quot;/workspace/input/input.txt&quot;,
  &quot;size_bytes&quot;: 18
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-oa-env-file-create-errors"></a>

## 错误码

| HTTP 状态码 | 错误类型 / 错误码 | 解决方案 |
| --- | --- | --- |
| `400` | `invalid_request_error` / `invalid_request_error` | 按字段说明补齐必填字段，并修正 `type`、`path` |
| `404` | `not_found_error` / `not_found_error` | 使用当前工作空间中存在且可见的源文件 ID |
| `400` | `invalid_request_error` / `invalid_request_error`，`param=file_id` | 使用通过 `POST /agents/file` 上传的源文件 |
| `409` | `invalid_request_error` / `file_not_available`，`param=file_id` | 更换为审核通过且可用的源文件 |
| `504` | `server_error` / `environment_file_timeout` | 稍后重试；持续失败时提交工单并提供 `x-request-id` |

错误正文形如 `{"error":{"type","code","message","param"}}`，网关错误可能使用不同结构。
