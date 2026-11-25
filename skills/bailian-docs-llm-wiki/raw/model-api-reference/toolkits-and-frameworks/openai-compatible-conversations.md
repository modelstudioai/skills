# OpenAI Conversations接口兼容

在跨设备或长时间中断的对话中，手动维护消息列表容易丢失上下文。阿里云百炼提供兼容 OpenAI 的 Conversations API。配合 Responses API，可自动注入历史上下文，无需手动同步消息，实现跨场景、跨设备的对话延续。

<a id="create-conversation"></a>

<a id="h2-create-conversation"></a>

## Create conversation

创建一个新会话，可同时添加初始消息项。

**华北2（北京）：POST** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations`

**新加坡：POST** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations`

> **重要**
>
> 旧版URL路径 `/api/v2/apps/protocols/compatible-mode/v1/conversations` 即将停止维护，请尽快迁移至新版路径 `/compatible-mode/v1/conversations`。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<table><tbody><tr><td><p><strong>items</strong><code>array</code>（可选）</p><p>初始消息项列表，最多20条。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>(必选)</strong></p><p>消息类型，仅支持 <code>message</code>。</p><p><strong>role</strong><code>string</code><strong>(必选)</strong></p><p>消息的角色。<code>system</code> 与<code>developer</code> 角色的指令优先级高于 <code>user</code> 角色，<code>assistant</code> 角色表示模型在之前交互中生成的消息。取值：<code>user</code> 、<code>assistant</code> 、<code>system</code> 、<code>developer</code> 。</p><p><strong>content</strong><code>string or array</code><strong>(必选)</strong></p><p>消息内容。支持纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组），列表格式可包含文本等多种内容类型。</p></div></section><p><strong>metadata</strong><code>object</code>（可选）</p><p>会话元数据，用于以结构化格式存储会话的附加信息。最多16对键值对，key最大长度64字符，value最大长度512字符。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

conversation = client.conversations.create(
    metadata={&quot;topic&quot;: &quot;demo&quot;},
    items=[
        {&quot;type&quot;: &quot;message&quot;, &quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。&quot;}
    ]
)
print(conversation)
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const conversation = await client.conversations.create({
    metadata: { topic: &quot;demo&quot; },
    items: [
        {
            type: &quot;message&quot;,
            role: &quot;system&quot;,
            content: &quot;李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。&quot;
        }
    ]
});
console.log(conversation);
</code></pre></div><a id="fig-code-group-curl-tab"></a>cURL<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    &quot;metadata&quot;: {
        &quot;topic&quot;: &quot;demo&quot;
    },
    &quot;items&quot;: [
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;system&quot;,
            &quot;content&quot;: &quot;李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画&quot;
        }
    ]
}'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数"></a>

<a id="h3-create-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>created_at</strong><code>integer</code></p><p>会话创建的 Unix 时间戳（毫秒）。</p><p><strong>id</strong><code>string</code></p><p>会话唯一标识符。</p><p><strong>metadata</strong><code>object</code></p><p>会话元数据，以键值对形式存储的附加信息。最多16对，key最大长度64字符，value最大长度512字符。</p><p><strong>object</strong><code>string</code></p><p>对象类型，固定为 <code>conversation</code>。</p></td><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;created_at&quot;: 1771316949128,
    &quot;id&quot;: &quot;conv_xxx&quot;,
    &quot;metadata&quot;: {
        &quot;topic&quot;: &quot;demo&quot;
    },
    &quot;object&quot;: &quot;conversation&quot;
}
</code></pre></td></tr></tbody></table>

<a id="retrieve-conversation"></a>

<a id="h2-retrieve-conversation"></a>

## Retrieve conversation

获取指定会话的信息。

**华北2（北京）：GET** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**新加坡：GET** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

conversation = client.conversations.retrieve(&quot;conv_xxx&quot;)
print(conversation)
</code></pre></div><a id="fig-code-group-2-node-js-tab"></a>Node.js<div><a id="code-code-group-2-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const conversation = await client.conversations.retrieve(
    &quot;conv_xxx&quot;
);
console.log(conversation);
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>cURL<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-2"></a>

