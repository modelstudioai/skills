# Paraformer非实时语音识别Python SDK

本文介绍Paraformer非实时语音识别Python SDK的参数和接口细节。

> **重要**
>
> 阿里云百炼为华北2（北京）地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
>
> `{WorkspaceId}`需要替换为真实的[Workspace ID](../model-user-guide/get-started-with-models/regions.md#h2_migrate_domain)。现有域名仍可正常使用。

**用户指南：**[非实时语音识别](../model-user-guide/model-experience/speech-and-audio/speech-recognition/non-realtime-speech-recognition-user-guide.md)

<a id="前提条件"></a>

<a id="8c73014707u4b"></a>

## 前提条件

已开通服务并[获取与配置 API Key](../model-api-reference/preparations/get-api-key.md)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

> **说明**
>
> 当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](../model-api-reference/more-about-models/generate-temporary-api-key.md)。
>
> 与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
>
> 使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

-   [安装最新版DashScope SDK](../model-api-reference/preparations/install-sdk.md)。

<a id="快速开始"></a>

<a id="15e6fc8aaeqma"></a>

## 快速开始

[核心资源（`client.audio.asr`）](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#adcb5e9bddbyq)提供了异步提交任务、同步等待任务结束和异步查询任务执行结果的接口（`transcribe`一步式 / `jobs.create`+`jobs.wait`+`jobs.fetch`分步）。可通过如下两种调用方式进行非实时语音识别：

-   异步提交任务+同步等待任务结束：提交任务后，阻塞当前线程直到任务结束并获取识别结果。
-   异步提交任务+异步查询任务执行结果：提交任务后，在需要的时候通过调用查询任务接口获取任务的执行结果。

<a id="异步提交任务-同步等待任务结束"></a>

<a id="3f0e8beb6ccng"></a>

### 异步提交任务+同步等待任务结束

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1609074871/CAEQURiBgMCvo5zjpxkiIDQyNzUwZjVjMWM3MjQ5Nzg4ODBjNDRjNzE1ZGFiOGFj4709861_20241015153444.149.svg)

