# 鞋靴模特API参考

本文介绍鞋靴模特模型的输入输出参数。鞋靴模特模型支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成，最终生成图片的效果布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新鞋AI试穿、模特穿戴布局重绘等场景。

**相关指南**：[鞋靴模特](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/shoes-and-boots-model.md)

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   shoemodel-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费。

<a id="模型概览"></a>

<a id="a0c22dbf96vss"></a>

## 模型概览

<table><tbody><tr><td rowspan="2"><strong>模型名</strong></td><td rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></td><td rowspan="2"><strong>计费单价</strong></td><td colspan="2"><strong>限流（含主账号与RAM子账号）</strong></td></tr><tr><td><strong>任务下发接口QPS限制</strong></td><td><strong>同时处理中任务数量</strong></td></tr><tr><td><p>shoemodel-v1</p></td><td><p>500张</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，敬请关注后续动态。</p></blockquote></td><td><p>2</p></td><td><p>1</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="15044a800dt2u"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="ffa47ca257gkh"></a>

## HTTP调用

为了减少等待时间并且避免请求超时，服务采用异步方式提供。您需要发起两个请求：

-   **创建任务**：首先发送一个请求创建鞋靴模特任务，该请求会返回任务ID。
-   **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="bde0fc73feflg"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐您使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><p><strong>X-DashScope-Async</strong><em>string</em><strong>必选</strong></p><p>是否使用DashScope异步调用。HTTP只支持异步调用，设置为<code>enable</code>。</p><p><strong>Content-Type</strong><em>string</em><strong>必选</strong></p><p>请求内容类型。固定为<code>application/json</code>。</p><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4><p><strong>model</strong><em>string</em><strong>必选</strong></p><p>调用模型。鞋靴模特生成模型为<code>shoemodel-v1</code>。</p><p><strong>parameters</strong> Integer<strong>必选</strong></p><p>图片生成的数量，目前支持 1~4 张，默认值 1。</p><p><strong>input</strong><em>object</em><strong>必选</strong></p><p>输入图像的基本信息，比如图像URL地址。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>template_image_url</strong> <em>string</em><strong>必选</strong></p><p>模板模特图片的URL地址。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图像限制：</p><ul><li>图片大小建议小于5M。</li><li>图像格式：jpg、png、jpeg、bmp、webp、avif。</li><li>图像比例：图长边与短边的比例需在<code>[2:3, 3:2]</code> 范围内，推荐比例为<code>4:3</code>。</li></ul><p><strong>shoe_image_url</strong> <em>list</em> <strong>必选</strong></p><p>鞋靴多视角图片URL地址。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><ul><li>图片大小建议小于5M。</li><li>图像格式：jpg、png、jpeg、bmp、webp、avif。</li><li>图像比例：图长边与短边的比例需在<code>[2:3, 3:2]</code> 范围内，推荐与模特模板一样，比例为<code>4:3</code>。</li><li>多视角图片张数小于3。</li></ul><p><strong>scale</strong> <em>float</em> 可选</p><p>控制生成强度。</p><p>范围在[2.0,8.0]，默认为5.0，数值越大，颜色越鲜亮。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="鞋靴模特试穿"></a><section><a id="鞋靴模特试穿-h4"></a><h4>鞋靴模特试穿</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;shoemodel-v1&quot;,
    &quot;input&quot;: {
        &quot;template_image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809310.webp&quot;,
        &quot;shoe_image_url&quot;: [&quot;https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809301.webp&quot;]
    },
    &quot;parameters&quot;:
    {
        &quot;n&quot;: 1
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_id</strong> <em>string</em></p><p>任务id。</p><p><strong>task_status</strong> <em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li></ul></div></section><p><strong>code</strong><em>string</em></p><p>任务执行失败的错误码。</p><p><strong>message</strong><em>string</em></p><p>任务执行失败的详细信息。</p><p><strong>request_id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-正常响应-tab"></a>正常响应<div><a id="code-code-group-正常响应"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
	&quot;task_id&quot;: &quot;d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;PENDING&quot;
    }
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

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="5043fa882c26r"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><em>string</em><strong>必选</strong></p><p>推荐使用阿里云百炼API-Key，也可填DashScope API-Key。例如：Bearer d1xxx2a。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong><em>string</em><strong>必选</strong></p><p>任务id。</p></td><td><a id="sec-tabs-2"></a><section><a id="获取任务结果"></a><section><a id="获取任务结果-h4"></a><h4>获取任务结果</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --location --request GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="fcab464334gzq"></a><h4>响应</h4><p><strong>output</strong><em>object</em></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <em>string</em></p><p>任务id。</p><p><strong>task_status</strong> <em>string</em></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li></ul><p><strong>task_metrics</strong> <em>object</em></p><p>任务信息统计指标。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <em>integer</em></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <em>integer</em></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <em>integer</em></p><p>任务状态为失败的任务数。</p></div></section><p><strong>submit_time</strong> <em>string</em></p><p>任务提交时间。</p><p><strong>scheduled_time</strong> <em>string</em></p><p>任务排期执行时间。</p><p><strong>end_time</strong> <em>string</em></p><p>任务完成时间。</p><p><strong>results</strong> <em>array</em></p><p>输出图片列表。每个元素包含一个<code>url</code>字段，表示生成图片的URL。</p><p><strong>code</strong><em>string</em></p><p>任务执行失败的错误码。</p><p><strong>message</strong><em>string</em></p><p>任务执行失败的详细信息。</p></div></section><p><strong>request_id</strong><em>string</em></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-任务执行成功-tab"></a>任务执行成功<div><a id="code-code-group-2-任务执行成功"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;&lt;your request id&gt;&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;&lt;your task id&gt;&quot;,
        &quot;task_status&quot;:&quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;:&quot;2024-05-16 13:50:xx.xxx&quot;,
        &quot;scheduled_time&quot;:&quot;2024-05-16 13:50:xx.xxx&quot;,
        &quot;end_time&quot;:&quot;2024-05-16 13:50:xx.xxx&quot;,
        &quot;results&quot;:[
            {
                &quot;url&quot;:&quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/res_img.png?Expires=xxx&amp;OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Signature=YOUR_SIGNATURE&quot;
            }
        ],
        &quot;task_metrics&quot;:{
            &quot;TOTAL&quot;:1,
            &quot;SUCCEEDED&quot;:1,
            &quot;FAILED&quot;:0
        }
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
  &quot;request_id&quot;: &quot;&lt;your request id&gt;&quot;,
  &quot;output&quot;: {
    &quot;task_id&quot;: &quot;&lt;your task id&gt;&quot;,
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
</code></pre></div></div></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

此API还有特定状态码，具体如下所示。

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidParameter | Required parameter(s) missing or invalid, please check the request parameters.（可根据实际情况修改） | 接口调用参数不合法 |
| 400 | InvalidFile.Content | The input image has no human body or has unclear human body. Please upload other image. | 输入图片中人体不完整或者没有人体 |
| 400 | InvalidParameter | The request is missing required parameters or in a wrong format, please check the parameters that you send. | 入参格式不对 |
| 400 | InvalidParameter.DataInspection | Unable to download the media resource during the data inspection process. | 数据检查过程中无法下载媒体资源，请检查输入URL是否可访问以及图片格式是否正确 |
| 400 | InvalidFile.Resolution | The image resolution is invalid, please make sure that the aspect ratio is smaller than 3:2, and largest length of image is smaller than 4096. | 上传图片大小不符合要求 |
| 500 | InternalError.Algo | An internal error occurs during computation, please try this model later. | 算法运行错误 |
