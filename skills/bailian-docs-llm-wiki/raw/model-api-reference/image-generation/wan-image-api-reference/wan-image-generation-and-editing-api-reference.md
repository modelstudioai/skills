# 万相-图像生成与编辑2.7 API参考

万相2.7图像生成与编辑模型支持文生图、文生组图、图生组图、图像编辑和多图参考生成。

<a id="模型概览"></a>

<a id="753cf1c4316ie"></a>

## 模型概览

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>模型简介</strong></p></th><th><p><strong>输出图像规格</strong></p></th></tr></thead><tbody><tr><td><p>wan2.7-image-pro</p></td><td><p>万相2.7 image专业版，文生图（非组图生成）支持4K高清输出</p></td><td rowspan="2"><p>图片格式：PNG。</p><p>图像分辨率和尺寸请参见<a href="wan-image-generation-and-editing-api-reference.md">size参数</a>。</p></td></tr><tr><td><p>wan2.7-image</p></td><td><p>万相2.7 image，生成速度更快</p></td></tr></tbody></table>

> **说明**
>
> 调用前，请查阅各地域支持的[模型列表与价格](../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl)。

<a id="前提条件"></a>

<a id="0e41425c577u4"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

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

<a id="http同步调用"></a>

<a id="wan27-sync-title"></a>

## HTTP同步调用

一次请求即可获得结果，流程简单，推荐大多数场景使用。

<a id="sec-tabs"></a>

<a id="北京"></a>

