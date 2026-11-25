# GUI-Plus API参考

本文介绍通过 OpenAI 兼容接口 或 DashScope API 调用GUI-Plus模型的输入与输出参数。

> 相关文档：[界面交互专用模型（GUI-Plus）](../../model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)

<a id="openai-兼容"></a>

<a id="d397bcc41eu3q"></a>

## OpenAI 兼容

SDK 调用配置的`base_url`为：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

> 您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK进行调用，需要[安装SDK](../preparations/install-sdk.md)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型：gui-plus。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong>传递给大模型的上下文，按对话顺序排列。</p><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在<code>messages</code>数组的第一位。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>系统消息的角色，固定为<code>system</code>。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>content</strong><code>array</code><strong>（必选）</strong></p><p>消息内容。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>可选值：</p><ul><li><p><code>text</code></p><p>输入文本时需设为<code>text</code>。</p></li><li><p><code>image_url</code></p><p>输入图片时需设为<code>image_url</code>。</p></li></ul><p><strong>text</strong><code>string</code><strong>（可选）</strong></p><p>输入的文本。当<code>type</code>为<code>text</code>时，是必选参数。</p><p><strong>image_url</strong><code>object</code></p><p>输入的图片信息。当<code>type</code>为<code>image_url</code>时是必选参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code><strong>（必选）</strong></p><p>图片的 URL或 Base64 Data URL。传入本地文件请参考<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">传入本地文件</a>。</p></div></section><p><strong>min_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最小像素阈值，单位为像素。</p><p>当输入图像像素小于<code>min_pixels</code>时，会将图像进行放大，直到总像素高于<code>min_pixels</code>。</p><p>默认值和最小值均为 3136 。</p><p><strong>max_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最大像素阈值，单位为像素。</p><p>当输入图像像素在<code>[min_pixels, max_pixels]</code>区间内时，模型会按原图进行识别。当输入图像像素大于<code>max_pixels</code>时，会将图像进行缩小，直到总像素低于<code>max_pixels</code>。</p><p>默认值和最大值和<a href="gui-plus-interface-interaction-model.md">vl_high_resolution_images</a>的取值有关：</p><ul><li>当 <a href="gui-plus-interface-interaction-model.md">vl_high_resolution_images</a> 为False时：默认值为1003520 ，最大值为12845056</li><li>当 <a href="gui-plus-interface-interaction-model.md">vl_high_resolution_images</a> 为True时：max_pixels无效，输入图像的最大像素固定为12845056</li></ul></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section><p>Assistant Message <code>object</code>（可选）</p><p>模型的回复。通常用于在多轮对话中作为上下文回传给模型。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code>（必选）</p><p>模型回复的文本内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>助手消息的角色，固定为<code>assistant</code>。</p></div></section></div></section><p><strong>stream</strong><code>boolean</code>（可选） 默认值为 <code>false</code></p><p>是否以流式方式输出回复。</p><p>可选值：</p><ul><li><code>false</code>：等待模型生成完整回复后一次性返回。</li><li><code>true</code>：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。</li></ul><p><strong>stream_options</strong><code>object</code>（可选）</p><p>流式输出的配置项，仅在 <code>stream</code> 为 <code>true</code> 时生效。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>include_usage</strong><code>boolean</code>（可选）默认值为 <code>false</code></p><p>是否在<strong>最后一个数据块</strong>包含Token消耗信息。</p><p>可选值：</p><ul><li><code>true</code>：包含；</li><li><code>false</code>：不包含。</li></ul></div></section><p><strong>max_tokens</strong><code>integer</code>（可选）</p><p>用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。</p><p>默认值与最大值均为模型的最大输出长度，请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#0573ce495fnnf">模型选型</a>。</p><p><strong>vl_high_resolution_images</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否将输入图像的像素上限提升至 16384 Token 对应的像素值。</p><ul><li><code>vl_high_resolution_images为true</code>，使用固定分辨率策略，像素上限固定为<code>12845056</code>，忽略 <code>max_pixels</code> 设置，超过此分辨率时会将图像总像素缩小至此上限内。</li><li><code>vl_high_resolution_images</code>为<code>false</code>，像素上限由<code>max_pixels</code>决定，输入图像的像素超过<code>max_pixels</code>会将图像缩小至<code>max_pixels</code>内。模型的默认像素上限即<code>max_pixels</code>的默认值。</li></ul><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>使用混合思考（回复前既可思考也可不思考）模型时，是否开启思考模式。在界面交互系列模型中，仅<code>gui-plus-2026-02-26</code>为混合思考模型。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#bc67a9a2bd2of">图像与视频理解</a></p><p>可选值：</p><ul><li><p><code>true</code>：开启</p><blockquote><p>开启后，思考内容将通过<code>reasoning_content</code>字段返回。</p></blockquote></li><li><p><code>false</code>：不开启</p></li></ul><blockquote><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中。配置方式为：<code>extra_body={&quot;enable_thinking&quot;: xxx}</code>。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><p><strong>temperature</strong><code>float</code>（可选）默认值为0.01</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><p><strong>top_p</strong><code>float</code>（可选）默认值为0.01</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><p><strong>top_k</strong><code>integer</code>（可选）默认值为1</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;top_k&quot;: xxx}</code>；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。</p><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。</p><p><strong>presence_penalty</strong> <code>float</code>（可选）</p><p>控制模型生成文本时的内容重复度。默认值为1.5</p><p>取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。</p><p>在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。</p><a id="accordion-原理介绍"></a><section><p>原理介绍</p><div><p>如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。</p></div></section><a id="accordion-示例"></a><section><p>示例</p><div><p>提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”</p><p>参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。</p><p>参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。</p><p>参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。</p></div></section><p><strong>stop</strong><code>string 或 array</code>（可选）</p><p>用于指定停止词。当模型生成的文本中出现<code>stop</code> 指定的字符串或<code>token_id</code>时，生成将立即终止。</p><p>可传入敏感词以控制模型的输出。</p><blockquote><p>stop为数组时，不可将<code>token_id</code>和字符串同时作为元素输入，比如不可以指定为<code>[&quot;你好&quot;,104307]</code>。</p></blockquote></td><td><a id="sec-tabs"></a><section><a id="非流式输出"></a><section><a id="非流式输出-h4"></a><h4>非流式输出</h4><a id="sec-tabs-2"></a><section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><a id="code-block"></a><pre class="language-python"><code>import os
from openai import OpenAI

system_prompt = &quot;&quot;&quot;# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:
&lt;tools&gt;
{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;computer_use&quot;, &quot;description&quot;: &quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {&quot;action&quot;: {&quot;description&quot;: &quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.&quot;, &quot;enum&quot;: [&quot;key&quot;, &quot;type&quot;, &quot;mouse_move&quot;, &quot;left_click&quot;, &quot;left_click_drag&quot;, &quot;right_click&quot;, &quot;middle_click&quot;, &quot;double_click&quot;, &quot;triple_click&quot;, &quot;scroll&quot;, &quot;hscroll&quot;, &quot;wait&quot;, &quot;terminate&quot;, &quot;answer&quot;, &quot;interact&quot;], &quot;type&quot;: &quot;string&quot;}, &quot;keys&quot;: {&quot;description&quot;: &quot;Required only by `action=key`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;text&quot;: {&quot;description&quot;: &quot;Required only by `action=type`, `action=answer` and `action=interact`.&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;coordinate&quot;: {&quot;description&quot;: &quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;pixels&quot;: {&quot;description&quot;: &quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;time&quot;: {&quot;description&quot;: &quot;The seconds to wait. Required only by `action=wait`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;status&quot;: {&quot;description&quot;: &quot;The status of the task. Required only by `action=terminate`.&quot;, &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;success&quot;, &quot;failure&quot;]}}, &quot;required&quot;: [&quot;action&quot;], &quot;type&quot;: &quot;object&quot;}}}
&lt;/tools&gt;

For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:
&lt;tool_call&gt;
{&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}
&lt;/tool_call&gt;

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}.

Rules:
- Output exactly in the order: Action, &lt;tool_call&gt;.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.&quot;&quot;&quot;

messages = [
    {
        &quot;role&quot;: &quot;system&quot;,
        &quot;content&quot;: system_prompt
    },
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {&quot;type&quot;: &quot;image_url&quot;, &quot;image_url&quot;: {&quot;url&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;}},
            {&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;帮我打开浏览器&quot;}
        ]
    }
]

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

