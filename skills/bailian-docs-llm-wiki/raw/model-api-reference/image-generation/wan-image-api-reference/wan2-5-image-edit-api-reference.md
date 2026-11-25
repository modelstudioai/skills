# 万相-通用图像编辑2.5

万相-通用图像编辑wan2.5模型仅需文本指令，即可基于单张或多张参考图像，实现主体一致的图像编辑、多图融合等能力。

**快速入口**：[使用指南](../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/wan-image-edit.md)

<a id="模型概览"></a>

<a id="4a3e46b825d2k"></a>

## 模型概览

| 模型功能 | 输入示例 | 输出图像 |
| --- | --- | --- |
| 单图编辑 | ![damotest2023\_Portrait\_photography\_outdoors\_fashionable\_beauty\_409ae3c1-19e8-4515-8e50-b3c9072e1282\_2-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3943878571/p1011665.webp) | ![a26b226d-f044-4e95-a41c-d1c0d301c30b-转换自-png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3943878571/p1011666.webp)<br><br>将花卉连衣裙换成一件复古风格的蕾丝长裙，领口和袖口有精致的刺绣细节。 |
| 多图融合 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8142593671/p1020961.png) | ![p1028883](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7142593671/p1028892.webp)<br><br>将图1中的闹钟放置到图2的餐桌的花瓶旁边位置 |

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型简介</strong></p></th><th><p><strong>输出图像规格</strong></p></th></tr></thead><tbody><tr><td><p>wan2.5-i2i-preview</p></td><td><p>万相2.5 preview</p><p>支持单图编辑、多图融合</p></td><td><p>图片格式：PNG。</p><p>图像分辨率：</p><ul><li><p>通过 <code>parameters.size</code> 参数指定输出图像的分辨率，格式为<code>宽*高</code>（单位：像素）。</p></li><li><p>若未指定分辨率，系统将默认生成总像素为 <code>1280*1280</code> 的图像，并按以下规则保持宽高比（近似值）：</p><ul><li><p>单图输入：宽高比与输入图像一致；</p></li><li><p>多图输入：宽高比与最后一张输入图像一致。</p></li></ul></li></ul></td></tr></tbody></table>

> **说明**
>
> 调用前，请查阅各地域支持的[模型列表与价格](../../../model-user-guide/get-started-with-models/models.md)。

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