<a id="北京-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="wan27-h4-params"></a><h4>请求参数</h4></td><td rowspan="8"><a id="sec-tabs-2"></a><section><a id="文生图"></a><section><a id="文生图-h4"></a><h4>文生图</h4><blockquote><p>wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率</p></blockquote><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;text&quot;: &quot;一间有着精致窗户的花店，漂亮的木质门，摆放着花朵&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;2K&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false,
        &quot;thinking_mode&quot;: true
    }
}'
</code></pre></section><a id="图像编辑"></a><section><a id="图像编辑-h4"></a><h4>图像编辑</h4><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp&quot;},
                    {&quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp&quot;},
                    {&quot;text&quot;: &quot;把图2的涂鸦喷绘在图1的汽车上&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;2K&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="交互式编辑"></a><section><a id="交互式编辑-h4"></a><h4>交互式编辑</h4><a id="code-block-3"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp&quot;},
                    {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp&quot;},
                    {&quot;text&quot;: &quot;把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;bbox_list&quot;: [[],[[989, 515, 1138, 681]]],
        &quot;size&quot;: &quot;2K&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="组图生成"></a><section><a id="组图生成-h4"></a><h4>组图生成</h4><blockquote><p>wan2.7-image-pro组图生成仅支持最高2K分辨率。</p></blockquote><a id="code-block-4"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;text&quot;: &quot;电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;enable_sequential&quot;: true,
        &quot;n&quot;: 4,
        &quot;size&quot;: &quot;2K&quot;
    }
}'
</code></pre></section></section></td></tr><tr><td><a id="wan27-h5-headers"></a><h5>请求头（Headers）</h5></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p></td></tr><tr><td><a id="wan27-h5-body"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值：<code>wan2.7-image-pro</code>、<code>wan2.7-image</code>。</p></td></tr><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数固定设置为<code>user</code>。</p><p><strong>content</strong> <code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code></p><p>用户输入提示词。支持中英文，长度不超过5000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p><strong>image</strong> <code>string</code></p><p>输入图像的URL或Base64编码字符串。</p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽高范围均为[240, 8000]像素，宽高比范围[1:8, 8:1]。</li><li>文件大小：不超过20MB。</li></ul><p>图像数量限制：</p><ul><li>可传入0-9张图片。</li><li>当输入多张图像时，需在<code>content</code>数组中传入多个<code>image</code>对象，并按照数组顺序定义图像顺序。</li></ul><p>支持的输入格式：</p><ol><li><p>使用公网可访问URL</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<code>http://wanx.alicdn.com/material/xxx.jpeg</code>。</li></ul></li><li><p>传入 Base64 编码图像后的字符串</p><ul><li>格式：data:{MIME_type};base64,{base64_data}</li><li>示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）</li><li>Base64 编码规范请参见<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/wan-image-edit.md#8db0e2215frua">图像传入方式</a>。</li></ul></li></ol></div></section></div></section></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> （可选）</p><p>模型参数配置。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>bbox_list</strong> <code>array[array[array[integer]]]</code> （可选）</p><p>交互式编辑框选区域。</p><ul><li>对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，请在对应位置传入空列表 <code>[]</code>。</li><li>坐标格式：<code>[x1, y1, x2, y2]</code>（左上角 x, 左上角 y, 右下角 x, 右下角 y），使用原图绝对像素坐标，左上角坐标为（0，0）。</li><li>限制条件：单张图片最多支持 2 个边界框。</li></ul><p>示例：输入 3 张图片，其中第 2 张无框选，第 1 张有两个框选：</p><a id="code-block-5"></a><pre class="language-json"><code>[
  [[0, 0, 12, 12], [25, 25, 100, 100]],  # 图 1 (2个框)
  [],                                    # 图 2 (无框)
  [[10, 10, 50, 50]]                    # 图 3 (1个框)
]
</code></pre><p><strong>enable_sequential</strong> <code>boolean</code> （可选）</p><p>控制生图模式：</p><ul><li>false：默认值。</li><li>true ：启用组图输出模式。</li></ul><p><strong>size</strong> <code>string</code> （可选）</p><p>关于输出图片分辨率参数，支持以下两种方式，不可混用：</p><strong>模型：wan2.7-image-pro</strong><ul><li><strong>方式一：指定输出图片的分辨率（推荐）</strong><ul><li><p>支持 1K、2K（默认）、4K 三种规格</p></li><li><p><strong>适用范围</strong>：</p><ul><li>文生图（无图片输入，非组图生成）：支持1K、2K、4K。</li><li>其他场景：支持1K、2K。</li></ul></li><li><p><strong>各规格总像素</strong>：1K：1024<em>1024、2K：2048</em>2048、4K：4096*4096</p></li><li><p><strong>图像比例</strong>：</p><ul><li>当有图片输入时：输出宽高比与输入图像（多图输入时为最后一张）一致，并缩放到选定分辨率。</li><li>当没有图片输入时：输出为正方形。</li></ul></li></ul></li><li><strong>方式二：指定生成图像的宽高像素值</strong><ul><li>文生图：总像素在 [768<em>768, 4096</em>4096] 之间，宽高比范围为 [1:8, 8:1]。</li><li>其他场景：总像素在 [768<em>768, 2048</em>2048] 之间，宽高比范围为 [1:8, 8:1]。</li></ul></li></ul><strong>模型：wan2.7-image</strong><ul><li><strong>方式一：指定输出图片的分辨率（推荐）</strong><ul><li>支持1K、2K（默认）两种规格，不支持4K。</li></ul></li><li><strong>方式二：指定生成图像的宽高像素值</strong><ul><li>所有场景下，总像素在 [768<em>768, 2048</em>2048] 之间，宽高比范围为 [1:8, 8:1]。</li></ul></li></ul><blockquote><p>输出图片的像素值可能和指定像素值存在微小差异。</p></blockquote><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl">模型价格</a>。</p></div></div><ul><li>关闭组图模式时，该数值代表生成图像数量，取值范围 1-4，<strong>默认为 1</strong>；</li><li>开启组图模式时，该数值代表最大生成图像数量，取值范围 1-12，<strong>默认为 12</strong>。实际数量由模型决定且不超过 n。</li></ul><p><strong>thinking_mode</strong> <code>boolean</code> （可选）</p><p>是否开启思考模式，默认为<code>true</code>（开启）。仅在关闭组图模式且无图片输入时生效。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。</p><p><strong>color_palette</strong> <code>array</code> （可选）</p><p>自定义颜色主题，一个包含颜色（hex）和占比（ratio）的对象数组，需要包含 3 至 10 种颜色，推荐设置为 8 种。</p><p>仅当关闭组图模式（<code>enable_sequential=false</code>）时可用。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>hex</strong> <code>string</code> <strong>（必选）</strong></p><p>十六进制（HEX）格式的色值。</p><p><strong>ratio</strong> <code>string</code> <strong>（必选）</strong></p><p>颜色所占的百分比，需精确到小数点后两位（如<code>&quot;25.00%&quot;</code>）。所有 ratio 值相加<strong>总和必须为 100.00%</strong>。</p></div></section><a id="accordion-点击查看输入示例"></a><section><p>点击查看输入示例</p><div><a id="code-block-6"></a><pre class="language-json"><code>&quot;color_palette&quot;: [
    {
        &quot;hex&quot;: &quot;#C2D1E6&quot;,
        &quot;ratio&quot;: &quot;23.51%&quot;
    },
    {
        &quot;hex&quot;: &quot;#CDD8E9&quot;,
        &quot;ratio&quot;: &quot;20.13%&quot;
    },
    {
        &quot;hex&quot;: &quot;#B5C8DB&quot;,
        &quot;ratio&quot;: &quot;15.88%&quot;
    },
    {
        &quot;hex&quot;: &quot;#C0B5B4&quot;,
        &quot;ratio&quot;: &quot;13.27%&quot;
    },
    {
        &quot;hex&quot;: &quot;#DAE0EC&quot;,
        &quot;ratio&quot;: &quot;10.11%&quot;
    },
    {
        &quot;hex&quot;: &quot;#636574&quot;,
        &quot;ratio&quot;: &quot;8.93%&quot;
    },
    {
        &quot;hex&quot;: &quot;#CACAD2&quot;,
        &quot;ratio&quot;: &quot;5.55%&quot;
    },
    {
        &quot;hex&quot;: &quot;#CBD4E4&quot;,
        &quot;ratio&quot;: &quot;2.62%&quot;
    }
]
</code></pre></div></section><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="0ef7966fee5nl"></a><h4>响应参数</h4></td><td rowspan="4"><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx&quot;,
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
        &quot;input_tokens&quot;: 10867,
        &quot;output_tokens&quot;: 2,
        &quot;size&quot;: &quot;1488*704&quot;,
        &quot;total_tokens&quot;: 10869
    },
    &quot;request_id&quot;: &quot;71dfc3c6-f796-9972-97e4-bc4efc4faxxx&quot;
}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr><tr><td><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因。自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出的类型，固定为image。</p><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。</p><p><strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section><p><strong>finished</strong> <code>boolean</code></p><p>任务是否结束。</p><ul><li>true：已结束。</li><li>false：未结束。</li></ul></div></section></td></tr><tr><td><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的张数。</p><p><strong>size</strong> <code>string</code></p><p>生成的图像分辨率。示例值：1376*768。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入token数量（不计费）。按图片张数计费。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出token数量（不计费）。按图片张数计费。</p><p><strong>total_tokens</strong><code>integer</code></p><p>总token数量（不计费）。按图片张数计费。</p></div></section></td></tr><tr><td><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td></tr><tr><td><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td></td></tr><tr><td><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td></td></tr></tbody></table>

