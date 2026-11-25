# Qwen-OCR API参考

本文介绍通过OpenAI兼容接口 或 DashScopeAPI 调用通义千问OCR 模型的输入与输出参数。

> 相关文档：[文字提取（Qwen-OCR）](../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md)

<a id="openai-兼容"></a>

<a id="d397bcc41eu3q"></a>

## OpenAI 兼容

<a id="sec-tabs"></a>

<a id="华北2-北京-地域"></a>

<a id="华北2-北京-地域-h4"></a>

#### 华北2（北京）地域

SDK 调用配置的`base_url`为：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="新加坡地域"></a>

<a id="新加坡地域-h4"></a>

#### 新加坡地域

SDK 调用配置的`base_url`为：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

<a id="美国-弗吉尼亚-地域"></a>

<a id="美国-弗吉尼亚-地域-h4"></a>

#### 美国（弗吉尼亚）地域

SDK 调用配置的`base_url`为：`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1`

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

> 您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过OpenAI SDK进行调用，需要[安装SDK](../preparations/install-sdk.md)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型可参见<code>选择模型</code>。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>传递给大模型的上下文，按对话顺序排列。</p><a id="accordion-消息类型"></a><section><p>消息类型</p><div><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递指令和待识别的图像。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>content</strong><code>array</code><strong>（必选）</strong></p><p>消息内容。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong><code>string</code><strong>（必选）</strong></p><p>可选值：</p><ul><li><p><code>text</code></p><p>输入文本时需设为<code>text</code>。</p></li><li><p><code>image_url</code></p><p>输入图片时需设为<code>image_url</code>。</p></li></ul><p><strong>text</strong><code>string</code><strong>（可选）</strong></p><p>输入的文本。</p><p>默认值为：<code>Please output only the text content from the image without any additional descriptions or formatting.</code> ，即模型默认提取图像中的全部文本。</p><p><strong>image_url</strong><code>object</code></p><p>输入的图片信息。当<code>type</code>为<code>image_url</code>时是必选参数。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>url</strong> <code>string</code><strong>（必选）</strong></p><p>图片的 URL或 Base64 Data URL。传入本地文件请参考<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#23d2494606vg6">文字提取</a>。</p></div></section><p><strong>min_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最小像素阈值，单位为像素。</p><p>当输入图像像素小于<code>min_pixels</code>时，会将图像进行放大，直到总像素高于<code>min_pixels</code>。</p><a id="accordion-图像token与像素的转换关系"></a><section><p>图像Token与像素的转换关系</p><div><p>不同模型，每个图像 Token 对应的像素不同：</p><ul><li><code>qwen3.5-ocr</code>、<code>qwen-vl-ocr-2025-11-20</code>：每 Token 对应像素为<code>32*32</code>。</li><li><code>qwen-vl-ocr</code>及之前更新的模型：每 Token 对应像素为<code>28*28</code>。</li></ul></div></section><a id="accordion-min-pixels-取值范围"></a><section><p>min_pixels 取值范围</p><div><ul><li><code>qwen3.5-ocr</code>、<code>qwen-vl-ocr-2025-11-20</code>：默认值和最小值均为3072（即<code>3×32×32</code>）</li><li><code>qwen-vl-ocr</code>及之前更新的模型：默认值和最小值均为 <code>3136</code> （即<code>4×28×28</code>）。</li></ul></div></section><p>示例值：<code>{&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;:&quot;https://xxxx.jpg&quot;},&quot;min_pixels&quot;: 3072}</code></p><p><strong>max_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最大像素阈值，单位为像素。</p><p>当输入图像像素在<code>[min_pixels, max_pixels]</code>区间内时，模型会按原图进行识别。当输入图像像素大于<code>max_pixels</code>时，会将图像进行缩小，直到总像素低于<code>max_pixels</code>。</p><a id="accordion-图像token与像素的转换关系-2"></a><section><p>图像Token与像素的转换关系</p><div><p>不同模型，每个图像 Token 对应的像素不同：</p><ul><li><code>qwen3.5-ocr</code>、<code>qwen-vl-ocr-2025-11-20</code>：每 Token 对应像素为<code>32*32</code>。</li><li><code>qwen-vl-ocr</code>及之前更新的模型：每 Token 对应像素为<code>28*28</code>。</li></ul></div></section><a id="accordion-max-pixels-取值范围"></a><section><p>max_pixels 取值范围</p><div><ul><li><p><code>qwen3.5-ocr、qwen-vl-ocr-2025-11-20</code></p><ul><li>默认值：8388608 （即<code>8192x32x32</code>）</li><li>最大值：30720000（即<code>30000x32x32</code>）</li></ul></li><li><p><code>qwen-vl-ocr</code>及之前更新的模型</p><ul><li>默认值：6422528（即<code>8192x28x28</code>）</li><li>最大值：23520000（即<code>30000x28x28</code>）</li></ul></li></ul></div></section><p>示例值：<code>{&quot;type&quot;: &quot;image_url&quot;,&quot;image_url&quot;: {&quot;url&quot;:&quot;https://xxxx.jpg&quot;},&quot;max_pixels&quot;: 8388608}</code></p></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section></div></section><p><strong>stream</strong><code>boolean</code>（可选） 默认值为 <code>false</code></p><p>是否以流式方式输出回复。</p><p>可选值：</p><ul><li><code>false</code>：等待模型生成完整回复后一次性返回。</li><li><code>true</code>：模型边生成边返回数据块。客户端需逐块读取，以还原完整回复。</li></ul><p><strong>stream_options</strong><code>object</code>（可选）</p><p>流式输出的配置项，仅在 <code>stream</code> 为 <code>true</code> 时生效。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>include_usage</strong><code>boolean</code>（可选）默认值为 <code>false</code></p><p>是否在<strong>最后一个数据块</strong>包含Token消耗信息。</p><p>可选值：</p><ul><li><code>true</code>：包含；</li><li><code>false</code>：不包含。</li></ul></div></section><p><strong>max_tokens</strong><code>integer</code>（可选）</p><p>用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。</p><ul><li><p><code>qwen3.5-ocr</code>：默认值与最大值为32768。</p></li><li><p><code>qwen-vl-ocr-2025-11-20</code>、<code>qwen-vl-ocr-2024-10-28</code>默认值与最大值均为模型的最大输出长度，请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#0573ce495fnnf">模型选型</a>。</p></li><li><p><code>qwen-vl-ocr</code>，默认值和最大值为4096。</p><blockquote><p>如需提高该参数值（4097~8192范围），请联系商务经理进行申请，并提供以下信息：主账号ID、图像类型（如文档图、电商图、合同等）、模型名称、预计 QPS 和每日请求总数，以及模型输出长度超过4096的请求占比。</p></blockquote></li></ul><p><strong>logprobs</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否返回输出 Token 的对数概率，可选值：</p><ul><li><p><code>true</code></p><p>返回</p></li><li><p><code>false</code></p><p>不返回</p></li></ul><p><strong>top_logprobs</strong> <code>integer</code> （可选）默认值为0</p><p>指定在每一步生成时，返回模型最大概率的候选 Token 个数。</p><p>取值范围：[0,5]</p><p>仅当 <code>logprobs</code> 为 <code>true</code> 时生效。</p><p><strong>temperature</strong><code>float</code>（可选）默认值为0.01</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>top_p</strong><code>float</code>（可选）默认值为0.001</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>top_k</strong><code>integer</code>（可选）默认值为1</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;top_k&quot;: xxx}</code>；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>presence_penalty</strong> <code>float</code>（可选）默认值为0.0</p><p>控制模型生成文本时的内容重复度。</p><p>取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。</p><p>在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。</p><a id="accordion-原理介绍"></a><section><p>原理介绍</p><div><p>如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。</p></div></section><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>stop</strong><code>string 或 array</code>（可选）</p><p>用于指定停止词。当模型生成的文本中出现<code>stop</code> 指定的字符串或<code>token_id</code>时，生成将立即终止。</p><p>可传入敏感词以控制模型的输出。</p><blockquote><p>stop为数组时，不可将<code>token_id</code>和字符串同时作为元素输入，比如不可以指定为<code>[&quot;你好&quot;,104307]</code>。</p></blockquote></td><td><a id="sec-tabs-2"></a><section><a id="非流式输出"></a><section><a id="非流式输出-h4"></a><h4>非流式输出</h4><a id="fig-code-group"></a><div><a id="fig-code-group-python-tab"></a>Python<div><a id="code-code-group-python"></a><pre class="language-python"><code>from openai import OpenAI
import os

