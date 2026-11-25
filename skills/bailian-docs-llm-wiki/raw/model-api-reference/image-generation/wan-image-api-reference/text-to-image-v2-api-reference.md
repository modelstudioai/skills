# 万相-文生图V2版API参考

万相-文生图模型基于文本生成图像，支持多种艺术风格与写实摄影效果，满足多样化创意需求。

**快速入口：**在线体验（[北京](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate?modelId=wan2.6-t2i) | [新加坡](https://bailian.console.aliyun.com/model/experience/vision/imageGenerate)| [弗吉尼亚](https://bailian.console.aliyun.com/us-east-1/model/experience/vision/imageGenerate?modelId=wan2.6-t2i)） | [万相官网](https://tongyi.aliyun.com/wan/generate/image/text-to-image) | [文生图使用指南](../../../model-user-guide/model-experience/image-and-video-generation/image-model/text-to-image.md)

> **说明**
>
> 万相官网的功能与API支持的能力可能存在差异。本文档以API的实际能力为准，并会随功能更新及时同步。

<a id="模型概览"></a>

<a id="4a3e46b825d2k"></a>

## 模型概览

<table><thead><tr><th><strong>模型名称</strong></th><th><strong>模型简介</strong></th><th><strong>输出图像格式</strong></th></tr></thead><tbody><tr><td><p>wan2.6-t2i <code>推荐</code></p></td><td><p>万相2.6</p><p>支持在总像素面积与宽高比约束内，自由选尺寸（同wan2.5）</p></td><td rowspan="2"><p>图像分辨率：总像素在[1280<em>1280, 1440</em>1440]之间</p><p>图像宽高比：[1:4, 4:1]<br>图像格式：png<br><br></p></td></tr><tr><td><p>wan2.5-t2i-preview <code>推荐</code></p></td><td><p>万相2.5 preview</p><p>支持在总像素面积与宽高比约束内，自由选尺寸</p><blockquote><p>例如，支持768*2700，而2.2及以下版本单边上限 1400</p></blockquote></td></tr><tr><td><p>wan2.2-t2i-flash</p></td><td><p>万相2.2极速版</p><p>较2.1模型速度提升50%</p></td><td rowspan="5"><p>图像分辨率：宽高均在[512, 1440]像素之间</p><p>图像格式：png</p></td></tr><tr><td><p>wan2.2-t2i-plus</p></td><td><p>万相2.2专业版</p><p>较2.1模型稳定性与成功率全面提升</p></td></tr><tr><td><p>wanx2.1-t2i-turbo</p></td><td><p>万相2.1极速版</p></td></tr><tr><td><p>wanx2.1-t2i-plus</p></td><td><p>万相2.1专业版</p></td></tr><tr><td><p>wanx2.0-t2i-turbo</p></td><td><p>万相2.0极速版</p></td></tr></tbody></table>

> **说明**
>
> -   调用前，请查阅各地域支持的模型列表。
> -   **wan2.6模型**：支持[HTTP同步调用](text-to-image-v2-api-reference.md#39337f0fd0wzt)、[HTTP异步调用](text-to-image-v2-api-reference.md#9c68ccc525nta)、[Dashscope Python SDK调用](text-to-image-v2-api-reference.md#b3d1dbc5dbtgx)和[Dashscope Java SDK调用](text-to-image-v2-api-reference.md#e8a7f6d4c9xyz)。
> -   **wan2.5及以下版本模型**：支持[HTTP异步调用](text-to-image-v2-api-reference.md#0d8029dcc8pxl)、[Dashscope Python SDK调用](text-to-image-v2-api-reference.md#7afdfdd68emtf)和[Dashscope Java SDK调用](text-to-image-v2-api-reference.md#589b80853e6rn)，不支持HTTP同步调用。

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

在调用前，先[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。

> **重要**
>
> 华北2（北京）、新加坡和美国（弗吉尼亚）地域拥有独立的 **API Key**与**请求地址**，不可混用，跨地域调用将导致鉴权失败或服务报错，详情请参见[选择地域、服务部署范围和接入域名](../../../model-user-guide/get-started-with-models/regions.md)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="http同步调用-wan2-6"></a>

<a id="39337f0fd0wzt"></a>

## HTTP同步调用（wan2.6）

> **重要**
>
> 本章节接口为**新版协议**，仅支持 **wan2.6**模型。

一次请求即可获得结果，流程简单，推荐大多数场景使用。

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

<table><tbody><tr><td><a id="576ce84612n7u"></a><h4>请求参数</h4><a id="bb0a157056fbk"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="45d1fa2260zn6"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wan2.6-t2i。</p><div><div><p><strong>说明</strong>wan2.5及以下版本模型，HTTP调用请参见<a href="text-to-image-v2-api-reference.md#0d8029dcc8pxl">HTTP异步调用</a>。</p></div></div><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词，用于描述期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过2100个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超出部分将自动截断。</p><p>示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图像的分辨率，格式为<code>宽*高</code>。</p><ul><li>默认值为 <code>1280*1280</code>。</li><li>总像素在 [1280<em>1280, 1440</em>1440] 之间且宽高比范围为 [1:4, 4:1]。例如，768*2700符合要求。</li></ul><p>示例值：1280*1280。</p><a id="accordion-常见比例推荐的分辨率"></a><section><p>常见比例推荐的分辨率</p><div><ul><li>1:1：1280*1280</li><li>3:4：1104*1472</li><li>4:3：1472*1104</li><li>9:16：960*1696</li><li>16:9：1696*960</li></ul></div></section><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#0006b52b83ua9">模型价格</a>。</p></div></div><p>生成图片的数量。取值范围为1~4张，默认为<code>4</code>。</p><p>注意：按张计费，测试建议设为 1。</p><p><strong>prompt_extend</strong> <code>bool</code> （可选）</p><p>是否开启提示词智能改写。开启后，将使用大模型优化正向提示词，对较短的提示词有明显提升效果，但增加3-4秒耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：关闭智能改写。</li></ul><div><div><p><strong>说明</strong>开启智能改写后，改写生成的提示词可能引入受版权保护的内容，从而触发内容审核，返回 <code>IPInfringementSuspect</code> 或 <code>DataInspectionFailed</code> 报错。</p><p>遇到上述报错时，可将 <code>prompt_extend</code> 设置为 <code>false</code> 后重试。若提示词本身直接包含受版权保护的角色名或作品名，关闭智能改写仍会报错，需修改提示词本身。</p></div></div><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="文生图"></a><section><a id="文生图-h4"></a><h4>文生图</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.6-t2i&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;一间有着精致窗户的花店，漂亮的木质门，摆放着花朵&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: false,
        &quot;n&quot;: 1,
        &quot;negative_prompt&quot;: &quot;&quot;,
        &quot;size&quot;: &quot;1280*1280&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="49792d3618l67"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p><p><strong>type</strong> <code>string</code></p><p>输出的类型，固定为image。</p></div></section></div></section></div></section><p><strong>finished</strong> <code>boolean</code></p><p>任务是否结束。</p><ul><li>true：已结束。</li><li>false：未结束。</li></ul></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的张数。</p><p><strong>size</strong> <code>string</code></p><p>生成的图像分辨率。示例值：1280*1280。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入token。文生图按图片张数计费，当前固定为0。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出token。文生图按图片张数计费，当前固定为0。</p><p><strong>total_tokens</strong><code>integer</code></p><p>总token。文生图按图片张数计费，当前固定为0。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ],
                    &quot;role&quot;: &quot;assistant&quot;
                }
            }
        ],
        &quot;finished&quot;: true
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1,
        &quot;input_tokens&quot;: 0,
        &quot;output_tokens&quot;: 0,
        &quot;size&quot;: &quot;1280*1280&quot;,
        &quot;total_tokens&quot;: 0
    },
    &quot;request_id&quot;: &quot;815505c6-7c3d-49d7-b197-xxxxx&quot;
}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="http异步调用-wan2-6"></a>