<a id="h3-retrieve-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>created_at</strong><code>integer</code></p><p>会话创建的 Unix 时间戳（毫秒）。</p><p><strong>id</strong><code>string</code></p><p>会话唯一标识符。</p><p><strong>metadata</strong><code>object</code></p><p>会话元数据，以键值对形式存储的附加信息。最多16对，key最大长度64字符，value最大长度512字符。</p><p><strong>object</strong><code>string</code></p><p>对象类型，固定为 <code>conversation</code>。</p></td><td><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;created_at&quot;: 1771316949128,
    &quot;id&quot;: &quot;conv_xxx&quot;,
    &quot;metadata&quot;: {
        &quot;topic&quot;: &quot;demo&quot;
    },
    &quot;object&quot;: &quot;conversation&quot;
}
</code></pre></td></tr></tbody></table>

<a id="update-conversation"></a>

<a id="h2-update-conversation"></a>

## Update conversation

更新会话的元数据信息。

**华北2（北京）：POST** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**新加坡：POST** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p><p><strong>metadata</strong><code>object</code><strong>(必选)</strong></p><p>会话元数据，会完全覆盖原有元数据。最多16对键值对，key最大长度64字符，value最大长度512字符。</p></td><td><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>Python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

updated = client.conversations.update(
    &quot;conv_xxx&quot;,
    metadata={&quot;topic&quot;: &quot;update&quot;}
)
print(updated)
</code></pre></div><a id="fig-code-group-3-node-js-tab"></a>Node.js<div><a id="code-code-group-3-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const updated = await client.conversations.update(
    &quot;conv_xxx&quot;,
    { metadata: { topic: &quot;update&quot; } }
);
console.log(updated);
</code></pre></div><a id="fig-code-group-3-curl-tab"></a>cURL<div><a id="code-code-group-3-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    &quot;metadata&quot;: {
        &quot;topic&quot;: &quot;update&quot;
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-3"></a>

<a id="h3-update-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>created_at</strong><code>integer</code></p><p>会话创建的 Unix 时间戳（毫秒）。</p><p><strong>id</strong><code>string</code></p><p>会话唯一标识符。</p><p><strong>metadata</strong><code>object</code></p><p>会话元数据，以键值对形式存储的附加信息。最多16对，key最大长度64字符，value最大长度512字符。</p><p><strong>object</strong><code>string</code></p><p>对象类型，固定为 <code>conversation</code>。</p></td><td><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;created_at&quot;: 1771318152759,
    &quot;id&quot;: &quot;conv_xxx&quot;,
    &quot;metadata&quot;: {
        &quot;topic&quot;: &quot;update&quot;
    },
    &quot;object&quot;: &quot;conversation&quot;
}
</code></pre></td></tr></tbody></table>

<a id="delete-conversation"></a>

<a id="h2-delete-conversation"></a>

## Delete conversation

删除指定会话。会话中的消息项不会被删除。

**华北2（北京）：DELETE** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

**新加坡：DELETE** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p></td><td><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>Python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

result = client.conversations.delete(&quot;conv_xxx&quot;)
print(result)
</code></pre></div><a id="fig-code-group-4-node-js-tab"></a>Node.js<div><a id="code-code-group-4-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const result = await client.conversations.del(
    &quot;conv_xxx&quot;
);
console.log(result);
</code></pre></div><a id="fig-code-group-4-curl-tab"></a>cURL<div><a id="code-code-group-4-curl"></a><pre class="language-bash"><code>curl --location --request DELETE 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-4"></a>

<a id="h3-delete-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>deleted</strong><code>boolean</code></p><p>是否删除成功。</p><p><strong>id</strong><code>string</code></p><p>被删除的会话ID。</p><p><strong>object</strong><code>string</code></p><p>对象类型，固定为 <code>conversation.deleted</code>。</p></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;deleted&quot;: true,
    &quot;id&quot;: &quot;conv_xxx&quot;,
    &quot;object&quot;: &quot;conversation.deleted&quot;
}
</code></pre></td></tr></tbody></table>

<a id="create-items"></a>

<a id="h2-create-items"></a>

## Create Items

向指定会话添加消息项。

**华北2（北京）：POST** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

