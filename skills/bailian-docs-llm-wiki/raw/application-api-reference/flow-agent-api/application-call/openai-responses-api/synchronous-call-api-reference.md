# 同步调用 API 参考

本文介绍如何通过 OpenAI 兼容模式的 Responses API 同步调用 阿里云百炼应用（ 智能体 、 工作流 ）。适用于需要 即时获取结果 的实时交互场景，可轻松复用现有的 OpenAI 代码库，或快速集成来自 OpenAI 生态的各类工具。

**相关参考**

-   **异步调用**：对于**耗时较长**的任务（如生成报告、多步骤工具调用），为避免请求超时，请参阅[异步调用 API 参考](asynchronous-call-api-reference.md)。
-   **DashScope API**：如需获取更全面的功能与更高的性能，请参阅[工作流与旧版智能体应用 API应用 DashScope API 参考](../../../../_short/agent-and-workflow-application-api-reference-ab48d043a951dcb2.md)。

> **重要**
>
> 本文档仅适用于华北2（北京）地域。

<a id="前提条件"></a>

<a id="bcad59b409rk8"></a>

## 前提条件

-   已[获取 API Key](../../../../model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   已创建[阿里云百炼应用](../../../../application-user-guide/agent-development/llm-application/llm-application-start-using/flow-agent-introduction.md)，并已获取应用ID：在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面的应用卡片上复制其ID。
-   如果通过SDK调用，还需要[安装OpenAI Python SDK](../../../../model-api-reference/preparations/install-sdk.md)。

使用SDK调用时需配置的`base_url`：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1`

使用HTTP方式调用时需配置的`Endpoint`：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`

> **说明**
>
> 请将 `{APP_ID}` 替换为实际的应用ID。

<table><tbody><tr><td><a id="bf3821567es4j"></a><h3>请求体</h3><p><strong>app_id</strong> <em>string</em><strong>（必选）</strong></p><p>应用的标识。</p><p>在<a href="https://bailian.console.aliyun.com/#/app-center">应用管理</a>页面的应用卡片上获取应用ID。</p><blockquote><p>通过 HTTP 调用时，请将实际的应用ID放入 URL 中，替换<code>APP_ID</code>。</p></blockquote><p><strong>input</strong><code>string</code>/<code>array</code><strong>（必选）</strong></p><p>请求的核心输入内容。可以是一个简单的字符串，也可以是一个包含多轮对话历史的消息数组。</p><ul><li><p><strong>简单字符串</strong>: 用于单轮文本对话，例如 <code>&quot;你好&quot;</code>。</p></li><li><p><strong>消息数组 (Messages)</strong>： 用于多轮对话或包含多媒体（如图片、文件）的输入。数组中的每个元素都是一个消息对象。</p><div><div><p><strong>说明</strong>基于<code>pre_response_id</code>或<code>conversation_id</code>的上下文功能将在<strong>后续支持</strong>。目前请在每次请求时传递完整的对话历史。</p></div></div><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p><strong>System Message</strong><code>object</code>（可选）</p><p>系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在<code>messages</code>数组的第一位。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>消息内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>system</code>。</p></div></section><p><strong>User Message</strong><code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>content</strong><code>string 或 array</code><strong>（必选）</strong></p><p>消息内容。</p><ul><li><p><strong>纯文本输入</strong>: <code>content</code> 为字符串，例如 <code>&quot;你好&quot;</code>。</p></li><li><p><strong>多模态输入</strong>: <code>content</code> 为一个数组，包含文本、图片或文件对象。</p><a id="accordion-子属性"></a><section><p>子属性</p><div><strong>文本</strong><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_text</code>。</p><p><strong>text</strong> <code>string</code><strong>（必选）</strong></p><p>文本内容。</p><strong>图像</strong><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_image</code>。</p><p><strong>image_url</strong> <code>string</code><strong>（必选）</strong></p><p>图片的 URL。</p><strong>文件</strong><p>仅<strong>智能体应用</strong>支持文件传入。</p><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>固定为 <code>input_file</code>。</p><p><strong>file_url</strong> <code>string</code><strong>（必选）</strong></p><p>文件的URL。</p></div></section></li></ul><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>user</code>。</p></div></section><p><strong>Assistant Message</strong> <code>object</code>（可选）</p><p>模型对用户消息的回复。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code>（可选）</p><p>消息内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>固定为<code>assistant</code>。</p></div></section></div></section></li></ul><p><strong>stream</strong> <code>boolean</code>（可选）</p><p>是否流式输出回复。</p><ul><li>false（默认值）：模型生成完所有内容后一次性返回结果。</li><li>true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。</li></ul><p><strong>background</strong> <code>boolean</code>（可选）</p><p>是否以异步方式执行任务。</p><div><div><p><strong>说明</strong>异步调用暂不支持流式输出。</p></div></div><ul><li><code>false</code>（默认值）：同步。API将保持连接直到任务完成。</li><li><code>true</code>：异步。API将立即返回一个任务ID，可通过查询接口来获取结果。</li></ul></td><td><a id="sec-tabs"></a><section><a id="文本输入"></a><section><a id="文本输入-h4"></a><h4>文本输入</h4><strong>单轮对话</strong><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>python<div><a id="code-code-group-python"></a><pre class="language-python"><code>from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

response = client.responses.create(
   input=&quot;你是谁？&quot;,
)

print(response.model_dump_json(indent=2))
</code></pre></div><a id="fig-code-group-bash-tab"></a>bash<div><a id="code-code-group-bash"></a><pre class="language-bash"><code>curl --location &quot;https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses&quot; \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer ${DASHSCOPE_API_KEY}&quot; \
--data '{
    &quot;input&quot;: [
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;你是谁？&quot;
                }
            ]
        }
    ]
}'
</code></pre></div></div><strong>多轮对话</strong><p>将包含完整历史消息的消息对象数组传递给<code>input</code> 参数。</p><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

