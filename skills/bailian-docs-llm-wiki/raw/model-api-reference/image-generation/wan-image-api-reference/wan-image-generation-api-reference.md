# 万相-图像生成与编辑2.6 API参考

万相图像生成模型支持 图像编辑 、 图文混排输出 ，满足多样化生成与集成需求。

<a id="模型概览"></a>

<a id="4a3e46b825d2k"></a>

## 模型概览

| 模型名称 | 模型简介 | 输出图像规格 |
| --- | --- | --- |
| wan2.6-image | 万相2.6 image<br><br>支持图像编辑和图文混排输出<br><br>如需纯文本生成图片（文生图），建议使用[wan2.6-t2i 模型（通义万相-文生图V2）](text-to-image-v2-api-reference.md)。 | 图片格式：PNG。<br><br>图像分辨率和尺寸请参见[size参数](wan-image-generation-api-reference.md)。 |

> **说明**
>
> 调用前，请查阅各地域支持的[模型列表与价格](../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl)。

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

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

<a id="http同步调用"></a>

<a id="dac5ce452cwz1"></a>

## HTTP同步调用

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

> 全球部署范围（法兰克福地域）仅支持[异步调用](wan-image-generation-api-reference.md#42703589880ts)。

<table><tbody><tr><td><a id="78f3155ff3r2l"></a><h4>请求参数</h4><a id="fd84180b66rpo"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Sse</strong><code>string</code>（可选）</p><p>用于启用流式输出。</p><ul><li>仅当 <code>parameters.enable_interleave=true</code> 时，<strong>必须</strong>将该字段设为 <code>enable</code>。</li><li>其他情况下可不传或忽略。</li></ul><a id="7d7bb26156npj"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。设置为wan2.6-image。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数固定设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词用于描述您期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过2000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p>示例值：参考这个风格的图片，生成番茄炒蛋。</p><p><strong>注意</strong>：<code>content</code>数组中，必须且只能包含一个含 <code>text</code> 字段的对象。</p><p><strong>image</strong><code>string</code>（可选）</p><p>输入图像的URL或Base64编码字符串。</p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽高范围均为[240, 8000]像素。</li><li>文件大小：不超过10MB。</li></ul><p>图像数量限制：</p><ul><li><p>输入图像数量与<code>parameters.enable_interleave</code>参数有关。</p><ul><li>当<code>enable_interleave=true</code>时（图文混排输出），可输入<strong>0~1</strong>张图像。</li><li>当<code>enable_interleave=false</code>时（图像编辑），<strong>必须</strong>输入<strong>1~4</strong>张图像。</li></ul></li><li><p>当输入多张图像时，需在<code>content</code>数组中传入多个<code>image</code>对象，并按照数组顺序定义图像顺序。</p></li></ul><p>支持的输入格式：</p><ol><li><p>使用公网可访问URL</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<code>http://wanx.alicdn.com/material/xxx.jpeg</code>。</li></ul></li><li><p>传入 Base64 编码图像后的字符串</p><ul><li>格式：data:{MIME_type};base64,{base64_data}</li><li>示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）</li><li>Base64 编码规范请参见<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/wan-image-edit.md#8db0e2215frua">图像传入方式</a>。</li></ul></li></ol></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超出部分将自动截断。</p><p>示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图片分辨率参数，支持参考输入图比例和直接指定两种方式。</p><p>当<code>enable_interleave=false</code>（即图像编辑模式）时：</p><ul><li><p>方式一：参考输入图比例（推荐）</p><p>可选的输出分辨率档位：<code>1K</code>（默认）、<code>2K</code>。</p><ul><li><code>1K</code>：输出总像素接近 1280*1280，宽高比与最后一张输入图像一致。</li><li><code>2K</code>：输出总像素接近 2048*2048，宽高比与最后一张输入图像一致。</li></ul></li><li><p>方式二：指定生成图像的宽高像素值</p><p>总像素在 [768<em>768, 2048</em>2048] 之间，且宽高比范围为 [1:4, 4:1]。</p><blockquote><p>实际输出图像的像素值为接近指定值的16的倍数。</p></blockquote></li></ul><p>当<code>enable_interleave=true</code>（即图文混排输出模式）时：</p><ul><li><p>方式一：参考输入图比例（默认方式）</p><ul><li>若输入图像总像素 ≤ 1280*1280，输出总像素和宽高比与输入图像一致。</li><li>若输入图像总像素 &gt; 1280<em>1280，输出总像素接近 1280</em>1280，宽高比与输入图像一致。</li><li>若无输入图像，则为1280*1280。</li></ul></li><li><p>方式二：指定生成图像的宽高像素值</p><p>总像素在 [768<em>768, 1280</em>1280] 之间，且宽高比范围为 [1:4, 4:1]。</p><blockquote><p>实际输出图像的像素值为接近指定值的16的倍数。</p></blockquote></li></ul><a id="accordion-常见比例推荐的分辨率"></a><section><p>常见比例推荐的分辨率</p><div><ul><li>1:1：1280*1280</li><li>2:3：800*1200</li><li>3:2：1200*800</li><li>3:4：960*1280</li><li>4:3：1280*960</li><li>9:16：720*1280</li><li>16:9：1280*720</li><li>21:9：1344*576</li></ul></div></section><p><strong>enable_interleave</strong> <code>bool</code> （可选）</p><p>控制生图模式：</p><ul><li><p>false：默认值，表示图像编辑模式（支持多图输入及主体一致性生成）。</p><ul><li>用途：基于1～4张输入图像进行编辑、风格迁移或主体一致性生成。</li><li>输入：必须提供至少1张参考图像。</li><li>输出：可生成1至4张结果图像。</li></ul></li><li><p>true ：表示启用图文混排输出模式（仅支持传入一张图像或不传图像）。</p><ul><li><p>用途：根据文本描述生成图文并茂的内容，或进行纯文本生成图像（文生图）。</p><p>纯文生图场景建议优先使用<a href="text-to-image-v2-api-reference.md">wan2.6-t2i 模型（通义万相-文生图V2）</a>。</p></li><li><p>输入：可以不提供图像（文生图），或提供最多1张参考图像。</p></li><li><p>输出：生成包含文本和图像的混合内容。</p></li></ul></li></ul><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl">模型价格</a>。</p></div></div><p>指定生成图片的数量。该参数的取值范围与含义取决于 enable_interleave（模式开关）的状态：</p><ul><li><p>当 <code>enable_interleave=false</code>（图像编辑模式）：</p><ul><li>作用：直接控制生成图像的数量。</li><li>取值范围：1～4，默认值为 4。</li><li>建议在测试阶段将此值设置为 1，以便低成本验证效果。</li></ul></li><li><p>当 <code>enable_interleave=true</code>（图文混排模式）：</p><ul><li>限制：此参数默认为1，且必须固定为1。若设置为其他值，接口将报错。</li><li>说明：在此模式下，如需控制生成图像的数量上限，请使用 <code>max_images</code> 参数。</li></ul></li></ul><p><strong>max_images</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>max_images影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl">模型价格</a>。</p></div></div><p>仅在图文混排模式（即 <code>enable_interleave=true</code>）下生效。</p><ul><li>作用：指定模型在单次回复中生成图像的<strong>最大数量</strong>。</li><li>取值范围：1～5，默认值为 5。</li><li>注意：该参数仅代表“数量上限”。实际生成的图像数量由模型推理决定，可能会少于设定值（例如：设置为 5，模型可能根据内容仅生成 3 张）。</li></ul><p><strong>prompt_extend</strong> <code>bool</code> （可选）</p><p>仅在图像编辑模式（即<code>enable_interleave = false</code>）下生效。</p><p>是否开启 Prompt（提示词）智能改写功能。该功能仅对正向提示词进行优化与润色，不会改变反向提示词。</p><ul><li>true：默认值，开启智能改写。</li><li>false：关闭智能改写，使用原始提示词。</li></ul><p><strong>stream</strong> <code>bool</code> （可选）</p><p>控制返回结果是否为流式输出。在图像混排模式（即 <code>enable_interleave = true</code>）下，<strong>必须</strong>设置为<code>true</code>。</p><ul><li>false：默认值，非流式输出。</li><li>true：流式输出。</li></ul><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="图像编辑"></a><section><a id="图像编辑-h4"></a><h4>图像编辑</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.6-image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;参考图1的风格和图2的背景，生成番茄炒蛋&quot;
                    },
                    {
                        &quot;image&quot;: &quot;https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png&quot;
                    },
                    {
                        &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: false,
        &quot;n&quot;: 1,
        &quot;enable_interleave&quot;: false,
        &quot;size&quot;: &quot;1K&quot;
    }
}'
</code></pre></section><a id="图文混排-仅支持流式"></a><section><a id="图文混排-仅支持流式-h4"></a><h4>图文混排（仅支持流式）</h4><p>同步接口在启用图文混排输出（即 <code>parameters.enable_interleave = true</code>）时，<strong>仅支持流式输出</strong>，必须同时满足以下两项配置：</p><ul><li>设置<code>X-DashScope-Sse</code>为<code>enable</code>。</li><li>设置<code>parameters.stream</code>为<code>true</code>。</li></ul><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'X-DashScope-Sse: enable' \
--data '{
    &quot;model&quot;: &quot;wan2.6-image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;给我一个3张图辣椒炒肉教程&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;max_images&quot;: 3,
        &quot;size&quot;: &quot;1280*1280&quot;,
        &quot;stream&quot;: true,
        &quot;enable_interleave&quot;:true
    }
}'
</code></pre></section><a id="dashscope-cli"></a><section><a id="dashscope-cli-h4"></a><h4>dashscope CLI</h4><a id="code-block-3"></a><pre class="language-bash"><code>export DASHSCOPE_API_KEY=&quot;your-api-key&quot;
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL=&quot;https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1&quot;
dashscope image-generation create -m wan2.6-t2i -t &quot;一只可爱的猫&quot;
</code></pre><div><div><p><strong>重要</strong>SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见</p><a href="../../preparations/dashscope-sdk-expert.md">DashScope SDK Expert</a>。</div></div><p>完整地域表见 <a href="../../preparations/base-url.md">Base URL 总览</a>。</p></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="dee809656c79t"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>choices</strong> <code>array of object</code></p><p>模型生成的输出内容。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因。</p><p><strong>非流式输出场景</strong>：自然停止时为<code>stop</code>。</p><p><strong>流式输出场景</strong>：当开启流式输出时，该参数判断数据流是否传输结束。</p><ul><li>传输过程中：前序数据包会持续返回 <code>&quot;finish_reason&quot;: &quot;null&quot;</code>，表示内容仍在生成中，请继续接收。</li><li>传输结束时：仅在<strong>最后一个</strong> JSON 结构体中返回 <code>&quot;finish_reason&quot;:&quot;stop&quot;</code>，表示流式请求已全部结束，应停止接收。</li></ul><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出的类型，枚举值为text、image。</p><p><strong>text</strong> <code>string</code></p><p>生成的文字。</p><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。</p><p><strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section><p><strong>finished</strong> <code>bool</code></p><p>请求结束标志符。</p><ul><li>true：表示请求结束。</li><li>false：表示请求未结束。</li></ul></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的张数。</p><p><strong>size</strong> <code>string</code></p><p>生成的图像分辨率。示例值：1376*768。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>按图片张数计费。</p><ul><li>在图像编辑模式下，固定为0。</li><li>在图文混排模式下，此字段统计输入文本的token数量（不计费）。</li></ul><p><strong>output_tokens</strong> <code>integer</code></p><p>按图片张数计费。</p><ul><li>在图像编辑模式下，固定为0。</li><li>在图文混排模式下，此字段统计输出文本的token数量（不计费）。</li></ul><p><strong>total_tokens</strong><code>integer</code></p><p>按图片张数计费。</p><ul><li>在图像编辑模式下，固定为0。</li><li>在图文混排模式下，此字段统计总token数量（不计费）。</li></ul></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx&quot;,
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
        &quot;size&quot;: &quot;1376*768&quot;,
        &quot;total_tokens&quot;: 0
    },
    &quot;request_id&quot;: &quot;a3f4befe-cacd-49c9-8298-xxxxxx&quot;
}
</code></pre></section><a id="任务执行成功-流式输出"></a><section><a id="任务执行成功-流式输出-h4"></a><h4>任务执行成功（流式输出）</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-5"></a><pre class="language-json"><code>{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;肉&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:571,&quot;image_count&quot;:3,&quot;output_tokens&quot;:543,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;香&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:572,&quot;image_count&quot;:3,&quot;output_tokens&quot;:544,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;交织&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:573,&quot;image_count&quot;:3,&quot;output_tokens&quot;:545,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
......
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;image&quot;,&quot;image&quot;:&quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxxx&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:557,&quot;image_count&quot;:3,&quot;output_tokens&quot;:529,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;趁&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:558,&quot;image_count&quot;:3,&quot;output_tokens&quot;:530,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;热&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:559,&quot;image_count&quot;:3,&quot;output_tokens&quot;:531,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;夹&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:560,&quot;image_count&quot;:3,&quot;output_tokens&quot;:532,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;起&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:561,&quot;image_count&quot;:3,&quot;output_tokens&quot;:533,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;一块&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;null&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:562,&quot;image_count&quot;:3,&quot;output_tokens&quot;:534,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
{&quot;output&quot;:{&quot;choices&quot;:[{&quot;message&quot;:{&quot;content&quot;:[{&quot;type&quot;:&quot;text&quot;,&quot;text&quot;:&quot;肉&quot;}],&quot;role&quot;:&quot;assistant&quot;},&quot;finish_reason&quot;:&quot;stop&quot;}],&quot;finished&quot;:true},&quot;usage&quot;:{&quot;total_tokens&quot;:563,&quot;image_count&quot;:3,&quot;output_tokens&quot;:535,&quot;size&quot;:&quot;1280*1280&quot;,&quot;input_tokens&quot;:28},&quot;request_id&quot;:&quot;d2dcb952-bf91-4a6a-aad5-xxxxxx&quot;}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="http异步调用"></a>

