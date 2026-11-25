# HappyHorse-文生视频API参考

HappyHorse文生视频模型，输入文本提示词生成物理真实、运动流畅的视频内容。

<a id="适用范围"></a>

<a id="hh01scope-title"></a>

## 适用范围

为确保调用成功，请务必保证模型、endpoint URL 和 API Key 均属于**同一地域**。跨地域调用将会失败。

-   [**选择模型**](https://bailian.console.aliyun.com/cn-beijing/model/market)：确认模型所属的地域。
-   **选择 URL**：选择对应的地域 Endpoint URL，支持HTTP URL。
-   **配置 API Key**：获取该地域的[API Key](../../preparations/get-api-key.md)，再[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。

> **说明**
>
> 本文的示例代码适用于**华北2（北京）地域**。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，**能够为推理请求提供卓越的性能和更高的稳定性**，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `https://dashscope.aliyuncs.com` 迁移至 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `https://dashscope-intl.aliyuncs.com` 迁移至 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`
>
> 其中 `{WorkspaceId}` 为您的业务空间 ID，可在阿里云百炼控制台的**业务空间详情**页面查看。现有域名仍可正常使用。

<a id="http调用"></a>

<a id="hh01http-title"></a>

## HTTP调用

文生视频任务耗时较长（通常为1-5分钟），API采用异步调用的方式。整个流程包含 **"创建任务 -> 轮询获取"** 两个核心步骤，具体如下：

<a id="步骤1-创建任务获取任务id"></a>

<a id="hh01step1-title"></a>

### 步骤1：创建任务获取任务ID

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="美国-弗吉尼亚"></a>

<a id="美国-弗吉尼亚-h4"></a>

#### 美国（弗吉尼亚）

`POST https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="德国-法兰克福"></a>

<a id="德国-法兰克福-h4"></a>

#### 德国（法兰克福）

`POST https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

<a id="日本-东京"></a>

<a id="日本-东京-h4"></a>

#### 日本（东京）

`POST https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **说明**
>
> -   创建成功后，使用接口返回的 `task_id` 查询结果，task\_id 有效期为 24 小时。**请勿重复创建任务**，轮询获取即可。
> -   新手指引请参见[Postman](https://help.aliyun.com/zh/model-studio/first-call-to-image-and-video-api)。

<table><tbody><tr><td><a id="hh01req-header-h4"></a><h4>请求参数</h4><p><strong>Content-Type</strong><code>string</code><strong>（必选）</strong></p><p>请求内容类型。此参数必须设置为<code>application/json</code>。</p><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><p><strong>X-DashScope-Async</strong><code>string</code><strong>（必选）</strong></p><p>异步处理配置参数。HTTP请求只支持异步，<strong>必须设置为</strong><code>enable</code>。</p><div><div><p><strong>重要</strong>缺少此请求头将报错：“current user api does not support synchronous calls”。</p></div></div><a id="hh01req-body-h5"></a><h5>请求体（Request Body）</h5><p><strong>model</strong> <code>string</code> <strong>（必选）</strong></p><p>模型名称。</p><p>可选值：</p><ul><li><code>happyhorse-1.1-t2v</code></li><li><code>happyhorse-1.0-t2v</code></li></ul><p><strong>input</strong> <code>object</code> <strong>（必选）</strong></p><p>模型的输入信息。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>prompt</strong> <code>string</code> <strong>（必选）</strong></p><p>文本提示词，用于描述期望生成的视频内容。</p><p>支持任何语言输入，长度不超过5000个非中文字符或2500个中文字符，超过部分将自动截断。</p></div></section><p><strong>parameters</strong> <code>object</code> （可选）</p><p>视频处理参数，如设置视频分辨率、设置视频时长等。</p><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>resolution</strong> <code>string</code> （可选）</p><p>指定生成视频的分辨率档位。</p><p>可选值：</p><ul><li><code>480P</code></li><li><code>720P</code></li><li><code>1080P</code>：默认值。</li></ul><p><strong>ratio</strong> <code>string</code> （可选）</p><p>指定生成视频的宽高比。</p><p>可选值：</p><ul><li><code>16:9</code>：默认值。</li><li><code>9:16</code></li><li><code>1:1</code></li><li><code>4:3</code></li><li><code>3:4</code></li><li><code>4:5</code></li><li><code>5:4</code></li><li><code>9:21</code></li><li><code>21:9</code></li></ul><p><strong>duration</strong> <code>integer</code> （可选）</p><p>指定生成视频的时长，单位为秒。</p><p>取值为[3, 15]之间的整数。默认值为<code>5</code>。</p><p><strong>watermark</strong> <code>boolean</code> （可选）</p><p>是否在生成的视频上添加水印标识。水印位于视频右下角，文案固定为“Happy Horse”。</p><ul><li><code>true</code>：默认值，添加水印。</li><li><code>false</code>：不添加水印。</li></ul><p><strong>seed</strong><code>integer</code>（可选）</p><p>随机数种子，取值范围为<code>[0, 2147483647]</code>。</p><p>未指定时，系统自动生成随机种子。若需提升生成结果的可复现性，建议固定seed值。</p><p>请注意，由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。</p></div></section></td><td><a id="sec-tabs-2"></a><section><a id="文生视频"></a><section><a id="文生视频-h4"></a><h4>文生视频</h4><a id="code-block"></a><pre class="language-bash"><code># 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
    -H 'Content-Type: application/json' \
    -d '{
    &quot;model&quot;: &quot;happyhorse-1.1-t2v&quot;,
    &quot;input&quot;: {
        &quot;prompt&quot;: &quot;一座由硬纸板和瓶盖搭建的微型城市，在夜晚焕发出生机。一列硬纸板火车缓缓驶过，小灯点缀其间，照亮前路。&quot;
    },
    &quot;parameters&quot;: {
        &quot;resolution&quot;: &quot;720P&quot;,
        &quot;ratio&quot;: &quot;16:9&quot;,
        &quot;duration&quot;: 5
    }
}'
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="hh01resp1-header-h4"></a><h4>响应参数</h4><p><strong>output</strong> <code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></td><td><a id="sec-tabs-3"></a><section><a id="成功响应"></a><section><a id="成功响应-h4"></a><h4>成功响应</h4><p>请保存 task_id，用于查询任务状态与结果。</p><a id="code-block-2"></a><pre class="language-json"><code>{
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

<a id="hh01step2-title"></a>

### 步骤2：根据任务ID查询结果

<a id="sec-tabs-4"></a>

<a id="华北2-北京-2"></a>

<a id="华北2-北京-2-h4"></a>

#### 华北2（北京）

`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="新加坡-2"></a>

<a id="新加坡-2-h4"></a>

#### 新加坡

`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="美国-弗吉尼亚-2"></a>

<a id="美国-弗吉尼亚-2-h4"></a>

#### 美国（弗吉尼亚）

`GET https://{WorkspaceId}.us-east-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="德国-法兰克福-2"></a>

<a id="德国-法兰克福-2-h4"></a>

#### 德国（法兰克福）

`GET https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

<a id="日本-东京-2"></a>

<a id="日本-东京-2-h4"></a>

#### 日本（东京）

`GET https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

> **说明**
>
> -   **轮询建议**：视频生成过程约需数分钟，建议采用**轮询**机制，并设置合理的查询间隔（如 15 秒）来获取结果。
> -   **任务状态流转**：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。
> -   **结果链接**：任务成功后返回视频链接，有效期为 **24 小时**。建议在获取链接后立即下载并转存至永久存储（如[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss)）。
> -   **task\_id 有效期**：**24小时**，超时后将无法查询结果，接口将返回任务状态为`UNKNOWN`。
> -   **RPS 限制**：查询接口默认RPS为20。如需更高频查询或事件通知，建议[配置异步任务回调](../../more-about-models/async-task-api.md)。
> -   **更多操作**：如需批量查询、取消任务等操作，请参见[管理异步任务](../../more-about-models/manage-asynchronous-tasks.md)。

<table><tbody><tr><td><a id="hh01step2-req-header-h4"></a><h4>请求参数</h4><a id="hh01step2-headers-h5"></a><h5>请求头（Headers）</h5><p><strong>Authorization</strong><code>string</code><strong>（必选）</strong></p><p>请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。</p><a id="hh01step2-path-h5"></a><h5>URL路径参数（Path parameters）</h5><p><strong>task_id</strong> <code>string</code><strong>（必选）</strong></p><p>任务ID。</p></td><td><a id="sec-tabs-5"></a><section><a id="查询任务结果"></a><section><a id="查询任务结果-h4"></a><h4>查询任务结果</h4><p>将<code>{task_id}</code>完整替换为上一步接口返回的<code>task_id</code>的值。<code>task_id</code>查询有效期为24小时，并请将<code>{WorkspaceId}</code>替换为真实的<a href="../../../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain">业务空间ID</a>。</p><a id="code-block-4"></a><pre class="language-bash"><code>curl -X GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id} \
--header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="hh01resp2-header-h4"></a><h4>响应参数</h4><p><strong>output</strong><code>object</code></p><p>任务输出信息。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong> <code>string</code></p><p>任务ID。查询有效期24小时。</p><p><strong>task_status</strong> <code>string</code></p><p>任务状态。</p><a id="accordion-枚举值-2"></a><section><p>枚举值</p><div><ul><li>PENDING：任务排队中</li><li>RUNNING：任务处理中</li><li>SUCCEEDED：任务执行成功</li><li>FAILED：任务执行失败</li><li>CANCELED：任务已取消</li><li>UNKNOWN：任务不存在或状态未知</li></ul></div></section><strong>轮询过程中的状态流转：</strong><ul><li>PENDING（排队中） → RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。</li><li>初次查询状态通常为 PENDING（排队中）或 RUNNING（处理中）。</li><li>当状态变为 SUCCEEDED 时，响应中将包含生成的视频URL。</li><li>若状态为 FAILED，请检查错误信息并重试。</li><li>若状态为 CANCELED，表示任务已取消，如需继续请重新提交任务。</li><li>若状态为 UNKNOWN，表示任务不存在或状态未知，可能在 task_id 不存在或超过 24 小时有效期后出现。</li></ul><p><strong>submit_time</strong> <code>string</code></p><p>任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>scheduled_time</strong> <code>string</code></p><p>任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>end_time</strong> <code>string</code></p><p>任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。</p><p><strong>video_url</strong><code>string</code></p><p>视频URL。仅在 task_status 为 SUCCEEDED 时返回。</p><p>链接有效期24小时，可通过此URL下载视频。视频格式为MP4（H.264 编码）。</p><p><strong>orig_prompt</strong> <code>string</code></p><p>原始输入的prompt，对应请求参数<code>prompt</code>。</p><p><strong>code</strong><code>string</code></p><p>请求失败的错误码。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p><p><strong>message</strong><code>string</code></p><p>请求失败的详细信息。请求成功时不会返回此参数，详情请参见<a href="../../preparations/error-code.md">错误码</a>。</p></div></section><p><strong>usage</strong> <code>object</code></p><p>输出信息统计，只对成功的结果计数。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>input_video_duration</strong> <code>integer</code></p><p>输入的视频的时长，单位秒。</p><p><strong>output_video_duration</strong> <code>integer</code></p><p>输出视频的时长，单位秒。</p><p><strong>duration</strong> <code>integer</code></p><p>总的视频时长，用于计费。</p><p><strong>SR</strong> <code>integer</code></p><p>输出视频的分辨率档位。</p><p><strong>ratio</strong> <code>string</code></p><p>输出视频的宽高比。</p><p><strong>video_count</strong> <code>integer</code></p><p>输出视频的数量。固定为1。</p></div></section><p><strong>request_id</strong><code>string</code></p><p>请求唯一标识。可用于请求明细溯源和问题排查。</p></td><td><a id="sec-tabs-6"></a><section><a id="任务执行成功"></a><section><a id="任务执行成功-h4"></a><h4>任务执行成功</h4><p>视频URL仅保留24小时，超时后会被自动清除，请及时保存生成的视频。</p><a id="code-block-5"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;99243b47-ec5f-9413-9993-xxxxxx&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;4673458e-28be-4a05-bf2a-xxxxxx&quot;,
        &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
        &quot;submit_time&quot;: &quot;2026-04-20 17:55:17.075&quot;,
        &quot;scheduled_time&quot;: &quot;2026-04-20 17:55:17.129&quot;,
        &quot;end_time&quot;: &quot;2026-04-20 17:56:36.658&quot;,
        &quot;orig_prompt&quot;: &quot;一座由硬纸板和瓶盖搭建的微型城市，在夜晚焕发出生机。一列硬纸板火车缓缓驶过，小灯点缀其间，照亮前路。&quot;,
        &quot;video_url&quot;: &quot;https://dashscope-result.oss-cn-beijing.aliyuncs.com/xxx.mp4?Expires=xxx&quot;
    },
    &quot;usage&quot;: {
        &quot;duration&quot;: 5,
        &quot;input_video_duration&quot;: 0,
        &quot;output_video_duration&quot;: 5,
        &quot;video_count&quot;: 1,
        &quot;SR&quot;: 720,
        &quot;ratio&quot;: &quot;16:9&quot;
    }
}
</code></pre></section><a id="任务执行失败"></a><section><a id="任务执行失败-h4"></a><h4>任务执行失败</h4><p>若任务执行失败，task_status将置为 FAILED，并提供错误码和信息。请参见<a href="../../preparations/error-code.md">错误码</a>进行解决。</p><a id="code-block-6"></a><pre class="language-json"><code>{
    &quot;request_id&quot;: &quot;e5d70b02-ebd3-98ce-9fe8-759d7d7b107d&quot;,
    &quot;output&quot;: {
        &quot;task_id&quot;: &quot;86ecf553-d340-4e21-af6e-a0c6a421c010&quot;,
        &quot;task_status&quot;: &quot;FAILED&quot;,
        &quot;code&quot;: &quot;InvalidParameter&quot;,
        &quot;message&quot;: &quot;The parameter is invalid.&quot;
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

<a id="0d0a562d05nkh"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../../preparations/error-code.md)进行解决。