PROMPT_TICKET_EXTRACTION = &quot;&quot;&quot;
请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。
要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。
返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'},
&quot;&quot;&quot;

try:
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
        # 以下为北京地域的 base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1
        # 若使用新加坡地域的模型，需将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
        base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
    )
    completion = client.chat.completions.create(
        model=&quot;qwen3.5-ocr&quot;,
        messages=[
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;type&quot;: &quot;image_url&quot;,
                        &quot;image_url&quot;: {&quot;url&quot;:&quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;},
                        # 输入图像的最小像素阈值，小于该值图像会放大，直到总像素大于min_pixels
                        &quot;min_pixels&quot;: 32 * 32 * 3,
                        # 输入图像的最大像素阈值，超过该值图像会缩小，直到总像素低于max_pixels
                        &quot;max_pixels&quot;: 32 * 32 * 8192
                    },
                    # 模型支持在以下text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
                    {&quot;type&quot;: &quot;text&quot;,
                     &quot;text&quot;: PROMPT_TICKET_EXTRACTION}
                ]
            }
        ])
    print(completion.choices[0].message.content)
except Exception as e:
    print(f&quot;错误信息: {e}&quot;)
</code></pre></div><a id="fig-code-group-node-js-tab"></a>Node.js<div><a id="code-code-group-node-js"></a><pre class="language-javascript"><code>import OpenAI from 'openai';

// 定义提取车票信息的Prompt
const PROMPT_TICKET_EXTRACTION = `
请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。
要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。
返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'}
`;

// 初始化OpenAI客户端
const client = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
   // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
   // 以下为北京地域的 base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1
   // 若使用新加坡地域的模型，需将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    baseURL: &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
});

async function main() {
    try {
        // 创建聊天完成请求
        const completion = await client.chat.completions.create({
            model: &quot;qwen3.5-ocr&quot;,
            messages: [
                {
                    role: &quot;user&quot;,
                    content: [
                        // 模型支持在text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
                        {
                            type: &quot;image_url&quot;,
                            image_url: {
                                url: &quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;,
                            },
                            // 输入图像的最小像素阈值，小于该值图像会放大，直到总像素大于min_pixels
                            min_pixels: 32 * 32 * 3,
                            // 输入图像的最大像素阈值，超过该值图像会缩小，直到总像素低于max_pixels
                            max_pixels: 32 * 32 * 8192
                        },
                        {type: &quot;text&quot;,
                         text: PROMPT_TICKET_EXTRACTION}
                    ]
                }
            ]
        });

        // 输出结果
        console.log(completion.choices[0].message.content);
    } catch (error) {
        console.log(`错误信息: ${error}`);
    }
}

main();
</code></pre></div><a id="fig-code-group-curl-tab"></a>curl<div><a id="code-code-group-curl"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;image_url&quot;,
                    &quot;image_url&quot;: {&quot;url&quot;:&quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;},
                    &quot;min_pixels&quot;: 3072,
                    &quot;max_pixels&quot;: 8388608
                },
                {&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'&quot;}
            ]
        }
    ]
}'
</code></pre></div></div></section><a id="流式输出"></a><section><a id="流式输出-h4"></a><h4>流式输出</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-python-tab"></a>Python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import os
from openai import OpenAI

PROMPT_TICKET_EXTRACTION = &quot;&quot;&quot;
请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。
要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。
返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'},
&quot;&quot;&quot;

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
    base_url=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1&quot;,
)
completion = client.chat.completions.create(
    model=&quot;qwen3.5-ocr&quot;,
    messages=[
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;image_url&quot;,
                    &quot;image_url&quot;: {&quot;url&quot;:&quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;},
                    # 输入图像的最小像素阈值，小于该值图像会放大，直到总像素大于min_pixels
                    &quot;min_pixels&quot;: 32 * 32 * 3,
                    # 输入图像的最大像素阈值，超过该值图像会缩小，直到总像素低于max_pixels
                    &quot;max_pixels&quot;: 32 * 32 * 8192
                },
                  # 模型支持在text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
                {&quot;type&quot;: &quot;text&quot;,&quot;text&quot;: PROMPT_TICKET_EXTRACTION}

            ]
        }
    ],
    stream=True,
    stream_options={&quot;include_usage&quot;: True}
)
for chunk in completion:
    print(chunk.model_dump_json())
</code></pre></div><a id="fig-code-group-2-node-js-tab"></a>Node.js<div><a id="code-code-group-2-node-js"></a><pre class="language-javascript"><code>import OpenAI from 'openai';

// 定义提取车票信息的Prompt
const PROMPT_TICKET_EXTRACTION = `
请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。
要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。
返回数据格式以json方式输出，格式为：{'发票号码': 'xxx','起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'}
`;

const openai = new OpenAI({
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: &quot;sk-xxx&quot;,
  // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
  apiKey: process.env.DASHSCOPE_API_KEY,
   // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1
  baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1',
});

async function main() {
  const response = await openai.chat.completions.create({
    model: 'qwen3.5-ocr',
    messages: [
      {
        role: 'user',
        content: [
          // 模型支持在text字段中传入Prompt，若未传入，则会使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
          { type: 'text', text: PROMPT_TICKET_EXTRACTION},
          {
            type: 'image_url',
            image_url: {
              url: 'https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg',
            },
              //  输入图像的最小像素阈值，小于该值图像会放大，直到总像素大于min_pixels
              &quot;min_pixels&quot;: 32 * 32 * 3,
              // 输入图像的最大像素阈值，超过该值图像会缩小，直到总像素低于max_pixels
              &quot;max_pixels&quot;: 32 * 32 * 8192
          }
        ]
      }
    ],
    stream: true,
    stream_options:{&quot;include_usage&quot;: true}
  });
let fullContent = &quot;&quot;
  console.log(&quot;流式输出内容为：&quot;)
  for await (const chunk of response) {
    if (chunk.choices[0] &amp;&amp; chunk.choices[0].delta.content != null) {
      fullContent += chunk.choices[0].delta.content;
      console.log(chunk.choices[0].delta.content);
    }
}
  console.log(`完整输出内容为：${fullContent}`)
}