<a id="9c68ccc525nta"></a>

## HTTP异步调用（wan2.6）

> **重要**
>
> 本章节接口为**新版协议**，仅支持 **wan2.6**模型。

任务流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="06ddfb0e63h4p"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs-4"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="13f75b0cab2wu"></a><h4>请求参数</h4><a id="f0bc65e20eu5a"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="962410e014g1v"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wan2.6-t2i。</p><div><div><p><strong>说明</strong>wan2.5及以下版本模型，HTTP调用请参见<a href="text-to-image-v2-api-reference.md#0d8029dcc8pxl">HTTP异步调用。</a></p></div></div><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词，用于描述期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过2100个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p>示例值：一间有着精致窗户的花店，漂亮的木质门，摆放着花朵。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超出部分将自动截断。</p><p>示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图像的分辨率，格式为<code>宽*高</code>。</p><ul><li>默认值为 <code>1280*1280</code>。</li><li>总像素在 [1280<em>1280, 1440</em>1440] 之间且宽高比范围为 [1:4, 4:1]。例如，768*2700符合要求。</li></ul><p>示例值：1280*1280。</p><a id="accordion-常见比例推荐的分辨率-2"></a><section><p>常见比例推荐的分辨率</p><div><ul><li>1:1：1280*1280</li><li>3:4：1104*1472</li><li>4:3：1472*1104</li><li>9:16：960*1696</li><li>16:9：1696*960</li></ul></div></section><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#0006b52b83ua9">模型价格</a>。</p></div></div><p>生成图片的数量。取值范围为1~4张，默认为<code>4</code>。</p><p>注意：按张计费，测试建议设为 1。</p><p><strong>prompt_extend</strong> <code>bool</code> （可选）</p><p>是否开启prompt智能改写。开启后，将使用大模型优化正向提示词，对较短的提示词有明显提升效果，但增加3-4秒耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：不开启智能改写。</li></ul><div><div><p><strong>说明</strong>开启智能改写后，改写生成的提示词可能引入受版权保护的内容，从而触发内容审核，返回 <code>IPInfringementSuspect</code> 或 <code>DataInspectionFailed</code> 报错。</p><p>遇到上述报错时，可将 <code>prompt_extend</code> 设置为 <code>false</code> 后重试。若提示词本身直接包含受版权保护的角色名或作品名，关闭智能改写仍会报错，需修改提示词本身。</p></div></div><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-5"></a><section><a id="文生图-2"></a><section><a id="文生图-2-h4"></a><h4>文生图</h4><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'X-DashScope-Async: enable' \
--data '{
    &quot;model&quot;: &quot;wan2.6-t2i&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;一间有着精致窗户的花店，漂亮的木质门，摆放着花朵&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: false,
        &quot;n&quot;: 1,
        &quot;negative_prompt&quot;: &quot;&quot;,
        &quot;size&quot;: &quot;1280*1280&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="37cef0683eg79"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-6"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="0d606bc055ssc"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-7"></a>