<a id="http异步调用"></a>

<a id="wan27-async-title"></a>

## HTTP异步调用

适用于耗时较长的任务，支持查询任务状态和结果。

<a id="步骤1-创建任务获取任务id"></a>

<a id="wan27-async-step1-title"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs-4"></a>

<a id="北京-2"></a>

<a id="北京-2-h4"></a>

#### 北京

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="wan27-async-h4-params"></a><h4>请求参数</h4></td><td rowspan="9"><a id="sec-tabs-5"></a><section><a id="文生图-2"></a><section><a id="文生图-2-h4"></a><h4>文生图</h4><blockquote><p>wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率</p></blockquote><a id="code-block-9"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;X-DashScope-Async: enable&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;text&quot;: &quot;一间有着精致窗户的花店，漂亮的木质门，摆放着花朵&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;2K&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false,
        &quot;thinking_mode&quot;: true
    }
}'
</code></pre></section><a id="图像编辑-2"></a><section><a id="图像编辑-2-h4"></a><h4>图像编辑</h4><a id="code-block-10"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;X-DashScope-Async: enable&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp&quot;},
                    {&quot;image&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp&quot;},
                    {&quot;text&quot;: &quot;把图2的涂鸦喷绘在图1的汽车上&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;2K&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="交互式编辑-2"></a><section><a id="交互式编辑-2-h4"></a><h4>交互式编辑</h4><a id="code-block-11"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;X-DashScope-Async: enable&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp&quot;},
                    {&quot;image&quot;: &quot;https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp&quot;},
                    {&quot;text&quot;: &quot;把图1的闹钟放在图2的框选的位置，保持场景和光线融合自然&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;bbox_list&quot;: [[],[[989, 515, 1138, 681]]],
        &quot;size&quot;: &quot;2K&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="组图生成-2"></a><section><a id="组图生成-2-h4"></a><h4>组图生成</h4><blockquote><p>wan2.7-image-pro组图生成仅支持最高2K分辨率。</p></blockquote><a id="code-block-12"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'Content-Type: application/json' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header &quot;X-DashScope-Async: enable&quot; \
--data '{
    &quot;model&quot;: &quot;wan2.7-image-pro&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {&quot;text&quot;: &quot;电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。&quot;}
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;enable_sequential&quot;: true,
        &quot;n&quot;: 4,
        &quot;size&quot;: &quot;2K&quot;
    }
}'
</code></pre></section></section></td></tr><tr><td><a id="wan27-async-h5-headers"></a><h5>请求头（Headers）</h5></td></tr><tr><td><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p></td></tr><tr><td><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p></td></tr><tr><td><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div></td></tr><tr><td><a id="wan27-async-h5-body"></a><h5>请求体（Request Body）</h5></td></tr><tr><td><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值：<code>wan2.7-image-pro</code>、<code>wan2.7-image</code>。</p></td></tr><tr><td><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。当前<strong>仅支持单轮对话</strong>，即传入一组role、content参数，不支持多轮对话。</p><a id="accordion-属性-12"></a><section><p>属性</p><div><p><strong>role</strong> <code>string</code> <strong>（必选）</strong></p><p>消息的角色。此参数固定设置为<code>user</code>。</p><p><strong>content</strong> <code>array</code> <strong>（必选）</strong></p><p>消息内容数组。</p><a id="accordion-属性-13"></a><section><p>属性</p><div><p><strong>text</strong> <code>string</code></p><p>用户输入提示词。支持中英文，长度不超过5000个字符，每个汉字、字母、数字或符号计为一个字符，超过部分会自动截断。</p><p><strong>image</strong> <code>string</code></p><p>输入图像的URL或Base64编码字符串。</p><p>图像限制：</p><ul><li>图像格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。</li><li>图像分辨率：图像的宽高范围均为[240, 8000]像素，宽高比范围[1:8, 8:1]。</li><li>文件大小：不超过20MB。</li></ul><p>图像数量限制：</p><ul><li>可传入0-9张图片。</li><li>当输入多张图像时，需在<code>content</code>数组中传入多个<code>image</code>对象，并按照数组顺序定义图像顺序。</li></ul><p>支持的输入格式：</p><ol><li><p>使用公网可访问URL</p><ul><li>支持HTTP或HTTPS协议。</li><li>示例值：<code>http://wanx.alicdn.com/material/xxx.jpeg</code>。</li></ul></li><li><p>传入 Base64 编码图像后的字符串</p><ul><li>格式：data:{MIME_type};base64,{base64_data}</li><li>示例：data:image/jpeg;base64,GDU7MtCZzEbTbmRZ...（仅示意，实际需传入完整字符串）</li><li>Base64 编码规范请参见<a href="../../../model-user-guide/model-experience/image-and-video-generation/image-model/image-edit-guide/wan-image-edit.md#8db0e2215frua">图像传入方式</a>。</li></ul></li></ol></div></section></div></section></div></section></td></tr><tr><td><p><strong>parameters</strong> <code>object</code> （可选）</p><p>模型参数配置。</p><a id="accordion-属性-14"></a><section><p>属性</p><div><p><strong>bbox_list</strong> <code>array[array[array[integer]]]</code> （可选）</p><p>交互式编辑框选区域。</p><ul><li>对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，请在对应位置传入空列表 <code>[]</code>。</li><li>坐标格式：<code>[x1, y1, x2, y2]</code>（左上角 x, 左上角 y, 右下角 x, 右下角 y），使用原图绝对像素坐标，左上角坐标为（0，0）。</li><li>限制条件：单张图片最多支持 2 个边界框。</li></ul><p>示例：输入 3 张图片，其中第 2 张无框选，第 1 张有两个框选：</p><a id="code-block-13"></a><pre class="language-json"><code>[
  [[0, 0, 12, 12], [25, 25, 100, 100]],  # 图 1 (2个框)
  [],                                    # 图 2 (无框)
  [[10, 10, 50, 50]]                    # 图 3 (1个框)
]
</code></pre><p><strong>enable_sequential</strong> <code>boolean</code> （可选）</p><p>控制生图模式：</p><ul><li>false：默认值。</li><li>true ：启用组图输出模式。</li></ul><p><strong>size</strong> <code>string</code> （可选）</p><p>关于输出图片分辨率参数，支持以下两种方式，不可混用：</p><strong>模型：wan2.7-image-pro</strong><ul><li><strong>方式一：指定输出图片的分辨率（推荐）</strong><ul><li><p>支持 1K、2K（默认）、4K 三种规格</p></li><li><p><strong>适用范围</strong>：</p><ul><li>文生图（无图片输入，非组图生成）：支持1K、2K、4K。</li><li>其他场景：支持1K、2K。</li></ul></li><li><p><strong>各规格总像素</strong>：1K：1024<em>1024、2K：2048</em>2048、4K：4096*4096</p></li><li><p><strong>图像比例</strong>：</p><ul><li>当有图片输入时：输出宽高比与输入图像（多图输入时为最后一张）一致，并缩放到选定分辨率。</li><li>当没有图片输入时：输出为正方形。</li></ul></li></ul></li><li><strong>方式二：指定生成图像的宽高像素值</strong><ul><li>文生图：总像素在 [768<em>768, 4096</em>4096] 之间，宽高比范围为 [1:8, 8:1]。</li><li>其他场景：总像素在 [768<em>768, 2048</em>2048] 之间，宽高比范围为 [1:8, 8:1]。</li></ul></li></ul><strong>模型：wan2.7-image</strong><ul><li><strong>方式一：指定输出图片的分辨率（推荐）</strong><ul><li>支持1K、2K（默认）两种规格，不支持4K。</li></ul></li><li><strong>方式二：指定生成图像的宽高像素值</strong><ul><li>所有场景下，总像素在 [768<em>768, 2048</em>2048] 之间，宽高比范围为 [1:8, 8:1]。</li></ul></li></ul><blockquote><p>输出图片的像素值可能和指定像素值存在微小差异。</p></blockquote><p><strong>n</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>n直接影响费用。费用 = 单价 × 成功生成的图片张数，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e2540d71a2utl">模型价格</a>。</p></div></div><ul><li>关闭组图模式时，该数值代表生成图像数量，取值范围 1-4，<strong>默认为 1</strong>；</li><li>开启组图模式时，该数值代表最大生成图像数量，取值范围 1-12，<strong>默认为 12</strong>。实际数量由模型决定且不超过 n。</li></ul><p><strong>thinking_mode</strong> <code>boolean</code> （可选）</p><p>是否开启思考模式，默认为<code>true</code>（开启）。仅在关闭组图模式且无图片输入时生效。开启时，模型将增强推理能力以提升出图质量，但会增加生成耗时。</p><p><strong>color_palette</strong> <code>array</code> （可选）</p><p>自定义颜色主题，一个包含颜色（hex）和占比（ratio）的对象数组，需要包含 3 至 10 种颜色，推荐设置为 8 种。</p><p>仅当关闭组图模式（<code>enable_sequential=false</code>）时可用。</p><a id="accordion-属性-15"></a><section><p>属性</p><div><p><strong>hex</strong> <code>string</code> <strong>（必选）</strong></p><p>十六进制（HEX）格式的色值。</p><p><strong>ratio</strong> <code>string</code> <strong>（必选）</strong></p><p>颜色所占的百分比，需精确到小数点后两位（如<code>&quot;25.00%&quot;</code>）。所有 ratio 值相加<strong>总和必须为 100.00%</strong>。</p></div></section><a id="accordion-点击查看输入示例-2"></a><section><p>点击查看输入示例</p><div><a id="code-block-14"></a><pre class="language-json"><code>&quot;color_palette&quot;: [
    {
        &quot;hex&quot;: &quot;#C2D1E6&quot;,
        &quot;ratio&quot;: &quot;23.51%&quot;
    },
    {
        &quot;hex&quot;: &quot;#CDD8E9&quot;,
        &quot;ratio&quot;: &quot;20.13%&quot;
    },
    {
        &quot;hex&quot;: &quot;#B5C8DB&quot;,
        &quot;ratio&quot;: &quot;15.88%&quot;
    },
    {
        &quot;hex&quot;: &quot;#C0B5B4&quot;,
        &quot;ratio&quot;: &quot;13.27%&quot;
    },
    {
        &quot;hex&quot;: &quot;#DAE0EC&quot;,
        &quot;ratio&quot;: &quot;10.11%&quot;
    },
    {
        &quot;hex&quot;: &quot;#636574&quot;,
        &quot;ratio&quot;: &quot;8.93%&quot;
    },
    {
        &quot;hex&quot;: &quot;#CACAD2&quot;,
        &quot;ratio&quot;: &quot;5.55%&quot;
    },
    {
        &quot;hex&quot;: &quot;#CBD4E4&quot;,
        &quot;ratio&quot;: &quot;2.62%&quot;
    }
]
</code></pre></div></section><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识，水印位于图片右下角，文案固定为“AI生成”。</p><ul><li>false：默认值，不添加水印。</li><li>true：添加水印。</li></ul><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p><strong>注意</strong>：模型生成过程具有概率性，即使使用相同的<code>seed</code>，也不能保证每次生成结果完全一致。</p></div></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应参数</h4></td><td rowspan="3"><a id="sec-tabs-6"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-15"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-16"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr><tr><td><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-16"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section></td></tr><tr><td><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td></tr><tr><td><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td></td></tr><tr><td><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="wan27-async-step2-title"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-7"></a>

