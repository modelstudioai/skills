# 爱诗-视频超清API参考

爱诗-视频超清模型支持将输入视频进行超分辨率处理，固定输出4K（3840×2160）分辨率视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
2.  在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="pvup003a0h2scp"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **说明**
>
> 本文的视频超清示例适用于**华北2（北京）地域**。

<a id="http调用"></a>

<a id="pvup101a0h2http"></a>

## HTTP调用

由于视频超清任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="pvup111a0h4stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="pvup123a0h4reqp"></a><h4>请求参数</h4><a id="pvup142a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="pvup154a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。固定值：<code>pixverse/pixverse-upscale</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，包括待超分的视频。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体资源列表。必须包含 1 个视频元素。</p><a id="accordion-元素属性"></a><section><p>元素属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。固定值为：</p><ul><li><code>video_url</code>：视频URL。</li></ul><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>输入视频的URL地址，必须为公网可访问的URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.mp4"></a><a href="https://xxx/xxx.mp4">https://xxx/xxx.mp4</a>。</li></ul><p>视频限制：</p><ul><li>格式：MP4、MOV、WebM。</li><li>分辨率：不支持 4K 及以上分辨率。</li><li>文件大小：不超过 100MB。</li><li>时长：不超过 30 秒。</li></ul></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频生成参数。如设置是否添加水印、随机种子等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为&quot;AI生成&quot;。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="视频超清"></a><section><a id="视频超清-h4"></a><h4>视频超清</h4><p>传入视频文件，输出超分辨率视频。</p><a id="code-block"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-upscale&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;seed&quot;: 12345,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block-2"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

media = [{'type': 'video_url', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250919/wqefue/mix_input_video.mp4'}]

def sample_async_call():
    # 异步提交视频生成任务
    try:
        job = client.videos.jobs.create(model='pixverse/pixverse-upscale',
                                        media=media,
                                        seed=12345,
                                        watermark=True)
        print(job)
        print(&quot;task_id: %s&quot; % job.task_id)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)
        return

    # 查询任务状态
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)

    # 等待任务完成
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f&quot;HTTP返回码：{e.status_code}&quot;)
        print(f&quot;错误码：{e.code}&quot;)
        print(f&quot;错误信息：{e.message}&quot;)
        print(&quot;请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code&quot;)

if __name__ == '__main__':
    sample_async_call()
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="pvup401a0h4stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="pvup424a0h4qr01"></a><h4>请求参数</h4><a id="pvup434a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="pvup440a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-2"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-3"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pvup454a0h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>计费时长（秒）。为用户上传视频时长向上取整。</p><p><strong>size</strong> <code>string</code></p><p>输出视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>输出视频的帧率。</p><p><strong>SR</strong> <code>string</code></p><p>输出视频的分辨率档位。</p><p><strong>video_count</strong> <code>integer</code></p><p>视频数量，固定为 1。</p></div></section></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;19171ea5-9efb-4d35-93a1-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;7ed706b7-a9a9-4319-820c-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-07-14 10:34:41.630&quot;,
        &quot;scheduled_time&quot;: &quot;2026-07-14 10:34:41.655&quot;,
        &quot;end_time&quot;: &quot;2026-07-14 10:35:12.725&quot;,
        &quot;video_url&quot;: &quot;https://media.pixverseai.cn/xxxx.mp4&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 6,
        &quot;size&quot;: &quot;3840*2156&quot;,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: &quot;4K&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;Invalid field type or value. Please verify your input data.&quot;
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

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