main();
</code></pre></div><a id="fig-code-group-2-curl-tab"></a>curl<div><a id="code-code-group-2-curl"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# 如果使用新加坡地域的模型，需要将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
-H &quot;Content-Type: application/json&quot; \
-d '{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;messages&quot;: [
        {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;type&quot;: &quot;image_url&quot;,
                    &quot;image_url&quot;: {&quot;url&quot;:&quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;},
                    &quot;min_pixels&quot;: 3072,
                    &quot;max_pixels&quot;: 8388608
                },
                {&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'&quot;}
            ]
        }
    ],
    &quot;stream&quot;: true,
    &quot;stream_options&quot;: {&quot;include_usage&quot;: true}
}'
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h3>chat响应对象（非流式输出）</h3><p><strong>id</strong><code>string</code></p><p>本次请求的唯一标识符。</p><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>模型停止生成的原因。</p><p>有两种情况：</p><ul><li>自然停止输出时为<code>stop</code>；</li><li>生成长度过长而结束为<code>length</code>。</li></ul><p><strong>index</strong><code>integer</code></p><p>当前对象在<code>choices</code>数组中的索引。</p><p><strong>message</strong><code>object</code></p><p>模型输出的消息。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>大模型的返回结果。</p><p><strong>processed_text</strong> <code>string</code></p><p>对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。</p><blockquote><p>仅通过 DashScope SDK 和 curl 调用时返回，OpenAI 兼容 SDK 不返回该字段。</p></blockquote><p><strong>refusal</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>audio</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>function_call</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>tool_calls</strong> <code>array</code></p><p>该参数当前固定为<code>null</code>。</p></div></section></div></section><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion</code>。</p><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>本次请求的 Token 消耗信息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>模型输出Token的细粒度分类。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>accepted_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输出文本对应的 Token 数。</p><p><strong>rejected_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>模型输入的图像对应的 Token数。</p></div></section></div></section></td><td><a id="code-block"></a><pre class="language-json"><code>{
  &quot;id&quot;: &quot;chatcmpl-ba21fa91-dcd6-4dad-90cc-6d49c3c39094&quot;,
  &quot;choices&quot;: [
    {
      &quot;finish_reason&quot;: &quot;stop&quot;,
      &quot;index&quot;: 0,
      &quot;logprobs&quot;: null,
      &quot;message&quot;: {
        &quot;content&quot;: &quot;```json\n{\n    \&quot;销售方名称\&quot;: \&quot;null\&quot;,\n    \&quot;购买方名称\&quot;: \&quot;蔡应时\&quot;,\n    \&quot;不含税价\&quot;: \&quot;230769.23\&quot;,\n    \&quot;组织机构代码\&quot;: \&quot;null\&quot;,\n    \&quot;发票代码\&quot;: \&quot;142011726001\&quot;\n}\n```&quot;,
        &quot;refusal&quot;: null,
        &quot;role&quot;: &quot;assistant&quot;,
        &quot;annotations&quot;: null,
        &quot;audio&quot;: null,
        &quot;function_call&quot;: null,
        &quot;tool_calls&quot;: null
      }
    }
  ],
  &quot;created&quot;: 1763283287,
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;object&quot;: &quot;chat.completion&quot;,
  &quot;service_tier&quot;: null,
  &quot;system_fingerprint&quot;: null,
  &quot;usage&quot;: {
    &quot;completion_tokens&quot;: 72,
    &quot;prompt_tokens&quot;: 1185,
    &quot;total_tokens&quot;: 1257,
    &quot;completion_tokens_details&quot;: {
      &quot;accepted_prediction_tokens&quot;: null,
      &quot;audio_tokens&quot;: null,
      &quot;reasoning_tokens&quot;: null,
      &quot;rejected_prediction_tokens&quot;: null,
      &quot;text_tokens&quot;: 72
    },
    &quot;prompt_tokens_details&quot;: {
      &quot;audio_tokens&quot;: null,
      &quot;cached_tokens&quot;: null,
      &quot;image_tokens&quot;: 1001,
      &quot;text_tokens&quot;: 184
    }
  }
}
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="e98e6b7aa5nb2"></a><h3>chat响应chunk对象（流式输出）</h3><p><strong>id</strong><code>string</code></p><p>本次调用的唯一标识符。每个chunk对象有相同的 id。</p><p><strong>choices</strong><code>array</code></p><p>模型生成内容的数组。若设置<code>include_usage</code>参数为<code>true</code>，则在最后一个chunk中为空。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>delta</strong> <code>object</code></p><p>流式返回的输出内容。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>content</strong> <code>string</code></p><p>大模型的返回结果。</p><p><strong>function_call</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>refusal</strong> <code>object</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>role</strong> <code>string</code></p><p>消息对象的角色，只在第一个chunk中有值。</p></div></section><p><strong>finish_reason</strong> <code>string</code></p><p>模型停止生成的原因。有三种情况：</p><ul><li>自然停止输出时为<code>stop</code>；</li><li>生成未结束时为<code>null</code>；</li><li>生成长度过长而结束为<code>length</code>。</li></ul><p><strong>index</strong> <code>integer</code></p><p>当前响应在<code>choices</code>数组中的索引。</p></div></section><p><strong>created</strong><code>integer</code></p><p>本次请求被创建时的时间戳。每个chunk有相同的时间戳。</p><p><strong>model</strong><code>string</code></p><p>本次请求使用的模型。</p><p><strong>object</strong> <code>string</code></p><p>始终为<code>chat.completion.chunk</code>。</p><p><strong>service_tier</strong> <code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>system_fingerprint</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>usage</strong> <code>object</code></p><p>本次请求消耗的Token。只在<code>include_usage</code>为<code>true</code>时，在最后一个chunk返回。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>completion_tokens</strong> <code>integer</code></p><p>模型输出的 Token 数。</p><p><strong>prompt_tokens</strong> <code>integer</code></p><p>输入的 Token 数。</p><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>prompt_tokens</code>与<code>completion_tokens</code>的总和。</p><p><strong>completion_tokens_details</strong> <code>object</code></p><p>模型输出Token的细粒度分类。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>accepted_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>reasoning_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输出文本对应的 Token 数。</p><p><strong>rejected_prediction_tokens</strong><code>integer</code></p><p>该参数当前固定为<code>null</code>。</p></div></section><p><strong>prompt_tokens_details</strong> <code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>audio_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>cached_tokens</strong> <code>integer</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>模型输入的图像对应的 Token数。</p></div></section></div></section></td><td><a id="code-block-2"></a><pre class="language-json"><code>{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:&quot;assistant&quot;,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;```&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;json&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;\n&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;{\n&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;   &quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
......
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;```&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:null,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[{&quot;delta&quot;:{&quot;content&quot;:&quot;&quot;,&quot;function_call&quot;:null,&quot;refusal&quot;:null,&quot;role&quot;:null,&quot;tool_calls&quot;:null},&quot;finish_reason&quot;:&quot;stop&quot;,&quot;index&quot;:0,&quot;logprobs&quot;:null}],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:null}
{&quot;id&quot;:&quot;chatcmpl-f6fbdc0d-78d6-418f-856f-f099c2e4859b&quot;,&quot;choices&quot;:[],&quot;created&quot;:1764139204,&quot;model&quot;:&quot;qwen3.5-ocr&quot;,&quot;object&quot;:&quot;chat.completion.chunk&quot;,&quot;service_tier&quot;:null,&quot;system_fingerprint&quot;:null,&quot;usage&quot;:{&quot;completion_tokens&quot;:141,&quot;prompt_tokens&quot;:513,&quot;total_tokens&quot;:654,&quot;completion_tokens_details&quot;:{&quot;accepted_prediction_tokens&quot;:null,&quot;audio_tokens&quot;:null,&quot;reasoning_tokens&quot;:null,&quot;rejected_prediction_tokens&quot;:null,&quot;text_tokens&quot;:141},&quot;prompt_tokens_details&quot;:{&quot;audio_tokens&quot;:null,&quot;cached_tokens&quot;:null,&quot;image_tokens&quot;:332,&quot;text_tokens&quot;:181}}}
</code></pre></td></tr></tbody></table>

<a id="dashscope"></a>

<a id="69cac67a477k2"></a>

## DashScope

<a id="sec-tabs-3"></a>

<a id="华北2-北京-地域-2"></a>

<a id="华北2-北京-地域-2-h4"></a>

#### 华北2（北京）地域

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用无需配置 `region`（默认为`cn-beijing`）。

<a id="新加坡地域-2"></a>

<a id="新加坡地域-2-h4"></a>

#### 新加坡地域

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`region`：

<a id="sec-tabs-4"></a>

<a id="python代码"></a>

<a id="python代码-h4"></a>

#### Python代码

<a id="code-block-3"></a>

```python
import dashscope

client = dashscope.Client(workspace="{WorkspaceId}", region="ap-southeast-1")
```

<a id="java代码"></a>

<a id="java代码-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-4"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-5"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";
```

<a id="美国-弗吉尼亚-地域-2"></a>

<a id="美国-弗吉尼亚-地域-2-h4"></a>

#### 美国（弗吉尼亚）地域

HTTP 调用配置的`endpoint`：`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的`region`：

<a id="sec-tabs-5"></a>

<a id="python代码-2"></a>

<a id="python代码-2-h4"></a>

#### Python代码

<a id="code-block-6"></a>

```python
import dashscope

client = dashscope.Client(workspace="{WorkspaceId}", region="us-east-1")
```

<a id="java代码-2"></a>

<a id="java代码-2-h4"></a>

#### Java代码

-   **方式一：**

<a id="code-block-7"></a>

