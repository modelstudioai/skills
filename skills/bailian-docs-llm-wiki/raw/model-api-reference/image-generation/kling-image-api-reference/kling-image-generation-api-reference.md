# 可灵-图像生成API参考

可灵-图像生成模型支持 文生图 、 参考图生图 两种任务。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="模型概览"></a>

<a id="e5bd43cfa8l83"></a>

## 模型概览

<table><thead><tr><th><p><strong>模型名称</strong></p></th><th><p><strong>能力支持</strong></p></th><th><p><strong>输入模态</strong></p></th><th><p><strong>输出图像规格</strong></p></th></tr></thead><tbody><tr><td><p>kling/kling-v3-image-generation</p></td><td><ul><li><p>文生图</p></li><li><p>参考图生图：仅单图输入。</p></li></ul></td><td><p>文本、图像</p></td><td><p>图像分辨率：1k、2k</p><p>宽高比：16:9、9:16、1:1</p><p>图像张数：通过参数n指定（1～9）</p><p>图像格式：png</p></td></tr><tr><td><p>kling/kling-v3-omni-image-generation</p></td><td><ul><li><p>文生图</p></li><li><p>参考图生图：支持多图输入，支持生成分镜组图。</p></li></ul></td><td><p>文本、图像</p></td><td><p>图像分辨率：1k、2k、4k</p><p>宽高比：16:9、9:16、1:1</p><p>图像张数：</p><ul><li><p>单图模式通过参数<code>n</code>指定：1～9</p></li><li><p>组图模式通过<code>series_amount</code>指定：2～9</p></li></ul><p>图像格式：png</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="8bb48973d87d6"></a>

## 前提条件

1.  **开通服务**：前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索“可灵”，找到**可灵AI**模型卡片，单击**立即开通**，在弹窗内确认开通及授权。
2.  **配置API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="omni_http_h2"></a>

## HTTP调用

图像生成任务有一定耗时（通常为1-2分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤一-提交图像生成任务"></a>

<a id="omni_step1_h3"></a>

### 步骤一：提交图像生成任务

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="omni_req_hdr_h4"></a><h4>请求参数</h4><a id="omni_headers_h5"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="omni_body_h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值：</p><ul><li><code>kling/kling-v3-image-generation</code></li><li><code>kling/kling-v3-omni-image-generation</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入参数对象，包含以下字段：</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>messages</strong> <code>array</code> <strong>（必选）</strong></p><p>请求内容数组。<strong>当前仅支持单轮对话</strong>，因此数组内<strong>有且只有一个对象</strong>，该对象包含<code>role</code>和<code>content</code>两个属性。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code> （可选）</p><p>消息的角色。此参数必须设置为<code>user</code>。</p><p><strong>content</strong><code>array</code> <strong>（必选）</strong></p><p>消息内容，包含文本提示词（text）和可选的参考图像（image，支持多张）。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>text</strong><code>string</code><strong>（条件必选）</strong></p><p>正向提示词，用于描述期望生成的图像内容、风格和构图。</p><p>支持中英文，长度不超过2500个字符，每个汉字、字母、数字或符号计为一个字符，超过将返回错误。</p><p>示例值：一只坐着的橘黄色的猫，表情愉悦，活泼可爱，逼真准确。</p><p><strong>注意</strong>：仅支持传入一个text，不传或传入多个将报错。</p><p><strong>image</strong> <code>string</code> （可选）</p><p>参考图像的URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.png"></a><a href="https://xxx/xxx.png">https://xxx/xxx.png</a>。</li></ul><p>图像限制：</p><ul><li>格式：JPEG、JPG、PNG（不支持透明通道）。</li><li>分辨率：宽和高的范围为[300, 8000]像素。</li><li>宽高比：在1:2.5 ~ 2.5:1之间。</li><li>文件大小：不超过10MB。</li><li>数量限制：参考图片数量和参考主体数量（element_list数组长度）之和<strong>不得超过10</strong>。</li></ul></div></section></div></section><p><strong>element_list</strong> <code>array</code> （可选）</p><p>主体列表，用于指定需要保持的主体。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>element_id</strong> <code>integer</code> （条件必填）</p><p>传<code>element_list</code>时必填，表示主体ID。请在<a href="../../video-generation-api/kling-api-reference/kling-object-ids.md">可灵-主体ID列表</a>获取主体ID。</p><p>数量限制：参考图片数量和参考主体数量（element_list数组长度）之和<strong>不得超过10</strong>。</p></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>控制图像生成，比如图像张数、宽高比等。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>n</strong> <code>integer</code> （可选）</p><p>生成的图像张数。</p><ul><li><p>kling/kling-v3-image-generation：取值范围为1～9。默认值为1。</p></li><li><p>kling/kling-v3-omni-image-generation：</p><ul><li>当且仅当<code>result_type=single</code>时生效。</li><li>取值范围为1～9。默认值为1。</li></ul></li></ul><p><strong>result_type</strong> <code>string</code> （可选）</p><p>支持模型：kling/kling-v3-omni-image-generation。</p><p>生成图像的类型。</p><ul><li><code>single</code>（ 默认值）：单图。批量生成时仅风格相似，无分镜关联。</li><li><code>series</code>：组图。生成具有叙事/视觉连续性的分镜系列图像。</li></ul><p><strong>series_amount</strong> <code>integer</code> （可选）</p><p>支持模型：kling/kling-v3-omni-image-generation。</p><p>组图模式下的输出张数。取值范围为2～9，默认值为4。</p><p>生效条件：当且仅当<code>result_type=series</code>时生效。</p><p><strong>aspect_ratio</strong> <code>string</code> （可选）</p><p>输出图像的宽高比。</p><ul><li><code>16:9</code>：默认值。</li><li><code>9:16</code></li><li><code>1:1</code></li></ul><p>示例值：16:9。</p><p><strong>resolution</strong> <code>string</code> （可选）</p><p>输出图像分辨率。</p><ul><li>kling/kling-v3-image-generation：可选值为<code>1k</code>、<code>2k</code>，默认值为<code>1k</code>。</li><li>kling/kling-v3-omni-image-generation：可选值为<code>1k</code>、<code>2k</code>、<code>4k</code>，默认值为<code>1k</code>。</li></ul><p>示例值：1k。</p><p><strong>watermark</strong> <code>bool</code> （可选）</p><p>是否同时生成含水印的图像。水印位于图像右下角，文案固定为”可灵AI”。</p><ul><li><code>false</code>：默认值，不生成含水印的图像。</li><li><code>true</code>：同时生成含水印的图像。</li></ul><p>示例值：false。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="文生图"></a><section><a id="文生图-h4"></a><h4>文生图</h4><p>支持模型：<code>kling/kling-v3-omni-image-generation</code>、<code>kling/kling-v3-image-generation</code>。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;kling/kling-v3-image-generation&quot;,
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
        &quot;n&quot;: 2,
        &quot;aspect_ratio&quot;: &quot;1:1&quot;,
        &quot;resolution&quot;: &quot;1k&quot;
    }
}'
</code></pre></section><a id="图生图-组图模式"></a><section><a id="图生图-组图模式-h4"></a><h4>图生图（组图模式）</h4><p>支持模型：<code>kling/kling-v3-omni-image-generation</code>。</p><p>支持以下模式：</p><ul><li><strong>单图</strong>（<code>result_type=single</code>）：独立生成，批量时仅风格相似。</li><li><strong>组图</strong>（<code>result_type=series</code>）：分镜序列生成，保持角色/场景/叙事连续性。</li></ul><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;kling/kling-v3-omni-image-generation&quot;,
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
        &quot;n&quot;: 4,
        &quot;result_type&quot;: &quot;series&quot;,
        &quot;aspect_ratio&quot;: &quot;1:1&quot;,
        &quot;resolution&quot;: &quot;1k&quot;
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="82c91c55bajs9"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤二-查询任务结果"></a>

