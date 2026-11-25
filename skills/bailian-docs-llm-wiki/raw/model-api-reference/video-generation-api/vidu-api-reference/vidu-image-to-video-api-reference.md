# Vidu-图生视频-基于首帧API参考

Vidu-图生视频模型根据 输入图像 和 文本提示词 ，生成一段流畅的视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

请前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **Vidu**，找到 **Vidu** 模型卡片，单击**立即开通**；在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="1fd78afa5brlj"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="http-title"></a>

## HTTP调用

图生视频任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="step1-title"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="req-header-title"></a><h4>请求参数</h4><a id="req-headers-title"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="req-body-title"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值为：</p><ul><li><code>vidu/viduq3-pro-fast_img2video</code></li><li><code>vidu/viduq3-pro_img2video</code></li><li><code>vidu/viduq3-turbo_img2video</code></li><li><code>vidu/viduq2-pro-fast_img2video</code></li><li><code>vidu/viduq2-pro_img2video</code></li><li><code>vidu/viduq2-turbo_img2video</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词、媒体素材等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> （可选）</p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，字符长度不能超过 5000 个字符，超过部分会自动截断。</p><p>提示词编写请参见<a href="../../../model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md">Vidu视频生成Prompt指南</a>。</p><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体素材列表，用于指定图生视频所需的图像。</p><p>数组的每个元素为一个媒体对象，包含 <code>type</code> 与 <code>url</code> 字段。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体素材类型。固定值为：</p><ul><li><code>image</code>：图像URL。</li></ul><p>素材限制：图像素材有且只有<strong>1张</strong>。</p><p><strong>url</strong> <code>string</code> <strong>（必选）</strong></p><p>图像文件的URL地址，必须为公网可访问的URL。</p><ul><li>支持 HTTP 或 HTTPS 协议。</li><li>示例值：<a href="https://xxx/xxx.jpg"></a><a href="https://xxx/xxx.jpg">https://xxx/xxx.jpg</a>。</li></ul><p>图像限制：</p><ul><li>格式：JPG、JPEG、PNG、WEBP。</li><li>宽高比：1:4～4:1。</li><li>文件大小：不超过50MB。</li></ul></div></section></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置视频分辨率、设置视频时长等。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong>resolution直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e5d1761f12xq3">模型价格</a>。</p></div></div><p>指定生成的视频分辨率档位。</p><p>模型根据选择的分辨率档位，自动缩放至相近总像素，视频宽高比将尽量接近输入图像的宽高比。</p><ul><li>vidu/viduq3-pro-fast_img2video：可选值：720P、1080P。默认值为<code>720P</code>。</li><li>vidu/viduq3-pro_img2video：可选值：540P、720P、1080P。默认值为<code>720P</code>。</li><li>vidu/viduq3-turbo_img2video：可选值：540P、720P、1080P。默认值为<code>720P</code>。</li><li>vidu/viduq2-pro-fast_img2video：可选值：720P、1080P。默认值为<code>720P</code>。</li><li>vidu/viduq2-pro_img2video：可选值：540P、720P、1080P。默认值为<code>720P</code>。</li><li>vidu/viduq2-turbo_img2video：可选值：540P、720P、1080P。默认值为<code>720P</code>。</li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，时间越长费用越高，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#e5d1761f12xq3">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li>vidu/viduq3-pro-fast_img2video：取值为[1, 16]之间的整数，默认值为5。</li><li>vidu/viduq3-pro_img2video：取值为[1, 16]之间的整数，默认值为5。</li><li>vidu/viduq3-turbo_img2video：取值为[1, 16]之间的整数，默认值为5。</li><li>vidu/viduq2-pro-fast_img2video：取值为[1, 10]之间的整数，默认值为5。</li><li>vidu/viduq2-pro_img2video：取值为[1, 10]之间的整数，默认值为5。</li><li>vidu/viduq2-turbo_img2video：取值为[1, 10]之间的整数，默认值为5。</li></ul><p><strong>audio</strong> <code>boolean</code> （可选）</p><p><strong>支持模型</strong>：vidu/viduq3-pro-fast_img2video、vidu/viduq3-pro_img2video、vidu/viduq3-turbo_img2video。</p><p>是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“内容由AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="图生视频"></a><section><a id="图生视频-h4"></a><h4>图生视频</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;vidu/viduq3-pro-fast_img2video&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;image&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp&quot;
            }
        ],
        &quot;prompt&quot;: &quot;镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。&quot;
    },
    &quot;parameters&quot;: {
        &quot;duration&quot;: 5,
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block-2"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

media = [{'type': 'image', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp'}]

def sample_async_call():
    # 异步提交视频生成任务
    try:
        job = client.videos.jobs.create(model='vidu/viduq3-pro-fast_img2video',
                                        media=media,
                                        prompt='镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。',
                                        duration=5,
                                        resolution='720P',
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

<table><tbody><tr><td><a id="64ee5e75edznz"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-3"></a><pre class="language-json"><code>{
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

<table><tbody><tr><td><a id="19f6e90ee5rnq"></a><h4>请求参数</h4><a id="1e961f0eb7gwq"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="96525d350eazf"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时</p><a id="code-block-5"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="9fed9a5bc6zes"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接<strong>有效期24小时</strong>，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>总的视频计费时长（秒）。</p><p><strong>output_video_duration</strong><code>integer</code></p><p>输出视频的时长（秒）。</p><p><strong>size</strong> <code>string</code></p><p>输出视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>输出视频的帧率。固定为24。</p><p><strong>SR</strong> <code>string</code></p><p>输出视频的分辨率档位。</p><p><strong>audio</strong> <code>boolean</code></p><p>输出视频是否为有声视频。</p><p><strong>video_count</strong> <code>integer</code></p><p>输出视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;3606f9f4-b833-44ec-8385-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;2846881f-0496-4288-947f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-27 14:25:32.057&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-27 14:25:32.084&quot;,
        &quot;end_time&quot;: &quot;2026-03-27 14:28:29.600&quot;,
        &quot;orig_prompt&quot;: &quot;镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。&quot;,
        &quot;video_url&quot;: &quot;https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;size&quot;: &quot;990*932&quot;,
        &quot;output_video_duration&quot;: 5,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;audio&quot;: false,
        &quot;SR&quot;: &quot;720&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-7"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-8"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;a4de7c32-7057-9f82-8581-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;502a00b1-19d9-4839-a82f-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;UNKNOWN&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="错误码"></a>

<a id="0d0a562d05nkh"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