completion = client.chat.completions.create(
    model=&quot;gui-plus-2026-02-26&quot;,
    messages=messages,
    extra_body={&quot;vl_high_resolution_images&quot;: True}
)

print(completion.choices[0].message.content)
</code></pre></section><a id="node-js"></a><section><a id="node-js-h4"></a><h4>Node.js</h4><a id="code-block-2"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const systemPrompt = `# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:
&lt;tools&gt;
{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;computer_use&quot;, &quot;description&quot;: &quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {&quot;action&quot;: {&quot;description&quot;: &quot;The action to perform. The available actions are:\\n* \`key\`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* \`type\`: Type a string of text on the keyboard.\\n* \`mouse_move\`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`left_click\`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`left_click_drag\`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`right_click\`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`middle_click\`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`double_click\`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`triple_click\`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* \`scroll\`: Performs a scroll of the mouse scroll wheel.\\n* \`hscroll\`: Performs a horizontal scroll (mapped to regular scroll).\\n* \`wait\`: Wait specified seconds for the change to happen.\\n* \`terminate\`: Terminate the current task and report its completion status.\\n* \`answer\`: Answer a question.\\n* \`interact\`: Resolve the blocking window by interacting with the user.&quot;, &quot;enum&quot;: [&quot;key&quot;, &quot;type&quot;, &quot;mouse_move&quot;, &quot;left_click&quot;, &quot;left_click_drag&quot;, &quot;right_click&quot;, &quot;middle_click&quot;, &quot;double_click&quot;, &quot;triple_click&quot;, &quot;scroll&quot;, &quot;hscroll&quot;, &quot;wait&quot;, &quot;terminate&quot;, &quot;answer&quot;, &quot;interact&quot;], &quot;type&quot;: &quot;string&quot;}, &quot;keys&quot;: {&quot;description&quot;: &quot;Required only by \`action=key\`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;text&quot;: {&quot;description&quot;: &quot;Required only by \`action=type\`, \`action=answer\` and \`action=interact\`.&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;coordinate&quot;: {&quot;description&quot;: &quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by \`action=mouse_move\` and \`action=left_click_drag\`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;pixels&quot;: {&quot;description&quot;: &quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by \`action=scroll\` and \`action=hscroll\`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;time&quot;: {&quot;description&quot;: &quot;The seconds to wait. Required only by \`action=wait\`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;status&quot;: {&quot;description&quot;: &quot;The status of the task. Required only by \`action=terminate\`.&quot;, &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;success&quot;, &quot;failure&quot;]}}, &quot;required&quot;: [&quot;action&quot;], &quot;type&quot;: &quot;object&quot;}}}
&lt;/tools&gt;

For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:
&lt;tool_call&gt;
{&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}
&lt;/tool_call&gt;

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}.

Rules:
- Output exactly in the order: Action, &lt;tool_call&gt;.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.`;

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const messages = [
  {
    role: &quot;system&quot;,
    content: systemPrompt,
  },
  {
    role: &quot;user&quot;,
    content: [
      {
        type: &quot;image_url&quot;,
        image_url: {
          url: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;,
        },
      },
      { type: &quot;text&quot;, text: &quot;帮我打开浏览器&quot; },
    ],
  },
];

const completion = await client.chat.completions.create({
  model: &quot;gui-plus-2026-02-26&quot;,
  messages: messages,
  extra_body: { vl_high_resolution_images: true },
});

console.log(completion.choices[0].message.content);
</code></pre></section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><a id="code-block-3"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;model&quot;: &quot;gui-plus-2026-02-26&quot;,
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;system&quot;,
        &quot;content&quot;: &quot;# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:\n&lt;tools&gt;\n{\&quot;type\&quot;: \&quot;function\&quot;, \&quot;function\&quot;: {\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;description\&quot;: \&quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\&quot;, \&quot;parameters\&quot;: {\&quot;properties\&quot;: {\&quot;action\&quot;: {\&quot;description\&quot;: \&quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\&quot;, \&quot;enum\&quot;: [\&quot;key\&quot;, \&quot;type\&quot;, \&quot;mouse_move\&quot;, \&quot;left_click\&quot;, \&quot;left_click_drag\&quot;, \&quot;right_click\&quot;, \&quot;middle_click\&quot;, \&quot;double_click\&quot;, \&quot;triple_click\&quot;, \&quot;scroll\&quot;, \&quot;hscroll\&quot;, \&quot;wait\&quot;, \&quot;terminate\&quot;, \&quot;answer\&quot;, \&quot;interact\&quot;], \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;keys\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=key`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;text\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=type`, `action=answer` and `action=interact`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;coordinate\&quot;: {\&quot;description\&quot;: \&quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;pixels\&quot;: {\&quot;description\&quot;: \&quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;time\&quot;: {\&quot;description\&quot;: \&quot;The seconds to wait. Required only by `action=wait`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;status\&quot;: {\&quot;description\&quot;: \&quot;The status of the task. Required only by `action=terminate`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;, \&quot;enum\&quot;: [\&quot;success\&quot;, \&quot;failure\&quot;]}}, \&quot;required\&quot;: [\&quot;action\&quot;], \&quot;type\&quot;: \&quot;object\&quot;}}}\n&lt;/tools&gt;\n\nFor each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:\n&lt;tool_call&gt;\n{\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}\n&lt;/tool_call&gt;\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}.\n\nRules:\n- Output exactly in the order: Action, &lt;tool_call&gt;.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call.&quot;
      },
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;type&quot;: &quot;image_url&quot;,
            &quot;image_url&quot;: {
              &quot;url&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;
            }
          },
          {
            &quot;type&quot;: &quot;text&quot;,
            &quot;text&quot;: &quot;帮我打开浏览器&quot;
          }
        ]
      }
    ],
    &quot;vl_high_resolution_images&quot;: true
  }'
</code></pre><a id="accordion-返回结果"></a><section><p>返回结果</p><div><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;choices&quot;: [
    {
      &quot;message&quot;: {
        &quot;content&quot;: &quot;&lt;tool_call&gt;\n{\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;arguments\&quot;: {\&quot;action\&quot;: \&quot;left_click\&quot;, \&quot;coordinate\&quot;: [2530, 314]}}\n&lt;/tool_call&gt;&quot;,
        &quot;role&quot;: &quot;assistant&quot;
      },
      &quot;finish_reason&quot;: &quot;stop&quot;,
      &quot;index&quot;: 0,
      &quot;logprobs&quot;: null
    }
  ],
  &quot;object&quot;: &quot;chat.completion&quot;,
  &quot;usage&quot;: {
    &quot;prompt_tokens&quot;: 7750,
    &quot;completion_tokens&quot;: 36,
    &quot;total_tokens&quot;: 7786,
    &quot;prompt_tokens_details&quot;: {
      &quot;image_tokens&quot;: 6743,
      &quot;text_tokens&quot;: 1007
    },
    &quot;completion_tokens_details&quot;: {
      &quot;text_tokens&quot;: 36
    }
  },
  &quot;created&quot;: 1773133741,
  &quot;system_fingerprint&quot;: null,
  &quot;model&quot;: &quot;gui-plus&quot;,
  &quot;id&quot;: &quot;chatcmpl-8b375016-abb8-9791-856c-74b2825c22d5&quot;
}
</code></pre></div></section></section></section></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

