# Vidu-文生视频API参考

Vidu-文生视频模型基于 文本提示词 ，生成一段流畅的视频。

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
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL或 DashScope SDK URL。
-   **配置 API Key**：选择地域并[获取与配置 API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   **安装 SDK**：如需通过SDK进行调用，请[安装DashScope SDK](../../preparations/install-sdk.md)。

<a id="http调用"></a>

<a id="vd101a0h2http"></a>

## HTTP调用

由于文生视频任务耗时较长（通常为1-5分钟），API采用异步调用。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="vd111a0h4stp1"></a>

### 步骤1：创建任务获取任务ID

**北京地域**：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="vd123a0h4reqp"></a><h4>请求参数</h4><a id="vd142a0h5hdr1"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="vd163a0h5body"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。可选值为：</p><ul><li><code>vidu/viduq3-pro_text2video</code></li><li><code>vidu/viduq3-turbo_text2video</code></li><li><code>vidu/viduq2_text2video</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>输入的基本信息，如提示词等。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词。用来描述生成视频中期望包含的元素和视觉特点。</p><p>支持中英文，每个汉字/字母占一个字符，字符长度不能超过 5000 个字符，超过部分会自动截断。</p><p>示例值：一只小猫在月光下奔跑。</p><p>提示词编写请参见<a href="../../../model-user-guide/use-cases/third-party-model-integration-tutorial/vidu-video-generation-prompt-guide.md">Vidu视频生成Prompt指南</a>。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频生成参数，如设置视频分辨率、时长等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><div><div><p><strong>重要</strong>resolution直接影响费用，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#2143d64593wck">模型价格</a>。</p></div></div><p>分辨率档位。可选值：</p><ul><li><code>540P</code></li><li><code>720P</code>：默认值。</li><li><code>1080P</code></li></ul><p><strong>size</strong> <code>string</code> （可选）</p><p>生成视频的分辨率，格式为<code>宽*高</code>的像素值。</p><p>默认值根据<code>resolution</code>而定：</p><ul><li>当 resolution=540P 时，size 默认为<code>1024*576</code>。</li><li>当 resolution=720P 时，size 默认为<code>1280*720</code>。</li><li>当 resolution=1080P 时，size 默认为<code>1920*1080</code>。</li></ul><table><tbody><tr><td><p>分辨率档位</p></td><td><p>宽高比</p></td><td><p><strong>size取值（宽*高）</strong></p></td></tr><tr><td rowspan="5"><p>540P</p></td><td><p>16:9</p></td><td><p>1024*576</p></td></tr><tr><td><p>9:16</p></td><td><p>576*1024</p></td></tr><tr><td><p>1:1</p></td><td><p>1024*1024</p></td></tr><tr><td><p>4:3</p></td><td><p>1024*768</p></td></tr><tr><td><p>3:4</p></td><td><p>768*1024</p></td></tr><tr><td rowspan="5"><p>720P</p></td><td><p>16:9</p></td><td><p>1280*720</p></td></tr><tr><td><p>9:16</p></td><td><p>720*1280</p></td></tr><tr><td><p>1:1</p></td><td><p>1280*1280</p></td></tr><tr><td><p>4:3</p></td><td><p>1280*960</p></td></tr><tr><td><p>3:4</p></td><td><p>960*1280</p></td></tr><tr><td rowspan="5"><p>1080P</p></td><td><p>16:9</p></td><td><p>1920*1080</p></td></tr><tr><td><p>9:16</p></td><td><p>1080*1920</p></td></tr><tr><td><p>1:1</p></td><td><p>1808*1808</p></td></tr><tr><td><p>4:3</p></td><td><p>1920*1440</p></td></tr><tr><td><p>3:4</p></td><td><p>1440*1920</p></td></tr></tbody></table><p><strong>duration</strong> <code>integer</code>（可选）</p><div><div><p><strong>重要</strong>duration直接影响费用，按秒计费，时间越长费用越高，请在调用前确认<a href="../../../model-user-guide/test-1/model-pricing.md#2143d64593wck">模型价格</a>。</p></div></div><p>生成视频的时长，单位为秒。</p><ul><li>vidu/viduq3-pro_text2video、vidu/viduq3-turbo_text2video：取值为[1, 16]之间的整数，默认值为5。</li><li>vidu/viduq2_text2video：取值为[1, 10]之间的整数，默认值为5。</li></ul><p><strong>audio</strong> <code>boolean</code> （可选）</p><p><strong>支持模型</strong>：vidu/viduq3-pro_text2video、vidu/viduq3-turbo_text2video。</p><p>是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。</p><ul><li><code>false</code>：默认值，输出无声视频。</li><li><code>true</code>：输出有声视频。</li></ul><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否添加水印标识，水印位于视频右下角，文案固定为“内容由AI生成”。</p><ul><li><code>false</code>：默认值，不添加水印。</li><li><code>true</code>：添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs"></a><section><a id="文生视频"></a><section><a id="文生视频-h4"></a><h4>文生视频</h4><a id="code-block"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;vidu/viduq3-turbo_text2video&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一只小猫在月光下奔跑&quot;
    },
    &quot;parameters&quot;: {
        &quot;size&quot;: &quot;1024*576&quot;,
        &quot;resolution&quot;: &quot;540P&quot;,
        &quot;duration&quot;: 5,
        &quot;watermark&quot;: true
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="64ee5e75edznz"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-2"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-2"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
        &quot;task_status&quot;: &quot;PENDING&quot;,
        &quot;task_id&quot;: &quot;0385dc79-5ff8-4d82-bcb6-xxxxxx&quot;
    },
    &quot;request_id&quot;: &quot;4909100c-7b5a-9f92-bfe5-xxxxxx&quot;
}
</code></pre></section><a id="异常响应"></a><section><a id="异常响应-h4"></a><h4>异常响应</h4><p>创建任务失败，请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;code&quot;: &quot;InvalidApiKey&quot;,
    &quot;message&quot;: &quot;No API-key provided.&quot;,
    &quot;request_id&quot;: &quot;7438d53d-6eb8-4596-8835-xxxxxx&quot;
}
</code></pre></section></section></td></tr></tbody></table>