<a id="42703589880ts"></a>

## HTTP异步调用

流程包含 **“创建任务 -> 轮询获取”** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="db8cf70432oe3"></a>

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

<table><tbody><tr><td><a id="f54fd191909ri"></a><h4>请求参数</h4><a id="0d489ca36e4mj"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="d6b6a20821cp8"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>示例值：wan2.6-image</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数固定设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（必选）</strong></p><p>正向提示词用于描述您期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过2000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p>示例值：参考这个风格的图片，生成番茄炒蛋。</p><p><strong>注意</strong>：<code>content</code>数组中，必须且只能包含一个含 <code>text</code> 字段的对象。</p><p><strong>image</strong><code>string</code>（可选）</p><p>输入图像的URL或Base64编码字符串。</p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽高范围均为[240, 8000]像素。</li><li>文件大小：不超过10MB。</li></ul><p>图像数量限制：</p><ul><li><p>输入图像数量与<code>parameters.enable_interleave</code>参数有关。</p><ul><li>当<code>enable_interleave=true</code>时（图文混排输出），可输入<strong>0~1</strong>张图像。</li><li>当<code>enable_interleave=false</code>时（图像编辑），<strong>必须</strong>输入<strong>1~4</strong>张图像。</li></ul></li><li><p>当输入多张图像时，需在<code>content</code>数组中传入多个<code>image</code>对象，并按照数组顺序定义图像顺序。</p></li></ul><p>支持的输入格式：</p><ol><li><p>使用公网可访问URL</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<code>http://wanx.alicdn.com/material/xxx.jpeg</code>。</li></ul></li><li><p>传入 Base64 编码图像后的字符串</p><ul><li>格式：data:{MIME_type};base64,{base64_data}</li><li>示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）</li><li>Base64 编码规范请参见<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/wan-image-edit.md#8db0e2215frua">图像传入方式</a>。</li></ul></li></ol></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>图像处理参数。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>negative_prompt</strong> <code>string</code> （可选）</p><p>反向提示词，用于描述不希望在图像中出现的内容，对画面进行限制。</p><p>支持中英文，长度不超过500个字符，超出部分将自动截断。</p><p>示例值：低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。</p><p><strong>size</strong> <code>string</code> （可选）</p><p>输出图片分辨率参数，支持参考输入图比例和直接指定两种方式。</p><p>当<code>enable_interleave=false</code>（即图像编辑模式）时：</p><ul><li><p>方式一：参考输入图比例（推荐）</p><p>可选的输出分辨率档位：<code>1K</code>（默认）、<code>2K</code>。</p><ul><li><code>1K</code>：输出总像素接近 1280*1280，宽高比与最后一张输入图像一致。</li><li><code>2K</code>：输出总像素接近 2048*2048，宽高比与最后一张输入图像一致。</li></ul></li><li><p>方式二：指定生成图像的宽高像素值</p><p>总像素在 [768<em>768, 2048</em>2048] 之间，且宽高比范围为 [1:4, 4:1]。</p><blockquote><p>实际输出图像的像素值为接近指定值的16的倍数。</p></blockquote></li></ul><p>当<code>enable_interleave=true</code>（即图文混排输出模式）时：</p><ul><li><p>方式一：参考输入图比例（默认方式）</p><ul><li>若输入图像总像素 ≤ 1280*1280，输出总像素和宽高比与输入图像一致。</li><li>若输入图像总像素 &gt; 1280<em>1280，输出总像素接近 1280</em>1280，宽高比与输入图像一致。</li><li>若无输入图像，则为1280*1280。</li></ul></li><li><p>方式二：指定生成图像的宽高像素值</p><p>总像素在 [768<em>768, 1280</em>1280] 之间，且宽高比范围为 [1:4, 4:1]。</p><blockquote><p>实际输出图像的像素值为接近指定值的16的倍数。</p></blockquote></li></ul><a id="accordion-常见比例推荐的分辨率-2"></a><section><p>常见比例推荐的分辨率</p><div><ul><li>1:1：1280*1280</li><li>2:3：800*1200</li><li>3:2：1200*800</li><li>3:4：960*1280</li><li>4:3：1280*960</li><li>9:16：720*1280</li><li>16:9：1280*720</li><li>21:9：1344*576</li></ul></div></section><p><strong>enable_interleave</strong> <code>bool</code> （可选）</p><p>控制生图模式：</p><ul><li><p>false：默认值，表示图像编辑模式（支持多图输入及主体一致性生成）。</p><ul><li>用途：基于1～4张输入图像进行编辑、风格迁移或主体一致性生成。</li><li>输入：必须提供至少1张参考图像。</li><li>输出：可生成1至4张结果图像。</li></ul></li><li><p>true ：表示启用图文混排输出模式（仅支持传入一张图像或不传图像）。</p><ul><li><p>用途：根据文本描述生成图文并茂的内容，或进行纯文本生成图像（文生图）。</p><p>纯文生图场景建议优先使用<a href="text-to-image-v2-api-reference.md">wan2.6-t2i 模型（通义万相-文生图V2）</a>。</p></li><li><p>输入：可以不提供图像（文生图），或提供最多1张参考图像。</p></li><li><p>输出：生成包含文本和图像的混合内容。</p></li></ul></li></ul><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl">模型价格</a>。</p></div></div><p>指定生成图片的数量。该参数的取值范围与含义取决于 enable_interleave（模式开关）的状态：</p><ul><li><p>当 <code>enable_interleave=false</code>（图像编辑模式）：</p><ul><li>作用：直接控制生成图像的数量。</li><li>取值范围：1～4，默认值为 4。</li><li>建议在测试阶段将此值设置为 1，以便低成本验证效果。</li></ul></li><li><p>当 <code>enable_interleave=true</code>（图文混排模式）：</p><ul><li>限制：此参数默认为1，且必须固定为1。若设置为其他值，接口将报错。</li><li>说明：在此模式下，如需控制生成图像的数量上限，请使用 <code>max_images</code> 参数。</li></ul></li></ul><p><strong>max_images</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>max_images影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl">模型价格</a>。</p></div></div><p>仅在图文混排模式（即 <code>enable_interleave=true</code>）下生效。</p><ul><li>作用：指定模型在单次回复中生成图像的<strong>最大数量</strong>。</li><li>取值范围：1～5，默认值为 5。</li><li>注意：该参数仅代表“数量上限”。实际生成的图像数量由模型推理决定，可能会少于设定值（例如：设置为 5，模型可能根据内容仅生成 3 张）。</li></ul><p><strong>prompt_extend</strong> <code>bool</code> （可选）</p><p>仅在图像编辑模式（即<code>enable_interleave = false</code>）下生效。</p><p>是否开启 Prompt（提示词）智能改写功能。该功能仅对正向提示词进行优化与润色，不会改变反向提示词。</p><ul><li>true：默认值，开启智能改写。</li><li>false：关闭智能改写，使用原始提示词。</li></ul><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-图像编辑-tab"></a>图像编辑<div><a id="code-code-group-图像编辑"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'X-DashScope-Async: enable' \
--data '{
    &quot;model&quot;: &quot;wan2.6-image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;参考图1的风格和图2的背景，生成番茄炒蛋&quot;
                    },
                    {
                        &quot;image&quot;: &quot;https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png&quot;
                    },
                    {
                        &quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;prompt_extend&quot;: true,
        &quot;watermark&quot;: false,
        &quot;n&quot;: 1,
        &quot;enable_interleave&quot;: false,
        &quot;size&quot;: &quot;1K&quot;
    }
}'
</code></pre></div><a id="fig-code-group-图文混排输出-tab"></a>图文混排输出<div><a id="code-code-group-图文混排输出"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'X-DashScope-Async: enable' \
--data '{
    &quot;model&quot;: &quot;wan2.6-image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;给我一个3张图辣椒炒肉教程&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;max_images&quot;: 3,
        &quot;size&quot;: &quot;1280*1280&quot;,
        &quot;enable_interleave&quot;:true
    }
}'
</code></pre></div></div></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-5"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="420e6e77a17om"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-6"></a>

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