<a id="华北2-北京-3"></a>

<a id="华北2-北京-3-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚-3"></a>

<a id="美国-弗吉尼亚-3-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   **轮询建议**：图像生成过程耗时较长，建议采用**轮询**机制，并设置合理的查询间隔（如 10 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回图像链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="8442f74589dej"></a><h4>请求参数</h4><a id="bb10a5aa136zm"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="09e80fbec7hk0"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-8"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-7"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="e1be57396anjq"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的图像URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>finished</strong> <code>boolean</code></p><p>任务是否结束。</p><ul><li>true：已结束。</li><li>false：未结束。</li></ul><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，正常完成时为 <code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。</p><p><strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p><p><strong>type</strong> <code>string</code></p><p>输出的类型，固定为image。</p></div></section></div></section></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。<strong>只对成功的结果计数。</strong></p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的张数。</p><p><strong>size</strong> <code>string</code></p><p>生成的图像分辨率。示例值：1280*1280。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入token数量。当前固定为0。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出token数量。当前固定为0。</p><p><strong>total_tokens</strong><code>integer</code></p><p>总token数量。当前固定为0。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-9"></a><section><a id="任务执行成功-2"></a><section><a id="任务执行成功-2-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;2ddf53fa-699a-4267-9446-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;3cd3fa4e-53ee-4136-9cab-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-12-18 20:03:01.802&quot;,
        &quot;scheduled_time&quot;: &quot;2025-12-18 20:03:01.834&quot;,
        &quot;end_time&quot;: &quot;2025-12-18 20:03:29.260&quot;,
        &quot;finished&quot;: true,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;size&quot;: &quot;1280*1280&quot;,
        &quot;total_tokens&quot;: 0,
        &quot;image_count&quot;: 1,
        &quot;output_tokens&quot;: 0,
        &quot;input_tokens&quot;: 0
    }
}
</code></pre></section><a id="任务执行异常-2"></a><section><a id="任务执行异常-2-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="http异步调用-wan2-5及以下版本模型"></a>

<a id="0d8029dcc8pxl"></a>

## HTTP异步调用（wan2.5及以下版本模型）

> **重要**
>
> 此接口为**旧版协议**，仅支持**wan2.5及以下版本模型**。

由于文生图任务耗时较长（通常为1-2分钟），API采用异步调用。整个流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="步骤1-创建任务获取任务id-2"></a>