在调用前，先[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。

> **重要**
>
> 华北2（北京）和新加坡地域拥有独立的 **API Key**与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="http调用"></a>

<a id="42703589880ts"></a>

## HTTP调用

由于图像编辑任务耗时较长（通常为1-2分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

**新加坡地域**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> （必选）</p><p>模型名称。详情参见<a href="../../../model-user-guide/get-started-with-models/models.md">模型列表与价格</a>。</p><p>示例值：wan2.5-i2i-preview。</p><p><strong>input</strong> <code>object</code> （必选）</p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>正向提示词，用来描述生成图像中期望包含的元素和视觉特点。</p><p>支持中英文，长度不超过2000个字符，每个汉字/字母占一个字符，超过部分会自动截断。</p><p>提示词的使用技巧请参见<a href="../../../model-user-guide/use-cases/text-to-image-prompt.md">文生图Prompt指南</a>。</p><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p><strong>images</strong> <code>array of string</code> <strong>（必选）</strong></p><p>图像URL数组。</p><ul><li>数组长度不超过3，即最多输入3张图片。</li><li>多图输入时，按照数组顺序定义图像顺序。</li></ul><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽高范围均为[384, 5000]像素。</li><li>文件大小：不超过10MB。</li></ul><p>支持的输入格式：</p><ol><li><p>使用公网可访问URL</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<code>http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg</code>。</li></ul></li><li><p>传入 Base64 编码图像后的字符串</p><ul><li>格式：data:{MIME_type};base64,{base64_data}</li><li>示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）</li><li>Base64 编码规范请参见<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/wan-image-edit.md#8db0e2215frua">图像传入方式</a>。</li></ul></li></ol><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。如设置图像分辨率、开启prompt智能改写、添加水印等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>size</strong> <code>string</code> （可选）</p><p>设置输出图像的分辨率，格式为<code>宽*高</code>。默认值为 <code>1280*1280</code>。</p><ul><li>图像分辨率：总像素在 [768<em>768, 1280</em>1280] 之间，且宽高比范围为 [1:4, 4:1]。</li><li>示例值：1280*1280。</li></ul><a id="accordion-推荐分辨率及对应宽高比"></a><section><p>推荐分辨率及对应宽高比</p><div><ul><li>1280*1280：1:1</li><li>1024*1024：1:1</li><li>800*1200：2:3</li><li>1200*800：3:2</li><li>960*1280：3:4</li><li>1280*960：4:3</li><li>720*1280：9:16</li><li>1280*720：16:9</li><li>1344*576：21:9</li></ul></div></section><p>若未指定<code>size</code>，系统将默认生成总像素为 <code>1280*1280</code> 的图像，并按以下规则保持宽高比（近似值）：</p><ul><li>单图输入：宽高比与输入图像一致；</li><li>多图输入：宽高比与最后一张输入图像一致。</li></ul><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。n越大费用越高，请在调用前确认<a href="../../../model-user-guide/get-started-with-models/models.md">模型价格</a>。</p></div></div><p>生成图片的数量。取值范围为1~4张，默认为<code>4</code>。为控制成本，测试建议显式设置为1。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>prompt_extend</strong><code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写，提升综合表现，但会增加耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：不开启智能改写。</li></ul><p>示例值：true。</p><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围是<code>[0, 2147483647]</code>。</p><p>如果不提供，则算法自动生成一个随机数作为种子。如果提供，则根据<code>n</code>的值分别为n张图片生成seed参数，例如n=4，算法将分别生成seed、seed+1、seed+2、seed+3作为参数的图片。</p><p>若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-单图编辑-tab"></a>单图编辑<div><a id="code-code-group-单图编辑"></a><pre class="language-bash"><code> curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-i2i-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;将花卉连衣裙换成一件复古风格的蕾丝长裙，领口和袖口有精致的刺绣细节。&quot;,
        &quot;images&quot;: [
            &quot;https://img.alicdn.com/imgextra/i2/O1CN01vHOj4h28jOxUJPwY8_!!6000000007968-49-tps-1344-896.webp&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true,
        &quot;n&quot;: 1
    }
}'
</code></pre></div><a id="fig-code-group-多图融合-tab"></a>多图融合<div><a id="code-code-group-多图融合"></a><pre class="language-bash"><code> curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-i2i-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;将图1中的闹钟放置到图2的餐桌的花瓶旁边位置&quot;,
        &quot;images&quot;: [
            &quot;https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp&quot;,
            &quot;https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;n&quot;: 1
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-2"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   **轮询建议**：图像生成过程耗时较长，建议采用**轮询**机制，并设置合理的查询间隔（如 10 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回图像链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><blockquote><p>若使用新加坡地域的模型，需将base_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。</p></blockquote><a id="code-block-3"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong> <code>array of object</code></p><p>任务结果列表，包括图像URL、prompt、部分任务执行失败报错信息等。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>actual_prompt</strong> <code>string</code></p><p>开启 prompt 智能改写后，返回实际使用的优化后 prompt。若未开启该功能，则不返回此字段。</p><p><strong>url</strong> <code>string</code></p><p>模型生成图片的URL地址。</p><p><strong>code</strong> <code>string</code></p><p>图像错误码。部分任务执行失败时会返回该字段。</p><p><strong>message</strong> <code>string</code></p><p>图像错误信息。部分任务执行失败时会返回该字段。</p></div></section><p><strong>task_metrics</strong> <code>object</code></p><p>任务结果统计。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>图像URL仅保留24小时，超时后会被自动清除，请及时保存生成的图像。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;d1f2a1be-9c58-48af-b43f-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;7f4836cd-1c47-41b3-b3a4-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-09-23 22:14:10.800&quot;,
        &quot;scheduled_time&quot;: &quot;2025-09-23 22:14:10.825&quot;,
        &quot;end_time&quot;: &quot;2025-09-23 22:15:23.456&quot;,
        &quot;results&quot;: [
            {
                &quot;orig_prompt&quot;: &quot;将花卉连衣裙换成一件复古风格的蕾丝长裙，领口和袖口有精致的刺绣细节。&quot;,
                &quot;actual_prompt&quot;: &quot;将粉色褶皱连衣裙替换为一件复古风格的蕾丝长裙，领口和袖口带有精致的刺绣细节，保持人物发型、妆容和姿态不变，整体风格与原图的柔和色调和古典氛围一致。&quot;,
                &quot;url&quot;: &quot;https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx&quot;
            }
        ],
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 1,
            &quot;FAILED&quot;: 0,
            &quot;SUCCEEDED&quot;: 1
        }
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;xxxxxx&quot;,
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 4,
            &quot;SUCCEEDED&quot;: 0,
            &quot;FAILED&quot;: 4
        }
    }
}
</code></pre></section><a id="任务部分失败"></a><section><a id="任务部分失败-h4"></a><h4>任务部分失败</h4><p>模型可以在一次任务中生成多张图片。只要有一张图片生成成功，任务状态将标记为<code>SUCCEEDED</code>，并且返回相应的图像URL。对于生成失败的图片，结果中会返回相应的失败原因。同时在usage统计中，只会对成功的结果计数。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;85eaba38-0185-99d7-8d16-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-xxxxxx&quot;,
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
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-sdk调用"></a>

