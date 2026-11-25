# 万相-图像局部重绘API参考

本文介绍万相-图像局部重绘模型的输入输出参数。

**相关指南**：[图像局部重绘](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/vary-region.md)

> **重要**
>
> -   本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。
> -   wanx-x-painting 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[图像编辑-千问](../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md)或[图像编辑-万相2.1](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md)获取替代方案。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，**能够为推理请求提供卓越的性能和更高的稳定性**，建议从 `https://dashscope.aliyuncs.com` 迁移至新域名。
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="模型概览"></a>

<a id="0594943e081vt"></a>

## 模型概览

**模型效果示意**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1300704371/p885604.png)

**模型简介**

| 模型名称 | 模型简介 |
| --- | --- |
| wanx-x-painting | 万相-图像局部重绘根据用户输入的原始图片、局部区域涂抹图和prompt提示词文字内容，在涂抹区域生成与文字描述相对应的内容，而涂抹区域外的部分则基本保持不变。 |

**模型说明**

<table><thead><tr><th rowspan="2"><strong>模型名称</strong></th><th rowspan="2"><strong>计费单价</strong></th><th colspan="2"><strong>限流（主账号与RAM子账号共用）</strong></th><th rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></th></tr><tr><th><strong>任务下发接口QPS限制</strong></th><th><strong>同时处理中任务数量</strong></th></tr></thead><tbody><tr><td><p>wanx-x-painting</p></td><td><p>目前仅供免费体验。</p><blockquote><p>免费额度用完后不可调用，推荐参考<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/qwen-image-edit-guide.md">图像编辑-千问</a>或<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/wanx-image-edit.md">图像编辑-万相2.1</a>获取替代方案。</p></blockquote></td><td><p>2</p></td><td><p>1</p></td><td><p>500张</p></td></tr></tbody></table>

