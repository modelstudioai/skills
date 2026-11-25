# Fun-ASR非实时语音识别HTTP API参考

本文介绍Fun-ASR非实时语音识别HTTP API的参数和接口细节。

关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见[音频规格](../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02)。

<a id="流程说明"></a>

<a id="4a1eca9360nd1"></a>

## 流程说明

与DashScope同步调用（一次请求、立即返回结果）不同，异步调用专为处理长音频文件或耗时较长的任务设计，该模式采用“提交-轮询”的两步式流程，避免了因长时间等待而导致的请求超时：

1.  第一步：提交任务
    
    -   客户端发起一个异步处理请求。
    -   服务器验证请求后，不会立即执行任务，而是返回一个唯一的 `task_id`，表示任务已成功创建。
2.  第二步：获取结果
    
    -   客户端使用获取到的 `task_id`，通过轮询方式反复调用结果查询接口。
    -   当任务处理完成后，结果查询接口将返回最终的识别结果。

<a id="接口地址"></a>

<a id="h2-ep"></a>

## 接口地址

<a id="sec-tabs"></a>

<a id="华北2-北京"></a>

<a id="华北2-北京-h4"></a>

#### 华北2（北京）

提交任务接口：`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`

查询任务接口：`GET https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

<a id="新加坡"></a>

<a id="新加坡-h4"></a>

#### 新加坡

提交任务接口：`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/asr/transcription`

查询任务接口：`GET https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/tasks/{task_id}`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。

> **重要**
>
> 阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：
>
> -   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
> -   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

> **重要**
>
> 使用新版域名（`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`）提交任务时，请求参数中必须包含`parameters`对象。即使无需设置任何参数，也必须传入空对象`{}`，否则任务可正常提交，但识别将失败。

<a id="请求头"></a>

<a id="h2-hd"></a>

## 请求头

| 参数 | 类型 | 是否必选 | 说明 |
| --- | --- | --- | --- |
| `Authorization` | `string` | 是 | 鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将"`<your_api_key>`"替换为实际的API Key。提交任务接口和查询任务接口均需要传入。 |
| `Content-Type` | `string` | 是 | 请求参数的媒体类型。仅提交任务接口需要传入，固定为`application/json`。 |
| `X-DashScope-Async` | `string` | 是 | 异步任务标识。仅提交任务接口需要传入，固定为`enable`，请勿遗漏，否则无法提交任务。 |

<a id="提交任务接口"></a>

<a id="418f2ac8ecxm4"></a>

## 提交任务接口

提交语音识别任务。该接口异步返回，业务侧需结合查询任务接口轮询任务状态。

<table><tbody><tr><td><a id="493b0f8f2ap0y"></a><h3>请求参数</h3><p><strong>model</strong><code>string</code><strong>（必选）</strong></p><p>模型名称。</p><p><strong>input</strong><code>object</code><strong>（必选）</strong></p><p>输入参数对象。</p><a id="accordion-属性"></a><section><p>属性</p><div><p><strong>file_urls</strong> <code>array[string]</code><strong>（必选）</strong></p><p>音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求仅支持1个URL。关于支持的音频格式、文件大小限制、时长限制等输入要求，请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md#asr_audio_spec02">音频规格</a>。</p><p>若录音文件存储在阿里云OSS，使用RESTful API方式支持使用以<code>oss://</code>为前缀的临时 URL，使用SDK方式不支持使用以 oss://为前缀的临时 URL。</p><div><div><p><strong>重要</strong></p><ul><li><p>临时 URL 有效期48小时，过期后无法使用，<strong>请勿用于生产环境。</strong></p></li><li><p>文件上传凭证接口限流为 100 QPS 且不支持扩容，<strong>请勿用于生产环境、高并发及压测场景。</strong></p></li><li><p>生产环境建议使用<a href="https://help.aliyun.com/zh/oss/user-guide/what-is-oss">阿里云OSS</a> 等稳定存储，确保文件长期可用并规避限流问题。</p></li><li><p>录音文件URL设置成OSS临时公网访问不通该如何处理？请求头中将<code>X-DashScope-OssResourceResolve</code>设为<code>enable</code>（不推荐该方式）。</p><p>SDK不支持对请求头进行配置。</p></li></ul></div></div></div></section><p><strong>parameters</strong><code>object</code>（可选）</p><p>请求参数对象。</p><div><div><p><strong>重要</strong>使用新版域名（<code>https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com</code>）时，<code>parameters</code>为必填项。即使无需设置任何参数，也必须传入空对象<code>{}</code>。若省略该字段，任务可正常提交，但查询任务结果时将返回识别失败。</p></div></div><a id="accordion-属性-2"></a><section><p>属性</p><div><p><strong>vocabulary_id</strong> <code>string</code>（可选）</p><p>预编译热词列表 ID。</p><p>需预先调用创建热词列表接口生成，识别时传入该 ID 即可使用列表中的热词。</p><p>适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_precompiled_h3">预编译热词</a>。</p><p><strong>vocabulary</strong> <code>object</code>（可选）</p><p>即时热词。以键值对形式传入，键为热词文本（<code>string</code>），值为整数权重（<code>integer</code>），无需预先创建热词列表。</p><p>使用方法请参见<a href="../model-user-guide/model-experience/speech-and-audio/speech-recognition/improve-asr-accuracy.md#hw_instant_h3">即时热词</a>。</p><p><strong>channel_id</strong> <code>array[integer]</code>（可选）</p><p>指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，[0] 表示识别第一个音轨，[0, 1] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。</p><div><div><p><strong>重要</strong>指定的每一个音轨都将独立计费。例如，为单个文件请求 [0, 1] 会产生两笔独立的费用。</p></div></div><p>默认值：[0]。</p><p><strong>special_word_filter</strong> <code>string</code>（可选）<a id="special-word-filter"></a></p><p>配置需要替换或移除的词语。参数值为 JSON 字符串，包含以下字段：</p><ul><li><code>filter_with_signed.word_list</code>：字符串数组，将匹配词替换为等长的 <code>*</code>。</li><li><code>filter_with_empty.word_list</code>：字符串数组，将匹配词从结果中移除。</li><li><code>system_reserved_filter</code>：布尔值，默认 <code>true</code>，控制是否同时使用系统预置词表；设为 <code>false</code> 时，自定义规则仍生效。</li></ul><p>未传入该参数时，使用系统内置的<a href="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt">阿里云百炼敏感词表</a>，将匹配词替换为等长的 <code>*</code>。</p><p>例如，以等长星号替换“测试”，并移除“开始”，参数值如下：</p><a id="code-block"></a><pre class="language-json"><code>{
  &quot;special_word_filter&quot;: &quot;{\&quot;filter_with_signed\&quot;:{\&quot;word_list\&quot;:[\&quot;测试\&quot;]},\&quot;filter_with_empty\&quot;:{\&quot;word_list\&quot;:[\&quot;开始\&quot;,\&quot;发生\&quot;]},\&quot;system_reserved_filter\&quot;:true}&quot;
}
</code></pre><p><strong>diarization_enabled</strong> <code>boolean</code>（可选）</p><p>是否启用说话人分离，默认关闭。</p><p>仅适用于单声道音频，多声道音频不支持说话人分离。</p><p>启用该功能后，识别结果中将显示<code>speaker_id</code>字段，用于区分不同说话人。</p><div><div><p><strong>说明</strong>如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。</p></div></div><p>有关<code>speaker_id</code>的示例，请参见识别结果说明。</p><p>默认值：false。</p><p><strong>speaker_count</strong> <code>integer</code>（可选）</p><div><div><p><strong>重要</strong>仅在开启说话人分离功能（<code>diarization_enabled</code>设置为<code>true</code>）时生效。</p></div></div><p>说话人数量参考值。取值范围为2至100的整数（包含2和100）。</p><p>默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。</p><p>无默认值。</p><p><strong>language_hints</strong> <code>array[string]</code>（可选）</p><p>设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。</p><p>最多支持设置 1 个值，超出时仅前 1 个生效。</p><a id="accordion-点击查看支持的语言代码"></a><section><p>点击查看支持的语言代码</p><div><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>ko：韩语</li><li>vi：越南语</li><li>th：泰语</li><li>id：印尼语</li><li>ms：马来语</li><li>tl：菲律宾语</li><li>hi：印地语</li><li>ar：阿拉伯语</li><li>fr：法语</li><li>de：德语</li><li>es：西班牙语</li><li>pt：葡萄牙语</li><li>ru：俄语</li><li>it：意大利语</li><li>nl：荷兰语</li><li>sv：瑞典语</li><li>da：丹麦语</li><li>fi：芬兰语</li><li>no：挪威语</li><li>el：希腊语</li><li>pl：波兰语</li><li>cs：捷克语</li><li>hu：匈牙利语</li><li>ro：罗马尼亚语</li><li>bg：保加利亚语</li><li>hr：克罗地亚语</li><li>sk：斯洛伐克语</li></ul></div></section></div></section></td><td><a id="sec-tabs-2"></a><section><a id="普通调用"></a><section><a id="普通调用-h4"></a><h4>普通调用</h4><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="code-block-2"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot; \
     --header &quot;Content-Type: application/json&quot; \
     --header &quot;X-DashScope-Async: enable&quot; \
     --data '{
    &quot;model&quot;: &quot;fun-asr&quot;,
    &quot;input&quot;: {
        &quot;file_urls&quot;: [
            &quot;{YOUR_AUDIO_URL}&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;channel_id&quot;: [0]
    }
}'
</code></pre></section><a id="即时热词"></a><section><a id="即时热词-h4"></a><h4>即时热词</h4><p>使用即时热词时格式如下：</p><a id="code-block-3"></a><pre class="language-json"><code>{
    &quot;model&quot;: &quot;fun-asr&quot;,
    &quot;input&quot;: {
        &quot;file_urls&quot;: [
            &quot;{YOUR_AUDIO_URL}&quot;
        ]
    },
    &quot;parameters&quot;: {
        &quot;vocabulary&quot;: {&quot;张三&quot;: 5, &quot;李四&quot;: 5}
    }
}
</code></pre></section></section></td></tr></tbody></table>

<table><tbody><tr><td><a id="h3-st-rs"></a><h3>响应参数</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>提交任务返回的数据。</p><a id="accordion-属性-3"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>任务ID。该ID在查询任务接口中作为<code>string</code>传入。</p><p><strong>task_status</strong><code>string</code></p><p>任务状态。提交成功时返回<code>PENDING</code>。</p></div></section></td><td><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;output&quot;: {
    &quot;task_status&quot;: &quot;PENDING&quot;,
    &quot;task_id&quot;: &quot;c2e5d63b-96e1-4607-bb91-************&quot;
  },
  &quot;request_id&quot;: &quot;77ae55ae-be17-97b8-9942--************&quot;
}
</code></pre></td></tr></tbody></table>

<a id="查询任务接口"></a>

<a id="480630e0582sb"></a>

## 查询任务接口

查询语音识别任务的执行情况和结果。建议轮询调用直至任务终态。

<table><tbody><tr><td><a id="h3-qt-rq"></a><h3>请求参数</h3><p><strong>task_id</strong><code>string</code><strong>（必选）</strong></p><div><div><p><strong>重要</strong>该参数为URL路径参数，无请求参数。</p></div></div><p>查询任务需指定其ID，该ID为提交任务接口被调用后返回的<code>task_id</code>。</p></td><td><p>以下为华北2（北京）地域的配置，调用时请将&quot;{WorkspaceId}&quot;替换为真实的业务空间ID，各地域的配置不同。</p><a id="code-block-5"></a><pre class="language-bash"><code>curl --location 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
     --header &quot;Authorization: Bearer $DASHSCOPE_API_KEY&quot;
</code></pre></td></tr></tbody></table>

<table><tbody><tr><td><a id="h3-qt-rs"></a><h3>响应参数</h3><p><strong>request_id</strong><code>string</code></p><p>本次调用的唯一标识符。</p><p><strong>output</strong><code>object</code></p><p>查询任务返回的数据。</p><a id="accordion-属性-4"></a><section><p>属性</p><div><p><strong>task_id</strong><code>string</code></p><p>被查询任务的ID。</p><p><strong>task_status</strong><code>string</code></p><p>被查询任务的状态。</p><div><div><p><strong>说明</strong>当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为<code>SUCCEEDED</code>，需通过<code>subtask_status</code>字段判断具体子任务结果。</p></div></div><p><strong>submit_time</strong><code>string</code></p><p>任务提交时间。</p><p><strong>scheduled_time</strong><code>string</code></p><p>任务被调度执行的时间。</p><p><strong>end_time</strong><code>string</code></p><p>任务结束时间。</p><p><strong>results</strong><code>array[object]</code></p><p>每个待识别音频文件对应的子任务结果列表。</p><a id="accordion-属性-5"></a><section><p>属性</p><div><p><strong>subtask_status</strong><code>string</code></p><p>子任务状态。</p><p><strong>file_url</strong><code>string</code></p><p>文件转写任务中所处理的文件URL。</p><p><strong>transcription_url</strong><code>string</code></p><p>获取识别结果对应的链接。该链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。</p><p>识别结果保存为JSON文件，您可以通过上述链接下载该文件或直接通过HTTP请求读取该文件中的内容。JSON数据中各字段含义请参见识别结果说明。</p><p><strong>code</strong><code>string</code></p><div><div><p><strong>重要</strong>仅当子任务失败时返回。</p></div></div><p>子任务失败的错误码。</p><p><strong>message</strong><code>string</code></p><div><div><p><strong>重要</strong>仅当子任务失败时返回。</p></div></div><p>子任务失败的错误信息。</p></div></section><p><strong>task_metrics</strong><code>object</code></p><p>任务整体执行情况统计。</p><a id="accordion-属性-6"></a><section><p>属性</p><div><p><strong>TOTAL</strong><code>integer</code></p><p>子任务总数。</p><p><strong>SUCCEEDED</strong><code>integer</code></p><p>成功的子任务数。</p><p><strong>FAILED</strong><code>integer</code></p><p>失败的子任务数。</p></div></section></div></section></td><td><a id="fig-code-group"></a><div><a id="fig-code-group-正常示例-tab"></a>正常示例<div><a id="code-code-group-正常示例"></a><pre class="language-json"><code>{
  &quot;request_id&quot;: &quot;f9e1afad-94d3-997e-a83b-************&quot;,
  &quot;output&quot;: {
    &quot;task_id&quot;: &quot;f86ec806-4d73-485f-a24f-************&quot;,
    &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
    &quot;submit_time&quot;: &quot;2024-09-12 15:11:40.041&quot;,
    &quot;scheduled_time&quot;: &quot;2024-09-12 15:11:40.071&quot;,
    &quot;end_time&quot;: &quot;2024-09-12 15:11:40.903&quot;,
    &quot;results&quot;: [
      {
        &quot;file_url&quot;: &quot;{YOUR_AUDIO_URL}&quot;,
        &quot;transcription_url&quot;: &quot;https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/filetrans-16k/20240912/15%3A11/409a4b92-445b-4dd8-8c1d-f110954d82d8-1.json?Expires=1726211500&amp;OSSAccessKeyId=YOUR_ACCESS_KEY_ID&amp;Signature=YOUR_SIGNATURE&quot;,
        &quot;subtask_status&quot;: &quot;SUCCEEDED&quot;
      }
    ],
    &quot;task_metrics&quot;: {
      &quot;TOTAL&quot;: 1,
      &quot;SUCCEEDED&quot;: 1,
      &quot;FAILED&quot;: 0
    }
  },
  &quot;usage&quot;: {
    &quot;duration&quot;: 9
  }
}
</code></pre></div><a id="fig-code-group-异常示例-tab"></a>异常示例<div><a id="code-code-group-异常示例"></a><pre class="language-json"><code>{
    &quot;task_id&quot;: &quot;7bac899c-06ec-4a79-8875-xxxxxxxxxxxx&quot;,
    &quot;task_status&quot;: &quot;SUCCEEDED&quot;,
    &quot;submit_time&quot;: &quot;2024-12-16 16:30:59.170&quot;,
    &quot;scheduled_time&quot;: &quot;2024-12-16 16:30:59.204&quot;,
    &quot;end_time&quot;: &quot;2024-12-16 16:31:02.375&quot;,
    &quot;results&quot;: [
        {
            &quot;file_url&quot;: &quot;{YOUR_AUDIO_URL}&quot;,
            &quot;code&quot;: &quot;FILE_DOWNLOAD_FAILED&quot;,
            &quot;message&quot;: &quot;FILE_DOWNLOAD_FAILED&quot;,
            &quot;subtask_status&quot;: &quot;FAILED&quot;
        }
    ],
    &quot;task_metrics&quot;: {
        &quot;TOTAL&quot;: 1,
        &quot;SUCCEEDED&quot;: 0,
        &quot;FAILED&quot;: 1
    }
}
</code></pre></div></div></td></tr></tbody></table>

<a id="其他接口-批量查询任务状态-取消任务"></a>

<a id="012da710f6a6e"></a>

## 其他接口：批量查询任务状态/取消任务

详情请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)：支持批量查询24小时内提交的非实时语音识别任务，同时支持取消`PENDING`（排队）状态的任务。

<a id="识别结果说明"></a>

<a id="5882b67243tcg"></a>

## 识别结果说明

识别结果保存为JSON文件。

<a id="code-block-6"></a>

```json
{
    "file_url":"{YOUR_AUDIO_URL}",
    "properties":{
        "audio_format":"pcm_s16le",
        "channels":[
            0
        ],
        "original_sampling_rate":16000,
        "original_duration_in_milliseconds":3834
    },
    "transcripts":[
        {
            "channel_id":0,
            "content_duration_in_milliseconds":3720,
            "text":"Hello world, 这里是阿里巴巴语音实验室。",
            "sentences":[
                {
                    "begin_time":100,
                    "end_time":3820,
                    "text":"Hello world, 这里是阿里巴巴语音实验室。",
                    "sentence_id":1,
                    "speaker_id":0, //当开启自动说话人分离功能时才会显示该字段
                    "words":[
                        {
                            "begin_time":100,
                            "end_time":596,
                            "text":"Hello ",
                            "punctuation":""
                        },
                        {
                            "begin_time":596,
                            "end_time":844,
                            "text":"world",
                            "punctuation":", "
                        }
                        // 这里省略其它内容
                    ]
                }
            ]
        }
    ]
}
```

需要关注的参数如下：

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| `audio_format` | `string` | 源文件中音频的格式。 |
| `channels` | array\[integer\] | 源文件中音频的音轨索引信息，对单轨音频返回\[0\]，对双轨音频返回\[0, 1\]，以此类推。 |
| `original_sampling_rate` | `integer` | 源文件中音频的采样率（Hz）。 |
| `original_duration_in_milliseconds` | `integer` | 源文件中的原始音频时长（ms）。 |
| `channel_id` | `integer` | 转写结果的音轨索引，以0为起始。 |
| `content_duration` | `integer` | 音轨中被判定为语音内容的时长（ms）。<br><br>语音识别模型服务仅对音轨中被判定为语音内容的时长进行语音转写，并据此进行计量计费，非语音内容不计量、不计费。通常情况下语音内容时长会短于原始音频时长。由于对是否存在语音内容的判定是由AI模型给出的，可能与实际情况存在一定误差。 |
| `transcript` | `string` | 段落级别的语音转写结果。 |
| `sentences` | `array` | 句子级别的语音转写结果。 |
| `words` | `array` | 词级别的语音转写结果。 |
| `begin_time` | `integer` | 开始时间戳（ms）。 |
| `end_time` | `integer` | 结束时间戳（ms）。 |
| `text` | `string` | 语音转写结果。 |
| `speaker_id` | `integer` | 当前说话人的索引，以0为起始，用于区分不同的说话人。<br><br>仅在启用说话人分离功能时，该字段才会显示于识别结果中。 |
| `punctuation` | `string` | 预测出的词之后的标点符号（如有）。 |