<table><tbody><tr><td><a id="eb9c8d77b6xg8"></a><h4>请求参数</h4><a id="36a28b657f196"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="0e29e015d8opn"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-7"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-9"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b7e833ee1f962"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的图像URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>finished</strong> <code>bool</code></p><p>请求结束标志符。</p><ul><li>true：表示请求结束。</li><li>false：表示请求未结束。</li></ul><p><strong>choices</strong> <code>array of object</code></p><p>模型生成的输出内容。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出的类型，枚举值为text、image。</p><p><strong>text</strong> <code>string</code></p><p>生成的文字。</p><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。</p><p><strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的张数。</p><p><strong>size</strong> <code>string</code></p><p>生成的图像分辨率。示例值：1376*768。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入token数量。按图片张数计费，当前固定为0。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出token数量。按图片张数计费，当前固定为0。</p><p><strong>total_tokens</strong><code>integer</code></p><p>总token数量。按图片张数计费，当前固定为0。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-8"></a><section><a id="任务执行成功-2"></a><section><a id="任务执行成功-2-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-10"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;43d9e959-25bc-4dc7-9888-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;858cad55-4bdc-4ba3-ae6c-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-12-16 04:21:02.275&quot;,
        &quot;scheduled_time&quot;: &quot;2025-12-16 04:21:02.304&quot;,
        &quot;end_time&quot;: &quot;2025-12-16 04:24:46.658&quot;,
        &quot;finished&quot;: true,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1xxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            },
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1xxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;size&quot;: &quot;1376*768&quot;,
        &quot;total_tokens&quot;: 0,
        &quot;image_count&quot;: 2,
        &quot;output_tokens&quot;: 0,
        &quot;input_tokens&quot;: 0
    }
}
</code></pre></section><a id="任务执行异常-2"></a><section><a id="任务执行异常-2-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-11"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="dashscope-python-sdk调用"></a>