<a id="omni_step2_h3"></a>

### 步骤二：查询任务结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   **轮询建议**：图像生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 5 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="pv414a0h4qr01"></a><h4>请求参数</h4><a id="pv424a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="pv430a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="d49207c2957vv"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-7"></a><section><p>属性</p><div><p><strong>choices</strong> <code>array</code></p><p>模型生成的输出内容。此数组仅包含一个元素。</p><a id="accordion-属性-8"></a><section><p>属性</p><div><p><strong>finish_reason</strong> <code>string</code></p><p>任务停止原因，自然停止时为<code>stop</code>。</p><p><strong>message</strong> <code>object</code></p><p>模型返回的消息。</p><a id="accordion-属性-9"></a><section><p>属性</p><div><p><strong>role</strong><code>string</code></p><p>消息的角色，固定为<code>assistant</code>。</p><p><strong>content</strong><code>array</code></p><a id="accordion-属性-10"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code></p><p>输出内容的类型。固定为<code>image</code>。</p><p><strong>image</strong> <code>string</code></p><p>生成图像的 URL，图像格式为PNG。<strong>链接有效期为30天</strong>，请及时下载并保存图像。</p></div></section></div></section></div></section></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-11"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>生成图像的数量。</p><p><strong>size</strong> <code>string</code></p><p>生成图片的分辨率，格式为<code>宽*高</code>。示例值：1360*768。</p><p><strong>SR</strong> <code>string</code></p><p>生成图像的分辨率档位。示例值：1080。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;95146d89-9d70-481a-8c16-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;2c502d25-12a9-4517-8972-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-27 22:46:01.536&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-27 22:46:01.580&quot;,
        &quot;end_time&quot;: &quot;2026-03-27 22:46:24.831&quot;,
        &quot;finished&quot;: true,
        &quot;choices&quot;: [
            {
                &quot;finish_reason&quot;: &quot;stop&quot;,
                &quot;message&quot;: {
                    &quot;role&quot;: &quot;assistant&quot;,
                    &quot;content&quot;: [
                        {
                            &quot;image&quot;: &quot;https://p4-fdl.klingai.com/xxx.png?xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        },
                        {
                            &quot;image&quot;: &quot;https://p4-fdl.klingai.com/xxx.png?xxx&quot;,
                            &quot;type&quot;: &quot;image&quot;
                        }
                    ]
                }
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;size&quot;: &quot;1024*1024&quot;,
        &quot;image_count&quot;: 2,
        &quot;SR&quot;: &quot;1080&quot;
    }
}
</code></pre></section><a id="任务执行异常"></a><section><a id="任务执行异常-h4"></a><h4>任务执行异常</h4><p>如果因为某种原因导致任务执行失败，将返回相关信息，可以通过code和message字段明确指示错误原因。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4d78a5f-655f-9639-8437-xxxxxx&quot;,
    &quot;code&quot;: &quot;InvalidParameter&quot;,
    &quot;message&quot;: &quot;num_images_per_prompt must be 1&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