<a id="北京-3"></a>

<a id="北京-3-h4"></a>

#### 北京

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="新加坡-3"></a>

<a id="新加坡-3-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<table><tbody><tr><td><a id="153278ecd2pkr"></a><h4>请求参数</h4></td><td rowspan="5"><a id="sec-tabs-8"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-17"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr><tr><td><a id="9c498abd774f2"></a><h5>请求头（Headers）</h5></td></tr><tr><td><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p></td></tr><tr><td><a id="5af2d40d88y8w"></a><h5>URL路径参数（Path parameters）</h5></td></tr><tr><td><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td></tr></tbody></table>

<table><tbody><tr><td><a id="bb05ff3e1blpf"></a><h4>响应参数</h4></td><td rowspan="6"><a id="sec-tabs-9"></a><section><a id="任务执行成功-2"></a><section><a id="任务执行成功-2-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-18"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;810fa5f5-334c-91f3-aaa4-ed89cf0caxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;a81ee7cb-014c-473d-b842-76e98311cxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-26 17:16:01.663&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-26 17:16:01.716&quot;,
        &quot;end_time&quot;: &quot;2026-03-26 17:16:22.961&quot;,
        &quot;finished&quot;: true,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;size&quot;: &quot;2976*1408&quot;,
        &quot;total_tokens&quot;: 11017,
        &quot;image_count&quot;: 1,
        &quot;output_tokens&quot;: 2,
        &quot;input_tokens&quot;: 11015
    }
}
</code></pre></section><a id="任务执行异常-2"></a><section><a id="任务执行异常-2-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-19"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr><tr><td><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-17"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的图像URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>finished</strong> <code>boolean</code></p><p>任务是否结束。</p><ul><li>true：已结束。</li><li>false：未结束。</li></ul><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。</p><a id="accordion-属性-18"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-19"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-20"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出的类型，枚举值为text、image。</p><p><strong>text</strong> <code>string</code></p><p>生成的文字。</p><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。</p><p><strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section></div></section></td></tr><tr><td><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-21"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的张数。</p><p><strong>size</strong> <code>string</code></p><p>生成的图像分辨率。示例值：1376*768。</p><p><strong>input_tokens</strong> <code>integer</code></p><p>输入token数量（不计费）。按图片张数计费。</p><p><strong>output_tokens</strong> <code>integer</code></p><p>输出token数量（不计费）。按图片张数计费。</p><p><strong>total_tokens</strong><code>integer</code></p><p>总token数量（不计费）。按图片张数计费。</p></div></section></td></tr><tr><td><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td></tr><tr><td><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td></tr><tr><td><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td></tr></tbody></table>

