# 创意海报生成API参考

本文介绍创意海报生成模型的输入输出参数。根据要求自动生成海报的背景和文字排版，支持多种海报风格。无需设计基础，轻松制作出彩作品，让创意触手可及。

**相关指南**：[创意海报生成](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/creative-poster-generation-overview.md)

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   wanx-poster-generation-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[文本生成图像](../../../model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md)获取替代方案。

<a id="模型概览"></a>

<a id="a0c22dbf96vss"></a>

## 模型概览

<table><tbody><tr><td rowspan="2"><strong>模型名</strong></td><td rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></td><td rowspan="2"><strong>计费单价</strong></td><td colspan="2"><strong>限流（含主账号与RAM子账号）</strong></td></tr><tr><td><strong>任务下发接口QPS限制</strong></td><td><strong>同时处理中任务数量</strong></td></tr><tr><td><p>wanx-poster-generation-v1</p></td><td><p>500张</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md">文本生成图像</a>获取替代方案。</p></blockquote></td><td><p>2</p></td><td><p>1</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="917981085bo9m"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="ffa47ca257gkh"></a>

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建文生图任务，该请求会返回任务ID。
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="03e14ae842meh"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><p><strong>X-DashScope-Async</strong><em>string</em><strong>必选</strong></p><p>是否使用DashScope异步调用。HTTP只支持异步调用，设置为<code>enable</code>。</p><p><strong>Content-Type</strong><em>string</em><strong>必选</strong></p><p>请求内容类型。固定为<code>application/json</code>。</p><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4><p><strong>model</strong><em>string</em><strong>必选</strong></p><p>调用模型。创意海报生成模型为<code>wanx-poster-generation-v1</code>。</p><p><strong>parameters</strong> <em>object</em><strong>必选</strong></p><p>其他模型调用参数，只需要输入一个空对象即可。示例：<code>{}</code></p><p><strong>input</strong><em>object</em><strong>必选</strong></p><p>输入图像的基本信息，比如图像URL地址。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>generate_mode</strong> <em>string</em><strong>必选</strong></p><p>海报生成模式。</p><ul><li>generate：默认模式。</li><li>sr：高分辨率模式。</li><li>hrf：高清修复模式。</li><li>只能从[&quot;generate&quot;,&quot;sr&quot;,&quot;hrf&quot;]中选择。海报生成的基础模式为&quot;generate&quot;，选择此模式会返回海报图片的url（render_urls）和与其一一对应的辅助参数（auxiliary_parameters）。用户可从返回的结果中，选择需要进行分辨率提升（或者高清修复）的海报，通过二次调用，输入选中的海报对应的辅助参数，将generate_mode设置为&quot;sr&quot;（或者&quot;hrf&quot;），得到对应的高分辨率（高清修复）结果。</li></ul><p><strong>generate_num</strong> <em>Int</em>可选</p><p>生成的海报数。该参数只在<code>generate_mode=generate</code>时有效。</p><p>取值范围：[1,4]，默认为1。如果设置的值大于4，则默认生成4张图。</p><p><strong>auxiliary_parameters</strong> <em>string</em>可选</p><p>当generate_mode为&quot;sr&quot;或&quot;hrf&quot;时为必选项。需要提升分辨率或者高清修复的海报图片对应的辅助参数，数量限制为1。</p><a id="accordion-注"></a><section><p>注</p><div><p>该字段必须为海报生成服务的&quot;generate&quot;模式所返回的辅助参数。</p></div></section><p><strong>title</strong> <em>string</em><strong>必选</strong></p><p>主标题。最多30个字符。例如，&quot;春节快乐&quot;。</p><p><strong>sub_title</strong> <em>string</em>可选</p><p>副标题。最多30个字符。例如，“家庭团聚，共享天伦之乐&quot;。</p><p><strong>body_text</strong> <em>string</em>可选</p><p>正文。最多50个字符。例如：&quot;春节是中国最重要的传统节日之一，它象征着新的开始和希望&quot;</p><p><strong>prompt_text_zh</strong> <em>string</em>可选</p><p>中文提示词。例如，“小朋友画的可爱的龙，白色背景&quot;</p><blockquote><p>中文和英文提示词至少二选一设置，支持两个参数同时设置。两个字段字符数加起来最多50个字/单词。</p></blockquote><p><strong>prompt_text_en</strong> <em>string</em>可选</p><p>的英文提示词。例如：&quot;Children draw a lovely dragon, white background&quot;。</p><blockquote><p>中文和英文提示词至少二选一设置，支持两个参数同时设置。两个字段字符数加起来最多50个字/单词。</p></blockquote><p><strong>wh_ratios</strong> <em>string</em>可选</p><p>生成海报的版式。</p><ul><li>横版：默认值。</li><li>竖版</li></ul><p><strong>lora_name</strong> <em>string</em>可选</p><p>海报风格名称。默认值为&quot;&quot;。</p><a id="accordion-海报风格枚举值及图示"></a><section><p>海报风格枚举值及图示</p><div><ul><li>2D插画1</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817373.jpeg" alt="image.jpeg"><ul><li>2D插画2</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817371.jpeg" alt="image.jpeg"><ul><li>浩瀚星云</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817370.jpeg" alt="image.jpeg"><ul><li>浓郁色彩</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817378.jpeg" alt="image.jpeg"><ul><li>光线粒子</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817368.jpeg" alt="image.jpeg"><ul><li>透明玻璃</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817374.jpeg" alt="image.jpeg"><ul><li>剪纸工艺</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817376.jpeg" alt="image.jpeg"><ul><li>折纸工艺</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817380.jpeg" alt="image.jpeg"><ul><li>中国水墨</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817377.jpeg" alt="image.jpeg"><ul><li>中国刺绣</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817372.jpeg" alt="image.jpeg"><ul><li>真实场景</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817382.jpeg" alt="image.jpeg"><ul><li>2D卡通</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817384.png" alt="image.png"><ul><li>儿童水彩</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817383.jpeg" alt="image.jpeg"><ul><li>赛博背景</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817375.jpeg" alt="image.jpeg"><ul><li>浅蓝抽象</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817381.jpeg" alt="image.jpeg"><ul><li>深蓝抽象</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817379.jpeg" alt="image.jpeg"><ul><li>抽象点线</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817385.jpeg" alt="image.jpeg"><ul><li>童话油画</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5391000271/p817369.jpeg" alt="image.jpeg"></div></section><p><strong>lora_weight</strong> <em>float</em>可选</p><p>海报风格权重，需要与lora_name参数配合使用。</p><p>取值范围：[0, 1]，默认值为0.8。取值越接近1，海报风格越明显。</p><p><strong>ctrl_ratio</strong> <em>float</em>可选</p><p>留白效果权重，用于控制海报留白效果。</p><p>取值范围：[0, 1]，默认值为0.7。取值越接近1，留白效果越好，但海报背景生成效果可能会受到负面影响。</p><p><strong>ctrl_step</strong> <em>float</em>可选</p><p>留白步数比例，用于控制海报留白效果。</p><p>取值范围：(0, 1]，默认值为0.7。取值越接近1，留白效果越好，但是海报背景生成效果可能会受到负面影响。</p><p><strong>creative_title_layout</strong> <em>bool</em>可选</p><p>标题是否启用创意排版。默认值为false。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="春节快乐海报"></a><section><a id="春节快乐海报-h4"></a><h4>春节快乐海报</h4><p>调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data-raw '{
    &quot;model&quot;:&quot;wanx-poster-generation-v1&quot;,
    &quot;input&quot;: {
        &quot;title&quot;:&quot;春节快乐&quot;,
        &quot;sub_title&quot;:&quot;家庭团聚，共享天伦之乐&quot;,
        &quot;body_text&quot;:&quot;春节是中国最重要的传统节日之一，它象征着新的开始和希望&quot;,
        &quot;prompt_text_zh&quot;:&quot;灯笼，小猫，梅花&quot;,
        &quot;wh_ratios&quot;:&quot;竖版&quot;,
        &quot;lora_name&quot;:&quot;童话油画&quot;,
        &quot;lora_weight&quot;:0.8,
        &quot;ctrl_ratio&quot;:0.7,
        &quot;ctrl_step&quot;:0.7,
        &quot;generate_mode&quot;:&quot;generate&quot;,
        &quot;generate_num&quot;:1
    },
    &quot;parameters&quot;:{}
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_id</strong> <em>string</em></p><p>任务id。</p><p><strong>task_status</strong> <em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li></ul></div></section><p><strong>code</strong><em>string</em></p><p>接口错误码。接口成功请求不会返回该参数。</p><p><strong>message</strong><em>string</em></p><p>接口错误信息。接口成功请求不会返回该参数。</p><p><strong>request_id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-成功响应-tab"></a>成功响应<div><a id="code-code-group-成功响应"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
	&quot;task_id&quot;: &quot;d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;PENDING&quot;
    },
    &quot;request_id&quot;: &quot;7574ee8f-38a3-4b1e-9280-11c33ab46e51&quot;
}
</code></pre></div><a id="fig-code-group-异常响应-tab"></a>异常响应<div><a id="code-code-group-异常响应"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="481754a27e8sb"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<table><tbody><tr><td><a id="5043fa882c26r"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong><em>string</em><strong>必选</strong></p><p>任务id。</p></td><td><a id="sec-tabs-2"></a><section><a id="获取任务结果"></a><section><a id="获取任务结果-h4"></a><h4>获取任务结果</h4><p>调用时请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location --request GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="fcab464334gzq"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <em>string</em></p><p>任务id。</p><p><strong>task_status</strong> <em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li></ul><p><strong>render_urls</strong> <em>list[string]</em></p><p>海报图像URL列表。海报图像URL有效时限为24小时。</p><ul><li>当<code>generate_mode=generate</code>时，返回1～4张海报图像的URL列表。</li><li>当<code>generate_mode=sr</code>或者<code>generate_mode=hrf</code>时，返回1张海报图像的URL。</li></ul><p>在返回海报图像URL之前，会进行敏感信息检测。如发现敏感内容，将拦截该图像，并替换为<code>output data may contain inappropriate content</code>。</p><p><strong>auxiliary_parameters</strong> <em>List[String]</em></p><p>高清修复和提升分辨率的辅助参数，与render_urls列表的URL一一对应。有效时限为24小时。</p><p>接口返回的auxiliary_parameters可用于二次调用，将其作为入参，对海报进行分辨率提升或者高清修复。</p><p>在返回海报图像URL之前，会进行敏感信息检测。如发现敏感内容，将拦截该图像，并替换为<code>output data may contain inappropriate content</code>。</p><p><strong>bg_urls</strong> <em>List[String]</em></p><p>不含文字的海报背景图URL。有效时限为24小时。</p><ul><li>当<code>generate_mode=generate</code>时，返回1～4张海报图像的URL列表。</li><li>当<code>generate_mode=sr</code>或者<code>generate_mode=hrf</code>时，返回1张海报图像的URL。</li></ul><p>在返回海报图像URL之前，会进行敏感信息检测。如发现敏感内容，将拦截该图像，并替换为<code>output data may contain inappropriate content</code>。</p><p><strong>task_metrics</strong> <em>object</em></p><p>任务信息统计指标。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <em>integer</em></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <em>integer</em></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <em>integer</em></p><p>任务状态为失败的任务数。</p></div></section><p><strong>submit_time</strong> <em>string</em></p><p>任务提交时间。</p><p><strong>scheduled_time</strong> <em>string</em></p><p>任务排期执行时间。</p><p><strong>end_time</strong> <em>string</em></p><p>任务完成时间。</p><p><strong>code</strong><em>string</em></p><p>接口错误码。接口成功请求不会返回该参数。</p><p><strong>message</strong><em>string</em></p><p>接口错误信息。接口成功请求不会返回该参数。</p></div></section><p><strong>usage</strong><em>object</em></p><p>输出信息统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>image_count</strong> <em>integer</em></p><p>生成图像的数量。</p></div></section><p><strong>request_id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-任务执行成功-tab"></a>任务执行成功<div><a id="code-code-group-2-任务执行成功"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;b67df059-ca6a-9d51-afcd-9b3c4456b1e2&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;d76ec1e8-ea27-4038-8913-235c88ef0f70&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2024-05-16 13:50:01.247&quot;,
        &quot;scheduled_time&quot;: &quot;2024-05-16 13:50:01.354&quot;,
        &quot;end_time&quot;: &quot;2024-05-16 13:50:27.795&quot;,
        &quot;render_urls&quot;: [&quot;http://vision-poster.oss-cn-shanghai.aliyuncs.com/xxxxxx&quot;],
        &quot;auxiliary_parameters&quot;: [&quot;xxxxxx&quot;],
        &quot;bg_urls&quot;:[&quot;http://vision-poster.oss-cn-shanghai.aliyuncs.com/xxxxxx&quot;]
    },
    &quot;usage&quot;:{
      &quot;image_count&quot;:1
    }
}
</code></pre></div><a id="fig-code-group-2-任务执行中-tab"></a>任务执行中<div><a id="code-code-group-2-任务执行中"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;:&quot;RUNNING&quot;,
        &quot;task_metrics&quot;:{
            &quot;TOTAL&quot;:1,
            &quot;SUCCEEDED&quot;:1,
            &quot;FAILED&quot;:0
        }
    }
}
</code></pre></div><a id="fig-code-group-2-任务执行失败-tab"></a>任务执行失败<div><a id="code-code-group-2-任务执行失败"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;dccfdf23-b38e-97a6-a07b-f35118c1ada6&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;4cbabbdf-2c1f-43f4-b983-c2cc47f4c115&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;: &quot;2024-05-16 14:15:14.103&quot;,
        &quot;scheduled_time&quot;: &quot;2024-05-16 14:15:14.154&quot;,
        &quot;end_time&quot;: &quot;2024-05-16 14:15:14.694&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;check input data style&quot;
    }
}
</code></pre></div></div></td></tr></tbody></table>

