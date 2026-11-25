# 删除 Webhook

删除 Webhook。删除后不再投递新的事件，已产生但尚未投递的事件会被取消。已有投递事件在 7 天保留期内仍可查询。

<a id="前提"></a>

<a id="h-delete-prereq"></a>

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](../managed-agents-api-overview.md)。

<a id="接口"></a>

<a id="h-delete-endpoint"></a>

## 接口

**DELETE** `/webhook_endpoints/{id}`

<table><tbody><tr><td><a id="h-delete-path"></a><h2>路径参数</h2><p><strong>id</strong> <code>string</code> <strong>（必选）</strong></p><p>Webhook ID，格式 wep_&lt;ULID&gt;</p></td><td><a id="h-delete-eg"></a><h2>请求示例</h2><a id="fig-code-group"></a><div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X DELETE &quot;$AGENTSTUDIO_URL/webhook_endpoints/wep_01JXX7YQGPRPV1BZXA35QE7WDP&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="h-delete-dto"></a><h3>响应字段</h3><p><strong>request_id</strong> <code>string</code></p><p>请求唯一标识</p></td><td><a id="h-delete-resp"></a><h2>响应</h2><a id="code-block"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;8e1d16e4&quot;
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="h-delete-err"></a>

## 错误码

| 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 404 | `11800001` | webhook not found |