```java
import com.alibaba.dashscope.protocol.Protocol;
MultiModalConversation conv = new MultiModalConversation(Protocol.HTTP.getValue(), "https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1");
```

-   **方式二：**

<a id="code-block-8"></a>

```java
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl="https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1";
```

> 您需要已[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。若通过DashScope SDK进行调用，需要[安装DashScope SDK](../preparations/install-sdk.md)。

<table><tbody><tr><td><a id="2a1c410015otp"></a><h3>请求体</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。支持的模型可参见<code>选择模型</code>。</p><p><strong>messages</strong><code>array</code><strong>（必选）</strong></p><p>传递给大模型的上下文，按对话顺序排列。</p><blockquote><p>通过HTTP调用时，请将<strong>messages</strong>放入 <strong>input</strong> 对象中。</p></blockquote><a id="accordion-消息类型-2"></a><section><p>消息类型</p><div><p>User Message<code>object</code><strong>（必选）</strong></p><p>用户消息，用于向模型传递问题、指令或上下文等。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>content</strong><code>string 或 array</code><strong>（必选）</strong></p><p>消息内容。若输入只有文本，则为 string 类型；若输入包含图像数据，则为 array 类型。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（可选）</strong></p><p>输入的文本。</p><p>默认值为：<code>Please output only the text content from the image without any additional descriptions or formatting.</code> ，即模型默认提取图像中的全部文本。</p><p><strong>image</strong><code>string</code>（可选）</p><p>图片的URL、 Base64 Data URL、或本地路径。传入本地文件请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#23d2494606vg6">传入本地文件</a>。</p><p>示例值：<code>{&quot;image&quot;:&quot;https://xxxx.jpeg&quot;}</code></p><p><strong>enable_rotate</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否对倾斜的图像进行校正处理。</p><p>可选值：</p><ul><li><code>true</code>：自动校正</li><li><code>false</code>：不进行校正</li></ul><p>示例值：<code>{&quot;image&quot;:&quot;https://xxxx.jpeg&quot;,&quot;enable_rotate&quot;: True}</code></p><p><strong>min_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最小像素阈值，单位为像素。</p><p>当输入图像像素小于<code>min_pixels</code>时，会将图像进行放大，直到总像素高于<code>min_pixels</code>。</p><a id="accordion-图像token与像素的转换关系-3"></a><section><p>图像Token与像素的转换关系</p><div><p>不同模型，每个图像 Token 对应的像素不同：</p><ul><li><code>qwen3.5-ocr</code>、<code>qwen-vl-ocr-2025-11-20</code>：每 Token 对应像素为<code>32*32</code>。</li><li><code>qwen-vl-ocr</code>及之前更新的模型：每 Token 对应像素为<code>28*28</code>。</li></ul></div></section><a id="accordion-min-pixels-取值范围-2"></a><section><p>min_pixels 取值范围</p><div><ul><li><code>qwen3.5-ocr</code>、<code>qwen-vl-ocr-2025-11-20</code>：默认值和最小值均为3072（即<code>3×32×32</code>）</li><li><code>qwen-vl-ocr</code>及之前更新的模型：默认值和最小值均为 <code>3136</code> （即<code>4×28×28</code>）。</li></ul></div></section><p>示例值：<code>{&quot;image&quot;:&quot;https://xxxx.jpeg&quot;,&quot;min_pixels&quot;: 3072}</code></p><p><strong>max_pixels</strong><code>integer</code>（可选）</p><p>用于设定输入图像的最大像素阈值，单位为像素。</p><p>当输入图像像素在<code>[min_pixels, max_pixels]</code>区间内时，模型会按原图进行识别。当输入图像像素大于<code>max_pixels</code>时，会将图像进行缩小，直到总像素低于<code>max_pixels</code>。</p><a id="accordion-图像token与像素的转换关系-4"></a><section><p>图像Token与像素的转换关系</p><div><p>不同模型，每个图像 Token 对应的像素不同：</p><ul><li><code>qwen3.5-ocr</code>、<code>qwen-vl-ocr-2025-11-20</code>：每 Token 对应像素为<code>32*32</code>。</li><li><code>qwen-vl-ocr</code>及之前更新的模型：每 Token 对应像素为<code>28*28</code>。</li></ul></div></section><a id="accordion-max-pixels-取值范围-2"></a><section><p>max_pixels 取值范围</p><div><ul><li><p><code>qwen3.5-ocr、qwen-vl-ocr-2025-11-20</code></p><ul><li>默认值：8388608 （即<code>8192x32x32</code>）</li><li>最大值：30720000（即<code>30000x32x32</code>）</li></ul></li><li><p><code>qwen-vl-ocr</code>及之前更新的模型</p><ul><li>默认值：6422528（即<code>8192x28x28</code>）</li><li>最大值：23520000（即<code>30000x28x28</code>）</li></ul></li></ul></div></section><p>示例值：<code>{&quot;image&quot;:&quot;https://xxxx.jpeg&quot;,&quot;max_pixels&quot;: 8388608}</code></p></div></section><p><strong>role</strong><code>string</code><strong>（必选）</strong></p><p>用户消息的角色，固定为<code>user</code>。</p></div></section></div></section><p><strong>max_tokens</strong><code>integer</code>（可选）</p><p>用于限制模型输出的最大 Token 数。若生成内容超过此值，响应将被截断。</p><ul><li><p><code>qwen3.5-ocr</code>：默认值与最大值为32768。</p></li><li><p><code>qwen-vl-ocr-2025-11-20</code>、<code>qwen-vl-ocr-2024-10-28</code>默认值与最大值均为模型的最大输出长度，请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#0573ce495fnnf">模型选型</a>。</p></li><li><p><code>qwen-vl-ocr</code>，默认值和最大值为4096。</p><blockquote><p>如需提高该参数值（4097~8192范围），请联系商务经理进行申请，并提供以下信息：主账号ID、图像类型（如文档图、电商图、合同等）、模型名称、预计 QPS 和每日请求总数，以及模型输出长度超过4096的请求占比。</p></blockquote></li></ul><blockquote><p>Java SDK中为<strong>maxTokens</strong>*。*通过HTTP调用时，请将 <strong>max_tokens</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>ocr_options</strong><em>object</em>（可选）</p><p>使用通义千问OCR模型<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>时需要配置的参数。调用内置任务时，无需传入<code>User Message</code>，模型内部会采用对应任务的<code>Prompt</code>。相关章节：<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>task</strong> <code>string</code> （必选）</p><p>内置任务的名称，可选值如下：</p><ul><li><code>text_recognition</code>：通用文字识别</li><li><code>key_information_extraction</code>：信息抽取</li><li><code>document_parsing</code>：文档解析</li><li><code>table_parsing</code>：表格解析</li><li><code>formula_recognition</code>：公式识别</li><li><code>multi_lan</code>：多语言识别</li><li><code>advanced_recognition</code>：高精识别</li></ul><p><strong>task_config</strong> <code>object</code> （可选）</p><p>当<code>task</code>的取值为<code>key_information_extraction</code>（信息抽取）时，此参数用于指定需抽取的特定字段。如未指定 <code>task_config</code>，模型将默认提取图像中的所有字段。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>result_schema</strong><code>object</code> （可选）</p><p>表示需要模型抽取的字段，应为JSON对象结构，最多可嵌套3层JSON 对象。</p><p>在JSON对象的键（<code>key</code>）中指定待抽取字段的名称，对应的值（<code>value</code>）可为空，建议在值中提供字段描述或格式要求，可提高信息提取的准确率。</p><p>示例值：</p><a id="code-block-9"></a><pre class="language-json"><code>&quot;result_schema&quot;: {
     &quot;发票号码&quot;: &quot;发票的唯一识别编号，通常为数字和字母的组合。&quot;,
     &quot;开票日期&quot;: &quot;发票开具的日期，请以YYYY-MM-DD格式提取，例如2023-10-26。&quot;,
     &quot;销售方名称&quot;: &quot;发票上显示的销售方公司全称。&quot;,
     &quot;总金额&quot;: &quot;发票中包含税费的总计金额，要求提取数值并保留两位小数，例如123.45。&quot;
}
</code></pre></div></section></div></section><blockquote><p>Java SDK为<strong>OcrOptions</strong>，DashScope Python SDK 最低版本为2.0.1， Java SDK 最低版本为2.18.4。</p></blockquote><blockquote><p>通过HTTP调用时，请将 <strong>ocr_options</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子。用于确保在相同输入和参数下生成结果可复现。若调用时传入相同的 <code>seed</code> 且其他参数不变，模型将尽可能返回相同结果。</p><p>取值范围：<code>[0,2 31 −1]</code>。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><blockquote><p>通过HTTP调用时，请将 <strong>seed</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>temperature</strong><code>float</code>（可选）默认值为0.01</p><p>采样温度，控制模型生成文本的多样性。</p><p>temperature越高，生成的文本更多样，反之，生成的文本更确定。</p><p>取值范围： [0, 2)</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><blockquote><p>通过HTTP调用时，请将 <strong>temperature</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>top_p</strong><code>float</code>（可选）默认值为0.001</p><p>核采样的概率阈值，控制模型生成文本的多样性。</p><p>top_p越高，生成的文本更多样。反之，生成的文本更确定。</p><p>取值范围：（0,1.0]</p><p>temperature与top_p均可以控制生成文本的多样性，建议只设置其中一个值。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><blockquote><p>Java SDK中为<strong>topP</strong>*。*通过HTTP调用时，请将 <strong>top_p</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>top_k</strong><code>integer</code>（可选）默认值为1</p><p>生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。</p><p>取值需要大于或等于0。</p><p>该参数非OpenAI标准参数。通过 Python SDK调用时，请放入 <strong>extra_body</strong> 对象中，配置方式为：<code>extra_body={&quot;top_k&quot;: xxx}</code>；通过 Node.js SDK 或 HTTP 方式调用时，请作为顶层参数传递。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>repetition_penalty</strong><code>float</code>（可选）默认值为1.0</p><p>模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。该参数对模型效果影响较大，建议保持默认值。</p><blockquote><p>建议设置为默认值即可。</p></blockquote><blockquote><p>Java SDK中为<strong>repetitionPenalty</strong>*。*通过HTTP调用时，请将 <strong>repetition_penalty</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>presence_penalty</strong> <code>float</code>（可选）默认值为0.0</p><p>控制模型生成文本时的内容重复度。</p><p>取值范围：[-2.0, 2.0]。正值降低重复度，负值增加重复度。</p><p>在创意写作或头脑风暴等需要多样性、趣味性或创造力的场景中，建议调高该值；在技术文档或正式文本等强调一致性与术语准确性的场景中，建议调低该值。</p><a id="accordion-原理介绍-2"></a><section><p>原理介绍</p><div><p>如果参数值是正数，模型将对目前文本中已存在的Token施加一个惩罚值（惩罚值与文本出现的次数无关），减少这些Token重复出现的几率，从而减少内容重复度，增加用词多样性。</p></div></section><blockquote><p>建议设置为默认值即可。</p></blockquote><p><strong>stream</strong><code>boolean</code>（可选）默认值为<code>false</code></p><p>是否流式输出回复。参数值：</p><ul><li>false：模型生成完所有内容后一次性返回结果。</li><li>true：边生成边输出，即每生成一部分内容就立即输出一个片段（chunk）。</li></ul><blockquote><p>该参数仅支持Python SDK。通过Java SDK实现流式输出请通过<code>streamCall</code>接口调用；通过HTTP实现流式输出请在Header中指定<code>X-DashScope-SSE</code>为<code>enable</code>。</p></blockquote><p><strong>incremental_output</strong><code>boolean</code>（可选）默认为<code>false</code></p><p>在流式输出模式下是否开启增量输出。推荐您优先设置为<code>true</code>。</p><p>参数值：</p><ul><li>false：每次输出为当前已经生成的整个序列，最后一次输出为生成的完整结果。</li></ul><a id="code-block-10"></a><pre class="language-text"><code>I
I like
I like apple
I like apple.
</code></pre><ul><li>true（推荐）：增量输出，即后续输出内容不包含已输出的内容。您需要实时地逐个读取这些片段以获得完整的结果。</li></ul><a id="code-block-11"></a><pre class="language-text"><code>I
like
apple
.
</code></pre><blockquote><p>Java SDK中为<strong>incrementalOutput</strong>*。*通过HTTP调用时，请将 <strong>incremental_output</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>stop</strong><code>string 或 array</code>（可选）</p><p>用于指定停止词。当模型生成的文本中出现<code>stop</code> 指定的字符串或<code>token_id</code>时，生成将立即终止。</p><p>可传入敏感词以控制模型的输出。</p><blockquote><p>stop为数组时，不可将<code>token_id</code>和字符串同时作为元素输入，比如不可以指定为<code>[&quot;你好&quot;,104307]</code>。</p></blockquote><p><strong>logprobs</strong> <code>boolean</code> （可选）默认值为 <code>false</code></p><p>是否返回输出 Token 的对数概率，可选值：</p><ul><li><p><code>true</code></p><p>返回</p></li><li><p><code>false</code></p><p>不返回</p></li></ul><p>支持的模型：qwen-vl-ocr-2025-11-20及之后更新的模型</p><blockquote><p>通过HTTP调用时，请将 <strong>logprobs</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote><p><strong>top_logprobs</strong> <code>integer</code> （可选）默认值为0</p><p>指定在每一步生成时，返回模型最大概率的候选 Token 个数。仅当 <code>logprobs</code> 为 <code>true</code> 时生效。</p><p>取值范围：[0,5]</p><blockquote><p>Java SDK中为<strong>topLogprobs</strong>*。*通过HTTP调用时，请将 <strong>top_logprobs</strong>放入 <strong>parameters</strong> 对象中。</p></blockquote></td><td><a id="sec-tabs-6"></a><section><a id="高精识别"></a><section><a id="高精识别-h4"></a><h4>高精识别</h4><blockquote><p>以下为调用高精识别内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-python-tab"></a>python<div><a id="code-code-group-3-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;