<a id="1751252d8bf7c"></a>

## DashScope Python SDK调用

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于任务耗时较长，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**`2.1.0`，再运行以下代码。更新请参考[安装SDK](../../preparations/install-sdk.md)。

各地域的`region`取值和 API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-9"></a>

<a id="华北2-北京-4"></a>

<a id="华北2-北京-4-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

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

<a id="图像编辑-2"></a>

<a id="626b76fc868or"></a>

### 图像编辑

<a id="sec-tabs-10"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="1f90197d8cagy"></a>

##### 请求示例

<a id="code-block-12"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

print("----sync call, please wait a moment----")
job = client.images.generate(
    model='wan2.6-image',
    prompt="参考图1的风格和图2的背景，生成番茄炒蛋",
    # 参考图列表，支持本地文件 如 "file://umbrella1.png"
    image_urls=[
        "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png",
        "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
    ],
    negative_prompt="",
    prompt_extend=True,
    watermark=False,
    n=1,
    parameters={"enable_interleave": False},
    size="1K"
)

print(job)
```

<a id="b0515f126ag6l"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-13"></a>

```json
{
    "request_id": "b6a4c68d-3a91-4018-ae96-3cf373xxxxxx",
    "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
    "status": "SUCCEEDED",
    "choices": [
        {
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                        "type": "image"
                    }
                ]
            }
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "image_count": 1,
        "size": "1376*768",
        "total_tokens": 0
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="7bd0a67abeuuz"></a>