<a id="db17b3098c2iv"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP调用](wan2-5-image-edit-api-reference.md#42703589880ts)基本一致，参数结构根据语言特性进行封装。

由于图像编辑任务耗时约30秒～60秒，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="a3ad9a3b6d9if"></a>

### Python SDK调用

> **重要**
>
> **请确保 DashScope Python SDK 版本不低于**2.0.1**。**
>
> 若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装或升级SDK](../../preparations/install-sdk.md)进行更新。

<a id="sec-tabs-5"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="de8be082068hw"></a>

##### 请求示例

本示例支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="code-block-8"></a>

```python
import base64
import mimetypes
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import dashscope
import requests
import os

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- 输入图片：使用 Base64 编码 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可

1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""

# 【方式一】使用公网图片 URL
image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# 格式要求：file:// + 文件路径
# 示例（绝对路径）：
# image_url_1 = "file://" + "/path/to/your/image_1.png"     # Linux/macOS
# image_url_2 = "file://" + "C:/path/to/your/image_2.png"  # Windows
# 示例（相对路径）：
# image_url_1 = "file://" + "./image_1.png"                 # 以实际路径为准
# image_url_2 = "file://" + "./image_1.png"                # 以实际路径为准

# 【方式三】使用Base64编码的图片
# image_url_1 = encode_file("./image_1.png")               # 以实际路径为准
# image_url_2 = encode_file("./image_2.png")              # 以实际路径为准

print('----sync call, please wait a moment----')
# generate 为一步式调用（提交+等待），直接返回已完成的任务结果
job = client.images.generate(model="wan2.5-i2i-preview",
                             prompt="将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                             extra_input={'images': [image_url_1, image_url_2]},
                             negative_prompt="",
                             n=1,
                             # size="1280*1280",
                             prompt_extend=True,
                             watermark=False,
                             seed=12345)
print('response: %s' % job)
# 在当前目录下保存图片
for result in job.results:
    file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
    with open('./%s' % file_name, 'wb+') as f:
        f.write(requests.get(result.url).content)
```

<a id="177b27c9b28it"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-9"></a>

```json
{
    "request_id": "8ad45834-4321-44ed-adf5-xxxxxx",
    "task_id": "3aff9ebd-35fc-4339-98a3-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
            "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
            "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟朝向镜头，与桌面平行，阴影自然投射于桌面。"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "FAILED": 0,
        "SUCCEEDED": 1
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

本示例使用公网URL方式传入图片。

<a id="b9b6d3bf42rc7"></a>

##### 请求示例

<a id="code-block-10"></a>

```python
import os
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import dashscope
import requests

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 使用公网图片 URL
image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task----')
    wait_async_task(task_info)

# 创建异步任务
def create_async_task():
    job = client.images.jobs.create(model="wan2.5-i2i-preview",
                                    prompt="将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                                    extra_input={'images': [image_url_1, image_url_2]},
                                    negative_prompt="",
                                    n=1,
                                    # size="1280*1280",
                                    prompt_extend=True,
                                    watermark=False,
                                    seed=12345)
    print(job)
    print(job.task_id, job.status)
    return job

# 等待异步任务结束（指数退避轮询，默认总预算24小时；任务失败会抛出DashScopeError）
def wait_async_task(task):
    done = client.images.jobs.wait(task)
    print(done)
    print(done.status)
    # save file to current directory
    for result in done.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(result.url).content)

# 获取异步任务信息
def fetch_task_status(task):
    snapshot = client.images.jobs.fetch(task)
    print(snapshot)
    print(snapshot.status)

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task):
    job = client.images.jobs.cancel(task)
    print(job)

if __name__ == '__main__':
    async_call()
```

<a id="4f9da575fdd1b"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-11"></a>

```json
{
    "request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
    "task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-12"></a>

```text
{
    "request_id": "8ad45834-4321-44ed-adf5-xxxxxx",
    "task_id": "3aff9ebd-35fc-4339-98a3-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
            "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
            "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟朝向镜头，与桌面平行，阴影自然投射于桌面。"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "FAILED": 0,
        "SUCCEEDED": 1
    },
    "usage": {
        "image_count": 1
    }
}
```

<a id="java-sdk调用"></a>

<a id="589b80853e6rn"></a>

### Java SDK调用

> **重要**
>
> **请确保 DashScope Java SDK 版本不低于**`2.22.2`**。**
>
> 若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装或升级SDK](../../preparations/install-sdk.md)进行更新。

<a id="sec-tabs-6"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="5ac3ea9f52tii"></a>

##### 请求示例

本示例支持三种图像输入方式：公网URL、Base64编码、本地文件路径。

