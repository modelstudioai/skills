# 获取输入项列表

获取生成指定 Response 时所使用的输入项列表。在多轮对话（使用 previous\_response\_id 串联）中，会一并返回历史轮次的用户输入和模型回复。仅当原创建请求中 store=true 时，返回的 Response ID 才支持查询。

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/{response_id}/input_items`

<table><tbody><tr><td><a id="list-req-path-h2"></a><h2>路径参数</h2><p><strong>response_id</strong><code>string</code>（必选）</p><p>要查询输入项的 Response ID，格式为 <code>resp_xxx</code>。仅当原创建请求中 <code>store=true</code> 时，返回的 Response ID 才支持查询。</p><a id="list-query-h2"></a><h2>查询参数</h2><p><strong>after</strong><code>string</code>（可选）</p><p>以指定的 item ID（格式为 <code>msg_xxx</code>）作为起点，返回排在该 ID 之后的数据，顺序由 <code>order</code> 决定。<strong>item ID 来源</strong>：<a href="qwen-api-via-openai-responses.md">创建响应</a>返回的 <code>output[].id</code>；或本接口返回的 <code>data[].id</code>、<code>first_id</code>、<code>last_id</code>。常用于翻页：把上一次返回的 <code>last_id</code> 作为本次的 <code>after</code> 传入，即可继续获取后续数据。</p><p><strong>limit</strong><code>integer</code>（可选）</p><p>返回的最大条数，取值范围 [1, 100]，默认值为 20。</p><p><strong>order</strong><code>string</code>（可选）</p><p>排序方式，支持 <code>asc</code>（升序）和 <code>desc</code>（降序），默认值为 <code>desc</code>。</p></td><td><div><a id="sec-tabs-2"></a><section><a id="默认查询"></a><section><a id="默认查询-h4"></a><h4>默认查询</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.input_items.list(&quot;resp_xxx&quot;)
print(response.data)
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.responses.inputItems.list(&quot;resp_xxx&quot;);
    console.log(response.data);
}

main();
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx/input_items \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></section><a id="按条件查询"></a><section><a id="按条件查询-h4"></a><h4>按条件查询</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.input_items.list(
    &quot;resp_xxx&quot;,
    # after 取 item ID（msg_xxx）：可来自创建响应返回的 output[].id，或本接口返回的 data[].id / first_id / last_id
    after=&quot;msg_xxx&quot;,
    limit=10,
    order=&quot;asc&quot;,
)
print(response.data)
</code></pre></div><a id="fig-code-group-2-node-js-tab"></a>Node.js<div><a id="code-code-group-2-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.responses.inputItems.list(&quot;resp_xxx&quot;, {
        // after 取 item ID（msg_xxx）：可来自创建响应返回的 output[].id，或本接口返回的 data[].id / first_id / last_id
        after: &quot;msg_xxx&quot;,
        limit: 10,
        order: &quot;asc&quot;,
    });
    console.log(response.data);
}

main();
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code># after 取 item ID（msg_xxx）：可来自创建响应返回的 output[].id，或本接口返回的 data[].id / first_id / last_id
curl &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx/input_items?after=msg_xxx&amp;limit=10&amp;order=asc&quot; \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></section></section></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="list-resp-h2"></a><h2>返回结果</h2><p><strong>data</strong> <code>array</code></p><p>输入项列表。每个元素是一个消息对象，包含 <code>id</code>、<code>role</code>、<code>content</code>、<code>type</code>、<code>status</code> 字段。<code>role</code> 取值为 <code>user</code> 或 <code>assistant</code>；<code>content</code> 中元素的 <code>type</code> 取值为 <code>input_text</code>（用户输入）或 <code>output_text</code>（模型回复）。多轮对话（使用 <code>previous_response_id</code> 串联）中，会按发生顺序包含历史用户消息与历史模型回复。</p><p><strong>first_id</strong> <code>string</code></p><p>列表中第一个元素的 ID。</p><p><strong>last_id</strong> <code>string</code></p><p>列表中最后一个元素的 ID。</p><p><strong>has_more</strong> <code>boolean</code></p><p>是否还有未返回的数据。当为 <code>true</code> 时，把本次返回的 <code>last_id</code> 作为下一次请求的 <code>after</code> 参数，可继续获取后续数据。</p><p><strong>id</strong> <code>string</code></p><p>对应的 Response ID。</p><p><strong>model</strong> <code>string</code></p><p>生成该 Response 时使用的模型名称。</p><p><strong>created_at</strong> <code>integer</code></p><p>Response 创建时间的 Unix 时间戳（<strong>毫秒</strong>）。注意：与&quot;创建响应/检索响应&quot;接口返回的 <code>created_at</code>（秒）单位不同。</p><p><strong>previous_response_id</strong> <code>string</code></p><p>多轮对话（使用 <code>previous_response_id</code> 串联）时返回，值为上一轮的 Response ID。</p></td><td><div><a id="code-block"></a><pre class="language-json"><code>{
    &quot;created_at&quot;: 1778674066000,
    &quot;data&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;text&quot;: &quot;你好&quot;,
                    &quot;type&quot;: &quot;input_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_8dac4972-fdba-42b5-bed9-280441ced8ea&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        }
    ],
    &quot;first_id&quot;: &quot;msg_8dac4972-fdba-42b5-bed9-280441ced8ea&quot;,
    &quot;has_more&quot;: false,
    &quot;id&quot;: &quot;resp_4ca7fa5e-6ff5-9787-bc18-af6ca5eff36c&quot;,
    &quot;last_id&quot;: &quot;msg_8dac4972-fdba-42b5-bed9-280441ced8ea&quot;,
    &quot;model&quot;: &quot;qwen3.8-max&quot;
}
</code></pre></div></td></tr></tbody></table>

<a id="错误响应"></a>

<a id="list-error-h2"></a>

## 错误响应

当指定的 Response ID 不存在时，返回以下错误：

<a id="code-block-2"></a>

```json
{
    "request_id": "339b771548c7fbb15717316b49627681",
    "code": "InvalidParameter",
    "message": "Response with id 'resp_xxx' not found."
}
```
