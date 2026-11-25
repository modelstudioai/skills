# 爱诗-图生视频-基于首帧API参考

爱诗-图生视频模型根据 输入图像 和 文本提示词 ，生成一段流畅的视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
2.  在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="c3d4e5f6g7h8i"></a>

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：获取该地域的[API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **说明**
>
> 本文的示例代码适用于**华北2（北京）地域**。

<a id="http调用"></a>

<a id="u1v2w3x4y5z6a"></a>

## HTTP调用

图生视频任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="x4y5z6a7b8c9d"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="h4i5j6k7l8m9n"></a><h4>请求参数</h4><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="z2a3b4c5d6e7f"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>可选值：</p><ul><li>pixverse/pixverse-v6-max-it2v</li><li>pixverse/pixverse-c1-it2v</li><li>pixverse/pixverse-v6-it2v</li><li>pixverse/pixverse-v5.6-it2v</li></ul><a id="accordion-模型选型"></a><section><p>模型选型</p><div><ul><li>推荐使用 <strong>v6-max</strong>。</li><li>针对打斗、法术特效及高速运动等动态场景，可选 <strong>c1</strong>。</li></ul></div></section><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词、媒体素材等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （可选）</p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，字符编码为UTF-8，超过部分会自动截断。</p><ul><li>pixverse/pixverse-v6-max-it2v：不超过5000个字符。</li><li>pixverse/pixverse-c1-it2v：不超过5000个字符。</li><li>pixverse/pixverse-v6-it2v：不超过5000个字符。</li><li>pixverse/pixverse-v5.6-it2v：不超过2048个字符。</li></ul><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体素材列表，用于指定视频生成所需的图像。</p><p>数组的每个元素为一个媒体对象，包含 <code>type</code> 与 <code>url</code> 字段。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。固定值为：</p><ul><li><code>image_url</code>：图像URL。</li></ul><p>素材限制：图像数量推荐为1张。</p><blockquote><p>若传入多张图像，系统将默认采用最后一个，建议始终只传一张图像以确保预期效果。</p></blockquote><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>图像文件的URL地址，必须为公网可访问的URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.jpg"></a><a href="https://xxx/xxx.jpg">https://xxx/xxx.jpg</a>。</li></ul><p>图像限制：</p><ul><li>格式：JPG、PNG、WEBP。</li><li>分辨率：建议图片分辨率不要太小，单边不低于100像素；不支持单边超过10000像素的图片。</li><li>文件大小：不超过20MB。</li></ul></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置视频分辨率、设置视频时长、开启音频生成、添加水印等。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>resolution直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxi002a0h3001">模型价格</a>。</p></div></div><p>指定生成的视频分辨率档位。</p><p>可选值：<code>360P</code>、<code>540P</code>、<code>720P</code>、<code>1080P</code>。</p><p><strong>duration</strong> <code>integer</code> <strong>（必选）</strong></p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxi002a0h3001">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li><p>pixverse/pixverse-v6-max-it2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-c1-it2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-v6-it2v：取值范围为[1, 15]之间的整数。</p></li><li><p>pixverse/pixverse-v5.6-it2v：</p><ul><li>当 resolution 为 360P / 540P / 720P 对应的所有分辨率时：取值为5、8、10。</li><li>当resolution为1080P对应的所有分辨率时：取值为5、8。</li></ul></li></ul><p><strong>audio</strong> <code>boolean</code> （可选）</p><div><div><p><strong>重要</strong>audio直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#pxi002a0h3001">模型价格</a>。</p></div></div><p>是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为&quot;AI生成&quot;。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>shot_type</strong> <code>string</code> （可选）</p><p><strong>支持模型</strong>：pixverse/pixverse-v6-it2v。</p><p>指定生成视频的镜头类型，控制视频是由一个连续镜头还是多镜头组成。</p><ul><li><code>single</code>：默认值，生成单镜头视频。</li><li><code>multi</code>：多镜头，系统会进行智能分镜。</li></ul><p>使用建议：prompt 参数优先级高于 shot_type 。为获得最佳效果，建议此参数设置与 prompt 描述保持一致。</p><ul><li>若想稳定输出单镜头：设置 <code>shot_type=&quot;single&quot;</code> 并在 prompt 中描述单镜头场景。</li><li>若想稳定输出多镜头：设置 <code>shot_type=&quot;multi&quot;</code> 并在 prompt 中描述多镜头场景。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="图生视频"></a><section><a id="图生视频-h4"></a><h4>图生视频</h4><p>支持模型：pixverse/pixverse-v6-max-it2v、pixverse/pixverse-c1-it2v、pixverse/pixverse-v6-it2v、pixverse/pixverse-v5.6-it2v。</p><a id="code-block"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-v6-max-it2v&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp&quot;
            }
        ],
        &quot;prompt&quot;: &quot;镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;duration&quot;: 5,
        &quot;audio&quot;: true,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="图生视频-多镜头"></a><section><a id="图生视频-多镜头-h4"></a><h4>图生视频（多镜头）</h4><a id="sec-tabs-2"></a><section><a id="pixverse-v6-max-pixverse-c1"></a><section><a id="pixverse-v6-max-pixverse-c1-h4"></a><h4>pixverse-v6-max、pixverse-c1</h4><p>支持模型：pixverse/pixverse-v6-max-it2v、pixverse/pixverse-c1-it2v。</p><p>在<code>prompt</code>中描述多镜头场景即可，不支持设置 <code>shot_type</code>参数。</p><a id="code-block-2"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-v6-max-it2v&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp&quot;
            }
        ],
        &quot;prompt&quot;: &quot;镜头1：从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。镜头2：远景，海龟旁边围绕着海草，海草也在左右摇摆&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;duration&quot;: 8,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="pixverse-v6"></a><section><a id="pixverse-v6-h4"></a><h4>pixverse-v6</h4><p>支持模型：pixverse/pixverse-v6-it2v。</p><p>在<code>prompt</code>中描述多镜头场景，并设置 <code>shot_type</code> 为<code>multi</code>， 即可生成有声多镜头视频。</p><a id="code-block-3"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-v6-it2v&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp&quot;
            }
        ],
        &quot;prompt&quot;: &quot;镜头1：从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。镜头2：远景，海龟旁边围绕着海草，海草也在左右摇摆&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;duration&quot;: 8,
        &quot;shot_type&quot;: &quot;multi&quot;,
        &quot;audio&quot;: false,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="64ee5e75edznz"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-4"></a><pre class="language-json"><code>{
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