messages = [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg&quot;,
                # 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192,
                # 是否开启图像自动转正功能
                &quot;enable_rotate&quot;: False}]
            }]

response = dashscope.MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3.5-ocr',
    messages=messages,
    # 设置内置任务为高精识别
    ocr_options={&quot;task&quot;: &quot;advanced_recognition&quot;}
)
# 高精识别任务的文本与坐标结果从 ocr_result 字段中获取
print(response[&quot;output&quot;][&quot;choices&quot;][0][&quot;message&quot;].content[0][&quot;ocr_result&quot;])
</code></pre></div><a id="fig-code-group-3-java-tab"></a>java<div><a id="code-code-group-3-java"></a><pre class="language-java"><code>// dashscope SDK的版本 &gt;= 2.21.8
import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);
        // 配置内置的OCR任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.ADVANCED_RECOGNITION)
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                        )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                 // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get(&quot;ocr_result&quot;));
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
</code></pre></div><a id="fig-code-group-3-bash-tab"></a>bash<div><a id="code-code-group-3-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '
{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg&quot;,
            &quot;min_pixels&quot;: 3072,
            &quot;max_pixels&quot;: 8388608,
            &quot;enable_rotate&quot;: false
          }
        ]
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;ocr_options&quot;: {
      &quot;task&quot;: &quot;advanced_recognition&quot;
    }
  }
}
'
</code></pre></div></div></section><a id="信息抽取"></a><section><a id="信息抽取-h4"></a><h4>信息抽取</h4><blockquote><p>以下为调用信息抽取内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-python-tab"></a>python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code># use [pip install -U dashscope] to update sdk

import os
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;

messages = [
      {
        &quot;role&quot;:&quot;user&quot;,
        &quot;content&quot;:[
          {
              &quot;image&quot;:&quot;http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg&quot;,
              &quot;min_pixels&quot;: 32 * 32 * 3,
              &quot;max_pixels&quot;: 32 * 32 *8192,
              &quot;enable_rotate&quot;: False
          }
        ]
      }
    ]