<a id="python-sdk调用"></a>

<a id="1751252d8bf7c"></a>

## Python SDK调用

SDK 参数命名与HTTP接口基本一致。

任务可能耗时较长，SDK 已封装HTTP异步调用流程，同时支持同步和异步调用。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

> **重要**
>
> 请确保 DashScope Python SDK版本**不低于 2.1.0**，再运行以下代码。更新请参考[安装SDK](../../preparations/install-sdk.md)。

各地域的`base_url`和API Key 不通用，以下示例以北京地域为例进行调用：

<a id="sec-tabs-10"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-4"></a>

<a id="新加坡-4-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="图像编辑-3"></a>

<a id="626b76fc868or"></a>

### 图像编辑

<a id="sec-tabs-11"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="1f90197d8cagy"></a>

##### 请求示例

<a id="code-block-20"></a>

```python
import os
import base64
import mimetypes
import urllib.request
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/car.png"
# image_2 = "file:///path/to/your/paint.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/car.png")
# image_2 = encode_file("/path/to/your/paint.png")

print("----sync call, please wait a moment----")
# generate 为一步式调用（提交+等待），直接返回已完成的任务结果
job = client.images.generate(
    model="wan2.7-image-pro",
    prompt="把图2的涂鸦喷绘在图1的汽车上",
    # 参考图列表，支持本地文件 如 "file:///path/to/your/car.png"
    image_urls=[image_1, image_2],
    watermark=False,
    n=1,
    size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
)

# 提取结果图片URL并保存到本地
for i, image_url in enumerate(job.image_urls):
    file_name = f"output_{i}.png"
    # 结果URL有效期为24小时，请及时下载
    urllib.request.urlretrieve(image_url, file_name)
    print(f"Image saved to {file_name}")
```

<a id="b0515f126ag6l"></a>

##### 响应示例

> URL 有效期24小时，请及时下载图像。

<a id="code-block-21"></a>

```json
{
    "status_code": 200,
    "request_id": "81d868c6-6ce1-92d8-a90d-d2ee71xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
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
        "audio": null,
        "finished": true
    },
    "usage": {
        "input_tokens": 18790,
        "output_tokens": 2,
        "characters": 0,
        "image_count": 1,
        "size": "2985*1405",
        "total_tokens": 18792
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="7bd0a67abeuuz"></a>

##### 请求示例

<a id="code-block-22"></a>

```python
import os
import base64
import mimetypes
import urllib.request
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/car.png"
# image_2 = "file:///path/to/your/paint.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/car.png")
# image_2 = encode_file("/path/to/your/paint.png")

