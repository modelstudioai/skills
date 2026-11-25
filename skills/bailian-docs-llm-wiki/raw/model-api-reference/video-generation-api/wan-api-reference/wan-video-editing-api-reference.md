# 万相2.7-视频编辑API参考

万相2.7-视频编辑模型，支持输入多模态（文本/图像/视频），可完成 指令编辑和视频迁移 任务。

**相关文档**：指南文档

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

<a id="09a068c6b1q5b"></a>

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](../../../model-user-guide/model-experience/image-and-video-generation/video-generate-edit-model.md)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：获取该地域的API Key，再配置API Key到环境变量。

> **说明**
>
> 本文的示例代码适用于**北京地域**。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="http调用"></a>

<a id="a5a4ad982dpoz"></a>

<a id="e9e21dd3a6945"></a>

## HTTP调用

视频编辑任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="9b685d1a9b6wv"></a>

<a id="9c71bffa84zm6"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的业务空间ID。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见Postman。

<table><tbody><tr><td><a id="f3da63afcam8r"></a><h4>请求参数</h4><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="ee4e0b58694zl"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>示例值：wan2.7-videoedit。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （可选）</p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，超过部分会自动截断。</p><ul><li>wan2.7-videoedit：长度不超过5000个字符。</li></ul><p>示例值：为人物换上酷闪的衣服，再戴参考图里的帽子。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在视频画面中出现的内容，可以对视频画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体素材列表，用于指定视频生成所需的参考素材（图像、视频）。</p><p>数组的每个元素为一个媒体对象，包含 <code>type</code> 与 <code>url</code> 字段。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。可选值为：</p><ul><li><code>video</code>：必传。待编辑的视频。</li><li><code>reference_image</code>：可选。参考图像。</li></ul><p>素材限制：</p><ul><li>视频有且仅有1个。</li><li>参考图像最多传入4张。</li></ul><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材URL、Base64 编码数据或资产中心 asset_id。素材包括视频和图像。</p><a id="accordion-传入视频-type-video"></a><section><p>传入视频（type=video）</p><div><p>待编辑的视频文件的 URL 或资产中心 asset_id。</p><p>视频限制：</p><ul><li>格式：mp4、mov。</li><li>时长：2～10s。</li><li>分辨率：宽度和高度范围为[240,4096]像素。</li><li>宽高比：1:8～8:1。</li><li>文件大小：不超过100MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL：</p><ul><li>支持 HTTP 和 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过上传文件获取临时 URL。</li><li>示例值：oss://dashscope-instant/xxx/xxx.mp4。</li></ul></li><li><p>资产中心 asset_id</p><ul><li>格式：<code>ark_asset_vid_xxxxxx</code>。</li><li>可通过<a href="../../../model-user-guide/asset-center-page/asset-center.md">资产中心</a>获取，与 URL 二选一。</li></ul></li></ol></div></section><a id="accordion-传入图像-type-reference-image"></a><section><p>传入图像（type=reference_image）</p><div><p>参考图像URL、Base64 编码数据或资产中心 asset_id。</p><p>图像限制：</p><ul><li>格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>分辨率：宽度和高度范围为[240, 8000]像素。</li><li>宽高比：1:8～8:1。</li><li>文件大小：不超过20MB。</li></ul><p>支持输入的格式：</p><ol><li><p>公网URL:</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.png"></a><a href="https://xxx/xxx.png">https://xxx/xxx.png</a>。</li></ul></li><li><p>临时URL：</p><ul><li>支持OSS协议，必须通过上传文件获取临时 URL。</li><li>示例值：oss://dashscope-instant/xxx/xxx.png。</li></ul></li><li><p>Base64 编码字符串：</p><ul><li>数据格式：<code>data:{MIME_type};base64,{base64_data}</code>。</li><li>示例值：data:image/png;base64,GDU7MtCZzEbTbmRZ......（示例已截断，仅做演示）。</li></ul><a id="accordion-base64编码数据格式"></a><section><p>Base64编码数据格式</p><div><p>格式： <code>data:{MIME_type};base64,{base64_data}</code> 。</p><ul><li>{base64_data}：图像文件经过 Base64 编码后的字符串。</li><li>{MIME_type}：图像的媒体类型，需与文件格式对应。</li></ul><table><tbody><tr><td><p>图像格式</p></td><td><p>MIME Type</p></td></tr><tr><td><p>JPEG</p></td><td><p>image/jpeg</p></td></tr><tr><td><p>JPG</p></td><td><p>image/jpeg</p></td></tr><tr><td><p>PNG</p></td><td><p>image/png</p></td></tr><tr><td><p>BMP</p></td><td><p>image/bmp</p></td></tr><tr><td><p>WEBP</p></td><td><p>image/webp</p></td></tr></tbody></table></div></section></li><li><p>资产中心 asset_id</p><ul><li>格式：<code>ark_asset_img_xxxxxx</code>。</li><li>可通过<a href="../../../model-user-guide/asset-center-page/asset-center.md">资产中心</a>获取，与 URL / Base64 三选一。</li></ul></li></ol></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置视频分辨率、设置视频时长、开启prompt智能改写、添加水印等。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><p>生成视频的分辨率档位，用于控制视频的清晰度（总像素）。</p><ul><li>wan2.7-videoedit：可选值：720P、1080P。默认值为<code>1080P</code>。</li></ul><p><strong>ratio</strong> <code>string</code> （可选）</p><p>生成视频的宽高比。</p><p>生效逻辑：</p><ul><li>不传 <code>ratio</code> 参数：以输入视频的宽高比生成近似比例的视频。</li><li>传入<code>ratio</code>参数：按指定的 <code>ratio</code> 生成视频。</li></ul><p>可选值为：</p><ul><li><code>16:9</code></li><li><code>9:16</code></li><li><code>1:1</code></li><li><code>4:3</code></li><li><code>3:4</code></li></ul><p>不同宽高比对应的输出视频分辨率（宽高像素值）见下方表格。</p><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p>输出视频分辨率（宽*高）</p></td></tr><tr><td rowspan="5"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td><p>1:1</p></td><td><p>960*960</p></td></tr><tr><td><p>4:3</p></td><td><p>1104*832</p></td></tr><tr><td><p>3:4</p></td><td><p>832*1104</p></td></tr><tr><td rowspan="5"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr><tr><td><p>1:1</p></td><td><p>1440*1440</p></td></tr><tr><td><p>4:3</p></td><td><p>1648*1248</p></td></tr><tr><td><p>3:4</p></td><td><p>1248*1648</p></td></tr></tbody></table><p><strong>duration</strong> <code>integer</code> （可选）</p><p>生成视频的时长，单位为秒。</p><p>使用建议：此参数仅在需要“截断视频”时才需配置。如果希望输出视频与输入视频时长一致，无需设置（或传入默认值 0）。</p><p>使用规则：</p><ul><li>默认行为：默认值为 0，代表直接使用输入视频的时长，不进行截断。</li><li>截断生效：当传入指定时长时，系统会从原视频的 0 秒起，截取至 duration 设置的长度。</li><li>取值范围：支持 [2, 10] 之间的整数。</li></ul><p><strong>audio_setting</strong> <code>string</code> （可选）</p><p>视频声音设置。</p><ul><li><code>auto</code> （默认）：模型根据 <code>prompt</code> 内容智能判断。若提示词涉及声音描述，可能重新生成音频；否则可能保留输入素材的原声。</li><li><code>origin</code>：强制保留输入视频的原声，不重新生成。</li></ul><p><strong>prompt_extend</strong><code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li><code>true</code>：默认值，开启智能改写。</li><li><code>false</code>：不开启智能改写。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p>示例值：false。</p><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-纯指令编辑-修改视频风格-tab"></a>纯指令编辑（修改视频风格）<div><a id="code-code-group-纯指令编辑-修改视频风格"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.7-videoedit&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;将整个画面转换为黏土风格&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div><a id="fig-code-group-指令-参考图编辑-局部替换-tab"></a>指令+参考图编辑（局部替换）<div><a id="code-code-group-指令-参考图编辑-局部替换"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.7-videoedit&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;将视频中女孩的衣服替换为图片中的衣服&quot;,
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4&quot;
            },
            {
                &quot;type&quot;: &quot;reference_image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: true
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="f61855da6bvbh"></a><a id="5c1654cd07xpd"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见错误码。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见错误码。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见错误码进行解决。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="be5d09eac3ayn"></a>

<a id="e3f32858d7hlv"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-3"></a>

<a id="北京-2"></a>

<a id="北京-2-h4"></a>

#### 北京

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的业务空间ID。

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议配置异步任务回调。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见管理异步任务。

<table><tbody><tr><td><a id="fd010a8092qiw"></a><a id="19df887abf8hc"></a><h4>请求参数</h4><a id="50cb3a1aa6yzu"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="f96cc5e8cf62s"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-4"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的业务空间ID。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="08a68c21dbgfk"></a><a id="1968190de5dwi"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见错误码。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见错误码。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>input_video_duration</strong> <code>float</code></p><p>输入视频的时长，单位秒。</p><p><strong>output_video_duration</strong> <code>float</code></p><p>输出视频的时长，单位秒。</p><p><strong>duration</strong> <code>float</code></p><p>总的视频时长，用于计费。</p><p>计费公式：<code>duration=input_video_duration+output_video_duration</code>。</p><p><strong>SR</strong> <code>integer</code></p><p>输出视频的分辨率档位。示例值：720。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-5"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;f16ae7e9-d518-92f8-a02c-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;05e68c7e-850c-49e4-b866-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-04-03 00:08:03.576&quot;,
        &quot;scheduled_time&quot;: &quot;2026-04-03 00:08:13.408&quot;,
        &quot;end_time&quot;: &quot;2026-04-03 00:11:57.286&quot;,
        &quot;orig_prompt&quot;: &quot;将视频中女孩的衣服替换为图片中的衣服&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?xxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 10.04,
        &quot;input_video_duration&quot;: 5.02,
        &quot;output_video_duration&quot;: 5.02,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 720
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见错误码进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-sdk调用"></a>

<a id="ve601a0h2sdk1"></a>

<a id="ve600a0sdksec"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](wan-video-editing-api-reference.md#e9e21dd3a6945)基本一致，参数结构根据语言特性进行封装。

由于视频编辑任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="ve607a0h3pyth"></a>

<a id="ve606a0sepyth"></a>

### Python SDK调用

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**`2.0.1`，再运行以下代码。
>
> 若版本过低，可能会触发 "url error, please check url!" 等错误。请参考安装SDK进行更新。

根据模型所在地域设置 `region`（构造 Client 时传入，各地域的region取值不同）:

<a id="sec-tabs-6"></a>

<a id="北京-3"></a>

<a id="北京-3-h4"></a>

#### 北京

`region="cn-beijing"`

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`region="ap-southeast-1"`

调用时请将`{WorkspaceId}`替换为真实的业务空间ID。

<a id="sec-tabs-7"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="ve643a0h5rq01"></a>

<a id="ve642a0secrq1"></a>

##### 请求示例

<a id="code-block-7"></a>

```python
import base64
import mimetypes
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# 参考图像URL，支持以下三种输入方式

# 【方式一】使用公网图片URL
reference_image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# reference_image_url = "file://" + "/path/to/image.png"     # Linux/macOS
# reference_image_url = "file://" + "C:/path/to/image.png"    # Windows
# 示例（相对路径）：
# reference_image_url = "file://" + "./image.png"             # 相对当前执行文件的路径

# 【方式三】使用Base64编码
# reference_image_url = encode_file("/path/to/image.png")

def sample_sync_call_videoedit():
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    print('please wait...')
    try:
        job = client.videos.generate(
            model='wan2.7-videoedit',
            prompt='将视频中女孩的衣服替换为图片中的衣服',
            media=[
                {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
                },
                {
                    "type": "reference_image",
                    "url": reference_image_url
                }
            ],
            resolution='720P',
            prompt_extend=True,
            watermark=True)
        print(job)
        print(job.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_videoedit()
```

<a id="ve646a0h5rs01"></a>

##### 响应示例

> `video_url` 有效期24小时，请及时下载视频。

<a id="code-block-8"></a>

```json
{
    "request_id": "d6c3c865-34e9-98a9-a53d-xxxxxx",
    "task_id": "1de7c853-755a-454a-91bc-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": 720
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="ve673a0h5rq03"></a>

<a id="ve672a0secrq3"></a>

##### 请求示例

<a id="code-block-9"></a>

```python
import base64
import mimetypes
import dashscope
import os
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# 参考图像URL，支持以下三种输入方式

# 【方式一】使用公网图片URL
reference_image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# reference_image_url = "file://" + "/path/to/image.png"     # Linux/macOS
# reference_image_url = "file://" + "C:/path/to/image.png"    # Windows
# 示例（相对路径）：
# reference_image_url = "file://" + "./image.png"             # 相对当前执行文件的路径

# 【方式三】使用Base64编码
# reference_image_url = encode_file("/path/to/image.png")

def sample_async_call_videoedit():
    # call async api, will return the task information
    # you can get task status with the returned task id.
    try:
        job = client.videos.jobs.create(
            model='wan2.7-videoedit',
            prompt='将视频中女孩的衣服替换为图片中的衣服',
            media=[
                {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
                },
                {
                    "type": "reference_image",
                    "url": reference_image_url
                }
            ],
            resolution='720P',
            prompt_extend=True,
            watermark=True)
        print(job)
        print("task_id: %s" % job.task_id)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return

    # get the task information include the task status.
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)  # check the task status
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # wait the task complete, will call fetch interval, and check it's in finished status.
    # （2.0 jobs.wait 指数退避轮询，默认总预算24小时，任务 FAILED 会抛出异常）
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_async_call_videoedit()
```

<a id="ve680a0h5rsp2"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-10"></a>

```json
{
    "request_id": "f16ae7e9-d518-92f8-a02c-xxxxxx",
    "task_id": "05e68c7e-850c-49e4-b866-xxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> `video_url` 有效期24小时，请及时下载视频。

<a id="code-block-11"></a>

```json
{
    "request_id": "d6c3c865-34e9-98a9-a53d-xxxxxx",
    "task_id": "1de7c853-755a-454a-91bc-xxxxxx",
    "status": "SUCCEEDED",
    "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxxx",
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": 720
    }
}
```

<a id="java-sdk调用"></a>

<a id="ve701a0h3java"></a>

<a id="ve700a0sejava"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.14`，再运行以下代码。
>
> 若版本过低，可能会触发 "url error, please check url!" 等错误。请参考安装SDK进行更新。

根据模型所在地域设置 `Constants.baseHttpApiUrl`:

<a id="sec-tabs-8"></a>

<a id="北京-4"></a>

<a id="北京-4-h4"></a>

#### 北京

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";`

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`Constants.baseHttpApiUrl = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1";`

调用时请将`{WorkspaceId}`替换为真实的业务空间ID。

<a id="sec-tabs-9"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="ve737a0h5jr01"></a>

<a id="ve736a0secjr1"></a>

##### 请求示例

<a id="code-block-12"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

public class VideoEdit {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 参考图像URL，支持以下三种输入方式

    // 【方式一】使用公网图片URL
    static String referenceImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png";

    // 【方式二】使用本地文件（支持绝对路径和相对路径）
    // 格式要求：file:// + 文件路径
    // 示例（绝对路径）：
    // static String referenceImageUrl = "file://" + "/path/to/image.png";     // Linux/macOS
    // static String referenceImageUrl = "file://" + "C:/path/to/image.png";   // Windows
    // 示例（相对路径）：
    // static String referenceImageUrl = "file://" + "./image.png";             // 相对当前执行文件的路径

    // 【方式三】使用Base64编码
    // static String referenceImageUrl = encodeFile("/path/to/image.png");

    // 格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        byte[] fileBytes = null;
        try {
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void videoEdit() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                    .type("video")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url(referenceImageUrl)
                    .type("reference_image")
                    .build());
        }};
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("resolution", "720P");
        parameters.put("prompt_extend", true);
        parameters.put("watermark", true);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt("将视频中女孩的衣服替换为图片中的衣服")
                        .media(media)
                        .parameters(parameters)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            videoEdit();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="ve740a0h5jr02"></a>

