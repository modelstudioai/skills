# Vidu-图像生成API参考

Vidu-参考生图模型支持 文生图 、 图片编辑、参考图生图等 任务。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="模型概览"></a>

<a id="vidu_overview_h2"></a>

## 模型概览

| 模型名称 | 能力支持 | 输入模态 | 输出图像规格 |
| --- | --- | --- | --- |
| vidu/vidu-image\_reference2image<br><br>vidu/vidu-image-pro\_reference2image<br><br>vidu/vidu-image-lite\_reference2image | 支持参考生图、文生图、图片编辑，对中英文字的精准渲染、UI/图表等设计细节的像素级还原，适合制作海报、信息图等。 | 文本、图像 | 图像分辨率：1K、2K、4K<br><br>图像张数：1<br><br>图像格式：PNG |
| vidu/viduq3-fast\_reference2image | 支持参考生图、文生图、图片编辑，主打高速高质与低成本，成本比Pro降低约50%。 | 文本、图像 | 图像分辨率：1K、2K、4K<br><br>图像张数：1<br><br>图像格式：PNG |
| vidu/viduq3.1-fast\_reference2image | 支持参考生图、文生图、图片编辑，可通过分辨率与画幅比例指定输出尺寸。 | 文本、图像 | 图像分辨率：1K、2K、4K<br><br>图像张数：1<br><br>图像格式：PNG |
| vidu/viduq2-pro\_reference2image | 支持参考生图、文生图、图片编辑，擅长处理复杂逻辑，具备超强上下文一致性和工业级稳定性。适合专业设计、漫剧制作等。 | 文本、图像 | 图像分辨率：1K、2K、4K<br><br>图像张数：1<br><br>图像格式：PNG |
| vidu/viduq2-fast\_reference2image | 支持参考生图、文生图、图片编辑，语义理解能力大幅提升，支持更多风格。 | 文本、图像 | 图像分辨率：1K<br><br>图像张数：1<br><br>图像格式：PNG |

<a id="前提条件"></a>

<a id="vidu_prereq_h2"></a>

## 前提条件

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索"Vidu"，找到对应模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)。

<a id="http调用"></a>

<a id="vidu_http_h2"></a>

## HTTP调用

图像生成任务有一定耗时，API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤一-提交图像生成任务"></a>

<a id="vidu_step1_h3"></a>

### 步骤一：提交图像生成任务

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