# 创建异步任务
def create_async_task():
    print("Creating async task...")
    job = client.images.jobs.create(
        model="wan2.7-image-pro",
        prompt="把图2的涂鸦喷绘在图1的汽车上",
        extra_input={'images': [image_1, image_2]},
        watermark=False,
        n=1,
        size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
    )

    print("Task created successfully:", job.task_id, job.status)
    return job

# 等待任务完成（指数退避轮询，默认总预算24小时；任务失败会抛出DashScopeError）
def wait_for_completion(job):
    print("Waiting for task completion...")
    done = client.images.jobs.wait(job)

    print("Task succeeded!")
    # 提取结果图片URL并保存到本地
    for i, image_url in enumerate(done.image_urls):
        file_name = f"output_{i}.png"
        # 结果URL有效期为24小时，请及时下载
        urllib.request.urlretrieve(image_url, file_name)
        print(f"Image saved to {file_name}")

# 获取异步任务信息
def fetch_task_status(task_id):
    print("Fetching task status...")
    snapshot = client.images.jobs.fetch(task_id)

    print("Task status:", snapshot.status)

# 取消异步任务，只有处于PENDING状态的任务才可以取消
def cancel_task(task_id):
    print("Canceling task...")
    client.images.jobs.cancel(task_id)

# 主执行流程
if __name__ == "__main__":
    job = create_async_task()
    wait_for_completion(job)
```

<a id="d5de68e40618u"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-23"></a>

```json
{
    "status_code": 200,
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
        "task_status": "PENDING"
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0
    }
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载图像。

<a id="code-block-24"></a>

```json
{
    "status_code": 200,
    "request_id": "3b99aae5-d26f-9059-8dd0-ee9ca4804xxx",
    "code": null,
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
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
        "audio": null,
        "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-31 22:58:47.646",
        "scheduled_time": "2026-03-31 22:58:47.683",
        "end_time": "2026-03-31 22:58:59.642",
        "finished": true
    },
    "usage": {
        "input_tokens": 18711,
        "output_tokens": 2,
        "characters": 0,
        "size": "2985*1405",
        "total_tokens": 18713,
        "image_count": 1
    }
}
```

<a id="组图生成-3"></a>

<a id="wan27-sequential-python-title"></a>

### 组图生成

<a id="sec-tabs-12"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="wan27-sequential-sync-request-title"></a>

##### 请求示例

<a id="code-block-25"></a>

```python
import os
import base64
import mimetypes
import urllib.request
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明（图生组图场景）：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
# image_1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/image.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/image.png")

print("----sync call, please wait a moment----")
# generate 为一步式调用（提交+等待），直接返回已完成的任务结果
job = client.images.generate(
    model="wan2.7-image-pro",
    prompt="电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。",
    # 图生组图场景：取消以下注释，传入参考图（并将上方提示词改为参考图片风格生成四季组图）
    # image_urls=[image_1],
    parameters={"enable_sequential": True},  # 组图生成
    n=4,
    size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
)

# 提取结果图片URL并保存到本地
for i, image_url in enumerate(job.image_urls):
    file_name = f"output_{i}.png"
    # 结果URL有效期为24小时，请及时下载
    urllib.request.urlretrieve(image_url, file_name)
    print(f"Image saved to {file_name}")
```

<a id="wan27-sequential-sync-response-title"></a>

##### 响应示例

> URL 有效期24小时，请及时下载图像。

<a id="code-block-26"></a>

```json
{
    "status_code": 200,
    "request_id": "56e318fd-ed60-99e8-8ca1-cdef25ca4xxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "finished": true
    },
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "characters": 0,
        "image_count": 4,
        "size": "2048*2048",
        "total_tokens": 731
    }
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

<a id="wan27-sequential-async-request-title"></a>

##### 请求示例

<a id="code-block-27"></a>

```python
import os
import base64
import mimetypes
import urllib.request
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# --- Base64编码函数 ---
# base64编码格式为 data:{MIME_type};base64,{base64_data}
def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded_string}"

"""
图像输入方式说明（图生组图场景）：
以下提供了三种图片输入方式，三选一即可
1. 使用公网URL - 适合已有公开可访问的图片
2. 使用本地文件 - 适合本地开发测试
3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
"""
# 【方式一】使用公网图片 URL
# image_1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp"

# 【方式二】使用本地文件（支持绝对路径和相对路径）
# image_1 = "file:///path/to/your/image.png"

# 【方式三】使用Base64编码的图片
# image_1 = encode_file("/path/to/your/image.png")