# 指定抽取字段
params = {
  &quot;ocr_options&quot;:{
    &quot;task&quot;: &quot;key_information_extraction&quot;,
    &quot;task_config&quot;: {
      &quot;result_schema&quot;: {
          &quot;乘车日期&quot;: &quot;对应图中乘车日期时间，格式为年-月-日，比如2025-03-05&quot;,
          &quot;发票代码&quot;: &quot;提取图中的发票代码，通常为一组数字或字母组合&quot;,
          &quot;发票号码&quot;: &quot;提取发票上的号码，通常由纯数字组成。&quot;
      }
    }
  }
}

response = MultiModalConversation.call(
    model='qwen3.5-ocr',
    messages=messages,
    **params,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'))

print(response.output.choices[0].message.content[0][&quot;ocr_result&quot;])
</code></pre></div><a id="fig-code-group-4-java-tab"></a>java<div><a id="code-code-group-4-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.google.gson.JsonObject;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;,3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);

        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                        )).build();

        // 创建主JSON对象
        JsonObject resultSchema = new JsonObject();
        resultSchema.addProperty(&quot;乘车日期&quot;, &quot;对应图中乘车日期时间，格式为年-月-日，比如2025-03-05&quot;);
        resultSchema.addProperty(&quot;发票代码&quot;, &quot;提取图中的发票代码，通常为一组数字或字母组合&quot;);
        resultSchema.addProperty(&quot;发票号码&quot;, &quot;提取发票上的号码，通常由纯数字组成。&quot;);

        // 配置内置的OCR任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.KEY_INFORMATION_EXTRACTION)
                .taskConfig(OcrOptions.TaskConfig.builder()
                        .resultSchema(resultSchema)
                        .build())
                .build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
               // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get(&quot;ocr_result&quot;));
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
</code></pre></div><a id="fig-code-group-4-bash-tab"></a>bash<div><a id="code-code-group-4-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '
{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;image&quot;: &quot;http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg&quot;,
            &quot;min_pixels&quot;: 3072,
            &quot;max_pixels&quot;: 8388608,
            &quot;enable_rotate&quot;: false
          }
        ]
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;ocr_options&quot;: {
      &quot;task&quot;: &quot;key_information_extraction&quot;,
      &quot;task_config&quot;: {
        &quot;result_schema&quot;: {
            &quot;乘车日期&quot;: &quot;对应图中乘车日期时间，格式为年-月-日，比如2025-03-05&quot;,
            &quot;发票代码&quot;: &quot;提取图中的发票代码，通常为一组数字或字母组合&quot;,
            &quot;发票号码&quot;: &quot;提取发票上的号码，通常由纯数字组成。&quot;
        }
    }
    }
  }
}
'
</code></pre></div></div></section><a id="表格解析"></a><section><a id="表格解析-h4"></a><h4>表格解析</h4><blockquote><p>以下为调用表格解析内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-5"></a><div><a id="fig-code-group-5-python-tab"></a>python<div><a id="code-code-group-5-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;image&quot;: &quot;http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/doc_parsing/tables/photo/eng/17.jpg&quot;,
                # 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192}]
           }]
response = client.multimodal.chat.create(
    model='qwen3.5-ocr',
    messages=messages,
    # 设置内置任务为表格解析
    parameters={&quot;ocr_options&quot;: {&quot;task&quot;: &quot;table_parsing&quot;}}
)
# 表格解析任务以HTML格式返回结果
print(response.output_text)
</code></pre></div><a id="fig-code-group-5-java-tab"></a>java<div><a id="code-code-group-5-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;https://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/doc_parsing/tables/photo/eng/17.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);
        // 配置内置的OCR任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.TABLE_PARSING)
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                        )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
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
</code></pre></div><a id="fig-code-group-5-bash-tab"></a>bash<div><a id="code-code-group-5-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '
{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;image&quot;: &quot;http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/doc_parsing/tables/photo/eng/17.jpg&quot;,
            &quot;min_pixels&quot;: 3072,
            &quot;max_pixels&quot;: 8388608,
            &quot;enable_rotate&quot;: false
          }
        ]
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;ocr_options&quot;: {
      &quot;task&quot;: &quot;table_parsing&quot;
    }
  }
}
'
</code></pre></div></div></section><a id="文档解析"></a><section><a id="文档解析-h4"></a><h4>文档解析</h4><blockquote><p>以下为调用文档解析内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-6"></a><div><a id="fig-code-group-6-python-tab"></a>python<div><a id="code-code-group-6-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i1/O1CN01ukECva1cisjyK6ZDK_!!6000000003635-0-tps-1500-1734.jpg&quot;,
                # 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192}]
            }]

response = client.multimodal.chat.create(
    model='qwen3.5-ocr',
    messages=messages,
    # 设置内置任务为文档解析
    parameters={&quot;ocr_options&quot;: {&quot;task&quot;: &quot;document_parsing&quot;}}
)
# 文档解析任务以LaTeX格式返回结果
print(response.output_text)
</code></pre></div><a id="fig-code-group-6-java-tab"></a>java<div><a id="code-code-group-6-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;https://img.alicdn.com/imgextra/i1/O1CN01ukECva1cisjyK6ZDK_!!6000000003635-0-tps-1500-1734.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);
        // 配置内置的OCR任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.DOCUMENT_PARSING)
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
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
</code></pre></div><a id="fig-code-group-6-bash-tab"></a>bash<div><a id="code-code-group-6-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'\
  --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;\
  --header 'Content-Type: application/json'\
  --data '{
&quot;model&quot;: &quot;qwen3.5-ocr&quot;,
&quot;input&quot;: {
  &quot;messages&quot;: [
    {
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: [{
          &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i1/O1CN01ukECva1cisjyK6ZDK_!!6000000003635-0-tps-1500-1734.jpg&quot;,
          &quot;min_pixels&quot;: 3072,
          &quot;max_pixels&quot;: 8388608,
          &quot;enable_rotate&quot;: false
        }
      ]
    }
  ]
},
&quot;parameters&quot;: {
  &quot;ocr_options&quot;: {
    &quot;task&quot;: &quot;document_parsing&quot;
  }
}
}
'
</code></pre></div></div></section><a id="公式识别"></a><section><a id="公式识别-h4"></a><h4>公式识别</h4><blockquote><p>以下为调用公式识别内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-7"></a><div><a id="fig-code-group-7-python-tab"></a>python<div><a id="code-code-group-7-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;image&quot;: &quot;http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/formula_handwriting/test/inline_5_4.jpg&quot;,
                # 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192}]
            }]

response = client.multimodal.chat.create(
    model='qwen3.5-ocr',
    messages=messages,
    # 设置内置任务为公式识别
    parameters={&quot;ocr_options&quot;: {&quot;task&quot;: &quot;formula_recognition&quot;}}
)

# 公式识别任务以LaTeX格式返回结果
print(response.output_text)
</code></pre></div><a id="fig-code-group-7-java-tab"></a>java<div><a id="code-code-group-7-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/formula_handwriting/test/inline_5_4.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);
        // 配置内置的OCR任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.FORMULA_RECOGNITION)
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                        )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
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
</code></pre></div><a id="fig-code-group-7-bash-tab"></a>bash<div><a id="code-code-group-7-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '
{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;image&quot;: &quot;http://duguang-llm.oss-cn-hangzhou.aliyuncs.com/llm_data_keeper/data/formula_handwriting/test/inline_5_4.jpg&quot;,
            &quot;min_pixels&quot;: 3072,
            &quot;max_pixels&quot;: 8388608,
            &quot;enable_rotate&quot;: false
          }
        ]
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;ocr_options&quot;: {
      &quot;task&quot;: &quot;formula_recognition&quot;
    }
  }
}
'
</code></pre></div></div></section><a id="通用文字识别"></a><section><a id="通用文字识别-h4"></a><h4>通用文字识别</h4><blockquote><p>以下为调用通用文字识别内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-8"></a><div><a id="fig-code-group-8-python-tab"></a>python<div><a id="code-code-group-8-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg&quot;,
                # 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192}]
        }]