<a id="code-block-13"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class Image2Image {

    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * 图像输入方式说明：三选一即可
     *
     * 1. 使用公网URL - 适合已有公开可访问的图片
     * 2. 使用本地文件 - 适合本地开发测试
     * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
     */

    //【方式一】公网URL
    static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
    static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

    //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
    // static String imageUrl_1 = "file://" + "/your/path/to/image_1.png";    // Linux/macOS
    // static String imageUrl_2 = "file:///" + "C:/your/path/to/image_2.png";  // Windows

    //【方式三】Base64编码
    // static String imageUrl_1 = encodeFile("/your/path/to/image_1.png");
    // static String imageUrl_2 = encodeFile("/your/path/to/image_2.png");

    // 设置待编辑的图片列表
    static List<String> imageUrls = new ArrayList<>();
    static {
        imageUrls.add(imageUrl_1);
        imageUrls.add(imageUrl_2);
    }

    public static void syncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-i2i-preview")
                        .prompt("将图1中的闹钟放置到图2的餐桌的花瓶旁边位置")
                        .images(imageUrls)
                        .n(1)
                         //.size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
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

    /**
     * 将文件编码为Base64字符串
     * @param filePath 文件路径
     * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
     */
    public static String encodeFile(String filePath) {
        Path path = Paths.get(filePath);
        if (!Files.exists(path)) {
            throw new IllegalArgumentException("文件不存在: " + filePath);
        }
        // 检测MIME类型
        String mimeType = null;
        try {
            mimeType = Files.probeContentType(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法检测文件类型: " + filePath);
        }
        if (mimeType == null || !mimeType.startsWith("image/")) {
            throw new IllegalArgumentException("不支持或无法识别的图像格式");
        }
        // 读取文件内容并编码
        byte[] fileBytes = null;
        try{
            fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
            throw new IllegalArgumentException("无法读取文件内容: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
        syncCall();
    }
}
```

<a id="ecf553d14e183"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-14"></a>

```json
{
    "request_id": "d362685b-757f-4eac-bab5-xxxxxx",
    "output": {
        "task_id": "bfa7fc39-3d87-4fa7-b1e6-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟正面朝向镜头，与花瓶平行摆放。",
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
            }
        ],
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

本示例使用公网URL方式传入图片。

<a id="f7b9a75fbbo26"></a>

##### 请求示例

<a id="code-block-15"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Image2Image {
    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    //公网URL
    static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
    static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

    // 设置待编辑的图片列表
    static List<String> imageUrls = new ArrayList<>();
    static {
        imageUrls.add(imageUrl_1);
        imageUrls.add(imageUrl_2);
    }

    public static void asyncCall() {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-i2i-preview")
                        .prompt("将图1中的闹钟放置到图2的餐桌的花瓶旁边位置")
                        .images(imageUrls)
                        .n(1)
                        //.size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
            System.out.println("---async call, please wait a moment----");
            result = imageSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();

        System.out.println("taskId=" + taskId);

        try {
            result = imageSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
    }

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空。
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
    }

    public static void main(String[] args) {
        asyncCall();
    }
}
```

<a id="228c690525jkh"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-16"></a>

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

> url 有效期24小时，请及时下载图片。

<a id="code-block-17"></a>

```text
{
    "request_id": "d362685b-757f-4eac-bab5-xxxxxx",
    "output": {
        "task_id": "bfa7fc39-3d87-4fa7-b1e6-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [
            {
                "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                "actual_prompt": "将图1中的蓝色闹钟放置在图2餐桌的花瓶右侧，靠近桌布边缘的位置，保持闹钟正面朝向镜头，与花瓶平行摆放。",
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
            }
        ],
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

<a id="使用限制"></a>

<a id="63a009e43a1iy"></a>

## 使用限制

-   **数据时效**：任务task\_id和 图像url均只保留 24 小时，过期后将无法查询或下载。
-   **内容审核**：输入prompt、图像和输出图像均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误码](../../preparations/error-code.md)。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="c928ee689aw6l"></a>

## 常见问题

<a id="4fbf0ee72aahq"></a>

##### Q：之前使用通用图像编辑 2.1，现在切换到 wan2.5 模型，SDK调用方式需要调整吗？

A：需要调整。两个版本的参数设计不同：

-   [通用图像编辑2.1](wanx-image-edit-api-reference.md)：需同时传入`prompt`和`function`参数。
-   [通用图像编辑2.5](wan2-5-image-edit-api-reference.md)：**仅需**传入`prompt`，所有编辑操作通过文本指令描述，**不再支持也不需要**`function`参数。

<a id="9d8d426f60za1"></a>

##### Q: 如何查看模型调用量？

A: 模型调用完成后数分钟内，请在[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)页面，查看模型的调用次数、成功率等指标。操作指引：[如何查看模型调用记录？](../../../model-user-guide/test-1/new-free-quota.md#ab6ba5c538rn3)