<table><tbody><tr><td><a id="vidu_req_hdr_h4"></a><h4>请求参数</h4><a id="vidu_headers_h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="vidu_body_h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值：</p><ul><li><code>vidu/vidu-image_reference2image</code></li><li><code>vidu/vidu-image-pro_reference2image</code></li><li><code>vidu/vidu-image-lite_reference2image</code></li><li><code>vidu/viduq3-fast_reference2image</code></li><li><code>vidu/viduq3.1-fast_reference2image</code></li><li><code>vidu/viduq2-pro_reference2image</code></li><li><code>vidu/viduq2-fast_reference2image</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>多轮消息列表。服务端会提取第一个非空<code>text</code>作为提示词，并提取全部<code>image</code>作为参考图。数组内<strong>有且只有一个对象</strong>，该对象包含<code>role</code>和<code>content</code>两个属性。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> （可选）</p><p>消息的角色，建议设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容，包含文本提示词（text）和可选的参考图像（image，支持多张）。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（条件必选）</strong></p><p>正向提示词，用于描述期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过5000个字符，每个汉字、字母、数字或符号计为一个字符。</p><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p><strong>注意</strong>：整个messages中至少需要一个非空文本。</p><p><strong>image</strong> <code>string</code> （可选）</p><p>参考图像的URL。支持传多张，所有模型最多支持输入14张。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png"></a><a href="https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png">https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png</a>。</li></ul><p>图像限制：</p><ul><li>格式：PNG、JPG、WEBP。</li><li>宽高比：在1:4 ~ 4:1之间。</li><li>文件大小：所有图片总和不超过50MB。</li><li>数量限制：最多14张参考图片。</li></ul></div></section></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>控制图像生成参数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>size</strong> <code>string</code> （可选）</p><p>图片尺寸，格式为<code>宽*高</code>（如<code>2048*2048</code>）。不传时默认<code>1024*1024</code>。</p><p>不同模型支持的尺寸列表请参见下方<a href="vidu-image-generation-api-reference.md#vidu_sizes_h2">可用尺寸列表</a>。</p><p>使用vidu/viduq3.1-fast_reference2image时，<code>size</code>须从可用尺寸列表中选择，不支持<code>auto</code>，并与<code>resolution</code>二选一：两者都不传返回参数错误，同时传入时以<code>resolution</code>为准。</p><p><strong>resolution</strong> <code>string</code> （可选）</p><p><strong>支持模型</strong>：vidu/viduq3.1-fast_reference2image。</p><p>生成图像的分辨率档位，与<code>size</code>二选一；传入该参数时忽略<code>size</code>。</p><ul><li><code>1K</code></li><li><code>2K</code></li><li><code>4K</code></li></ul><p>不支持<code>auto</code>和<code>512</code>。</p><p><strong>aspect_ratio</strong> <code>string</code> （可选）</p><p><strong>支持模型</strong>：vidu/viduq3.1-fast_reference2image。</p><p>生成图像的画幅比例，仅在设置<code>resolution</code>时生效。</p><ul><li><code>auto</code>：默认值，由模型根据提示词决定画幅比例，不固定为<code>1:1</code>。</li><li><code>1:1</code></li><li><code>2:3</code></li><li><code>3:2</code></li><li><code>3:4</code></li><li><code>4:3</code></li><li><code>4:5</code></li><li><code>5:4</code></li><li><code>9:16</code></li><li><code>16:9</code></li><li><code>21:9</code></li><li><code>1:4</code></li><li><code>4:1</code></li><li><code>1:8</code></li><li><code>8:1</code></li></ul><p>仅传<code>aspect_ratio</code>而不传<code>resolution</code>时，返回缺少<code>resolution</code>的参数错误。</p><p><strong>n</strong> <code>integer</code> （可选）</p><p>生成图片数量，当前仅支持<code>1</code>。传其他值会返回参数错误。</p><p><strong>seed</strong> <code>integer</code> （可选）</p><p>随机数种子，取值范围<code>[0,2147483647]</code>，<code>0</code>表示随机。</p><p>使用相同的<code>seed</code>参数值可使生成内容保持相对稳定。若不提供，算法将自动使用随机数种子。</p><p>使用vidu/viduq3.1-fast_reference2image时不生效。</p><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否添加水印标识。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="文生图"></a><section><a id="文生图-h4"></a><h4>文生图</h4><p>支持所有Vidu模型。</p><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;vidu/vidu-image_reference2image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;一间有着精致窗户的花店,漂亮的木质门,摆放着花朵&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="参考图生图"></a><section><a id="参考图生图-h4"></a><h4>参考图生图</h4><p>支持所有Vidu模型，最多可传入14张参考图。</p><a id="code-block-2"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;vidu/vidu-image_reference2image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;参考图片的风格，生成一只坐着的橘黄色的猫&quot;
                    },
                    {
                        &quot;image&quot;: &quot;https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;2048*2048&quot;,
        &quot;n&quot;: 1,
        &quot;watermark&quot;: false
    }
}'
</code></pre></section><a id="指定分辨率-viduq3-1-fast"></a><section><a id="指定分辨率-viduq3-1-fast-h4"></a><h4>指定分辨率（viduq3.1-fast）</h4><p>传入<code>resolution</code>时，<code>size</code>会被忽略。</p><a id="code-block-3"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;vidu/viduq3.1-fast_reference2image&quot;,
    &quot;input&quot;: {
        &quot;messages&quot;: [
            {
                &quot;role&quot;: &quot;user&quot;,
                &quot;content&quot;: [
                    {
                        &quot;text&quot;: &quot;把背景改成海边日落&quot;
                    },
                    {
                        &quot;image&quot;: &quot;https://cdn.wanx.aliyuncs.com/tmp/pressure/umbrella1.png&quot;
                    }
                ]
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;1K&quot;,
        &quot;aspect_ratio&quot;: &quot;16:9&quot;,
        &quot;n&quot;: 1
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="vidu_resp1_hdr_h4"></a><h4>响应参数</h4><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤二-查询任务结果"></a>

<a id="vidu_step2_h3"></a>

### 步骤二：查询任务结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：图像生成过程需一定时间，建议采用**轮询**机制，并设置合理的查询间隔（如5秒）来获取结果。
> -   **任务状态流转**：PENDING（等待中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **图片链接有效期**：生成图像的下载链接**24小时**内有效，请及时下载并保存图像。

<table><tbody><tr><td><a id="vidu_qry_hdr_h4"></a><h4>请求参数</h4><a id="vidu_qry_headers_h5"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><a id="code-block-6"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location --request GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="vidu_resp2_hdr_h4"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。</p><p><strong>choices</strong> <code>array</code></p><p>图片输出候选列表，仅在task_status=SUCCEEDED时返回。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>结束原因，成功时通常为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出内容的类型，固定为<code>image</code>。</p><p><strong>image</strong> <code>string</code></p><p>生成图像的下载链接，图像格式为PNG。<strong>链接有效期为24小时</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section><p><strong>finished</strong> <code>bool</code></p><p>是否完成，仅在task_status=SUCCEEDED时返回。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>资源用量信息。只对成功的结果计数。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的数量。</p><p><strong>size</strong> <code>string</code></p><p>生成图片的分辨率，格式为<code>宽*高</code>。示例值：2048*2048。</p><p><strong>SR</strong> <code>string</code></p><p>生成图像的分辨率档位。示例值：2K。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;f584a817-6e00-9841-961a-49f7382a03d4&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;6404d4ec-4cdf-45b5-8d7d-3d429c6baed5&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-07-13 20:27:41.291&quot;,
        &quot;scheduled_time&quot;: &quot;2026-07-13 20:27:41.320&quot;,
        &quot;end_time&quot;: &quot;2026-07-13 20:28:39.767&quot;,
        &quot;finished&quot;: true,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://example.com/generated-image.png&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;SR&quot;: &quot;2K&quot;,
        &quot;size&quot;: &quot;2048*2048&quot;,
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;1f015514-b04c-9190-b4dd-8ba11bb15708&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;ccae6c03-fe9f-48fd-b3d6-a524c4707f17&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;: &quot;2026-07-13 20:27:50.654&quot;,
        &quot;scheduled_time&quot;: &quot;2026-07-13 20:27:50.689&quot;,
        &quot;end_time&quot;: &quot;2026-07-13 20:27:51.090&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;Missing required field 'parameters.n' in request body&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="可用尺寸列表"></a>

<a id="vidu_sizes_h2"></a>

## 可用尺寸列表

<a id="vidu-image-vidu-image-pro-vidu-image-lite"></a>

<a id="vidu_sizes_m1_h3"></a>

### vidu-image、vidu-image-pro、vidu-image-lite

| 分辨率 | 支持尺寸 |
| --- | --- |
| 1K | 1024\*1024、720\*1440、1440\*720、1024\*768、768\*1024、1920\*1088、1088\*1920、1536\*1024、1024\*1536、1920\*816、816\*1920 |
| 2K | 2048\*2048、1088\*2160、2160\*1088、2736\*2048、2048\*2736、2560\*1440、1440\*2560、3072\*2048、2048\*3072、2560\*1104、1104\*2560 |
| 4K | 2880\*2880、1440\*2880、2880\*1440、3312\*2480、2480\*3312、3840\*2160、2160\*3840、3520\*2352、2352\*3520、3840\*1648、1648\*3840 |

<a id="viduq3-fast-viduq3-1-fast"></a>

<a id="vidu_sizes_m2_h3"></a>

### viduq3-fast、viduq3.1-fast

vidu/viduq3-fast\_reference2image和vidu/viduq3.1-fast\_reference2image支持的尺寸相同。传入`size`时，服务端会将其映射为分辨率与画幅比例，此时请求中的`aspect_ratio`会被忽略。

| 分辨率 | 支持尺寸 |
| --- | --- |
| 1K | 1024\*1024、768\*1376、848\*1264、896\*1200、928\*1152、1152\*928、1200\*896、1264\*848、1376\*768、1584\*672、512\*2064、2064\*512、352\*2928、2928\*352 |
| 2K | 2048\*2048、1536\*2752、1696\*2528、1792\*2400、1856\*2304、2304\*1856、2400\*1792、2528\*1696、2752\*1536、3168\*1344、1024\*4128、4128\*1024、704\*5856、5856\*704 |
| 4K | 4096\*4096、3072\*5504、3392\*5056、3584\*4800、3712\*4608、4608\*3712、4800\*3584、5056\*3392、5504\*3072、6336\*2688、2048\*8256、8256\*2048、1408\*11712、11712\*1408 |

<a id="viduq2-pro"></a>

<a id="vidu_sizes_m3_h3"></a>

### viduq2-pro

| 分辨率 | 支持尺寸 |
| --- | --- |
| 1K | 1024\*1024、768\*1376、848\*1264、896\*1200、928\*1152、1152\*928、1200\*896、1264\*848、1376\*768、1584\*672 |
| 2K | 2048\*2048、1536\*2752、1696\*2528、1792\*2400、1856\*2304、2304\*1856、2400\*1792、2528\*1696、2752\*1536、3168\*1344 |
| 4K | 4096\*4096、3072\*5504、3392\*5056、3584\*4800、3712\*4608、4608\*3712、4800\*3584、5056\*3392、5504\*3072、6336\*2688 |

<a id="viduq2-fast"></a>

<a id="vidu_sizes_m4_h3"></a>

### viduq2-fast

| 分辨率 | 支持尺寸 |
| --- | --- |
| 1K | 1024\*1024、768\*1376、848\*1264、896\*1200、928\*1152、1152\*928、1200\*896、1264\*848、1376\*768、1584\*672 |