response = client.multimodal.chat.create(
    model='qwen3.5-ocr',
    messages=messages,
    # 设置内置任务为通用文字识别
    parameters={&quot;ocr_options&quot;: {&quot;task&quot;: &quot;text_recognition&quot;}}
)
# 通用文字识别任务以纯文本格式返回结果
print(response.output_text)
</code></pre></div><a id="fig-code-group-8-java-tab"></a>java<div><a id="code-code-group-8-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);

        // 配置内置任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.TEXT_RECOGNITION)
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                        )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
               // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
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
</code></pre></div><a id="fig-code-group-8-bash-tab"></a>bash<div><a id="code-code-group-8-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'\
  --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;\
  --header 'Content-Type: application/json'\
  --data '{
&quot;model&quot;: &quot;qwen3.5-ocr&quot;,
&quot;input&quot;: {
  &quot;messages&quot;: [
    {
      &quot;role&quot;: &quot;user&quot;,
      &quot;content&quot;: [{
          &quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg&quot;,
          &quot;min_pixels&quot;: 3072,
          &quot;max_pixels&quot;: 8388608,
          &quot;enable_rotate&quot;: false
        }
      ]
    }
  ]
},
&quot;parameters&quot;: {
  &quot;ocr_options&quot;: {
      &quot;task&quot;: &quot;text_recognition&quot;
    }
}
}'
</code></pre></div></div></section><a id="多语言识别"></a><section><a id="多语言识别-h4"></a><h4>多语言识别</h4><blockquote><p>以下为调用通用多语言识别内置任务的代码示例，详情请参见<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/qwen-vl-ocr.md#3ea70c9a1a4lz">调用内置任务</a>。</p></blockquote><a id="fig-code-group-9"></a><div><a id="fig-code-group-9-python-tab"></a>python<div><a id="code-code-group-9-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

messages = [{
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [{
                &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN01VvUMNP1yq8YvkSDFY_!!6000000006629-2-tps-6000-3000.png&quot;,
                # 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192}]
            }]

response = client.multimodal.chat.create(
    model='qwen3.5-ocr',
    messages=messages,
    # 设置内置任务为多语言识别
    parameters={&quot;ocr_options&quot;: {&quot;task&quot;: &quot;multi_lan&quot;}}
)
# 多语言识别任务以纯文本的形式返回结果
print(response.output_text)
</code></pre></div><a id="fig-code-group-9-java-tab"></a>java<div><a id="code-code-group-9-java"></a><pre class="language-java"><code>import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.multimodalconversation.OcrOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;https://img.alicdn.com/imgextra/i2/O1CN01VvUMNP1yq8YvkSDFY_!!6000000006629-2-tps-6000-3000.png&quot;);
        // 输入图像的最大像素阈值，超过该值图像会进行缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会进行放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 是否开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);
        // 配置内置的OCR任务
        OcrOptions ocrOptions = OcrOptions.builder()
                .task(OcrOptions.Task.MULTI_LAN)
                .build();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map
                        )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .ocrOptions(ocrOptions)
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
</code></pre></div><a id="fig-code-group-9-bash-tab"></a>bash<div><a id="code-code-group-9-bash"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '
{
  &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
  &quot;input&quot;: {
    &quot;messages&quot;: [
      {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
          {
            &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN01VvUMNP1yq8YvkSDFY_!!6000000006629-2-tps-6000-3000.png&quot;,
            &quot;min_pixels&quot;: 3072,
            &quot;max_pixels&quot;: 8388608,
            &quot;enable_rotate&quot;: false
          }
        ]
      }
    ]
  },
  &quot;parameters&quot;: {
    &quot;ocr_options&quot;: {
      &quot;task&quot;: &quot;multi_lan&quot;
    }
  }
}
'
</code></pre></div></div></section><a id="流式输出-2"></a><section><a id="流式输出-2-h4"></a><h4>流式输出</h4><a id="fig-code-group-10"></a><div><a id="fig-code-group-10-python-tab"></a>Python<div><a id="code-code-group-10-python"></a><pre class="language-python"><code>import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
# 若使用弗吉尼亚地域模型，需要将region换成 us-east-1；若使用新加坡地域的模型，需将region替换为 ap-southeast-1。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;,
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;),
    workspace=&quot;{WorkspaceId}&quot;,
    region=&quot;cn-beijing&quot;,
)

PROMPT_TICKET_EXTRACTION = &quot;&quot;&quot;
请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。
要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。
返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'},
&quot;&quot;&quot;

messages = [
    {
        &quot;role&quot;: &quot;user&quot;,
        &quot;content&quot;: [
            {
                &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;,
                # 输入图像的最小像素阈值，小于该值图像会放大，直到总像素大于min_pixels
                &quot;min_pixels&quot;: 32 * 32 * 3,
                # 输入图像的最大像素阈值，超过该值图像会缩小，直到总像素低于max_pixels
                &quot;max_pixels&quot;: 32 * 32 * 8192,
            },
            # 未设置内置任务时，支持在text字段中传入Prompt，若未传入则使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
            {
                &quot;type&quot;: &quot;text&quot;,
                &quot;text&quot;: PROMPT_TICKET_EXTRACTION,
            },
        ],
    }
]
stream = client.multimodal.chat.create(
    model=&quot;qwen3.5-ocr&quot;,
    messages=messages,
    stream=True,
    # 流式输出默认为增量模式：每个数据块仅包含新生成的内容。
)

full_content = &quot;&quot;
print(&quot;流式输出内容为：&quot;)
for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content)
        full_content += delta.content