更多说明请参见[模型计费及限流说明](vary-region-api-reference.md#b8457b7223zhp)。

<a id="前提条件"></a>

<a id="8e0253f790lhf"></a>

## 前提条件

图像局部重绘API支持通过HTTP和DashScope SDK进行调用。

在调用前，您需要[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。目前，该SDK已支持Python和Java。

<a id="http调用"></a>

<a id="65796f7146azl"></a>

## HTTP调用

图像模型处理时间较长，为了避免请求超时，HTTP调用仅支持异步获取模型结果。您需要发起两个请求：

1.  **创建任务获取任务ID**：首先发起创建任务请求，该请求会返回任务ID（task\_id）。
2.  **根据任务ID查询结果**：使用上一步获得的任务ID，查询任务状态及结果。任务成功执行时将返回图像URL，有效期24小时。

> **说明**
>
> 创建任务后，该任务将被加入到排队队列，等待调度执行。后续需要调用“根据任务ID查询结果接口”获取任务状态及结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="f1a4f32d54adq"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="040b1c0e468bz"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。示例值：wanx-x-painting。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入的基本信息，如提示词、图像URL等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词，用来描述生成图像中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过75个字符，超过部分会自动截断。</p><p><strong>base_image_url</strong><code>string</code><strong>（必选）</strong></p><p>输入图像URL地址，不支持填写图像Base64数据。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP。</li><li>图像分辨率：大于256×256像素，小于4096×4096像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p><strong>mask_image_url</strong><code>string</code><strong>（必选）</strong></p><p>用户标记涂抹区域的图像URL地址，需要和base_image_url图像分辨率保持一致。不支持填写图像Base64数据。</p><p>URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。您也可在此<a href="../../more-about-models/get-temporary-file-url.md">获取临时公网URL</a>。</p><p>图像限制：</p><ul><li>图像格式：JPG、JPEG、PNG、BMP。</li><li>图像分辨率：大于256×256像素，小于4096×4096像素。</li><li>图像大小：不超过10MB。</li><li>URL地址中不能包含中文字符。</li></ul><p>您可以使用PS或者其他图像编辑工具在原图上涂抹获得掩码图像。</p></div></section><p><strong>parameters</strong><code>object</code>（可选）</p><p>图像处理参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>style</strong><code>string</code>（可选）</p><p>输出图像的风格。目前支持以下风格取值：</p><ul><li>&lt;auto&gt;： 默认。</li><li>&lt;3d cartoon&gt;：3D卡通。</li><li>&lt;anime&gt;：动画。</li><li>&lt;oil painting&gt;： 油画。</li><li>&lt;watercolor&gt;：水彩。</li><li>&lt;sketch&gt;：素描。</li><li>&lt;chinese painting&gt;：中国画。</li><li>&lt;flat illustration&gt;：扁平插画。</li></ul><p><strong>size</strong><code>string</code>（可选）</p><p>输出图像的分辨率。目前支持3种图像分辨率：</p><ul><li>1024*1024：默认值。</li><li>720*1280</li><li>1280*720</li></ul><p><strong>n</strong><code>integer</code>（可选）</p><p>生成图片的数量。取值范围为1~4张，默认为1。</p><p><strong>mask_color</strong><code>array</code>（可选）</p><p>RGB颜色数值列表，用于指定掩码图片中表示涂改区域的颜色。默认值为[]。</p><p>当该字段为空，默认对掩码图片进行二值化处理（处理后白色代表涂抹区域）。当该字段非空时，表示RGB颜色数值列表，代表一种或多种颜色。这些RGB颜色所描绘的区域即为涂改区域，如[0,0,0]和[134,134,134]，而未被指定的颜色则视为背景色。</p><p>示例值：[[0, 0, 0], [134, 134, 134]]。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="图像局部重绘"></a><section><a id="图像局部重绘-h4"></a><h4>图像局部重绘</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
  &quot;model&quot;: &quot;wanx-x-painting&quot;,
  &quot;input&quot;: {
    &quot;prompt&quot;: &quot;一只狗戴着红色眼镜&quot;,
    &quot;base_image_url&quot;: &quot;http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg&quot;,
    &quot;mask_image_url&quot;: &quot;http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png&quot;
  },
  &quot;parameters&quot;: {
    &quot;size&quot;: &quot;1024*1024&quot;,
    &quot;n&quot;: 1
  }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="a69639162eu4i"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-2"></a><pre class="language-json"><code>{
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

<a id="25d6501e22xb4"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<table><tbody><tr><td><a id="c7a5b38b94icr"></a><h4>请求参数</h4><a id="6cbbceaeb6jyo"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><blockquote><p>若使用新加坡地域的模型，需将base_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="3f1ae57ce6qd5"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>task_metrics</strong> <code>object</code></p><p>任务结果统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section><p><strong>results</strong> <code>array of object</code></p><p>任务结果列表，包括图像URL、部分任务执行失败报错信息等。</p><a id="accordion-数据结构"></a><section><p>数据结构</p><div><a id="code-block-5"></a><pre class="language-json"><code>{
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

<a id="34914775efbhb"></a>

## DashScope SDK调用

请先确认已安装最新版DashScope SDK：[安装SDK](../../preparations/install-sdk.md)。

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

<a id="code-block-9"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

prompt = "一只狗戴着红色眼镜"
model = "wanx-x-painting"
extra_input = {
    "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
    "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
}

print('----sync call, please wait a moment----')
try:
    job = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size='1024*1024',
        extra_input=extra_input)
    print(job)
    # save file to current directory
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

<a id="code-block-10"></a>

```json
{
	"request_id": "4126d9dd-e037-9f32-8d56-6d29ab3f9a06",
	"task_id": "b476bc4e-35c1-4c4e-a4d9-xxxxxxx",
	"status": "SUCCEEDED",
	"results": [{
		"url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxxx.png"
	}],
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

<a id="b994ca9918t7e"></a>

##### 请求示例

<a id="code-block-11"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

prompt = "一只狗戴着红色眼镜"
model = "wanx-x-painting"
extra_input = {
    "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
    "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
}

def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task done then save image----')
    wait_async_task(task_info)

# 创建异步任务
def create_async_task():
    job = client.images.jobs.create(
        model=model,
        prompt=prompt,
        n=1,
        size='1024*1024',
        extra_input=extra_input)
    print(job)
    print(job.task_id, job.status)
    return job

# 等待异步任务结束
def wait_async_task(job):
    done = client.images.jobs.wait(job)
    print(done)
    print(done.status)
    # save file to current directory
    for url in done.image_urls:
        file_name = PurePosixPath(unquote(urlparse(url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(url).content)

if __name__ == '__main__':
    try:
        async_call()
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="ae28dc8f72g6i"></a>

##### 响应示例

**1、创建任务的响应示例**

<a id="code-block-12"></a>

```json
{
	"request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
	"task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
	"status": "PENDING"
}
```

**2、查询任务结果的响应示例**

<a id="code-block-13"></a>

```json
{
	"request_id": "d861d3ba-4b29-9491-abad-266ef4fb2f08",
	"task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
	"status": "SUCCEEDED",
	"results": [{
		"url": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxxx.png"
	}],
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

<a id="3e3609efb9rhl"></a>

##### 请求示例

<a id="code-block-14"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public void syncCall() {
        String task = "image2image";
        ImageSynthesis imageSynthesis = new ImageSynthesis(task);
        ImageSynthesisParam param = genImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageSynthesis.call(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    private ImageSynthesisParam genImageSynthesis(){
        HashMap<String,Object> extraInputMap = new HashMap<>();
        extraInputMap.put("base_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg");
        extraInputMap.put("mask_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png");
        String prompt = "一只狗戴着红色眼镜";
        String model = "wanx-x-painting";
        return ImageSynthesisParam.builder()
                .model(model)
                .prompt(prompt)
                .n(1)
                .size("1024*1024")
                .extraInputs(extraInputMap)
                .build();
    }

    public static void main(String[] args){
        Main text2Image = new Main();
        text2Image.syncCall();
    }

}
```

<a id="dfe6c9cc786iy"></a>

##### 响应示例

<a id="code-block-15"></a>

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

<a id="code-block-16"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import com.alibaba.dashscope.utils.Constants;

public class Main {
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
        String task = "image2image";
        ImageSynthesis imageSynthesis = new ImageSynthesis(task);
        ImageSynthesisParam param = genImageSynthesis();
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

    private ImageSynthesisParam genImageSynthesis(){
        String prompt = "一只狗戴着红色眼镜";
        String model = "wanx-x-painting";
        HashMap<String,Object> extraInputMap = new HashMap<>();
        extraInputMap.put("base_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg");
        extraInputMap.put("mask_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png");

        return ImageSynthesisParam.builder()
                .model(model)
                .prompt(prompt)
                .n(1)
                .size("1024*1024")
                .extraInputs(extraInputMap)
                .build();
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
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result.getOutput()));
        System.out.println(JsonUtils.toJson(result.getUsage()));
    }

    public static void main(String[] args){
        Main text2Image = new Main();
        text2Image.asyncCall();
    }

}
```

<a id="38e1e3c7303rm"></a>

##### 响应示例

**1、创建任务的响应示例**

<a id="code-block-17"></a>

```json
{
	"request_id": "5dbf9dc5-4f4c-9605-85ea-542f97709ba8",
	"output": {
		"task_id": "7277e20e-aa01-4709-xxxxxxxx",
		"task_status": "PENDING"
	}
}
```

**2、查询任务结果的响应示例****output字段内容：**

<a id="code-block-18"></a>

```json
{
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
}
```

**usage字段内容：**

<a id="code-block-19"></a>

```json
{
	"image_count": 1
}
```

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="45b31d4f7bk24"></a>

## 常见问题

<a id="模型计费及限流说明"></a>

<a id="b8457b7223zhp"></a>

### 模型计费及限流说明

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

<a id="图像局部重绘api通用问题"></a>

<a id="6af451b0a1ykp"></a>

### 图像局部重绘API通用问题

1.  **输入图像的掩码图像（mask\_image）有什么限制？**
    -   只能使用图像URL地址，暂不支持填写图像Base64数据。
    -   需要和输入图像的分辨率保持一致。
    -   文档中的示例掩码图像为白色背景，实际上，掩码图像并不要求必须为白色背景，可以通过`mask_color`字段指定其他颜色。
2.  **如何获得输入图像的掩码图像？**
    
    您可以使用PS或者其他图像编辑工具在原图上涂抹获得掩码图像。
    
3.  **使用图像局部重绘功能时，若涂抹区域外的图片输出效果不理想，应如何处理？**
    
    建议您使用[通用图像编辑](wanx-image-edit-api-reference.md)的局部重绘功能重新生成。