messages = [
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你是谁？&quot;},
    {&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: &quot;我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。&quot;},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你能做什么？&quot;}
]
response = client.responses.create(
    input=messages
)

# 打印完整的响应JSON对象
print(response.model_dump_json(indent=2))
</code></pre></div><a id="fig-code-group-2-bash-tab"></a>bash<div><a id="code-code-group-2-bash"></a><pre class="language-bash"><code>curl --location &quot;https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses&quot; \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer ${DASHSCOPE_API_KEY}&quot; \
--data '{
    &quot;input&quot;: [
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;你是谁？&quot;
                }
            ]
        },
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;assistant&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。&quot;
                }
            ]
        },
        {
            &quot;type&quot;: &quot;message&quot;,
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;你能做什么？&quot;
                }
            ]
        }
    ]
}'
</code></pre></div></div></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><p>在请求体中设置<code>stream</code>为<code>true</code>，以流式方式获取响应，实现实时展示生成内容的效果。</p><p><strong>应用配置：</strong>若应用类型为<strong>工作流</strong>，需在<strong>结束节点</strong>或<strong>流程输出节点</strong>中启用<strong>流式输出</strong>开关，并重新<strong>发布</strong>应用。</p><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

messages = [
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你是谁？&quot;},
    {&quot;role&quot;: &quot;assistant&quot;, &quot;content&quot;: &quot;我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。&quot;},
    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: &quot;你能做什么？&quot;}
]
# 设置 stream=True 来发起流式请求
stream = client.responses.create(
    input=messages,
    stream=True,
)

# 遍历并处理事件流
for chunk in stream:
    # 只输出文字内容
    if hasattr(chunk, 'delta') and chunk.delta:
        print(chunk.delta, end='', flush=True)
