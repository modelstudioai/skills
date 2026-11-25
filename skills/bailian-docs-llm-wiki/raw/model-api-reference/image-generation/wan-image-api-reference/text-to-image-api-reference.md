# 万相-文生图V1版API参考

本文介绍万相-文生图V1版模型的输入输出参数。

**相关指南**：[文本生成图像](../../../model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md)

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   推荐使用全面升级的[文生图V2版模型](text-to-image-v2-api-reference.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，**能够为推理请求提供卓越的性能和更高的稳定性**，建议从 `https://dashscope.aliyuncs.com` 迁移至新域名。
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="模型概览"></a>

<a id="4a3e46b825d2k"></a>

## 模型概览

**模型简介**

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型简介</strong></p></th></tr></thead><tbody><tr><td><p>wanx-v1</p></td><td><p>万相-文本生成图像大模型，主要功能包括：</p><ul><li><p>支持中英文双语输入。</p></li><li><p>支持多种图像风格。</p></li><li><p>支持输入参考图片，进行内容或风格迁移，实现更加丰富的风格、主题及派别。</p></li></ul></td></tr></tbody></table>

更多说明请参见[模型计费及限流](text-to-image-api-reference.md#b8457b7223zhp)。

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

文生图V1版模型API支持通过HTTP和DashScope SDK进行调用。

在调用前，您需要[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。目前，该SDK已支持Python和Java。

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

图像模型处理时间较长，为了避免请求超时，HTTP调用仅支持异步获取模型结果。您需要发起两个请求：

1.  **创建任务获取任务ID**：首先发起创建任务请求，该请求会返回任务ID（task\_id）。
2.  **根据任务ID查询结果**：使用上一步获得的任务ID，查询任务状态及结果。任务成功执行时将返回图像URL，有效期24小时。

> **说明**
>
> 创建任务后，该任务将被加入到排队队列，等待调度执行。后续需要调用“根据任务ID查询结果接口”获取任务状态及结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="76829ab923es8"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><p><strong>X-DashScope-WorkSpace</strong><code>string</code>（可选）</p><p>阿里云百炼业务空间ID。示例值：llm-xxxx。</p><p>您可以在此<a href="../../../application-api-reference/flow-agent-api/application-call/obtain-the-app-id-and-workspace-id.md#732535cfc959h">获取Workspace ID</a>。</p><a id="accordion-详细说明"></a><section><p>详细说明</p><div><p>此参数根据阿里云百炼API Key进行填写。</p><ul><li>若为主账号API Key，可不填。不填则使用主账号权限，填写则使用对应的业务空间权限。</li><li>若为RAM子账号API Key，则必填。RAM子账号一定归属于某个业务空间。</li></ul><p>业务空间必须具备访问模型的权限，才能调用API。若无权限，请参考<a href="https://help.aliyun.com/zh/model-studio/use-workspace">授权子业务空间模型调用、训练和部署</a>。</p><blockquote><p>关于如何区分阿里云百炼主账号和RAM子账号，请参考<a href="https://help.aliyun.com/zh/model-studio/business-space-management">主账号管理</a>。</p></blockquote></div></section><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。示例值：wanx-v1。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词，用来描述生成图像中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过800个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p>提示词的使用技巧请参见<a href="../../../model-user-guide/use-cases/text-to-image-prompt.md">文生图Prompt指南</a>。</p><p><strong>negative_prompt</strong><code>string</code>（可选）</p><p>反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>ref_img</strong><code>string</code><strong>（</strong>可选<strong>）</strong></p><p>参考图像（垫图）的URL地址。模型根据参考图像生成相似风格的图像。</p><p>图像限制：</p><ul><li>图片格式：JPG、JPEG、PNG、BMP、TIFF、WEBP等常见格式。</li><li>图像大小：不超过10 MB。</li><li>图像分辨率：不低于256×256像素且不超过4096×4096像素。</li><li>URL地址中不能包含中文字符。</li></ul></div></section><p><strong>parameters</strong><code>object</code>（可选）</p><p>图像处理参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>style</strong><code>string</code>（可选）</p><p>输出图像的风格。目前支持以下风格取值：</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>&lt;auto&gt;：默认值，由模型随机输出图像风格。</li><li>&lt;photography&gt;：摄影。</li><li>&lt;portrait&gt;：人像写真。</li><li>&lt;3d cartoon&gt;：3D卡通。</li><li>&lt;anime&gt;：动画。</li><li>&lt;oil painting&gt;：油画。</li><li>&lt;watercolor&gt;：水彩。</li><li>&lt;sketch&gt;：素描。</li><li>&lt;chinese painting&gt;：中国画。</li><li>&lt;flat illustration&gt;：扁平插画。</li></ul></div></section><p><strong>size</strong><code>string</code>（可选）</p><p>输出图像的分辨率。目前支持4种图像分辨率：</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>1024*1024：默认值。</li><li>720*1280</li><li>768*1152</li><li>1280*720</li></ul></div></section><p><strong>n</strong><code>integer</code>（可选）</p><p>生成图片的数量。取值范围为1~4张，默认为4。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，用于控制模型生成内容的随机性。seed参数取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果给定了，则根据<code>n</code>的值分别为n张图片生成seed参数，例如n=4，算法将分别生成seed、seed+1、seed+2、seed+3作为参数的图片。</p><p>如果您希望生成内容保持相对稳定，请使用相同的seed参数值。</p><p><strong>ref_strength</strong><code>float</code><strong>（</strong>可选<strong>）</strong></p><p>控制输出图像与垫图（参考图）的相似度。</p><p>取值范围为[0.0, 1.0]。取值越大，代表生成的图像与参考图越相似。</p><p><strong>ref_mode</strong><code>string</code><strong>（</strong>可选<strong>）</strong></p><p>基于垫图（参考图）生成图像的模式。目前支持的模式有：</p><a id="accordion-枚举值-3"></a><section><p>枚举值</p><div><ul><li>repaint：默认值，基于参考图的内容生成图像。</li><li>refonly：基于参考图的风格生成图像。</li></ul></div></section></div></section></td><td><a id="sec-tabs"></a><section><a id="文字作画"></a><section><a id="文字作画-h4"></a><h4>文字作画</h4><a id="fig-code-group"></a><div><a id="fig-code-group-正向提示词-tab"></a>正向提示词<div><a id="code-code-group-正向提示词"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx-v1&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。&quot;
    },
    &quot;parameters&quot;: {
        &quot;style&quot;: &quot;&lt;auto&gt;&quot;,
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;n&quot;: 1
    }
}'
</code></pre></div><a id="fig-code-group-正向-反向提示词-tab"></a>正向+反向提示词<div><a id="code-code-group-正向-反向提示词"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx-v1&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。&quot;,
        &quot;negative_prompt&quot;: &quot;不要使用红色元素&quot;
    },
    &quot;parameters&quot;: {
        &quot;style&quot;: &quot;&lt;auto&gt;&quot;,
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;n&quot;: 1
    }
}'
</code></pre></div></div></section><a id="参考图生成"></a><section><a id="参考图生成-h4"></a><h4>参考图生成</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-基于参考图内容-tab"></a>基于参考图内容<div><a id="code-code-group-2-基于参考图内容"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx-v1&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一个英气的黑发女人，飞舞着金色的蝴蝶，背景中有若隐若现的水墨竹林，高细节，高质量。&quot;,
        &quot;ref_image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png&quot;
    },
    &quot;parameters&quot;: {
        &quot;style&quot;: &quot;&lt;auto&gt;&quot;,
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;n&quot;: 1,
        &quot;ref_strength&quot;: 1.0,
        &quot;ref_mode&quot;: &quot;repaint&quot;
    }
}'
</code></pre></div><a id="fig-code-group-2-基于参考图风格-tab"></a>基于参考图风格<div><a id="code-code-group-2-基于参考图风格"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wanx-v1&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;有一只黑色的小猫&quot;,
        &quot;ref_image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/gpqnqy/house.png&quot;
    },
    &quot;parameters&quot;: {
        &quot;style&quot;: &quot;&lt;auto&gt;&quot;,
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;n&quot;: 1,
        &quot;ref_strength&quot;: 0.7,
        &quot;ref_mode&quot;: &quot;refonly&quot;
    }
}'
</code></pre></div></div></section><a id="dashscope-cli"></a><section><a id="dashscope-cli-h4"></a><h4>dashscope CLI</h4><a id="code-block"></a><pre class="language-bash"><code>export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
dashscope image-synthesis create -m wanx2.1-t2i-turbo -p &quot;一只可爱的猫&quot; -n 1
</code></pre><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../../preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div><p>完整地域表见 <a href="../../preparations/base-url.md">Base URL 总览</a>。</p></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-4"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<table><tbody><tr><td><a id="c7a5b38b94icr"></a><h4>请求参数</h4><a id="6cbbceaeb6jyo"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><blockquote><p>若使用新加坡地域的模型，需将base_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="3f1ae57ce6qd5"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-5"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>task_metrics</strong> <code>object</code></p><p>任务结果统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section><p><strong>results</strong> <code>array of object</code></p><p>任务结果列表，包括图像URL、部分任务执行失败报错信息等。</p><a id="accordion-数据结构"></a><section><p>数据结构</p><div><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;results&quot;: [
        {
            &quot;url&quot;: &quot;&quot;
        },
        {
            &quot;code&quot;: &quot;&quot;,
            &quot;message&quot;: &quot;&quot;
        }
    ]
}
</code></pre></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;85eaba38-0185-99d7-8d16-4d9135238846&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;results&quot;: [
            {
                &quot;url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png&quot;
            },
            {
                &quot;url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/b2.png&quot;
            }
        ],
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 2,
            &quot;SUCCEEDED&quot;: 2,
            &quot;FAILED&quot;: 0
        }
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 2
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match the allowed size ['1024*1024', '720*1280', '1280*720']&quot;,
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 4,
            &quot;SUCCEEDED&quot;: 0,
            &quot;FAILED&quot;: 4
        }
    }
}
</code></pre></section><a id="任务部分失败"></a><section><a id="任务部分失败-h4"></a><h4>任务部分失败</h4><p>模型可以在一次任务中生成多张图片。只要有一张图片生成成功，任务状态将标记为<code>SUCCEEDED</code>，并且返回相应的图像URL。对于生成失败的图片，结果中会返回相应的失败原因。同时在usage统计中，只会对成功的结果计数。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;85eaba38-0185-99d7-8d16-4d9135238846&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;results&quot;: [
            {
                &quot;url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/123/a1.png&quot;
            },
            {
                &quot;code&quot;: &quot;InternalError.Timeout&quot;,
                &quot;message&quot;: &quot;An internal timeout error has occured during execution, please try again later or contact service support.&quot;
            }
        ],
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 2,
            &quot;SUCCEEDED&quot;: 1,
            &quot;FAILED&quot;: 1
        }
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-sdk调用"></a>

