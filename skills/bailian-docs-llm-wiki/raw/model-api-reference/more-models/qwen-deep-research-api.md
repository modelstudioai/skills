# Qwen-Deep-Research API 参考

本文介绍通过 DashScope API 调用 Qwen-Deep-Research 模型的输入与输出参数。

> 相关文档：[深入研究（Qwen-Deep-Research）](../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-deep-research.md)

> **重要**
>
> Qwen-Deep-Research模型仅支持华北2（北京）地域，如需使用模型，请使用华北2（北京）地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

> **说明**
>
> 模型当前仅支持通过 Python DashScope SDK 调用，暂不支持 Java SDK 与 OpenAI 兼容接口。

<a id="dashscope"></a>

<a id="c906e0db10vf1"></a>

## DashScope

> 您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过DashScope SDK进行调用，需要[安装DashScope SDK](../preparations/install-sdk.md)。

<table><tbody><tr><td><a id="2a1c410015otp"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型：qwen-deep-research。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>传递给大模型的上下文，按对话顺序排列。</p><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文。在 Qwen-Deep-Research 的两阶段调用流程中，用户消息起到不同作用：</p><ul><li><strong>第一步（模型反问确认）</strong>：用户消息用于发起初始的研究请求，提出一个较为宽泛的研究主题。</li><li><strong>第二步（深入研究）</strong>：用户消息用于回答模型提出的澄清式问题，帮助模型聚焦研究方向，进行更具针对性的深入分析。</li></ul><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>消息内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>系统消息的角色，固定为user。</p></div></section><p>Assistant Message <code>object</code>（可选）</p><p>模型对用户消息的回复。在第二步（深入研究）的API调用中，此参数用以传入模型在第一步（反问确认）中返回的澄清式问题，作为对话历史的一部分，从而引导模型进行更具针对性的分析。</p><p><strong>content</strong><code>string</code>（可选）</p><p>消息内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>assistant</code>。</p></div></section><p><strong>output_format</strong><code>string</code>（可选）</p><p>指定输出研究报告的格式和详细程度。支持以下取值：</p><ul><li><code>model_detailed_report</code>（默认） 生成一份结构完整、内容详尽的深度研究报告，篇幅约6000 Token，适合需要全面深入分析的场景。</li><li><code>model_summary_report</code> 生成一份核心观点突出、内容精炼的摘要式研究报告，篇幅约1500-2000 Token，适合快速了解关键信息和结论的场景。</li></ul></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;

# 第一步：模型反问确认
messages = [{'role': 'user', 'content': '研究一下人工智能在教育中的应用'}]

responses = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model=&quot;qwen-deep-research&quot;,
    messages=messages,
    stream=True
)

# 获取模型反问内容
step1_content = &quot;&quot;
for response in responses:
    if hasattr(response, 'output') and response.output:
        message = response.output.get('message', {})
        content = message.get('content', '')
        if content:
            step1_content += content
            print(content, end='', flush=True)

# 第二步：深入研究
messages = [
    {'role': 'user', 'content': '研究一下人工智能在教育中的应用'},
    {'role': 'assistant', 'content': step1_content},
    {'role': 'user', 'content': '我主要关注个性化学习和智能评估这两个方面'}
]

responses = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model=&quot;qwen-deep-research&quot;,
    messages=messages
)

# 流式输出研究结果
for response in responses:
    if hasattr(response, 'output') and response.output:
        message = response.output.get('message', {})
        content = message.get('content', '')
        if content:
            print(content, end='', flush=True)
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>echo &quot;第一步：模型反问确认&quot;
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'X-DashScope-SSE: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;content&quot;: &quot;研究一下人工智能在教育中的应用&quot;,
                &quot;role&quot;: &quot;user&quot;
            }
        ]
    },
    &quot;model&quot;: &quot;qwen-deep-research&quot;
}'