<a id="db8cf70432oe3"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs-10"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求参数</h4><a id="79473e45c592d"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> （必选）</p><p>模型名称。文生图模型请参见<a href="wanx-image-edit-api-reference.md">模型列表</a>。</p><p>示例值：wan2.5-t2i-preview。</p><div><div><p><strong>说明</strong>wan2.6模型的HTTP调用请参见<a href="text-to-image-v2-api-reference.md#39337f0fd0wzt">HTTP同步调用</a>、<a href="text-to-image-v2-api-reference.md#9c68ccc525nta">HTTP异步调用</a>。</p></div></div><p><strong>input</strong> <code>object</code> （必选）</p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>正向提示词，用来描述生成图像中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母/标点符号占一个字符，超过部分会自动截断。长度限制因模型版本而异：</p><ul><li>wan2.5-t2i-preview：长度不超过2000个字符。</li><li>wan2.2、wan2.1系列模型：长度不超过500个字符。</li><li>wanx2.0-t2i-turbo：长度不超过800个字符。</li></ul><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p>提示词的使用技巧请参见<a href="../../../model-user-guide/use-cases/text-to-image-prompt.md">文生图Prompt指南</a>。</p><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用来描述不希望在画面中看到的内容，可以对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超过部分会自动截断。</p><p>示例值：低分辨率、错误、最差质量、低质量、残缺、多余的手指、比例不良等。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。如设置图像分辨率、开启prompt智能改写、添加水印等。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图像的分辨率，格式为<code>宽*高</code>。默认值和约束因模型版本而异：</p><ul><li>wan2.5-t2i-preview：默认值为 <code>1280*1280</code>。总像素在 [1280<em>1280, 1440</em>1440] 之间且宽高比范围为 [1:4, 4:1]。例如，768*2700符合要求。</li><li>wan2.2及以下版本模型：默认值为<code>1024*1024</code>。图像宽高在[512, 1440]之间，最大分辨率为1440<em>1440。例如， 768</em>2700超单边限制，不支持。</li></ul><p>示例值：1280*1280。</p><a id="accordion-常见比例推荐的分辨率-3"></a><section><p>常见比例推荐的分辨率</p><div><p>以下分辨率适用于wan2.5-t2i-preview</p><ul><li>1:1：1280*1280</li><li>3:4：1104*1472</li><li>4:3：1472*1104</li><li>9:16：960*1696</li><li>16:9：1696*960</li></ul></div></section><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#0006b52b83ua9">模型价格</a>。</p></div></div><p>生成图片的数量。取值范围为1~4张，默认为<code>4</code>。测试阶段建议设置为1，便于低成本验证。</p><p><strong>prompt_extend</strong><code>boolean</code> （可选）</p><p>是否开启prompt智能改写。开启后使用大模型对输入prompt进行智能改写。对于较短的prompt生成效果提升明显，但会增加耗时。</p><ul><li>true：默认值，开启智能改写。</li><li>false：关闭智能改写。</li></ul><p>示例值：true。</p><div><div><p><strong>说明</strong>开启智能改写后，改写生成的提示词可能引入受版权保护的内容，从而触发内容审核，返回 <code>IPInfringementSuspect</code> 或 <code>DataInspectionFailed</code> 报错。</p><p>遇到上述报错时，可将 <code>prompt_extend</code> 设置为 <code>false</code> 后重试。若提示词本身直接包含受版权保护的角色名或作品名，关闭智能改写仍会报错，需修改提示词本身。</p></div></div><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-11"></a><section><a id="文生图-3"></a><section><a id="文生图-3-h4"></a><h4>文生图</h4><a id="code-block-10"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.5-t2i-preview&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一间有着精致窗户的花店，漂亮的木质门，摆放着花朵&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1280*1280&quot;,
        &quot;n&quot;: 1
    }
}'
</code></pre></section><a id="文生图-使用反向提示词"></a><section><a id="文生图-使用反向提示词-h4"></a><h4>文生图（使用反向提示词）</h4><p>通过 negative_prompt 指定生成的图片避免出现“人物”元素。</p><a id="code-block-11"></a><pre class="language-bash"><code>curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;wan2.2-t2i-flash&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;雪地，白色小教堂，极光，冬日场景，柔和的光线。&quot;,
        &quot;negative_prompt&quot;: &quot;人物&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;n&quot;: 1
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-22"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-3"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-12"></a><section><a id="成功响应-2"></a><section><a id="成功响应-2-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-12"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应-2"></a><section><a id="异常响应-2-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-13"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果-2"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-13"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-5"></a>