<a id="错误码"></a>

<a id="Tk99S"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

同时本模型还有如下特定错误码：

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidParameter | check input data style | 输入参数不满足入参要求 |
| 500 | InternalError | inference error | 算法内部错误 |

<a id="常见问题"></a>

<a id="aa98e673c3avi"></a>

## 常见问题

-   **如何查询已经提交的所有异步任务？**
    
    具体操作请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。
    
-   **创意海报生成API是否支持对已经生成的海报进行二次编辑？**
    
    不支持对已生成海报的内容（如标题、正文、风格等）进行二次编辑。仅能通过再次调用本API来提升已生成海报的分辨率。如需调整海报的内容，请重新设计并生成新的海报。
    
    提升已生成海报分辨率的方法为：将上次生成海报时的输入参数`"generate_mode"`的值修改为`sr`或`hrf`，并在输入参数中新增`"auxiliary_parameters"`，其值为上次生成海报时返回的完整参数集，其它参数保持不变。
    
    调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。
    

<a id="code-block-3"></a>

```bash
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data-raw '{
    "model":"wanx-poster-generation-v1",
    "input": {
        "title":"春节快乐",
        "sub_title":"家庭团聚，共享天伦之乐",
        "body_text":"春节是中国最重要的传统节日之一，它象征着新的开始和希望",
        "prompt_text_zh":"灯笼，小猫，梅花",
        "wh_ratios":"竖版",
        "lora_name":"童话油画",
        "lora_weight":0.8,
        "ctrl_ratio":0.7,
        "ctrl_step":0.7,
        "generate_mode":"hrf",
        "auxiliary_parameters": "WMq4SC4......",
        "generate_num":1
    },
    "parameters":{}
}'
```