##### 响应示例

> `video_url` 有效期24小时，请及时下载视频。

<a id="code-block-13"></a>

```json
{
    "request_id": "0a15ad3c-cde7-9f7e-b8d2-xxxxxx",
    "output": {
        "task_id": "0025d1e1-009a-4f53-9c27-xxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服",
        "submit_time": "2026-04-10 17:21:01.719",
        "scheduled_time": "2026-04-10 17:21:13.182",
        "end_time": "2026-04-10 17:31:41.286"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

<a id="ve773a0h5jr04"></a>

<a id="ve772a0secjr3"></a>

##### 请求示例

<a id="code-block-14"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

public class VideoEdit {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 参考图像URL，支持以下三种输入方式

    // 【方式一】使用公网图片URL
    static String referenceImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png";

    // 【方式二】使用本地文件（支持绝对路径和相对路径）
    // 格式要求：file:// + 文件路径
    // 示例（绝对路径）：
    // static String referenceImageUrl = "file://" + "/path/to/image.png";     // Linux/macOS
    // static String referenceImageUrl = "file://" + "C:/path/to/image.png";   // Windows
    // 示例（相对路径）：
    // static String referenceImageUrl = "file://" + "./image.png";             // 相对当前执行文件的路径

    // 【方式三】使用Base64编码
    // static String referenceImageUrl = encodeFile("/path/to/image.png");

    // 格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        byte[] fileBytes = null;
        try {
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }
        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void videoEdit() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
            add(VideoSynthesisParam.Media.builder()
                    .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                    .type("video")
                    .build());
            add(VideoSynthesisParam.Media.builder()
                    .url(referenceImageUrl)
                    .type("reference_image")
                    .build());
        }};
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("resolution", "720P");
        parameters.put("prompt_extend", true);
        parameters.put("watermark", true);

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt("将视频中女孩的衣服替换为图片中的衣服")
                        .media(media)
                        .parameters(parameters)
                        .build();

        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        // 获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    // 获取任务列表
    public static void listTask() throws ApiException, NoApiKeyException {
        VideoSynthesis is = new VideoSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        VideoSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    // 获取单个任务结果
    public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        VideoSynthesis is = new VideoSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空
        VideoSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args) {
        try {
            videoEdit();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="ve780a0h5jrp2"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-15"></a>

```json
{
    "request_id": "f16ae7e9-d518-92f8-a02c-xxxxxx",
    "output": {
        "task_id": "05e68c7e-850c-49e4-b866-xxxxxx",
        "task_status": "PENDING",
        "video_url": ""
    },
    "usage": null,
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> `video_url` 有效期24小时，请及时下载视频。

<a id="code-block-16"></a>

```json
{
    "request_id": "0a15ad3c-cde7-9f7e-b8d2-xxxxxx",
    "output": {
        "task_id": "0025d1e1-009a-4f53-9c27-xxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
        "orig_prompt": "将视频中女孩的衣服替换为图片中的衣服",
        "submit_time": "2026-04-10 17:21:01.719",
        "scheduled_time": "2026-04-10 17:21:13.182",
        "end_time": "2026-04-10 17:31:41.286"
    },
    "usage": {
        "video_count": 1,
        "duration": 10.08,
        "input_video_duration": 5.04,
        "output_video_duration": 5.04,
        "SR": "720"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="错误码"></a>

<a id="0d0a562d05nkh"></a>

<a id="2e1d8db361w9w"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见错误码进行解决。