<a id="步骤2-根据任务id查询结果"></a>

<a id="vd401a0h4stp2"></a>

### 步骤2：根据任务ID查询结果

**北京地域**：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="19f6e90ee5rnq"></a><h4>请求参数</h4><a id="1e961f0eb7gwq"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="96525d350eazf"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-3"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时</p><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="9fed9a5bc6zes"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>视频格式为MP4（H.264 编码）。视频链接有效期<strong>24小时</strong>，请及时下载。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>duration</strong> <code>integer</code></p><p>总的视频计费时长（秒）。示例值：5。</p><p><strong>output_video_duration</strong><code>integer</code></p><p>输出视频的时长（秒）。示例值：5。</p><p><strong>size</strong> <code>string</code></p><p>生成视频的分辨率。示例值：960*528。</p><p><strong>fps</strong> <code>integer</code></p><p>生成视频的帧率。示例值：24。</p><p><strong>SR</strong> <code>string</code></p><p>生成视频的分辨率档位。示例值：540。</p><p><strong>audio</strong> <code>boolean</code></p><p>生成视频是否为有声视频。示例值：false。</p><p><strong>video_count</strong> <code>integer</code></p><p>生成视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-4"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;eda50dad-a6d3-4e62-a70b-26bbb797ae81&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;d9254244-1f9b-4b4c-be82-d9560ba25708&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-03-27 13:32:13.962&quot;,
        &quot;scheduled_time&quot;: &quot;2026-03-27 13:32:14.008&quot;,
        &quot;end_time&quot;: &quot;2026-03-27 13:32:43.375&quot;,
        &quot;orig_prompt&quot;: &quot;一只小猫在月光下奔跑&quot;,
        &quot;video_url&quot;: &quot;https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;size&quot;: &quot;960*528&quot;,
        &quot;output_video_duration&quot;: 5,
        &quot;fps&quot;: 24,
        &quot;video_count&quot;: 1,
        &quot;audio&quot;: false,
        &quot;SR&quot;: &quot;540&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The size is not match xxxxxx&quot;
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

<a id="dashscope-sdk调用"></a>

<a id="vd601a0h2sdk1"></a>

## DashScope SDK调用