**新加坡：POST** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p><p><strong>items</strong><code>array</code><strong>(必选)</strong></p><p>消息项列表，每次最多添加20条。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>(必选)</strong></p><p>消息类型，仅支持 <code>message</code>。</p><p><strong>role</strong><code>string</code><strong>(必选)</strong></p><p>消息的角色。<code>system</code> 、<code>developer</code>角色的指令优先级高于 <code>user</code> 角色，<code>assistant</code> 角色表示模型在之前交互中生成的消息。取值：<code>user</code>、<code>assistant</code>、<code>system</code>、<code>developer</code>。</p><p><strong>content</strong><code>string or array</code><strong>(必选)</strong></p><p>消息内容。支持纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组），列表格式可包含文本等多种内容类型。</p></div></section></td><td><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>Python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

items = client.conversations.items.create(
    &quot;conv_xxx&quot;,
    items=[
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{&quot;type&quot;: &quot;input_text&quot;, &quot;text&quot;: &quot;李红的专业是师范教育&quot;}],
        }
    ],
)
print(items.data)
</code></pre></div><a id="fig-code-group-5-node-js-tab"></a>Node.js<div><a id="code-code-group-5-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const items = await client.conversations.items.create(
    &quot;conv_xxx&quot;,
    {
        items: [
            {
                type: &quot;message&quot;,
                role: &quot;user&quot;,
                content: [{ type: &quot;input_text&quot;, text: &quot;李红的专业是师范教育&quot; }]
            }
        ]
    }
);
console.log(items.data);
</code></pre></div><a id="fig-code-group-5-curl-tab"></a>cURL<div><a id="code-code-group-5-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
--data '{
    &quot;items&quot;: [
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;type&quot;: &quot;input_text&quot;,
                &quot;text&quot;: &quot;李红的专业是师范教育&quot;
            }]
        }
    ]
}'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-5"></a>

<a id="h3-create-items-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>data</strong><code>array[object]</code></p><p>创建的消息项列表。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>消息项唯一标识符。</p><p><strong>content</strong><code>string or array</code></p><p>消息内容。纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组）。</p><p><strong>role</strong><code>string</code></p><p>消息的角色类型，取值：<code>user</code>、<code>assistant</code>、<code>system</code>、<code>developer</code>。</p><p><strong>status</strong><code>string</code></p><p>消息的处理状态，取值：<code>in_progress</code>（处理中）、<code>completed</code>（已完成）、<code>incomplete</code>（未完成）。</p><p><strong>type</strong><code>string</code></p><p>消息项的类型，固定为 <code>message</code>。</p></div></section><p><strong>first_id</strong><code>string</code></p><p>列表中第一条消息项的ID。</p><p><strong>has_more</strong><code>boolean</code></p><p>是否还有更多数据。</p><p><strong>last_id</strong><code>string</code></p><p>列表中最后一条消息项的ID。</p></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;data&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;text&quot;: &quot;李红的专业是师范教育&quot;,
                    &quot;type&quot;: &quot;input_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_xxx&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        }
    ],
    &quot;first_id&quot;: &quot;msg_xxx&quot;,
    &quot;has_more&quot;: false,
    &quot;last_id&quot;: &quot;msg_xxx&quot;
}
</code></pre></td></tr></tbody></table>

<a id="list-items"></a>

<a id="h2-list-items"></a>

## List Items

列出会话中的所有消息项。

**华北2（北京）：GET** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

**新加坡：GET** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p><p><strong>after</strong><code>string</code>（可选）</p><p>分页游标，返回指定消息ID之后的消息项。</p><p><strong>order</strong><code>string</code>（可选）</p><p>排序方式，<code>asc</code>（升序）或 <code>desc</code>（降序），默认 <code>desc</code>。</p><p><strong>limit</strong><code>integer</code>（可选）</p><p>返回数量，范围1-100，默认20。</p></td><td><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>Python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

items = client.conversations.items.list(&quot;conv_xxx&quot;)
print(items.data)
</code></pre></div><a id="fig-code-group-6-node-js-tab"></a>Node.js<div><a id="code-code-group-6-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const items = await client.conversations.items.list(
    &quot;conv_xxx&quot;
);
console.log(items.data);
</code></pre></div><a id="fig-code-group-6-curl-tab"></a>cURL<div><a id="code-code-group-6-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items?limit=10&amp;order=asc' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-6"></a>

