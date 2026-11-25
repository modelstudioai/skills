# 视频风格重绘API参考

视频风格重绘 API 可将输入视频转换为多种预设艺术风格，并保证画面动态流畅、内容连贯。支持8种预设风格：日式漫画、美式漫画、清新漫画、3D卡通、国风卡通、纸艺风格、简易插画、国风水墨。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="效果示意"></a>

<a id="95fb1121df2gl"></a>

## 效果示意

| 输入视频 | 输出视频（日式漫画） |
| --- | --- |
|  |  |

更多案例请参见[附录：更多风格效果示意](video-style-transform-api-reference.md#a45f4df85e6h7)。

<a id="前提条件"></a>

<a id="3b14076a680k8"></a>

## 前提条件

在调用前，您需要[获取 API Key](../../preparations/get-api-key.md)，再[配置API Key为环境变量DASHSCOPE\_API\_KEY](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

<a id="http调用"></a>

<a id="aDbIs"></a>

## HTTP调用

因视频处理耗时长，为避免同步请求超时，视频风格重绘采用异步调用，分为以下两步：

1.  **提交异步任务**：通过 `POST` 请求提交原始视频 URL 和期望的风格参数，获取一个唯一的 `task_id`。
2.  **查询任务结果**：使用 `task_id` 通过 `GET` 请求轮询任务状态，直至任务完成并获取结果视频的 URL。

<a id="步骤1-提交视频风格重绘任务"></a>

<a id="bepIa"></a>

### 步骤1：提交视频风格重绘任务

<a id="code-block"></a>

```bash
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

<table><tbody><tr><td><a id="afcd41d2b57zf"></a><h4>请求</h4><a id="d11205db082b6"></a><h5>请求头（Headers）</h5><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="66a778d4fbfub"></a><h5>请求体（Request Body）</h5><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。设置为<code>video-style-transform</code>。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入内容。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>video_url</strong><code>string</code><strong>（必选）</strong></p><p>输入视频公网URL。例如：<code>https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4</code>。</p><p>输入视频要求：</p><ul><li><strong>分辨率</strong>：视频单边尺寸不小于 256 像素，不超过 4096 像素。长边与短边的比例不超过 1.8。</li><li><strong>格式</strong>：支持 MP4、AVI、MKV、MOV、FLV、TS、MPG、MXF。</li><li><strong>时长</strong>：不超过 30 秒。</li><li><strong>大小</strong>：不超过 100 MB。</li><li><strong>URL</strong>：若原始URL包含中文字符等非ASCII字符，请先进行URL编码。</li></ul></div></section><p><strong>parameters</strong><code>object</code> <strong>（可选）</strong></p><p>视频处理参数。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>style</strong><code>int</code><strong>（可选）</strong></p><p>风格类型，预设类型如下：</p><ul><li>0：日式漫画，默认值</li><li>1：美式漫画</li><li>2：清新漫画</li><li>3：3D卡通</li><li>4：国风卡通（古装输入最佳）</li><li>5：纸艺风格</li><li>6：简易插画</li><li>7：国风水墨</li></ul><p><strong>video_fps</strong><code>int</code><strong>（可选）</strong></p><p>生成视频的帧率，默认为15，范围区间为[15, 25]。</p><p><strong>animate_emotion</strong><code>bool</code><strong>（可选）</strong></p><p>是否进行面部表情优化。默认为<code>true</code>。</p><p>开启后，通常能提升口型与表情同步精度。在人脸区域占比较小时，关闭此项可能效果更佳。</p><p><strong>min_len</strong><code>int</code><strong>（可选）</strong></p><p>指定输出视频的短边像素，用于控制分辨率。可选值为<code>720</code>或<code>540</code>，默认为<code>720</code>。</p><div><div><p><strong>说明</strong>此参数值影响计费，720P视频的费用会高于540P。详情请参见<a href="video-style-transform-api-reference.md#34ab17504ad65">计费与限流</a>。</p></div></div><p><strong>use_SR</strong><code>bool</code><strong>（可选）</strong></p><p>是否对风格重绘后视频进行超分辨率（Super-Resolution，SR）处理。默认为<code>false</code>。设置为<code>true</code>，将免费提升画质。</p><div><div><p><strong>说明</strong>若<code>min_len</code>设置为540，开启此项后，输出视频将提升至1080P画质，但计费仍按照540P标准。这会增加处理耗时，推荐在需要高画质输出时开启。</p></div></div></div></section></td><td><a id="sec-tabs"></a><section><a id="生成720p视频"></a><section><a id="生成720p视频-h4"></a><h4>生成720P视频</h4><a id="fig-code-group"></a><div><a id="fig-code-group-bash-tab"></a>bash<div><a id="code-code-group-bash"></a><pre class="language-bash"><code>curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;video-style-transform&quot;,
    &quot;input&quot;: {
        &quot;video_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4&quot;
    },
    &quot;parameters&quot;: {
        &quot;style&quot;: 0,
        &quot;video_fps&quot;: 15
    }
}'
</code></pre></div><a id="fig-code-group-python-tab"></a>python<div><a id="code-code-group-python"></a><pre class="language-python"><code>import requests
import os

DASHSCOPE_API_KEY = os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
# 替换为你的视频 URL
video_url = &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4&quot;

response = requests.post(
            &quot;https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis&quot;,
            headers={
                &quot;Authorization&quot;: f&quot;Bearer {DASHSCOPE_API_KEY}&quot;,
                &quot;X-DashScope-Async&quot;: &quot;enable&quot;,
            },
            json={
            &quot;model&quot;: &quot;video-style-transform&quot;,
            &quot;input&quot;: {
                &quot;video_url&quot;: video_url
            },
            &quot;parameters&quot;: {
                &quot;style&quot;: 0,
                &quot;video_fps&quot;: 15
            }
        }
        )
print(response.json())
</code></pre></div></div></section><a id="生成540p视频"></a><section><a id="生成540p视频-h4"></a><h4>生成540P视频</h4><a id="fig-code-group-2"></a><div><a id="fig-code-group-2-bash-tab"></a>bash<div><a id="code-code-group-2-bash"></a><pre class="language-bash"><code>curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
--header 'Content-Type: application/json' \
--data '{
    &quot;model&quot;: &quot;video-style-transform&quot;,
    &quot;input&quot;: {
        &quot;video_url&quot;: &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4&quot;
    },
    &quot;parameters&quot;: {
        &quot;style&quot;: 0,
        &quot;video_fps&quot;: 15,
        &quot;min_len&quot;: 540
    }
}'
</code></pre></div><a id="fig-code-group-2-python-tab"></a>python<div><a id="code-code-group-2-python"></a><pre class="language-python"><code>import requests
import os

DASHSCOPE_API_KEY = os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
# 替换为你的视频 URL
video_url = &quot;https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250704/viwndw/%E5%8E%9F%E8%A7%86%E9%A2%91.mp4&quot;

response = requests.post(
            &quot;https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis&quot;,
            headers={
                &quot;Authorization&quot;: f&quot;Bearer {DASHSCOPE_API_KEY}&quot;,
                &quot;X-DashScope-Async&quot;: &quot;enable&quot;,
            },
            json={
            &quot;model&quot;: &quot;video-style-transform&quot;,
            &quot;input&quot;: {
                &quot;video_url&quot;: video_url
            },
            &quot;parameters&quot;: {
                &quot;style&quot;: 0,
                &quot;video_fps&quot;: 15,
                &quot;min_len&quot;: 540
            }
        }
        )
print(response.json())
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="9ea3a66e2a0uv"></a><h4>响应</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>任务id，任务的唯一标识，用于后续查询。</p><p><strong>task_status</strong><code>string</code></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li></ul></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="fig-code-group-3"></a><div><a id="fig-code-group-3-成功响应-tab"></a>成功响应<div><a id="code-code-group-3-成功响应"></a><pre class="language-json"><code>{
    &quot;output&quot;: {
	  &quot;task_id&quot;: &quot;xxxxxxxx&quot;,
          &quot;task_status&quot;: &quot;PENDING&quot;
    },
    &quot;request_id&quot;: &quot;7574ee8f-38a3-4b1e-9280-11c33ab46e51&quot;
}
</code></pre></div><a id="fig-code-group-3-异常响应-tab"></a>异常响应<div><a id="code-code-group-3-异常响应"></a><pre class="language-json"><code>{
    &quot;code&quot;:&quot;InvalidApiKey&quot;,
    &quot;message&quot;:&quot;Invalid API-key provided.&quot;,
    &quot;request_id&quot;:&quot;fb53c4ec-1c12-4fc4-a580-xxxxxxxxxxxx&quot;
}
</code></pre></div></div></td></tr></tbody></table>

<a id="步骤2-查询任务执行状态和结果"></a>

<a id="1c5471b844yvg"></a>

### 步骤2：查询任务执行状态和结果

<a id="code-block-2"></a>

```bash
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

> **重要**
>
> 任务结果数据（如任务状态、生成的视频URL等）有效期为24小时，超时后会被自动清除。请务必及时查询并保存结果。

<table><tbody><tr><td><a id="5043fa882c26r"></a><h4>请求</h4><a id="2af8ee144dwd5"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="aa6a7e4730pr2"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><p>任务id。</p></td><td><a id="sec-tabs-2"></a><section><a id="获取任务结果"></a><section><a id="获取任务结果-h4"></a><h4>获取任务结果</h4><p>您需要将<code>{task_id}</code>替换为真实的<code>task_id</code>。</p><a id="fig-code-group-4"></a><div><a id="fig-code-group-4-bash-tab"></a>bash<div><a id="code-code-group-4-bash"></a><pre class="language-bash"><code>curl -X GET \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
</code></pre></div><a id="fig-code-group-4-python-tab"></a>python<div><a id="code-code-group-4-python"></a><pre class="language-python"><code>import requests
import os

DASHSCOPE_API_KEY = os.getenv(&quot;DASHSCOPE_API_KEY&quot;)
# task_id 请替换为你的 task_id
task_id = &quot;0c9c33e6-b2e7-41e5-*********&quot;

task_response = requests.get(
        f&quot;https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}&quot;,
        headers={
            &quot;Authorization&quot;: f&quot;Bearer {DASHSCOPE_API_KEY}&quot;
        })
print(task_response.json())
</code></pre></div></div></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="b14ec019d4k6f"></a><h4>响应</h4><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>output_video_url</strong><code>string</code></p><p>结果视频URL地址。例如：<code>http://xxx/result.mp4</code>。</p><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong><code>string</code></p><p>任务状态。</p><ul><li>PENDING：排队中</li><li>RUNNING：处理中</li><li>SUSPENDED：挂起</li><li>SUCCEEDED：执行成功</li><li>FAILED：执行失败</li><li>UNKNOWN：任务不存在或状态未知。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong><code>object</code></p><p>输出信息统计。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>duration</strong><code>float</code></p><p>生成视频时长（秒）。</p><p><strong>SR</strong><code>int</code></p><p>用于计费的视频短边像素值（该值与您请求中设置的<strong>min_len</strong>值相同）。</p></div></section></td><td><a id="sec-tabs-3"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;b67df059-ca6a-9d51-afcd-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;d76ec1e8-ea27-4038-8913-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2024-05-16 13:50:01.247&quot;,
        &quot;scheduled_time&quot;: &quot;2024-05-16 13:50:01.354&quot;,
        &quot;end_time&quot;: &quot;2024-05-16 13:50:27.795&quot;,
        &quot;output_video_url&quot;: &quot;http://xxx/result.mp4&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 3,
        &quot;SR&quot;: 720
    }
}
</code></pre></section><a id="任务执行中"></a><section><a id="任务执行中-h4"></a><h4>任务执行中</h4><p>任务提交后将处于排队状态，在得到调度之后将转为运行状态，此时任务的状态为RUNNING；</p><a id="code-block-4"></a><pre class="language-json"><code>{
    &quot;request_id&quot;:&quot;e5d70b02-ebd3-98ce-9fe8-xxxxxxxxxxxx&quot;,
    &quot;output&quot;:{
        &quot;task_id&quot;:&quot;13b1848b-5493-4c0e-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;:&quot;RUNNING&quot;,
        &quot;submit_time&quot;:&quot;2025-09-08 15:53:13.143&quot;,
        &quot;scheduled_time&quot;:&quot;2025-09-08 15:53:13.169&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;dccfdf23-b38e-97a6-a07b-xxxxxxxxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;4cbabbdf-2c1f-43f4-b983-xxxxxxxxxxxx&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;submit_time&quot;: &quot;2024-05-16 14:15:14.103&quot;,
        &quot;scheduled_time&quot;: &quot;2024-05-16 14:15:14.154&quot;,
        &quot;end_time&quot;: &quot;2024-05-16 14:15:14.694&quot;,
        &quot;code&quot;: &quot;InvalidParameter.FileDownload&quot;,
        &quot;message&quot;: &quot;download for input video error&quot;
    }
}
</code></pre></section></section></td></tr></tbody></table>