SDK 的参数命名与[HTTP接口](vidu-text-to-video-api-reference.md#vd101a0h2http)基本一致，参数结构根据语言特性进行封装。

由于文生视频任务耗时较长（通常为1-5分钟），SDK 在底层封装了 HTTP 异步调用流程，支持同步、异步两种调用方式。

> 具体耗时受限于排队任务数和服务执行情况，请在获取结果时耐心等待。

<a id="python-sdk调用"></a>

<a id="vd607a0h3pyth"></a>

### Python SDK调用

> **重要**
>
> 请确保 DashScope Python SDK 版本**不低于**2.0.1，再运行以下代码。

**北京地域**：`region="cn-beijing"`

<a id="sec-tabs-5"></a>

<a id="同步调用"></a>

<a id="同步调用-h4"></a>

#### 同步调用

<a id="vd626a0h5syn1"></a>

##### 请求示例

<a id="code-block-8"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_sync_call_t2v():
    # call sync api, will return the result
    print('please wait...')
    # generate 为一步式调用（提交任务并等待完成），返回已完成的 Job
    try:
        job = client.videos.generate(model='vidu/viduq3-turbo_text2video',
                                     prompt='一只小猫在月光下奔跑',
                                     size='1024*576',
                                     duration=5,
                                     resolution='540P',
                                     watermark=True)
        print(job)
        print(job.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_sync_call_t2v()
```

<a id="vd628a0h5syn2"></a>

##### 响应示例

> `video_url`24小时内有效，请及时下载。

<a id="code-block-9"></a>

```json
{
    "request_id": "15bd86e5-28b1-40ad-a427-xxxxxx",
    "task_id": "a876c6ee-1c63-4d17-b6c0-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 5,
        "size": "960*528",
        "output_video_duration": 5,
        "fps": 24,
        "audio": false,
        "SR": "540"
    }
}
```

<a id="异步调用"></a>

<a id="异步调用-h4"></a>

#### 异步调用

<a id="vd637a0h5asy1"></a>

##### 请求示例

<a id="code-block-10"></a>

```python
import os
import dashscope
from dashscope import DashScopeError

# 以下为华北2（北京）地域的配置。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的region取值不同。
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

def sample_async_call_t2v():
    # call async api, will return the task information
    try:
        job = client.videos.jobs.create(model='vidu/viduq3-turbo_text2video',
                                        prompt='一只小猫在月光下奔跑',
                                        size='1024*576',
                                        duration=5,
                                        resolution='540P')
        print(job)
        print("task_id: %s" % job.task_id)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        return

    # get the task information include the task status.
    try:
        snapshot = client.videos.jobs.fetch(job.task_id)
        print(snapshot.status)  # check the task status
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    # wait the task complete
    try:
        done = client.videos.jobs.wait(job)
        print(done)
        print(done.video_url)
    except DashScopeError as e:
        print(f"HTTP返回码：{e.status_code}")
        print(f"错误码：{e.code}")
        print(f"错误信息：{e.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

if __name__ == '__main__':
    sample_async_call_t2v()
```

<a id="vd639a0h5asy2"></a>

##### 响应示例

1、创建任务的响应示例

<a id="code-block-11"></a>

```json
{
	"request_id": "c86ff7ba-8377-917a-90ed-xxxxxx",
	"task_id": "721164c6-8619-4a35-a6d9-xxxxxx",
	"status": "PENDING"
}
```

2、查询任务结果的响应示例

> `video_url` 24小时内有效，请及时下载。

<a id="code-block-12"></a>

```json
{
    "request_id": "15bd86e5-28b1-40ad-a427-xxxxxx",
    "task_id": "a876c6ee-1c63-4d17-b6c0-xxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 1,
        "FAILED": 0
    },
    "usage": {
        "video_count": 1,
        "video_duration": 0,
        "video_ratio": "",
        "duration": 5,
        "size": "960*528",
        "output_video_duration": 5,
        "fps": 24,
        "audio": false,
        "SR": "540"
    }
}
```

<a id="java-sdk调用"></a>

<a id="vd649a0h3java"></a>

### Java SDK调用

> **重要**
>
> 请确保 DashScope Java SDK 版本**不低于**`2.22.6`，再运行以下代码。

**北京地域**：`Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";`

<a id="sec-tabs-6"></a>

<a id="同步调用-2"></a>

<a id="同步调用-2-h4"></a>

#### 同步调用

<a id="vd659a0h5syn3"></a>

##### 请求示例

<a id="code-block-13"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Text2Video {

    static {
        // 以下为北京地域URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("vidu/viduq3-turbo_text2video")
                        .prompt("一只小猫在月光下奔跑")
                        .size("1024*576")
                        .resolution("540P")
                        .duration(5)
                        .watermark(true)
                        .build();
        System.out.println("please wait...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            text2Video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="vd661a0h5syn4"></a>

##### 响应示例

> `video_url` 24小时内有效，请及时下载。

<a id="code-block-14"></a>

```json
{
    "request_id": "bebc5f6b-a081-4b02-ad29-xxxxxx",
    "output": {
        "task_id": "2b0e287f-ebdc-49af-82aa-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/infer_92/xxx.mp4?xxx",
        "orig_prompt": "一只小猫在月光下奔跑",
        "submit_time": "2026-03-30 10:19:00.827",
        "scheduled_time": "2026-03-30 10:19:00.879",
        "end_time": "2026-03-30 10:19:28.172"
    },
    "usage": {
        "video_count": 1,
        "duration": 5.0,
        "size": "960*528",
        "input_video_duration": 0.0,
        "output_video_duration": 5.0,
        "SR": "540"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="异步调用-2"></a>

<a id="异步调用-2-h4"></a>

#### 异步调用

<a id="vd670a0h5asy3"></a>

##### 请求示例

<a id="code-block-15"></a>

```java
// Copyright (c) Alibaba, Inc. and its affiliates.

import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Text2Video {

    static {
        // 以下为北京地域URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }

    // 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
     * Create a video compositing task and wait for the task to complete.
     */
    public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();

        VideoSynthesisParam param =
                VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("vidu/viduq3-turbo_text2video")
                        .prompt("一只小猫在月光下奔跑")
                        .size("1024*576")
                        .resolution("540P")
                        .duration(5)
                        .watermark(true)
                        .build();

        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        //获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
        try {
            text2Video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

<a id="vd672a0h5asy4"></a>

##### 响应示例

1、创建任务的响应示例。

<a id="code-block-16"></a>

```json
{
    "request_id": "9b583f1b-2423-4fac-bb3f-xxxxxx",
    "output": {
        "task_id": "3944b819-1bbb-4da0-a230-xxxxxx",
        "task_status": "PENDING"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

2、查询任务结果的响应示例

> `video_url` 24小时内有效，请及时下载。

<a id="code-block-17"></a>

```json
{
    "request_id": "bebc5f6b-a081-4b02-ad29-xxxxxx",
    "output": {
        "task_id": "2b0e287f-ebdc-49af-82aa-xxxxxx",
        "task_status": "SUCCEEDED",
        "video_url": "https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/infer_92/xxx.mp4?xxx",
        "orig_prompt": "一只小猫在月光下奔跑",
        "submit_time": "2026-03-30 10:19:00.827",
        "scheduled_time": "2026-03-30 10:19:00.879",
        "end_time": "2026-03-30 10:19:28.172"
    },
    "usage": {
        "video_count": 1,
        "duration": 5.0,
        "size": "960*528",
        "input_video_duration": 0.0,
        "output_video_duration": 5.0,
        "SR": "540"
    },
    "status_code": 200,
    "code": "",
    "message": ""
}
```

<a id="错误码"></a>

<a id="0d0a562d05nkh"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="常见问题"></a>

<a id="a0379eaad3lho"></a>

## 常见问题

<a id="q-size-与-resolution-必须同时传入吗"></a>

<a id="d64acbbcf61fn"></a>

#### Q：size 与 resolution 必须同时传入吗？

**A：** 不必。二者均为可选参数，但**推荐同时传入**。同时传入可精准控制生成视频的宽高比，具体参见[size取值](vidu-text-to-video-api-reference.md)。

若不同时传入，系统将按以下两种场景处理：

-   **仅传 size**：size参数会被忽略，系统强制按默认的 `resolution=720P` 及其对应的`size`默认值（`1280*720`）处理。
    
    > 例如：接口返回为size="1280\*720", SR=720。
    
-   **仅传 resolution**：按指定分辨率档位及该档位对应的 16:9 比例输出。
    
    > 例如：当resolution=540P时，接口返回 size="960_528", SR=540；当resolution=1080P时，接口返回 size="1920_1080", SR=1080。