system_prompt = &quot;&quot;&quot;# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:
&lt;tools&gt;
{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;computer_use&quot;, &quot;description&quot;: &quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {&quot;action&quot;: {&quot;description&quot;: &quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.&quot;, &quot;enum&quot;: [&quot;key&quot;, &quot;type&quot;, &quot;mouse_move&quot;, &quot;left_click&quot;, &quot;left_click_drag&quot;, &quot;right_click&quot;, &quot;middle_click&quot;, &quot;double_click&quot;, &quot;triple_click&quot;, &quot;scroll&quot;, &quot;hscroll&quot;, &quot;wait&quot;, &quot;terminate&quot;, &quot;answer&quot;, &quot;interact&quot;], &quot;type&quot;: &quot;string&quot;}, &quot;keys&quot;: {&quot;description&quot;: &quot;Required only by `action=key`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;text&quot;: {&quot;description&quot;: &quot;Required only by `action=type`, `action=answer` and `action=interact`.&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;coordinate&quot;: {&quot;description&quot;: &quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;pixels&quot;: {&quot;description&quot;: &quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;time&quot;: {&quot;description&quot;: &quot;The seconds to wait. Required only by `action=wait`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;status&quot;: {&quot;description&quot;: &quot;The status of the task. Required only by `action=terminate`.&quot;, &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;success&quot;, &quot;failure&quot;]}}, &quot;required&quot;: [&quot;action&quot;], &quot;type&quot;: &quot;object&quot;}}}
&lt;/tools&gt;

For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:
&lt;tool_call&gt;
{&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}
&lt;/tool_call&gt;

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}.

Rules:
- Output exactly in the order: Action, &lt;tool_call&gt;.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.&quot;&quot;&quot;

messages = [
    {
        &quot;role&quot;: &quot;system&quot;,
        &quot;content&quot;: system_prompt
    },
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {&quot;type&quot;: &quot;image_url&quot;, &quot;image_url&quot;: {&quot;url&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;}},
            {&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;帮我打开浏览器&quot;}
        ]
    }
]

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)

completion = client.chat.completions.create(
    model=&quot;gui-plus-2026-02-26&quot;,
    messages=messages,
    stream=True,
    stream_options={&quot;include_usage&quot;:True}
)
for chunk in completion:
    print(chunk.model_dump_json())
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from &quot;openai&quot;;

const systemPrompt = `# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:
&lt;tools&gt;
{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;computer_use&quot;, &quot;description&quot;: &quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {&quot;action&quot;: {&quot;description&quot;: &quot;The action to perform. The available actions are:\\n* \`key\`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* \`type\`: Type a string of text on the keyboard.\\n* \`mouse_move\`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`left_click\`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`left_click_drag\`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* \`right_click\`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`middle_click\`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`double_click\`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* \`triple_click\`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* \`scroll\`: Performs a scroll of the mouse scroll wheel.\\n* \`hscroll\`: Performs a horizontal scroll (mapped to regular scroll).\\n* \`wait\`: Wait specified seconds for the change to happen.\\n* \`terminate\`: Terminate the current task and report its completion status.\\n* \`answer\`: Answer a question.\\n* \`interact\`: Resolve the blocking window by interacting with the user.&quot;, &quot;enum&quot;: [&quot;key&quot;, &quot;type&quot;, &quot;mouse_move&quot;, &quot;left_click&quot;, &quot;left_click_drag&quot;, &quot;right_click&quot;, &quot;middle_click&quot;, &quot;double_click&quot;, &quot;triple_click&quot;, &quot;scroll&quot;, &quot;hscroll&quot;, &quot;wait&quot;, &quot;terminate&quot;, &quot;answer&quot;, &quot;interact&quot;], &quot;type&quot;: &quot;string&quot;}, &quot;keys&quot;: {&quot;description&quot;: &quot;Required only by \`action=key\`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;text&quot;: {&quot;description&quot;: &quot;Required only by \`action=type\`, \`action=answer\` and \`action=interact\`.&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;coordinate&quot;: {&quot;description&quot;: &quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by \`action=mouse_move\` and \`action=left_click_drag\`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;pixels&quot;: {&quot;description&quot;: &quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by \`action=scroll\` and \`action=hscroll\`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;time&quot;: {&quot;description&quot;: &quot;The seconds to wait. Required only by \`action=wait\`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;status&quot;: {&quot;description&quot;: &quot;The status of the task. Required only by \`action=terminate\`.&quot;, &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;success&quot;, &quot;failure&quot;]}}, &quot;required&quot;: [&quot;action&quot;], &quot;type&quot;: &quot;object&quot;}}}
&lt;/tools&gt;

For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:
&lt;tool_call&gt;
{&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}
&lt;/tool_call&gt;

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}.

Rules:
- Output exactly in the order: Action, &lt;tool_call&gt;.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.`;