print(f&quot;完整内容为：{full_content}&quot;)
</code></pre></div><a id="fig-code-group-10-java-tab"></a>Java<div><a id="code-code-group-10-java"></a><pre class="language-java"><code>import java.util.*;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为北京地域 base_url，若使用弗吉尼亚地域模型，需要将base_url换成 https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1
    // 若使用新加坡地域的模型，需将base_url替换为：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1
    static {Constants.baseHttpApiUrl=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;;}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        Map&lt;String, Object&gt; map = new HashMap&lt;&gt;();
        map.put(&quot;image&quot;, &quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;);
        // 输入图像的最大像素阈值，超过该值图像会缩小，直到总像素低于max_pixels
        map.put(&quot;max_pixels&quot;, 8388608);
        // 输入图像的最小像素阈值，小于该值图像会放大，直到总像素大于min_pixels
        map.put(&quot;min_pixels&quot;, 3072);
        // 开启图像自动转正功能
        map.put(&quot;enable_rotate&quot;, false);
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        map,
                        // 模型未设置内置任务时，支持在text字段中传入Prompt，若未传入则使用默认的Prompt：Please output only the text content from the image without any additional descriptions or formatting.
                        Collections.singletonMap(&quot;text&quot;, &quot;请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'&quot;))).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey(&quot;sk-xxx&quot;)
               // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv(&quot;DASHSCOPE_API_KEY&quot;))
                .model(&quot;qwen3.5-ocr&quot;)
                .message(userMessage)
                .incrementalOutput(true)
                .build();
        Flowable&lt;MultiModalConversationResult&gt; result = conv.streamCall(param);
        result.blockingForEach(item -&gt; {
            try {
                List&lt;Map&lt;String, Object&gt;&gt; contentList = item.getOutput().getChoices().get(0).getMessage().getContent();
                if (!contentList.isEmpty()){
                    System.out.println(contentList.get(0).get(&quot;text&quot;));
                }//
            } catch (Exception e){
                System.exit(0);
            }
        });
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
</code></pre></div><a id="fig-code-group-10-curl-tab"></a>curl<div><a id="code-code-group-10-curl"></a><pre class="language-bash"><code># ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域base_url，若使用弗吉尼亚地域模型，需要将base_url换成：https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 若使用新加坡地域的模型，需要将base_url换成：https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# === 执行时请删除该注释 ===

curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
--data '{
    &quot;model&quot;: &quot;qwen3.5-ocr&quot;,
    &quot;input&quot;:{
        &quot;messages&quot;:[
          {
            &quot;role&quot;: &quot;user&quot;,
            &quot;content&quot;: [
                {
                    &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i2/O1CN01ktT8451iQutqReELT_!!6000000004408-0-tps-689-487.jpg&quot;,
                    &quot;min_pixels&quot;: 3072,
                    &quot;max_pixels&quot;: 8388608
                },
                {&quot;type&quot;: &quot;text&quot;, &quot;text&quot;: &quot;请提取车票图像中的发票号码、车次、起始站、终点站、发车日期和时间点、座位号、席别类型、票价、身份证号码、购票人姓名。要求准确无误的提取上述关键信息、不要遗漏和捏造虚假信息，模糊或者强光遮挡的单个文字可以用英文问号?代替。返回数据格式以json方式输出，格式为：{'发票号码': 'xxx', '起始站': 'xxx', '终点站': 'xxx', '发车日期和时间点':'xxx', '座位号': 'xxx','票价':'xxx', '身份证号码': 'xxx', '购票人姓名': 'xxx'&quot;}
            ]
          }
        ]
    },
    &quot;parameters&quot;: {
        &quot;incremental_output&quot;: true
    }
}'
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="0e1c44902ea1e"></a><h3>chat响应对象（流式与非流式输出格式一致）</h3><blockquote><p>以下为HTTP接口返回的原始响应。调用失败时，Python SDK 会抛出 <code>DashScopeError</code> 异常，可通过异常属性 <code>e.status_code</code>/<code>e.code</code>/<code>e.message</code>/<code>e.request_id</code> 获取错误信息；Java SDK 调用失败会抛出异常，异常信息为<strong>status_code</strong>和<strong>message</strong>的内容。</p></blockquote><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><blockquote><p>Java SDK返回参数为<strong>requestId。</strong></p></blockquote><p><strong>output</strong><code>object</code></p><p>调用结果信息。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code></p><p>该参数当前固定为<code>null</code>。</p><p><strong>finish_reason</strong><code>string</code></p><p>模型结束生成的原因。有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code>；</li></ul><p><strong>choices</strong><code>array</code></p><p>模型的输出信息。</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>finish_reason</strong><code>string</code></p><p>有以下情况：</p><ul><li>正在生成时为<code>null</code>；</li><li>因模型输出自然结束为<code>stop</code>；</li><li>因生成长度过长而结束为<code>length</code>；</li></ul><p><strong>message</strong><code>object</code></p><p>模型输出的消息对象。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>输出消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>object</code></p><p>输出消息的内容。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>ocr_result</strong><code>object</code></p><p>当Qwen-OCR系列模型调用内置的信息抽取、高精识别任务时，输出的任务结果信息。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>kv_result</strong><code>array</code></p><p>信息抽取任务的输出结果。</p><p><strong>words_info</strong><code>array</code></p><p>高精识别任务的输出结果。</p><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>rotate_rect</strong> <code>array</code></p><p>示例值：<code>[center_x, center_y, width, height, angle]</code></p><p>文字框的旋转矩形表示：</p><ul><li><code>center_x、center_y为文本框中心点坐标</code></li><li><code>width</code>为文本框宽度，<code>height</code>为高度</li><li><code>angle</code>为文本框相对于水平方向的旋转角度，取值范围为<code>[-90, 90]</code></li></ul><p><strong>location</strong> <code>array</code></p><p>示例值：<code>[x1, y1, x2, y2, x3, y3, x4, y4]</code></p><p>文字框四个顶点的坐标，坐标顺序为左上角开起，按左上角→右上角→右下角→左下角的顺时针顺序排列。</p><p><strong>text</strong><code>string</code></p><p>文本行的内容</p></div></section><p><strong>text</strong><code>string</code></p><p>输出消息的内容。</p></div></section><p><strong>processed_text</strong><code>string</code></p><p>对模型原始输出进行后处理的结果，自动删除重复片段等。当模型输出存在重复内容时，该字段提供清洗后的文本。</p></div></section><p><strong>logprobs</strong><code>object</code></p><p>当前 choices 对象的概率信息。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>content</strong> <code>array</code></p><p>带有对数概率信息的 Token 数组。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 null 表示概率值极低。</p><p><strong>top_logprobs</strong> <code>array</code></p><p>当前 Token 位置最可能的若干个 Token 及其对数概率，元素个数与入参的<code>top_logprobs</code>保持一致。</p><a id="accordion-属性-27"></a><section><p>属性</p><div><p><strong>token</strong> <code>string</code></p><p>当前 Token。</p><p><strong>bytes</strong> <code>array</code></p><p>当前 Token 的 UTF‑8 原始字节列表，用于精确还原输出内容，在处理表情符号、中文字符时有帮助。</p><p><strong>logprob</strong> <code>float</code></p><p>当前 Token 的对数概率。返回值为 null 表示概率值极低。</p></div></section></div></section></div></section></div></section></div></section></div></section><p><strong>usage</strong><code>object</code></p><p>本次请求使用的Token信息。</p><a id="accordion-属性-28"></a><section><p>属性</p><div><p><strong>input_tokens</strong> <code>integer</code></p><p>输入 Token 数。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出 Token 数。</p><p><strong>characters</strong> <code>integer</code></p><p>该参数当前固定为0。</p><p><strong>input_tokens_details</strong><code>object</code></p><p>输入 Token 的细粒度分类。</p><a id="accordion-属性-29"></a><section><p>属性</p><div><p><strong>image_tokens</strong> <code>integer</code></p><p>模型输入的图像对应的 Token数。</p><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p></div></section><p><strong>output_tokens_details</strong><code>object</code></p><p>输出 Token 的细粒度分类。</p><a id="accordion-属性-30"></a><section><p>属性</p><div><p><strong>text_tokens</strong> <code>integer</code></p><p>模型输入的文本对应的Token 数。</p></div></section><p><strong>total_tokens</strong> <code>integer</code></p><p>消耗的总 Token 数，为<code>input_tokens</code>与<code>output_tokens</code>的总和。</p><p><strong>image_tokens</strong> <code>integer</code></p><p>输入内容包含<code>image</code>时返回该字段。为用户输入图片内容转换成Token后的长度。</p></div></section></td><td><a id="code-block-12"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;8f8c0f6e-6805-4056-bb65-d26d66080a41&quot;,
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
              &quot;ocr_result&quot;: {
                &quot;kv_result&quot;: {
                  &quot;不含税价&quot;: &quot;230769.23&quot;,
                  &quot;发票代码&quot;: &quot;142011726001&quot;,
                  &quot;组织机构代码&quot;: &quot;null&quot;,
                  &quot;购买方名称&quot;: &quot;蔡应时&quot;,
                  &quot;销售方名称&quot;: &quot;null&quot;
                }
              },
              &quot;text&quot;: &quot;```json\n{\n    \&quot;不含税价\&quot;: \&quot;230769.23\&quot;,\n    \&quot;发票代码\&quot;: \&quot;142011726001\&quot;,\n    \&quot;组织机构代码\&quot;: \&quot;null\&quot;,\n    \&quot;购买方名称\&quot;: \&quot;蔡应时\&quot;,\n    \&quot;销售方名称\&quot;: \&quot;null\&quot;\n}\n```&quot;,
              &quot;processed_text&quot;: &quot;```json\n{\n    \&quot;不含税价\&quot;: \&quot;230769.23\&quot;,\n    \&quot;发票代码\&quot;: \&quot;142011726001\&quot;,\n    \&quot;组织机构代码\&quot;: \&quot;null\&quot;,\n    \&quot;购买方名称\&quot;: \&quot;蔡应时\&quot;,\n    \&quot;销售方名称\&quot;: \&quot;null\&quot;\n}\n```&quot;
            }
          ]
        }
      }
    ],
    &quot;audio&quot;: null
  },
  &quot;usage&quot;: {
    &quot;input_tokens&quot;: 926,
    &quot;output_tokens&quot;: 72,
    &quot;characters&quot;: 0,
    &quot;image_tokens&quot;: 754,
    &quot;input_tokens_details&quot;: {
      &quot;image_tokens&quot;: 754,
      &quot;text_tokens&quot;: 172
    },
    &quot;output_tokens_details&quot;: {
      &quot;text_tokens&quot;: 72
    },
    &quot;total_tokens&quot;: 998
  }
}
</code></pre></td></tr></tbody></table>

<a id="错误码"></a>

<a id="97e145aeabbwf"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。