<a id="计费与限流"></a>

<a id="34ab17504ad65"></a>

## 计费与限流

仅对**执行成功**的任务计费，费用根据输出视频的实际时长（秒）和所选分辨率计算。

**计费公式**：`总费用 = 输出视频时长 (秒) × 对应分辨率的单价`（**最终费用将严格按照任务成功后返回的**`usage`**对象中的**`duration`**和**`SR`**字段进行结算**）

免费额度按输出视频时长进行抵扣，不区分视频分辨率。

<table><thead><tr><th rowspan="2"><p><strong>模型名</strong></p></th><th rowspan="2"><p><strong>免费额度</strong><a href="../../../model-user-guide/test-1/new-free-quota.md">（查看）</a></p></th><th rowspan="2" colspan="2"><p><strong>计费单价</strong></p></th><th colspan="2"><p><strong>限流（主账号与RAM子账号共用）</strong></p></th></tr><tr><th><p><strong>任务下发接口QPS限制</strong></p></th><th><p><strong>同时处理中任务数量</strong></p></th></tr></thead><tbody><tr><td rowspan="2"><p>video-style-transform</p></td><td rowspan="2"><p>600秒</p></td><td><p>720P</p></td><td><p>0.5元/秒</p></td><td rowspan="2"><p>2</p></td><td rowspan="2"><p>1</p></td></tr><tr><td><p>540P</p></td><td><p>0.2元/秒</p></td></tr></tbody></table>

**计费示例**

假设您提交一个 10 秒的视频，选择 720P 分辨率进行风格转换，任务成功后生成的视频时长为 10 秒。则本次任务费用为：`10 秒 × 0.5 元/秒 = 5 元`。

<a id="错误码"></a>

<a id="OajFO"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。

<a id="附录-更多风格效果示意"></a>

<a id="a45f4df85e6h7"></a>

## 附录：更多风格效果示意

| 风格名称 | 原始视频 | 重绘效果 |
| --- | --- | --- |
| **日式漫画（style=0）** |  |  |
| **美式漫画（style=1）** |  |  |
| **清新漫画（style=2）** |  |  |
| **3D卡通（style=3）** |  |  |
| **国风卡通（style=4）** |  |  |
| **纸艺风格（style=5）** |  |  |
| **简易插画（style=6）** |  |  |
| **国风水墨（style=7）** |  |  |