</code></pre></div><a id="fig-code-group-3-bash-tab"></a>bash<div><a id="code-code-group-3-bash"></a><pre class="language-bash"><code>curl --location &quot;https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses&quot; \
    --header 'Content-Type: application/json' \
    --header &quot;Authorization: Bearer ${DASHSCOPE_API_KEY}&quot; \
    --data '{
         &quot;input&quot;: [
             {
                 &quot;type&quot;: &quot;message&quot;,
                 &quot;role&quot;: &quot;user&quot;,
                 &quot;content&quot;: [
                     {
                         &quot;type&quot;: &quot;input_text&quot;,
                         &quot;text&quot;: &quot;你是谁？&quot;
                     }
                 ]
             },
             {
                 &quot;type&quot;: &quot;message&quot;,
                 &quot;role&quot;: &quot;assistant&quot;,
                 &quot;content&quot;: [
                     {
                         &quot;type&quot;: &quot;input_text&quot;,
                         &quot;text&quot;: &quot;我是一个AI助手，可以帮助你解答问题、提供信息和协助完成各种任务。&quot;
                     }
                 ]
             },
             {
                 &quot;type&quot;: &quot;message&quot;,
                 &quot;role&quot;: &quot;user&quot;,
                 &quot;content&quot;: [
                     {
                         &quot;type&quot;: &quot;input_text&quot;,
                         &quot;text&quot;: &quot;用不少于100字介绍一下你自己&quot;
                     }
                 ]
             }
         ],
         &quot;stream&quot;: true
     }'
</code></pre></div></div></section><a id="图像输入"></a><section><a id="图像输入-h4"></a><h4>图像输入</h4><p>在 <code>content</code> 数组中包含 <code>image_url</code> 对象，向模型提供图像的 URL，模型基于图像内容进行问答。</p><p><strong>智能体应用</strong>配置：需选用<a href="../../../../model-user-guide/model-experience/text-generation-model/vision.md">通义千问VL系列模型</a>，并将文件处理方式选为<strong>自定义处理</strong>，然后重新<strong>发布</strong>应用。</p><p><strong>工作流应用</strong>配置：需选用<a href="../../../../model-user-guide/model-experience/text-generation-model/vision.md">通义千问VL系列模型</a>，并将模型节点的模型入参变量填为<code>imageList</code>，然后重新<strong>发布</strong>应用。</p><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.responses.create(
    input=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                { &quot;type&quot;: &quot;input_text&quot;, &quot;text&quot;: &quot;这是什么&quot; },
                {
                    &quot;type&quot;: &quot;input_image&quot;,
                    &quot;image_url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;
                }
            ]
        }
    ]
)

# 打印完整的响应JSON对象
print(response.model_dump_json(indent=2))
</code></pre></div><a id="fig-code-group-4-bash-tab"></a>bash<div><a id="code-code-group-4-bash"></a><pre class="language-bash"><code>curl --location &quot;https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses&quot; \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer ${DASHSCOPE_API_KEY}&quot; \
--data '{
    &quot;input&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;这是什么&quot;
                },
                {
                    &quot;type&quot;: &quot;input_image&quot;,
                    &quot;image_url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg&quot;
                }
            ]
        }
    ]
}'
</code></pre></div></div></section><a id="文件输入"></a><section><a id="文件输入-h4"></a><h4>文件输入</h4><p>在 <code>content</code> 数组中包含 <code>input_file</code> 对象，向模型提供文件的 URL，模型基于文件中的内容进行问答。</p><p>仅<strong>智能体应用</strong>支持，应用内的文件处理方式需选择<strong>全文引用</strong>或<strong>切片检索</strong>。</p><p>相关文档：<a href="../../../../application-user-guide/agent-development/llm-application/file-q-a.md">文件问答</a>。</p><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>from openai import OpenAI
import os

# 若没有配置环境变量，可用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;。但不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
app_id='APP_ID' # 替换为实际的应用 ID
base_url = f'https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/'

# 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.responses.create(
    input=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;总结这个文件的内容。&quot;
                },
                {
                    &quot;type&quot;: &quot;input_file&quot;,
                    &quot;file_url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3&quot;
                }
            ]
        }
    ]
)

