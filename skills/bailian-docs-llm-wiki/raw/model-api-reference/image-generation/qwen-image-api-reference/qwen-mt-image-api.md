# 千问-图像翻译API参考

千问-图像翻译模型（Qwen-MT-Image）可精准翻译图像中的文字，并保留原始排版。该模型还支持领域提示、敏感词过滤、术语干预等自定义功能。

<a id="模型概览"></a>

<a id="5849834e92mb7"></a>

## 模型概览

|  |  |  |
| --- | --- | --- |
| ![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1007156.webp)<br><br>源语种：中文 | ![2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006389.webp)<br><br>英文 | ![3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006396.webp)<br><br>日文 |
| ![4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006438.webp)<br><br>韩语 | ![es](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006451.webp)<br><br>西班牙语 | ![fr](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6962921671/p1006452.webp)<br><br>法语 |

| 模型名称 | 模型简介 | 可用地域 | 输出图像规格 |
| --- | --- | --- | --- |
| qwen-mt-image-2.0 | 专注做图片翻译的模型服务，能将中、英、日等55个语言的图片翻译到指定的语言，精准还原图片排版和内容信息。<br><br>支持术语定义、敏感词过滤、商品主体检测等自定义功能，提供灵活、准确、高效的图像本地化服务。 | 华北2（北京）<br><br>新加坡 | 图片格式：JPG。 |
| qwen-mt-image | 千问-图像翻译模型<br><br>支持中/英文与其他语种之间的互译，但不支持在非中/英语种之间直接翻译（例如，从日语翻译为韩语）。详情请参见[支持的语种](qwen-mt-image-api.md#d2aa4b03d2kco)。 | 华北2（北京） | 图片格式：JPG。 |

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **重要**
>
> **在线体验**：在编写代码前，可先通过控制台 [Playground](https://bailian.console.aliyun.com/mt_image_playground) 在线体验图像翻译。

<a id="同步调用"></a>

<a id="f6g7h8i9j0syn"></a>

## 同步调用

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`，调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

同步模式下，请求会等待处理完成后直接返回翻译后的图像URL，无需轮询任务状态。

<table><tbody><tr><td><h4>请求参数</h4><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，设置为<code>qwen-mt-image-2.0</code>或<code>qwen-mt-image</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>图像的公网可访问的URL，支持 HTTP 和 HTTPS 协议。如需获取本地文件的公网URL，请参见<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a> 。</p><ul><li><strong>格式限制</strong>：JPG、JPEG、PNG、BMP、PNM、PPM、TIFF、WEBP</li><li><strong>尺寸限制</strong>：图像的宽度和高度均需在15-8192像素范围内，宽高比在1:10至10:1范围内。</li><li><strong>大小限制</strong>：不超过100MB</li><li>URL地址中不能包含中文字符。</li><li><strong>示例</strong>：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp</code></li></ul><p><strong>source_lang</strong> <code>string</code> <strong>（必选）</strong></p><p><a href="qwen-mt-image-api.md#d2aa4b03d2kco">源语种</a>。</p><ul><li><strong>支持值</strong>：语种全称、语种编码或<code>auto</code>（自动检测），对大小写不敏感</li><li><strong>限制</strong>：与<code>target_lang</code>不同。<code>qwen-mt-image-2.0</code>无语种限制；<code>qwen-mt-image</code>要求源语种或目标语种至少有一项为中文或英文。</li><li><strong>示例</strong>：<code>Chinese</code>、<code>en</code>、<code>auto</code></li></ul><p><strong>target_lang</strong> <code>string</code> <strong>（必选）</strong></p><p><a href="qwen-mt-image-api.md#d2aa4b03d2kco">目标语种</a>。</p><ul><li><strong>支持值</strong>：语种全称或语种编码，对大小写不敏感</li><li><strong>限制</strong>：与<code>source_lang</code>不同。<code>qwen-mt-image-2.0</code>无语种限制；<code>qwen-mt-image</code>要求源语种或目标语种至少有一项为中文或英文。</li><li><strong>示例</strong>：<code>Chinese</code>、<code>en</code></li></ul><p><strong>ext</strong> <code>object</code> （可选）</p><p>可选拓展字段。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>domainHint</strong> <code>string</code> （可选）</p><p>领域提示，为使译文风格更贴合特定领域，可以使用英文描述使用场景、译文风格等需求。</p><p>为确保翻译效果，建议不超过200个英文单词。</p><div><div><p><strong>重要</strong>领域提示语句当前<strong>只支持英文</strong>。</p></div></div><p><strong>示例：</strong>These sentences are from seller-buyer conversations on a B2C ecommerce platform. Translate them into clear, engaging customer service language, ensuring the translation is appropriate for handling potential issues or disputes.</p><p><strong>sensitives</strong> <code>array</code> （可选）</p><p>配置敏感词，以在翻译前过滤图片中<strong>完全匹配</strong>的文本，<strong>对大小写敏感</strong>。</p><p>敏感词的语种可与源语种不一致，支持全部的<a href="qwen-mt-image-api.md">源语种</a>和<a href="qwen-mt-image-api.md#d2aa4b03d2kco">目标语种</a>。为确保翻译效果，建议单次请求添加的敏感词不超过50个。</p><p><strong>示例：</strong>[&quot;全场9折&quot;, &quot;七天无理由退换&quot;]</p><p><strong>terminologies</strong> <code>array</code> （可选）</p><p>术语干预，为特定术语设定译文，以满足特定领域的翻译需求，术语对的语种需要与<code>source_lang</code>和<code>target_lang</code>对应。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>src</strong> <code>string</code> <strong>（必选）</strong></p><p>术语的源文本，语种需要与源语种<code>source_lang</code>一致。</p><p><strong>tgt</strong><code>string</code> <strong>（必选）</strong></p><p>术语的目标文本，语种需要与目标语种<code>target_lang</code>一致。</p></div></section><p><strong>示例</strong>：[{&quot;src&quot;: &quot;应用程序接口&quot;, &quot;tgt&quot;: &quot;API&quot;}, {&quot;src&quot;: &quot;机器学习&quot;, &quot;tgt&quot;: &quot;ML&quot;}]</p><p><strong>config</strong> <code>object</code> （可选）</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>imageSegment</strong><code>bool</code> （可选）</p><p>是否开启图像主体分割。开启后，将跳过对图像中主体（如人物、商品、Logo）上文字的翻译。</p><ul><li><code>false</code>：（默认值）翻译图像中的所有文字。</li><li><code>true</code>：不翻译图像主体的文字。</li></ul><blockquote><p><strong>注意</strong>：旧版本参数名为<code>skipImgSegment</code>（是否跳过图像主体分割）。为保持兼容，该参数仍受支持，但建议使用新的 <code>imageSegment</code>参数。</p></blockquote></div></section></div></section></div></section></td><td><a id="sec-tabs"></a><section><a id="curl"></a><section><a id="curl-h4"></a><h4>curl</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen-mt-image-2.0&quot;,
    &quot;input&quot;: {
        &quot;image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp&quot;,
        &quot;source_lang&quot;: &quot;zh&quot;,
        &quot;target_lang&quot;: &quot;en&quot;
    }
}'
</code></pre></section><a id="python"></a><section><a id="python-h4"></a><h4>Python</h4><a id="code-block-2"></a><pre class="language-python"><code>import requests
import os

# 请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同
url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis&quot;

headers = {
  &quot;Authorization&quot;: f&quot;Bearer {os.getenv('DASHSCOPE_API_KEY')}&quot;,
  &quot;Content-Type&quot;: &quot;application/json&quot;
}

# 同步调用：不设置 X-DashScope-Async 请求头
payload = {
  &quot;model&quot;: &quot;qwen-mt-image-2.0&quot;,
  &quot;input&quot;: {
    &quot;image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp&quot;,
    &quot;source_lang&quot;: &quot;zh&quot;,
    &quot;target_lang&quot;: &quot;en&quot;
  }
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(result)
# 同步模式直接返回 image_url
image_url = result[&quot;output&quot;][&quot;image_url&quot;]
print(f&quot;翻译完成，图像URL: {image_url}&quot;)
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>image_url</strong> <code>string</code></p><p>模型生成图像的URL地址，与原图长宽相同，JPG格式。有效期为24小时，请及时下载并保存图像。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型生成图像的数量，固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;image_url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.jpg?Expires=xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    },
    &quot;request_id&quot;: &quot;b60d747a-adee-940a-aa3e-ac55b957189a&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="异步调用"></a>

<a id="42703589880ts"></a>

## 异步调用

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`，调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

异步调用流程分两步：

1.  **创建任务获取任务ID**：发送一个请求创建任务，该请求会返回**任务ID（task\_id）**。
2.  **根据任务ID查询结果**：使用task\_id轮询任务状态，直到任务完成并获得图像URL。

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将使用同步模式（仅<code>qwen-mt-image-2.0</code>支持同步）。<code>qwen-mt-image</code>模型必须设置此请求头。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称，设置为<code>qwen-mt-image-2.0</code>或<code>qwen-mt-image</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>图像的公网可访问的URL，支持 HTTP 和 HTTPS 协议。如需获取本地文件的公网URL，请参见<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a> 。</p><ul><li><strong>格式限制</strong>：JPG、JPEG、PNG、BMP、PNM、PPM、TIFF、WEBP</li><li><strong>尺寸限制</strong>：图像的宽度和高度均需在15-8192像素范围内，宽高比在1:10至10:1范围内。</li><li><strong>大小限制</strong>：不超过100MB</li><li>URL地址中不能包含中文字符。</li><li><strong>示例</strong>：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp</code></li></ul><p><strong>source_lang</strong> <code>string</code> <strong>（必选）</strong></p><p><a href="qwen-mt-image-api.md#d2aa4b03d2kco">源语种</a>。</p><ul><li><strong>支持值</strong>：语种全称、语种编码或<code>auto</code>（自动检测），对大小写不敏感</li><li><strong>限制</strong>：与<code>target_lang</code>不同。<code>qwen-mt-image-2.0</code>无语种限制；<code>qwen-mt-image</code>要求源语种或目标语种至少有一项为中文或英文。</li><li><strong>示例</strong>：<code>Chinese</code>、<code>en</code>、<code>auto</code></li></ul><p><strong>target_lang</strong> <code>string</code> <strong>（必选）</strong></p><p><a href="qwen-mt-image-api.md#d2aa4b03d2kco">目标语种</a>。</p><ul><li><strong>支持值</strong>：语种全称或语种编码，对大小写不敏感</li><li><strong>限制</strong>：与<code>source_lang</code>不同。<code>qwen-mt-image-2.0</code>无语种限制；<code>qwen-mt-image</code>要求源语种或目标语种至少有一项为中文或英文。</li><li><strong>示例</strong>：<code>Chinese</code>、<code>en</code></li></ul><p><strong>ext</strong> <code>object</code> （可选）</p><p>可选拓展字段。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>domainHint</strong> <code>string</code> （可选）</p><p>领域提示，为使译文风格更贴合特定领域，可以使用英文描述使用场景、译文风格等需求。</p><p>为确保翻译效果，建议不超过200个英文单词。</p><div><div><p><strong>重要</strong>领域提示语句当前<strong>只支持英文</strong>。</p></div></div><p><strong>示例：</strong>These sentences are from seller-buyer conversations on a B2C ecommerce platform. Translate them into clear, engaging customer service language, ensuring the translation is appropriate for handling potential issues or disputes.</p><p><strong>sensitives</strong> <code>array</code> （可选）</p><p>配置敏感词，以在翻译前过滤图片中<strong>完全匹配</strong>的文本，<strong>对大小写敏感</strong>。</p><p>敏感词的语种可与源语种不一致，支持全部的<a href="qwen-mt-image-api.md">源语种</a>和<a href="qwen-mt-image-api.md#d2aa4b03d2kco">目标语种</a>。为确保翻译效果，建议单次请求添加的敏感词不超过50个。</p><p><strong>示例：</strong>[&quot;全场9折&quot;, &quot;七天无理由退换&quot;]</p><p><strong>terminologies</strong> <code>array</code> （可选）</p><p>术语干预，为特定术语设定译文，以满足特定领域的翻译需求，术语对的语种需要与<code>source_lang</code>和<code>target_lang</code>对应。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>src</strong> <code>string</code> <strong>（必选）</strong></p><p>术语的源文本，语种需要与源语种<code>source_lang</code>一致。</p><p><strong>tgt</strong><code>string</code> <strong>（必选）</strong></p><p>术语的目标文本，语种需要与目标语种<code>target_lang</code>一致。</p></div></section><p><strong>示例</strong>：[{&quot;src&quot;: &quot;应用程序接口&quot;, &quot;tgt&quot;: &quot;API&quot;}, {&quot;src&quot;: &quot;机器学习&quot;, &quot;tgt&quot;: &quot;ML&quot;}]</p><p><strong>config</strong> <code>object</code> （可选）</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>imageSegment</strong><code>bool</code> （可选）</p><p>是否开启图像主体分割。开启后，将跳过对图像中主体（如人物、商品、Logo）上文字的翻译。</p><ul><li><code>false</code>：（默认值）翻译图像中的所有文字。</li><li><code>true</code>：不翻译图像主体的文字。</li></ul><blockquote><p><strong>注意</strong>：旧版本参数名为<code>skipImgSegment</code>（是否跳过图像主体分割）。为保持兼容，该参数仍受支持，但建议使用新的 <code>imageSegment</code>参数。</p></blockquote></div></section></div></section></div></section></td><td><a id="sec-tabs-3"></a><section><a id="curl-2"></a><section><a id="curl-2-h4"></a><h4>curl</h4><a id="code-block-5"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;qwen-mt-image-2.0&quot;,
    &quot;input&quot;: {
        &quot;image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp&quot;,
        &quot;source_lang&quot;: &quot;zh&quot;,
        &quot;target_lang&quot;: &quot;en&quot;,
        &quot;ext&quot;: {
            &quot;config&quot;: {
                &quot;imageSegment&quot;: false
            }
        }
    }
}'
</code></pre></section><a id="python-2"></a><section><a id="python-2-h4"></a><h4>Python</h4><a id="code-block-6"></a><pre class="language-python"><code>import requests
import os

# 请将 {WorkspaceId} 替换为您的百炼业务空间ID
url = &quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis&quot;

headers = {
  &quot;X-DashScope-Async&quot;: &quot;enable&quot;,
  &quot;Authorization&quot;: f&quot;Bearer {os.getenv('DASHSCOPE_API_KEY')}&quot;,
  &quot;Content-Type&quot;: &quot;application/json&quot;
}

payload = {
  &quot;model&quot;: &quot;qwen-mt-image-2.0&quot;,
  &quot;input&quot;: {
    &quot;image_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250916/ordhsk/1.webp&quot;,
    &quot;source_lang&quot;: &quot;zh&quot;,
    &quot;target_lang&quot;: &quot;en&quot;,
    &quot;ext&quot;: {
      &quot;config&quot;: {
        &quot;imageSegment&quot;: False
      }
    }
  }
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
print(result)
# 保存 task_id，用于步骤2查询结果
task_id = result[&quot;output&quot;][&quot;task_id&quot;]
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-4"></a><section><a id="成功响应-2"></a><section><a id="成功响应-2-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应-2"></a><section><a id="异常响应-2-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   `task_id` 有效期为**24小时**，若ID不存在或已过期，任务状态将返回 `UNKNOWN`。
> -   任务成功后返回的 `url`有效期为**24小时**，请及时下载并保存图像。
> -   此查询接口的默认RPS为1。如需更高频次的查询或事件通知，请[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   如需批量查询或取消任务，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>您需要将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><a id="code-block-9"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>image_url</strong> <code>string</code></p><p>模型生成图像的URL地址，与原图长宽相同，JPG格式。有效期为24小时，请及时下载并保存图像。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p>通常请求成功时不会返回此参数，仅在图像中无可翻译文本（例如，在分割图像主体后，其余部分无文字）时，<strong>任务仍会成功并正常计费</strong>，但会返回<code>No text detected for translation</code>的提示。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型生成图像的数量，固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功-存在可翻译内容"></a><section><a id="任务执行成功-存在可翻译内容-h4"></a><h4>任务执行成功-存在可翻译内容</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;5fec62eb-bf94-91f8-b9f4-f7f758e4e27e&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;72c52225-8444-4cab-ad0c-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-08-13 18:11:16.954&quot;,
        &quot;scheduled_time&quot;: &quot;2025-08-13 18:11:17.003&quot;,
        &quot;end_time&quot;: &quot;2025-08-13 18:11:23.860&quot;,
        &quot;image_url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx?Expires=xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;:1
    }
}
</code></pre></section><a id="任务执行成功-无可翻译内容"></a><section><a id="任务执行成功-无可翻译内容-h4"></a><h4>任务执行成功-无可翻译内容</h4><p>在图像中无可翻译文本（例如，在识别出图像主体后，其余部分无文字）时，<strong>任务仍会成功并正常计费</strong>，但会返回<code>No text detected for translation</code>的提示。</p><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;0ccb84aa-e034-431d-9d54-08e14fxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;34ec4208-97d6-498b-a390-9173f7xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-01-12 17:56:23.625&quot;,
        &quot;scheduled_time&quot;: &quot;2026-01-12 17:56:23.656&quot;,
        &quot;end_time&quot;: &quot;2026-01-12 17:56:25.324&quot;,
        &quot;image_url&quot;: &quot;http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.jpg?Expires=xxx&quot;,
        &quot;message&quot;: &quot;No text detected for translation&quot;
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;daad9007-6acd-9fb3-a6bc-d55902b9c9ff&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;fe8aa114-d9f1-4f76-b598-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;: &quot;2025-08-20 09:54:21.911&quot;,
        &quot;scheduled_time&quot;: &quot;2025-08-20 09:54:21.984&quot;,
        &quot;end_time&quot;: &quot;2025-08-20 12:55:00.818&quot;,
        &quot;code&quot;: &quot;InternalError&quot;,
        &quot;message&quot;: &quot;xxxxxx&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="支持的语种"></a>

<a id="d2aa4b03d2kco"></a>

## 支持的语种

若不确定源语种，可将 `source_lang` 设置为 `auto` 进行自动检测。

<a id="qwen-mt-image-2-0-支持的语种"></a>

### qwen-mt-image-2.0 支持的语种

`qwen-mt-image-2.0`支持以下55种语言的任意组合互译，无需源语种或目标语种为中文或英文。所有语种均可作为源语种和目标语种。

| 语种（中文名） | 英文全称 | 编码 |
| --- | --- | --- |
| 简体中文 | Simplified Chinese | zh |
| 繁体中文 | Traditional Chinese | zh-tw |
| 英语 | English | en |
| 日语 | Japanese | ja |
| 韩语 | Korean | ko |
| 德语 | German | de |
| 西班牙语 | Spanish | es |
| 俄语 | Russian | ru |
| 法语 | French | fr |
| 葡萄牙语 | Portuguese | pt |
| 意大利语 | Italian | it |
| 越南语 | Vietnamese | vi |
| 印度尼西亚语 | Indonesian | id |
| 马来语 | Malay | ms |
| 泰语 | Thai | th |
| 阿拉伯语 | Arabic | ar |
| 荷兰语 | Dutch | nl |
| 波兰语 | Polish | pl |
| 土耳其语 | Turkish | tr |
| 乌克兰语 | Ukrainian | uk |
| 希腊语 | Greek | el |
| 匈牙利语 | Hungarian | hu |
| 罗马尼亚语 | Romanian | ro |
| 捷克语 | Czech | cs |
| 瑞典语 | Swedish | sv |
| 丹麦语 | Danish | da |
| 芬兰语 | Finnish | fi |
| 挪威语 | Norwegian | no |
| 印地语 | Hindi | hi |
| 泰米尔语 | Tamil | ta |
| 泰卢固语 | Telugu | te |
| 尼泊尔语 | Nepali | ne |
| 波斯语 | Persian | fa |
| 阿塞拜疆语 | Azerbaijani | az |
| 哈萨克语 | Kazakh | kk |
| 乌兹别克语 | Uzbek | uz |
| 蒙古语 | Mongolian | mn |
| 维吾尔语 | Uyghur | ug |
| 白俄罗斯语 | Belarusian | be |
| 保加利亚语 | Bulgarian | bg |
| 塞尔维亚语 | Serbian | sr |
| 克罗地亚语 | Croatian | hr |
| 波斯尼亚语 | Bosnian | bs |
| 斯洛文尼亚语 | Slovenian | sl |
| 斯洛伐克语 | Slovak | sk |
| 马其顿语 | Macedonian | mk |
| 拉脱维亚语 | Latvian | lv |
| 立陶宛语 | Lithuanian | lt |
| 爱尔兰语 | Irish | ga |
| 卢森堡语 | Luxembourgish | lb |
| 南非荷兰语 | Afrikaans | af |
| 拉丁语 | Latin | la |
| 车臣语 | Chechen | ce |
| 印古什语 | Ingush | inh |
| 马里语 | Mari | chm |

<a id="qwen-mt-image-支持的语种"></a>

### qwen-mt-image 支持的语种

`qwen-mt-image`要求**源语种或目标语种必须至少有一种是中文或英文**，不支持在两个非中、英语种之间直接翻译（例如，从日语翻译为韩语）。

| 语种（中文名） | 英文全称 | 编码 | 支持作为源语种 | 支持作为目标语种 |
| --- | --- | --- | --- | --- |
| 简体中文 | Chinese | zh | 支持 | 支持 |
| 英文 | English | en | 支持 | 支持 |
| 韩语 | Korean | ko | 支持 | 支持 |
| 日语 | Japanese | ja | 支持 | 支持 |
| 俄语 | Russian | ru | 支持 | 支持 |
| 西班牙语 | Spanish | es | 支持 | 支持 |
| 法语 | French | fr | 支持 | 支持 |
| 葡萄牙语 | Portuguese | pt | 支持 | 支持 |
| 意大利语 | Italian | it | 支持 | 支持 |
| 德语 | German | de | 支持 | 不支持 |
| 越南语 | Vietnamese | vi | 支持 | 支持 |
| 马来语 | Malay | ms | 不支持 | 支持 |
| 泰语 | Thai | th | 不支持 | 支持 |
| 印尼语 | Indonesian | id | 不支持 | 支持 |
| 阿拉伯语 | Arabian | ar | 不支持 | 支持 |

<a id="计费与限流"></a>

<a id="5dafefe82bgrh"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](../../../model-user-guide/test-1/model-pricing.md#a3250eda6bgjx)。
-   模型限流请参见[限流](../../../model-user-guide/get-started-with-models/rate-limit.md#f812e7c63axvx)。
-   计费说明：按成功生成的**图像张数**计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](../../../model-user-guide/test-1/new-free-quota.md)。
-   **注意**：如果图像中无可翻译文本，或在启用主体识别功能后，非主体部分无文字时，**任务仍记为成功**并**正常计费**，此时接口会返回`No text detected for translation`的提示。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="c928ee689aw6l"></a>

## 常见问题

<a id="q-为什么图中的内容没有被翻译"></a>

<a id="fde7e2e421sy9h4"></a>

#### Q：为什么图中的内容没有被翻译？

A：因为启用了[主体分割](qwen-mt-image-api.md)功能，模型不会翻译图片中人物、商品、Logo等主体上的文字。若需翻译所有文字，请将`ext.config.imgSegment`参数设置为`false`。

<a id="q-如何将临时的图像链接转为永久链接"></a>

<a id="c8e2ec8554vqhh4"></a>

#### Q：如何将临时的图像链接转为永久链接？

A：临时链接无法直接转为永久链接。需通过后端服务下载图像，再上传至对象存储服务（如阿里云 OSS）以生成新的永久链接。

<a id="accordion-示例代码-下载图像到本地"></a>

示例代码：下载图像到本地

<a id="code-block-13"></a>

```python
import requests

def download_and_save_image(image_url, save_path):
  try:
    response = requests.get(image_url, stream=True, timeout=300)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
      for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
    print(f"图像已成功下载到: {save_path}")
  except requests.exceptions.RequestException as e:
    print(f"图像下载失败: {e}")

if __name__ == '__main__':
  image_url = "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx?Expires=xxx"
  save_path = "image-translation.jpg"
  download_and_save_image(image_url, save_path)
```

<a id="q-如何查看模型调用量"></a>

<a id="ae11776b04p4u"></a>

### Q: 如何查看模型调用量？

A: 模型调用完一小时后，请在[**模型监控**（北京）](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[**模型监控**（新加坡）](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry) 页面，查看模型的调用次数、成功率等指标。详情请参见[账单查询与成本管理](../../../model-user-guide/test-1/bill-query-and-cost-management.md)。

<a id="q-如何获取图像存储的访问域名白名单"></a>

<a id="5fb153423ct8z"></a>

### Q：如何获取图像存储的访问域名白名单？

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会根据业务情况进行动态变更，为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。

<a id="q-翻译后的文字没有覆盖原内容-出现格式错位怎么办"></a>

#### Q：翻译后的文字没有覆盖原内容，出现格式错位怎么办？

A：复杂排版（如多列文本、混合字体大小）的图片在翻译后容易出现文字错位，属于已知的模型限制。建议将复杂排版的图片分割为简单区域后分别翻译，即可规避此问题。