<a id="db17b3098c2iv"></a>

## DashScope SDK调用

请先确认已安装最新版DashScope SDK，否则可能运行报错：[安装SDK](../../preparations/install-sdk.md)。

DashScope SDK目前已支持Python和Java。

SDK与HTTP接口的参数名基本一致，参数结构根据不同语言的SDK封装而定。参数说明可参考[HTTP调用](text-to-image-api-reference.md#42703589880ts)。

由于图像模型处理时间较长，底层服务采用异步方式提供。SDK在上层进行了封装，支持同步、异步两种调用方式。

<a id="python-sdk调用"></a>

<a id="a3ad9a3b6d9if"></a>

### Python SDK调用

<a id="sec-tabs-5"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="3cd4969b00193"></a>

##### 请求示例

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-文字作画-tab"></a>

文字作画

<a id="code-code-group-3-文字作画"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

print('----sync call, please wait a moment----')
try:
    job = client.images.generate(model='wanx-v1',
                                 prompt=prompt,
                                 n=1,
                                 style='<watercolor>',
                                 size='1024*1024')
    print('response: %s' % job)
    # 在当前目录下保存图片
    for url in job.image_urls:
        file_name = PurePosixPath(unquote(urlparse(url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(url).content)
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="fig-code-group-3-参考图生成-tab"></a>

参考图生成

<a id="code-code-group-3-参考图生成"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

# 上传参考图方式：url链接和本地路径二选一
# 使用公网url链接
ref_img = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png"
# 使用本地文件路径（传入后SDK会自动上传）
sketch_image_url = './girl.png'

print('----sync call, please wait a moment----')
try:
    job = client.images.generate(model='wanx-v1',
                                 prompt=prompt,
                                 n=1,
                                 style='<auto>',
                                 size='1024*1024',
                                 parameters={'ref_mode': 'repaint', 'ref_strength': 1.0},
                                 # 本地文件路径也可作为ref_img的值传入：
                                 # extra_input={'ref_img': sketch_image_url},
                                 extra_input={'ref_img': ref_img})
    print(job)
    # 保留图片到当前目录
    for url in job.image_urls:
        file_name = PurePosixPath(unquote(urlparse(url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(url).content)
except DashScopeError as e:
    print(f"HTTP返回码：{e.status_code}")
    print(f"错误码：{e.code}")
    print(f"错误信息：{e.message}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="0c0533477emwb"></a>

##### 响应示例

<a id="code-block-9"></a>

```json
{
    "request_id": "4126d9dd-e037-9f32-8d56-6d29ab3f9a06",
    "task_id": "b476bc4e-35c1-4c4e-a4d9-xxxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxxx.png"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="e5003f55e8kjn"></a>

##### 请求示例

<a id="fig-code-group-4"></a>

<a id="fig-code-group-4-文字作画-tab"></a>

文字作画

<a id="code-code-group-4-文字作画"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

def async_call():
    print('----create task----')
    task_info = create_async_task()
    if task_info is None:
        return
    print('----wait task done then save image----')
    wait_async_task(task_info)

# 创建异步任务
def create_async_task():
    try:
        job = client.images.jobs.create(model='wanx-v1',
                                        prompt=prompt,
                                        n=1,
                                        style='<watercolor>',
                                        size='1024*1024')
        print(job)
        return job
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return None

# 等待异步任务结束（指数退避轮询，默认总预算24小时）
def wait_async_task(task):
    try:
        done = client.images.jobs.wait(task)
        print(done)
        for url in done.image_urls:
            file_name = PurePosixPath(unquote(urlparse(url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(url).content)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

# 获取异步任务信息
def fetch_task_status(task):
    try:
        snapshot = client.images.jobs.fetch(task.task_id)
        print(snapshot)
        print(snapshot.status)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task):
    try:
        job = client.images.jobs.cancel(task.task_id)
        print(job)
        print(job.status)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    async_call()
```

<a id="fig-code-group-4-参考图生成-tab"></a>

参考图生成

<a id="code-code-group-4-参考图生成"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。"

# 上传参考图方式：url链接和本地路径二选一
# 使用公网url链接
ref_img = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png"
# 使用本地文件路径（传入后SDK会自动上传）
sketch_image_url = './girl.png'

def async_call():
    print('----create task----')
    task_info = create_async_task()
    if task_info is None:
        return
    print('----wait task done then save image----')
    wait_async_task(task_info)

# 创建异步任务
def create_async_task():
    try:
        job = client.images.jobs.create(model='wanx-v1',
                                        prompt=prompt,
                                        n=1,
                                        style='<auto>',
                                        size='1024*1024',
                                        parameters={'ref_mode': 'repaint', 'ref_strength': 1.0},
                                        # 本地文件路径也可作为ref_img的值传入：
                                        # extra_input={'ref_img': sketch_image_url},
                                        extra_input={'ref_img': ref_img})
        print(job)
        return job
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return None

# 等待异步任务结束（指数退避轮询，默认总预算24小时）
def wait_async_task(task):
    try:
        done = client.images.jobs.wait(task)
        print(done)
        for url in done.image_urls:
            file_name = PurePosixPath(unquote(urlparse(url).path)).parts[-1]
            with open('./%s' % file_name, 'wb+') as f:
                f.write(requests.get(url).content)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    async_call()
```

<a id="ae28dc8f72g6i"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-10"></a>

```json
{
    "request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
    "task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

<a id="code-block-11"></a>

```json
{
    "request_id": "d861d3ba-4b29-9491-abad-266ef4fb2f08",
    "task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxxx.png"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="java-sdk调用"></a>

<a id="589b80853e6rn"></a>

### Java SDK调用

<a id="sec-tabs-6"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="b568661fa6mie"></a>

##### 请求示例

<a id="fig-code-group-5"></a>

<a id="fig-code-group-5-文字作画-tab"></a>

文字作画

<a id="code-code-group-5-文字作画"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void basicCall() throws ApiException, NoApiKeyException {
        String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(ImageSynthesis.Models.WANX_V1)
                        .prompt(prompt)
                        .style("<watercolor>")
                        .n(1)
                        .size("1024*1024")
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public void fetchTask() throws ApiException, NoApiKeyException {
        String taskId = "your task id";
        ImageSynthesis is = new ImageSynthesis();
        // If set DASHSCOPE_API_KEY environment variable, apiKey can null.
        ImageSynthesisResult result = is.fetch(taskId, null);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args){
        try{
            basicCall();
            //listTask();
        }catch(ApiException|NoApiKeyException e){
            System.out.println(e.getMessage());
        }
    }
}
```

<a id="fig-code-group-5-相似图生成-tab"></a>

相似图生成

<a id="code-code-group-5-相似图生成"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.HashMap;

public class Main {
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public void syncCall() {
        String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
        //使用公网url链接
        String refImage = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png";
        HashMap<String,Object> parameters = new HashMap<>();
        parameters.put("ref_strength", 0.5);
        parameters.put("ref_mode", "repaint");

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(ImageSynthesis.Models.WANX_V1)
                        .prompt(prompt)
                        .style("<auto>")
                        .n(1)
                        .size("1024*1024")
                        .refImage(refImage)
                        .parameters(parameters)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException|NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args){
        Main text2Image = new Main();
        text2Image.syncCall();
    }

}
```

<a id="2539143f9bnpo"></a>

##### 响应示例

<a id="code-block-12"></a>

```json
{
	"request_id": "150edcda-05d5-9ffe-8803-84626d1db623",
	"output": {
		"task_id": "f2098ff0-146e-404c-bb25-xxxxxxxx",
		"task_status": "SUCCEEDED",
		"results": [{
			"url": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxxx.png"
		}],
		"task_metrics": {
			"TOTAL": 1,
			"SUCCEEDED": 1,
			"FAILED": 0
		}
	},
	"usage": {
		"image_count": 1
	}
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

<a id="2fc30f223b9py"></a>

##### 请求示例

<a id="fig-code-group-6"></a>

<a id="fig-code-group-6-文字作画-tab"></a>

文字作画

<a id="code-code-group-6-文字作画"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public void asyncCall() {
        System.out.println("---create task----");
        String taskId = this.createAsyncTask();
        System.out.println("---wait task done then return image url----");
        this.waitAsyncTask(taskId);
    }

    /**
     * 创建异步任务
     * @return taskId
     */
    public String createAsyncTask() {
        String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(ImageSynthesis.Models.WANX_V1)
                        .prompt(prompt)
                        .style("<watercolor>")
                        .n(1)
                        .size("1024*1024")
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            result = imageSynthesis.asyncCall(param);
        } catch (Exception e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        String taskId = result.getOutput().getTaskId();
        System.out.println("taskId=" + taskId);
        return taskId;
    }

    /**
     * 等待异步任务结束
     * @param taskId 任务id
     * */
    public void waitAsyncTask(String taskId) {
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            //环境变量配置后，可在这里将apiKey设置为null
            result = imageSynthesis.wait(taskId, null);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    public static void main(String[] args){
        Main main = new Main();
        main.asyncCall();
    }
}
```

<a id="fig-code-group-6-相似图生成-tab"></a>

相似图生成

<a id="code-code-group-6-相似图生成"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public void asyncCall() {
        System.out.println("---create task----");
        String taskId = this.createAsyncTask();
        System.out.println("---wait task done then return image url----");
        this.waitAsyncTask(taskId);
    }

    /**
     * 创建异步任务
     * @return taskId
     */
    public String createAsyncTask() {
        String prompt = "近景镜头，18岁的中国女孩，古代服饰，圆脸，正面看着镜头，民族优雅的服装，商业摄影，室外，电影级光照，半身特写，精致的淡妆，锐利的边缘。";
        String refImage = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241031/rguyzt/girl.png";
        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(ImageSynthesis.Models.WANX_V1)
                        .prompt(prompt)
                        .style("<auto>")
                        .n(1)
                        .size("1024*1024")
                        .refImage(refImage)
                        .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            result = imageSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        String taskId = result.getOutput().getTaskId();
        System.out.println("taskId=" + taskId);
        return taskId;
    }

    /**
     * 等待异步任务结束
     * @param taskId 任务id
     * */
    public void waitAsyncTask(String taskId) {
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            // If you have set the DASHSCOPE_API_KEY in the system environment variable, the apiKey can be null.
            result = imageSynthesis.wait(taskId, null);
        } catch (ApiException|NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    public static void main(String[] args){
        Main text2Image = new Main();
        text2Image.asyncCall();
    }
}
```

<a id="adf8613a57bqa"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-13"></a>

```json
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-542f97709ba8",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

2、查询任务结果的响应示例

<a id="code-block-14"></a>

```json
{
	"request_id": "c44213ba-7aa3-91e4-97c1-c527ade82597",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "SUCCEEDED",
		"results": [{
			"url": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxxx.png"
		}],
		"task_metrics": {
			"TOTAL": 1,
			"SUCCEEDED": 1,
			"FAILED": 0
		}
	},
	"usage": {
		"image_count": 1
	}
}
```

<a id="图片输出存储域名"></a>

<a id="h7i8j9k0l1m2n"></a>

## 图片输出存储域名

通义万相图片生成服务会将生成的图片存储在OSS中，生成结果URL中的域名根据地域不同而不同。如果您的企业网络环境有出口白名单限制，需要将以下OSS域名加入白名单才能正常获取生成的图片结果。

目前支持以下10个地域的出口域名：

|  |  |
| --- | --- |
| **地域** | **OSS域名** |
| 华北2（北京） | `dashscope-result-bj.oss-cn-beijing.aliyuncs.com` |
| 华东1（杭州） | `dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com` |
| 华东2（上海） | `dashscope-result-sh.oss-cn-shanghai.aliyuncs.com` |
| 华北6（乌兰察布） | `dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com` |
| 华北3（张家口） | `dashscope-result-zjk.oss-cn-zhangjiakou.aliyuncs.com` |
| 华南1（深圳） | `dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com` |
| 华南2（河源） | `dashscope-result-hy.oss-cn-heyuan.aliyuncs.com` |
| 西南1（成都） | `dashscope-result-cd.oss-cn-chengdu.aliyuncs.com` |
| 华南3（广州） | `dashscope-result-gz.oss-cn-guangzhou.aliyuncs.com` |
| 华北6（乌兰察布）ACDR | `dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com` |

<a id="错误码"></a>

<a id="4533746f2c15t"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="6d3e655950tcy"></a>

## 常见问题

<a id="模型计费及限流"></a>

<a id="b8457b7223zhp"></a>

### 模型计费及限流

**免费额度**

-   额度说明：免费额度是指模型成功生成的输出图片数量。输入图片及模型处理失败的情况不占用免费额度。
-   领取方式：开通阿里云百炼大模型服务后自动发放，有效期90天。
-   使用账号：阿里云主账号与其RAM子账号共享免费额度。
-   更多详情请参见[新人免费额度](../../../model-user-guide/test-1/new-free-quota.md)。

**限时免费**

-   当计费为限时免费时，表示该模型处于公测阶段，免费额度用尽后不可使用。

**计费说明**

-   当计费有明确单价时，如0.2元/秒，表示该模型已商业化，免费额度用尽或过期后需付费使用。
-   计费项：只对模型成功生成的输出图片进行收费，其余情况暂不计费。
-   付费方式：由阿里云主账号统一付费。RAM子账号不能独立计量计费，必须由所属的主账号付费。如果您需要查询账单信息，请前往阿里云控制台[账单概览](https://billing-cost.console.aliyun.com/finance/month-bill/account)。
-   充值途径：您可以在阿里云控制台[费用与成本](https://billing-cost.console.aliyun.com/home?spm=a2c4g.11186623.0.0.2d543048F4KRQP)页面进行充值。
-   模型调用情况：您可以前往阿里云百炼的[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)查看模型调用量及调用次数。
-   更多计费问题请参见[计费项](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)。

**限流**

-   限流说明：阿里云主账号与其RAM子账号共享限流限制。
