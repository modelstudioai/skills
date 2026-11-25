# Z-Image API参考

Z-Image 是一款轻量级文生图模型，可快速生成图像，支持中英文字渲染，并灵活适配多种分辨率与宽高比例。

**快速入口**：在线体验（[北京](https://bailian.console.aliyun.com/cn-beijing/model/experience/vision/imageGenerate?modelId=z-image-turbo) | [新加坡](https://bailian.console.aliyun.com/ap-southeast-1/model/experience/vision/imageGenerate?modelId=z-image-turbo)） | [技术博客](https://tongyi-mai.github.io/Z-Image-blog/)

<a id="效果展示"></a>

<a id="5849834e92mb7"></a>

## 效果展示

| 输入提示词 | 输出图像 |
| --- | --- |
| film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“**Press esc to exit full screen**”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。 | ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6915736671/p1036890.png) |

<a id="模型概览"></a>

<a id="4a3e46b825d2k"></a>

## 模型概览

| 模型名称 | 模型简介 | 输出图像规格 |
| --- | --- | --- |
| z-image-turbo | 轻量模型，快速生图 | 图像分辨率：总像素在\[512\*512, 2048\*2048\]之间，推荐分辨率请参见[size参数设置](z-image-api-reference.md)<br><br>图像格式：png<br><br>图像张数：固定1张 |

> **说明**
>
> 调用前，请查阅各地域支持的模型列表。

<a id="前提条件"></a>

<a id="b0dc1cbdbfd9g"></a>

## 前提条件

您需要[获取与配置 API Key](../../preparations/get-api-key.md)，并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="http同步调用"></a>

<a id="39337f0fd0wzt"></a>

## HTTP同步调用

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

**新加坡地域**：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="576ce84612n7u"></a><h4>请求参数</h4><a id="bb0a157056fbk"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="45d1fa2260zn6"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。必须为：z-image-turbo。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组。必须包含且仅包含<strong>1 个 text 对象</strong>。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词用于描述期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过800个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图像的分辨率，格式为<code>宽*高</code>。</p><ul><li>默认值：<code>1024*1536</code>。</li><li>总像素范围限制：总像素在 [512<em>512, 2048</em>2048]之间。</li><li>推荐分辨率范围：总像素在 [1024<em>1024, 1536</em>1536]之间，出图效果更佳。</li></ul><p>示例值：1024*1536。</p><a id="accordion-总像素为1024-1024的推荐分辨率"></a><section><p>总像素为1024*1024的推荐分辨率：</p><div><ul><li>1:1: 1024*1024</li><li>2:3: 832*1248</li><li>3:2: 1248*832</li><li>3:4: 864*1152</li><li>4:3: 1152*864</li><li>7:9: 896*1152</li><li>9:7: 1152*896</li><li>9:16: 720*1280</li><li>9:21: 576*1344</li><li>16:9: 1280*720</li><li>21:9：1344*576</li></ul></div></section><a id="accordion-总像素为1280-1280的推荐分辨率"></a><section><p>总像素为1280*1280的推荐分辨率：</p><div><ul><li>1:1: 1280*1280</li><li>2:3: 1024*1536</li><li>3:2: 1536*1024</li><li>3:4: 1104*1472</li><li>4:3: 1472*1104</li><li>7:9: 1120*1440</li><li>9:7: 1440*1120</li><li>9:16: 864*1536</li><li>9:21: 720*1680</li><li>16:9: 1536*864</li><li>21:9: 1680*720</li></ul></div></section><a id="accordion-总像素为1536-1536的推荐分辨率"></a><section><p>总像素为1536*1536的推荐分辨率：</p><div><ul><li>1:1：1536*1536</li><li>2:3: 1248*1872</li><li>3:2: 1872*1248</li><li>3:4: 1296*1728</li><li>4:3: 1728*1296</li><li>7:9: 1344*1728</li><li>9:7: 1728*1344</li><li>9:16: 1152*2048</li><li>9:21: 864*2016</li><li>16:9: 2048*1152</li><li>21:9: 2016*864</li></ul></div></section><p><strong>prompt_extend</strong> <code>bool</code> （可选）</p><div><div><p><strong>重要</strong>prompt_extend直接影响费用。设为 <code>true</code> 时价格高于 <code>false</code>，具体见参见<a href="../../../model-user-guide/test-1/model-pricing.md#6713612f55h4l">模型价格</a>。</p></div></div><p>是否启用智能提示词（text）改写。开启后，将使用大模型优化提示词，并输出思考过程。</p><ul><li>false：默认值，关闭智能改写。输出图像和原始文本提示词。</li><li>true：开启智能改写。输出图像、优化后的文本提示词、思考过程。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="文生图"></a><section><a id="文生图-h4"></a><h4>文生图</h4><p>以下示例直接返回图片，响应速度较快。</p><p>若想开启“智能思考”能力，请设置<code>prompt_extend=true</code> 。开启后，系统将在返回图片的同时，返回优化后的提示词及其推理过程，但会增加响应时间。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;z-image-turbo&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“Press esc to exit full screen”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: false,
        &quot;size&quot;: &quot;1120*1440&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b7e833ee1f962"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。此数组仅包含1个元素。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，正常完成时为 <code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p><p><strong>text</strong> <code>string</code></p><ul><li>当prompt_extend=false时，为输入的提示词。</li><li>当prompt_extend=true时，为改写后的提示词。</li></ul></div></section><p><strong>reasoning_content</strong> <code>string</code></p><p>模型的思考过程，仅在prompt_extend=true时返回思考文本。</p></div></section></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>width</strong> <code>integer</code></p><p>生成图像的宽度（像素）。</p><p><strong>height</strong> <code>integer</code></p><p>生成图像的高度（像素）。</p><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的数量，固定为1。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入token数量，prompt_extend=false时固定为0。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出token数量，prompt_extend=false时固定为0。</p><p><strong>output_tokens_details</strong><code>object</code></p><p>输出 token 详情，仅当prompt_extend=true时返回。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>reasoning_tokens</strong><code>integer</code></p><p>推理思考使用的 token 数量。</p></div></section><p><strong>total_tokens</strong><code>integer</code></p><p>总token数量，prompt_extend=false时固定为0。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx&quot;
                        },
                        {
                            &quot;text&quot;: &quot;film grain, analog film texture, soft film lighting, Kodak Portra 400 style, cinematic grainy texture, photorealistic details, subtle noise, (film grain:1.2)。采用近景特写镜头拍摄的东亚年轻女性，呈现户外雪地场景。她体型纤瘦，呈站立姿势，身体微微向右侧倾斜，头部抬起看向画面上方，姿态自然放松。她的面部是典型东亚长相，肤色白皙，脸颊带有自然的红润感，五官清秀：眼睛是深棕色，眼型偏圆，眼神略带惊讶地望向上方，眼白部分可见；眉毛是深黑色，形状自然弯长；鼻子小巧挺直，嘴唇涂有红色口红，唇瓣微张，表情带着轻微的惊讶或好奇。她的头发是深黑色长直发，发丝被风吹得略显凌乱，部分垂在脸颊两侧，头顶佩戴一顶深灰色的头盔，头盔边缘露出少量发丝。服装是蓝白拼接的厚重外套，外套材质看起来是毛绒与布料结合，显得温暖厚实，适合雪地环境。背景是被白雪覆盖的户外场景，远处可见模糊的树木轮廓，天空是明亮的浅蓝色，带有少量白云，光线是强烈的自然日光，照亮人物面部与头发，形成清晰的光影，色调以蓝、白、黑为主，整体风格清新自然。画面顶部有黑色提示框，内有“Press esc to exit full screen”的白色文字。镜头的近景视角放大了人物的表情与细节，营造出户外雪地的真实氛围。&quot;
                        }
                    ],
                    &quot;reasoning_content&quot;: &quot;&quot;,
                    &quot;role&quot;: &quot;assistant&quot;
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;height&quot;: 1440,
        &quot;image_count&quot;: 1,
        &quot;input_tokens&quot;: 0,
        &quot;output_tokens&quot;: 0,
        &quot;total_tokens&quot;: 0,
        &quot;width&quot;: 1120
    },
    &quot;request_id&quot;: &quot;8a0809b4-a796-47f4-a095-394b02b62xxx&quot;
}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="使用限制"></a>

