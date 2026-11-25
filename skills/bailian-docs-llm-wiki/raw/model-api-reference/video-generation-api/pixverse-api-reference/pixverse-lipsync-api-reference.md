# 爱诗-视频对口型API参考

爱诗-视频对口型模型支持输入 视频 和 音频 （或 TTS 文本），生成与音频同步的对口型视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="服务开通"></a>

<a id="8bb48973d87d6"></a>

## 服务开通

1.  前往[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 **PixVerse**，找到 PixVerse 模型卡片，单击**立即开通**；
2.  在弹窗内确认开通及授权。

<a id="适用范围"></a>

<a id="pvls003a0h2scp"></a>

## 适用范围

为确保调用成功，请务必保证**模型、Endpoint URL 和 API Key 均属于同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **说明**
>
> 本文的视频对口型示例适用于**华北2（北京）地域**。

<a id="http调用"></a>

<a id="pvls101a0h2http"></a>

## HTTP调用

由于视频对口型任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="pvls111a0h4stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="pvls123a0h4reqp"></a><h4>请求参数</h4><a id="pvls142a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="pvls154a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。固定值：<code>pixverse/pixverse-lipsync</code>。</p><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，包括人脸视频和音频来源。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>media</strong> <code>array</code> <strong>（必选）</strong></p><p>媒体资源列表。必须包含一个 <code>video_url</code> 类型的视频，以及音频来源（二选一）：</p><ul><li><strong>方式一（音频驱动）</strong>：传入 <code>audio_url</code> 类型的音频文件。</li><li><strong>方式二（TTS 合成）</strong>：同时传入 <code>lip_sync_tts_speaker_id</code> 和 <code>lip_sync_tts_content</code>。</li></ul><div><div><p><strong>重要</strong><code>audio_url</code> 与 <code>lip_sync_tts_speaker_id</code> + <code>lip_sync_tts_content</code> 二选一，不允许同时传入。</p></div></div><a id="accordion-元素属性"></a><section><p>元素属性</p><div><p><strong>type</strong> <code>string</code> <strong>（必选）</strong></p><p>媒体类型标识符。取值范围：</p><ul><li><code>video_url</code>：人脸视频。</li><li><code>audio_url</code>：音频文件。</li><li><code>lip_sync_tts_speaker_id</code>：TTS 音色 ID。</li><li><code>lip_sync_tts_content</code>：TTS 文本内容。</li></ul><p><strong>url</strong> <code>string</code> <strong>（条件必选）</strong></p><p>当 type 为 <code>video_url</code> 或 <code>audio_url</code> 时必填。媒体资源的 URL 地址。</p><ul><li><p><code>video_url</code>：输入视频的 URL。视频需包含可用于对口型的人脸画面。</p><ul><li>文件大小：不超过 250MB。</li><li>时长：不超过 300 秒。</li><li>支持格式：MP4、MOV、WebM。</li></ul></li><li><p><code>audio_url</code>：音频文件的 URL。</p><ul><li>文件大小：不超过 100MB。</li><li>时长：不超过 300 秒。</li><li>支持格式：MP3、WAV、M4A、AAC。</li></ul></li></ul><p><strong>id</strong> <code>string</code> <strong>（条件必选）</strong></p><p>当 type 为 <code>lip_sync_tts_speaker_id</code> 时必填。TTS 音色 ID。取值为 <code>auto</code> 时随机选择音色，取值为数字字符串时按音色 ID 指定。支持的取值见下表。</p><a id="accordion-音色取值表"></a><section><p>音色取值表</p><div><table><thead><tr><th><p><strong>id 取值</strong></p></th><th><p><strong>音色名称</strong></p></th></tr></thead><tbody><tr><td><p>auto</p></td><td><p>随机</p></td></tr><tr><td><p>2</p></td><td><p>詹有鱼</p></td></tr><tr><td><p>4</p></td><td><p>外国阿利</p></td></tr><tr><td><p>6</p></td><td><p>李解</p></td></tr><tr><td><p>10</p></td><td><p>姜姜好</p></td></tr><tr><td><p>11</p></td><td><p>老森</p></td></tr><tr><td><p>12</p></td><td><p>李杰克</p></td></tr><tr><td><p>13</p></td><td><p>钱多多</p></td></tr><tr><td><p>14</p></td><td><p>呆萌王小拍</p></td></tr><tr><td><p>16</p></td><td><p>屯里大嗓</p></td></tr><tr><td><p>18</p></td><td><p>豫语汉子</p></td></tr><tr><td><p>19</p></td><td><p>宝岛囡囡</p></td></tr><tr><td><p>20</p></td><td><p>陕西掌柜</p></td></tr><tr><td><p>21</p></td><td><p>港风阿sir</p></td></tr></tbody></table></div></section><p><strong>content</strong> <code>string</code> <strong>（条件必选）</strong></p><p>当 type 为 <code>lip_sync_tts_content</code> 时必填。需要驱动口型的文本内容，支持中英文，不超过 200 字（UTF-8 编码）。</p></div></section></div></section><p><strong>parameters</strong> <code>object</code> <strong>（可选）</strong></p><p>视频生成参数。如设置是否添加水印等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为&quot;AI生成&quot;。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul></div></section></td><td><a id="sec-tabs"></a><section><a id="音频驱动"></a><section><a id="音频驱动-h4"></a><h4>音频驱动</h4><p>传入视频和音频文件，生成对口型视频。</p><a id="code-block"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-lipsync&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4&quot;
            },
            {
                &quot;type&quot;: &quot;audio_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/aumwir/stella2-%E6%9C%89%E5%A3%B0%E4%B9%A67.wav&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;watermark&quot;: true
    }
}'
</code></pre></section><a id="python-sdk"></a><section><a id="python-sdk-h4"></a><h4>Python SDK</h4><a id="code-block-2"></a><pre class="language-python"><code>import dashscope
import os
from dashscope import DashScopeError

# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key=&quot;sk-xxx&quot;
# 获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
client = dashscope.Client(api_key=os.getenv(&quot;DASHSCOPE_API_KEY&quot;))

media = [{'type': 'video_url', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4'}, {'type': 'audio_url', 'url': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/aumwir/stella2-%E6%9C%89%E5%A3%B0%E4%B9%A67.wav'}]

def sample_async_call():
    # 异步提交视频生成任务
    try:
        job = client.videos.jobs.create(model='pixverse/pixverse-lipsync',
                                        media=media,
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
</code></pre></section><a id="tts-文本驱动"></a><section><a id="tts-文本驱动-h4"></a><h4>TTS 文本驱动</h4><p>传入视频和 TTS 文本，由模型合成语音并生成对口型视频。</p><a id="code-block-3"></a><pre class="language-bash"><code># 调用时请将 {WorkspaceId} 替换为真实的业务空间ID。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;pixverse/pixverse-lipsync&quot;,
    &quot;input&quot;: {
        &quot;media&quot;: [
            {
                &quot;type&quot;: &quot;video_url&quot;,
                &quot;url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250717/pvegot/input_video_01.mp4&quot;
            },
            {
                &quot;type&quot;: &quot;lip_sync_tts_speaker_id&quot;,
                &quot;id&quot;: &quot;auto&quot;
            },
            {
                &quot;type&quot;: &quot;lip_sync_tts_content&quot;,
                &quot;content&quot;: &quot;保持热爱持续开心，琐碎小事不值得烦心&quot;
            }
        ]
    },
    &quot;parameters&quot;: {
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="pvls401a0h4stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="pvls424a0h4qr01"></a><h4>请求参数</h4><a id="pvls434a0h5qr01"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="pvls440a0h5qr02"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-2"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="pvls454a0h4qrs1"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接暂无过期时间，但不建议将其作为长期存储，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计。只对成功的结果计数。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>计费时长（秒）。音频驱动方式为音频时长向上取整；TTS 方式为文本字节数（UTF-8）÷ 15 向上取整。</p><p><strong>size</strong> <code>string</code></p><p>输出视频的分辨率。</p><p><strong>fps</strong> <code>integer</code></p><p>输出视频的帧率。</p><p><strong>SR</strong> <code>string</code></p><p>输出视频的分辨率档位。</p><p><strong>video_count</strong> <code>integer</code></p><p>视频数量，固定为 1。</p></div></section></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;ddf8140e-67c6-9e70-8953-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;1acb9d0c-7a63-4ff6-a198-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-07-15 17:01:49.352&quot;,
        &quot;scheduled_time&quot;: &quot;2026-07-15 17:01:49.398&quot;,
        &quot;end_time&quot;: &quot;2026-07-15 17:02:29.724&quot;,
        &quot;video_url&quot;: &quot;https://media.pixverseai.cn/xxxx.mp4&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 7,
        &quot;size&quot;: &quot;1080*1920&quot;,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: &quot;&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;Invalid field type or value. Please verify your input data.&quot;
    }
}
</code></pre></section><a id="任务查询过期"></a><section><a id="任务查询过期-h4"></a><h4>任务查询过期</h4><p>task_id查询有效期为 24 小时，超时后将无法查询，返回以下报错信息。</p><a id="code-block-7"></a><pre class="language-json"><code>{
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