<a id="新加坡-5-h4"></a>

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

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-14"></a><section><a id="查询任务结果-2"></a><section><a id="查询任务结果-2-h4"></a><h4>查询任务结果</h4><p>请将<code>86ecf553-d340-4e21-xxxxxxxxx</code>替换为真实的task_id。</p><blockquote><p>若使用新加坡地域的模型，需将base_url替换为https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx，其中{WorkspaceId}需替换为真实的业务空间ID。</p></blockquote><a id="code-block-14"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f277d7425foyq"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-23"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-4"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的图像URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>results</strong> <code>array of object</code></p><p>任务结果列表，包括图像URL、prompt、部分任务执行失败报错信息等。</p><a id="accordion-数据结构"></a><section><p>数据结构</p><div><a id="code-block-15"></a><pre class="language-json"><code>{
    &quot;results&quot;: [
        {
            &quot;orig_prompt&quot;: &quot;&quot;,
            &quot;actual_prompt&quot;: &quot;&quot;,
            &quot;url&quot;: &quot;&quot;
        },
        {
            &quot;code&quot;: &quot;&quot;,
            &quot;message&quot;: &quot;&quot;
        }
    ]
}
</code></pre></div></section><a id="accordion-属性-24"></a><section><p>属性</p><div><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>actual_prompt</strong> <code>string</code></p><p>开启 prompt 智能改写后，返回实际使用的优化后 prompt。若未开启该功能，则不返回此字段。</p><p><strong>url</strong> <code>string</code></p><p>图像URL地址。仅在 task_status 为 SUCCEEDED 时返回。链接有效期24小时，可通过此URL下载图像。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>task_metrics</strong> <code>object</code></p><p>任务结果统计。</p><a id="accordion-属性-25"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-26"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-15"></a><section><a id="任务执行成功-3"></a><section><a id="任务执行成功-3-h4"></a><h4>任务执行成功</h4><p>图像URL仅保留24小时，超时后会被自动清除，请及时保存生成的图像。</p><a id="code-block-16"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;f767d108-7d50-908b-a6d9-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;d492bffd-10b5-4169-b639-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-01-08 16:03:59.840&quot;,
        &quot;scheduled_time&quot;: &quot;2025-01-08 16:03:59.863&quot;,
        &quot;end_time&quot;: &quot;2025-01-08 16:04:10.660&quot;,
        &quot;results&quot;: [
            {
                &quot;orig_prompt&quot;: &quot;一间有着精致窗户的花店，漂亮的木质门，摆放着花朵&quot;,
                &quot;actual_prompt&quot;: &quot;一间有着精致雕花窗户的花店，漂亮的深色木质门上挂着铜制把手。店内摆放着各式各样的鲜花，包括玫瑰、百合和向日葵，色彩鲜艳，生机勃勃。背景是温馨的室内场景，透过窗户可以看到街道。高清写实摄影，中景构图。&quot;,
                &quot;url&quot;: &quot;https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png&quot;
            }
        ],
        &quot;task_metrics&quot;: {
            &quot;TOTAL&quot;: 1,
            &quot;SUCCEEDED&quot;: 1,
            &quot;FAILED&quot;: 0
        }
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-17"></a><pre class="language-json"><code>{
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
</code></pre></section><a id="任务部分失败"></a><section><a id="任务部分失败-h4"></a><h4>任务部分失败</h4><p>模型可以在一次任务中生成多张图片。只要有一张图片生成成功，任务状态将标记为<code>SUCCEEDED</code>，并且返回相应的图像URL。对于生成失败的图片，结果中会返回相应的失败原因。同时在usage统计中，只会对成功的结果计数。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-18"></a><pre class="language-json"><code>{
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
                &quot;message&quot;: &quot;An internal timeout error has occurred during execution, please try again later or contact service support.&quot;
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
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-19"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-python-sdk调用"></a>

<a id="1751252d8bf7c"></a>

## DashScope Python SDK调用

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于文生图任务耗时较长，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="wan2-6"></a>

<a id="b3d1dbc5dbtgx"></a>

### wan2.6

> **重要**
>
> -   以下代码仅适合 **wan2.6** 模型。
> -   请确保 DashScope Python SDK 版本**不低于**2.0.1，再运行以下代码。更新请参考[安装SDK](../../preparations/install-sdk.md)。

各地域的`region`和 API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-16"></a>

<a id="华北2-北京-5"></a>

<a id="华北2-北京-5-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-6"></a>