<a id="步骤2-根据任务id查询结果"></a>

<a id="6da9d53d19x71"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="19f6e90ee5rnq"></a><h4>请求参数</h4><a id="1e961f0eb7gwq"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="96525d350eazf"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-4"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-6"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="9fed9a5bc6zes"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储依赖，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>生成视频的总视频时长，用于计费。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。</p><p><strong>audio</strong> <code>boolean</code></p><p>生成视频是否为有声视频。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p><p>使用pixverse/pixverse-v6-max-it2v时不返回该字段。</p><p><strong>shot_type</strong><code>string</code></p><p>生成视频的镜头类型。</p><p>使用pixverse/pixverse-v6-max-it2v时不返回该字段。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-5"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;7df19cf7-d76c-4bb8-b4c5-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;5abf2c85-ea81-4cbf-8918-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-20 11:48:50.499&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-20 11:48:50.551&quot;,
        &quot;end_time&quot;: &quot;2026-03-20 11:49:46.462&quot;,
        &quot;orig_prompt&quot;: &quot;镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。&quot;,
        &quot;video_url&quot;: &quot;https://media.pixverseai.cn/xxxx.mp4&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;shot_type&quot;: &quot;single&quot;,
        &quot;size&quot;: &quot;992*944&quot;,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;audio&quot;: false,
        &quot;SR&quot;: &quot;720&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-9"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