const client = new OpenAI({
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

const messages = [
  {
    role: &quot;system&quot;,
    content: systemPrompt,
  },
  {
    role: &quot;user&quot;,
    content: [
      {
        type: &quot;image_url&quot;,
        image_url: {
          url: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;,
        },
      },
      { type: &quot;text&quot;, text: &quot;帮我打开浏览器&quot; },
    ],
  },
];

const openai = new OpenAI({
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;
});

async function main() {
  const response = await openai.chat.completions.create({
    model: &quot;gui-plus&quot;,
    messages: messages,
    stream:true,
    stream_options:{&quot;include_usage&quot;:true}
  });

    console.log(&quot;流式输出内容为：&quot;)
    for await (const chunk of response) {
        // 如果stream_options.include_usage为true，则最后一个chunk的choices字段为空数组，需要跳过（可以通过chunk.usage获取 Token 使用量）
        if (chunk.choices[0] &amp;&amp; chunk.choices[0].delta.content != null) {
          console.log(chunk.choices[0].delta.content);
        }
    }
}
main()
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;model&quot;: &quot;gui-plus-2026-02-26&quot;,
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;system&quot;,
        &quot;content&quot;: &quot;# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:\n&lt;tools&gt;\n{\&quot;type\&quot;: \&quot;function\&quot;, \&quot;function\&quot;: {\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;description\&quot;: \&quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\&quot;, \&quot;parameters\&quot;: {\&quot;properties\&quot;: {\&quot;action\&quot;: {\&quot;description\&quot;: \&quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\&quot;, \&quot;enum\&quot;: [\&quot;key\&quot;, \&quot;type\&quot;, \&quot;mouse_move\&quot;, \&quot;left_click\&quot;, \&quot;left_click_drag\&quot;, \&quot;right_click\&quot;, \&quot;middle_click\&quot;, \&quot;double_click\&quot;, \&quot;triple_click\&quot;, \&quot;scroll\&quot;, \&quot;hscroll\&quot;, \&quot;wait\&quot;, \&quot;terminate\&quot;, \&quot;answer\&quot;, \&quot;interact\&quot;], \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;keys\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=key`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;text\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=type`, `action=answer` and `action=interact`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;coordinate\&quot;: {\&quot;description\&quot;: \&quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;pixels\&quot;: {\&quot;description\&quot;: \&quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;time\&quot;: {\&quot;description\&quot;: \&quot;The seconds to wait. Required only by `action=wait`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;status\&quot;: {\&quot;description\&quot;: \&quot;The status of the task. Required only by `action=terminate`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;, \&quot;enum\&quot;: [\&quot;success\&quot;, \&quot;failure\&quot;]}}, \&quot;required\&quot;: [\&quot;action\&quot;], \&quot;type\&quot;: \&quot;object\&quot;}}}\n&lt;/tools&gt;\n\nFor each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:\n&lt;tool_call&gt;\n{\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}\n&lt;/tool_call&gt;\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}.\n\nRules:\n- Output exactly in the order: Action, &lt;tool_call&gt;.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call.&quot;
      },
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;type&quot;: &quot;image_url&quot;,
            &quot;image_url&quot;: {
              &quot;url&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;
            }
          },
          {
            &quot;type&quot;: &quot;text&quot;,
            &quot;text&quot;: &quot;帮我打开浏览器&quot;
          }
        ]
      }
    ],
    &quot;vl_high_resolution_images&quot;: true,
    &quot;stream&quot;:true,
    &quot;stream_options&quot;:{&quot;include_usage&quot;:true}
  }'
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h3>chat响应对象（非流式输出）</h3><p><strong>id</strong><code>string</code></p><p>本次请求的唯一标识符。</p><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>模型停止生成的原因。</p><p>有两种情况：</p><ul><li>自然停止输出时为<code>stop</code>；</li><li>生成长度过长而结束为<code>length</code>。</li></ul><p><strong>index</strong><code>integer</code></p><p>当前对象在<code>choices</code>数组中的索引。</p><p><strong>message</strong><code>object</code></p><p>模型输出的消息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>GUI任务的结果。</p><p><strong>refusal</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>audio</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>function_call</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>tool_calls</strong> <code>array</code></p><p>该参数当前固定为<code>null</code>。</p></div></section></div></section><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion</code>。</p><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>本次请求的 Token 消耗信息。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>模型输出Token的细粒度分类。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>accepted_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输出文本对应的 Token 数。</p><p><strong>rejected_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>模型输入的图像对应的 Token数。</p></div></section></div></section></td><td><a id="code-block-5"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;chatcmpl-ef17511a-aceb-4c47-8757-13a87af2152d&quot;,
  &quot;choices&quot;: [
    {
      &quot;finish_reason&quot;: &quot;stop&quot;,
      &quot;index&quot;: 0,
      &quot;logprobs&quot;: null,
      &quot;message&quot;: {
        &quot;content&quot;: &quot;```json\n{\&quot;thought\&quot;: \&quot;用户想要打开浏览器，我观察到屏幕截图中有一个Google Chrome的图标，其位置在右上角一排的最后一个。因此，下一步操作应该是点击这个Chrome浏览器图标来启动它。\&quot;, \&quot;action\&quot;: \&quot;click\&quot;, \&quot;parameters\&quot;: {\&quot;x\&quot;: 1086, \&quot;y\&quot;: 129}}\n```&quot;,
        &quot;refusal&quot;: null,
        &quot;role&quot;: &quot;assistant&quot;,
        &quot;annotations&quot;: null,
        &quot;audio&quot;: null,
        &quot;function_call&quot;: null,
        &quot;tool_calls&quot;: null
      }
    }
  ],
  &quot;created&quot;: 1763451557,
  &quot;model&quot;: &quot;gui-plus&quot;,
  &quot;object&quot;: &quot;chat.completion&quot;,
  &quot;service_tier&quot;: null,
  &quot;system_fingerprint&quot;: null,
  &quot;usage&quot;: {
    &quot;completion_tokens&quot;: 78,
    &quot;prompt_tokens&quot;: 2020,
    &quot;total_tokens&quot;: 2098,
    &quot;completion_tokens_details&quot;: {
      &quot;accepted_prediction_tokens&quot;: null,
      &quot;audio_tokens&quot;: null,
      &quot;reasoning_tokens&quot;: null,
      &quot;rejected_prediction_tokens&quot;: null,
      &quot;text_tokens&quot;: 78
    },
    &quot;prompt_tokens_details&quot;: {
      &quot;audio_tokens&quot;: null,
      &quot;cached_tokens&quot;: null,
      &quot;image_tokens&quot;: 1244,
      &quot;text_tokens&quot;: 776
    }
  }
}
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="e98e6b7aa5nb2"></a><h3>chat响应chunk对象（流式输出）</h3><p><strong>id</strong><code>string</code></p><p>本次调用的唯一标识符。每个chunk对象有相同的 id。</p><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。若设置<code>include_usage</code>参数为<code>true</code>，则在最后一个chunk中为空。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>delta</strong> <code>object</code></p><p>流式返回的输出内容。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>翻译结果，qwen-mt-flash为增量式更新，qwen-mt-plus为非增量式更新。</p><p><strong>function_call</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>refusal</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息对象的角色，只在第一个chunk中有值。</p></div></section><p><strong>finish_reason</strong> <code>string</code></p><p>模型停止生成的原因。有三种情况：</p><ul><li>自然停止输出时为<code>stop</code>；</li><li>生成未结束时为<code>null</code>；</li><li>生成长度过长而结束为<code>length</code>。</li></ul><p><strong>index</strong> <code>integer</code></p><p>当前响应在<code>choices</code>数组中的索引。</p></div></section><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。每个chunk有相同的时间戳。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion.chunk</code>。</p><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>本次请求消耗的Token。只在<code>include_usage</code>为<code>true</code>时，在最后一个chunk返回。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>模型输出Token的细粒度分类。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>accepted_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输出文本对应的 Token 数。</p><p><strong>rejected_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>模型输入的图像对应的 Token数。</p></div></section></div></section></td><td><a id="code-block-6"></a><pre class="language-json"><code>ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='', function_call=None, refusal=None, role='assistant', tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='```', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='json', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='\n{&quot;thought&quot;: &quot;', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
...
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=' 1086', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=', &quot;y&quot;:', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content=' 127', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason=None, index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-9f3c627a-b0fc-4160-a558-3cc2cc7aa988', choices=[Choice(delta=ChoiceDelta(content='}}\n```', function_call=None, refusal=None, role=None, tool_calls=None), finish_reason='stop', index=0, logprobs=None)], created=1763452343, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=None)
ChatCompletionChunk(id='chatcmpl-bdb03054-42a2-459b-8a7e-5b94b39626f2', choices=[], created=1763452463, model='gui-plus', object='chat.completion.chunk', service_tier=None, system_fingerprint=None, usage=CompletionUsage(completion_tokens=78, prompt_tokens=2020, total_tokens=2098, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=None, rejected_prediction_tokens=None, text_tokens=78), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=None, image_tokens=1244, text_tokens=776)))
</code></pre></td></tr></tbody></table>

<a id="dashscope"></a>

<a id="69cac67a477k2"></a>

## DashScope

-   HTTP 请求地址：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
-   SDK 调用：无需配置 `base_url`

> 您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过DashScope SDK进行调用，需要[安装DashScope SDK](../preparations/install-sdk.md)。

<table><tbody><tr><td><a id="2a1c410015otp"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型：gui-plus。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>传递给大模型的上下文，按对话顺序排列。</p><blockquote><p>通过HTTP调用时，请将<strong>messages</strong>放入 <strong>input</strong> 对象中。</p></blockquote><a id="accordion-消息类型-2"></a><section><p>消息类型</p><div><p>System Message<code>object</code>（可选）</p><p>系统消息，用于设定大模型的角色、语气、任务目标或约束条件等。一般放在<code>messages</code>数组的第一位。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code><strong>（必选）</strong></p><p>系统指令，用于明确模型的角色、行为规范、回答风格和任务约束等。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>系统消息的角色，固定为<code>system</code>。</p></div></section><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文等。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>content</strong><code>string 或 array</code><strong>（必选）</strong></p><p>消息内容。若输入只有文本，则为 string 类型；若输入包含图像数据，则为 array 类型。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>输入的文本。</p><p><strong>image</strong><code>string</code>（可选）</p><p>传入的图片文件。可以为图片的URL或本地路径。传入本地文件请参见<a href="../../model-user-guide/model-experience/text-generation-model/vision.md">传入本地文件</a>。</p><p>示例值：{&quot;image&quot;:&quot;<a href="https://xxxx.jpeg"></a><a href="https://xxxx.jpeg">https://xxxx.jpeg</a>&quot;,&quot;max-pixels&quot;:1280<em>28</em>28}</p><p><strong>min_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最小像素阈值，单位为像素。</p><p>当输入图像像素小于<code>min_pixels</code>时，会将图像进行放大，直到总像素高于<code>min_pixels</code>。</p><p>默认值和最小值均为 3136 。</p><p>与 image 参数一起使用，示例：{&quot;image&quot;:&quot;<a href="https://xxxx.jpeg"></a><a href="https://xxxx.jpeg">https://xxxx.jpeg</a>&quot;,&quot;min_pixels&quot;:3136}</p><p><strong>max_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最大像素阈值，单位为像素。</p><p>当输入图像像素在<code>[min_pixels, max_pixels]</code>区间内时，模型会按原图进行识别。当输入图像像素大于<code>max_pixels</code>时，会将图像进行缩小，直到总像素低于<code>max_pixels</code>。</p><p>默认值和最大值和<a href="gui-plus-interface-interaction-model.md">vl_high_resolution_images</a>的取值有关：</p><ul><li>当 <a href="gui-plus-interface-interaction-model.md">vl_high_resolution_images</a> 为False时：默认值为1003520 ，最大值为12845056</li><li>当 <a href="gui-plus-interface-interaction-model.md">vl_high_resolution_images</a> 为True时：max_pixels无效，输入图像的最大像素固定为12845056</li></ul><p>与 image 参数一起使用，示例：{&quot;image&quot;:&quot;<a href="https://xxxx.jpeg"></a><a href="https://xxxx.jpeg">https://xxxx.jpeg</a>&quot;,&quot;max_pixels&quot;:1003520 }</p></div></section></div></section><p>Assistant Message <code>object</code>（可选）</p><p>模型的回复。通常用于在多轮对话中作为上下文回传给模型。</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>content</strong><code>string</code>（必选）</p><p>模型回复的文本内容。</p><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>助手消息的角色，固定为<code>assistant</code>。</p></div></section></div></section><p><strong>vl_high_resolution_images</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否将输入图像的像素上限提升至 16384 Token 对应的像素值。</p><ul><li><code>vl_high_resolution_images为true</code>，使用固定分辨率策略，像素上限固定为<code>12845056</code>，忽略 <code>max_pixels</code> 设置，超过此分辨率时会将图像总像素缩小至此上限内。</li><li><code>vl_high_resolution_images</code>为<code>false</code>，像素上限由<code>max_pixels</code>决定，输入图像的像素超过<code>max_pixels</code>会将图像缩小至<code>max_pixels</code>内。模型的默认像素上限即<code>max_pixels</code>的默认值。</li></ul><p><strong>enable_thinking</strong> <code>boolean</code> （可选）</p><p>使用混合思考模型时，是否开启思考模式。在界面交互系列模型中，仅<code>gui-plus-2026-02-26</code>为混合思考模型。相关文档：<a href="../../model-user-guide/model-experience/text-generation-model/vision.md#bc67a9a2bd2of">图像与视频理解</a></p><p>可选值：</p><ul><li><p><code>true</code>：开启</p><blockquote><p>开启后，思考内容将通过<code>reasoning_content</code>字段返回。</p></blockquote></li><li><p><code>false</code>：不开启</p></li></ul><p>不同模型的默认值：<a href="../../model-user-guide/model-experience/text-generation-model/deep-thinking.md#78286fdc35hlw">支持的模型</a></p><blockquote><p>Java SDK 为enableThinking；通过HTTP调用时，请将 <strong>enable_thinking</strong> 放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>max_tokens</strong><code>integer</code>（可选）</p><p>用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。</p><p>默认值与最大值均为模型的最大输出长度，请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/machine-translation.md#154957e783dxk">模型选型</a>。</p><blockquote><p>Java SDK中为<strong>maxTokens</strong>*。*通过HTTP调用时，请将 <strong>max_tokens</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><blockquote><p>通过HTTP调用时，请将 <strong>seed</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>temperature</strong><code>float</code>（可选）默认值为0.01</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>通过HTTP调用时，请将 <strong>temperature</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>top_p</strong><code>float</code>（可选）默认值为0.01</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>Java SDK中为<strong>topP</strong>*。*通过HTTP调用时，请将 <strong>top_p</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。</p><blockquote><p>Java SDK中为<strong>repetitionPenalty</strong>*。*通过HTTP调用时，请将 <strong>repetition_penalty</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>presence_penalty</strong> <code>float</code>（可选）</p><p>控制模型生成文本时的内容重复度。默认值为1.5</p><p>取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。</p><p>在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。</p><a id="accordion-原理介绍-2"></a><section><p>原理介绍</p><div><p>如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。</p></div></section><a id="accordion-示例-2"></a><section><p>示例</p><div><p>提示词：把这句话翻译成中文“This movie is good. The plot is good, the acting is good, the music is good, and overall, the whole movie is just good. It is really good, in fact. The plot is so good, and the acting is so good, and the music is so good.”</p><p>参数值为2.0：这部电影很好。剧情很棒，演技棒，音乐也非常好听，总的来说，整部电影都好得不得了。实际上它真的很优秀。剧情非常精彩，演技出色，音乐也是那么的动听。</p><p>参数值为0.0：这部电影很好。剧情好，演技好，音乐也好，总的来说，整部电影都很好。事实上，它真的很棒。剧情非常好，演技也非常出色，音乐也同样优秀。</p><p>参数值为-2.0：这部电影很好。情节很好，演技很好，音乐也很好，总的来说，整部电影都很好。实际上，它真的很棒。情节非常好，演技也非常好，音乐也非常好。</p></div></section><p><strong>top_k</strong><code>integer</code>（可选）默认值为1</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;top_k&quot;: xxx}</code>；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。</p><blockquote><p>Java SDK中为<strong>topK</strong>*。*通过HTTP调用时，请将 <strong>top_k</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。</p><p><strong>stream</strong><code>boolean</code>（可选）</p><p>是否以流式方式输出回复。</p><p>可选值：</p><ul><li><code>false</code>：等待模型生成完整回复后一次性返回。</li><li><code>true</code>：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。</li></ul><blockquote><p>该参数仅支持Python SDK。通过Java SDK实现流式输出请通过<code>streamCall</code>接口调用；通过HTTP实现流式输出请在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</p></blockquote><p><strong>incremental_output</strong><code>boolean</code>（可选）默认为<code>false</code></p><p>在流式输出模式下是否开启增量输出。推荐您优先设置为<code>true</code>。</p><p>参数值：</p><ul><li>false：每次输出为当前已经生成的整个序列，最后一次输出为生成的完整结果。</li></ul><a id="code-block-7"></a><pre class="language-text"><code>I
I like
I like apple
I like apple.
</code></pre><ul><li>true（推荐）：增量输出，即后续输出内容不包含已输出的内容。您需要实时地逐个读取这些片段以获得完整的结果。</li></ul><a id="code-block-8"></a><pre class="language-text"><code>I
like
apple
.
</code></pre><blockquote><p>Java SDK中为<strong>incrementalOutput</strong>*。*通过HTTP调用时，请将 <strong>incremental_output</strong>放入 <strong>parameters</strong> 对象中；Python SDK 2.0 的流式输出始终为增量输出，无需设置该参数。</p></blockquote><p><strong>stop</strong><code>string 或 array</code>（可选）</p><p>用于指定停止词。当模型生成的文本中出现<code>stop</code> 指定的字符串或<code>token_id</code>时，生成将立即终止。</p><p>可传入敏感词以控制模型的输出。</p><blockquote><p>stop为数组时，不可将<code>token_id</code>和字符串同时作为元素输入，比如不可以指定为<code>[&quot;你好&quot;,104307]</code>。</p></blockquote></td><td><a id="sec-tabs-3"></a><section><a id="非流式输出-2"></a><section><a id="非流式输出-2-h4"></a><h4>非流式输出</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key = &quot;sk-xxx&quot;
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

system_prompt = &quot;&quot;&quot;# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:
&lt;tools&gt;
{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;computer_use&quot;, &quot;description&quot;: &quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {&quot;action&quot;: {&quot;description&quot;: &quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.&quot;, &quot;enum&quot;: [&quot;key&quot;, &quot;type&quot;, &quot;mouse_move&quot;, &quot;left_click&quot;, &quot;left_click_drag&quot;, &quot;right_click&quot;, &quot;middle_click&quot;, &quot;double_click&quot;, &quot;triple_click&quot;, &quot;scroll&quot;, &quot;hscroll&quot;, &quot;wait&quot;, &quot;terminate&quot;, &quot;answer&quot;, &quot;interact&quot;], &quot;type&quot;: &quot;string&quot;}, &quot;keys&quot;: {&quot;description&quot;: &quot;Required only by `action=key`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;text&quot;: {&quot;description&quot;: &quot;Required only by `action=type`, `action=answer` and `action=interact`.&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;coordinate&quot;: {&quot;description&quot;: &quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;pixels&quot;: {&quot;description&quot;: &quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;time&quot;: {&quot;description&quot;: &quot;The seconds to wait. Required only by `action=wait`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;status&quot;: {&quot;description&quot;: &quot;The status of the task. Required only by `action=terminate`.&quot;, &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;success&quot;, &quot;failure&quot;]}}, &quot;required&quot;: [&quot;action&quot;], &quot;type&quot;: &quot;object&quot;}}}
&lt;/tools&gt;

For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:
&lt;tool_call&gt;
{&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}
&lt;/tool_call&gt;

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}.

Rules:
- Output exactly in the order: Action, &lt;tool_call&gt;.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.&quot;&quot;&quot;

messages = [
    {
        &quot;role&quot;: &quot;system&quot;,
        &quot;content&quot;: system_prompt
    },
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;},
            {&quot;text&quot;: &quot;帮我打开浏览器。&quot;}]
    }]

response = client.multimodal.chat.create(
    model='gui-plus-2026-02-26',
    messages=messages,
    parameters={&quot;vl_high_resolution_images&quot;: True}
)

print(response.output_text)
</code></pre></div><a id="fig-code-group-2-java-tab"></a>Java<div><a id="code-code-group-2-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
        // 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        String systemPrompt = &quot;# Tools\n\n&quot; +
                &quot;You may call one or more functions to assist with the user query.\n\n&quot; +
                &quot;You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:\n&quot; +
                &quot;&lt;tools&gt;\n&quot; +
                &quot;{\&quot;type\&quot;: \&quot;function\&quot;, \&quot;function\&quot;: {\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;description\&quot;: \&quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\&quot;, \&quot;parameters\&quot;: {\&quot;properties\&quot;: {\&quot;action\&quot;: {\&quot;description\&quot;: \&quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\&quot;, \&quot;enum\&quot;: [\&quot;key\&quot;, \&quot;type\&quot;, \&quot;mouse_move\&quot;, \&quot;left_click\&quot;, \&quot;left_click_drag\&quot;, \&quot;right_click\&quot;, \&quot;middle_click\&quot;, \&quot;double_click\&quot;, \&quot;triple_click\&quot;, \&quot;scroll\&quot;, \&quot;hscroll\&quot;, \&quot;wait\&quot;, \&quot;terminate\&quot;, \&quot;answer\&quot;, \&quot;interact\&quot;], \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;keys\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=key`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;text\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=type`, `action=answer` and `action=interact`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;coordinate\&quot;: {\&quot;description\&quot;: \&quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;pixels\&quot;: {\&quot;description\&quot;: \&quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;time\&quot;: {\&quot;description\&quot;: \&quot;The seconds to wait. Required only by `action=wait`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;status\&quot;: {\&quot;description\&quot;: \&quot;The status of the task. Required only by `action=terminate`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;, \&quot;enum\&quot;: [\&quot;success\&quot;, \&quot;failure\&quot;]}}, \&quot;required\&quot;: [\&quot;action\&quot;], \&quot;type\&quot;: \&quot;object\&quot;}}}\n&quot; +
                &quot;&lt;/tools&gt;\n\n&quot; +
                &quot;For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:\n&quot; +
                &quot;&lt;tool_call&gt;\n&quot; +
                &quot;{\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}\n&quot; +
                &quot;&lt;/tool_call&gt;\n\n&quot; +
                &quot;# Response format\n\n&quot; +
                &quot;Response format for every step:\n&quot; +
                &quot;1) Action: a short imperative describing what to do in the UI.\n&quot; +
                &quot;2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}.\n\n&quot; +
                &quot;Rules:\n&quot; +
                &quot;- Output exactly in the order: Action, &lt;tool_call&gt;.\n&quot; +
                &quot;- Be brief: one for Action.\n&quot; +
                &quot;- Do not output anything else outside those two parts.\n&quot; +
                &quot;- If finishing, use action=terminate in the tool call.&quot;;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;text&quot;,systemPrompt))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;image&quot;, &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;),
                        Collections.singletonMap(&quot;text&quot;, &quot;帮我打开浏览器。&quot;))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;gui-plus-2026-02-26&quot;)
                .messages(Arrays.asList(systemMsg,userMessage))
                .vlHighResolutionImages(true)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get(&quot;text&quot;));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
  -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
  -H &quot;Content-Type: application/json&quot; \
  -d '{
    &quot;model&quot;: &quot;gui-plus-2026-02-26&quot;,
    &quot;input&quot;: {
      &quot;messages&quot;: [
        {
          &quot;role&quot;: &quot;system&quot;,
          &quot;content&quot;: [
            {
              &quot;text&quot;: &quot;# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:\n&lt;tools&gt;\n{\&quot;type\&quot;: \&quot;function\&quot;, \&quot;function\&quot;: {\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;description\&quot;: \&quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\&quot;, \&quot;parameters\&quot;: {\&quot;properties\&quot;: {\&quot;action\&quot;: {\&quot;description\&quot;: \&quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\&quot;, \&quot;enum\&quot;: [\&quot;key\&quot;, \&quot;type\&quot;, \&quot;mouse_move\&quot;, \&quot;left_click\&quot;, \&quot;left_click_drag\&quot;, \&quot;right_click\&quot;, \&quot;middle_click\&quot;, \&quot;double_click\&quot;, \&quot;triple_click\&quot;, \&quot;scroll\&quot;, \&quot;hscroll\&quot;, \&quot;wait\&quot;, \&quot;terminate\&quot;, \&quot;answer\&quot;, \&quot;interact\&quot;], \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;keys\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=key`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;text\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=type`, `action=answer` and `action=interact`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;coordinate\&quot;: {\&quot;description\&quot;: \&quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;pixels\&quot;: {\&quot;description\&quot;: \&quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;time\&quot;: {\&quot;description\&quot;: \&quot;The seconds to wait. Required only by `action=wait`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;status\&quot;: {\&quot;description\&quot;: \&quot;The status of the task. Required only by `action=terminate`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;, \&quot;enum\&quot;: [\&quot;success\&quot;, \&quot;failure\&quot;]}}, \&quot;required\&quot;: [\&quot;action\&quot;], \&quot;type\&quot;: \&quot;object\&quot;}}}\n&lt;/tools&gt;\n\nFor each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:\n&lt;tool_call&gt;\n{\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}\n&lt;/tool_call&gt;\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}.\n\nRules:\n- Output exactly in the order: Action, &lt;tool_call&gt;.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call.&quot;
            }
          ]
        },
        {
          &quot;role&quot;: &quot;user&quot;,
          &quot;content&quot;: [
            {
              &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;
            },
            {
              &quot;text&quot;: &quot;帮我打开浏览器&quot;
            }
          ]
        }
      ]
    },
    &quot;parameters&quot;: {
      &quot;vl_high_resolution_images&quot;: true
    }
  }'
</code></pre></div></div></section><a id="流式输出-2"></a><section><a id="流式输出-2-h4"></a><h4>流式输出</h4><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>Python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key = &quot;sk-xxx&quot;
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

system_prompt = &quot;&quot;&quot;# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:
&lt;tools&gt;
{&quot;type&quot;: &quot;function&quot;, &quot;function&quot;: {&quot;name&quot;: &quot;computer_use&quot;, &quot;description&quot;: &quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.&quot;, &quot;parameters&quot;: {&quot;properties&quot;: {&quot;action&quot;: {&quot;description&quot;: &quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.&quot;, &quot;enum&quot;: [&quot;key&quot;, &quot;type&quot;, &quot;mouse_move&quot;, &quot;left_click&quot;, &quot;left_click_drag&quot;, &quot;right_click&quot;, &quot;middle_click&quot;, &quot;double_click&quot;, &quot;triple_click&quot;, &quot;scroll&quot;, &quot;hscroll&quot;, &quot;wait&quot;, &quot;terminate&quot;, &quot;answer&quot;, &quot;interact&quot;], &quot;type&quot;: &quot;string&quot;}, &quot;keys&quot;: {&quot;description&quot;: &quot;Required only by `action=key`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;text&quot;: {&quot;description&quot;: &quot;Required only by `action=type`, `action=answer` and `action=interact`.&quot;, &quot;type&quot;: &quot;string&quot;}, &quot;coordinate&quot;: {&quot;description&quot;: &quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.&quot;, &quot;type&quot;: &quot;array&quot;}, &quot;pixels&quot;: {&quot;description&quot;: &quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;time&quot;: {&quot;description&quot;: &quot;The seconds to wait. Required only by `action=wait`.&quot;, &quot;type&quot;: &quot;number&quot;}, &quot;status&quot;: {&quot;description&quot;: &quot;The status of the task. Required only by `action=terminate`.&quot;, &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;success&quot;, &quot;failure&quot;]}}, &quot;required&quot;: [&quot;action&quot;], &quot;type&quot;: &quot;object&quot;}}}
&lt;/tools&gt;

For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:
&lt;tool_call&gt;
{&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}
&lt;/tool_call&gt;

# Response format

Response format for every step:
1) Action: a short imperative describing what to do in the UI.
2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {&quot;name&quot;: &lt;function-name&gt;, &quot;arguments&quot;: &lt;args-json-object&gt;}.

Rules:
- Output exactly in the order: Action, &lt;tool_call&gt;.
- Be brief: one for Action.
- Do not output anything else outside those two parts.
- If finishing, use action=terminate in the tool call.&quot;&quot;&quot;

messages = [
    {
        &quot;role&quot;: &quot;system&quot;,
        &quot;content&quot;: system_prompt
    },
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;},
            {&quot;text&quot;: &quot;帮我打开浏览器。&quot;}]
    }]

stream = client.multimodal.chat.create(
    model='gui-plus',
    messages=messages,
    stream=True
)
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content)
</code></pre></div><a id="fig-code-group-3-java-tab"></a>Java<div><a id="code-code-group-3-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
        // 以下为华北2（北京）地域的配置，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        String systemPrompt = &quot;# Tools\n\n&quot; +
                &quot;You may call one or more functions to assist with the user query.\n\n&quot; +
                &quot;You are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:\n&quot; +
                &quot;&lt;tools&gt;\n&quot; +
                &quot;{\&quot;type\&quot;: \&quot;function\&quot;, \&quot;function\&quot;: {\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;description\&quot;: \&quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn't open, try wait and taking another screenshot.\\n* The screen's resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don't click boxes on their edges unless asked.\&quot;, \&quot;parameters\&quot;: {\&quot;properties\&quot;: {\&quot;action\&quot;: {\&quot;description\&quot;: \&quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it's the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\&quot;, \&quot;enum\&quot;: [\&quot;key\&quot;, \&quot;type\&quot;, \&quot;mouse_move\&quot;, \&quot;left_click\&quot;, \&quot;left_click_drag\&quot;, \&quot;right_click\&quot;, \&quot;middle_click\&quot;, \&quot;double_click\&quot;, \&quot;triple_click\&quot;, \&quot;scroll\&quot;, \&quot;hscroll\&quot;, \&quot;wait\&quot;, \&quot;terminate\&quot;, \&quot;answer\&quot;, \&quot;interact\&quot;], \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;keys\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=key`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;text\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=type`, `action=answer` and `action=interact`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;coordinate\&quot;: {\&quot;description\&quot;: \&quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;pixels\&quot;: {\&quot;description\&quot;: \&quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;time\&quot;: {\&quot;description\&quot;: \&quot;The seconds to wait. Required only by `action=wait`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;status\&quot;: {\&quot;description\&quot;: \&quot;The status of the task. Required only by `action=terminate`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;, \&quot;enum\&quot;: [\&quot;success\&quot;, \&quot;failure\&quot;]}}, \&quot;required\&quot;: [\&quot;action\&quot;], \&quot;type\&quot;: \&quot;object\&quot;}}}\n&quot; +
                &quot;&lt;/tools&gt;\n\n&quot; +
                &quot;For each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:\n&quot; +
                &quot;&lt;tool_call&gt;\n&quot; +
                &quot;{\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}\n&quot; +
                &quot;&lt;/tool_call&gt;\n\n&quot; +
                &quot;# Response format\n\n&quot; +
                &quot;Response format for every step:\n&quot; +
                &quot;1) Action: a short imperative describing what to do in the UI.\n&quot; +
                &quot;2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}.\n\n&quot; +
                &quot;Rules:\n&quot; +
                &quot;- Output exactly in the order: Action, &lt;tool_call&gt;.\n&quot; +
                &quot;- Be brief: one for Action.\n&quot; +
                &quot;- Do not output anything else outside those two parts.\n&quot; +
                &quot;- If finishing, use action=terminate in the tool call.&quot;;
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;text&quot;,systemPrompt))).build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap(&quot;image&quot;, &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;),
                        Collections.singletonMap(&quot;text&quot;, &quot;帮我打开浏览器。&quot;))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;gui-plus&quot;)
                .messages(Arrays.asList(userMessage,systemMsg))
                .incrementalOutput(true)
                .build();
        Flowable&lt;MultiModalConversationResult&gt; result = conv.streamCall(param);
        result.blockingForEach(item -&gt; {
            try {
                var content = item.getOutput().getChoices().get(0).getMessage().getContent();
                // 判断content是否存在且不为空
                if (content != null &amp;&amp;  !content.isEmpty()) {
                    System.out.println(content.get(0).get(&quot;text&quot;));
                }
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
</code></pre></div><a id="fig-code-group-3-curl-tab"></a>curl<div><a id="code-code-group-3-curl"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H 'Content-Type: application/json' \
-H &quot;X-DashScope-SSE: enable&quot; \
-d '{
    &quot;model&quot;: &quot;gui-plus-2026-02-26&quot;,
    &quot;input&quot;: {
      &quot;messages&quot;: [
        {
          &quot;role&quot;: &quot;system&quot;,
          &quot;content&quot;: [
            {
              &quot;text&quot;: &quot;# Tools\n\nYou may call one or more functions to assist with the user query.\n\nYou are provided with function signatures within &lt;tools&gt;&lt;/tools&gt; XML tags:\n&lt;tools&gt;\n{\&quot;type\&quot;: \&quot;function\&quot;, \&quot;function\&quot;: {\&quot;name\&quot;: \&quot;computer_use\&quot;, \&quot;description\&quot;: \&quot;Use a mouse and keyboard to interact with a computer, and take screenshots.\\n* This is an interface to a desktop GUI. You do not have access to a terminal or applications menu. You must click on desktop icons to start applications.\\n* Some applications may take time to start or process actions, so you may need to wait and take successive screenshots to see the results of your actions. E.g. if you click on Firefox and a window doesn'\''t open, try wait and taking another screenshot.\\n* The screen'\''s resolution is 1000x1000.\\n* Make sure to click any buttons, links, icons, etc with the cursor tip in the center of the element. Don'\''t click boxes on their edges unless asked.\&quot;, \&quot;parameters\&quot;: {\&quot;properties\&quot;: {\&quot;action\&quot;: {\&quot;description\&quot;: \&quot;The action to perform. The available actions are:\\n* `key`: Performs key down presses on the arguments passed in order, then performs key releases in reverse order.\\n* `type`: Type a string of text on the keyboard.\\n* `mouse_move`: Move the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `left_click`: Click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `left_click_drag`: Click and drag the cursor to a specified (x, y) pixel coordinate on the screen.\\n* `right_click`: Click the right mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `middle_click`: Click the middle mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `double_click`: Double-click the left mouse button at a specified (x, y) pixel coordinate on the screen.\\n* `triple_click`: Triple-click the left mouse button at a specified (x, y) pixel coordinate on the screen (simulated as double-click since it'\''s the closest action).\\n* `scroll`: Performs a scroll of the mouse scroll wheel.\\n* `hscroll`: Performs a horizontal scroll (mapped to regular scroll).\\n* `wait`: Wait specified seconds for the change to happen.\\n* `terminate`: Terminate the current task and report its completion status.\\n* `answer`: Answer a question.\\n* `interact`: Resolve the blocking window by interacting with the user.\&quot;, \&quot;enum\&quot;: [\&quot;key\&quot;, \&quot;type\&quot;, \&quot;mouse_move\&quot;, \&quot;left_click\&quot;, \&quot;left_click_drag\&quot;, \&quot;right_click\&quot;, \&quot;middle_click\&quot;, \&quot;double_click\&quot;, \&quot;triple_click\&quot;, \&quot;scroll\&quot;, \&quot;hscroll\&quot;, \&quot;wait\&quot;, \&quot;terminate\&quot;, \&quot;answer\&quot;, \&quot;interact\&quot;], \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;keys\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=key`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;text\&quot;: {\&quot;description\&quot;: \&quot;Required only by `action=type`, `action=answer` and `action=interact`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;}, \&quot;coordinate\&quot;: {\&quot;description\&quot;: \&quot;(x, y): The x (pixels from the left edge) and y (pixels from the top edge) coordinates to move the mouse to. Required only by `action=mouse_move` and `action=left_click_drag`.\&quot;, \&quot;type\&quot;: \&quot;array\&quot;}, \&quot;pixels\&quot;: {\&quot;description\&quot;: \&quot;The amount of scrolling to perform. Positive values scroll up, negative values scroll down. Required only by `action=scroll` and `action=hscroll`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;time\&quot;: {\&quot;description\&quot;: \&quot;The seconds to wait. Required only by `action=wait`.\&quot;, \&quot;type\&quot;: \&quot;number\&quot;}, \&quot;status\&quot;: {\&quot;description\&quot;: \&quot;The status of the task. Required only by `action=terminate`.\&quot;, \&quot;type\&quot;: \&quot;string\&quot;, \&quot;enum\&quot;: [\&quot;success\&quot;, \&quot;failure\&quot;]}}, \&quot;required\&quot;: [\&quot;action\&quot;], \&quot;type\&quot;: \&quot;object\&quot;}}}\n&lt;/tools&gt;\n\nFor each function call, return a json object with function name and arguments within &lt;tool_call&gt;&lt;/tool_call&gt; XML tags:\n&lt;tool_call&gt;\n{\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}\n&lt;/tool_call&gt;\n\n# Response format\n\nResponse format for every step:\n1) Action: a short imperative describing what to do in the UI.\n2) A single &lt;tool_call&gt;...&lt;/tool_call&gt; block containing only the JSON: {\&quot;name\&quot;: &lt;function-name&gt;, \&quot;arguments\&quot;: &lt;args-json-object&gt;}.\n\nRules:\n- Output exactly in the order: Action, &lt;tool_call&gt;.\n- Be brief: one for Action.\n- Do not output anything else outside those two parts.\n- If finishing, use action=terminate in the tool call.&quot;
            }
          ]
        },
        {
          &quot;role&quot;: &quot;user&quot;,
          &quot;content&quot;: [
            {
              &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png&quot;
            },
            {
              &quot;text&quot;: &quot;帮我打开浏览器&quot;
            }
          ]
        }
      ]
    },
    &quot;parameters&quot;: {
      &quot;vl_high_resolution_images&quot;: true
    }
  }'
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h3>chat响应对象（流式与非流式输出格式一致）</h3><p>调用失败时，Python SDK 2.0 会抛出 <code>DashScopeError</code> 异常，可通过异常属性 <code>e.status_code</code>/<code>e.code</code>/<code>e.message</code>/<code>e.request_id</code> 获取错误信息（HTTP 接口返回的原始响应中亦有对应的 code/message 字段）；Java SDK 调用失败会抛出异常，异常信息为 <strong>status_code</strong> 和 <strong>message</strong> 的内容。</p><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><blockquote><p>Java SDK返回参数为<strong>requestId。</strong></p></blockquote><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>finish_reason</strong><code>string</code></p><p>模型结束生成的原因。有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code>；</li></ul><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>因模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code>；</li></ul><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>string</code></p><p>模型输出结果</p></div></section></div></section><p><strong>audio</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求使用的Token信息。</p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入内容包含<code>image</code>时返回该字段。为用户输入图片内容转换成Token后的长度。</p><p><strong>characters</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>input_tokens_details</strong><code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>image_tokens</strong> <code>integer</code></p><p>模型输入的图像对应的 Token数。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p></div></section><p><strong>output_tokens_details</strong><code>object</code></p><p>输出 Token 的细粒度分类。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>input_tokens</code>与<code>output_tokens</code>的总和。</p></div></section></td><td><p>以下为 HTTP 接口返回的原始响应（Python SDK 2.0 返回扁平化后的响应对象，输出内容可通过 <code>response.output_text</code> 获取）。</p><a id="code-block-9"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;b74b3a25-3968-4059-8c44-63d793c07f02&quot;,
  &quot;output&quot;: {
    &quot;text&quot;: null,
    &quot;finish_reason&quot;: null,
    &quot;choices&quot;: [
      {
        &quot;finish_reason&quot;: &quot;stop&quot;,
        &quot;message&quot;: {
          &quot;role&quot;: &quot;assistant&quot;,
          &quot;content&quot;: [
            {
              &quot;text&quot;: &quot;```json\n{\&quot;thought\&quot;: \&quot;用户想要打开浏览器，我观察到屏幕截图中有一个Google Chrome的图标，其位置在右上角一排的最后一个。因此，下一步操作应该是点击这个Chrome浏览器图标来启动它。\&quot;, \&quot;action\&quot;: \&quot;CLICK\&quot;, \&quot;parameters\&quot;: {\&quot;x\&quot;: 1086, \&quot;y\&quot;: 127}}\n```&quot;
            }
          ]
        }
      }
    ],
    &quot;audio&quot;: null
  },
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 2021,
    &quot;output_tokens&quot;: 78,
    &quot;characters&quot;: 0,
    &quot;image_tokens&quot;: 1244,
    &quot;input_tokens_details&quot;: {
      &quot;image_tokens&quot;: 1244,
      &quot;text_tokens&quot;: 777
    },
    &quot;output_tokens_details&quot;: {
      &quot;text_tokens&quot;: 78
    },
    &quot;total_tokens&quot;: 2099
  }
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="97e145aeabbwf"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。