##### 请求示例

<a id="code-block-14"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 创建异步任务
def create_async_task():
    print("Creating async task...")
    job = client.images.jobs.create(
        model="wan2.6-image",
        prompt='参考图1的风格和图2的背景，生成番茄炒蛋',
        # 参考图列表，支持本地文件 如 "file://umbrella1.png"
        image_urls=[
            'https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png',
            'https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp'
        ],
        negative_prompt="",
        prompt_extend=True,
        watermark=False,
        n=1,
        parameters={"enable_interleave": False},
        size="1K"
    )

    print("Task created successfully:", job)
    return job  # 返回任务

# 等待任务完成
def wait_for_completion(task_response):
    print("Waiting for task completion...")
    done = client.images.jobs.wait(task_response)

    if done.succeeded:
        print("Task succeeded!")
        print("Response:", done)
    else:
        raise Exception(f"Task failed with status: {done.status}")

# 获取异步任务信息
def fetch_task_status(task_id):
    print("Fetching task status...")
    snapshot = client.images.jobs.fetch(task_id)

    print("Task status:", snapshot.status)
    print("Response details:", snapshot)

# 取消异步任务
def cancel_task(task_id):
    print("Canceling task...")
    response = client.images.jobs.cancel(task_id)
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

<a id="code-block-15"></a>