def main():
    # 提交异步任务
    print("提交异步任务...")
    job = client.images.jobs.create(
        model="wan2.7-image-pro",
        prompt="电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。",
        # 图生组图场景：取消以下注释，传入参考图（并将上方提示词改为参考图片风格生成四季组图）
        # extra_input={'images': [image_1]},
        parameters={"enable_sequential": True},  # 组图生成
        n=4,
        size="2K",  # wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
    )
    print(f"任务提交成功，任务ID: {job.task_id}")

    # 等待任务完成（指数退避轮询，默认总预算24小时；任务失败会抛出DashScopeError）
    done = client.images.jobs.wait(job)

    if done.succeeded:
        print("任务完成!")
        # 提取结果图片URL并保存到本地
        for i, image_url in enumerate(done.image_urls):
            file_name = f"output_{i}.png"
            # 结果URL有效期为24小时，请及时下载
            urllib.request.urlretrieve(image_url, file_name)
            print(f"Image saved to {file_name}")
    else:
        print(f"任务失败，状态: {done.status}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
```

<a id="wan27-sequential-async-response-title"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-28"></a>

```json
{
    "status_code": 200,
    "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": null,
        "audio": null,
        "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
        "task_status": "PENDING"
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 0
    }
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载图像。

<a id="code-block-29"></a>

```json
{
    "status_code": 200,
    "request_id": "56e318fd-ed60-99e8-8ca1-cdef25ca4xxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": null,
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "audio": null,
        "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2026-03-31 23:04:46.166",
        "scheduled_time": "2026-03-31 23:04:46.208",
        "end_time": "2026-03-31 23:05:11.664",
        "finished": true
    },
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "characters": 0,
        "size": "2048*2048",
        "total_tokens": 731,
        "image_count": 4
    }
}
```

<a id="java-sdk调用"></a>

<a id="d3a0dcecf1tyl"></a>

## Java SDK调用

SDK 参数命名与HTTP接口基本一致。

任务可能耗时较长，SDK 已封装HTTP异步调用流程，同时支持同步和异步调用。

> **重要**
>
> 请确保 DashScope Java SDK版本不低于 `2.22.13`，否则可能不支持本文所用的部分参数。

<a id="sec-tabs-13"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡-5"></a>

<a id="新加坡-5-h4"></a>

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="图像编辑-2-2"></a>

<a id="180cc839317zj"></a>

### 图像编辑

<a id="sec-tabs-14"></a>

<a id="同步调用-3"></a>

<a id="同步调用-3-h4"></a>

#### 同步调用

<a id="189e4d8658kmi"></a>

##### 请求示例

<a id="code-block-30"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 图像编辑 - 同步调用示例
 */
public class Main {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
        String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/car.png";
        // String image2 = "file:///path/to/your/paint.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/car.png");
        // String image2 = encodeFile("/path/to/your/paint.png");

        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
                        Collections.singletonMap("image", image1),
                        Collections.singletonMap("image", image2)
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .n(1)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("---sync call for image editing, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        basicCall();
    }
}
```

<a id="e4fbc7f75d4gg"></a>

##### 响应示例

> URL 有效期24小时，请及时下载并保存图像。

<a id="code-block-31"></a>

```java
{
    "requestId": "1bf6173a-e8de-9f75-94d3-5e618f875xxx",
    "usage": {
        "input_tokens": 18790,
        "output_tokens": 2,
        "total_tokens": 18792,
        "image_count": 1,
        "size": "2985*1405"
    },
    "output": {
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

<a id="5ce97169950io"></a>

##### 请求示例

<a id="code-block-32"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 图像编辑 - 异步调用示例
 */
public class Main {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
        String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/car.png";
        // String image2 = "file:///path/to/your/paint.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/car.png");
        // String image2 = encodeFile("/path/to/your/paint.png");

        // 构建多图输入消息
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Arrays.asList(
                        // 支持多图输入，可以提供多张参考图片
                        Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
                        Collections.singletonMap("image", image1),
                        Collections.singletonMap("image", image2)
                )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .n(1)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
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

    public static void waitTask(String taskId) throws ApiException, NoApiKeyException, IOException {
        ImageGeneration imageGeneration = new ImageGeneration();
        System.out.println("\n---waiting for task completion----");
        ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        asyncCall();
    }
}
```

<a id="02dea79668owz"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-33"></a>

```json
{
    "requestId": "ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx",
    "output": {
        "task_id": "8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载并保存图像。

<a id="code-block-34"></a>

```json
{
    "requestId": "60a08540-f1c1-9e76-8cd3-d5949db8cxxx",
    "usage": {
        "input_tokens": 18711,
        "output_tokens": 2,
        "total_tokens": 18713,
        "image_count": 1,
        "size": "2985*1405"
    },
    "output": {
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
        "task_id": "8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-03-31 19:57:58.840",
        "scheduled_time": "2026-03-31 19:57:58.877",
        "end_time": "2026-03-31 19:58:11.563"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="组图生成-2-2"></a>

<a id="12158ab94dwat"></a>

### 组图生成

<a id="sec-tabs-15"></a>

<a id="同步调用-4"></a>

<a id="同步调用-4-h4"></a>

#### 同步调用

<a id="fdcc0bc0b5xw2"></a>

##### 请求示例

<a id="code-block-35"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 组图生成 - 同步调用示例（北京地域）
 */
public class Main {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明（图生组图场景）：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        // String image1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/image.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/image.png");

        // 构建文本输入消息（支持文生组图以及图生组图，此处以文生组图为例）
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。")
                )).build();
        // 图生组图场景：取消以下注释并注释掉上方纯文本构建
        // ImageGenerationMessage message = ImageGenerationMessage.builder()
        //         .role("user")
        //         .content(Arrays.asList(
        //                 Collections.singletonMap("text", "参考图片风格生成四季组图"),
        //                 Collections.singletonMap("image", image1)
        //         )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .enableSequential(true)
                .n(4)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult result = null;
        try {
            System.out.println("----sync call, please wait a moment----");
            result = imageGeneration.call(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        basicCall();
    }
}
```

<a id="4dff52f5a4izo"></a>

##### 响应示例

> URL 有效期24小时，请及时下载并保存图像。

<a id="code-block-36"></a>

```java
{
    "requestId": "4678c314-b37a-91c9-a2ae-2d3cd54bbxxx",
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "total_tokens": 731,
        "image_count": 4,
        "size": "2048*2048"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
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

<a id="异步调用-4"></a>

<a id="异步调用-4-h4"></a>

#### 异步调用

<a id="fb681a63465zq"></a>

##### 请求示例

<a id="code-block-37"></a>

```java
import com.alibaba.dashscope.aigc.imagegeneration.*;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Arrays;
import java.util.Base64;
import java.util.Collections;
import java.util.List;
import java.util.Map;

/**
 * wan2.7-image-pro 组图生成 - 异步调用示例（北京地域）
 */
public class Main {

    static {
        // 以下为华北2（北京）地域的URL，调用时请将{WorkspaceId}替换为真实的业务空间ID，各地域的URL不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey="sk-xxx"
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // --- Base64编码函数 ---
    // base64编码格式为 data:{MIME_type};base64,{base64_data}
    public static String encodeFile(String filePath) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
        String base64String = Base64.getEncoder().encodeToString(fileContent);
        String mimeType = Files.probeContentType(Paths.get(filePath));
        return "data:" + mimeType + ";base64," + base64String;
    }

    public static ImageGenerationResult waitTask(String taskId)
            throws ApiException, NoApiKeyException {
        ImageGeneration imageGeneration = new ImageGeneration();
        return imageGeneration.wait(taskId, apiKey);
    }

    public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException, IOException {
        /*
         * 图像输入方式说明（图生组图场景）：
         * 以下提供了三种图片输入方式，三选一即可
         * 1. 使用公网URL - 适合已有公开可访问的图片
         * 2. 使用本地文件 - 适合本地开发测试
         * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
         */
        // 【方式一】使用公网图片 URL
        // String image1 = "https://img.alicdn.com/imgextra/i4/O1CN01IM44WN23dq5uY1yla_!!6000000007279-49-tps-1024-1024.webp";

        // 【方式二】使用本地文件（支持绝对路径和相对路径）
        // 格式要求：file:// + 文件路径
        // String image1 = "file:///path/to/your/image.png";

        // 【方式三】使用Base64编码的图片
        // String image1 = encodeFile("/path/to/your/image.png");

        // 构建文本输入消息（支持文生组图以及图生组图，此处以文生组图为例）
        ImageGenerationMessage message = ImageGenerationMessage.builder()
                .role("user")
                .content(Collections.singletonList(
                        Collections.singletonMap("text", "电影感组图，记录同一只流浪橘猫，特征必须前后一致。第一张：春天，橘猫穿梭在盛开的樱花树下；第二张：夏天，橘猫在老街的树荫下乘凉避暑；第三张：秋天，橘猫踩在满地的金色落叶上；第四张：冬天，橘猫在雪地上走留下足迹。")
                )).build();
        // 图生组图场景：取消以下注释并注释掉上方纯文本构建
        // ImageGenerationMessage message = ImageGenerationMessage.builder()
        //         .role("user")
        //         .content(Arrays.asList(
        //                 Collections.singletonMap("text", "参考图片风格生成四季组图"),
        //                 Collections.singletonMap("image", image1)
        //         )).build();

        ImageGenerationParam param = ImageGenerationParam.builder()
                .apiKey(apiKey)
                .model("wan2.7-image-pro")
                .messages(Collections.singletonList(message))
                .enableSequential(true)
                .n(4)
                .size("2K") // wan2.7-image-pro仅文生图场景支持4K分辨率，图像编辑和组图生成支持最高2K分辨率
                .build();

        ImageGeneration imageGeneration = new ImageGeneration();
        ImageGenerationResult taskResult = null;
        try {
            System.out.println("----async call, creating task----");
            taskResult = imageGeneration.asyncCall(param);
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
        }
        System.out.println("Task created: " + JsonUtils.toJson(taskResult));

        // 等待任务完成
        String taskId = taskResult.getOutput().getTaskId();
        ImageGenerationResult result = waitTask(taskId);
        // 提取结果图片URL并保存到本地
        for (int i = 0; i < result.getOutput().getChoices().size(); i++) {
            List<Map<String, Object>> contents = result.getOutput().getChoices().get(i)
                    .getMessage().getContent();
            for (int j = 0; j < contents.size(); j++) {
                if ("image".equals(contents.get(j).get("type"))) {
                    String imageUrl = (String) contents.get(j).get("image");
                    String fileName = "output_" + i + "_" + j + ".png";
                    // 结果URL有效期为24小时，请及时下载
                    try (InputStream in = new URL(imageUrl).openStream()) {
                        Files.copy(in, Paths.get(fileName), StandardCopyOption.REPLACE_EXISTING);
                    }
                    System.out.println("Image saved to " + fileName);
                }
            }
        }
    }

    public static void main(String[] args) throws ApiException, NoApiKeyException, UploadFileException, IOException {
        asyncCall();
    }
}
```

<a id="d207a5a32d9sj"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-38"></a>

```json
{
    "requestId": "7d026dc1-e8c9-9caa-84ac-e82e2da97xxx",
    "output": {
        "task_id": "2de18c56-c151-4b80-8105-1d164733exxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> URL 有效期24小时，请及时下载并保存图像。

<a id="code-block-39"></a>

```json
{
    "requestId": "daea7295-4ce0-928a-9a11-4d2bea058xxx",
    "usage": {
        "input_tokens": 720,
        "output_tokens": 11,
        "total_tokens": 731,
        "image_count": 4,
        "size": "2048*2048"
    },
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        },
                        {
                            "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                            "type": "image"
                        }
                    ]
                }
            }
        ],
        "task_id": "2de18c56-c151-4b80-8105-1d164733exxx",
        "task_status": "SUCCEEDED",
        "finished": true,
        "submit_time": "2026-03-31 19:49:53.124",
        "scheduled_time": "2026-03-31 19:49:53.175",
        "end_time": "2026-03-31 19:50:53.160"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

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
