# 虚拟模特API参考

本文介绍万相-虚拟模特模型的输入输出参数。该模型可以对上传的真人或者人台实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容。在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。同时支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。

**相关指南**：[虚拟模特生成](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/virtual-model-generation.md)

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   wanx-virtualmodel、virtualmodel-v2 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[图像编辑-千问](../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md)或[图像编辑-万相2.1](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)获取替代方案。

<a id="模型概览"></a>

<a id="50446bc4ab3pt"></a>

## 模型概览

万相-虚拟模特可以对上传的真人实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。

<table><thead><tr><th><strong>模型版本</strong></th><th><strong>模型名称</strong></th><th><strong>模型简介</strong></th></tr></thead><tbody><tr><td><p>虚拟模特</p><p>（V1版本）</p></td><td><p>wanx-virtualmodel</p></td><td><ul><li><p>支持真人实拍图上传</p></li></ul><ul><li><p>生成的图片短边：512像素或1024像素</p></li></ul></td></tr><tr><td><p>虚拟模特V2</p><p>（V2版本）</p></td><td><p>virtualmodel-v2</p></td><td><ul><li><p>支持真人、人台实拍图上传</p></li><li><p>生成的图片短边为：1024像素或2048像素</p></li><li><p>支持改变分辨率，生成图片长宽比可选择：比例不变、2:1、16:9、4:3、1:1、3:4、 9:16、1:2。</p></li><li><p>支持背景参考图权重自由控制</p></li><li><p>文本引导效果更准确</p></li></ul></td></tr></tbody></table>

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>计费单价</strong></th><th colspan="2"><strong>限流（主账号与RAM子账号共用）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></th></tr><tr><th><strong>任务下发接口RPS限制</strong></th><th><strong>同时处理中任务数量</strong></th></tr></thead><tbody><tr><td><p>wanx-virtualmodel</p></td><td rowspan="2"><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td rowspan="2"><p>2</p></td><td rowspan="2"><p>1</p></td><td rowspan="2"><p>500张</p></td></tr><tr><td><p>virtualmodel-v2</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="24334fea04ia9"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="ffa47ca257gkh"></a>

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建文生图任务，该请求会返回任务ID。
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="24e4121a7fyos"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> 注意：若无特殊说明，下面的参数支持在虚拟模特模型V1版本和V2版本中使用。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><p><strong>X-DashScope-Async</strong><em>string</em><strong>必选</strong></p><p>是否使用异步调用。HTTP只支持异步调用，设置为<code>enable</code>。</p><p><strong>Content-Type</strong><em>string</em><strong>必选</strong></p><p>请求内容类型。固定为<code>application/json</code>。</p><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4><p><strong>model</strong><em>string</em><strong>必选</strong></p><p>调用模型。</p><p><strong>input</strong><em>object</em><strong>必选</strong></p><p>输入图像的基本信息，比如图像URL地址。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>base_image_url</strong> <em>string</em><strong>必选</strong></p><p>原始真人展示图像URL地址。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG、WEBP。</li><li>图像分辨率：不低于256×256像素且不超过4096×4096像素，人脸占比不低于128×128像素。</li><li>图修比例：长宽比大于1:2且小于2:1。</li><li>图像大小：不超过5MB。</li><li>URL地址中不能包含中文字符。</li></ul><a id="accordion-真人图像示例"></a><section><p>真人图像示例</p><div><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7749386271/p850516.png" alt="image"></div></section><p><strong>mask_image_url</strong> <em>string</em><strong>必选</strong></p><p>对应原图的期望保留区域mask图URL，图片为（0,255）的黑白图，其中白色表示商品主体区域。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图片限制：</p><ul><li>图像格式：JPEG、JPG、PNG、WEBP。</li><li>图像分辨率：与base_image_url参数对应的图像保持一致。</li><li>图修比例：长宽比大于1:2且小于2:1。</li><li>图像大小：不超过5MB。</li><li>URL地址中不能包含中文字符。</li></ul><a id="accordion-mask图像示例"></a><section><p>mask图像示例</p><div><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7068778171/p810523.png" alt="image.png"></div></section><p><strong>predefined_face_id</strong> <em>string 可选</em></p><p>预设人物ID。<strong>仅在V1版本使用。</strong></p><a id="accordion-枚举示例"></a><section><p>枚举示例</p><div><ul><li>girl1</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850530.png" alt="image"><ul><li>girl2</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850531.png" alt="image"><ul><li>girl3</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850532.png" alt="image"><ul><li>boy1</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850533.png" alt="image"><ul><li>boy2</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850534.png" alt="image"><ul><li>boy3</li></ul><img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0489386271/p850535.png" alt="image"></div></section><p><strong>face_image_url</strong> <em>string 可选</em></p><p>期望替换的人物图像URL地址。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图片限制：</p><ul><li>图像格式：JPEG、JPG、PNG、WEBP。</li><li>图像分辨率：长边像素不大于2048，人脸区域大于128×128像素。</li><li>图像大小：建议不超过5MB。</li></ul><p>优先级低于predefined_face_id参数。</p><p><strong>prompt</strong> <em>string</em><strong>必选</strong></p><p>针对生成图像背景环境、模特的全身形象描述。</p><p>支持中英文，小于100字符。</p><p>示例：一名年轻女子，身穿白色短裤，极简风格调色板，长镜头，双色效果，暗银色和浅粉色。</p><p><strong>face_prompt</strong> <em>string</em><strong>必选</strong></p><p>生成人像面部描述，支持中英文，小于100字符。</p><p>示例：一名年轻女子，面容娇好，最好的品质。</p><p><strong>background_image_url</strong> <em>string 可选</em></p><p>背景环境参考图像URL地址。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图片限制：</p><ul><li>图像格式：JPEG、JPG、PNG、WEBP。</li><li>图像分辨率：图像长边像素不大于4096。</li><li>图像比例：长宽比小于等于2。</li><li>图像大小：不超过5MB。</li></ul><p><strong>bgstyle_scale</strong> <em>float 可选</em></p><p>背景参考图像权重控制。<strong>仅在V2版本使用。</strong></p><p>取值范围：[0.0, 1.0]，默认0.7。</p><p>数值越大表示参考程度越大。</p><p><strong>realPerson</strong> <em>bool 可选</em></p><p>输入图片是否是真人。<strong>仅在V2版本使用。</strong></p><ul><li>true：默认值，表示输入图像是真人。</li><li>false：表示输入图像是人台或者非真人。</li></ul><p><strong>style</strong> <em>string 可选</em></p><p>生成图片风格。<strong>仅在V2版本使用。</strong></p><p>可选参数[&quot;&quot;,&quot;portrait&quot;]，默认是portrait，</p><p>说明：portrait模式会增加一些景深，突出人像的效果*。*</p><p><strong>seed</strong> <em>integer 可选</em></p><p>控制生成seed。<strong>仅在V2版本使用。</strong></p><p>取值范围：[0, 4294967290]。不传时系统随机生成 seed。指定具体值（0～4294967290）时使用固定随机种子，相同 seed 值会生成相同结果。</p><p><strong>aspect_ratio</strong> <em>String 可选</em></p><p>生成图片长宽比例。<strong>仅在V2版本使用。</strong></p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><p>可选的比例有：</p><ul><li>比例不变，默认值</li><li>2:1</li><li>16:9</li><li>4:3</li><li>1:1</li><li>3:4</li><li>9:16</li><li>1:2</li></ul></div></section></div></section><p><strong>parameters</strong><em>object</em>可选</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>n</strong> <em>Integer 可选</em></p><p>生成图像的数量，支持 1~4 张，默认值 1。</p><p><strong>short_side_size</strong> <em>string</em><strong>必选</strong></p><p>指定生成的图像短边大小，单位：像素。生成图片和输入原图会保持相同的长宽比。</p><p>V1版本可选值：512和1024。</p><p>V2版本可选值：1024和2048</p></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-虚拟模特v1-tab"></a>虚拟模特V1<div><a id="code-code-group-虚拟模特v1"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx-virtualmodel&quot;,
  &quot;input&quot;: {
    &quot;base_image_url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm/common/images/6a4b3c2d1e0f9275.jpg&quot;,
    &quot;mask_image_url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm/common/images/6a4b3c2d1e0f9274.png&quot;,
    &quot;prompt&quot;: &quot;一名年轻女子，身穿白色短裤，极简风格调色板，长镜头，双色效果（暗银色和浅粉色）&quot;,
    &quot;face_prompt&quot;: &quot;年轻女子，面容姣好，最高品质&quot;
  },
  &quot;parameters&quot;: {
    &quot;short_side_size&quot;: &quot;512&quot;,
    &quot;n&quot;: 1
  }
}'
</code></pre></div><a id="fig-code-group-虚拟模特v2-tab"></a>虚拟模特V2<div><a id="code-code-group-虚拟模特v2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;virtualmodel-v2&quot;,
  &quot;input&quot;: {
    &quot;base_image_url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm/common/images/6a4b3c2d1e0f9275.jpg&quot;,
    &quot;mask_image_url&quot;: &quot;https://g-adoc.alcasset.com/media/maas_docs/sfm/common/images/6a4b3c2d1e0f9274.png&quot;,
    &quot;background_image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4644874271/p827239.png&quot;,
    &quot;prompt&quot;: &quot;a beautiful chinese woman stands in front of a plain white background&quot;,
    &quot;face_prompt&quot;: &quot;a beautiful chinese woman, good face, best face, best quality&quot;
  },
  &quot;parameters&quot;: {
      &quot;short_side_size&quot;: &quot;1024&quot;,
      &quot;n&quot;: 1
  }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <em>string</em></p><p>任务id。</p><p><strong>task_status</strong> <em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>code</strong><em>string</em></p><p>接口错误码。接口成功请求不会返回该参数。</p><p><strong>message</strong><em>string</em></p><p>接口错误信息。接口成功请求不会返回该参数。</p><p><strong>request_id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-成功响应-tab"></a>成功响应<div><a id="code-code-group-2-成功响应"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-28c7cece6b47&quot;
}
</code></pre></div><a id="fig-code-group-2-异常响应-tab"></a>异常响应<div><a id="code-code-group-2-异常响应"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="481754a27e8sb"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="5043fa882c26r"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong><em>string</em><strong>必选</strong></p><p>任务id。</p></td><td><a id="sec-tabs"></a><section><a id="获取任务结果"></a><section><a id="获取任务结果-h4"></a><h4>获取任务结果</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location --request GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="fcab464334gzq"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <em>string</em></p><p>任务id。</p><p><strong>task_status</strong> <em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li><li>UNKNOWN：任务不存在或状态未知</li></ul><p><strong>results</strong><em>array object</em></p><p>任务结果列表，包括图像URL。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>url</strong> <em>string</em></p><p>模型生成图片的URL地址。</p></div></section><p><strong>task_metrics</strong> <em>object</em></p><p>任务信息统计指标。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <em>integer</em></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <em>integer</em></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <em>integer</em></p><p>任务状态为失败的任务数。</p></div></section><p><strong>submit_time</strong> <em>string</em></p><p>任务提交时间。</p><p><strong>scheduled_time</strong> <em>string</em></p><p>任务排期执行时间。</p><p><strong>end_time</strong> <em>string</em></p><p>任务完成时间。</p><p><strong>result_url</strong> <em>string</em></p><p>输出图片url。</p><p><strong>code</strong><em>string</em></p><p>任务执行失败的错误码。</p><p><strong>message</strong><em>string</em></p><p>任务执行失败的详细信息。</p></div></section><p><strong>usage</strong><em>object</em></p><p>输出信息统计。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>image_count</strong> <em>integer</em></p><p>模型生成图像的数量。</p></div></section><p><strong>request_id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-2"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;f24149fe-4722-9763-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;9d62befa-0139-4e4d-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-04-24 10:51:35.004&quot;,
        &quot;scheduled_time&quot;: &quot;2025-04-24 10:51:35.033&quot;,
        &quot;end_time&quot;: &quot;2025-04-24 10:51:59.424&quot;,
        &quot;results&quot;: [
            {
                &quot;url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_1.png&quot;
            },
            {
                &quot;url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/test_2.png&quot;
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
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><a id="code-block-3"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;f24149fe-4722-9763-xxxxxx&quot;,
  &quot;output&quot;: {
    &quot;task_id&quot;: &quot;9d62befa-0139-4e4d-xxxxxx&quot;,
    &quot;task_status&quot;: &quot;FAILED&quot;,
    &quot;submit_time&quot;: &quot;2024-05-16 13:50:xx.xxx&quot;,
    &quot;scheduled_time&quot;: &quot;2024-05-16 13:50:xx.xxx&quot;,
    &quot;end_time&quot;: &quot;2024-05-16 13:50:xx.xxx&quot;,
    &quot;code&quot;: &quot;InvalidImageResolution&quot;,
    &quot;message&quot;: &quot;The input image resolution is too large or small&quot;
  },
  &quot;usage&quot;: {
    &quot;image_num&quot;: 0
  }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

此API还有特定状态码，具体如下所示。

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidFile.Content | The input image has no human body or has unclear human body. Please upload other image | 输入图片中没有人 |
| 400 | InvalidParameter | The request is missing required parameters or in a wrong format, please check the parameters that you send. | 入参格式不对 |
| 400 | InvalidURL | The request URL is invalid, please check the request URL is available and the request image format is one of the following types: JPEG, JPG, PNG, BMP, and WEBP. | 输入图片下载失败，请检查网络或者输入格式 |
| 400 | InvalidFile.Resolution | The image resolution is invalid, please make sure that the aspect ratio is smaller than 2.0, and largest length of image is smaller than 4096 | 上传图片大小不符合要求 |
| 500 | InternalError.Algo | An internal error occurs during computation, please try this model later. | 算法运行错误 |