<a id="63a009e43a1iy"></a>

## 使用限制

-   图像`url`均只保留 24 小时，请及时下载。
-   **内容审核**：输入的 `prompt` 和输出的图像均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误码](../../preparations/error-code.md)。

<a id="计费与限流"></a>

<a id="5dafefe82bgrh"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](../../../model-user-guide/test-1/model-pricing.md#6713612f55h4l)。
-   模型限流请参见[Z-Image](../../../model-user-guide/get-started-with-models/rate-limit.md#e17ad85fd8wwl)。
-   根据是否开启智能按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[免费额度](../../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="e2b1945f71tld"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="c928ee689aw6l"></a>

## 常见问题

<a id="q-如何查看模型调用量"></a>

<a id="ae11776b04p4u"></a>

### Q: 如何查看模型调用量？

A: 模型调用完一小时后，请在[**模型监控**（北京）](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)或[**模型监控**（新加坡）](https://bailian.console.aliyun.com/ap-southeast-1/model/telemetry) 页面，查看模型的调用次数、成功率等指标。详情请参见[账单查询与成本管理](../../../model-user-guide/test-1/bill-query-and-cost-management.md)。

<a id="q-如何获取图像存储的访问域名白名单"></a>

<a id="5fb153423ct8z"></a>

### Q：如何获取图像存储的访问域名白名单？

A： 模型生成的图像存储于阿里云OSS，API将返回一个临时的公网URL（链接有效期为 24 小时，请及时下载保存）。图片URL的域名格式为`dashscope-{标识}.oss-accelerate.aliyuncs.com`或`dashscope-{标识}.oss-cn-{地域}.aliyuncs.com`。**若需要对该下载地址进行防火墙白名单配置**，请注意：由于底层存储会动态变更，以下bucket名称仅供参考，可能随时更新：dashscope-a717、dashscope-66f3、dashscope-7c2c、dashscope-2522、dashscope-c72b、dashscope-0484、dashscope-7e0f、dashscope-5859、dashscope-5496、dashscope-35f9、dashscope-31d9、dashscope-7f1f、dashscope-cc75、dashscope-64e9。为避免过期信息影响访问，文档不提供固定的OSS域名白名单。如有安全管控需求，请联系客户经理获取最新OSS域名列表。API当前仅支持返回URL格式，不支持base64格式输出。