1.  调用[核心资源（`client.audio.asr`）](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#adcb5e9bddbyq)（`jobs.create`/`transcribe`）并设置[请求参数](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#340f6879fci7d)。
    
    > **说明**
    >
    > -   文件转写服务对通过API提交的任务采取尽力服务原则进行处理。任务提交后将进入排队（`PENDING`）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内。任务开始处理后，语音识别将以数百倍加速完成。
    > -   每一个任务完成后，识别结果和URL下载链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。
    
2.  调用[核心资源（`client.audio.asr`）](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#adcb5e9bddbyq)（`jobs.wait`，或`transcribe`一步式）同步等待任务结束。
    
    任务的状态包括`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`。当任务处于`PENDING`或`RUNNING`状态时，`wait`接口将被阻塞。当任务处于`SUCCEEDED`或`FAILED`状态时，`wait`接口不再阻塞并返回任务的执行结果。
    
    `jobs.wait`返回终态`Job`（结构参见[响应参数](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#c4fe4e43ee4n6)）。
    

<a id="accordion-点击查看完整示例"></a>

点击查看完整示例

<a id="code-block"></a>

```python
import os
import json
import dashscope

# 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 提交录音文件识别任务并同步等待任务完成
job = client.audio.asr.transcribe(
    ['{YOUR_AUDIO_URL}'],
    model='paraformer-v2',
    parameters={'language_hints': ['zh', 'en']}  # “language_hints”只支持paraformer-v2模型
)

print(json.dumps(job.model_dump(), indent=4, ensure_ascii=False))
print('transcription done!')
```

<a id="sec-tabs"></a>

<a id="dashscope-cli"></a>

<a id="dashscope-cli-h4"></a>

#### dashscope CLI

<a id="code-block-2"></a>

```bash
# 提交录音文件识别任务
export DASHSCOPE_API_KEY="your-api-key"
# 将 {WorkspaceId} 替换为业务空间ID，cn-beijing 替换为对应地域（新加坡: ap-southeast-1, 美东: us-east-1）
export DASHSCOPE_HTTP_BASE_URL="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
dashscope transcription create -m paraformer-v2 --file-url "https://example.com/audio.mp3"
# 查询任务列表
dashscope transcription list
```

> **重要**
>
> SDK Expert 交互式助手可按自然语言完成同样的开发与排障，见
>
> [DashScope SDK Expert](../model-api-reference/preparations/dashscope-sdk-expert.md)。

完整地域表见 [Base URL 总览](../model-api-reference/preparations/base-url.md)。

<a id="异步提交任务-异步查询任务执行结果"></a>

<a id="909738567dq8d"></a>

### 异步提交任务+异步查询任务执行结果

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2609074871/CAEQURiBgMCN3qzkpxkiIGE0YmU4YTdjMWNiNzRmYjJhMjFlMWZkZmFmOWQ1NmEx4709861_20241015153444.149.svg)

1.  调用[核心资源（`client.audio.asr`）](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#adcb5e9bddbyq)（`jobs.create`/`transcribe`）并设置[请求参数](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#340f6879fci7d)。
    
    > **说明**
    >
    > -   文件转写服务对通过API提交的任务采取尽力服务原则进行处理。任务提交后将进入排队（`PENDING`）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内。任务开始处理后，语音识别将以数百倍加速完成。
    > -   每一个任务完成后，识别结果和URL下载链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。
    
2.  循环调用[核心资源（`client.audio.asr`）](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#adcb5e9bddbyq)（`jobs.fetch`）直到获取最终的任务结果。
    
    当任务状态为`SUCCEEDED`或`FAILED`时，停止轮询并处理结果。
    
    `jobs.fetch`返回`Job`（结构参见[响应参数](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#c4fe4e43ee4n6)）。
    

<a id="accordion-点击查看完整示例-2"></a>

点击查看完整示例

<a id="code-block-3"></a>

```python
import os
import json
import dashscope
# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 提交录音文件识别任务
job = client.audio.asr.jobs.create(
    model='paraformer-v2',
    file_urls=['{YOUR_AUDIO_URL}'],
    parameters={'language_hints': ['zh', 'en']}  # “language_hints”只支持paraformer-v2模型
)

# 循环查询任务直到获取最终结果
while True:
    if job.status == 'SUCCEEDED' or job.status == 'FAILED':
        break
    job = client.audio.asr.jobs.fetch(job.task_id)

print(json.dumps(job.model_dump(), indent=4, ensure_ascii=False))
print('transcription done!')
```

<a id="请求参数"></a>

<a id="340f6879fci7d"></a>

## 请求参数

请求参数通过[核心资源（`client.audio.asr`）](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#adcb5e9bddbyq)的`jobs.create`/`transcribe`方法进行设置。

> **重要**
>
> 如果多声道音频的说话人分离结果不符合预期，可尝试将音频转换为单声道后重新识别。可使用ffmpeg进行转换：`ffmpeg -i input.wav -ac 1 output_mono.wav`。

<table><thead><tr><th><strong>参数</strong></th><th><strong>类型</strong></th><th><strong>默认值</strong></th><th><strong>是否必须</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>model</p></td><td><p>str</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>指定用于音视频文件转写的Paraformer模型名。参见<a href="https://help.aliyun.com/zh/model-studio/recording-file-recognition">支持的模型</a>。</p></td></tr><tr><td><p>file_urls</p></td><td><p>list[str]</p></td><td><ul><li></li></ul></td><td><p>是</p></td><td><p>音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求仅支持1个URL。</p><p>若录音文件存储在阿里云OSS，使用SDK方式不支持使用以 oss://为前缀的临时 URL。</p></td></tr><tr><td><p>vocabulary_id</p></td><td><p>str</p></td><td><ul><li></li></ul></td><td><p>否</p></td><td><p>最新热词ID，支持最新v2系列模型并配置语种信息，此次语音识别中生效此热词ID对应的热词信息。默认不启用。使用方法请参考<a href="../model-api-reference/audio-api-directory/speech-recognition-api-reference/custom-hot-words.md">定制热词</a>。</p></td></tr><tr><td><p>channel_id</p></td><td><p>list[int]</p></td><td><p>[0]</p></td><td><p>否</p></td><td><p>指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，[0] 表示识别第一个音轨，[0, 1] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。</p><div><div><p><strong>重要</strong>指定的每一个音轨都将独立计费。例如，为单个文件请求 [0, 1] 会产生两笔独立的费用。</p></div></div></td></tr><tr><td><p>disfluency_removal_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><p>过滤语气词，默认关闭。</p></td></tr><tr><td><p>timestamp_alignment_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><p>是否启用时间戳校准功能，默认关闭。</p></td></tr><tr><td><p>special_word_filter</p></td><td><p>str</p></td><td><ul><li></li></ul></td><td><p>否</p></td><td><p>指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。</p><p>若未传入该参数，系统将启用系统内置的敏感词过滤逻辑，识别结果中与<a href="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt">阿里云百炼敏感词表</a>匹配的词语将被替换为等长的<code>*</code>。</p><p>若传入该参数，则可实现以下敏感词处理策略：</p><ul><li>替换为 <code>*</code>：将匹配的敏感词替换为等长的 <code>*</code>；</li><li>直接过滤：将匹配的敏感词从识别结果中完全移除。</li></ul><p>该参数的值应为一个 JSON 字符串，其结构如下所示：</p><a id="code-block-4"></a><pre class="language-json"><code>{
  &quot;filter_with_signed&quot;: {
    &quot;word_list&quot;: [&quot;测试&quot;]
  },
  &quot;filter_with_empty&quot;: {
    &quot;word_list&quot;: [&quot;开始&quot;, &quot;发生&quot;]
  },
  &quot;system_reserved_filter&quot;: true
}
</code></pre><p>JSON字段说明：</p><ul><li><p><code>filter_with_signed</code></p><ul><li><p>类型：对象。</p></li><li><p>是否必填：否。</p></li><li><p>描述：配置需替换为<code>*</code>的敏感词列表。识别结果中匹配的词语将被等长的 <code>*</code> 替代。</p></li><li><p>示例：以上述JSON为例，“帮我测试一下这段代码”的语音识别结果将会是“帮我**一下这段代码”。</p></li><li><p>内部字段：</p><ul><li><code>word_list</code>: 字符串数组，列出需被替换的敏感词。</li></ul></li></ul></li><li><p><code>filter_with_empty</code></p><ul><li><p>类型：对象。</p></li><li><p>是否必填：否。</p></li><li><p>描述：配置需从识别结果中移除（过滤）的敏感词列表。识别结果中匹配的词语将被完全删除。</p></li><li><p>示例：以上述JSON为例，“比赛这就要开始了吗？”的语音识别结果将会是“比赛这就要了吗”。</p></li><li><p>内部字段：</p><ul><li><code>word_list</code>: 字符串数组，列出需被完全移除（过滤）的敏感词。</li></ul></li></ul></li><li><p><code>system_reserved_filter</code></p><ul><li>类型：布尔值。</li><li>是否必填：否。</li><li>默认值：true。</li><li>描述：是否启用系统预置的敏感词规则。设为<code>true</code>时，将同时启用系统内置的敏感词过滤逻辑，识别结果中与<a href="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt">阿里云百炼敏感词表</a>匹配的词语将被替换为等长的<code>*</code>。</li></ul></li></ul></td></tr><tr><td><p>language_hints</p></td><td><p>list[str]</p></td><td><p>[&quot;zh&quot;, &quot;en&quot;]</p></td><td><p>否</p></td><td><p>指定待识别语音的语言代码。</p><p>该参数仅适用于paraformer-v2模型。</p><p>支持的语言代码：</p><ul><li>zh: 中文</li><li>en: 英文</li><li>ja: 日语</li><li>yue: 粤语</li><li>ko: 韩语</li><li>de：德语</li><li>fr：法语</li><li>ru：俄语</li></ul></td></tr><tr><td><p>diarization_enabled</p></td><td><p>bool</p></td><td><p>False</p></td><td><p>否</p></td><td><p>自动说话人分离，默认关闭。</p><p>仅适用于单声道音频，多声道音频不支持说话人分离。</p><p>启用该功能后，识别结果中将显示<code>speaker_id</code>字段，用于区分不同说话人。</p><div><div><p><strong>说明</strong>如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。</p></div></div><p>有关<code>speaker_id</code>的示例，请参见<a href="paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#a9021178ccl7s">识别结果说明</a>。</p></td></tr><tr><td><p>speaker_count</p></td><td><p>int</p></td><td><ul><li></li></ul></td><td><p>否</p></td><td><p>说话人数量参考值。取值范围为2至100的整数（包含2和100）。</p><p>开启说话人分离功能后（<code>diarization_enabled</code>设置为true）生效。</p><p>默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。</p></td></tr></tbody></table>

<a id="响应结果"></a>

<a id="daf592c1feacp"></a>

## 响应结果

<a id="job"></a>

<a id="c4fe4e43ee4n6"></a>

### `Job`

`Job`封装了任务的基本信息（`task_id`和`status`）和执行结果（`results`参见[子任务识别结果](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#3c2916848c07k)、`task_metrics`、`usage`）。`jobs.create`提交任务后返回的`Job`仅包含`task_id`与`status`；`jobs.fetch`、`jobs.wait`（以及一步式`transcribe`）返回的`Job`包含任务的执行结果。

<a id="accordion-点击查看-job-结构示例"></a>

点击查看 Job 结构示例

`jobs.create`方法返回的`Job`示例如下（任务提交后处于`PENDING`状态）：

<a id="code-block-5"></a>

```json
{
    "request_id":"251aceab-a6aa-9fc4-b7f7-0cc6d3e2a9f3",
    "task_id":"7d0a58a3-1dbe-4de9-8cff-5f48213128b0",
    "status":"PENDING"
}
```

`jobs.fetch`、`jobs.wait`（以及一步式`transcribe`）返回的`Job`示例如下：

<a id="fig-code-group"></a>

<a id="fig-code-group-pending-状态-tab"></a>

PENDING 状态

<a id="code-code-group-pending-状态"></a>

```json
{
    "request_id":"251aceab-a6aa-9fc4-b7f7-0cc6d3e2a9f3",
    "task_id":"7d0a58a3-1dbe-4de9-8cff-5f48213128b0",
    "status":"PENDING",
    "task_metrics":{
        "TOTAL":1,
        "SUCCEEDED":0,
        "FAILED":0
    }
}
```

<a id="fig-code-group-running-状态-tab"></a>

RUNNING 状态

<a id="code-code-group-running-状态"></a>

```json
{
    "request_id":"d9d530f1-853c-9848-a5f1-f5de59086ff7",
    "task_id":"6351feef-9694-45d2-9d32-63454f2ffb8d",
    "status":"RUNNING",
    "task_metrics":{
        "TOTAL":1,
        "SUCCEEDED":0,
        "FAILED":0
    }
}
```

<a id="fig-code-group-succeeded-状态-tab"></a>

SUCCEEDED 状态

<a id="code-code-group-succeeded-状态"></a>

```json
{
    "request_id":"16668704-6702-9e03-8ab7-a32a5d7bb095",
    "task_id":"6351feef-9694-45d2-9d32-63454f2ffb8d",
    "status":"SUCCEEDED",
    "results":[
        {
            "file_url":"{YOUR_AUDIO_URL}",
            "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/17%3A31/20ee4e4f-0404-4806-b617-c7d4c62eed19-1.json?Expires=1739525481&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
            "subtask_status":"SUCCEEDED"
        }
    ],
    "task_metrics":{
        "TOTAL":1,
        "SUCCEEDED":1,
        "FAILED":0
    },
    "usage":{
        "duration":9
    }
}
```

<a id="fig-code-group-failed-状态-tab"></a>

FAILED 状态

<a id="code-code-group-failed-状态"></a>

```json
{
    "request_id":"16668704-6702-9e03-8ab7-a32a5d7bb095",
    "task_id":"7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
    "status":"SUCCEEDED",
    "results":[
        {
            "file_url":"{YOUR_AUDIO_URL}",
            "code":"InvalidFile.DownloadFailed",
            "message":"The audio file cannot be downloaded.",
            "subtask_status":"FAILED"
        }
    ],
    "task_metrics":{
        "TOTAL":1,
        "SUCCEEDED":0,
        "FAILED":1
    },
    "usage":{
        "duration":9
    }
}
```

需要关注的参数：

| 参数 | 说明 |
| --- | --- |
| request\_id | 系统生成的标识本次调用的ID。 |
| task\_id | 任务ID。 |
| status | 任务状态。<br><br>有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。<br><br>当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。 |
| results | 子任务识别结果，每项包含`file_url`、`transcription_url`、`subtask_status`，参见[子任务识别结果](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#3c2916848c07k)。 |
| subtask\_status | 子任务状态。<br><br>有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。 |
| file\_url | 被识别音频的URL。 |
| transcription\_url | 音频识别结果对应的URL。<br><br>识别结果保存为JSON文件，您可以通过`transcription_url`对应的链接下载文件或直接通过HTTP请求读取该文件中的内容。JSON文件的内容请参见[识别结果说明](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#a9021178ccl7s)。 |
| usage | 计量信息，包含`duration`（音频时长，单位为秒）。 |

调用失败时，Python SDK 将抛出 DashScopeError 异常，可通过 e.code/e.status\_code/e.message/e.request\_id 获取错误码、HTTP状态码、错误信息与请求ID。子任务失败不会抛出异常，需通过`results`中的`subtask_status`、`code`、`message`判断。

<a id="results-子任务识别结果"></a>

<a id="3c2916848c07k"></a>

### `results`（子任务识别结果）

`results`数组对应`Job`中每个音频文件的子任务识别结果，每项包含`file_url`、`transcription_url`、`subtask_status`；子任务失败时还会包含`code`、`message`。

<a id="accordion-点击查看-results-结构示例"></a>

点击查看 results 结构示例

<a id="sec-tabs-2"></a>

<a id="succeeded-状态"></a>

<a id="succeeded-状态-h4"></a>

#### SUCCEEDED 状态

<a id="code-block-6"></a>

```json
{
    "file_url":"{YOUR_AUDIO_URL}",
    "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/17%3A59/70e737cc-bf8c-418b-b0c8-83fab192a0fa-1.json?Expires=1739527168&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
    "subtask_status":"SUCCEEDED"
}
```

<a id="failed-状态"></a>

<a id="failed-状态-h4"></a>

#### FAILED 状态

`code`为错误码，`message`为错误信息，只有子任务异常时才有这两个字段，您可以通过这两个字段，对照[错误码](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#c70f9758027ph)排查问题。

<a id="code-block-7"></a>

```json
{
    "file_url": "{YOUR_AUDIO_URL}",
    "code": "InvalidFile.DownloadFailed",
    "message": "The audio file cannot be downloaded.",
    "subtask_status": "FAILED"
}
```

需要关注的参数：

| 参数 | 说明 |
| --- | --- |
| code | 代表错误码。可以结合`message`字段，对照[错误码](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#c70f9758027ph)排查问题。 |
| message | 代表错误信息。可以结合`code`字段，对照[错误码](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#c70f9758027ph)排查问题。 |
| subtask\_status | 子任务状态。<br><br>有`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四种状态。 |
| file\_url | 被识别音频的URL。 |
| transcription\_url | 音频识别结果对应的URL。<br><br>识别结果以JSON格式保存在一个JSON文件中，您可以通过`transcription_url`对应的链接下载文件或直接通过HTTP请求读取该文件中的内容。JSON文件的内容请参见[识别结果说明](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#a9021178ccl7s)。 |

<a id="识别结果说明"></a>

<a id="a9021178ccl7s"></a>

### 识别结果说明

识别结果保存为JSON文件。

<a id="accordion-点击查看识别结果示例"></a>

点击查看识别结果示例

<a id="code-block-8"></a>

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
| audio\_format | string | 源文件中音频的格式。 |
| channels | array\[integer\] | 源文件中音频的音轨索引信息，对单轨音频返回\[0\]，对双轨音频返回\[0, 1\]，以此类推。 |
| original\_sampling\_rate | integer | 源文件中音频的采样率（Hz）。 |
| original\_duration | integer | 源文件中的原始音频时长（ms）。 |
| channel\_id | integer | 转写结果的音轨索引，以0为起始。 |
| content\_duration | integer | 音轨中被判定为语音内容的时长（ms）。<br><br>Paraformer语音识别模型服务仅对音轨中被判定为语音内容的时长进行语音转写，并据此进行计量计费，非语音内容不计量、不计费。通常情况下语音内容时长会短于原始音频时长。由于对是否存在语音内容的判定是由AI模型给出的，可能与实际情况存在一定误差。 |
| transcript | string | 段落级别的语音转写结果。 |
| sentences | array | 句子级别的语音转写结果。 |
| words | array | 词级别的语音转写结果。 |
| begin\_time | integer | 开始时间戳（ms）。 |
| end\_time | integer | 结束时间戳（ms）。 |
| text | string | 语音转写结果。 |
| speaker\_id | integer | 当前说话人的索引，以0为起始，用于区分不同的说话人。<br><br>仅在启用说话人分离功能时，该字段才会显示于识别结果中。 |
| punctuation | string | 预测出的词之后的标点符号（如有）。 |

<a id="关键接口"></a>

<a id="60280ef1ec77f"></a>

## 关键接口

<a id="核心资源-client-audio-asr"></a>

<a id="adcb5e9bddbyq"></a>

### 核心资源（`client.audio.asr`）

非实时语音识别能力挂载在`client.audio.asr`资源上，可通过`client.audio.asr.transcribe`一步完成提交与等待，或通过`client.audio.asr.jobs`分步控制。

<table><thead><tr><th><strong>成员方法</strong></th><th><strong>方法签名</strong></th><th><strong>说明</strong></th></tr></thead><tbody><tr><td><p>transcribe</p></td><td><a id="code-block-9"></a><pre class="language-python"><code>def transcribe(self,
               file_urls: List[str],
               *,
               model: str = &quot;paraformer-v2&quot;,
               parameters: Dict = None,
               phrase_id: str = None,
               timeout: float = ...,
               ...) -&gt; Job
</code></pre></td><td><p>提交录音文件识别任务并阻塞当前线程直到任务结束（任务状态为<code>SUCCEEDED</code>或<code>FAILED</code>）。</p><p>该方法返回<code>Job</code>，转写结果读<code>job.results</code>（每项含<code>transcription_url</code>）。</p></td></tr><tr><td><p>jobs.create</p></td><td><a id="code-block-10"></a><pre class="language-python"><code>def create(self,
           *,
           model: str,
           file_urls: List[str],
           parameters: Dict = None,
           phrase_id: str = None,
           ...) -&gt; Job
</code></pre></td><td><p>异步提交语音识别任务。</p><p>该方法返回<code>Job</code>（<code>job.task_id</code>/<code>job.status</code>）。</p></td></tr><tr><td><p>jobs.wait</p></td><td><a id="code-block-11"></a><pre class="language-python"><code>def wait(self,
         task: Union[str, Job],
         poll_interval: float = 1,
         timeout: float = 86400,
         ...) -&gt; Job
</code></pre></td><td><p>阻塞当前线程直到异步任务结束（指数退避轮询，默认总预算24小时）。</p><p>该方法返回终态<code>Job</code>。</p></td></tr><tr><td><p>jobs.fetch</p></td><td><a id="code-block-12"></a><pre class="language-python"><code>def fetch(self,
          task_id: str,
          ...) -&gt; Job
</code></pre></td><td><p>异步查询当前任务执行结果。</p><p>该方法返回<code>Job</code>。</p></td></tr></tbody></table>

<a id="其他接口-批量查询任务状态-取消任务"></a>

<a id="afbd594d9a7hx"></a>

## 其他接口：批量查询任务状态/取消任务

详情请参见[管理异步任务](../model-api-reference/more-about-models/manage-asynchronous-tasks.md)：支持批量查询24小时内提交的非实时语音识别任务，同时支持取消`PENDING`（排队）状态的任务。

<a id="错误码"></a>

<a id="c70f9758027ph"></a>

## 错误码

如遇报错问题，请参见[错误码](../model-api-reference/preparations/error-code.md)进行排查。

若问题仍未解决，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)反馈遇到的问题，并提供Request ID，以便进一步排查问题。

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

错误返回示例：

<a id="code-block-13"></a>

```json
{
    "request_id": "16668704-6702-9e03-8ab7-a32a5d7bb095",
    "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
    "status": "SUCCEEDED",
    "results": [
        {
            "file_url": "{YOUR_AUDIO_URL}",
            "code": "InvalidFile.DownloadFailed",
            "message": "The audio file cannot be downloaded.",
            "subtask_status": "FAILED"
        }
    ],
    "task_metrics": {
        "TOTAL": 1,
        "SUCCEEDED": 0,
        "FAILED": 1
    }
}
```

<a id="更多示例"></a>

<a id="4c2fd163e80k0"></a>

## 更多示例

更多示例，请参见[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

<a id="常见问题"></a>

<a id="9684d0f31d53e"></a>

## 常见问题

<a id="功能特性"></a>

<a id="ef653d0bb7ol9"></a>

### 功能特性

<a id="q-是否支持base64编码方式的音频"></a>

<a id="326a5e31a2p0m"></a>

#### Q：是否支持Base64编码方式的音频？

不支持Base64编码方式的音频。仅支持可通过公网访问的 URL 所指向的音频的识别，不支持识别二进制流，也不支持直接识别本地文件。

<a id="q-如何将音频文件以公网可访问的url形式提供"></a>

<a id="01d5f797c8ksz"></a>

#### Q：如何将音频文件以公网可访问的URL形式提供？

通常遵循以下几个步骤（这里为您提供一种思路，具体情况因不同存储产品而异，推荐将音频[上传至阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)）：

<a id="accordion-1-选择存储和托管方式"></a>

1、选择存储和托管方式

如以下这几种：

-   对象存储服务（推荐）：
    
    -   使用云服务商的对象存储服务（如[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)），将音频文件上传到存储桶中，并设置为公开访问。
    -   优点：高可用性、支持 CDN 加速、易于管理。
-   Web 服务器：
    
    -   将音频文件放置在支持 HTTP/HTTPS 访问的 Web 服务器上（如 Nginx、Apache）。
    -   优点：适合小型项目或本地测试。
-   内容分发网络（CDN）：
    
    -   将音频文件托管在 CDN 上，通过 CDN 提供的 URL 访问。
    -   优点：加速文件传输，适合高并发场景。

<a id="accordion-2-上传音频文件"></a>

2、上传音频文件

根据选择的存储/托管方式，将音频上传，如：

-   对象存储服务：
    
    -   登录云服务商的控制台，创建存储桶。
    -   上传音频文件，并设置文件权限为“公共读”或生成临时访问链接。
-   Web 服务器：
    
    -   将音频文件放置在服务器指定目录下（如 `/var/www/html/audio/`）。
    -   确保文件可以通过 HTTP/HTTPS 访问。

<a id="accordion-3-生成公网可访问的url"></a>

3、生成公网可访问的URL

例如：

-   对象存储服务：
    
    -   文件上传后，系统会自动生成一个公网访问 URL（通常格式为 `https://<bucket-name>.<region>.aliyuncs.com/<file-name>`）。
    -   如果需要更友好的域名，可以绑定自定义域名并开启 HTTPS。
-   Web 服务器：
    
    -   文件的访问 URL 通常是服务器地址加上文件路径（如 `https://your-domain.com/audio/file.mp3`）。
-   CDN：
    
    -   配置 CDN 加速后，使用 CDN 提供的 URL（如 `https://cdn.your-domain.com/audio/file.mp3`）。

<a id="accordion-4-验证url的可用性"></a>

4、验证URL的可用性

公网环境下，确保生成的 URL 可以正常访问，例如：

-   在浏览器中打开 URL，检查是否能播放音频文件。
-   使用工具（如 `curl` 或 Postman）验证 URL 是否返回正确的 HTTP 响应（状态码 200）。

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL：

> **重要**
>
> -   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
> -   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
> -   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。

<a id="q-多久能获取识别结果"></a>

<a id="33c69cf322xkf"></a>

#### Q：多久能获取识别结果？

任务提交后将进入排队（PENDING）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内，请耐心等待。并且音频时长越长，所需时间越久。

<a id="故障排查"></a>

<a id="abe43b2c2a8sq"></a>

### 故障排查

如遇代码报错问题，请根据[错误码](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#c70f9758027ph)中的信息进行排查。

<a id="q-识别结果和语音播放不同步怎么办"></a>

<a id="2cecceb3af4uc"></a>

#### Q：识别结果和语音播放不同步怎么办？

将[请求参数](paraformer-recorded-speech-recognition-python-sd-cec7d242cc0bcda0.md#340f6879fci7d)`timestamp_alignment_enabled`设为`true`将启用时间戳校准功能，能够让识别结果和语音播放同步。

<a id="q-一直轮询不到结果"></a>

<a id="ed3d52b907dbl"></a>

#### Q：一直轮询不到结果？

可能是限流原因，请耐心等待。若需扩容，请加入[开发者群](https://github.com/aliyun/alibabacloud-bailian-speech-demo)进行申请。

<a id="q-无法识别语音-无识别结果-是什么原因"></a>

<a id="88d8b9a4b6xv7"></a>

#### Q：无法识别语音（无识别结果）是什么原因？

-   请检查音频是否符合要求（格式、采样率）。
-   若是使用了`paraformer-v2`模型，检查`language_hints`的设置是否正确。
-   以上都没问题，可通过定制热词，提升对特定词语的识别效果。

<a id="q-说话人分离结果全部标记为同一个speaker怎么办"></a>

<a id="f5a8b2c3e1n6q"></a>

#### Q：说话人分离结果全部标记为同一个Speaker怎么办？

请按以下步骤排查：

1.  检查音频声道数。可使用ffprobe查看：`ffprobe -i input.wav -show_entries stream=channels -of default=noprint_wrappers=1`。
2.  如果音频为多声道，可尝试转换为单声道后重新识别：`ffmpeg -i input.wav -ac 1 output_mono.wav`。
3.  确认已设置`diarization_enabled=true`。`speaker_count`为可选参数，默认自动判断说话人数；如需设置，取值范围为2至100，但不保证结果中的说话人数与设置值一致。

<a id="更多问题"></a>

<a id="6c1d546e27vq0"></a>

### 更多问题

请参见GitHub [QA](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/docs/QA)。
