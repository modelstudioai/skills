# 人像风格重绘API参考

人像风格重绘模型支持将人物照片，转换为多种预设或自定义的艺术风格。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

> **说明**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`，**能够为推理请求提供卓越的性能和更高的稳定性**，建议从 `https://dashscope.aliyuncs.com` 迁移至新域名。
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

|  |
| --- |
| **快速入口：**[使用指南](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md) ｜ [HTTP调用新手指南](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api) ｜ [新人免费额度](../../../model-user-guide/test-1/new-free-quota.md) ｜ [计费与限流](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md#d34d4c23aew5n) |

<a id="模型概览"></a>

<a id="72e2f172021m9"></a>

## 模型概览

<table><thead><tr><th rowspan="2"><p><strong>模型名称</strong></p></th><th rowspan="2"><p><strong>计费单价</strong></p></th><th colspan="2"><p><strong>限流（主账号与RAM子账号共享）</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></th></tr><tr><th><p><strong>任务下发接口QPS限制</strong></p></th><th><p><strong>同时处理中任务数量</strong></p></th></tr></thead><tbody><tr><td><p>wanx-style-repaint-v1</p></td><td><p>0.12元/张</p></td><td><p>2</p></td><td><p>1</p></td><td><p>500张</p></td></tr></tbody></table>

<a id="前提条件"></a>

<a id="cd03ebba5cblt"></a>

## 前提条件

您需要已[获取与配置 API Key](../../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="65796f7146azl"></a>

## HTTP调用

本模型**仅提供 HTTP API，暂无SDK**。由于图像生成耗时较长，API 采用异步模式，调用流程分两步：

1.  **创建任务**：创建人像风格重绘任务，获取唯一任务ID（task\_id）。
2.  **查询结果**：使用 `task_id` 轮询任务状态，直至完成并获取生成的图像URL。图像URL有效期为24小时。

> **说明**
>
> -   创建任务后，系统将立即返回一个 `task_id`。在步骤2中使用该 `task_id` 查询任务结果，有效期24小时。
> -   如需集成至现有项目，需自行实现对应语言的 HTTP 调用逻辑。部分示例代码请参见[人像风格重绘](../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md)。
> -   HTTP调用新手指南请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<a id="步骤1-创建任务获取任务id"></a>

<a id="161d4c0111m87"></a>

### 步骤1：创建任务获取任务ID

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求头（Headers）</h4><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h4>请求体（Request Body）</h4><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。示例值：wanx-style-repaint-v1。</p><p><strong>input</strong> <code>object</code> （必选）</p><p>输入图像的基本信息，比如图像URL地址。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>image_url</strong> <code>string</code> <strong>（必选）</strong></p><p>输入的图像URL地址。</p><ul><li><p>支持公网可访问的HTTP/HTTPS地址，不包含中文字符。</p></li><li><p>支持传入Base64编码字符串。</p></li><li><p>对于本地文件，可通过以下两种方式获取合法参数值：</p><ul><li>获取URL：请参见<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</li><li>生成Base64编码字符串：请参见<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md#fa664addf5wph">图像Base64编码传值方式</a>。</li></ul></li></ul><p>图像限制：</p><ul><li>图像分辨率：不低于256×256像素，不超过5760×3240像素。</li><li>图像格式：JPEG、PNG、JPG、BMP、WEBP。</li><li>图像比例：长短边比例不超过 2:1。</li><li>图片大小：不超过10M。</li><li>图像质量：为确保生成质量，请上传脸部清晰照片，人脸比例不宜过小，并避免夸张姿势和表情。</li></ul><p><strong>style_index</strong> <code>integer</code> <strong>（必选）</strong></p><p>选择一个预置的风格索引值，即可生成风格化人像。风格化效果请参考<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md">使用指南</a>。</p><ul><li>-1：使用参考图像风格（需提供<code>style_ref_url</code>）</li><li>0：复古漫画</li><li>1：3D童话</li><li>2：二次元</li><li>3：小清新</li><li>4：未来科技</li><li>5：国画古风</li><li>6：将军百战</li><li>7：炫彩卡通</li><li>8：清雅国风</li><li>9：喜迎新年</li><li>14：国风工笔</li><li>15：恭贺新禧</li><li>30：童话世界</li><li>31：黏土世界</li><li>32：像素世界</li><li>33：冒险世界</li><li>34：日漫世界</li><li>35：3D世界</li><li>36：二次元世界</li><li>37：手绘世界</li><li>38：蜡笔世界</li><li>39：冰箱贴世界</li><li>40：吧唧世界</li></ul><p><strong>style_ref_url</strong> <code>string</code> （可选）</p><p>当<code>style_index=-1</code>时，必须传入，其他风格无需传入。</p><p>风格参考图像URL地址。风格参考效果请参考<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md">使用指南</a>。</p><ul><li><p>支持公网可访问的HTTP/HTTPS地址，不包含中文字符。</p></li><li><p>支持传入Base64编码字符串。</p></li><li><p>对于本地文件，可通过以下两种方式获取合法参数值：</p><ul><li>获取URL：请参见<a href="../../more-about-models/get-temporary-file-url.md">上传文件获取临时URL</a>。</li><li>生成Base64编码字符串：请参见<a href="../../../model-user-guide/use-cases/legacy-resources/legacy-image-generation/style-repaint.md#fa664addf5wph">图像Base64编码传值方式</a>。</li></ul></li></ul><p>图像限制：</p><ul><li>图片分辨率：不小于256×256像素且不超过5760×3240像素。</li><li>图像比例：为取得最佳效果，建议图像长短边比例不超过 2:1，否则可能影响生成或导致报错。</li><li>图片格式：JPEG、PNG、JPG、BMP、WEBP。</li><li>图片大小：不超过10M。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="使用预置风格"></a><section><a id="使用预置风格-h4"></a><h4>使用预置风格</h4><p>设置style_index（不能设为-1）。</p><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx-style-repaint-v1&quot;,
    &quot;input&quot;: {
        &quot;image_url&quot;: &quot;https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/image_demo_input.png&quot;,
        &quot;style_index&quot;: 3
    }
}'
</code></pre></section><a id="使用自定义风格"></a><section><a id="使用自定义风格-h4"></a><h4>使用自定义风格</h4><p>设置style_ref_url（风格参考图），并将 style_index 设为 -1。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;wanx-style-repaint-v1&quot;,
    &quot;input&quot;: {
        &quot;image_url&quot;: &quot;https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/input_example.png&quot;,
        &quot;style_ref_url&quot;: &quot;https://vigen-video.oss-cn-shanghai.aliyuncs.com/demo_image/style_example.png&quot;,
        &quot;style_index&quot;: -1
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="cd3063363egdc"></a><h4>响应</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-3"></a><pre class="language-json"><code>{
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

<a id="步骤2-根据任务id查询结果"></a>

<a id="0578e132d2n1d"></a>

### 步骤2：根据任务ID查询结果

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   模型耗时约15秒。建议采用轮询机制，并设置合理的查询间隔（如 3 秒）来获取结果。
> -   `task_id`查询有效期为**24小时**，超时后将无法查询结果，系统将返回任务状态为`UNKNOWN`。
> -   任务成功后返回的 `url`有效期为**24小时**，请及时下载并保存图像。
> -   此查询接口的默认QPS为20。如需更高频次的查询或事件通知，请[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   如需批量查询或取消任务，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="5043fa882c26r"></a><h4>请求头（Headers）</h4><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="aa6a7e4730pr2"></a><h4>URL路径参数（Path parameters）</h4><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="f641893b4bykq"></a><h4>响应</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>start_time</strong> <code>string</code></p><p>任务开始时间。</p><p><strong>error_message</strong> <code>string</code></p><p>错误信息。正常请求时返回，可忽略。</p><p><strong>error_code</strong> <code>integer</code></p><p>错误码。正常请求时返回，可忽略。</p><p><strong>style_index</strong> <code>integer</code></p><p>返回指定所选风格的索引值。</p><p><strong>results</strong> <code>array object</code></p><p>任务结果列表，包括图像URL、prompt、部分任务执行失败报错信息等。</p><a id="accordion-数据结构"></a><section><p>数据结构</p><div><a id="code-block-6"></a><pre class="language-json"><code>{
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
</code></pre></div></section><p><strong>task_metrics</strong> <code>object</code></p><p>任务结果统计。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>TOTAL</strong> <code>integer</code></p><p>总的任务数。</p><p><strong>SUCCEEDED</strong> <code>integer</code></p><p>任务状态为成功的任务数。</p><p><strong>FAILED</strong> <code>integer</code></p><p>任务状态为失败的任务数。</p></div></section><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>image_count</strong> <code>integer</code></p><p>模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;f7fee4f1-1f68-9f17-85df-xxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;316c7af0-e91f-476f-99bd-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2025-08-12 10:55:43.768&quot;,
        &quot;scheduled_time&quot;: &quot;2025-08-12 10:55:43.799&quot;,
        &quot;end_time&quot;: &quot;2025-08-12 10:55:48&quot;,
        &quot;error_message&quot;: &quot;Success&quot;,
        &quot;start_time&quot;: &quot;2025-08-12 10:55:43&quot;,
        &quot;style_index&quot;: 0,
        &quot;error_code&quot;: 0,
        &quot;results&quot;: [
            {
                &quot;url&quot;: &quot;http://oss.aliyuncs.com/xxx/abc.jpg&quot;
            }
        ]
    },
    &quot;usage&quot;: {
        &quot;image_count&quot;: 1
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;&lt;your request id&gt;&quot;,
  &quot;output&quot;: {
    &quot;task_id&quot;: &quot;&lt;your task id&gt;&quot;,
    &quot;task_status&quot;: &quot;FAILED&quot;,
    &quot;submit_time&quot;: &quot;xxx&quot;,
    &quot;scheduled_time&quot;: &quot;xxx&quot;,
    &quot;end_time&quot;: &quot;xxx&quot;,
    &quot;code&quot;: &quot;InvalidImageResolution&quot;,
    &quot;message&quot;: &quot;The input image resolution is too large or small&quot;
  },
  &quot;usage&quot;: {
    &quot;image_num&quot;: 0
  }
}
</code></pre></section><a id="任务执行中"></a><section><a id="任务执行中-h4"></a><h4>任务执行中</h4><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;:&quot;RUNNING&quot;,
        &quot;task_metrics&quot;:{
            &quot;TOTAL&quot;:1,
            &quot;SUCCEEDED&quot;:1,
            &quot;FAILED&quot;:0
        }
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="9c31ff011bxae"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

此API还有特定状态码，具体如下所示。

| HTTP状态码 | 接口错误码（code） | 接口错误信息（message） | 含义说明 |
| --- | --- | --- | --- |
| 400 | InvalidURL | The request URL is invalid, make sure the url is correct and is an image | 输入URL错误，请确保URL链接的正确性 |
| 400 | InvalidImageResolution | The input image resolution is too large or small | 输入图像分辨率过大或过小 |
| 400 | InvalidImageFormat | The input image is in invalid format | 输入图像格式无效 |

<a id="常见问题"></a>

<a id="3a78f4e212bx9"></a>

## 常见问题

**Q：调用风格重绘接口报错**`"code":"InvalidImageFormat","message":"The input image is in invalid format"}`**？**

A：输出图像格式不符合要求，请查看本文档中图像参数的使用说明。

**Q：输出图像的尺寸是否与输入图像一致？**

A：**不一致。** 输出图像会保持输入图像的宽高比，但会将短边固定为 1536 像素，长边按比例缩放。
