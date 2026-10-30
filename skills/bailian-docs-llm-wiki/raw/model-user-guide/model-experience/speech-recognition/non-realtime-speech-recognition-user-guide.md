# 非实时语音识别

非实时语音识别模型能将录制好的音频转换为文本，支持多语言识别、歌唱识别、噪声拒识、说话人分离等功能，适用于会议转写、通话分析、字幕生成等场景。

## 概述

通过异步任务对录制好的音视频文件进行批量转写。

-   支持上下文增强，通过配置上下文提高识别准确率
-   支持自定义热词，通过预设词表提升专有名词识别准确率
-   支持说话人分离、敏感词过滤、句子/词语级时间戳等可配置功能
-   支持单个时长不超过 12 小时、体积不超过 2GB 的音频文件异步转写
-   支持任意采样率，兼容 aac、wav、mp3 等多种主流音视频格式

实时场景（直播字幕、在线会议、语音助手等）可使用[实时语音识别](raw/model-user-guide/model-experience/speech-recognition/real-time-speech-recognition-user-guide.md)。各模型选型建议请参见[语音识别](raw/model-user-guide/model-experience/speech-recognition/asr-model.md)。

## 前提条件

-   已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并将其[配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   如果通过 DashScope SDK 调用，需要[安装最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 快速开始

**重要**以下示例使用 `qwen-audio-3.1-asr-flash-filetrans` 和 `qwen-audio-3.1-asr-flash`。前者采用异步调用，提交请求时需设置 `X-DashScope-Async: enable`，然后查询任务结果；后者采用同步调用，支持流式或非流式返回结果。

如果您调用**独享部署**的模型服务时收到报错 `current user api does not support asynchronous calls`，表示该部署仅支持**同步调用**，请将请求头改为 `X-DashScope-Async: disable`（其余调用方式保持不变）。

#### Qwen-Audio-ASR-Filetrans

音视频文件较大，文件转写 API 采用异步调用：提交任务后通过查询接口轮询状态，任务完成后获取识别结果。

#### cURL

使用 cURL 调用时，先提交任务获取 `task_id`，再通过该 ID 查询任务执行结果。

#### 提交任务

以下为华北2（北京）地域的配置，调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，各地域的配置不同。

```
curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/transcription' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-Async: enable" \
-d '{
    "model": "qwen-audio-3.1-asr-flash-filetrans",
    "input": {
        "file_urls": [
            "{YOUR_AUDIO_URL}"
        ]
    },
    "parameters": {
        "channel_id": [0],
        "language_hints": ["zh", "en"]
    }
}'
```

#### 获取任务执行结果

此查询接口默认 20 QPS、最高可扩容到 100 QPS。如需更高频次或避免轮询限流，建议配置异步任务回调（参见 [高并发场景：使用回调替代轮询](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_callback_h3)）。

以下为华北2（北京）地域的配置，调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，各地域的配置不同。

```
curl -X GET 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json"
```

#### 下载识别结果

任务成功后，查询接口返回的 `output.results[].transcription_url` 指向公网可下载的 JSON 文件，包含完整识别结果。该 URL 默认在 **24 小时**内有效，请及时下载并落盘保存。

```
# 将 {transcription_url} 替换为查询接口返回的 transcription_url 值
curl -sS '{transcription_url}' -o transcription.json
cat transcription.json | jq .
```

#### Python

```
import os
import json
import dashscope
from urllib import request

# 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
client = dashscope.Client(
    # 若没有将API Key配置到环境变量中，请将下行替换为自己的API Key：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",
    region="cn-beijing",
)

# 提交录音文件识别任务并同步等待任务完成
job = client.audio.asr.transcribe(
    ['{YOUR_AUDIO_URL}'],
    model='qwen-audio-3.1-asr-flash-filetrans',
    # language_hints为可选参数，用于指定待识别音频的语言代码。取值范围请参见API参考文档。
    parameters={'language_hints': ['zh', 'en']},
)

for result in job.results:
    if result.subtask_status == 'SUCCEEDED':
        url = result.transcription_url
        transcription = json.loads(request.urlopen(url).read().decode('utf8'))
        print(json.dumps(transcription, indent=4,
                        ensure_ascii=False))
    else:
        print('transcription failed!')
        print(result)
```

#### Java

```
import com.alibaba.dashscope.audio.asr.transcription.*;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Arrays;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        // 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
        // 创建转写请求参数。
        TranscriptionParam param =
                TranscriptionParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model("qwen-audio-3.1-asr-flash-filetrans")
                        // language_hints为可选参数，用于指定待识别音频的语言代码。取值范围请参见API参考文档。
                        .parameter("language_hints", new String[]{"zh", "en"})
                        .fileUrls(
                                Arrays.asList(
                                        "{YOUR_AUDIO_URL}"))
                        .build();
        try {
            Transcription transcription = new Transcription();
            // 提交转写请求
            TranscriptionResult result = transcription.asyncCall(param);
            System.out.println("RequestId: " + result.getRequestId());
            // 检查任务是否提交成功
            if (result.getTaskId() == null) {
                System.out.println("Error: " + result.getOutput());
                System.exit(1);
            }
            // 阻塞等待任务完成并获取结果
            result = transcription.wait(
                    TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            // 获取转写结果
            List<TranscriptionTaskResult> taskResultList = result.getResults();
            if (taskResultList != null && taskResultList.size() > 0) {
                for (TranscriptionTaskResult taskResult : taskResultList) {
                    String transcriptionUrl = taskResult.getTranscriptionUrl();
                    HttpURLConnection connection =
                            (HttpURLConnection) new URL(transcriptionUrl).openConnection();
                    connection.setRequestMethod("GET");
                    connection.connect();
                    BufferedReader reader =
                            new BufferedReader(new InputStreamReader(connection.getInputStream()));
                    Gson gson = new GsonBuilder().setPrettyPrinting().create();
                    JsonElement jsonResult = gson.fromJson(reader, JsonObject.class);
                    System.out.println(gson.toJson(jsonResult));
                }
            }
        } catch (Exception e) {
            System.out.println("error: " + e);
        }
        System.exit(0);
    }
}
```

完整的识别结果会以JSON格式打印在控制台。完整结果包含转换后的文本以及文本在音视频文件中的起始、结束时间（以毫秒为单位）。

-   识别结果

```
{
    "file_url": "{YOUR_AUDIO_URL}",
    "properties": {
        "audio_format": "pcm_s16le",
        "channels": [
            0
        ],
        "original_sampling_rate": 16000,
        "original_duration_in_milliseconds": 3834
    },
    "transcripts": [
        {
            "channel_id": 0,
            "content_duration_in_milliseconds": 2480,
            "text": "Hello World，这里是阿里巴巴语音实验室。",
            "sentences": [
                {
                    "begin_time": 760,
                    "end_time": 3240,
                    "text": "Hello World，这里是阿里巴巴语音实验室。",
                    "sentence_id": 1,
                    "words": [
                        {
                            "begin_time": 760,
                            "end_time": 1000,
                            "text": "Hello",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 1000,
                            "end_time": 1120,
                            "text": " World",
                            "punctuation": "，"
                        },
                        {
                            "begin_time": 1400,
                            "end_time": 1920,
                            "text": "这里是",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 1920,
                            "end_time": 2520,
                            "text": "阿里巴巴",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 2520,
                            "end_time": 2840,
                            "text": "语音",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 2840,
                            "end_time": 3240,
                            "text": "实验室",
                            "punctuation": "。"
                        }
                    ]
                }
            ]
        }
    ]
}
```

#### Qwen-Audio-ASR

Qwen-Audio-ASR 系列模型支持同步调用，适用于 5 分钟以内的音频文件，可流式或非流式返回识别结果。

以下为华北2（北京）地域的配置，调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，各地域的配置不同。

```
curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: disable" \
     --data '{
    "model": "qwen-audio-3.1-asr-flash",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "{YOUR_AUDIO_URL}"
                        }
                    }
                ]
            }
        ]
    },
    "parameters": {
        "format": "wav",
        "sample_rate": "16000"
    }
}'
```

**重要**`qwen-audio-3.1-asr-flash` 的 HTTP 响应不包含 `choices` 字段，识别结果结构如下：

```
{
  "output": {
    "sentence": {
      "text": "识别文本内容"
    },
    "text": "识别文本内容"
  },
  "request_id": "..."
}
```

识别文本位于 `output.sentence.text` 和 `output.text`。

## 进阶功能

### 长音频文件处理

非实时语音识别支持长音频文件异步转写，适用于会议记录、访谈整理、通话回放等场景。

**限制说明：**

-   **Qwen-Audio-ASR-Filetrans**/**Fun-ASR / Qwen3-ASR-Filetrans / Paraformer：**单个音频文件大小不超过 2GB，时长不超过 12 小时。
-   **Qwen-Audio-ASR、Fun-ASR-Flash：**单个音频文件大小不超过 2GB，时长不超过 5 分钟。
-   **Qwen3-ASR-Flash：**单个音频文件大小不超过 10MB，时长不超过 5 分钟。对于较长音频，请使用 Qwen-Audio-ASR-Filetrans。
-   **启用说话人分离时**：建议音频时长不超过 2 小时，否则可能导致识别失败或超时。详见[说话人分离](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_diarization_h3)。

**调用方式**：长音频转写采用异步任务模式，分三步：

1.  提交转写任务，获取 `task_id`。
2.  通过轮询接口查询任务状态（或使用 SDK 的等待方法阻塞等待）。
3.  任务完成后从返回的 URL 下载识别结果 JSON。

具体代码示例请参见[Qwen-Audio-ASR-Filetrans](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)的快速开始代码。

### 流式输出

Qwen-Audio-ASR/Fun-ASR-Flash/Qwen3-ASR-Flash 支持流式输出：边识别边返回中间结果，适用于需要实时反馈进度的场景。 Qwen-Audio-ASR 和 Fun-ASR-Flash 的 HTTP SSE 调用方式及返回结构，请参见[Qwen-Audio-ASR HTTP API](raw/_short/qwen-audio-asr-http-api-b304ee1b83ae18cd.md)和[Fun-ASR-Flash HTTP API](raw/_short/fun-asr-flash-recorded-speech-recognition-http-a-ba2d322512e386cb.md)。

Qwen-Audio-ASR-Filetrans、Fun-ASR、Qwen3-ASR-Filetrans、Paraformer 等异步转写模型不支持流式输出，需通过任务轮询获取最终结果（详见[长音频文件处理](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_longaudio_h3)）。

**启用方式：**

-   DashScope Python SDK：设置 `stream` 参数为 `True`。
-   DashScope Java SDK：通过 `streamCall` 接口调用。
-   DashScope HTTP：在 Header 中设置 `X-DashScope-SSE` 为 `enable`。

### 使用热词提升准确率

支持通过热词提升特定领域专有名词（人名、地名、产品名等）的识别准确率。详细的创建和使用方法，请参见[提升识别准确率](raw/model-user-guide/model-experience/speech-recognition/improve-asr-accuracy.md)。

不同 SDK 暴露上述参数的命名习惯不同（如字典 key、对象属性、方法等），完整字段对照请参见各 SDK 的 API 参考。

### 使用上下文增强提升准确率

支持上下文增强功能，可将对话历史传入 ASR 模型，显著提升专有词汇的转写准确率。详细的使用方法和效果示例，请参见[上下文增强](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_enhance_h2)。

### 说话人分离

`qwen-audio-3.1-asr-flash` 使用 `speaker_diarization_enabled` 开启说话人分离，其参数和返回结构请参见 [HTTP API](raw/_short/qwen-audio-asr-http-api-b304ee1b83ae18cd.md)。

说话人分离可自动识别音频中不同说话人，并在转写结果中为每个句子标注说话人标签，适用于多人会议、访谈录音等场景。

**以下配置及示例适用于：**Qwen-Audio-ASR-Filetrans、Fun-ASR 和 Paraformer 系列模型。

**启用方式：**在 API 请求参数中设置 `diarization_enabled` 为 `true`。识别结果中每个句子会包含 `speaker_id` 字段，标识不同说话人。

返回结构示例（节选）：

```
{
  "transcripts": [
    {
      "sentences": [
        { "begin_time": 100, "end_time": 3820, "text": "你好，我们今天讨论项目进度。", "speaker_id": 0 },
        { "begin_time": 3820, "end_time": 6500, "text": "好的，我先汇报一下。", "speaker_id": 1 }
      ]
    }
  ]
}
```

不同 SDK 暴露上述字段的命名习惯不同（如字典 key、对象属性、方法等），完整字段对照请参见各 SDK 的 API 参考。

**重要**启用说话人分离功能时，建议音频时长不超过 2 小时，否则可能导致识别失败或超时（不启用时音频长度限制详见[长音频文件处理](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_longaudio_h3)）。说话人分离仅支持单声道音频。

完整字段定义请参见API参考。

### 敏感词过滤

敏感词过滤可对识别结果中的敏感词执行替换或移除，适用于客服质检、内容合规、字幕审核等场景。

**支持范围：**Qwen-Audio-ASR-Filetrans、Fun-ASR 与 Paraformer 系列模型。

**默认行为**：未传入 `special_word_filter` 参数时，系统启用内置的[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)，匹配的词语会被替换为等长的 `*`。

**自定义配置**：`special_word_filter` 是 JSON 对象，包含三个子字段：

-   `filter_with_signed.word_list`：字符串数组，列出需要被替换为等长 `*` 的敏感词。例如 `["测试"]`，「帮我测试一下」会变成「帮我\*\*一下」。
-   `filter_with_empty.word_list`：字符串数组，列出需要从结果中完全移除的敏感词。例如 `["开始"]`，「比赛这就要开始了吗」会变成「比赛这就要了吗」。
-   `system_reserved_filter`：布尔值，默认 `true`。是否同时启用系统预置敏感词表（与自定义词表叠加生效）。

配置示例：

```
{
  "special_word_filter": {
    "filter_with_signed": {
      "word_list": ["测试"]
    },
    "filter_with_empty": {
      "word_list": ["开始", "发生"]
    },
    "system_reserved_filter": true
  }
}
```

不同 SDK 暴露上述参数的命名习惯不同（如字典 key、对象属性、方法等），完整字段对照请参见 API参考。

### 获取时间戳

Flash 流式结果的时间戳稳定条件及字段路径请参见 [Qwen-Audio-ASR HTTP API](https://help.aliyun.com/zh/model-studio/qwen-audio-asr-http-api#h-fl-stream-logic)和[Fun-ASR-Flash HTTP API](https://help.aliyun.com/zh/model-studio/fun-asr-flash-recorded-speech-recognition-http-api#h-fl-stream-logic)。

非实时语音识别支持在转写结果中输出时间戳，便于字幕生成、关键词高亮、音视频剪辑等场景。Qwen-Audio-ASR-Filetrans、Qwen-Audio-ASR、Fun-ASR、Fun-ASR-Flash、Qwen3-ASR-Filetrans、Paraformer 均支持，但各模型的时间戳默认行为和控制方式不同：

-   **Qwen-Audio-ASR-Filetrans/Qwen-Audio-ASR/Fun-ASR/Fun-ASR-Flash/Paraformer**：时间戳功能固定开启，不可关闭。
-   **Qwen3-ASR-Filetrans**：仅 DashScope 异步调用方式支持时间戳，时间戳功能固定开启。可通过请求参数 `enable_words` 控制时间戳级别：设为 `false`（默认）返回句级时间戳，设为 `true` 返回字级时间戳。字级别时间戳仅支持以下语种：中文、英语、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语、俄语，其他语种可能无法保证准确性。

时间戳单位均为毫秒，分两个层级返回：

-   **句级**：`sentences[].begin_time` 与 `sentences[].end_time`，标识每个句子在音频中的起止时刻。
-   **字级**：`sentences[].words[]` 数组，每个元素包含 `begin_time`、`end_time` 与 `text`（该字/词文本）。

返回结构示例（DashScope 异步任务接口节选）：

```
{
  "transcripts": [{
    "sentences": [{
      "begin_time": 100,
      "end_time": 3820,
      "text": "你好，我们今天讨论项目进度。",
      "words": [
        { "begin_time": 100, "end_time": 596, "text": "你好" },
        { "begin_time": 596, "end_time": 844, "text": "我们" }
      ]
    }]
  }]
}
```

**重要**音频内时间戳是毫秒整数（如 `100`），与任务级 `end_time`（任务完成时间，字符串日期如 `"2024-09-12 15:11:40.903"`）不是同一字段，请勿混淆。

不同 SDK 暴露上述字段的命名习惯不同（如字典 key、对象属性、方法等），完整字段对照请参见 API参考。

## 应用于生产环境

将非实时语音识别应用于生产环境时，以下最佳实践有助于提升识别效果和系统稳定性。

### 高并发场景：使用回调替代轮询

异步转写任务（Qwen-Audio-ASR-Filetrans、Fun-ASR、Qwen3-ASR-Filetrans、Paraformer）通过 `POST /api/v1/services/audio/asr/transcription` 提交后，通常做法是周期性调用查询接口 `GET /api/v1/tasks/{task_id}` 获取结果。**该查询接口默认 20 QPS、最高可扩容至 100 QPS，在高并发批量场景下，频繁轮询易触发限流。**

通过事件总线 EventBridge 配置回调通知，任务完成时阿里云百炼会自动推送 `dashscope:System:AsyncTaskFinish` 事件至您配置的目标（HTTP/HTTPS 端点或 RocketMQ Topic），消费端收到事件后无需再调用查询接口，从而规避因频繁轮询而被限流的风险。详情请参见[配置 EventBridge 回调通知](raw/model-api-reference/more-about-models/async-task-api.md)。

#### 适用模型

-   **适用模型：**Qwen-Audio-ASR-Filetrans、Fun-ASR、Qwen3-ASR-Filetrans、Paraformer（均为异步转写任务）。
-   **不适用：**Qwen3-ASR-Flash（同步/流式调用，不属异步任务范畴）。

#### 回调消息内容

三种模型的回调消息体中 `data.contain_result` 均为 `true`，`data.output_result` 直接携带 `transcription_url`，消费端收到回调后即可获取识别结果，无需再调用 `GET /api/v1/tasks/{task_id}`。但三个模型的结果字段路径与结构不同，详见下表。

**说明**编写消费端时请按使用的模型选择正确路径，不可写死为单一路径。失败场景下 `data.output_result.output` 不再含 `results`/`result`，而是含 `code` 与 `message` 字段，需先判断 `data.task_status` 再取结果。

**模型**

**提交参数**

**结果字段路径（基于回调 Body）**

**usage 字段**

Qwen-Audio-ASR-Filetrans、Fun-ASR

`input.file_urls`（数组，单次仅支持 1 个 URL）

`data.output_result.output.results[ ].transcription_url`（数组，每个文件一项，含 `subtask_status`；并附 `task_metrics`）

`duration`

Paraformer

`input.file_urls`（数组，单次仅支持 1 个 URL）

同 Qwen-Audio-ASR-Filetrans/Fun-ASR：`data.output_result.output.results[ ].transcription_url`

`duration`

Qwen3-ASR-Filetrans

`input.file_url`（**单对象**，单次仅支持 1 个 URL）

`data.output_result.output.result.transcription_url`（**单对象**，无 `results[ ]` / `task_metrics`）

`seconds`

#### 注意事项

**安全（HTTP/HTTPS 投递方式）：**生产环境必须校验回调请求头中的 `X-Eventbridge-Signature*` 系列字段后再消费，否则任意外部 IP 都可伪造 `AsyncTaskFinish` 事件，注入虚假识别结果。建议同时为接收端设置至少 5 秒的接收超时。RocketMQ 投递方式无消息级签名，安全性由 RocketMQ 鉴权机制保证。

**投递延迟：**从任务结束（`end_time`）到投递目标（HTTP/HTTPS 端点或 RocketMQ Topic）收到消息，通常约 1–90 秒，具体延迟受 EventBridge 实时负载影响。

**幂等性：**同一事件可能因重试而被投递多次。消费端需实现幂等处理，建议以 CloudEvents `data.id` 或 `data.task_id` 作为去重键。

### 生产环境建议

-   **文件托管：**将音频文件上传至[阿里云 OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，通过 URL 方式调用，避免使用本地文件上传（本地文件调用上限 100 QPS，不支持扩容）。
-   **异步轮询：**长音频转写采用异步模式，建议设置合理的轮询间隔（如 2~5 秒），避免频繁查询消耗配额。如需突破 20–100 QPS 查询上限，可改用事件回调通知，详见[高并发场景：使用回调替代轮询](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#nrt03_callback_h3)。
-   **错误处理：**实现完善的重试机制；网络超时或服务端临时错误（5xx）按指数退避策略重试。
-   **降噪处理：**噪声较大的音频建议先用 FFmpeg 等工具预处理后再提交识别。
-   **模型选择：**5 分钟以内的短音频使用 Qwen-Audio-ASR；长音频或需要异步处理时使用 Qwen-Audio-ASR-Filetrans。

## 支持的模型与地域

#### 华北2（北京）

调用以下模型时，请选择北京地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-ASR-Filetrans：**`qwen-audio-3.1-asr-flash-filetrans`、`qwen-audio-3.0-asr-flash-filetrans`
-   **Qwen-Audio-ASR：**`qwen-audio-3.1-asr-flash`、`qwen-audio-3.0-asr-flash`
-   **Fun-ASR：**`fun-asr`（稳定版）
-   **Fun-ASR-Flash：**`fun-asr-flash-2026-06-15`
-   **Qwen3-ASR-Filetrans：**`qwen3-asr-flash-filetrans`（稳定版）
-   **Qwen3-ASR-Flash：**`qwen3-asr-flash`（稳定版）
-   **Paraformer：**`paraformer-v2`、`paraformer-8k-v2`

#### 新加坡

调用以下模型时，请选择新加坡地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)：

-   **Qwen-Audio-ASR-Filetrans：**`qwen-audio-3.1-asr-flash-filetrans`、`qwen-audio-3.0-asr-flash-filetrans`
-   **Qwen-Audio-ASR：**`qwen-audio-3.1-asr-flash`、`qwen-audio-3.0-asr-flash`
-   **Fun-ASR：**`fun-asr`（稳定版）
-   **Fun-ASR-Flash：**`fun-asr-flash-2026-06-15`
-   **Qwen3-ASR-Filetrans：**`qwen3-asr-flash-filetrans`（稳定版）
-   **Qwen3-ASR-Flash：**`qwen3-asr-flash`（稳定版）

#### 美国（弗吉尼亚）

调用以下模型时，请选择美国地域的[API Key](https://bailian.console.aliyun.com/us-east-1/model/settings/api-key)：

**Qwen3-ASR-Flash：**`qwen3-asr-flash`（稳定版）

## API参考

-   [非实时语音识别-Qwen-Audio-ASR-Filetrans API参考](raw/_short/qwen-audio-asr-filetrans-api-c91600a5bccc788c.md)
-   [非实时语音识别-Fun-ASR API参考](raw/_short/fun-asr-recorded-speech-recognition-api-referenc-cdd1d2e565f281cc.md)
-   [非实时语音识别-Qwen-Audio-ASR API参考](raw/_short/qwen-audio-asr-api-12cd76f68a22ae50.md)
-   [非实时语音识别-Fun-ASR-Flash API参考](raw/_short/non-real-time-speech-recognition-for-fun-asr-fla-a39568e6f8404553.md)
-   [非实时语音识别-Qwen-ASR API参考](raw/_short/qwen-asr-api-reference-60b7c9eb88d7f83b.md)
-   [非实时语音识别-Paraformer API参考](raw/_short/paraformer-recorded-speech-recognition-api-refer-8ca94e9578cc12b7.md)

## 常见问题

### Q：如何为API提供公网可访问的音频URL？

推荐使用[阿里云对象存储OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，它提供了高可用、高可靠的存储服务，并且可以方便地生成公网访问URL。

**在公网环境下验证生成的 URL 可正常访问：**可在浏览器或通过 curl 命令访问该 URL，确保音频文件能够成功下载或播放（HTTP状态码为200）。

### Q：如何检查音频格式是否符合要求？

可以使用开源工具[ffprobe](https://ffmpeg.org/ffprobe.html)快速获取音频的详细信息：

```
# 查询音频的容器格式(format_name)、编码(codec_name)、采样率(sample_rate)、声道数(channels)
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 your_audio_file.mp3
```

### Q：如何处理音频以满足模型要求？

可以使用开源工具[FFmpeg](https://ffmpeg.org/download.html)对音频进行裁剪或格式转换：

-   **音频裁剪：从长音频中截取片段**

```
# -i: 输入文件
# -ss 00:01:30: 设置裁剪的起始时间 (从1分30秒开始)
# -t 00:02:00: 设置裁剪的持续时长 (裁剪2分钟)
# -c copy: 直接复制音频流，不重新编码，速度快
# output_clip.wav: 输出文件
ffmpeg -i long_audio.wav -ss 00:01:30 -t 00:02:00 -c copy output_clip.wav
```

-   **格式转换**
    
    例如，将任意音频转换为16kHz、16-bit、单声道WAV文件
    

```
# -i: 输入文件
# -ac 1: 设置声道数为1 (单声道)
# -ar 16000: 设置采样率为16000Hz (16kHz)
# -sample_fmt s16: 设置采样格式为16-bit signed integer PCM
# output.wav: 输出文件
ffmpeg -i input.mp3 -ac 1 -ar 16000 -sample_fmt s16 output.wav
```

### Q：如何提升识别准确率？

以下因素影响识别准确率，请逐项排查并针对性优化。

主要影响因素：

1.  声音质量：录音设备品质、采样率及环境噪声直接影响音频清晰度，高质量音频输入是准确识别的基础
2.  说话人特征：音调、语速、口音和方言差异（尤其少见方言或重口音）增加识别难度
3.  语言和词汇：多语言混合、专业术语或俚语增加识别难度，可通过配置热词优化特定领域术语的准确率

优化方法：

1.  优化音频质量：使用高性能麦克风，按推荐采样率录音，尽量减少环境噪声与回声
2.  适配说话人：对于口音较重或方言明显的音频，选用支持对应方言的模型
3.  配置热词：为专业术语、专有名词等设置热词

## 模型应用上架及备案

参见[应用合规备案](raw/_short/compliance-and-launch-filing-guide-for-ai-apps-p-d8d98ba3cff2bf6f.md)。