```json
{
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-16"></a>

```json
{
    "request_id": "b2a7fab4-5e00-4b0a-86fe-8b9964xxxxxx",
    "task_id": "127ec645-118f-4884-955d-0eba8xxxxxx",
    "status": "SUCCEEDED",
    "choices": [
        {
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                        "type": "image"
                    }
                ]
            }
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "image_count": 1,
        "size": "1376*768",
        "total_tokens": 0
    }
}
```

<a id="图文混合输出"></a>

<a id="a988ae3cdau3e"></a>

### 图文混合输出

<a id="sec-tabs-11"></a>

<a id="同步调用-仅支持流式"></a>

<a id="同步调用-仅支持流式-h4"></a>

#### 同步调用（仅支持流式）

<a id="e677ebd437p7j"></a>

##### 请求示例

<a id="code-block-17"></a>

```python
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sync_call_with_stream():
    print("\n========== 同步调用 - 流式图文输出 ==========")

    stream = client.multimodal.chat.create(
        model="wan2.6-image",
        messages=[
            {
                "role": "user",
                "content": [
                    {"text": "给我一个3张图辣椒炒肉教程"}
                ],
            }
        ],
        stream=True,  # 仅支持流式调用
        # 注意：必须显式传 parameters.stream=True（stream=True 不会自动落到 wire 层），
        # 否则服务端会报错 "stream=False is not supported"
        parameters={
            "stream": True,
            "negative_prompt": "",
            "enable_interleave": True,  # 开启图文混排输出
            "max_images": 3,
            "size": "1280*1280",
        },
    )

    print("流式输出结果:")
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        # 文本增量输出
        if delta.content:
            print(delta.content, end="")
        # 图像增量输出：content_parts 携带含图片URL的 image part
        for part in delta.content_parts or []:
            if part.get("type") == "image":
                print(f"\n[图片] {part['image']}")

if __name__ == "__main__":
    sync_call_with_stream()
```

<a id="95e7baa6180vj"></a>

##### 响应示例（HTTP 接口返回）

> url 有效期24小时，请及时下载图像。 以上为 HTTP 接口返回的流式数据块。

<a id="code-block-18"></a>

```json
{"request_id": "5b98e8f3-aeff-4c20-a26c-499a7525axxx", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": [{"type": "text", "text": "辣椒"}]}}], "audio": null, "finished": false}, "usage": {"input_tokens": 28, "output_tokens": 0, "characters": 0, "total_tokens": 28, "image_count": 0, "size": "0*0"}}
{"request_id": "5b98e8f3-aeff-4c20-a26c-499a7525axxx", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": [{"type": "text", "text": "炒"}]}}], "audio": null, "finished": false}, "usage": {"input_tokens": 28, "output_tokens": 1, "characters": 0, "total_tokens": 29, "image_count": 0, "size": "0*0"}}
{"request_id": "5b98e8f3-aeff-4c20-a26c-499a7525axxx", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": [{"type": "text", "text": "肉"}]}}], "audio": null, "finished": false}, "usage": {"input_tokens": 28, "output_tokens": 2, "characters": 0, "total_tokens": 30, "image_count": 0, "size": "0*0"}}

......

{"request_id": "5b98e8f3-aeff-4c20-a26c-499a7525axxx", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "null", "message": {"role": "assistant", "content": [{"type": "text", "text": "。"}]}}], "audio": null, "finished": false}, "usage": {"input_tokens": 28, "output_tokens": 398, "characters": 0, "total_tokens": 426, "image_count": 2, "size": "1280*1280"}}
{"request_id": "5b98e8f3-aeff-4c20-a26c-499a7525axxx", "output": {"text": null, "finish_reason": null, "choices": [{"finish_reason": "stop", "message": {"role": "assistant", "content": [{"type": "image", "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"}]}}], "audio": null, "finished": true}, "usage": {"input_tokens": 28, "output_tokens": 523, "characters": 0, "total_tokens": 551, "image_count": 3, "size": "1280*1280"}}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

<a id="ef2f7d167d3dx"></a>

##### 请求示例

**注意**：异步调用不需要设置stream参数

