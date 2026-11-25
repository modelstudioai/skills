# 获取响应

根据 Response ID 获取一个已完成的模型响应。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

SDK 调用配置的`base_url`：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 请求地址：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/{response_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="retrieve-req-h2"></a><h2>路径参数</h2><p><strong>response_id</strong><code>string</code>（必选）</p><p>要获取的 Response ID，格式为 <code>resp_xxx</code>。可从<a href="qwen-api-via-openai-responses.md">创建响应</a>接口的响应中获取。仅当原创建请求中 <code>store=true</code> 时返回的 Response ID 可被检索。</p></td><td><div><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

response = client.responses.retrieve(&quot;resp_xxx&quot;)
print(response)
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
    const response = await openai.responses.retrieve(&quot;resp_xxx&quot;);
    console.log(response);
}

main();
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses/resp_xxx \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></div></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="retrieve-resp-h2"></a><h2>返回结果</h2><p>返回与<a href="qwen-api-via-openai-responses.md#8b91df45f4k58">创建响应</a>相同的 Response 对象。各字段含义如下：</p><p><strong>id</strong> <code>string</code></p><p>本次响应的唯一标识符，格式为 <code>resp_xxx</code>。</p><p><strong>object</strong> <code>string</code></p><p>对象类型，固定为 <code>response</code>。</p><p><strong>status</strong> <code>string</code></p><p>响应状态。枚举值:<code>completed</code>(完成)、<code>failed</code>(失败)、<code>in_progress</code>(生成中)、<code>cancelled</code>(已取消)、<code>queued</code>(排队中)、<code>incomplete</code>(不完整)。</p><p><strong>created_at</strong> <code>integer</code></p><p>响应创建时的 Unix 时间戳（秒）。</p><p><strong>completed_at</strong> <code>integer</code></p><p>响应生成完成时的 Unix 时间戳（秒）。响应未完成时为 <code>null</code>。</p><p><strong>error</strong> <code>object</code></p><p>当模型生成响应失败时返回的错误对象。成功时为 <code>null</code>。</p><p><strong>model</strong> <code>string</code></p><p>用于生成响应的模型 ID。</p><p><strong>output</strong> <code>array</code></p><p>模型生成的输出项数组。数组中的元素类型和顺序取决于模型的响应。</p><a id="accordion-数组元素属性"></a><section><p>数组元素属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出项类型。枚举值：</p><ul><li><code>message</code>：消息类型，包含模型最终生成的回复内容。</li><li><code>reasoning</code>：推理类型，设置 <code>reasoning.effort</code>（非 <code>none</code>）或开启思考模式时返回。推理 Token 会被计入 <code>output_tokens_details.reasoning_tokens</code> 中，按推理 Token 计费。</li><li><code>function_call</code>：函数调用类型，使用自定义 <code>function</code> 工具时返回。需要处理函数调用并返回结果。</li><li><code>web_search_call</code>：搜索调用类型，使用 <code>web_search</code> 工具时返回。</li><li><code>code_interpreter_call</code>：代码执行类型，使用 <code>code_interpreter</code> 工具时返回。</li><li><code>web_extractor_call</code>：网页抽取类型，使用 <code>web_extractor</code> 工具时返回。需要配合 <code>web_search</code> 工具一起使用。</li><li><code>web_search_image_call</code>：文搜图调用类型，使用 <code>web_search_image</code> 工具时返回。包含搜索到的图片列表。</li><li><code>image_search_call</code>：图搜图调用类型，使用 <code>image_search</code> 工具时返回。包含搜索到的相似图片列表。</li><li><code>mcp_call</code>：MCP 调用类型，使用 <code>mcp</code> 工具时返回。包含 MCP 服务的调用结果。</li><li><code>file_search_call</code>：知识库搜索调用类型，使用 <code>file_search</code> 工具时返回。包含知识库的检索查询和结果。</li></ul><p><strong>id</strong> <code>string</code></p><p>输出项的唯一标识符。所有类型的输出项都包含此字段。</p><p><strong>role</strong> <code>string</code></p><p>消息角色，固定为 <code>assistant</code>。仅当 <code>type</code> 为 <code>message</code> 时存在。</p><p><strong>status</strong> <code>string</code></p><p>输出项状态。可选值：<code>completed</code>（完成）、<code>in_progress</code>（生成中）。当 <code>type</code> 不为<code>reasoning</code>时存在。</p><p><strong>name</strong> <code>string</code></p><p>工具或函数名称。当 <code>type</code> 为 <code>function_call</code>、<code>web_search_image_call</code>、<code>image_search_call</code>、<code>mcp_call</code> 时存在。</p><p>对于 <code>web_search_image_call</code> 和 <code>image_search_call</code>，值分别固定为 <code>&quot;web_search_image&quot;</code> 和 <code>&quot;image_search&quot;</code>。</p><p>对于 <code>mcp_call</code>，值为 MCP 服务中被调用的具体函数名（如 <code>amap-maps-maps_geo</code>）。</p><p><strong>arguments</strong> <code>string</code></p><p>工具调用的参数，JSON 字符串格式。当 <code>type</code> 为 <code>function_call</code>、<code>web_search_image_call</code>、<code>image_search_call</code>、<code>mcp_call</code> 时存在。使用前需要通过 <code>JSON.parse()</code> 解析。不同工具类型的 arguments 内容：</p><ul><li><code>web_search_image_call</code>：<code>{&quot;queries&quot;: [&quot;搜索关键词1&quot;, &quot;搜索关键词2&quot;]}</code>，其中 <code>queries</code> 为模型根据用户输入自动生成的搜索关键词列表。</li><li><code>image_search_call</code>：<code>{&quot;img_idx&quot;: 0, &quot;bbox&quot;: [0, 0, 1000, 1000]}</code>，其中 <code>img_idx</code> 为输入图片的索引（从 0 开始），<code>bbox</code> 为搜索区域的边界框坐标 [x1, y1, x2, y2]，坐标范围 0-1000。</li><li><code>function_call</code>：按用户定义的函数参数 schema 生成的参数对象。</li><li><code>mcp_call</code>：MCP 服务中被调用函数的参数对象。</li></ul><p><strong>call_id</strong> <code>string</code></p><p>函数调用的唯一标识符。仅当 <code>type</code> 为 <code>function_call</code> 时存在。在返回函数调用结果时，需要通过此 ID 关联请求与响应。</p><p><strong>content</strong> <code>array</code></p><p>消息内容数组。仅当 <code>type</code> 为 <code>message</code> 时存在。</p><a id="accordion-数组元素属性-2"></a><section><p>数组元素属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容类型，固定为 <code>output_text</code>。</p><p><strong>text</strong> <code>string</code></p><p>模型生成的文本内容。</p><p><strong>annotations</strong> <code>array</code></p><p>文本注释数组。通常为空数组。</p></div></section><p><strong>summary</strong> <code>array</code></p><p>推理摘要数组。仅当 <code>type</code> 为 <code>reasoning</code> 时存在。每个元素包含 <code>type</code>（值为 <code>summary_text</code>）和 <code>text</code>（摘要文本）字段。</p><p><strong>action</strong> <code>object</code></p><p>搜索动作信息。仅当 <code>type</code> 为 <code>web_search_call</code> 时存在。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>query</strong> <code>string</code></p><p>搜索查询关键词。</p><p><strong>type</strong> <code>string</code></p><p>搜索类型，固定为 <code>search</code>。</p><p><strong>sources</strong> <code>array</code></p><p>搜索来源列表。每个元素包含 <code>type</code>和 <code>url</code>字段。</p></div></section><p><strong>code</strong> <code>string</code></p><p>模型生成并执行的代码。仅当 <code>type</code> 为 <code>code_interpreter_call</code> 时存在。</p><p><strong>outputs</strong> <code>array</code></p><p>代码执行输出数组。仅当 <code>type</code> 为 <code>code_interpreter_call</code> 时存在。每个元素包含 <code>type</code>（值为 <code>logs</code>）和 <code>logs</code>（代码执行日志）字段。</p><p><strong>container_id</strong> <code>string</code></p><p>代码解释器容器标识符。仅当 <code>type</code> 为 <code>code_interpreter_call</code> 时存在。用于关联同一会话中的多次代码执行。</p><p><strong>goal</strong> <code>string</code></p><p>抽取目标描述，说明需要从网页中提取哪些信息。仅当 <code>type</code> 为 <code>web_extractor_call</code> 时存在。</p><p><strong>output</strong> <code>string</code></p><p>工具调用的输出结果，字符串格式。</p><ul><li>当 <code>type</code> 为 <code>web_extractor_call</code> 时为网页抽取的内容摘要</li><li>当 <code>type</code> 为 <code>web_search_image_call</code> 或 <code>image_search_call</code> 时为 JSON 字符串，包含图片搜索结果数组，每个元素包含 <code>title</code>（图片标题）、<code>url</code>（图片 URL）和 <code>index</code>（序号）字段</li><li>当 <code>type</code> 为 <code>mcp_call</code> 时为 MCP 服务返回的 JSON 字符串结果。</li></ul><p><strong>urls</strong> <code>array</code></p><p>被抽取的网页 URL 列表。仅当 <code>type</code> 为 <code>web_extractor_call</code> 时存在。</p><p><strong>server_label</strong> <code>string</code></p><p>MCP 服务标签。仅当 <code>type</code> 为 <code>mcp_call</code> 时存在。标识本次调用所使用的 MCP 服务。</p><p><strong>queries</strong> <code>array</code></p><p>知识库检索使用的查询列表。仅当 <code>type</code> 为 <code>file_search_call</code> 时存在。数组元素为字符串，表示模型生成的搜索查询词。</p><p><strong>results</strong> <code>array</code></p><p>知识库检索结果数组。仅当 <code>type</code> 为 <code>file_search_call</code> 时存在。</p><a id="accordion-数组元素属性-3"></a><section><p>数组元素属性</p><div><p><strong>file_id</strong> <code>string</code></p><p>匹配文档的文件 ID。</p><p><strong>filename</strong> <code>string</code></p><p>匹配文档的文件名。</p><p><strong>score</strong> <code>float</code></p><p>匹配相关度评分，取值范围 0-1，值越大表示相关度越高。</p><p><strong>text</strong> <code>string</code></p><p>匹配到的文档内容片段。</p></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>本次请求的 Token 消耗信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入的 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为 input_tokens 与 output_tokens 的总和。</p><p><strong>input_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>cached_tokens</strong> <code>integer</code></p><p>命中缓存的 Token 数。</p></div></section><p><strong>output_tokens_details</strong> <code>object</code></p><p>输出 Token 的细粒度分类。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>思考过程 Token 数。</p></div></section><p><strong>x_details</strong> <code>array</code></p><p>计费明细数组。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>本计费类型的输入 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>本计费类型的输出 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>本计费类型的总 Token 数。</p><p><strong>x_billing_type</strong> <code>string</code></p><p>固定为<code>response_api</code>。</p><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>启用 Session 缓存后返回。包含 <code>cached_tokens</code>（命中缓存的 Token 数）字段。</p></div></section><p><strong>x_tools</strong> <code>object</code></p><p>工具使用统计信息。当使用内置工具时，包含各工具的调用次数。示例：<code>{&quot;web_search&quot;: {&quot;count&quot;: 1}}</code></p></div></section><p><strong>tools</strong> <code>array</code></p><p>回显原创建响应请求中 <code>tools</code> 参数的完整内容。结构与请求体中的 <code>tools</code> 参数相同。无工具时为空数组 <code>[]</code>。</p><p><strong>tool_choice</strong> <code>string</code></p><p>回显原创建响应请求中 <code>tool_choice</code> 参数的值。枚举值：<code>auto</code>、<code>none</code>、<code>required</code>。</p><p><strong>parallel_tool_calls</strong> <code>boolean</code></p><p>回显原创建响应请求中 <code>parallel_tool_calls</code> 参数的值，表示是否允许模型并行调用多个工具。</p><p><strong>temperature</strong> <code>float</code></p><p>回显原创建响应请求中 <code>temperature</code> 参数的值。采样温度，控制模型生成文本的多样性，取值范围 [0, 2)。未设置时返回模型默认值。</p><p><strong>top_p</strong> <code>float</code></p><p>回显原创建响应请求中 <code>top_p</code> 参数的值。核采样的概率阈值，取值范围 (0, 1.0]。未设置时返回模型默认值。</p><p><strong>frequency_penalty</strong> <code>float</code></p><p>回显原创建响应请求中 <code>frequency_penalty</code> 参数的值。频率惩罚系数，正值降低重复用词的概率。</p><p><strong>presence_penalty</strong> <code>float</code></p><p>回显原创建响应请求中 <code>presence_penalty</code> 参数的值。存在惩罚系数，正值增加生成新主题的概率。</p><p><strong>top_logprobs</strong> <code>integer</code></p><p>回显原创建响应请求中 <code>top_logprobs</code> 参数的值。每个位置返回的最可能 Token 数量。未启用时为 <code>0</code>。</p><p><strong>store</strong> <code>boolean</code></p><p>回显原创建响应请求中 <code>store</code> 参数的值。<code>true</code> 表示该响应已储存，可被 <code>previous_response_id</code> 引用；<code>false</code> 表示未储存。</p><p><strong>service_tier</strong> <code>string</code></p><p>服务等级，固定为 <code>default</code>。</p><p><strong>background</strong> <code>boolean</code></p><p>是否为后台异步执行的响应。当前百炼仅支持同步调用，固定为 <code>false</code>。</p><p><strong>metadata</strong> <code>object</code></p><p>回显原创建响应请求中 <code>metadata</code> 参数的内容。可用于附加自定义键值对的对象，无设置时为空对象 <code>{}</code>。</p></td><td><div><a id="code-block"></a><pre class="language-json"><code>{
    &quot;background&quot;: false,
    &quot;completed_at&quot;: 1778676420,
    &quot;created_at&quot;: 1778676418,
    &quot;frequency_penalty&quot;: 0.0,
    &quot;id&quot;: &quot;resp_801bc2c4-93d9-910f-b35d-5274f5a737c1&quot;,
    &quot;metadata&quot;: {},
    &quot;model&quot;: &quot;qwen-plus&quot;,
    &quot;object&quot;: &quot;response&quot;,
    &quot;output&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;annotations&quot;: [],
                    &quot;text&quot;: &quot;你好！很高兴见到你。有什么我可以帮助你的吗？&quot;,
                    &quot;type&quot;: &quot;output_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_8c54756c-9b65-4a95-81d7-4276d91406db&quot;,
            &quot;role&quot;: &quot;assistant&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        }
    ],
    &quot;parallel_tool_calls&quot;: true,
    &quot;presence_penalty&quot;: 0.0,
    &quot;service_tier&quot;: &quot;default&quot;,
    &quot;status&quot;: &quot;completed&quot;,
    &quot;store&quot;: true,
    &quot;temperature&quot;: 1.0,
    &quot;tool_choice&quot;: &quot;auto&quot;,
    &quot;tools&quot;: [],
    &quot;top_logprobs&quot;: 0,
    &quot;top_p&quot;: 1.0,
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 45,
        &quot;input_tokens_details&quot;: {
            &quot;cached_tokens&quot;: 0
        },
        &quot;output_tokens&quot;: 63,
        &quot;output_tokens_details&quot;: {
            &quot;reasoning_tokens&quot;: 0
        },
        &quot;total_tokens&quot;: 108,
        &quot;x_details&quot;: [
            {
                &quot;input_tokens&quot;: 45,
                &quot;output_tokens&quot;: 63,
                &quot;prompt_tokens_details&quot;: {
                    &quot;cached_tokens&quot;: 0
                },
                &quot;total_tokens&quot;: 108,
                &quot;x_billing_type&quot;: &quot;response_api&quot;
            }
        ]
    }
}
</code></pre></div></td></tr></tbody></table>

<a id="错误响应"></a>

<a id="retrieve-error-h2"></a>

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