<a id="新加坡-6-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚-4"></a>

<a id="美国-弗吉尼亚-4-h4"></a>

#### 美国（弗吉尼亚）

`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1`

<a id="德国-法兰克福-3"></a>

<a id="德国-法兰克福-3-h4"></a>

#### 德国（法兰克福）

`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> 全球部署范围（法兰克福地域）仅支持异步调用。

<a id="sec-tabs-17"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="84e6e611eeumd"></a>

##### 请求示例

<a id="code-block-20"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

print("----sync call, please wait a moment----")
# generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
job = client.images.generate(
    model="wan2.6-t2i",
    prompt='一间有着精致窗户的花店，漂亮的木质门，摆放着花朵',
    negative_prompt="",
    prompt_extend=True,
    watermark=False,
    n=1,
    size="1280*1280"
)
print(job)
print(job.image_urls)
```

<a id="b0515f126ag6l"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-21"></a>

```json
{
    "request_id": "820dd0db-eb42-4e05-8d6a-1ddb4axxxxxx",
    "task_id": "f470bbfd-d955-4165-935b-d35b8eexxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx"
        }
    ],
    "usage": {
        "image_count": 1,
        "size": "1280*1280"
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="4ad5f44591826"></a>

##### 请求示例

<a id="code-block-22"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 创建异步任务
def create_async_task():
    print("Creating async task...")
    job = client.images.jobs.create(
        model="wan2.6-t2i",
        prompt='一间有着精致窗户的花店，漂亮的木质门，摆放着花朵',
        negative_prompt="",
        prompt_extend=True,
        watermark=False,
        n=1,
        size="1280*1280"
    )
    print("Task created successfully:", job)
    return job

# 等待任务完成（指数退避轮询，任务 FAILED 或被取消时抛出 DashScopeError）
def wait_for_completion(task):
    print("Waiting for task completion...")
    done = client.images.jobs.wait(task)
    print("Task succeeded!")
    print("Response:", done)
    print("Image URLs:", done.image_urls)

# 获取异步任务信息
def fetch_task_status(task):
    print("Fetching task status...")
    status = client.images.jobs.fetch(task)
    print("Task status:", status.status)

# 取消异步任务
def cancel_task(task):
    print("Canceling task...")
    response = client.images.jobs.cancel(task)
    print("Task canceled successfully:", response.status)

# 主执行流程
if __name__ == "__main__":
    try:
        task = create_async_task()
        wait_for_completion(task)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="d5de68e40618u"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-23"></a>

```json
{
    "request_id": "c4f11410-ea42-4996-957d-9c82f9xxxxxx",
    "task_id": "f470bbfd-d955-4165-935b-d35b8eexxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-24"></a>

```json
{
    "request_id": "7e57e7e8-00b0-4534-9aff-fe31e0xxxxxx",
    "task_id": "f470bbfd-d955-4165-935b-d35b8exxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx"
        }
    ],
    "usage": {
        "image_count": 1,
        "size": "1280*1280"
    }
}
```

<a id="wan2-5及以下版本模型"></a>

<a id="7afdfdd68emtf"></a>

### wan2.5及以下版本模型

> **重要**
>
> -   以下代码仅适合wan2.5及以下版本模型。
>     
> -   请确保 DashScope Python SDK 版本**不低于**2.0.1，再运行以下代码。
>     
>     请参考[安装SDK](../../preparations/install-sdk.md)进行更新。

各地域的`region`和 API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-18"></a>

<a id="华北2-北京-6"></a>

<a id="华北2-北京-6-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-7"></a>

<a id="新加坡-7-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-19"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="de8be082068hw"></a>

##### 请求示例

<a id="code-block-25"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

print('----sync call, please wait a moment----')
try:
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    job = client.images.generate(
        model="wan2.5-t2i-preview",
        prompt="一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
        negative_prompt="",
        n=1,
        size='1280*1280',
        prompt_extend=True,
        watermark=False,
        seed=12345
    )
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

<a id="177b27c9b28it"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-26"></a>

```json
{
    "request_id": "9d634fda-5fe9-9968-a908-xxxxxx",
    "task_id": "d35658e4-483f-453b-b8dc-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png",
            "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间精致的花店，窗户上装饰着优雅的雕花，漂亮的木质门上挂着铜制把手。店内摆放着各种色彩鲜艳的花朵，如玫瑰、郁金香和百合等。背景是温馨的室内场景，光线柔和，营造出宁静舒适的氛围。高清写实摄影，近景中心构图。"
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

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

<a id="b9b6d3bf42rc7"></a>

##### 请求示例

<a id="code-block-27"></a>

```python
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def async_call():
    print('----create task----')
    task_info = create_async_task()
    print('----wait task done then save image----')
    wait_async_task(task_info)

# 创建异步任务
def create_async_task():
    job = client.images.jobs.create(
        model="wan2.5-t2i-preview",
        prompt="一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
        negative_prompt="",
        n=1,
        size='1280*1280',
        prompt_extend=True,
        watermark=False,
        seed=12345
    )
    print(job)
    print(job.task_id, job.status)
    return job

# 等待异步任务结束（指数退避轮询，任务 FAILED 或被取消时抛出 DashScopeError）
def wait_async_task(task):
    done = client.images.jobs.wait(task)
    print(done)
    # save file to current directory
    for url in done.image_urls:
        file_name = PurePosixPath(unquote(urlparse(url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(url).content)

# 获取异步任务信息
def fetch_task_status(task):
    status = client.images.jobs.fetch(task)
    print(status)
    print(status.status)

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task):
    rsp = client.images.jobs.cancel(task)
    print(rsp)
    print(rsp.status)

if __name__ == '__main__':
    try:
        async_call()
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="4f9da575fdd1b"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-28"></a>

```json
{
    "request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
    "task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-29"></a>

```json
{
    "request_id": "9d634fda-5fe9-9968-a908-xxxxxx",
    "task_id": "d35658e4-483f-453b-b8dc-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.png",
            "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间精致的花店，窗户上装饰着优雅的雕花，漂亮的木质门上挂着铜制把手。店内摆放着各种色彩鲜艳的花朵，如玫瑰、郁金香和百合等。背景是温馨的室内场景，光线柔和，营造出宁静舒适的氛围。高清写实摄影，近景中心构图。"
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

<a id="dashscope-java-sdk调用"></a>

<a id="db17b3098c2iv"></a>

## DashScope Java SDK调用

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于文生图任务耗时较长，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="wan2-6-2"></a>

<a id="e8a7f6d4c9xyz"></a>

### wan2.6

> **重要**
>
> -   以下代码仅适合 **wan2.6-t2i** 模型。
> -   请确保 DashScope Java SDK 版本**不低于**`2.22.6`，再运行以下代码。

各地域的`region`和 API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-20"></a>

<a id="华北2-北京-7"></a>

<a id="华北2-北京-7-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-8"></a>

<a id="新加坡-8-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="美国-弗吉尼亚-5"></a>

<a id="美国-弗吉尼亚-5-h4"></a>

#### 美国（弗吉尼亚）

`https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1`

<a id="德国-法兰克福-4"></a>

<a id="德国-法兰克福-4-h4"></a>

#### 德国（法兰克福）

`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> 全球部署范围（法兰克福地域）仅支持异步调用。

<a id="sec-tabs-21"></a>

<a id="同步调用-3"></a>

<a id="同步调用-3-h4"></a>

#### 同步调用

<a id="a8c9f7e6d5bcd"></a>

##### 请求示例

<a id="code-block-30"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.Collections;

public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException {
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-t2i")
                .n(1)
                .size("1280*1280")
                .negativePrompt("")
                .promptExtend(true)
                .watermark(false)
                .messages(Collections.singletonList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---sync call, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            basicCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

<a id="e8a9f7d6c5fgh"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-31"></a>

```json
{
    "status_code": 200,
    "request_id": "50b57166-eaaa-4f17-b1e0-35a5ca88672c",
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "finished": true
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "image_count": 1,
        "size": "1280*1280",
        "total_tokens": 0
    }
}
```

<a id="异步调用-3"></a>

<a id="异步调用-3-h4"></a>

#### 异步调用

<a id="e8a9f7d6c5lmn"></a>

##### 请求示例

<a id="code-block-32"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import java.util.Collections;

public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-t2i")
                .n(1)
                .size("1280*1280")
                .negativePrompt("")
                .promptExtend(true)
                .watermark(false)
                .messages(Collections.singletonList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---async call, creating task----");
            result = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();
        // 等待任务完成
        waitTask(taskId);
    }

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            asyncCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
    }
}
```

<a id="d9f8a7e6b5qrs"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-33"></a>

```json
{
    "status_code": 200,
    "request_id": "9cd85950-2e26-4b2c-b562-1694cf9288e5",
    "code": "",
    "message": "",
    "output": {
        "task_id": "4c861fbe-af89-4a2f-8fc5-4bb15c3139ba",
        "task_status": "PENDING"
    },
    "usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-34"></a>

```json
{
    "status_code": 200,
    "request_id": "cbdf1424-306e-4a52-82f3-8bf5d8a99103",
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "4c861fbe-af89-4a2f-8fc5-4bb15c3139ba",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-01-16 16:36:06.556",
        "scheduled_time": "2026-01-16 16:36:06.591",
        "end_time": "2026-01-16 16:36:25.190",
        "finished": true
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "size": "1280*1280",
        "total_tokens": 0,
        "image_count": 1
    }
}
```

<a id="wan2-5及以下版本模型-2"></a>

<a id="589b80853e6rn"></a>

### wan2.5及以下版本模型

> **重要**
>
> -   以下代码仅适合wan2.5及以下版本模型。
>     
> -   请确保 DashScope Java SDK 版本**不低于**`2.22.2`，再运行以下代码。
>     
>     若版本过低，可能会触发 “url error, please check url!” 等错误。请参考[安装SDK](../../preparations/install-sdk.md)进行更新。

各地域的`region`和 API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-22"></a>

<a id="华北2-北京-8"></a>

<a id="华北2-北京-8-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-9"></a>

<a id="新加坡-9-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="sec-tabs-23"></a>

<a id="同步调用-4"></a>

<a id="同步调用-4-h4"></a>

#### 同步调用

<a id="5ac3ea9f52tii"></a>

##### 请求示例

<a id="code-block-35"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.task.AsyncTaskListParam;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import java.util.Map;

public class Main {

    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void basicCall() throws ApiException, NoApiKeyException {
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-t2i-preview")
                        .prompt("一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                        .n(1)
                        .size("1280*1280")
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

    public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
    }

    public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // If set DASHSCOPE_API_KEY environment variable, apiKey can null.
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
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

<a id="ecf553d14e183"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-36"></a>

```json
{
    "request_id": "22f9c744-206c-9a78-899a-xxxxxx",
    "output": {
        "task_id": "4a0f8fc6-03fb-4c44-a13a-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [{
           "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间有着精致雕花窗户的花店，漂亮的深色木质门微微敞开。店内摆放着各式各样的鲜花，包括玫瑰、百合和向日葵，色彩鲜艳，香气扑鼻。背景是温馨的室内场景，光线柔和，透过窗户洒在花朵上。高清写实摄影，中景构图。",
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png"
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

<a id="异步调用-4"></a>

<a id="异步调用-4-h4"></a>

#### 异步调用

<a id="f7b9a75fbbo26"></a>

##### 请求示例

<a id="code-block-37"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.HashMap;
import java.util.Map;

public class Main {

    static {
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    String apiKey = System.getenv("DASHSCOPE_API_KEY");

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
        // 设置parameters参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
                ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-t2i-preview")
                        .prompt("一间有着精致窗户的花店，漂亮的木质门，摆放着花朵")
                        .n(1)
                        .size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
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
            result = imageSynthesis.wait(taskId, apiKey);
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

<a id="228c690525jkh"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-38"></a>

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

<a id="code-block-39"></a>

```json
{
    "request_id": "22f9c744-206c-9a78-899a-xxxxxx",
    "output": {
        "task_id": "4a0f8fc6-03fb-4c44-a13a-xxxxxx",
        "task_status": "SUCCEEDED",
        "results": [{
           "orig_prompt": "一间有着精致窗户的花店，漂亮的木质门，摆放着花朵",
            "actual_prompt": "一间有着精致雕花窗户的花店，漂亮的深色木质门微微敞开。店内摆放着各式各样的鲜花，包括玫瑰、百合和向日葵，色彩鲜艳，香气扑鼻。背景是温馨的室内场景，光线柔和，透过窗户洒在花朵上。高清写实摄影，中景构图。",
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1.png"
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

<a id="使用限制"></a>

<a id="63a009e43a1iy"></a>

## 使用限制

-   **数据时效**：任务`task_id`和 图像`url`均只保留 24 小时，过期后将无法查询或下载。
-   **内容审核**：输入的 `prompt` 和输出的图像均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误码](../../preparations/error-code.md)。

<a id="计费与限流"></a>

<a id="5dafefe82bgrh"></a>

## 计费与限流

-   模型免费额度和计费单价请参见百炼控制台。
-   模型限流请参见[万相](../../../model-user-guide/get-started-with-models/rate-limit.md#513e0a3df24v7)。
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](../../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