<a id="h3-list-items-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>data</strong><code>array[object]</code></p><p>消息项列表。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>id</strong><code>string</code></p><p>消息项唯一标识符。</p><p><strong>content</strong><code>string or array</code></p><p>消息内容。纯文本字符串或结构化内容列表（如 ResponseInputText 对象数组）。</p><p><strong>role</strong><code>string</code></p><p>消息的角色类型，取值：<code>user</code>、<code>assistant</code>、<code>system</code>、<code>developer</code>。</p><p><strong>status</strong><code>string</code></p><p>消息的处理状态，取值：<code>in_progress</code>（处理中）、<code>completed</code>（已完成）、<code>incomplete</code>（未完成）。</p><p><strong>type</strong><code>string</code></p><p>消息项的类型，固定为 <code>message</code>。</p></div></section><p><strong>first_id</strong><code>string</code></p><p>列表中第一条消息项的ID。</p><p><strong>has_more</strong><code>boolean</code></p><p>是否还有更多数据。</p><p><strong>last_id</strong><code>string</code></p><p>列表中最后一条消息项的ID。</p><p><strong>object</strong><code>string</code></p><p>对象类型，固定为 <code>list</code>。</p></td><td><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;data&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;text&quot;: &quot;李红，一位温婉而坚韧的江南女子，出生在浙江省，今年20岁&quot;,
                    &quot;type&quot;: &quot;input_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_7639f8f6-484b-454a-8125-96a3f40eb9e8&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        },
        {
            &quot;content&quot;: [
                {
                    &quot;text&quot;: &quot;李红的闺蜜是小芳&quot;,
                    &quot;type&quot;: &quot;input_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_288594f6-6ef1-4519-94d4-a545ca311828&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        }
    ],
    &quot;first_id&quot;: &quot;msg_7639f8f6-484b-454a-8125-96a3f40eb9e8&quot;,
    &quot;has_more&quot;: false,
    &quot;last_id&quot;: &quot;msg_288594f6-6ef1-4519-94d4-a545ca311828&quot;,
    &quot;object&quot;: &quot;list&quot;
}
</code></pre></td></tr></tbody></table>

<a id="retrieve-item"></a>

<a id="h2-retrieve-item"></a>

## Retrieve Item

获取指定消息项的详情。

**华北2（北京）：GET** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

**新加坡：GET** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p><p><strong>item_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>消息项ID。</p></td><td><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>Python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

item = client.conversations.items.retrieve(
    &quot;msg_xxx&quot;,
    conversation_id=&quot;conv_xxx&quot;
)
print(item)
</code></pre></div><a id="fig-code-group-7-node-js-tab"></a>Node.js<div><a id="code-code-group-7-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const item = await client.conversations.items.retrieve(
    &quot;msg_xxx&quot;,
    { conversation_id: &quot;conv_xxx&quot; }
);
console.log(item);
</code></pre></div><a id="fig-code-group-7-curl-tab"></a>cURL<div><a id="code-code-group-7-curl"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items/msg_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-7"></a>

<a id="h3-retrieve-item-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>content</strong><code>array[object]</code></p><p>消息内容列表，包含一个或多个内容对象。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code></p><p>内容类型，如 <code>input_text</code>（用户输入文本）或 <code>output_text</code>（模型输出文本）。</p><p><strong>text</strong><code>string</code></p><p>文本内容。</p></div></section><p><strong>id</strong><code>string</code></p><p>消息项唯一标识符。</p><p><strong>role</strong><code>string</code></p><p>消息的角色类型，取值：<code>user</code>、<code>assistant</code>、<code>system</code>、<code>developer</code>。</p><p><strong>status</strong><code>string</code></p><p>消息的处理状态，取值：<code>in_progress</code>（处理中）、<code>completed</code>（已完成）、<code>incomplete</code>（未完成）。</p><p><strong>type</strong><code>string</code></p><p>消息项的类型，固定为 <code>message</code>。</p></td><td><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;content&quot;: [
        {
            &quot;text&quot;: &quot;李红的专业是师范教育&quot;,
            &quot;type&quot;: &quot;input_text&quot;
        }
    ],
    &quot;id&quot;: &quot;msg_xxx&quot;,
    &quot;role&quot;: &quot;user&quot;,
    &quot;status&quot;: &quot;completed&quot;,
    &quot;type&quot;: &quot;message&quot;
}
</code></pre></td></tr></tbody></table>