<a id="code-block-19"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
client = dashscope.Client(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def main():
    """异步调用 - 图文输出"""
    print("========== wan2.6-image 异步调用 - 图文输出 ==========")

    # 创建异步任务
    print("---async call, creating task----")
    job = client.images.jobs.create(
        model="wan2.6-image",
        prompt="给我一个3张图的辣椒炒肉教程",
        # 异步调用不需要设置stream参数
        negative_prompt="",
        parameters={"enable_interleave": True, "max_images": 3},
        size="1280*1280"
    )

    print(f"任务创建成功:")
    print(job)

    # 等待任务完成
    print("\n---waiting for task completion----")
    done = client.images.jobs.wait(job)

    if done.succeeded:
        print("任务完成!")
        print(f"结果:")
        print(f"图片URL: {done.image_urls}")
    else:
        print(f"任务失败，状态: {done.status}")

if __name__ == "__main__":
    try:
        main()
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
```

<a id="3831331c686e8"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-20"></a>

```json
{
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "task_id": "5c67585e-a3be-4943-b04d-c3fbb2xxxxxx",
    "status": "PENDING"
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-21"></a>

```json
{
    "request_id": "997a759b-fbb9-4b35-9a4d-6dab1xxxxxx",
    "task_id": "5c67585e-a3be-4943-b04d-c3fbb2xxxxxx",
    "status": "SUCCEEDED",
    "choices": [
        {
            "finish_reason": "stop",
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "text": "辣椒炒肉是湘菜中的经典，也是许多人心中的家常美味。它以鲜辣爽口、肉质鲜嫩而闻名，制作过程简单，却能带来极致的味蕾享受。今天，我们就来一起学习这道菜的制作方法。\n\n首先，准备好所有食材是成功的第一步。新鲜的猪肉、红绿辣椒、蒜瓣和姜片是必不可少的。将猪肉切成薄片，辣椒切段，蒜和姜切片备用。",
                        "type": "text"
                    },
                    {
                        "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                        "type": "image"
                    },
                    {
                        "text": "接下来是炒制的关键环节。热锅凉油，放入蒜片和姜片爆香，接着倒入切好的肉片，快速翻炒至肉片变色。肉片炒香后，加入切好的辣椒段，继续翻炒，让辣椒的香气充分释放出来，与肉片的鲜美完美融合。",
                        "type": "text"
                    },
                    {
                        "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                        "type": "image"
                    },
                    {
                        "text": "最后，加入适量的生抽、老抽、蚝油和少许糖调味，快速翻炒均匀，让每一片肉和辣椒都裹上酱汁。待汤汁收浓，即可关火出锅。这道色香味俱全的辣椒炒肉就大功告成了！",
                        "type": "text"
                    },
                    {
                        "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                        "type": "image"
                    }
                ]
            }
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "input_tokens": 29,
        "output_tokens": 477,
        "size": "1280*1280",
        "total_tokens": 506,
        "image_count": 3
    }
}
```

<a id="dashscope-java-sdk调用"></a>

<a id="a5c3e8d7b9xyz"></a>

## DashScope Java SDK调用

SDK 的参数命名与HTTP接口基本一致，参数结构根据语言特性进行封装。

由于任务耗时较长，SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.6`，再运行以下代码。

各地域的`base_url`和 API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-12"></a>

<a id="华北2-北京-5"></a>

<a id="华北2-北京-5-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-5"></a>

<a id="新加坡-5-h4"></a>

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

<a id="图像编辑-2-2"></a>

<a id="a89623b02bahd"></a>

### 图像编辑

<a id="sec-tabs-13"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="d7f8a6b5c9yza"></a>

##### 请求示例

<a id="code-block-22"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.Arrays;
import java.util.Collections;

/**
 * wan2.6-image 图像编辑 - 同步调用示例
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException {
        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "参考图1的风格和图2的背景，生成番茄炒蛋"),
                        Collections.singletonMap("image", "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"),
                        Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp")
                )).build();

        // 图像编辑使用普通同步调用，不需要设置stream和enable_interleave
        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-image")
                .messages(Collections.singletonList(message))
                .n(1)
                .size("1K")
                .negativePrompt("")
                .promptExtend(true)
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---sync call for image editing, please wait a moment----");
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

<a id="b8e9f7a6d5efg"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-23"></a>

```json
{
    "requestId": "b148327e-830f-414c-a8df-724dec28exxx",
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "image_count": 1,
        "size": "1376*768"
    },
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
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="异步调用-3"></a>

<a id="异步调用-3-h4"></a>

#### 异步调用

<a id="b9e8f7d6a5klm"></a>

##### 请求示例

<a id="code-block-24"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.Arrays;
import java.util.Collections;

/**
 * wan2.6-image 图像编辑 - 异步调用示例
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "参考图1的风格和图2的背景，生成番茄炒蛋"),
                        Collections.singletonMap("image", "https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"),
                        Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-image")
                .n(1)
                .size("1K")
                .negativePrompt("")
                .promptExtend(true)
                .messages(Arrays.asList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---async call for image editing, creating task----");
            result = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("任务创建结果:");
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();
        // 等待任务完成
        waitTask(taskId);
    }

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        System.out.println("\n---waiting for task completion----");
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        System.out.println("任务完成结果:");
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

<a id="a8c9f7e6b5pqr"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-25"></a>

```json
{
    "status_code": 200,
    "request_id": "9cd85950-2e26-4b2c-b562-1694cf928xxx",
    "code": "",
    "message": "",
    "output": {
        "task_id": "4c861fbe-af89-4a2f-8fc5-4bb15c313xxx",
        "task_status": "PENDING"
    },
    "usage": null
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-26"></a>

```json
{
    "status_code": 200,
    "request_id": "cbdf1424-306e-4a52-82f3-8bf5d8a99xxx",
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
        "size": "1376*768",
        "total_tokens": 0,
        "image_count": 1
    }
}
```

<a id="图文混合输出-2"></a>

<a id="eecec85d17ql5"></a>

### 图文混合输出

<a id="sec-tabs-14"></a>

<a id="同步调用-仅支持流式-2"></a>

<a id="同步调用-仅支持流式-2-h4"></a>

#### 同步调用（仅支持流式）

<a id="be34d558a0k0l"></a>

##### 请求示例

<a id="code-block-27"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import io.reactivex.Flowable;

import java.util.Collections;

/**
 * wan2.6-image 图文输出 - 流式调用示例
 */
public class Main {

    static {
        // 以下为北京地域url，各地域的base_url不同
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void streamCall() throws ApiException, NoApiKeyException, UploadFileException {
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "给我一个3张图辣椒炒肉教程")
                )).build();

        // 图文输出必须使用流式调用
        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-image")
                .messages(Collections.singletonList(message))
                .stream(true) // 必须开启流式输出
                .enableInterleave(true)
                .size("1280*1280")
                .negativePrompt("")
                .maxImages(3)
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        try {
            System.out.println("---stream call for image interleave----");
            Flowable<ImageGenerationResult> resultFlowable = imageGeneration.streamCall(param);
            resultFlowable.blockingForEach(result -> {
                System.out.println(JsonUtils.toJson(result));
            });
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="55f0d419c4pkv"></a>

##### 响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-28"></a>

```json
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":0,"total_tokens":28,"image_count":0,"size":"0*0"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"辣椒"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":1,"total_tokens":29,"image_count":0,"size":"0*0"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"炒"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":2,"total_tokens":30,"image_count":0,"size":"0*0"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"肉"}]}}],"finished":false},"status_code":200,"code":"","message":""}

......

{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":73,"total_tokens":101,"image_count":0,"size":"0*0"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"。"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":198,"total_tokens":226,"image_count":1,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"image","image":"https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":199,"total_tokens":227,"image_count":1,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"接下来"}]}}],"finished":false},"status_code":200,"code":"","message":""}

......

{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":245,"total_tokens":273,"image_count":1,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"。"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":368,"total_tokens":396,"image_count":2,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"image","image":"https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":369,"total_tokens":397,"image_count":2,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"最后"}]}}],"finished":false},"status_code":200,"code":"","message":""}

......

{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":416,"total_tokens":444,"image_count":2,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"锅"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":417,"total_tokens":445,"image_count":2,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":[{"type":"text","text":"。"}]}}],"finished":false},"status_code":200,"code":"","message":""}
{"requestId":"12c7432c-8028-4289-a97c-4e22df98bxxx","usage":{"input_tokens":28,"output_tokens":541,"total_tokens":569,"image_count":3,"size":"1280*1280"},"output":{"choices":[{"finish_reason":"stop","message":{"role":"assistant","content":[{"type":"image","image":"https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"}]}}],"finished":true},"status_code":200,"code":"","message":""}
```

<a id="异步调用-4"></a>

<a id="异步调用-4-h4"></a>

#### 异步调用

<a id="31bd2b2db4s5m"></a>

##### 请求示例

**注意**：异步调用不需要设置stream参数

<a id="code-block-29"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.util.Collections;

/**
 * wan2.6-image 图文输出 - 异步调用示例
 */
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
                        Collections.singletonMap("text", "给我一个3张图的辣椒炒肉教程")
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-image")
                .size("1280*1280")
                .enableInterleave(true)
                .maxImages(3)
                .negativePrompt("")
                .messages(Collections.singletonList(message))
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---async call for image interleave, creating task----");
            result = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("任务创建结果:");
        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();
        // 等待任务完成
        waitTask(taskId);
    }

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        System.out.println("\n---waiting for task completion----");
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        System.out.println("任务完成结果:");
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

<a id="f8468ee4c3kwp"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-30"></a>

```json
{
    "requestId": "7d6c5760-334b-48c4-9b1e-08ee9c7fexxx",
    "output": {
        "task_id": "1bb9d9fa-bf1a-43dc-b5fe-366c1dc70xxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> url 有效期24小时，请及时下载图像。

<a id="code-block-31"></a>

```json
{
    "requestId": "6ed62b00-2225-4fc3-8ee3-2aed0b484xxx",
    "usage": {
        "input_tokens": 29,
        "output_tokens": 471,
        "total_tokens": 500,
        "image_count": 3,
        "size": "1280*1280"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "text": "辣椒炒肉是湘菜中的经典，也是许多人心中的家常美味。它以鲜辣爽口、肉质鲜嫩而闻名，制作过程简单，却能带来极致的味蕾享受。今天，我们就来一起学习这道菜的制作方法。\n\n首先，准备好所有食材是成功的第一步。新鲜的猪肉、红绿辣椒、蒜瓣和姜片是必不可少的。将猪肉切成薄片，辣椒切段，蒜和姜切片备用。",
                            "type": "text"
                        },
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        },
                        {
                            "text": "接下来是腌制猪肉。将切好的猪肉片放入碗中，加入少许生抽、料酒、淀粉和食用油，用手抓匀，腌制10-15分钟。这样处理过的肉片会更加滑嫩入味。",
                            "type": "text"
                        },
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        },
                        {
                            "text": "最后，热锅凉油，放入腌制好的肉片快速滑炒至变色，盛出备用。锅中留底油，放入蒜片和姜片爆香，再加入辣椒段翻炒出香味。随后倒入肉片，加入生抽、老抽、少许糖和蚝油，快速翻炒均匀，撒上葱花即可出锅。",
                            "type": "text"
                        },
                        {
                            "image": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "1bb9d9fa-bf1a-43dc-b5fe-366c1dc70836",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-01-16 18:26:32.082",
        "scheduled_time": "2026-01-16 18:26:32.133",
        "end_time": "2026-01-16 18:28:41.748"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="使用限制"></a>

<a id="20263d27eeksq"></a>

## 使用限制

-   **数据时效**：任务`task_id`和 图像`url`均只保留 24 小时，过期后将无法查询或下载。
-   **内容审核**：输入的 `prompt` 和输出的图像均会经过内容安全审核，包含违规内容的请求将报错“IPInfringementSuspect”或“DataInspectionFailed”，具体参见[错误码](../../preparations/error-code.md)。

<a id="计费与限流"></a>

<a id="5dafefe82bgrh"></a>

## 计费与限流

-   模型免费额度和计费单价请参见[模型价格](../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl)。
-   模型限流请参见[万相](../../../model-user-guide/get-started-with-models/rate-limit.md#513e0a3df24v7)。
-   计费说明：按成功生成的 **图像张数** 计费。模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](../../../model-user-guide/test-1/new-free-quota.md)。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="ed3bed65cdp1s"></a>

## 常见问题

**Q：为什么代码示例无法调用？**

A：请升级您的SDK版本到最新版，更新请参考[安装SDK](../../preparations/install-sdk.md)。
