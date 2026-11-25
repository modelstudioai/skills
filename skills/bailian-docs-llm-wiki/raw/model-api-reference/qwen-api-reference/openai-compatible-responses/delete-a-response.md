# 删除响应

根据 Response ID 删除一个已存储的模型响应。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`DELETE https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/{response_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="delete-req-h2"></a><h2>路径参数</h2><p><strong>response_id</strong><code>string</code>（必选）</p><p>要删除的 Response ID，格式为 <code>resp_xxx</code>。仅当原创建请求中 <code>store=true</code> 时返回的 Response ID 可被删除。</p></td><td><div><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.delete(&quot;resp_xxx&quot;)
print(response)
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.responses.del(&quot;resp_xxx&quot;);
    console.log(response);
}

main();
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X DELETE https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="delete-resp-h2"></a><h2>返回结果</h2><p><strong>id</strong> <code>string</code></p><p>被删除的 Response ID。</p><p><strong>deleted</strong> <code>boolean</code></p><p>是否删除成功，成功为 <code>true</code>。</p></td><td><div><a id="code-block"></a><pre class="language-json"><code>{
    &quot;deleted&quot;: true,
    &quot;id&quot;: &quot;resp_4ca7fa5e-6ff5-9787-bc18-af6ca5eff36c&quot;
}
</code></pre></div></td></tr></tbody></table>

<a id="错误响应"></a>

<a id="delete-error-h2"></a>

## 错误响应

当指定的 Response ID 不存在时，返回以下错误：

<a id="code-block-2"></a>

```json
{
    "error": {
        "message": "Response with id 'resp_xxx' not found.",
        "type": "InvalidParameter"
    }
}
```