<a id="delete-item"></a>

<a id="h2-delete-item"></a>

## Delete Item

删除指定的消息项。

**华北2（北京）：DELETE** `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

**新加坡：DELETE** `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/conversations/{conversation_id}/items/{item_id}`

<table><tbody><tr><td><p><strong>conversation_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>会话ID。</p><p><strong>item_id</strong><code>string</code><strong>(必选, Path)</strong></p><p>消息项ID。</p></td><td><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-python-tab"></a>Python<div><a id="code-code-group-8-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

result = client.conversations.items.delete(
    &quot;msg_xxx&quot;,
    conversation_id=&quot;conv_xxx&quot;
)
print(result)
</code></pre></div><a id="fig-code-group-8-node-js-tab"></a>Node.js<div><a id="code-code-group-8-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const result = await client.conversations.items.del(
    &quot;msg_xxx&quot;,
    { conversation_id: &quot;conv_xxx&quot; }
);
console.log(result);
</code></pre></div><a id="fig-code-group-8-curl-tab"></a>cURL<div><a id="code-code-group-8-curl"></a><pre class="language-bash"><code>curl --location --request DELETE 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items/msg_xxx' \
--header 'Authorization: Bearer $DASHSCOPE_API_KEY'
</code></pre></div></div></td></tr></tbody></table>

<a id="响应参数-8"></a>

<a id="h3-delete-item-response"></a>

### 响应参数

<table><tbody><tr><td><p><strong>deleted</strong><code>boolean</code></p><p>是否删除成功。</p><p><strong>id</strong><code>string</code></p><p>被删除的消息项ID。</p><p><strong>object</strong><code>string</code></p><p>对象类型，固定为 <code>conversation.item.deleted</code>。</p></td><td><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;deleted&quot;: true,
    &quot;id&quot;: &quot;msg_xxx&quot;,
    &quot;object&quot;: &quot;conversation.item.deleted&quot;
}
</code></pre></td></tr></tbody></table>

<a id="response-api-使用-conversation-示例"></a>

<a id="8c6069bd19h5p"></a>

## Response API 使用 conversation 示例

通过 Responses API 的 `conversation` 参数，可以实现多轮对话的上下文保持。

> 请勿同时传入`previous_response_id`和`conversation`，否则会报错：`[400] INVALID_REQUEST: Mutually exclusive parameters: Ensure you are only providing one of: previous_response_id or conversation.`

<a id="fig-code-group-9"></a>

<a id="fig-code-group-9-python-tab"></a>

Python

<a id="code-code-group-9-python"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

conversation = client.conversations.create(
    items=[
        {
            "type": "message",
            "role": "system",
            "content": "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。",
        }
    ]
)

response1 = client.responses.create(
    conversation=conversation.id, model="qwen3.8-max", input="李红今年多大了"
)
print(f"第一轮响应: {response1.output_text}")

response2 = client.responses.create(
    conversation=conversation.id, model="qwen3.8-max", input="她的兴趣爱好是什么？"
)
print(f"第二轮响应: {response2.output_text}")
```

<a id="fig-code-group-9-node-js-tab"></a>

Node.js

<a id="code-code-group-9-node-js"></a>

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

const conversation = await client.conversations.create({
  items: [
    {
      type: "message",
      role: "system",
      content: "李红，一位温婉而坚韧的江南女子，出生在浙江省杭州市，她今年20岁，她的兴趣爱好是琴棋书画。"
    }
  ]
});

const response1 = await client.responses.create({
  conversation: conversation.id,
  model: "qwen3.8-max",
  input: "李红今年多大了"
});
console.log("第一轮响应:", response1.output_text);

const response2 = await client.responses.create({
  conversation: conversation.id,
  model: "qwen3.8-max",
  input: "她的兴趣爱好是什么？"
});
console.log("第二轮响应:", response2.output_text);
```

<a id="使用限制"></a>

<a id="h2-limits"></a>

## 使用限制

-   创建会话或添加消息项时，`items` 最多包含20条。
-   `metadata` 最多16对键值对，key最大长度64字符，value最大长度512字符。
-   会话信息保留最近7天内的最新100条，超出时间或数量限制的内容将自动清理。