# 打印完整的响应JSON对象
print(response.model_dump_json(indent=2))
</code></pre></div><a id="fig-code-group-5-bash-tab"></a>bash<div><a id="code-code-group-5-bash"></a><pre class="language-bash"><code># 请将 {APP_ID} 替换为实际的应用ID
curl --location &quot;https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses&quot; \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer ${DASHSCOPE_API_KEY}&quot; \
--data '{
    &quot;input&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;input_text&quot;,
                    &quot;text&quot;: &quot;总结这个文件的内容。&quot;
                },
                {
                    &quot;type&quot;: &quot;input_file&quot;,
                    &quot;file_url&quot;: &quot;https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3&quot;
                }
            ]
        }
    ]
}'
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="aa1c81920140j"></a><h3>响应对象（非流式输出）</h3><p><strong>id</strong> <code>string</code><br>本次请求的唯一标识符（ID），可用于日志记录和问题追踪。</p><p><strong>object</strong><code>string</code></p><p>对象类型，对于本API，其值固定为 <code>response</code>。</p><p><strong>created_at</strong> <code>integer</code><br>响应创建时间的Unix时间戳（以秒为单位）。</p><p><strong>status</strong><code>string</code></p><p>整个响应任务的最终状态。<code>completed</code> 表示任务已成功结束。</p><p><strong>output</strong><code>array</code><br>一个数组，包含了模型生成的所有输出内容。</p><a id="accordion-子属性-2"></a><section><p>子属性</p><div><p><strong>output</strong> <strong>message</strong><code>object</code></p><p>包含了模型输出内容的消息对象。</p><a id="accordion-子属性-3"></a><section><p>子属性</p><div><p><strong>content</strong> <code>array</code><br>消息的核心内容数组，包含多种类型的内容块（如文本、代码、图片等）。</p><a id="accordion-子属性-4"></a><section><p>子属性</p><div><p><strong>text</strong> <code>string</code><br>模型实际生成的文本回复。</p><p><strong>type</strong> <code>string</code><br>内容块的类型。<code>output_text</code> 表示这是一个输出的文本块。</p></div></section><p><strong>id</strong> <code>string</code><br>此条输出消息的唯一ID。</p><p><strong>role</strong> <code>string</code><br>消息的角色。<code>assistant</code> 表示这条消息是由AI助手生成的。</p><p><strong>status</strong> <code>string</code><br>表示该条消息的生成状态。<code>completed</code> 表示该条消息已成功生成。</p><p><strong>type</strong> <code>string</code><br><code>output</code>数组中元素的类型。<code>message</code> 表示这是一个消息对象。</p></div></section></div></section></td><td><a id="code-block"></a><pre class="language-json"><code>{
    &quot;created_at&quot;: 1758624774,
    &quot;id&quot;: &quot;ce65e29a-3d14-4b21-a5c0-ac601f3af888&quot;,
    &quot;model&quot;: &quot;&quot;,
    &quot;object&quot;: &quot;response&quot;,
    &quot;output&quot;: [
        {
            &quot;content&quot;: [
                {
                    &quot;annotations&quot;: [
                    ],
                    &quot;text&quot;: &quot;我可以帮助你做很多事情，包括但不限于：\n\n1. **回答问题**：无论是科学、历史、文化、技术等领域的知识，我都可以尽力为你提供准确的信息。\n2. **写作帮助**：我可以帮你写文章、邮件、报告、故事、诗歌等，也可以进行润色和修改。\n3. **语言翻译**：我可以将文本从一种语言翻译成另一种语言。\n4. **学习辅导**：我可以帮助你理解复杂的概念，解答数学题、物理题等学科问题。\n5. **编程帮助**：我可以协助你编写代码、调试程序、解释算法等。\n6. **提供建议**：在生活、工作、学习等方面，我可以提供一些实用的建议和思路。\n7. **娱乐互动**：我可以讲笑话、玩文字游戏可以将进行简单的聊天互动。\n\n如果你有任何具体的需求或问题，随时告诉我，我会尽力帮助你！&quot;,
                    &quot;type&quot;: &quot;output_text&quot;
                }
            ],
            &quot;id&quot;: &quot;msg_f25e8129-a130-447c-8e03-3f2b148c4e1d&quot;,
            &quot;role&quot;: &quot;assistant&quot;,
            &quot;status&quot;: &quot;completed&quot;,
            &quot;type&quot;: &quot;message&quot;
        }
    ],
    &quot;parallel_tool_calls&quot;: false,
    &quot;status&quot;: &quot;completed&quot;,
    &quot;tool_choice&quot;: &quot;auto&quot;,
    &quot;tools&quot;: [
    ]
}
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="13ebf1c527c8d"></a><h3>响应对象（流式输出）</h3><p><strong>id</strong> <code>string</code></p><p>事件的消息ID。</p><p><strong>code</strong> <code>string</code></p><p>错误码，调用成功时为空值。</p><p><strong>message</strong><code>string</code></p><p>表示错误详细信息，请求成功则忽略。</p><p><strong>event</strong> <code>string</code></p><p>事件类型，表示当前响应的状态。</p><a id="accordion-事件通用数据"></a><section><p>事件通用数据</p><div><p><strong>sequence_number</strong> <code>integer</code></p><p>事件的序列号，从0开始递增。</p><p><strong>type</strong> <code>string</code></p><p>事件类型，与<code>event</code>内容相同。</p></div></section><a id="accordion-事件类型详解"></a><section><p>事件类型详解</p><div><a id="accordion-整体响应生命周期事件"></a><section><p>整体响应生命周期事件</p><div><p><strong>response.created</strong>: 表示响应已创建。</p><p><strong>response.in_progress</strong>: 表示响应处理中。</p><p><strong>response.completed</strong>: 响应完成。</p><a id="accordion-通用数据"></a><section><p>通用数据</p><div><p><strong>response</strong><code>object</code></p><p>响应对象，包含响应的详细信息*。*</p><a id="accordion-子属性-5"></a><section><p>子属性</p><div><p><strong>id</strong> <code>string</code></p><p>响应的唯一标识符。</p><p><strong>status</strong><code>string</code></p><p>响应的最终状态。</p><p><strong>object</strong><code>string</code></p><p>对象类型<strong>。</strong>固定值为 <code>&quot;response&quot;</code>。</p><p><strong>created_at</strong><code>integer</code><br>响应创建时间的Unix时间戳（以秒为单位）。</p><p><strong>output</strong> <code>array</code><br>输出内容列表。</p><a id="accordion-子属性-6"></a><section><p>子属性</p><div><p><strong>output</strong> <strong>message</strong><code>object</code></p><p>包含了模型输出内容的消息对象。</p><a id="accordion-子属性-7"></a><section><p>子属性</p><div><p><strong>id</strong><code>string</code></p><p>输出项的唯一标识符。</p><p><strong>type</strong> <code>string</code></p><p>输出项的类型。</p><ul><li><code>&quot;reasoning&quot;</code>: 模型的思考过程。</li><li><code>&quot;message&quot;</code>: 最终回复。</li></ul><p><strong>role</strong> <code>string</code></p><p>消息的角色。</p><p><strong>content</strong><code>array</code></p><p>输出内容部分的列表。</p><a id="accordion-子属性-8"></a><section><p>子属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容部分的类型。例如 <code>&quot;output_text&quot;</code> 表示这是一个文本部分。</p><p><strong>text</strong><code>string</code></p><p>文本内容。</p><p><strong>annotations</strong><code>array</code></p><p>注解列表。</p></div></section><p><strong>status</strong><code>string</code></p><p>响应的当前状态。</p></div></section></div></section></div></section></div></section></div></section><a id="accordion-内容构建事件"></a><section><p>内容构建事件</p><div><p><strong>response.output_item.added</strong>: 表示输出项已添加。</p><a id="accordion-子属性-9"></a><section><p>子属性</p><div><p><strong>output_index</strong><code>integer</code></p><p><code>item</code> 在 <code>output</code> 数组中的索引。</p><p><strong>item</strong><code>object</code></p><p>新增的输出项对象。</p><a id="accordion-子属性-10"></a><section><p>子属性</p><div><p><strong>output</strong> <strong>message</strong><code>object</code></p><p>包含了模型输出内容的消息对象。</p><a id="accordion-子属性-11"></a><section><p>子属性</p><div><p><strong>id</strong><code>string</code></p><p>输出项的唯一标识符。</p><p><strong>type</strong> <code>string</code></p><p>输出项的类型。</p><ul><li><code>&quot;reasoning&quot;</code>: 模型的思考过程。</li><li><code>&quot;message&quot;</code>: 最终回复。</li></ul><p><strong>role</strong> <code>string</code></p><p>消息的角色。</p><p><strong>content</strong><code>array</code></p><p>内容部分列表。</p><p><strong>status</strong><code>string</code></p><p>响应的当前状态。</p></div></section></div></section></div></section><p><strong>response.output_item.done</strong>: 输出项完成。</p><a id="accordion-子属性-12"></a><section><p>子属性</p><div><p><strong>output_index</strong><code>integer</code></p><p>已完成的 <code>item</code> 在 <code>output</code> 数组中的索引。</p><p><strong>item</strong><code>object</code></p><p>完整的输出项对象。</p><a id="accordion-子属性-13"></a><section><p>子属性</p><div><p><strong>id</strong><code>string</code></p><p>输出项的唯一标识符。</p><p><strong>type</strong> <code>string</code></p><p>输出项的类型。</p><ul><li><code>&quot;reasoning&quot;</code>: 模型的思考过程。</li><li><code>&quot;message&quot;</code>: 最终回复。</li></ul><p><strong>role</strong> <code>string</code></p><p>消息的角色。</p><p><strong>content</strong><code>array</code></p><p>输出内容部分的列表。</p><a id="accordion-子属性-14"></a><section><p>子属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容部分的类型。例如 <code>&quot;output_text&quot;</code> 表示这是一个文本部分。</p><p><strong>text</strong><code>string</code></p><p>文本内容。</p><p><strong>annotations</strong><code>array</code></p><p>注解列表。</p></div></section><p><strong>status</strong><code>string</code></p><p>响应的当前状态。</p></div></section></div></section><p><strong>response.content_part.added</strong>: 表示在一个输出项（如一条消息）中，新生成了一个内容块（如文本、图片等）。</p><a id="accordion-子属性-15"></a><section><p>子属性</p><div><p><strong>output_index</strong><code>integer</code></p><p>关联的 <code>response.output</code> 数组索引。</p><p><strong>content_index</strong><code>integer</code></p><p>关联的 <code>item.content</code> 数组索引。</p><p><strong>item_id</strong><code>string</code></p><p>关联的输出项ID。</p><p><strong>part</strong><code>object</code></p><p>新添加的内容部分对象。</p><a id="accordion-子属性-16"></a><section><p>子属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容部分的类型。例如 <code>&quot;output_text&quot;</code> 表示这是一个文本部分。</p><p><strong>text</strong> <code>string</code></p><p>文本内容。</p><p><strong>annotations</strong><code>array</code></p><p>注解列表。</p></div></section></div></section><p><strong>response.content_part.done</strong>: 内容部分完成。</p><a id="accordion-子属性-17"></a><section><p>子属性</p><div><p><strong>output_index</strong><code>integer</code></p><p>关联的 <code>response.output</code> 数组索引。</p><p><strong>content_index</strong><code>integer</code></p><p>关联的 <code>item.content</code> 数组索引。</p><p><strong>item_id</strong><code>string</code></p><p>关联的输出项ID。</p><p><strong>part</strong><code>object</code></p><p>新添加的内容部分对象。</p><a id="accordion-子属性-18"></a><section><p>子属性</p><div><p><strong>type</strong> <code>string</code></p><p>内容部分的类型。例如 <code>&quot;output_text&quot;</code> 表示这是一个文本部分。</p><p><strong>text</strong> <code>string</code></p><p>文本内容。</p><p><strong>annotations</strong><code>array</code></p><p>注解列表。</p></div></section></div></section></div></section><a id="accordion-文本流事件"></a><section><p>文本流事件</p><div><p><strong>response.output_text.delta</strong>：输出内容的文本增量。</p><a id="accordion-子属性-19"></a><section><p>子属性</p><div><p><strong>delta</strong> <code>string</code></p><p>输出文本的增量片段。</p><p><strong>output_index</strong><code>integer</code></p><p>关联的 <code>response.output</code> 数组索引。</p><p><strong>content_index</strong><code>integer</code></p><p>关联的 <code>item.content</code> 数组索引。</p><p><strong>item_id</strong><code>string</code></p><p>关联的输出项ID。</p></div></section><p><strong>response.output_text.done</strong>: 输出文本完成。</p><a id="accordion-子属性-20"></a><section><p>子属性</p><div><p><strong>text</strong> <code>String</code></p><p>完整的输出文本内容。</p><p><strong>output_index</strong><code>integer</code></p><p>关联的 <code>response.output</code> 数组索引。</p><p><strong>content_index</strong><code>integer</code></p><p>关联的 <code>item.content</code> 数组索引。</p><p><strong>item_id</strong><code>string</code></p><p>关联的输出项ID。</p></div></section><p><strong>response.reasoning_text.delta</strong>：思考过程的文本增量。</p><a id="accordion-子属性-21"></a><section><p>子属性</p><div><p><strong>delta</strong> <code>string</code></p><p>思考文本的增量片段。</p><p><strong>output_index</strong><code>integer</code></p><p>关联的 <code>response.output</code> 数组索引。</p><p><strong>content_index</strong><code>integer</code></p><p>关联的 <code>item.content</code> 数组索引。</p><p><strong>item_id</strong><code>string</code></p><p>关联的输出项ID。</p></div></section><p><strong>response.reasoning_text.done</strong>：思考过程的流式输出已全部结束。</p><a id="accordion-子属性-22"></a><section><p>子属性</p><div><p><strong>text</strong> <code>String</code></p><p>完整的思考过程。</p><p><strong>output_index</strong><code>integer</code></p><p>关联的 <code>response.output</code> 数组索引。</p><p><strong>content_index</strong><code>integer</code></p><p>关联的 <code>item.content</code> 数组索引。</p><p><strong>item_id</strong><code>string</code></p><p>关联的输出项ID。</p></div></section></div></section></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>id:1 | event:response.created | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:0,&quot;type&quot;:&quot;response.created&quot;,&quot;response&quot;:{&quot;output&quot;:[],&quot;parallel_tool_calls&quot;:false,&quot;created_at&quot;:1760076609,&quot;tool_choice&quot;:&quot;auto&quot;,&quot;model&quot;:&quot;&quot;,&quot;id&quot;:&quot;508f1306-3760-49da-9e43-380fd952c297&quot;,&quot;tools&quot;:[],&quot;object&quot;:&quot;response&quot;,&quot;status&quot;:&quot;queued&quot;}}
id:2 | event:response.in_progress | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:1,&quot;type&quot;:&quot;response.in_progress&quot;,&quot;response&quot;:{&quot;output&quot;:[],&quot;parallel_tool_calls&quot;:false,&quot;created_at&quot;:1760076609,&quot;tool_choice&quot;:&quot;auto&quot;,&quot;model&quot;:&quot;&quot;,&quot;id&quot;:&quot;508f1306-3760-49da-9e43-380fd952c297&quot;,&quot;tools&quot;:[],&quot;object&quot;:&quot;response&quot;,&quot;status&quot;:&quot;in_progress&quot;}}
id:3 | event:response.output_item.added | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:2,&quot;item&quot;:{&quot;id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;role&quot;:&quot;assistant&quot;,&quot;type&quot;:&quot;message&quot;,&quot;content&quot;:[],&quot;status&quot;:&quot;in_progress&quot;},&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_item.added&quot;}
id:4 | event:response.content_part.added | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:3,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.content_part.added&quot;,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;part&quot;:{&quot;type&quot;:&quot;output_text&quot;,&quot;annotations&quot;:[],&quot;text&quot;:&quot;&quot;}}
id:5 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:4,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;你好&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:6 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:5,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;！我是通&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:7 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:6,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;义千问&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:8 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:7,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;（Qwen&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:9 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:8,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;），由阿里云研发的&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:10 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:9,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;超大规模语言模型。我&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:11 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:10,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;能够回答问题、创作文字&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:12 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:11,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;，比如写故事、写&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:13 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:12,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;公文、写邮件、&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:14 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:13,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;写剧本、逻辑推理、&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:15 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:14,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;编程等等，还能表达观点&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:16 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:15,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;，玩游戏等。我支持&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:17 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:16,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;多种语言，包括但不限于&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:18 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:17,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;中文、英文、德语&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:19 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:18,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;、法语、西班牙语&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:20 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:19,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;等，满足国际&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:21 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:20,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;化的使用需求。我&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:22 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:21,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;擅长处理各种任务&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:23 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:22,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;，无论是专业领域的&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:24 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:23,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;知识问答，还是&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:25 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:24,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;日常生活中的问题咨询&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:26 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:25,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;，我都会尽力提供帮助&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:27 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:26,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;。我的目标是成为&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:28 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:27,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;你最可靠的智能&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:29 | event:response.output_text.delta | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:28,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;delta&quot;:&quot;伙伴！&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.delta&quot;,&quot;logprobs&quot;:[]}
id:30 | event:response.output_text.done | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:29,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;text&quot;:&quot;你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！&quot;,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_text.done&quot;,&quot;logprobs&quot;:[]}
id:31 | event:response.content_part.done | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:30,&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.content_part.done&quot;,&quot;content_index&quot;:0,&quot;item_id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;part&quot;:{&quot;type&quot;:&quot;output_text&quot;,&quot;annotations&quot;:[],&quot;text&quot;:&quot;你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！&quot;}}
id:32 | event:response.output_item.done | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:31,&quot;item&quot;:{&quot;id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;role&quot;:&quot;assistant&quot;,&quot;type&quot;:&quot;message&quot;,&quot;content&quot;:[{&quot;type&quot;:&quot;output_text&quot;,&quot;annotations&quot;:[],&quot;text&quot;:&quot;你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！&quot;}],&quot;status&quot;:&quot;completed&quot;},&quot;output_index&quot;:0,&quot;type&quot;:&quot;response.output_item.done&quot;}
id:33 | event:response.completed | :HTTP_STATUS/200 | data:{&quot;sequence_number&quot;:32,&quot;type&quot;:&quot;response.completed&quot;,&quot;response&quot;:{&quot;output&quot;:[{&quot;id&quot;:&quot;msg_8087bfdd-ba53-45db-b309-6a3b92ca4f3e&quot;,&quot;role&quot;:&quot;assistant&quot;,&quot;type&quot;:&quot;message&quot;,&quot;content&quot;:[{&quot;type&quot;:&quot;output_text&quot;,&quot;annotations&quot;:[],&quot;text&quot;:&quot;你好！我是通义千问（Qwen），由阿里云研发的超大规模语言模型。我能够回答问题、创作文字，比如写故事、写公文、写邮件、写剧本、逻辑推理、编程等等，还能表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等，满足国际化的使用需求。我擅长处理各种任务，无论是专业领域的知识问答，还是日常生活中的问题咨询，我都会尽力提供帮助。我的目标是成为你最可靠的智能伙伴！&quot;}],&quot;status&quot;:&quot;completed&quot;}],&quot;parallel_tool_calls&quot;:false,&quot;created_at&quot;:1760076609,&quot;tool_choice&quot;:&quot;auto&quot;,&quot;model&quot;:&quot;&quot;,&quot;id&quot;:&quot;508f1306-3760-49da-9e43-380fd952c297&quot;,&quot;tools&quot;:[],&quot;object&quot;:&quot;response&quot;,&quot;status&quot;:&quot;completed&quot;}}
</code></pre></td></tr></tbody></table>

<a id="常见问题"></a>

<a id="ee8d61ccf2yyp"></a>

## 常见问题

1.  **如何传递多轮对话的上下文？**
    
    需要在客户端维护完整的对话历史，并在每次请求时将所有历史消息完整地放在`input`数组中传递给API。
    
    基于`pre_response_id`或`conversation_id`的上下文功能将在**后续支持**。
    
2.  **为什么响应示例中的某些字段未在本文说明？**
    
    如果使用OpenAI的官方SDK，它可能会根据其自身的模型结构打印出一些额外的字段（通常为`null`）。这些字段是OpenAI协议本身定义的，我们的服务当前不支持，所以它们为空值。只需关注本文档中描述的字段即可。
    

<a id="错误码"></a>

<a id="1f1a8d78e3wck"></a>

## 错误码

如果应用调用失败并返回报错信息，请参阅[错误码](../../../../model-api-reference/preparations/error-code.md)解决。