echo -e &quot;\n\n&quot;
echo &quot;第二步：深入研究&quot;
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
--header 'X-DashScope-SSE: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;content&quot;: &quot;研究一下人工智能在教育中的应用&quot;,
                &quot;role&quot;: &quot;user&quot;
            },
            {
                &quot;content&quot;: &quot;请告诉我您希望重点研究人工智能在教育中的哪些具体应用场景？&quot;,
                &quot;role&quot;: &quot;assistant&quot;
            },
            {
                &quot;content&quot;: &quot;我主要关注个性化学习方面&quot;,
                &quot;role&quot;: &quot;user&quot;
            }
        ]
    },
    &quot;model&quot;: &quot;qwen-deep-research&quot;
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h3>响应对象</h3><p><strong>status_code</strong><code>string</code></p><p>本次请求的状态码。200 表示请求成功，否则表示请求失败。</p><blockquote><p>调用失败会抛出异常，异常信息为<strong>status_code</strong>和<strong>message</strong>的内容。</p></blockquote><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>code</strong><code>string</code></p><p>错误码，调用成功时为空值。</p><blockquote><p>只有Python SDK返回该参数。</p></blockquote><p><strong>message</strong> <code>string</code></p><p>错误提示信息，调用成功时为空值。</p><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>finish_reason</strong><code>string</code></p><p>模型结束生成的原因。有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code></li></ul><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>因模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code></li></ul></div></section><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><strong>属性</strong><p><strong>phase</strong><code>string</code></p><p>当前所处阶段，其中包含：</p><ul><li>answer：反问确认与回答阶段;</li><li>ResearchPlanning：研究规划阶段</li><li>WebResearch：网络搜索阶段</li><li>KeepAlive：连接保持阶段</li></ul><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>string</code></p><p>模型的输出内容。</p><p><strong>extra</strong> <code>array</code></p><p>模型获取的网络搜索与参考信息。</p><p><strong>deep_research</strong><code>object</code></p><p>仅在<code>answer</code>与<code>WebResearch</code>阶段包含获取的网络搜索与参考信息，其余阶段均为null。</p><p><strong>research</strong><code>object</code></p><p>模型的研究过程与内容信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>researchGoal</strong><code>string</code></p><p>研究目标。</p><p><strong>query</strong><code>string</code></p><p>研究过程中的搜索内容。</p><p><strong>id</strong><code>integer</code></p><p>搜索的轮数*，*取值范围 [1-15]。</p><p><strong>learningMap</strong><code>object</code></p><p>从调用工具总结获取到的内容，和调用工具相关联。</p><p><strong>references</strong><code>object</code></p><p>模型生成答案所引用的内容，仅回答阶段包含此参数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>icon</strong> <code>string</code></p><p>参考内容URL的网页图标链接。</p><p><strong>index_number</strong> <code>integer</code></p><p>参考内容的索引。</p><p><strong>description</strong><code>string</code></p><p>参考内容的简介。</p><p><strong>title</strong><code>string</code></p><p>参考内容的网页标题。</p><p><strong>url</strong> <code>string</code></p><p>参考内容的网页URL。</p></div></section><p><strong>webSites</strong><code>object</code></p><p>模型研究过程中所参考的内容，仅网络搜索阶段包含此参数。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>icon</strong> <code>string</code></p><p>参考内容URL的网页图标链接。</p><p><strong>index_number</strong> <code>integer</code></p><p>参考内容的索引。</p><p><strong>description</strong><code>string</code></p><p>参考内容的简介。</p><p><strong>title</strong><code>string</code></p><p>参考内容的网页标题。</p><p><strong>url</strong> <code>string</code></p><p>参考内容的网页URL。</p></div></section></div></section><p><strong>status</strong><code>string</code></p><p>模型输出过程中不同阶段的状态：</p><ul><li>typing：正在生成该阶段内容。</li><li>finished：阶段已完成。</li><li>streamingQueries：正在生成研究目标和搜索查询</li><li>streamingWebResult：正在执行搜索、网页阅读和代码执行</li><li>WebResultFinished：网络搜索阶段完成</li></ul></div></section><p><strong>finished</strong><code>boolean</code></p><p>标识模型的内容流式输出是否已全部完成。有以下情况：</p><ul><li>内容仍在持续输出中为<code>false</code>；</li><li>内容已全部输出完毕，当前为最后一个响应为<code>true</code></li></ul><p><strong>finished_reason</strong> <code>string</code></p><p>标识模型的内容流式输出结束的原因。有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>模型内容流式输出自然结束为<code>stop</code></li></ul></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求使用的Token信息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数。</p></div></section></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-研究规划阶段-tab"></a>研究规划阶段<div><a id="code-code-group-2-研究规划阶段"></a><pre class="language-json"><code>{
  &quot;status_code&quot;: 200,
  &quot;request_id&quot;: &quot;2a6187f0-7e7b-40bb-a87e-xxx&quot;,
  &quot;code&quot;: &quot;&quot;,
  &quot;message&quot;: &quot;&quot;,
  &quot;output&quot;: {
        &quot;text&quot;: null,
        &quot;finish_reason&quot;: null,
        &quot;choices&quot;: null,
        &quot;message&quot;: {
            &quot;phase&quot;: &quot;ResearchPlanning&quot;,
            &quot;role&quot;: &quot;assistant&quot;,
            &quot;content&quot;: &quot;&quot;,
            &quot;extra&quot;: {
                &quot;deep_research&quot;: {}
            },
            &quot;status&quot;: &quot;typing&quot;
        },
        &quot;fininshed&quot;: false,
        &quot;fininshed_reason&quot;: &quot;null&quot;
    },
    &quot;usage&quot;: {
        &quot;input_tokens&quot;: 694,
        &quot;output_tokens&quot;: 0
    },
    &quot;request_id&quot;: &quot;2a6187f0-7e7b-40bb-xxx&quot;
}
</code></pre></div><a id="fig-code-group-2-网络搜索阶段-tab"></a>网络搜索阶段<div><a id="code-code-group-2-网络搜索阶段"></a><pre class="language-json"><code>{
  &quot;status_code&quot;: 200,
  &quot;request_id&quot;: &quot;2a6187f0-7e7b-40bb-a87e-xxx&quot;,
  &quot;code&quot;: &quot;&quot;,
  &quot;message&quot;: &quot;&quot;,
  &quot;output&quot;: {
    &quot;message&quot;: {
      &quot;phase&quot;: &quot;WebResearch&quot;,
      &quot;role&quot;: &quot;assistant&quot;,
      &quot;content&quot;: &quot;&quot;,
      &quot;extra&quot;: {
        &quot;deep_research&quot;: {
          &quot;query&quot;: {
            &quot;researchGoal&quot;: &quot;通过查找&quot;,
            &quot;query&quot;: &quot;&quot;,
            &quot;id&quot;: 1
          }
        }
      },
      &quot;status&quot;: &quot;streamingQueries&quot;
    },
    &quot;fininshed&quot;: false,
    &quot;fininshed_reason&quot;: &quot;null&quot;
  },
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 694,
    &quot;output_tokens&quot;: 0
  }
}
</code></pre></div><a id="fig-code-group-2-连接保持阶段-tab"></a>连接保持阶段<div><a id="code-code-group-2-连接保持阶段"></a><pre class="language-json"><code>{
  &quot;status_code&quot;: 200,
  &quot;request_id&quot;: &quot;2a6187f0-7e7b-40bb-a87e-xxx&quot;,
  &quot;code&quot;: &quot;&quot;,
  &quot;message&quot;: &quot;&quot;,
  &quot;output&quot;: {
    &quot;message&quot;: {
      &quot;phase&quot;: &quot;KeepAlive&quot;,
      &quot;role&quot;: &quot;assistant&quot;,
      &quot;content&quot;: &quot;&quot;,
      &quot;extra&quot;: {
        &quot;deep_research&quot;: {}
      },
      &quot;status&quot;: &quot;typing&quot;
    },
    &quot;fininshed&quot;: false,
    &quot;fininshed_reason&quot;: &quot;null&quot;
  },
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 694,
    &quot;output_tokens&quot;: 0
  }
}
</code></pre></div><a id="fig-code-group-2-反问确认与回答阶段-tab"></a>反问确认与回答阶段<div><a id="code-code-group-2-反问确认与回答阶段"></a><pre class="language-json"><code>{
  &quot;status_code&quot;: 200,
  &quot;request_id&quot;: &quot;2a6187f0-7e7b-40bb-a87e-xxx&quot;,
  &quot;code&quot;: &quot;&quot;,
  &quot;message&quot;: &quot;&quot;,
  &quot;output&quot;: {
    &quot;message&quot;: {
      &quot;phase&quot;: &quot;answer&quot;,
      &quot;role&quot;: &quot;assistant&quot;,
      &quot;content&quot;: &quot;，这些承诺相互&quot;,
      &quot;extra&quot;: {
        &quot;deep_research&quot;: {
          &quot;references&quot;: [
            {
              &quot;icon&quot;: &quot;&quot;,
              &quot;index_number&quot;: 1,
              &quot;description&quot;: &quot;计划中设想的两个xxx从未在 &quot;,
              &quot;title&quot;: &quot;历史和背景| 联合国 - the United Nations&quot;,
              &quot;url&quot;: &quot;https://www.un.org/xxx&quot;
            }
          ]
        }
      },
      &quot;status&quot;: &quot;typing&quot;
    },
    &quot;fininshed&quot;: false,
    &quot;fininshed_reason&quot;: &quot;null&quot;
  },
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 694,
    &quot;output_tokens&quot;: 0
  }
}
</code></pre></div></div></td></tr></tbody></table>
